# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MessageDefinition resource.

MessageDefinition defines the structure of a message that can be sent between systems.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext


@dataclass
class MessageDefinitionFocus:
    """
    FHIR MessageDefinition.focus complex type.
    
    Identifies the resource (or resources) that are being addressed by the event.
    """
    
    code: str  # Type of resource (required)
    min: int  # Minimum number of focuses of this type (required)
    profile: Optional[str] = None  # Profile that must be adhered to
    max: Optional[str] = None  # Maximum number of focuses of this type
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class MessageDefinitionAllowedResponse:
    """
    FHIR MessageDefinition.allowedResponse complex type.
    
    Responses to this message.
    """
    
    message: str  # Canonical reference to message definition (required)
    situation: Optional[str] = None  # When should this response be used
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class MessageDefinition(MetadataResource):
    """
    FHIR R4 MessageDefinition resource.
    
    Defines the structure of a message that can be sent between systems.
    Extends MetadataResource.
    """
    
    resourceType: str = "MessageDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Any] = field(default_factory=list)  # Additional identifiers
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this message definition
    # Title
    title: Optional[str] = None  # Title for this message definition
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Purpose
    purpose: Optional[str] = None  # Why this message definition is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Base
    base: Optional[str] = None  # Definition this one is based on
    # Parent
    parent: List[str] = field(default_factory=list)  # Protocol/workflow this is part of
    # Event Coding
    eventCoding: Optional[Any] = None  # Event code or link to the EventDefinition
    # Event URI
    eventUri: Optional[str] = None  # Event code or link to the EventDefinition
    # Category
    category: Optional[str] = None  # consequence | currency | notification
    # Focus
    focus: List[MessageDefinitionFocus] = field(default_factory=list)  # Resource(s) that are the subject of the event
    # Response Required
    responseRequired: Optional[str] = None  # always | never | on-error | sometimes
    # Allowed Response
    allowedResponse: List[MessageDefinitionAllowedResponse] = field(default_factory=list)  # Responses to this message
    # Graph
    graph: List[str] = field(default_factory=list)  # Canonical reference to a GraphDefinition resource

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
