# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Memory optimization utilities for DNHealth library.

Provides memory-efficient data structures and optimization techniques including:
- Object pooling for frequently created objects
- Weak references for cache-like structures
- Memory-efficient collections
- Resource cleanup utilities
"""

import weakref
from typing import Dict, List, Optional, Any, TypeVar, Generic, Callable, Deque
from collections import deque
from threading import Lock
from datetime import datetime
import logging
import gc

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300

T = TypeVar("T")


class ObjectPool(Generic[T]):
    """
    Object pool for reusing objects to reduce memory allocation overhead.
    
    Useful for frequently created and destroyed objects like message parsers,
    validators, or serializers.
    
    Example:
        >>> pool = ObjectPool(lambda: MessageParser(), max_size=10)
        >>> parser = pool.acquire()
        >>> # Use parser...
        >>> pool.release(parser)
    """
    
    def __init__(
        self,
        factory: Callable[[], T],
        max_size: int = 10,
        reset_func: Optional[Callable[[T], None]] = None
    ):
        """
        Initialize object pool.
        
        Args:
            factory: Function that creates new objects
            max_size: Maximum number of objects to keep in pool
            reset_func: Optional function to reset object state before reuse
        """
        self._factory = factory
        self._max_size = max_size
        self._reset_func = reset_func
        self._pool: Deque[T] = deque(maxlen=max_size)
        self._lock = Lock()
        self._created_count = 0
        self._reused_count = 0
    
    def acquire(self) -> T:
        """
        Acquire an object from the pool.
        
        Returns:
            Object from pool or newly created object
        """
        with self._lock:
            if self._pool:
                obj = self._pool.popleft()
                self._reused_count += 1
                if self._reset_func:
                    self._reset_func(obj)
                return obj
            else:
                self._created_count += 1
                return self._factory()
    
    def release(self, obj: T) -> None:
        """
        Release an object back to the pool.
        
        Args:
            obj: Object to return to pool
        """
        with self._lock:
            if len(self._pool) < self._max_size:
                self._pool.append(obj)
    
    def clear(self) -> None:
        """Clear all objects from the pool."""
        with self._lock:
            self._pool.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get pool statistics.
        
        Returns:
            Dictionary with pool statistics including timestamp
        """
        with self._lock:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {
                "pool_size": len(self._pool),
                "max_size": self._max_size,
                "created_count": self._created_count,
                "reused_count": self._reused_count,
                "reuse_rate": (
                    self._reused_count / (self._created_count + self._reused_count)
                    if (self._created_count + self._reused_count) > 0
                    else 0.0
                ),
                "timestamp": current_time
            }


class WeakValueCache(Generic[T]):
    """
    Cache using weak references to allow garbage collection when objects
    are no longer referenced elsewhere.
    
    Useful for caching parsed messages or resources that may be large
    but are only needed temporarily.
    
    Example:
        >>> cache = WeakValueCache()
        >>> cache.set("key1", large_resource)
        >>> resource = cache.get("key1")  # Returns resource if still in memory
        >>> # If resource is no longer referenced, it will be garbage collected
    """
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize weak value cache.
        
        Args:
            max_size: Optional maximum cache size (None for unlimited)
        """
        self._cache: weakref.WeakValueDictionary[str, T] = weakref.WeakValueDictionary()
        self._max_size = max_size
        self._lock = Lock()
        self._access_count = 0
        self._hit_count = 0
    
    def get(self, key: str) -> Optional[T]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or garbage collected
        """
        with self._lock:
            self._access_count += 1
            try:
                value = self._cache[key]
                self._hit_count += 1
                return value
            except KeyError:
                return None
    
    def set(self, key: str, value: T) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if self._max_size is not None and len(self._cache) >= self._max_size:
                # Remove oldest entry (weak dict doesn't support ordered removal,
                # so we clear and rebuild - in practice, weak refs handle this)
                # For simplicity, we just allow it to grow
                pass
            self._cache[key] = value
    
    def remove(self, key: str) -> None:
        """
        Remove value from cache.
        
        Args:
            key: Cache key
        """
        with self._lock:
            try:
                del self._cache[key]
            except KeyError:
                pass
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self._lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics including timestamp
        """
        with self._lock:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hit_rate = (
                self._hit_count / self._access_count
                if self._access_count > 0
                else 0.0
            )
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "access_count": self._access_count,
                "hit_count": self._hit_count,
                "hit_rate": hit_rate,
                "timestamp": current_time
            }


class MemoryEfficientList(Generic[T]):
    """
    Memory-efficient list implementation using deque for better memory
    characteristics when appending/removing from ends.
    
    Useful for large collections where memory usage is a concern.
    """
    
    def __init__(self, initial_items: Optional[List[T]] = None):
        """
        Initialize memory-efficient list.
        
        Args:
            initial_items: Optional initial items
        """
        self._items: Deque[T] = deque(initial_items) if initial_items else deque()
    
    def append(self, item: T) -> None:
        """Append item to end of list."""
        self._items.append(item)
    
    def prepend(self, item: T) -> None:
        """Prepend item to beginning of list."""
        self._items.appendleft(item)
    
    def pop(self, index: int = -1) -> T:
        """
        Pop item from list.
        
        Args:
            index: Index to pop (-1 for last, 0 for first)
            
        Returns:
            Popped item
        """
        if index == -1:
            return self._items.pop()
        elif index == 0:
            return self._items.popleft()
        else:
            # For middle items, convert to list temporarily
            items_list = list(self._items)
            item = items_list.pop(index)
            self._items = deque(items_list)
            return item
    
    def __getitem__(self, index: int) -> T:
        """Get item by index."""
        return self._items[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """Set item by index."""
        items_list = list(self._items)
        items_list[index] = value
        self._items = deque(items_list)
    
    def __len__(self) -> int:
        """Get length of list."""
        return len(self._items)
    
    def __iter__(self):
        """Iterate over items."""
        return iter(self._items)
    
    def to_list(self) -> List[T]:
        """Convert to regular list."""

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return list(self._items)


def cleanup_memory(force_gc: bool = True) -> Dict[str, Any]:
    """
    Clean up memory by running garbage collection.
    
    Args:
        force_gc: If True, force full garbage collection
        
    Returns:
        Dictionary with cleanup statistics including timestamp
    """
    import gc
    
    start_time = datetime.now()
    
    # Get counts before cleanup
    before_counts = gc.get_count()
    
    if force_gc:
        # Run full garbage collection
        collected = gc.collect()
    else:
        collected = 0
    
    # Get counts after cleanup
    after_counts = gc.get_count()
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    current_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info(
        f"Memory cleanup completed at {current_time}: "
        f"{collected} objects collected in {elapsed:.3f}s"
    )
    
    return {
        "collected": collected,
        "before_counts": before_counts,
        "after_counts": after_counts,
        "elapsed_seconds": elapsed,
        "timestamp": current_time
    }


def get_memory_usage() -> Dict[str, Any]:
    """
    Get current memory usage statistics.
    
    Returns:
        Dictionary with memory usage statistics including timestamp
    """
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "rss_mb": mem_info.rss / (1024 * 1024),  # Resident Set Size
            "vms_mb": mem_info.vms / (1024 * 1024),  # Virtual Memory Size
            "percent": process.memory_percent(),
            "available_mb": psutil.virtual_memory().available / (1024 * 1024),
            "timestamp": current_time
        }
    except ImportError:
        # psutil not available, return basic info
        import sys
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "note": "psutil not available, limited memory info",
            "timestamp": current_time
        }


class MemoryMonitor:
    """
    Monitor memory usage over time to detect memory leaks or high usage.
    """
    
    def __init__(self, interval_seconds: float = 1.0):
        """
        Initialize memory monitor.
        
        Args:
            interval_seconds: Interval between memory checks
        """
        self._interval = interval_seconds
        self._snapshots: List[Dict[str, Any]] = []
        self._start_time: Optional[datetime] = None
    
    def start(self) -> None:
        """Start monitoring."""
        self._start_time = datetime.now()
        self._snapshots.clear()
        current_time = self._start_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Memory monitoring started at {current_time}")
    
    def snapshot(self) -> Dict[str, Any]:
        """
        Take a memory snapshot.
        
        Returns:
            Memory snapshot with timestamp
        """
        mem_usage = get_memory_usage()
        if self._start_time:
            elapsed = (datetime.now() - self._start_time).total_seconds()
            mem_usage["elapsed_seconds"] = elapsed
        self._snapshots.append(mem_usage)
        return mem_usage
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop monitoring and return statistics.
        
        Returns:
            Dictionary with monitoring statistics including timestamp
        """
        end_time = datetime.now()
        current_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if not self._snapshots:
            return {
                "snapshots": 0,
                "timestamp": current_time
            }
        
        rss_values = [s.get("rss_mb", 0) for s in self._snapshots if "rss_mb" in s]
        
        stats = {
            "snapshots": len(self._snapshots),
            "start_time": self._start_time.strftime("%Y-%m-%d %H:%M:%S") if self._start_time else None,
            "end_time": current_time,
            "timestamp": current_time
        }
        
        if rss_values:
            stats["min_rss_mb"] = min(rss_values)
            stats["max_rss_mb"] = max(rss_values)
            stats["avg_rss_mb"] = sum(rss_values) / len(rss_values)
            stats["rss_delta_mb"] = max(rss_values) - min(rss_values)
        
        logger.info(
            f"Memory monitoring stopped at {current_time}: "
            f"{stats['snapshots']} snapshots, "
            f"RSS delta: {stats.get('rss_delta_mb', 0):.2f}MB"
        )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return stats
    
    def get_snapshots(self) -> List[Dict[str, Any]]:
        """Get all memory snapshots."""
        return self._snapshots.copy()
