import chromadb
from app.services.embedding_service import get_embedding

def search_relevant_chunks(repo_id: int, question: str, top_k: int = 5):
    client = chromadb.PersistentClient(path="storage/chroma")
    collection = client.get_or_create_collection(
        name = "engbrain_chunks"
    )
    question_embedding = get_embedding(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={"repo_id":repo_id}
    )
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    sources = []
    for doc, meta, distance in zip(documents, metadatas, distances):
        sources.append({
            "file_path": meta["file_path"],
            "start_line": meta["start_line"],
            "end_line": meta["end_line"],
            "text":doc,
            "preview": doc[:600],
            "distance": distance
        })
    return sources
        