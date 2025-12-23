# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R5 Code Generator Module.

This module provides tools for generating Python resource classes from
FHIR R5 StructureDefinition profile JSON files.

The generator consists of:
- profile_parser: Parses StructureDefinition JSON files
- element_analyzer: Analyzes element definitions and constraints
- type_mapper: Maps FHIR types to Python types
- code_generator: Generates Python dataclass code
- resource_generator: Orchestrates resource generation
"""

# Import profile_parser (always available)
from dnhealth.dnhealth_fhir.r5_generator.profile_parser import (
    parse_profile,
    StructureDefinition,
    ElementDefinition,
)

__all__ = [
    "parse_profile",
    "StructureDefinition",
    "ElementDefinition",
]

# Conditionally import other modules as they become available
try:
    from dnhealth.dnhealth_fhir.r5_generator.element_analyzer import (
        analyze_elements,
        ElementMetadata,
    )
    __all__.extend(["analyze_elements", "ElementMetadata"])
except ImportError:
    pass

try:
    from dnhealth.dnhealth_fhir.r5_generator.type_mapper import (
        map_fhir_type_to_python,
        TypeMapping,
    )
    __all__.extend(["map_fhir_type_to_python", "TypeMapping"])
except ImportError:
    pass

try:
    from dnhealth.dnhealth_fhir.r5_generator.code_generator import (
        generate_resource_code,
        generate_nested_class_code,
    )
    __all__.extend(["generate_resource_code", "generate_nested_class_code"])
except ImportError:
    pass

try:
    from dnhealth.dnhealth_fhir.r5_generator.resource_generator import (
        generate_all_resources,
        generate_resource_from_profile,
    )
    __all__.extend(["generate_all_resources", "generate_resource_from_profile"])
except ImportError:
    pass
