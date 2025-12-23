# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 PaymentReconciliation resource.

PaymentReconciliation provides payment reconciliation information.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Money,
    Annotation,
)


@dataclass
class PaymentReconciliationDetail:
    """
    FHIR PaymentReconciliation.detail complex type.
    
    Payment details.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    identifier: Optional[Identifier] = None  # Business identifier of the payment detail
    predecessor: Optional[Identifier] = None  # Business identifier of the prior payment detail
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[CodeableConcept] = None  # Type of payment (required)
    request: Optional[Reference] = None  # Claim request
    submitter: Optional[Reference] = None  # Submitter of the request
    response: Optional[Reference] = None  # Claim response
    date: Optional[str] = None  # Date of the payment
    responsible: Optional[Reference] = None  # Responsible practitioner
    payee: Optional[Reference] = None  # Recipient of the payment
    amount: Optional[Money] = None  # Amount allocated to this payable


@dataclass
class PaymentReconciliationProcessNote:
    """
    FHIR PaymentReconciliation.processNote complex type.
    
    Processing notes.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: Optional[str] = None  # display | print | printoper
    text: Optional[str] = None  # Note explanatory text


@dataclass
class PaymentReconciliation(DomainResource):
    """
    FHIR R4 PaymentReconciliation resource.
    
    Provides payment reconciliation information.
    Extends DomainResource.
    """
    
    resourceType: str = "PaymentReconciliation"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for the payment reconciliation
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (identifier has default value).
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | cancelled | draft | entered-in-error (required in FHIR)
    # Period
    period: Optional[Period] = None  # Period covered
    # Created
    # Note: created is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (period has default value).
    # Validation should enforce created is provided.
    created: Optional[str] = None  # Creation date (required in FHIR)
    # Payment Issuer
    paymentIssuer: Optional[Reference] = None  # Party generating payment
    # Request
    request: Optional[Reference] = None  # Reference to requesting resource
    # Requestor
    requestor: Optional[Reference] = None  # Responsible practitioner
    # Outcome
    outcome: Optional[str] = None  # queued | complete | error | partial
    # Disposition
    disposition: Optional[str] = None  # Disposition message
    # Payment Date
    # Note: paymentDate is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce paymentDate is provided.
    paymentDate: Optional[str] = None  # When payment issued (required)
    # Payment Amount
    # Note: paymentAmount is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce paymentAmount is provided.
    paymentAmount: Optional[Money] = None  # Total amount of payment (required)
    # Payment Identifier
    paymentIdentifier: Optional[Identifier] = None  # Business identifier for the payment
    # Detail
    detail: List[PaymentReconciliationDetail] = field(default_factory=list)  # Payment details
    # Form Code
    formCode: Optional[CodeableConcept] = None  # Printed form identifier
    # Process Note
    processNote: List[PaymentReconciliationProcessNote] = field(default_factory=list)  # Processing comments

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

