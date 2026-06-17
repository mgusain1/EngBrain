import chromadb
from app.database import SessionLocal
from app.models import FileChunk
from app.services.embedding_service import get_embedding

def build_vector_index(repo_id:int):
    db = SessionLocal()
    try:
        client = chromadb.PersistentClient(path="storage/chroma")
        collection = client.get_or_create_collection(
            name = "engbrain_chunks"
        )
        chunks = db.query(FileChunk).filter(FileChunk.repo_id == repo_id).all()
        count =0
        for chunk in chunks:
            embedding = get_embedding(chunk.chunk_text)
            collection.add(
                ids=[str(chunk.id)],
                documents=[chunk.chunk_text],
                embeddings=[embedding],
                metadatas=[{
                    "repo_id": chunk.repo_id,
                    "file_id": chunk.file_id,
                    "file_path": chunk.file_path,
                    "start_line": chunk.start_line,
                    "end_line": chunk.end_line
                }]
            )
            count+=1
        return {
            "chunks_indexed": count
        }
    finally:
        db.close()