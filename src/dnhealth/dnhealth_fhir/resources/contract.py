# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Contract resource.

Contract represents a legally enforceable, formally recorded unilateral or bilateral directive.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Attachment
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ContractContentDefinition:
    """
    FHIR Contract.contentDefinition complex type.
    
    Precise type of Contract as distinct from other types.
    """
    
    type: CodeableConcept  # Content structure type (required)
    subType: Optional[CodeableConcept] = None  # Detailed Content structure type
    publisher: Optional[Reference] = None  # Publisher Entity
    publicationDate: Optional[str] = None  # When published
    publicationStatus: str  # amended | appended | cancelled | disputed | entered-in-error | executable | executed | negotiable | offered | policy | rejected | renewed | revoked | resolved | terminated (required)
    copyright: Optional[str] = None  # Publication Ownership
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractTermAssetContext:
    """
    FHIR Contract.term.asset.context complex type.
    
    Circumstance of the asset.
    """
    
    reference: Optional[Reference] = None  # Creator/custodian of the Contract
    code: List[CodeableConcept] = field(default_factory=list)  # CodeableAssetContext
    text: Optional[str] = None  # Context description
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractTermAssetValuedItem:
    """
    FHIR Contract.term.asset.valuedItem complex type.
    
    Contract Valued Item List.
    """
    
    entityCodeableConcept: Optional[CodeableConcept] = None  # Contract Valued Item Type
    entityReference: Optional[Reference] = None  # Contract Valued Item Type
    identifier: Optional[Identifier] = None  # Contract Valued Item Number
    effectiveTime: Optional[str] = None  # Contract Valued Item Effective Tiem
    quantity: Optional[Any] = None  # Count of Contract Valued Items
    unitPrice: Optional[Any] = None  # Contract Valued Item fee, charge, or cost
    factor: Optional[float] = None  # Contract Valued Item Price Scaling Factor
    points: Optional[float] = None  # Contract Valued Item Difficulty Scaling Factor
    net: Optional[Any] = None  # Total Contract Valued Item Value
    payment: Optional[str] = None  # Terms of valuation
    paymentDate: Optional[str] = None  # When payment is due
    responsible: Optional[Reference] = None  # Who will make payment
    recipient: Optional[Reference] = None  # Who will receive payment
    linkId: List[str] = field(default_factory=list)  # Pointer to specific item
    securityLabelNumber: List[int] = field(default_factory=list)  # Security Labels that define affected terms
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractTermAsset:
    """
    FHIR Contract.term.asset complex type.
    
    Contract Term Asset List.
    """
    
    scope: Optional[CodeableConcept] = None  # Range of asset
    type: List[CodeableConcept] = field(default_factory=list)  # Asset category or type
    typeReference: List[Reference] = field(default_factory=list)  # Associated entities
    subtype: List[CodeableConcept] = field(default_factory=list)  # Asset sub-category
    relationship: Optional[Any] = None  # Kinship of the asset
    context: List[ContractTermAssetContext] = field(default_factory=list)  # Circumstance of the asset
    condition: Optional[str] = None  # Quality desctiption of asset
    periodType: List[CodeableConcept] = field(default_factory=list)  # Asset availability periods
    period: List[Period] = field(default_factory=list)  # Time period of the asset
    usePeriod: List[Period] = field(default_factory=list)  # Time period
    text: Optional[str] = None  # Asset clause or question text
    linkId: List[str] = field(default_factory=list)  # Pointer to specific item
    answer: List[Any] = field(default_factory=list)  # Response to assets
    securityLabelNumber: List[int] = field(default_factory=list)  # Security Labels that define affected terms
    valuedItem: List[ContractTermAssetValuedItem] = field(default_factory=list)  # Contract Valued Item List
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractTermActionSubject:
    """
    FHIR Contract.term.action.subject complex type.
    
    Entity of the action.
    """
    
    reference: List[Reference] = field(default_factory=list)  # Entity of the action
    role: Optional[CodeableConcept] = None  # Role type of the agent
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractTermAction:
    """
    FHIR Contract.term.action complex type.
    
    Action or action group with associated or default items.
    """
    
    doNotPerform: Optional[bool] = None  # True if the term prohibits the action
    type: CodeableConcept  # Type or form of the action (required)
    subject: List[ContractTermActionSubject] = field(default_factory=list)  # Entity of the action
    intent: CodeableConcept  # Purpose for the Contract Term Action (required)
    linkId: List[str] = field(default_factory=list)  # Pointer to specific item
    status: CodeableConcept  # State of the action (required)
    context: Optional[Reference] = None  # Episode associated with action
    contextLinkId: List[str] = field(default_factory=list)  # Pointer to specific item
    occurrenceDateTime: Optional[str] = None  # When action occurs
    occurrencePeriod: Optional[Period] = None  # When action occurs
    occurrenceTiming: Optional[Any] = None  # When action occurs
    requester: List[Reference] = field(default_factory=list)  # Who asked for action
    requesterLinkId: List[str] = field(default_factory=list)  # Pointer to specific item
    performerType: List[CodeableConcept] = field(default_factory=list)  # Kind of service performer
    performerRole: Optional[CodeableConcept] = None  # Competency of the performer
    performer: Optional[Reference] = None  # Who will perform action
    performerLinkId: List[str] = field(default_factory=list)  # Pointer to specific item
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why is action (not) needed?
    reasonReference: List[Reference] = field(default_factory=list)  # Why is action (not) needed?
    reason: List[str] = field(default_factory=list)  # Rationale for the action
    reasonLinkId: List[str] = field(default_factory=list)  # Pointer to specific item
    note: List[Annotation] = field(default_factory=list)  # Comments about the action
    securityLabelNumber: List[int] = field(default_factory=list)  # Action restriction numbers
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractTerm:
    """
    FHIR Contract.term complex type.
    
    One or more Contract Provisions, which may be related and conveyed as a group, and may contain nested groups.
    """
    
    identifier: Optional[Identifier] = None  # Contract Term Number
    issued: Optional[str] = None  # Contract Term Issue Date Time
    applies: Optional[Period] = None  # Contract Term Effective Time
    topicCodeableConcept: Optional[CodeableConcept] = None  # Term Topic
    topicReference: Optional[Reference] = None  # Term Topic
    type: Optional[CodeableConcept] = None  # Contract Term Type or Form
    subType: Optional[CodeableConcept] = None  # Contract Term Type specific classification
    text: Optional[str] = None  # Term Statement
    securityLabel: List[CodeableConcept] = field(default_factory=list)  # Protection for the Term
    offer: Optional[Any] = None  # Context of the Contract term
    asset: List[ContractTermAsset] = field(default_factory=list)  # Contract Term Asset List
    action: List[ContractTermAction] = field(default_factory=list)  # Entity being ascribed responsibility
    group: List["ContractTerm"] = field(default_factory=list)  # Nested Contract Term Group
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractSigner:
    """
    FHIR Contract.signer complex type.
    
    Parties with legal standing in the Contract.
    """
    
    type: CodeableConcept  # Contract Signatory Role (required)
    party: Reference  # Party which is a signator to this Contract (required)
    signature: List[Any] = field(default_factory=list)  # Contract Documentation Signature
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractFriendly:
    """
    FHIR Contract.friendly complex type.
    
    The "patient friendly language" version of the Contract in whole or in parts.
    """
    
    contentAttachment: Optional[Attachment] = None  # Easily comprehended representation of this Contract
    contentReference: Optional[Reference] = None  # Easily comprehended representation of this Contract
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ContractLegal:
    """
    FHIR Contract.legal complex type.
    
    List of Legal expressions or representations of this Contract.
    """
    
    contentAttachment: Optional[Attachment] = None  # Contract Legal Text
    contentReference: Optional[Reference] = None  # Contract Legal Text
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Contract(DomainResource):
    """
    FHIR R4 Contract resource.
    
    Represents a legally enforceable, formally recorded unilateral or bilateral directive.
    Extends DomainResource.
    """
    
    resourceType: str = "Contract"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Contract number
    # URL
    url: Optional[str] = None  # Basal definition
    # Version
    version: Optional[str] = None  # Business edition
    # Status
    status: Optional[str] = None  # amended | appended | cancelled | disputed | entered-in-error | executable | executed | negotiable | offered | policy | rejected | renewed | revoked | resolved | terminated
    # Legal State
    legalState: Optional[CodeableConcept] = None  # Negotiation status
    # Instantiates Canonical
    instantiatesCanonical: Optional[Reference] = None  # Source Contract Definition
    # Instantiates URI
    instantiatesUri: Optional[str] = None  # External Contract Definition
    # Content Derivation
    contentDerivation: Optional[str] = None  # Content derived from the basal information
    # Sub Type
    subType: List[CodeableConcept] = field(default_factory=list)  # Subtype within the context of type
    # Scope
    scope: Optional[CodeableConcept] = None  # Range of Legal Concerns
    # Topic CodeableConcept
    topicCodeableConcept: Optional[CodeableConcept] = None  # Focus of contract interest
    # Topic Reference
    topicReference: Optional[Reference] = None  # Focus of contract interest
    # Type
    type: Optional[CodeableConcept] = None  # Legal instrument category
    # Content Definition
    contentDefinition: Optional[ContractContentDefinition] = None  # Contract precursor content
    # Term
    term: List[ContractTerm] = field(default_factory=list)  # Contract Term List
    # Supporting Info
    supportingInfo: List[Reference] = field(default_factory=list)  # Extra Information
    # Relevant History
    relevantHistory: List[Reference] = field(default_factory=list)  # Key event in Contract History
    # Signer
    signer: List[ContractSigner] = field(default_factory=list)  # Contract Signatory
    # Friendly
    friendly: List[ContractFriendly] = field(default_factory=list)  # Contract Friendly Language
    # Legal
    legal: List[ContractLegal] = field(default_factory=list)  # Contract Legal Language
    # Rule
    rule: List[Any] = field(default_factory=list)  # Computable Contract Language
    # Legally Binding Attachment
    legallyBindingAttachment: Optional[Attachment] = None  # Legally binding Contract
    # Legally Binding Reference
    legallyBindingReference: Optional[Reference] = None  # Legally binding Contract

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


