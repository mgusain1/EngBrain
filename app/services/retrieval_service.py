import chromadb
from app.services.embedding_service import get_embedding

def search_relevant_chunks(question: str, top_k: int = 5):
    client = chromadb.PersistentClient(path="storage/chroma")
    collection = client.get_or_create_collection(
        name = "engbrain_chunks"
    )
    question_embedding = get_embedding(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
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
            "text": doc,
            "distance": distance
        })
    return sources
        