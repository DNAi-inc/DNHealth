# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Observation resource.

Complete Observation resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Quantity,
    Attachment,
    Period,
    Annotation,
    Range,
    Ratio,
    SampledData,
    Timing,
)
from typing import Any


@dataclass
class Observation(FHIRResource):
    """
    FHIR R4 Observation resource.

    Represents a measurement or assertion about a patient.
    """

    resourceType: str = "Observation"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    status: str  # registered, preliminary, final, amended, corrected, cancelled, entered-in-error, unknown
    # Category
    category: List[CodeableConcept] = field(default_factory=list)
    # Code
    code: CodeableConcept
    # Subject
    subject: Optional[Reference] = None
    # Focus
    focus: List[Reference] = field(default_factory=list)
    # Encounter
    encounter: Optional[Reference] = None
    # Effective time
    effectiveDateTime: Optional[str] = None
    effectivePeriod: Optional[Period] = None
    effectiveTiming: Optional[Timing] = None
    effectiveInstant: Optional[str] = None
    # Issued
    issued: Optional[str] = None
    # Performer
    performer: List[Reference] = field(default_factory=list)
    # Value
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueRange: Optional[Range] = None
    valueRatio: Optional[Ratio] = None
    valueSampledData: Optional[SampledData] = None
    valueTime: Optional[str] = None
    valueDateTime: Optional[str] = None
    valuePeriod: Optional[Period] = None
    # Data absent reason
    dataAbsentReason: Optional[CodeableConcept] = None
    # Interpretation
    interpretation: List[CodeableConcept] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Body site
    bodySite: Optional[CodeableConcept] = None
    # Method
    method: Optional[CodeableConcept] = None
    # Specimen
    specimen: Optional[Reference] = None
    # Device
    device: Optional[Reference] = None
    # Reference range
    referenceRange: List["ObservationReferenceRange"] = field(default_factory=list)
    # Has member
    hasMember: List[Reference] = field(default_factory=list)
    # Derived from
    derivedFrom: List[Reference] = field(default_factory=list)
    # Component
    component: List["ObservationComponent"] = field(default_factory=list)


@dataclass
class ObservationReferenceRange:
    """
    Reference range for an observation.

    Normal range for the observation value.
    """

    low: Optional[Quantity] = None
    high: Optional[Quantity] = None
    type: Optional[CodeableConcept] = None
    appliesTo: List[CodeableConcept] = field(default_factory=list)
    age: Optional[Range] = None
    text: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class ObservationComponent:
    """
    Component of a multi-part observation.

    For observations with multiple values.
    """

    code: CodeableConcept
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueRange: Optional[Range] = None
    valueRatio: Optional[Ratio] = None
    valueSampledData: Optional[SampledData] = None
    valueTime: Optional[str] = None
    valueDateTime: Optional[str] = None
    valuePeriod: Optional[Period] = None
    dataAbsentReason: Optional[CodeableConcept] = None
    interpretation: List[CodeableConcept] = field(default_factory=list)
    referenceRange: List[ObservationReferenceRange] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


# Note: Range, Ratio, SampledData, and Timing types are imported from dnhealth.dnhealth_fhir.types

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
