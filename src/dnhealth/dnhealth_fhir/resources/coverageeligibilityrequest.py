# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CoverageEligibilityRequest resource.

CoverageEligibilityRequest represents a request for coverage eligibility determination.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CoverageEligibilityRequestSupportingInfo:
    """
    FHIR CoverageEligibilityRequest.supportingInfo complex type.
    
    Additional information codes regarding exceptions, special considerations.
    """
    
    sequence: int  # Information instance identifier (required)
    information: Reference  # Data to be provided (required)
    appliesToAll: Optional[bool] = None  # Applies to all items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityRequestInsurance:
    """
    FHIR CoverageEligibilityRequest.insurance complex type.
    
    Financial instruments for reimbursement for the health care products and services.
    """
    
    focal: Optional[bool] = None  # Applicable coverage
    coverage: Reference  # Insurance information (required)
    businessArrangement: Optional[str] = None  # Additional provider contract number
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityRequestItemDiagnosis:
    """
    FHIR CoverageEligibilityRequest.item.diagnosis complex type.
    
    Patient diagnosis for which care is sought.
    """
    
    diagnosisCodeableConcept: Optional[CodeableConcept] = None  # Nature of illness or injury
    diagnosisReference: Optional[Reference] = None  # Nature of illness or injury
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityRequestItem:
    """
    FHIR CoverageEligibilityRequest.item complex type.
    
    Service categories or billable services for which benefit details and/or an authorization prior to service delivery may be required.
    """
    
    supportingInfoSequence: List[int] = field(default_factory=list)  # Applicable exception or supporting information
    category: Optional[CodeableConcept] = None  # Benefit classification
    productOrService: Optional[CodeableConcept] = None  # Billing, service, product, or drug code
    modifier: List[CodeableConcept] = field(default_factory=list)  # Product or service billing modifiers
    provider: Optional[Reference] = None  # Performing practitioner
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    facility: Optional[Reference] = None  # Servicing facility
    diagnosis: List[CoverageEligibilityRequestItemDiagnosis] = field(default_factory=list)  # Applicable diagnoses
    detail: List[Reference] = field(default_factory=list)  # Product or service details
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityRequest(DomainResource):
    """
    FHIR R4 CoverageEligibilityRequest resource.
    
    Represents a request for coverage eligibility determination.
    Extends DomainResource.
    """
    
    resourceType: str = "CoverageEligibilityRequest"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for coverage eligiblity request
    # Status
    status: str  # active | cancelled | draft | entered-in-error (required)
    # Priority
    priority: Optional[CodeableConcept] = None  # Desired processing priority
    # Purpose
    purpose: List[str] = field(default_factory=list)  # auth-requirements | benefits | discovery | validation
    # Patient
    patient: Reference  # The recipient of the products and services (required)
    # Serviced Date
    servicedDate: Optional[str] = None  # Estimated date or dates of service
    # Serviced Period
    servicedPeriod: Optional[Period] = None  # Estimated date or dates of service
    # Created
    created: str  # Creation date (required)
    # Enterer
    enterer: Optional[Reference] = None  # Author
    # Provider
    provider: Optional[Reference] = None  # Responsible practitioner
    # Insurer
    insurer: Reference  # Coverage issuer (required)
    # Facility
    facility: Optional[Reference] = None  # Servicing facility
    # Supporting Info
    supportingInfo: List[CoverageEligibilityRequestSupportingInfo] = field(default_factory=list)  # Supporting information
    # Insurance
    insurance: List[CoverageEligibilityRequestInsurance] = field(default_factory=list)  # Patient insurance information
    # Item
    item: List[CoverageEligibilityRequestItem] = field(default_factory=list)  # Item to be evaluated for eligibiity

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


