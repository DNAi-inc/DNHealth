# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 RelatedPerson resource.

Information about a person that is involved in a patient's health or the care for a patient, but who is not the target of healthcare, nor has a formal responsibility in the care process.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Attachment, BackboneElement, CodeableConcept, ContactPoint, Extension, HumanName, Identifier, Period, Reference
from typing import List, Optional

@dataclass
class RelatedPersonCommunication:
    """
    RelatedPersonCommunication nested class.
    """

    language: Optional[CodeableConcept] = None  # The ISO-639-1 alpha 2 code in lower case for the language, optionally followed by a hyphen and th...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    preferred: Optional[bool] = None  # Indicates whether or not the related person prefers this language (over other languages he or she...


@dataclass
class RelatedPerson(FHIRResource):
    """
    Information about a person that is involved in a patient's health or the care for a patient, but who is not the target of healthcare, nor has a formal responsibility in the care process.
    """

    patient: Optional[Reference] = None  # The patient this person is related to.
    resourceType: str = "RelatedPerson"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for a person within a particular scope.
    active: Optional[bool] = None  # Whether this related person record is in active use.
    relationship: Optional[List[CodeableConcept]] = field(default_factory=list)  # The nature of the relationship between the related person and the patient.
    name: Optional[List[HumanName]] = field(default_factory=list)  # A name associated with the person.
    telecom: Optional[List[ContactPoint]] = field(default_factory=list)  # A contact detail for the person, e.g. a telephone number or an email address.
    gender: Optional[str] = None  # Administrative Gender - the gender that the person is considered to have for administration and r...
    birthDate: Optional[str] = None  # The date on which the related person was born.
    address: Optional[List[Address]] = field(default_factory=list)  # Address where the related person can be contacted or visited.
    photo: Optional[List[Attachment]] = field(default_factory=list)  # Image of the person.
    period: Optional[Period] = None  # The period of time during which this relationship is or was active. If there are no dates defined...
    communication: Optional[List[BackboneElement]] = field(default_factory=list)  # A language which may be used to communicate with the related person about the patient's health.