# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Message queuing utilities for DNHealth library.

Provides thread-safe message queues with support for priority queuing,
FIFO/LIFO ordering, and message statistics tracking.
All queue operations include timestamps in logs for traceability.
"""

import heapq
import threading
from collections import deque
from datetime import datetime
from enum import Enum
from typing import Any, Deque, Dict, List, Optional, Tuple

from dnhealth.errors import DNHealthError
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class QueueOrder(Enum):
    """Queue ordering strategies."""

    FIFO = "fifo"  # First In, First Out
    LIFO = "lifo"  # Last In, First Out


class QueueError(DNHealthError):
    """Base exception for queue operations."""

    pass


class QueueFullError(QueueError):
    """Raised when queue is full and cannot accept more messages."""

    pass


class QueueEmptyError(QueueError):
    """Raised when queue is empty and no messages are available."""

    pass


class QueuedMessage:
    """
    Represents a message in the queue with metadata.

    Attributes:
        message: The actual message content
        priority: Priority level (lower number = higher priority)
        timestamp: When the message was enqueued
        message_id: Unique identifier for the message
        metadata: Optional additional metadata
    """

    def __init__(
        self,
        message: Any,
        priority: int = 0,
        message_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a queued message.

        Args:
            message: The message content
            priority: Priority level (default: 0, lower = higher priority)
            message_id: Optional unique identifier
            metadata: Optional additional metadata
        """
        self.message = message
        self.priority = priority
        self.timestamp = datetime.now()
        self.message_id = message_id or f"msg_{id(self)}"
        self.metadata = metadata or {}

    def __lt__(self, other: "QueuedMessage") -> bool:
        """Compare messages for priority queue ordering."""
        if self.priority != other.priority:
            return self.priority < other.priority
        # If priorities are equal, older messages come first
        return self.timestamp < other.timestamp

    def __repr__(self) -> str:
        """String representation of the message."""
        return (
            f"QueuedMessage(id={self.message_id}, priority={self.priority}, "
            f"timestamp={self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
        )


class MessageQueue:
    """
    Thread-safe message queue with support for priority and ordering strategies.

    Provides FIFO/LIFO ordering and optional priority queuing.
    All operations are logged with timestamps for audit purposes.
    """

    def __init__(
        self,
        maxsize: Optional[int] = None,
        order: QueueOrder = QueueOrder.FIFO,
        priority_enabled: bool = False,
        name: Optional[str] = None,
    ):
        """
        Initialize a message queue.

        Args:
            maxsize: Maximum queue size (None for unlimited)
            order: Queue ordering strategy (FIFO or LIFO)
            priority_enabled: Enable priority queuing (default: False)
            name: Optional name for the queue (for logging)
        """
        self.maxsize = maxsize
        self.order = order
        self.priority_enabled = priority_enabled
        self.name = name or "MessageQueue"
        self._lock = threading.RLock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

        # Statistics tracking
        self._stats = {
            "enqueued": 0,
            "dequeued": 0,
            "dropped": 0,
            "current_size": 0,
            "max_size_reached": 0,
        }

        # Choose appropriate data structure
        if priority_enabled:
            # Use heap for priority queue
            self._queue: List[QueuedMessage] = []
        else:
            # Use deque for FIFO/LIFO
            self._queue: Deque[QueuedMessage] = deque()

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"MessageQueue '{self.name}' initialized "
            f"(maxsize={maxsize}, order={order.value}, priority={priority_enabled})"
        )

    def enqueue(
        self,
        message: Any,
        priority: int = 0,
        message_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        block: bool = True,
        timeout: Optional[float] = None,
    ) -> bool:
        """
        Enqueue a message.

        Args:
            message: The message to enqueue
            priority: Priority level (only used if priority_enabled=True)
            message_id: Optional unique identifier
            metadata: Optional additional metadata
            block: If True, block until space is available
            timeout: Maximum time to wait if block=True (None = wait indefinitely)

        Returns:
            True if message was enqueued, False if queue was full and block=False

        Raises:
            QueueFullError: If queue is full and block=False
        """
        queued_msg = QueuedMessage(message, priority, message_id, metadata)

        with self._not_full:
            # Check if queue is full
            if self.maxsize is not None and len(self._queue) >= self.maxsize:
                if not block:
                    self._stats["dropped"] += 1
                    logger.warning(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                        f"Queue '{self.name}' is full, message dropped "
                        f"(id={queued_msg.message_id})"
                    )
                    raise QueueFullError(
                        f"Queue '{self.name}' is full (maxsize={self.maxsize})"
                    )

                # Wait for space using condition variable
                if timeout:
                    import time

                    start_time = time.time()
                    while len(self._queue) >= self.maxsize:
                        remaining_time = timeout - (time.time() - start_time)
                        if remaining_time <= 0:
                            self._stats["dropped"] += 1
                            raise QueueFullError(
                                f"Queue '{self.name}' is full after timeout"
                            )
                        self._not_full.wait(timeout=min(remaining_time, 0.1))
                else:
                    # Wait indefinitely
                    while len(self._queue) >= self.maxsize:
                        self._not_full.wait()

            # Add message to queue
            if self.priority_enabled:
                heapq.heappush(self._queue, queued_msg)
            else:
                # For FIFO: append to right, popleft from left
                # For LIFO: append to right, pop from right (last in, first out)
                self._queue.append(queued_msg)

            self._stats["enqueued"] += 1
            self._stats["current_size"] = len(self._queue)
            if self.maxsize and len(self._queue) >= self.maxsize:
                self._stats["max_size_reached"] += 1

            logger.debug(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"Message enqueued to '{self.name}' "
                f"(id={queued_msg.message_id}, size={len(self._queue)})"
            )

            # Notify waiting consumers
            self._not_empty.notify()

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

        return True

    def dequeue(
        self, block: bool = True, timeout: Optional[float] = None
    ) -> Optional[QueuedMessage]:
        """
        Dequeue a message.

        Args:
            block: If True, block until a message is available
            timeout: Maximum time to wait if block=True (None = wait indefinitely)

        Returns:
            QueuedMessage if available, None if queue is empty and block=False

        Raises:
            QueueEmptyError: If queue is empty and block=False
        """
        with self._not_empty:
            if len(self._queue) == 0:
                if not block:
                    raise QueueEmptyError(f"Queue '{self.name}' is empty")

                # Wait for message using condition variable
                if timeout:
                    import time

                    start_time = time.time()
                    while len(self._queue) == 0:
                        remaining_time = timeout - (time.time() - start_time)
                        if remaining_time <= 0:
                            raise QueueEmptyError(
                                f"Queue '{self.name}' is empty after timeout"
                            )
                        self._not_empty.wait(timeout=min(remaining_time, 0.1))
                else:
                    # Wait indefinitely
                    while len(self._queue) == 0:
                        self._not_empty.wait()

            # Remove message from queue
            if self.priority_enabled:
                queued_msg = heapq.heappop(self._queue)
            else:
                if self.order == QueueOrder.FIFO:
                    queued_msg = self._queue.popleft()
                else:  # LIFO - pop from right (last in, first out)
                    queued_msg = self._queue.pop()

            self._stats["dequeued"] += 1
            self._stats["current_size"] = len(self._queue)

            logger.debug(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"Message dequeued from '{self.name}' "
                f"(id={queued_msg.message_id}, size={len(self._queue)})"
            )

            # Notify waiting producers
            self._not_full.notify()

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

        return queued_msg

    def peek(self) -> Optional[QueuedMessage]:
        """
        Peek at the next message without removing it.

        Returns:
            QueuedMessage if available, None if queue is empty
        """
        with self._lock:
            if len(self._queue) == 0:
                return None

            if self.priority_enabled:
                # For priority queue, return the highest priority item
                return self._queue[0]
            else:
                if self.order == QueueOrder.FIFO:
                    return self._queue[0]
                else:  # LIFO
                    return self._queue[-1]

    def size(self) -> int:
        """
        Get current queue size.

        Returns:
            Number of messages in the queue
        """
        with self._lock:
            return len(self._queue)

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        Returns:
            True if queue is empty, False otherwise
        """
        with self._lock:
            return len(self._queue) == 0

    def is_full(self) -> bool:
        """
        Check if queue is full.

        Returns:
            True if queue is full, False otherwise
        """
        with self._lock:
            if self.maxsize is None:
                return False
            return len(self._queue) >= self.maxsize

    def clear(self) -> int:
        """
        Clear all messages from the queue.

        Returns:
            Number of messages cleared
        """
        with self._lock:
            count = len(self._queue)
            if self.priority_enabled:
                self._queue.clear()
            else:
                self._queue.clear()
            self._stats["current_size"] = 0

            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"Queue '{self.name}' cleared ({count} messages removed)"
            )

        return count


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    def get_stats(self) -> Dict[str, Any]:
        """
        Get queue statistics.

        Returns:
            Dictionary with queue statistics including timestamps
        """
        with self._lock:
            stats = self._stats.copy()
            stats["current_size"] = len(self._queue)
            stats["timestamp"] = datetime.now().isoformat()
            stats["maxsize"] = self.maxsize
            stats["order"] = self.order.value
            stats["priority_enabled"] = self.priority_enabled
            return stats

    def reset_stats(self) -> None:
        """Reset queue statistics."""
        with self._lock:
            self._stats = {
                "enqueued": 0,
                "dequeued": 0,
                "dropped": 0,
                "current_size": len(self._queue),
                "max_size_reached": 0,
            }
            logger.debug(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"Statistics reset for queue '{self.name}'"
            )
