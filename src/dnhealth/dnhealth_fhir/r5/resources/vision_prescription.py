# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 VisionPrescription resource.

An authorization for the provision of glasses and/or contact lenses to a patient.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import List, Optional

@dataclass
class VisionPrescriptionLensSpecification:
    """
    VisionPrescriptionLensSpecification nested class.
    """

    product: Optional[CodeableConcept] = None  # Identifies the type of vision correction product which is required for the patient.
    eye: Optional[str] = None  # The eye for which the lens specification applies.
    amount: Optional[float] = None  # Amount of prism to compensate for eye alignment in fractional units.
    base: Optional[str] = None  # The relative base, or reference lens edge, for the prism.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    sphere: Optional[float] = None  # Lens power measured in dioptres (0.25 units).
    cylinder: Optional[float] = None  # Power adjustment for astigmatism measured in dioptres (0.25 units).
    axis: Optional[int] = None  # Adjustment for astigmatism measured in integer degrees.
    prism: Optional[List[BackboneElement]] = field(default_factory=list)  # Allows for adjustment on two axis.
    add: Optional[float] = None  # Power adjustment for multifocal lenses measured in dioptres (0.25 units).
    power: Optional[float] = None  # Contact lens power measured in dioptres (0.25 units).
    backCurve: Optional[float] = None  # Back curvature measured in millimetres.
    diameter: Optional[float] = None  # Contact lens diameter measured in millimetres.
    duration: Optional[Quantity] = None  # The recommended maximum wear period for the lens.
    color: Optional[str] = None  # Special color or pattern.
    brand: Optional[str] = None  # Brand recommendations or restrictions.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Notes for special requirements such as coatings and lens materials.

@dataclass
class VisionPrescriptionLensSpecificationPrism:
    """
    VisionPrescriptionLensSpecificationPrism nested class.
    """

    amount: Optional[float] = None  # Amount of prism to compensate for eye alignment in fractional units.
    base: Optional[str] = None  # The relative base, or reference lens edge, for the prism.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class VisionPrescription(FHIRResource):
    """
    An authorization for the provision of glasses and/or contact lenses to a patient.
    """

    status: Optional[str] = None  # The status of the resource instance.
    created: Optional[str] = None  # The date this resource was created.
    patient: Optional[Reference] = None  # A resource reference to the person to whom the vision prescription applies.
    dateWritten: Optional[str] = None  # The date (and perhaps time) when the prescription was written.
    prescriber: Optional[Reference] = None  # The healthcare professional responsible for authorizing the prescription.
    lensSpecification: List[BackboneElement] = field(default_factory=list)  # Contain the details of  the individual lens specifications and serves as the authorization for th...
    resourceType: str = "VisionPrescription"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this vision prescription.
    encounter: Optional[Reference] = None  # A reference to a resource that identifies the particular occurrence of contact between patient an...