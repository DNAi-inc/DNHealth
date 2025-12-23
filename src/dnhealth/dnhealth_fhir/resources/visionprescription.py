# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 VisionPrescription resource.

VisionPrescription represents an authorization for the provision of glasses and/or contact lenses.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Annotation,
)


logger = logging.getLogger(__name__)


@dataclass
class VisionPrescriptionLensSpecification:
    """
    FHIR VisionPrescription.lensSpecification complex type.
    
    Contain the details of the individual lens specifications for both eyes.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: product is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce product is provided.
    product: Optional[CodeableConcept] = None  # Product to be supplied (required)
    # Note: eye is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce eye is provided.
    eye: Optional[str] = None  # right | left (required)
    sphere: Optional[float] = None  # Power of the lens
    cylinder: Optional[float] = None  # Lens power for astigmatism
    axis: Optional[int] = None  # Lens meridian which contain no power for astigmatism
    prism: List["VisionPrescriptionLensSpecificationPrism"] = field(default_factory=list)  # Eye alignment compensation
    add: Optional[float] = None  # Added power for multifocal levels
    power: Optional[float] = None  # Contact lens power
    backCurve: Optional[float] = None  # Contact lens back curvature
    diameter: Optional[float] = None  # Contact lens diameter
    duration: Optional[Any] = None  # Lens wear duration (Quantity)
    color: Optional[str] = None  # Color required
    brand: Optional[str] = None  # Brand required
    note: List[Annotation] = field(default_factory=list)  # Notes for coatings


@dataclass
class VisionPrescriptionLensSpecificationPrism:
    """
    FHIR VisionPrescription.lensSpecification.prism complex type.
    
    Eye alignment compensation.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: amount is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce amount is provided.
    amount: Optional[float] = None  # Amount of adjustment (required)
    # Note: base is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce base is provided.
    base: Optional[str] = None  # up | down | in | out (required)


@dataclass
class VisionPrescription(DomainResource):
    """
    FHIR R4 VisionPrescription resource.
    
    Represents an authorization for the provision of glasses and/or contact lenses.
    Extends DomainResource.
    """
    
    resourceType: str = "VisionPrescription"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for vision prescription
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (DomainResource has modifierExtension with default).
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | cancelled | draft | entered-in-error (required in FHIR)
    # Created
    # Note: created is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce created is provided.
    created: Optional[str] = None  # Response creation date (required)
    # Patient
    # Note: patient is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce patient is provided.
    patient: Optional[Reference] = None  # Who prescription is for (required)
    # Encounter
    encounter: Optional[Reference] = None  # Created during encounter / admission / stay
    # Date Written
    # Note: dateWritten is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce dateWritten is provided.
    dateWritten: Optional[str] = None  # When prescription was written (required)
    # Prescriber
    # Note: prescriber is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce prescriber is provided.
    prescriber: Optional[Reference] = None  # Who authorized the vision prescription (required)
    # Lens Specification
    lensSpecification: List[VisionPrescriptionLensSpecification] = field(default_factory=list)  # Vision lens authorization (required)

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

