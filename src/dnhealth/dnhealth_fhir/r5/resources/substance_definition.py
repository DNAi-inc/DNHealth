# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SubstanceDefinition resource.

The detailed description of a substance, typically at a level beyond what is used for prescribing.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class SubstanceDefinitionMoiety:
    """
    SubstanceDefinitionMoiety nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    role: Optional[CodeableConcept] = None  # Role that the moiety is playing.
    identifier: Optional[Identifier] = None  # Identifier by which this moiety substance is known.
    name: Optional[str] = None  # Textual name for this moiety substance.
    stereochemistry: Optional[CodeableConcept] = None  # Stereochemistry type.
    opticalActivity: Optional[CodeableConcept] = None  # Optical activity type.
    molecularFormula: Optional[str] = None  # Molecular formula for this moiety of this substance, typically using the Hill system.
    amount: Optional[Any] = None  # Quantitative value for this moiety.
    measurementType: Optional[CodeableConcept] = None  # The measurement type of the quantitative value. In capturing the actual relative amounts of subst...

@dataclass
class SubstanceDefinitionCharacterization:
    """
    SubstanceDefinitionCharacterization nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    technique: Optional[CodeableConcept] = None  # The method used to elucidate the characterization of the drug substance. Example: HPLC.
    form: Optional[CodeableConcept] = None  # Describes the nature of the chemical entity and explains, for instance, whether this is a base or...
    description: Optional[str] = None  # The description or justification in support of the interpretation of the data file.
    file: Optional[List[Attachment]] = field(default_factory=list)  # The data produced by the analytical instrument or a pictorial representation of that data. Exampl...

@dataclass
class SubstanceDefinitionProperty:
    """
    SubstanceDefinitionProperty nested class.
    """

    type: Optional[CodeableConcept] = None  # A code expressing the type of property.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # A value for the property.

@dataclass
class SubstanceDefinitionMolecularWeight:
    """
    SubstanceDefinitionMolecularWeight nested class.
    """

    amount: Optional[Quantity] = None  # Used to capture quantitative values for a variety of elements. If only limits are given, the arit...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    method: Optional[CodeableConcept] = None  # The method by which the molecular weight was determined.
    type: Optional[CodeableConcept] = None  # Type of molecular weight such as exact, average (also known as. number average), weight average.

@dataclass
class SubstanceDefinitionStructure:
    """
    SubstanceDefinitionStructure nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    stereochemistry: Optional[CodeableConcept] = None  # Stereochemistry type.
    opticalActivity: Optional[CodeableConcept] = None  # Optical activity type.
    molecularFormula: Optional[str] = None  # An expression which states the number and type of atoms present in a molecule of a substance.
    molecularFormulaByMoiety: Optional[str] = None  # Specified per moiety according to the Hill system, i.e. first C, then H, then alphabetical, each ...
    molecularWeight: Optional[Any] = None  # The molecular weight or weight range (for proteins, polymers or nucleic acids).
    technique: Optional[List[CodeableConcept]] = field(default_factory=list)  # The method used to elucidate the structure of the drug substance. Examples: X-ray, NMR, Peptide m...
    sourceDocument: Optional[List[Reference]] = field(default_factory=list)  # The source of information about the structure.
    representation: Optional[List[BackboneElement]] = field(default_factory=list)  # A depiction of the structure of the substance.
    type: Optional[CodeableConcept] = None  # The kind of structural representation (e.g. full, partial).
    format: Optional[CodeableConcept] = None  # The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF. The logical c...
    document: Optional[Reference] = None  # An attached file with the structural representation e.g. a molecular structure graphic of the sub...

@dataclass
class SubstanceDefinitionStructureRepresentation:
    """
    SubstanceDefinitionStructureRepresentation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The kind of structural representation (e.g. full, partial).
    representation: Optional[str] = None  # The structural representation as a text string in a standard format.
    format: Optional[CodeableConcept] = None  # The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF. The logical c...
    document: Optional[Reference] = None  # An attached file with the structural representation e.g. a molecular structure graphic of the sub...

@dataclass
class SubstanceDefinitionCode:
    """
    SubstanceDefinitionCode nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[CodeableConcept] = None  # The specific code.
    status: Optional[CodeableConcept] = None  # Status of the code assignment, for example 'provisional', 'approved'.
    statusDate: Optional[str] = None  # The date at which the code status was changed as part of the terminology maintenance.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Any comment can be provided in this field, if necessary.
    source: Optional[List[Reference]] = field(default_factory=list)  # Supporting literature.

@dataclass
class SubstanceDefinitionName:
    """
    SubstanceDefinitionName nested class.
    """

    name: Optional[str] = None  # The actual name.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Name type, for example 'systematic',  'scientific, 'brand'.
    status: Optional[CodeableConcept] = None  # The status of the name, for example 'current', 'proposed'.
    preferred: Optional[bool] = None  # If this is the preferred name for this substance.
    language: Optional[List[CodeableConcept]] = field(default_factory=list)  # Human language that the name is written in.
    domain: Optional[List[CodeableConcept]] = field(default_factory=list)  # The use context of this name for example if there is a different name a drug active ingredient as...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # The jurisdiction where this name applies.
    synonym: Optional[List[Any]] = field(default_factory=list)  # A synonym of this particular name, by which the substance is also known.
    translation: Optional[List[Any]] = field(default_factory=list)  # A translation for this name into another human language.
    official: Optional[List[BackboneElement]] = field(default_factory=list)  # Details of the official nature of this name.
    authority: Optional[CodeableConcept] = None  # Which authority uses this official name.
    date: Optional[str] = None  # Date of the official name change.
    source: Optional[List[Reference]] = field(default_factory=list)  # Supporting literature.

@dataclass
class SubstanceDefinitionNameOfficial:
    """
    SubstanceDefinitionNameOfficial nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    authority: Optional[CodeableConcept] = None  # Which authority uses this official name.
    status: Optional[CodeableConcept] = None  # The status of the official name, for example 'draft', 'active', 'retired'.
    date: Optional[str] = None  # Date of the official name change.

@dataclass
class SubstanceDefinitionRelationship:
    """
    SubstanceDefinitionRelationship nested class.
    """

    type: Optional[CodeableConcept] = None  # For example \"salt to parent\", \"active moiety\", \"starting material\", \"polymorph\", \"impuri...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    substanceDefinition: Optional[Any] = None  # A pointer to another substance, as a resource or just a representational code.
    isDefining: Optional[bool] = None  # For example where an enzyme strongly bonds with a particular substance, this is a defining relati...
    amount: Optional[Any] = None  # A numeric factor for the relationship, for instance to express that the salt of a substance has s...
    ratioHighLimitAmount: Optional[Ratio] = None  # For use when the numeric has an uncertain range.
    comparator: Optional[CodeableConcept] = None  # An operator for the amount, for example \"average\", \"approximately\", \"less than\".
    source: Optional[List[Reference]] = field(default_factory=list)  # Supporting literature.

@dataclass
class SubstanceDefinitionSourceMaterial:
    """
    SubstanceDefinitionSourceMaterial nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # A classification that provides the origin of the raw material. Example: cat hair would be an Anim...
    genus: Optional[CodeableConcept] = None  # The genus of an organism, typically referring to the Latin epithet of the genus element of the pl...
    species: Optional[CodeableConcept] = None  # The species of an organism, typically referring to the Latin epithet of the species of the plant/...
    part: Optional[CodeableConcept] = None  # An anatomical origin of the source material within an organism.
    countryOfOrigin: Optional[List[CodeableConcept]] = field(default_factory=list)  # The country or countries where the material is harvested.


@dataclass
class SubstanceDefinition(FHIRResource):
    """
    The detailed description of a substance, typically at a level beyond what is used for prescribing.
    """

    resourceType: str = "SubstanceDefinition"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier by which this substance is known.
    version: Optional[str] = None  # A business level version identifier of the substance.
    status: Optional[CodeableConcept] = None  # Status of substance within the catalogue e.g. active, retired.
    classification: Optional[List[CodeableConcept]] = field(default_factory=list)  # A high level categorization, e.g. polymer or nucleic acid, or food, chemical, biological, or a lo...
    domain: Optional[CodeableConcept] = None  # If the substance applies to human or veterinary use.
    grade: Optional[List[CodeableConcept]] = field(default_factory=list)  # The quality standard, established benchmark, to which substance complies (e.g. USP/NF, Ph. Eur, J...
    description: Optional[str] = None  # Textual description of the substance.
    informationSource: Optional[List[Reference]] = field(default_factory=list)  # Supporting literature.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Textual comment about the substance's catalogue or registry record.
    manufacturer: Optional[List[Reference]] = field(default_factory=list)  # The entity that creates, makes, produces or fabricates the substance. This is a set of potential ...
    supplier: Optional[List[Reference]] = field(default_factory=list)  # An entity that is the source for the substance. It may be different from the manufacturer. Suppli...
    moiety: Optional[List[BackboneElement]] = field(default_factory=list)  # Moiety, for structural modifications.
    characterization: Optional[List[BackboneElement]] = field(default_factory=list)  # General specifications for this substance.
    property: Optional[List[BackboneElement]] = field(default_factory=list)  # General specifications for this substance.
    referenceInformation: Optional[Reference] = None  # General information detailing this substance.
    molecularWeight: Optional[List[BackboneElement]] = field(default_factory=list)  # The average mass of a molecule of a compound compared to 1/12 the mass of carbon 12 and calculate...
    structure: Optional[BackboneElement] = None  # Structural information.
    code: Optional[List[BackboneElement]] = field(default_factory=list)  # Codes associated with the substance.
    name: Optional[List[BackboneElement]] = field(default_factory=list)  # Names applicable to this substance.
    relationship: Optional[List[BackboneElement]] = field(default_factory=list)  # A link between this substance and another, with details of the relationship.
    nucleicAcid: Optional[Reference] = None  # Data items specific to nucleic acids.
    polymer: Optional[Reference] = None  # Data items specific to polymers.
    protein: Optional[Reference] = None  # Data items specific to proteins.
    sourceMaterial: Optional[BackboneElement] = None  # Material or taxonomic/anatomical source for the substance.