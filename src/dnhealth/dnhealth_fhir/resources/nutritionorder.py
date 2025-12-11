# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 NutritionOrder resource.

NutritionOrder represents a request for a diet, oral nutritional supplement, or enteral/formula feeding.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Annotation,
    Timing,
)


logger = logging.getLogger(__name__)


@dataclass
class NutritionOrderOralDiet:
    """
    FHIR NutritionOrder.oralDiet complex type.
    
    Diet instructions for the patient.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: List[CodeableConcept] = field(default_factory=list)  # Type of oral diet
    schedule: List[Timing] = field(default_factory=list)  # Scheduled frequency of diet
    nutrient: List["NutritionOrderOralDietNutrient"] = field(default_factory=list)  # Required nutrient modifications
    texture: List["NutritionOrderOralDietTexture"] = field(default_factory=list)  # Texture modifications
    fluidConsistencyType: List[CodeableConcept] = field(default_factory=list)  # The required consistency of fluids
    instruction: Optional[str] = None  # Instructions or additional information about the oral diet


@dataclass
class NutritionOrderOralDietNutrient:
    """
    FHIR NutritionOrder.oralDiet.nutrient complex type.
    
    Required nutrient modifications.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    modifier: Optional[CodeableConcept] = None  # Type of nutrient that is being modified
    amount: Optional[Any] = None  # Quantity of the specified nutrient (Quantity)


@dataclass
class NutritionOrderOralDietTexture:
    """
    FHIR NutritionOrder.oralDiet.texture complex type.
    
    Texture modifications.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    modifier: Optional[CodeableConcept] = None  # Code to indicate how to alter the texture of the foods
    foodType: Optional[CodeableConcept] = None  # Foods that are modified by this texture modifier


@dataclass
class NutritionOrderSupplement:
    """
    FHIR NutritionOrder.supplement complex type.
    
    Oral nutritional supplement orders.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: Optional[CodeableConcept] = None  # Type of supplement product requested
    productName: Optional[str] = None  # Product or brand name of the nutritional supplement
    schedule: List[Timing] = field(default_factory=list)  # Scheduled frequency of supplement
    quantity: Optional[Any] = None  # Amount of the nutritional supplement (Quantity)
    instruction: Optional[str] = None  # Instructions or additional information about the oral supplement


@dataclass
class NutritionOrderEnteralFormula:
    """
    FHIR NutritionOrder.enteralFormula complex type.
    
    Enteral formula feeding orders.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    baseFormulaType: Optional[CodeableConcept] = None  # Type of enteral or infant formula
    baseFormulaProductName: Optional[str] = None  # Product or brand name of the enteral or infant formula
    additiveType: Optional[CodeableConcept] = None  # Type of modular component to add to the feeding
    additiveProductName: Optional[str] = None  # Product or brand name of the modular additive
    caloricDensity: Optional[Any] = None  # Amount of energy per specified volume (Quantity)
    routeofAdministration: Optional[CodeableConcept] = None  # How the formula should enter the patient's gastrointestinal tract
    administration: List["NutritionOrderEnteralFormulaAdministration"] = field(default_factory=list)  # Formula feeding instructions
    maxVolumeToDeliver: Optional[Any] = None  # Upper limit on formula volume per unit of time (Quantity)
    administrationInstruction: Optional[str] = None  # Formula feeding instructions expressed as text


@dataclass
class NutritionOrderEnteralFormulaAdministration:
    """
    FHIR NutritionOrder.enteralFormula.administration complex type.
    
    Formula feeding instructions.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    schedule: Optional[Timing] = None  # Scheduled frequency of enteral feeding
    quantity: Optional[Any] = None  # The volume of formula to provide (Quantity)
    rateQuantity: Optional[Any] = None  # Speed with which the formula is provided per unit of time (Quantity)
    rateRatio: Optional[Any] = None  # Speed with which the formula is provided per unit of time (Ratio)


@dataclass
class NutritionOrder(DomainResource):
    """
    FHIR R4 NutritionOrder resource.
    
    Represents a request for a diet, oral nutritional supplement, or enteral/formula feeding.
    Extends DomainResource.
    """
    
    resourceType: str = "NutritionOrder"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Identifiers assigned to this order
    # Instantiates Canonical
    instantiatesCanonical: List[str] = field(default_factory=list)  # Instantiates FHIR protocol or definition (canonical references)
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)  # Instantiates external protocol or definition (URIs)
    # Instantiates
    instantiates: List[str] = field(default_factory=list)  # Instantiates protocol or definition
    # Status
    status: str  # draft | active | on-hold | revoked | completed | entered-in-error | unknown (required)
    # Intent
    intent: str  # proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option (required)
    # Patient
    patient: Reference  # The person who requires the diet, formula or nutritional supplement (required)
    # Encounter
    encounter: Optional[Reference] = None  # The encounter associated with this nutrition order
    # DateTime
    dateTime: str  # Date and time the nutrition order was requested (required)
    # Orderer
    orderer: Optional[Reference] = None  # Practitioner that creates or initiates the order
    # Allergy Intolerance
    allergyIntolerance: List[Reference] = field(default_factory=list)  # List of patient food allergies and intolerances
    # Food Preference Modifier
    foodPreferenceModifier: List[CodeableConcept] = field(default_factory=list)  # Order-specific modifier about the type of food
    # Exclude Food Modifier
    excludeFoodModifier: List[CodeableConcept] = field(default_factory=list)  # Order-specific modifier about the type of food
    # Oral Diet
    oralDiet: Optional[NutritionOrderOralDiet] = None  # Oral diet components
    # Supplement
    supplement: List[NutritionOrderSupplement] = field(default_factory=list)  # Supplement components
    # Enteral Formula
    enteralFormula: Optional[NutritionOrderEnteralFormula] = None  # Enteral formula components
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about the nutrition order

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

