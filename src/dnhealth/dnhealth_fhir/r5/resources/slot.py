# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Slot resource.

A slot of time on a schedule that may be available for booking appointments.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class Slot(FHIRResource):
    """
    A slot of time on a schedule that may be available for booking appointments.
    """

    schedule: Optional[Reference] = None  # The schedule resource that this slot defines an interval of status information.
    status: Optional[str] = None  # busy | free | busy-unavailable | busy-tentative | entered-in-error.
    start: Optional[str] = None  # Date/Time that the slot is to begin.
    end: Optional[str] = None  # Date/Time that the slot is to conclude.
    resourceType: str = "Slot"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # External Ids for this item.
    serviceCategory: Optional[List[CodeableConcept]] = field(default_factory=list)  # A broad categorization of the service that is to be performed during this appointment.
    serviceType: Optional[List[Any]] = field(default_factory=list)  # The type of appointments that can be booked into this slot (ideally this would be an identifiable...
    specialty: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specialty of a practitioner that would be required to perform the service requested in this a...
    appointmentType: Optional[List[CodeableConcept]] = field(default_factory=list)  # The style of appointment or patient that may be booked in the slot (not service type).
    overbooked: Optional[bool] = None  # This slot has already been overbooked, appointments are unlikely to be accepted for this time.
    comment: Optional[str] = None  # Comments on the slot to describe any extended information. Such as custom constraints on the slot.