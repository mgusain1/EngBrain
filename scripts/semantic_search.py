import sys
import chromadb
from app.services.embedding_service import get_embedding

def semantic_search(text:str):
    client = chromadb.PersistentClient(path = 'storage/chroma')
    collection = client.get_or_create_collection(
        name = "engbrain_chunks"
    )
    question_embedding = get_embedding(text)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    for doc, meta, distance in zip(documents, metadatas, distances):
        print("=" * 60)
        print(f"File: {meta['file_path']}")
        print(f"Lines: {meta['start_line']}-{meta['end_line']}")
        print(f"Distance: {distance}")
        print()
        print(doc[:600])
        print()
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python -m scripts.semantic_search "your question"')
        sys.exit(1)

    semantic_search(sys.argv[1])