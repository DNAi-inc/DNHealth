# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Code Generator for FHIR R5 resources.

Generates Python dataclass code from parsed StructureDefinitions.
"""

from typing import List, Dict, Set
from pathlib import Path

from dnhealth.dnhealth_fhir.r5_generator.profile_parser import StructureDefinition
from dnhealth.dnhealth_fhir.r5_generator.element_analyzer import ElementMetadata
from dnhealth.dnhealth_fhir.r5_generator.type_mapper import (
    map_fhir_type_to_python,
    get_all_imports_for_elements,
    format_imports,
)


COPYRIGHT_HEADER = """# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.
"""


def generate_resource_code(
    struct_def: StructureDefinition,
    top_level_metadata: List[ElementMetadata],
    nested_metadata: Dict[str, List[ElementMetadata]],
    base_class: str = "FHIRResource"
) -> str:
    """
    Generate Python code for a resource class.
    
    Args:
        struct_def: StructureDefinition to generate code for
        top_level_metadata: Metadata for top-level fields
        nested_metadata: Metadata for nested classes
        base_class: Base class to inherit from
        
    Returns:
        Generated Python code as string
    """
    resource_name = struct_def.type or struct_def.id
    
    # Generate imports
    all_elements = [meta.original_element for meta in top_level_metadata if meta.original_element]
    for nested_elems in nested_metadata.values():
        all_elements.extend([meta.original_element for meta in nested_elems if meta.original_element])
    
    imports = get_all_imports_for_elements(all_elements)
    imports.add("from dataclasses import dataclass, field")
    imports.add("from typing import List, Optional")
    imports.add(f"from dnhealth.dnhealth_fhir.resources.base import {base_class}")
    
    # Generate docstring
    docstring = _generate_docstring(struct_def)
    
    # Generate nested classes first
    nested_classes_code = []
    for nested_class_name, nested_elems in nested_metadata.items():
        nested_code = generate_nested_class_code(
            nested_class_name,
            nested_elems,
            struct_def
        )
        nested_classes_code.append(nested_code)
    
    # Generate main resource class
    class_code = _generate_class_code(
        resource_name,
        base_class,
        top_level_metadata,
        docstring
    )
    
    # Combine all parts
    code_parts = [
        COPYRIGHT_HEADER,
        "",
        '"""',
        f"FHIR R5 {resource_name} resource.",
        "",
        docstring,
        '"""',
        "",
        format_imports(imports),
        "",
    ]
    
    # Add nested classes
    if nested_classes_code:
        code_parts.extend(nested_classes_code)
        code_parts.append("")
    
    # Add main class
    code_parts.append(class_code)
    
    return "\n".join(code_parts)


def generate_nested_class_code(
    class_name: str,
    elements_metadata: List[ElementMetadata],
    struct_def: StructureDefinition
) -> str:
    """
    Generate Python code for a nested class.
    
    Args:
        class_name: Name of the nested class
        elements_metadata: Metadata for nested class fields
        struct_def: StructureDefinition (for context)
        
    Returns:
        Generated Python code as string
    """
    # Deduplicate fields by field_name (keep first occurrence)
    seen_fields = {}
    unique_metadata = []
    for meta in elements_metadata:
        if meta.field_name not in seen_fields:
            seen_fields[meta.field_name] = True
            unique_metadata.append(meta)
    elements_metadata = unique_metadata
    
    # Update field types based on element definitions
    for meta in elements_metadata:
        if meta.original_element:
            is_list = meta.is_list
            is_optional = not meta.is_required
            type_mapping = map_fhir_type_to_python(
                meta.original_element,
                is_list=is_list,
                is_optional=is_optional
            )
            meta.field_type = type_mapping.python_type
    
    # Sort fields: required fields first, then optional fields
    required_fields = [meta for meta in elements_metadata if meta.is_required]
    optional_fields = [meta for meta in elements_metadata if not meta.is_required]
    sorted_metadata = required_fields + optional_fields
    
    # Generate fields
    fields = []
    for meta in sorted_metadata:
        field_def = _generate_field_definition(meta)
        fields.append(f"    {field_def}")
    
    # Generate docstring
    docstring = f"    \"\"\"\n    {class_name} nested class.\n    \"\"\""
    
    class_code = f"""@dataclass
class {class_name}:
{docstring}

{chr(10).join(fields)}
"""
    return class_code


def _generate_class_code(
    resource_name: str,
    base_class: str,
    elements_metadata: List[ElementMetadata],
    docstring: str
) -> str:
    """
    Generate the main resource class code.
    
    Args:
        resource_name: Name of the resource
        base_class: Base class name
        elements_metadata: Metadata for fields
        docstring: Class docstring
        
    Returns:
        Generated class code
    """
    # Deduplicate fields by field_name (keep first occurrence)
    seen_fields = {}
    unique_metadata = []
    for meta in elements_metadata:
        if meta.field_name not in seen_fields:
            seen_fields[meta.field_name] = True
            unique_metadata.append(meta)
    elements_metadata = unique_metadata
    
    # Update field types based on element definitions
    for meta in elements_metadata:
        if meta.original_element:
            is_list = meta.is_list
            is_optional = not meta.is_required
            type_mapping = map_fhir_type_to_python(
                meta.original_element,
                is_list=is_list,
                is_optional=is_optional
            )
            meta.field_type = type_mapping.python_type
    
    # Sort fields: required fields first, then optional fields
    required_fields = [meta for meta in elements_metadata if meta.is_required]
    optional_fields = [meta for meta in elements_metadata if not meta.is_required]
    sorted_metadata = required_fields + optional_fields
    
    # Generate resourceType field (has default, so goes after required fields)
    resource_type_field = f'    resourceType: str = "{resource_name}"'
    
    # Generate fields: required first, then resourceType, then optional
    fields = []
    for meta in required_fields:
        field_def = _generate_field_definition(meta)
        fields.append(f"    {field_def}")
    fields.append(resource_type_field)
    for meta in optional_fields:
        field_def = _generate_field_definition(meta)
        fields.append(f"    {field_def}")
    
    class_code = f"""@dataclass
class {resource_name}({base_class}):
    \"\"\"
    {docstring}
    \"\"\"

{chr(10).join(fields)}
"""
    return class_code


def _generate_field_definition(meta: ElementMetadata) -> str:
    """
    Generate a field definition line.
    
    Args:
        meta: Element metadata
        
    Returns:
        Field definition string
    """
    field_name = meta.field_name
    field_type = meta.field_type
    
    # Generate default value
    if meta.is_list:
        default = "= field(default_factory=list)"
    elif meta.is_required:
        # Required field - but since we inherit from base class with defaults,
        # we need to provide a default to avoid dataclass ordering issues
        # Make it Optional with None default (FHIR spec required but can be None in practice)
        if not field_type.startswith("Optional["):
            field_type = f"Optional[{field_type}]"
        default = "= None"
    else:
        # Optional field
        if meta.default_value:
            default = f"= {meta.default_value}"
        else:
            default = "= None"
    
    # Generate docstring if available
    docstring = ""
    if meta.docstring:
        # Clean up docstring for use in code
        clean_doc = meta.docstring.replace('"', '\\"').replace("\n", " ").strip()
        # Remove any trailing ellipsis or incomplete sentences
        if clean_doc.endswith("..."):
            clean_doc = clean_doc[:-3].strip()
        # Remove any standalone "The" or incomplete words at the end
        if clean_doc.endswith(" The") or clean_doc.endswith(" The..."):
            clean_doc = clean_doc.replace(" The", "").replace(" The...", "").strip()
        # Truncate if too long
        if len(clean_doc) > 100:
            # Try to truncate at a word boundary
            truncated = clean_doc[:97]
            last_space = truncated.rfind(" ")
            if last_space > 80:
                clean_doc = truncated[:last_space] + "..."
            else:
                clean_doc = truncated + "..."
        docstring = f'  # {clean_doc}'
    
    if default:
        return f"{field_name}: {field_type} {default}{docstring}"
    else:
        return f"{field_name}: {field_type}{docstring}"


def _generate_docstring(struct_def: StructureDefinition) -> str:
    """
    Generate docstring for the resource class.
    
    Args:
        struct_def: StructureDefinition
        
    Returns:
        Docstring text
    """
    if struct_def.description:
        return struct_def.description
    elif struct_def.title:
        return struct_def.title
    else:
        return f"FHIR R5 {struct_def.type or struct_def.id} resource."
