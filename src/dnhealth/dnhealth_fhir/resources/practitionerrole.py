# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 PractitionerRole resource.

Complete PractitionerRole resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    ContactPoint,
)


@dataclass
class PractitionerRoleAvailableTime:
    """
    Times the Service Site is available.
    
    A collection of times that the Service Site is available.
    """

    daysOfWeek: List[str] = field(default_factory=list)  # mon | tue | wed | thu | fri | sat | sun
    allDay: Optional[bool] = None
    availableStartTime: Optional[str] = None  # Time (HH:MM:SS)
    availableEndTime: Optional[str] = None  # Time (HH:MM:SS)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class PractitionerRoleNotAvailable:
    """
    Not available during this time due to provided reason.
    
    The HealthcareService is not available during this period of time due
    to the provided reason.
    """

    description: str  # Reason presented to the user explaining why time not available (required)
    during: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class PractitionerRole(FHIRResource):
    """
    FHIR R4 PractitionerRole resource.

    Represents a specific set of Roles/Locations/specialties/services that
    a practitioner may perform at an organization for a period of time.
    """

    resourceType: str = "PractitionerRole"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Active
    active: Optional[bool] = None
    # Period
    period: Optional[Period] = None
    # Practitioner
    practitioner: Optional[Reference] = None
    # Organization
    organization: Optional[Reference] = None
    # Code
    code: List[CodeableConcept] = field(default_factory=list)
    # Specialty
    specialty: List[CodeableConcept] = field(default_factory=list)
    # Location
    location: List[Reference] = field(default_factory=list)
    # Healthcare service
    healthcareService: List[Reference] = field(default_factory=list)
    # Telecom
    telecom: List[ContactPoint] = field(default_factory=list)
    # Available time
    availableTime: List[PractitionerRoleAvailableTime] = field(default_factory=list)
    # Not available
    notAvailable: List[PractitionerRoleNotAvailable] = field(default_factory=list)
    # Availability exceptions
    availabilityExceptions: Optional[str] = None
    # Endpoint
    endpoint: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
