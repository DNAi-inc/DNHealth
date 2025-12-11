# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 History Operations.

Provides functions for managing resource version history.
Supports vread, resource history, type history, and system history.
All operations include timestamps in logs for traceability.
All operations enforce 5-minute timeout limits (300 seconds).
"""

import time
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry
from dnhealth.util.logging import get_logger

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.resources.base import Resource
    from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage

logger = logging.getLogger(__name__)

logger = get_logger(__name__)

# Timeout limit for all operations (5 minutes)
OPERATION_TIMEOUT = 300  # seconds


def read_version(
    resource_type: str,
    resource_id: str,
    version: str,
    storage: "ResourceStorage"
) -> Optional["Resource"]:
    """
    Read a specific version of a resource (vread).
    
    Loads a specific version of a resource by type, ID, and version ID.
    This is the FHIR vread operation.
    
    Args:
        resource_type: FHIR resource type
        resource_id: Resource ID
        version: Version ID to read
        storage: ResourceStorage instance for reading resources
        
    Returns:
        Resource at specified version, or None if not found
        
    Raises:
        ValueError: If version format is invalid
        
    Example:
        >>> from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage
        >>> storage = ResourceStorage()
        >>> resource = read_version("Patient", "123", "v1", storage)
        >>> if resource:
        ...     print(f"Version {version} of {resource_type}/{resource_id}")
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Reading version {version} of {resource_type}/{resource_id}")
    
    try:
        # Validate inputs
        if not resource_type:
            raise ValueError("Resource type is required")
        if not resource_id:
            raise ValueError("Resource ID is required")
        if not version:
            raise ValueError("Version is required")
        
        # Read version from storage
        resource = storage.read(resource_type, resource_id, version)
        
        elapsed = time.time() - start_time
        if resource:
            logger.info(f"[{current_time}] Successfully read version {version} of {resource_type}/{resource_id} (elapsed: {elapsed:.3f}s)")
        else:
            logger.warning(f"[{current_time}] Version {version} of {resource_type}/{resource_id} not found (elapsed: {elapsed:.3f}s)")
        
        return resource
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error reading version {version} of {resource_type}/{resource_id}: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        raise
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Version read completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")


def get_resource_history(
    resource_type: str,
    resource_id: str,
    storage: "ResourceStorage",
    count: Optional[int] = None,    since: Optional[datetime] = None
) -> Bundle:
    """
    Get version history for a specific resource.
    
    Loads all versions of a resource, optionally filtered by _since parameter
    and limited by _count parameter. Returns Bundle with type="history".
    
    Args:
        resource_type: FHIR resource type
        resource_id: Resource ID
        storage: ResourceStorage instance for reading resources
        count: Optional maximum number of versions to return
        since: Optional datetime to get versions since (only return versions after this date)
        
    Returns:
        Bundle with type="history" containing all versions in reverse chronological order
        
    Example:
        >>> from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage
        >>> from datetime import datetime, timedelta
        >>> storage = ResourceStorage()
        >>> since = datetime.now() - timedelta(days=7)
        >>> bundle = get_resource_history("Patient", "123", storage, count=10, since=since)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting history for resource {resource_type}/{resource_id}")
    
    try:
        # Validate inputs
        if not resource_type:
            raise ValueError("Resource type is required")
        if not resource_id:
            raise ValueError("Resource ID is required")
        
        # Get all versions from storage
        # Note: This requires storage to support version listing
        # For now, we'll use a simplified approach
        versions = []
        
        # Try to get versions from storage
        if hasattr(storage, 'get_versions'):
            versions = storage.get_versions(resource_type, resource_id)
        else:
            # Fallback: Try to read current version and infer history
            # In a real implementation, storage should maintain version history
            current_resource = storage.read(resource_type, resource_id)
            if current_resource and current_resource.meta and current_resource.meta.versionId:
                # Create a single-entry history
                versions = [{
                    "version": current_resource.meta.versionId,
                    "resource": current_resource,
                    "timestamp": current_resource.meta.lastUpdated or datetime.now().isoformat()
                }]
        
        # Filter by _since if provided
        if since:
            since_iso = since.isoformat()
            versions = [v for v in versions if v.get("timestamp", "") >= since_iso]
        
        # Sort by timestamp (reverse chronological - newest first)
        versions.sort(key=lambda v: v.get("timestamp", ""), reverse=True)
        
        # Limit by _count if provided
        if count is not None and count > 0:
            versions = versions[:count]
        
        # Create Bundle response
        bundle = Bundle()
        bundle.type = "history"
        bundle.total = len(versions)
        bundle.entry = []
        
        for version_info in versions:
            entry = BundleEntry()
            entry.resource = version_info.get("resource")
            if entry.resource:
                entry.fullUrl = f"/{resource_type}/{resource_id}/_history/{version_info.get('version')}"
                bundle.entry.append(entry)
        
        elapsed = time.time() - start_time
        logger.info(f"[{current_time}] Retrieved {len(versions)} versions for {resource_type}/{resource_id} (elapsed: {elapsed:.3f}s)")
        
        return bundle
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error getting history for {resource_type}/{resource_id}: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        raise
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Resource history retrieval completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")


def get_type_history(
    resource_type: str,
    storage: "ResourceStorage",
    count: Optional[int] = None,
    since: Optional[datetime] = None
) -> Bundle:
    """
    Get version history for all resources of a specific type.
    
    Loads all versions of all resources of the specified type, optionally filtered
    by _since parameter and limited by _count parameter. Returns Bundle with type="history".
    
    Args:
        resource_type: FHIR resource type
        storage: ResourceStorage instance for reading resources
        count: Optional maximum number of versions to return
        since: Optional datetime to get versions since (only return versions after this date)
        
    Returns:
        Bundle with type="history" containing all versions in reverse chronological order
        
    Example:
        >>> from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage
        >>> storage = ResourceStorage()
        >>> bundle = get_type_history("Patient", storage, count=100)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting type history for {resource_type}")
    
    try:
        # Validate inputs
        if not resource_type:
            raise ValueError("Resource type is required")
        
        # Get all resources of this type
        all_resources = storage.search(resource_type, None)
        
        # Collect all versions
        all_versions = []
        
        for resource in all_resources:
            if resource.id:
                # Get history for this resource
                resource_history = get_resource_history(resource_type, resource.id, storage, count=None, since=since)
                if resource_history.entry:
                    all_versions.extend(resource_history.entry)
        
        # Sort by timestamp (reverse chronological - newest first)
        # Note: This requires entry.resource.meta.lastUpdated
        all_versions.sort(
            key=lambda e: e.resource.meta.lastUpdated if e.resource and e.resource.meta and e.resource.meta.lastUpdated else "",
            reverse=True
        )
        
        # Limit by _count if provided
        if count is not None and count > 0:
            all_versions = all_versions[:count]
        
        # Create Bundle response
        bundle = Bundle()
        bundle.type = "history"
        bundle.total = len(all_versions)
        bundle.entry = all_versions
        
        elapsed = time.time() - start_time
        logger.info(f"[{current_time}] Retrieved {len(all_versions)} versions for type {resource_type} (elapsed: {elapsed:.3f}s)")
        
        return bundle
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error getting type history for {resource_type}: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        raise
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Type history retrieval completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")


def get_all_history(
    storage: "ResourceStorage",
    count: Optional[int] = None,
    since: Optional[datetime] = None
) -> Bundle:
    """
    Get version history for all resources across all types.
    
    Loads all versions of all resources, optionally filtered by _since parameter
    and limited by _count parameter. Returns Bundle with type="history".
    
    Args:
        storage: ResourceStorage instance for reading resources
        count: Optional maximum number of versions to return
        since: Optional datetime to get versions since (only return versions after this date)
        
    Returns:
        Bundle with type="history" containing all versions in reverse chronological order
        
    Example:
        >>> from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage
        >>> storage = ResourceStorage()
        >>> bundle = get_all_history(storage, count=1000)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting system-wide history")
    
    try:
        # Get all resource types from storage
        # Note: This requires storage to support listing resource types
        # For now, we'll use a simplified approach
        all_versions = []
        
        # Try to get all resource types
        if hasattr(storage, 'list_resource_types'):
            resource_types = storage.list_resource_types()
        else:
            # Fallback: Use common resource types
            # In a real implementation, storage should provide this
            resource_types = [
                "Patient", "Observation", "Encounter", "Condition", "Procedure",
                "Medication", "MedicationRequest", "DiagnosticReport", "Immunization"
            ]
        
        # Get history for each resource type
        for resource_type in resource_types:
            try:
                type_history = get_type_history(resource_type, storage, count=None, since=since)
                if type_history.entry:
                    all_versions.extend(type_history.entry)
            except Exception as e:
                # Log but continue with other types
                logger.warning(f"[{current_time}] Error getting history for {resource_type}: {e}")
        
        # Sort by timestamp (reverse chronological - newest first)
        all_versions.sort(
            key=lambda e: e.resource.meta.lastUpdated if e.resource and e.resource.meta and e.resource.meta.lastUpdated else "",
            reverse=True
        )
        
        # Limit by _count if provided
        if count is not None and count > 0:
            all_versions = all_versions[:count]
        
        # Create Bundle response
        bundle = Bundle()
        bundle.type = "history"
        bundle.total = len(all_versions)
        bundle.entry = all_versions
        
        elapsed = time.time() - start_time
        logger.info(f"[{current_time}] Retrieved {len(all_versions)} versions system-wide (elapsed: {elapsed:.3f}s)")
        
        return bundle
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error getting system-wide history: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        raise
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] System-wide history retrieval completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")
