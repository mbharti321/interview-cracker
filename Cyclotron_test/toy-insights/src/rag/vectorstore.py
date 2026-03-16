"""
Vector store abstraction using FAISS with local persistence.
Handles document indexing and similarity search.
"""
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class VectorStore:
    """FAISS-based vector store with local persistence."""
    
    def __init__(self, index_dir: str = "data/vectors", embedding_dim: int = 384):
        """
        Initialize vector store.
        
        Args:
            index_dir: Directory to persist index
            embedding_dim: Dimension of embeddings
        """
        self.index_dir = index_dir
        self.embedding_dim = embedding_dim
        self.metadata_file = os.path.join(index_dir, "metadata.json")
        
        # Create index dir if needed
        os.makedirs(index_dir, exist_ok=True)
        
        self._index = None
        self._metadata = []
        self._load_index()
    
    def _load_index(self):
        """Load existing index or create new one."""
        try:
            import faiss
            index_file = os.path.join(self.index_dir, "index.faiss")
            if os.path.exists(index_file):
                self._index = faiss.read_index(index_file)
                logger.info(f"Loaded FAISS index with {self._index.ntotal} vectors")
            else:
                self._index = faiss.IndexFlatL2(self.embedding_dim)
                logger.info("Created new FAISS index")
            
            # Load metadata
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file) as f:
                    self._metadata = json.load(f)
        except ImportError:
            logger.warning("FAISS not installed. Using mock vector store.")
            self._index = None
    
    def add(self, embeddings: list[list[float]], metadata: list[dict]):
        """
        Add embeddings and metadata to index.
        
        Args:
            embeddings: List of embedding vectors
            metadata: List of metadata dicts (one per embedding)
        """
        if self._index is None:
            # Mock: just store metadata
            self._metadata.extend(metadata)
            self._save_metadata()
            return
        
        import faiss
        import numpy as np
        
        embeddings_array = np.array(embeddings, dtype=np.float32)
        self._index.add(embeddings_array)
        self._metadata.extend(metadata)
        
        self._save_index()
        self._save_metadata()
        logger.info(f"Added {len(embeddings)} embeddings to index")
    
    def search(self, query_embedding: list[float], k: int = 5) -> list[dict]:
        """
        Search for similar embeddings.
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            
        Returns:
            List of metadata dicts with distance scores
        """
        if self._index is None or not self._metadata:
            # Mock: return first k metadata items
            return self._metadata[:k]
        
        import numpy as np
        query_array = np.array([query_embedding], dtype=np.float32)
        distances, indices = self._index.search(query_array, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self._metadata):
                result = self._metadata[idx].copy()
                result["score"] = 1.0 / (1.0 + distances[0][i])  # Convert distance to similarity
                results.append(result)
        
        return results
    
    def _save_index(self):
        """Persist FAISS index to disk."""
        if self._index is not None:
            import faiss
            index_file = os.path.join(self.index_dir, "index.faiss")
            faiss.write_index(self._index, index_file)
    
    def _save_metadata(self):
        """Persist metadata to JSON."""
        with open(self.metadata_file, "w") as f:
            json.dump(self._metadata, f, indent=2)
