from pydantic import BaseModel

class CrawlRequest(BaseModel):
    start_url: str
    max_pages: int = 20
    max_depth: int = 2
    crawl_delay_ms: float = 0.5  # milliseconds

class IndexRequest(BaseModel):
    chunk_size: int = 800
    chunk_overlap: int = 100
    embedding_model: str = "all-MiniLM-L6-v2"

class AskRequest(BaseModel):
    question: str
    top_k: int = 3
