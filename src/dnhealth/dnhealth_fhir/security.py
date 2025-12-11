# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Resource Security Labels.

Provides functions for managing security labels on FHIR resources.
Security labels are stored in resource.meta.security as Coding objects.
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
def add_security_label(resource: "Resource", label: Coding) -> None:
    """
    Add a security label to a FHIR resource.
    
    Security labels are stored in resource.meta.security as Coding objects.
    They indicate sensitivity/confidentiality levels.
    If the label already exists (same system and code), it will not be duplicated.
    
    Args:
        resource: FHIR resource to add security label to
        label: Coding object representing the security label (must have system and code)
    
    Raises:
        ValueError: If label is missing system or code
        AttributeError: If resource doesn't have meta attribute
    
    Example:
        >>> from dnhealth.dnhealth_fhir.types import Coding
        >>> from dnhealth.dnhealth_fhir.resources.patient import Patient
        >>> patient = Patient(resourceType="Patient", id="test-1")
        >>> label = Coding(
        ...     system="http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
        ...     code="N",
        ...     display="Normal"
        ... )
        >>> add_security_label(patient, label)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Adding security label to resource {resource.resourceType}/{resource.id}")
    
    # Validate label
    if not label.system:
        raise ValueError("Security label must have a system")
    if not label.code:
        raise ValueError("Security label must have a code")
    
    # Ensure resource has meta
    if not hasattr(resource, 'meta') or resource.meta is None:
        from dnhealth.dnhealth_fhir.resources.base import Meta
        resource.meta = Meta()
    
    # Check if label already exists
    if resource.meta.security:
        for existing_label in resource.meta.security:
            if existing_label.system == label.system and existing_label.code == label.code:
                logger.debug(f"[{current_time}] Security label {label.system}|{label.code} already exists, skipping")
                return
    
    # Add label
    resource.meta.security.append(label)
    logger.info(f"[{current_time}] Added security label {label.system}|{label.code} to resource {resource.resourceType}/{resource.id}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Add security label operation completed")


def remove_security_label(resource: "Resource", label_system: str, label_code: str) -> None:
    """
    Remove a security label from a FHIR resource.
    
    Removes the security label matching the specified system and code.
    If the label doesn't exist, no error is raised.
    
    Args:
        resource: FHIR resource to remove security label from
        label_system: Security label system URI
        label_code: Security label code
    
    Example:
        >>> remove_security_label(patient, "http://terminology.hl7.org/CodeSystem/v3-Confidentiality", "N")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Removing security label {label_system}|{label_code} from resource {resource.resourceType}/{resource.id}")
    
    # Check if resource has meta and security labels
    if not hasattr(resource, 'meta') or resource.meta is None:
        logger.debug(f"[{current_time}] Resource has no meta, nothing to remove")
        return
    
    if not resource.meta.security:
        logger.debug(f"[{current_time}] Resource has no security labels, nothing to remove")
        return
    
    # Remove matching label
    original_count = len(resource.meta.security)
    resource.meta.security = [
        label for label in resource.meta.security
        if not (label.system == label_system and label.code == label_code)
    ]
    
    removed_count = original_count - len(resource.meta.security)
    if removed_count > 0:
        logger.info(f"[{current_time}] Removed {removed_count} security label(s) {label_system}|{label_code} from resource {resource.resourceType}/{resource.id}")
    else:
        logger.debug(f"[{current_time}] Security label {label_system}|{label_code} not found in resource")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Remove security label operation completed")


def get_security_labels(resource: "Resource") -> List[Coding]:
    """
    Get all security labels from a FHIR resource.
    
    Returns a list of Coding objects representing the security labels.
    Returns an empty list if the resource has no security labels.
    
    Args:
        resource: FHIR resource to get security labels from
    
    Returns:
        List of Coding objects (security labels)
    
    Example:
        >>> labels = get_security_labels(patient)
        >>> for label in labels:
        ...     print(f"{label.system}|{label.code}: {label.display}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting security labels from resource {resource.resourceType}/{resource.id}")
    
    # Check if resource has meta and security labels
    if not hasattr(resource, 'meta') or resource.meta is None:
        return []
    
    if not resource.meta.security:
        return []
    
    labels = list(resource.meta.security)  # Return a copy
    logger.debug(f"[{current_time}] Found {len(labels)} security label(s) on resource {resource.resourceType}/{resource.id}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Get security labels operation completed")
    
    return labels


def validate_security_labels(resource: "Resource") -> List[str]:
    """
    Validate security labels on a FHIR resource.
    
    Checks that all security labels have required fields (system and code).
    Returns a list of validation errors (empty if all labels are valid).
    
    Args:
        resource: FHIR resource to validate security labels for
    
    Returns:
        List of validation error messages (empty if valid)
    
    Example:
        >>> errors = validate_security_labels(patient)
        >>> if errors:
        ...     for error in errors:
        ...         print(f"Validation error: {error}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Validating security labels on resource {resource.resourceType}/{resource.id}")
    
    errors = []
    labels = get_security_labels(resource)
    
    for i, label in enumerate(labels):
        if not label.system:
            errors.append(f"Security label {i+1} is missing system")
        if not label.code:
            errors.append(f"Security label {i+1} is missing code")
    
    if errors:
        logger.warning(f"[{current_time}] Found {len(errors)} validation error(s) in security labels for resource {resource.resourceType}/{resource.id}")
    else:
        logger.debug(f"[{current_time}] All security labels are valid for resource {resource.resourceType}/{resource.id}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Validate security labels operation completed")
    
    return errors


def filter_by_security_label(resources: List["Resource"], label_system: str, label_code: str) -> List["Resource"]:
    """
    Filter resources by security label.
    
    Returns only resources that have the specified security label (matching system and code).
    
    Args:
        resources: List of FHIR resources to filter
        label_system: Security label system URI to match
        label_code: Security label code to match
    
    Returns:
        List of resources that have the specified security label
    
    Example:
        >>> patients = [patient1, patient2, patient3]
        >>> normal_confidentiality = filter_by_security_label(
        ...     patients,
        ...     "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
        ...     "N"
        ... )
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Filtering {len(resources)} resource(s) by security label {label_system}|{label_code}")
    
    filtered = []
    for resource in resources:
        labels = get_security_labels(resource)
        for label in labels:
            if label.system == label_system and label.code == label_code:
                filtered.append(resource)
                break
    
    logger.info(f"[{current_time}] Filtered {len(resources)} resource(s) to {len(filtered)} resource(s) with security label {label_system}|{label_code}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Filter by security label operation completed")
    
    return filtered


def has_security_label(resource: "Resource", label_system: str, label_code: str) -> bool:
    """
    Check if a resource has a specific security label.
    
    Args:
        resource: FHIR resource to check
        label_system: Security label system URI to check for
        label_code: Security label code to check for
    
    Returns:
        True if resource has the security label, False otherwise
    
    Example:
        >>> if has_security_label(patient, "http://terminology.hl7.org/CodeSystem/v3-Confidentiality", "N"):
        ...     print("Patient has normal confidentiality")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking if resource {resource.resourceType}/{resource.id} has security label {label_system}|{label_code}")
    
    labels = get_security_labels(resource)
    for label in labels:
        if label.system == label_system and label.code == label_code:
            # Log completion timestamp at end of operation
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{completion_time}] Has security label operation completed (found)")
            return True
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Has security label operation completed (not found)")
    return False
