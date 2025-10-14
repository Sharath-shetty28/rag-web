# 🧠 RAG Web Project — Website Crawler + Index + Q&A API

## 📋 Overview
This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that crawls a website, extracts and indexes its textual content, and answers user questions grounded **strictly** in the crawled data — with **citations** of source URLs.

---

## ⚙️ Architecture
**Pipeline Flow:**



```bash
Crawl Website → Extract & Clean Text → Chunk & Embed → Store in Vector Index → Retrieve Top-K → Generate Grounded Answer

```
    
## Main Components:
| Component | Description                                                                                 |
| --------- | ------------------------------------------------------------------------------------------- |
| `/crawl`  | Crawls website pages (within domain), respecting `robots.txt`.                              |
| `/index`  | Chunks text, creates embeddings using `SentenceTransformer`, and stores FAISS index.        |
| `/ask`    | Retrieves top-K context chunks, generates grounded answer, and returns citations + timings. |

## 🧩 API Endpoints

1️⃣ POST /crawl

Crawls the website.

Request Body

```bash
{
  "start_url": "https://example.com",
  "max_pages": 30,
  "max_depth": 2,
  "crawl_delay_ms": 500
}
```

Response

```bash
{
  "page_count": 30,
  "skipped_count": 5,
  "urls": ["https://example.com/about", "..."]
}

```

2️⃣ POST /index

Indexes crawled content.

Request Body
```bash
{
  "chunk_size": 800,
  "chunk_overlap": 100,
  "embedding_model": "all-MiniLM-L6-v2"
}

```

Response
```bash
{
  "message": "Index built successfully",
  "vector_count": 120
}

```

3️⃣ POST /ask

Answers user questions strictly from crawled content.

Request Body
```bash
{
  "question": "What services does the company offer?",
  "top_k": 3
}

```
Response

```bash
{
  "answer": "The company provides data analytics and AI consulting services.",
  "sources": [
    {"url": "https://example.com/services", "snippet": "Our core services include..."}
  ],
  "timings": {
    "retrieval_ms": 125,
    "generation_ms": 870,
    "total_ms": 995
  }
}

```

### 💾 Setup Instructions
1. Clone Repository

```bash
git clone https://github.com/<your-username>/rag-web.git
cd rag-web
```

2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   
```

3. Install Requirements

```bash
pip install -r requirements.txt
```
4. Run the Backend
```bash
cd backend
uvicorn server:app --reload

```

5. Open Frontend (HTML)
```bash
 Open frontend/index.html in your browser.
 http://127.0.0.1:3000/frontend/index.html

```
### 📊 Example Demo Flow
1.Crawl → Provide a website (e.g., https://fastapi.tiangolo.com)
2.Index → Choose chunk size and embedding model (default: all-MiniLM-L6-v2)
3.Ask → Ask a question like “What is FastAPI?”
4.Observe → The model answers using only crawled text, citing sources.



### Design Choices & Tradeoffs

* ✅ Chunk Size (800) — balanced between retrieval precision and context coherence.
* ✅ Overlap (100) — ensures no important information is split across chunks.
* ✅ Embedding Model — all-MiniLM-L6-v2 chosen for speed + good semantic accuracy.
* ✅ FAISS used for fast similarity search.
* ✅ Politeness — respects robots.txt and includes a crawl delay.
* ✅ Grounding — model refuses with “not found in crawled content” when unsure.
* ⚠️ Limitation: No JavaScript-rendered pages; only static HTML text supported.
* ⚙️ Future Work: Add persistence DB and improved text cleaning.



 ### 🔒Safety & Guardrails
 
 * Refuses to answer out-of-domain questions.
 * Ignores any “prompt injection” instructions inside crawled pages.
 * Logs retrieval + generation latency for monitoring.


### 🧰 Tooling & Models
| Component       | Tool / Library                           |
| --------------- | ---------------------------------------- |
| Language        | Python 3.10                              |
| Web Server      | FastAPI                                  |
| Frontend        | HTML + CSS + JS                          |
| Text Extraction | BeautifulSoup                            |
| Embeddings      | `SentenceTransformer (all-MiniLM-L6-v2)` |
| Vector Store    | FAISS                                    |
| LLM             | Gemini / Open-source model (via API)     |


### 🧪 Example Evals
| Type            | Input                            | Expected Output                           |
| --------------- | -------------------------------- | ----------------------------------------- |
| ✅ Answerable    | “Who founded FastAPI?”           | Returns answer + source URLs              |
| 🚫 Unanswerable | “Who is the president of India?” | Responds: “Not found in crawled content.” |


### 🧾 Metrics Logged

```bash
{
  "latency_stats": {
    "p50_ms": 12416.88,
    "p95_ms": 15004.80,
    "min_ms": 8864.18,
    "max_ms": 15292.35
  }
}

```
