# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SpecimenDefinition resource.

A kind of specimen with associated set of requirements.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Duration, Extension, Identifier, Period, Quantity, Range, Reference, UsageContext
from typing import Any, List, Optional

@dataclass
class SpecimenDefinitionTypeTested:
    """
    SpecimenDefinitionTypeTested nested class.
    """

    preference: Optional[str] = None  # The preference for this type of conditioned specimen.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    isDerived: Optional[bool] = None  # Primary of secondary specimen.
    type: Optional[CodeableConcept] = None  # The kind of specimen conditioned for testing expected by lab.
    container: Optional[BackboneElement] = None  # The specimen's container.
    material: Optional[CodeableConcept] = None  # The type of material of the container.
    cap: Optional[CodeableConcept] = None  # Color of container cap.
    description: Optional[str] = None  # The textual description of the kind of container.
    capacity: Optional[Quantity] = None  # The capacity (volume or other measure) of this kind of container.
    minimumVolume: Optional[Any] = None  # The minimum volume to be conditioned in the container.
    additive: Optional[List[BackboneElement]] = field(default_factory=list)  # Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Exam...
    preparation: Optional[str] = None  # Special processing that should be applied to the container for this kind of specimen.
    requirement: Optional[str] = None  # Requirements for delivery and special handling of this kind of conditioned specimen.
    retentionTime: Optional[Duration] = None  # The usual time that a specimen of this kind is retained after the ordered tests are completed, fo...
    singleUse: Optional[bool] = None  # Specimen can be used by only one test or panel if the value is \"true\".
    rejectionCriterion: Optional[List[CodeableConcept]] = field(default_factory=list)  # Criterion for rejection of the specimen in its container by the laboratory.
    handling: Optional[List[BackboneElement]] = field(default_factory=list)  # Set of instructions for preservation/transport of the specimen at a defined temperature interval,...
    temperatureQualifier: Optional[CodeableConcept] = None  # It qualifies the interval of temperature, which characterizes an occurrence of handling. Conditio...
    temperatureRange: Optional[Range] = None  # The temperature interval for this set of handling instructions.
    maxDuration: Optional[Duration] = None  # The maximum time interval of preservation of the specimen with these conditions.
    instruction: Optional[str] = None  # Additional textual instructions for the preservation or transport of the specimen. For instance, ...
    testingDestination: Optional[List[CodeableConcept]] = field(default_factory=list)  # Where the specimen will be tested: e.g., lab, sector, device or any combination of these.

@dataclass
class SpecimenDefinitionTypeTestedContainer:
    """
    SpecimenDefinitionTypeTestedContainer nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    material: Optional[CodeableConcept] = None  # The type of material of the container.
    type: Optional[CodeableConcept] = None  # The type of container used to contain this kind of specimen.
    cap: Optional[CodeableConcept] = None  # Color of container cap.
    description: Optional[str] = None  # The textual description of the kind of container.
    capacity: Optional[Quantity] = None  # The capacity (volume or other measure) of this kind of container.
    minimumVolume: Optional[Any] = None  # The minimum volume to be conditioned in the container.
    additive: Optional[List[BackboneElement]] = field(default_factory=list)  # Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Exam...
    preparation: Optional[str] = None  # Special processing that should be applied to the container for this kind of specimen.

@dataclass
class SpecimenDefinitionTypeTestedContainerAdditive:
    """
    SpecimenDefinitionTypeTestedContainerAdditive nested class.
    """

    additive: Optional[Any] = None  # Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Exam...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class SpecimenDefinitionTypeTestedHandling:
    """
    SpecimenDefinitionTypeTestedHandling nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    temperatureQualifier: Optional[CodeableConcept] = None  # It qualifies the interval of temperature, which characterizes an occurrence of handling. Conditio...
    temperatureRange: Optional[Range] = None  # The temperature interval for this set of handling instructions.
    maxDuration: Optional[Duration] = None  # The maximum time interval of preservation of the specimen with these conditions.
    instruction: Optional[str] = None  # Additional textual instructions for the preservation or transport of the specimen. For instance, ...


@dataclass
class SpecimenDefinition(FHIRResource):
    """
    A kind of specimen with associated set of requirements.
    """

    status: Optional[str] = None  # The current state of theSpecimenDefinition.
    resourceType: str = "SpecimenDefinition"
    url: Optional[str] = None  # An absolute URL that is used to identify this SpecimenDefinition when it is referenced in a speci...
    identifier: Optional[Identifier] = None  # A business identifier assigned to this SpecimenDefinition.
    version: Optional[str] = None  # The identifier that is used to identify this version of the SpecimenDefinition when it is referen...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the {{title}}. This name should be usable as an identifier fo...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the SpecimenDefinition.
    derivedFromCanonical: Optional[List[str]] = field(default_factory=list)  # The canonical URL pointing to another FHIR-defined SpecimenDefinition that is adhered to in whole...
    derivedFromUri: Optional[List[str]] = field(default_factory=list)  # The URL pointing to an externally-defined type of specimen, guideline or other definition that is...
    experimental: Optional[bool] = None  # A flag to indicate that this SpecimenDefinition is not authored for  genuine usage.
    subject: Optional[Any] = None  # A code or group definition that describes the intended subject  from which this kind of specimen ...
    date: Optional[str] = None  # For draft definitions, indicates the date of initial creation. For active definitions, represents...
    publisher: Optional[str] = None  # Helps establish the \"authority/credibility\" of the SpecimenDefinition. May also allow for contact.
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the SpecimenDefinition from the consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A jurisdiction in which the SpecimenDefinition is intended to be used.
    purpose: Optional[str] = None  # Explains why this SpecimeDefinition is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # Copyright statement relating to the SpecimenDefinition and/or its contents. Copyright statements ...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    approvalDate: Optional[str] = None  # The date on which the asset content was approved by the publisher. Approval happens once when the...
    lastReviewDate: Optional[str] = None  # The date on which the asset content was last reviewed. Review happens periodically after that, bu...
    effectivePeriod: Optional[Period] = None  # The period during which the SpecimenDefinition content was or is planned to be effective.
    typeCollected: Optional[CodeableConcept] = None  # The kind of material to be collected.
    patientPreparation: Optional[List[CodeableConcept]] = field(default_factory=list)  # Preparation of the patient for specimen collection.
    timeAspect: Optional[str] = None  # Time aspect of specimen collection (duration or offset).
    collection: Optional[List[CodeableConcept]] = field(default_factory=list)  # The action to be performed for collecting the specimen.
    typeTested: Optional[List[BackboneElement]] = field(default_factory=list)  # Specimen conditioned in a container as expected by the testing laboratory.