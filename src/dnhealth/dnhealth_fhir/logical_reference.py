# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Logical Reference handling.

Logical references use identifiers instead of direct resource references.
This module provides utilities for parsing, validating, and handling logical references.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.types import Reference, Identifier
from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


def is_logical_reference(reference: Reference) -> bool:
    """
    Check if a reference is a logical reference (uses identifier instead of direct reference).
    
    Logical references use the identifier field to reference resources by their
    business identifiers rather than by direct resource type/id references.
    
    Args:
        reference: Reference to check
        
    Returns:
        True if this is a logical reference, False otherwise
    """
    # Logical reference has identifier but may or may not have reference
    # If it has identifier and no reference (or reference is empty), it's logical
    if reference.identifier and not reference.reference:
        return True
    
    # If it has both, check if reference is just a placeholder
    # In FHIR, logical references can have a reference field with just the resource type
    if reference.identifier and reference.reference:
        # If reference is just a resource type (no id), it's likely logical
        if "/" not in reference.reference:
            return True
    
    return False


def parse_logical_reference(reference: Reference) -> Optional[Dict[str, Any]]:
    """
    Parse a logical reference to extract identifier information.
    
    Args:
        reference: Logical reference to parse
        
    Returns:
        Dictionary with identifier information, or None if not a logical reference
    """
    if not is_logical_reference(reference):
        return None
    
    if not reference.identifier:
        return None
    
    return {
        "system": reference.identifier.system,
        "value": reference.identifier.value,
        "type": reference.type,  # Optional resource type hint
        "display": reference.display  # Optional display text
    }


def validate_logical_reference(reference: Reference) -> List[str]:
    """
    Validate a logical reference.
    
    Validates that:
    - Identifier is present (required for logical references)
    - Identifier has at least a value
    - If reference field is present, it should be a valid resource type
    
    Args:
        reference: Logical reference to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if not is_logical_reference(reference):
        return errors  # Not a logical reference, skip validation
    
    # Logical reference must have identifier
    if not reference.identifier:
        errors.append("Logical reference must have an identifier")
        return errors
    
    # Identifier must have a value
    if not reference.identifier.value:
        errors.append("Logical reference identifier must have a value")
    
    # If reference type is specified, validate it's a valid resource type name
    if reference.type:
        # Basic validation: should start with capital letter and be alphanumeric
        if not reference.type[0].isupper() or not reference.type.replace("_", "").isalnum():
            errors.append(f"Invalid resource type in logical reference: '{reference.type}'")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def resolve_logical_reference(
    reference: Reference,
    resources: List[FHIRResource],
    resource_type: Optional[str] = None
) -> Optional[FHIRResource]:
    """
    Resolve a logical reference by finding a resource with matching identifier.
    
    Args:
        reference: Logical reference to resolve
        resources: List of resources to search
        resource_type: Optional resource type to filter by
        
    Returns:
        Matching resource if found, None otherwise
    """
    if not is_logical_reference(reference) or not reference.identifier:
        return None
    
    # Get identifier system and value
    identifier_system = reference.identifier.system
    identifier_value = reference.identifier.value
    
    if not identifier_value:
        return None
    
    # Search for matching resource
    for resource in resources:
        # Filter by resource type if specified
        if resource_type and hasattr(resource, "resourceType"):
            if resource.resourceType != resource_type:
                continue
        
        # Check if resource has identifier field
        if hasattr(resource, "identifier") and resource.identifier:
            # Handle both single identifier and list of identifiers
            identifiers = resource.identifier if isinstance(resource.identifier, list) else [resource.identifier]
            
            for ident in identifiers:
                if isinstance(ident, Identifier):
                    # Match by value (required) and system (if specified)
                    if ident.value == identifier_value:
                        # If system is specified, it must match
                        if identifier_system:
                            if ident.system == identifier_system:
                                # Log completion timestamp at end of operation
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                logger.debug(f"[{current_time}] Logical reference resolution completed successfully")
                                return resource
                        else:
                            # No system specified, match by value only
                            # Log completion timestamp at end of operation
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            logger.debug(f"[{current_time}] Logical reference resolution completed successfully")
                            return resource
    
    # Log completion timestamp at end of operation (even if not found)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Logical reference resolution completed (no match found)")
    return None


def create_logical_reference(
    identifier: Identifier,
    resource_type: Optional[str] = None,
    display: Optional[str] = None
) -> Reference:
    """
    Create a logical reference from an identifier.
    
    Args:
        identifier: Identifier to use for the logical reference
        resource_type: Optional resource type hint
        display: Optional display text
        
    Returns:
        Reference object configured as a logical reference
    """
    result = Reference(
        reference=resource_type if resource_type else None,  # Optional type hint
        type=resource_type,
        identifier=identifier,
        display=display
    )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Logical reference creation completed successfully")
    
    return result
