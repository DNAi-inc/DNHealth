# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DeviceDispense resource.

Indicates that a device is to be or has been dispensed for a named person/patient.  This includes a description of the product (supply) provided and the instructions for using the device.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class DeviceDispensePerformer:
    """
    DeviceDispensePerformer nested class.
    """

    actor: Optional[Reference] = None  # The device, practitioner, etc. who performed the action.  It should be assumed that the actor is ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of performer in the dispense.  For example, date enterer, packager, final ...


@dataclass
class DeviceDispense(FHIRResource):
    """
    Indicates that a device is to be or has been dispensed for a named person/patient.  This includes a description of the product (supply) provided and the instructions for using the device.
    """

    status: Optional[str] = None  # A code specifying the state of the set of dispense events.
    device: Optional[Any] = None  # Identifies the device being dispensed. This is either a link to a resource representing the detai...
    subject: Optional[Reference] = None  # A link to a resource representing the person to whom the device is intended.
    resourceType: str = "DeviceDispense"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for this dispensation.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # The order or request that this dispense is fulfilling.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # The bigger event that this dispense is a part of.
    statusReason: Optional[Any] = None  # Indicates the reason why a dispense was or was not performed.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Indicates the type of device dispense.
    receiver: Optional[Reference] = None  # Identifies the person who picked up the device or the person or location where the device was del...
    encounter: Optional[Reference] = None  # The encounter that establishes the context for this event.
    supportingInformation: Optional[List[Reference]] = field(default_factory=list)  # Additional information that supports the device being dispensed.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what performed the event.
    location: Optional[Reference] = None  # The principal physical location where the dispense was performed.
    type: Optional[CodeableConcept] = None  # Indicates the type of dispensing event that is performed.
    quantity: Optional[Quantity] = None  # The number of devices that have been dispensed.
    preparedDate: Optional[str] = None  # The time when the dispensed product was packaged and reviewed.
    whenHandedOver: Optional[str] = None  # The time the dispensed product was made available to the patient or their representative.
    destination: Optional[Reference] = None  # Identification of the facility/location where the device was /should be shipped to, as part of th...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Extra information about the dispense that could not be conveyed in the other attributes.
    usageInstruction: Optional[str] = None  # The full representation of the instructions.
    eventHistory: Optional[List[Reference]] = field(default_factory=list)  # A summary of the events of interest that have occurred, such as when the dispense was verified.