# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SubstanceReferenceInformation resource.

Todo.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Range, Reference
from typing import Any, List, Optional

@dataclass
class SubstanceReferenceInformationGene:
    """
    SubstanceReferenceInformationGene nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    geneSequenceOrigin: Optional[CodeableConcept] = None  # Todo.
    gene: Optional[CodeableConcept] = None  # Todo.
    source: Optional[List[Reference]] = field(default_factory=list)  # Todo.

@dataclass
class SubstanceReferenceInformationGeneElement:
    """
    SubstanceReferenceInformationGeneElement nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Todo.
    element: Optional[Identifier] = None  # Todo.
    source: Optional[List[Reference]] = field(default_factory=list)  # Todo.

@dataclass
class SubstanceReferenceInformationTarget:
    """
    SubstanceReferenceInformationTarget nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    target: Optional[Identifier] = None  # Todo.
    type: Optional[CodeableConcept] = None  # Todo.
    interaction: Optional[CodeableConcept] = None  # Todo.
    organism: Optional[CodeableConcept] = None  # Todo.
    organismType: Optional[CodeableConcept] = None  # Todo.
    amount: Optional[Any] = None  # Todo.
    amountType: Optional[CodeableConcept] = None  # Todo.
    source: Optional[List[Reference]] = field(default_factory=list)  # Todo.


@dataclass
class SubstanceReferenceInformation(FHIRResource):
    """
    Todo.
    """

    resourceType: str = "SubstanceReferenceInformation"
    comment: Optional[str] = None  # Todo.
    gene: Optional[List[BackboneElement]] = field(default_factory=list)  # Todo.
    geneElement: Optional[List[BackboneElement]] = field(default_factory=list)  # Todo.
    target: Optional[List[BackboneElement]] = field(default_factory=list)  # Todo.