from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search_relevant_chunks
from app.services.runbook_service import generate_runbook


router = APIRouter()


class RunbookRequest(BaseModel):
    repo_id: int
    task: str
    top_k: int = 5


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

    return {
        "repo_id": request.repo_id,
        "task": request.task,
        "runbook": runbook,
        "sources": sources
    }