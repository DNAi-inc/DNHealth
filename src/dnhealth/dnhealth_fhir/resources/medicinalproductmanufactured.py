# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductManufactured resource.

Complete MedicinalProductManufactured resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Quantity,
    Attachment,
)


@dataclass
class MedicinalProductManufactured(FHIRResource):
    """
    FHIR R4 MedicinalProductManufactured resource.

    The manufactured item as contained in the packaged medicinal product.
    """

    resourceType: str = "MedicinalProductManufactured"
    # Manufactured Dose Form
    manufacturedDoseForm: CodeableConcept  # Dose form of a single manufactured item (required)
    # Unit of Presentation
    unitOfPresentation: Optional[CodeableConcept] = None
    # Quantity
    quantity: Quantity  # The quantity or "count number" of the manufactured item (required)
    # Manufacturer
    manufacturer: List[Reference] = field(default_factory=list)
    # Ingredient
    ingredient: List[Reference] = field(default_factory=list)
    # Physical Characteristics
    physicalCharacteristics: Optional["MedicinalProductManufacturedPhysicalCharacteristics"] = None
    # Other Characteristics
    otherCharacteristics: List[CodeableConcept] = field(default_factory=list)


@dataclass
class MedicinalProductManufacturedPhysicalCharacteristics:
    """
    Dimensions, color etc.
    """

    height: Optional[Quantity] = None
    width: Optional[Quantity] = None
    depth: Optional[Quantity] = None
    weight: Optional[Quantity] = None
    nominalVolume: Optional[Quantity] = None
    externalDiameter: Optional[Quantity] = None
    shape: Optional[str] = None
    color: List[str] = field(default_factory=list)
    imprint: List[str] = field(default_factory=list)
    image: List[Attachment] = field(default_factory=list)
    scoring: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
