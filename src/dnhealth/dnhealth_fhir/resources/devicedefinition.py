# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DeviceDefinition resource.

DeviceDefinition represents the characteristics, operational status and capabilities of a medical-related component of a medical device.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, ContactPoint, Quantity, Money


@dataclass
class DeviceDefinitionUdiDeviceIdentifier:
    """
    FHIR DeviceDefinition.udiDeviceIdentifier complex type.
    
    Unique Device Identifier (UDI) assigned to device label or package.
    """
    
    deviceIdentifier: str  # The identifier that is to be associated with every Device that is produced from this DeviceDefinition (required)
    issuer: str  # The organization that assigns the identifier (required)
    jurisdiction: Optional[str] = None  # The jurisdiction to which the deviceIdentifier applies
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDefinitionDeviceName:
    """
    FHIR DeviceDefinition.deviceName complex type.
    
    A name given to the device to identify it.
    """
    
    name: str  # The name of the device (required)
    type: str  # udi-label-name | user-friendly-name | patient-reported-name | manufacturer-name | model-name | other (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDefinitionSpecialization:
    """
    FHIR DeviceDefinition.specialization complex type.
    
    What kind of device or device system this is.
    """
    
    systemType: CodeableConcept  # The standard that is used to operate and communicate (required)
    version: Optional[str] = None  # The version of the standard that is used to operate and communicate
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDefinitionCapability:
    """
    FHIR DeviceDefinition.capability complex type.
    
    Device capabilities.
    """
    
    type: CodeableConcept  # Type of capability (required)
    description: List[CodeableConcept] = field(default_factory=list)  # Description of capability
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDefinitionProperty:
    """
    FHIR DeviceDefinition.property complex type.
    
    The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.
    """
    
    type: CodeableConcept  # Code that specifies the property being represented (required)
    valueQuantity: List[Quantity] = field(default_factory=list)  # Property value as a quantity
    valueCode: List[CodeableConcept] = field(default_factory=list)  # Property value as a code
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDefinitionMaterial:
    """
    FHIR DeviceDefinition.material complex type.
    
    A substance used to create the material(s) of which the device is made.
    """
    
    substance: CodeableConcept  # The substance (required)
    alternate: Optional[bool] = None  # Indicates an alternative material of the device
    allergenicIndicator: Optional[bool] = None  # Whether the substance is a known or suspected allergen
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceDefinition(DomainResource):
    """
    FHIR R4 DeviceDefinition resource.
    
    Represents the characteristics, operational status and capabilities of a medical-related component of a medical device.
    Extends DomainResource.
    """
    
    resourceType: str = "DeviceDefinition"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Instance identifier
    # UDI Device Identifier
    udiDeviceIdentifier: List[DeviceDefinitionUdiDeviceIdentifier] = field(default_factory=list)  # Unique Device Identifier (UDI) assigned to device label or package
    # Manufacturer String
    manufacturerString: Optional[str] = None  # Name of device manufacturer
    # Manufacturer Reference
    manufacturerReference: Optional[Reference] = None  # Name of device manufacturer
    # Device Name
    deviceName: List[DeviceDefinitionDeviceName] = field(default_factory=list)  # A name given to the device to identify it
    # Model Number
    modelNumber: Optional[str] = None  # The model number for the device
    # Type
    type: Optional[CodeableConcept] = None  # What kind of device this is
    # Specialization
    specialization: List[DeviceDefinitionSpecialization] = field(default_factory=list)  # What kind of device or device system this is
    # Version
    version: List[str] = field(default_factory=list)  # The versions of the device system
    # Safety
    safety: List[CodeableConcept] = field(default_factory=list)  # Safety characteristics of Device
    # Shelf Life Storage
    shelfLifeStorage: List[Any] = field(default_factory=list)  # Shelf Life and storage information
    # Physical Characteristics
    physicalCharacteristics: Optional[Any] = None  # Dimensions, color etc.
    # Language Code
    languageCode: List[CodeableConcept] = field(default_factory=list)  # Language code for the human-readable text strings produced by the device
    # Capability
    capability: List[DeviceDefinitionCapability] = field(default_factory=list)  # Device capabilities
    # Property
    property: List[DeviceDefinitionProperty] = field(default_factory=list)  # The actual configuration settings of a device
    # Owner
    owner: Optional[Reference] = None  # Organization responsible for device
    # Contact
    contact: List[ContactPoint] = field(default_factory=list)  # Contact details for the device
    # URL
    url: Optional[str] = None  # Network address to contact device
    # Online Information
    onlineInformation: Optional[str] = None  # Access to on-line information
    # Note
    note: List[Annotation] = field(default_factory=list)  # Device notes and comments
    # Quantity
    quantity: Optional[Quantity] = None  # The quantity of the device present in the packaging
    # Parent Device
    parentDevice: Optional[Reference] = None  # The parent device it can be part of
    # Material
    material: List[DeviceDefinitionMaterial] = field(default_factory=list)  # A substance used to create the material(s) of which the device is made

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


