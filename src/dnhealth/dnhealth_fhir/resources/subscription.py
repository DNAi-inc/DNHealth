# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Subscription resource.

Subscription represents a server push subscription criteria.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
)


@dataclass
class SubscriptionChannel:
    """
    FHIR Subscription.channel complex type.
    
    The channel on which to report matches to the criteria.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[str] = None  # rest-hook | websocket | email | sms | message (required)
    endpoint: Optional[str] = None  # Where the channel points to
    payload: Optional[str] = None  # MIME type to send
    header: List[str] = field(default_factory=list)  # Usage depends on the channel type


@dataclass
class Subscription(DomainResource):
    """
    FHIR R4 Subscription resource.
    
    Represents a server push subscription criteria.
    Extends DomainResource.
    """
    
    resourceType: str = "Subscription"
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce status is provided.
    status: Optional[str] = None  # requested | active | error | off | entered-in-error (required)
    # Contact
    contact: List[Any] = field(default_factory=list)  # Contact details for source (ContactPoint)
    # End
    end: Optional[str] = None  # When to automatically delete the subscription
    # Reason
    # Note: reason is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce reason is provided.
    reason: Optional[str] = None  # Description of why this subscription was created (required)
    # Criteria
    # Note: criteria is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce criteria is provided.
    criteria: Optional[str] = None  # Rule for server push (required)
    # Error
    error: Optional[str] = None  # Latest error note
    # Channel
    # Note: channel is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce channel is provided.
    channel: Optional[SubscriptionChannel] = None  # The channel on which to report matches to the criteria (required)

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

