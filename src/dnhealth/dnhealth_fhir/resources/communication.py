# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Communication resource.

Communication represents an exchange of information between parties.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Attachment
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CommunicationPayload:
    """
    FHIR Communication.payload complex type.
    
    Text, attachment(s), or resource(s) that was communicated to the recipient.
    """
    
    contentString: Optional[str] = None  # Message content
    contentAttachment: Optional[Attachment] = None  # Message content (Attachment type)
    contentReference: Optional[Reference] = None  # Message content (Reference type)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Communication(DomainResource):
    """
    FHIR R4 Communication resource.
    
    Represents an exchange of information between parties.
    Extends DomainResource.
    """
    
    resourceType: str = "Communication"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Unique identifier
    # Instantiates Canonical
    instantiatesCanonical: List[str] = field(default_factory=list)  # Instantiates FHIR protocol or definition
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)  # Instantiates external protocol or definition
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # Request fulfilled by this communication
    # Part Of
    partOf: List[Reference] = field(default_factory=list)  # Part of this action
    # In Response To
    inResponseTo: List[Reference] = field(default_factory=list)  # Reply to
    # Status (required - using Optional with None default to satisfy dataclass ordering, validated in __post_init__)
    status: Optional[str] = None  # preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown (required)
    # Status Reason
    statusReason: Optional[CodeableConcept] = None  # Reason for current status
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Message category
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Medium
    medium: List[CodeableConcept] = field(default_factory=list)  # A channel of communication
    # Subject
    subject: Optional[Reference] = None  # Focus of message
    # Topic
    topic: Optional[CodeableConcept] = None  # Description of the purpose/content
    # About
    about: List[Reference] = field(default_factory=list)  # Resources that pertain to this communication
    # Encounter
    encounter: Optional[Reference] = None  # Encounter created as part of
    # Sent
    sent: Optional[str] = None  # When sent
    # Received
    received: Optional[str] = None  # When received
    # Recipient
    recipient: List[Reference] = field(default_factory=list)  # Message recipient
    # Sender
    sender: Optional[Reference] = None  # Message sender
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Indication for message
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Indication for message
    # Payload
    payload: List[CommunicationPayload] = field(default_factory=list)  # Message payload
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about the communication

    def __post_init__(self):
        """Validate required fields."""
        if self.status is None:
            raise ValueError("status is required for Communication")

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


