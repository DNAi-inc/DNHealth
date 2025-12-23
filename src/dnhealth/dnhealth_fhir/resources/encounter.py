# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Encounter resource.

Complete Encounter resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    Duration,
)
from typing import Any


@dataclass
class Encounter(FHIRResource):
    """
    FHIR R4 Encounter resource.

    Represents an interaction between a patient and healthcare provider.
    """

    resourceType: str = "Encounter"
    # Required fields (must come before optional fields)
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce status is provided.
    status: Optional[str] = None  # planned, arrived, triaged, in-progress, onleave, finished, cancelled, entered-in-error, unknown
    # Optional fields
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Status history
    statusHistory: List["EncounterStatusHistory"] = field(default_factory=list)
    # Class
    class_: Optional[CodeableConcept] = None  # class is a Python keyword, so use class_
    # Class history
    classHistory: List["EncounterClassHistory"] = field(default_factory=list)
    # Type
    type: List[CodeableConcept] = field(default_factory=list)
    # Service type
    serviceType: Optional[CodeableConcept] = None
    # Priority
    priority: Optional[CodeableConcept] = None
    # Subject
    subject: Optional[Reference] = None
    # Episode of care
    episodeOfCare: List[Reference] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Participant
    participant: List["EncounterParticipant"] = field(default_factory=list)
    # Appointment
    appointment: List[Reference] = field(default_factory=list)
    # Period
    period: Optional[Period] = None
    # Length
    length: Optional[Duration] = None
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Diagnosis
    diagnosis: List["EncounterDiagnosis"] = field(default_factory=list)
    # Account
    account: List[Reference] = field(default_factory=list)
    # Hospitalization
    hospitalization: Optional["EncounterHospitalization"] = None
    # Location
    location: List["EncounterLocation"] = field(default_factory=list)
    # Service provider
    serviceProvider: Optional[Reference] = None
    # Part of
    partOf: Optional[Reference] = None


@dataclass
class EncounterStatusHistory:
    """Status history for an encounter."""

    # Note: status is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce status is provided.
    status: Optional[str] = None
    # Note: period is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce period is provided.
    period: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class EncounterClassHistory:
    """Class history for an encounter."""

    class_: CodeableConcept
    period: Period
    extension: List[Extension] = field(default_factory=list)


@dataclass
class EncounterParticipant:
    """Participant in an encounter."""

    type: List[CodeableConcept] = field(default_factory=list)
    period: Optional[Period] = None
    individual: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class EncounterDiagnosis:
    """Diagnosis associated with an encounter."""

    condition: Reference
    use: Optional[CodeableConcept] = None
    rank: Optional[int] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class EncounterHospitalization:
    """Hospitalization details for an encounter."""

    preAdmissionIdentifier: Optional[Identifier] = None
    origin: Optional[Reference] = None
    admitSource: Optional[CodeableConcept] = None
    reAdmission: Optional[CodeableConcept] = None
    dietPreference: List[CodeableConcept] = field(default_factory=list)
    specialCourtesy: List[CodeableConcept] = field(default_factory=list)
    specialArrangement: List[CodeableConcept] = field(default_factory=list)
    destination: Optional[Reference] = None
    dischargeDisposition: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class EncounterLocation:
    """Location where encounter occurred."""

    location: Reference
    status: Optional[str] = None  # planned, active, reserved, completed
    physicalType: Optional[CodeableConcept] = None
    period: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


# Note: Duration type is now available from dnhealth.dnhealth_fhir.types
# Import it if needed, or use the Duration from types module

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
