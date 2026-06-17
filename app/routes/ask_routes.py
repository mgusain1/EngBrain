from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval_service import search_relevant_chunks
from app.services.answer_service import generate_answer

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    top_k: int =5
    repo_id: int
    
@router.post("/ask")
def ask_question(request: AskRequest):
    sources = search_relevant_chunks(repo_id= request.repo_id, question=request.question, top_k=request.top_k)
    best_source = sources[0] if sources else None
    answer = generate_answer(
        question=request.question,
        source=sources
    )
    return {
        "question" : request.question,
        "answer": answer,
        "sources": sources
    }