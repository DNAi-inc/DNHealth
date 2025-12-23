# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 PractitionerRole resource.

A specific set of Roles/Locations/specialties/services that a practitioner may perform, or has performed at an organization during a period of time.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class PractitionerRole(FHIRResource):
    """
    A specific set of Roles/Locations/specialties/services that a practitioner may perform, or has performed at an organization during a period of time.
    """

    resourceType: str = "PractitionerRole"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business Identifiers that are specific to a role/location.
    active: Optional[bool] = None  #  Whether this practitioner role record is in active use. Some systems may use this property to ma...
    period: Optional[Period] = None  # The period during which the person is authorized to act as a practitioner in these role(s) for th...
    practitioner: Optional[Reference] = None  # Practitioner that is able to provide the defined services for the organization.
    organization: Optional[Reference] = None  # The organization where the Practitioner performs the roles associated.
    code: Optional[List[CodeableConcept]] = field(default_factory=list)  # Roles which this practitioner is authorized to perform for the organization.
    specialty: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specialty of a practitioner that describes the functional role they are practicing at a given...
    location: Optional[List[Reference]] = field(default_factory=list)  # The location(s) at which this practitioner provides care.
    healthcareService: Optional[List[Reference]] = field(default_factory=list)  # The list of healthcare services that this worker provides for this role's Organization/Location(s).
    contact: Optional[List[Any]] = field(default_factory=list)  # The contact details of communication devices available relevant to the specific PractitionerRole....
    characteristic: Optional[List[CodeableConcept]] = field(default_factory=list)  # Collection of characteristics (attributes).
    communication: Optional[List[CodeableConcept]] = field(default_factory=list)  # A language the practitioner can use in patient communication. The practitioner may know several l...
    availability: Optional[List[Any]] = field(default_factory=list)  # A collection of times the practitioner is available or performing this role at the location and/o...
    endpoint: Optional[List[Reference]] = field(default_factory=list)  #  Technical endpoints providing access to services operated for the practitioner with this role. C...