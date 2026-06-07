from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval_service import search_relevant_chunks

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    top_k: int =5
    
@router.post("/ask")
def ask_question(request: AskRequest):
    sources = search_relevant_chunks(question=request.question, top_k=request.top_k)
    return {
        "question" : request.ask_question,
        "sources": sources
    }