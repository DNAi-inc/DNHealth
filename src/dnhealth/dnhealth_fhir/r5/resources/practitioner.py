# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Practitioner resource.

A person who is directly or indirectly involved in the provisioning of healthcare or related services.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Attachment, BackboneElement, CodeableConcept, ContactPoint, Extension, HumanName, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class PractitionerQualification:
    """
    PractitionerQualification nested class.
    """

    code: Optional[CodeableConcept] = None  # Coded representation of the qualification.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # An identifier that applies to this person's qualification.
    period: Optional[Period] = None  # Period during which the qualification is valid.
    issuer: Optional[Reference] = None  # Organization that regulates and issues the qualification.

@dataclass
class PractitionerCommunication:
    """
    PractitionerCommunication nested class.
    """

    language: Optional[CodeableConcept] = None  # The ISO-639-1 alpha 2 code in lower case for the language, optionally followed by a hyphen and th...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    preferred: Optional[bool] = None  # Indicates whether or not the person prefers this language (over other languages he masters up a c...


@dataclass
class Practitioner(FHIRResource):
    """
    A person who is directly or indirectly involved in the provisioning of healthcare or related services.
    """

    resourceType: str = "Practitioner"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # An identifier that applies to this person in this role.
    active: Optional[bool] = None  # Whether this practitioner's record is in active use.
    name: Optional[List[HumanName]] = field(default_factory=list)  # The name(s) associated with the practitioner.
    telecom: Optional[List[ContactPoint]] = field(default_factory=list)  # A contact detail for the practitioner, e.g. a telephone number or an email address.
    gender: Optional[str] = None  # Administrative Gender - the gender that the person is considered to have for administration and r...
    birthDate: Optional[str] = None  # The date of birth for the practitioner.
    deceased: Optional[Any] = None  # Indicates if the practitioner is deceased or not.
    address: Optional[List[Address]] = field(default_factory=list)  # Address(es) of the practitioner that are not role specific (typically home address).
    photo: Optional[List[Attachment]] = field(default_factory=list)  # Image of the person.
    qualification: Optional[List[BackboneElement]] = field(default_factory=list)  # The official qualifications, certifications, accreditations, training, licenses (and other types ...
    communication: Optional[List[BackboneElement]] = field(default_factory=list)  # A language which may be used to communicate with the practitioner, often for correspondence/admin...