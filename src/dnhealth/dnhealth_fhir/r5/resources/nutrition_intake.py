# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 NutritionIntake resource.

A record of food or fluid that is being consumed by a patient.  A NutritionIntake may indicate that the patient may be consuming the food or fluid now or has consumed the food or fluid in the past.  The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician.  A common scenario where this information is captured is during the history taking process during a patient visit or stay or through an app that tracks food or fluids consumed.   The consumption information may come from sources such as the patient's memory, from a nutrition label,  or from a clinician documenting observed intake.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Reference, Timing
from typing import Any, List, Optional

@dataclass
class NutritionIntakeConsumedItem:
    """
    NutritionIntakeConsumedItem nested class.
    """

    type: Optional[CodeableConcept] = None  # Indicates what a category of item that was consumed: e.g., food, fluid, enteral, etc.
    nutritionProduct: Optional[Any] = None  # Identifies the food or fluid product that was consumed. This is potentially a link to a resource ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    schedule: Optional[Timing] = None  # Scheduled frequency of consumption.
    amount: Optional[Quantity] = None  # Quantity of the specified food.
    rate: Optional[Quantity] = None  # Rate at which enteral feeding was administered.
    notConsumed: Optional[bool] = None  # Indicator when a patient is in a setting where it is helpful to know if food was not consumed, su...
    notConsumedReason: Optional[CodeableConcept] = None  # Document the reason the food or fluid was not consumed, such as refused, held, etc.

@dataclass
class NutritionIntakeIngredientLabel:
    """
    NutritionIntakeIngredientLabel nested class.
    """

    nutrient: Optional[Any] = None  # Total nutrient consumed. This could be a macronutrient (protein, fat, carbohydrate), or a vitamin...
    amount: Optional[Quantity] = None  # Total amount of nutrient consumed.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class NutritionIntakePerformer:
    """
    NutritionIntakePerformer nested class.
    """

    actor: Optional[Reference] = None  # Who performed the intake.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Type of performer.


@dataclass
class NutritionIntake(FHIRResource):
    """
    A record of food or fluid that is being consumed by a patient.  A NutritionIntake may indicate that the patient may be consuming the food or fluid now or has consumed the food or fluid in the past.  The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician.  A common scenario where this information is captured is during the history taking process during a patient visit or stay or through an app that tracks food or fluids consumed.   The consumption information may come from sources such as the patient's memory, from a nutrition label,  or from a clinician documenting observed intake.
    """

    status: Optional[str] = None  # A code representing the patient or other source's judgment about the state of the intake that thi...
    subject: Optional[Reference] = None  # The person, animal or group who is/was consuming the food or fluid.
    consumedItem: List[BackboneElement] = field(default_factory=list)  # What food or fluid product or item was consumed.
    resourceType: str = "NutritionIntake"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers associated with this Nutrition Intake that are defined by business processes and/or u...
    instantiatesCanonical: Optional[List[str]] = field(default_factory=list)  # Instantiates FHIR protocol or definition.
    instantiatesUri: Optional[List[str]] = field(default_factory=list)  # Instantiates external protocol or definition.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan, proposal or order that is fulfilled in whole or in part by this event.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular event is a component or step.
    statusReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # Captures the reason for the current state of the NutritionIntake.
    code: Optional[CodeableConcept] = None  # Overall type of nutrition intake.
    encounter: Optional[Reference] = None  # The encounter that establishes the context for this NutritionIntake.
    occurrence: Optional[Any] = None  # The interval of time during which it is being asserted that the patient is/was consuming the food...
    recorded: Optional[str] = None  # The date when the Nutrition Intake was asserted by the information source.
    reported: Optional[Any] = None  # The person or organization that provided the information about the consumption of this food or fl...
    ingredientLabel: Optional[List[BackboneElement]] = field(default_factory=list)  # Total nutrient amounts for the whole meal, product, serving, etc.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Who performed the intake and how they were involved.
    location: Optional[Reference] = None  # Where the intake occurred.
    derivedFrom: Optional[List[Reference]] = field(default_factory=list)  # Allows linking the NutritionIntake to the underlying NutritionOrder, or to other information, suc...
    reason: Optional[List[Any]] = field(default_factory=list)  # A reason, Condition or observation for why the food or fluid is /was consumed.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Provides extra information about the Nutrition Intake that is not conveyed by the other attributes.