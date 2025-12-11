# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ValueSet resource parser and support.

ValueSet defines a set of codes from one or more code systems.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept, Identifier, ContactDetail, UsageContext

logger = logging.getLogger(__name__)


@dataclass
class ValueSetComposeIncludeConcept:
    """
    FHIR ValueSet.compose.include.concept complex type.
    
    Represents a concept in a value set.
    """
    
    code: Optional[str] = None
    display: Optional[str] = None
    designation: List[Dict[str, Any]] = field(default_factory=list)
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSetComposeIncludeFilter:
    """
    FHIR ValueSet.compose.include.filter complex type.
    
    Represents a filter for including codes.
    """
    
    property: Optional[str] = None  # property name
    op: Optional[str] = None  # operator: =, is-a, descendent-of, is-not-a, regex, in, not-in, generalizes, exists
    value: Optional[str] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSetComposeInclude:
    """
    FHIR ValueSet.compose.include complex type.
    
    Represents a set of codes from a code system.
    """
    
    system: Optional[str] = None
    version: Optional[str] = None
    concept: List[ValueSetComposeIncludeConcept] = field(default_factory=list)
    filter: List[ValueSetComposeIncludeFilter] = field(default_factory=list)
    valueSet: List[str] = field(default_factory=list)  # List of ValueSet URLs
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSetCompose:
    """
    FHIR ValueSet.compose complex type.
    
    Defines the composition of a value set.
    """
    
    lockedDate: Optional[str] = None
    inactive: Optional[bool] = None
    include: List[ValueSetComposeInclude] = field(default_factory=list)
    exclude: List[ValueSetComposeInclude] = field(default_factory=list)
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSetExpansionContains:
    """
    FHIR ValueSet.expansion.contains complex type.
    
    Represents a code in an expanded value set.
    """
    
    system: Optional[str] = None
    abstract: Optional[bool] = None
    inactive: Optional[bool] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    designation: List[Dict[str, Any]] = field(default_factory=list)
    contains: List["ValueSetExpansionContains"] = field(default_factory=list)  # Nested contains
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSetExpansionParameter:
    """
    FHIR ValueSet.expansion.parameter complex type.
    
    Represents a parameter used in expansion.
    """
    
    name: Optional[str] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueDecimal: Optional[float] = None
    valueUri: Optional[str] = None
    valueCode: Optional[str] = None
    valueDateTime: Optional[str] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSetExpansion:
    """
    FHIR ValueSet.expansion complex type.
    
    Represents an expanded value set.
    """
    
    identifier: Optional[str] = None
    timestamp: Optional[str] = None
    total: Optional[int] = None
    offset: Optional[int] = None
    parameter: List[ValueSetExpansionParameter] = field(default_factory=list)
    contains: List[ValueSetExpansionContains] = field(default_factory=list)
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ValueSet(FHIRResource):
    """
    FHIR R4 ValueSet resource.
    
    Defines a set of codes from one or more code systems.
    """
    
    resourceType: str = "ValueSet"
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
    immutable: Optional[bool] = None
    purpose: Optional[str] = None
    copyright: Optional[str] = None
    compose: Optional[ValueSetCompose] = None
    expansion: Optional[ValueSetExpansion] = None
    # For unknown extensions and fields
    _unknown_fields: Dict[str, Any] = field(default_factory=dict)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def parse_valueset_json(json_data: Dict[str, Any]) -> ValueSet:
    """
    Parse a ValueSet from JSON data.
    
    Args:
        json_data: JSON dictionary containing ValueSet data
        
    Returns:
        ValueSet object
    """
    import json
    from dnhealth.dnhealth_fhir.parser_json import parse_fhir_json
    
    # Convert dict to JSON string, then parse
    json_str = json.dumps(json_data)
    result = parse_fhir_json(json_str, ValueSet)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] ValueSet JSON parsing completed")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    return result


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
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] ValueSet code extraction completed ({len(codes)} codes extracted)")
    
    return codes


def _extract_codes_from_expansion(expansion: ValueSetExpansion, codes: Set[str]) -> None:
    """
    Recursively extract codes from expansion.contains.
    
    Args:
        expansion: ValueSetExpansion object
        codes: Set to add codes to
    """
    for contains in expansion.contains:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        if contains.code:
            codes.add(contains.code)
        # Recursively process nested contains
        if contains.contains:
            for nested in contains.contains:
                if nested.code:
                    codes.add(nested.code)
                # Handle deeper nesting if needed
                if nested.contains:
                    _extract_codes_from_expansion_nested(nested.contains, codes)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def _extract_codes_from_expansion_nested(contains_list: List[ValueSetExpansionContains], codes: Set[str]) -> None:
    """
    Recursively extract codes from nested contains lists.
    
    Args:
        contains_list: List of ValueSetExpansionContains objects
        codes: Set to add codes to
    """
    for contains in contains_list:
        if contains.code:
            codes.add(contains.code)
        if contains.contains:
            _extract_codes_from_expansion_nested(contains.contains, codes)


def get_value_set_by_url(valuesets: List[ValueSet], url: str) -> Optional[ValueSet]:
    """
    Get a ValueSet by URL from a list of ValueSets.
    
    Args:
        valuesets: List of ValueSet resources
        url: ValueSet URL
        
    Returns:
        ValueSet or None if not found
    """
    for vs in valuesets:
        if vs.url == url:
            return vs
    return None

