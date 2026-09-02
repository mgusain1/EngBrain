from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ingestion_service import ingest_repo
from app.services.vector_index_service import build_vector_index
from app.database import Base, engine, SessionLocal
from app.models import Repo
from app.services.event_log_service import log_event

router = APIRouter(prefix="/repos")

class IngestRepoRequest(BaseModel):
    repo_path: str
    session_id : str| None = None
    
@router.post("/ingest")
def ingest_repo_route(request:IngestRepoRequest):
    log_event(
        event_type="ingest_started",
        session_id=request.session_id,
        repo_input=request.repo_path,
        status="started"
    )
    try:
        ingest_result = ingest_repo(request.repo_path)
        index_result = build_vector_index(ingest_result["repo_id"])
        log_event(
            event_type="ingest_success",
            session_id=request.session_id,
            repo_input=request.repo_path,
            repo_id=ingest_result["repo_id"],
            status="success",
            message="Repository ingested and indexed successfully."
        )
        return {
            **ingest_result,
            **index_result
        }
    except ValueError as e:
        log_event(
            event_type="ingest_failed",
            session_id=request.session_id,
            repo_input=request.repo_path,
            status="failed",
            message=str(e)
        )
        raise HTTPException(status_code=400, detail=str(e))
    
    except RuntimeError as e:
        log_event(
            event_type="ingest_failed",
            session_id=request.session_id,
            repo_input=request.repo_path,
            status="failed",
            message=str(e)
        )
        raise HTTPException(status_code=502, detail=str(e))
    
    except Exception as e:
        log_event(
            event_type="ingest_failed",
            session_id=request.session_id,
            repo_input=request.repo_path,
            status="failed",
            message=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("")
def list_repos():
    Base.metadata.create_all(bind=engine)
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