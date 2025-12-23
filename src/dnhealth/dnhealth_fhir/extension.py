# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Extension definition support.

Supports parsing and working with Extension definitions from StructureDefinition.
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.structuredefinition import StructureDefinition, ElementDefinition, get_element_definitions


@dataclass
class ExtensionDefinition:
    """
    Represents an Extension definition parsed from StructureDefinition.
    """
    
    url: str
    name: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    context: List[str] = field(default_factory=list)
    value_types: List[str] = field(default_factory=list)  # List of allowed value types
    cardinality_min: Optional[int] = None
    cardinality_max: Optional[str] = None
    is_modifier: bool = False
    description: Optional[str] = None
    binding: Optional[Dict[str, Any]] = None
    constraint: List[Dict[str, Any]] = field(default_factory=list)


def parse_extension_definition(structure_def: StructureDefinition) -> Optional[ExtensionDefinition]:
    """
    Parse an Extension definition from a StructureDefinition.
    
    Args:
        structure_def: StructureDefinition representing an Extension
        
    Returns:
        ExtensionDefinition object or None if not an Extension
    """
    # Check if this is an Extension StructureDefinition
    if structure_def.kind != "complex-type" or structure_def.type != "Extension":
        return None
    
    if not structure_def.url:
        return None
    
    ext_def = ExtensionDefinition(url=structure_def.url)
    ext_def.name = structure_def.name
    ext_def.title = structure_def.title
    ext_def.status = structure_def.status
    ext_def.description = structure_def.description
    
    # Get element definitions
    elements = get_element_definitions(structure_def)
    
    # Find Extension.value[x] element
    for element in elements:
        if element.path and element.path.startswith("Extension.value"):
            # Extract value type from path (e.g., "Extension.valueString" -> "string")
            if "." in element.path:
                value_type = element.path.split(".")[-1].replace("value", "").lower()
                if value_type:
                    ext_def.value_types.append(value_type)
            
            # Get cardinality
            if element.min is not None:
                ext_def.cardinality_min = element.min
            if element.max:
                ext_def.cardinality_max = element.max
            
            # Get binding
            if element.binding:
                ext_def.binding = element.binding
            
            # Get constraints
            if element.constraint:
                ext_def.constraint.extend(element.constraint)
            
            # Check if modifier
            if element.isModifier:
                ext_def.is_modifier = True
    
    # Find Extension.url element to get context
    for element in elements:
        if element.path == "Extension.url":
            # Context might be in constraints or elsewhere
            pass
    
    return ext_def


def get_extension_definitions(structure_defs: List[StructureDefinition]) -> Dict[str, ExtensionDefinition]:
    """
    Extract Extension definitions from a list of StructureDefinitions.
    
    Args:
        structure_defs: List of StructureDefinition objects
        
    Returns:
        Dictionary mapping extension URLs to ExtensionDefinition objects
    """
    extensions = {}
    
    for sd in structure_defs:
        ext_def = parse_extension_definition(sd)
        if ext_def:
            extensions[ext_def.url] = ext_def
    
    return extensions


def validate_extension_value(extension_url: str, value: Any, extension_def: ExtensionDefinition) -> List[str]:
    """
    Validate an extension value against its definition.
    
    Args:
        extension_url: Extension URL
        value: Extension value to validate
        extension_def: ExtensionDefinition
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Check if value type is allowed
    if extension_def.value_types:
        value_type = _get_value_type(value)
        if value_type not in extension_def.value_types:
            errors.append(
                f"Extension '{extension_url}' value type '{value_type}' is not allowed. "
                f"Allowed types: {extension_def.value_types}"
            )
    
    # Check cardinality
    if extension_def.cardinality_min is not None and extension_def.cardinality_min > 0:
        if value is None:
            errors.append(
                f"Extension '{extension_url}' is required (min={extension_def.cardinality_min})"
            )
    
    return errors


def _get_value_type(value: Any) -> str:
    """
    Get the FHIR value type for a Python value.
    
    Args:
        value: Python value
        
    Returns:
        FHIR value type name
    """
    if isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "decimal"
    elif isinstance(value, str):
        # Could be string, uri, url, code, id, markdown, date, dateTime, time, instant, base64Binary, canonical, oid, uuid
        # For now, default to string
        return "string"
    elif isinstance(value, dict):
        # Complex type - would need to check structure
        return "complex"
    elif isinstance(value, list):
        return "array"
    return "unknown"


def find_extension_definition(extension_url: str, extension_defs: Dict[str, ExtensionDefinition]) -> Optional[ExtensionDefinition]:
    """
    Find an Extension definition by URL.
    
    Args:
        extension_url: Extension URL
        extension_defs: Dictionary of ExtensionDefinition objects
        
    Returns:
        ExtensionDefinition or None if not found
    """
    return extension_defs.get(extension_url)


def get_extension_contexts(extension_def: ExtensionDefinition) -> List[str]:
    """
    Get the contexts where an extension can be used.
    
    Args:
        extension_def: ExtensionDefinition
        
    Returns:
        List of context strings (e.g., ["Patient", "Observation"])
    """
    return extension_def.context.copy()


def is_modifier_extension(extension: "Extension", extension_definitions: Dict[str, ExtensionDefinition]) -> bool:
    """
    Check if an extension is a modifier extension.
    
    Args:
        extension: Extension object
        extension_definitions: Dictionary of ExtensionDefinition objects by URL
        
    Returns:
        True if extension is a modifier extension, False otherwise
    """
    if not extension.url:
        return False
    
    ext_def = find_extension_definition(extension.url, extension_definitions)
    if ext_def:
        return ext_def.is_modifier
    
    return False


def get_modifier_extensions(resource: "FHIRResource", extension_definitions: Dict[str, ExtensionDefinition]) -> List["Extension"]:
    """
    Get all modifier extensions from a resource.
    
    Args:
        resource: FHIR resource
        extension_definitions: Dictionary of ExtensionDefinition objects by URL
        
    Returns:
        List of modifier Extension objects
    """
    from dnhealth.dnhealth_fhir.types import Extension
    
    modifier_extensions = []
    
    # Check modifierExtension field if it exists
    if hasattr(resource, "modifierExtension") and resource.modifierExtension:
        modifier_extensions.extend(resource.modifierExtension)
    
    # Also check regular extension field for modifier extensions
    if hasattr(resource, "extension") and resource.extension:
        for ext in resource.extension:
            if is_modifier_extension(ext, extension_definitions):
                modifier_extensions.append(ext)
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return modifier_extensions


def validate_modifier_extensions(
    resource: "FHIRResource",
    extension_definitions: Dict[str, ExtensionDefinition]
) -> List[str]:
    """
    Validate modifier extensions on a resource.
    
    Modifier extensions change the meaning of the element they're on.
    
    Args:
        resource: FHIR resource
        extension_definitions: Dictionary of ExtensionDefinition objects by URL
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Get modifier extensions
    modifier_extensions = get_modifier_extensions(resource, extension_definitions)
    
    # Validate each modifier extension
    for ext in modifier_extensions:
        if not ext.url:
            errors.append("Modifier extension missing required 'url' field")
            continue
        
        # Find extension definition
        ext_def = find_extension_definition(ext.url, extension_definitions)
        if not ext_def:
            # Unknown modifier extension - this is a warning
            errors.append(f"Unknown modifier extension: '{ext.url}'")
            continue
        
        # Validate that it's actually marked as a modifier
        if not ext_def.is_modifier:
            errors.append(f"Extension '{ext.url}' is not marked as a modifier extension")
        
        # Validate value
        ext_value = _get_extension_value_for_validation(ext)
        if ext_value is not None:
            value_errors = validate_extension_value(ext.url, ext_value, ext_def)
            for error in value_errors:
                errors.append(f"Modifier extension '{ext.url}': {error}")
    
    return errors


def _get_extension_value_for_validation(extension: "Extension") -> Any:
    """
    Get the value from an Extension object for validation.
    
    Args:
        extension: Extension object
        
    Returns:
        Extension value or None
    """
    # Check all value fields
    value_fields = [
        "valueString", "valueBoolean", "valueInteger", "valueDecimal",
        "valueDate", "valueDateTime", "valueUri", "valueCode"
    ]
    
    for field in value_fields:
        if hasattr(extension, field):
            value = getattr(extension, field)
            if value is not None:
                return value
    
    return None


# ============================================================================
# Nested Extension Support
# ============================================================================

def parse_nested_extension(extension_data: Dict[str, Any]) -> "Extension":
    """
    Parse extension with nested extensions in extension.extension.
    
    Recursively parses all nested levels of extensions.
    
    Args:
        extension_data: Dictionary containing extension data (JSON format)
        
    Returns:
        Extension object with nested extensions
        
    Raises:
        ValueError: If extension_data is invalid
    """
    from datetime import datetime
    import logging
    
    logger = logging.getLogger(__name__)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting nested extension parsing")
    
    from dnhealth.dnhealth_fhir.types import Extension
    from dnhealth.dnhealth_fhir.parser_json import _parse_field
    
    if not isinstance(extension_data, dict):
        raise ValueError("extension_data must be a dictionary")
    
    if "url" not in extension_data:
        raise ValueError("Extension must have a 'url' field")
    
    # Parse the base extension
    extension = _parse_field(extension_data, Extension, "extension")
    
    # Recursively parse nested extensions if present
    if "extension" in extension_data and isinstance(extension_data["extension"], list):
        nested_extensions = []
        for nested_data in extension_data["extension"]:
            if isinstance(nested_data, dict):
                nested_ext = parse_nested_extension(nested_data)
                nested_extensions.append(nested_ext)
        extension.extension = nested_extensions
    
    logger.debug(f"[{current_time}] Nested extension parsing completed")
    return extension


def validate_nested_extension(
    extension: "Extension",
    extension_def: Optional[ExtensionDefinition] = None
) -> List[str]:
    """
    Validate extension structure including nested extensions.
    
    Validates extension structure, nested extensions against extension definition,
    checks cardinality, and required nested extensions.
    
    Args:
        extension: Extension object to validate
        extension_def: Optional ExtensionDefinition for validation
        
    Returns:
        List of validation error messages (empty if valid)
    """
    from datetime import datetime
    import logging
    
    logger = logging.getLogger(__name__)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting nested extension validation")
    
    errors = []
    
    if not extension:
        errors.append("Extension is None")
        logger.warning(f"[{current_time}] Nested extension validation failed: extension is None")
        return errors
    
    # Validate base extension
    if not extension.url:
        errors.append("Extension missing required 'url' field")
    
    # Validate nested extensions if present
    if extension.extension:
        if not isinstance(extension.extension, list):
            errors.append("Extension.extension must be a list")
            return errors
        
        # Validate each nested extension recursively
        for i, nested_ext in enumerate(extension.extension):
            if not isinstance(nested_ext, Extension):
                errors.append(f"Nested extension at index {i} is not a valid Extension")
                continue
            
            # Recursively validate nested extension
            nested_errors = validate_nested_extension(nested_ext, extension_def)
            for error in nested_errors:
                errors.append(f"Nested extension at index {i}: {error}")
    
    # If extension definition provided, validate against it
    if extension_def:
        # Check if nested extensions match extension definition
        # This would require extension definition to specify nested extension structure
        # For now, we do basic validation
        
        # Check cardinality if specified
        if extension_def.cardinality_min is not None:
            nested_count = len(extension.extension) if extension.extension else 0
            if nested_count < extension_def.cardinality_min:
                errors.append(
                    f"Extension '{extension.url}' has {nested_count} nested extensions, "
                    f"but minimum is {extension_def.cardinality_min}"
                )
        
        if extension_def.cardinality_max and extension_def.cardinality_max != "*":
            try:
                max_count = int(extension_def.cardinality_max)
                nested_count = len(extension.extension) if extension.extension else 0
                if nested_count > max_count:
                    errors.append(
                        f"Extension '{extension.url}' has {nested_count} nested extensions, "
                        f"but maximum is {max_count}"
                    )
            except ValueError:
                pass  # Invalid max value, skip
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.debug(f"[{current_time}] Nested extension validation passed")
    else:
        logger.warning(f"[{current_time}] Nested extension validation failed: {len(errors)} errors")
    
    return errors


def serialize_nested_extension(extension: "Extension", format: str = "json") -> Dict[str, Any]:
    """
    Serialize extension with nested extensions.
    
    Recursively serializes all nested levels of extensions.
    
    Args:
        extension: Extension object with nested extensions
        format: Output format ("json" or "xml")
        
    Returns:
        Dictionary (for JSON) or string (for XML) containing serialized extension
        
    Raises:
        ValueError: If format is not supported
    """
    from datetime import datetime
    import logging
    
    logger = logging.getLogger(__name__)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting nested extension serialization (format: {format})")
    
    if format not in ("json", "xml"):
        raise ValueError(f"Unsupported format: {format}. Must be 'json' or 'xml'")
    
    if format == "json":
        from dnhealth.dnhealth_fhir.serializer_json import _serialize_dataclass
        
        # Serialize base extension
        result = _serialize_dataclass(extension)
        
        # Recursively serialize nested extensions
        if extension.extension:
            nested_list = []
            for nested_ext in extension.extension:
                nested_dict = serialize_nested_extension(nested_ext, format="json")
                nested_list.append(nested_dict)
            result["extension"] = nested_list
        
        logger.debug(f"[{current_time}] Nested extension serialization completed (JSON)")
        return result
    
    else:  # XML format
        from dnhealth.dnhealth_fhir.serializer_xml import serialize_extension_to_xml
        
        # Use XML serializer if available, otherwise build manually
        try:
            return serialize_extension_to_xml(extension)
        except (ImportError, AttributeError):
            # Fallback: build XML manually
            xml_parts = [f'<extension url="{extension.url}">']
            
            # Add value if present
            value_fields = [
                "valueString", "valueBoolean", "valueInteger", "valueDecimal",
                "valueDate", "valueDateTime", "valueUri", "valueCode"
            ]
            for field in value_fields:
                if hasattr(extension, field):
                    value = getattr(extension, field)
                    if value is not None:
                        field_name = field.replace("value", "").lower()
                        xml_parts.append(f'<value{field_name.capitalize()} value="{value}"/>')
            
            # Recursively serialize nested extensions
            if extension.extension:
                for nested_ext in extension.extension:
                    nested_xml = serialize_nested_extension(nested_ext, format="xml")
                    if isinstance(nested_xml, str):
                        xml_parts.append(nested_xml)
            
            xml_parts.append("</extension>")
            result = "".join(xml_parts)
            logger.debug(f"[{current_time}] Nested extension serialization completed (XML)")
            return result


# ============================================================================
# Extension Registry
# ============================================================================

class ExtensionRegistry:
    """
    Registry for Extension definitions.
    
    Maintains a registry of extension definitions and supports lookup by URL
    and validation against definitions.
    """
    
    def __init__(self):
        """Initialize the extension registry."""
        self._extensions: Dict[str, ExtensionDefinition] = {}
    
    def register(self, ext_def: ExtensionDefinition) -> None:
        """
        Register an extension definition.
        
        Args:
            ext_def: ExtensionDefinition to register
        """
        if not ext_def.url:
            raise ValueError("Extension definition must have a URL")
        self._extensions[ext_def.url] = ext_def
    
    def get(self, url: str) -> Optional[ExtensionDefinition]:
        """
        Get extension definition by URL.
        
        Args:
            url: Extension URL
            
        Returns:
            ExtensionDefinition or None if not found
        """
        return self._extensions.get(url)
    
    def list(self) -> List[str]:
        """
        List all registered extension URLs.
        
        Returns:
            List of extension URLs
        """
        return list(self._extensions.keys())
    
    def validate_extension(self, extension: "Extension") -> List[str]:
        """
        Validate extension against registry.
        
        Args:
            extension: Extension object to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not extension.url:
            errors.append("Extension missing required 'url' field")
            return errors
        
        ext_def = self.get(extension.url)
        if ext_def:
            # Validate against definition
            validation_errors = validate_nested_extension(extension, ext_def)
            errors.extend(validation_errors)
        else:
            # Unknown extension - this is a warning, not an error
            pass  # Could add warning if desired
        
        return errors

