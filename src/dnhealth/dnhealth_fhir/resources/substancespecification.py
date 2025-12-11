# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SubstanceSpecification resource.

Complete SubstanceSpecification resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Quantity,
    Ratio,
    Attachment,
    String,
)


@dataclass
class SubstanceSpecificationMoiety:
    """
    Moiety, for structural modifications.
    """

    role: Optional[CodeableConcept] = None
    identifier: Optional[Identifier] = None
    name: Optional[str] = None
    stereochemistry: Optional[CodeableConcept] = None
    opticalActivity: Optional[CodeableConcept] = None
    molecularFormula: Optional[str] = None
    amountQuantity: Optional[Quantity] = None
    amountString: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationProperty:
    """
    General specifications for this substance, including how it is related to other substances.
    """

    category: Optional[CodeableConcept] = None
    code: Optional[CodeableConcept] = None
    parameters: Optional[str] = None
    definingSubstanceReference: Optional[Reference] = None
    definingSubstanceCodeableConcept: Optional[CodeableConcept] = None
    amountQuantity: Optional[Quantity] = None
    amountString: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationStructure:
    """
    Structural information.
    """

    stereochemistry: Optional[CodeableConcept] = None
    opticalActivity: Optional[CodeableConcept] = None
    molecularFormula: Optional[str] = None
    molecularFormulaByMoiety: Optional[str] = None
    isotope: List["SubstanceSpecificationStructureIsotope"] = field(default_factory=list)
    molecularWeight: Optional["SubstanceSpecificationStructureMolecularWeight"] = None
    source: List[Reference] = field(default_factory=list)
    representation: List["SubstanceSpecificationStructureRepresentation"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationStructureIsotope:
    """
    Applicable for single substances that contain a radionuclide or a non-natural isotopic ratio.
    """

    identifier: Optional[Identifier] = None
    name: Optional[CodeableConcept] = None
    substitution: Optional[CodeableConcept] = None
    halfLife: Optional[Quantity] = None
    molecularWeight: Optional["SubstanceSpecificationStructureMolecularWeight"] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationStructureMolecularWeight:
    """
    The molecular weight or weight range (for proteins, polymers or nucleic acids).
    """

    method: Optional[CodeableConcept] = None
    type: Optional[CodeableConcept] = None
    amount: Optional[Quantity] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationStructureRepresentation:
    """
    Molecular structural representation.
    """

    type: Optional[CodeableConcept] = None
    representation: Optional[str] = None
    format: Optional[CodeableConcept] = None
    attachment: Optional[Attachment] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationCode:
    """
    Codes associated with the substance.
    """

    code: Optional[CodeableConcept] = None
    status: Optional[CodeableConcept] = None
    statusDate: Optional[str] = None  # ISO 8601 dateTime
    comment: Optional[str] = None
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationName:
    """
    Names applicable to this substance.
    """

    name: str  # The actual name (required)
    type: Optional[CodeableConcept] = None
    status: Optional[CodeableConcept] = None
    preferred: Optional[bool] = None
    language: List[CodeableConcept] = field(default_factory=list)
    domain: List[CodeableConcept] = field(default_factory=list)
    jurisdiction: List[CodeableConcept] = field(default_factory=list)
    synonym: List["SubstanceSpecificationName"] = field(default_factory=list)
    translation: List["SubstanceSpecificationName"] = field(default_factory=list)
    official: List["SubstanceSpecificationNameOfficial"] = field(default_factory=list)
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationNameOfficial:
    """
    Details of the official nature of this name.
    """

    authority: Optional[CodeableConcept] = None
    status: Optional[CodeableConcept] = None
    date: Optional[str] = None  # ISO 8601 dateTime
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecificationRelationship:
    """
    A link between this substance and another, with details of the relationship.
    """

    substanceReference: Optional[Reference] = None
    substanceCodeableConcept: Optional[CodeableConcept] = None
    relationship: Optional[CodeableConcept] = None
    isDefining: Optional[bool] = None
    amountQuantity: Optional[Quantity] = None
    amountRatio: Optional[Ratio] = None
    amountString: Optional[str] = None
    amountRatioLowLimit: Optional[Ratio] = None
    amountType: Optional[CodeableConcept] = None
    source: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSpecification(FHIRResource):
    """
    FHIR R4 SubstanceSpecification resource.

    The detailed description of a substance, typically at a level beyond what is used
    for prescribing.
    """

    resourceType: str = "SubstanceSpecification"
    # Identifier
    identifier: Optional[Identifier] = None
    # Type
    type: Optional[CodeableConcept] = None
    # Status
    status: Optional[CodeableConcept] = None
    # Domain
    domain: Optional[CodeableConcept] = None
    # Description
    description: Optional[str] = None
    # Source
    source: List[Reference] = field(default_factory=list)
    # Comment
    comment: Optional[str] = None
    # Moiety
    moiety: List[SubstanceSpecificationMoiety] = field(default_factory=list)
    # Property
    property: List[SubstanceSpecificationProperty] = field(default_factory=list)
    # Reference Information
    referenceInformation: Optional[Reference] = None
    # Structure
    structure: Optional[SubstanceSpecificationStructure] = None
    # Code
    code: List[SubstanceSpecificationCode] = field(default_factory=list)
    # Name
    name: List[SubstanceSpecificationName] = field(default_factory=list)
    # Relationship
    relationship: List[SubstanceSpecificationRelationship] = field(default_factory=list)
    # Nucleic Acid
    nucleicAcid: Optional[Reference] = None
    # Polymer
    polymer: Optional[Reference] = None
    # Protein
    protein: Optional[Reference] = None
    # Source Material
    sourceMaterial: Optional[Reference] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
