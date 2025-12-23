# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SubstancePolymer resource.

Properties of a substance specific to it being a polymer.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Quantity
from typing import List, Optional

@dataclass
class SubstancePolymerMonomerSet:
    """
    SubstancePolymerMonomerSet nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    ratioType: Optional[CodeableConcept] = None  # Captures the type of ratio to the entire polymer, e.g. Monomer/Polymer ratio, SRU/Polymer Ratio.
    startingMaterial: Optional[List[BackboneElement]] = field(default_factory=list)  # The starting materials - monomer(s) used in the synthesis of the polymer.
    code: Optional[CodeableConcept] = None  # The type of substance for this starting material.
    category: Optional[CodeableConcept] = None  # Substance high level category, e.g. chemical substance.
    isDefining: Optional[bool] = None  # Used to specify whether the attribute described is a defining element for the unique identificati...
    amount: Optional[Quantity] = None  # A percentage.

@dataclass
class SubstancePolymerMonomerSetStartingMaterial:
    """
    SubstancePolymerMonomerSetStartingMaterial nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[CodeableConcept] = None  # The type of substance for this starting material.
    category: Optional[CodeableConcept] = None  # Substance high level category, e.g. chemical substance.
    isDefining: Optional[bool] = None  # Used to specify whether the attribute described is a defining element for the unique identificati...
    amount: Optional[Quantity] = None  # A percentage.

@dataclass
class SubstancePolymerRepeat:
    """
    SubstancePolymerRepeat nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    averageMolecularFormula: Optional[str] = None  # A representation of an (average) molecular formula from a polymer.
    repeatUnitAmountType: Optional[CodeableConcept] = None  # How the quantitative amount of Structural Repeat Units is captured (e.g. Exact, Numeric, Average).
    repeatUnit: Optional[List[BackboneElement]] = field(default_factory=list)  # An SRU - Structural Repeat Unit.
    unit: Optional[str] = None  # Structural repeat units are essential elements for defining polymers.
    orientation: Optional[CodeableConcept] = None  # The orientation of the polymerisation, e.g. head-tail, head-head, random.
    amount: Optional[int] = None  # Number of repeats of this unit.
    degreeOfPolymerisation: Optional[List[BackboneElement]] = field(default_factory=list)  # Applies to homopolymer and block co-polymers where the degree of polymerisation within a block ca...
    type: Optional[CodeableConcept] = None  # The type of the degree of polymerisation shall be described, e.g. SRU/Polymer Ratio.
    average: Optional[int] = None  # An average amount of polymerisation.
    low: Optional[int] = None  # A low expected limit of the amount.
    high: Optional[int] = None  # A high expected limit of the amount.
    structuralRepresentation: Optional[List[BackboneElement]] = field(default_factory=list)  # A graphical structure for this SRU.
    representation: Optional[str] = None  # The structural representation as text string in a standard format e.g. InChI, SMILES, MOLFILE, CD...
    format: Optional[CodeableConcept] = None  # The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF.
    attachment: Optional[Attachment] = None  # An attached file with the structural representation.

@dataclass
class SubstancePolymerRepeatRepeatUnit:
    """
    SubstancePolymerRepeatRepeatUnit nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    unit: Optional[str] = None  # Structural repeat units are essential elements for defining polymers.
    orientation: Optional[CodeableConcept] = None  # The orientation of the polymerisation, e.g. head-tail, head-head, random.
    amount: Optional[int] = None  # Number of repeats of this unit.
    degreeOfPolymerisation: Optional[List[BackboneElement]] = field(default_factory=list)  # Applies to homopolymer and block co-polymers where the degree of polymerisation within a block ca...
    type: Optional[CodeableConcept] = None  # The type of the degree of polymerisation shall be described, e.g. SRU/Polymer Ratio.
    average: Optional[int] = None  # An average amount of polymerisation.
    low: Optional[int] = None  # A low expected limit of the amount.
    high: Optional[int] = None  # A high expected limit of the amount.
    structuralRepresentation: Optional[List[BackboneElement]] = field(default_factory=list)  # A graphical structure for this SRU.
    representation: Optional[str] = None  # The structural representation as text string in a standard format e.g. InChI, SMILES, MOLFILE, CD...
    format: Optional[CodeableConcept] = None  # The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF.
    attachment: Optional[Attachment] = None  # An attached file with the structural representation.

@dataclass
class SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation:
    """
    SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The type of the degree of polymerisation shall be described, e.g. SRU/Polymer Ratio.
    average: Optional[int] = None  # An average amount of polymerisation.
    low: Optional[int] = None  # A low expected limit of the amount.
    high: Optional[int] = None  # A high expected limit of the amount.

@dataclass
class SubstancePolymerRepeatRepeatUnitStructuralRepresentation:
    """
    SubstancePolymerRepeatRepeatUnitStructuralRepresentation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The type of structure (e.g. Full, Partial, Representative).
    representation: Optional[str] = None  # The structural representation as text string in a standard format e.g. InChI, SMILES, MOLFILE, CD...
    format: Optional[CodeableConcept] = None  # The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF.
    attachment: Optional[Attachment] = None  # An attached file with the structural representation.


@dataclass
class SubstancePolymer(FHIRResource):
    """
    Properties of a substance specific to it being a polymer.
    """

    resourceType: str = "SubstancePolymer"
    identifier: Optional[Identifier] = None  # A business idenfier for this polymer, but typically this is handled by a SubstanceDefinition iden...
    class_: Optional[CodeableConcept] = None  # Overall type of the polymer.
    geometry: Optional[CodeableConcept] = None  # Polymer geometry, e.g. linear, branched, cross-linked, network or dendritic.
    copolymerConnectivity: Optional[List[CodeableConcept]] = field(default_factory=list)  # Descrtibes the copolymer sequence type (polymer connectivity).
    modification: Optional[str] = None  # Todo - this is intended to connect to a repeating full modification structure, also used by Prote...
    monomerSet: Optional[List[BackboneElement]] = field(default_factory=list)  # Todo.
    repeat: Optional[List[BackboneElement]] = field(default_factory=list)  # Specifies and quantifies the repeated units and their configuration.