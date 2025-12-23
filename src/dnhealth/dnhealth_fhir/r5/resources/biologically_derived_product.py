# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 BiologicallyDerivedProduct resource.

A biological material originating from a biological entity intended to be transplanted or infused into another (possibly the same) biological entity.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Period, Quantity, Range, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class BiologicallyDerivedProductCollection:
    """
    BiologicallyDerivedProductCollection nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    collector: Optional[Reference] = None  # Healthcare professional who is performing the collection.
    source: Optional[Reference] = None  # The patient or entity, such as a hospital or vendor in the case of a processed/manipulated/manufa...
    collected: Optional[Any] = None  # Time of product collection.

@dataclass
class BiologicallyDerivedProductProperty:
    """
    BiologicallyDerivedProductProperty nested class.
    """

    type: Optional[CodeableConcept] = None  # Code that specifies the property. It should reference an established coding system.
    value: Optional[Any] = None  # Property values.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class BiologicallyDerivedProduct(FHIRResource):
    """
    A biological material originating from a biological entity intended to be transplanted or infused into another (possibly the same) biological entity.
    """

    resourceType: str = "BiologicallyDerivedProduct"
    productCategory: Optional[Coding] = None  # Broad category of this product.
    productCode: Optional[CodeableConcept] = None  # A codified value that systematically supports characterization and classification of medical prod...
    parent: Optional[List[Reference]] = field(default_factory=list)  # Parent product (if any) for this biologically-derived product.
    request: Optional[List[Reference]] = field(default_factory=list)  # Request to obtain and/or infuse this biologically derived product.
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique instance identifiers assigned to a biologically derived product. Note: This is a business ...
    biologicalSourceEvent: Optional[Identifier] = None  # An identifier that supports traceability to the event during which material in this product from ...
    processingFacility: Optional[List[Reference]] = field(default_factory=list)  # Processing facilities responsible for the labeling and distribution of this biologically derived ...
    division: Optional[str] = None  # A unique identifier for an aliquot of a product.  Used to distinguish individual aliquots of a pr...
    productStatus: Optional[Coding] = None  # Whether the product is currently available.
    expirationDate: Optional[str] = None  # Date, and where relevant time, of expiration.
    collection: Optional[BackboneElement] = None  # How this product was collected.
    storageTempRequirements: Optional[Range] = None  # The temperature requirements for storage of the biologically-derived product.
    property: Optional[List[BackboneElement]] = field(default_factory=list)  # A property that is specific to this BiologicallyDerviedProduct instance.