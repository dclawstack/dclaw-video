from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return naive UTC datetime for SQLAlchemy models."""
    return datetime.now(UTC).replace(tzinfo=None)
