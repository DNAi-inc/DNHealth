# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 InventoryItem resource.

functional description of an inventory item used in inventory and supply-related workflows.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Address, Annotation, BackboneElement, CodeableConcept, Coding, Duration, Extension, Identifier, Quantity, Range, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class InventoryItemName:
    """
    InventoryItemName nested class.
    """

    nameType: Optional[Coding] = None  # The type of name e.g. 'brand-name', 'functional-name', 'common-name'.
    language: Optional[str] = None  # The language that the item name is expressed in.
    name: Optional[str] = None  # The name or designation that the item is given.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class InventoryItemResponsibleOrganization:
    """
    InventoryItemResponsibleOrganization nested class.
    """

    role: Optional[CodeableConcept] = None  # The role of the organization e.g. manufacturer, distributor, etc.
    organization: Optional[Reference] = None  # An organization that has an association with the item, e.g. manufacturer, distributor, responsibl...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class InventoryItemDescription:
    """
    InventoryItemDescription nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    language: Optional[str] = None  # The language for the item description, when an item must be described in different languages and ...
    description: Optional[str] = None  # Textual description of the item.

@dataclass
class InventoryItemAssociation:
    """
    InventoryItemAssociation nested class.
    """

    associationType: Optional[CodeableConcept] = None  # This attribute defined the type of association when establishing associations or relations betwee...
    relatedItem: Optional[Reference] = None  # The related item or product.
    quantity: Optional[Ratio] = None  # The quantity of the related product in this product - Numerator is the quantity of the related pr...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class InventoryItemCharacteristic:
    """
    InventoryItemCharacteristic nested class.
    """

    characteristicType: Optional[CodeableConcept] = None  # The type of characteristic that is being defined.
    value: Optional[Any] = None  # The value of the attribute.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class InventoryItemInstance:
    """
    InventoryItemInstance nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The identifier for the physical instance, typically a serial number.
    lotNumber: Optional[str] = None  # The lot or batch number of the item.
    expiry: Optional[str] = None  # The expiry date or date and time for the product.
    subject: Optional[Reference] = None  # The subject that the item is associated with.
    location: Optional[Reference] = None  # The location that the item is associated with.


@dataclass
class InventoryItem(FHIRResource):
    """
    functional description of an inventory item used in inventory and supply-related workflows.
    """

    status: Optional[str] = None  # Status of the item entry.
    resourceType: str = "InventoryItem"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for the inventory item.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Category or class of the item.
    code: Optional[List[CodeableConcept]] = field(default_factory=list)  # Code designating the specific type of item.
    name: Optional[List[BackboneElement]] = field(default_factory=list)  # The item name(s) - the brand name, or common name, functional name, generic name.
    responsibleOrganization: Optional[List[BackboneElement]] = field(default_factory=list)  # Organization(s) responsible for the product.
    description: Optional[BackboneElement] = None  # The descriptive characteristics of the inventory item.
    inventoryStatus: Optional[List[CodeableConcept]] = field(default_factory=list)  # The usage status e.g. recalled, in use, discarded... This can be used to indicate that the items ...
    baseUnit: Optional[CodeableConcept] = None  # The base unit of measure - the unit in which the product is used or counted.
    netContent: Optional[Quantity] = None  # Net content or amount present in the item.
    association: Optional[List[BackboneElement]] = field(default_factory=list)  # Association with other items or products.
    characteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # The descriptive or identifying characteristics of the item.
    instance: Optional[BackboneElement] = None  # Instances or occurrences of the product.
    productReference: Optional[Reference] = None  # Link to a product resource used in clinical workflows.