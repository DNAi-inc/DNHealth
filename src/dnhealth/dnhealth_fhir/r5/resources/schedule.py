# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Schedule resource.

A container for slots of time that may be available for booking appointments.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class Schedule(FHIRResource):
    """
    A container for slots of time that may be available for booking appointments.
    """

    actor: List[Reference] = field(default_factory=list)  # Slots that reference this schedule resource provide the availability details to these referenced ...
    resourceType: str = "Schedule"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # External Ids for this item.
    active: Optional[bool] = None  # Whether this schedule record is in active use or should not be used (such as was entered in error).
    serviceCategory: Optional[List[CodeableConcept]] = field(default_factory=list)  # A broad categorization of the service that is to be performed during this appointment.
    serviceType: Optional[List[Any]] = field(default_factory=list)  # The specific service that is to be performed during this appointment.
    specialty: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specialty of a practitioner that would be required to perform the service requested in this a...
    name: Optional[str] = None  # Further description of the schedule as it would be presented to a consumer while searching.
    planningHorizon: Optional[Period] = None  # The period of time that the slots that reference this Schedule resource cover (even if none exist...
    comment: Optional[str] = None  # Comments on the availability to describe any extended information. Such as custom constraints on ...