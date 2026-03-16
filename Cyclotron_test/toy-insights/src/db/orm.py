"""
SQLAlchemy ORM setup and models.
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database URL from environment or default SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./toy_insights.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Document(Base):
    """Document metadata."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    
    chunks = relationship("Chunk", back_populates="document")


class Chunk(Base):
    """Document chunks for retrieval."""
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    
    document = relationship("Document", back_populates="chunks")


class ChatTranscript(Base):
    """Chat interaction history."""
    __tablename__ = "chat_transcripts"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)
