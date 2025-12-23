# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 AppointmentResponse resource.

A reply to an appointment request for a patient and/or practitioner(s), such as a confirmation or rejection.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Reference
from typing import List, Optional

@dataclass
class AppointmentResponse(FHIRResource):
    """
    A reply to an appointment request for a patient and/or practitioner(s), such as a confirmation or rejection.
    """

    appointment: Optional[Reference] = None  # Appointment that this response is replying to.
    participantStatus: Optional[str] = None  # Participation status of the participant. When the status is declined or tentative if the start/en...
    resourceType: str = "AppointmentResponse"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # This records identifiers associated with this appointment response concern that are defined by bu...
    proposedNewTime: Optional[bool] = None  # Indicates that the response is proposing a different time that was initially requested.  The new ...
    start: Optional[str] = None  # Date/Time that the appointment is to take place, or requested new start time.
    end: Optional[str] = None  # This may be either the same as the appointment request to confirm the details of the appointment,...
    participantType: Optional[List[CodeableConcept]] = field(default_factory=list)  # Role of participant in the appointment.
    actor: Optional[Reference] = None  # A Person, Location, HealthcareService, or Device that is participating in the appointment.
    comment: Optional[str] = None  # Additional comments about the appointment.
    recurring: Optional[bool] = None  # Indicates that this AppointmentResponse applies to all occurrences in a recurring request.
    occurrenceDate: Optional[str] = None  # The original date within a recurring request. This could be used in place of the recurrenceId to ...
    recurrenceId: Optional[int] = None  # The recurrence ID (sequence number) of the specific appointment when responding to a recurring re...