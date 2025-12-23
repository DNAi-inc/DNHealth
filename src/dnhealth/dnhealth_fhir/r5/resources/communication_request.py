# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 CommunicationRequest resource.

A request to convey information; e.g. the CDS system proposes that an alert be sent to a responsible provider, the CDS system proposes that the public health agency be notified about a reportable condition.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class CommunicationRequestPayload:
    """
    CommunicationRequestPayload nested class.
    """

    content: Optional[Any] = None  # The communicated content (or for multi-part communications, one portion of the communication).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class CommunicationRequest(FHIRResource):
    """
    A request to convey information; e.g. the CDS system proposes that an alert be sent to a responsible provider, the CDS system proposes that the public health agency be notified about a reportable condition.
    """

    status: Optional[str] = None  # The status of the proposal or order.
    intent: Optional[str] = None  # Indicates the level of authority/intentionality associated with the CommunicationRequest and wher...
    resourceType: str = "CommunicationRequest"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this communication request by the performer or other systems whi...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan or proposal that is fulfilled in whole or in part by this request.
    replaces: Optional[List[Reference]] = field(default_factory=list)  # Completed or terminated request(s) whose function is taken by this new request.
    groupIdentifier: Optional[Identifier] = None  # A shared identifier common to multiple independent Request instances that were activated/authoriz...
    statusReason: Optional[CodeableConcept] = None  # Captures the reason for the current state of the CommunicationRequest.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # The type of message to be sent such as alert, notification, reminder, instruction, etc.
    priority: Optional[str] = None  # Characterizes how quickly the proposed act must be initiated. Includes concepts such as stat, urg...
    doNotPerform: Optional[bool] = None  # If true indicates that the CommunicationRequest is asking for the specified action to *not* occur.
    medium: Optional[List[CodeableConcept]] = field(default_factory=list)  # A channel that was used for this communication (e.g. email, fax).
    subject: Optional[Reference] = None  # The patient or group that is the focus of this communication request.
    about: Optional[List[Reference]] = field(default_factory=list)  # Other resources that pertain to this communication request and to which this communication reques...
    encounter: Optional[Reference] = None  # The Encounter during which this CommunicationRequest was created or to which the creation of this...
    payload: Optional[List[BackboneElement]] = field(default_factory=list)  # Text, attachment(s), or resource(s) to be communicated to the recipient.
    occurrence: Optional[Any] = None  # The time when this communication is to occur.
    authoredOn: Optional[str] = None  # For draft requests, indicates the date of initial creation.  For requests with other statuses, in...
    requester: Optional[Reference] = None  # The device, individual, or organization who asks for the information to be shared.
    recipient: Optional[List[Reference]] = field(default_factory=list)  # The entity (e.g. person, organization, clinical information system, device, group, or care team) ...
    informationProvider: Optional[List[Reference]] = field(default_factory=list)  # The entity (e.g. person, organization, clinical information system, or device) which is to be the...
    reason: Optional[List[Any]] = field(default_factory=list)  # Describes why the request is being made in coded or textual form.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the request by the requester, sender, recipient, subject or other participants.