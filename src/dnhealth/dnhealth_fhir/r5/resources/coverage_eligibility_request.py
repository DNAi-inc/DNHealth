# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 CoverageEligibilityRequest resource.

The CoverageEligibilityRequest provides patient and insurance coverage information to an insurer for them to respond, in the form of an CoverageEligibilityResponse, with information regarding whether the stated coverage is valid and in-force and optionally to provide the insurance details of the policy.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class CoverageEligibilityRequestEvent:
    """
    CoverageEligibilityRequestEvent nested class.
    """

    type: Optional[CodeableConcept] = None  # A coded event such as when a service is expected or a card printed.
    when: Optional[Any] = None  # A date or period in the past or future indicating when the event occurred or is expectd to occur.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class CoverageEligibilityRequestSupportingInfo:
    """
    CoverageEligibilityRequestSupportingInfo nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify supporting information entries.
    information: Optional[Reference] = None  # Additional data or information such as resources, documents, images etc. including references to ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    appliesToAll: Optional[bool] = None  # The supporting materials are applicable for all detail items, product/servce categories and speci...

@dataclass
class CoverageEligibilityRequestInsurance:
    """
    CoverageEligibilityRequestInsurance nested class.
    """

    coverage: Optional[Reference] = None  # Reference to the insurance card level information contained in the Coverage resource. The coverag...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    focal: Optional[bool] = None  # A flag to indicate that this Coverage is to be used for evaluation of this request when set to true.
    businessArrangement: Optional[str] = None  # A business agreement number established between the provider and the insurer for special business...

@dataclass
class CoverageEligibilityRequestItem:
    """
    CoverageEligibilityRequestItem nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    supportingInfoSequence: Optional[List[int]] = field(default_factory=list)  # Exceptions, special conditions and supporting information applicable for this service or product ...
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    productOrService: Optional[CodeableConcept] = None  # This contains the product, service, drug or other billing code for the item.
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    provider: Optional[Reference] = None  # The practitioner who is responsible for the product or service to be rendered to the patient.
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # The amount charged to the patient by the provider for a single unit.
    facility: Optional[Reference] = None  # Facility where the services will be provided.
    diagnosis: Optional[List[BackboneElement]] = field(default_factory=list)  # Patient diagnosis for which care is sought.
    detail: Optional[List[Reference]] = field(default_factory=list)  # The plan/proposal/order describing the proposed service in detail.

@dataclass
class CoverageEligibilityRequestItemDiagnosis:
    """
    CoverageEligibilityRequestItemDiagnosis nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    diagnosis: Optional[Any] = None  # The nature of illness or problem in a coded form or as a reference to an external defined Condition.


@dataclass
class CoverageEligibilityRequest(FHIRResource):
    """
    The CoverageEligibilityRequest provides patient and insurance coverage information to an insurer for them to respond, in the form of an CoverageEligibilityResponse, with information regarding whether the stated coverage is valid and in-force and optionally to provide the insurance details of the policy.
    """

    status: Optional[str] = None  # The status of the resource instance.
    purpose: List[str] = field(default_factory=list)  # Code to specify whether requesting: prior authorization requirements for some service categories ...
    patient: Optional[Reference] = None  # The party who is the beneficiary of the supplied coverage and for whom eligibility is sought.
    created: Optional[str] = None  # The date when this resource was created.
    insurer: Optional[Reference] = None  # The Insurer who issued the coverage in question and is the recipient of the request.
    resourceType: str = "CoverageEligibilityRequest"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this coverage eligiblity request.
    priority: Optional[CodeableConcept] = None  # When the requestor expects the processor to complete processing.
    event: Optional[List[BackboneElement]] = field(default_factory=list)  # Information code for an event with a corresponding date or period.
    serviced: Optional[Any] = None  # The date or dates when the enclosed suite of services were performed or completed.
    enterer: Optional[Reference] = None  # Person who created the request.
    provider: Optional[Reference] = None  # The provider which is responsible for the request.
    facility: Optional[Reference] = None  # Facility where the services are intended to be provided.
    supportingInfo: Optional[List[BackboneElement]] = field(default_factory=list)  # Additional information codes regarding exceptions, special considerations, the condition, situati...
    insurance: Optional[List[BackboneElement]] = field(default_factory=list)  # Financial instruments for reimbursement for the health care products and services.
    item: Optional[List[BackboneElement]] = field(default_factory=list)  # Service categories or billable services for which benefit details and/or an authorization prior t...