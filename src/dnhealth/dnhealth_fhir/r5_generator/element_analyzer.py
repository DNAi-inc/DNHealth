# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Element Analyzer for FHIR R5 StructureDefinitions.

Analyzes element definitions to extract types, cardinality, constraints,
choice types, nested structures, and other metadata needed for code generation.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from dnhealth.dnhealth_fhir.r5_generator.profile_parser import (
    StructureDefinition,
    ElementDefinition,
    TypeDefinition,
)


@dataclass
class ElementMetadata:
    """
    Metadata about an element for code generation.
    
    Contains processed information about an element that's needed
    to generate Python code.
    """
    
    field_name: str  # Python field name (e.g., "status", "patient")
    field_type: str  # Python type (e.g., "Optional[str]", "List[Reference]")
    is_required: bool  # Whether field is required (min > 0)
    is_list: bool  # Whether field is a list (max == "*" or max > 1)
    is_choice_type: bool  # Whether this is a choice type (e.g., value[x])
    choice_base_name: Optional[str] = None  # Base name for choice type (e.g., "value" for value[x])
    choice_types: List[str] = field(default_factory=list)  # List of choice type variants
    is_nested: bool = False  # Whether this is a nested structure (backbone element)
    nested_class_name: Optional[str] = None  # Name of nested class if applicable
    is_primitive: bool = False  # Whether this is a primitive type
    is_reference: bool = False  # Whether this is a Reference type
    is_extension: bool = False  # Whether this is an extension
    is_modifier_extension: bool = False  # Whether this is a modifierExtension
    docstring: Optional[str] = None  # Documentation string
    default_value: Optional[str] = None  # Default value as Python code
    original_element: ElementDefinition = None  # Original element definition


def analyze_elements(
    struct_def: StructureDefinition,
    resource_name: str
) -> Tuple[List[ElementMetadata], Dict[str, List[ElementMetadata]]]:
    """
    Analyze all elements in a StructureDefinition.
    
    Args:
        struct_def: StructureDefinition to analyze
        resource_name: Name of the resource (e.g., "Task", "Patient")
        
    Returns:
        Tuple of:
        - List of ElementMetadata for top-level resource fields
        - Dictionary mapping nested class names to their ElementMetadata lists
    """
    # Filter elements to only those for this resource (not base Resource/DomainResource)
    resource_elements = [
        elem for elem in struct_def.elements
        if elem.path.startswith(resource_name + ".") and elem.path != resource_name
    ]
    
    # Identify nested structures (backbone elements)
    nested_structures = _identify_nested_structures(resource_elements, resource_name)
    
    # Process top-level elements
    top_level_metadata = []
    nested_metadata = {}
    
    for elem in resource_elements:
        # Skip if this is part of a nested structure
        is_nested = any(
            elem.path.startswith(nested_path + ".")
            for nested_path in nested_structures.keys()
        )
        
        if is_nested:
            # This will be handled when processing nested structures
            continue
        
        metadata = _analyze_element(elem, resource_name, nested_structures)
        if metadata:
            top_level_metadata.append(metadata)
    
    # Process nested structures
    for nested_path, nested_elements in nested_structures.items():
        nested_class_name = _path_to_class_name(nested_path, resource_name)
        nested_elems_metadata = []
        
        for elem in nested_elements:
            metadata = _analyze_element(elem, resource_name, nested_structures, is_nested=True)
            if metadata:
                nested_elems_metadata.append(metadata)
        
        if nested_elems_metadata:
            nested_metadata[nested_class_name] = nested_elems_metadata
    
    return top_level_metadata, nested_metadata


def _identify_nested_structures(
    elements: List[ElementDefinition],
    resource_name: str
) -> Dict[str, List[ElementDefinition]]:
    """
    Identify nested structures (backbone elements) in the element list.
    
    Args:
        elements: List of element definitions
        resource_name: Name of the resource
        
    Returns:
        Dictionary mapping nested structure paths to their elements
    """
    nested_structures = {}
    
    for elem in elements:
        # Check if this element has a type that indicates a nested structure
        # Nested structures typically have types like "BackboneElement" or are
        # elements that have children but aren't primitives
        has_nested_type = any(
            type_def.code in ["BackboneElement", "Element"] or
            (not _is_primitive_type(type_def.code) and len(elem.path.split(".")) > 2)
            for type_def in elem.types
        )
        
        # Check if this element has children (elements with paths like "Task.input.item")
        path_parts = elem.path.split(".")
        if len(path_parts) > 2:  # More than "Resource.field"
            # This might be a nested structure
            # Find all elements that are children of this element
            parent_path = ".".join(path_parts[:-1])
            if parent_path not in nested_structures:
                nested_structures[parent_path] = []
    
    # Now collect elements for each nested structure
    for nested_path in list(nested_structures.keys()):
        nested_structures[nested_path] = [
            elem for elem in elements
            if elem.path.startswith(nested_path + ".") and elem.path != nested_path
        ]
    
    return nested_structures


def _analyze_element(
    elem: ElementDefinition,
    resource_name: str,
    nested_structures: Dict[str, List[ElementDefinition]],
    is_nested: bool = False
) -> Optional[ElementMetadata]:
    """
    Analyze a single element and create metadata for code generation.
    
    Args:
        elem: Element definition to analyze
        resource_name: Name of the resource
        nested_structures: Dictionary of nested structures
        is_nested: Whether this element is part of a nested structure
        
    Returns:
        ElementMetadata object, or None if element should be skipped
    """
    # Skip base Resource/DomainResource fields that are already in base classes
    base_fields = {
        "id", "meta", "implicitRules", "language",  # Resource fields
        "text", "contained", "extension", "modifierExtension"  # DomainResource fields
    }
    
    field_name = _path_to_field_name(elem.path, resource_name)
    if field_name in base_fields and not is_nested:
        # This field is already in the base class, skip it
        return None
    
    # Check if this is a choice type (e.g., value[x], deceased[x])
    is_choice_type, choice_base_name = _is_choice_type(elem.path, field_name)
    
    # Determine if required
    is_required = elem.min > 0
    
    # Determine if list
    is_list = elem.max == "*" or (elem.max.isdigit() and int(elem.max) > 1)
    
    # Determine field type (will be refined by type mapper)
    field_type = "Any"  # Placeholder, will be set by type mapper
    
    # Check if primitive
    is_primitive = any(_is_primitive_type(type_def.code) for type_def in elem.types)
    
    # Check if reference
    is_reference = any(type_def.code == "Reference" for type_def in elem.types)
    
    # Check if extension
    is_extension = field_name == "extension"
    is_modifier_extension = field_name == "modifierExtension"
    
    # Get docstring
    docstring = elem.definition or elem.short or elem.comment
    
    # Get default value
    default_value = None
    if elem.defaultValue is not None:
        default_value = _format_default_value(elem.defaultValue)
    
    # Get choice types if applicable
    choice_types = []
    if is_choice_type:
        # Extract choice type variants from element path or types
        # For value[x], types might be valueString, valueInteger, etc.
        # We'll need to look at sibling elements or type definitions
        pass  # Will be handled separately
    
    return ElementMetadata(
        field_name=field_name,
        field_type=field_type,  # Will be set by type mapper
        is_required=is_required,
        is_list=is_list,
        is_choice_type=is_choice_type,
        choice_base_name=choice_base_name,
        choice_types=choice_types,
        is_nested=is_nested,
        nested_class_name=None,  # Will be set if nested
        is_primitive=is_primitive,
        is_reference=is_reference,
        is_extension=is_extension,
        is_modifier_extension=is_modifier_extension,
        docstring=docstring,
        default_value=default_value,
        original_element=elem,
    )


def _is_choice_type(path: str, field_name: str) -> Tuple[bool, Optional[str]]:
    """
    Check if an element is a choice type (e.g., value[x]).
    
    Args:
        path: Element path
        field_name: Field name
        
    Returns:
        Tuple of (is_choice_type, choice_base_name)
    """
    if "[x]" in path or "[x]" in field_name:
        # Extract base name (e.g., "value" from "value[x]")
        base_name = field_name.replace("[x]", "")
        return True, base_name
    return False, None


def _is_primitive_type(type_code: str) -> bool:
    """
    Check if a type code represents a primitive type.
    
    Args:
        type_code: Type code (e.g., "string", "integer", "Reference")
        
    Returns:
        True if primitive, False otherwise
    """
    primitive_types = {
        "string", "code", "id", "uri", "url", "canonical", "base64Binary",
        "integer", "positiveInt", "unsignedInt", "decimal",
        "boolean", "date", "dateTime", "time", "instant",
        "markdown", "xhtml", "oid", "uuid",
    }
    return type_code in primitive_types


def _path_to_field_name(path: str, resource_name: str) -> str:
    """
    Convert element path to Python field name.
    
    Args:
        path: Element path (e.g., "Task.status", "Task.input.item", "Task.participant.id")
        resource_name: Resource name (e.g., "Task")
        
    Returns:
        Python field name (e.g., "status", "input", "id")
    """
    # Python keywords that cannot be used as field names
    PYTHON_KEYWORDS = {
        "and", "as", "assert", "break", "class", "continue", "def", "del",
        "elif", "else", "except", "exec", "finally", "for", "from", "global",
        "if", "import", "in", "is", "lambda", "not", "or", "pass", "print",
        "raise", "return", "try", "while", "with", "yield", "False", "None",
        "True", "nonlocal"
    }
    
    # Built-in functions and common imports that should be avoided
    RESERVED_NAMES = {
        "field", "dataclass", "list", "dict", "set", "tuple", "str", "int",
        "float", "bool", "type", "object", "Any", "Optional", "Union"
    }
    
    # Remove resource name prefix
    if path.startswith(resource_name + "."):
        path = path[len(resource_name) + 1:]
    
    # Get the last part (field name) - this handles nested structures correctly
    # For "Task.participant.id", we want "id", not "participant"
    parts = path.split(".")
    field_name = parts[-1]  # Get the last part, not the first
    
    # Remove [x] from choice types for base name
    field_name = field_name.replace("[x]", "")
    
    # Convert to snake_case if needed (FHIR uses camelCase, Python typically uses snake_case)
    # But we'll keep camelCase to match existing R4 resources
    
    # Handle Python keywords and reserved names by appending underscore
    if field_name in PYTHON_KEYWORDS or field_name in RESERVED_NAMES:
        field_name = field_name + "_"
    
    return field_name


def _path_to_class_name(path: str, resource_name: str) -> str:
    """
    Convert nested structure path to Python class name.
    
    Args:
        path: Element path (e.g., "Task.input")
        resource_name: Resource name (e.g., "Task")
        
    Returns:
        Python class name (e.g., "TaskInput")
    """
    # Remove resource name prefix
    if path.startswith(resource_name + "."):
        path = path[len(resource_name) + 1:]
    
    # Convert to PascalCase
    parts = path.split(".")
    class_name = resource_name + "".join(part[0].upper() + part[1:] if part else "" for part in parts)
    
    return class_name


def _format_default_value(value: Any) -> str:
    """
    Format a default value as Python code.
    
    Args:
        value: Default value (could be str, int, bool, etc.)
        
    Returns:
        Python code string for the default value
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "True" if value else "False"
    elif isinstance(value, (int, float)):
        return str(value)
    elif value is None:
        return "None"
    else:
        # For complex types, return as string representation
        return repr(value)
