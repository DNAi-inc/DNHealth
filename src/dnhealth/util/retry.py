# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Retry mechanism utilities for DNHealth library.

Provides configurable retry strategies with various backoff policies for
robust handling of transient failures in parsing, validation, and network operations.
All retry operations include timestamps in logs for traceability.
"""

import time
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from functools import wraps

from dnhealth.errors import DNHealthError
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class RetryStrategy(Enum):
    """Types of retry strategies."""

    FIXED_DELAY = "fixed_delay"
    LINEAR_BACKOFF = "linear_backoff"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    EXPONENTIAL_BACKOFF_WITH_JITTER = "exponential_backoff_with_jitter"


class RetryCondition:
    """
    Defines conditions for when to retry an operation.

    Can retry on specific exceptions, return values, or custom conditions.
    """

    def __init__(
        self,
        retry_on_exceptions: Optional[List[Type[Exception]]] = None,
        retry_on_return_value: Optional[Callable[[Any], bool]] = None,
        retry_on_custom: Optional[Callable[[Exception, Any], bool]] = None,
    ):
        """
        Initialize retry condition.

        Args:
            retry_on_exceptions: List of exception types to retry on.
                               If None, retries on all exceptions.
            retry_on_return_value: Function that returns True if retry needed based on return value.
            retry_on_custom: Custom function that takes (exception, return_value) and returns bool.
        """
        self.retry_on_exceptions = retry_on_exceptions
        self.retry_on_return_value = retry_on_return_value
        self.retry_on_custom = retry_on_custom

    def should_retry(
        self, exception: Optional[Exception] = None, return_value: Any = None
    ) -> bool:
        """
        Determine if operation should be retried.

        Args:
            exception: Exception that was raised (if any)
            return_value: Return value from the operation (if no exception)

        Returns:
            True if operation should be retried, False otherwise
        """
        # Custom condition takes precedence
        if self.retry_on_custom:
            return self.retry_on_custom(exception, return_value)

        # Check return value condition
        if exception is None and self.retry_on_return_value:
            return self.retry_on_return_value(return_value)

        # Check exception condition
        if exception is not None:
            if self.retry_on_exceptions is None:
                # Retry on all exceptions by default
                return True
            return any(isinstance(exception, exc_type) for exc_type in self.retry_on_exceptions)

        return False


class RetryHandler:
    """
    Retry handler for operations that may fail transiently.

    Provides configurable retry strategies with various backoff policies.
    All retry attempts are logged with timestamps for audit and debugging purposes.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        multiplier: float = 2.0,
        jitter: bool = False,
        condition: Optional[RetryCondition] = None,
        timeout: Optional[float] = None,
    ):
        """
        Initialize retry handler.

        Args:
            max_attempts: Maximum number of retry attempts (default: 3)
            strategy: Retry strategy to use (default: exponential backoff)
            initial_delay: Initial delay in seconds before first retry (default: 1.0)
            max_delay: Maximum delay between retries in seconds (default: 60.0)
            multiplier: Multiplier for exponential/linear backoff (default: 2.0)
            jitter: Whether to add random jitter to delays (default: False)
            condition: Retry condition - when to retry (default: retry on all exceptions)
            timeout: Maximum total time for all retries in seconds (default: None, no timeout)
        """
        self.max_attempts = max_attempts
        self.strategy = strategy
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.multiplier = multiplier
        self.jitter = jitter
        self.condition = condition or RetryCondition()
        self.timeout = timeout

        self.retry_attempts: List[Dict[str, Any]] = []
        self.successful_attempts = 0
        self.failed_attempts = 0

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - RetryHandler initialized "
            f"with max_attempts={max_attempts}, strategy={strategy.value}, "
            f"initial_delay={initial_delay}s"
        )

    def execute(
        self,
        func: Callable[[], Any],
        *args: Any,        **kwargs: Any,
    ) -> Any:
        """
        Execute a function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments to pass to function
            **kwargs: Keyword arguments to pass to function

        Returns:
            Return value from successful function execution

        Raises:
            Exception: Last exception raised if all retries fail
        """
        start_time = time.time()
        last_exception: Optional[Exception] = None
        last_return_value: Any = None

        for attempt in range(1, self.max_attempts + 1):
            attempt_start_time = time.time()

            # Check timeout
            if self.timeout and (attempt_start_time - start_time) > self.timeout:
                logger.warning(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Retry timeout exceeded "
                    f"after {attempt_start_time - start_time:.2f}s"
                )
                if last_exception:
                    raise last_exception
                return last_return_value

            try:
                logger.debug(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Retry attempt {attempt}/{self.max_attempts} "
                    f"for function {func.__name__}"
                )

                result = func(*args, **kwargs)
                attempt_duration = time.time() - attempt_start_time

                # Check if we should retry based on return value
                if self.condition.should_retry(exception=None, return_value=result):
                    last_return_value = result
                    if attempt < self.max_attempts:
                        delay = self._calculate_delay(attempt)
                        logger.info(
                            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Retry condition met for return value, "
                            f"retrying in {delay:.2f}s (attempt {attempt}/{self.max_attempts})"
                        )
                        self._record_attempt(attempt, None, result, attempt_duration, True)
                        time.sleep(delay)
                        continue
                    else:
                        logger.warning(
                            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Max retries reached, "
                            f"returning last result"
                        )
                        self._record_attempt(attempt, None, result, attempt_duration, False)
                        return result

                # Success
                self.successful_attempts += 1
                logger.info(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Operation succeeded on attempt {attempt} "
                    f"after {attempt_duration:.2f}s"
                )
                self._record_attempt(attempt, None, result, attempt_duration, False)
                return result

            except Exception as e:
                attempt_duration = time.time() - attempt_start_time
                last_exception = e

                # Check if we should retry based on exception
                if self.condition.should_retry(exception=e, return_value=None):
                    if attempt < self.max_attempts:
                        delay = self._calculate_delay(attempt)
                        logger.warning(
                            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Retry attempt {attempt} failed "
                            f"with {type(e).__name__}: {str(e)}, retrying in {delay:.2f}s"
                        )
                        self._record_attempt(attempt, e, None, attempt_duration, True)
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(
                            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Max retries reached, "
                            f"operation failed after {attempt} attempts"
                        )
                        self._record_attempt(attempt, e, None, attempt_duration, False)
                        raise
                else:
                    # Exception not in retry condition, fail immediately
                    logger.error(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Non-retryable exception "
                        f"{type(e).__name__}: {str(e)}"
                    )
                    self._record_attempt(attempt, e, None, attempt_duration, False)
                    raise

        # Should not reach here, but satisfy type checker
        if last_exception:
            raise last_exception
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Retry operation completed successfully")
        
        return last_return_value

    def _calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay before next retry attempt.

        Args:
            attempt: Current attempt number (1-indexed)

        Returns:
            Delay in seconds
        """
        if self.strategy == RetryStrategy.FIXED_DELAY:
            delay = self.initial_delay
        elif self.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = self.initial_delay * self.multiplier * (attempt - 1)
        elif self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = self.initial_delay * (self.multiplier ** (attempt - 1))
        elif self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF_WITH_JITTER:
            import random
            base_delay = self.initial_delay * (self.multiplier ** (attempt - 1))
            # Add jitter: random value between 0 and 25% of base delay
            jitter_amount = base_delay * 0.25 * random.random()
            delay = base_delay + jitter_amount
        else:
            delay = self.initial_delay

        # Apply max delay cap
        delay = min(delay, self.max_delay)

        return delay

    def _record_attempt(
        self,
        attempt: int,
        exception: Optional[Exception],
        return_value: Any,
        duration: float,
        will_retry: bool,
    ) -> None:
        """Record retry attempt for statistics."""
        self.retry_attempts.append(
            {
                "timestamp": datetime.now().isoformat(),
                "attempt": attempt,
                "exception_type": type(exception).__name__ if exception else None,
                "exception_message": str(exception) if exception else None,
                "return_value": return_value,
                "duration": duration,
                "will_retry": will_retry,
            }
        )

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get retry statistics.

        Returns:
            Dictionary with retry statistics
        """
        total_attempts = len(self.retry_attempts)
        retried_attempts = sum(1 for a in self.retry_attempts if a["will_retry"])

        stats = {
            "total_attempts": total_attempts,
            "successful_attempts": self.successful_attempts,
            "failed_attempts": self.failed_attempts,
            "retried_attempts": retried_attempts,
            "success_rate": (
                self.successful_attempts / total_attempts if total_attempts > 0 else 0.0
            ),
            "strategy": self.strategy.value,
            "max_attempts": self.max_attempts,
        }
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Get statistics operation completed")
        stats["completion_timestamp"] = completion_time
        
        return stats

    def clear_history(self) -> None:
        """Clear retry attempt history."""
        self.retry_attempts.clear()
        self.successful_attempts = 0
        self.failed_attempts = 0
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"{completion_time} - Retry history cleared"
        )
        logger.debug(f"[{completion_time}] Clear history operation completed")


def retry(
    max_attempts: int = 3,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    multiplier: float = 2.0,
    jitter: bool = False,
    retry_on_exceptions: Optional[List[Type[Exception]]] = None,
    retry_on_return_value: Optional[Callable[[Any], bool]] = None,
    timeout: Optional[float] = None,
):
    """
    Decorator for adding retry logic to functions.

    Args:
        max_attempts: Maximum number of retry attempts
        strategy: Retry strategy to use
        initial_delay: Initial delay in seconds before first retry
        max_delay: Maximum delay between retries in seconds
        multiplier: Multiplier for exponential/linear backoff
        jitter: Whether to add random jitter to delays
        retry_on_exceptions: List of exception types to retry on
        retry_on_return_value: Function that returns True if retry needed based on return value
        timeout: Maximum total time for all retries in seconds

    Returns:
        Decorated function with retry logic

    Example:
        @retry(max_attempts=3, retry_on_exceptions=[ConnectionError])
        def fetch_data():
            # This will retry up to 3 times on ConnectionError

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return requests.get("https://example.com")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            condition = RetryCondition(
                retry_on_exceptions=retry_on_exceptions,
                retry_on_return_value=retry_on_return_value,
            )
            handler = RetryHandler(
                max_attempts=max_attempts,
                strategy=strategy,
                initial_delay=initial_delay,
                max_delay=max_delay,
                multiplier=multiplier,
                jitter=jitter,
                condition=condition,
                timeout=timeout,
            )
            return handler.execute(func, *args, **kwargs)

        return wrapper

    return decorator
