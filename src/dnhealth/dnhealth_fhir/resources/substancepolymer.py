# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SubstancePolymer resource.

Complete SubstancePolymer resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Attachment,
    Quantity,
    Ratio,
)


@dataclass
class SubstancePolymerMonomerSet:
    """
    FHIR R4 SubstancePolymer.monomerSet element.
    
    A polymer is defined as a material composed of repeating structural units
    and these units can be described as monomer sets. This element describes
    the type of monomer set and the starting materials used to create the polymer.
    """

    ratioType: Optional[CodeableConcept] = None
    startingMaterial: List["SubstancePolymerMonomerSetStartingMaterial"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstancePolymerMonomerSetStartingMaterial:
    """
    FHIR R4 SubstancePolymer.monomerSet.startingMaterial element.
    
    A starting material for a polymer substance. This element describes the
    material used as a starting point in the polymerization process, including
    the material type, whether it is defining, and the amount used.
    """

    material: Optional[CodeableConcept] = None
    type: Optional[CodeableConcept] = None
    isDefining: Optional[bool] = None
    amount: Optional[Quantity] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstancePolymerRepeat:
    """
    FHIR R4 SubstancePolymer.repeat element.
    
    A polymer is characterized by repeating structural units. This element
    describes the repeating units of the polymer, including the number of units,
    average molecular formula, and the type of repeat units.
    """

    numberOfUnits: Optional[int] = None
    averageMolecularFormula: Optional[str] = None
    repeatUnitAmountType: Optional[CodeableConcept] = None
    repeatUnit: List["SubstancePolymerRepeatRepeatUnit"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstancePolymerRepeatRepeatUnit:
    """
    FHIR R4 SubstancePolymer.repeat.repeatUnit element.
    
    A repeating unit of a polymer substance. This element describes the
    structural unit that repeats in the polymer, including its orientation,
    amount, degree of polymerization, and structural representation.
    """

    orientationOfPolymerisation: Optional[CodeableConcept] = None
    repeatUnit: Optional[str] = None
    amount: Optional[Quantity] = None
    degreeOfPolymerisation: List["SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation"] = field(default_factory=list)
    structuralRepresentation: List["SubstancePolymerRepeatRepeatUnitStructuralRepresentation"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation:
    """
    FHIR R4 SubstancePolymer.repeat.repeatUnit.degreeOfPolymerisation element.
    
    The degree of polymerization describes the number of repeating units in a
    polymer chain. This element specifies the degree type and the amount
    (number of units) for the polymer.
    """

    degree: Optional[CodeableConcept] = None
    amount: Optional[Quantity] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstancePolymerRepeatRepeatUnitStructuralRepresentation:
    """
    FHIR R4 SubstancePolymer.repeat.repeatUnit.structuralRepresentation element.
    
    A structural representation of the repeating unit. This element provides
    different ways to represent the structure, including text-based notation,
    attachments with structural diagrams, or other representation types.
    """

    type: Optional[CodeableConcept] = None
    representation: Optional[str] = None
    attachment: Optional[Attachment] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstancePolymer(FHIRResource):
    """
    FHIR R4 SubstancePolymer resource.

    A polymer is a material composed of repeating structural units connected
    by covalent chemical bonds. This resource describes the polymer substance,
    including its class, geometry, copolymer connectivity, modifications,
    monomer sets, and repeating units.
    """

    resourceType: str = "SubstancePolymer"
    # Class
    class_: Optional[CodeableConcept] = None
    # Geometry
    geometry: Optional[CodeableConcept] = None
    # Copolymer Connectivity
    copolymerConnectivity: List[CodeableConcept] = field(default_factory=list)
    # Modification
    modification: List[str] = field(default_factory=list)
    # Monomer Set
    monomerSet: List[SubstancePolymerMonomerSet] = field(default_factory=list)
    # Repeat
    repeat: List[SubstancePolymerRepeat] = field(default_factory=list)


def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()
