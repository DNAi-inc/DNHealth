# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Specimen resource.

A sample to be used for analysis.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Duration, Extension, Identifier, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class SpecimenFeature:
    """
    SpecimenFeature nested class.
    """

    type: Optional[CodeableConcept] = None  # The landmark or feature being highlighted.
    description: Optional[str] = None  # Description of the feature of the specimen.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class SpecimenCollection:
    """
    SpecimenCollection nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    collector: Optional[Reference] = None  # Person who collected the specimen.
    collected: Optional[Any] = None  # Time when specimen was collected from subject - the physiologically relevant time.
    duration: Optional[Duration] = None  # The span of time over which the collection of a specimen occurred.
    quantity: Optional[Quantity] = None  # The quantity of specimen collected; for instance the volume of a blood sample, or the physical me...
    method: Optional[CodeableConcept] = None  # A coded value specifying the technique that is used to perform the procedure.
    device: Optional[Any] = None  # A coded value specifying the technique that is used to perform the procedure.
    procedure: Optional[Reference] = None  # The procedure event during which the specimen was collected (e.g. the surgery leading to the coll...
    bodySite: Optional[Any] = None  # Anatomical location from which the specimen was collected (if subject is a patient). This is the ...
    fastingStatus: Optional[Any] = None  # Abstinence or reduction from some or all food, drink, or both, for a period of time prior to samp...

@dataclass
class SpecimenProcessing:
    """
    SpecimenProcessing nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Textual description of procedure.
    method: Optional[CodeableConcept] = None  # A coded value specifying the method used to process the specimen.
    additive: Optional[List[Reference]] = field(default_factory=list)  # Material used in the processing step.
    time: Optional[Any] = None  # A record of the time or period when the specimen processing occurred.  For example the time of sa...

@dataclass
class SpecimenContainer:
    """
    SpecimenContainer nested class.
    """

    device: Optional[Reference] = None  # The device resource for the the container holding the specimen. If the container is in a holder t...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    location: Optional[Reference] = None  # The location of the container holding the specimen.
    specimenQuantity: Optional[Quantity] = None  # The quantity of specimen in the container; may be volume, dimensions, or other appropriate measur...


@dataclass
class Specimen(FHIRResource):
    """
    A sample to be used for analysis.
    """

    resourceType: str = "Specimen"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Id for specimen.
    accessionIdentifier: Optional[Identifier] = None  # The identifier assigned by the lab when accessioning specimen(s). This is not necessarily the sam...
    status: Optional[str] = None  # The availability of the specimen.
    type: Optional[CodeableConcept] = None  # The kind of material that forms the specimen.
    subject: Optional[Reference] = None  # Where the specimen came from. This may be from patient(s), from a location (e.g., the source of a...
    receivedTime: Optional[str] = None  # Time when specimen is received by the testing laboratory for processing or testing.
    parent: Optional[List[Reference]] = field(default_factory=list)  # Reference to the parent (source) specimen which is used when the specimen was either derived from...
    request: Optional[List[Reference]] = field(default_factory=list)  # Details concerning a service request that required a specimen to be collected.
    combined: Optional[str] = None  # This element signifies if the specimen is part of a group or pooled.
    role: Optional[List[CodeableConcept]] = field(default_factory=list)  # The role or reason for the specimen in the testing workflow.
    feature: Optional[List[BackboneElement]] = field(default_factory=list)  # A physical feature or landmark on a specimen, highlighted for context by the collector of the spe...
    collection: Optional[BackboneElement] = None  # Details concerning the specimen collection.
    processing: Optional[List[BackboneElement]] = field(default_factory=list)  # Details concerning processing and processing steps for the specimen.
    container: Optional[List[BackboneElement]] = field(default_factory=list)  # The container holding the specimen.  The recursive nature of containers; i.e. blood in tube in tr...
    condition: Optional[List[CodeableConcept]] = field(default_factory=list)  # A mode or state of being that describes the nature of the specimen.
    note: Optional[List[Annotation]] = field(default_factory=list)  # To communicate any details or issues about the specimen or during the specimen collection. (for e...