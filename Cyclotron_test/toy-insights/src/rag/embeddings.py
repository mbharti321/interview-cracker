"""
Embedding utilities using Hugging Face models.
Provides sentence transformers for text-to-vector conversion.
"""
import os
import logging
from typing import Union

logger = logging.getLogger(__name__)


class EmbeddingProvider:
    """Wrapper for embedding models."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding provider.
        
        Args:
            model_name: Hugging Face model identifier
        """
        self.model_name = model_name
        self._model = None
    
    def _load_model(self):
        """Lazy-load the embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                logger.error("sentence-transformers not installed. Using mock embeddings.")
                self._model = None
    
    def embed(self, text: Union[str, list[str]]) -> list[list[float]]:
        """
        Embed text(s) into vectors.
        
        Args:
            text: Single string or list of strings
            
        Returns:
            List of embedding vectors (list of floats)
        """
        self._load_model()
        
        if self._model is None:
            # Mock embedding for testing/demo
            import hashlib
            if isinstance(text, str):
                text = [text]
            embeddings = []
            for t in text:
                # Deterministic mock embedding based on text hash
                hash_obj = hashlib.md5(t.encode())
                hash_int = int(hash_obj.hexdigest(), 16)
                embedding = [(hash_int >> (i * 8)) % 256 / 256.0 for i in range(384)]
                embeddings.append(embedding)
            return embeddings
        
        if isinstance(text, str):
            return [self._model.encode(text).tolist()]
        else:
            return self._model.encode(text).tolist()
    
    def embed_single(self, text: str) -> list[float]:
        """Embed a single text string."""
        return self.embed(text)[0]
