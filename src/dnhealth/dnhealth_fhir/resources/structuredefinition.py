# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 StructureDefinition resource.

StructureDefinition defines the structure of FHIR resources and data types.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    ContactDetail,
    UsageContext,
)


@dataclass
class ElementDefinition:
    """
    FHIR ElementDefinition complex type.
    
    Defines the structure and constraints for an element.
    Note: This is a simplified version. Full ElementDefinition has many fields.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
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
    # Note: ElementDefinition has many defaultValue* and fixed* fields
    # For simplicity, we'll store them as a dict
    _default_values: Dict[str, Any] = field(default_factory=dict)
    _fixed_values: Dict[str, Any] = field(default_factory=dict)
    meaningWhenMissing: Optional[str] = None
    orderMeaning: Optional[str] = None
    # Additional fields can be stored in _unknown_fields
    _unknown_fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructureDefinitionMapping:
    """
    FHIR StructureDefinition.mapping complex type.
    
    Defines an external mapping.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    identity: Optional[str] = None  # Internal id when this mapping is used
    uri: Optional[str] = None  # Identifies what this mapping refers to
    name: Optional[str] = None  # Names what this mapping refers to
    comment: Optional[str] = None  # Versions, issues, scope limitations


@dataclass
class StructureDefinitionContext:
    """
    FHIR StructureDefinition.context complex type.
    
    Identifies the types of resource or data type elements to which the extension can be applied.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: Optional[str] = None  # fhirpath | element | extension
    expression: Optional[str] = None  # Where the extension can be used in instances


@dataclass
class StructureDefinitionSnapshot:
    """
    FHIR StructureDefinition.snapshot complex type.
    
    A snapshot view is expressed in a standalone form that can be used and interpreted
    without considering the base StructureDefinition.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    element: List[ElementDefinition] = field(default_factory=list)


@dataclass
class StructureDefinitionDifferential:
    """
    FHIR StructureDefinition.differential complex type.
    
    A differential view is expressed relative to the base StructureDefinition -
    a statement of differences that it applies.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    element: List[ElementDefinition] = field(default_factory=list)


@dataclass
class StructureDefinition(MetadataResource):
    """
    FHIR R4 StructureDefinition resource.
    
    Defines the structure of FHIR resources and data types.
    Extends MetadataResource.
    """
    
    resourceType: str = "StructureDefinition"
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
    # Keyword
    keyword: List[CodeableConcept] = field(default_factory=list)
    # FHIR Version
    fhirVersion: Optional[str] = None  # FHIR Version this StructureDefinition targets
    # Mapping
    mapping: List[StructureDefinitionMapping] = field(default_factory=list)
    # Kind
    kind: Optional[str] = None  # primitive-type, complex-type, resource, logical
    # Abstract
    abstract: Optional[bool] = None  # Whether the structure is abstract
    # Context
    context: List[StructureDefinitionContext] = field(default_factory=list)
    # Context Invariant
    contextInvariant: List[str] = field(default_factory=list)  # FHIRPath invariants
    # Type
    type: Optional[str] = None  # Type this structure describes
    # Base Definition
    baseDefinition: Optional[str] = None  # Canonical URL of base definition
    # Derivation
    derivation: Optional[str] = None  # specialization, constraint
    # Snapshot
    snapshot: Optional[StructureDefinitionSnapshot] = None  # Snapshot view
    # Differential
    differential: Optional[StructureDefinitionDifferential] = None  # Differential view

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
