Project: Mini Retrieval-Augmented Generation (RAG) system for any website

Language: Python 3.10+

Crawling: Polite, in-domain, 30–50 pages max, uses readability-lxml

Indexing: Chunk size 800, overlap 100, embeddings via all-MiniLM-L6-v2, stored in FAISS

RAG Retrieval: Top-k semantic search + grounded prompt to LLM

LLM: Open-source local (e.g., Gemma-2b, Phi-2)

Refusals: Returns “not found in crawled content” if answer missing

API: FastAPI with /crawl, /index, /ask endpoints

Observability: Retrieval/generation/total latency logged, p50/p95 computed

Query Logging: Stores each question, answer, sources, and timings

Evaluation: Small test set demonstrates answerable + unanswerable queries

Safety: Context-only answering, ignores page instructions, stays within domain

Tradeoffs: Does not render JavaScript-heavy sites, only HTML content

Setup: venv, pip install requirements, run server.py

Next Steps: Can add multi-domain crawling, larger models, or async crawling
