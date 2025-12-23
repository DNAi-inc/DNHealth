# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Evidence resource.

The Evidence Resource provides a machine-interpretable expression of an evidence concept including the evidence variables (e.g., population, exposures/interventions, comparators, outcomes, measured variables, confounding variables), the statistics, and the certainty of this evidence.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Quantity, Range, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class EvidenceVariableDefinition:
    """
    EvidenceVariableDefinition nested class.
    """

    variableRole: Optional[CodeableConcept] = None  # population | subpopulation | exposure | referenceExposure | measuredVariable | confounder.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # A text description or summary of the variable.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Footnotes and/or explanatory notes.
    observed: Optional[Reference] = None  # Definition of the actual variable related to the statistic(s).
    intended: Optional[Reference] = None  # Definition of the intended variable related to the Evidence.
    directnessMatch: Optional[CodeableConcept] = None  # Indication of quality of match between intended variable to actual variable.

@dataclass
class EvidenceStatistic:
    """
    EvidenceStatistic nested class.
    """

    code: Optional[CodeableConcept] = None  # Description of a component of the method to generate the statistic.
    variableDefinition: Optional[Reference] = None  # Description of the variable.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # A description of the content value of the statistic.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Footnotes and/or explanatory notes.
    statisticType: Optional[CodeableConcept] = None  # Type of statistic, e.g., relative risk.
    category: Optional[CodeableConcept] = None  # When the measured variable is handled categorically, the category element is used to define which...
    quantity: Optional[Quantity] = None  # Statistic value.
    numberOfEvents: Optional[int] = None  # The number of events associated with the statistic, where the unit of analysis is different from ...
    numberAffected: Optional[int] = None  # The number of participants affected where the unit of analysis is the same as sampleSize.knownDat...
    sampleSize: Optional[BackboneElement] = None  # Number of samples in the statistic.
    numberOfStudies: Optional[int] = None  # Number of participants in the population.
    numberOfParticipants: Optional[int] = None  # A human-readable string to clarify or explain concepts about the sample size.
    knownDataCount: Optional[int] = None  # Number of participants with known results for measured variables.
    attributeEstimate: Optional[List[BackboneElement]] = field(default_factory=list)  # A statistical attribute of the statistic such as a measure of heterogeneity.
    type: Optional[CodeableConcept] = None  # The type of attribute estimate, e.g., confidence interval or p value.
    level: Optional[float] = None  # Use 95 for a 95% confidence interval.
    range: Optional[Range] = None  # Lower bound of confidence interval.
    modelCharacteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # A component of the method to generate the statistic.
    value: Optional[Quantity] = None  # Further specification of the quantified value of the component of the method to generate the stat...
    variable: Optional[List[BackboneElement]] = field(default_factory=list)  # A variable adjusted for in the adjusted analysis.
    handling: Optional[str] = None  # How the variable is classified for use in adjusted analysis.
    valueCategory: Optional[List[CodeableConcept]] = field(default_factory=list)  # Description for grouping of ordinal or polychotomous variables.
    valueQuantity: Optional[List[Quantity]] = field(default_factory=list)  # Discrete value for grouping of ordinal or polychotomous variables.
    valueRange: Optional[List[Range]] = field(default_factory=list)  # Range of values for grouping of ordinal or polychotomous variables.

@dataclass
class EvidenceStatisticSampleSize:
    """
    EvidenceStatisticSampleSize nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Human-readable summary of population sample size.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Footnote or explanatory note about the sample size.
    numberOfStudies: Optional[int] = None  # Number of participants in the population.
    numberOfParticipants: Optional[int] = None  # A human-readable string to clarify or explain concepts about the sample size.
    knownDataCount: Optional[int] = None  # Number of participants with known results for measured variables.

@dataclass
class EvidenceStatisticAttributeEstimate:
    """
    EvidenceStatisticAttributeEstimate nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Human-readable summary of the estimate.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Footnote or explanatory note about the estimate.
    type: Optional[CodeableConcept] = None  # The type of attribute estimate, e.g., confidence interval or p value.
    quantity: Optional[Quantity] = None  # The singular quantity of the attribute estimate, for attribute estimates represented as single va...
    level: Optional[float] = None  # Use 95 for a 95% confidence interval.
    range: Optional[Range] = None  # Lower bound of confidence interval.
    attributeEstimate: Optional[List[Any]] = field(default_factory=list)  # A nested attribute estimate; which is the attribute estimate of an attribute estimate.

@dataclass
class EvidenceStatisticModelCharacteristic:
    """
    EvidenceStatisticModelCharacteristic nested class.
    """

    code: Optional[CodeableConcept] = None  # Description of a component of the method to generate the statistic.
    variableDefinition: Optional[Reference] = None  # Description of the variable.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Quantity] = None  # Further specification of the quantified value of the component of the method to generate the stat...
    variable: Optional[List[BackboneElement]] = field(default_factory=list)  # A variable adjusted for in the adjusted analysis.
    handling: Optional[str] = None  # How the variable is classified for use in adjusted analysis.
    valueCategory: Optional[List[CodeableConcept]] = field(default_factory=list)  # Description for grouping of ordinal or polychotomous variables.
    valueQuantity: Optional[List[Quantity]] = field(default_factory=list)  # Discrete value for grouping of ordinal or polychotomous variables.
    valueRange: Optional[List[Range]] = field(default_factory=list)  # Range of values for grouping of ordinal or polychotomous variables.
    attributeEstimate: Optional[List[Any]] = field(default_factory=list)  # An attribute of the statistic used as a model characteristic.

@dataclass
class EvidenceStatisticModelCharacteristicVariable:
    """
    EvidenceStatisticModelCharacteristicVariable nested class.
    """

    variableDefinition: Optional[Reference] = None  # Description of the variable.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    handling: Optional[str] = None  # How the variable is classified for use in adjusted analysis.
    valueCategory: Optional[List[CodeableConcept]] = field(default_factory=list)  # Description for grouping of ordinal or polychotomous variables.
    valueQuantity: Optional[List[Quantity]] = field(default_factory=list)  # Discrete value for grouping of ordinal or polychotomous variables.
    valueRange: Optional[List[Range]] = field(default_factory=list)  # Range of values for grouping of ordinal or polychotomous variables.

@dataclass
class EvidenceCertainty:
    """
    EvidenceCertainty nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Textual description of certainty.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Footnotes and/or explanatory notes.
    type: Optional[CodeableConcept] = None  # Aspect of certainty being rated.
    rating: Optional[CodeableConcept] = None  # Assessment or judgement of the aspect.
    rater: Optional[str] = None  # Individual or group who did the rating.
    subcomponent: Optional[List[Any]] = field(default_factory=list)  # A domain or subdomain of certainty.


@dataclass
class Evidence(FHIRResource):
    """
    The Evidence Resource provides a machine-interpretable expression of an evidence concept including the evidence variables (e.g., population, exposures/interventions, comparators, outcomes, measured variables, confounding variables), the statistics, and the certainty of this evidence.
    """

    status: Optional[str] = None  # The status of this summary. Enables tracking the life-cycle of the content.
    variableDefinition: List[BackboneElement] = field(default_factory=list)  # Evidence variable such as population, exposure, or outcome.
    resourceType: str = "Evidence"
    url: Optional[str] = None  # An absolute URI that is used to identify this evidence when it is referenced in a specification, ...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this summary when it is represented in other formats...
    version: Optional[str] = None  # The identifier that is used to identify this version of the summary when it is referenced in a sp...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the evidence. This name should be usable as an identifier for...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the summary.
    citeAs: Optional[Any] = None  # Citation Resource or display of suggested citation for this evidence.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this resource is authored for testing purposes (or education/eva...
    date: Optional[str] = None  # The date  (and optionally time) when the summary was last significantly changed. The date must ch...
    approvalDate: Optional[str] = None  # The date on which the resource content was approved by the publisher. Approval happens once when ...
    lastReviewDate: Optional[str] = None  # The date on which the resource content was last reviewed. Review happens periodically after appro...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    author: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device primarily involved in the creation and maintenance of the...
    editor: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device primarily responsible for internal coherence of the content.
    reviewer: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device primarily responsible for review of some aspect of the co...
    endorser: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device responsible for officially endorsing the content for use ...
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    purpose: Optional[str] = None  # Explanation of why this Evidence is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the Evidence and/or its contents. Copyright statements are gene...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Link or citation to artifact associated with the summary.
    description: Optional[str] = None  # A free text natural language description of the evidence from a consumer's perspective.
    assertion: Optional[str] = None  # Declarative description of the Evidence.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Footnotes and/or explanatory notes.
    synthesisType: Optional[CodeableConcept] = None  # The method to combine studies.
    studyDesign: Optional[List[CodeableConcept]] = field(default_factory=list)  # The design of the study that produced this evidence. The design is described with any number of s...
    statistic: Optional[List[BackboneElement]] = field(default_factory=list)  # Values and parameters for a single statistic.
    certainty: Optional[List[BackboneElement]] = field(default_factory=list)  # Assessment of certainty, confidence in the estimates, or quality of the evidence.