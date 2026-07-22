import chromadb

from app.services.embedding_service import get_embedding


def get_file_priority(file_path: str):
    file_path = file_path.lower()

    if file_path.startswith(".github/"):
        return -0.60

    if "issue_template" in file_path:
        return -0.60

    if "pull_request_template" in file_path:
        return -0.60

    if file_path.startswith("src/"):
        return 0.55

    if file_path.startswith("app/"):
        return 0.55

    if file_path.startswith("lib/"):
        return 0.55

    if file_path.endswith(".py"):
        return 0.45

    if file_path.endswith(".java"):
        return 0.45

    if file_path.endswith(".ts"):
        return 0.45

    if file_path.endswith(".js"):
        return 0.45

    if file_path.startswith("tests/"):
        return 0.15

    if file_path.startswith("docs/"):
        return -0.25

    if file_path.endswith(".md"):
        return -0.25

    if file_path.endswith(".rst"):
        return -0.20

    return 0.0


def search_relevant_chunks(repo_id: int, question: str, top_k: int = 5):
    client = chromadb.PersistentClient(path="storage/chroma")

    collection = client.get_or_create_collection(
        name="engbrain_chunks"
    )

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=50,
        where={"repo_id": repo_id}
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    candidates = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        file_path = metadata["file_path"]
        priority = get_file_priority(file_path)

        adjusted_score = distance - priority

        candidates.append({
            "file_path": file_path,
            "start_line": metadata["start_line"],
            "end_line": metadata["end_line"],
            "text": document,
            "preview": document[:600],
            "distance": distance,
            "adjusted_score": adjusted_score
        })

    candidates = sorted(
        candidates,
        key=lambda item: item["adjusted_score"]
    )

    sources = []
    file_counts = {}

    for item in candidates:
        file_path = item["file_path"]

        if file_path not in file_counts:
            file_counts[file_path] = 0

        max_chunks_for_file = 2

        if file_path.startswith("tests/"):
            max_chunks_for_file = 1

        if file_path.startswith("docs/"):
            max_chunks_for_file = 1

        if file_path.startswith(".github/"):
            max_chunks_for_file = 0

        if file_counts[file_path] >= max_chunks_for_file:
            continue

        sources.append({
            "file_path": item["file_path"],
            "start_line": item["start_line"],
            "end_line": item["end_line"],
            "text": item["text"],
            "preview": item["preview"],
            "distance": item["distance"]
        })

        file_counts[file_path] += 1

        if len(sources) == top_k:
            break

    return sources