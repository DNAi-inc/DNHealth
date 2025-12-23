# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 AuditEvent resource.

Complete AuditEvent resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Coding,
    Reference,
    Period,
)


@dataclass
class AuditEventAgent:
    """
    Actor involved in the event.
    
    An actor taking an active role in the event or activity that is logged.
    """

    type: Optional[CodeableConcept] = None
    role: List[CodeableConcept] = field(default_factory=list)
    who: Optional[Reference] = None
    altId: Optional[str] = None
    name: Optional[str] = None
    # Note: requestor is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce requestor is provided.
    requestor: Optional[bool] = None  # Whether user is initiator (required)
    location: Optional[Reference] = None
    policy: List[str] = field(default_factory=list)
    media: Optional[Coding] = None
    network: Optional["AuditEventAgentNetwork"] = None
    purposeOfUse: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class AuditEventAgentNetwork:
    """
    Logical network location for application activity.
    """

    address: Optional[str] = None
    type: Optional[str] = None  # 1 | 2 | 3 | 4 | 5
    extension: List[Extension] = field(default_factory=list)


@dataclass
class AuditEventSource:
    """
    Audit Event Reporter.
    
    The system that is reporting the event.
    """

    site: Optional[str] = None
    # Note: observer is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce observer is provided.
    observer: Optional[Reference] = None  # Identifier of the source (required)
    type: List[Coding] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class AuditEventEntity:
    """
    Data or objects used.
    
    Specific instances of data or objects that have been accessed.
    """

    what: Optional[Reference] = None
    type: Optional[Coding] = None
    role: Optional[Coding] = None
    lifecycle: Optional[Coding] = None
    securityLabel: List[Coding] = field(default_factory=list)
    name: Optional[str] = None
    description: Optional[str] = None
    query: Optional[str] = None  # Base64 encoded
    detail: List["AuditEventEntityDetail"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class AuditEventEntityDetail:
    """
    Additional Information about the entity.
    """

    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[str] = None  # Name of the property (required)
    valueString: Optional[str] = None
    valueBase64Binary: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class AuditEvent(FHIRResource):
    """
    FHIR R4 AuditEvent resource.

    Represents a record of an event made for purposes of maintaining a
    security log.
    """

    resourceType: str = "AuditEvent"
    # Type
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[Coding] = None  # Type/identifier of event (required)
    # Subtype
    subtype: List[Coding] = field(default_factory=list)
    # Action
    action: Optional[str] = None  # C | R | U | D | E
    # Period
    period: Optional[Period] = None
    # Recorded
    # Note: recorded is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce recorded is provided.
    recorded: Optional[str] = None  # Time when the event was recorded (required) - ISO 8601 instant
    # Outcome
    outcome: Optional[str] = None  # 0 | 4 | 8 | 12
    # Outcome description
    outcomeDesc: Optional[str] = None
    # Purpose of event
    purposeOfEvent: List[CodeableConcept] = field(default_factory=list)
    # Agent
    agent: List[AuditEventAgent] = field(default_factory=list)
    # Source
    # Note: source is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce source is provided.
    source: Optional[AuditEventSource] = None  # Audit Event Reporter (required)
    # Entity
    entity: List[AuditEventEntity] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
