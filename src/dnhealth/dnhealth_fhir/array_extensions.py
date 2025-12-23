# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Array Extensions support.

Array extensions allow extensions to be placed on list/array fields.
In FHIR JSON, array extensions use the format "_fieldName" where fieldName
is the name of the array field.
"""

from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime
import logging

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.extension import ExtensionDefinition

from dnhealth.dnhealth_fhir.types import Extension

logger = logging.getLogger(__name__)


def parse_array_extensions(
    data: Dict[str, Any],    field_name: str
) -> Optional[List[Extension]]:
    """
    Parse array extensions for a list field.
    
    Array extensions are stored in a field named "_fieldName" where fieldName
    is the name of the array field. The extension field contains an object
    with an "extension" array.
    
    Args:
        data: JSON data dictionary
        field_name: Name of the array field
        
    Returns:
        List of Extension objects if found, None otherwise
    """
    extension_field_name = f"_{field_name}"
    
    if extension_field_name not in data:
        return None
    
    extension_data = data[extension_field_name]
    
    # Array extension should be an object with an "extension" field
    if not isinstance(extension_data, dict):
        return None
    
    if "extension" not in extension_data:
        return None
    
    extensions_list = extension_data["extension"]
    if not isinstance(extensions_list, list):
        return None
    
    # Parse each extension
    from dnhealth.dnhealth_fhir.parser_json import _parse_field
    from typing import get_type_hints
    
    extensions = []
    for ext_data in extensions_list:
        if isinstance(ext_data, dict):
            try:
                # Parse extension using the same logic as regular extensions
                ext = _parse_field(ext_data, Extension, "extension")
                if ext:
                    extensions.append(ext)
            except Exception:
                # Skip invalid extensions
                pass
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Array extensions parsing completed: {len(extensions)} extensions found for field '{field_name}'")
    
    return extensions if extensions else None


def serialize_array_extensions(
    extensions: Optional[List[Extension]],
    field_name: str,
    format: str = "json"
) -> Optional[Dict[str, Any]]:
    """
    Serialize array extensions for a list field.
    
    Args:
        extensions: List of Extension objects
        field_name: Name of the array field
        format: Output format ("json" or "xml")
        
    Returns:
        Dictionary with "_fieldName" key containing extension data (for JSON), or None
    """
    if not extensions:
        return None
    
    if format == "json":
        # Serialize extensions with nested extension support
        from dnhealth.dnhealth_fhir.extension import serialize_nested_extension
        
        extension_list = []
        for ext in extensions:
            ext_dict = serialize_nested_extension(ext, format="json")
            extension_list.append(ext_dict)
        
        return {
            f"_{field_name}": {
                "extension": extension_list
            }
        }
    else:  # XML format
        # For XML, return as string
        from dnhealth.dnhealth_fhir.extension import serialize_nested_extension
        
        xml_parts = [f'<_{field_name}>']
        for ext in extensions:
            ext_xml = serialize_nested_extension(ext, format="xml")
            if isinstance(ext_xml, str):
                xml_parts.append(ext_xml)
        xml_parts.append(f'</_{field_name}>')
        
        result = "".join(xml_parts)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Array extensions serialization completed: {len(extensions)} extensions serialized for field '{field_name}' in {format} format")
        
        return result


def validate_array_extensions(
    extensions: Optional[List[Extension]],
    field_name: str,
    extension_def: Optional["ExtensionDefinition"] = None
) -> List[str]:
    """
    Validate array extensions.
    
    Validates each extension in array, validates array cardinality (min, max),
    and checks for duplicate extensions.
    
    Args:
        extensions: List of Extension objects to validate
        field_name: Name of the array field
        extension_def: Optional ExtensionDefinition for validation
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if not extensions:
        # Check if extensions are required
        if extension_def and extension_def.cardinality_min and extension_def.cardinality_min > 0:
            errors.append(
                f"Array extensions for field '{field_name}' are required "
                f"(min={extension_def.cardinality_min})"
            )
        return errors
    
    # Validate array cardinality
    if extension_def:
        array_length = len(extensions)
        
        # Check minimum
        if extension_def.cardinality_min is not None and array_length < extension_def.cardinality_min:
            errors.append(
                f"Array extensions for field '{field_name}' has {array_length} items, "
                f"but minimum is {extension_def.cardinality_min}"
            )
        
        # Check maximum
        if extension_def.cardinality_max and extension_def.cardinality_max != "*":
            try:
                max_count = int(extension_def.cardinality_max)
                if array_length > max_count:
                    errors.append(
                        f"Array extensions for field '{field_name}' has {array_length} items, "
                        f"but maximum is {max_count}"
                    )
            except ValueError:
                pass  # Invalid max value, skip
    
    # Validate each extension in array
    seen_urls = set()
    for i, ext in enumerate(extensions):
        if not isinstance(ext, Extension):
            errors.append(f"Array extension at index {i} for field '{field_name}' is not a valid Extension")
            continue
        
        if not ext.url:
            errors.append(f"Array extension at index {i} for field '{field_name}' missing required 'url' field")
            continue
        
        # Check for duplicates (if not allowed)
        if ext.url in seen_urls:
            errors.append(
                f"Duplicate extension URL '{ext.url}' at index {i} for field '{field_name}'"
            )
        seen_urls.add(ext.url)
        
        # Validate nested extensions if present
        if ext.extension:
            from dnhealth.dnhealth_fhir.extension import validate_nested_extension
            nested_errors = validate_nested_extension(ext, extension_def)
            for error in nested_errors:
                errors.append(f"Array extension at index {i} for field '{field_name}': {error}")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Array extensions validation completed: {len(errors)} errors found for field '{field_name}'")
    
    return errors


def parse_array_extension(extension_data: List[Dict[str, Any]]) -> List[Extension]:
    """
    Parse array of extensions.
    
    Each extension in array can have nested extensions.
    
    Args:
        extension_data: List of dictionaries containing extension data (JSON format)
        
    Returns:
        List of Extension objects
        
    Raises:
        ValueError: If extension_data is invalid
    """
    if not isinstance(extension_data, list):
        raise ValueError("extension_data must be a list")
    
    from dnhealth.dnhealth_fhir.extension import parse_nested_extension
    
    extensions = []
    for i, ext_data in enumerate(extension_data):
        if not isinstance(ext_data, dict):
            raise ValueError(f"Extension at index {i} must be a dictionary")
        
        try:
            ext = parse_nested_extension(ext_data)
            extensions.append(ext)
        except Exception as e:
            raise ValueError(f"Failed to parse extension at index {i}: {e}")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Array extension parsing completed successfully: {len(extensions)} extensions parsed")
    
    return extensions


def serialize_array_extensions_list(
    extensions: List[Extension],
    format: str = "json"
) -> List[Dict[str, Any]]:
    """
    Serialize array of extensions to list format.
    
    Serializes a list of extensions (not the _fieldName format, but direct list).
    Each extension can have nested extensions.
    
    Args:
        extensions: List of Extension objects
        format: Output format ("json" or "xml")
        
    Returns:
        List of dictionaries (for JSON) or XML string (for XML)
        
    Raises:
        ValueError: If format is not supported
    """
    if format not in ("json", "xml"):
        raise ValueError(f"Unsupported format: {format}. Must be 'json' or 'xml'")
    
    from dnhealth.dnhealth_fhir.extension import serialize_nested_extension
    
    if format == "json":
        result = []
        for ext in extensions:
            ext_dict = serialize_nested_extension(ext, format="json")
            result.append(ext_dict)
    else:  # XML format
        xml_parts = []
        for ext in extensions:
            ext_xml = serialize_nested_extension(ext, format="xml")
            if isinstance(ext_xml, str):
                xml_parts.append(ext_xml)
        result = "".join(xml_parts)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Array extension serialization completed successfully: {len(extensions)} extensions serialized")
    
    return result
