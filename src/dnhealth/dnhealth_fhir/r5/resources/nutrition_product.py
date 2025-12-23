# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 NutritionProduct resource.

A food or supplement that is consumed by patients.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class NutritionProductNutrient:
    """
    NutritionProductNutrient nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    item: Optional[Any] = None  # The (relevant) nutrients in the product.
    amount: Optional[List[Ratio]] = field(default_factory=list)  # The amount of nutrient expressed in one or more units: X per pack / per serving / per dose.

@dataclass
class NutritionProductIngredient:
    """
    NutritionProductIngredient nested class.
    """

    item: Optional[Any] = None  # The ingredient contained in the product.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    amount: Optional[List[Ratio]] = field(default_factory=list)  # The amount of ingredient that is in the product.

@dataclass
class NutritionProductCharacteristic:
    """
    NutritionProductCharacteristic nested class.
    """

    type: Optional[CodeableConcept] = None  # A code specifying which characteristic of the product is being described (for example, colour, sh...
    value: Optional[Any] = None  # The actual characteristic value corresponding to the type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class NutritionProductInstance:
    """
    NutritionProductInstance nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    quantity: Optional[Quantity] = None  # The amount of items or instances that the resource considers, for instance when referring to 2 id...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The identifier for the physical instance, typically a serial number or manufacturer number.
    name: Optional[str] = None  # The name for the specific product.
    lotNumber: Optional[str] = None  # The identification of the batch or lot of the product.
    expiry: Optional[str] = None  # The time after which the product is no longer expected to be in proper condition, or its use is n...
    useBy: Optional[str] = None  # The time after which the product is no longer expected to be in proper condition, or its use is n...
    biologicalSourceEvent: Optional[Identifier] = None  # An identifier that supports traceability to the event during which material in this product from ...


@dataclass
class NutritionProduct(FHIRResource):
    """
    A food or supplement that is consumed by patients.
    """

    status: Optional[str] = None  # The current state of the product.
    resourceType: str = "NutritionProduct"
    code: Optional[CodeableConcept] = None  # The code assigned to the product, for example a USDA NDB number, a USDA FDC ID number, or a Langu...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Nutrition products can have different classifications - according to its nutritional properties, ...
    manufacturer: Optional[List[Reference]] = field(default_factory=list)  # The organisation (manufacturer, representative or legal authorization holder) that is responsible...
    nutrient: Optional[List[BackboneElement]] = field(default_factory=list)  # The product's nutritional information expressed by the nutrients.
    ingredient: Optional[List[BackboneElement]] = field(default_factory=list)  # Ingredients contained in this product.
    knownAllergen: Optional[List[Any]] = field(default_factory=list)  # Allergens that are known or suspected to be a part of this nutrition product.
    characteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # Specifies descriptive properties of the nutrition product.
    instance: Optional[List[BackboneElement]] = field(default_factory=list)  # Conveys instance-level information about this product item. One or several physical, countable in...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the product.