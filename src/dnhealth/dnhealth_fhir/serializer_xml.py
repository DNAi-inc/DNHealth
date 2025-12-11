# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 XML serializer.

Serializes FHIR resource objects to XML format.
"""

import xml.etree.ElementTree as ET
from typing import Any, get_type_hints, get_origin, get_args
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def _serialize_field_xml(value: Any, field_type: Any, field_name: str, parent: ET.Element) -> None:
    """
    Serialize a field value to XML element.

    Args:
        value: Field value
        field_type: Field type
        field_name: Field name
        parent: Parent XML element
    """
    if value is None:
        return

    # Handle Python keywords
    xml_field_name = field_name
    if field_name == "class_":
        xml_field_name = "class"

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
            for item in value:
                _serialize_field_xml(item, field_type, xml_field_name, parent)
        return

    # Handle dataclass types
    if hasattr(field_type, "__dataclass_fields__"):
        element = ET.SubElement(parent, xml_field_name)
        _serialize_dataclass_xml(value, element)
        return

    # Handle primitive types

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    element = ET.SubElement(parent, xml_field_name)
    element.text = str(value)


def _serialize_dataclass_xml(obj: Any, element: ET.Element, skip_contained: bool = False) -> None:
    """
    Serialize a dataclass to XML element.

    Args:
        obj: Dataclass instance
        element: XML element
        skip_contained: If True, skip serializing contained resources (handled separately)
    """
    if not hasattr(obj, "__dataclass_fields__"):
        element.text = str(obj)
        return

    hints = get_type_hints(type(obj))

    # Handle resourceType and id as attributes for root element
    if hasattr(obj, "resourceType") and element.tag == obj.resourceType:
        if hasattr(obj, "id") and obj.id:
            element.set("id", obj.id)

    for field_name, field_value in obj.__dict__.items():
        if field_name.startswith("_"):
            continue
        if field_name in ("resourceType", "id") and element.tag == obj.resourceType:
            continue  # Already handled as attributes

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        # Skip contained field if it's being handled separately
        if skip_contained and field_name == "contained":
            continue
        if field_value is not None:
            field_type = hints.get(field_name, Any)
            _serialize_field_xml(field_value, field_type, field_name, element)


def serialize_fhir_xml(resource: FHIRResource, encoding: str = "UTF-8") -> str:
    """
    Serialize FHIR resource to XML string.

    Args:
        resource: FHIR resource object
        encoding: XML encoding

    Returns:
        XML string
    """
    # Create root element
    root = ET.Element(resource.resourceType)
    if resource.id:
        root.set("id", resource.id)

    # Handle contained resources - serialize them before other content
    # Contained resources should appear as a "contained" element with child resource elements
    if hasattr(resource, "contained") and resource.contained:
        contained_elem = ET.SubElement(root, "contained")
        for contained_resource in resource.contained:
            if isinstance(contained_resource, FHIRResource):
                # Create element for contained resource
                contained_root = ET.SubElement(contained_elem, contained_resource.resourceType)
                if contained_resource.id:
                    contained_root.set("id", contained_resource.id)
                # Serialize the contained resource
                _serialize_dataclass_xml(contained_resource, contained_root)
            else:
                # If it's already an XML element or dict, handle appropriately
                # For now, skip non-FHIRResource contained items
                pass

    # Serialize content (skip contained as it's already handled above)
    _serialize_dataclass_xml(resource, root, skip_contained=True)

    # Create tree and serialize
    tree = ET.ElementTree(root)
    xml_bytes = ET.tostring(root, encoding=encoding, xml_declaration=True)
    result = xml_bytes.decode(encoding)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] FHIR XML serialization completed successfully")
    logger.debug(f"[{current_time}] Current Time at End of Operations: {current_time}")
    
    return result

