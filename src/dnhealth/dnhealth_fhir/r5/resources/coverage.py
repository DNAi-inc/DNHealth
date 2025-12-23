# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Coverage resource.

Financial instrument which may be used to reimburse or pay for health care products and services. Includes both insurance and self-payment.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class CoveragePaymentBy:
    """
    CoveragePaymentBy nested class.
    """

    party: Optional[Reference] = None  # The list of parties providing non-insurance payment for the treatment costs.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    responsibility: Optional[str] = None  #  Description of the financial responsibility.

@dataclass
class CoverageClass:
    """
    CoverageClass nested class.
    """

    type: Optional[CodeableConcept] = None  # The type of classification for which an insurer-specific class label or number and optional name ...
    value: Optional[Identifier] = None  # The alphanumeric identifier associated with the insurer issued label.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # A short description for the class.

@dataclass
class CoverageCostToBeneficiary:
    """
    CoverageCostToBeneficiary nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The category of patient centric costs associated with treatment.
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    network: Optional[CodeableConcept] = None  # Is a flag to indicate whether the benefits refer to in-network providers or out-of-network provid...
    unit: Optional[CodeableConcept] = None  # Indicates if the benefits apply to an individual or to the family.
    term: Optional[CodeableConcept] = None  # The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'.
    value: Optional[Any] = None  # The amount due from the patient for the cost category.
    exception: Optional[List[BackboneElement]] = field(default_factory=list)  # A suite of codes indicating exceptions or reductions to patient costs and their effective periods.
    period: Optional[Period] = None  # The timeframe the exception is in force.

@dataclass
class CoverageCostToBeneficiaryException:
    """
    CoverageCostToBeneficiaryException nested class.
    """

    type: Optional[CodeableConcept] = None  # The code for the specific exception.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    period: Optional[Period] = None  # The timeframe the exception is in force.


@dataclass
class Coverage(FHIRResource):
    """
    Financial instrument which may be used to reimburse or pay for health care products and services. Includes both insurance and self-payment.
    """

    status: Optional[str] = None  # The status of the resource instance.
    kind: Optional[str] = None  # The nature of the coverage be it insurance, or cash payment such as self-pay.
    beneficiary: Optional[Reference] = None  # The party who benefits from the insurance coverage; the patient when products and/or services are...
    resourceType: str = "Coverage"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The identifier of the coverage as issued by the insurer.
    paymentBy: Optional[List[BackboneElement]] = field(default_factory=list)  # Link to the paying party and optionally what specifically they will be responsible to pay.
    type: Optional[CodeableConcept] = None  # The type of coverage: social program, medical plan, accident coverage (workers compensation, auto...
    policyHolder: Optional[Reference] = None  # The party who 'owns' the insurance policy.
    subscriber: Optional[Reference] = None  # The party who has signed-up for or 'owns' the contractual relationship to the policy or to whom t...
    subscriberId: Optional[List[Identifier]] = field(default_factory=list)  # The insurer assigned ID for the Subscriber.
    dependent: Optional[str] = None  # A designator for a dependent under the coverage.
    relationship: Optional[CodeableConcept] = None  # The relationship of beneficiary (patient) to the subscriber.
    period: Optional[Period] = None  # Time period during which the coverage is in force. A missing start date indicates the start date ...
    insurer: Optional[Reference] = None  # The program or plan underwriter, payor, insurance company.
    class_: Optional[List[BackboneElement]] = field(default_factory=list)  # A suite of underwriter specific classifiers.
    order: Optional[int] = None  # The order of applicability of this coverage relative to other coverages which are currently in fo...
    network: Optional[str] = None  # The insurer-specific identifier for the insurer-defined network of providers to which the benefic...
    costToBeneficiary: Optional[List[BackboneElement]] = field(default_factory=list)  # A suite of codes indicating the cost category and associated amount which have been detailed in t...
    subrogation: Optional[bool] = None  # When 'subrogation=true' this insurance instance has been included not for adjudication but to pro...
    contract: Optional[List[Reference]] = field(default_factory=list)  # The policy(s) which constitute this insurance coverage.
    insurancePlan: Optional[Reference] = None  # The insurance plan details, benefits and costs, which constitute this insurance coverage.