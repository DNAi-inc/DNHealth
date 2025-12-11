# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Claim resource.

Claim represents a request for payment for goods and services rendered.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money, Quantity, Attachment
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ClaimRelated:
    """
    FHIR Claim.related complex type.
    
    Other claims which are related to this claim.
    """
    
    claim: Optional[Reference] = None  # Reference to the related claim
    relationship: Optional[CodeableConcept] = None  # How the claim reference is related
    reference: Optional[Identifier] = None  # File or case reference
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimPayee:
    """
    FHIR Claim.payee complex type.
    
    The party to be reimbursed for the services.
    """
    
    type: CodeableConcept  # Category of recipient (required)
    party: Optional[Reference] = None  # Party to receive the payment
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimCareTeam:
    """
    FHIR Claim.careTeam complex type.
    
    Members of the team who provided the products and services.
    """
    
    sequence: int  # Order of care team (required)
    provider: Reference  # Practitioner or organization (required)
    responsible: Optional[bool] = None  # Indicator of the lead practitioner
    role: Optional[CodeableConcept] = None  # Function within the team
    qualification: Optional[CodeableConcept] = None  # Practitioner credential or specialization
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimSupportingInfo:
    """
    FHIR Claim.supportingInfo complex type.
    
    Additional information codes regarding exceptions, special considerations, the condition, situation, prior or concurrent issues.
    """
    
    sequence: int  # Information instance identifier (required)
    category: CodeableConcept  # Classification of the supplied information (required)
    code: Optional[CodeableConcept] = None  # Type of information
    timingDate: Optional[str] = None  # When it occurred
    timingPeriod: Optional[Period] = None  # When it occurred
    valueBoolean: Optional[bool] = None  # Data to be provided
    valueString: Optional[str] = None  # Data to be provided
    valueQuantity: Optional[Quantity] = None  # Data to be provided
    valueAttachment: Optional[Attachment] = None  # Data to be provided
    valueReference: Optional[Reference] = None  # Data to be provided
    reason: Optional[CodeableConcept] = None  # Explanation for the information
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimDiagnosis:
    """
    FHIR Claim.diagnosis complex type.
    
    Information about diagnoses relevant to the claim items.
    """
    
    sequence: int  # Diagnosis instance identifier (required)
    diagnosisCodeableConcept: Optional[CodeableConcept] = None  # Nature of illness or problem
    diagnosisReference: Optional[Reference] = None  # Nature of illness or problem
    type: List[CodeableConcept] = field(default_factory=list)  # Timing or nature of the diagnosis
    onAdmission: Optional[CodeableConcept] = None  # Present on admission
    packageCode: Optional[CodeableConcept] = None  # Package billing code
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimProcedure:
    """
    FHIR Claim.procedure complex type.
    
    Procedures performed on the patient relevant to the billing items with the claim.
    """
    
    sequence: int  # Procedure instance identifier (required)
    type: List[CodeableConcept] = field(default_factory=list)  # Category of Procedure
    date: Optional[str] = None  # When the procedure was performed
    procedureCodeableConcept: Optional[CodeableConcept] = None  # Specific clinical procedure
    procedureReference: Optional[Reference] = None  # Specific clinical procedure
    udi: List[Reference] = field(default_factory=list)  # Unique device identifier
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimInsurance:
    """
    FHIR Claim.insurance complex type.
    
    Financial instruments for reimbursement for the health care products and services.
    """
    
    sequence: int  # Insurance instance identifier (required)
    focal: bool  # Coverage to be used for adjudication (required)
    coverage: Reference  # Insurance information (required)
    identifier: Optional[Identifier] = None  # Pre-assigned Claim number
    businessArrangement: Optional[str] = None  # Additional provider contract number
    preAuthRef: List[str] = field(default_factory=list)  # Prior authorization reference number
    claimResponse: Optional[Reference] = None  # Adjudication results
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimAccident:
    """
    FHIR Claim.accident complex type.
    
    Details of an accident which resulted in injuries which required the products and services listed in the claim.
    """
    
    date: str  # When the incident occurred (required)
    type: Optional[CodeableConcept] = None  # The nature of the accident
    locationAddress: Optional[Any] = None  # Where the event occurred
    locationReference: Optional[Reference] = None  # Where the event occurred
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimItemDetailSubDetail:
    """
    FHIR Claim.item.detail.subDetail complex type.
    
    Third-tier service code.
    """
    
    sequence: int  # Item instance identifier (required)
    productOrService: CodeableConcept  # Billing, service, product, or drug code (required)
    revenue: Optional[CodeableConcept] = None  # Revenue or cost center code
    category: Optional[CodeableConcept] = None  # Benefit classification
    modifier: List[CodeableConcept] = field(default_factory=list)  # Service/product billing modifiers
    programCode: List[CodeableConcept] = field(default_factory=list)  # Program specific reason
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    factor: Optional[float] = None  # Price scaling factor
    net: Optional[Money] = None  # Total item cost
    udi: List[Reference] = field(default_factory=list)  # Unique device identifier
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimItemDetail:
    """
    FHIR Claim.item.detail complex type.
    
    Second-tier service code.
    """
    
    sequence: int  # Item instance identifier (required)
    productOrService: CodeableConcept  # Billing, service, product, or drug code (required)
    revenue: Optional[CodeableConcept] = None  # Revenue or cost center code
    category: Optional[CodeableConcept] = None  # Benefit classification
    modifier: List[CodeableConcept] = field(default_factory=list)  # Service/product billing modifiers
    programCode: List[CodeableConcept] = field(default_factory=list)  # Program specific reason
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    factor: Optional[float] = None  # Price scaling factor
    net: Optional[Money] = None  # Total item cost
    udi: List[Reference] = field(default_factory=list)  # Unique device identifier
    subDetail: List[ClaimItemDetailSubDetail] = field(default_factory=list)  # Product or service provided
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimItem:
    """
    FHIR Claim.item complex type.
    
    A claim line. Either a simple product or service or a 'group' of details which can each be a simple items or groups of sub-details.
    """
    
    sequence: int  # Item instance identifier (required)
    productOrService: CodeableConcept  # Billing, service, product, or drug code (required)
    careTeamSequence: List[int] = field(default_factory=list)  # Applicable careTeam members
    diagnosisSequence: List[int] = field(default_factory=list)  # Applicable diagnoses
    procedureSequence: List[int] = field(default_factory=list)  # Applicable procedures
    informationSequence: List[int] = field(default_factory=list)  # Applicable exception and supporting information
    revenue: Optional[CodeableConcept] = None  # Revenue or cost center code
    category: Optional[CodeableConcept] = None  # Benefit classification
    modifier: List[CodeableConcept] = field(default_factory=list)  # Product or service billing modifiers
    programCode: List[CodeableConcept] = field(default_factory=list)  # Program the product or service is provided under
    servicedDate: Optional[str] = None  # Date or dates of service or product delivery
    servicedPeriod: Optional[Period] = None  # Date or dates of service or product delivery
    locationCodeableConcept: Optional[CodeableConcept] = None  # Place of service or where product was supplied
    locationAddress: Optional[Any] = None  # Place of service or where product was supplied
    locationReference: Optional[Reference] = None  # Place of service or where product was supplied
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    factor: Optional[float] = None  # Price scaling factor
    net: Optional[Money] = None  # Total item cost
    udi: List[Reference] = field(default_factory=list)  # Unique device identifier
    bodySite: Optional[CodeableConcept] = None  # Anatomical location
    subSite: List[CodeableConcept] = field(default_factory=list)  # Anatomical sub-location
    encounter: List[Reference] = field(default_factory=list)  # Encounters related to this billed item
    detail: List[ClaimItemDetail] = field(default_factory=list)  # Product or service provided
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass(kw_only=True)
class Claim(DomainResource):
    """
    FHIR R4 Claim resource.
    
    Represents a request for payment for goods and services rendered.
    Extends DomainResource.
    """
    
    resourceType: str = "Claim"
    # Required fields (must come before optional fields)
    # Status
    status: str  # active | cancelled | draft | entered-in-error (required)
    # Type
    type: CodeableConcept  # Category or discipline (required)
    # Use
    use: str  # claim | preauthorization | predetermination (required)
    # Patient
    patient: Reference  # The recipient of the products and services (required)
    # Created
    created: str  # Resource creation date (required)
    # Provider
    provider: Reference  # Party responsible for the claim (required)
    # Priority
    priority: CodeableConcept  # Desired processing priority (required)
    # Optional fields
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for claim
    # Sub Type
    subType: Optional[CodeableConcept] = None  # More granular claim type
    # Billable Period
    billablePeriod: Optional[Period] = None  # Relevant time frame for the claim
    # Enterer
    enterer: Optional[Reference] = None  # Author of the claim
    # Insurer
    insurer: Optional[Reference] = None  # Target
    # Funds Reserve
    fundsReserve: Optional[CodeableConcept] = None  # For whom to reserve funds
    # Related
    related: List[ClaimRelated] = field(default_factory=list)  # Related claims
    # Prescription
    prescription: Optional[Reference] = None  # Prescription authorizing services or products
    # Original Prescription
    originalPrescription: Optional[Reference] = None  # Original prescription if superceded by fulfiller
    # Payee
    payee: Optional[ClaimPayee] = None  # Recipient of benefits payable
    # Referral
    referral: Optional[Reference] = None  # Treatment referral
    # Facility
    facility: Optional[Reference] = None  # Servicing facility
    # Care Team
    careTeam: List[ClaimCareTeam] = field(default_factory=list)  # Members of the team
    # Supporting Info
    supportingInfo: List[ClaimSupportingInfo] = field(default_factory=list)  # Supporting information
    # Diagnosis
    diagnosis: List[ClaimDiagnosis] = field(default_factory=list)  # Pertinent diagnosis information
    # Procedure
    procedure: List[ClaimProcedure] = field(default_factory=list)  # Clinical procedures performed
    # Insurance
    insurance: List[ClaimInsurance] = field(default_factory=list)  # Patient insurance information
    # Accident
    accident: Optional[ClaimAccident] = None  # Details of the event
    # Item
    item: List[ClaimItem] = field(default_factory=list)  # Product or service provided
    # Total
    total: Optional[Money] = None  # Total claim cost

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


