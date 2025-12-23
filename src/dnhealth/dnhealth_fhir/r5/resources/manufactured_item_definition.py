# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ManufacturedItemDefinition resource.

The definition and characteristics of a medicinal manufactured item, such as a tablet or capsule, as contained in a packaged medicinal product.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class ManufacturedItemDefinitionProperty:
    """
    ManufacturedItemDefinitionProperty nested class.
    """

    type: Optional[CodeableConcept] = None  # A code expressing the type of characteristic.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # A value for the characteristic.

@dataclass
class ManufacturedItemDefinitionComponent:
    """
    ManufacturedItemDefinitionComponent nested class.
    """

    type: Optional[CodeableConcept] = None  # Defining type of the component e.g. shell, layer, ink.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[List[CodeableConcept]] = field(default_factory=list)  # The function of this component within the item e.g. delivers active ingredient, masks taste.
    amount: Optional[List[Quantity]] = field(default_factory=list)  # The measurable amount of total quantity of all substances in the component, expressable in differ...
    constituent: Optional[List[BackboneElement]] = field(default_factory=list)  # A reference to a constituent of the manufactured item as a whole, linked here so that its compone...
    location: Optional[List[CodeableConcept]] = field(default_factory=list)  # The physical location of the constituent/ingredient within the component. Example – if the compon...
    hasIngredient: Optional[List[Any]] = field(default_factory=list)  # The ingredient that is the constituent of the given component.
    property: Optional[List[Any]] = field(default_factory=list)  # General characteristics of this component.
    component: Optional[List[Any]] = field(default_factory=list)  # A component that this component contains or is made from.

@dataclass
class ManufacturedItemDefinitionComponentConstituent:
    """
    ManufacturedItemDefinitionComponentConstituent nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    amount: Optional[List[Quantity]] = field(default_factory=list)  # The measurable amount of the substance, expressable in different ways (e.g. by mass or volume).
    location: Optional[List[CodeableConcept]] = field(default_factory=list)  # The physical location of the constituent/ingredient within the component. Example – if the compon...
    function: Optional[List[CodeableConcept]] = field(default_factory=list)  # The function of this constituent within the component e.g. binder.
    hasIngredient: Optional[List[Any]] = field(default_factory=list)  # The ingredient that is the constituent of the given component.


@dataclass
class ManufacturedItemDefinition(FHIRResource):
    """
    The definition and characteristics of a medicinal manufactured item, such as a tablet or capsule, as contained in a packaged medicinal product.
    """

    status: Optional[str] = None  # The status of this item. Enables tracking the life-cycle of the content.
    manufacturedDoseForm: Optional[CodeableConcept] = None  # Dose form as manufactured and before any transformation into the pharmaceutical product.
    resourceType: str = "ManufacturedItemDefinition"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique identifier.
    name: Optional[str] = None  # A descriptive name applied to this item.
    unitOfPresentation: Optional[CodeableConcept] = None  # The “real-world” units in which the quantity of the manufactured item is described.
    manufacturer: Optional[List[Reference]] = field(default_factory=list)  # Manufacturer of the item, one of several possible.
    marketingStatus: Optional[List[Any]] = field(default_factory=list)  # Allows specifying that an item is on the market for sale, or that it is not available, and the da...
    ingredient: Optional[List[CodeableConcept]] = field(default_factory=list)  # The ingredients of this manufactured item. This is only needed if the ingredients are not specifi...
    property: Optional[List[BackboneElement]] = field(default_factory=list)  # General characteristics of this item.
    component: Optional[List[BackboneElement]] = field(default_factory=list)  # Physical parts of the manufactured item, that it is intrisically made from. This is distinct from...