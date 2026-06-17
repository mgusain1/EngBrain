from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ingestion_service import ingest_repo
from app.services.vector_index_service import build_vector_index
from app.database import SessionLocal
from app.models import Repo

router = APIRouter(prefix="/repos")

class IngestRepoRequest(BaseModel):
    repo_path: str
    
@router.post("/ingest")
def ingest_repo_route(request:IngestRepoRequest):
    ingest_result = ingest_repo(request.repo_path)
    index_result = build_vector_index(ingest_result["repo_id"])
    return {
    **ingest_result,
    **index_result
}
    
@router.get("")
def list_repos():
    db = SessionLocal()
    try:
        repos = db.query(Repo).order_by(Repo.id.desc()).all()
        result = []
        for repo in repos:
            result.append({
                "repo_id":repo.id,
                "repo_name": repo.name,
                "repo_path": repo.path,
                "created_at": str(repo.created_at)
            })
        return result
    finally:
        db.close()