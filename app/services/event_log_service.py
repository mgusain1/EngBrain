from app.database import Base, engine, SessionLocal
from app.models import EventLog


def log_event(
    event_type: str,
    session_id: str | None = None,
    repo_input: str | None = None,
    repo_id: int | None = None,
    status: str | None = None,
    message: str | None = None
):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        event = EventLog(
            session_id=session_id,
            event_type=event_type,
            repo_input=repo_input,
            repo_id=repo_id,
            status=status,
            message=message
        )

        db.add(event)
        db.commit()

    finally:
        db.close()