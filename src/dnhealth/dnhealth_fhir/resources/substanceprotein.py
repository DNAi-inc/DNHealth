# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SubstanceProtein resource.

Complete SubstanceProtein resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Identifier,
    Attachment,
)


@dataclass
class SubstanceProteinSubunit:
    """
    This sub-element refers to a specific sequence of amino acids making up the protein.
    """

    subunit: Optional[int] = None
    sequence: Optional[str] = None
    length: Optional[int] = None
    sequenceAttachment: Optional[Attachment] = None
    nTerminalModificationId: Optional[Identifier] = None
    nTerminalModification: Optional[str] = None
    cTerminalModificationId: Optional[Identifier] = None
    cTerminalModification: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceProtein(FHIRResource):
    """
    FHIR R4 SubstanceProtein resource.

    A SubstanceProtein is defined as a single protein sequence, or a complex of
    protein sequences with modifications, attachments, or linked molecules.
    """

    resourceType: str = "SubstanceProtein"
    # Sequence Type
    sequenceType: Optional[CodeableConcept] = None
    # Number of Subunits
    numberOfSubunits: Optional[int] = None
    # Disulfide Linkage
    disulfideLinkage: List[str] = field(default_factory=list)
    # Subunit
    subunit: List[SubstanceProteinSubunit] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
