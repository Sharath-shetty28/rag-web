from fastapi import APIRouter
import time
from core.indexer import build_index
from models.schemas import IndexRequest

router = APIRouter()

@router.post("/index")
def index(req: IndexRequest):
    vector_count = build_index(
        json_path="data/pages.json",
        out_dir="data/index",
        model_name=req.embedding_model
    )
    return {"vector_count": vector_count["vector_count"], "errors": vector_count["errors"]}
