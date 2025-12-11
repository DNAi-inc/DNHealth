# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ExplanationOfBenefit resource.

ExplanationOfBenefit explains what benefits were provided and why.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Money, Quantity, Attachment


@dataclass
class ExplanationOfBenefitRelated:
    """
    FHIR ExplanationOfBenefit.related complex type.
    
    Other claims which are related to this claim.
    """
    
    claim: Optional[Reference] = None  # Reference to the related claim
    relationship: Optional[CodeableConcept] = None  # How the claim reference relates to this claim
    reference: Optional[Identifier] = None  # File or case reference
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExplanationOfBenefitPayee:
    """
    FHIR ExplanationOfBenefit.payee complex type.
    
    Party to be paid any benefits payable.
    """
    
    type: Optional[CodeableConcept] = None  # Category of recipient
    party: Optional[Reference] = None  # Recipient reference
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExplanationOfBenefitCareTeam:
    """
    FHIR ExplanationOfBenefit.careTeam complex type.
    
    Care Team members.
    """
    
    sequence: int  # Order of care team (required)
    provider: Reference  # Practitioner or organization (required)
    responsible: Optional[bool] = None  # Indicator of the lead practitioner
    role: Optional[CodeableConcept] = None  # Function within the team
    qualification: Optional[CodeableConcept] = None  # Practitioner credential or specialization
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExplanationOfBenefitSupportingInfo:
    """
    FHIR ExplanationOfBenefit.supportingInfo complex type.
    
    Supporting information.
    """
    
    sequence: int  # Information instance identifier (required)
    category: CodeableConcept  # Classification of the supplied information (required)
    code: Optional[CodeableConcept] = None  # Type of information
    timingDate: Optional[str] = None  # When it occurred
    timingPeriod: Optional[Period] = None  # When it occurred
    valueString: Optional[str] = None  # Data to be provided
    valueQuantity: Optional[Quantity] = None  # Data to be provided
    valueAttachment: Optional[Attachment] = None  # Data to be provided
    valueReference: Optional[Reference] = None  # Data to be provided
    reason: Optional[CodeableConcept] = None  # Explanation for the information
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExplanationOfBenefitDiagnosis:
    """
    FHIR ExplanationOfBenefit.diagnosis complex type.
    
    Pertinent diagnosis information.
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
class ExplanationOfBenefitProcedure:
    """
    FHIR ExplanationOfBenefit.procedure complex type.
    
    Clinical procedures performed.
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
class ExplanationOfBenefit(DomainResource):
    """
    FHIR R4 ExplanationOfBenefit resource.
    
    Explains what benefits were provided and why.
    Extends DomainResource.
    """
    
    resourceType: str = "ExplanationOfBenefit"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for the resource
    # Status
    status: str  # active | cancelled | draft | entered-in-error (required)
    # Type
    type: CodeableConcept  # Category or discipline (required)
    # Sub Type
    subType: Optional[CodeableConcept] = None  # More granular claim type
    # Use
    use: str  # claim | preauthorization | predetermination (required)
    # Patient
    patient: Reference  # The recipient of the products and services (required)
    # Billable Period
    billablePeriod: Optional[Period] = None  # Relevant time frame for the claim
    # Created
    created: str  # Creation date (required)
    # Enterer
    enterer: Optional[Reference] = None  # Author of the claim
    # Insurer
    insurer: Reference  # Party responsible for reimbursement (required)
    # Provider
    provider: Reference  # Party responsible for the claim (required)
    # Priority
    priority: Optional[CodeableConcept] = None  # Desired processing urgency
    # Funds Reservation
    fundsReserve: Optional[CodeableConcept] = None  # Funds reserved status
    # Related
    related: List[ExplanationOfBenefitRelated] = field(default_factory=list)  # Other claims which are related to this claim
    # Prescription
    prescription: Optional[Reference] = None  # Prescription authorizing services or products
    # Original Prescription
    originalPrescription: Optional[Reference] = None  # Original prescription if superceded by fulfiller
    # Payee
    payee: Optional[ExplanationOfBenefitPayee] = None  # Party to be paid any benefits payable
    # Referral
    referral: Optional[Reference] = None  # Treatment referral
    # Facility
    facility: Optional[Reference] = None  # Servicing facility
    # Claim
    claim: Optional[Reference] = None  # Claim reference
    # Claim Response
    claimResponse: Optional[Reference] = None  # Claim response reference
    # Outcome
    outcome: str  # queued | complete | error | partial (required)
    # Disposition
    disposition: Optional[str] = None  # Disposition Message
    # Pre Auth Ref
    preAuthRef: List[str] = field(default_factory=list)  # Preauthorization reference
    # Pre Auth Ref Period
    preAuthRefPeriod: List[Period] = field(default_factory=list)  # Preauthorization in-effect period
    # Care Team
    careTeam: List[ExplanationOfBenefitCareTeam] = field(default_factory=list)  # Care Team members
    # Supporting Info
    supportingInfo: List[ExplanationOfBenefitSupportingInfo] = field(default_factory=list)  # Supporting information
    # Diagnosis
    diagnosis: List[ExplanationOfBenefitDiagnosis] = field(default_factory=list)  # Pertinent diagnosis information
    # Procedure
    procedure: List[ExplanationOfBenefitProcedure] = field(default_factory=list)  # Clinical procedures performed
    # Precedence
    precedence: Optional[int] = None  # Precedence (primary, secondary, etc.)
    # Insurance
    insurance: List[Any] = field(default_factory=list)  # Patient insurance information
    # Accident
    accident: Optional[Any] = None  # Details of the event
    # Item
    item: List[Any] = field(default_factory=list)  # Product or service provided
    # Add Item
    addItem: List[Any] = field(default_factory=list)  # Insurer added line items
    # Adjudication
    adjudication: List[Any] = field(default_factory=list)  # Header-level adjudication
    # Total
    total: List[Any] = field(default_factory=list)  # Adjudication totals
    # Payment
    payment: Optional[Any] = None  # Payment details
    # Form Code
    formCode: Optional[CodeableConcept] = None  # Printed form identifier
    # Form
    form: Optional[Attachment] = None  # Printed reference or actual form
    # Process Note
    processNote: List[Any] = field(default_factory=list)  # Note concerning adjudication
    # Benefit Period
    benefitPeriod: Optional[Period] = None  # When the benefits are applicable
    # Benefit Balance
    benefitBalance: List[Any] = field(default_factory=list)  # Balance by Benefit Category

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


