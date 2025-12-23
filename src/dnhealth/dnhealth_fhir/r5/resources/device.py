# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Device resource.

This resource describes the properties (regulated, has real time clock, etc.), adminstrative (manufacturer name, model number, serial number, firmware, etc.), and type (knee replacement, blood pressure cuff, MRI, etc.) of a physical unit (these values do not change much within a given module, for example the serail number, manufacturer name, and model number). An actual unit may consist of several modules in a distinct hierarchy and these are represented by multiple Device resources and bound through the 'parent' element.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, ContactPoint, Count, Duration, Extension, Identifier, Quantity, Range, Reference
from typing import Any, List, Optional

@dataclass
class DeviceUdiCarrier:
    """
    DeviceUdiCarrier nested class.
    """

    deviceIdentifier: Optional[str] = None  # The device identifier (DI) is a mandatory, fixed portion of a UDI that identifies the labeler and...
    issuer: Optional[str] = None  # Organization that is charged with issuing UDIs for devices. For example, the US FDA issuers inclu...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    jurisdiction: Optional[str] = None  # The identity of the authoritative source for UDI generation within a jurisdiction. All UDIs are g...
    carrierAIDC: Optional[str] = None  # The full UDI carrier of the Automatic Identification and Data Capture (AIDC) technology represent...
    carrierHRF: Optional[str] = None  # The full UDI carrier as the human readable form (HRF) representation of the barcode string as pri...
    entryType: Optional[str] = None  # A coded entry to indicate how the data was entered.

@dataclass
class DeviceName:
    """
    DeviceName nested class.
    """

    value: Optional[str] = None  # The actual name that identifies the device.
    type: Optional[str] = None  # Indicates the kind of name. RegisteredName | UserFriendlyName | PatientReportedName.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    display: Optional[bool] = None  # Indicates the default or preferred name to be displayed.

@dataclass
class DeviceVersion:
    """
    DeviceVersion nested class.
    """

    value: Optional[str] = None  # The version text.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The type of the device version, e.g. manufacturer, approved, internal.
    component: Optional[Identifier] = None  # The hardware or software module of the device to which the version applies.
    installDate: Optional[str] = None  # The date the version was installed on the device.

@dataclass
class DeviceConformsTo:
    """
    DeviceConformsTo nested class.
    """

    specification: Optional[CodeableConcept] = None  # Code that identifies the specific standard, specification, protocol, formal guidance, regulation,...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # Describes the type of the standard, specification, or formal guidance.
    version: Optional[str] = None  # Identifies the specific form or variant of the standard, specification, or formal guidance. This ...

@dataclass
class DeviceProperty:
    """
    DeviceProperty nested class.
    """

    type: Optional[CodeableConcept] = None  # Code that specifies the property, such as resolution, color, size, being represented.
    value: Optional[Any] = None  # The value of the property specified by the associated property.type code.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Device(FHIRResource):
    """
    This resource describes the properties (regulated, has real time clock, etc.), adminstrative (manufacturer name, model number, serial number, firmware, etc.), and type (knee replacement, blood pressure cuff, MRI, etc.) of a physical unit (these values do not change much within a given module, for example the serail number, manufacturer name, and model number). An actual unit may consist of several modules in a distinct hierarchy and these are represented by multiple Device resources and bound through the 'parent' element.
    """

    resourceType: str = "Device"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique instance identifiers assigned to a device by manufacturers other organizations or owners.
    displayName: Optional[str] = None  # The name used to display by default when the device is referenced. Based on intent of use by the ...
    definition: Optional[Any] = None  # The reference to the definition for the device.
    udiCarrier: Optional[List[BackboneElement]] = field(default_factory=list)  # Unique device identifier (UDI) assigned to device label or package.  Note that the Device may inc...
    status: Optional[str] = None  # The Device record status. This is not the status of the device like availability.
    availabilityStatus: Optional[CodeableConcept] = None  # The availability of the device.
    biologicalSourceEvent: Optional[Identifier] = None  # An identifier that supports traceability to the event during which material in this product from ...
    manufacturer: Optional[str] = None  # A name of the manufacturer or entity legally responsible for the device.
    manufactureDate: Optional[str] = None  # The date and time when the device was manufactured.
    expirationDate: Optional[str] = None  # The date and time beyond which this device is no longer valid or should not be used (if applicable).
    lotNumber: Optional[str] = None  # Lot number assigned by the manufacturer.
    serialNumber: Optional[str] = None  # The serial number assigned by the organization when the device was manufactured.
    name: Optional[List[BackboneElement]] = field(default_factory=list)  # This represents the manufacturer's name of the device as provided by the device, from a UDI label...
    modelNumber: Optional[str] = None  # The manufacturer's model number for the device.
    partNumber: Optional[str] = None  # The part number or catalog number of the device.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Devices may be associated with one or more categories.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The kind or type of device. A device instance may have more than one type - in which case those a...
    version: Optional[List[BackboneElement]] = field(default_factory=list)  # The actual design of the device or software version running on the device.
    conformsTo: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies the standards, specifications, or formal guidances for the capabilities supported by t...
    property: Optional[List[BackboneElement]] = field(default_factory=list)  # Static or essentially fixed characteristics or features of the device (e.g., time or timing attri...
    mode: Optional[CodeableConcept] = None  # The designated condition for performing a task with the device.
    cycle: Optional[Count] = None  # The series of occurrences that repeats during the operation of the device.
    duration: Optional[Duration] = None  # A measurement of time during the device's operation (e.g., days, hours, mins, etc.).
    owner: Optional[Reference] = None  # An organization that is responsible for the provision and ongoing maintenance of the device.
    contact: Optional[List[ContactPoint]] = field(default_factory=list)  # Contact details for an organization or a particular human that is responsible for the device.
    location: Optional[Reference] = None  # The place where the device can be found.
    url: Optional[str] = None  # A network address on which the device may be contacted directly.
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # Technical endpoints providing access to services provided by the device defined at this resource.
    gateway: Optional[List[Any]] = field(default_factory=list)  # The linked device acting as a communication controller, data collector, translator, or concentrat...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Descriptive information, usage information or implantation information that is not captured in an...
    safety: Optional[List[CodeableConcept]] = field(default_factory=list)  # Provides additional safety characteristics about a medical device.  For example devices containin...
    parent: Optional[Reference] = None  # The higher level or encompassing device that this device is a logical part of.