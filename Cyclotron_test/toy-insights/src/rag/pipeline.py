"""
RAG pipeline: retrieval, augmentation, and answer generation.
Orchestrates embedding, vector search, prompt assembly, and mock LLM.
"""
import os
import logging
from typing import Tuple
from datetime import datetime

from sqlalchemy.orm import Session

from src.rag.embeddings import EmbeddingProvider
from src.rag.vectorstore import VectorStore
from src.api.models import SearchResult

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Orchestrates the RAG workflow."""
    
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        """
        Initialize RAG pipeline.
        
        Args:
            chunk_size: Characters per chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = EmbeddingProvider()
        self.vectorstore = VectorStore()
        self._prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load prompt template from file."""
        template_file = os.path.join(os.path.dirname(__file__), "prompt.txt")
        if os.path.exists(template_file):
            with open(template_file) as f:
                return f.read()
        return self._default_prompt_template()
    
    def _default_prompt_template(self) -> str:
        """Default prompt if template file missing."""
        return """You are a helpful toy product expert. Answer the user's question based on the provided context.

                    Context:
                    {context}

                    Question: {query}

                    Answer:
                """
    
    def _chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping chunks."""
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i : i + self.chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks if chunks else [text]
    
    def ingest_documents(self, file_paths: list[str], db: Session) -> Tuple[int, int]:
        """
        Ingest documents from file paths.
        
        Args:
            file_paths: List of file paths to read
            db: SQLAlchemy session
            
        Returns:
            Tuple of (document_count, chunk_count)
        """
        from src.db.orm import Document, Chunk
        
        doc_count = 0
        chunk_count = 0
        embeddings_to_add = []
        metadata_to_add = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                continue
            
            with open(file_path) as f:
                content = f.read()
            
            # Create document record
            doc = Document(
                source=file_path,
                content=content,
                ingested_at=datetime.utcnow(),
            )
            db.add(doc)
            db.flush()  # Get document ID
            doc_count += 1
            
            # Split into chunks
            chunks_text = self._chunk_text(content)
            
            for i, chunk_text in enumerate(chunks_text):
                # Create chunk record
                chunk = Chunk(
                    document_id=doc.id,
                    text=chunk_text,
                    chunk_index=i,
                )
                db.add(chunk)
                db.flush()
                chunk_count += 1
                
                # Prepare embedding
                embedding = self.embeddings.embed_single(chunk_text)
                embeddings_to_add.append(embedding)
                metadata_to_add.append({
                    "chunk_id": chunk.id,
                    "document_id": doc.id,
                    "source": file_path,
                    "text": chunk_text[:100],  # Preview
                })
        
        # Add to vector store
        if embeddings_to_add:
            self.vectorstore.add(embeddings_to_add, metadata_to_add)
        
        db.commit()
        logger.info(f"Ingested {doc_count} documents, {chunk_count} chunks")
        
        return doc_count, chunk_count
    
    def search(self, query: str, k: int = 5, db: Session = None) -> list[SearchResult]:
        """
        Search vector store for relevant chunks.
        
        Args:
            query: Search query
            k: Number of results
            db: SQLAlchemy session (optional)
            
        Returns:
            List of SearchResult objects
        """
        # Embed query
        query_embedding = self.embeddings.embed_single(query)
        
        # Search vector store
        results = self.vectorstore.search(query_embedding, k)
        
        # Convert to SearchResult objects
        search_results = []
        for result in results:
            search_results.append(
                SearchResult(
                    score=result.get("score", 0.0),
                    content=result.get("text", ""),
                    document_id=result.get("document_id", 0),
                    source=result.get("source", ""),
                )
            )
        
        return search_results
    
    def chat(self, query: str, k: int = 5, db: Session = None) -> Tuple[str, list[dict]]:
        """
        RAG chat: retrieve context and generate answer.
        
        Args:
            query: User query
            k: Number of chunks to retrieve
            db: SQLAlchemy session (optional)
            
        Returns:
            Tuple of (answer, sources)
        """
        # Retrieve relevant chunks
        search_results = self.search(query, k, db)
        
        if not search_results:
            return "I don't have enough information to answer that.", []
        
        # Build context from search results
        context_parts = []
        sources = []
        
        for i, result in enumerate(search_results):
            context_parts.append(f"[{i+1}] {result.content}")
            sources.append({
                "document_id": result.document_id,
                "source": result.source,
                "score": result.score,
                "snippet": result.content[:150],
            })
        
        context = "\n".join(context_parts)
        
        # Build prompt
        prompt = self._prompt_template.format(context=context, query=query)
        
        # Generate answer (mock LLM)
        answer = self._mock_generate_answer(query, context)
        
        return answer, sources
    
    def _mock_generate_answer(self, query: str, context: str) -> str:
        """
        Mock LLM answer generation.
        Replace with real LLM call (e.g., OpenAI, HF, etc).
        """
        # Simple heuristic answer
        keywords = query.lower().split()
        context_lower = context.lower()
        
        if any(word in context_lower for word in ["recommend", "best", "great"]):
            return f"Based on the toy reviews, this product receives positive feedback. The provided information suggests it's a quality toy. {context[:200]}..."
        elif any(word in context_lower for word in ["problem", "issue", "broken", "bad"]):
            return f"According to the reviews, there are some concerns mentioned. Please refer to the source materials for details: {context[:200]}..."
        else:
            return f"Based on the available information about toys and reviews: {context[:200]}..."
    
    def store_transcript(
        self,
        query: str,
        answer: str,
        sources: list[dict],
        db: Session,
    ):
        """Store chat transcript in database."""
        from src.db.orm import ChatTranscript
        import json
        
        transcript = ChatTranscript(
            query=query,
            answer=answer,
            sources=json.dumps(sources),
            timestamp=datetime.utcnow(),
        )
        db.add(transcript)
        db.commit()
