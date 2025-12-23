# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 CoverageEligibilityResponse resource.

This resource provides eligibility and plan details from the processing of an CoverageEligibilityRequest resource.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Reference
from typing import Any, List, Optional

@dataclass
class CoverageEligibilityResponseEvent:
    """
    CoverageEligibilityResponseEvent nested class.
    """

    type: Optional[CodeableConcept] = None  # A coded event such as when a service is expected or a card printed.
    when: Optional[Any] = None  # A date or period in the past or future indicating when the event occurred or is expectd to occur.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class CoverageEligibilityResponseInsurance:
    """
    CoverageEligibilityResponseInsurance nested class.
    """

    coverage: Optional[Reference] = None  # Reference to the insurance card level information contained in the Coverage resource. The coverag...
    type: Optional[CodeableConcept] = None  # Classification of benefit being provided.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    inforce: Optional[bool] = None  # Flag indicating if the coverage provided is inforce currently if no service date(s) specified or ...
    benefitPeriod: Optional[Period] = None  # The term of the benefits documented in this response.
    item: Optional[List[BackboneElement]] = field(default_factory=list)  # Benefits and optionally current balances, and authorization details by category or service.
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    productOrService: Optional[CodeableConcept] = None  # This contains the product, service, drug or other billing code for the item.
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    provider: Optional[Reference] = None  # The practitioner who is eligible for the provision of the product or service.
    excluded: Optional[bool] = None  # True if the indicated class of service is excluded from the plan, missing or False indicates the ...
    name: Optional[str] = None  # A short name or tag for the benefit.
    description: Optional[str] = None  # A richer description of the benefit or services covered.
    network: Optional[CodeableConcept] = None  # Is a flag to indicate whether the benefits refer to in-network providers or out-of-network provid...
    unit: Optional[CodeableConcept] = None  # Indicates if the benefits apply to an individual or to the family.
    term: Optional[CodeableConcept] = None  # The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'.
    benefit: Optional[List[BackboneElement]] = field(default_factory=list)  # Benefits used to date.
    allowed: Optional[Any] = None  # The quantity of the benefit which is permitted under the coverage.
    used: Optional[Any] = None  # The quantity of the benefit which have been consumed to date.
    authorizationRequired: Optional[bool] = None  # A boolean flag indicating whether a preauthorization is required prior to actual service delivery.
    authorizationSupporting: Optional[List[CodeableConcept]] = field(default_factory=list)  # Codes or comments regarding information or actions associated with the preauthorization.
    authorizationUrl: Optional[str] = None  # A web location for obtaining requirements or descriptive information regarding the preauthorization.

@dataclass
class CoverageEligibilityResponseInsuranceItem:
    """
    CoverageEligibilityResponseInsuranceItem nested class.
    """

    type: Optional[CodeableConcept] = None  # Classification of benefit being provided.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    productOrService: Optional[CodeableConcept] = None  # This contains the product, service, drug or other billing code for the item.
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    provider: Optional[Reference] = None  # The practitioner who is eligible for the provision of the product or service.
    excluded: Optional[bool] = None  # True if the indicated class of service is excluded from the plan, missing or False indicates the ...
    name: Optional[str] = None  # A short name or tag for the benefit.
    description: Optional[str] = None  # A richer description of the benefit or services covered.
    network: Optional[CodeableConcept] = None  # Is a flag to indicate whether the benefits refer to in-network providers or out-of-network provid...
    unit: Optional[CodeableConcept] = None  # Indicates if the benefits apply to an individual or to the family.
    term: Optional[CodeableConcept] = None  # The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'.
    benefit: Optional[List[BackboneElement]] = field(default_factory=list)  # Benefits used to date.
    allowed: Optional[Any] = None  # The quantity of the benefit which is permitted under the coverage.
    used: Optional[Any] = None  # The quantity of the benefit which have been consumed to date.
    authorizationRequired: Optional[bool] = None  # A boolean flag indicating whether a preauthorization is required prior to actual service delivery.
    authorizationSupporting: Optional[List[CodeableConcept]] = field(default_factory=list)  # Codes or comments regarding information or actions associated with the preauthorization.
    authorizationUrl: Optional[str] = None  # A web location for obtaining requirements or descriptive information regarding the preauthorization.

@dataclass
class CoverageEligibilityResponseInsuranceItemBenefit:
    """
    CoverageEligibilityResponseInsuranceItemBenefit nested class.
    """

    type: Optional[CodeableConcept] = None  # Classification of benefit being provided.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    allowed: Optional[Any] = None  # The quantity of the benefit which is permitted under the coverage.
    used: Optional[Any] = None  # The quantity of the benefit which have been consumed to date.

@dataclass
class CoverageEligibilityResponseError:
    """
    CoverageEligibilityResponseError nested class.
    """

    code: Optional[CodeableConcept] = None  # An error code,from a specified code system, which details why the eligibility check could not be ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    expression: Optional[List[str]] = field(default_factory=list)  # A [simple subset of FHIRPath](fhirpath.html#simple) limited to element names, repetition indicato...


@dataclass
class CoverageEligibilityResponse(FHIRResource):
    """
    This resource provides eligibility and plan details from the processing of an CoverageEligibilityRequest resource.
    """

    status: Optional[str] = None  # The status of the resource instance.
    purpose: List[str] = field(default_factory=list)  # Code to specify whether requesting: prior authorization requirements for some service categories ...
    patient: Optional[Reference] = None  # The party who is the beneficiary of the supplied coverage and for whom eligibility is sought.
    created: Optional[str] = None  # The date this resource was created.
    request: Optional[Reference] = None  # Reference to the original request resource.
    outcome: Optional[str] = None  # The outcome of the request processing.
    insurer: Optional[Reference] = None  # The Insurer who issued the coverage in question and is the author of the response.
    resourceType: str = "CoverageEligibilityResponse"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this coverage eligiblity request.
    event: Optional[List[BackboneElement]] = field(default_factory=list)  # Information code for an event with a corresponding date or period.
    serviced: Optional[Any] = None  # The date or dates when the enclosed suite of services were performed or completed.
    requestor: Optional[Reference] = None  # The provider which is responsible for the request.
    disposition: Optional[str] = None  # A human readable description of the status of the adjudication.
    insurance: Optional[List[BackboneElement]] = field(default_factory=list)  # Financial instruments for reimbursement for the health care products and services.
    preAuthRef: Optional[str] = None  # A reference from the Insurer to which these services pertain to be used on further communication ...
    form: Optional[CodeableConcept] = None  # A code for the form to be used for printing the content.
    error: Optional[List[BackboneElement]] = field(default_factory=list)  # Errors encountered during the processing of the request.