# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Device resource.

Device represents a type of manufactured item that is used in the provision of healthcare without being substantially changed through that activity.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, ContactPoint, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class DeviceUdiCarrier:
    """
    FHIR Device.udiCarrier complex type.
    
    Unique Device Identifier (UDI) Barcode string.
    """
    
    deviceIdentifier: Optional[str] = None  # Mandatory fixed portion of UDI
    issuer: Optional[str] = None  # UDI Issuing Organization
    jurisdiction: Optional[str] = None  # Regional UDI authority
    carrierAIDC: Optional[str] = None  # UDI Machine Readable Barcode String
    carrierHRF: Optional[str] = None  # UDI Human Readable Barcode String
    entryType: Optional[str] = None  # barcode | rfid | manual | card | unknown | electronic-transmitted | data-matrix | qr-code
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDeviceName:
    """
    FHIR Device.deviceName complex type.
    
    The name or names of the device manufacturer.
    """
    
    name: str  # The name of the device (required)
    type: str  # udi-label-name | user-friendly-name | patient-reported-name | manufacturer-name | model-name | other (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceSpecialization:
    """
    FHIR Device.specialization complex type.
    
    The capabilities supported on a device, the standards to which the device conforms for a particular purpose, and used for the communication.
    """
    
    systemType: CodeableConcept  # The standard that is used to operate and communicate (required)
    version: Optional[str] = None  # The version of the standard that is used to operate and communicate
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceVersion:
    """
    FHIR Device.version complex type.
    
    The actual design of the device or software version running on the device.
    """
    
    type: Optional[CodeableConcept] = None  # The type of the device version
    component: Optional[Identifier] = None  # A single device version
    value: str  # The version of the device or software (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceProperty:
    """
    FHIR Device.property complex type.
    
    The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.
    """
    
    type: CodeableConcept  # Code that specifies the property being represented (required)
    valueQuantity: List[Quantity] = field(default_factory=list)  # Property value as a quantity
    valueCode: List[CodeableConcept] = field(default_factory=list)  # Property value as a code
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Device(DomainResource):
    """
    FHIR R4 Device resource.
    
    Represents a type of manufactured item that is used in the provision of healthcare without being substantially changed through that activity.
    Extends DomainResource.
    """
    
    resourceType: str = "Device"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Instance identifier
    # Definition
    definition: Optional[Reference] = None  # The reference to the definition for the device
    # UDI Carrier
    udiCarrier: List[DeviceUdiCarrier] = field(default_factory=list)  # Unique Device Identifier (UDI) Barcode string
    # Status
    status: Optional[str] = None  # active | inactive | entered-in-error | unknown
    # Status Reason
    statusReason: List[CodeableConcept] = field(default_factory=list)  # online | paused | standby | offline | not-ready | transduc-discon | hw-discon
    # Distinct Identifier
    distinctIdentifier: Optional[str] = None  # The distinct identification string
    # Manufacturer
    manufacturer: Optional[str] = None  # Name of device manufacturer
    # Manufacture Date
    manufactureDate: Optional[str] = None  # Date when the device was made
    # Expiration Date
    expirationDate: Optional[str] = None  # Date and time of expiry of this device
    # Lot Number
    lotNumber: Optional[str] = None  # Lot number of manufacture
    # Serial Number
    serialNumber: Optional[str] = None  # Serial number assigned by the manufacturer
    # Device Name
    deviceName: List[DeviceDeviceName] = field(default_factory=list)  # The name or names of the device manufacturer
    # Model Number
    modelNumber: Optional[str] = None  # The model number for the device
    # Part Number
    partNumber: Optional[str] = None  # The part number of the device
    # Type
    type: Optional[CodeableConcept] = None  # What kind of device this is
    # Specialization
    specialization: List[DeviceSpecialization] = field(default_factory=list)  # The capabilities supported on a device
    # Version
    version: List[DeviceVersion] = field(default_factory=list)  # The actual design of the device or software version running on the device
    # Property
    property: List[DeviceProperty] = field(default_factory=list)  # The actual configuration settings of a device
    # Patient
    patient: Optional[Reference] = None  # Patient to whom Device is affixed
    # Owner
    owner: Optional[Reference] = None  # Organization responsible for device
    # Contact
    contact: List[ContactPoint] = field(default_factory=list)  # Contact details for the device
    # Location
    location: Optional[Reference] = None  # Where the device is found
    # URL
    url: Optional[str] = None  # Network address to contact device
    # Note
    note: List[Annotation] = field(default_factory=list)  # Device notes and comments
    # Safety
    safety: List[CodeableConcept] = field(default_factory=list)  # Safety Characteristics of Device
    # Parent
    parent: Optional[Reference] = None  # The parent device

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


