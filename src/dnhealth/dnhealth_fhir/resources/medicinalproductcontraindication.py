# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductContraindication resource.

Complete MedicinalProductContraindication resource with all R4 elements.
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
class MedicinalProductContraindicationOtherTherapy:
    """
    Information about the use of the medicinal product in relation to other therapies.
    """

    therapyRelationshipType: CodeableConcept  # The type of relationship between the medicinal product indication or contraindication and another therapy (required)
    medicationCodeableConcept: Optional[CodeableConcept] = None
    medicationReference: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductContraindication(FHIRResource):
    """
    FHIR R4 MedicinalProductContraindication resource.

    MedicinalProductContraindication includes the use of a medicinal product in relation to
    other therapies, medical conditions, allergies, etc.
    """

    resourceType: str = "MedicinalProductContraindication"
    # Subject
    subject: List[Reference] = field(default_factory=list)
    # Disease
    disease: Optional[CodeableConcept] = None
    # Disease Status
    diseaseStatus: Optional[CodeableConcept] = None
    # Comorbidity
    comorbidity: List[CodeableConcept] = field(default_factory=list)
    # Therapeutic Indication
    therapeuticIndication: List[Reference] = field(default_factory=list)
    # Other Therapy
    otherTherapy: List[MedicinalProductContraindicationOtherTherapy] = field(default_factory=list)
    # Population
    population: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
