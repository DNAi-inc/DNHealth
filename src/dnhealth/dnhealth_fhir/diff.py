# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 resource comparison and diff utilities.

Provides functions to compare two FHIR resources and identify differences.
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


@dataclass
class ResourceDiff:
    """
    Represents differences between two FHIR resources.
    """
    
    field_differences: List[Dict[str, Any]] = field(default_factory=list)
    structural_differences: List[str] = field(default_factory=list)
    identical: bool = True
    
    def add_field_difference(self, field_path: str, resource1_value: Any, resource2_value: Any):
        """Add a field difference."""
        self.identical = False
        self.field_differences.append({
            "path": field_path,
            "resource1": resource1_value,
            "resource2": resource2_value,
        })

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    def add_structural_difference(self, description: str):
        """Add a structural difference."""
        self.identical = False
        self.structural_differences.append(description)


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def _get_all_fields(resource: FHIRResource, prefix: str = "") -> Dict[str, Any]:
    """
    Get all fields from a resource recursively.
    
    Args:
        resource: FHIR resource
        prefix: Field path prefix
        
    Returns:
        Dictionary mapping field paths to values
    """
    fields = {}
    
    if resource is None:
        return fields
    
    # Get all attributes
    for key, value in resource.__dict__.items():
        if key.startswith("_"):
            continue  # Skip internal fields
        
        field_path = f"{prefix}.{key}" if prefix else key
        
        if value is None:
            continue  # Skip None values
        
        if isinstance(value, list):
            if len(value) == 0:
                continue
            # For lists, store as list or individual items
            fields[field_path] = value
        elif isinstance(value, (str, int, float, bool)):
            fields[field_path] = value
        elif hasattr(value, "__dict__"):
            # Nested object - recurse
            nested_fields = _get_all_fields(value, field_path)
            fields.update(nested_fields)
        else:
            fields[field_path] = value
    
    return fields


def _normalize_value(value: Any) -> Any:
    """
    Normalize a value for comparison.
    
    Args:
        value: Value to normalize
        
    Returns:
        Normalized value
    """
    if value is None:
        return None
    
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    
    if hasattr(value, "__dict__"):
        # Convert object to dict
        result = {}
        for key, val in value.__dict__.items():
            if not key.startswith("_"):
                result[key] = _normalize_value(val)
        return result

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    return value


def compare_resources(resource1: FHIRResource, resource2: FHIRResource) -> ResourceDiff:
    """
    Compare two FHIR resources and return differences.
    
    Args:
        resource1: First resource to compare
        resource2: Second resource to compare
        
    Returns:
        ResourceDiff object containing all differences
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Resource comparison started at {current_time}")
    
    diff = ResourceDiff()
    
    # Compare resource types
    if resource1.resourceType != resource2.resourceType:
        diff.add_structural_difference(
            f"Resource type mismatch: {resource1.resourceType} vs {resource2.resourceType}"
        )
        end_time = datetime.now()
        completion_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"Resource comparison completed at {completion_time}: "
            f"Different resource types, {len(diff.structural_differences)} structural differences"
        )
        return diff  # Can't compare different resource types
    
    # Compare IDs
    if resource1.id != resource2.id:
        diff.add_field_difference("id", resource1.id, resource2.id)
    
    # Get all fields from both resources
    fields1 = _get_all_fields(resource1)
    fields2 = _get_all_fields(resource2)
    
    # Find all unique field paths
    all_paths = set(fields1.keys()) | set(fields2.keys())
    
    # Compare each field
    for path in sorted(all_paths):
        value1 = fields1.get(path)
        value2 = fields2.get(path)
        
        # Normalize values for comparison
        norm_value1 = _normalize_value(value1)
        norm_value2 = _normalize_value(value2)
        
        if norm_value1 != norm_value2:
            diff.add_field_difference(path, value1, value2)
    
    end_time = datetime.now()
    completion_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    elapsed = (end_time - start_time).total_seconds()
    
    logger.info(
        f"Resource comparison completed at {completion_time} ({elapsed:.4f}s elapsed): "

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        f"Identical={diff.identical}, "
        f"{len(diff.structural_differences)} structural differences, "
        f"{len(diff.field_differences)} field differences"
    )
    
    return diff


def format_diff(diff: ResourceDiff, show_identical: bool = False) -> str:
    """
    Format ResourceDiff as human-readable text.
    
    Args:
        diff: ResourceDiff object
        show_identical: If True, show message even when resources are identical
        
    Returns:
        Formatted diff text
    """
    lines = []
    lines.append("FHIR Resource Comparison")
    lines.append("=" * 60)
    
    if diff.identical:
        lines.append("Resources are IDENTICAL")
        if not show_identical:
            return "\n".join(lines) + "\n"
    else:
        lines.append("Resources are DIFFERENT")
        lines.append("")
    
    # Structural differences
    if diff.structural_differences:
        lines.append("Structural Differences:")
        for diff_desc in diff.structural_differences:
            lines.append(f"  - {diff_desc}")
        lines.append("")
    
    # Field differences
    if diff.field_differences:
        lines.append("Field Differences:")
        for field_diff in diff.field_differences:
            lines.append(f"  {field_diff['path']}:")
            lines.append(f"    Resource 1: {_format_value(field_diff['resource1'])}")
            lines.append(f"    Resource 2: {_format_value(field_diff['resource2'])}")
        lines.append("")
    
    # Summary
    lines.append("Summary:")
    lines.append(f"  Structural differences: {len(diff.structural_differences)}")
    lines.append(f"  Field differences: {len(diff.field_differences)}")
    
    # Add timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"  Comparison timestamp: {current_time}")
    
    return "\n".join(lines) + "\n"


def _format_value(value: Any, max_length: int = 100) -> str:
    """
    Format a value for display.
    
    Args:
        value: Value to format
        max_length: Maximum length for string values
        
    Returns:
        Formatted string
    """
    if value is None:
        return "<missing>"
    
    if isinstance(value, str):
        if len(value) > max_length:
            return value[:max_length] + "..."
        return value
    
    if isinstance(value, (int, float, bool)):
        return str(value)
    
    if isinstance(value, list):
        if len(value) == 0:
            return "[]"
        return f"[{len(value)} items]"
    
    if hasattr(value, "__dict__"):
        return f"<{type(value).__name__}>"
    
    return str(value)

