# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Type Mapper for FHIR R5 to Python types.

Maps FHIR data types to Python types and generates appropriate
type hints and import statements.
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

from dnhealth.dnhealth_fhir.r5_generator.profile_parser import TypeDefinition, ElementDefinition


@dataclass
class TypeMapping:
    """
    Type mapping result.
    
    Contains the Python type string and required imports.
    """
    
    python_type: str  # Python type string (e.g., "Optional[str]", "List[Reference]")
    imports: Set[str]  # Set of import statements needed
    is_primitive: bool  # Whether this is a primitive type
    is_list: bool  # Whether this is a list type
    is_optional: bool  # Whether this is optional


# Mapping of FHIR primitive types to Python types
FHIR_PRIMITIVE_TO_PYTHON: Dict[str, str] = {
    "string": "str",
    "code": "str",
    "id": "str",
    "uri": "str",
    "url": "str",
    "canonical": "str",
    "base64Binary": "str",
    "integer": "int",
    "positiveInt": "int",
    "unsignedInt": "int",
    "decimal": "float",
    "boolean": "bool",
    "date": "str",  # ISO date format
    "dateTime": "str",  # ISO datetime format
    "time": "str",  # ISO time format
    "instant": "str",  # ISO instant format
    "markdown": "str",
    "xhtml": "str",
    "oid": "str",
    "uuid": "str",
}

# Mapping of FHIR complex types to Python imports
# These types are available in dnhealth.dnhealth_fhir.types
FHIR_COMPLEX_TYPES: Dict[str, str] = {
    "Extension": "Extension",
    "Narrative": "Narrative",
    "Identifier": "Identifier",
    "HumanName": "HumanName",
    "ContactPoint": "ContactPoint",
    "Address": "Address",
    "Reference": "Reference",
    "Attachment": "Attachment",
    "CodeableConcept": "CodeableConcept",
    "Coding": "Coding",
    "Period": "Period",
    "Quantity": "Quantity",
    "Range": "Range",
    "Ratio": "Ratio",
    "SampledData": "SampledData",
    "Timing": "Timing",
    "Annotation": "Annotation",
    "Age": "Age",
    "Distance": "Distance",
    "Duration": "Duration",
    "Count": "Count",
    "Money": "Money",
    "Signature": "Signature",
    "ContactDetail": "ContactDetail",
    "Contributor": "Contributor",
    "DataRequirement": "DataRequirement",
    "Expression": "Expression",
    "ParameterDefinition": "ParameterDefinition",
    "RelatedArtifact": "RelatedArtifact",
    "TriggerDefinition": "TriggerDefinition",
    "UsageContext": "UsageContext",
    "Dosage": "Dosage",
    "Meta": "Meta",
    "Element": "Element",
    "BackboneElement": "BackboneElement",
    "Resource": "Resource",
    "DomainResource": "DomainResource",
}

# Special handling for types that need special imports
SPECIAL_TYPE_IMPORTS: Dict[str, str] = {
    "Meta": "from dnhealth.dnhealth_fhir.resources.base import Meta",
    "Resource": "from dnhealth.dnhealth_fhir.resources.base import Resource",
    "DomainResource": "from dnhealth.dnhealth_fhir.resources.base import DomainResource",
    "FHIRResource": "from dnhealth.dnhealth_fhir.resources.base import FHIRResource",
}


def map_fhir_type_to_python(
    element: ElementDefinition,
    is_list: bool = False,
    is_optional: bool = True
) -> TypeMapping:
    """
    Map a FHIR element definition to Python type.
    
    Args:
        element: Element definition
        is_list: Whether this is a list type
        is_optional: Whether this is optional
        
    Returns:
        TypeMapping with Python type and imports
    """
    types = element.types
    imports: Set[str] = set()
    python_type_str: str = "Any"
    is_primitive = False
    
    if not types:
        # No type information, use Any
        python_type_str = "Any"
        imports.add("from typing import Any")
    elif len(types) == 1:
        # Single type
        type_def = types[0]
        python_type_str, type_imports, is_primitive = _map_single_type(type_def)
        imports.update(type_imports)
    else:
        # Multiple types - use Union (or Any for simplicity)
        # For now, we'll use Any, but could use Union[Type1, Type2, ...]
        python_type_str = "Any"
        imports.add("from typing import Any")
        # Could also collect all types and create Union
        for type_def in types:
            _, type_imports, _ = _map_single_type(type_def)
            imports.update(type_imports)
    
    # Wrap in List if needed
    if is_list:
        python_type_str = f"List[{python_type_str}]"
        imports.add("from typing import List")
    
    # Wrap in Optional if needed
    if is_optional:
        python_type_str = f"Optional[{python_type_str}]"
        imports.add("from typing import Optional")
    
    return TypeMapping(
        python_type=python_type_str,
        imports=imports,
        is_primitive=is_primitive,
        is_list=is_list,
        is_optional=is_optional,
    )


def _map_single_type(type_def: TypeDefinition) -> Tuple[str, Set[str], bool]:
    """
    Map a single FHIR type definition to Python type.
    
    Args:
        type_def: Type definition
        
    Returns:
        Tuple of (python_type_str, imports_set, is_primitive)
    """
    type_code = type_def.code
    
    # Handle special cases - FHIRPath system types
    if type_code.startswith("http://hl7.org/fhirpath/System."):
        # FHIRPath system types - extract the base type
        base_type = type_code.split(".")[-1]
        # Map common FHIRPath system types to Python
        if base_type == "String":
            return "str", set(), True
        elif base_type == "Integer":
            return "int", set(), True
        elif base_type == "Decimal":
            return "float", set(), True
        elif base_type == "Boolean":
            return "bool", set(), True
        elif base_type in FHIR_PRIMITIVE_TO_PYTHON:
            return FHIR_PRIMITIVE_TO_PYTHON[base_type], set(), True
        else:
            # Unknown FHIRPath system type, default to str
            return "str", set(), True
    
    # Check if primitive
    if type_code in FHIR_PRIMITIVE_TO_PYTHON:
        return FHIR_PRIMITIVE_TO_PYTHON[type_code], set(), True
    
    # Check if complex type from types module
    if type_code in FHIR_COMPLEX_TYPES:
        type_name = FHIR_COMPLEX_TYPES[type_code]
        if type_code in SPECIAL_TYPE_IMPORTS:
            import_stmt = SPECIAL_TYPE_IMPORTS[type_code]
        else:
            import_stmt = f"from dnhealth.dnhealth_fhir.types import {type_name}"
        return type_name, {import_stmt}, False
    
    # Check if it's a Reference type
    if type_code == "Reference":
        imports = {"from dnhealth.dnhealth_fhir.types import Reference"}
        # If there are target profiles, we could add them as comments
        return "Reference", imports, False
    
    # Check if it's a nested resource type (e.g., "Patient", "Task")
    # These will be imported from resources module
    # For now, we'll use the type name directly and assume it's imported
    # The resource generator will handle proper imports
    
    # Default: use Any for unknown types (safer than using raw type_code)
    return "Any", {"from typing import Any"}, False


def get_all_imports_for_elements(elements: List[ElementDefinition]) -> Set[str]:
    """
    Get all import statements needed for a list of elements.
    
    Args:
        elements: List of element definitions
        
    Returns:
        Set of import statements
    """
    all_imports: Set[str] = set()
    
    for element in elements:
        is_list = element.max == "*" or (element.max.isdigit() and int(element.max) > 1)
        is_optional = element.min == 0
        
        type_mapping = map_fhir_type_to_python(element, is_list=is_list, is_optional=is_optional)
        all_imports.update(type_mapping.imports)
    
    return all_imports


def format_imports(imports: Set[str]) -> str:
    """
    Format import statements as a string, deduplicating and grouping imports.
    
    Args:
        imports: Set of import statements
        
    Returns:
        Formatted import string with deduplicated imports
    """
    # Group imports by module to avoid duplicates
    from_imports: Dict[str, Set[str]] = {}  # module -> set of names
    other_imports: List[str] = []  # Other import types (e.g., "import X")
    
    for imp in imports:
        if imp.startswith("from "):
            # Parse "from module import name" or "from module import name1, name2"
            parts = imp.split(" import ", 1)
            if len(parts) == 2:
                module = parts[0].replace("from ", "").strip()
                names_str = parts[1].strip()
                # Handle multiple names: "name1, name2"
                names = [n.strip() for n in names_str.split(",")]
                
                if module not in from_imports:
                    from_imports[module] = set()
                from_imports[module].update(names)
            else:
                other_imports.append(imp)
        else:
            other_imports.append(imp)
    
    # Build import lines
    import_lines = []
    
    # Format grouped imports: "from module import name1, name2"
    for module in sorted(from_imports.keys()):
        names = sorted(from_imports[module])
        if len(names) == 1:
            import_lines.append(f"from {module} import {names[0]}")
        else:
            # Single line format: "from module import name1, name2, name3"
            import_lines.append(f"from {module} import {', '.join(names)}")
    
    # Add other imports
    import_lines.extend(sorted(other_imports))
    
    return "\n".join(import_lines)
