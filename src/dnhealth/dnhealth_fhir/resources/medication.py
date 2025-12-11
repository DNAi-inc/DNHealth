# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Medication resource.

Complete Medication resource with all R4 elements.
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
)


@dataclass
class MedicationIngredient:
    """
    Active or inactive ingredient.
    
    Identifies a particular constituent of interest in the product.
    """

    itemCodeableConcept: Optional[CodeableConcept] = None
    itemReference: Optional[Reference] = None
    isActive: Optional[bool] = None
    strength: Optional[Ratio] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationBatch:
    """
    Details about packaged medications.
    
    Information that only applies to packages (not products).
    """

    lotNumber: Optional[str] = None
    expirationDate: Optional[str] = None  # YYYY-MM-DD
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Medication(FHIRResource):
    """
    FHIR R4 Medication resource.

    Represents a medication or substance that may be administered to a patient.
    """

    resourceType: str = "Medication"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Code
    code: Optional[CodeableConcept] = None
    # Status
    status: Optional[str] = None  # active | inactive | entered-in-error
    # Manufacturer
    manufacturer: Optional[Reference] = None
    # Form
    form: Optional[CodeableConcept] = None
    # Amount
    amount: Optional[Ratio] = None
    # Ingredient
    ingredient: List[MedicationIngredient] = field(default_factory=list)
    # Batch
    batch: Optional[MedicationBatch] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
