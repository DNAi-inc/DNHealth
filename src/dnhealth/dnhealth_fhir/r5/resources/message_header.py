# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MessageHeader resource.

The header for a message exchange that is either requesting or responding to an action.  The reference(s) that are the subject of the action as well as other information related to the action are typically transmitted in a bundle in which the MessageHeader resource instance is the first resource in the bundle.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactPoint, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class MessageHeaderDestination:
    """
    MessageHeaderDestination nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    endpoint: Optional[Any] = None  # Indicates where the message should be routed.
    name: Optional[str] = None  # Human-readable name for the target system.
    target: Optional[Reference] = None  # Identifies the target end system in situations where the initial message transmission is to an in...
    receiver: Optional[Reference] = None  # Allows data conveyed by a message to be addressed to a particular person or department when routi...

@dataclass
class MessageHeaderSource:
    """
    MessageHeaderSource nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    endpoint: Optional[Any] = None  # Identifies the routing target to send acknowledgements to.
    name: Optional[str] = None  # Human-readable name for the source system.
    software: Optional[str] = None  # May include configuration or other information useful in debugging.
    version: Optional[str] = None  # Can convey versions of multiple systems in situations where a message passes through multiple hands.
    contact: Optional[ContactPoint] = None  # An e-mail, phone, website or other contact point to use to resolve issues with message communicat...

@dataclass
class MessageHeaderResponse:
    """
    MessageHeaderResponse nested class.
    """

    identifier: Optional[Identifier] = None  # The Bundle.identifier of the message to which this message is a response.
    code: Optional[str] = None  # Code that identifies the type of response to the message - whether it was successful or not, and ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    details: Optional[Reference] = None  # Full details of any issues found in the message.


@dataclass
class MessageHeader(FHIRResource):
    """
    The header for a message exchange that is either requesting or responding to an action.  The reference(s) that are the subject of the action as well as other information related to the action are typically transmitted in a bundle in which the MessageHeader resource instance is the first resource in the bundle.
    """

    event: Optional[Any] = None  # Code that identifies the event this message represents and connects it with its definition. Event...
    source: Optional[BackboneElement] = None  # The source application from which this message originated.
    resourceType: str = "MessageHeader"
    destination: Optional[List[BackboneElement]] = field(default_factory=list)  # The destination application which the message is intended for.
    sender: Optional[Reference] = None  # Identifies the sending system to allow the use of a trust relationship.
    author: Optional[Reference] = None  # The logical author of the message - the personor device that decided the described event should h...
    responsible: Optional[Reference] = None  # The person or organization that accepts overall responsibility for the contents of the message. T...
    reason: Optional[CodeableConcept] = None  # Coded indication of the cause for the event - indicates  a reason for the occurrence of the event...
    response: Optional[BackboneElement] = None  # Information about the message that this message is a response to.  Only present if this message i...
    focus: Optional[List[Reference]] = field(default_factory=list)  # The actual data of the message - a reference to the root/focus class of the event. This is allowe...
    definition: Optional[str] = None  # Permanent link to the MessageDefinition for this message.