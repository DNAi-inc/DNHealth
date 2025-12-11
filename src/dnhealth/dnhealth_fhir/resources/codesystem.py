# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CodeSystem resource.

CodeSystem defines a set of codes from a single code system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Set

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    ContactDetail,
    UsageContext,
    Coding,
)


@dataclass
class CodeSystemConceptDesignation:
    """
    FHIR CodeSystem.concept.designation complex type.
    
    Represents a designation (display name) for a concept.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    language: Optional[str] = None
    use: Optional[Coding] = None
    value: Optional[str] = None


@dataclass
class CodeSystemConceptProperty:
    """
    FHIR CodeSystem.concept.property complex type.
    
    Represents a property of a concept.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    valueCode: Optional[str] = None
    valueCoding: Optional[Coding] = None
    valueString: Optional[str] = None
    valueInteger: Optional[int] = None
    valueBoolean: Optional[bool] = None
    valueDateTime: Optional[str] = None
    valueDecimal: Optional[float] = None


@dataclass
class CodeSystemConcept:
    """
    FHIR CodeSystem.concept complex type.
    
    Represents a concept (code) in a code system.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    display: Optional[str] = None
    definition: Optional[str] = None
    designation: List[CodeSystemConceptDesignation] = field(default_factory=list)
    property: List[CodeSystemConceptProperty] = field(default_factory=list)
    concept: List["CodeSystemConcept"] = field(default_factory=list)  # Nested concepts


@dataclass
class CodeSystemFilter:
    """
    FHIR CodeSystem.filter complex type.
    
    Represents a filter that can be used in a value set.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    description: Optional[str] = None
    operator: List[str] = field(default_factory=list)  # =, is-a, descendent-of, is-not-a, regex, in, not-in, generalizes, exists
    value: Optional[str] = None


@dataclass
class CodeSystemProperty:
    """
    FHIR CodeSystem.property complex type.
    
    Represents a property definition for concepts in the code system.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    uri: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None  # code, Coding, string, integer, boolean, dateTime, decimal


@dataclass
class CodeSystem(MetadataResource):
    """
    FHIR R4 CodeSystem resource.
    
    Defines a set of codes from a single code system.
    Extends MetadataResource.
    """
    
    resourceType: str = "CodeSystem"
    # URL (inherited from CanonicalResource)
    url: Optional[str] = None
    # Identifier (inherited from CanonicalResource)
    identifier: List[Identifier] = field(default_factory=list)
    # Version (inherited from CanonicalResource)
    version: Optional[str] = None
    # Name (inherited from CanonicalResource)
    name: Optional[str] = None
    # Title (inherited from CanonicalResource)
    title: Optional[str] = None
    # Status (inherited from CanonicalResource)
    status: Optional[str] = None  # draft, active, retired, unknown
    # Experimental (inherited from CanonicalResource)
    experimental: Optional[bool] = None
    # Date (inherited from CanonicalResource)
    date: Optional[str] = None
    # Publisher (inherited from CanonicalResource)
    publisher: Optional[str] = None
    # Contact (inherited from CanonicalResource)
    contact: List[ContactDetail] = field(default_factory=list)
    # Description (inherited from CanonicalResource)
    description: Optional[str] = None
    # Use Context (inherited from CanonicalResource)
    useContext: List[UsageContext] = field(default_factory=list)
    # Jurisdiction (inherited from CanonicalResource)
    jurisdiction: List[CodeableConcept] = field(default_factory=list)
    # Purpose (inherited from CanonicalResource)
    purpose: Optional[str] = None
    # Copyright (inherited from CanonicalResource)
    copyright: Optional[str] = None
    # Case Sensitive
    caseSensitive: Optional[bool] = None
    # Value Set
    valueSet: Optional[str] = None  # Canonical URL of the value set
    # Hierarchy Meaning
    hierarchyMeaning: Optional[str] = None  # grouped-by, is-a, part-of, classified-with
    # Compositional
    compositional: Optional[bool] = None
    # Version Needed
    versionNeeded: Optional[bool] = None
    # Content
    content: Optional[str] = None  # not-present, example, fragment, complete, supplement
    # Supplements
    supplements: Optional[str] = None  # Canonical URL of another code system
    # Count
    count: Optional[int] = None
    # Filter
    filter: List[CodeSystemFilter] = field(default_factory=list)
    # Property
    property: List[CodeSystemProperty] = field(default_factory=list)
    # Concept
    concept: List[CodeSystemConcept] = field(default_factory=list)


def get_codes_from_codesystem(codesystem: CodeSystem) -> Set[str]:
    """
    Extract all codes from a CodeSystem.
    
    Args:
        codesystem: CodeSystem resource
        
    Returns:
        Set of code strings
    """
    codes: Set[str] = set()
    
    # Extract codes from concept list (including nested)
    for concept in codesystem.concept:
        _extract_codes_from_concept(concept, codes)
    
    # Log completion timestamp at end of operation
    from datetime import datetime
    import logging
    logger = logging.getLogger(__name__)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return codes


def _extract_codes_from_concept(concept: CodeSystemConcept, codes: Set[str]) -> None:
    """
    Recursively extract codes from a concept and its nested concepts.
    
    Args:
        concept: CodeSystemConcept object
        codes: Set to add codes to
    """
    if concept.code:
        codes.add(concept.code)
    
    # Recursively process nested concepts
    for nested_concept in concept.concept:
        _extract_codes_from_concept(nested_concept, codes)
