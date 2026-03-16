"""
Dependency injection utilities for FastAPI.
Provides DB sessions, cache clients, and other shared resources.
"""
from typing import Generator
from sqlalchemy.orm import Session
from src.db.orm import SessionLocal
from src.cache.redis_client import get_redis_client


def get_db() -> Generator[Session, None, None]:
    """Dependency: provide SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    """Dependency: provide Redis client."""
    return get_redis_client()
