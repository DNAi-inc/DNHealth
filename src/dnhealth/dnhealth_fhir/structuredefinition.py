# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 StructureDefinition parser and support.

StructureDefinition defines the structure of FHIR resources and data types.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


@dataclass
class ElementDefinition:
    """
    FHIR ElementDefinition complex type.
    
    Defines the structure and constraints for an element.
    """
    
    id: Optional[str] = None
    extension: List[Any] = field(default_factory=list)
    modifierExtension: List[Any] = field(default_factory=list)
    path: Optional[str] = None
    representation: List[str] = field(default_factory=list)
    sliceName: Optional[str] = None
    sliceIsConstraining: Optional[bool] = None
    label: Optional[str] = None
    code: List[Any] = field(default_factory=list)
    slicing: Optional[Dict[str, Any]] = None
    short: Optional[str] = None
    definition: Optional[str] = None
    comment: Optional[str] = None
    requirements: Optional[str] = None
    alias: List[str] = field(default_factory=list)
    min: Optional[int] = None
    max: Optional[str] = None
    base: Optional[Dict[str, Any]] = None
    contentReference: Optional[str] = None
    type: List[Dict[str, Any]] = field(default_factory=list)
    defaultValueBase64Binary: Optional[str] = None
    defaultValueBoolean: Optional[bool] = None
    defaultValueCanonical: Optional[str] = None
    defaultValueCode: Optional[str] = None
    defaultValueDate: Optional[str] = None
    defaultValueDateTime: Optional[str] = None
    defaultValueDecimal: Optional[float] = None
    defaultValueId: Optional[str] = None
    defaultValueInstant: Optional[str] = None
    defaultValueInteger: Optional[int] = None
    defaultValueMarkdown: Optional[str] = None
    defaultValueOid: Optional[str] = None
    defaultValuePositiveInt: Optional[int] = None
    defaultValueString: Optional[str] = None
    defaultValueTime: Optional[str] = None
    defaultValueUnsignedInt: Optional[int] = None
    defaultValueUri: Optional[str] = None
    defaultValueUrl: Optional[str] = None
    defaultValueUuid: Optional[str] = None
    defaultValueAddress: Optional[Dict[str, Any]] = None
    defaultValueAge: Optional[Dict[str, Any]] = None
    defaultValueAnnotation: Optional[Dict[str, Any]] = None
    defaultValueAttachment: Optional[Dict[str, Any]] = None
    defaultValueCodeableConcept: Optional[Dict[str, Any]] = None
    defaultValueCoding: Optional[Dict[str, Any]] = None
    defaultValueContactPoint: Optional[Dict[str, Any]] = None
    defaultValueCount: Optional[Dict[str, Any]] = None
    defaultValueDistance: Optional[Dict[str, Any]] = None
    defaultValueDuration: Optional[Dict[str, Any]] = None
    defaultValueHumanName: Optional[Dict[str, Any]] = None
    defaultValueIdentifier: Optional[Dict[str, Any]] = None
    defaultValueMoney: Optional[Dict[str, Any]] = None
    defaultValuePeriod: Optional[Dict[str, Any]] = None
    defaultValueQuantity: Optional[Dict[str, Any]] = None
    defaultValueRange: Optional[Dict[str, Any]] = None
    defaultValueRatio: Optional[Dict[str, Any]] = None
    defaultValueReference: Optional[Dict[str, Any]] = None
    defaultValueSampledData: Optional[Dict[str, Any]] = None
    defaultValueSignature: Optional[Dict[str, Any]] = None
    defaultValueTiming: Optional[Dict[str, Any]] = None
    defaultValueContactDetail: Optional[Dict[str, Any]] = None
    defaultValueContributor: Optional[Dict[str, Any]] = None
    defaultValueDataRequirement: Optional[Dict[str, Any]] = None
    defaultValueExpression: Optional[Dict[str, Any]] = None
    defaultValueParameterDefinition: Optional[Dict[str, Any]] = None
    defaultValueRelatedArtifact: Optional[Dict[str, Any]] = None
    defaultValueTriggerDefinition: Optional[Dict[str, Any]] = None
    defaultValueUsageContext: Optional[Dict[str, Any]] = None
    defaultValueDosage: Optional[Dict[str, Any]] = None
    defaultValueMeta: Optional[Dict[str, Any]] = None
    meaningWhenMissing: Optional[str] = None
    orderMeaning: Optional[str] = None
    fixedBase64Binary: Optional[str] = None
    fixedBoolean: Optional[bool] = None
    fixedCanonical: Optional[str] = None
    fixedCode: Optional[str] = None
    fixedDate: Optional[str] = None
    fixedDateTime: Optional[str] = None
    fixedDecimal: Optional[float] = None
    fixedId: Optional[str] = None
    fixedInstant: Optional[str] = None
    fixedInteger: Optional[int] = None
    fixedMarkdown: Optional[str] = None
    fixedOid: Optional[str] = None
    fixedPositiveInt: Optional[int] = None
    fixedString: Optional[str] = None
    fixedTime: Optional[str] = None
    fixedUnsignedInt: Optional[int] = None
    fixedUri: Optional[str] = None
    fixedUrl: Optional[str] = None
    fixedUuid: Optional[str] = None
    fixedAddress: Optional[Dict[str, Any]] = None
    fixedAge: Optional[Dict[str, Any]] = None
    fixedAnnotation: Optional[Dict[str, Any]] = None
    fixedAttachment: Optional[Dict[str, Any]] = None
    fixedCodeableConcept: Optional[Dict[str, Any]] = None
    fixedCoding: Optional[Dict[str, Any]] = None
    fixedContactPoint: Optional[Dict[str, Any]] = None
    fixedCount: Optional[Dict[str, Any]] = None
    fixedDistance: Optional[Dict[str, Any]] = None
    fixedDuration: Optional[Dict[str, Any]] = None
    fixedHumanName: Optional[Dict[str, Any]] = None
    fixedIdentifier: Optional[Dict[str, Any]] = None
    fixedMoney: Optional[Dict[str, Any]] = None
    fixedPeriod: Optional[Dict[str, Any]] = None
    fixedQuantity: Optional[Dict[str, Any]] = None
    fixedRange: Optional[Dict[str, Any]] = None
    fixedRatio: Optional[Dict[str, Any]] = None
    fixedReference: Optional[Dict[str, Any]] = None
    fixedSampledData: Optional[Dict[str, Any]] = None
    fixedSignature: Optional[Dict[str, Any]] = None
    fixedTiming: Optional[Dict[str, Any]] = None
    fixedContactDetail: Optional[Dict[str, Any]] = None
    fixedContributor: Optional[Dict[str, Any]] = None
    fixedDataRequirement: Optional[Dict[str, Any]] = None
    fixedExpression: Optional[Dict[str, Any]] = None
    fixedParameterDefinition: Optional[Dict[str, Any]] = None
    fixedRelatedArtifact: Optional[Dict[str, Any]] = None
    fixedTriggerDefinition: Optional[Dict[str, Any]] = None
    fixedUsageContext: Optional[Dict[str, Any]] = None
    fixedDosage: Optional[Dict[str, Any]] = None
    fixedMeta: Optional[Dict[str, Any]] = None
    patternBase64Binary: Optional[str] = None
    patternBoolean: Optional[bool] = None
    patternCanonical: Optional[str] = None
    patternCode: Optional[str] = None
    patternDate: Optional[str] = None
    patternDateTime: Optional[str] = None
    patternDecimal: Optional[float] = None
    patternId: Optional[str] = None
    patternInstant: Optional[str] = None
    patternInteger: Optional[int] = None
    patternMarkdown: Optional[str] = None
    patternOid: Optional[str] = None
    patternPositiveInt: Optional[int] = None
    patternString: Optional[str] = None
    patternTime: Optional[str] = None
    patternUnsignedInt: Optional[int] = None
    patternUri: Optional[str] = None
    patternUrl: Optional[str] = None
    patternUuid: Optional[str] = None
    patternAddress: Optional[Dict[str, Any]] = None
    patternAge: Optional[Dict[str, Any]] = None
    patternAnnotation: Optional[Dict[str, Any]] = None
    patternAttachment: Optional[Dict[str, Any]] = None
    patternCodeableConcept: Optional[Dict[str, Any]] = None
    patternCoding: Optional[Dict[str, Any]] = None
    patternContactPoint: Optional[Dict[str, Any]] = None
    patternCount: Optional[Dict[str, Any]] = None
    patternDistance: Optional[Dict[str, Any]] = None
    patternDuration: Optional[Dict[str, Any]] = None
    patternHumanName: Optional[Dict[str, Any]] = None
    patternIdentifier: Optional[Dict[str, Any]] = None
    patternMoney: Optional[Dict[str, Any]] = None
    patternPeriod: Optional[Dict[str, Any]] = None
    patternQuantity: Optional[Dict[str, Any]] = None
    patternRange: Optional[Dict[str, Any]] = None
    patternRatio: Optional[Dict[str, Any]] = None
    patternReference: Optional[Dict[str, Any]] = None
    patternSampledData: Optional[Dict[str, Any]] = None
    patternSignature: Optional[Dict[str, Any]] = None
    patternTiming: Optional[Dict[str, Any]] = None
    patternContactDetail: Optional[Dict[str, Any]] = None
    patternContributor: Optional[Dict[str, Any]] = None
    patternDataRequirement: Optional[Dict[str, Any]] = None
    patternExpression: Optional[Dict[str, Any]] = None
    patternParameterDefinition: Optional[Dict[str, Any]] = None
    patternRelatedArtifact: Optional[Dict[str, Any]] = None
    patternTriggerDefinition: Optional[Dict[str, Any]] = None
    patternUsageContext: Optional[Dict[str, Any]] = None
    patternDosage: Optional[Dict[str, Any]] = None
    patternMeta: Optional[Dict[str, Any]] = None
    example: List[Dict[str, Any]] = field(default_factory=list)
    minValueDate: Optional[str] = None
    minValueDateTime: Optional[str] = None
    minValueInstant: Optional[str] = None
    minValueTime: Optional[str] = None
    minValueDecimal: Optional[float] = None
    minValueInteger: Optional[int] = None
    minValuePositiveInt: Optional[int] = None
    minValueUnsignedInt: Optional[int] = None
    minValueQuantity: Optional[Dict[str, Any]] = None
    maxValueDate: Optional[str] = None
    maxValueDateTime: Optional[str] = None
    maxValueInstant: Optional[str] = None
    maxValueTime: Optional[str] = None
    maxValueDecimal: Optional[float] = None
    maxValueInteger: Optional[int] = None
    maxValuePositiveInt: Optional[int] = None
    maxValueUnsignedInt: Optional[int] = None
    maxValueQuantity: Optional[Dict[str, Any]] = None
    maxLength: Optional[int] = None
    condition: List[str] = field(default_factory=list)
    constraint: List[Dict[str, Any]] = field(default_factory=list)
    mustSupport: Optional[bool] = None
    isModifier: Optional[bool] = None
    isModifierReason: Optional[str] = None
    isSummary: Optional[bool] = None
    binding: Optional[Dict[str, Any]] = None
    mapping: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class StructureDefinition(FHIRResource):
    """
    FHIR R4 StructureDefinition resource.
    
    Defines the structure of FHIR resources and data types.
    """
    
    resourceType: str = "StructureDefinition"
    url: Optional[str] = None
    identifier: List[Any] = field(default_factory=list)
    version: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    experimental: Optional[bool] = None
    date: Optional[str] = None
    publisher: Optional[str] = None
    contact: List[Any] = field(default_factory=list)
    description: Optional[str] = None
    useContext: List[Any] = field(default_factory=list)
    jurisdiction: List[Any] = field(default_factory=list)
    purpose: Optional[str] = None
    copyright: Optional[str] = None
    keyword: List[Any] = field(default_factory=list)
    fhirVersion: Optional[str] = None
    mapping: List[Any] = field(default_factory=list)
    kind: Optional[str] = None  # primitive-type, complex-type, resource, logical
    abstract: Optional[bool] = None
    context: List[Any] = field(default_factory=list)
    contextInvariant: List[str] = field(default_factory=list)
    type: Optional[str] = None
    baseDefinition: Optional[str] = None
    derivation: Optional[str] = None  # specialization, constraint
    snapshot: Optional[Dict[str, Any]] = None
    differential: Optional[Dict[str, Any]] = None
    # Note: snapshot and differential contain element arrays in the "element" key.
    # The get_element_definitions() function properly extracts and parses these arrays.



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def parse_structure_definition_json(json_data: Dict[str, Any]) -> StructureDefinition:
    """
    Parse a StructureDefinition from JSON data.
    
    Args:
        json_data: JSON dictionary containing StructureDefinition data
        
    Returns:
        StructureDefinition object
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting StructureDefinition JSON parsing")
    
    import json
    from dnhealth.dnhealth_fhir.parser_json import parse_fhir_json
    
    # Convert dict to JSON string, then parse
    json_str = json.dumps(json_data)
    result = parse_fhir_json(json_str, StructureDefinition)
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] StructureDefinition JSON parsing completed in {elapsed:.3f} seconds")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return result


def get_element_definitions(structure_def: StructureDefinition) -> List[ElementDefinition]:
    """
    Extract ElementDefinition objects from a StructureDefinition.
    
    Args:
        structure_def: StructureDefinition object
        
    Returns:
        List of ElementDefinition objects
    """
    start_time = datetime.now()
    elements = []
    
    # Check snapshot first
    if structure_def.snapshot and isinstance(structure_def.snapshot, dict):
        element_list = structure_def.snapshot.get("element", [])
        for elem_data in element_list:
            if isinstance(elem_data, dict):
                element = _parse_element_definition(elem_data)
                elements.append(element)
    
    # Check differential
    if structure_def.differential and isinstance(structure_def.differential, dict):
        element_list = structure_def.differential.get("element", [])
        for elem_data in element_list:
            if isinstance(elem_data, dict):
                element = _parse_element_definition(elem_data)
                elements.append(element)
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Element definitions extraction completed in {elapsed:.3f} seconds ({len(elements)} elements)")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return elements


def _parse_element_definition(elem_data: Dict[str, Any]) -> ElementDefinition:
    """
    Parse an ElementDefinition from dictionary data.
    
    Args:
        elem_data: Dictionary containing ElementDefinition data
        
    Returns:
        ElementDefinition object
    """
    element = ElementDefinition()
    
    # Basic fields
    element.id = elem_data.get("id")
    element.path = elem_data.get("path")
    element.sliceName = elem_data.get("sliceName")
    element.short = elem_data.get("short")
    element.definition = elem_data.get("definition")
    element.comment = elem_data.get("comment")
    element.min = elem_data.get("min")
    element.max = elem_data.get("max")
    element.mustSupport = elem_data.get("mustSupport")
    element.isModifier = elem_data.get("isModifier")
    element.isSummary = elem_data.get("isSummary")
    
    # Type
    if "type" in elem_data:
        element.type = elem_data["type"] if isinstance(elem_data["type"], list) else [elem_data["type"]]
    
    # Binding
    if "binding" in elem_data:
        element.binding = elem_data["binding"]
    
    # Constraint
    if "constraint" in elem_data:
        element.constraint = elem_data["constraint"] if isinstance(elem_data["constraint"], list) else [elem_data["constraint"]]

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return element


def get_element_by_path(structure_def: StructureDefinition, path: str) -> Optional[ElementDefinition]:
    """
    Get an ElementDefinition by path.
    
    Args:
        structure_def: StructureDefinition object
        path: Element path (e.g., "Patient.name")
        
    Returns:
        ElementDefinition or None if not found
    """
    elements = get_element_definitions(structure_def)
    for element in elements:
        if element.path == path:
            return element
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return None


def get_required_fields(structure_def: StructureDefinition) -> Set[str]:
    """
    Get set of required field paths from StructureDefinition.
    
    Args:
        structure_def: StructureDefinition object
        
    Returns:
        Set of required field paths (where min > 0)
    """
    start_time = datetime.now()
    required = set()
    elements = get_element_definitions(structure_def)
    for element in elements:
        if element.path and element.min is not None and element.min > 0:
            required.add(element.path)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return required

