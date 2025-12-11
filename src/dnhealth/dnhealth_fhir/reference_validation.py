# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Reference validation.

Validates that references point to existing resources.
"""

from typing import List, Optional, Dict, Set
import re
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.types import Reference
from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


def parse_reference(reference_str: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a reference string into resource type and id.
    
    Args:
        reference_str: Reference string (e.g., "Patient/123" or "http://example.com/Patient/123")
        
    Returns:
        Tuple of (resource_type, resource_id) or (None, None) if invalid format
    """
    if not reference_str:
        return None, None
    
    # Handle full URL references
    if reference_str.startswith("http://") or reference_str.startswith("https://"):
        # Extract resource type and id from URL
        # Format: http://example.com/fhir/ResourceType/id
        parts = reference_str.rstrip("/").split("/")
        if len(parts) >= 2:
            resource_id = parts[-1]
            resource_type = parts[-2]
            return resource_type, resource_id
        return None, None
    
    # Handle relative references (ResourceType/id)
    if "/" in reference_str:
        parts = reference_str.split("/", 1)
        if len(parts) == 2:
            resource_type, resource_id = parts
            return resource_type, resource_id
    
    # Handle just an id (assumes same resource type)
    result = (None, reference_str)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Reference parsing completed: {result}")
    
    return result


def validate_reference_format(reference: Reference) -> List[str]:
    """
    Validate that a reference has a valid format.
    
    Args:
        reference: Reference to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Reference must have either reference or identifier
    if not reference.reference and not reference.identifier:
        errors.append("Reference must have either 'reference' or 'identifier'")
        return errors
    
    # If reference string is provided, validate format
    if reference.reference:
        resource_type, resource_id = parse_reference(reference.reference)
        
        # Check if it's a valid format
        if resource_type is None and resource_id is None:
            # Check if it's a valid relative reference format
            if not re.match(r'^[A-Z][a-zA-Z0-9]*/[A-Za-z0-9\-\.]{1,64}$', reference.reference):
                # Check if it's a valid URL
                if not (reference.reference.startswith("http://") or reference.reference.startswith("https://")):
                    errors.append(f"Invalid reference format: '{reference.reference}'")
        
        # If type is specified, check that it matches the reference
        if reference.type and resource_type:
            if reference.type != resource_type:
                errors.append(
                    f"Reference type '{reference.type}' does not match reference string type '{resource_type}'"
                )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Reference format validation completed: {len(errors)} errors found")
    
    return errors


def get_resources_by_id(bundle: Optional["Bundle"] = None, resources: Optional[List[FHIRResource]] = None) -> Dict[str, FHIRResource]:
    """
    Build a map of resource IDs from a Bundle or list of resources.
    
    Args:
        bundle: Optional Bundle containing resources
        resources: Optional list of resources
        
    Returns:
        Dictionary mapping "ResourceType/id" to resource
    """
    resource_map: Dict[str, FHIRResource] = {}
    
    # Add resources from bundle
    if bundle:
        from dnhealth.dnhealth_fhir.resources.bundle import Bundle
        if isinstance(bundle, Bundle) and bundle.entry:
            for entry in bundle.entry:
                if entry.resource and entry.resource.id:
                    key = f"{entry.resource.resourceType}/{entry.resource.id}"
                    resource_map[key] = entry.resource
                # Also use fullUrl if available
                if entry.fullUrl:
                    resource_map[entry.fullUrl] = entry.resource
    
    # Add resources from list
    if resources:
        for resource in resources:
            if resource.id:
                key = f"{resource.resourceType}/{resource.id}"
                resource_map[key] = resource
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return resource_map


def validate_reference_exists(
    reference: Reference,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None,
    expected_resource_types: Optional[Set[str]] = None
) -> List[str]:
    """
    Validate that a reference points to an existing resource.
    
    Args:
        reference: Reference to validate
        bundle: Optional Bundle containing resources to check against
        resources: Optional list of resources to check against
        expected_resource_types: Optional set of expected resource types
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # If no bundle or resources provided, we can't validate existence
    if not bundle and not resources:
        return errors
    
    # Validate format first
    format_errors = validate_reference_format(reference)
    errors.extend(format_errors)
    
    # If format is invalid, don't check existence
    if format_errors:
        return errors
    
    # Build resource map
    resource_map = get_resources_by_id(bundle, resources)
    
    # Check if reference exists
    if reference.reference:
        # Check direct match
        if reference.reference in resource_map:
            # Check resource type if expected
            if expected_resource_types:
                found_resource = resource_map[reference.reference]
                if found_resource.resourceType not in expected_resource_types:
                    errors.append(
                        f"Referenced resource type '{found_resource.resourceType}' is not in expected types {expected_resource_types}"
                    )
            return errors
        
        # Parse and check
        resource_type, resource_id = parse_reference(reference.reference)
        if resource_type and resource_id:
            key = f"{resource_type}/{resource_id}"
            if key in resource_map:
                # Check resource type if expected
                if expected_resource_types:
                    found_resource = resource_map[key]
                    if found_resource.resourceType not in expected_resource_types:
                        errors.append(
                            f"Referenced resource type '{found_resource.resourceType}' is not in expected types {expected_resource_types}"
                        )
                return errors
        
        # Reference not found
        errors.append(f"Referenced resource '{reference.reference}' not found")
    
    # If using identifier, we can't easily validate without a terminology server
    # For now, we just validate that identifier is present
    if reference.identifier:
        # Identifier-based references are valid but we can't check existence locally
        pass
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Reference existence validation completed: {len(errors)} errors found")
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def resolve_relative_reference(
    reference_str: str,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None,
    base_url: Optional[str] = None
) -> Optional[FHIRResource]:
    """
    Resolve a relative reference within a Bundle or list of resources.
    
    Relative references are resolved by finding resources within the same
    Bundle or resource list. If base_url is provided, absolute references
    are also resolved.
    
    Args:
        reference_str: Reference string to resolve (e.g., "Patient/123")
        bundle: Optional Bundle containing resources
        resources: Optional list of resources
        base_url: Optional base URL for resolving absolute references
        
    Returns:
        Resolved resource if found, None otherwise
    """
    if not reference_str:
        return None
    
    # Build resource map
    resource_map = get_resources_by_id(bundle, resources)
    
    # Check direct match
    if reference_str in resource_map:
        return resource_map[reference_str]
    
    # Parse and check
    resource_type, resource_id = parse_reference(reference_str)
    if resource_type and resource_id:
        key = f"{resource_type}/{resource_id}"
        if key in resource_map:
            return resource_map[key]
    
    # If it's an absolute URL and base_url is provided, try to resolve
    if base_url and (reference_str.startswith("http://") or reference_str.startswith("https://")):
        # Extract resource type and id from absolute URL
        resource_type, resource_id = parse_reference(reference_str)
        if resource_type and resource_id:
            key = f"{resource_type}/{resource_id}"
            if key in resource_map:
                result = resource_map[key]
                
                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.debug(f"[{current_time}] Relative reference resolution completed: resolved '{reference_str}' to {result.resourceType}/{result.id if result.id else 'N/A'}")
                
                return result
    
    # Log completion timestamp at end of operation (not found)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Relative reference resolution completed: '{reference_str}' not found")
    
    return None


def resolve_reference_chain(
    reference: Reference,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None,
    contained_resources: Optional[List[FHIRResource]] = None,
    max_depth: int = 10,
    visited: Optional[Set[str]] = None
) -> Optional[List[FHIRResource]]:
    """
    Resolve a reference chain by following references recursively.
    
    This function follows a chain of references, resolving each reference
    and then following references within the resolved resource, up to max_depth.
    Supports all reference types: contained (#id), relative (ResourceType/id),
    absolute URLs, logical (identifier-based), and canonical references.
    
    Args:
        reference: Starting reference
        bundle: Optional Bundle containing resources
        resources: Optional list of resources
        contained_resources: Optional list of contained resources
        max_depth: Maximum depth to follow references (default: 10)
        visited: Set of already visited resource IDs (to prevent cycles)
        
    Returns:
        List of resources in the reference chain, or None if chain is broken
    """
    if max_depth <= 0:
        return None
    
    if visited is None:
        visited = set()
    
    # Resolve initial reference using comprehensive resolution
    resource = None
    
    # Try contained resource reference first
    if reference.reference and reference.reference.startswith("#"):
        from dnhealth.dnhealth_fhir.contained import resolve_contained_reference
        if contained_resources:
            resource = resolve_contained_reference(reference.reference, contained_resources)
    
    # Try relative/absolute reference
    if not resource and reference.reference:
        resource = resolve_relative_reference(reference.reference, bundle, resources)
    
    # Try logical reference (identifier-based)
    if not resource and reference.identifier:
        from dnhealth.dnhealth_fhir.logical_reference import resolve_logical_reference
        all_resources = []
        if bundle:
            from dnhealth.dnhealth_fhir.resources.bundle import Bundle
            if isinstance(bundle, Bundle) and bundle.entry:
                all_resources.extend([e.resource for e in bundle.entry if e.resource])
        if resources:
            all_resources.extend(resources)
        if all_resources:
            resource = resolve_logical_reference(reference, all_resources, reference.type)
    
    # Try canonical reference if reference.reference looks like a canonical URL
    if not resource and reference.reference:
        from dnhealth.dnhealth_fhir.canonical import is_canonical_reference, resolve_canonical_reference
        if is_canonical_reference(reference.reference):
            all_resources = []
            if bundle:
                from dnhealth.dnhealth_fhir.resources.bundle import Bundle
                if isinstance(bundle, Bundle) and bundle.entry:
                    all_resources.extend([e.resource for e in bundle.entry if e.resource])
            if resources:
                all_resources.extend(resources)
            if all_resources:
                resource = resolve_canonical_reference(reference.reference, all_resources, reference.type)
    
    if not resource:
        return None
    
    # Check for cycles
    resource_key = f"{resource.resourceType}/{resource.id}" if resource.id else None
    if resource_key and resource_key in visited:
        return None  # Cycle detected
    if resource_key:
        visited.add(resource_key)
    
    chain = [resource]
    
    # If max_depth allows, look for references in this resource and follow them
    if max_depth > 1:
        # Search for Reference fields in the resource
        from dataclasses import fields
        for field in fields(resource):
            field_value = getattr(resource, field.name, None)
            if field_value:
                # Check if field is a Reference
                if isinstance(field_value, Reference):
                    sub_chain = resolve_reference_chain(
                        field_value, bundle, resources, contained_resources, max_depth - 1, visited
                    )
                    if sub_chain:
                        chain.extend(sub_chain)
                # Check if field is a list of References
                elif isinstance(field_value, list):
                    for item in field_value:
                        if isinstance(item, Reference):
                            sub_chain = resolve_reference_chain(
                                item, bundle, resources, contained_resources, max_depth - 1, visited
                            )
                            if sub_chain:
                                chain.extend(sub_chain)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Reference chain resolution completed: {len(chain)} resources in chain")
    
    return chain

