# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Patient resource.

Complete Patient resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    HumanName,
    ContactPoint,
    Address,
    Reference,
    Attachment,
    CodeableConcept,
    Period,
)


@dataclass
class Patient(FHIRResource):
    """
    FHIR R4 Patient resource.

    Represents a patient receiving healthcare services.
    """

    resourceType: str = "Patient"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Status
    active: Optional[bool] = None
    # Name
    name: List[HumanName] = field(default_factory=list)
    # Contact
    telecom: List[ContactPoint] = field(default_factory=list)
    # Gender
    gender: Optional[str] = None  # male, female, other, unknown
    # Birth date
    birthDate: Optional[str] = None
    # Deceased
    deceasedBoolean: Optional[bool] = None
    deceasedDateTime: Optional[str] = None
    # Address
    address: List[Address] = field(default_factory=list)
    # Marital status
    maritalStatus: Optional[CodeableConcept] = None
    # Multiple birth
    multipleBirthBoolean: Optional[bool] = None
    multipleBirthInteger: Optional[int] = None
    # Photo
    photo: List[Attachment] = field(default_factory=list)
    # Contact (related persons)
    contact: List["PatientContact"] = field(default_factory=list)
    # Communication
    communication: List["PatientCommunication"] = field(default_factory=list)
    # General practitioner
    generalPractitioner: List[Reference] = field(default_factory=list)
    # Managing organization
    managingOrganization: Optional[Reference] = None
    # Link to other patients
    link: List["PatientLink"] = field(default_factory=list)


@dataclass
class PatientContact:
    """
    Patient contact (related person).

    A contact person for the patient.
    """

    relationship: List[CodeableConcept] = field(default_factory=list)
    name: Optional[HumanName] = None
    telecom: List[ContactPoint] = field(default_factory=list)
    address: Optional[Address] = None
    gender: Optional[str] = None
    organization: Optional[Reference] = None
    period: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class PatientCommunication:
    """
    Patient communication preferences.

    Languages the patient can communicate in.
    """

    language: CodeableConcept
    preferred: Optional[bool] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class PatientLink:
    """
    Link to another patient resource.

    Links this patient to another patient (e.g., merged records).
    """

    other: Reference
    type: str  # replaced-by, replaces, refer, seealso
    extension: List[Extension] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
