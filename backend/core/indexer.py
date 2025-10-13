# core/indexer.py
import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def load_pages(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["pages"]

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """
    Splits long text into overlapping chunks.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += (chunk_size - overlap)
        if start >= len(words):
            break
    return chunks


def build_index(json_path="data/pages.json", out_dir="data/index", model_name="all-MiniLM-L6-v2"):
    os.makedirs(out_dir, exist_ok=True)

    errors = []  #  store failed URLs or chunks

    print(f"Loading model: {model_name}")
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:
        print("❌ Error loading model:", str(e))
        return {"vector_count": 0, "errors": [f"Model load failed: {str(e)}"]}

    try:
        pages = load_pages(json_path)
    except Exception as e:
        print("❌ Failed to load pages:", str(e))
        return {"vector_count": 0, "errors": [f"Failed to load pages: {str(e)}"]}

    texts = []
    metadata = []

    print("Chunking pages...")
    for url, text in tqdm(pages.items()):
        try:
            chunks = chunk_text(text)
            for chunk in chunks:
                if not chunk.strip():
                    continue
                texts.append(chunk)
                metadata.append({"url": url, "chunk_len": len(chunk)})
        except Exception as e:
            errors.append(f"Chunking failed for {url}: {str(e)}")

    print(f"Total chunks: {len(texts)}")

    # Encode all chunks
    print("Encoding chunks...")
    embeddings = []
    for i, chunk in enumerate(tqdm(texts)):
        try:
            emb = model.encode(chunk, convert_to_numpy=True, normalize_embeddings=True)
            embeddings.append(emb)
        except Exception as e:
            errors.append(f"Encoding failed for chunk {i}: {str(e)}")

    if not embeddings:
        print("❌ No embeddings generated.")
        return {"vector_count": 0, "errors": errors}

    embeddings = np.vstack(embeddings)
    dim = embeddings.shape[1]
    print(f"Embedding dimension: {dim}")

    # Build FAISS index
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    print(f"Indexed {index.ntotal} vectors.")

    # Save
    faiss.write_index(index, os.path.join(out_dir, "index.faiss"))
    np.save(os.path.join(out_dir, "texts.npy"), np.array(texts, dtype=object))
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("✅ Index built and saved in", out_dir)
    return {"vector_count": index.ntotal, "errors": errors}


if __name__ == "__main__":
    result = build_index()
    print(result)
