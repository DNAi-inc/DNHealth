# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Caching utilities for parsed FHIR resources.
logger = logging.getLogger(__name__)

Provides caching functionality to improve performance when parsing the same
FHIR resources multiple times. Includes timestamp tracking for cache operations.
"""

import hashlib
import json
from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar
from threading import Lock

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.util.logging import get_logger

T = TypeVar("T", bound=FHIRResource)

logger = get_logger(__name__)


class ResourceCache:
    """
    Cache for parsed FHIR resources.
    
    Provides in-memory caching of parsed FHIR resources to avoid re-parsing
    the same JSON/XML content. Cache entries include timestamps for tracking.
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: Optional[int] = None):
        """
        Initialize the resource cache.

        Args:
            max_size: Maximum number of entries in cache (default: 1000)
            ttl_seconds: Time-to-live for cache entries in seconds (None = no expiration)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._lock = Lock()
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ResourceCache initialized with max_size={max_size}, ttl={ttl_seconds}s")

    def _generate_key(self, content: str) -> str:
        """
        Generate a cache key from content.

        Args:
            content: JSON or XML string content

        Returns:
            SHA256 hash of the content
        """

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """
        Check if a cache entry has expired.

        Args:
            entry: Cache entry dictionary

        Returns:
            True if expired, False otherwise
        """
        if self._ttl_seconds is None:
            return False
        cached_time = entry.get("cached_at")
        if cached_time is None:
            return True
        elapsed = (datetime.now() - cached_time).total_seconds()
        return elapsed > self._ttl_seconds

    def get(self, content: str, resource_type: Optional[Type[T]] = None) -> Optional[T]:
        """
        Get a cached resource.

        Args:
            content: JSON or XML string content
            resource_type: Optional resource type hint

        Returns:
            Cached resource if found and not expired, None otherwise
        """
        cache_key = self._generate_key(content)
        
        with self._lock:
            if cache_key not in self._cache:
                logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cache miss for key {cache_key[:16]}...")
                return None

            entry = self._cache[cache_key]
            
            # Check expiration
            if self._is_expired(entry):
                logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cache entry expired for key {cache_key[:16]}...")
                del self._cache[cache_key]
                return None

            # Verify resource type matches if provided
            if resource_type is not None:
                cached_type = entry.get("resource_type")
                if cached_type != resource_type.__name__:
                    logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cache type mismatch for key {cache_key[:16]}...")
                    return None

            logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cache hit for key {cache_key[:16]}...")
            return entry["resource"]

    def put(self, content: str, resource: T) -> None:
        """
        Store a resource in the cache.

        Args:
            content: JSON or XML string content
            resource: Parsed FHIR resource to cache
        """
        cache_key = self._generate_key(content)
        
        with self._lock:
            # Evict oldest entry if cache is full
            if len(self._cache) >= self._max_size and cache_key not in self._cache:
                # Remove oldest entry (simple FIFO)
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Evicted cache entry {oldest_key[:16]}...")

            self._cache[cache_key] = {
                "resource": resource,
                "resource_type": resource.__class__.__name__,
                "cached_at": datetime.now(),
            }
            logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cached resource {resource.__class__.__name__} with key {cache_key[:16]}...")

    def clear(self) -> None:
        """
        Clear all cache entries.
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cleared {count} cache entries")

    def size(self) -> int:
        """
        Get the current cache size.

        Returns:
            Number of entries in cache
        """
        with self._lock:
            return len(self._cache)

    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics including size, max_size, ttl
        """
        with self._lock:
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "ttl_seconds": self._ttl_seconds,
                "current_time": datetime.now().isoformat(),
            }


# Global default cache instance
_default_cache: Optional[ResourceCache] = None
_cache_lock = Lock()



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def get_default_cache() -> ResourceCache:
    """
    Get the default global cache instance.

    Returns:
        Default ResourceCache instance
    """
    global _default_cache
    with _cache_lock:
        if _default_cache is None:
            _default_cache = ResourceCache()
        return _default_cache


def set_default_cache(cache: ResourceCache) -> None:
    """
    Set the default global cache instance.

    Args:
        cache: ResourceCache instance to use as default
    """
    global _default_cache
    with _cache_lock:
        _default_cache = cache
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Default cache instance updated")
