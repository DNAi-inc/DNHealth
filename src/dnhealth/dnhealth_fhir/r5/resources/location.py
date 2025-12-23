# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Location resource.

Details and position information for a place where services are provided and resources and participants may be stored, found, contained, or accommodated.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class LocationPosition:
    """
    LocationPosition nested class.
    """

    longitude: Optional[float] = None  # Longitude. The value domain and the interpretation are the same as for the text of the longitude ...
    latitude: Optional[float] = None  # Latitude. The value domain and the interpretation are the same as for the text of the latitude el...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    altitude: Optional[float] = None  # Altitude. The value domain and the interpretation are the same as for the text of the altitude el...


@dataclass
class Location(FHIRResource):
    """
    Details and position information for a place where services are provided and resources and participants may be stored, found, contained, or accommodated.
    """

    resourceType: str = "Location"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique code or number identifying the location to its users.
    status: Optional[str] = None  # The status property covers the general availability of the resource, not the current value which ...
    operationalStatus: Optional[Coding] = None  # The operational status covers operation values most relevant to beds (but can also apply to rooms...
    name: Optional[str] = None  # Name of the location as used by humans. Does not need to be unique.
    alias: Optional[List[str]] = field(default_factory=list)  # A list of alternate names that the location is known as, or was known as, in the past.
    description: Optional[str] = None  # Description of the Location, which helps in finding or referencing the place.
    mode: Optional[str] = None  # Indicates whether a resource instance represents a specific location or a class of locations.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Indicates the type of function performed at the location.
    contact: Optional[List[Any]] = field(default_factory=list)  # The contact details of communication devices available at the location. This can include addresse...
    address: Optional[Address] = None  # Physical location.
    form: Optional[CodeableConcept] = None  # Physical form of the location, e.g. building, room, vehicle, road, virtual.
    position: Optional[BackboneElement] = None  # The absolute geographic location of the Location, expressed using the WGS84 datum (This is the sa...
    managingOrganization: Optional[Reference] = None  # The organization responsible for the provisioning and upkeep of the location.
    partOf: Optional[Reference] = None  # Another Location of which this Location is physically a part of.
    characteristic: Optional[List[CodeableConcept]] = field(default_factory=list)  # Collection of characteristics (attributes).
    hoursOfOperation: Optional[List[Any]] = field(default_factory=list)  # What days/times during a week is this location usually open, and any exceptions where the locatio...
    virtualService: Optional[List[Any]] = field(default_factory=list)  # Connection details of a virtual service (e.g. shared conference call facility with dedicated numb...
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # Technical endpoints providing access to services operated for the location.