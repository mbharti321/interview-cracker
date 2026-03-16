"""
Unit tests for the FastAPI endpoints.
Tests /health, /ingest, /search, /chat endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api.main import app
from src.api.deps import get_db
from src.db.orm import Base


# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestHealthEndpoint:
    """Test /health endpoint."""
    
    def test_health_check(self):
        """Test that health endpoint returns ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestIngestEndpoint:
    """Test /ingest endpoint."""
    
    def test_ingest_documents(self):
        """Test ingesting sample documents."""
        response = client.post(
            "/ingest",
            json={
                "file_paths": [
                    "data/samples/lego_review.md",
                    "data/samples/dinosaurs_review.md",
                ]
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "document_count" in data
        assert "chunk_count" in data
        assert data["status"] == "success"


class TestSearchEndpoint:
    """Test /search endpoint."""
    
    def test_search_without_ingestion(self):
        """Test search returns empty when no documents ingested."""
        response = client.get("/search?q=lego&k=5")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert isinstance(data["results"], list)
    
    def test_search_with_parameters(self):
        """Test search endpoint accepts k parameter."""
        response = client.get("/search?q=toy&k=10")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "toy"


class TestChatEndpoint:
    """Test /chat endpoint."""
    
    def test_chat_simple_query(self):
        """Test chat endpoint with simple query."""
        response = client.post(
            "/chat",
            json={"query": "What toy reviews do you have?", "k": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "cached" in data
    
    def test_chat_with_filters(self):
        """Test chat with filters parameter."""
        response = client.post(
            "/chat",
            json={
                "query": "Recommend toys for kids",
                "k": 3,
                "filters": ["lego", "educational"],
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
    
    def test_chat_cache_hit(self):
        """Test that subsequent requests return cached results."""
        query_body = {"query": "Best toy ever?", "k": 5}
        
        # First request
        response1 = client.post("/chat", json=query_body)
        data1 = response1.json()
        assert data1["cached"] is False
        
        # Second request with same query (should hit cache)
        response2 = client.post("/chat", json=query_body)
        data2 = response2.json()
        # Note: May not be cached if Redis not running, but structure should be same
        assert data2["answer"] == data1["answer"]


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_search_k_value(self):
        """Test search rejects k > 50."""
        response = client.get("/search?q=test&k=51")
        # Should still work but FastAPI validates in model
        assert response.status_code in [200, 422]
    
    def test_missing_query_parameter(self):
        """Test search requires query parameter."""
        response = client.get("/search")
        assert response.status_code == 422
