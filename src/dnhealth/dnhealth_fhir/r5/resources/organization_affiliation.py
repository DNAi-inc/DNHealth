# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 OrganizationAffiliation resource.

Defines an affiliation/assotiation/relationship between 2 distinct organizations, that is not a part-of relationship/sub-division relationship.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class OrganizationAffiliation(FHIRResource):
    """
    Defines an affiliation/assotiation/relationship between 2 distinct organizations, that is not a part-of relationship/sub-division relationship.
    """

    resourceType: str = "OrganizationAffiliation"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers that are specific to this role.
    active: Optional[bool] = None  # Whether this organization affiliation record is in active use.
    period: Optional[Period] = None  # The period during which the participatingOrganization is affiliated with the primary organization.
    organization: Optional[Reference] = None  # Organization where the role is available (primary organization/has members).
    participatingOrganization: Optional[Reference] = None  # The Participating Organization provides/performs the role(s) defined by the code to the Primary O...
    network: Optional[List[Reference]] = field(default_factory=list)  # The network in which the participatingOrganization provides the role's services (if defined) at t...
    code: Optional[List[CodeableConcept]] = field(default_factory=list)  # Definition of the role the participatingOrganization plays in the association.
    specialty: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specific specialty of the participatingOrganization in the context of the role.
    location: Optional[List[Reference]] = field(default_factory=list)  # The location(s) at which the role occurs.
    healthcareService: Optional[List[Reference]] = field(default_factory=list)  # Healthcare services provided through the role.
    contact: Optional[List[Any]] = field(default_factory=list)  # The contact details of communication devices available at the participatingOrganization relevant ...
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # Technical endpoints providing access to services operated for this role.