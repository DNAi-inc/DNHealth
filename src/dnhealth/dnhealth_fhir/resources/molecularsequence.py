# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MolecularSequence resource.

Complete MolecularSequence resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Quantity,
)


@dataclass
class MolecularSequenceReferenceSeq:
    """
    A sequence used as reference to describe variants that are present in a sequence analyzed.
    """

    chromosome: Optional[CodeableConcept] = None
    genomeBuild: Optional[str] = None
    orientation: Optional[str] = None  # sense | antisense
    referenceSeqId: Optional[CodeableConcept] = None
    referenceSeqPointer: Optional[Reference] = None
    referenceSeqString: Optional[str] = None
    strand: Optional[str] = None  # watson | crick
    windowStart: Optional[int] = None
    windowEnd: Optional[int] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequenceVariant:
    """
    The definition of variant here originates from Sequence ontology (variant).
    """

    start: Optional[int] = None
    end: Optional[int] = None
    observedAllele: Optional[str] = None
    referenceAllele: Optional[str] = None
    cigar: Optional[str] = None
    variantPointer: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequenceQuality:
    """
    Quality for sequence quality. Scores are calculated using standard methods
    such as phred quality score.
    """

    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[str] = None  # indel | snp | unknown (required)
    standardSequence: Optional[CodeableConcept] = None
    start: Optional[int] = None
    end: Optional[int] = None
    score: Optional[Quantity] = None
    method: Optional[CodeableConcept] = None
    truthTP: Optional[float] = None
    queryTP: Optional[float] = None
    truthFN: Optional[float] = None
    queryFP: Optional[float] = None
    gtFP: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    fScore: Optional[float] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequenceRepository:
    """
    Configurations of the external repository.
    """

    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[str] = None  # directlink | openapi | login | oauth | other (required)
    url: Optional[str] = None
    name: Optional[str] = None
    datasetId: Optional[str] = None
    variantsetId: Optional[str] = None
    readsetId: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequenceStructureVariant:
    """
    Structural variant.
    """

    variantType: Optional[CodeableConcept] = None
    exact: Optional[bool] = None
    length: Optional[int] = None
    outer: Optional["MolecularSequenceStructureVariantOuter"] = None
    inner: Optional["MolecularSequenceStructureVariantInner"] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequenceStructureVariantOuter:
    """
    Structural variant outer.
    """

    start: Optional[int] = None
    end: Optional[int] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequenceStructureVariantInner:
    """
    Structural variant inner.
    """

    start: Optional[int] = None
    end: Optional[int] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MolecularSequence(FHIRResource):
    """
    FHIR R4 MolecularSequence resource.

    Raw data describing a biological sequence.
    """

    resourceType: str = "MolecularSequence"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Type
    type: Optional[str] = None  # aa | dna | rna
    # Coordinate System
    # Note: coordinateSystem is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce coordinateSystem is provided.
    coordinateSystem: Optional[int] = None  # Base number of coordinate system (0-based coordinate system) (required)
    # Patient
    patient: Optional[Reference] = None
    # Specimen
    specimen: Optional[Reference] = None
    # Device
    device: Optional[Reference] = None
    # Performer
    performer: Optional[Reference] = None
    # Quantity
    quantity: Optional[Quantity] = None
    # Reference Seq
    referenceSeq: Optional[MolecularSequenceReferenceSeq] = None
    # Variant
    variant: List[MolecularSequenceVariant] = field(default_factory=list)
    # Observed Seq
    observedSeq: Optional[str] = None
    # Quality
    quality: List[MolecularSequenceQuality] = field(default_factory=list)
    # Read Coverage
    readCoverage: Optional[int] = None
    # Repository
    repository: List[MolecularSequenceRepository] = field(default_factory=list)
    # Pointer
    pointer: List[Reference] = field(default_factory=list)
    # Structure Variant
    structureVariant: List[MolecularSequenceStructureVariant] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
