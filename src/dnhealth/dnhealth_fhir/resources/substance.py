# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Substance resource.

Complete Substance resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Quantity,
    Ratio,
)


@dataclass
class SubstanceInstance:
    """
    Substance may be used to describe a kind of substance, or a specific package/container of the substance.
    """

    identifier: Optional[Identifier] = None
    expiry: Optional[str] = None  # ISO 8601 dateTime
    quantity: Optional[Quantity] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceIngredient:
    """
    A substance can be composed of other substances.
    """

    quantity: Optional[Ratio] = None
    substanceCodeableConcept: Optional[CodeableConcept] = None
    substanceReference: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Substance(FHIRResource):
    """
    FHIR R4 Substance resource.

    A homogeneous material with a definite composition.
    """

    resourceType: str = "Substance"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Status
    status: Optional[str] = None  # active | inactive | entered-in-error
    # Category
    category: List[CodeableConcept] = field(default_factory=list)
    # Code
    # Note: code is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce code is provided.
    code: Optional[CodeableConcept] = None  # What substance this is (required)
    # Description
    description: Optional[str] = None
    # Instance
    instance: List[SubstanceInstance] = field(default_factory=list)
    # Ingredient
    ingredient: List[SubstanceIngredient] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
