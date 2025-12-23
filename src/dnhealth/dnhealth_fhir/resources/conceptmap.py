# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ConceptMap resource.

ConceptMap defines mappings between codes from different code systems.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Tuple

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
class ConceptMapGroupElementTargetDependsOn:
    """
    FHIR ConceptMap.group.element.target.dependsOn complex type.
    
    Represents a dependency for a target element.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    property: Optional[str] = None  # Property identifier
    system: Optional[str] = None  # Code system (if canonical URL)
    value: Optional[str] = None  # Value of the property
    display: Optional[str] = None  # Display for the value


@dataclass
class ConceptMapGroupElementTarget:
    """
    FHIR ConceptMap.group.element.target complex type.
    
    Represents a target concept in a concept map.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    display: Optional[str] = None
    equivalence: Optional[str] = None  # related-to, equivalent, wider, narrower, specializes, generalizes, inexact, unmatched, disjoint
    comment: Optional[str] = None
    dependsOn: List[ConceptMapGroupElementTargetDependsOn] = field(default_factory=list)
    product: List[ConceptMapGroupElementTargetDependsOn] = field(default_factory=list)


@dataclass
class ConceptMapGroupElement:
    """
    FHIR ConceptMap.group.element complex type.
    
    Represents a source concept and its mappings.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[str] = None
    display: Optional[str] = None
    target: List[ConceptMapGroupElementTarget] = field(default_factory=list)


@dataclass
class ConceptMapGroupUnmapped:
    """
    FHIR ConceptMap.group.unmapped complex type.
    
    Defines what to do when a source concept has no mapping.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    mode: Optional[str] = None  # provided, fixed, other-map
    code: Optional[str] = None
    display: Optional[str] = None
    url: Optional[str] = None  # Canonical URL of another concept map
    comment: Optional[str] = None


@dataclass
class ConceptMapGroup:
    """
    FHIR ConceptMap.group complex type.
    
    Represents a group of mappings between source and target code systems.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    source: Optional[str] = None  # Canonical URL of source code system
    sourceVersion: Optional[str] = None
    target: Optional[str] = None  # Canonical URL of target code system
    targetVersion: Optional[str] = None
    element: List[ConceptMapGroupElement] = field(default_factory=list)
    unmapped: Optional[ConceptMapGroupUnmapped] = None


@dataclass
class ConceptMap(MetadataResource):
    """
    FHIR R4 ConceptMap resource.
    
    Defines mappings between codes from different code systems.
    Extends MetadataResource.
    """
    
    resourceType: str = "ConceptMap"
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
    # Source URI
    sourceUri: Optional[str] = None  # Canonical URL of source ValueSet
    # Source Canonical
    sourceCanonical: Optional[str] = None  # Canonical URL of source ValueSet
    # Target URI
    targetUri: Optional[str] = None  # Canonical URL of target ValueSet
    # Target Canonical
    targetCanonical: Optional[str] = None  # Canonical URL of target ValueSet
    # Group
    group: List[ConceptMapGroup] = field(default_factory=list)


def translate_code(
    concept_map: ConceptMap,
    source_code: str,
    source_system: Optional[str] = None,
    target_system: Optional[str] = None
) -> List[Tuple[str, str, str]]:
    """
    Translate a code using a ConceptMap.
    
    Args:
        concept_map: Optional[ConceptMap resource] = None
        source_code: Optional[Source code to translate] = None
        source_system: Optional[Optional source code system URL (if None, uses first group's source)] = None
        target_system: Optional[Optional target code system URL (if None, uses first group's target)] = None
        
    Returns: Optional[] = None
        List of tuples (target_code, target_system, equivalence) for each mapping found
    """
    translations = []
    
    for group in concept_map.group:
        # Check if source system matches
        if source_system and group.source != source_system:
            continue
        
        # Check if target system matches (if specified)
        if target_system and group.target != target_system:
            continue
        
        # Find element with matching code
        for element in group.element:
            if element.code == source_code:
                # Get all target mappings
                for target in element.target:
                    translations.append((
                        target.code or "",
                        group.target or "",
                        target.equivalence or "related-to"
                    ))
        
        # If no mapping found and unmapped is defined, handle it
        if not translations and group.unmapped:
            if group.unmapped.mode == "fixed" and group.unmapped.code:
                translations.append((
                    group.unmapped.code,
                    group.target or "",
                    "unmapped"
                ))
    
    # Log completion timestamp at end of operation
    from datetime import datetime
    import logging
    logger = logging.getLogger(__name__)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return translations
