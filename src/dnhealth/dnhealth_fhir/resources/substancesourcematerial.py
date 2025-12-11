# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SubstanceSourceMaterial resource.

Complete SubstanceSourceMaterial resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Identifier,
    Reference,
)


@dataclass
class SubstanceSourceMaterialFractionDescription:
    """
    FHIR R4 SubstanceSourceMaterial.fractionDescription element.
    
    Many complex materials are fractions of parts of plants, animals, or fungi.
    Physical elements are used for fractions not otherwise specified, such as
    starch and its derivatives, and cellulose.
    """

    fraction: Optional[str] = None
    materialType: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSourceMaterialOrganism:
    """
    FHIR R4 SubstanceSourceMaterial.organism element.
    
    This sub-element refers to a substance source material organism entity.
    It captures taxonomic information about the organism from which the
    substance is derived, including family, genus, species, and other
    taxonomic classifications.
    """

    family: Optional[CodeableConcept] = None
    genus: Optional[CodeableConcept] = None
    species: Optional[CodeableConcept] = None
    intraspecificType: Optional[CodeableConcept] = None
    intraspecificDescription: Optional[str] = None
    author: List["SubstanceSourceMaterialOrganismAuthor"] = field(default_factory=list)
    hybrid: Optional["SubstanceSourceMaterialOrganismHybrid"] = None
    organismGeneral: Optional["SubstanceSourceMaterialOrganismOrganismGeneral"] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSourceMaterialOrganismAuthor:
    """
    FHIR R4 SubstanceSourceMaterial.organism.author element.
    
    4.9.13.6.1 Author of an organism species shall be specified if applicable.
    """

    authorType: Optional[CodeableConcept] = None
    authorDescription: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSourceMaterialOrganismHybrid:
    """
    FHIR R4 SubstanceSourceMaterial.organism.hybrid element.
    
    4.9.13.6.2 An organism shall be defined as a hybrid (maternal and paternal)
    given the circumstances.
    """

    maternalOrganismId: Optional[str] = None
    maternalOrganismName: Optional[str] = None
    paternalOrganismId: Optional[str] = None
    paternalOrganismName: Optional[str] = None
    hybridType: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSourceMaterialOrganismOrganismGeneral:
    """
    FHIR R4 SubstanceSourceMaterial.organism.organismGeneral element.
    
    4.9.13.6.3 The 7 kingdom of life shall be specified if applicable.
    """

    kingdom: Optional[CodeableConcept] = None
    phylum: Optional[CodeableConcept] = None
    class_: Optional[CodeableConcept] = None
    order: Optional[CodeableConcept] = None
    family: Optional[CodeableConcept] = None
    genus: Optional[CodeableConcept] = None
    species: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSourceMaterialPartDescription:
    """
    FHIR R4 SubstanceSourceMaterial.partDescription element.
    
    This sub-element refers to a substance source material part entity.
    It describes the anatomical part of the organism from which the
    substance is derived, including the specific part and its location.
    """

    part: Optional[CodeableConcept] = None
    partLocation: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class SubstanceSourceMaterial(FHIRResource):
    """
    FHIR R4 SubstanceSourceMaterial resource.

    Source material shall capture information on the taxonomic and anatomical origins
    as well as the fraction of a material that can result in or can be modified to form
    a substance.
    """

    resourceType: str = "SubstanceSourceMaterial"
    # Source Material Class
    sourceMaterialClass: Optional[CodeableConcept] = None
    # Source Material Type
    sourceMaterialType: Optional[CodeableConcept] = None
    # Source Material State
    sourceMaterialState: Optional[CodeableConcept] = None
    # Organism Id
    organismId: Optional[Identifier] = None
    # Organism Name
    organismName: Optional[str] = None
    # Parent Substance Id
    parentSubstanceId: List[Identifier] = field(default_factory=list)
    # Parent Substance Name
    parentSubstanceName: List[str] = field(default_factory=list)
    # Country of Origin
    countryOfOrigin: List[CodeableConcept] = field(default_factory=list)
    # Geographical Location
    geographicalLocation: List[str] = field(default_factory=list)
    # Development Stage
    developmentStage: Optional[CodeableConcept] = None
    # Fraction Description
    fractionDescription: List[SubstanceSourceMaterialFractionDescription] = field(default_factory=list)
    # Organism
    organism: Optional[SubstanceSourceMaterialOrganism] = None
    # Part Description
    partDescription: List[SubstanceSourceMaterialPartDescription] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
