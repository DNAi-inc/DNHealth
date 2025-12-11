# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CommunicationRequest resource.

CommunicationRequest represents a request for information to be sent to a receiver.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Timing, Attachment
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CommunicationRequestPayload:
    """
    FHIR CommunicationRequest.payload complex type.
    
    Text, attachment(s), or resource(s) to be communicated to the recipient.
    """
    
    contentString: Optional[str] = None  # Message content
    contentAttachment: Optional[Attachment] = None  # Message content (Attachment type)
    contentReference: Optional[Reference] = None  # Message content (Reference type)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CommunicationRequest(DomainResource):
    """
    FHIR R4 CommunicationRequest resource.
    
    Represents a request for information to be sent to a receiver.
    Extends DomainResource.
    """
    
    resourceType: str = "CommunicationRequest"
    # Required fields (must come before optional fields in dataclasses)
    status: str  # draft | active | on-hold | revoked | completed | entered-in-error | unknown (required)
    # Optional fields (with defaults)
    identifier: List[Identifier] = field(default_factory=list)  # Unique identifier
    basedOn: List[Reference] = field(default_factory=list)  # Fulfills plan or proposal
    replaces: List[Reference] = field(default_factory=list)  # Request(s) replaced by this request
    groupIdentifier: Optional[Identifier] = None  # Composite request this is part of
    # Status Reason
    statusReason: Optional[CodeableConcept] = None  # Reason for current status
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Message category
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Do Not Perform
    doNotPerform: Optional[bool] = None  # True if request is prohibiting action
    # Medium
    medium: List[CodeableConcept] = field(default_factory=list)  # A channel of communication
    # Subject
    subject: Optional[Reference] = None  # Focus of message
    # About
    about: List[Reference] = field(default_factory=list)  # Resources that pertain to this communication request
    # Encounter
    encounter: Optional[Reference] = None  # Encounter created as part of
    # Payload
    payload: List[CommunicationRequestPayload] = field(default_factory=list)  # Message payload
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # When scheduled
    # Occurrence Period
    occurrencePeriod: Optional[Period] = None  # When scheduled
    # Occurrence Timing
    occurrenceTiming: Optional[Timing] = None  # When scheduled
    # Authored On
    authoredOn: Optional[str] = None  # When request transitioned to being actionable
    # Requester
    requester: Optional[Reference] = None  # Who/what is requesting service
    # Recipient
    recipient: List[Reference] = field(default_factory=list)  # Message recipient
    # Sender
    sender: Optional[Reference] = None  # Message sender
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why is communication needed?
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why is communication needed?
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about communication request

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


