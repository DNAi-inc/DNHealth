# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR XML parser (version-aware).

Parses FHIR XML resources into Python dataclass models.
Supports both R4 and R5 versions with automatic version detection.
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, Type, TypeVar, Optional, get_type_hints, get_origin, get_args
from datetime import datetime
import time
import logging

from dnhealth.errors import FHIRParseError
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.resources.condition import Condition
from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome
from dnhealth.dnhealth_fhir.version import (
    detect_version_from_xml,
    FHIRVersion,
    normalize_version,
)
from dnhealth.dnhealth_fhir.resource_registry import get_resource_class

logger = logging.getLogger(__name__)

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

T = TypeVar("T", bound=FHIRResource)


def _parse_xml_element(element: ET.Element, field_type: Type, field_name: str) -> Any:
    """
    Parse an XML element based on field type.

    Args:
        element: XML element
        field_type: Expected Python type
        field_name: Field name for error reporting

    Returns:
        Parsed value
    """
    if element is None:
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
        args = get_args(field_type)
        item_type = args[0] if args else Any
        # Find all child elements with this name
        children = list(element.findall(field_name))
        return [_parse_xml_element(child, item_type, field_name) for child in children]

    # Handle dataclass types
    if hasattr(field_type, "__dataclass_fields__"):
        return _parse_xml_dataclass(element, field_type)

    # Handle primitive types - check for value attribute first, then text content
    # FHIR XML can use either <field value="value"/> or <field>value</field>
    value = None
    if "value" in element.attrib:
        value = element.attrib["value"]
    elif element.text:
        value = element.text.strip()
    
    # Convert boolean strings to boolean values
    if value is not None and field_type is bool:
        if value.lower() in ("true", "1", "yes"):
            return True
        elif value.lower() in ("false", "0", "no"):
            return False
    
    return value


def _parse_xml_dataclass(element: ET.Element, cls: Type) -> Any:
    """
    Parse a dataclass from XML element.

    Args:
        element: XML element
        cls: Dataclass type

    Returns:
        Parsed dataclass instance
    """
    hints = get_type_hints(cls)
    fields = {}

    for field_name, field_type in hints.items():
        if field_name.startswith("_"):
            continue

        # Handle Python keywords
        xml_field_name = field_name
        if field_name == "class_":
            xml_field_name = "class"

        # Special handling for contained resources
        if field_name == "contained":
            contained_elements = element.findall("contained")
            if contained_elements:
                contained_resources = []
                for contained_elem in contained_elements:
                    # Each contained resource should have a resourceType attribute or child element
                    contained_resource_type = contained_elem.get("resourceType")
                    if not contained_resource_type:
                        # Try finding resourceType as a child element
                        resource_type_elem = contained_elem.find("resourceType")
                        if resource_type_elem is not None and resource_type_elem.text:
                            contained_resource_type = resource_type_elem.text
                    
                    if contained_resource_type:
                        # Get the resource class
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
                            contained_resource = _parse_xml_dataclass(contained_elem, contained_cls)
                            contained_resources.append(contained_resource)
                        except Exception as e:
                            raise FHIRParseError(f"Error parsing contained resource {contained_resource_type}: {e}") from e
                    else:
                        raise FHIRParseError("Contained resource missing resourceType")
                fields[field_name] = contained_resources
            continue

        # Check if this is a list type (handle Optional[List[...]] first)
        origin = get_origin(field_type)
        actual_field_type = field_type
        
        # Unwrap Optional if present
        if origin is not None:
            args = get_args(field_type)
            if len(args) == 2 and type(None) in args:
                # It's Optional[Something], get the actual type
                actual_field_type = args[0] if args[0] is not type(None) else args[1]
                origin = get_origin(actual_field_type)
        
        # Handle namespaces - check if element has a namespace
        # ElementTree stores namespaced tags as "{namespace}localname"
        # We need to search for elements with or without namespace
        def find_with_namespace(parent, local_name):
            """Find elements with or without namespace."""
            # Try without namespace first (for elements without xmlns)
            children = list(parent.findall(local_name))
            if children:
                return children
            
            # Try with namespace (for elements with default namespace)
            # Check if parent has a namespace
            if parent.tag.startswith("{"):
                # Extract namespace from parent
                ns_end = parent.tag.find("}")
                if ns_end != -1:
                    namespace = parent.tag[1:ns_end]
                    # Search with namespace
                    ns_tag = f"{{{namespace}}}{local_name}"
                    children = list(parent.findall(ns_tag))
                    if children:
                        return children
            
            # Also try searching all children and matching by local name
            # This handles cases where namespace might differ
            matching = []
            for child in parent:
                child_local = child.tag
                if child_local.startswith("{"):
                    child_local = child_local.split("}")[-1]
                if child_local == local_name:
                    matching.append(child)
            return matching
        
        if origin is list:
            # For list types, find all children with this name
            children = find_with_namespace(element, xml_field_name)
            if children:
                args = get_args(actual_field_type)
                item_type = args[0] if args else Any
                fields[field_name] = [_parse_xml_element(child, item_type, xml_field_name) for child in children]
        else:
            # For non-list types, find single child element
            children = find_with_namespace(element, xml_field_name)
            if children:
                child = children[0]  # Take first match
                try:
                    fields[field_name] = _parse_xml_element(child, actual_field_type, xml_field_name)
                except Exception as e:
                    raise FHIRParseError(f"Error parsing {xml_field_name}: {e}") from e

    # Also check attributes for resourceType, id, etc.
    if "resourceType" in element.attrib:
        fields["resourceType"] = element.attrib["resourceType"]
    if "id" in element.attrib:
        fields["id"] = element.attrib["id"]

    try:
        return cls(**fields)
    except Exception as e:
        raise FHIRParseError(f"Error creating {cls.__name__}: {e}") from e


def parse_fhir_xml(
    xml_str: str,
    resource_type: Type[T] = None,
    fhir_version: Optional[str] = None,
) -> T:
    """
    Parse FHIR XML string into a resource object.
    
    Version-aware parser that supports both R4 and R5. Automatically detects
    version from XML data, or uses provided version parameter.

    Args:
        xml_str: FHIR XML string
        resource_type: Optional resource type (if None, inferred from root element)
        fhir_version: Optional FHIR version override ("4.0", "R4", "5.0", "R5", etc.)
                     If None, version is auto-detected from XML data

    Returns:
        Parsed FHIR resource object

    Raises:
        FHIRParseError: If parsing fails
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting FHIR XML parsing")
    
    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] FHIR XML parsing failed: Invalid XML (elapsed: {elapsed:.2f}s)")
        raise FHIRParseError(f"Invalid XML: {e}") from e

    # Detect or normalize version
    if fhir_version is not None:
        version = normalize_version(fhir_version)
    else:
        version = detect_version_from_xml(xml_str)
    
    # Determine resource type using version-aware registry
    if resource_type is None:
        resource_type_name = root.tag
        # Remove namespace prefix if present
        if "}" in resource_type_name:
            resource_type_name = resource_type_name.split("}")[1]
        
        # Use version-aware resource registry
        resource_type = get_resource_class(resource_type_name, version)
        
        # Fallback to legacy RESOURCE_TYPE_MAP for backward compatibility
        if resource_type is None:
            resource_type = RESOURCE_TYPE_MAP.get(resource_type_name)
            if resource_type is None:
                # Try lazy loading for StructureDefinition, ValueSet, CodeSystem, ConceptMap
                if resource_type_name == "StructureDefinition":
                    from dnhealth.dnhealth_fhir.structuredefinition import StructureDefinition
                    resource_type = StructureDefinition
                elif resource_type_name == "ValueSet":
                    from dnhealth.dnhealth_fhir.resources.valueset import ValueSet
                    resource_type = ValueSet
                elif resource_type_name == "CodeSystem":
                    from dnhealth.dnhealth_fhir.resources.codesystem import CodeSystem
                    resource_type = CodeSystem
                elif resource_type_name == "ConceptMap":
                    from dnhealth.dnhealth_fhir.resources.conceptmap import ConceptMap
                    resource_type = ConceptMap
            else:
                elapsed = time.time() - start_time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(f"[{current_time}] FHIR XML parsing failed: Unknown resource type '{resource_type_name}' (elapsed: {elapsed:.2f}s)")
                raise FHIRParseError(f"Unknown resource type: {resource_type_name}")

    # Parse resource
    try:
        result = _parse_xml_dataclass(root, resource_type)
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] FHIR XML parsing completed successfully in {elapsed:.2f}s (version: {version.value})")
        logger.debug(f"[{current_time}] Current Time at End of Operations: {current_time}")
        return result
    except Exception as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] FHIR XML parsing failed: {e} (elapsed: {elapsed:.2f}s)")
        raise

