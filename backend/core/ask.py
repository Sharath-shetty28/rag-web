#!/usr/bin/env python3
# ask.py — retrieve + generate grounded answer

import os
import time
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from dotenv import load_dotenv
import re

load_dotenv()  # automatically load .env variables


def load_index(index_dir="data/index"):
    try:
        index = faiss.read_index(os.path.join(index_dir, "index.faiss"))
        texts = np.load(os.path.join(index_dir, "texts.npy"), allow_pickle=True)
        with open(os.path.join(index_dir, "meta.json"), "r", encoding="utf-8") as f:
            meta = json.load(f)
        return index, texts, meta
    except FileNotFoundError:
        raise FileNotFoundError("Index not found. Please run /index first.")


def retrieve(question, model, index, texts, meta, top_k=3):
    q_emb = model.encode([question], normalize_embeddings=True)
    D, I = index.search(q_emb, top_k)
    results = []
    for idx, score in zip(I[0], D[0]):
        results.append({
            "score": float(score),
            "text": texts[idx],
            "url": meta[idx]["url"]
        })
    # Sort descending by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results


def format_answer(raw_text, max_sentences=3):
    """
    Clean the LLM output: limit to 2-3 sentences + bullets
    """
    # Split sentences
    sentences = re.split(r'(?<=[.!?])\s+', raw_text.strip())
    short_answer = " ".join(sentences[:max_sentences])

    # Extract bullets if exist
    bullets = re.findall(r"[\*\-]\s*(.+)", raw_text)
    bullet_text = ""
    if bullets:
        bullet_text = "\n- " + "\n- ".join(bullets)

    return f"{short_answer}{bullet_text}"


def generate_answer(question, context_chunks, llm, use_gemini=False):
    # Combine top chunks into one grounded context
    context = "\n\n".join([f"Source: {c['url']}\n{c['text']}" for c in context_chunks])
    prompt = (
        "You are a precise and factual assistant. Use ONLY the CONTEXT below to answer. "
        "Do NOT use outside knowledge or assumptions. "
        "If the answer cannot be derived from the CONTEXT, respond exactly: `not found in crawled content` "
        "and include the most relevant snippets and their URLs.\n\n"
        "If an answer is found, summarize it clearly in 2–3 short sentences and list key details as bullet points.\n\n"
        f"QUESTION: {question}\n\nCONTEXT:\n{context}\n\nANSWER:"
    )

    if use_gemini:
        response = llm.generate_content(prompt)
        return format_answer(response.text.strip())
    else:
        answer = llm(prompt, max_new_tokens=200)[0]["generated_text"]
        return format_answer(answer.strip())


def ask(question, top_k=3):
    t0 = time.time()
    index, texts, meta = load_index()
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    retrieved = retrieve(question, embed_model, index, texts, meta, top_k)
    retrieval_ms = round((time.time() - t0) * 1000, 2)

    # Initialize LLM
    use_gemini = False
    if os.getenv("GEMINI_API_KEY"):
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        llm = genai.GenerativeModel("models/gemini-2.5-flash")
        use_gemini = True
    else:
        llm = pipeline("text2text-generation", model="google/flan-t5-small", device_map="auto")

    t1 = time.time()
    answer = generate_answer(question, retrieved, llm, use_gemini)
    generation_ms = round((time.time() - t1) * 1000, 2)
    total_ms = round((time.time() - t0) * 1000, 2)

    # Deduplicate sources by URL and truncate snippet
    seen_urls = set()
    formatted_sources = []
    for r in retrieved:
        if r["url"] not in seen_urls:
            snippet = r["text"][:150] + "..." if len(r["text"]) > 150 else r["text"]
            formatted_sources.append({"url": r["url"], "snippet": snippet})
            seen_urls.add(r["url"])

    result = {
        "answer": answer,
        "sources": formatted_sources,
        "timings": {
            "retrieval_ms": retrieval_ms,
            "generation_ms": generation_ms,
            "total_ms": total_ms
        }
    }
    return result


if __name__ == "__main__":
    q = input("Enter your question: ")
    response = ask(q, top_k=3)
    print(json.dumps(response, indent=2, ensure_ascii=False))
