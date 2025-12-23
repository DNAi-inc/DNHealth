# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 InsurancePlan resource.

Details of a Health Insurance product/plan provided by an organization.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class InsurancePlanCoverage:
    """
    InsurancePlanCoverage nested class.
    """

    type: Optional[CodeableConcept] = None  # Type of coverage  (Medical; Dental; Mental Health; Substance Abuse; Vision; Drug; Short Term; Lon...
    benefit: List[BackboneElement] = field(default_factory=list)  # Specific benefits under this type of coverage.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    network: Optional[List[Reference]] = field(default_factory=list)  # Reference to the network that providing the type of coverage.
    requirement: Optional[str] = None  # The referral requirements to have access/coverage for this benefit.
    limit: Optional[List[BackboneElement]] = field(default_factory=list)  # The specific limits on the benefit.
    value: Optional[Quantity] = None  # The maximum amount of a service item a plan will pay for a covered benefit.  For examples. wellne...
    code: Optional[CodeableConcept] = None  # The specific limit on the benefit.

@dataclass
class InsurancePlanCoverageBenefit:
    """
    InsurancePlanCoverageBenefit nested class.
    """

    type: Optional[CodeableConcept] = None  # Type of benefit (primary care; speciality care; inpatient; outpatient).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    requirement: Optional[str] = None  # The referral requirements to have access/coverage for this benefit.
    limit: Optional[List[BackboneElement]] = field(default_factory=list)  # The specific limits on the benefit.
    value: Optional[Quantity] = None  # The maximum amount of a service item a plan will pay for a covered benefit.  For examples. wellne...
    code: Optional[CodeableConcept] = None  # The specific limit on the benefit.

@dataclass
class InsurancePlanCoverageBenefitLimit:
    """
    InsurancePlanCoverageBenefitLimit nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Quantity] = None  # The maximum amount of a service item a plan will pay for a covered benefit.  For examples. wellne...
    code: Optional[CodeableConcept] = None  # The specific limit on the benefit.

@dataclass
class InsurancePlanPlan:
    """
    InsurancePlanPlan nested class.
    """

    category: Optional[CodeableConcept] = None  # General category of benefit (Medical; Dental; Vision; Drug; Mental Health; Substance Abuse; Hospi...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this health insurance plan which remain constant as the resource...
    type: Optional[CodeableConcept] = None  # Type of plan. For example, \"Platinum\" or \"High Deductable\".
    coverageArea: Optional[List[Reference]] = field(default_factory=list)  # The geographic region in which a health insurance plan's benefits apply.
    network: Optional[List[Reference]] = field(default_factory=list)  # Reference to the network that providing the type of coverage.
    generalCost: Optional[List[BackboneElement]] = field(default_factory=list)  # Overall costs associated with the plan.
    groupSize: Optional[int] = None  # Number of participants enrolled in the plan.
    cost: Optional[Money] = None  # Value of the cost.
    comment: Optional[str] = None  # Additional information about the general costs associated with this plan.
    specificCost: Optional[List[BackboneElement]] = field(default_factory=list)  # Costs associated with the coverage provided by the product.
    benefit: Optional[List[BackboneElement]] = field(default_factory=list)  # List of the specific benefits under this category of benefit.
    applicability: Optional[CodeableConcept] = None  # Whether the cost applies to in-network or out-of-network providers (in-network; out-of-network; o...
    qualifiers: Optional[List[CodeableConcept]] = field(default_factory=list)  # Additional information about the cost, such as information about funding sources (e.g. HSA, HRA, ...
    value: Optional[Quantity] = None  # The actual cost value. (some of the costs may be represented as percentages rather than currency,...

@dataclass
class InsurancePlanPlanGeneralCost:
    """
    InsurancePlanPlanGeneralCost nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Type of cost.
    groupSize: Optional[int] = None  # Number of participants enrolled in the plan.
    cost: Optional[Money] = None  # Value of the cost.
    comment: Optional[str] = None  # Additional information about the general costs associated with this plan.

@dataclass
class InsurancePlanPlanSpecificCost:
    """
    InsurancePlanPlanSpecificCost nested class.
    """

    category: Optional[CodeableConcept] = None  # General category of benefit (Medical; Dental; Vision; Drug; Mental Health; Substance Abuse; Hospi...
    type: Optional[CodeableConcept] = None  # Type of specific benefit (preventative; primary care office visit; speciality office visit; hospi...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    benefit: Optional[List[BackboneElement]] = field(default_factory=list)  # List of the specific benefits under this category of benefit.
    cost: Optional[List[BackboneElement]] = field(default_factory=list)  # List of the costs associated with a specific benefit.
    applicability: Optional[CodeableConcept] = None  # Whether the cost applies to in-network or out-of-network providers (in-network; out-of-network; o...
    qualifiers: Optional[List[CodeableConcept]] = field(default_factory=list)  # Additional information about the cost, such as information about funding sources (e.g. HSA, HRA, ...
    value: Optional[Quantity] = None  # The actual cost value. (some of the costs may be represented as percentages rather than currency,...

@dataclass
class InsurancePlanPlanSpecificCostBenefit:
    """
    InsurancePlanPlanSpecificCostBenefit nested class.
    """

    type: Optional[CodeableConcept] = None  # Type of specific benefit (preventative; primary care office visit; speciality office visit; hospi...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    cost: Optional[List[BackboneElement]] = field(default_factory=list)  # List of the costs associated with a specific benefit.
    applicability: Optional[CodeableConcept] = None  # Whether the cost applies to in-network or out-of-network providers (in-network; out-of-network; o...
    qualifiers: Optional[List[CodeableConcept]] = field(default_factory=list)  # Additional information about the cost, such as information about funding sources (e.g. HSA, HRA, ...
    value: Optional[Quantity] = None  # The actual cost value. (some of the costs may be represented as percentages rather than currency,...

@dataclass
class InsurancePlanPlanSpecificCostBenefitCost:
    """
    InsurancePlanPlanSpecificCostBenefitCost nested class.
    """

    type: Optional[CodeableConcept] = None  # Type of cost (copay; individual cap; family cap; coinsurance; deductible).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    applicability: Optional[CodeableConcept] = None  # Whether the cost applies to in-network or out-of-network providers (in-network; out-of-network; o...
    qualifiers: Optional[List[CodeableConcept]] = field(default_factory=list)  # Additional information about the cost, such as information about funding sources (e.g. HSA, HRA, ...
    value: Optional[Quantity] = None  # The actual cost value. (some of the costs may be represented as percentages rather than currency,...


@dataclass
class InsurancePlan(FHIRResource):
    """
    Details of a Health Insurance product/plan provided by an organization.
    """

    resourceType: str = "InsurancePlan"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this health insurance product which remain constant as the resou...
    status: Optional[str] = None  # The current state of the health insurance product.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The kind of health insurance product.
    name: Optional[str] = None  # Official name of the health insurance product as designated by the owner.
    alias: Optional[List[str]] = field(default_factory=list)  # A list of alternate names that the product is known as, or was known as in the past.
    period: Optional[Period] = None  # The period of time that the health insurance product is available.
    ownedBy: Optional[Reference] = None  # The entity that is providing  the health insurance product and underwriting the risk.  This is ty...
    administeredBy: Optional[Reference] = None  # An organization which administer other services such as underwriting, customer service and/or cla...
    coverageArea: Optional[List[Reference]] = field(default_factory=list)  # The geographic region in which a health insurance product's benefits apply.
    contact: Optional[List[Any]] = field(default_factory=list)  # The contact details of communication devices available relevant to the specific Insurance Plan/Pr...
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # The technical endpoints providing access to services operated for the health insurance product.
    network: Optional[List[Reference]] = field(default_factory=list)  # Reference to the network included in the health insurance product.
    coverage: Optional[List[BackboneElement]] = field(default_factory=list)  # Details about the coverage offered by the insurance product.
    plan: Optional[List[BackboneElement]] = field(default_factory=list)  # Details about an insurance plan.