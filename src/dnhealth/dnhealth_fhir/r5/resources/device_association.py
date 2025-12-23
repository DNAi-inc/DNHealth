# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DeviceAssociation resource.

A record of association of a device.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import List, Optional

@dataclass
class DeviceAssociationOperation:
    """
    DeviceAssociationOperation nested class.
    """

    status: Optional[CodeableConcept] = None  # Device operational condition corresponding to the association.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    operator: Optional[List[Reference]] = field(default_factory=list)  # The individual performing the action enabled by the device.
    period: Optional[Period] = None  # Begin and end dates and times for the device's operation.


@dataclass
class DeviceAssociation(FHIRResource):
    """
    A record of association of a device.
    """

    device: Optional[Reference] = None  # Reference to the devices associated with the patient or group.
    status: Optional[CodeableConcept] = None  # Indicates the state of the Device association.
    resourceType: str = "DeviceAssociation"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Instance identifier.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Describes the relationship between the device and subject.
    statusReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reasons given for the current association status.
    subject: Optional[Reference] = None  # The individual, group of individuals or device that the device is on or associated with.
    bodyStructure: Optional[Reference] = None  # Current anatomical location of the device in/on subject.
    period: Optional[Period] = None  # Begin and end dates and times for the device association.
    operation: Optional[List[BackboneElement]] = field(default_factory=list)  # The details about the device when it is in use to describe its operation.