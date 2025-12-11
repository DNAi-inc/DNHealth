# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductIngredient resource.

Complete MedicinalProductIngredient resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Ratio,
    Quantity,
)


@dataclass
class MedicinalProductIngredientSpecifiedSubstance:
    """
    A specified substance that comprises this ingredient.
    """

    code: CodeableConcept  # The specified substance (required)
    group: CodeableConcept  # The group of specified substance (required)
    confidentiality: Optional[CodeableConcept] = None
    strength: List["MedicinalProductIngredientSpecifiedSubstanceStrength"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductIngredientSpecifiedSubstanceStrength:
    """
    Quantity of the substance or specified substance present in the ingredient.
    """

    presentation: Ratio  # The quantity of substance in the unit of presentation (required)
    presentationLowLimit: Optional[Ratio] = None
    concentration: Optional[Ratio] = None
    concentrationLowLimit: Optional[Ratio] = None
    measurementPoint: Optional[str] = None
    country: List[CodeableConcept] = field(default_factory=list)
    referenceStrength: List["MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength:
    """
    Strength expressed in terms of a reference substance.
    """

    substance: Optional[CodeableConcept] = None
    strength: Ratio  # Strength of the reference substance (required)
    strengthLowLimit: Optional[Ratio] = None
    measurementPoint: Optional[str] = None
    country: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductIngredientSubstance:
    """
    The ingredient substance.
    """

    code: CodeableConcept  # The ingredient substance (required)
    strength: List[MedicinalProductIngredientSpecifiedSubstanceStrength] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductIngredient(FHIRResource):
    """
    FHIR R4 MedicinalProductIngredient resource.

    An ingredient of a manufactured item or pharmaceutical product.
    """

    resourceType: str = "MedicinalProductIngredient"
    # Identifiers
    identifier: Optional[Identifier] = None
    # Role
    role: CodeableConcept  # Ingredient role (required)
    # Allergenic Indicator
    allergenicIndicator: Optional[bool] = None
    # Manufacturer
    manufacturer: List[Reference] = field(default_factory=list)
    # Specified Substance
    specifiedSubstance: List[MedicinalProductIngredientSpecifiedSubstance] = field(default_factory=list)
    # Substance
    substance: Optional[MedicinalProductIngredientSubstance] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
