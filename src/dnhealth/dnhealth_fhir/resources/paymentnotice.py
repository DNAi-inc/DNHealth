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
    status: str  # active | cancelled | draft | entered-in-error (required)
    # Request
    request: Optional[Reference] = None  # Request reference
    # Response
    response: Optional[Reference] = None  # Response reference
    # Created
    created: str  # Creation date (required)
    # Provider
    provider: Optional[Reference] = None  # Responsible practitioner
    # Payment
    payment: Reference  # Payment reference (required)
    # Payment Date
    paymentDate: Optional[str] = None  # Payment date
    # Payee
    payee: Optional[Reference] = None  # Party being paid
    # Recipient
    recipient: Reference  # Party receiving notification (required)
    # Amount
    amount: Money  # Monetary amount of the payment (required)
    # Payment Status
    paymentStatus: Optional[CodeableConcept] = None  # Issued or cleared status of the payment

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

