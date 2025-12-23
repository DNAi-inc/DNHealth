# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 RegulatedAuthorization resource.

Regulatory approval, clearance or licencing related to a regulated product, treatment, facility or activity that is cited in a guidance, regulation, rule or legislative act. An example is Market Authorization relating to a Medicinal Product.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class RegulatedAuthorizationCase:
    """
    RegulatedAuthorizationCase nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[Identifier] = None  # Identifier by which this case can be referenced.
    type: Optional[CodeableConcept] = None  # The defining type of case.
    status: Optional[CodeableConcept] = None  # The status associated with the case.
    date: Optional[Any] = None  # Relevant date for this case.
    application: Optional[List[Any]] = field(default_factory=list)  # A regulatory submission from an organization to a regulator, as part of an assessing case. Multip...


@dataclass
class RegulatedAuthorization(FHIRResource):
    """
    Regulatory approval, clearance or licencing related to a regulated product, treatment, facility or activity that is cited in a guidance, regulation, rule or legislative act. An example is Market Authorization relating to a Medicinal Product.
    """

    resourceType: str = "RegulatedAuthorization"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for the authorization, typically assigned by the authorizing body.
    subject: Optional[List[Reference]] = field(default_factory=list)  # The product type, treatment, facility or activity that is being authorized.
    type: Optional[CodeableConcept] = None  # Overall type of this authorization, for example drug marketing approval, orphan drug designation.
    description: Optional[str] = None  # General textual supporting information.
    region: Optional[List[CodeableConcept]] = field(default_factory=list)  # The territory (e.g., country, jurisdiction etc.) in which the authorization has been granted.
    status: Optional[CodeableConcept] = None  # The status that is authorised e.g. approved. Intermediate states and actions can be tracked with ...
    statusDate: Optional[str] = None  # The date at which the current status was assigned.
    validityPeriod: Optional[Period] = None  # The time period in which the regulatory approval, clearance or licencing is in effect. As an exam...
    indication: Optional[List[Any]] = field(default_factory=list)  # Condition for which the use of the regulated product applies.
    intendedUse: Optional[CodeableConcept] = None  # The intended use of the product, e.g. prevention, treatment, diagnosis.
    basis: Optional[List[CodeableConcept]] = field(default_factory=list)  # The legal or regulatory framework against which this authorization is granted, or other reasons f...
    holder: Optional[Reference] = None  # The organization that has been granted this authorization, by some authoritative body (the 'regul...
    regulator: Optional[Reference] = None  # The regulatory authority or authorizing body granting the authorization. For example, European Me...
    attachedDocument: Optional[List[Reference]] = field(default_factory=list)  # Additional information or supporting documentation about the authorization.
    case: Optional[BackboneElement] = None  # The case or regulatory procedure for granting or amending a regulated authorization. An authoriza...