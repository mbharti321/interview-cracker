"""
Database schema initialization and migrations.
"""
from sqlalchemy import text
from src.db.orm import Base, engine


def init_db(engine_instance):
    """Create all database tables."""
    Base.metadata.create_all(bind=engine_instance)


def get_schema_sql() -> str:
    """
    Get SQL schema definition for reference.
    For production, use Alembic for migrations.
    """
    return """
    -- Documents table
    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        source VARCHAR(500) NOT NULL,
        content TEXT NOT NULL,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Chunks table
    CREATE TABLE chunks (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES documents(id),
        text TEXT NOT NULL,
        chunk_index INTEGER NOT NULL
    );
    
    -- Chat transcripts table
    CREATE TABLE chat_transcripts (
        id SERIAL PRIMARY KEY,
        query TEXT NOT NULL,
        answer TEXT NOT NULL,
        sources TEXT,  -- JSON string with metadata
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Indexes for performance
    CREATE INDEX idx_chunks_document_id ON chunks(document_id);
    CREATE INDEX idx_chat_timestamp ON chat_transcripts(timestamp);
    """
