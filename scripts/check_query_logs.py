from app.database import SessionLocal
from app.models import QueryLog


def main():
    db = SessionLocal()

    try:
        logs = db.query(QueryLog).order_by(QueryLog.id.desc()).limit(50).all()

        print("Recent query logs:")
        print("-" * 80)

        for log in logs:
            print("ID:", log.id)
            print("Session:", log.session_id)
            print("Repo ID:", log.repo_id)
            print("Type:", log.query_type)
            print("Question:", log.question)
            print("Answer:", (log.answer or "")[:300])
            print("Sources:", log.sources_returned)
            print("Created:", log.created_at)
            print("-" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    main()