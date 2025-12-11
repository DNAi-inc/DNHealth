# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SubstanceReferenceInformation resource.

Complete SubstanceReferenceInformation resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Reference,
    Quantity,
    Range,
    Identifier,
    Attachment,
)


@dataclass
class SubstanceReferenceInformationGene:
    """
    FHIR R4 SubstanceReferenceInformation.gene element.
    
    Substance reference information related to genes. This element describes
    the gene sequence origin, the specific gene, and sources of information
    about the gene's relationship to the substance.
    """

    geneSequenceOrigin: Optional[CodeableConcept] = None
    gene: Optional[CodeableConcept] = None
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceReferenceInformationGeneElement:
    """
    FHIR R4 SubstanceReferenceInformation.geneElement element.
    
    Substance reference information related to gene elements. This element
    describes the type of gene element, the specific element identifier, and
    sources of information about the gene element's relationship to the substance.
    """

    type: Optional[CodeableConcept] = None
    element: Optional[Identifier] = None
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceReferenceInformationClassification:
    """
    FHIR R4 SubstanceReferenceInformation.classification element.
    
    Substance reference information classification. This element describes
    the domain, classification, subtypes, and sources of information for
    classifying the substance.
    """

    domain: Optional[CodeableConcept] = None
    classification: Optional[CodeableConcept] = None
    subtype: List[CodeableConcept] = field(default_factory=list)
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceReferenceInformationTarget:
    """
    FHIR R4 SubstanceReferenceInformation.target element.
    
    Substance reference information related to targets. This element
    describes the target identifier, type, interaction, organism information,
    amount, and sources of information about the target's relationship to
    the substance.
    """

    target: Optional[Identifier] = None
    type: Optional[CodeableConcept] = None
    interaction: Optional[CodeableConcept] = None
    organism: Optional[CodeableConcept] = None
    organismType: Optional[CodeableConcept] = None
    amountQuantity: Optional[Quantity] = None
    amountRange: Optional[Range] = None
    amountString: Optional[str] = None
    amountType: Optional[CodeableConcept] = None
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceReferenceInformation(FHIRResource):
    """
    FHIR R4 SubstanceReferenceInformation resource.

    Substance reference information provides additional information about
    a substance, including gene-related information, classifications, targets,
    and other reference data that helps characterize the substance.
    """

    resourceType: str = "SubstanceReferenceInformation"
    # Comment
    comment: Optional[str] = None
    # Gene
    gene: List[SubstanceReferenceInformationGene] = field(default_factory=list)
    # Gene Element
    geneElement: List[SubstanceReferenceInformationGeneElement] = field(default_factory=list)
    # Classification
    classification: List[SubstanceReferenceInformationClassification] = field(default_factory=list)
    # Target
    target: List[SubstanceReferenceInformationTarget] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
