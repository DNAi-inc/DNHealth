# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductPackaged resource.

Complete MedicinalProductPackaged resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Quantity,
    Period,
    Attachment,
)


@dataclass
class MedicinalProductPackagedBatchIdentifier:
    """
    Batch numbering.
    """

    outerPackaging: Identifier  # A number appearing on the outer packaging of a specific batch (required)
    immediatePackaging: Optional[Identifier] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPackagedPackageItem:
    """
    A packaging item, as a contained for medicine, possibly with other packaging items within.
    """

    identifier: List[Identifier] = field(default_factory=list)
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[CodeableConcept] = None  # The physical type of the container of the medicine (required)
    # Note: quantity is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce quantity is provided.
    quantity: Optional[Quantity] = None  # The quantity of this package in the medicinal product (required)
    material: List[CodeableConcept] = field(default_factory=list)
    alternateMaterial: List[CodeableConcept] = field(default_factory=list)
    device: List[Reference] = field(default_factory=list)
    manufacturedItem: List[Reference] = field(default_factory=list)
    packageItem: List["MedicinalProductPackagedPackageItem"] = field(default_factory=list)
    physicalCharacteristics: Optional["MedicinalProductPackagedPhysicalCharacteristics"] = None
    shelfLifeStorage: List["MedicinalProductPackagedShelfLifeStorage"] = field(default_factory=list)
    manufacturer: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPackagedPhysicalCharacteristics:
    """
    Dimensions, color etc.
    """

    height: Optional[Quantity] = None
    width: Optional[Quantity] = None
    depth: Optional[Quantity] = None
    weight: Optional[Quantity] = None
    nominalVolume: Optional[Quantity] = None
    externalDiameter: Optional[Quantity] = None
    shape: Optional[str] = None
    color: List[str] = field(default_factory=list)
    imprint: List[str] = field(default_factory=list)
    image: List[Attachment] = field(default_factory=list)
    scoring: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPackagedShelfLifeStorage:
    """
    Shelf Life and storage information.
    """

    type: Optional[CodeableConcept] = None
    periodDuration: Optional[Period] = None
    periodString: Optional[str] = None
    specialPrecautionsForStorage: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPackaged(FHIRResource):
    """
    FHIR R4 MedicinalProductPackaged resource.

    A medicinal product in a container or package.
    """

    resourceType: str = "MedicinalProductPackaged"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Subject
    subject: List[Reference] = field(default_factory=list)
    # Description
    description: Optional[str] = None
    # Legal Status of Supply
    legalStatusOfSupply: Optional[CodeableConcept] = None
    # Marketing Status
    marketingStatus: List[Reference] = field(default_factory=list)
    # Marketing Authorization
    marketingAuthorization: Optional[Reference] = None
    # Manufacturer
    manufacturer: List[Reference] = field(default_factory=list)
    # Batch Identifier
    batchIdentifier: List[MedicinalProductPackagedBatchIdentifier] = field(default_factory=list)
    # Package Item
    packageItem: List[MedicinalProductPackagedPackageItem] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
