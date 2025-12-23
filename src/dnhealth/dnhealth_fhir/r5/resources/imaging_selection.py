# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ImagingSelection resource.

A selection of DICOM SOP instances and/or frames within a single Study and Series. This might include additional specifics such as an image region, an Observation UID or a Segmentation Number, allowing linkage to an Observation Resource or transferring this information along with the ImagingStudy Resource.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class ImagingSelectionPerformer:
    """
    ImagingSelectionPerformer nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the performer.
    actor: Optional[Reference] = None  # Author – human or machine.

@dataclass
class ImagingSelectionInstance:
    """
    ImagingSelectionInstance nested class.
    """

    uid: Optional[str] = None  # The SOP Instance UID for the selected DICOM instance.
    regionType: Optional[str] = None  # Specifies the type of image region.
    coordinate: List[float] = field(default_factory=list)  # The coordinates describing the image region. Encoded as a set of (column, row) pairs that denote ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    number: Optional[int] = None  # The Instance Number for the selected DICOM instance.
    sopClass: Optional[Coding] = None  # The SOP Class UID for the selected DICOM instance.
    subset: Optional[List[str]] = field(default_factory=list)  # Selected subset of the SOP Instance. The content and format of the subset item is determined by t...
    imageRegion2D: Optional[List[BackboneElement]] = field(default_factory=list)  # Each imaging selection instance or frame list might includes an image region, specified by a regi...
    imageRegion3D: Optional[List[BackboneElement]] = field(default_factory=list)  # Each imaging selection might includes a 3D image region, specified by a region type and a set of ...

@dataclass
class ImagingSelectionInstanceImageRegion2D:
    """
    ImagingSelectionInstanceImageRegion2D nested class.
    """

    regionType: Optional[str] = None  # Specifies the type of image region.
    coordinate: List[float] = field(default_factory=list)  # The coordinates describing the image region. Encoded as a set of (column, row) pairs that denote ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ImagingSelectionInstanceImageRegion3D:
    """
    ImagingSelectionInstanceImageRegion3D nested class.
    """

    regionType: Optional[str] = None  # Specifies the type of image region.
    coordinate: List[float] = field(default_factory=list)  # The coordinates describing the image region. Encoded as an ordered set of (x,y,z) triplets (in mm...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class ImagingSelection(FHIRResource):
    """
    A selection of DICOM SOP instances and/or frames within a single Study and Series. This might include additional specifics such as an image region, an Observation UID or a Segmentation Number, allowing linkage to an Observation Resource or transferring this information along with the ImagingStudy Resource.
    """

    status: Optional[str] = None  # The current state of the ImagingSelection resource. This is not the status of any ImagingStudy, S...
    code: Optional[CodeableConcept] = None  # Reason for referencing the selected content.
    resourceType: str = "ImagingSelection"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this imaging selection.
    subject: Optional[Reference] = None  # The patient, or group of patients, location, device, organization, procedure or practitioner this...
    issued: Optional[str] = None  # The date and time this imaging selection was created.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Selector of the instances – human or machine.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A list of the diagnostic requests that resulted in this imaging selection being performed.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Classifies the imaging selection.
    studyUid: Optional[str] = None  # The Study Instance UID for the DICOM Study from which the images were selected.
    derivedFrom: Optional[List[Reference]] = field(default_factory=list)  # The imaging study from which the imaging selection is made.
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # The network service providing retrieval access to the selected images, frames, etc. See implement...
    seriesUid: Optional[str] = None  # The Series Instance UID for the DICOM Series from which the images were selected.
    seriesNumber: Optional[int] = None  # The Series Number for the DICOM Series from which the images were selected.
    frameOfReferenceUid: Optional[str] = None  # The Frame of Reference UID identifying the coordinate system that conveys spatial and/or temporal...
    bodySite: Optional[Any] = None  # The anatomic structures examined. See DICOM Part 16 Annex L (http://dicom.nema.org/medical/dicom/...
    focus: Optional[List[Reference]] = field(default_factory=list)  # The actual focus of an observation when it is not the patient of record representing something or...
    instance: Optional[List[BackboneElement]] = field(default_factory=list)  # Each imaging selection includes one or more selected DICOM SOP instances.