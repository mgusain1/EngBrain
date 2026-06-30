from fastapi import APIRouter
from pydantic import BaseModel
from app.services.query_log_service import log_query
from app.services.retrieval_service import search_relevant_chunks
from app.services.runbook_service import generate_runbook


router = APIRouter()


class RunbookRequest(BaseModel):
    repo_id: int
    task: str
    top_k: int = 5
    session_id: str | None = None


@router.post("/runbook")
def create_runbook(request: RunbookRequest):
    sources = search_relevant_chunks(
        repo_id=request.repo_id,
        question=request.task,
        top_k=request.top_k
    )

    runbook = generate_runbook(
        task=request.task,
        sources=sources
    )
    if request.session_id:
        log_query(
            session_id=request.session_id,
            repo_id=request.repo_id,
            query_type="runbook",
            question=request.task,
            answer=runbook,
            sources=sources
        )

    return {
        "repo_id": request.repo_id,
        "task": request.task,
        "runbook": runbook,
        "sources": sources
    }