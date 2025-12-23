# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 PaymentNotice resource.

PaymentNotice provides payment status information.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Money,
)


logger = logging.getLogger(__name__)


@dataclass
class PaymentNotice(DomainResource):
    """
    FHIR R4 PaymentNotice resource.
    
    Provides payment status information.
    Extends DomainResource.
    """
    
    resourceType: str = "PaymentNotice"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for the payment notice
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (identifier has default value).
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | cancelled | draft | entered-in-error (required in FHIR)
    # Request
    request: Optional[Reference] = None  # Request reference
    # Response
    response: Optional[Reference] = None  # Response reference
    # Created
    # Note: created is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce created is provided.
    created: Optional[str] = None  # Creation date (required)
    # Provider
    provider: Optional[Reference] = None  # Responsible practitioner
    # Payment
    # Note: payment is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce payment is provided.
    payment: Optional[Reference] = None  # Payment reference (required)
    # Payment Date
    paymentDate: Optional[str] = None  # Payment date
    # Payee
    payee: Optional[Reference] = None  # Party being paid
    # Recipient
    # Note: recipient is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce recipient is provided.
    recipient: Optional[Reference] = None  # Party receiving notification (required)
    # Amount
    # Note: amount is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce amount is provided.
    amount: Optional[Money] = None  # Monetary amount of the payment (required)
    # Payment Status
    paymentStatus: Optional[CodeableConcept] = None  # Issued or cleared status of the payment

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

