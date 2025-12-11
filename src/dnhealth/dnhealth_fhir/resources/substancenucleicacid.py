# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SubstanceNucleicAcid resource.

Complete SubstanceNucleicAcid resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Attachment,
)


@dataclass
class SubstanceNucleicAcidSubunit:
    """
    Subunits are listed in order of decreasing length; sequences of the same length will be ordered by molecular weight.
    """

    subunit: Optional[int] = None
    sequence: Optional[str] = None
    length: Optional[int] = None
    sequenceAttachment: Optional[Attachment] = None
    fivePrime: Optional[CodeableConcept] = None
    threePrime: Optional[CodeableConcept] = None
    linkage: List["SubstanceNucleicAcidSubunitLinkage"] = field(default_factory=list)
    sugar: List["SubstanceNucleicAcidSubunitSugar"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceNucleicAcidSubunitLinkage:
    """
    The linkages between sugar residues will also be captured.
    """

    connectivity: Optional[str] = None
    identifier: Optional[Identifier] = None
    name: Optional[str] = None
    residueSite: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceNucleicAcidSubunitSugar:
    """
    5' prime sugar or sugar analog composing part of the nucleotide.
    """

    identifier: Optional[Identifier] = None
    name: Optional[str] = None
    residueSite: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceNucleicAcid(FHIRResource):
    """
    FHIR R4 SubstanceNucleicAcid resource.

    Nucleic acids are defined by three distinct elements: the base, sugar and linkage.
    Individual substance/moiety IDs will be created for each of these elements.
    """

    resourceType: str = "SubstanceNucleicAcid"
    # Sequence Type
    sequenceType: Optional[CodeableConcept] = None
    # Number of Subunits
    numberOfSubunits: Optional[int] = None
    # Area of Hybridisation
    areaOfHybridisation: Optional[str] = None
    # Oligo Nucleotide Type
    oligoNucleotideType: Optional[CodeableConcept] = None
    # Subunit
    subunit: List[SubstanceNucleicAcidSubunit] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
