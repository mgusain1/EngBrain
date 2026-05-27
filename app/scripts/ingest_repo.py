import sys
from pathlib import Path
from app.database import Base, engine, SessionLocal
from app.models import Repo, RepoFile
from app.services.repo_reader import read_repo_files
from app.services.chunker import chunk_file

def ingest_repo(repo_path:str):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("Databse Ready")
        db.close()
        repo_name = Path(repo_path).name
        repo = Repo(
        name=repo_name,
        path=repo_path
        )
        db.add(repo)
        db.commit()
        db.refresh(repo)
        print(repo.id, repo.name)
        files = read_repo_files(repo_path)
        print(len(files))
    finally:
        db.close()
        
        