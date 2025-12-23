# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ValueSet resource.

ValueSet defines a set of codes from one or more code systems.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Set

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    ContactDetail,
    UsageContext,
)


@dataclass
class ValueSetComposeIncludeConcept:
    """
    FHIR ValueSet.compose.include.concept complex type.
    
    Represents a concept in a value set.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    display: Optional[str] = None
    designation: List[Any] = field(default_factory=list)


@dataclass
class ValueSetComposeIncludeFilter:
    """
    FHIR ValueSet.compose.include.filter complex type.
    
    Represents a filter for including codes.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    property: Optional[str] = None  # property name
    op: Optional[str] = None  # operator: =, is-a, descendent-of, is-not-a, regex, in, not-in, generalizes, exists
    value: Optional[str] = None


@dataclass
class ValueSetComposeInclude:
    """
    FHIR ValueSet.compose.include complex type.
    
    Represents a set of codes from a code system.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    system: Optional[str] = None
    version: Optional[str] = None
    concept: List[ValueSetComposeIncludeConcept] = field(default_factory=list)
    filter: List[ValueSetComposeIncludeFilter] = field(default_factory=list)
    valueSet: List[str] = field(default_factory=list)  # List of ValueSet URLs


@dataclass
class ValueSetCompose:
    """
    FHIR ValueSet.compose complex type.
    
    Defines the composition of a value set.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    lockedDate: Optional[str] = None
    inactive: Optional[bool] = None
    include: List[ValueSetComposeInclude] = field(default_factory=list)
    exclude: List[ValueSetComposeInclude] = field(default_factory=list)


@dataclass
class ValueSetExpansionContains:
    """
    FHIR ValueSet.expansion.contains complex type.
    
    Represents a code in an expanded value set.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    system: Optional[str] = None
    abstract: Optional[bool] = None
    inactive: Optional[bool] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    designation: List[Any] = field(default_factory=list)
    contains: List["ValueSetExpansionContains"] = field(default_factory=list)  # Nested contains


@dataclass
class ValueSetExpansionParameter:
    """
    FHIR ValueSet.expansion.parameter complex type.
    
    Represents a parameter used in expansion.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    name: Optional[str] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueDecimal: Optional[float] = None
    valueUri: Optional[str] = None
    valueCode: Optional[str] = None
    valueDateTime: Optional[str] = None


@dataclass
class ValueSetExpansion:
    """
    FHIR ValueSet.expansion complex type.
    
    Represents an expanded value set.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    identifier: Optional[str] = None
    timestamp: Optional[str] = None
    total: Optional[int] = None
    offset: Optional[int] = None
    parameter: List[ValueSetExpansionParameter] = field(default_factory=list)
    contains: List[ValueSetExpansionContains] = field(default_factory=list)


@dataclass
class ValueSet(MetadataResource):
    """
    FHIR R4 ValueSet resource.
    
    Defines a set of codes from one or more code systems.
    Extends MetadataResource.
    """
    
    resourceType: str = "ValueSet"
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
    # Immutable
    immutable: Optional[bool] = None  # Whether the value set is locked
    # Compose
    compose: Optional[ValueSetCompose] = None  # Content logical definition
    # Expansion
    expansion: Optional[ValueSetExpansion] = None  # Used when the value set is "expanded"


def get_codes_from_valueset(valueset: ValueSet) -> Set[str]:
    """
    Extract all codes from a ValueSet.
    
    Args:
        valueset: ValueSet resource
        
    Returns:
        Set of code strings
    """
    codes: Set[str] = set()
    
    # Extract codes from compose.include
    if valueset.compose:
        for include in valueset.compose.include:
            for concept in include.concept:
                if concept.code:
                    codes.add(concept.code)
    
    # Extract codes from expansion.contains
    if valueset.expansion:
        _extract_codes_from_expansion(valueset.expansion, codes)
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return codes


def _extract_codes_from_expansion(expansion: ValueSetExpansion, codes: Set[str]) -> None:
    """
    Recursively extract codes from expansion.contains.
    
    Args:
        expansion: Optional[ValueSetExpansion object] = None
        codes: Optional[Set to add codes to] = None
    """
    for contains in expansion.contains:
        if contains.code:
            codes.add(contains.code)
        # Recursively process nested contains
        if contains.contains:
            _extract_codes_from_expansion_nested(contains.contains, codes)


def _extract_codes_from_expansion_nested(contains_list: List[ValueSetExpansionContains], codes: Set[str]) -> None:
    """
    Recursively extract codes from nested contains lists.
    
    Args:
        contains_list: Optional[List of ValueSetExpansionContains objects] = None
        codes: Optional[Set to add codes to] = None
    """
    for contains in contains_list:
        if contains.code:
            codes.add(contains.code)
        if contains.contains:
            _extract_codes_from_expansion_nested(contains.contains, codes)
