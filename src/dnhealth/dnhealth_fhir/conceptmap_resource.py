# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ConceptMap resource parser and support.

ConceptMap defines mappings between codes from different code systems.
"""

from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept, Identifier, ContactDetail, UsageContext

logger = logging.getLogger(__name__)


@dataclass
class ConceptMapGroupElementTargetDependsOn:
    """
    FHIR ConceptMap.group.element.target.dependsOn complex type.
    
    Represents a dependency for a target element.
    """
    
    property: Optional[str] = None  # Property identifier
    system: Optional[str] = None  # Code system (if canonical URL)
    value: Optional[str] = None  # Value of the property
    display: Optional[str] = None  # Display for the value
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ConceptMapGroupElementTarget:
    """
    FHIR ConceptMap.group.element.target complex type.
    
    Represents a target concept in a concept map.
    """
    
    code: Optional[str] = None
    display: Optional[str] = None
    equivalence: Optional[str] = None  # related-to, equivalent, wider, narrower, specializes, generalizes, inexact, unmatched, disjoint
    comment: Optional[str] = None
    dependsOn: List[ConceptMapGroupElementTargetDependsOn] = field(default_factory=list)
    product: List[ConceptMapGroupElementTargetDependsOn] = field(default_factory=list)
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ConceptMapGroupElement:
    """
    FHIR ConceptMap.group.element complex type.
    
    Represents a source concept and its mappings.
    """
    
    code: Optional[str] = None
    display: Optional[str] = None
    target: List[ConceptMapGroupElementTarget] = field(default_factory=list)
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ConceptMapGroupUnmapped:
    """
    FHIR ConceptMap.group.unmapped complex type.
    
    Defines what to do when a source concept has no mapping.
    """
    
    mode: Optional[str] = None  # provided, fixed, other-map
    code: Optional[str] = None
    display: Optional[str] = None
    url: Optional[str] = None  # Canonical URL of another concept map
    comment: Optional[str] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ConceptMapGroup:
    """
    FHIR ConceptMap.group complex type.
    
    Represents a group of mappings between source and target code systems.
    """
    
    source: Optional[str] = None  # Canonical URL of source code system
    sourceVersion: Optional[str] = None
    target: Optional[str] = None  # Canonical URL of target code system
    targetVersion: Optional[str] = None
    element: List[ConceptMapGroupElement] = field(default_factory=list)
    unmapped: Optional[ConceptMapGroupUnmapped] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)


@dataclass
class ConceptMap(FHIRResource):
    """
    FHIR R4 ConceptMap resource.
    
    Defines mappings between codes from different code systems.
    """
    
    resourceType: str = "ConceptMap"
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
    sourceUri: Optional[str] = None  # Canonical URL of source ValueSet
    sourceCanonical: Optional[str] = None  # Canonical URL of source ValueSet
    targetUri: Optional[str] = None  # Canonical URL of target ValueSet
    targetCanonical: Optional[str] = None  # Canonical URL of target ValueSet
    group: List[ConceptMapGroup] = field(default_factory=list)
    # For unknown extensions and fields
    _unknown_fields: Dict[str, Any] = field(default_factory=dict)


def parse_conceptmap_json(json_data: Dict[str, Any]) -> ConceptMap:
    """
    Parse ConceptMap from JSON data.
    
    Args:
        json_data: JSON dictionary containing ConceptMap data
        
    Returns:
        ConceptMap object
    """
    # Extract group data
    groups = []
    for group_data in json_data.get("group", []):
        elements = []
        for element_data in group_data.get("element", []):
            targets = []
            for target_data in element_data.get("target", []):
                depends_on_list = []
                for dep_data in target_data.get("dependsOn", []):
                    depends_on_list.append(ConceptMapGroupElementTargetDependsOn(
                        property=dep_data.get("property"),
                        system=dep_data.get("system"),
                        value=dep_data.get("value"),
                        display=dep_data.get("display")
                    ))
                
                product_list = []
                for prod_data in target_data.get("product", []):
                    product_list.append(ConceptMapGroupElementTargetDependsOn(
                        property=prod_data.get("property"),
                        system=prod_data.get("system"),
                        value=prod_data.get("value"),
                        display=prod_data.get("display")
                    ))
                
                targets.append(ConceptMapGroupElementTarget(
                    code=target_data.get("code"),
                    display=target_data.get("display"),
                    equivalence=target_data.get("equivalence"),
                    comment=target_data.get("comment"),
                    dependsOn=depends_on_list,
                    product=product_list
                ))
            
            elements.append(ConceptMapGroupElement(
                code=element_data.get("code"),
                display=element_data.get("display"),
                target=targets
            ))
        
        unmapped_data = group_data.get("unmapped")
        unmapped = None
        if unmapped_data:
            unmapped = ConceptMapGroupUnmapped(
                mode=unmapped_data.get("mode"),
                code=unmapped_data.get("code"),
                display=unmapped_data.get("display"),
                url=unmapped_data.get("url"),
                comment=unmapped_data.get("comment")
            )
        
        groups.append(ConceptMapGroup(
            source=group_data.get("source"),
            sourceVersion=group_data.get("sourceVersion"),
            target=group_data.get("target"),
            targetVersion=group_data.get("targetVersion"),
            element=elements,
            unmapped=unmapped
        ))
    
    # Create ConceptMap object
    concept_map = ConceptMap(
        resourceType="ConceptMap",
        url=json_data.get("url"),
        version=json_data.get("version"),
        name=json_data.get("name"),
        title=json_data.get("title"),
        status=json_data.get("status"),
        experimental=json_data.get("experimental"),
        date=json_data.get("date"),
        publisher=json_data.get("publisher"),
        description=json_data.get("description"),
        purpose=json_data.get("purpose"),
        copyright=json_data.get("copyright"),
        sourceUri=json_data.get("sourceUri"),
        sourceCanonical=json_data.get("sourceCanonical"),
        targetUri=json_data.get("targetUri"),
        targetCanonical=json_data.get("targetCanonical"),
        group=groups
    )
    
    # Parse identifier
    for ident_data in json_data.get("identifier", []):
        from dnhealth.dnhealth_fhir.types import Identifier
        concept_map.identifier.append(Identifier(
            use=ident_data.get("use"),
            type=ident_data.get("type"),
            system=ident_data.get("system"),
            value=ident_data.get("value")
        ))
    
    # Parse contact
    for contact_data in json_data.get("contact", []):
        from dnhealth.dnhealth_fhir.types import ContactDetail
        concept_map.contact.append(ContactDetail(
            name=contact_data.get("name"),
            telecom=contact_data.get("telecom", [])
        ))
    
    # Parse useContext
    for uc_data in json_data.get("useContext", []):
        from dnhealth.dnhealth_fhir.types import UsageContext
        concept_map.useContext.append(UsageContext(
            code=uc_data.get("code"),
            valueCodeableConcept=uc_data.get("valueCodeableConcept"),
            valueQuantity=uc_data.get("valueQuantity"),
            valueRange=uc_data.get("valueRange"),
            valueReference=uc_data.get("valueReference")
        ))
    
    # Parse jurisdiction
    for jur_data in json_data.get("jurisdiction", []):
        from dnhealth.dnhealth_fhir.types import CodeableConcept
        concept_map.jurisdiction.append(CodeableConcept(
            coding=jur_data.get("coding", []),
            text=jur_data.get("text")
        ))
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] ConceptMap parsing completed successfully")
    
    return concept_map


def translate_code(
    concept_map: ConceptMap,
    source_code: str,
    source_system: Optional[str] = None,
    target_system: Optional[str] = None
) -> List[Tuple[str, str, str]]:
    """
    Translate a code using a ConceptMap.
    
    Args:
        concept_map: ConceptMap resource
        source_code: Source code to translate
        source_system: Optional source code system URL (if None, uses first group's source)
        target_system: Optional target code system URL (if None, uses first group's target)
        
    Returns:
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
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Code translation completed: {len(translations)} translations found")
    
    return translations



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def get_concept_map_by_url(url: str, concept_maps: List[ConceptMap]) -> Optional[ConceptMap]:
    """
    Find a ConceptMap by URL.
    
    Args:
        url: ConceptMap URL
        concept_maps: List of ConceptMap resources to search
        
    Returns:
        ConceptMap if found, None otherwise
    """
    for cm in concept_maps:
        if cm.url == url:
            return cm
    return None

