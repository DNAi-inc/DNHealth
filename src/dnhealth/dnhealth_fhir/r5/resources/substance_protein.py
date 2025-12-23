# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SubstanceProtein resource.

A SubstanceProtein is defined as a single unit of a linear amino acid sequence, or a combination of subunits that are either covalently linked or have a defined invariant stoichiometric relationship. This includes all synthetic, recombinant and purified SubstanceProteins of defined sequence, whether the use is therapeutic or prophylactic. This set of elements will be used to describe albumins, coagulation factors, cytokines, growth factors, peptide/SubstanceProtein hormones, enzymes, toxins, toxoids, recombinant vaccines, and immunomodulators.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Extension, Identifier
from typing import List, Optional

@dataclass
class SubstanceProteinSubunit:
    """
    SubstanceProteinSubunit nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    subunit: Optional[int] = None  # Index of primary sequences of amino acids linked through peptide bonds in order of decreasing len...
    sequence: Optional[str] = None  # The sequence information shall be provided enumerating the amino acids from N- to C-terminal end ...
    length: Optional[int] = None  # Length of linear sequences of amino acids contained in the subunit.
    sequenceAttachment: Optional[Attachment] = None  # The sequence information shall be provided enumerating the amino acids from N- to C-terminal end ...
    nTerminalModificationId: Optional[Identifier] = None  # Unique identifier for molecular fragment modification based on the ISO 11238 Substance ID.
    nTerminalModification: Optional[str] = None  # The name of the fragment modified at the N-terminal of the SubstanceProtein shall be specified.
    cTerminalModificationId: Optional[Identifier] = None  # Unique identifier for molecular fragment modification based on the ISO 11238 Substance ID.
    cTerminalModification: Optional[str] = None  # The modification at the C-terminal shall be specified.


@dataclass
class SubstanceProtein(FHIRResource):
    """
    A SubstanceProtein is defined as a single unit of a linear amino acid sequence, or a combination of subunits that are either covalently linked or have a defined invariant stoichiometric relationship. This includes all synthetic, recombinant and purified SubstanceProteins of defined sequence, whether the use is therapeutic or prophylactic. This set of elements will be used to describe albumins, coagulation factors, cytokines, growth factors, peptide/SubstanceProtein hormones, enzymes, toxins, toxoids, recombinant vaccines, and immunomodulators.
    """

    resourceType: str = "SubstanceProtein"
    sequenceType: Optional[CodeableConcept] = None  # The SubstanceProtein descriptive elements will only be used when a complete or partial amino acid...
    numberOfSubunits: Optional[int] = None  # Number of linear sequences of amino acids linked through peptide bonds. The number of subunits co...
    disulfideLinkage: Optional[List[str]] = field(default_factory=list)  # The disulphide bond between two cysteine residues either on the same subunit or on two different ...
    subunit: Optional[List[BackboneElement]] = field(default_factory=list)  # This subclause refers to the description of each subunit constituting the SubstanceProtein. A sub...