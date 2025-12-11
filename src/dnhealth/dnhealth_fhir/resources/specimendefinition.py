# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SpecimenDefinition resource.

Complete SpecimenDefinition resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    ContactDetail,
    UsageContext,
    RelatedArtifact,
    Duration,
    Quantity,
    Range,
)


@dataclass
class SpecimenDefinitionTypeTested:
    """
    Specimen handling before testing.
    
    Specimen handling before testing.
    """

    isDerived: Optional[bool] = None
    type: Optional[CodeableConcept] = None
    preference: str  # preferred | alternate (required)
    container: Optional["SpecimenDefinitionTypeTestedContainer"] = None
    requirement: Optional[str] = None
    retentionTime: Optional[Duration] = None
    rejectionCriterion: List[CodeableConcept] = field(default_factory=list)
    handling: List["SpecimenDefinitionTypeTestedHandling"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenDefinitionTypeTestedContainer:
    """
    The specimen's container.
    """

    material: Optional[CodeableConcept] = None
    type: Optional[CodeableConcept] = None
    cap: Optional[CodeableConcept] = None
    description: Optional[str] = None
    capacity: Optional[Quantity] = None
    minimumVolumeQuantity: Optional[Quantity] = None
    minimumVolumeString: Optional[str] = None
    additive: List["SpecimenDefinitionTypeTestedContainerAdditive"] = field(default_factory=list)
    preparation: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenDefinitionTypeTestedContainerAdditive:
    """
    Additive associated with container.
    """

    additiveCodeableConcept: Optional[CodeableConcept] = None
    additiveReference: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenDefinitionTypeTestedHandling:
    """
    Set of instructions for preservation/transport of the specimen.
    """

    temperatureQualifier: Optional[CodeableConcept] = None
    temperatureRange: Optional[Range] = None
    maxDuration: Optional[Duration] = None
    instruction: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenDefinitionCollection:
    """
    Specimen collection procedure.
    
    Specimen collection procedure.
    """

    method: Optional[CodeableConcept] = None
    patientPreparation: List[CodeableConcept] = field(default_factory=list)
    timeAspect: Optional[str] = None
    collection: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SpecimenDefinition(CanonicalResource):
    """
    FHIR R4 SpecimenDefinition resource.

    Represents a kind of specimen, or the specification of a kind of specimen
    to be created.
    """

    resourceType: str = "SpecimenDefinition"
    # Type collected
    typeCollected: Optional[CodeableConcept] = None
    # Patient preparation
    patientPreparation: List[CodeableConcept] = field(default_factory=list)
    # Time aspect
    timeAspect: Optional[str] = None
    # Collection
    collection: List[CodeableConcept] = field(default_factory=list)
    # Type tested
    typeTested: List[SpecimenDefinitionTypeTested] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
