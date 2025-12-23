# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR XML serializer (version-aware).

Serializes FHIR resource objects to XML format.
Supports both R4 and R5 versions.
"""

import xml.etree.ElementTree as ET
from typing import Any, Optional, get_type_hints, get_origin, get_args
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.version import FHIRVersion, get_version_string, normalize_version

logger = logging.getLogger(__name__)


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
            args = get_args(field_type)
            item_type = args[0] if args else Any
            for item in value:
                _serialize_field_xml(item, item_type, xml_field_name, parent)
        return

    # Handle dataclass types
    if hasattr(field_type, "__dataclass_fields__"):
        element = ET.SubElement(parent, xml_field_name)
        # If value is a dict, try to convert it to dataclass instance
        if isinstance(value, dict):
            try:
                # Create instance from dict
                value = field_type(**value)
            except Exception:
                # If conversion fails, serialize dict directly
                pass
        _serialize_dataclass_xml(value, element)
        return
    
    # Handle dict types (for cases where dict is passed directly)
    if isinstance(value, dict):
        element = ET.SubElement(parent, xml_field_name)
        for key, val in value.items():
            _serialize_field_xml(val, Any, key, element)
        return

    # Handle primitive types
    # FHIR XML uses value attribute for primitive types: <field value="value"/>
    element = ET.SubElement(parent, xml_field_name)
    element.set("value", str(value))


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

    # Handle resourceType and id as attributes for root element (only for FHIRResource)
    if isinstance(obj, FHIRResource) and hasattr(obj, "resourceType") and element.tag == obj.resourceType:
        if hasattr(obj, "id") and obj.id:
            element.set("id", obj.id)

    for field_name, field_value in obj.__dict__.items():
        if field_name.startswith("_"):
            continue
        # Skip resourceType and id for root resource element (already handled as attributes)
        if isinstance(obj, FHIRResource) and field_name in ("resourceType", "id") and element.tag == obj.resourceType:
            continue
        
        # Skip contained field if it's being handled separately
        if skip_contained and field_name == "contained":
            continue
        if field_value is not None:
            field_type = hints.get(field_name, Any)
            _serialize_field_xml(field_value, field_type, field_name, element)


def serialize_fhir_xml(
    resource: FHIRResource,
    encoding: str = "UTF-8",
    fhir_version: Optional[str] = None,
    include_version: bool = False,
) -> str:
    """
    Serialize FHIR resource to XML string.
    
    Version-aware serializer that supports both R4 and R5. Can optionally
    include fhirVersion attribute in the XML root element.

    Args:
        resource: FHIR resource object
        encoding: XML encoding
        fhir_version: Optional FHIR version to include in output ("4.0", "R4", "5.0", "R5", etc.)
        include_version: If True, include fhirVersion attribute in root element (default: False for backward compatibility)

    Returns:
        XML string
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    resource_type = getattr(resource, 'resourceType', 'Unknown')
    logger.debug(f"[{current_time}] Starting FHIR XML serialization for resource type: {resource_type}")
    
    # Create root element
    root = ET.Element(resource.resourceType)
    if resource.id:
        root.set("id", resource.id)
    
    # Optionally add fhirVersion attribute
    if include_version and fhir_version:
        version = normalize_version(fhir_version)
        root.set("fhirVersion", get_version_string(version))

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
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] FHIR XML serialization completed successfully in {elapsed:.3f} seconds")
    logger.debug(f"[{current_time}] Current Time at End of Operations: {current_time}")
    
    return result

