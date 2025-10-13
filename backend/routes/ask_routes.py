from fastapi import APIRouter
from core.ask import ask
from models.schemas import AskRequest

router = APIRouter()

@router.post("/ask")
def ask_question(req: AskRequest):
    result = ask(req.question, top_k=req.top_k)
    return result
