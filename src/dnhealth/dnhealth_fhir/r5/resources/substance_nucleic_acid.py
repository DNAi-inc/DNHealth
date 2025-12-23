# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SubstanceNucleicAcid resource.

Nucleic acids are defined by three distinct elements: the base, sugar and linkage. Individual substance/moiety IDs will be created for each of these elements. The nucleotide sequence will be always entered in the 5’-3’ direction.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Extension, Identifier
from typing import List, Optional

@dataclass
class SubstanceNucleicAcidSubunit:
    """
    SubstanceNucleicAcidSubunit nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    subunit: Optional[int] = None  # Index of linear sequences of nucleic acids in order of decreasing length. Sequences of the same l...
    sequence: Optional[str] = None  # Actual nucleotide sequence notation from 5' to 3' end using standard single letter codes. In addi...
    length: Optional[int] = None  # The length of the sequence shall be captured.
    sequenceAttachment: Optional[Attachment] = None  # (TBC).
    fivePrime: Optional[CodeableConcept] = None  # The nucleotide present at the 5’ terminal shall be specified based on a controlled vocabulary. Si...
    threePrime: Optional[CodeableConcept] = None  # The nucleotide present at the 3’ terminal shall be specified based on a controlled vocabulary. Si...
    linkage: Optional[List[BackboneElement]] = field(default_factory=list)  # The linkages between sugar residues will also be captured.
    connectivity: Optional[str] = None  # The entity that links the sugar residues together should also be captured for nearly all naturall...
    identifier: Optional[Identifier] = None  # Each linkage will be registered as a fragment and have an ID.
    name: Optional[str] = None  # Each linkage will be registered as a fragment and have at least one name. A single name shall be ...
    residueSite: Optional[str] = None  # Residues shall be captured as described in 5.3.6.8.3.
    sugar: Optional[List[BackboneElement]] = field(default_factory=list)  # 5.3.6.8.1 Sugar ID (Mandatory).

@dataclass
class SubstanceNucleicAcidSubunitLinkage:
    """
    SubstanceNucleicAcidSubunitLinkage nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    connectivity: Optional[str] = None  # The entity that links the sugar residues together should also be captured for nearly all naturall...
    identifier: Optional[Identifier] = None  # Each linkage will be registered as a fragment and have an ID.
    name: Optional[str] = None  # Each linkage will be registered as a fragment and have at least one name. A single name shall be ...
    residueSite: Optional[str] = None  # Residues shall be captured as described in 5.3.6.8.3.

@dataclass
class SubstanceNucleicAcidSubunitSugar:
    """
    SubstanceNucleicAcidSubunitSugar nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[Identifier] = None  # The Substance ID of the sugar or sugar-like component that make up the nucleotide.
    name: Optional[str] = None  # The name of the sugar or sugar-like component that make up the nucleotide.
    residueSite: Optional[str] = None  # The residues that contain a given sugar will be captured. The order of given residues will be cap...


@dataclass
class SubstanceNucleicAcid(FHIRResource):
    """
    Nucleic acids are defined by three distinct elements: the base, sugar and linkage. Individual substance/moiety IDs will be created for each of these elements. The nucleotide sequence will be always entered in the 5’-3’ direction.
    """

    resourceType: str = "SubstanceNucleicAcid"
    sequenceType: Optional[CodeableConcept] = None  # The type of the sequence shall be specified based on a controlled vocabulary.
    numberOfSubunits: Optional[int] = None  # The number of linear sequences of nucleotides linked through phosphodiester bonds shall be descri...
    areaOfHybridisation: Optional[str] = None  # The area of hybridisation shall be described if applicable for double stranded RNA or DNA. The nu...
    oligoNucleotideType: Optional[CodeableConcept] = None  # (TBC).
    subunit: Optional[List[BackboneElement]] = field(default_factory=list)  # Subunits are listed in order of decreasing length; sequences of the same length will be ordered b...