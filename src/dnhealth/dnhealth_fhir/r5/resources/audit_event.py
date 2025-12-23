# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 AuditEvent resource.

A record of an event relevant for purposes such as operations, privacy, security, maintenance, and performance analysis.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, Extension, Period, Quantity, Range, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class AuditEventOutcome:
    """
    AuditEventOutcome nested class.
    """

    code: Optional[Coding] = None  # Indicates whether the event succeeded or failed.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    detail: Optional[List[CodeableConcept]] = field(default_factory=list)  # Additional details about the error. This may be a text description of the error or a system code ...

@dataclass
class AuditEventAgent:
    """
    AuditEventAgent nested class.
    """

    who: Optional[Reference] = None  # Reference to who this agent is that was involved in the event.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The Functional Role of the user when performing the event.
    role: Optional[List[CodeableConcept]] = field(default_factory=list)  # The structural roles of the agent indicating the agent's competency. The security role enabling t...
    requestor: Optional[bool] = None  # Indicator that the user is or is not the requestor, or initiator, for the event being audited.
    location: Optional[Reference] = None  # Where the agent location is known, the agent location when the event occurred.
    policy: Optional[List[str]] = field(default_factory=list)  # Where the policy(ies) are known that authorized the agent participation in the event. Typically, ...
    network: Optional[Any] = None  # When the event utilizes a network there should be an agent describing the local system, and an ag...
    authorization: Optional[List[CodeableConcept]] = field(default_factory=list)  # The authorization (e.g., PurposeOfUse) that was used during the event being recorded.

@dataclass
class AuditEventSource:
    """
    AuditEventSource nested class.
    """

    observer: Optional[Reference] = None  # Identifier of the source where the event was detected.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    site: Optional[Reference] = None  # Logical source location within the healthcare enterprise network.  For example, a hospital or oth...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Code specifying the type of source where event originated.

@dataclass
class AuditEventEntity:
    """
    AuditEventEntity nested class.
    """

    type: Optional[CodeableConcept] = None  # The type of extra detail provided in the value.
    value: Optional[Any] = None  # The  value of the extra detail.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    what: Optional[Reference] = None  # Identifies a specific instance of the entity. The reference should be version specific. This is a...
    role: Optional[CodeableConcept] = None  # Code representing the role the entity played in the event being audited.
    securityLabel: Optional[List[CodeableConcept]] = field(default_factory=list)  # Security labels for the identified entity.
    query: Optional[str] = None  # The query parameters for a query-type entities.
    detail: Optional[List[BackboneElement]] = field(default_factory=list)  # Tagged value pairs for conveying additional information about the entity.
    agent: Optional[List[Any]] = field(default_factory=list)  # The entity is attributed to an agent to express the agent's responsibility for that entity in the...

@dataclass
class AuditEventEntityDetail:
    """
    AuditEventEntityDetail nested class.
    """

    type: Optional[CodeableConcept] = None  # The type of extra detail provided in the value.
    value: Optional[Any] = None  # The  value of the extra detail.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class AuditEvent(FHIRResource):
    """
    A record of an event relevant for purposes such as operations, privacy, security, maintenance, and performance analysis.
    """

    code: Optional[CodeableConcept] = None  # Describes what happened. The most specific code for the event.
    recorded: Optional[str] = None  # The time when the event was recorded.
    agent: List[BackboneElement] = field(default_factory=list)  # An actor taking an active role in the event or activity that is logged.
    source: Optional[BackboneElement] = None  # The actor that is reporting the event.
    resourceType: str = "AuditEvent"
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Classification of the type of event.
    action: Optional[str] = None  # Indicator for type of action performed during the event that generated the audit.
    severity: Optional[str] = None  # Indicates and enables segmentation of various severity including debugging from critical.
    occurred: Optional[Any] = None  # The time or period during which the activity occurred.
    outcome: Optional[BackboneElement] = None  # Indicates whether the event succeeded or failed. A free text descripiton can be given in outcome....
    authorization: Optional[List[CodeableConcept]] = field(default_factory=list)  # The authorization (e.g., PurposeOfUse) that was used during the event being recorded.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Allows tracing of authorizatino for the events and tracking whether proposals/recommendations wer...
    patient: Optional[Reference] = None  # The patient element is available to enable deterministic tracking of activities that involve the ...
    encounter: Optional[Reference] = None  # This will typically be the encounter the event occurred, but some events may be initiated prior t...
    entity: Optional[List[BackboneElement]] = field(default_factory=list)  # Specific instances of data or objects that have been accessed.