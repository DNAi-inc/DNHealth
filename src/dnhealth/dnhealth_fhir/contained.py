# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 contained resource utilities.

Provides functions for parsing, resolving, validating, and serializing
contained resources within FHIR resources.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from dnhealth.dnhealth_fhir.resources.base import DomainResource, FHIRResource
from dnhealth.dnhealth_fhir.types import Reference
from dnhealth.errors import FHIRParseError

logger = logging.getLogger(__name__)


def resolve_contained_reference(
    reference: str,
    contained_resources: List[FHIRResource],    recursive: bool = True
) -> Optional[FHIRResource]:
    """
    Resolve a reference to a contained resource.
    
    Contained resource references use the format "#<id>" where <id> is
    the id of the contained resource. Supports nested contained resources
    (contained resources within contained resources) when recursive=True.
    
    Args:
        reference: Reference string (e.g., "#patient1")
        contained_resources: List of contained resources
        recursive: If True, also search within nested contained resources
        
    Returns:
        Contained resource if found, None otherwise
    """
    if not reference or not reference.startswith("#"):
        return None
    
    resource_id = reference[1:]  # Remove leading "#"
    
    # Search in top-level contained resources
    for resource in contained_resources:
        if hasattr(resource, "id") and resource.id == resource_id:
            return resource
    
    # If recursive search is enabled, search within nested contained resources
    if recursive:
        for resource in contained_resources:
            # Check if this resource has contained resources
            if hasattr(resource, "contained") and resource.contained:
                nested_result = resolve_contained_reference(
                    reference, resource.contained, recursive=True
                )
                if nested_result:
                    return nested_result
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return None


def resolve_reference(
    reference: str,
    contained_resources: Optional[List[FHIRResource]] = None,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None
) -> Optional[FHIRResource]:
    """
    Resolve a reference, checking contained resources first, then bundle/resources.
    
    Resolution order:
    1. Contained resources (if reference starts with "#")
    2. Bundle entries (if bundle provided)
    3. Resource list (if resources provided)
    
    Args:
        reference: Reference string (may be contained "#id", relative "ResourceType/id", or absolute URL)
        contained_resources: Optional list of contained resources
        bundle: Optional Bundle containing resources
        resources: Optional list of resources
        
    Returns:
        Resolved resource if found, None otherwise
    """
    # Check contained resources first (for "#id" references)
    if reference and reference.startswith("#"):
        if contained_resources:
            return resolve_contained_reference(reference, contained_resources)
        return None
    
    # Check bundle
    if bundle:
        from dnhealth.dnhealth_fhir.resources.bundle import Bundle
        if isinstance(bundle, Bundle) and bundle.entry:
            # Check fullUrl first
            for entry in bundle.entry:
                if entry.fullUrl == reference:
                    return entry.resource
            
            # Parse reference and check resource type/id
            if "/" in reference:
                parts = reference.split("/", 1)
                if len(parts) == 2:
                    resource_type, resource_id = parts
                    for entry in bundle.entry:
                        if entry.resource and entry.resource.resourceType == resource_type and entry.resource.id == resource_id:
                            return entry.resource
    
    # Check resources list
    if resources:
        # Parse reference
        if "/" in reference:
            parts = reference.split("/", 1)
            if len(parts) == 2:
                resource_type, resource_id = parts
                for resource in resources:
                    if hasattr(resource, "resourceType") and hasattr(resource, "id"):
                        if resource.resourceType == resource_type and resource.id == resource_id:
                            return resource
    
    return None


def _collect_all_contained_ids(resource: FHIRResource, collected_ids: Optional[set] = None) -> set:
    """
    Recursively collect all contained resource IDs from a resource and its nested contained resources.
    
    Args:
        resource: FHIRResource to collect IDs from
        collected_ids: Set to accumulate IDs (created if None)
        
    Returns:
        Set of all contained resource IDs (including nested)
    """
    if collected_ids is None:
        collected_ids = set()
    
    # Collect IDs from this resource's contained resources
    if hasattr(resource, "contained") and resource.contained:
        for contained in resource.contained:
            if isinstance(contained, FHIRResource) and hasattr(contained, "id") and contained.id:
                collected_ids.add(contained.id)
                # Recursively collect from nested contained resources
                _collect_all_contained_ids(contained, collected_ids)
    
    return collected_ids


def _traverse_fields_for_references(obj: Any, contained_ids: set, path: str = "") -> List[str]:
    """
    Traverse all fields in an object to find and validate references to contained resources.
    
    Supports nested contained resources by collecting all IDs recursively.
    
    Args:
        obj: Object to traverse (dataclass, dict, list, etc.)
        contained_ids: Set of contained resource IDs (should include nested IDs)
        path: Current field path for error reporting
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if obj is None:
        return errors
    
    # Handle Reference type
    from dnhealth.dnhealth_fhir.types import Reference
    if isinstance(obj, Reference):
        if obj.reference and obj.reference.startswith("#"):
            ref_id = obj.reference[1:]  # Remove leading "#"
            if ref_id not in contained_ids:
                errors.append(f"Reference at path '{path}' points to non-existent contained resource: #{ref_id}")
        return errors
    
    # Handle lists
    if isinstance(obj, list):
        for idx, item in enumerate(obj):
            item_path = f"{path}[{idx}]" if path else f"[{idx}]"
            errors.extend(_traverse_fields_for_references(item, contained_ids, item_path))
        return errors
    
    # Handle dictionaries
    if isinstance(obj, dict):
        for key, value in obj.items():
            item_path = f"{path}.{key}" if path else key
            errors.extend(_traverse_fields_for_references(value, contained_ids, item_path))
        return errors
    
    # Handle dataclasses
    if hasattr(obj, "__dataclass_fields__"):
        for field_name, field_value in obj.__dict__.items():
            if field_name.startswith("_"):
                continue
            item_path = f"{path}.{field_name}" if path else field_name
            errors.extend(_traverse_fields_for_references(field_value, contained_ids, item_path))
        return errors
    
    return errors


def validate_contained_resources(resource: DomainResource) -> List[str]:
    """
    Validate contained resources in a DomainResource.
    
    Validates:
    - Each contained resource has an id
    - Each contained resource has a resourceType
    - No duplicate ids within contained resources (including nested)
    - References to contained resources are valid (traverses all fields)
    - Supports nested contained resources (contained resources within contained resources)
    
    Args:
        resource: DomainResource with contained resources
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if not hasattr(resource, "contained") or not resource.contained:
        return errors
    
    # Check for duplicate ids and collect valid IDs (including nested)
    seen_ids = set()
    contained_ids = set()
    
    def validate_contained_recursive(contained_list: List[FHIRResource], parent_path: str = ""):
        """Recursively validate contained resources."""
        for idx, contained in enumerate(contained_list):
            if not isinstance(contained, FHIRResource):
                path_str = f"{parent_path}[{idx}]" if parent_path else f"[{idx}]"
                errors.append(f"Contained resource at {path_str} is not a valid FHIR resource")
                continue
            
            # Check resourceType
            if not hasattr(contained, "resourceType") or not contained.resourceType:
                path_str = f"{parent_path}[{idx}]" if parent_path else f"[{idx}]"
                errors.append(f"Contained resource at {path_str} missing resourceType")
            
            # Check id
            if not hasattr(contained, "id") or not contained.id:
                path_str = f"{parent_path}[{idx}]" if parent_path else f"[{idx}]"
                errors.append(f"Contained resource at {path_str} missing required id")
            else:
                if contained.id in seen_ids:
                    path_str = f"{parent_path}[{idx}]" if parent_path else f"[{idx}]"
                    errors.append(f"Duplicate contained resource id '{contained.id}' at {path_str}")
                seen_ids.add(contained.id)
                contained_ids.add(contained.id)
            
            # Recursively validate nested contained resources
            if hasattr(contained, "contained") and contained.contained:
                nested_path = f"{parent_path}[{idx}].contained" if parent_path else f"[{idx}].contained"
                validate_contained_recursive(contained.contained, nested_path)
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    # Validate top-level contained resources (recursively)
    validate_contained_recursive(resource.contained)
    
    # Validate references to contained resources by traversing all fields
    # Use recursive collection to include nested IDs
    all_contained_ids = set()
    for contained in resource.contained:
        if isinstance(contained, FHIRResource):
            _collect_all_contained_ids(contained, all_contained_ids)
    errors.extend(_traverse_fields_for_references(resource, all_contained_ids))
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Contained resources validation completed with {len(errors)} error(s)")
    
    return errors


def get_contained_resource_by_id(
    resource: DomainResource,
    resource_id: str
) -> Optional[FHIRResource]:
    """
    Get a contained resource by its id.
    
    Args:
        resource: DomainResource with contained resources
        resource_id: Id of the contained resource to find
        
    Returns:
        Contained resource if found, None otherwise
    """
    if not hasattr(resource, "contained") or not resource.contained:
        return None
    
    for contained in resource.contained:
        if isinstance(contained, FHIRResource) and hasattr(contained, "id"):

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
            if contained.id == resource_id:
                return contained
    
    return None


def add_contained_resource(
    resource: DomainResource,
    contained_resource: FHIRResource
) -> None:
    """
    Add a contained resource to a DomainResource.
    
    Validates that the contained resource has an id before adding.
    
    Args:
        resource: DomainResource to add contained resource to
        contained_resource: FHIRResource to add as contained
        
    Raises:
        FHIRParseError: If contained resource is invalid
    """
    if not isinstance(contained_resource, FHIRResource):
        raise FHIRParseError("Contained resource must be a FHIRResource instance")
    
    if not hasattr(contained_resource, "id") or not contained_resource.id:
        raise FHIRParseError("Contained resource must have an id")
    

            # Log completion timestamp at end of operation
    if not hasattr(resource, "contained"):
        resource.contained = []
    
    # Check for duplicate id
    if get_contained_resource_by_id(resource, contained_resource.id):
        raise FHIRParseError(f"Contained resource with id '{contained_resource.id}' already exists")
    
    resource.contained.append(contained_resource)


def remove_contained_resource(
    resource: DomainResource,
    resource_id: str
) -> bool:
    """
    Remove a contained resource by id.
    
    Args:
        resource: DomainResource to remove contained resource from
        resource_id: Id of the contained resource to remove
        
    Returns:
        True if resource was removed, False if not found
    """

            # Log completion timestamp at end of operation
    if not hasattr(resource, "contained") or not resource.contained:
        return False
    
    for idx, contained in enumerate(resource.contained):
        if isinstance(contained, FHIRResource) and hasattr(contained, "id"):
            if contained.id == resource_id:
                resource.contained.pop(idx)
                return True
    
    return False


def resolve_reference_object(
    reference: Reference,
    contained_resources: Optional[List[FHIRResource]] = None,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None
) -> Optional[FHIRResource]:
    """
    Resolve a Reference object to a resource.
    
    Handles:
    - Contained resource references (#id)
    - Relative references (ResourceType/id)
    - Absolute URL references
    - Logical references (using identifier)
    
    Args:
        reference: Reference object to resolve
        contained_resources: Optional list of contained resources
        bundle: Optional Bundle containing resources
        resources: Optional list of resources
        
    Returns:
        Resolved resource if found, None otherwise
    """
    # Handle contained resource references
    if reference.reference and reference.reference.startswith("#"):
        if contained_resources:
            return resolve_contained_reference(reference.reference, contained_resources)
        return None
    
    # Handle direct reference string
    if reference.reference:
        return resolve_reference(reference.reference, contained_resources, bundle, resources)
    
    # Handle logical references (identifier-based)
    if reference.identifier:
        from dnhealth.dnhealth_fhir.logical_reference import resolve_logical_reference
        all_resources = []
        if bundle:
            from dnhealth.dnhealth_fhir.resources.bundle import Bundle
            if isinstance(bundle, Bundle) and bundle.entry:
                all_resources.extend([e.resource for e in bundle.entry if e.resource])
        if resources:
            all_resources.extend(resources)
        
        if all_resources:
            return resolve_logical_reference(reference, all_resources, reference.type)
    
    return None
