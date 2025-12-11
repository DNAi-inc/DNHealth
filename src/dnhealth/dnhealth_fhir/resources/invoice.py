# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Invoice resource.

Invoice represents a request for payment for goods and services rendered.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Money, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class InvoiceParticipant:
    """
    FHIR Invoice.participant complex type.
    
    Participants in creation of this Invoice.
    """
    
    role: Optional[CodeableConcept] = None  # Type of involvement in creation of this Invoice
    actor: Reference  # The individual, device or organization who participated (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InvoiceLineItemPriceComponent:
    """
    FHIR Invoice.lineItem.priceComponent complex type.
    
    Factors affecting the line item price.
    """
    
    type: str  # base | surcharge | deduction | discount | tax | informational (required)
    code: Optional[CodeableConcept] = None  # Code identifying the specific component
    factor: Optional[float] = None  # Factor used for calculating this component
    amount: Optional[Money] = None  # Monetary amount associated with this component
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class InvoiceLineItem:
    """
    FHIR Invoice.lineItem complex type.
    
    Each line item represents one charge for goods and services rendered.
    """
    
    sequence: Optional[int] = None  # Sequence number of line item
    chargeItemReference: Optional[Reference] = None  # Reference to ChargeItem containing details of this line item
    chargeItemCodeableConcept: Optional[CodeableConcept] = None  # Reference to ChargeItem containing details of this line item
    priceComponent: List[InvoiceLineItemPriceComponent] = field(default_factory=list)  # Components of total line item price
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Invoice(DomainResource):
    """
    FHIR R4 Invoice resource.
    
    Represents a request for payment for goods and services rendered.
    Extends DomainResource.
    """
    
    resourceType: str = "Invoice"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for item
    # Status
    status: str  # draft | issued | balanced | cancelled | entered-in-error (required)
    # Cancelled Reason
    cancelledReason: Optional[str] = None  # Reason for cancellation of this Invoice
    # Type
    type: Optional[CodeableConcept] = None  # Type of Invoice
    # Subject
    subject: Optional[Reference] = None  # Recipient(s) of goods and services
    # Recipient
    recipient: Optional[Reference] = None  # Recipient of this invoice
    # Date
    date: Optional[str] = None  # Invoice date / posting date
    # Participant
    participant: List[InvoiceParticipant] = field(default_factory=list)  # Participants in creation of this Invoice
    # Issuer
    issuer: Optional[Reference] = None  # Issuing Organization of Invoice
    # Account
    account: Optional[Reference] = None  # Account that is being balanced
    # Line Item
    lineItem: List[InvoiceLineItem] = field(default_factory=list)  # Line items of this Invoice
    # Total Price Component
    totalPriceComponent: List[InvoiceLineItemPriceComponent] = field(default_factory=list)  # Components of Invoice total
    # Total Net
    totalNet: Optional[Money] = None  # Net total of this Invoice
    # Total Gross
    totalGross: Optional[Money] = None  # Gross total of this Invoice
    # Payment Terms
    paymentTerms: Optional[str] = None  # Payment details
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about the invoice

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


