# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DeviceDefinition resource.

This is a specialized resource that defines the characteristics and capabilities of a device.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Coding, ContactPoint, Extension, Identifier, Period, Quantity, Range, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class DeviceDefinitionUdiDeviceIdentifier:
    """
    DeviceDefinitionUdiDeviceIdentifier nested class.
    """

    deviceIdentifier: Optional[str] = None  # The identifier that is to be associated with every Device that references this DeviceDefintiion f...
    issuer: Optional[str] = None  # The organization that assigns the identifier algorithm.
    jurisdiction: Optional[str] = None  # The jurisdiction to which the deviceIdentifier applies.
    marketPeriod: Optional[Period] = None  # Begin and end dates for the commercial distribution of the device.
    subJurisdiction: Optional[str] = None  # National state or territory to which the marketDistribution recers, typically where the device is...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    marketDistribution: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates where and when the device is available on the market.

@dataclass
class DeviceDefinitionUdiDeviceIdentifierMarketDistribution:
    """
    DeviceDefinitionUdiDeviceIdentifierMarketDistribution nested class.
    """

    marketPeriod: Optional[Period] = None  # Begin and end dates for the commercial distribution of the device.
    subJurisdiction: Optional[str] = None  # National state or territory to which the marketDistribution recers, typically where the device is...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DeviceDefinitionRegulatoryIdentifier:
    """
    DeviceDefinitionRegulatoryIdentifier nested class.
    """

    type: Optional[str] = None  # The type of identifier itself.
    deviceIdentifier: Optional[str] = None  # The identifier itself.
    issuer: Optional[str] = None  # The organization that issued this identifier.
    jurisdiction: Optional[str] = None  # The jurisdiction to which the deviceIdentifier applies.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DeviceDefinitionDeviceName:
    """
    DeviceDefinitionDeviceName nested class.
    """

    name: Optional[str] = None  # A human-friendly name that is used to refer to the device - depending on the type, it can be the ...
    type: Optional[str] = None  # The type of deviceName. RegisteredName | UserFriendlyName | PatientReportedName.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DeviceDefinitionClassification:
    """
    DeviceDefinitionClassification nested class.
    """

    type: Optional[CodeableConcept] = None  # A classification or risk class of the device model.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    justification: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Further information qualifying this classification of the device model.

@dataclass
class DeviceDefinitionConformsTo:
    """
    DeviceDefinitionConformsTo nested class.
    """

    specification: Optional[CodeableConcept] = None  # Code that identifies the specific standard, specification, protocol, formal guidance, regulation,...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # Describes the type of the standard, specification, or formal guidance.
    version: Optional[List[str]] = field(default_factory=list)  # Identifies the specific form or variant of the standard, specification, or formal guidance. This ...
    source: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Standard, regulation, certification, or guidance website, document, or other publication, or simi...

@dataclass
class DeviceDefinitionHasPart:
    """
    DeviceDefinitionHasPart nested class.
    """

    reference: Optional[Reference] = None  # Reference to the device that is part of the current device.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    count: Optional[int] = None  # Number of instances of the component device in the current device.

@dataclass
class DeviceDefinitionPackaging:
    """
    DeviceDefinitionPackaging nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[Identifier] = None  # The business identifier of the packaged medication.
    type: Optional[CodeableConcept] = None  # A code that defines the specific type of packaging.
    count: Optional[int] = None  # The number of items contained in the package (devices or sub-packages).
    distributor: Optional[List[BackboneElement]] = field(default_factory=list)  # An organization that distributes the packaged device.
    name: Optional[str] = None  # Distributor's human-readable name.
    organizationReference: Optional[List[Reference]] = field(default_factory=list)  # Distributor as an Organization resource.
    udiDeviceIdentifier: Optional[List[Any]] = field(default_factory=list)  # Unique Device Identifier (UDI) Barcode string on the packaging.
    packaging: Optional[List[Any]] = field(default_factory=list)  # Allows packages within packages.

@dataclass
class DeviceDefinitionPackagingDistributor:
    """
    DeviceDefinitionPackagingDistributor nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Distributor's human-readable name.
    organizationReference: Optional[List[Reference]] = field(default_factory=list)  # Distributor as an Organization resource.

@dataclass
class DeviceDefinitionVersion:
    """
    DeviceDefinitionVersion nested class.
    """

    value: Optional[str] = None  # The version text.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The type of the device version, e.g. manufacturer, approved, internal.
    component: Optional[Identifier] = None  # The hardware or software module of the device to which the version applies.

@dataclass
class DeviceDefinitionProperty:
    """
    DeviceDefinitionProperty nested class.
    """

    type: Optional[CodeableConcept] = None  # Code that specifies the property such as a resolution or color being represented.
    value: Optional[Any] = None  # The value of the property specified by the associated property.type code.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DeviceDefinitionLink:
    """
    DeviceDefinitionLink nested class.
    """

    relation: Optional[Coding] = None  # The type indicates the relationship of the related device to the device instance.
    relatedDevice: Optional[Any] = None  # A reference to the linked device.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DeviceDefinitionMaterial:
    """
    DeviceDefinitionMaterial nested class.
    """

    substance: Optional[CodeableConcept] = None  # A substance that the device contains, may contain, or is made of - for example latex - to be used...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    alternate: Optional[bool] = None  # Indicates an alternative material of the device.
    allergenicIndicator: Optional[bool] = None  # Whether the substance is a known or suspected allergen.

@dataclass
class DeviceDefinitionGuideline:
    """
    DeviceDefinitionGuideline nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The circumstances that form the setting for using the device.
    usageInstruction: Optional[str] = None  # Detailed written and visual directions for the user on how to use the device.
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # A source of information or reference for this guideline.
    indication: Optional[List[CodeableConcept]] = field(default_factory=list)  # A clinical condition for which the device was designed to be used.
    contraindication: Optional[List[CodeableConcept]] = field(default_factory=list)  # A specific situation when a device should not be used because it may cause harm.
    warning: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specific hazard alert information that a user needs to know before using the device.
    intendedUse: Optional[str] = None  # A description of the general purpose or medical use of the device or its function.

@dataclass
class DeviceDefinitionCorrectiveAction:
    """
    DeviceDefinitionCorrectiveAction nested class.
    """

    recall: Optional[bool] = None  # Whether the last corrective action known for this device was a recall.
    period: Optional[Period] = None  # Start and end dates of the  corrective action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    scope: Optional[str] = None  # The scope of the corrective action - whether the action targeted all units of a given device mode...

@dataclass
class DeviceDefinitionChargeItem:
    """
    DeviceDefinitionChargeItem nested class.
    """

    chargeItemCode: Optional[Any] = None  # The code or reference for the charge item.
    count: Optional[Quantity] = None  # Coefficient applicable to the billing code.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    effectivePeriod: Optional[Period] = None  # A specific time period in which this charge item applies.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The context to which this charge item applies.


@dataclass
class DeviceDefinition(FHIRResource):
    """
    This is a specialized resource that defines the characteristics and capabilities of a device.
    """

    resourceType: str = "DeviceDefinition"
    description: Optional[str] = None  # Additional information to describe the device.
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique instance identifiers assigned to a device by the software, manufacturers, other organizati...
    udiDeviceIdentifier: Optional[List[BackboneElement]] = field(default_factory=list)  # Unique device identifier (UDI) assigned to device label or package.  Note that the Device may inc...
    regulatoryIdentifier: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifier associated with the regulatory documentation (certificates, technical documentation, p...
    partNumber: Optional[str] = None  # The part number or catalog number of the device.
    manufacturer: Optional[Reference] = None  # A name of the manufacturer  or legal representative e.g. labeler. Whether this is the actual manu...
    deviceName: Optional[List[BackboneElement]] = field(default_factory=list)  # The name or names of the device as given by the manufacturer.
    modelNumber: Optional[str] = None  # The model number for the device for example as defined by the manufacturer or labeler, or other a...
    classification: Optional[List[BackboneElement]] = field(default_factory=list)  # What kind of device or device system this is.
    conformsTo: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies the standards, specifications, or formal guidances for the capabilities supported by t...
    hasPart: Optional[List[BackboneElement]] = field(default_factory=list)  # A device that is part (for example a component) of the present device.
    packaging: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about the packaging of the device, i.e. how the device is packaged.
    version: Optional[List[BackboneElement]] = field(default_factory=list)  # The version of the device or software.
    safety: Optional[List[CodeableConcept]] = field(default_factory=list)  # Safety characteristics of the device.
    shelfLifeStorage: Optional[List[Any]] = field(default_factory=list)  # Shelf Life and storage information.
    languageCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Language code for the human-readable text strings produced by the device (all supported).
    property: Optional[List[BackboneElement]] = field(default_factory=list)  # Static or essentially fixed characteristics or features of this kind of device that are otherwise...
    owner: Optional[Reference] = None  # An organization that is responsible for the provision and ongoing maintenance of the device.
    contact: Optional[List[ContactPoint]] = field(default_factory=list)  # Contact details for an organization or a particular human that is responsible for the device.
    link: Optional[List[BackboneElement]] = field(default_factory=list)  # An associated device, attached to, used with, communicating with or linking a previous or new dev...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Descriptive information, usage information or implantation information that is not captured in an...
    material: Optional[List[BackboneElement]] = field(default_factory=list)  # A substance used to create the material(s) of which the device is made.
    productionIdentifierInUDI: Optional[List[str]] = field(default_factory=list)  # Indicates the production identifier(s) that are expected to appear in the UDI carrier on the devi...
    guideline: Optional[BackboneElement] = None  # Information aimed at providing directions for the usage of this model of device.
    correctiveAction: Optional[BackboneElement] = None  # Tracking of latest field safety corrective action.
    chargeItem: Optional[List[BackboneElement]] = field(default_factory=list)  # Billing code or reference associated with the device.