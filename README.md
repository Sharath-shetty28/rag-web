# 🧠 RAG Web Project — Website Crawler + Index + Q&A API

## 📋 Overview
This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that crawls a website, extracts and indexes its textual content, and answers user questions grounded **strictly** in the crawled data — with **citations** of source URLs.

---

## ⚙️ Architecture
**Pipeline Flow:**


LLM: Open-source local (e.g., gemini api)

```bash
Crawl Website → Extract & Clean Text → Chunk & Embed → Store in Vector Index → Retrieve Top-K → Generate Grounded Answer

```

## Folder Structure

```bash
|   README.md       
+---backend
|   |   .env
|   |   eval_queries.py
|   |   requirements.txt
|   |   server.py
|   |   
|   +---core
|   |   |   ask.py
|   |   |   crawler.py
|   |   |   indexer.py
|   |   |   metrics.py
|   |   |   
|   |           
|   +---data
|   |   |   pages.json
|   |   |   
|   |   \---index
|   |           index.faiss
|   |           meta.json
|   |           texts.npy
|   |           
|   +---models
|   |   |   schemas.py
|   |           
|   +---routes
|   |   |   ask_routes.py
|   |   |   crawl_routes.py
|   |   |   index_routes.py
|   |   |   
|           
\---frontend
        index.html
        script.js
        style.css
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
  "start_url": "https://www.djangoproject.com",
  "max_pages": 10,
  "max_depth": 2,
  "crawl_delay_ms": 10
}
```

Response

```bash
{
  "page_count": 10,
  "skipped_count": 0,
  "urls": [
    "https://www.djangoproject.com",
    "https://www.djangoproject.com/",
    "https://www.djangoproject.com/start/overview/",
    "https://www.djangoproject.com/download/",
    "https://docs.djangoproject.com/",
    "https://www.djangoproject.com/weblog/",
    "https://www.djangoproject.com/community/",
    "https://code.djangoproject.com/",
    "https://www.djangoproject.com/foundation/",
    "https://www.djangoproject.com/fundraising/"
  ],
  "duration_ms": 113028.2
}

```

2️⃣ POST /index

Indexes crawled content.

Request Body
```bash
{
  "chunk_size": 500,
  "chunk_overlap": 50,
  "embedding_model": "all-MiniLM-L6-v2"
}

```

Response
```bash
{
  "vector_count": 11,
  "errors": []
}

```

3️⃣ POST /ask

* Answers user questions strictly from crawled content.

Request Body
```bash
{
  "question": "what is Django?",
  "top_k": 3
}

```
Response

```bash
{
  "answer": "Django is a high-level Python web framework designed to encourage rapid development and clean, pragmatic design. It handles much of the complexity of web development, allowing developers to focus on building their applications quickly. Django is free, open source, and built to be fast, secure, and highly scalable.\n\nKey details:\n*   High-level Python web framework\n*   Encourages rapid development and clean, pragmatic design\n*   Free and open source\n*   Designed to be fast, secure, and scalable\n*   Includes built-in features for tasks like user authentication, content administration, and site maps",
  "sources": [
    {
      "url": "https://www.djangoproject.com/",
      "snippet": "Meet Django Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web devel"
    },
    {
      "url": "https://www.djangoproject.com",
      "snippet": "Meet Django Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web devel"
    },
    {
      "url": "https://www.djangoproject.com/start/overview/",
      "snippet": "Why Django? With Django, you can take web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of web development, so you can focus on writing your app wit"
    }
  ],
  "timings": {
    "retrieval_ms": 5608.5,
    "generation_ms": 4535.75,
    "total_ms": 11088.82
  }
}

```
case 2:

Request Body
```bash
{
  "question": "what is my IP address",
  "top_k": 2
}

```

Request Body

```bash
{
  "answer": "not found in crawled content",
  "sources": [
    {
      "url": "https://www.djangoproject.com/community/",
      "snippet": "django-admin-cursor-paginator Oct. 12, 2025, 6:07 p.m. by Django Packages django-related-field-display Oct. 8, 2025, 3:39 p.m. by Django Packages An assortment of Django mixins and middleware for work"
    },
    {
      "url": "https://www.djangoproject.com/",
      "snippet": "Meet Django Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web devel"
    }
  ],
  "timings": {
    "retrieval_ms": 5569.21,
    "generation_ms": 2005.11,
    "total_ms": 7574.7
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
* Crawl → Provide a website (e.g., https://fastapi.tiangolo.com)
* Index → Choose chunk size and embedding model (default: all-MiniLM-L6-v2)
* Ask → Ask a question like “What is FastAPI?”
* Observe → The model answers using only crawled text, citing sources.



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
| ✅ Answerable    | “What is Django? ”           | Returns answer + source URLs              |
| 🚫 Unanswerable | “What is my IP address ?” | Responds: “Not found in crawled content.” |


### Run the test file

- For the metrics

```bash
python eval_queries.py
```
         
### 🧾 Metrics Logged

```bash
{
 Latency stats: {
    'p50_ms': 8191.81,
    'p95_ms': 15841.576,
    'min_ms': 7167.52,
    'max_ms': 16691.55
   }
}

```

### 🧮 Latency Metrics (Sample Run)
| Metric | Value (ms) |
|--------|-------------|
| p50 | 8191.8 |
| p95 | 15841.6 |
| min | 7167.5 |
| max | 16691.5 |

> Average query: ~8 s. Tail latency driven by model generation.  
> Retrieval and embedding times were sub-second, confirming that generation is the primary contributor.


🧩 Summary Flow
```
Raw File (PDF, DOCX, HTML)
      ↓
Parsing (Extract Text)
      ↓
Cleaning (Remove noise)
      ↓
Chunking (Split into small pieces)
      ↓
Embedding (Convert to vectors)
      ↓
Store in Vector DB (for Retrieval)

```

Raw text → clean → split into 400–800 token chunks (with 10–20% overlap)
→ send chunks to embedding model in batches (e.g., 100 per batch)
→ store embeddings + chunk metadata in vector DB

