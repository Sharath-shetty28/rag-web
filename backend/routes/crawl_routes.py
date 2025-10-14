from fastapi import APIRouter
import time
from core.crawler import crawl_site
from models.schemas import CrawlRequest

router = APIRouter()

@router.post("/crawl")
def crawl(req: CrawlRequest):
    start_time = time.time()
    result = crawl_site(req.start_url, req.max_pages, req.max_depth,  req.crawl_delay_ms, out_file="data/pages.json")
    duration = round((time.time() - start_time) * 1000, 2)
    result["duration_ms"] = duration
    return result
