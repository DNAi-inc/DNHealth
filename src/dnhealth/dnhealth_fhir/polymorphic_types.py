# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 polymorphic choice type (value[x]) utilities.

Handles parsing, validation, and serialization of polymorphic choice types
where a field can be one of multiple types (e.g., valueQuantity, valueString, etc.).
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Type, get_type_hints
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def detect_value_x_fields(cls: Type) -> List[str]:
    """
    Detect all value[x] fields in a dataclass.
    
    Value[x] fields follow the pattern: value<Type> (e.g., valueQuantity, valueString).
    
    Args:
        cls: Dataclass type to inspect
        
    Returns:
        List of value[x] field names
    """
    if not hasattr(cls, "__dataclass_fields__"):
        return []
    
    value_fields = []
    for field_name in cls.__dataclass_fields__.keys():
        if field_name.startswith("value") and len(field_name) > 5:
            # Check if it's a value[x] field (value + capitalized type name)
            value_fields.append(field_name)
    
    return sorted(value_fields)


def get_value_x_value(instance: Any) -> Tuple[Optional[str], Optional[Any]]:
    """
    Get the set value[x] field and its value from an instance.
    
    Args:
        instance: Dataclass instance
        
    Returns:
        Tuple of (field_name, value) or (None, None) if no value[x] is set
    """
    value_fields = detect_value_x_fields(type(instance))
    
    for field_name in value_fields:
        value = getattr(instance, field_name, None)
        if value is not None:
            return field_name, value
    
    return None, None


def set_value_x_value(instance: Any, field_name: str, value: Any) -> None:
    """
    Set a value[x] field value, clearing all other value[x] fields.
    
    Args:
        instance: Dataclass instance
        field_name: Name of the value[x] field to set
        value: Value to set
    """
    value_fields = detect_value_x_fields(type(instance))
    
    # Clear all value[x] fields first
    for vf in value_fields:
        setattr(instance, vf, None)
    
    # Set the specified field
    if field_name in value_fields:
        setattr(instance, field_name, value)
    else:
        raise ValueError(f"Invalid value[x] field name: {field_name}")


def validate_value_x_fields(instance: Any) -> List[str]:
    """
    Validate that at most one value[x] field is set.
    
    Args:
        instance: Dataclass instance
        
    Returns:
        List of error messages (empty if valid)
    """
    start_time = datetime.now()
    errors = []
    value_fields = detect_value_x_fields(type(instance))
    
    set_fields = []
    for field_name in value_fields:
        value = getattr(instance, field_name, None)
        if value is not None:
            set_fields.append(field_name)
    
    if len(set_fields) > 1:
        errors.append(
            f"Multiple value[x] fields set: {', '.join(set_fields)}. "
            f"Only one value[x] field should be set."
        )
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Value[x] fields validation completed in {elapsed:.3f} seconds ({len(errors)} errors)")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def parse_value_x_from_json(
    data: Dict[str, Any],
    cls: Type,
    base_field_name: str = "value"
) -> Tuple[Optional[str], Optional[Any]]:
    """
    Parse a value[x] field from JSON data.
    
    Looks for fields matching the pattern value<Type> in the JSON data
    and returns the first one found along with its value.
    
    Args:
        data: JSON dictionary
        cls: Dataclass type
        base_field_name: Base name for value[x] fields (default: "value")
        
    Returns:
        Tuple of (field_name, value) or (None, None) if no value[x] found
    """
    value_fields = detect_value_x_fields(cls)
    
    # Check JSON data for any value[x] fields
    for field_name in value_fields:
        json_field_name = field_name
        # Handle Python keywords
        if field_name == "class_":
            json_field_name = "class"
        
        if json_field_name in data:
            return field_name, data[json_field_name]
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return None, None


def serialize_value_x_to_json(
    instance: Any,
    result: Dict[str, Any],
    base_field_name: str = "value"
) -> None:
    """
    Serialize value[x] fields to JSON, including only the set field.
    
    Args:
        instance: Dataclass instance
        result: Dictionary to add serialized value[x] to
        base_field_name: Base name for value[x] fields (default: "value")
    """
    field_name, value = get_value_x_value(instance)
    
    if field_name and value is not None:
        json_field_name = field_name
        # Handle Python keywords
        if field_name == "class_":
            json_field_name = "class"
        
        # Serialize the value
        if hasattr(value, "__dataclass_fields__"):
            # Complex type - serialize as dict
            from dnhealth.dnhealth_fhir.serializer_json import _serialize_dataclass
            result[json_field_name] = _serialize_dataclass(value)
        else:
            # Primitive type
            result[json_field_name] = value


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def parse_value_x_from_xml(
    element,
    cls: Type,
    base_field_name: str = "value"
) -> Tuple[Optional[str], Optional[Any]]:
    """
    Parse a value[x] field from XML element.
    
    Looks for child elements matching the pattern value<Type> in the XML
    and returns the first one found along with its value.
    
    Args:
        element: XML element
        cls: Dataclass type
        base_field_name: Base name for value[x] fields (default: "value")
        
    Returns:
        Tuple of (field_name, value) or (None, None) if no value[x] found
    """
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        return None, None
    
    if not isinstance(element, ET.Element):
        return None, None
    
    value_fields = detect_value_x_fields(cls)
    
    # Check XML element for any value[x] child elements
    for field_name in value_fields:
        xml_field_name = field_name
        # Handle Python keywords
        if field_name == "class_":
            xml_field_name = "class"
        
        child = element.find(xml_field_name)
        if child is not None:
            # Parse the value based on type
            # For complex types, we'll need to parse the element
            # For primitive types, get text content
            if child.text:
                return field_name, child.text
            elif len(child) > 0:
                # Complex type - return element for further parsing
                return field_name, child
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return None, None


def serialize_value_x_to_xml(
    instance: Any,
    parent_element,
    base_field_name: str = "value"
) -> None:
    """
    Serialize value[x] fields to XML, including only the set field.
    
    Args:
        instance: Dataclass instance
        parent_element: XML element to add serialized value[x] to
        base_field_name: Base name for value[x] fields (default: "value")
    """
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        return
    
    field_name, value = get_value_x_value(instance)
    
    if field_name and value is not None:
        xml_field_name = field_name
        # Handle Python keywords
        if field_name == "class_":
            xml_field_name = "class"
        
        # Create child element
        child = ET.SubElement(parent_element, xml_field_name)
        
        # Serialize the value
        if hasattr(value, "__dataclass_fields__"):
            # Complex type - serialize as XML element
            from dnhealth.dnhealth_fhir.serializer_xml import _serialize_dataclass_xml
            _serialize_dataclass_xml(value, child)
        else:
            # Primitive type - set text content
            child.text = str(value) if value is not None else None


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def validate_nested_value_x_fields(instance: Any, path: str = "") -> List[str]:
    """
    Validate value[x] fields recursively in nested structures.
    
    Traverses the instance and validates all value[x] fields found,
    including those in nested components, items, etc.
    
    Args:
        instance: Dataclass instance to validate
        path: Current path for error messages
        
    Returns:
        List of error messages (empty if valid)
    """
    start_time = datetime.now()
    errors = []
    
    # Validate this instance's value[x] fields
    instance_errors = validate_value_x_fields(instance)
    for error in instance_errors:
        errors.append(f"{path}: {error}" if path else error)
    
    # Check for nested structures that might have value[x] fields
    if hasattr(instance, "__dataclass_fields__"):
        for field_name, field_value in instance.__dict__.items():
            if field_name.startswith("_"):
                continue
            
            field_path = f"{path}.{field_name}" if path else field_name
            
            # Check if field is a list
            if isinstance(field_value, list):
                for idx, item in enumerate(field_value):
                    item_path = f"{field_path}[{idx}]"
                    if hasattr(item, "__dataclass_fields__"):
                        # Recursively validate nested items
                        nested_errors = validate_nested_value_x_fields(item, item_path)
                        errors.extend(nested_errors)
            # Check if field is a dataclass
            elif hasattr(field_value, "__dataclass_fields__"):
                # Recursively validate nested structures
                nested_errors = validate_nested_value_x_fields(field_value, field_path)
                errors.extend(nested_errors)
    
    # Log completion timestamp at end of operation (only at top level)
    if not path:
        completion_time = datetime.now()
        elapsed = (completion_time - start_time).total_seconds()
        current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Nested value[x] fields validation completed in {elapsed:.3f} seconds ({len(errors)} errors)")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors
