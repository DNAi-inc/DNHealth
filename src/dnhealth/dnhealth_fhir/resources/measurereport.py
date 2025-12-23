# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MeasureReport resource.

MeasureReport contains the results of evaluating a measure.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
)


@dataclass
class MeasureReportGroup:
    """
    FHIR MeasureReport.group complex type.
    
    Results of the measure calculation for a group.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # Meaning of the group
    population: List["MeasureReportGroupPopulation"] = field(default_factory=list)  # Population results
    measureScore: Optional[Any] = None  # What score this group achieved (Quantity)
    stratifier: List["MeasureReportGroupStratifier"] = field(default_factory=list)  # Stratification results


@dataclass
class MeasureReportGroupPopulation:
    """
    FHIR MeasureReport.group.population complex type.
    
    Population results for a specific population.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # initial-population | numerator | numerator-exclusion | denominator | denominator-exclusion | denominator-exception | measure-population | measure-population-exclusion | measure-observation
    count: Optional[int] = None  # Size of the population
    subjectResults: Optional[Reference] = None  # For subject-list reports, the subject results in this population


@dataclass
class MeasureReportGroupStratifier:
    """
    FHIR MeasureReport.group.stratifier complex type.
    
    Stratification results.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: List[CodeableConcept] = field(default_factory=list)  # What stratifier of the group
    stratum: List["MeasureReportGroupStratifierStratum"] = field(default_factory=list)  # Stratum results


@dataclass
class MeasureReportGroupStratifierStratum:
    """
    FHIR MeasureReport.group.stratifier.stratum complex type.
    
    Stratum results.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    value: Optional[CodeableConcept] = None  # The stratum value
    component: List["MeasureReportGroupStratifierStratumComponent"] = field(default_factory=list)  # Stratifier component values
    population: List["MeasureReportGroupPopulation"] = field(default_factory=list)  # Population results in this stratum
    measureScore: Optional[Any] = None  # What score this stratum achieved (Quantity)


@dataclass
class MeasureReportGroupStratifierStratumComponent:
    """
    FHIR MeasureReport.group.stratifier.stratum.component complex type.
    
    Stratifier component values.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # What stratifier component of the group
    value: Optional[CodeableConcept] = None  # The stratum component value


@dataclass
class MeasureReport(DomainResource):
    """
    FHIR R4 MeasureReport resource.
    
    Contains the results of evaluating a measure.
    Extends DomainResource.
    """
    
    resourceType: str = "MeasureReport"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifier for the MeasureReport
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # complete | pending | error (required in FHIR)
    # Type
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[str] = None  # individual | subject-list | summary | data-exchange (required)
    # Data Update Requirement
    dataUpdateRequirement: Optional[CodeableConcept] = None  # The data update requirement for the measure
    # Measure
    # Note: measure is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce measure is provided.
    measure: Optional[str] = None  # What measure was calculated (canonical reference, required)
    # Subject
    subject: Optional[Reference] = None  # What individual(s) the report is for
    # Date
    date: Optional[str] = None  # When the report was generated
    # Reporter
    reporter: Optional[Reference] = None  # Who is reporting the data
    # Period
    # Note: period is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce period is provided.
    period: Optional[Period] = None  # What period the report covers (required)
    # Improvement Notation
    improvementNotation: Optional[CodeableConcept] = None  # increase | decrease
    # Group
    group: List[MeasureReportGroup] = field(default_factory=list)  # Measure results for each group
    # Evaluated Resource
    evaluatedResource: List[Reference] = field(default_factory=list)  # What data was used to calculate the measure

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

