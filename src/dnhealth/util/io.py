# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
I/O helper functions for reading and writing text, JSON, and XML files.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)


def read_text_file(file_path: Union[str, Path]) -> str:
    """
    Read a text file and return its contents.

    Args:
        file_path: Path to the text file

    Returns:
        File contents as string

    Raises:
        IOError: If file cannot be read
    """
    path = Path(file_path)
    if not path.exists():
        raise IOError(f"File not found: {file_path}")
    result = path.read_text(encoding="utf-8")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Text file read operation completed: {file_path}")
    
    return result


def write_text_file(file_path: Union[str, Path], content: str) -> None:
    """
    Write content to a text file.

    Args:
        file_path: Path to the text file
        content: Content to write

    Raises:
        IOError: If file cannot be written
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Text file write operation completed: {file_path}")


def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Read a JSON file and return parsed contents.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON as dictionary

    Raises:
        IOError: If file cannot be read
        json.JSONDecodeError: If JSON is invalid
    """
    path = Path(file_path)
    if not path.exists():
        raise IOError(f"File not found: {file_path}")
    text = path.read_text(encoding="utf-8")
    result = json.loads(text)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] JSON file read operation completed: {file_path}")
    
    return result


def write_json_file(
    file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2
) -> None:
    """
    Write data to a JSON file.

    Args:
        file_path: Path to the JSON file
        data: Data to write (must be JSON-serializable)
        indent: Indentation level for pretty-printing

    Raises:
        IOError: If file cannot be written
        TypeError: If data is not JSON-serializable
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    path.write_text(json_str, encoding="utf-8")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] JSON file write operation completed: {file_path}")


def read_xml_file(file_path: Union[str, Path]) -> str:
    """
    Read an XML file and return its contents.

    Args:
        file_path: Path to the XML file

    Returns:
        File contents as string

    Raises:
        IOError: If file cannot be read
    """
    return read_text_file(file_path)


def write_xml_file(file_path: Union[str, Path], content: str) -> None:
    """
    Write content to an XML file.

    Args:
        file_path: Path to the XML file
        content: XML content to write

    Raises:
        IOError: If file cannot be written
    """
    write_text_file(file_path, content)


def read_stdin() -> str:
    """
    Read content from stdin.

    Returns:
        Content from stdin as string
    """
    result = sys.stdin.read()
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Stdin read operation completed")
    
    return result


def write_stdout(content: str) -> None:
    """
    Write content to stdout.

    Args:
        content: Content to write
    """
    sys.stdout.write(content)
    sys.stdout.flush()
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Stdout write operation completed")


# Log completion timestamp at end of operations
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")

