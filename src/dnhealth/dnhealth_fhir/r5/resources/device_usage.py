# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DeviceUsage resource.

A record of a device being used by a patient where the record is the result of a report from the patient or a clinician.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference, Timing
from typing import Any, List, Optional

@dataclass
class DeviceUsageAdherence:
    """
    DeviceUsageAdherence nested class.
    """

    code: Optional[CodeableConcept] = None  # Type of adherence.
    reason: List[CodeableConcept] = field(default_factory=list)  # Reason for adherence type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class DeviceUsage(FHIRResource):
    """
    A record of a device being used by a patient where the record is the result of a report from the patient or a clinician.
    """

    status: Optional[str] = None  # A code representing the patient or other source's judgment about the state of the device used tha...
    patient: Optional[Reference] = None  # The patient who used the device.
    device: Optional[Any] = None  # Code or Reference to device used.
    resourceType: str = "DeviceUsage"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # An external identifier for this statement such as an IRI.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan, proposal or order that is fulfilled in whole or in part by this DeviceUsage.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # This attribute indicates a category for the statement - The device statement may be made in an in...
    derivedFrom: Optional[List[Reference]] = field(default_factory=list)  # Allows linking the DeviceUsage to the underlying Request, or to other information that supports o...
    context: Optional[Reference] = None  # The encounter or episode of care that establishes the context for this device use statement.
    timing: Optional[Any] = None  # How often the device was used.
    dateAsserted: Optional[str] = None  # The time at which the statement was recorded by informationSource.
    usageStatus: Optional[CodeableConcept] = None  # The status of the device usage, for example always, sometimes, never. This is not the same as the...
    usageReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reason for asserting the usage status - for example forgot, lost, stolen, broken.
    adherence: Optional[BackboneElement] = None  # This indicates how or if the device is being used.
    informationSource: Optional[Reference] = None  # Who reported the device was being used by the patient.
    reason: Optional[List[Any]] = field(default_factory=list)  # Reason or justification for the use of the device. A coded concept, or another resource whose exi...
    bodySite: Optional[Any] = None  # Indicates the anotomic location on the subject's body where the device was used ( i.e. the target).
    note: Optional[List[Annotation]] = field(default_factory=list)  # Details about the device statement that were not represented at all or sufficiently in one of the...