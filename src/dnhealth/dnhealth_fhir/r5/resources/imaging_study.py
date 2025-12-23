# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ImagingStudy resource.

Representation of the content produced in a DICOM imaging study. A study comprises a set of series, each of which includes a set of Service-Object Pair Instances (SOP Instances - images or other data) acquired or produced in a common context.  A series is of only one modality (e.g. X-ray, CT, MR, ultrasound), but a study may have multiple series of different modalities.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class ImagingStudySeries:
    """
    ImagingStudySeries nested class.
    """

    uid: Optional[str] = None  # The DICOM Series Instance UID for the series.
    modality: Optional[CodeableConcept] = None  # The distinct modality for this series. This may include both acquisition and non-acquisition moda...
    actor: Optional[Reference] = None  # Indicates who or what performed the series.
    sopClass: Optional[Coding] = None  # DICOM instance  type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    number: Optional[int] = None  # The numeric identifier of this series in the study.
    description: Optional[str] = None  # A description of the series.
    numberOfInstances: Optional[int] = None  # Number of SOP Instances in the Study. The value given may be larger than the number of instance e...
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # The network service providing access (e.g., query, view, or retrieval) for this series. See imple...
    bodySite: Optional[Any] = None  # The anatomic structures examined. See DICOM Part 16 Annex L (http://dicom.nema.org/medical/dicom/...
    laterality: Optional[CodeableConcept] = None  # The laterality of the (possibly paired) anatomic structures examined. E.g., the left knee, both l...
    specimen: Optional[List[Reference]] = field(default_factory=list)  # The specimen imaged, e.g., for whole slide imaging of a biopsy.
    started: Optional[str] = None  # The date and time the series was started.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what performed the series and how they were involved.
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the performer in the series.
    instance: Optional[List[BackboneElement]] = field(default_factory=list)  # A single SOP instance within the series, e.g. an image, or presentation state.
    title: Optional[str] = None  # The description of the instance.

@dataclass
class ImagingStudySeriesPerformer:
    """
    ImagingStudySeriesPerformer nested class.
    """

    actor: Optional[Reference] = None  # Indicates who or what performed the series.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the performer in the series.

@dataclass
class ImagingStudySeriesInstance:
    """
    ImagingStudySeriesInstance nested class.
    """

    uid: Optional[str] = None  # The DICOM SOP Instance UID for this image or other DICOM content.
    sopClass: Optional[Coding] = None  # DICOM instance  type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    number: Optional[int] = None  # The number of instance in the series.
    title: Optional[str] = None  # The description of the instance.


@dataclass
class ImagingStudy(FHIRResource):
    """
    Representation of the content produced in a DICOM imaging study. A study comprises a set of series, each of which includes a set of Service-Object Pair Instances (SOP Instances - images or other data) acquired or produced in a common context.  A series is of only one modality (e.g. X-ray, CT, MR, ultrasound), but a study may have multiple series of different modalities.
    """

    status: Optional[str] = None  # The current state of the ImagingStudy resource. This is not the status of any ServiceRequest or T...
    subject: Optional[Reference] = None  # The subject, typically a patient, of the imaging study.
    resourceType: str = "ImagingStudy"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers for the ImagingStudy such as DICOM Study Instance UID.
    modality: Optional[List[CodeableConcept]] = field(default_factory=list)  # A list of all the distinct values of series.modality. This may include both acquisition and non-a...
    encounter: Optional[Reference] = None  # The healthcare event (e.g. a patient and healthcare provider interaction) during which this Imagi...
    started: Optional[str] = None  # Date and time the study started.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A list of the diagnostic requests that resulted in this imaging study being performed.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular ImagingStudy is a component or step.  For example,  an Im...
    referrer: Optional[Reference] = None  # The requesting/referring physician.
    endpoint: Optional[List[Reference]] = field(default_factory=list)  # The network service providing access (e.g., query, view, or retrieval) for the study. See impleme...
    numberOfSeries: Optional[int] = None  # Number of Series in the Study. This value given may be larger than the number of series elements ...
    numberOfInstances: Optional[int] = None  # Number of SOP Instances in Study. This value given may be larger than the number of instance elem...
    procedure: Optional[List[Any]] = field(default_factory=list)  # This field corresponds to the DICOM Procedure Code Sequence (0008,1032). This is different from t...
    location: Optional[Reference] = None  # The principal physical location where the ImagingStudy was performed.
    reason: Optional[List[Any]] = field(default_factory=list)  # Description of clinical condition indicating why the ImagingStudy was requested, and/or Indicates...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Per the recommended DICOM mapping, this element is derived from the Study Description attribute (...
    description: Optional[str] = None  # The Imaging Manager description of the study. Institution-generated description or classification...
    series: Optional[List[BackboneElement]] = field(default_factory=list)  # Each study has one or more series of images or other content.