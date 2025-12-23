# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Appointment resource.

Complete Appointment resource with all R4 elements.
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
    ContactPoint,
)


@dataclass
class AppointmentParticipant:
    """
    Participant in an appointment.
    
    Represents a participant (patient, practitioner, location, etc.) in an appointment.
    """

    type: List[CodeableConcept] = field(default_factory=list)
    actor: Optional[Reference] = None
    required: Optional[str] = None  # required | optional | information-only
    # Note: status is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce status is provided.
    status: Optional[str] = None  # accepted | declined | tentative | needs-action
    period: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Appointment(FHIRResource):
    """
    FHIR R4 Appointment resource.

    Represents a booking of a healthcare event among patient(s), practitioner(s),
    related person(s) and/or device(s) for a specific date/time.
    """

    resourceType: str = "Appointment"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # proposed | pending | booked | arrived | fulfilled | cancelled | noshow | entered-in-error | checked-in | waitlist (required in FHIR)
    # Cancelation reason
    cancelationReason: Optional[CodeableConcept] = None
    # Service category
    serviceCategory: List[CodeableConcept] = field(default_factory=list)
    # Service type
    serviceType: List[CodeableConcept] = field(default_factory=list)
    # Specialty
    specialty: List[CodeableConcept] = field(default_factory=list)
    # Appointment type
    appointmentType: Optional[CodeableConcept] = None
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Priority
    priority: Optional[int] = None
    # Description
    description: Optional[str] = None
    # Supporting information
    supportingInformation: List[Reference] = field(default_factory=list)
    # Start instant
    start: Optional[str] = None  # ISO 8601 dateTime
    # End instant
    end: Optional[str] = None  # ISO 8601 dateTime
    # Minutes duration
    minutesDuration: Optional[int] = None
    # Slot
    slot: List[Reference] = field(default_factory=list)
    # Created
    created: Optional[str] = None  # ISO 8601 dateTime
    # Comment
    comment: Optional[str] = None
    # Patient instruction
    patientInstruction: Optional[str] = None
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Participant
    participant: List[AppointmentParticipant] = field(default_factory=list)
    # Requested period
    requestedPeriod: List[Period] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
