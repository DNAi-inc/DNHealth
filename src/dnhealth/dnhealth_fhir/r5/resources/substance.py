# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Substance resource.

A homogeneous material with a definite composition.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class SubstanceIngredient:
    """
    SubstanceIngredient nested class.
    """

    substance: Optional[Any] = None  # Another substance that is a component of this substance.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    quantity: Optional[Ratio] = None  # The amount of the ingredient in the substance - a concentration ratio.


@dataclass
class Substance(FHIRResource):
    """
    A homogeneous material with a definite composition.
    """

    instance: Optional[bool] = None  # A boolean to indicate if this an instance of a substance or a kind of one (a definition).
    code: Optional[Any] = None  # A code (or set of codes) that identify this substance.
    resourceType: str = "Substance"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique identifier for the substance. For an instance, an identifier associated with the package/c...
    status: Optional[str] = None  # A code to indicate if the substance is actively used.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A code that classifies the general type of substance.  This is used  for searching, sorting and d...
    description: Optional[str] = None  # A description of the substance - its appearance, handling requirements, and other usage notes.
    expiry: Optional[str] = None  # When the substance is no longer valid to use. For some substances, a single arbitrary date is use...
    quantity: Optional[Quantity] = None  # The amount of the substance.
    ingredient: Optional[List[BackboneElement]] = field(default_factory=list)  # A substance can be composed of other substances.