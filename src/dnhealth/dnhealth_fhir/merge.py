# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 resource merging utilities.

Provides functions to merge multiple FHIR resources.
"""

from typing import List, Optional, Any, Dict
from copy import deepcopy
import dataclasses
import logging
from datetime import datetime

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry

logger = logging.getLogger(__name__)


def merge_resources(
    resources: List[FHIRResource],
    merge_strategy: str = "replace",    merge_lists: str = "append"
) -> FHIRResource:
    """
    Merge multiple FHIR resources of the same type into a single resource.
    
    Args:
        resources: List of FHIR resources to merge (must be same resourceType)
        merge_strategy: Strategy for merging fields:
            - "replace": Replace fields with values from later resources (default)
            - "keep-first": Keep values from first resource
            - "combine": Combine all values (for lists)
        merge_lists: Strategy for merging list fields:
            - "append": Append all items from all resources
            - "replace": Replace with items from last resource
            - "unique": Keep unique items only
            
    Returns:
        Merged FHIRResource object
        
    Raises:
        ValueError: If resources list is empty or resources have different types
    """
    if not resources:
        raise ValueError("Cannot merge empty list of resources")
    
    if len(resources) == 1:
        return deepcopy(resources[0])
    
    # Check all resources have same type
    resource_type = resources[0].resourceType
    for res in resources[1:]:
        if res.resourceType != resource_type:
            raise ValueError(f"Cannot merge different resource types: {resource_type} vs {res.resourceType}")
    
    # Use first resource as base
    merged = deepcopy(resources[0])
    
    # Merge fields from other resources
    for resource in resources[1:]:
        merged = _merge_resource_fields(merged, resource, merge_strategy, merge_lists)
    
    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return merged


def _merge_resource_fields(
    base: FHIRResource,
    other: FHIRResource,
    merge_strategy: str,
    merge_lists: str
) -> FHIRResource:
    """
    Merge fields from another resource into base resource.
    
    Args:
        base: Base resource to merge into
        other: Resource to merge from
        merge_strategy: Strategy for merging fields
        merge_lists: Strategy for merging list fields
        
    Returns:
        Merged resource
    """
    # Get all fields from both resources
    base_fields = {f.name for f in dataclasses.fields(base)}
    other_fields = {f.name for f in dataclasses.fields(other)}
    
    # Merge each field
    for field_name in base_fields | other_fields:
        base_value = getattr(base, field_name, None)
        other_value = getattr(other, field_name, None)
        
        if other_value is None:
            continue  # Skip if other doesn't have this field
        
        if base_value is None:
            # Base doesn't have this field, copy from other
            setattr(base, field_name, deepcopy(other_value))
            continue
        
        # Both have the field - merge based on type
        if isinstance(base_value, list) and isinstance(other_value, list):
            # Merge lists
            if merge_lists == "append":
                merged_list = base_value + [deepcopy(item) for item in other_value]
            elif merge_lists == "replace":
                merged_list = [deepcopy(item) for item in other_value]
            elif merge_lists == "unique":
                # Keep unique items (simple comparison)
                merged_list = list(base_value)
                for item in other_value:
                    if item not in merged_list:
                        merged_list.append(deepcopy(item))
            else:
                merged_list = base_value + [deepcopy(item) for item in other_value]
            setattr(base, field_name, merged_list)
        elif merge_strategy == "replace":
            # Replace with other value
            setattr(base, field_name, deepcopy(other_value))
        elif merge_strategy == "keep-first":
            # Keep base value
            pass
        else:

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            # Default: replace
            setattr(base, field_name, deepcopy(other_value))
    
    return base


def merge_resources_into_bundle(
    resources: List[FHIRResource],
    bundle_type: str = "collection"
) -> Bundle:
    """
    Merge multiple FHIR resources into a Bundle.
    
    Args:
        resources: List of FHIR resources to include in bundle
        bundle_type: Bundle type (default: collection)
        
    Returns:
        Bundle resource containing all resources
    """
    from datetime import datetime
    
    entries = []
    for resource in resources:
        full_url = f"{resource.resourceType}/{resource.id}" if resource.id else None
        entry = BundleEntry(
            fullUrl=full_url,
            resource=resource
        )
        entries.append(entry)
    
    bundle = Bundle(
        resourceType="Bundle",
        type=bundle_type,
        entry=entries,
        timestamp=datetime.now().isoformat(),
        total=len(entries)
    )
    
    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return bundle

