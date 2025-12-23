# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DeviceMetric resource.

DeviceMetric represents measurements, simple or complex, made by a device.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Timing
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class DeviceMetricCalibration:
    """
    FHIR DeviceMetric.calibration complex type.
    
    Describes the calibrations that have been performed or that are required to be performed.
    """
    
    type: Optional[str] = None  # unspecified | offset | gain | two-point
    state: Optional[str] = None  # not-calibrated | calibration-required | calibrated | unspecified
    time: Optional[str] = None  # Describes the time last calibration has been performed
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DeviceMetric(DomainResource):
    """
    FHIR R4 DeviceMetric resource.
    
    Represents measurements, simple or complex, made by a device.
    Extends DomainResource.
    """
    
    resourceType: str = "DeviceMetric"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Instance identifier
    # Type
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[CodeableConcept] = None  # Identity of metric, for example Heart Rate or PEEP Setting (required)
    # Unit
    unit: Optional[CodeableConcept] = None  # Unit of Measure for the Metric
    # Device
    # Note: device is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce device is provided.
    device: Optional[Reference] = None  # Describes the link to the Device (required)
    # Operational Status
    operationalStatus: Optional[str] = None  # on | off | standby | entered-in-error
    # Color
    color: Optional[str] = None  # black | red | green | yellow | blue | magenta | cyan | white
    # Category
    # Note: category is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce category is provided.
    category: Optional[str] = None  # measurement | setting | calculation | unspecified (required)
    # Measurement Frequency
    measurementFrequency: Optional[Timing] = None  # Indicates how often the metric is taken or recorded
    # Calibration
    calibration: List[DeviceMetricCalibration] = field(default_factory=list)  # Describes the calibrations that have been performed or that are required to be performed

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


