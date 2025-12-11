# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 JSON serializer.

Serializes FHIR resource objects to JSON format.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, get_type_hints, get_origin, get_args

from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def _serialize_field(value: Any, field_type: Any) -> Any:
    """
    Serialize a field value to JSON-serializable format.

    Args:
        value: Field value
        field_type: Field type

    Returns:
        JSON-serializable value
    """
    if value is None:
        return None

    # Handle Optional types
    origin = get_origin(field_type)
    if origin is not None:
        args = get_args(field_type)
        if len(args) == 2 and type(None) in args:
            field_type = args[0] if args[0] is not type(None) else args[1]
            origin = get_origin(field_type)

    # Handle List types
    if origin is list:
        if isinstance(value, list):
            args = get_args(field_type)
            item_type = args[0] if args else Any
            return [_serialize_field(item, item_type) for item in value]
        return []

    # Handle dataclass types
    if hasattr(field_type, "__dataclass_fields__"):
        return _serialize_dataclass(value)


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    # Handle primitive types
    return value


def _serialize_extension(ext: Any) -> Dict[str, Any]:
    """
    Serialize an Extension, including nested extensions.
    
    Args:
        ext: Extension object
        
    Returns:
        Dictionary representation of extension with nested extensions
    """
    if not hasattr(ext, "__dataclass_fields__"):
        return ext
    
    result = _serialize_dataclass(ext)
    
    # Ensure nested extensions are properly serialized
    if "extension" in result and isinstance(result["extension"], list):

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        result["extension"] = [
            _serialize_extension(nested_ext) if hasattr(nested_ext, "__dataclass_fields__") else nested_ext
            for nested_ext in result["extension"]
        ]
    
    return result


def _serialize_dataclass(obj: Any) -> Dict[str, Any]:
    """
    Serialize a dataclass to dictionary.

    Args:
        obj: Dataclass instance

    Returns:
        Dictionary representation
    """
    if not hasattr(obj, "__dataclass_fields__"):
        return obj

    result = {}
    hints = get_type_hints(type(obj))
    
    # Get primitive extensions if they exist
    primitive_extensions = getattr(obj, "_primitive_extensions", {})

    for field_name, field_value in obj.__dict__.items():
        if field_name.startswith("_"):
            continue

        # Handle Python keywords
        json_field_name = field_name
        if field_name == "class_":
            json_field_name = "class"

        if field_value is not None:
            field_type = hints.get(field_name, Any)
            serialized_value = _serialize_field(field_value, field_type)
            
            # Check if this field has primitive extensions
            if json_field_name in primitive_extensions:
                # Serialize as _element field with value and extensions
                extensions = primitive_extensions[json_field_name]
                if extensions:
                    elem_obj = {json_field_name: serialized_value}
                    # Serialize extensions (including nested extensions)
                    from dnhealth.dnhealth_fhir.types import Extension
                    if isinstance(extensions, list):
                        elem_obj["extension"] = [
                            _serialize_extension(ext) for ext in extensions
                        ]
                    result[f"_{json_field_name}"] = elem_obj
                else:
                    # No extensions, serialize normally
                    result[json_field_name] = serialized_value
            else:

                    # Log completion timestamp at end of operation
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Current Time at End of Operations: {current_time}")
                # No primitive extensions, serialize normally
                result[json_field_name] = serialized_value
        else:
            # Field is None - check if it's an extension field that might have nested extensions
            # This shouldn't happen normally, but handle it for completeness
            if field_name == "extension" or field_name == "modifierExtension":
                # Extensions should be lists, not None
                pass

    return result


def serialize_fhir_json(resource: FHIRResource, indent: int = 2) -> str:
    """
    Serialize FHIR resource to JSON string.

    Args:
        resource: FHIR resource object
        indent: JSON indentation level

    Returns:
        JSON string
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting FHIR JSON serialization for resource type: {getattr(resource, 'resourceType', 'Unknown')}")
    
    data = _serialize_dataclass(resource)
    
    # Handle contained resources - serialize them before the main resource
    # Contained resources should appear as a "contained" array in the JSON
    if hasattr(resource, "contained") and resource.contained:
        contained_data = []
        for contained_resource in resource.contained:
            if isinstance(contained_resource, FHIRResource):
                # Serialize each contained resource
                contained_dict = _serialize_dataclass(contained_resource)
                # Ensure resourceType is first in contained resource
                if "resourceType" in contained_dict:
                    resource_type = contained_dict.pop("resourceType")
                    contained_result = {"resourceType": resource_type}
                    contained_result.update(contained_dict)
                    contained_data.append(contained_result)
                else:
                    contained_data.append(contained_dict)
            else:
                # If it's already a dict, use it directly
                contained_data.append(contained_resource)
        
        # Add contained array to the data
        data["contained"] = contained_data
    
    # Ensure resourceType is first
    if "resourceType" in data:
        resource_type = data.pop("resourceType")
        result = {"resourceType": resource_type}
        result.update(data)
        data = result
    
    json_result = json.dumps(data, indent=indent, ensure_ascii=False)
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] FHIR JSON serialization completed in {elapsed:.3f} seconds")
    logger.info(f"[{current_time}] Current Time at End of Operations: {current_time}")
    
    return json_result

