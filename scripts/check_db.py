from app.database import SessionLocal
from app.models import Repo, RepoFile, FileChunk

def check_db():
    db = SessionLocal()
    try:
        repo_count = db.query(Repo).count()
        file_count = db.query(RepoFile).count()
        chunk_count = db.query(FileChunk).count()
        print(repo_count)
        print(file_count)
        print(chunk_count)
        latest_repo = db.query(Repo).order_by(Repo.id.desc()).first()
        if latest_repo:
            print(f"Latest Repo Id: {latest_repo.id}")
            print(f"Latest Repo name: {latest_repo.name}")
            print(f"Latest Repo Path: {latest_repo.path}")
        files = db.query(RepoFile).limit(5).all()
        print("\nSample Files")
        for file in files:
            print(f"{file.id} | {file.file_path} | {file.file_type}")
        chunk = db.query(FileChunk).first()
        if chunk:
            print("\nSample chunk:")
            print(f"File: {chunk.file_path}")
            print(f"Lines: {chunk.start_line}-{chunk.end_line}")
            print(chunk.chunk_text[:300])
    finally:
        db.close()
        
if __name__ == "__main__":
    check_db()