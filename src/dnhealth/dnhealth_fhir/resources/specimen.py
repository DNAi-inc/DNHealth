# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Specimen resource.

Complete Specimen resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    Duration,
    Quantity,
    Annotation,
)


@dataclass
class SpecimenCollection:
    """
    Collection details.
    
    Details concerning the specimen collection.
    """

    collector: Optional[Reference] = None
    collectedDateTime: Optional[str] = None  # ISO 8601 dateTime
    collectedPeriod: Optional[Period] = None
    duration: Optional["Duration"] = None
    quantity: Optional["Quantity"] = None
    method: Optional[CodeableConcept] = None
    bodySite: Optional[CodeableConcept] = None
    fastingStatusCodeableConcept: Optional[CodeableConcept] = None
    fastingStatusDuration: Optional["Duration"] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenProcessing:
    """
    Processing and processing step details.
    
    Details concerning processing and processing steps for the specimen.
    """

    description: Optional[str] = None
    procedure: Optional[CodeableConcept] = None
    additive: List[Reference] = field(default_factory=list)
    timeDateTime: Optional[str] = None  # ISO 8601 dateTime
    timePeriod: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenContainer:
    """
    Container details.
    
    The container holding the specimen.
    """

    identifier: List[Identifier] = field(default_factory=list)
    description: Optional[str] = None
    type: Optional[CodeableConcept] = None
    capacity: Optional["Quantity"] = None
    specimenQuantity: Optional["Quantity"] = None
    additiveCodeableConcept: Optional[CodeableConcept] = None
    additiveReference: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenCondition:
    """
    State and condition of the specimen.
    
    The condition of the specimen.
    """

    code: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Specimen(FHIRResource):
    """
    FHIR R4 Specimen resource.

    Represents a sample for analysis.
    """

    resourceType: str = "Specimen"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Accession identifier
    accessionIdentifier: Optional[Identifier] = None
    # Status
    status: Optional[str] = None  # available | unavailable | unsatisfactory | entered-in-error
    # Type
    type: Optional[CodeableConcept] = None
    # Subject
    subject: Optional[Reference] = None
    # Received time
    receivedTime: Optional[str] = None  # ISO 8601 dateTime
    # Parent
    parent: List[Reference] = field(default_factory=list)
    # Request
    request: List[Reference] = field(default_factory=list)
    # Collection
    collection: Optional[SpecimenCollection] = None
    # Processing
    processing: List[SpecimenProcessing] = field(default_factory=list)
    # Container
    container: List[SpecimenContainer] = field(default_factory=list)
    # Condition
    condition: List[SpecimenCondition] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
