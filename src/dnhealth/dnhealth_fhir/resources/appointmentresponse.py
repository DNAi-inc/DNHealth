# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 AppointmentResponse resource.

Complete AppointmentResponse resource with all R4 elements.
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
class AppointmentResponse(FHIRResource):
    """
    FHIR R4 AppointmentResponse resource.

    Represents a reply to an appointment request for a patient and/or practitioner(s),
    such as a confirmation or rejection.
    """

    resourceType: str = "AppointmentResponse"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Appointment
    appointment: Reference  # Appointment that this response is replying to (required)
    # Start
    start: Optional[str] = None  # ISO 8601 dateTime
    # End
    end: Optional[str] = None  # ISO 8601 dateTime
    # Participant type
    participantType: List[CodeableConcept] = field(default_factory=list)
    # Actor
    actor: Optional[Reference] = None
    # Participant status
    participantStatus: str  # accepted | declined | tentative | needs-action | entered-in-error
    # Comment
    comment: Optional[str] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
