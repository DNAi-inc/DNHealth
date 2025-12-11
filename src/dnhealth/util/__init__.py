# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""Utility modules for DNHealth."""

from dnhealth.util.logging import get_logger, setup_logging
from dnhealth.util.config import Config, get_config
from dnhealth.util.profiling import PerformanceProfiler, profile_operation, time_function
from dnhealth.util.memory_optimization import (
    ObjectPool,
    WeakValueCache,
    MemoryEfficientList,
    cleanup_memory,
    get_memory_usage,
    MemoryMonitor,
)
from dnhealth.util.recovery import (
    ErrorRecovery,
    RecoveryStrategy,
    recover_from_error,
)
from dnhealth.util.retry import (
    RetryHandler,
    RetryStrategy,
    RetryCondition,
    retry,
)
from dnhealth.util.routing import (
    MessageRouter,
    RoutingRule,
    MessageType,
)
from dnhealth.util.transformation import (
    MessageTransformer,
    TransformationRule,
)
from dnhealth.util.validation_pipeline import (
    ValidationPipeline,
    ValidationRule,
    ValidationResult,
    ValidationSeverity,
)
from dnhealth.util.queue import (
    MessageQueue,
    QueueOrder,
    QueuedMessage,
    QueueError,
    QueueFullError,
    QueueEmptyError,
)
from dnhealth.util.database import (
    MessageDatabase,
    MessageType as DBMessageType,
    DatabaseError,
    DatabaseConnectionError,
    DatabaseQueryError,
)

__all__ = [
    "get_logger",
    "setup_logging",
    "Config",
    "get_config",
    "PerformanceProfiler",
    "profile_operation",
    "time_function",
    "ErrorRecovery",
    "RecoveryStrategy",
    "recover_from_error",
    "RetryHandler",
    "RetryStrategy",
    "RetryCondition",
    "retry",
    "MessageRouter",
    "RoutingRule",
    "MessageType",
    "MessageTransformer",
    "TransformationRule",
    "ValidationPipeline",
    "ValidationRule",
    "ValidationResult",
    "ValidationSeverity",
    "MessageQueue",
    "QueueOrder",
    "QueuedMessage",
    "QueueError",
    "QueueFullError",
    "QueueEmptyError",
    "MessageDatabase",
    "DBMessageType",
    "DatabaseError",
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "ObjectPool",
    "WeakValueCache",
    "MemoryEfficientList",
    "cleanup_memory",
    "get_memory_usage",
    "MemoryMonitor",
]

