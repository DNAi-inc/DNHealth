# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicationDispense resource.

Complete MedicationDispense resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Quantity,
    Period,
)


@dataclass
class MedicationDispensePerformer:
    """
    Who performed the dispense and what they did.
    """

    function: Optional[CodeableConcept] = None
    actor: Reference  # Who performed the dispense (required)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationDispenseSubstitution:
    """
    Whether a substitution was performed on the dispense.
    """

    wasSubstituted: bool  # Whether a substitution was or was not performed on the dispense (required)
    type: Optional[CodeableConcept] = None
    reason: List[CodeableConcept] = field(default_factory=list)
    responsibleParty: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationDispense(FHIRResource):
    """
    FHIR R4 MedicationDispense resource.

    Represents the supply of a medication to a patient.
    """

    resourceType: str = "MedicationDispense"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    status: str  # preparation | in-progress | cancelled | on-hold | completed | entered-in-error | stopped | declined | unknown
    # Status reason codeable concept
    statusReasonCodeableConcept: Optional[CodeableConcept] = None
    # Status reason reference
    statusReasonReference: Optional[Reference] = None
    # Category
    category: Optional[CodeableConcept] = None
    # Medication codeable concept
    medicationCodeableConcept: Optional[CodeableConcept] = None
    # Medication reference
    medicationReference: Optional[Reference] = None
    # Subject
    subject: Optional[Reference] = None
    # Context
    context: Optional[Reference] = None
    # Supporting information
    supportingInformation: List[Reference] = field(default_factory=list)
    # Performer
    performer: List[MedicationDispensePerformer] = field(default_factory=list)
    # Location
    location: Optional[Reference] = None
    # Authorizing prescription
    authorizingPrescription: List[Reference] = field(default_factory=list)
    # Type
    type: Optional[CodeableConcept] = None
    # Quantity
    quantity: Optional[Quantity] = None
    # Days supply
    daysSupply: Optional[Quantity] = None
    # When prepared
    whenPrepared: Optional[str] = None  # ISO 8601 dateTime
    # When handed over
    whenHandedOver: Optional[str] = None  # ISO 8601 dateTime
    # Destination
    destination: Optional[Reference] = None
    # Receiver
    receiver: List[Reference] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Dosage instruction (Dosage complex type - using Any for now)
    dosageInstruction: List[Any] = field(default_factory=list)
    # Substitution
    substitution: Optional[MedicationDispenseSubstitution] = None
    # Detected issue
    detectedIssue: List[Reference] = field(default_factory=list)
    # Event history
    eventHistory: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
