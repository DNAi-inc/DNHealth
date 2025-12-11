# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Audit logging utilities for DNHealth library.
logger = logging.getLogger(__name__)

Provides structured audit logging for tracking operations, including
timestamps, user actions, resource access, and system events.
All audit logs include timestamps for compliance and traceability.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path

from dnhealth.util.logging import get_logger

logger = get_logger(__name__)


class AuditEventType(Enum):
    """Types of audit events."""

    RESOURCE_ACCESS = "resource_access"
    RESOURCE_CREATE = "resource_create"
    RESOURCE_UPDATE = "resource_update"
    RESOURCE_DELETE = "resource_delete"
    RESOURCE_READ = "resource_read"
    PARSE_OPERATION = "parse_operation"
    SERIALIZE_OPERATION = "serialize_operation"
    VALIDATION_OPERATION = "validation_operation"
    SEARCH_OPERATION = "search_operation"
    BATCH_OPERATION = "batch_operation"
    CACHE_OPERATION = "cache_operation"
    ERROR = "error"
    SYSTEM_EVENT = "system_event"


class AuditLogger:
    """
    Audit logger for tracking operations and events.

    Provides structured logging with timestamps for all audit events.
    Supports both in-memory logging and file-based logging.
    """

    def __init__(
        self,
        log_file: Optional[Path] = None,
        max_memory_entries: int = 1000,
        include_timestamp: bool = True,
    ):
        """
        Initialize the audit logger.

        Args:
            log_file: Optional file path for persistent audit logs
            max_memory_entries: Maximum entries to keep in memory (default: 1000)
            include_timestamp: Always include timestamp in logs (default: True)
        """
        self.log_file = log_file
        self.max_memory_entries = max_memory_entries
        self.include_timestamp = include_timestamp
        self._memory_log: List[Dict[str, Any]] = []
        self._entry_count = 0

        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - AuditLogger initialized "
            f"(log_file={log_file}, max_memory={max_memory_entries})"
        )

    def log(
        self,
        event_type: AuditEventType,
        message: str,
        user: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log an audit event.

        Args:
            event_type: Type of audit event
            message: Human-readable message
            user: Optional user identifier
            resource_type: Optional resource type (e.g., "Patient", "Observation")
            resource_id: Optional resource ID
            metadata: Optional additional metadata
        """
        timestamp = datetime.now()
        entry = {
            "timestamp": timestamp.isoformat(),
            "event_type": event_type.value,
            "message": message,
        }

        if user:
            entry["user"] = user
        if resource_type:
            entry["resource_type"] = resource_type
        if resource_id:
            entry["resource_id"] = resource_id
        if metadata:
            entry["metadata"] = metadata

        # Add to memory log
        self._memory_log.append(entry)
        self._entry_count += 1

        # Trim memory log if needed
        if len(self._memory_log) > self.max_memory_entries:
            self._memory_log.pop(0)

        # Write to file if configured
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    log_line = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {json.dumps(entry)}\n"
                    f.write(log_line)
            except Exception as e:
                logger.error(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Failed to write audit log: {e}"
                )

        # Also log to standard logger
        log_msg = f"[AUDIT] {event_type.value}: {message}"
        if resource_type:
            log_msg += f" (resource_type={resource_type})"
        if resource_id:
            log_msg += f" (resource_id={resource_id})"
        if user:
            log_msg += f" (user={user})"

        logger.info(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {log_msg}")
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Audit log operation completed")

    def log_resource_access(
        self,
        resource_type: str,
        resource_id: str,
        operation: str,
        user: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a resource access event.

        Args:
            resource_type: Type of resource accessed
            resource_id: ID of resource accessed
            operation: Operation performed (read, write, delete, etc.)
            user: Optional user identifier
            metadata: Optional additional metadata
        """
        self.log(
            event_type=AuditEventType.RESOURCE_ACCESS,
            message=f"Resource access: {operation} on {resource_type}/{resource_id}",
            user=user,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata,
        )
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Resource access logging completed")

    def log_parse_operation(
        self,
        resource_type: str,
        success: bool,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a parse operation.

        Args:
            resource_type: Type of resource being parsed
            success: Whether parsing succeeded
            error: Optional error message if parsing failed
            metadata: Optional additional metadata
        """
        message = f"Parse operation: {resource_type} {'succeeded' if success else 'failed'}"
        if error:
            message += f" - {error}"

        meta = metadata or {}
        meta["success"] = success
        if error:
            meta["error"] = error

        self.log(
            event_type=AuditEventType.PARSE_OPERATION,
            message=message,
            resource_type=resource_type,
            metadata=meta,
        )
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Parse operation logging completed")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def log_batch_operation(
        self,
        operation: str,
        resource_count: int,
        success_count: int,
        error_count: int,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a batch operation.

        Args:
            operation: Type of batch operation (parse, serialize, validate, etc.)
            resource_count: Total number of resources processed
            success_count: Number of successful operations
            error_count: Number of failed operations
            metadata: Optional additional metadata
        """
        message = (
            f"Batch operation: {operation} - "
            f"{resource_count} total, {success_count} succeeded, {error_count} failed"
        )

        meta = metadata or {}
        meta["operation"] = operation
        meta["resource_count"] = resource_count
        meta["success_count"] = success_count
        meta["error_count"] = error_count

        self.log(
            event_type=AuditEventType.BATCH_OPERATION,
            message=message,
            metadata=meta,
        )
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Batch operation logging completed")

    def get_logs(
        self,
        event_type: Optional[AuditEventType] = None,
        resource_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get audit logs matching criteria.

        Args:
            event_type: Optional event type filter
            resource_type: Optional resource type filter
            limit: Optional limit on number of results

        Returns:
            List of audit log entries
        """
        results = self._memory_log.copy()

        # Apply filters
        if event_type:
            results = [e for e in results if e.get("event_type") == event_type.value]
        if resource_type:
            results = [e for e in results if e.get("resource_type") == resource_type]

        # Apply limit
        if limit:
            results = results[-limit:]

        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Get logs operation completed (returned {len(results)} results)")
        
        return results

    def clear_memory_log(self) -> None:
        """Clear the in-memory audit log."""
        count = len(self._memory_log)
        self._memory_log.clear()
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"{completion_time} - Cleared {count} audit log entries from memory"
        )
        logger.debug(f"[{completion_time}] Clear memory log operation completed")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get audit log statistics.

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_entries": self._entry_count,
            "memory_entries": len(self._memory_log),
            "max_memory_entries": self.max_memory_entries,
            "log_file": str(self.log_file) if self.log_file else None,
            "current_time": datetime.now().isoformat(),
        }

        # Count by event type
        event_counts: Dict[str, int] = {}
        for entry in self._memory_log:
            event_type = entry.get("event_type", "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        stats["event_type_counts"] = event_counts
        
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Get stats operation completed")
        stats["completion_timestamp"] = completion_time

        return stats



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
# Global default audit logger instance
_default_audit_logger: Optional[AuditLogger] = None


def get_default_audit_logger() -> AuditLogger:
    """
    Get the default global audit logger instance.

    Returns:
        Default AuditLogger instance
    """
    global _default_audit_logger
    if _default_audit_logger is None:
        _default_audit_logger = AuditLogger()
    return _default_audit_logger


def set_default_audit_logger(audit_logger: AuditLogger) -> None:
    """
    Set the default global audit logger instance.

    Args:
        audit_logger: AuditLogger instance to use as default
    """
    global _default_audit_logger
    _default_audit_logger = audit_logger
    logger.info(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Default audit logger instance updated"
    )
