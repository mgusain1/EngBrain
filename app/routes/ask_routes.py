from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval_service import search_relevant_chunks
from app.services.answer_service import generate_answer
from app.services.query_log_service import log_query

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    top_k: int =5
    repo_id: int
    session_id: str | None = None
    
@router.post("/ask")
def ask_question(request: AskRequest):
    sources = search_relevant_chunks(repo_id= request.repo_id, question=request.question, top_k=request.top_k)
    best_source = sources[0] if sources else None
    answer = generate_answer(
        question=request.question,
        source=sources
    )
    if request.session_id:
        log_query(
            session_id=request.session_id,
            repo_id=request.repo_id,
            query_type="ask",
            question=request.question,
            answer=answer,
            sources=sources
        )
    return {
        "repo":request.repo_id,
        "question" : request.question,
        "answer": answer,
        "sources": sources
    }