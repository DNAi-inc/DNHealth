# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Resource Tagging.

Provides functions for managing tags on FHIR resources.
Tags are stored in resource.meta.tag as Coding objects.
All operations include timestamps in logs for traceability.
"""

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from dnhealth.dnhealth_fhir.types import Coding
from dnhealth.util.logging import get_logger

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.resources.base import Resource, Meta

logger = logging.getLogger(__name__)

logger = get_logger(__name__)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def add_tag(resource: "Resource", tag: Coding) -> None:
    """
    Add a tag to a FHIR resource.
    
    Tags are stored in resource.meta.tag as Coding objects.
    If the tag already exists (same system and code), it will not be duplicated.
    
    Args:
        resource: FHIR resource to add tag to
        tag: Coding object representing the tag (must have system and code)
    
    Raises:
        ValueError: If tag is missing system or code
        AttributeError: If resource doesn't have meta attribute
    
    Example:
        >>> from dnhealth.dnhealth_fhir.types import Coding
        >>> from dnhealth.dnhealth_fhir.resources.patient import Patient
        >>> patient = Patient(resourceType="Patient", id="test-1")
        >>> tag = Coding(system="http://example.org/tags", code="important")
        >>> add_tag(patient, tag)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Adding tag to resource {resource.resourceType}/{resource.id}")
    
    # Validate tag
    if not tag.system:
        raise ValueError("Tag must have a system")
    if not tag.code:
        raise ValueError("Tag must have a code")
    
    # Ensure resource has meta
    if not hasattr(resource, 'meta') or resource.meta is None:
        from dnhealth.dnhealth_fhir.resources.base import Meta
        resource.meta = Meta()
    
    # Check if tag already exists
    if resource.meta.tag:
        for existing_tag in resource.meta.tag:
            if existing_tag.system == tag.system and existing_tag.code == tag.code:
                logger.debug(f"[{current_time}] Tag {tag.system}|{tag.code} already exists, skipping")
                return
    
    # Add tag
    resource.meta.tag.append(tag)
    logger.info(f"[{current_time}] Added tag {tag.system}|{tag.code} to resource {resource.resourceType}/{resource.id}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Add tag operation completed")


def remove_tag(resource: "Resource", tag_system: str, tag_code: str) -> None:
    """
    Remove a tag from a FHIR resource.
    
    Removes the tag matching the specified system and code.
    If the tag doesn't exist, no error is raised.
    
    Args:
        resource: FHIR resource to remove tag from
        tag_system: Tag system URI
        tag_code: Tag code
    
    Example:
        >>> remove_tag(patient, "http://example.org/tags", "important")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Removing tag {tag_system}|{tag_code} from resource {resource.resourceType}/{resource.id}")
    
    # Check if resource has meta and tags
    if not hasattr(resource, 'meta') or resource.meta is None:
        logger.debug(f"[{current_time}] Resource has no meta, nothing to remove")
        return
    
    if not resource.meta.tag:
        logger.debug(f"[{current_time}] Resource has no tags, nothing to remove")
        return
    
    # Remove matching tag
    original_count = len(resource.meta.tag)
    resource.meta.tag = [
        tag for tag in resource.meta.tag
        if not (tag.system == tag_system and tag.code == tag_code)
    ]
    
    removed_count = original_count - len(resource.meta.tag)
    if removed_count > 0:
        logger.info(f"[{current_time}] Removed {removed_count} tag(s) {tag_system}|{tag_code} from resource {resource.resourceType}/{resource.id}")
    else:
        logger.debug(f"[{current_time}] Tag {tag_system}|{tag_code} not found in resource")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Remove tag operation completed")


def get_tags(resource: "Resource") -> List[Coding]:
    """
    Get all tags from a FHIR resource.
    
    Returns a list of Coding objects representing the tags.
    Returns an empty list if the resource has no tags.
    
    Args:
        resource: FHIR resource to get tags from
    
    Returns:
        List of Coding objects (tags)
    
    Example:
        >>> tags = get_tags(patient)
        >>> for tag in tags:
        ...     print(f"{tag.system}|{tag.code}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting tags from resource {resource.resourceType}/{resource.id}")
    
    # Check if resource has meta and tags
    if not hasattr(resource, 'meta') or resource.meta is None:
        return []
    
    if not resource.meta.tag:
        return []
    
    tags = list(resource.meta.tag)  # Return a copy
    logger.debug(f"[{current_time}] Found {len(tags)} tag(s) on resource {resource.resourceType}/{resource.id}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Get tags operation completed")
    
    return tags


def filter_by_tag(resources: List["Resource"], tag_system: str, tag_code: str) -> List["Resource"]:
    """
    Filter resources by tag.
    
    Returns only resources that have the specified tag (matching system and code).
    
    Args:
        resources: List of FHIR resources to filter
        tag_system: Tag system URI to match
        tag_code: Tag code to match
    
    Returns:
        List of resources that have the specified tag
    
    Example:
        >>> patients = [patient1, patient2, patient3]
        >>> important_patients = filter_by_tag(patients, "http://example.org/tags", "important")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Filtering {len(resources)} resource(s) by tag {tag_system}|{tag_code}")
    
    filtered = []
    for resource in resources:
        tags = get_tags(resource)
        for tag in tags:
            if tag.system == tag_system and tag.code == tag_code:
                filtered.append(resource)
                break
    
    logger.info(f"[{current_time}] Filtered {len(resources)} resource(s) to {len(filtered)} resource(s) with tag {tag_system}|{tag_code}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Filter by tag operation completed")
    
    return filtered


def has_tag(resource: "Resource", tag_system: str, tag_code: str) -> bool:
    """
    Check if a resource has a specific tag.
    
    Args:
        resource: FHIR resource to check
        tag_system: Tag system URI to check for
        tag_code: Tag code to check for
    
    Returns:
        True if resource has the tag, False otherwise
    
    Example:
        >>> if has_tag(patient, "http://example.org/tags", "important"):
        ...     print("Patient is important")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking if resource {resource.resourceType}/{resource.id} has tag {tag_system}|{tag_code}")
    
    tags = get_tags(resource)
    for tag in tags:
        if tag.system == tag_system and tag.code == tag_code:
            # Log completion timestamp at end of operation
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{completion_time}] Has tag operation completed (found)")
            return True
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Has tag operation completed (not found)")
    return False
