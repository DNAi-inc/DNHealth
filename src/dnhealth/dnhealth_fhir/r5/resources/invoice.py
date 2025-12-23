# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Invoice resource.

Invoice containing collected ChargeItems from an Account with calculated individual and total price for Billing purpose.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Reference
from typing import Any, List, Optional

@dataclass
class InvoiceParticipant:
    """
    InvoiceParticipant nested class.
    """

    actor: Optional[Reference] = None  # The device, practitioner, etc. who performed or participated in the service.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    role: Optional[CodeableConcept] = None  # Describes the type of involvement (e.g. transcriptionist, creator etc.). If the invoice has been ...

@dataclass
class InvoiceLineItem:
    """
    InvoiceLineItem nested class.
    """

    chargeItem: Optional[Any] = None  # The ChargeItem contains information such as the billing code, date, amount etc. If no further det...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    sequence: Optional[int] = None  # Sequence in which the items appear on the invoice.
    serviced: Optional[Any] = None  # Date/time(s) range when this service was delivered or completed.
    priceComponent: Optional[List[Any]] = field(default_factory=list)  # The price for a ChargeItem may be calculated as a base price with surcharges/deductions that appl...


@dataclass
class Invoice(FHIRResource):
    """
    Invoice containing collected ChargeItems from an Account with calculated individual and total price for Billing purpose.
    """

    status: Optional[str] = None  # The current state of the Invoice.
    resourceType: str = "Invoice"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier of this Invoice, often used for reference in correspondence about this invoice or for ...
    cancelledReason: Optional[str] = None  # In case of Invoice cancellation a reason must be given (entered in error, superseded by corrected...
    type: Optional[CodeableConcept] = None  # Type of Invoice depending on domain, realm an usage (e.g. internal/external, dental, preliminary).
    subject: Optional[Reference] = None  # The individual or set of individuals receiving the goods and services billed in this invoice.
    recipient: Optional[Reference] = None  # The individual or Organization responsible for balancing of this invoice.
    date: Optional[str] = None  # Depricared by the element below.
    creation: Optional[str] = None  # Date/time(s) of when this Invoice was posted.
    period: Optional[Any] = None  # Date/time(s) range of services included in this invoice.
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what performed or participated in the charged service.
    issuer: Optional[Reference] = None  # The organizationissuing the Invoice.
    account: Optional[Reference] = None  # Account which is supposed to be balanced with this Invoice.
    lineItem: Optional[List[BackboneElement]] = field(default_factory=list)  # Each line item represents one charge for goods and services rendered. Details such.ofType(date), ...
    totalPriceComponent: Optional[List[Any]] = field(default_factory=list)  # The total amount for the Invoice may be calculated as the sum of the line items with surcharges/d...
    totalNet: Optional[Money] = None  # Invoice total , taxes excluded.
    totalGross: Optional[Money] = None  # Invoice total, tax included.
    paymentTerms: Optional[str] = None  # Payment details such as banking details, period of payment, deductibles, methods of payment.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the invoice by the issuer, subject, or other participants.