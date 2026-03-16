"""
FastAPI application for Toy Insights RAG service.

Endpoints:
  GET  /health          - Health check
  POST /ingest          - Ingest documents from file paths
  GET  /search          - Query vector store
  POST /chat            - RAG-style chat endpoint
"""
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.api.models import (
    HealthResponse,
    IngestRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
    ChatRequest,
    ChatResponse,
)
from src.api.deps import get_db, get_cache
from src.rag.pipeline import RAGPipeline
from src.db.orm import engine
from src.db import schema as db_schema

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Toy Insights API",
    description="RAG-enabled service for toy product insights",
    version="0.1.0",
)

# Initialize RAG pipeline (lazy-loaded on first use)
_rag_pipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or initialize the RAG pipeline."""
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    db_schema.init_db(engine)
    logger.info("Database initialized")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    request: IngestRequest,
    db: Session = Depends(get_db),
):
    """
    Ingest documents from file paths.
    
    - Splits documents into chunks
    - Stores metadata in PostgreSQL
    - Updates vector index
    """
    try:
        pipeline = get_rag_pipeline()
        doc_count, chunk_count = pipeline.ingest_documents(request.file_paths, db)
        return IngestResponse(
            document_count=doc_count,
            chunk_count=chunk_count,
            status="success",
        )
    except Exception as e:
        logger.exception(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", response_model=SearchResponse)
async def search(
    q: str,
    k: int = 5,
    db: Session = Depends(get_db),
):
    """
    Search the vector store for top-k results.
    
    Query parameters:
      - q: search query
      - k: number of results (1-50)
    """
    try:
        pipeline = get_rag_pipeline()
        results = pipeline.search(q, k, db)
        return SearchResponse(query=q, results=results)
    except Exception as e:
        logger.exception(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    cache=Depends(get_cache),
):
    """
    RAG-style chat endpoint.
    
    - Checks Redis cache for recent answers
    - Retrieves top-k chunks from vector store
    - Augments prompt with context
    - Generates answer (mock or LLM)
    - Stores transcript in PostgreSQL
    - Caches result for 5 minutes
    
    NOTE: request.filters has mutable default bug!
    """
    try:
        pipeline = get_rag_pipeline()
        
        # Attempt cache hit
        cache_key = f"chat:{request.query}:{request.k}"
        cached_answer = cache.get(cache_key)
        if cached_answer:
            logger.info(f"Cache hit for query: {request.query}")
            import json
            cached_data = json.loads(cached_answer)
            return ChatResponse(
                answer=cached_data["answer"],
                sources=cached_data["sources"],
                cached=True,
            )
        
        # Cache miss: run RAG pipeline
        answer, sources = pipeline.chat(request.query, request.k, db)
        
        # Store transcript
        pipeline.store_transcript(request.query, answer, sources, db)
        
        # Cache result
        import json
        cache_data = {
            "answer": answer,
            "sources": sources,
        }
        cache.set(cache_key, json.dumps(cache_data), ttl=300)  # 5 minutes
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            cached=False,
        )
    except Exception as e:
        logger.exception(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
