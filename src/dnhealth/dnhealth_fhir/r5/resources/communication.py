# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Communication resource.

A clinical or business level record of information being transmitted or shared; e.g. an alert that was sent to a responsible provider, a public health agency communication to a provider/reporter in response to a case report for a reportable condition.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class CommunicationPayload:
    """
    CommunicationPayload nested class.
    """

    content: Optional[Any] = None  # A communicated content (or for multi-part communications, one portion of the communication).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Communication(FHIRResource):
    """
    A clinical or business level record of information being transmitted or shared; e.g. an alert that was sent to a responsible provider, a public health agency communication to a provider/reporter in response to a case report for a reportable condition.
    """

    status: Optional[str] = None  # The status of the transmission.
    resourceType: str = "Communication"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this communication by the performer or other systems which remai...
    instantiatesCanonical: Optional[List[str]] = field(default_factory=list)  # The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhe...
    instantiatesUri: Optional[List[str]] = field(default_factory=list)  # The URL pointing to an externally maintained protocol, guideline, orderset or other definition th...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # An order, proposal or plan fulfilled in whole or in part by this Communication.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event (e.g. Communication, Procedure) of which this particular communication is a compon...
    inResponseTo: Optional[List[Reference]] = field(default_factory=list)  # Prior communication that this communication is in response to.
    statusReason: Optional[CodeableConcept] = None  # Captures the reason for the current state of the Communication.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # The type of message conveyed such as alert, notification, reminder, instruction, etc.
    priority: Optional[str] = None  # Characterizes how quickly the planned or in progress communication must be addressed. Includes co...
    medium: Optional[List[CodeableConcept]] = field(default_factory=list)  # A channel that was used for this communication (e.g. email, fax).
    subject: Optional[Reference] = None  # The patient or group that was the focus of this communication.
    topic: Optional[CodeableConcept] = None  # Description of the purpose/content, similar to a subject line in an email.
    about: Optional[List[Reference]] = field(default_factory=list)  # Other resources that pertain to this communication and to which this communication should be asso...
    encounter: Optional[Reference] = None  # The Encounter during which this Communication was created or to which the creation of this record...
    sent: Optional[str] = None  # The time when this communication was sent.
    received: Optional[str] = None  # The time when this communication arrived at the destination.
    recipient: Optional[List[Reference]] = field(default_factory=list)  # The entity (e.g. person, organization, clinical information system, care team or device) which is...
    sender: Optional[Reference] = None  # The entity (e.g. person, organization, clinical information system, or device) which is the sourc...
    reason: Optional[List[Any]] = field(default_factory=list)  # The reason or justification for the communication.
    payload: Optional[List[BackboneElement]] = field(default_factory=list)  # Text, attachment(s), or resource(s) that was communicated to the recipient.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional notes or commentary about the communication by the sender, receiver or other intereste...