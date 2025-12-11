# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 XML parser.

Parses FHIR XML resources into Python dataclass models.
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, Type, TypeVar, get_type_hints, get_origin, get_args
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

logger = logging.getLogger(__name__)

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

T = TypeVar("T", bound=FHIRResource)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
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

    # Handle primitive types - get text content

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    text = element.text.strip() if element.text else None
    return text


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

        # Find child element
        child = element.find(xml_field_name)
        if child is not None:
            try:
                fields[field_name] = _parse_xml_element(child, field_type, xml_field_name)
            except Exception as e:
                raise FHIRParseError(f"Error parsing {xml_field_name}: {e}") from e

    # Also check attributes for resourceType, id, etc.
    if "resourceType" in element.attrib:
        fields["resourceType"] = element.attrib["resourceType"]
    if "id" in element.attrib:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        fields["id"] = element.attrib["id"]

    try:
        return cls(**fields)
    except Exception as e:
        raise FHIRParseError(f"Error creating {cls.__name__}: {e}") from e


def parse_fhir_xml(xml_str: str, resource_type: Type[T] = None) -> T:
    """
    Parse FHIR XML string into a resource object.

    Args:
        xml_str: FHIR XML string
        resource_type: Optional resource type (if None, inferred from root element)

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

    # Determine resource type
    if resource_type is None:
        resource_type_name = root.tag
        # Remove namespace prefix if present
        if "}" in resource_type_name:
            resource_type_name = resource_type_name.split("}")[1]
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
                from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystem
                resource_type = CodeSystem
            elif resource_type_name == "ConceptMap":
                from dnhealth.dnhealth_fhir.conceptmap_resource import ConceptMap
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
        logger.debug(f"[{current_time}] FHIR XML parsing completed successfully in {elapsed:.2f}s")
        logger.debug(f"[{current_time}] Current Time at End of Operations: {current_time}")
        return result
    except Exception as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] FHIR XML parsing failed: {e} (elapsed: {elapsed:.2f}s)")
        raise

