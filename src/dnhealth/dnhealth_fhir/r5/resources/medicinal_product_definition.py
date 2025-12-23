# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MedicinalProductDefinition resource.

Detailed definition of a medicinal product, typically for uses other than direct patient care (e.g. regulatory use, drug catalogs, to support prescribing, adverse events management etc.).
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class MedicinalProductDefinitionContact:
    """
    MedicinalProductDefinitionContact nested class.
    """

    contact: Optional[Reference] = None  # A product specific contact, person (in a role), or an organization.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Allows the contact to be classified, for example QPPV, Pharmacovigilance Enquiry Information.

@dataclass
class MedicinalProductDefinitionName:
    """
    MedicinalProductDefinitionName nested class.
    """

    productName: Optional[str] = None  # The full product name.
    country: Optional[CodeableConcept] = None  # Country code for where this name applies.
    language: Optional[CodeableConcept] = None  # Language code for this name.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Type of product name, such as rINN, BAN, Proprietary, Non-Proprietary.
    part: Optional[List[BackboneElement]] = field(default_factory=list)  # Coding words or phrases of the name.
    usage: Optional[List[BackboneElement]] = field(default_factory=list)  # Country and jurisdiction where the name applies, and associated language.
    jurisdiction: Optional[CodeableConcept] = None  # Jurisdiction code for where this name applies. A jurisdiction may be a sub- or supra-national ent...

@dataclass
class MedicinalProductDefinitionNamePart:
    """
    MedicinalProductDefinitionNamePart nested class.
    """

    part: Optional[str] = None  # A fragment of a product name.
    type: Optional[CodeableConcept] = None  # Identifying type for this part of the name (e.g. strength part).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class MedicinalProductDefinitionNameUsage:
    """
    MedicinalProductDefinitionNameUsage nested class.
    """

    country: Optional[CodeableConcept] = None  # Country code for where this name applies.
    language: Optional[CodeableConcept] = None  # Language code for this name.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    jurisdiction: Optional[CodeableConcept] = None  # Jurisdiction code for where this name applies. A jurisdiction may be a sub- or supra-national ent...

@dataclass
class MedicinalProductDefinitionCrossReference:
    """
    MedicinalProductDefinitionCrossReference nested class.
    """

    product: Optional[Any] = None  # Reference to another product, e.g. for linking authorised to investigational product.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The type of relationship, for instance branded to generic, virtual to actual product, product to ...

@dataclass
class MedicinalProductDefinitionOperation:
    """
    MedicinalProductDefinitionOperation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[Any] = None  # The type of manufacturing operation e.g. manufacturing itself, re-packaging. For the authorizatio...
    effectiveDate: Optional[Period] = None  # Date range of applicability.
    organization: Optional[List[Reference]] = field(default_factory=list)  # The organization or establishment responsible for (or associated with) the particular process or ...
    confidentialityIndicator: Optional[CodeableConcept] = None  # Specifies whether this particular business or manufacturing process is considered proprietary or ...

@dataclass
class MedicinalProductDefinitionCharacteristic:
    """
    MedicinalProductDefinitionCharacteristic nested class.
    """

    type: Optional[CodeableConcept] = None  # A code expressing the type of characteristic.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # A value for the characteristic.text.


@dataclass
class MedicinalProductDefinition(FHIRResource):
    """
    Detailed definition of a medicinal product, typically for uses other than direct patient care (e.g. regulatory use, drug catalogs, to support prescribing, adverse events management etc.).
    """

    name: List[BackboneElement] = field(default_factory=list)  # The product's name, including full name and possibly coded parts.
    resourceType: str = "MedicinalProductDefinition"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for this product. Could be an MPID. When in development or being regulated, p...
    type: Optional[CodeableConcept] = None  # Regulatory type, e.g. Investigational or Authorized.
    domain: Optional[CodeableConcept] = None  # If this medicine applies to human or veterinary uses.
    version: Optional[str] = None  # A business identifier relating to a specific version of the product, this is commonly used to sup...
    status: Optional[CodeableConcept] = None  # The status within the lifecycle of this product record. A high-level status, this is not intended...
    statusDate: Optional[str] = None  # The date at which the given status became applicable.
    description: Optional[str] = None  # General description of this product.
    combinedPharmaceuticalDoseForm: Optional[CodeableConcept] = None  # The dose form for a single part product, or combined form of a multiple part product. This is one...
    route: Optional[List[CodeableConcept]] = field(default_factory=list)  # The path by which the product is taken into or makes contact with the body. In some regions this ...
    indication: Optional[str] = None  # Description of indication(s) for this product, used when structured indications are not required....
    legalStatusOfSupply: Optional[CodeableConcept] = None  # The legal status of supply of the medicinal product as classified by the regulator.
    additionalMonitoringIndicator: Optional[CodeableConcept] = None  # Whether the Medicinal Product is subject to additional monitoring for regulatory reasons, such as...
    specialMeasures: Optional[List[CodeableConcept]] = field(default_factory=list)  # Whether the Medicinal Product is subject to special measures for regulatory reasons, such as a re...
    pediatricUseIndicator: Optional[CodeableConcept] = None  # If authorised for use in children, or infants, neonates etc.
    classification: Optional[List[CodeableConcept]] = field(default_factory=list)  # Allows the product to be classified by various systems, commonly WHO ATC.
    marketingStatus: Optional[List[Any]] = field(default_factory=list)  # Marketing status of the medicinal product, in contrast to marketing authorization. This refers to...
    packagedMedicinalProduct: Optional[List[CodeableConcept]] = field(default_factory=list)  # Package type for the product. See also the PackagedProductDefinition resource.
    comprisedOf: Optional[List[Reference]] = field(default_factory=list)  # Types of medicinal manufactured items and/or devices that this product consists of, such as table...
    ingredient: Optional[List[CodeableConcept]] = field(default_factory=list)  # The ingredients of this medicinal product - when not detailed in other resources. This is only ne...
    impurity: Optional[List[Any]] = field(default_factory=list)  # Any component of the drug product which is not the chemical entity defined as the drug substance,...
    attachedDocument: Optional[List[Reference]] = field(default_factory=list)  # Additional information or supporting documentation about the medicinal product.
    masterFile: Optional[List[Reference]] = field(default_factory=list)  # A master file for the medicinal product (e.g. Pharmacovigilance System Master File). Drug master ...
    contact: Optional[List[BackboneElement]] = field(default_factory=list)  # A product specific contact, person (in a role), or an organization.
    clinicalTrial: Optional[List[Reference]] = field(default_factory=list)  # Clinical trials or studies that this product is involved in.
    code: Optional[List[Coding]] = field(default_factory=list)  # A code that this product is known by, usually within some formal terminology, perhaps assigned by...
    crossReference: Optional[List[BackboneElement]] = field(default_factory=list)  # Reference to another product, e.g. for linking authorised to investigational product, or a virtua...
    operation: Optional[List[BackboneElement]] = field(default_factory=list)  # A manufacturing or administrative process or step associated with (or performed on) the medicinal...
    characteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # Allows the key product features to be recorded, such as \"sugar free\", \"modified release\", \"p...