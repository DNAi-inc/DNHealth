# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 JSON parser.

Parses FHIR JSON resources into Python dataclass models.
Supports optional caching for improved performance.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar, List, get_type_hints, get_origin, get_args

from dnhealth.errors import FHIRParseError
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.resources.condition import Condition
from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome
from dnhealth.dnhealth_fhir.cache import ResourceCache, get_default_cache
from dnhealth.dnhealth_fhir.types import Extension

# Resource type mapping
RESOURCE_TYPE_MAP = {
    "Patient": Patient,
    "Observation": Observation,
    "Encounter": Encounter,
    "Bundle": Bundle,
    "Condition": Condition,
    "OperationOutcome": OperationOutcome,
    "StructureDefinition": None,  # Lazy loaded
    "ValueSet": None,  # Lazy loaded
    "CodeSystem": None,  # Lazy loaded
    "ConceptMap": None,  # Lazy loaded
}

# Lazy import for StructureDefinition to avoid circular imports
def _get_structure_definition_class():
    """Get StructureDefinition class lazily."""
    from dnhealth.dnhealth_fhir.structuredefinition import StructureDefinition

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return StructureDefinition

T = TypeVar("T", bound=FHIRResource)

logger = logging.getLogger(__name__)


def _parse_primitive_value(data: Any, field_name: str) -> Any:
    """
    Parse a primitive FHIR value, handling _element extensions.

    Args:
        data: JSON data (can be primitive or dict with value)
        field_name: Field name for error reporting

    Returns:
        Parsed primitive value
    """
    if isinstance(data, (str, int, float, bool)) or data is None:
        return data
    if isinstance(data, dict):
        # Check for value field (primitive extension)
        if "value" in data:
            return data["value"]
        # Otherwise return as-is (complex type)
        return data
    raise FHIRParseError(f"Invalid primitive value for {field_name}: {data}")


def _parse_list_field(data: Any, item_type: Type, field_name: str) -> list:
    """
    Parse a list field.

    Args:
        data: JSON data
        item_type: Type of list items
        field_name: Field name for error reporting

    Returns:
        List of parsed items
    """
    if data is None:
        return []
    if not isinstance(data, list):
        return [_parse_field(data, item_type, field_name)]
    return [_parse_field(item, item_type, field_name) for item in data]


def _parse_field(data: Any, field_type: Type, field_name: str) -> Any:
    """
    Parse a field based on its type.

    Args:
        data: JSON data
        field_type: Expected Python type
        field_name: Field name for error reporting

    Returns:
        Parsed value
    """
    if data is None:
        return None

    # Handle Optional types
    origin = get_origin(field_type)
    if origin is not None:
        # Check if it's Optional
        args = get_args(field_type)
        if len(args) == 2 and type(None) in args:
            # Optional type - get the actual type
            field_type = args[0] if args[0] is not type(None) else args[1]
            origin = get_origin(field_type)

    # Handle List types
    if origin is list:
        args = get_args(field_type)
        item_type = args[0] if args else Any
        return _parse_list_field(data, item_type, field_name)

    # Handle dataclass types (complex types)
    if hasattr(field_type, "__dataclass_fields__"):
        return _parse_dataclass(data, field_type, field_name)

    # Handle primitive types
    return _parse_primitive_value(data, field_name)


def _parse_dataclass(data: Dict[str, Any], cls: Type, context: str = "") -> Any:
    """
    Parse a dataclass from JSON data.

    Args:
        data: JSON dictionary
        cls: Dataclass type
        context: Context for error reporting

    Returns:
        Parsed dataclass instance
    """
    if not isinstance(data, dict):
        raise FHIRParseError(f"Expected dict for {cls.__name__}, got {type(data).__name__}")

    # Get field types
    hints = get_type_hints(cls)
    fields = {}
    primitive_extensions = {}

    # First pass: handle _element fields (primitive extensions)
    # These are fields like _id, _status that contain both value and extensions
    for json_field_name in list(data.keys()):
        if json_field_name.startswith("_") and len(json_field_name) > 1:
            # This is a primitive extension field (e.g., _id, _status)
            base_field_name = json_field_name[1:]  # Remove leading underscore
            
            # Check if base field exists in the dataclass
            # Handle Python keywords
            actual_field_name = base_field_name
            if base_field_name == "class":
                actual_field_name = "class_"
            
            if actual_field_name in hints:
                elem_data = data[json_field_name]
                if isinstance(elem_data, dict):
                    # Extract the primitive value (field name matches base field name)
                    if base_field_name in elem_data:
                        # Set the actual field value
                        field_type = hints[actual_field_name]
                        try:
                            fields[actual_field_name] = _parse_field(
                                elem_data[base_field_name], field_type, base_field_name
                            )
                        except Exception as e:
                            raise FHIRParseError(
                                f"Error parsing {json_field_name} in {context or cls.__name__}: {e}"
                            ) from e
                    
                    # Extract extensions if present
                    if "extension" in elem_data:
                        extensions = _parse_field(elem_data["extension"], List[Extension], "extension")
                        if extensions:
                            primitive_extensions[base_field_name] = extensions
                    
                    # Remove from data so we don't process it again
                    del data[json_field_name]

    # Second pass: handle regular fields
    for field_name, field_type in hints.items():
        # Skip private fields
        if field_name.startswith("_"):
            continue

        # Handle Python keywords (e.g., class -> class_)
        json_field_name = field_name
        if field_name == "class_":
            json_field_name = "class"

        if json_field_name in data:
            try:
                # Check for array extensions (extensions on list fields)
                # Array extensions use format "_fieldName" and contain extension array
                array_ext_field_name = f"_{json_field_name}"
                if array_ext_field_name in data:
                    from dnhealth.dnhealth_fhir.array_extensions import parse_array_extensions
                    array_extensions = parse_array_extensions(data, json_field_name)
                    if array_extensions:
                        # Store array extensions for later attachment to the instance
                        if not hasattr(cls, "_array_extensions"):
                            cls._array_extensions = {}
                        cls._array_extensions[field_name] = array_extensions
                
                # Special handling for contained resources
                if json_field_name == "contained" and isinstance(data[json_field_name], list):
                    # Parse each contained resource
                    contained_resources = []
                    for contained_data in data[json_field_name]:
                        if isinstance(contained_data, dict):
                            # Each contained resource must have resourceType
                            contained_resource_type = contained_data.get("resourceType")
                            if contained_resource_type:
                                # Parse the contained resource
                                contained_cls = RESOURCE_TYPE_MAP.get(contained_resource_type)
                                if contained_cls is None:
                                    # Try lazy loading
                                    if contained_resource_type == "StructureDefinition":
                                        from dnhealth.dnhealth_fhir.structuredefinition import StructureDefinition
                                        contained_cls = StructureDefinition
                                    elif contained_resource_type == "ValueSet":
                                        from dnhealth.dnhealth_fhir.resources.valueset import ValueSet
                                        contained_cls = ValueSet
                                    elif contained_resource_type == "CodeSystem":
                                        from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystem
                                        contained_cls = CodeSystem
                                    elif contained_resource_type == "ConceptMap":
                                        from dnhealth.dnhealth_fhir.conceptmap_resource import ConceptMap
                                        contained_cls = ConceptMap
                                    else:
                                        # Use generic FHIRResource if type not found
                                        contained_cls = FHIRResource
                                
                                try:
                                    contained_resource = _parse_dataclass(contained_data, contained_cls, f"contained.{contained_resource_type}")
                                    contained_resources.append(contained_resource)
                                except Exception as e:
                                    raise FHIRParseError(f"Error parsing contained resource {contained_resource_type}: {e}") from e
                            else:
                                raise FHIRParseError("Contained resource missing resourceType")
                        else:
                            raise FHIRParseError(f"Invalid contained resource format: expected dict, got {type(contained_data).__name__}")
                    fields[field_name] = contained_resources
                else:
                    fields[field_name] = _parse_field(data[json_field_name], field_type, json_field_name)
            except Exception as e:
                raise FHIRParseError(f"Error parsing {json_field_name} in {context or cls.__name__}: {e}") from e

    # Create instance
    try:
        instance = cls(**fields)
        # Set primitive extensions if any were found
        if primitive_extensions:
            instance._primitive_extensions = primitive_extensions

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
        return instance
    except Exception as e:
        raise FHIRParseError(f"Error creating {cls.__name__}: {e}") from e


def parse_fhir_json(
    json_str: str,
    resource_type: Type[T] = None,
    cache: Optional[ResourceCache] = None,
    use_cache: bool = True,
) -> T:
    """
    Parse FHIR JSON string into a resource object.

    Args:
        json_str: FHIR JSON string
        resource_type: Optional resource type (if None, inferred from resourceType field)
        cache: Optional ResourceCache instance (defaults to global cache if use_cache=True)
        use_cache: Whether to use caching (default: True)

    Returns:
        Parsed FHIR resource object

    Raises:
        FHIRParseError: If parsing fails
    """
    # Try cache first if enabled
    if use_cache:
        if cache is None:
            cache = get_default_cache()
        cached_resource = cache.get(json_str, resource_type)
        if cached_resource is not None:
            return cached_resource

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise FHIRParseError(f"Invalid JSON: {e}") from e

    if not isinstance(data, dict):
        raise FHIRParseError("FHIR resource must be a JSON object")

    # Determine resource type
    if resource_type is None:
        resource_type_name = data.get("resourceType")
        if not resource_type_name:
            raise FHIRParseError("Missing resourceType field")
        resource_type = RESOURCE_TYPE_MAP.get(resource_type_name)
        if resource_type is None:
            # Try StructureDefinition as fallback
            if resource_type_name == "StructureDefinition":
                from dnhealth.dnhealth_fhir.structuredefinition import StructureDefinition
                resource_type = StructureDefinition
            elif resource_type_name == "ValueSet":
                from dnhealth.dnhealth_fhir.resources.valueset import ValueSet
                resource_type = ValueSet
            elif resource_type_name == "CodeSystem":
                from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystem
                resource_type = CodeSystem
            elif resource_type_name == "ConceptMap":
                from dnhealth.dnhealth_fhir.conceptmap_resource import ConceptMap
                resource_type = ConceptMap
            else:
                raise FHIRParseError(f"Unknown resource type: {resource_type_name}")

    # Parse resource
    resource = _parse_dataclass(data, resource_type, resource_type_name)

    # Cache the parsed resource if caching is enabled
    if use_cache and cache is not None:
        cache.put(json_str, resource)

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] FHIR JSON parsing completed successfully")
    logger.debug(f"[{current_time}] Current Time at End of Operations: {current_time}")

    return resource

