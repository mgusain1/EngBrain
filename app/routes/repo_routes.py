from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ingestion_service import ingest_repo

router = APIRouter(prefix="/repos")

class IngestRepoRequest(BaseModel):
    repo_path: str
    
@router.post("/ingest")
def ingest_repo_route(request:IngestRepoRequest):
    result = ingest_repo(request.repo_path)
    return result