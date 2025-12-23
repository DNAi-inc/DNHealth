# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 PaymentReconciliation resource.

This resource provides the details including amount of a payment and allocates the payment items being paid.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Reference
from typing import Any, List, Optional

@dataclass
class PaymentReconciliationAllocation:
    """
    PaymentReconciliationAllocation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[Identifier] = None  # Unique identifier for the current payment item for the referenced payable.
    predecessor: Optional[Identifier] = None  # Unique identifier for the prior payment item for the referenced payable.
    target: Optional[Reference] = None  # Specific resource to which the payment/adjustment/advance applies.
    targetItem: Optional[Any] = None  #  Identifies the claim line item, encounter or other sub-element being paid. Note payment may be p...
    encounter: Optional[Reference] = None  # The Encounter to which this payment applies, may be completed by the receiver, used for search.
    account: Optional[Reference] = None  # The Account to which this payment applies, may be completed by the receiver, used for search.
    type: Optional[CodeableConcept] = None  # Code to indicate the nature of the payment.
    submitter: Optional[Reference] = None  # The party which submitted the claim or financial transaction.
    response: Optional[Reference] = None  # A resource, such as a ClaimResponse, which contains a commitment to payment.
    date: Optional[str] = None  # The date from the response resource containing a commitment to pay.
    responsible: Optional[Reference] = None  # A reference to the individual who is responsible for inquiries regarding the response and its pay...
    payee: Optional[Reference] = None  # The party which is receiving the payment.
    amount: Optional[Money] = None  # The monetary amount allocated from the total payment to the payable.

@dataclass
class PaymentReconciliationProcessNote:
    """
    PaymentReconciliationProcessNote nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[str] = None  # The business purpose of the note text.
    text: Optional[str] = None  # The explanation or description associated with the processing.


@dataclass
class PaymentReconciliation(FHIRResource):
    """
    This resource provides the details including amount of a payment and allocates the payment items being paid.
    """

    type: Optional[CodeableConcept] = None  # Code to indicate the nature of the payment such as payment, adjustment.
    status: Optional[str] = None  # The status of the resource instance.
    created: Optional[str] = None  # The date when the resource was created.
    date: Optional[str] = None  # The date of payment as indicated on the financial instrument.
    amount: Optional[Money] = None  # Total payment amount as indicated on the financial instrument.
    resourceType: str = "PaymentReconciliation"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this payment reconciliation.
    kind: Optional[CodeableConcept] = None  # The workflow or activity which gave rise to or during which the payment ocurred such as a kiosk, ...
    period: Optional[Period] = None  # The period of time for which payments have been gathered into this bulk payment for settlement.
    enterer: Optional[Reference] = None  # Payment enterer if not the actual payment issuer.
    issuerType: Optional[CodeableConcept] = None  # The type of the source such as patient or insurance.
    paymentIssuer: Optional[Reference] = None  # The party who generated the payment.
    request: Optional[Reference] = None  # Original request resource reference.
    requestor: Optional[Reference] = None  # The practitioner who is responsible for the services rendered to the patient.
    outcome: Optional[str] = None  # The outcome of a request for a reconciliation.
    disposition: Optional[str] = None  # A human readable description of the status of the request for the reconciliation.
    location: Optional[Reference] = None  # The location of the site or device for electronic transfers or physical location for cash payments.
    method: Optional[CodeableConcept] = None  # The means of payment such as check, card cash, or electronic funds transfer.
    cardBrand: Optional[str] = None  # The card brand such as debit, Visa, Amex etc. used if a card is the method of payment.
    accountNumber: Optional[str] = None  # A portion of the account number, often the last 4 digits, used for verification not charging purp...
    expirationDate: Optional[str] = None  # The year and month (YYYY-MM) when the instrument, typically card, expires.
    processor: Optional[str] = None  # The name of the card processor, etf processor, bank for checks.
    referenceNumber: Optional[str] = None  # The check number, eft reference, car processor reference.
    authorization: Optional[str] = None  # An alphanumeric issued by the processor to confirm the successful issuance of payment.
    tenderedAmount: Optional[Money] = None  # The amount offered by the issuer, typically applies to cash when the issuer provides an amount in...
    returnedAmount: Optional[Money] = None  # The amount returned by the receiver which is excess to the amount payable, often referred to as '...
    paymentIdentifier: Optional[Identifier] = None  # Issuer's unique identifier for the payment instrument.
    allocation: Optional[List[BackboneElement]] = field(default_factory=list)  # Distribution of the payment amount for a previously acknowledged payable.
    formCode: Optional[CodeableConcept] = None  # A code for the form to be used for printing the content.
    processNote: Optional[List[BackboneElement]] = field(default_factory=list)  # A note that describes or explains the processing in a human readable form.