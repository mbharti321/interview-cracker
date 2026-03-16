"""
Script to seed the vector store with sample documents.
Run this after starting services to populate the index.
"""
import os
import sys
from sqlalchemy.orm import Session

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.db.orm import SessionLocal, engine
from src.db import schema as db_schema
from src.rag.pipeline import RAGPipeline


def seed_database():
    """Ingest sample documents and build vector index."""
    # Create tables
    db_schema.init_db(engine)
    
    # Get database session
    db = SessionLocal()
    
    # Initialize RAG pipeline
    pipeline = RAGPipeline()
    
    # List sample files
    samples_dir = "data/samples"
    file_paths = [
        os.path.join(samples_dir, f)
        for f in os.listdir(samples_dir)
        if f.endswith(".md")
    ]
    
    if not file_paths:
        print(f"No sample files found in {samples_dir}")
        return
    
    print(f"Seeding database with {len(file_paths)} documents...")
    
    try:
        doc_count, chunk_count = pipeline.ingest_documents(file_paths, db)
        print(f"✓ Ingested {doc_count} documents, {chunk_count} chunks")
        print(f"✓ Vector index updated at data/vectors/")
    except Exception as e:
        print(f"✗ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
