# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductUndesirableEffect resource.

Complete MedicinalProductUndesirableEffect resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Reference,
    CodeableConcept,
    Range,
)


@dataclass
class Population:
    """
    FHIR Population complex type.
    
    A populatio group (e.g. patients, practitioners, etc.).
    """

    ageRange: Optional[Range] = None
    ageCodeableConcept: Optional[CodeableConcept] = None
    gender: Optional[CodeableConcept] = None
    race: Optional[CodeableConcept] = None
    physiologicalCondition: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductUndesirableEffect(FHIRResource):
    """
    FHIR R4 MedicinalProductUndesirableEffect resource.

    Describe the undesirable effects of the medicinal product.
    """

    resourceType: str = "MedicinalProductUndesirableEffect"
    # Subject
    subject: List[Reference] = field(default_factory=list)
    # Symptom Condition Effect
    symptomConditionEffect: Optional[CodeableConcept] = None
    # Classification
    classification: Optional[CodeableConcept] = None
    # Frequency of Occurrence
    frequencyOfOccurrence: Optional[CodeableConcept] = None
    # Population
    population: List[Population] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
