# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ExplanationOfBenefit resource.

This resource provides: the claim details; adjudication details from the processing of a Claim; and optionally account balance information, for informing the subscriber of the benefits provided.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Attachment, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Money, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class ExplanationOfBenefitRelated:
    """
    ExplanationOfBenefitRelated nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    claim: Optional[Reference] = None  # Reference to a related claim.
    relationship: Optional[CodeableConcept] = None  # A code to convey how the claims are related.
    reference: Optional[Identifier] = None  # An alternate organizational reference to the case or file to which this particular claim pertains.

@dataclass
class ExplanationOfBenefitEvent:
    """
    ExplanationOfBenefitEvent nested class.
    """

    type: Optional[CodeableConcept] = None  # A coded event such as when a service is expected or a card printed.
    when: Optional[Any] = None  # A date or period in the past or future indicating when the event occurred or is expectd to occur.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ExplanationOfBenefitPayee:
    """
    ExplanationOfBenefitPayee nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Type of Party to be reimbursed: Subscriber, provider, other.
    party: Optional[Reference] = None  # Reference to the individual or organization to whom any payment will be made.

@dataclass
class ExplanationOfBenefitCareTeam:
    """
    ExplanationOfBenefitCareTeam nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify care team entries.
    provider: Optional[Reference] = None  # Member of the team who provided the product or service.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    responsible: Optional[bool] = None  # The party who is billing and/or responsible for the claimed products or services.
    role: Optional[CodeableConcept] = None  # The lead, assisting or supervising practitioner and their discipline if a multidisciplinary team.
    specialty: Optional[CodeableConcept] = None  # The specialization of the practitioner or provider which is applicable for this service.

@dataclass
class ExplanationOfBenefitSupportingInfo:
    """
    ExplanationOfBenefitSupportingInfo nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify supporting information entries.
    category: Optional[CodeableConcept] = None  # The general class of the information supplied: information; exception; accident, employment; onse...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[CodeableConcept] = None  # System and code pertaining to the specific information regarding special conditions relating to t...
    timing: Optional[Any] = None  # The date when or period to which this information refers.
    value: Optional[Any] = None  # Additional data or information such as resources, documents, images etc. including references to ...
    reason: Optional[Coding] = None  # Provides the reason in the situation where a reason code is required in addition to the content.

@dataclass
class ExplanationOfBenefitDiagnosis:
    """
    ExplanationOfBenefitDiagnosis nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify diagnosis entries.
    diagnosis: Optional[Any] = None  # The nature of illness or problem in a coded form or as a reference to an external defined Condition.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # When the condition was observed or the relative ranking.
    onAdmission: Optional[CodeableConcept] = None  # Indication of whether the diagnosis was present on admission to a facility.

@dataclass
class ExplanationOfBenefitProcedure:
    """
    ExplanationOfBenefitProcedure nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify procedure entries.
    procedure: Optional[Any] = None  # The code or reference to a Procedure resource which identifies the clinical intervention performed.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # When the condition was observed or the relative ranking.
    date: Optional[str] = None  # Date and optionally time the procedure was performed.
    udi: Optional[List[Reference]] = field(default_factory=list)  # Unique Device Identifiers associated with this line item.

@dataclass
class ExplanationOfBenefitInsurance:
    """
    ExplanationOfBenefitInsurance nested class.
    """

    focal: Optional[bool] = None  # A flag to indicate that this Coverage is to be used for adjudication of this claim when set to true.
    coverage: Optional[Reference] = None  # Reference to the insurance card level information contained in the Coverage resource. The coverag...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    preAuthRef: Optional[List[str]] = field(default_factory=list)  # Reference numbers previously provided by the insurer to the provider to be quoted on subsequent c...

@dataclass
class ExplanationOfBenefitAccident:
    """
    ExplanationOfBenefitAccident nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    date: Optional[str] = None  # Date of an accident event  related to the products and services contained in the claim.
    type: Optional[CodeableConcept] = None  # The type or context of the accident event for the purposes of selection of potential insurance co...
    location: Optional[Any] = None  # The physical location of the accident event.

@dataclass
class ExplanationOfBenefitItem:
    """
    ExplanationOfBenefitItem nested class.
    """

    sequence: Optional[int] = None  # A number to uniquely identify item entries.
    site: List[Any] = field(default_factory=list)  # Physical service site on the patient (limb, tooth, etc.).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    careTeamSequence: Optional[List[int]] = field(default_factory=list)  # Care team members related to this service or product.
    diagnosisSequence: Optional[List[int]] = field(default_factory=list)  # Diagnoses applicable for this service or product.
    procedureSequence: Optional[List[int]] = field(default_factory=list)  # Procedures applicable for this service or product.
    informationSequence: Optional[List[int]] = field(default_factory=list)  # Exceptions, special conditions and supporting information applicable for this service or product.
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    request: Optional[List[Reference]] = field(default_factory=list)  # Request or Referral for Goods or Service to be rendered.
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    programCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies the program under which this may be recovered.
    serviced: Optional[Any] = None  # The date or dates when the service or product was supplied, performed or completed.
    location: Optional[Any] = None  # Where the product or service was provided.
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the group (if a grouper) or the line item. Net = unit price * quanti...
    udi: Optional[List[Reference]] = field(default_factory=list)  # Unique Device Identifiers associated with this line item.
    bodySite: Optional[List[BackboneElement]] = field(default_factory=list)  # Physical location where the service is performed or applies.
    subSite: Optional[List[CodeableConcept]] = field(default_factory=list)  # A region or surface of the bodySite, e.g. limb region or tooth surface(s).
    encounter: Optional[List[Reference]] = field(default_factory=list)  # Healthcare encounters related to this claim.
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[BackboneElement] = None  # The high-level results of the adjudication if adjudication has been performed.
    decision: Optional[CodeableConcept] = None  # The result of the claim, predetermination, or preauthorization adjudication.
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reasons for the result of the claim, predetermination, or preauthorization adjudication.
    preAuthRef: Optional[str] = None  # Reference from the Insurer which is used in later communications which refers to this adjudication.
    preAuthPeriod: Optional[Period] = None  # The time frame during which this authorization is effective.
    adjudication: Optional[List[BackboneElement]] = field(default_factory=list)  # If this item is a group then the values here are a summary of the adjudication of the detail item...
    amount: Optional[Money] = None  # Monetary amount associated with the category.
    detail: Optional[List[BackboneElement]] = field(default_factory=list)  # Second-tier of goods and services.
    subDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # Third-tier of goods and services.

@dataclass
class ExplanationOfBenefitItemBodySite:
    """
    ExplanationOfBenefitItemBodySite nested class.
    """

    site: List[Any] = field(default_factory=list)  # Physical service site on the patient (limb, tooth, etc.).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    subSite: Optional[List[CodeableConcept]] = field(default_factory=list)  # A region or surface of the bodySite, e.g. limb region or tooth surface(s).

@dataclass
class ExplanationOfBenefitItemReviewOutcome:
    """
    ExplanationOfBenefitItemReviewOutcome nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    decision: Optional[CodeableConcept] = None  # The result of the claim, predetermination, or preauthorization adjudication.
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reasons for the result of the claim, predetermination, or preauthorization adjudication.
    preAuthRef: Optional[str] = None  # Reference from the Insurer which is used in later communications which refers to this adjudication.
    preAuthPeriod: Optional[Period] = None  # The time frame during which this authorization is effective.

@dataclass
class ExplanationOfBenefitItemAdjudication:
    """
    ExplanationOfBenefitItemAdjudication nested class.
    """

    category: Optional[CodeableConcept] = None  # A code to indicate the information type of this adjudication record. Information types may includ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    reason: Optional[CodeableConcept] = None  # A code supporting the understanding of the adjudication result and explaining variance from expec...
    amount: Optional[Money] = None  # Monetary amount associated with the category.
    quantity: Optional[Quantity] = None  # A non-monetary value associated with the category. Mutually exclusive to the amount element above.

@dataclass
class ExplanationOfBenefitItemDetail:
    """
    ExplanationOfBenefitItemDetail nested class.
    """

    sequence: Optional[int] = None  # A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    programCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies the program under which this may be recovered.
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the group (if a grouper) or the line item.detail. Net = unit price *...
    udi: Optional[List[Reference]] = field(default_factory=list)  # Unique Device Identifiers associated with this line item.
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.
    subDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # Third-tier of goods and services.

@dataclass
class ExplanationOfBenefitItemDetailSubDetail:
    """
    ExplanationOfBenefitItemDetailSubDetail nested class.
    """

    sequence: Optional[int] = None  # A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    programCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies the program under which this may be recovered.
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the line item.detail.subDetail. Net = unit price * quantity * factor.
    udi: Optional[List[Reference]] = field(default_factory=list)  # Unique Device Identifiers associated with this line item.
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.

@dataclass
class ExplanationOfBenefitAddItem:
    """
    ExplanationOfBenefitAddItem nested class.
    """

    site: List[Any] = field(default_factory=list)  # Physical service site on the patient (limb, tooth, etc.).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    itemSequence: Optional[List[int]] = field(default_factory=list)  # Claim items which this service line is intended to replace.
    detailSequence: Optional[List[int]] = field(default_factory=list)  # The sequence number of the details within the claim item which this line is intended to replace.
    subDetailSequence: Optional[List[int]] = field(default_factory=list)  # The sequence number of the sub-details woithin the details within the claim item which this line ...
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
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
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
class ExplanationOfBenefitAddItemBodySite:
    """
    ExplanationOfBenefitAddItemBodySite nested class.
    """

    site: List[Any] = field(default_factory=list)  # Physical service site on the patient (limb, tooth, etc.).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    subSite: Optional[List[CodeableConcept]] = field(default_factory=list)  # A region or surface of the bodySite, e.g. limb region or tooth surface(s).

@dataclass
class ExplanationOfBenefitAddItemDetail:
    """
    ExplanationOfBenefitAddItemDetail nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
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
class ExplanationOfBenefitAddItemDetailSubDetail:
    """
    ExplanationOfBenefitAddItemDetailSubDetail nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    revenue: Optional[CodeableConcept] = None  # The type of revenue or cost center providing the product and/or service.
    productOrService: Optional[CodeableConcept] = None  # When the value is a group code then this item collects a set of related item details, otherwise t...
    productOrServiceEnd: Optional[CodeableConcept] = None  # This contains the end of a range of product, service, drug or other billing codes for the item. T...
    modifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Item typification or modifiers codes to convey additional context for the product or service.
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
    quantity: Optional[Quantity] = None  # The number of repetitions of a service or product.
    unitPrice: Optional[Money] = None  # If the item is not a group then this is the fee for the product or service, otherwise this is the...
    factor: Optional[float] = None  # A real number that represents a multiplier used in determining the overall value of services deli...
    tax: Optional[Money] = None  # The total of taxes applicable for this product or service.
    net: Optional[Money] = None  # The total amount claimed for the addItem.detail.subDetail. Net = unit price * quantity * factor.
    noteNumber: Optional[List[int]] = field(default_factory=list)  # The numbers associated with notes below which apply to the adjudication of this item.
    reviewOutcome: Optional[Any] = None  # The high-level results of the adjudication if adjudication has been performed.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results.

@dataclass
class ExplanationOfBenefitTotal:
    """
    ExplanationOfBenefitTotal nested class.
    """

    category: Optional[CodeableConcept] = None  # A code to indicate the information type of this adjudication record. Information types may includ...
    amount: Optional[Money] = None  # Monetary total amount associated with the category.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ExplanationOfBenefitPayment:
    """
    ExplanationOfBenefitPayment nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Whether this represents partial or complete payment of the benefits payable.
    adjustment: Optional[Money] = None  # Total amount of all adjustments to this payment included in this transaction which are not relate...
    adjustmentReason: Optional[CodeableConcept] = None  # Reason for the payment adjustment.
    date: Optional[str] = None  # Estimated date the payment will be issued or the actual issue date of payment.
    amount: Optional[Money] = None  # Benefits payable less any payment adjustment.
    identifier: Optional[Identifier] = None  # Issuer's unique identifier for the payment instrument.

@dataclass
class ExplanationOfBenefitProcessNote:
    """
    ExplanationOfBenefitProcessNote nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    number: Optional[int] = None  # A number to uniquely identify a note entry.
    type: Optional[CodeableConcept] = None  # The business purpose of the note text.
    text: Optional[str] = None  # The explanation or description associated with the processing.
    language: Optional[CodeableConcept] = None  # A code to define the language used in the text of the note.

@dataclass
class ExplanationOfBenefitBenefitBalance:
    """
    ExplanationOfBenefitBenefitBalance nested class.
    """

    category: Optional[CodeableConcept] = None  # Code to identify the general type of benefits under which products and services are provided.
    type: Optional[CodeableConcept] = None  # Classification of benefit being provided.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    excluded: Optional[bool] = None  # True if the indicated class of service is excluded from the plan, missing or False indicates the ...
    name: Optional[str] = None  # A short name or tag for the benefit.
    description: Optional[str] = None  # A richer description of the benefit or services covered.
    network: Optional[CodeableConcept] = None  # Is a flag to indicate whether the benefits refer to in-network providers or out-of-network provid...
    unit: Optional[CodeableConcept] = None  # Indicates if the benefits apply to an individual or to the family.
    term: Optional[CodeableConcept] = None  # The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'.
    financial: Optional[List[BackboneElement]] = field(default_factory=list)  # Benefits Used to date.
    allowed: Optional[Any] = None  # The quantity of the benefit which is permitted under the coverage.
    used: Optional[Any] = None  # The quantity of the benefit which have been consumed to date.

@dataclass
class ExplanationOfBenefitBenefitBalanceFinancial:
    """
    ExplanationOfBenefitBenefitBalanceFinancial nested class.
    """

    type: Optional[CodeableConcept] = None  # Classification of benefit being provided.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    allowed: Optional[Any] = None  # The quantity of the benefit which is permitted under the coverage.
    used: Optional[Any] = None  # The quantity of the benefit which have been consumed to date.


@dataclass
class ExplanationOfBenefit(FHIRResource):
    """
    This resource provides: the claim details; adjudication details from the processing of a Claim; and optionally account balance information, for informing the subscriber of the benefits provided.
    """

    status: Optional[str] = None  # The status of the resource instance.
    type: Optional[CodeableConcept] = None  # The category of claim, e.g. oral, pharmacy, vision, institutional, professional.
    use: Optional[str] = None  # A code to indicate whether the nature of the request is: Claim - A request to an Insurer to adjud...
    patient: Optional[Reference] = None  # The party to whom the professional services and/or products have been supplied or are being consi...
    created: Optional[str] = None  # The date this resource was created.
    outcome: Optional[str] = None  # The outcome of the claim, predetermination, or preauthorization processing.
    resourceType: str = "ExplanationOfBenefit"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this explanation of benefit.
    traceNumber: Optional[List[Identifier]] = field(default_factory=list)  # Trace number for tracking purposes. May be defined at the jurisdiction level or between trading p...
    subType: Optional[CodeableConcept] = None  # A finer grained suite of claim type codes which may convey additional information such as Inpatie...
    billablePeriod: Optional[Period] = None  # The period for which charges are being submitted.
    enterer: Optional[Reference] = None  # Individual who created the claim, predetermination or preauthorization.
    insurer: Optional[Reference] = None  # The party responsible for authorization, adjudication and reimbursement.
    provider: Optional[Reference] = None  # The provider which is responsible for the claim, predetermination or preauthorization.
    priority: Optional[CodeableConcept] = None  # The provider-required urgency of processing the request. Typical values include: stat, normal def...
    fundsReserveRequested: Optional[CodeableConcept] = None  # A code to indicate whether and for whom funds are to be reserved for future claims.
    fundsReserve: Optional[CodeableConcept] = None  # A code, used only on a response to a preauthorization, to indicate whether the benefits payable h...
    related: Optional[List[BackboneElement]] = field(default_factory=list)  # Other claims which are related to this claim such as prior submissions or claims for related serv...
    prescription: Optional[Reference] = None  # Prescription is the document/authorization given to the claim author for them to provide products...
    originalPrescription: Optional[Reference] = None  # Original prescription which has been superseded by this prescription to support the dispensing of...
    event: Optional[List[BackboneElement]] = field(default_factory=list)  # Information code for an event with a corresponding date or period.
    payee: Optional[BackboneElement] = None  # The party to be reimbursed for cost of the products and services according to the terms of the po...
    referral: Optional[Reference] = None  # The referral information received by the claim author, it is not to be used when the author gener...
    encounter: Optional[List[Reference]] = field(default_factory=list)  # Healthcare encounters related to this claim.
    facility: Optional[Reference] = None  # Facility where the services were provided.
    claim: Optional[Reference] = None  # The business identifier for the instance of the adjudication request: claim predetermination or p...
    claimResponse: Optional[Reference] = None  # The business identifier for the instance of the adjudication response: claim, predetermination or...
    decision: Optional[CodeableConcept] = None  # The result of the claim, predetermination, or preauthorization adjudication.
    disposition: Optional[str] = None  # A human readable description of the status of the adjudication.
    preAuthRef: Optional[List[str]] = field(default_factory=list)  # Reference from the Insurer which is used in later communications which refers to this adjudication.
    preAuthRefPeriod: Optional[List[Period]] = field(default_factory=list)  # The timeframe during which the supplied preauthorization reference may be quoted on claims to obt...
    diagnosisRelatedGroup: Optional[CodeableConcept] = None  # A package billing code or bundle code used to group products and services to a particular health ...
    careTeam: Optional[List[BackboneElement]] = field(default_factory=list)  # The members of the team who provided the products and services.
    supportingInfo: Optional[List[BackboneElement]] = field(default_factory=list)  # Additional information codes regarding exceptions, special considerations, the condition, situati...
    diagnosis: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about diagnoses relevant to the claim items.
    procedure: Optional[List[BackboneElement]] = field(default_factory=list)  # Procedures performed on the patient relevant to the billing items with the claim.
    precedence: Optional[int] = None  # This indicates the relative order of a series of EOBs related to different coverages for the same...
    insurance: Optional[List[BackboneElement]] = field(default_factory=list)  # Financial instruments for reimbursement for the health care products and services specified on th...
    accident: Optional[BackboneElement] = None  # Details of a accident which resulted in injuries which required the products and services listed ...
    patientPaid: Optional[Money] = None  # The amount paid by the patient, in total at the claim claim level or specifically for the item an...
    item: Optional[List[BackboneElement]] = field(default_factory=list)  # A claim line. Either a simple (a product or service) or a 'group' of details which can also be a ...
    addItem: Optional[List[BackboneElement]] = field(default_factory=list)  # The first-tier service adjudications for payor added product or service lines.
    adjudication: Optional[List[Any]] = field(default_factory=list)  # The adjudication results which are presented at the header level rather than at the line-item or ...
    total: Optional[List[BackboneElement]] = field(default_factory=list)  # Categorized monetary totals for the adjudication.
    payment: Optional[BackboneElement] = None  # Payment details for the adjudication of the claim.
    formCode: Optional[CodeableConcept] = None  # A code for the form to be used for printing the content.
    form: Optional[Attachment] = None  # The actual form, by reference or inclusion, for printing the content or an EOB.
    processNote: Optional[List[BackboneElement]] = field(default_factory=list)  # A note that describes or explains adjudication results in a human readable form.
    benefitPeriod: Optional[Period] = None  # The term of the benefits documented in this response.
    benefitBalance: Optional[List[BackboneElement]] = field(default_factory=list)  # Balance by Benefit Category.