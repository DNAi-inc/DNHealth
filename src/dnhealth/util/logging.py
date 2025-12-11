# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Logging utilities for DNHealth library.

Provides structured logging with appropriate levels and formatting.
Always includes timestamps in log messages.
"""

import logging
import sys
from datetime import datetime
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    stream: Optional[sys.stdout] = None,
) -> logging.Logger:
    """
    Set up logging for DNHealth library.
    
    All log messages will include timestamps in the format: YYYY-MM-DD HH:MM:SS.
    Timestamps are always included to ensure traceability of operations.

    Args:
        level: Logging level (default: INFO)
        format_string: Custom format string (default: standard format with timestamp)
        stream: Output stream (default: sys.stderr)

    Returns:
        Configured logger instance
    """
    # Ensure timestamp is always included in format string
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    elif "%(asctime)s" not in format_string:
        # If custom format doesn't include timestamp, prepend it
        format_string = "%(asctime)s - " + format_string

    if stream is None:
        stream = sys.stderr

    logging.basicConfig(
        level=level,
        format=format_string,
        stream=stream,
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # Force reconfiguration if already configured
    )

    logger = logging.getLogger("dnhealth")
    # Set a formatter that always includes timestamp
    for handler in logger.handlers:
        if handler.formatter is None or "%(asctime)s" not in handler.formatter._fmt:
            handler.setFormatter(logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return logging.getLogger(f"dnhealth.{name}")


# Default logger for the package
logger = logging.getLogger("dnhealth")


def get_current_time() -> str:
    """
    Get current timestamp in standard format.
    
    Returns:
        Current time as string in format 'YYYY-MM-DD HH:MM:SS'
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

