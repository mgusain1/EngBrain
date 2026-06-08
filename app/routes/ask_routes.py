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
    best_source = sources[0] if sources else None
    answer_preview = None
    if best_source:
        answer_preview = (
            f"The most relevant source is {best_source['file_path']} "
            f"at lines {best_source['start_line']}-{best_source['end_line']}."
        )
    return {
        "question" : request.question,
        "answer_preview": answer_preview,
        "sources": sources
    }