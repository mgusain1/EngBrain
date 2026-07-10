from pathlib import Path
from app.database import Base, engine, SessionLocal
from app.models import Repo, RepoFile, FileChunk
from app.services.repo_reader import read_repo_files
from app.services.github_service import is_github_url, read_github_repo
from app.services.chunker import chunk_file


def ingest_repo(repo_path: str):
    Base.metadata.create_all(bind=engine)

    repo_path = repo_path.strip()

    if not repo_path:
        raise ValueError("Repository path or GitHub URL is required.")
    if is_github_url(repo_path):
        repo_name = repo_path.rstrip("/").split("/")[-1]

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        files = read_github_repo(repo_path)

    else:
        local_path = Path(repo_path)

        if not local_path.exists():
            raise ValueError("Local repository path does not exist.")

        if not local_path.is_dir():
            raise ValueError("Repository path must point to a directory.")

        repo_name = local_path.name
        files = read_repo_files(repo_path)

    if not files:
        raise ValueError(
            "No supported source, documentation, or configuration files were found."
        )

    db = SessionLocal()

    try:
        repo = Repo(
            name=repo_name,
            path=repo_path
        )

        db.add(repo)
        db.flush()

        file_count = 0
        chunk_count = 0

        for file in files:
            chunks = chunk_file(file["content"])

            # Skip files that produce no searchable chunks.
            if not chunks:
                continue

            repo_file = RepoFile(
                repo_id=repo.id,
                file_path=file["file_path"],
                file_type=file["file_type"],
                content=file["content"]
            )

            db.add(repo_file)
            db.flush()

            file_count += 1

            for chunk in chunks:
                file_chunk = FileChunk(
                    repo_id=repo.id,
                    file_id=repo_file.id,
                    file_path=file["file_path"],
                    chunk_text=chunk["chunk_text"],
                    start_line=chunk["start_line"],
                    end_line=chunk["end_line"]
                )

                db.add(file_chunk)
                chunk_count += 1

        if file_count == 0 or chunk_count == 0:
            raise ValueError(
                "Repository files were found, but no searchable chunks were created."
            )

        db.commit()
        db.refresh(repo)

        return {
            "repo_id": repo.id,
            "repo_name": repo.name,
            "repo_path": repo.path,
            "files_indexed": file_count,
            "chunks_created": chunk_count
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()