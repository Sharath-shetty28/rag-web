#!/usr/bin/env python3
# server.py — unified RAG API
from fastapi import FastAPI
from routes.crawl_routes import router as crawl_router
from routes.index_routes import router as index_router
from routes.ask_routes import router as ask_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5500",  # if using normal HTML/JS
    "http://127.0.0.1:3000",
]


app = FastAPI(title="Mini RAG Service", version="1.0", description="A simple RAG (Retrieval-Augmented Generation) service with crawling, indexing, and Q&A capabilities. by https://sharathshetty.me")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],      # allow Content-Type headers etc.
)

# include routers
app.include_router(crawl_router, prefix="/api", tags=["Crawl"])
app.include_router(index_router, prefix="/api", tags=["Index"])
app.include_router(ask_router, prefix="/api", tags=["Ask"])

@app.get("/")
def home():
    return {"message": "RAG Service Running 🚀"}
