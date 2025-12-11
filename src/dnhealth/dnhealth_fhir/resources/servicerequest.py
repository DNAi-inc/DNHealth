# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ServiceRequest resource.

Complete ServiceRequest resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Timing,
    Period,
    Quantity,
    Ratio,
    Range,
)


@dataclass
class ServiceRequest(FHIRResource):
    """
    FHIR R4 ServiceRequest resource.

    Represents a request for a service to be performed.
    """

    resourceType: str = "ServiceRequest"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Instantiates canonical
    instantiatesCanonical: List[str] = field(default_factory=list)
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Replaces
    replaces: List[Reference] = field(default_factory=list)
    # Requisition
    requisition: Optional[Identifier] = None
    # Status
    status: str  # draft | active | on-hold | revoked | completed | entered-in-error | unknown
    # Intent
    intent: str  # proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
    # Category
    category: List[CodeableConcept] = field(default_factory=list)
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Do not perform
    doNotPerform: Optional[bool] = None
    # Code
    code: Optional[CodeableConcept] = None
    # Order detail
    orderDetail: List[CodeableConcept] = field(default_factory=list)
    # Quantity
    quantityQuantity: Optional["Quantity"] = None
    quantityRatio: Optional["Ratio"] = None
    quantityRange: Optional["Range"] = None
    # Subject
    subject: Reference  # Individual or entity the service is ordered for (required)
    # Encounter
    encounter: Optional[Reference] = None
    # Occurrence dateTime
    occurrenceDateTime: Optional[str] = None  # ISO 8601 dateTime
    # Occurrence period
    occurrencePeriod: Optional[Period] = None
    # Occurrence timing
    occurrenceTiming: Optional[Timing] = None
    # As needed boolean
    asNeededBoolean: Optional[bool] = None
    # As needed codeable concept
    asNeededCodeableConcept: Optional[CodeableConcept] = None
    # Authored on
    authoredOn: Optional[str] = None  # ISO 8601 dateTime
    # Requester
    requester: Optional[Reference] = None
    # Performer type
    performerType: Optional[CodeableConcept] = None
    # Performer
    performer: List[Reference] = field(default_factory=list)
    # Location code
    locationCode: List[CodeableConcept] = field(default_factory=list)
    # Location reference
    locationReference: List[Reference] = field(default_factory=list)
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Insurance
    insurance: List[Reference] = field(default_factory=list)
    # Supporting info
    supportingInfo: List[Reference] = field(default_factory=list)
    # Specimen
    specimen: List[Reference] = field(default_factory=list)
    # Body site
    bodySite: List[CodeableConcept] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Patient instruction
    patientInstruction: Optional[str] = None
    # Relevant history
    relevantHistory: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
