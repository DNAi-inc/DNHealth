# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Endpoint resource.

Endpoint represents the technical details of a connection to a system where data can be sent or received.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, ContactPoint, Coding, Period
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class Endpoint(DomainResource):
    """
    FHIR R4 Endpoint resource.
    
    Represents the technical details of a connection to a system where data can be sent or received.
    Extends DomainResource.
    """
    
    resourceType: str = "Endpoint"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Identifies this endpoint across multiple systems
    # Status
    status: str  # active | suspended | error | off | entered-in-error | test (required)
    # Connection Type
    connectionType: Coding  # Protocol/Profile/Standard to be used with this endpoint connection (required)
    # Name
    name: Optional[str] = None  # A name that this endpoint can be identified by
    # Managing Organization
    managingOrganization: Optional[Reference] = None  # Organization that manages this endpoint
    # Contact
    contact: List[ContactPoint] = field(default_factory=list)  # Contact details for source and target systems
    # Period
    period: Optional[Period] = None  # Interval the endpoint is expected to be operational
    # Payload Type
    payloadType: List[CodeableConcept] = field(default_factory=list)  # The type of content that may be used at this endpoint (required)
    # Payload MIME Type
    payloadMimeType: List[str] = field(default_factory=list)  # Mimetype to send. If not specified, the content could be anything (including no payload)
    # Address
    address: str  # The technical base address for connecting to this endpoint (required)
    # Header
    header: List[str] = field(default_factory=list)  # Additional headers / information to send as part of the notification

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


