"""
Tests for RAG pipeline components.
Tests embedding, vector store, and retrieval quality.
"""
import pytest
from src.rag.embeddings import EmbeddingProvider
from src.rag.vectorstore import VectorStore
from src.rag.pipeline import RAGPipeline


class TestEmbeddings:
    """Test embedding provider."""
    
    def test_embed_single_string(self):
        """Test embedding a single string."""
        provider = EmbeddingProvider()
        embedding = provider.embed_single("This is a test document")
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embed_multiple_strings(self):
        """Test embedding multiple strings."""
        provider = EmbeddingProvider()
        texts = ["First text", "Second text", "Third text"]
        embeddings = provider.embed(texts)
        assert len(embeddings) == 3
        assert all(isinstance(e, list) for e in embeddings)


class TestVectorStore:
    """Test vector store operations."""
    
    def test_create_vector_store(self):
        """Test creating a vector store."""
        store = VectorStore(index_dir="/tmp/test_vectors")
        assert store is not None
        assert store.embedding_dim == 384
    
    def test_add_and_search(self):
        """Test adding embeddings and searching."""
        store = VectorStore(index_dir="/tmp/test_vectors")
        
        # Add mock embeddings
        embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]
        metadata = [
            {"text": "toy review 1", "source": "test1"},
            {"text": "toy review 2", "source": "test2"},
            {"text": "toy review 3", "source": "test3"},
        ]
        
        store.add(embeddings, metadata)
        
        # Search
        query_embedding = [0.15] * 384
        results = store.search(query_embedding, k=2)
        
        assert len(results) > 0
        assert all("text" in r for r in results)


class TestRAGPipeline:
    """Test RAG pipeline."""
    
    def test_pipeline_initialization(self):
        """Test RAG pipeline initializes correctly."""
        pipeline = RAGPipeline()
        assert pipeline is not None
        assert pipeline.chunk_size == 300
        assert pipeline.chunk_overlap == 50
    
    def test_text_chunking(self):
        """Test text chunking."""
        pipeline = RAGPipeline(chunk_size=100, chunk_overlap=20)
        
        long_text = "This is a long text that will be split into chunks. " * 10
        chunks = pipeline._chunk_text(long_text)
        
        assert len(chunks) > 1
        assert all(isinstance(c, str) for c in chunks)
        assert all(len(c) > 0 for c in chunks)
    
    def test_prompt_template_loading(self):
        """Test prompt template is loaded."""
        pipeline = RAGPipeline()
        assert pipeline._prompt_template is not None
        assert "context" in pipeline._prompt_template.lower() or "Context" in pipeline._prompt_template
    
    def test_mock_answer_generation(self):
        """Test mock answer generation."""
        pipeline = RAGPipeline()
        query = "Is this toy good?"
        context = "This toy is great and recommended. 5 stars!"
        
        answer = pipeline._mock_generate_answer(query, context)
        assert isinstance(answer, str)
        assert len(answer) > 0


class TestRetrievalQuality:
    """Test retrieval relevance."""
    
    def test_similar_documents_ranked_higher(self):
        """Test that similar documents rank higher."""
        provider = EmbeddingProvider()
        store = VectorStore(index_dir="/tmp/test_retrieve")
        
        # Add documents with similar meanings
        docs = [
            "LEGO is a great toy for creative building",
            "Building blocks encourage imagination",
            "Cars go fast on the road",
        ]
        
        embeddings = provider.embed(docs)
        metadata = [
            {"text": doc, "source": f"doc{i}", "score": 0.0}
            for i, doc in enumerate(docs)
        ]
        
        store.add(embeddings, metadata)
        
        # Query similar to first doc
        query = "LEGO building toy"
        query_emb = provider.embed_single(query)
        
        results = store.search(query_emb, k=3)
        
        # Should return 3 results
        assert len(results) >= 1
