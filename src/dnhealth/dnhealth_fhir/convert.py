# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR resource version conversion utilities.

Provides functions to convert resources between different FHIR versions (R4, R5, etc.).
Note: Full version conversion requires extensive version-specific mappings.
This module provides basic version identifier updates.
"""

import logging
from datetime import datetime
from typing import Optional, List, Tuple, Any, TYPE_CHECKING
from copy import deepcopy

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.resources.base import Resource

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def convert_resource_version(
    resource: "Resource",
    target_version: str,
    preserve_unknown_fields: bool = True,
) -> Tuple["Resource", List[str]]:
    """
    Convert a FHIR resource to a different FHIR version.
    
    This function performs basic version conversion including:
    - Updating fhirVersion in meta if present
    - Preserving resource structure
    
    Note: Full version conversion requires extensive version-specific mappings
    and understanding of differences between FHIR versions (R4, R5, etc.).
    This implementation provides basic version identifier updates.
    
    Args:
        resource: Resource object to convert
        target_version: Target FHIR version (e.g., "4.0.1", "5.0.0")
        preserve_unknown_fields: If True, preserve fields not defined in target version
        
    Returns:
        Tuple of (converted_resource, warnings)
        - converted_resource: Converted Resource object
        - warnings: List of warning messages about conversion issues
        
    Raises:
        ValueError: If target_version is invalid
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting FHIR resource conversion to version {target_version}")
    
    warnings = []
    
    # Validate target version format
    if not target_version:
        raise ValueError("Target version cannot be empty")
    
    # Create a copy of the resource
    converted_resource = deepcopy(resource)
    
    # Update meta.fhirVersion if meta exists
    if hasattr(converted_resource, 'meta') and converted_resource.meta:
        # Check if meta has fhirVersion attribute
        if hasattr(converted_resource.meta, 'fhirVersion'):
            converted_resource.meta.fhirVersion = target_version
            logger.debug(f"[{current_time}] Updated meta.fhirVersion to {target_version}")
        else:
            # Try to add fhirVersion if it doesn't exist
            # Note: This depends on the Meta class structure
            logger.debug(f"[{current_time}] meta.fhirVersion not found, skipping update")
    
    # Update resource.meta.source if it contains version info
    if hasattr(converted_resource, 'meta') and converted_resource.meta:
        if hasattr(converted_resource.meta, 'source') and converted_resource.meta.source:
            # Update source URL if it contains version info
            source = converted_resource.meta.source
            # Common pattern: "http://hl7.org/fhir/R4/..."
            if "/fhir/" in source:
                parts = source.split("/fhir/")
                if len(parts) > 1:
                    # Replace version in source URL
                    new_source = f"{parts[0]}/fhir/{target_version}/{'/'.join(parts[1].split('/')[1:])}"
                    converted_resource.meta.source = new_source
                    logger.debug(f"[{current_time}] Updated meta.source to {new_source}")
    
    # Add warning about limited conversion
    warnings.append(
        f"Basic version conversion performed. Full conversion between FHIR versions "
        f"requires extensive version-specific mappings and field transformations."
    )
    
    elapsed = (datetime.now() - start_time).total_seconds()
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        f"[{completion_time}] FHIR version conversion completed in {elapsed:.3f}s - "
        f"converted to version {target_version}"
    )
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return converted_resource, warnings


def convert_resource_simple(resource: "Resource", target_version: str) -> "Resource":
    """
    Simple version conversion that only updates version identifiers.
    
    This is a minimal conversion that preserves all fields,
    only updating version identifiers to target version.
    
    Note: This function maintains backward compatibility. For comprehensive
    conversion with validation and warnings, use convert_resource_version().
    
    Args:
        resource: Resource object to convert
        target_version: Target FHIR version (e.g., "4.0.1", "5.0.0")
        
    Returns:
        Converted Resource object
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Performing simple FHIR conversion to {target_version}")
    
    # Use full conversion but ignore warnings
    converted_resource, _ = convert_resource_version(
        resource,
        target_version=target_version,
        preserve_unknown_fields=True
    )
    
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Simple FHIR conversion completed")
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return converted_resource
