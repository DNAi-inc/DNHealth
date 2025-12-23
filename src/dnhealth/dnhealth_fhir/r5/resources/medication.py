# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Medication resource.

This resource is primarily used for the identification and definition of a medication, including ingredients, for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class MedicationIngredient:
    """
    MedicationIngredient nested class.
    """

    item: Optional[Any] = None  # The ingredient (substance or medication) that the ingredient.strength relates to.  This is repres...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    isActive: Optional[bool] = None  # Indication of whether this ingredient affects the therapeutic action of the drug.
    strength: Optional[Any] = None  # Specifies how many (or how much) of the items there are in this Medication.  For example, 250 mg ...

@dataclass
class MedicationBatch:
    """
    MedicationBatch nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    lotNumber: Optional[str] = None  # The assigned lot number of a batch of the specified product.
    expirationDate: Optional[str] = None  # When this specific batch of product will expire.


@dataclass
class Medication(FHIRResource):
    """
    This resource is primarily used for the identification and definition of a medication, including ingredients, for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.
    """

    resourceType: str = "Medication"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for this medication.
    code: Optional[CodeableConcept] = None  # A code (or set of codes) that specify this medication, or a textual description if no code is ava...
    status: Optional[str] = None  # A code to indicate if the medication is in active use.
    marketingAuthorizationHolder: Optional[Reference] = None  # The company or other legal entity that has authorization, from the appropriate drug regulatory au...
    doseForm: Optional[CodeableConcept] = None  # Describes the form of the item.  Powder; tablets; capsule.
    totalVolume: Optional[Quantity] = None  # When the specified product code does not infer a package size, this is the specific amount of dru...
    ingredient: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies a particular constituent of interest in the product.
    batch: Optional[BackboneElement] = None  # Information that only applies to packages (not products).
    definition: Optional[Reference] = None  # A reference to a knowledge resource that provides more information about this medication.