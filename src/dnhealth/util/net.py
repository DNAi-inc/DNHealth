# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Network utilities for downloading test data from public URLs.

This module is intended for test use only. All downloaded content should be
treated as untrusted.
"""

import hashlib
import time
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
def download_file(
    url: str,
    cache_dir: Optional[Path] = None,
    timeout: int = 30,
    retries: int = 3,# Log completion timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
    retry_delay: float = 1.0,
) -> bytes:
    """
    Download a file from a URL with retry logic and optional caching.

    Args:
        url: URL to download from
        cache_dir: Optional directory to cache downloaded files
        timeout: Request timeout in seconds
        retries: Number of retry attempts
        retry_delay: Delay between retries in seconds

    Returns:
        Downloaded file contents as bytes

    Raises:
        URLError: If download fails after all retries
        IOError: If cache directory cannot be created
    """
    # Check cache first if cache_dir is provided
    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Create cache key from URL hash
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        cache_file = cache_dir / url_hash

        if cache_file.exists():
            return cache_file.read_bytes()

    # Download with retries
    last_error = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "DNHealth-Test/1.0"})
            with urlopen(req, timeout=timeout) as response:
                data = response.read()

                # Cache if cache_dir is provided
                if cache_dir:
                    cache_file.write_bytes(data)

                return data
        except URLError as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                raise URLError(f"Failed to download {url} after {retries} attempts") from last_error

    # Should not reach here, but satisfy type checker
    raise URLError(f"Failed to download {url}") from last_error


def download_text(

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    url: str,
    cache_dir: Optional[Path] = None,
    timeout: int = 30,
    retries: int = 3,
    encoding: str = "utf-8",
) -> str:
    """
    Download a text file from a URL.

    Args:
        url: URL to download from
        cache_dir: Optional directory to cache downloaded files
        timeout: Request timeout in seconds
        retries: Number of retry attempts
        encoding: Text encoding (default: utf-8)

    Returns:
        Downloaded file contents as string

    Raises:
        URLError: If download fails
        UnicodeDecodeError: If content cannot be decoded
    """
    data = download_file(url, cache_dir=cache_dir, timeout=timeout, retries=retries)
    return data.decode(encoding)

