import json

from app.database import Base, engine, declarative_base
from app.models import QueryLog

import json

from app.database import Base, engine, SessionLocal
from app.models import QueryLog


def log_query(session_id, repo_id, query_type, question, answer, sources):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        simplified_sources = []

        for source in sources:
            simplified_sources.append({
                "file_path": source.get("file_path"),
                "start_line": source.get("start_line"),
                "end_line": source.get("end_line")
            })

        query_log = QueryLog(
            session_id=session_id,
            repo_id=repo_id,
            query_type=query_type,
            question=question,
            answer=answer,
            sources_returned=json.dumps(simplified_sources)
        )

        db.add(query_log)
        db.commit()

    finally:
        db.close()