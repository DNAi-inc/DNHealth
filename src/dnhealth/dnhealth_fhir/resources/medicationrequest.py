# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicationRequest resource.

Complete MedicationRequest resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from typing import Any
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Timing,
    Period,
    Duration,
    Quantity,
)


@dataclass
class MedicationRequestDispenseRequest:
    """
    Medication supply authorization.
    
    Indicates the specific details for the dispense or medication supply part
    of a medication request (also known as a Medication Prescription or
    Medication Order).
    """

    initialFill: Optional["MedicationRequestDispenseRequestInitialFill"] = None
    dispenseInterval: Optional[Duration] = None
    validityPeriod: Optional[Period] = None
    numberOfRepeatsAllowed: Optional[int] = None
    quantity: Optional[Quantity] = None
    expectedSupplyDuration: Optional[Duration] = None
    performer: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationRequestDispenseRequestInitialFill:
    """
    First fill details.
    """

    quantity: Optional[Quantity] = None
    duration: Optional[Duration] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationRequestSubstitution:
    """
    Any restrictions on medication substitution.
    
    Indicates whether or not substitution can or should be part of the
    dispense. In some cases, substitution must happen, in other cases
    substitution must not happen, and in others, substitution does not matter.
    """

    allowedBoolean: Optional[bool] = None
    allowedCodeableConcept: Optional[CodeableConcept] = None
    reason: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationRequest(FHIRResource):
    """
    FHIR R4 MedicationRequest resource.

    Represents an order or request for both supply of the medication and the
    instructions for administration of the medication to a patient.
    """

    resourceType: str = "MedicationRequest"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (identifier has default value).
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | on-hold | cancelled | completed | entered-in-error | stopped | draft | unknown (required in FHIR)
    # Status reason
    statusReason: Optional[CodeableConcept] = None
    # Intent
    # Note: intent is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce intent is provided.
    intent: Optional[str] = None  # proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
    # Category
    category: List[CodeableConcept] = field(default_factory=list)
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Do not perform
    doNotPerform: Optional[bool] = None
    # Reported boolean
    reportedBoolean: Optional[bool] = None
    # Reported reference
    reportedReference: Optional[Reference] = None
    # Medication codeable concept
    medicationCodeableConcept: Optional[CodeableConcept] = None
    # Medication reference
    medicationReference: Optional[Reference] = None
    # Subject
    # Note: subject is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce subject is provided.
    subject: Optional[Reference] = None  # Who or group medication request is for (required)
    # Encounter
    encounter: Optional[Reference] = None
    # Supporting information
    supportingInformation: List[Reference] = field(default_factory=list)
    # Authored on
    authoredOn: Optional[str] = None  # ISO 8601 dateTime
    # Requester
    requester: Optional[Reference] = None
    # Performer
    performer: Optional[Reference] = None
    # Performer type
    performerType: Optional[CodeableConcept] = None
    # Recorder
    recorder: Optional[Reference] = None
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Instantiates canonical
    instantiatesCanonical: List[str] = field(default_factory=list)
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Group identifier
    groupIdentifier: Optional[Identifier] = None
    # Course of therapy type
    courseOfTherapyType: Optional[CodeableConcept] = None
    # Insurance
    insurance: List[Reference] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Dosage instruction (Dosage complex type - using Any for now)
    dosageInstruction: List[Any] = field(default_factory=list)
    # Dispense request
    dispenseRequest: Optional[MedicationRequestDispenseRequest] = None
    # Substitution
    substitution: Optional[MedicationRequestSubstitution] = None
    # Prior prescription
    priorPrescription: Optional[Reference] = None
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
