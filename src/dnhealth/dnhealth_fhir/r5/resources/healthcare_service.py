# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 HealthcareService resource.

The details of a healthcare service available at a location or in a catalog.  In the case where there is a hierarchy of services (for example, Lab -> Pathology -> Wound Cultures), this can be represented using a set of linked HealthcareServices.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class HealthcareServiceEligibility:
    """
    HealthcareServiceEligibility nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[CodeableConcept] = None  # Coded value for the eligibility.
    comment: Optional[str] = None  # Describes the eligibility conditions for the service.


@dataclass
class HealthcareService(FHIRResource):
    """
    The details of a healthcare service available at a location or in a catalog.  In the case where there is a hierarchy of services (for example, Lab -> Pathology -> Wound Cultures), this can be represented using a set of linked HealthcareServices.
    """

    resourceType: str = "HealthcareService"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # External identifiers for this item.
    active: Optional[bool] = None  # This flag is used to mark the record to not be used. This is not used when a center is closed for...
    providedBy: Optional[Reference] = None  # The organization that provides this healthcare service.
    offeredIn: Optional[List[Reference]] = field(default_factory=list)  # When the HealthcareService is representing a specific, schedulable service, the availableIn prope...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies the broad category of service being performed or delivered.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specific type of service that may be delivered or performed.
    specialty: Optional[List[CodeableConcept]] = field(default_factory=list)  # Collection of specialties handled by the Healthcare service. This is more of a medical term.
    location: Optional[List[Reference]] = field(default_factory=list)  # The location(s) where this healthcare service may be provided.
    name: Optional[str] = None  # Further description of the service as it would be presented to a consumer while searching.
    comment: Optional[str] = None  # Any additional description of the service and/or any specific issues not covered by the other att...
    extraDetails: Optional[str] = None  # Extra details about the service that can't be placed in the other fields.
    photo: Optional[Attachment] = None  # If there is a photo/symbol associated with this HealthcareService, it may be included here to fac...
    contact: Optional[List[Any]] = field(default_factory=list)  # The contact details of communication devices available relevant to the specific HealthcareService...
    coverageArea: Optional[List[Reference]] = field(default_factory=list)  # The location(s) that this service is available to (not where the service is provided).
    serviceProvisionCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # The code(s) that detail the conditions under which the healthcare service is available/offered.
    eligibility: Optional[List[BackboneElement]] = field(default_factory=list)  # Does this service have specific eligibility requirements that need to be met in order to use the ...
    program: Optional[List[CodeableConcept]] = field(default_factory=list)  # Programs that this service is applicable to.
    characteristic: Optional[List[CodeableConcept]] = field(default_factory=list)  # Collection of characteristics (attributes).
    communication: Optional[List[CodeableConcept]] = field(default_factory=list)  # Some services are specifically made available in multiple languages, this property permits a dire...
    referralMethod: Optional[List[CodeableConcept]] = field(default_factory=list)  # Ways that the service accepts referrals, if this is not provided then it is implied that no refer...
    appointmentRequired: Optional[bool] = None  # Indicates whether or not a prospective consumer will require an appointment for a particular serv...
    availability: Optional[List[Any]] = field(default_factory=list)  # A collection of times that the healthcare service is available.
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # Technical endpoints providing access to services operated for the specific healthcare services de...