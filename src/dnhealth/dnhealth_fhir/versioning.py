# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Resource Versioning.

Provides functions for managing resource versions.
Versions are stored in resource.meta.versionId and resource.meta.lastUpdated.
All operations include timestamps in logs for traceability.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from dnhealth.util.logging import get_logger

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.resources.base import Resource, Meta

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


@dataclass
class VersionInfo:
    """
    Information about a resource version.
    
    Attributes:
        version_id: Version identifier
        timestamp: Last updated timestamp
        deleted: Whether this version represents a deleted resource
    """
    version_id: str
    timestamp: str
    deleted: bool = False



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def create_version(resource: "Resource") -> str:
    """
    Create a new version ID for a FHIR resource.
    
    Generates a UUID-based version ID and updates resource.meta.versionId.
    Also updates resource.meta.lastUpdated with current timestamp.
    
    Args:
        resource: FHIR resource to create version for
    
    Returns:
        Version ID string (UUID format)
    
    Example:
        >>> version_id = create_version(patient)
        >>> print(f"Created version: {version_id}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Creating version for resource {resource.resourceType}/{resource.id}")
    
    # Generate UUID-based version ID
    version_id = str(uuid.uuid4())
    
    # Ensure resource has meta
    if not hasattr(resource, 'meta') or resource.meta is None:
        from dnhealth.dnhealth_fhir.resources.base import Meta
        resource.meta = Meta()
    
    # Set version ID and last updated

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    resource.meta.versionId = version_id
    resource.meta.lastUpdated = datetime.now().isoformat()
    
    logger.info(f"[{current_time}] Created version {version_id} for resource {resource.resourceType}/{resource.id}")
    return version_id


def get_version(resource: "Resource") -> Optional[str]:
    """
    Get the current version ID of a FHIR resource.
    
    Args:
        resource: FHIR resource to get version for
    
    Returns:
        Version ID string if available, None otherwise
    
    Example:
        >>> version_id = get_version(patient)
        >>> if version_id:
        ...     print(f"Current version: {version_id}")
    """
    if not hasattr(resource, 'meta') or resource.meta is None:
        return None
    
    return resource.meta.versionId


def increment_version(resource: "Resource") -> str:
    """
    Increment the version of a FHIR resource.
    
    Creates a new version ID and updates resource.meta.versionId and resource.meta.lastUpdated.
    This is typically called when updating a resource.
    
    Args:
        resource: FHIR resource to increment version for
    
    Returns:
        New version ID string
    
    Example:
        >>> new_version = increment_version(patient)
        >>> print(f"New version: {new_version}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    old_version = get_version(resource)
    logger.debug(f"[{current_time}] Incrementing version for resource {resource.resourceType}/{resource.id} (old: {old_version})")
    
    # Create new version
    new_version_id = create_version(resource)
    
    logger.info(f"[{current_time}] Incremented version for resource {resource.resourceType}/{resource.id} from {old_version} to {new_version_id}")
    return new_version_id


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version IDs.
    
    For UUID-based versions, this compares them lexicographically.
    For sequential versions, this compares them numerically.
    
    Args:
        version1: First version ID
        version2: Second version ID
    
    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    
    Example:
        >>> result = compare_versions("v1", "v2")
        >>> if result < 0:
        ...     print("version1 is older")
    """
    # Try to parse as UUIDs first
    try:
        uuid1 = uuid.UUID(version1)
        uuid2 = uuid.UUID(version2)
        # Compare UUIDs lexicographically (not ideal, but works for ordering)
        if version1 < version2:
            return -1
        elif version1 > version2:
            return 1
        else:
            return 0
    except ValueError:
        # Not UUIDs, try numeric comparison
        try:
            # Extract numeric part if possible (e.g., "v1" -> 1)
            num1 = int(''.join(filter(str.isdigit, version1)) or '0')
            num2 = int(''.join(filter(str.isdigit, version2)) or '0')
            if num1 < num2:
                return -1
            elif num1 > num2:
                return 1
            else:

                    # Log completion timestamp at end of operation
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Current Time at End of Operations: {current_time}")
                return 0
        except ValueError:
            # Fall back to string comparison
            if version1 < version2:
                return -1
            elif version1 > version2:
                return 1
            else:
                return 0


def get_version_history(resource_type: str, resource_id: str, storage: Optional[Any] = None) -> List[VersionInfo]:
    """
    Get version history for a resource.
    
    Retrieves all versions of a resource from storage.
    This requires a storage backend that supports version history.
    
    Args:
        resource_type: Resource type (e.g., "Patient")
        resource_id: Resource ID
        storage: Optional storage backend (if None, returns empty list)
    
    Returns:
        List of VersionInfo objects representing version history
    
    Example:
        >>> history = get_version_history("Patient", "test-1", storage)
        >>> for version in history:
        ...     print(f"Version {version.version_id} at {version.timestamp}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting version history for {resource_type}/{resource_id}")
    
    if storage is None:
        logger.warning(f"[{current_time}] No storage provided, cannot retrieve version history")
        return []
    
    # Check if storage has version history support
    if not hasattr(storage, 'get_version_history'):
        logger.warning(f"[{current_time}] Storage does not support version history")
        return []
    
    try:
        history = storage.get_version_history(resource_type, resource_id)
        logger.info(f"[{current_time}] Retrieved {len(history)} version(s) for {resource_type}/{resource_id}")
        return history
    except Exception as e:
        logger.error(f"[{current_time}] Error retrieving version history: {e}")
        return []
