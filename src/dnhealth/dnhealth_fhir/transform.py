# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 resource transformation utilities.

Provides functions to transform FHIR resources using mappings or rules.
"""

from typing import Dict, List, Optional, Any, Callable
from copy import deepcopy
import dataclasses
import logging
from datetime import datetime

from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


def transform_resource(
    resource: FHIRResource,
    mapping: Dict[str, Any],    target_resource_type: Optional[str] = None
) -> FHIRResource:
    """
    Transform a FHIR resource using a field mapping.
    
    Args:
        resource: FHIR resource to transform
        mapping: Dictionary mapping source field paths to target field paths
                 Example: {"status": "status", "name.family": "familyName"}
        target_resource_type: Optional target resource type (if different from source)
        
    Returns:
        Transformed FHIRResource object
        
    Raises:
        ValueError: If transformation fails
    """
    # For now, implement basic field mapping
    # If target_resource_type is specified, we'd need to create new resource type
    # For simplicity, we'll transform fields in place
    
    transformed = deepcopy(resource)
    
    # Apply field mappings
    for source_path, target_path in mapping.items():
        # Get value from source path
        source_value = _get_field_value_by_path(resource, source_path)
        
        if source_value is not None:
            # Set value at target path
            _set_field_value_by_path(transformed, target_path, source_value)
    
    # Change resource type if specified
    if target_resource_type and target_resource_type != resource.resourceType:
        transformed.resourceType = target_resource_type
    
    return transformed


def _get_field_value_by_path(resource: FHIRResource, path: str) -> Any:
    """
    Get field value by path.
    
    Args:
        resource: FHIR resource
        path: Field path (e.g., "status" or "name.family")
        
    Returns:
        Field value or None
    """
    parts = path.split(".")
    current = resource
    
    for part in parts:
        if current is None:
            return None
        
        if hasattr(current, part):
            current = getattr(current, part)
        elif isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and len(current) > 0:
            # Handle list - get first item
            current = current[0]
            if hasattr(current, part):
                current = getattr(current, part)
            else:
                return None
        else:
            return None
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return current


def _set_field_value_by_path(resource: FHIRResource, path: str, value: Any) -> None:
    """
    Set field value by path.
    
    Args:
        resource: FHIR resource
        path: Field path (e.g., "status" or "name.family")
        value: Value to set
    """
    parts = path.split(".")
    
    if len(parts) == 1:
        # Simple field
        if hasattr(resource, parts[0]):
            setattr(resource, parts[0], value)
    else:
        # Nested path - for now, only handle simple cases
        # This is a simplified implementation
        field_name = parts[0]
        if hasattr(resource, field_name):
            field_value = getattr(resource, field_name)
            if isinstance(field_value, list) and len(field_value) > 0:
                # Set on first item in list
                nested_path = ".".join(parts[1:])
                if hasattr(field_value[0], nested_path):
                    setattr(field_value[0], nested_path, value)
            elif hasattr(field_value, parts[1]):
                setattr(field_value, parts[1], value)


def apply_field_mapping(
    resource: FHIRResource,
    field_mapping: Dict[str, str]
) -> FHIRResource:
    """
    Apply field mapping to a resource.
    
    Args:
        resource: FHIR resource to transform
        field_mapping: Dictionary mapping source paths to target paths
        
    Returns:
        Transformed resource

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
    """
    return transform_resource(resource, field_mapping)


def create_resource_mapping(
    source_resource_type: str,
    target_resource_type: str,
    field_mappings: Dict[str, str],
    transformation_rules: Optional[Dict[str, Callable]] = None
) -> Dict[str, Any]:
    """
    Create a resource mapping configuration.
    
    Args:
        source_resource_type: Source resource type (e.g., "Patient")
        target_resource_type: Target resource type (e.g., "Person")
        field_mappings: Dictionary mapping source field paths to target field paths
        transformation_rules: Optional dictionary of transformation functions keyed by field path
        
    Returns:
        Mapping configuration dictionary
        
    Example:
        mapping = create_resource_mapping(
            "Patient",
            "Person",
            {
                "name.family": "name.family",
                "name.given": "name.given",
                "birthDate": "birthDate"
            },
            {
                "name.family": lambda x: x.upper() if x else None
            }
        )
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Creating resource mapping: {source_resource_type} -> {target_resource_type}")
    
    return {
        "source_resource_type": source_resource_type,
        "target_resource_type": target_resource_type,
        "field_mappings": field_mappings,
        "transformation_rules": transformation_rules or {}
    }


def apply_resource_mapping(
    resource: FHIRResource,
    mapping_config: Dict[str, Any]
) -> FHIRResource:
    """
    Apply a resource mapping configuration to transform a resource.
    
    Args:
        resource: Source FHIR resource to transform
        mapping_config: Mapping configuration created with create_resource_mapping()
        
    Returns:
        Transformed FHIRResource object
        
    Raises:
        ValueError: If resource type doesn't match mapping configuration
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Applying resource mapping to {resource.resourceType}")
    
    # Verify resource type matches mapping
    if resource.resourceType != mapping_config.get("source_resource_type"):
        raise ValueError(
            f"Resource type {resource.resourceType} does not match mapping source type "
            f"{mapping_config.get('source_resource_type')}"
        )
    
    # Get mapping components
    field_mappings = mapping_config.get("field_mappings", {})
    transformation_rules = mapping_config.get("transformation_rules", {})
    target_resource_type = mapping_config.get("target_resource_type")
    
    # Transform resource
    transformed = deepcopy(resource)
    
    # Apply field mappings with transformations
    for source_path, target_path in field_mappings.items():
        # Get source value
        source_value = _get_field_value_by_path(resource, source_path)
        
        if source_value is not None:
            # Apply transformation if rule exists
            if source_path in transformation_rules:
                transform_func = transformation_rules[source_path]
                try:
                    source_value = transform_func(source_value)
                except Exception as e:
                    logger.warning(
                        f"[{current_time}] Transformation failed for {source_path}: {e}"
                    )
                    continue
            
            # Set transformed value at target path
            _set_field_value_by_path(transformed, target_path, source_value)
    
    # Change resource type if specified
    if target_resource_type and target_resource_type != resource.resourceType:
        transformed.resourceType = target_resource_type
    
    logger.debug(f"[{current_time}] Resource mapping completed: {resource.resourceType} -> {transformed.resourceType}")
    return transformed


def map_resources(
    resources: List[FHIRResource],
    mapping_config: Dict[str, Any]
) -> List[FHIRResource]:
    """
    Map multiple resources using a mapping configuration.
    
    Args:
        resources: List of source FHIR resources to transform
        mapping_config: Mapping configuration created with create_resource_mapping()
        
    Returns:
        List of transformed FHIRResource objects
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Mapping {len(resources)} resources")
    
    transformed_resources = []

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    for resource in resources:
        try:
            transformed = apply_resource_mapping(resource, mapping_config)
            transformed_resources.append(transformed)
        except ValueError as e:
            logger.warning(f"[{current_time}] Skipping resource {resource.resourceType}: {e}")
            continue
    
    logger.debug(f"[{current_time}] Mapping completed: {len(transformed_resources)} resources transformed")
    return transformed_resources


def get_jsonpath_for_field(resource: FHIRResource, field_path: str) -> str:
    """
    Generate JSONPath expression for a field in a resource.
    
    Args:
        resource: FHIR resource
        field_path: Field path (e.g., "name.family" or "name[0].family")
        

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    Returns:
        JSONPath expression (e.g., "$.name[0].family")
    """
    parts = field_path.split(".")
    jsonpath_parts = ["$"]
    
    for part in parts:
        if "[" in part:
            # Already has array index
            jsonpath_parts.append(part)
        else:
            jsonpath_parts.append(part)
    
    return ".".join(jsonpath_parts)


def validate_mapping_config(mapping_config: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate a resource mapping configuration.
    
    Args:
        mapping_config: Mapping configuration dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    if "source_resource_type" not in mapping_config:
        errors.append("Missing required field: source_resource_type")
    
    if "target_resource_type" not in mapping_config:
        errors.append("Missing required field: target_resource_type")
    
    if "field_mappings" not in mapping_config:
        errors.append("Missing required field: field_mappings")
    elif not isinstance(mapping_config["field_mappings"], dict):
        errors.append("field_mappings must be a dictionary")
    
    # Check transformation rules if present
    if "transformation_rules" in mapping_config:
        if not isinstance(mapping_config["transformation_rules"], dict):
            errors.append("transformation_rules must be a dictionary")
        else:
            # Verify all transformation rule keys are callable
            for key, value in mapping_config["transformation_rules"].items():
                if not callable(value):
                    errors.append(f"transformation_rules[{key}] must be callable")
    
    return len(errors) == 0, errors

