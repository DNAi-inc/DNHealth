# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MeasureReport resource.

The MeasureReport resource contains the results of the calculation of a measure; and optionally a reference to the resources involved in that calculation.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Duration, Extension, Identifier, Period, Quantity, Range, Reference
from typing import Any, List, Optional

@dataclass
class MeasureReportGroup:
    """
    MeasureReportGroup nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # The group from the Measure that corresponds to this group in the MeasureReport resource.
    code: Optional[CodeableConcept] = None  # The meaning of the population group as defined in the measure definition.
    subject: Optional[Reference] = None  # Optional subject identifying the individual or individuals the report is for.
    population: Optional[List[BackboneElement]] = field(default_factory=list)  # The populations that make up the population group, one for each type of population appropriate fo...
    count: Optional[int] = None  # The number of members of the population.
    subjectResults: Optional[Reference] = None  # This element refers to a List of individual level MeasureReport resources, one for each subject i...
    subjectReport: Optional[List[Reference]] = field(default_factory=list)  # A reference to an individual level MeasureReport resource for a member of the population.
    subjects: Optional[Reference] = None  # Optional Group identifying the individuals that make up the population.
    measureScore: Optional[Any] = None  # The measure score for this population group, calculated as appropriate for the measure type and s...
    stratifier: Optional[List[BackboneElement]] = field(default_factory=list)  # When a measure includes multiple stratifiers, there will be a stratifier group for each stratifie...
    stratum: Optional[List[BackboneElement]] = field(default_factory=list)  # This element contains the results for a single stratum within the stratifier. For example, when s...
    value: Optional[Any] = None  # The value for this stratum, expressed as a CodeableConcept. When defining stratifiers on complex ...
    component: Optional[List[BackboneElement]] = field(default_factory=list)  # A stratifier component value.

@dataclass
class MeasureReportGroupPopulation:
    """
    MeasureReportGroupPopulation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # The population from the Measure that corresponds to this population in the MeasureReport resource.
    code: Optional[CodeableConcept] = None  # The type of the population.
    count: Optional[int] = None  # The number of members of the population.
    subjectResults: Optional[Reference] = None  # This element refers to a List of individual level MeasureReport resources, one for each subject i...
    subjectReport: Optional[List[Reference]] = field(default_factory=list)  # A reference to an individual level MeasureReport resource for a member of the population.
    subjects: Optional[Reference] = None  # Optional Group identifying the individuals that make up the population.

@dataclass
class MeasureReportGroupStratifier:
    """
    MeasureReportGroupStratifier nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # The stratifier from the Measure that corresponds to this stratifier in the MeasureReport resource.
    code: Optional[CodeableConcept] = None  # The meaning of this stratifier, as defined in the measure definition.
    stratum: Optional[List[BackboneElement]] = field(default_factory=list)  # This element contains the results for a single stratum within the stratifier. For example, when s...
    value: Optional[Any] = None  # The value for this stratum, expressed as a CodeableConcept. When defining stratifiers on complex ...
    component: Optional[List[BackboneElement]] = field(default_factory=list)  # A stratifier component value.
    population: Optional[List[BackboneElement]] = field(default_factory=list)  # The populations that make up the stratum, one for each type of population appropriate to the meas...
    count: Optional[int] = None  # The number of members of the population in this stratum.
    subjectResults: Optional[Reference] = None  # This element refers to a List of individual level MeasureReport resources, one for each subject i...
    subjectReport: Optional[List[Reference]] = field(default_factory=list)  # A reference to an individual level MeasureReport resource for a member of the population.
    subjects: Optional[Reference] = None  # Optional Group identifying the individuals that make up the population.
    measureScore: Optional[Any] = None  # The measure score for this stratum, calculated as appropriate for the measure type and scoring me...

@dataclass
class MeasureReportGroupStratifierStratum:
    """
    MeasureReportGroupStratifierStratum nested class.
    """

    code: Optional[CodeableConcept] = None  # The code for the stratum component value.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # The value for this stratum, expressed as a CodeableConcept. When defining stratifiers on complex ...
    component: Optional[List[BackboneElement]] = field(default_factory=list)  # A stratifier component value.
    linkId: Optional[str] = None  # The stratifier component from the Measure that corresponds to this stratifier component in the Me...
    population: Optional[List[BackboneElement]] = field(default_factory=list)  # The populations that make up the stratum, one for each type of population appropriate to the meas...
    count: Optional[int] = None  # The number of members of the population in this stratum.
    subjectResults: Optional[Reference] = None  # This element refers to a List of individual level MeasureReport resources, one for each subject i...
    subjectReport: Optional[List[Reference]] = field(default_factory=list)  # A reference to an individual level MeasureReport resource for a member of the population.
    subjects: Optional[Reference] = None  # Optional Group identifying the individuals that make up the population.
    measureScore: Optional[Any] = None  # The measure score for this stratum, calculated as appropriate for the measure type and scoring me...

@dataclass
class MeasureReportGroupStratifierStratumComponent:
    """
    MeasureReportGroupStratifierStratumComponent nested class.
    """

    code: Optional[CodeableConcept] = None  # The code for the stratum component value.
    value: Optional[Any] = None  # The stratum component value.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # The stratifier component from the Measure that corresponds to this stratifier component in the Me...

@dataclass
class MeasureReportGroupStratifierStratumPopulation:
    """
    MeasureReportGroupStratifierStratumPopulation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # The population from the Measure that corresponds to this population in the MeasureReport resource.
    code: Optional[CodeableConcept] = None  # The type of the population.
    count: Optional[int] = None  # The number of members of the population in this stratum.
    subjectResults: Optional[Reference] = None  # This element refers to a List of individual level MeasureReport resources, one for each subject i...
    subjectReport: Optional[List[Reference]] = field(default_factory=list)  # A reference to an individual level MeasureReport resource for a member of the population.
    subjects: Optional[Reference] = None  # Optional Group identifying the individuals that make up the population.


@dataclass
class MeasureReport(FHIRResource):
    """
    The MeasureReport resource contains the results of the calculation of a measure; and optionally a reference to the resources involved in that calculation.
    """

    status: Optional[str] = None  # The MeasureReport status. No data will be available until the MeasureReport status is complete.
    type: Optional[str] = None  # The type of measure report. This may be an individual report, which provides the score for the me...
    period: Optional[Period] = None  # The reporting period for which the report was calculated.
    resourceType: str = "MeasureReport"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this MeasureReport when it is represented in other f...
    dataUpdateType: Optional[str] = None  # Indicates whether the data submitted in a data-exchange report represents a snapshot or increment...
    measure: Optional[str] = None  # A reference to the Measure that was calculated to produce this report.
    subject: Optional[Reference] = None  # Optional subject identifying the individual or individuals the report is for.
    date: Optional[str] = None  # The date this measure was calculated.
    reporter: Optional[Reference] = None  # The individual or organization that is reporting the data.
    reportingVendor: Optional[Reference] = None  # A reference to the vendor who queried the data, calculated results and/or generated the report. T...
    location: Optional[Reference] = None  # A reference to the location for which the data is being reported.
    inputParameters: Optional[Reference] = None  # A reference to a Parameters resource (typically represented using a contained resource) that repr...
    scoring: Optional[CodeableConcept] = None  # Indicates how the calculation is performed for the measure, including proportion, ratio, continuo...
    improvementNotation: Optional[CodeableConcept] = None  # Whether improvement in the measure is noted by an increase or decrease in the measure score.
    group: Optional[List[BackboneElement]] = field(default_factory=list)  # The results of the calculation, one for each population group in the measure.
    supplementalData: Optional[List[Reference]] = field(default_factory=list)  # A reference to a Resource that represents additional information collected for the report. If the...
    evaluatedResource: Optional[List[Reference]] = field(default_factory=list)  # Evaluated resources are used to capture what data was involved in the calculation of a measure. T...