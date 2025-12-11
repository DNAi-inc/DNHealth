# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Slot resource.

Complete Slot resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
)


@dataclass
class Slot(FHIRResource):
    """
    FHIR R4 Slot resource.

    Represents a slot of time on a schedule that may be available for
    booking appointments.
    """

    resourceType: str = "Slot"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Service category
    serviceCategory: List[CodeableConcept] = field(default_factory=list)
    # Service type
    serviceType: List[CodeableConcept] = field(default_factory=list)
    # Specialty
    specialty: List[CodeableConcept] = field(default_factory=list)
    # Appointment type
    appointmentType: Optional[CodeableConcept] = None
    # Schedule
    schedule: Reference  # The schedule resource that this slot defines an interval of status information for (required)
    # Status
    status: str  # busy | free | busy-unavailable | busy-tentative | entered-in-error (required)
    # Start
    start: str  # Date/Time that the slot is to begin (required) - ISO 8601 dateTime
    # End
    end: str  # Date/Time that the slot is to conclude (required) - ISO 8601 dateTime
    # Overbooked
    overbooked: Optional[bool] = None
    # Comment
    comment: Optional[str] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
