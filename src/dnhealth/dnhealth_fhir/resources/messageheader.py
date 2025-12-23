# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MessageHeader resource.

Complete MessageHeader resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Reference,
    CodeableConcept,
    ContactPoint,
    Coding,
)


@dataclass
class MessageHeaderSource:
    """
    Message source application.
    
    The source application from which this message originated.
    """

    name: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None
    contact: Optional[ContactPoint] = None
    endpoint: Optional[str] = None  # URI
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MessageHeaderDestination:
    """
    Message destination application(s).
    
    The destination application which the message is intended for.
    """

    name: Optional[str] = None
    target: Optional[Reference] = None
    # Note: endpoint is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce endpoint is provided.
    endpoint: Optional[str] = None  # Actual destination address or id (required)
    receiver: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MessageHeaderResponse:
    """
    If this is a reply to prior message.
    
    Information about the message that this message is a response to.
    """

    # Note: identifier is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce identifier is provided.
    identifier: Optional[str] = None  # Id of original message (required)
    # Note: code is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce code is provided.
    code: Optional[str] = None  # ok | transient-error | fatal-error (required)
    details: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MessageHeader(FHIRResource):
    """
    FHIR R4 MessageHeader resource.

    Represents the header information for a message exchange that is either
    requesting or responding to an action.
    """

    resourceType: str = "MessageHeader"
    # Event coding
    eventCoding: Optional["Coding"] = None
    # Event URI
    eventUri: Optional[str] = None
    # Destination
    destination: List[MessageHeaderDestination] = field(default_factory=list)
    # Receiver
    receiver: Optional[Reference] = None
    # Sender
    sender: Optional[Reference] = None
    # Enterer
    enterer: Optional[Reference] = None
    # Author
    author: Optional[Reference] = None
    # Source
    # Note: source is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce source is provided.
    source: Optional[MessageHeaderSource] = None  # Message source application (required)
    # Responsible
    responsible: Optional[Reference] = None
    # Reason
    reason: Optional[CodeableConcept] = None
    # Response
    response: Optional[MessageHeaderResponse] = None
    # Focus
    focus: List[Reference] = field(default_factory=list)
    # Definition
    definition: Optional[str] = None  # Canonical URL to message definition

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
