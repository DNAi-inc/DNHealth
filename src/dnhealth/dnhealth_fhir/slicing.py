# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Slicing support.

Slicing allows elements to be divided into multiple variants based on discriminator values.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.structuredefinition import ElementDefinition, get_element_definitions

logger = logging.getLogger(__name__)


@dataclass
class SlicingDiscriminator:
    """
    Represents a slicing discriminator.
    
    Discriminators define how to distinguish between slices.
    """
    
    type: str  # value, exists, pattern, type, profile
    path: str  # Path to element to discriminate on


@dataclass
class SlicingDefinition:
    """
    Represents a slicing definition from ElementDefinition.
    """
    
    discriminator: List[SlicingDiscriminator] = field(default_factory=list)
    description: Optional[str] = None
    ordered: Optional[bool] = None
    rules: Optional[str] = None  # closed, open, openAtEnd


def parse_slicing_definition(element: ElementDefinition) -> Optional[SlicingDefinition]:
    """
    Parse a slicing definition from an ElementDefinition.
    
    Args:
        element: ElementDefinition with slicing information
        
    Returns:
        SlicingDefinition object or None if no slicing
    """
    if not element.slicing:
        return None
    
    slicing_def = SlicingDefinition()
    
    # Parse discriminator
    if isinstance(element.slicing, dict):
        discriminator_data = element.slicing.get("discriminator", [])
        if isinstance(discriminator_data, list):
            for disc_data in discriminator_data:
                if isinstance(disc_data, dict):
                    disc = SlicingDiscriminator(
                        type=disc_data.get("type", "value"),
                        path=disc_data.get("path", "")
                    )
                    slicing_def.discriminator.append(disc)
        
        slicing_def.description = element.slicing.get("description")
        slicing_def.ordered = element.slicing.get("ordered")
        slicing_def.rules = element.slicing.get("rules")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return slicing_def


def get_sliced_elements(elements: List[ElementDefinition]) -> Dict[str, List[ElementDefinition]]:
    """
    Group elements by their slice names.
    
    Args:
        elements: List of ElementDefinition objects
        
    Returns:
        Dictionary mapping base paths to lists of sliced elements
    """
    sliced = {}
    
    for element in elements:
        if element.sliceName:
            base_path = element.path.rsplit(":", 1)[0] if ":" in element.path else element.path
            if base_path not in sliced:
                sliced[base_path] = []
            sliced[base_path].append(element)
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return sliced


def validate_slicing(
    resource: Any,
    element: ElementDefinition,
    slicing_def: SlicingDefinition,
    field_value: Any,
    all_elements: Optional[List[ElementDefinition]] = None
) -> List[str]:
    """
    Validate slicing constraints on a field value.
    
    Args:
        resource: FHIR resource
        element: ElementDefinition with slicing
        slicing_def: SlicingDefinition
        field_value: Field value to validate
        all_elements: Optional list of all ElementDefinition objects (for finding slice definitions)
        
    Returns:
        List of validation error messages (empty if valid)
    """
    start_time = datetime.now()
    errors = []
    
    if not isinstance(field_value, list):
        return errors  # Slicing only applies to lists
    
    if not slicing_def.discriminator:
        return errors  # No discriminator defined, can't validate
    
    # Get all sliced elements for this base path
    base_path = element.path
    sliced_elements = []
    if all_elements:
        for elem in all_elements:
            if elem.sliceName and elem.path.startswith(base_path):
                sliced_elements.append(elem)
    
    # Group items by discriminator values
    if slicing_def.discriminator:
        # Use first discriminator for grouping
        discriminator = slicing_def.discriminator[0]
        grouped_items = apply_slicing_discriminator(field_value, discriminator, resource)
        
        # Check slicing rules
        if slicing_def.rules == "closed":
            # All items must match a slice
            # Check that all discriminator values correspond to defined slices
            for disc_value, items in grouped_items.items():
                # Check if this discriminator value matches any slice
                matched_slice = False
                for slice_elem in sliced_elements:
                    # Check if slice matches discriminator value
                    # This is simplified - full implementation would check slice constraints
                    if slice_elem.sliceName:
                        matched_slice = True
                        break
                
                if not matched_slice and disc_value:
                    errors.append(
                        f"Slicing rule 'closed' violated: items with discriminator value '{disc_value}' "
                        f"do not match any defined slice for path '{base_path}'"
                    )
        
        elif slicing_def.rules == "openAtEnd":
            # Items can match slices or be unmatched, but unmatched items must be at the end
            unmatched_found = False
            for i, item in enumerate(field_value):
                disc_value = _get_discriminator_value(item, discriminator, resource)
                matched_slice = False
                
                for slice_elem in sliced_elements:
                    if slice_elem.sliceName:
                        matched_slice = True
                        break
                
                if not matched_slice and disc_value:
                    unmatched_found = True
                elif unmatched_found and matched_slice:
                    errors.append(
                        f"Slicing rule 'openAtEnd' violated: unmatched items must be at the end "
                        f"for path '{base_path}'"
                    )
                    break
    
    # Check ordered constraint if specified
    if slicing_def.ordered:
        # If ordered, items should be in a specific order
        # This is a simplified check - full implementation would validate order constraints
        pass
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Slicing validation completed in {elapsed:.3f} seconds ({len(errors)} errors)")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def apply_slicing_discriminator(
    items: List[Any],
    discriminator: SlicingDiscriminator,
    resource: Any
) -> Dict[str, List[Any]]:
    """
    Apply a slicing discriminator to group items into slices.
    
    Args:
        items: List of items to slice
        discriminator: SlicingDiscriminator
        resource: FHIR resource (for context)
        
    Returns:
        Dictionary mapping slice names to lists of items
    """
    slices: Dict[str, List[Any]] = {}
    
    for item in items:
        slice_key = _get_discriminator_value(item, discriminator, resource)
        if slice_key not in slices:
            slices[slice_key] = []
        slices[slice_key].append(item)
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return slices


def _get_discriminator_value(
    item: Any,
    discriminator: SlicingDiscriminator,
    resource: Any
) -> str:
    """
    Get the discriminator value for an item.
    
    Args:
        item: Item to get discriminator value from
        discriminator: SlicingDiscriminator
        resource: FHIR resource (for context)
        
    Returns:
        Discriminator value as string
    """
    if discriminator.type == "value":
        # Get value from path
        value = _get_value_by_path(item, discriminator.path)
        return str(value) if value is not None else ""
    elif discriminator.type == "exists":
        # Check if path exists
        value = _get_value_by_path(item, discriminator.path)
        return "true" if value is not None else "false"
    elif discriminator.type == "pattern":
        # Match pattern (simplified)
        value = _get_value_by_path(item, discriminator.path)
        return str(value) if value is not None else ""
    elif discriminator.type == "type":
        # Match type
        return type(item).__name__
    elif discriminator.type == "profile":
        # Match profile (simplified)
        return "default"
    
    return "default"


def _get_value_by_path(obj: Any, path: str) -> Any:
    """
    Get value from object by path.
    
    Args:
        obj: Object to get value from
        path: Path to value (e.g., "system" or "coding.system")
        
    Returns:
        Value or None
    """
    if not path:
        return None
    
    parts = path.split(".")
    current = obj
    
    for part in parts:
        if hasattr(current, part):
            current = getattr(current, part)
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            return None
        
        if current is None:
            return None
    
    return current


def get_slice_by_name(elements: List[ElementDefinition], slice_name: str) -> Optional[ElementDefinition]:
    """
    Get an ElementDefinition by slice name.
    
    Args:
        elements: List of ElementDefinition objects
        slice_name: Slice name
        
    Returns:
        ElementDefinition or None if not found
    """
    for element in elements:
        if element.sliceName == slice_name:
            return element
    return None

