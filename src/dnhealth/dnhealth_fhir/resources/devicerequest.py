# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DeviceRequest resource.

DeviceRequest represents a request for a patient to employ a medical device.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Timing, Quantity, Range
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class DeviceRequestParameter:
    """
    FHIR DeviceRequest.parameter complex type.
    
    Specific parameters for the ordered item.
    """
    
    code: Optional[CodeableConcept] = None  # Device detail
    valueCodeableConcept: Optional[CodeableConcept] = None  # Value of detail
    valueQuantity: Optional[Quantity] = None  # Value of detail
    valueRange: Optional[Range] = None  # Value of detail
    valueBoolean: Optional[bool] = None  # Value of detail
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceRequest(DomainResource):
    """
    FHIR R4 DeviceRequest resource.
    
    Represents a request for a patient to employ a medical device.
    Extends DomainResource.
    """
    
    resourceType: str = "DeviceRequest"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External Request identifier
    # Instantiates Canonical
    instantiatesCanonical: List[str] = field(default_factory=list)  # Instantiates FHIR protocol or definition
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)  # Instantiates external protocol or definition
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # What request fulfills
    # Prior Request
    priorRequest: List[Reference] = field(default_factory=list)  # What request replaces
    # Group Identifier
    groupIdentifier: Optional[Identifier] = None  # Identifier of composite request this is part of
    # Status
    status: Optional[str] = None  # draft | active | on-hold | revoked | completed | entered-in-error | unknown
    # Intent
    intent: str  # proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option (required)
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Code Reference
    codeReference: Optional[Reference] = None  # Device requested
    # Code CodeableConcept
    codeCodeableConcept: Optional[CodeableConcept] = None  # Device requested
    # Parameter
    parameter: List[DeviceRequestParameter] = field(default_factory=list)  # Specific parameters for the ordered item
    # Subject
    subject: Reference  # Focus of request (required)
    # Encounter
    encounter: Optional[Reference] = None  # Encounter motivating request
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # Desired time or schedule for use
    # Occurrence Period
    occurrencePeriod: Optional[Period] = None  # Desired time or schedule for use
    # Occurrence Timing
    occurrenceTiming: Optional[Timing] = None  # Desired time or schedule for use
    # Authored On
    authoredOn: Optional[str] = None  # When recorded
    # Requester
    requester: Optional[Reference] = None  # Who/what is requesting device
    # Performer Type
    performerType: Optional[CodeableConcept] = None  # Requested Filler
    # Performer
    performer: Optional[Reference] = None  # Requested Filler
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Coded reason for request
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Coded reason for request
    # Insurance
    insurance: List[Reference] = field(default_factory=list)  # Associated insurance coverage
    # Supporting Info
    supportingInfo: List[Reference] = field(default_factory=list)  # Additional clinical information
    # Note
    note: List[Annotation] = field(default_factory=list)  # Notes or comments
    # Relevant History
    relevantHistory: List[Reference] = field(default_factory=list)  # Request provenance

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


