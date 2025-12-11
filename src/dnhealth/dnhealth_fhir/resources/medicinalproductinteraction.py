# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductInteraction resource.

Complete MedicinalProductInteraction resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Reference,
    CodeableConcept,
)


@dataclass
class MedicinalProductInteractionInteractant:
    """
    The specific medication, food or laboratory test that interacts.
    """

    itemReference: Optional[Reference] = None
    itemCodeableConcept: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductInteraction(FHIRResource):
    """
    FHIR R4 MedicinalProductInteraction resource.

    The interactions of the medicinal product with other medicinal products,
    or other forms of interactions.
    """

    resourceType: str = "MedicinalProductInteraction"
    # Subject
    subject: List[Reference] = field(default_factory=list)
    # Description
    description: Optional[str] = None
    # Interactant
    interactant: List[MedicinalProductInteractionInteractant] = field(default_factory=list)
    # Type
    type: Optional[CodeableConcept] = None
    # Effect
    effect: Optional[CodeableConcept] = None
    # Incidence
    incidence: Optional[CodeableConcept] = None
    # Management
    management: Optional[CodeableConcept] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
