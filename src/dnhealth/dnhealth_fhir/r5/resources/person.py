# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Person resource.

Demographics and administrative information about a person independent of a specific health-related context.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Attachment, BackboneElement, CodeableConcept, ContactPoint, Extension, HumanName, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class PersonCommunication:
    """
    PersonCommunication nested class.
    """

    language: Optional[CodeableConcept] = None  # The ISO-639-1 alpha 2 code in lower case for the language, optionally followed by a hyphen and th...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    preferred: Optional[bool] = None  # Indicates whether or not the person prefers this language (over other languages he masters up a c...

@dataclass
class PersonLink:
    """
    PersonLink nested class.
    """

    target: Optional[Reference] = None  # The resource to which this actual person is associated.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    assurance: Optional[str] = None  # Level of assurance that this link is associated with the target resource.


@dataclass
class Person(FHIRResource):
    """
    Demographics and administrative information about a person independent of a specific health-related context.
    """

    resourceType: str = "Person"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for a person within a particular scope.
    active: Optional[bool] = None  # Whether this person's record is in active use.
    name: Optional[List[HumanName]] = field(default_factory=list)  # A name associated with the person.
    telecom: Optional[List[ContactPoint]] = field(default_factory=list)  # A contact detail for the person, e.g. a telephone number or an email address.
    gender: Optional[str] = None  # Administrative Gender.
    birthDate: Optional[str] = None  # The birth date for the person.
    deceased: Optional[Any] = None  # Indicates if the individual is deceased or not.
    address: Optional[List[Address]] = field(default_factory=list)  # One or more addresses for the person.
    maritalStatus: Optional[CodeableConcept] = None  # This field contains a person's most recent marital (civil) status.
    photo: Optional[List[Attachment]] = field(default_factory=list)  # An image that can be displayed as a thumbnail of the person to enhance the identification of the ...
    communication: Optional[List[BackboneElement]] = field(default_factory=list)  # A language which may be used to communicate with the person about his or her health.
    managingOrganization: Optional[Reference] = None  # The organization that is the custodian of the person record.
    link: Optional[List[BackboneElement]] = field(default_factory=list)  # Link to a resource that concerns the same actual person.