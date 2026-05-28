import sys
from pathlib import Path
from app.database import Base, engine, SessionLocal
from app.models import Repo, RepoFile, FileChunk
from app.services.repo_reader import read_repo_files
from app.services.chunker import chunk_file

def ingest_repo(repo_path:str):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("Databse Ready")
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
        print(f"Files found: {len(files)}")
        file_count =0
        chunk_count =0
        for file in files:
            repo_file = RepoFile(
                repo_id=repo.id,
                file_path=file["file_path"],
                file_type=file["file_type"],
                content=file["content"]
            )
            db.add(repo_file)
            db.commit()
            db.refresh(repo_file)
            file_count+=1
            chunks = chunk_file(file["content"])
            for chunk in chunks:
                    file_chunk = FileChunk(
                        repo_id = repo.id,
                        file_id = repo_file.id,
                        file_path = file["file_path"],
                        chunk_text = chunk["chunk_text"],
                        start_line = chunk["start_line"],
                        end_line = chunk["end_line"]
                    )
                    db.add(file_chunk)
                    chunk_count+=1
        db.commit()
        print(f"Files saved: {file_count}")
        print(f"Chunk count:{chunk_count}")
            
    finally:
        db.close()
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python scripts/ingest_repo.py "path/to/repo"')
        sys.exit(1)

    ingest_repo(sys.argv[1])
        
        