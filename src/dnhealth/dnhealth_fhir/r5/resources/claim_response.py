# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ClaimResponse resource.

This resource provides the adjudication details from the processing of a Claim resource.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class ClaimResponseEvent:
    """
    ClaimResponseEvent nested class.
    """

    type: Optional[CodeableConcept] = None  # A coded event such as when a service is expected or a card printed.
    when: Optional[Any] = None  # A date or period in the past or future indicating when the event occurred or is expectd to occur.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ClaimResponseItem:
    """
    ClaimResponseItem nested class.
    """

    itemSequence: Optional[int] = None  # A number to uniquely reference the claim item entries.
    category: Optional[CodeableConcept] = None  # A code to indicate the information type of this adjudication record. Information types may includ...
    detailSequence: Optional[int] = None  # A number to uniquely reference the claim detail entry.
    subDetailSequence: Optional[int] = None  # A number to uniquely reference the claim sub-detail entry.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[BackboneElement] = None  # The high-level results of the adjudication if adjudication has been performed.
    decision: Optional[CodeableConcept] = None  # The result of the claim, predetermination, or preauthorization adjudication.
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reasons for the result of the claim, predetermination, or preauthorization adjudication.
    preAuthRef: Optional[str] = None  # Reference from the Insurer which is used in later communications which refers to this adjudication.
    preAuthPeriod: Optional[Period] = None  # The time frame during which this authorization is effective.
    adjudication: Optional[List[BackboneElement]] = field(default_factory=list)  # If this item is a group then the values here are a summary of the adjudication of the detail item...
    amount: Optional[Money] = None  # Monetary amount associated with the category.
    quantity: Optional[Quantity] = None  # A non-monetary value associated with the category. Mutually exclusive to the amount element above.
    detail: Optional[List[BackboneElement]] = field(default_factory=list)  # A claim detail. Either a simple (a product or service) or a 'group' of sub-details which are simp...
    subDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # A sub-detail adjudication of a simple product or service.

@dataclass
class ClaimResponseItemReviewOutcome:
    """
    ClaimResponseItemReviewOutcome nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    decision: Optional[CodeableConcept] = None  # The result of the claim, predetermination, or preauthorization adjudication.
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reasons for the result of the claim, predetermination, or preauthorization adjudication.
    preAuthRef: Optional[str] = None  # Reference from the Insurer which is used in later communications which refers to this adjudication.
    preAuthPeriod: Optional[Period] = None  # The time frame during which this authorization is effective.

@dataclass
class ClaimResponseItemAdjudication:
    """
    ClaimResponseItemAdjudication nested class.
    """

    category: Optional[CodeableConcept] = None  # A code to indicate the information type of this adjudication record. Information types may includ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    reason: Optional[CodeableConcept] = None  # A code supporting the understanding of the adjudication result and explaining variance from expec...
    amount: Optional[Money] = None  # Monetary amount associated with the category.
    quantity: Optional[Quantity] = None  # A non-monetary value associated with the category. Mutually exclusive to the amount element above.

@dataclass
class ClaimResponseItemDetail:
    """
    ClaimResponseItemDetail nested class.
    """

    detailSequence: Optional[int] = None  # A number to uniquely reference the claim detail entry.
    subDetailSequence: Optional[int] = None  # A number to uniquely reference the claim sub-detail entry.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.
    subDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # A sub-detail adjudication of a simple product or service.

@dataclass
class ClaimResponseItemDetailSubDetail:
    """
    ClaimResponseItemDetailSubDetail nested class.
    """

    subDetailSequence: Optional[int] = None  # A number to uniquely reference the claim sub-detail entry.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.

@dataclass
class ClaimResponseAddItem:
    """
    ClaimResponseAddItem nested class.
    """

    site: List[Any] = field(default_factory=list)  # Physical service site on the patient (limb, tooth, etc.).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    itemSequence: Optional[List[int]] = field(default_factory=list)  # Claim items which this service line is intended to replace.
    detailSequence: Optional[List[int]] = field(default_factory=list)  # The sequence number of the details within the claim item which this line is intended to replace.
    subdetailSequence: Optional[List[int]] = field(default_factory=list)  # The sequence number of the sub-details within the details within the claim item which this line i...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    provider: Optional[List[Reference]] = field(default_factory=list)  # The providers who are authorized for the services rendered to the patient.
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    request: Optional[List[Reference]] = field(default_factory=list)  # Request or Referral for Goods or Service to be rendered.
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    programCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies the program under which this may be recovered.
    serviced: Optional[Any] = None  # The date or dates when the service or product was supplied, performed or completed.
    location: Optional[Any] = None  # Where the product or service was provided.
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the group (if a grouper) or the addItem. Net = unit price * quantity...
    bodySite: Optional[List[BackboneElement]] = field(default_factory=list)  # Physical location where the service is performed or applies.
    subSite: Optional[List[CodeableConcept]] = field(default_factory=list)  # A region or surface of the bodySite, e.g. limb region or tooth surface(s).
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.
    detail: Optional[List[BackboneElement]] = field(default_factory=list)  # The second-tier service adjudications for payor added services.
    subDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # The third-tier service adjudications for payor added services.

@dataclass
class ClaimResponseAddItemBodySite:
    """
    ClaimResponseAddItemBodySite nested class.
    """

    site: List[Any] = field(default_factory=list)  # Physical service site on the patient (limb, tooth, etc.).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    subSite: Optional[List[CodeableConcept]] = field(default_factory=list)  # A region or surface of the bodySite, e.g. limb region or tooth surface(s).

@dataclass
class ClaimResponseAddItemDetail:
    """
    ClaimResponseAddItemDetail nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the group (if a grouper) or the addItem.detail. Net = unit price * q...
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.
    subDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # The third-tier service adjudications for payor added services.

@dataclass
class ClaimResponseAddItemDetailSubDetail:
    """
    ClaimResponseAddItemDetailSubDetail nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the addItem.detail.subDetail. Net = unit price * quantity * factor.
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.

@dataclass
class ClaimResponseTotal:
    """
    ClaimResponseTotal nested class.
    """

    category: Optional[CodeableConcept] = None  # A code to indicate the information type of this adjudication record. Information types may includ...
    amount: Optional[Money] = None  # Monetary total amount associated with the category.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ClaimResponsePayment:
    """
    ClaimResponsePayment nested class.
    """

    type: Optional[CodeableConcept] = None  # Whether this represents partial or complete payment of the benefits payable.
    amount: Optional[Money] = None  # Benefits payable less any payment adjustment.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    adjustment: Optional[Money] = None  # Total amount of all adjustments to this payment included in this transaction which are not relate...
    adjustmentReason: Optional[CodeableConcept] = None  # Reason for the payment adjustment.
    date: Optional[str] = None  # Estimated date the payment will be issued or the actual issue date of payment.
    identifier: Optional[Identifier] = None  # Issuer's unique identifier for the payment instrument.

@dataclass
class ClaimResponseProcessNote:
    """
    ClaimResponseProcessNote nested class.
    """

    text: Optional[str] = None  # The explanation or description associated with the processing.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    number: Optional[int] = None  # A number to uniquely identify a note entry.
    type: Optional[CodeableConcept] = None  # The business purpose of the note text.
    language: Optional[CodeableConcept] = None  # A code to define the language used in the text of the note.

@dataclass
class ClaimResponseInsurance:
    """
    ClaimResponseInsurance nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify insurance entries and provide a sequence of coverages to convey coo...
    focal: Optional[bool] = None  # A flag to indicate that this Coverage is to be used for adjudication of this claim when set to true.
    coverage: Optional[Reference] = None  # Reference to the insurance card level information contained in the Coverage resource. The coverag...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    businessArrangement: Optional[str] = None  # A business agreement number established between the provider and the insurer for special business...
    claimResponse: Optional[Reference] = None  # The result of the adjudication of the line items for the Coverage specified in this insurance.

@dataclass
class ClaimResponseError:
    """
    ClaimResponseError nested class.
    """

    code: Optional[CodeableConcept] = None  # An error code, from a specified code system, which details why the claim could not be adjudicated.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    itemSequence: Optional[int] = None  # The sequence number of the line item submitted which contains the error. This value is omitted wh...
    detailSequence: Optional[int] = None  # The sequence number of the detail within the line item submitted which contains the error. This v...
    subDetailSequence: Optional[int] = None  # The sequence number of the sub-detail within the detail within the line item submitted which cont...
    expression: Optional[List[str]] = field(default_factory=list)  # A [simple subset of FHIRPath](fhirpath.html#simple) limited to element names, repetition indicato...


@dataclass
class ClaimResponse(FHIRResource):
    """
    This resource provides the adjudication details from the processing of a Claim resource.
    """

    status: Optional[str] = None  # The status of the resource instance.
    type: Optional[CodeableConcept] = None  # A finer grained suite of claim type codes which may convey additional information such as Inpatie...
    use: Optional[str] = None  # A code to indicate whether the nature of the request is: Claim - A request to an Insurer to adjud...
    patient: Optional[Reference] = None  # The party to whom the professional services and/or products have been supplied or are being consi...
    created: Optional[str] = None  # The date this resource was created.
    outcome: Optional[str] = None  # The outcome of the claim, predetermination, or preauthorization processing.
    resourceType: str = "ClaimResponse"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this claim response.
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    subType: Optional[CodeableConcept] = None  # A finer grained suite of claim type codes which may convey additional information such as Inpatie...
    insurer: Optional[Reference] = None  # The party responsible for authorization, adjudication and reimbursement.
    requestor: Optional[Reference] = None  # The provider which is responsible for the claim, predetermination or preauthorization.
    request: Optional[Reference] = None  # Original request resource reference.
    decision: Optional[CodeableConcept] = None  # The result of the claim, predetermination, or preauthorization adjudication.
    disposition: Optional[str] = None  # A human readable description of the status of the adjudication.
    preAuthRef: Optional[str] = None  # Reference from the Insurer which is used in later communications which refers to this adjudication.
    preAuthPeriod: Optional[Period] = None  # The time frame during which this authorization is effective.
    event: Optional[List[BackboneElement]] = field(default_factory=list)  # Information code for an event with a corresponding date or period.
    payeeType: Optional[CodeableConcept] = None  # Type of Party to be reimbursed: subscriber, provider, other.
    encounter: Optional[List[Reference]] = field(default_factory=list)  # Healthcare encounters related to this claim.
    diagnosisRelatedGroup: Optional[CodeableConcept] = None  # A package billing code or bundle code used to group products and services to a particular health ...
    item: Optional[List[BackboneElement]] = field(default_factory=list)  # A claim line. Either a simple (a product or service) or a 'group' of details which can also be a ...
    addItem: Optional[List[BackboneElement]] = field(default_factory=list)  # The first-tier service adjudications for payor added product or service lines.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results which are presented at the header level rather than at the line-item or ...
    total: Optional[List[BackboneElement]] = field(default_factory=list)  # Categorized monetary totals for the adjudication.
    payment: Optional[BackboneElement] = None  # Payment details for the adjudication of the claim.
    fundsReserve: Optional[CodeableConcept] = None  # A code, used only on a response to a preauthorization, to indicate whether the benefits payable h...
    formCode: Optional[CodeableConcept] = None  # A code for the form to be used for printing the content.
    form: Optional[Attachment] = None  # The actual form, by reference or inclusion, for printing the content or an EOB.
    processNote: Optional[List[BackboneElement]] = field(default_factory=list)  # A note that describes or explains adjudication results in a human readable form.
    communicationRequest: Optional[List[Reference]] = field(default_factory=list)  # Request for additional supporting or authorizing information.
    insurance: Optional[List[BackboneElement]] = field(default_factory=list)  # Financial instruments for reimbursement for the health care products and services specified on th...
    error: Optional[List[BackboneElement]] = field(default_factory=list)  # Errors encountered during the processing of the adjudication.