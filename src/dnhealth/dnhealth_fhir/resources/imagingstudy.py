# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ImagingStudy resource.

ImagingStudy represents a set of images produced in a study.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, Reference, CodeableConcept, Annotation, Coding
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ImagingStudySeriesPerformer:
    """
    FHIR ImagingStudy.series.performer complex type.
    
    Who performed the series.
    """
    
    function: Optional[CodeableConcept] = None  # Type of performance
    actor: Reference  # Who performed the series (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImagingStudySeriesInstance:
    """
    FHIR ImagingStudy.series.instance complex type.
    
    A single SOP instance within the series.
    """
    
    uid: str  # DICOM SOP Instance UID (required)
    sopClass: Coding  # DICOM class type (required)
    number: Optional[int] = None  # The number of this instance in the series
    title: Optional[str] = None  # Description of instance
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImagingStudySeries:
    """
    FHIR ImagingStudy.series complex type.
    
    Each series has one or more instances of the study.
    """
    
    uid: str  # DICOM Series Instance UID for the series (required)
    number: Optional[int] = None  # Numeric identifier of this series
    modality: Coding  # The modality used for this series (required)
    description: Optional[str] = None  # A human-friendly description of the series
    numberOfInstances: Optional[int] = None  # Number of Series Related Instances
    endpoint: List[Reference] = field(default_factory=list)  # Series access endpoint
    bodySite: Optional[Coding] = None  # Body part examined
    laterality: Optional[Coding] = None  # Body part laterality
    specimen: List[Reference] = field(default_factory=list)  # Specimen imaged
    started: Optional[str] = None  # When the series started
    performer: List[ImagingStudySeriesPerformer] = field(default_factory=list)  # Who performed the series
    instance: List[ImagingStudySeriesInstance] = field(default_factory=list)  # A single SOP instance within the series
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImagingStudy(DomainResource):
    """
    FHIR R4 ImagingStudy resource.
    
    Represents a set of images produced in a study.
    Extends DomainResource.
    """
    
    resourceType: str = "ImagingStudy"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Identifiers for the whole study
    # Status
    status: str  # registered | available | cancelled | entered-in-error | unknown (required)
    # Modality
    modality: List[Coding] = field(default_factory=list)  # All series modality if actual acquisition modalities
    # Subject
    subject: Reference  # Who or what is the subject of the imaging study (required)
    # Encounter
    encounter: Optional[Reference] = None  # Encounter with which this imaging study is associated
    # Started
    started: Optional[str] = None  # When the study was started
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # Request fulfilled
    # Referrer
    referrer: Optional[Reference] = None  # Referring physician
    # Interpreter
    interpreter: List[Reference] = field(default_factory=list)  # Who interpreted images
    # Endpoint
    endpoint: List[Reference] = field(default_factory=list)  # Study access endpoint
    # Number Of Series
    numberOfSeries: Optional[int] = None  # Number of Study Related Series
    # Number Of Instances
    numberOfInstances: Optional[int] = None  # Number of Study Related Instances
    # Procedure Reference
    procedureReference: Optional[Reference] = None  # The procedure which triggered this imaging study
    # Procedure Code
    procedureCode: List[CodeableConcept] = field(default_factory=list)  # The procedure which triggered this imaging study
    # Location
    location: Optional[Reference] = None  # Where the study was performed
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why the study was requested
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why the study was requested
    # Note
    note: List[Annotation] = field(default_factory=list)  # User-defined comments
    # Description
    description: Optional[str] = None  # Institution-generated description
    # Series
    series: List[ImagingStudySeries] = field(default_factory=list)  # Each series has one or more instances of the study

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


