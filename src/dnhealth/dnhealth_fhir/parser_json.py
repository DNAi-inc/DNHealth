# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR JSON parser (version-aware).

Parses FHIR JSON resources into Python dataclass models.
Supports both R4 and R5 versions with automatic version detection.
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
from dnhealth.dnhealth_fhir.version import (
    detect_version_from_json,
    detect_version_from_json_string,
    FHIRVersion,
    normalize_version,
)
from dnhealth.dnhealth_fhir.resource_registry import get_resource_class

# Resource type mapping (deprecated - use get_resource_class instead)
# Kept for backward compatibility with existing code
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
    # Tolerance: if array is provided for primitive field, extract first item
    # This handles edge cases where JSON has arrays but schema expects primitive
    # Common in R5 where some fields changed structure
    if isinstance(data, list):
        if len(data) == 0:
            return None
        elif len(data) == 1:
            # Single-item array - extract the item
            item = data[0]
            # If item is a dict with "value" field, extract the value
            if isinstance(item, dict) and "value" in item:
                return item["value"]
            # Otherwise return the item itself if it's a primitive
            if isinstance(item, (str, int, float, bool)):
                return item
            # If it's a dict without "value", this might be an error but be tolerant
            return item
        else:
            # Multi-item array - extract first item's value if it's a dict with "value"
            first_item = data[0]
            if isinstance(first_item, dict) and "value" in first_item:
                return first_item["value"]
            # Otherwise, this is an error but provide helpful message
            raise FHIRParseError(
                f"Invalid primitive value for {field_name}: expected primitive or single-item array, "
                f"got array with {len(data)} items. First item: {first_item}"
            )
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
        # Special handling for Reference when data is a string
        # FHIR allows Reference fields to be represented as just a string (the reference URL)
        if field_type.__name__ == "Reference" and isinstance(data, str):
            from dnhealth.dnhealth_fhir.types import Reference
            return Reference(reference=data)
        
        # Special handling for Reference when data is a list (should be List[Reference])
        if field_type.__name__ == "Reference" and isinstance(data, list):
            from dnhealth.dnhealth_fhir.types import Reference
            # Convert list of strings/dicts to list of References
            references = []
            for item in data:
                if isinstance(item, str):
                    references.append(Reference(reference=item))
                elif isinstance(item, dict):
                    references.append(_parse_dataclass(item, Reference, field_name, version=None))
                else:
                    references.append(item)
            # Return first item if single-item list, otherwise return list
            # Actually, if field_type is Reference (not List[Reference]), this is an error
            # But we'll be tolerant and return the first item
            if len(references) == 1:
                return references[0]
            raise FHIRParseError(f"Expected single Reference for {field_name}, got list with {len(references)} items")
        
        # Special handling for CodeableConcept when data is a list
        # This might indicate the field should be List[CodeableConcept] instead
        if field_type.__name__ == "CodeableConcept" and isinstance(data, list):
            from dnhealth.dnhealth_fhir.types import CodeableConcept
            # If it's a list, try to parse each item as CodeableConcept
            # But if field_type is CodeableConcept (not List[CodeableConcept]), this is an error
            # Be tolerant and return the first item if single-item list
            if len(data) == 1:
                return _parse_dataclass(data[0], CodeableConcept, field_name, version=None)
            raise FHIRParseError(f"Expected single CodeableConcept for {field_name}, got list with {len(data)} items")
        
        # Special handling for Attachment when data is a list (R5 allows arrays)
        # This is common in R5 where fields that were single values in R4 became arrays
        if field_type.__name__ == "Attachment" and isinstance(data, list):
            from dnhealth.dnhealth_fhir.types import Attachment
            # Be tolerant: if single-item list, return the first item
            # This handles R5 structure where sourceAttachment is an array
            if len(data) == 1:
                return _parse_dataclass(data[0], Attachment, field_name, version=None)
            raise FHIRParseError(f"Expected single Attachment for {field_name}, got list with {len(data)} items")
        
        # Special handling for Identifier when data is a list (R5 allows arrays)
        # This is common in R5 where fields that were single values in R4 became arrays
        if field_type.__name__ == "Identifier" and isinstance(data, list):
            from dnhealth.dnhealth_fhir.types import Identifier
            # Be tolerant: if single-item list, return the first item
            # This handles R5 structure where identifier can be an array
            if len(data) == 1:
                return _parse_dataclass(data[0], Identifier, field_name, version=None)
            raise FHIRParseError(f"Expected single Identifier for {field_name}, got list with {len(data)} items")
        
        # General tolerance: if a list is provided but a dict is expected,
        # try to extract the first item if it's a single-item list
        # This handles edge cases where JSON has arrays but the schema expects single objects
        # Common in R5 where some fields changed from single to array, or vice versa
        if isinstance(data, list):
            if len(data) == 1 and isinstance(data[0], dict):
                # Single-item list with dict - extract first item
                # This handles cases like DocumentReference.context, Organization.contact.name, etc.
                return _parse_dataclass(data[0], field_type, field_name, version=None)
            elif len(data) > 0:
                # Multi-item list - this is an error, but provide helpful message
                raise FHIRParseError(
                    f"Expected single {field_type.__name__} for {field_name}, got list with {len(data)} items. "
                    f"First item type: {type(data[0]).__name__}"
                )
            else:
                # Empty list - return None for optional fields
                return None
        
        # Note: version parameter not available in _parse_field, will use None
        # This is acceptable as version is mainly needed for resource class lookup
        return _parse_dataclass(data, field_type, field_name, version=None)

    # Handle primitive types
    return _parse_primitive_value(data, field_name)


def _parse_dataclass(data: Dict[str, Any], cls: Type, context: str = "", version: Optional[FHIRVersion] = None) -> Any:
    """
    Parse a dataclass from JSON data.

    Args:
        data: JSON dictionary
        cls: Dataclass type
        context: Context for error reporting
        version: Optional FHIR version for version-aware parsing

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
                                # Parse the contained resource using version-aware registry
                                # Use the same version as the parent resource
                                contained_cls = get_resource_class(contained_resource_type, version)
                                
                                # Fallback to legacy RESOURCE_TYPE_MAP
                                if contained_cls is None:
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
                                        from dnhealth.dnhealth_fhir.resources.codesystem import CodeSystem
                                        contained_cls = CodeSystem
                                    elif contained_resource_type == "ConceptMap":
                                        from dnhealth.dnhealth_fhir.resources.conceptmap import ConceptMap
                                        contained_cls = ConceptMap
                                    else:
                                        # Use generic FHIRResource if type not found
                                        contained_cls = FHIRResource
                                
                                try:
                                    contained_resource = _parse_dataclass(contained_data, contained_cls, f"contained.{contained_resource_type}", version=version)
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
    fhir_version: Optional[str] = None,
) -> T:
    """
    Parse FHIR JSON string into a resource object.
    
    Version-aware parser that supports both R4 and R5. Automatically detects
    version from resource data, or uses provided version parameter.

    Args:
        json_str: FHIR JSON string
        resource_type: Optional resource type (if None, inferred from resourceType field)
        cache: Optional ResourceCache instance (defaults to global cache if use_cache=True)
        use_cache: Whether to use caching (default: True)
        fhir_version: Optional FHIR version override ("4.0", "R4", "5.0", "R5", etc.)
                     If None, version is auto-detected from resource data

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

    # Detect or normalize version
    if fhir_version is not None:
        version = normalize_version(fhir_version)
    else:
        version = detect_version_from_json(data)
    
    # Determine resource type using version-aware registry
    if resource_type is None:
        resource_type_name = data.get("resourceType")
        if not resource_type_name:
            raise FHIRParseError("Missing resourceType field")
        
        # Use version-aware resource registry
        resource_type = get_resource_class(resource_type_name, version)
        
        # Fallback to legacy RESOURCE_TYPE_MAP for backward compatibility
        if resource_type is None:
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
    else:
        # If resource_type is provided, get resource_type_name from the resource type or data
        resource_type_name = data.get("resourceType") or getattr(resource_type, "__name__", "Unknown")

    # Parse resource
    resource = _parse_dataclass(data, resource_type, resource_type_name, version=version)

    # Cache the parsed resource if caching is enabled
    if use_cache and cache is not None:
        cache.put(json_str, resource)

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] FHIR JSON parsing completed successfully (version: {version.value})")
    logger.debug(f"[{current_time}] Current Time at End of Operations: {current_time}")

    return resource

