# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 InsurancePlan resource.

InsurancePlan represents details of a health insurance product/plan.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, ContactPoint, ContactDetail
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class InsurancePlanContact:
    """
    FHIR InsurancePlan.contact complex type.
    
    Contact for the health insurance product.
    """
    
    purpose: Optional[CodeableConcept] = None  # The type of contact
    name: Optional[Any] = None  # A name associated with the contact (HumanName)
    telecom: List[ContactPoint] = field(default_factory=list)  # Contact details
    address: Optional[Any] = None  # Visiting or postal address for the contact (Address)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanCoverageBenefitLimit:
    """
    FHIR InsurancePlan.coverage.benefit.limit complex type.
    
    Benefit limits.
    """
    
    value: Optional[Any] = None  # Maximum value allowed (Quantity)
    code: Optional[CodeableConcept] = None  # Benefit limit details
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanCoverageBenefit:
    """
    FHIR InsurancePlan.coverage.benefit complex type.
    
    Specific benefits under this type of coverage.
    """
    
    type: CodeableConcept  # Type of benefit (required)
    requirement: Optional[str] = None  # Referral requirements
    limit: List[InsurancePlanCoverageBenefitLimit] = field(default_factory=list)  # Benefit limits
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanCoverage:
    """
    FHIR InsurancePlan.coverage complex type.
    
    Coverage details.
    """
    
    type: CodeableConcept  # Type of coverage (required)
    network: List[Reference] = field(default_factory=list)  # What networks provide coverage
    benefit: List[InsurancePlanCoverageBenefit] = field(default_factory=list)  # Specific benefits under this type of coverage (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanPlanGeneralCost:
    """
    FHIR InsurancePlan.plan.generalCost complex type.
    
    Overall costs.
    """
    
    type: Optional[CodeableConcept] = None  # Type of cost
    groupSize: Optional[int] = None  # Number of enrollees
    cost: Optional[Any] = None  # Cost value (Money)
    comment: Optional[str] = None  # Additional cost information
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanPlanSpecificCostBenefitCost:
    """
    FHIR InsurancePlan.plan.specificCost.benefit.cost complex type.
    
    List of the costs.
    """
    
    type: CodeableConcept  # Type of cost (required)
    applicability: Optional[CodeableConcept] = None  # in-network | out-of-network | other
    qualifiers: List[CodeableConcept] = field(default_factory=list)  # Additional information about the cost
    value: Optional[Any] = None  # The actual cost value (Quantity)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanPlanSpecificCostBenefit:
    """
    FHIR InsurancePlan.plan.specificCost.benefit complex type.
    
    Specific benefits.
    """
    
    type: CodeableConcept  # Type of specific benefit (required)
    cost: List[InsurancePlanPlanSpecificCostBenefitCost] = field(default_factory=list)  # List of the costs
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanPlanSpecificCost:
    """
    FHIR InsurancePlan.plan.specificCost complex type.
    
    Costs associated with the plan.
    """
    
    category: CodeableConcept  # General category of benefit (required)
    benefit: List[InsurancePlanPlanSpecificCostBenefit] = field(default_factory=list)  # Specific benefits
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlanPlan:
    """
    FHIR InsurancePlan.plan complex type.
    
    Details about an insurance plan.
    """
    
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier for the plan
    type: Optional[CodeableConcept] = None  # Type of plan
    coverageArea: List[Reference] = field(default_factory=list)  # Where product applies
    network: List[Reference] = field(default_factory=list)  # What networks provide coverage
    generalCost: List[InsurancePlanPlanGeneralCost] = field(default_factory=list)  # Overall costs
    specificCost: List[InsurancePlanPlanSpecificCost] = field(default_factory=list)  # Costs associated with the plan
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InsurancePlan(DomainResource):
    """
    FHIR R4 InsurancePlan resource.
    
    Represents details of a health insurance product/plan.
    Extends DomainResource.
    """
    
    resourceType: str = "InsurancePlan"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier for the plan
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown
    # Type
    type: List[CodeableConcept] = field(default_factory=list)  # Kind of product
    # Name
    name: Optional[str] = None  # Official name
    # Alias
    alias: List[str] = field(default_factory=list)  # Alternate names
    # Period
    period: Optional[Period] = None  # When the product is available
    # Owned By
    ownedBy: Optional[Reference] = None  # Plan issuer
    # Administered By
    administeredBy: Optional[Reference] = None  # Product administrator
    # Coverage Area
    coverageArea: List[Reference] = field(default_factory=list)  # Where product applies
    # Contact
    contact: List[InsurancePlanContact] = field(default_factory=list)  # Contact for the product
    # Endpoint
    endpoint: List[Reference] = field(default_factory=list)  # Technical endpoint
    # Network
    network: List[Reference] = field(default_factory=list)  # What networks are Included
    # Coverage
    coverage: List[InsurancePlanCoverage] = field(default_factory=list)  # Coverage details
    # Plan
    plan: List[InsurancePlanPlan] = field(default_factory=list)  # Plan details

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


