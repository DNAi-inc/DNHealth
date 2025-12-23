# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 PaymentNotice resource.

This resource provides the status of the payment for goods and services rendered, and the request and response resource references.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Money, Reference
from typing import List, Optional

@dataclass
class PaymentNotice(FHIRResource):
    """
    This resource provides the status of the payment for goods and services rendered, and the request and response resource references.
    """

    status: Optional[str] = None  # The status of the resource instance.
    created: Optional[str] = None  # The date when this resource was created.
    recipient: Optional[Reference] = None  # The party who is notified of the payment status.
    amount: Optional[Money] = None  # The amount sent to the payee.
    resourceType: str = "PaymentNotice"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this payment notice.
    request: Optional[Reference] = None  # Reference of resource for which payment is being made.
    response: Optional[Reference] = None  # Reference of response to resource for which payment is being made.
    reporter: Optional[Reference] = None  # The party who reports the payment notice.
    payment: Optional[Reference] = None  # A reference to the payment which is the subject of this notice.
    paymentDate: Optional[str] = None  # The date when the above payment action occurred.
    payee: Optional[Reference] = None  # The party who will receive or has received payment that is the subject of this notification.
    paymentStatus: Optional[CodeableConcept] = None  # A code indicating whether payment has been sent or cleared.