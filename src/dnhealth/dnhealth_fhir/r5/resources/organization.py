# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Organization resource.

A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action.  Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, payer/insurer, etc.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class OrganizationQualification:
    """
    OrganizationQualification nested class.
    """

    code: Optional[CodeableConcept] = None  # Coded representation of the qualification.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # An identifier allocated to this qualification for this organization.
    period: Optional[Period] = None  # Period during which the qualification is valid.
    issuer: Optional[Reference] = None  # Organization that regulates and issues the qualification.


@dataclass
class Organization(FHIRResource):
    """
    A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action.  Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, payer/insurer, etc.
    """

    resourceType: str = "Organization"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for the organization that is used to identify the organization across multiple dispara...
    active: Optional[bool] = None  # Whether the organization's record is still in active use.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The kind(s) of organization that this is.
    name: Optional[str] = None  # A name associated with the organization.
    alias: Optional[List[str]] = field(default_factory=list)  # A list of alternate names that the organization is known as, or was known as in the past.
    description: Optional[str] = None  # Description of the organization, which helps provide additional general context on the organizati...
    contact: Optional[List[Any]] = field(default_factory=list)  # The contact details of communication devices available relevant to the specific Organization. Thi...
    partOf: Optional[Reference] = None  # The organization of which this organization forms a part.
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # Technical endpoints providing access to services operated for the organization.
    qualification: Optional[List[BackboneElement]] = field(default_factory=list)  # The official certifications, accreditations, training, designations and licenses that authorize a...