from app.database import SessionLocal
from app.models import EventLog


def main():
    db = SessionLocal()

    try:
        logs = db.query(EventLog).order_by(EventLog.id.desc()).limit(50).all()

        print("Recent event logs:")
        print("-" * 80)

        for log in logs:
            print("ID:", log.id)
            print("Session:", log.session_id)
            print("Event:", log.event_type)
            print("Repo input:", log.repo_input)
            print("Repo ID:", log.repo_id)
            print("Status:", log.status)
            print("Message:", log.message)
            print("Created:", log.created_at)
            print("-" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    main()