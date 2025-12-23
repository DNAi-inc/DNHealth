# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 BodyStructure resource.

Record details about an anatomical structure.  This resource may be used when a coded concept does not provide the necessary detail needed for the use case.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class BodyStructureIncludedStructure:
    """
    BodyStructureIncludedStructure nested class.
    """

    structure: Optional[CodeableConcept] = None  # Code that represents the included structure.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    laterality: Optional[CodeableConcept] = None  # Code that represents the included structure laterality.
    bodyLandmarkOrientation: Optional[List[BackboneElement]] = field(default_factory=list)  # Body locations in relation to a specific body landmark (tatoo, scar, other body structure).
    landmarkDescription: Optional[List[CodeableConcept]] = field(default_factory=list)  # A description of a landmark on the body used as a reference to locate something else.
    clockFacePosition: Optional[List[CodeableConcept]] = field(default_factory=list)  # An description of the direction away from a landmark something is located based on a radial clock...
    distanceFromLandmark: Optional[List[BackboneElement]] = field(default_factory=list)  # The distance in centimeters a certain observation is made from a body landmark.
    device: Optional[List[Any]] = field(default_factory=list)  # An instrument, tool, analyzer, etc. used in the measurement.
    value: Optional[List[Quantity]] = field(default_factory=list)  # The measured distance (e.g., in cm) from a body landmark.
    surfaceOrientation: Optional[List[CodeableConcept]] = field(default_factory=list)  # The surface area a body location is in relation to a landmark.
    spatialReference: Optional[List[Reference]] = field(default_factory=list)  # XY or XYZ-coordinate orientation for structure.
    qualifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Code that represents the included structure qualifier.

@dataclass
class BodyStructureIncludedStructureBodyLandmarkOrientation:
    """
    BodyStructureIncludedStructureBodyLandmarkOrientation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    landmarkDescription: Optional[List[CodeableConcept]] = field(default_factory=list)  # A description of a landmark on the body used as a reference to locate something else.
    clockFacePosition: Optional[List[CodeableConcept]] = field(default_factory=list)  # An description of the direction away from a landmark something is located based on a radial clock...
    distanceFromLandmark: Optional[List[BackboneElement]] = field(default_factory=list)  # The distance in centimeters a certain observation is made from a body landmark.
    device: Optional[List[Any]] = field(default_factory=list)  # An instrument, tool, analyzer, etc. used in the measurement.
    value: Optional[List[Quantity]] = field(default_factory=list)  # The measured distance (e.g., in cm) from a body landmark.
    surfaceOrientation: Optional[List[CodeableConcept]] = field(default_factory=list)  # The surface area a body location is in relation to a landmark.

@dataclass
class BodyStructureIncludedStructureBodyLandmarkOrientationDistanceFromLandmark:
    """
    BodyStructureIncludedStructureBodyLandmarkOrientationDistanceFromLandmark nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    device: Optional[List[Any]] = field(default_factory=list)  # An instrument, tool, analyzer, etc. used in the measurement.
    value: Optional[List[Quantity]] = field(default_factory=list)  # The measured distance (e.g., in cm) from a body landmark.


@dataclass
class BodyStructure(FHIRResource):
    """
    Record details about an anatomical structure.  This resource may be used when a coded concept does not provide the necessary detail needed for the use case.
    """

    includedStructure: List[BackboneElement] = field(default_factory=list)  # The anatomical location(s) or region(s) of the specimen, lesion, or body structure.
    patient: Optional[Reference] = None  # The person to which the body site belongs.
    resourceType: str = "BodyStructure"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for this instance of the anatomical structure.
    active: Optional[bool] = None  # Whether this body site is in active use.
    morphology: Optional[CodeableConcept] = None  # The kind of structure being represented by the body structure at `BodyStructure.location`.  This ...
    excludedStructure: Optional[List[Any]] = field(default_factory=list)  # The anatomical location(s) or region(s) not occupied or represented by the specimen, lesion, or b...
    description: Optional[str] = None  # A summary, characterization or explanation of the body structure.
    image: Optional[List[Attachment]] = field(default_factory=list)  # Image or images used to identify a location.