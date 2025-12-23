# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DeviceUseStatement resource.

DeviceUseStatement records the time period over which a device was used by a patient.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Timing
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class DeviceUseStatement(DomainResource):
    """
    FHIR R4 DeviceUseStatement resource.
    
    Records the time period over which a device was used by a patient.
    Extends DomainResource.
    """
    
    resourceType: str = "DeviceUseStatement"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External identifier for this record
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # Fulfills plan, proposal or order
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | completed | entered-in-error | intended | stopped | on-hold (required in FHIR)
    # Subject
    # Note: subject is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce subject is provided.
    subject: Optional[Reference] = None  # Patient using device (required)
    # Derived From
    derivedFrom: List[Reference] = field(default_factory=list)  # Supporting information
    # Timing Timing
    timingTiming: Optional[Timing] = None  # How often the device was used
    # Timing Period
    timingPeriod: Optional[Period] = None  # How often the device was used
    # Timing DateTime
    timingDateTime: Optional[str] = None  # How often the device was used
    # Recorded On
    recordedOn: Optional[str] = None  # When statement was recorded
    # Source
    source: Optional[Reference] = None  # Who made the statement
    # Device
    # Note: device is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce device is provided.
    device: Optional[Reference] = None  # Reference to device used (required)
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why device was used
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why device was used
    # Body Site
    bodySite: Optional[CodeableConcept] = None  # Target body site
    # Note
    note: List[Annotation] = field(default_factory=list)  # Addition details (comments, instructions)

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


