"""
Pydantic request/response models for the Toy Insights API.

NOTE: Contains deliberate bug in ChatRequest.filters (mutable default).
"""
from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response."""
    status: str


class IngestRequest(BaseModel):
    """Request to ingest documents from file paths."""
    file_paths: list[str] = Field(..., description="List of file paths to ingest")


class IngestResponse(BaseModel):
    """Response after ingestion."""
    document_count: int
    chunk_count: int
    status: str


class SearchRequest(BaseModel):
    """Search query request."""
    q: str = Field(..., description="Search query")
    k: int = Field(5, ge=1, le=50, description="Number of top results to return")


class SearchResult(BaseModel):
    """Individual search result."""
    score: float
    content: str
    document_id: int
    source: str


class SearchResponse(BaseModel):
    """Search response with ranked results."""
    query: str
    results: list[SearchResult]


class ChatRequest(BaseModel):
    """
    Chat/RAG request.
    
    BUG: filters uses mutable default (empty list).
    This causes state bleed across requests if not careful.
    """
    query: str = Field(..., description="User query")
    k: int = Field(5, ge=1, le=50, description="Retrieval top-k")
    # filters: list[str] = []  # <-- DELIBERATE BUG: mutable default  -> # None
    filters: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Chat/RAG response with answer and citations."""
    answer: str
    sources: list[dict]  # Each dict: {document_id, source, score, snippet}
    cached: bool = False


class ChatTranscript(BaseModel):
    """Stored chat transcript in database."""
    query: str
    answer: str
    timestamp: str
    sources: str  # JSON string
    cached: bool = False
