"""
Redis caching utilities with TTL support.
"""
import os
import json
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    """Simple Redis wrapper with TTL support."""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """
        Initialize Redis client.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
        """
        self.host = host
        self.port = port
        self.db = db
        self._client = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
            )
            self._client.ping()
            logger.info(f"Connected to Redis at {self.host}:{self.port}")
        except ImportError:
            logger.warning("redis package not installed. Using in-memory mock cache.")
            self._client = None
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Using in-memory mock.")
            self._client = None
    
    def get(self, key: str) -> str | None:
        """Get value by key."""
        if self._client is None:
            return self._mock_cache.get(key)
        try:
            return self._client.get(key)
        except Exception as e:
            logger.error(f"Redis get failed: {e}")
            return None
    
    def set(self, key: str, value: str, ttl: int = 300):
        """
        Set value with TTL (Time To Live).
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds (default 5 minutes)
        """
        if self._client is None:
            self._mock_cache[key] = value
            return
        try:
            self._client.setex(key, ttl, value)
        except Exception as e:
            logger.error(f"Redis set failed: {e}")
    
    def delete(self, key: str):
        """Delete key."""
        if self._client is None:
            self._mock_cache.pop(key, None)
            return
        try:
            self._client.delete(key)
        except Exception as e:
            logger.error(f"Redis delete failed: {e}")
    
    def clear(self):
        """Clear all keys (use carefully)."""
        if self._client is None:
            self._mock_cache.clear()
            return
        try:
            self._client.flushdb()
        except Exception as e:
            logger.error(f"Redis flushdb failed: {e}")
    
    # In-memory mock cache (fallback)
    _mock_cache = {}


# Global Redis client instance
_redis_client: RedisClient | None = None


def get_redis_client() -> RedisClient:
    """Get or create Redis client singleton."""
    global _redis_client
    if _redis_client is None:
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", "6379"))
        _redis_client = RedisClient(host=host, port=port)
    return _redis_client
