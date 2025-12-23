# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ClaimResponse resource.

ClaimResponse represents the response to a claim submission.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money, Quantity, Attachment


@dataclass
class ClaimResponseItemAdjudication:
    """
    FHIR ClaimResponse.item.adjudication complex type.
    
    The adjudication results.
    """
    
    category: CodeableConcept  # Type of adjudication information (required)
    reason: Optional[CodeableConcept] = None  # Explanation of adjudication outcome
    amount: Optional[Money] = None  # Monetary amount
    value: Optional[float] = None  # Non-monetary value
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseItemDetailSubDetail:
    """
    FHIR ClaimResponse.item.detail.subDetail complex type.
    
    Third-tier service code.
    """
    
    subDetailSequence: int  # Subdetail instance identifier (required)
    noteNumber: List[int] = field(default_factory=list)  # Applicable note numbers
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Subdetail level adjudication details
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseItemDetail:
    """
    FHIR ClaimResponse.item.detail complex type.
    
    Second-tier service code.
    """
    
    detailSequence: int  # Detail instance identifier (required)
    noteNumber: List[int] = field(default_factory=list)  # Applicable note numbers
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Detail level adjudication details
    subDetail: List[ClaimResponseItemDetailSubDetail] = field(default_factory=list)  # Subdetail line items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseItem:
    """
    FHIR ClaimResponse.item complex type.
    
    A claim line. Either a simple product or service or a 'group' of details which can each be a simple items or groups of sub-details.
    """
    
    itemSequence: int  # Claim item instance identifier (required)
    noteNumber: List[int] = field(default_factory=list)  # Applicable note numbers
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Adjudication details
    detail: List[ClaimResponseItemDetail] = field(default_factory=list)  # Adjudication for claim line items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseAddItemDetailSubDetail:
    """
    FHIR ClaimResponse.addItem.detail.subDetail complex type.
    
    Third-tier service code.
    """
    
    productOrService: CodeableConcept  # Billing, service, product, or drug code (required)
    modifier: List[CodeableConcept] = field(default_factory=list)  # Service/product billing modifiers
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    factor: Optional[float] = None  # Price scaling factor
    net: Optional[Money] = None  # Total item cost
    noteNumber: List[int] = field(default_factory=list)  # Applicable note numbers
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Subdetail level adjudication details
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseAddItemDetail:
    """
    FHIR ClaimResponse.addItem.detail complex type.
    
    Second-tier service code.
    """
    
    productOrService: CodeableConcept  # Billing, service, product, or drug code (required)
    modifier: List[CodeableConcept] = field(default_factory=list)  # Service/product billing modifiers
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    factor: Optional[float] = None  # Price scaling factor
    net: Optional[Money] = None  # Total item cost
    noteNumber: List[int] = field(default_factory=list)  # Applicable note numbers
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Detail level adjudication details
    subDetail: List[ClaimResponseAddItemDetailSubDetail] = field(default_factory=list)  # Subdetail line items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseAddItem:
    """
    FHIR ClaimResponse.addItem complex type.
    
    The first-tier service adjudications for payor added product or service lines.
    """
    
    productOrService: CodeableConcept  # Billing, service, product, or drug code (required)
    itemSequence: List[int] = field(default_factory=list)  # Item sequence number
    detailSequence: List[int] = field(default_factory=list)  # Detail sequence number
    subDetailSequence: List[int] = field(default_factory=list)  # Subdetail sequence number
    provider: List[Reference] = field(default_factory=list)  # Authorized providers
    modifier: List[CodeableConcept] = field(default_factory=list)  # Service/product billing modifiers
    programCode: List[CodeableConcept] = field(default_factory=list)  # Program the product or service is provided under
    servicedDate: Optional[str] = None  # Date or dates of service
    servicedPeriod: Optional[Period] = None  # Date or dates of service
    locationCodeableConcept: Optional[CodeableConcept] = None  # Place of service or where product was supplied
    locationAddress: Optional[Any] = None  # Place of service or where product was supplied
    locationReference: Optional[Reference] = None  # Place of service or where product was supplied
    quantity: Optional[Quantity] = None  # Count of products or services
    unitPrice: Optional[Money] = None  # Fee, charge or cost per item
    factor: Optional[float] = None  # Price scaling factor
    net: Optional[Money] = None  # Total item cost
    bodySite: Optional[CodeableConcept] = None  # Anatomical location
    subSite: List[CodeableConcept] = field(default_factory=list)  # Anatomical sub-location
    noteNumber: List[int] = field(default_factory=list)  # Applicable note numbers
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Added items adjudication
    detail: List[ClaimResponseAddItemDetail] = field(default_factory=list)  # Insurer added line items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseTotal:
    """
    FHIR ClaimResponse.total complex type.
    
    Categorized monetary totals for the adjudication.
    """
    
    category: CodeableConcept  # Type of adjudication information (required)
    amount: Money  # Financial total for the category (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponsePayment:
    """
    FHIR ClaimResponse.payment complex type.
    
    Payment details for the adjudication of the claim.
    """
    
    type: CodeableConcept  # Partial or complete payment (required)
    amount: Money  # Payable amount after adjustment (required)
    adjustment: Optional[Money] = None  # Payment adjustment for non-claim issues
    adjustmentReason: Optional[CodeableConcept] = None  # Explanation for the adjustment
    date: Optional[str] = None  # Expected date of payment
    identifier: Optional[Identifier] = None  # Business identifier for the payment
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseProcessNote:
    """
    FHIR ClaimResponse.processNote complex type.
    
    A note that describes or explains adjudication results in a human readable form.
    """
    
    number: Optional[int] = None  # Note instance identifier
    type: Optional[str] = None  # display | print | printoper
    text: Optional[str] = None  # Note explanatory text
    language: Optional[CodeableConcept] = None  # Language of the text
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseInsurance:
    """
    FHIR ClaimResponse.insurance complex type.
    
    Financial instruments for reimbursement for the health care products and services.
    """
    
    sequence: int  # Insurance instance identifier (required)
    focal: bool  # Coverage to be used for adjudication (required)
    coverage: Reference  # Insurance information (required)
    businessArrangement: Optional[str] = None  # Additional provider contract number
    claimResponse: Optional[Reference] = None  # Adjudication results
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponseError:
    """
    FHIR ClaimResponse.error complex type.
    
    Errors encountered during the processing of the adjudication.
    """
    
    code: CodeableConcept  # Error code detailing processing issues (required)
    itemSequence: Optional[int] = None  # Item sequence number
    detailSequence: Optional[int] = None  # Detail sequence number
    subDetailSequence: Optional[int] = None  # Subdetail sequence number
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClaimResponse(DomainResource):
    """
    FHIR R4 ClaimResponse resource.
    
    Represents the response to a claim submission.
    Extends DomainResource.
    """
    
    resourceType: str = "ClaimResponse"
    # Required fields (using field(default=None) to fix dataclass field ordering with parent classes)
    # Status
    status: Optional[str] = field(default=None)  # active | cancelled | draft | entered-in-error (required)
    # Type
    type: Optional[CodeableConcept] = field(default=None)  # More granular claim type (required)
    # Use
    use: Optional[str] = field(default=None)  # claim | preauthorization | predetermination (required)
    # Patient
    patient: Optional[Reference] = field(default=None)  # The recipient of the products and services (required)
    # Created
    created: Optional[str] = field(default=None)  # Response creation date (required)
    # Insurer
    insurer: Optional[Reference] = field(default=None)  # Party responsible for reimbursement (required)
    # Outcome
    outcome: Optional[str] = field(default=None)  # queued | complete | error | partial (required)
    # Optional fields (all have defaults) - must come after required fields
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for a claim response
    # Sub Type
    subType: Optional[CodeableConcept] = None  # More granular claim type
    # Requestor
    requestor: Optional[Reference] = None  # Party responsible for the claim
    # Request
    request: Optional[Reference] = None  # Id of resource triggering adjudication
    # Disposition
    disposition: Optional[str] = None  # Disposition Message
    # Pre Auth Ref
    preAuthRef: Optional[str] = None  # Preauthorization reference
    # Pre Auth Period
    preAuthPeriod: Optional[Period] = None  # Preauthorization reference effective period
    # Payee Type
    payeeType: Optional[CodeableConcept] = None  # Party to be paid any benefits payable
    # Item
    item: List[ClaimResponseItem] = field(default_factory=list)  # Adjudication for claim line items
    # Add Item
    addItem: List[ClaimResponseAddItem] = field(default_factory=list)  # Insurer added line items
    # Adjudication
    adjudication: List[ClaimResponseItemAdjudication] = field(default_factory=list)  # Header-level adjudication
    # Total
    total: List[ClaimResponseTotal] = field(default_factory=list)  # Adjudication totals
    # Payment
    payment: Optional[ClaimResponsePayment] = None  # Payment details
    # Funds Reserve
    fundsReserve: Optional[CodeableConcept] = None  # Funds reserved status
    # Form Code
    formCode: Optional[CodeableConcept] = None  # Printed form identifier
    # Form
    form: Optional[Attachment] = None  # Printed reference or actual form
    # Process Note
    processNote: List[ClaimResponseProcessNote] = field(default_factory=list)  # Note concerning adjudication
    # Communication Request
    communicationRequest: List[Reference] = field(default_factory=list)  # Request for additional information
    # Insurance
    insurance: List[ClaimResponseInsurance] = field(default_factory=list)  # Patient insurance information
    # Error
    error: List[ClaimResponseError] = field(default_factory=list)  # Processing errors
    
    def __post_init__(self):
        """Validate required fields."""
        if self.status is None:
            raise ValueError("status is required")
        if self.type is None:
            raise ValueError("type is required")
        if self.use is None:
            raise ValueError("use is required")
        if self.patient is None:
            raise ValueError("patient is required")
        if self.created is None:
            raise ValueError("created is required")
        if self.insurer is None:
            raise ValueError("insurer is required")
        if self.outcome is None:
            raise ValueError("outcome is required")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


