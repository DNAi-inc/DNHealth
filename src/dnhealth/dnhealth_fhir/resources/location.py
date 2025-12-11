# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Location resource.

Complete Location resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Address,
    ContactPoint,
    Coding,
)


@dataclass
class LocationPosition:
    """
    Absolute geographic location.
    
    The absolute geographic location of the Location, expressed using the WGS84
    datum (This is the same co-ordinate system used in KML).
    """

    longitude: float  # Longitude with WGS84 datum (required)
    latitude: float  # Latitude with WGS84 datum (required)
    altitude: Optional[float] = None  # Altitude with WGS84 datum
    extension: List[Extension] = field(default_factory=list)


@dataclass
class LocationHoursOfOperation:
    """
    What days/times during a week is this location usually open.
    """

    daysOfWeek: List[str] = field(default_factory=list)  # mon | tue | wed | thu | fri | sat | sun
    allDay: Optional[bool] = None
    openingTime: Optional[str] = None  # Time (HH:MM:SS)
    closingTime: Optional[str] = None  # Time (HH:MM:SS)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Location(FHIRResource):
    """
    FHIR R4 Location resource.

    Represents details and position information for a physical place where
    services are provided and resources and participants may be stored, found,
    contained, or accommodated.
    """

    resourceType: str = "Location"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Status
    status: Optional[str] = None  # active | suspended | inactive
    # Operational status
    operationalStatus: Optional[Coding] = None
    # Name
    name: Optional[str] = None
    # Alias
    alias: List[str] = field(default_factory=list)
    # Description
    description: Optional[str] = None
    # Mode
    mode: Optional[str] = None  # instance | kind
    # Type
    type: List[CodeableConcept] = field(default_factory=list)
    # Telecom
    telecom: List[ContactPoint] = field(default_factory=list)
    # Address
    address: Optional[Address] = None
    # Physical type
    physicalType: Optional[CodeableConcept] = None
    # Position
    position: Optional[LocationPosition] = None
    # Managing organization
    managingOrganization: Optional[Reference] = None
    # Part of
    partOf: Optional[Reference] = None
    # Hours of operation
    hoursOfOperation: List[LocationHoursOfOperation] = field(default_factory=list)
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
