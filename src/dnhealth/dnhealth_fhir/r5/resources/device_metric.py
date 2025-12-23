# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DeviceMetric resource.

Describes a measurement, calculation or setting capability of a device.  The DeviceMetric resource is derived from the ISO/IEEE 11073-10201 Domain Information Model standard, but is more widely applicable.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import List, Optional

@dataclass
class DeviceMetricCalibration:
    """
    DeviceMetricCalibration nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[str] = None  # Describes the type of the calibration method.
    state: Optional[str] = None  # Describes the state of the calibration.
    time: Optional[str] = None  # Describes the time last calibration has been performed.


@dataclass
class DeviceMetric(FHIRResource):
    """
    Describes a measurement, calculation or setting capability of a device.  The DeviceMetric resource is derived from the ISO/IEEE 11073-10201 Domain Information Model standard, but is more widely applicable.
    """

    type: Optional[CodeableConcept] = None  # Describes the type of the metric. For example: Heart Rate, PEEP Setting, etc.
    device: Optional[Reference] = None  # Describes the link to the Device.  This is also known as a channel device.
    category: Optional[str] = None  # Indicates the category of the observation generation process. A DeviceMetric can be for example a...
    resourceType: str = "DeviceMetric"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Instance identifiers assigned to a device, by the device or gateway software, manufacturers, othe...
    unit: Optional[CodeableConcept] = None  # Describes the unit that an observed value determined for this metric will have. For example: Perc...
    operationalStatus: Optional[str] = None  # Indicates current operational state of the device. For example: On, Off, Standby, etc.
    color: Optional[str] = None  # The preferred color associated with the metric (e.g., display color). This is often used to aid c...
    measurementFrequency: Optional[Quantity] = None  # The frequency at which the metric is taken or recorded. Devices measure metrics at a wide range o...
    calibration: Optional[List[BackboneElement]] = field(default_factory=list)  # Describes the calibrations that have been performed or that are required to be performed.