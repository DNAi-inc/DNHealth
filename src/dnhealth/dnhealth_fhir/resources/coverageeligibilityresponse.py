# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CoverageEligibilityResponse resource.

CoverageEligibilityResponse represents the response to a coverage eligibility request.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CoverageEligibilityResponseInsuranceItemBenefit:
    """
    FHIR CoverageEligibilityResponse.insurance.item.benefit complex type.
    
    Benefits and authorization details.
    """
    
    type: CodeableConcept  # Benefit classification (required)
    allowedUnsignedInt: Optional[int] = None  # Benefits allowed
    allowedString: Optional[str] = None  # Benefits allowed
    allowedMoney: Optional[Money] = None  # Benefits allowed
    usedUnsignedInt: Optional[int] = None  # Benefits used
    usedString: Optional[str] = None  # Benefits used
    usedMoney: Optional[Money] = None  # Benefits used
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityResponseInsuranceItem:
    """
    FHIR CoverageEligibilityResponse.insurance.item complex type.
    
    Benefits and authorization details.
    """
    
    category: Optional[CodeableConcept] = None  # Benefit classification
    productOrService: Optional[CodeableConcept] = None  # Billing, service, product, or drug code
    modifier: List[CodeableConcept] = field(default_factory=list)  # Product or service billing modifiers
    provider: Optional[Reference] = None  # Performing practitioner
    excluded: Optional[bool] = None  # Excluded from the plan
    name: Optional[str] = None  # Short name for the benefit
    description: Optional[str] = None  # Description of the benefit or services covered
    network: Optional[CodeableConcept] = None  # In or out of network
    unit: Optional[CodeableConcept] = None  # Individual or family
    term: Optional[CodeableConcept] = None  # Annual or lifetime
    benefit: List[CoverageEligibilityResponseInsuranceItemBenefit] = field(default_factory=list)  # Benefits and authorization details
    authorizationRequired: Optional[bool] = None  # Authorization required flag
    authorizationSupporting: List[CodeableConcept] = field(default_factory=list)  # Type of required supporting materials
    authorizationUrl: Optional[str] = None  # Preauthorization requirements endpoint
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityResponseInsurance:
    """
    FHIR CoverageEligibilityResponse.insurance complex type.
    
    Patient insurance information.
    """
    
    coverage: Reference  # Insurance information (required)
    inforce: Optional[bool] = None  # Coverage inforce indicator
    benefitPeriod: Optional[Period] = None  # When the benefits are applicable
    item: List[CoverageEligibilityResponseInsuranceItem] = field(default_factory=list)  # Benefits and authorization details
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityResponseError:
    """
    FHIR CoverageEligibilityResponse.error complex type.
    
    Errors encountered during the processing of the request.
    """
    
    code: CodeableConcept  # Error code detailing processing issues (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CoverageEligibilityResponse(DomainResource):
    """
    FHIR R4 CoverageEligibilityResponse resource.
    
    Represents the response to a coverage eligibility request.
    Extends DomainResource.
    """
    
    resourceType: str = "CoverageEligibilityResponse"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for coverage eligiblity response
    # Status
    status: str  # active | cancelled | draft | entered-in-error (required)
    # Purpose
    purpose: List[str] = field(default_factory=list)  # auth-requirements | benefits | discovery | validation
    # Patient
    patient: Reference  # The recipient of the products and services (required)
    # Serviced Date
    servicedDate: Optional[str] = None  # Estimated date or dates of service
    # Serviced Period
    servicedPeriod: Optional[Period] = None  # Estimated date or dates of service
    # Created
    created: str  # Response creation date (required)
    # Requestor
    requestor: Optional[Reference] = None  # Party responsible for the request
    # Request
    request: Reference  # Eligibility request reference (required)
    # Outcome
    outcome: str  # queued | complete | error | partial (required)
    # Disposition
    disposition: Optional[str] = None  # Disposition Message
    # Insurer
    insurer: Reference  # Coverage issuer (required)
    # Insurance
    insurance: List[CoverageEligibilityResponseInsurance] = field(default_factory=list)  # Patient insurance information
    # Pre Auth Ref
    preAuthRef: Optional[str] = None  # Preauthorization reference
    # Form
    form: Optional[CodeableConcept] = None  # Printed form identifier
    # Error
    error: List[CoverageEligibilityResponseError] = field(default_factory=list)  # Processing errors

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


