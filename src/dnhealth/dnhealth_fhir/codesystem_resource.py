# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CodeSystem resource parser and support.

CodeSystem defines a set of codes from a single code system.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept, Identifier, ContactDetail, UsageContext

logger = logging.getLogger(__name__)


@dataclass
class CodeSystemConceptDesignation:
    """
    FHIR CodeSystem.concept.designation complex type.
    
    Represents a designation (display name) for a concept.
    """
    
    language: Optional[str] = None
    use: Optional[Coding] = None
    value: Optional[str] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class CodeSystemConceptProperty:
    """
    FHIR CodeSystem.concept.property complex type.
    
    Represents a property of a concept.
    """
    
    code: Optional[str] = None
    valueCode: Optional[str] = None
    valueCoding: Optional[Coding] = None
    valueString: Optional[str] = None
    valueInteger: Optional[int] = None
    valueBoolean: Optional[bool] = None
    valueDateTime: Optional[str] = None
    valueDecimal: Optional[float] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class CodeSystemConcept:
    """
    FHIR CodeSystem.concept complex type.
    
    Represents a concept (code) in a code system.
    """
    
    code: Optional[str] = None
    display: Optional[str] = None
    definition: Optional[str] = None
    designation: List[CodeSystemConceptDesignation] = field(default_factory=list)
    property: List[CodeSystemConceptProperty] = field(default_factory=list)
    concept: List["CodeSystemConcept"] = field(default_factory=list)  # Nested concepts
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class CodeSystemFilter:
    """
    FHIR CodeSystem.filter complex type.
    
    Represents a filter that can be used in a value set.
    """
    
    code: Optional[str] = None
    description: Optional[str] = None
    operator: List[str] = field(default_factory=list)  # =, is-a, descendent-of, is-not-a, regex, in, not-in, generalizes, exists
    value: Optional[str] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class CodeSystemProperty:
    """
    FHIR CodeSystem.property complex type.
    
    Represents a property definition for concepts in the code system.
    """
    
    code: Optional[str] = None
    uri: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None  # code, Coding, string, integer, boolean, dateTime, decimal
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class CodeSystem(FHIRResource):
    """
    FHIR R4 CodeSystem resource.
    
    Defines a set of codes from a single code system.
    """
    
    resourceType: str = "CodeSystem"
    url: Optional[str] = None
    identifier: List[Identifier] = field(default_factory=list)
    version: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None  # draft, active, retired, unknown
    experimental: Optional[bool] = None
    date: Optional[str] = None
    publisher: Optional[str] = None
    contact: List[ContactDetail] = field(default_factory=list)
    description: Optional[str] = None
    useContext: List[UsageContext] = field(default_factory=list)
    jurisdiction: List[CodeableConcept] = field(default_factory=list)
    purpose: Optional[str] = None
    copyright: Optional[str] = None
    caseSensitive: Optional[bool] = None
    valueSet: Optional[str] = None  # Canonical URL of the value set
    hierarchyMeaning: Optional[str] = None  # grouped-by, is-a, part-of, classified-with
    compositional: Optional[bool] = None
    versionNeeded: Optional[bool] = None
    content: Optional[str] = None  # not-present, example, fragment, complete, supplement
    supplements: Optional[str] = None  # Canonical URL of another code system
    count: Optional[int] = None
    filter: List[CodeSystemFilter] = field(default_factory=list)
    property: List[CodeSystemProperty] = field(default_factory=list)
    concept: List[CodeSystemConcept] = field(default_factory=list)
    # For unknown extensions and fields
    _unknown_fields: Dict[str, Any] = field(default_factory=dict)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def parse_codesystem_json(json_data: Dict[str, Any]) -> CodeSystem:
    """
    Parse a CodeSystem from JSON data.
    
    Args:
        json_data: JSON dictionary containing CodeSystem data
        
    Returns:
        CodeSystem object
    """
    import json
    from dnhealth.dnhealth_fhir.parser_json import parse_fhir_json
    
    # Convert dict to JSON string, then parse
    json_str = json.dumps(json_data)
    result = parse_fhir_json(json_str, CodeSystem)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] CodeSystem JSON parsing completed")
    
    return result


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

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] CodeSystem code extraction completed ({len(codes)} codes extracted)")
    
    return codes


def _extract_codes_from_concept(concept: CodeSystemConcept, codes: Set[str]) -> None:
    """
    Recursively extract codes from a concept and its nested concepts.
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    Args:
        concept: CodeSystemConcept object
        codes: Set to add codes to
    """
    if concept.code:
        codes.add(concept.code)
    
    # Recursively process nested concepts
    for nested_concept in concept.concept:
        _extract_codes_from_concept(nested_concept, codes)


def get_code_system_by_url(codesystems: List[CodeSystem], url: str) -> Optional[CodeSystem]:
    """
    Get a CodeSystem by URL from a list of CodeSystems.
    
    Args:
        codesystems: List of CodeSystem resources
        url: CodeSystem URL
        
    Returns:
        CodeSystem or None if not found
    """
    for cs in codesystems:
        if cs.url == url:
            return cs
    return None


def get_concept_by_code(codesystem: CodeSystem, code: str) -> Optional[CodeSystemConcept]:
    """
    Find a concept by code in a CodeSystem.
    
    Args:
        codesystem: CodeSystem resource
        code: Code to find
        
    Returns:
        CodeSystemConcept or None if not found
    """
    for concept in codesystem.concept:
        found = _find_concept_in_concept(concept, code)
        if found:
            return found
    return None


def _find_concept_in_concept(concept: CodeSystemConcept, code: str) -> Optional[CodeSystemConcept]:
    """
    Recursively find a concept by code.
    
    Args:
        concept: CodeSystemConcept to search in
        code: Code to find
        
    Returns:
        CodeSystemConcept or None if not found
    """
    if concept.code == code:
        return concept
    
    # Search nested concepts
    for nested_concept in concept.concept:
        found = _find_concept_in_concept(nested_concept, code)
        if found:
            return found
    
    return None

