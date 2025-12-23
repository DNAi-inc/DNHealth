# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Coverage resource.

Coverage represents financial or other arrangements for the provision of healthcare services.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CoverageCostToBeneficiaryException:
    """
    FHIR Coverage.costToBeneficiary.exception complex type.
    
    Exceptions for patient payments.
    """
    
    type: CodeableConcept  # Exception category (required)
    period: Optional[Period] = None  # The effective period of the exception
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageCostToBeneficiary:
    """
    FHIR Coverage.costToBeneficiary complex type.
    
    Patient payments for services/products.
    """
    
    type: Optional[CodeableConcept] = None  # Cost category
    valueQuantity: Optional[Quantity] = None  # The amount or percentage value of the coverage
    valueMoney: Optional[Money] = None  # The amount or percentage value of the coverage
    exception: List[CoverageCostToBeneficiaryException] = field(default_factory=list)  # Exceptions for patient payments
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageClass:
    """
    FHIR Coverage.class complex type.
    
    Additional coverage classifications.
    """
    
    type: CodeableConcept  # Type of class such as 'group' or 'plan' (required)
    value: str  # Value associated with the type (required)
    name: Optional[str] = None  # Human readable description of the type and value
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Coverage(DomainResource):
    """
    FHIR R4 Coverage resource.
    
    Represents financial or other arrangements for the provision of healthcare services.
    Extends DomainResource.
    """
    
    resourceType: str = "Coverage"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for the coverage
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (identifier has default value).
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | cancelled | draft | entered-in-error (required in FHIR)
    # Type
    type: Optional[CodeableConcept] = None  # Coverage category such as medical or accident
    # Policy Holder
    policyHolder: Optional[Reference] = None  # Owner of the policy
    # Subscriber
    subscriber: Optional[Reference] = None  # Subscriber to the policy
    # Subscriber ID
    subscriberId: Optional[str] = None  # ID assigned to the subscriber
    # Beneficiary
    # Note: beneficiary is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (subscriberId has default value).
    # Validation should enforce beneficiary is provided.
    beneficiary: Optional[Reference] = None  # Plan beneficiary (required in FHIR)
    # Dependent
    dependent: Optional[str] = None  # Dependent number
    # Relationship
    relationship: Optional[CodeableConcept] = None  # Beneficiary relationship to the subscriber
    # Period
    period: Optional[Period] = None  # Coverage start and end dates
    # Payor
    payor: List[Reference] = field(default_factory=list)  # Issuer of the policy
    # Class
    class_: List[CoverageClass] = field(default_factory=list)  # Additional coverage classifications
    # Order
    order: Optional[int] = None  # Relative order of the coverage
    # Network
    network: Optional[str] = None  # Insurer network
    # Cost To Beneficiary
    costToBeneficiary: List[CoverageCostToBeneficiary] = field(default_factory=list)  # Patient payments for services/products
    # Subrogation
    subrogation: Optional[bool] = None  # Reimbursement to insurer
    # Contract
    contract: List[Reference] = field(default_factory=list)  # Contract details

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


