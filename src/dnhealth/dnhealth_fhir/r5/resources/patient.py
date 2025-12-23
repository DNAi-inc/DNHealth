# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Patient resource.

Demographics and other administrative information about an individual or animal receiving care or other health-related services.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Attachment, BackboneElement, CodeableConcept, ContactPoint, Extension, HumanName, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class PatientContact:
    """
    PatientContact nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    relationship: Optional[List[CodeableConcept]] = field(default_factory=list)  # The nature of the relationship between the patient and the contact person.
    name: Optional[HumanName] = None  # A name associated with the contact person.
    telecom: Optional[List[ContactPoint]] = field(default_factory=list)  # A contact detail for the person, e.g. a telephone number or an email address.
    address: Optional[Address] = None  # Address for the contact person.
    gender: Optional[str] = None  # Administrative Gender - the gender that the contact person is considered to have for administrati...
    organization: Optional[Reference] = None  # Organization on behalf of which the contact is acting or for which the contact is working.
    period: Optional[Period] = None  # The period during which this contact person or organization is valid to be contacted relating to ...

@dataclass
class PatientCommunication:
    """
    PatientCommunication nested class.
    """

    language: Optional[CodeableConcept] = None  # The ISO-639-1 alpha 2 code in lower case for the language, optionally followed by a hyphen and th...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    preferred: Optional[bool] = None  # Indicates whether or not the patient prefers this language (over other languages he masters up a ...

@dataclass
class PatientLink:
    """
    PatientLink nested class.
    """

    other: Optional[Reference] = None  # Link to a Patient or RelatedPerson resource that concerns the same actual individual.
    type: Optional[str] = None  # The type of link between this patient resource and another patient resource.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Patient(FHIRResource):
    """
    Demographics and other administrative information about an individual or animal receiving care or other health-related services.
    """

    resourceType: str = "Patient"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # An identifier for this patient.
    active: Optional[bool] = None  # Whether this patient record is in active use.  Many systems use this property to mark as non-curr...
    name: Optional[List[HumanName]] = field(default_factory=list)  # A name associated with the individual.
    telecom: Optional[List[ContactPoint]] = field(default_factory=list)  # A contact detail (e.g. a telephone number or an email address) by which the individual may be con...
    gender: Optional[str] = None  # Administrative Gender - the gender that the patient is considered to have for administration and ...
    birthDate: Optional[str] = None  # The date of birth for the individual.
    deceased: Optional[Any] = None  # Indicates if the individual is deceased or not.
    address: Optional[List[Address]] = field(default_factory=list)  # An address for the individual.
    maritalStatus: Optional[CodeableConcept] = None  # This field contains a patient's most recent marital (civil) status.
    multipleBirth: Optional[Any] = None  # Indicates whether the patient is part of a multiple (boolean) or indicates the actual birth order...
    photo: Optional[List[Attachment]] = field(default_factory=list)  # Image of the patient.
    contact: Optional[List[BackboneElement]] = field(default_factory=list)  # A contact party (e.g. guardian, partner, friend) for the patient.
    communication: Optional[List[BackboneElement]] = field(default_factory=list)  # A language which may be used to communicate with the patient about his or her health.
    generalPractitioner: Optional[List[Reference]] = field(default_factory=list)  # Patient's nominated care provider.
    managingOrganization: Optional[Reference] = None  # Organization that is the custodian of the patient record.
    link: Optional[List[BackboneElement]] = field(default_factory=list)  # Link to a Patient or RelatedPerson resource that concerns the same actual individual.