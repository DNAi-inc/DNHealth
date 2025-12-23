# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ResearchStudy resource.

A scientific study of nature that sometimes includes processes involved in health and disease. For example, clinical trials are research studies that involve people. These studies may be related to new ways to screen, prevent, diagnose, and treat disease. They may also study certain outcomes and certain groups of people by looking at data collected in the past or future.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference, RelatedArtifact
from typing import Any, List, Optional

@dataclass
class ResearchStudyLabel:
    """
    ResearchStudyLabel nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Kind of name.
    value: Optional[str] = None  # The name.

@dataclass
class ResearchStudyAssociatedParty:
    """
    ResearchStudyAssociatedParty nested class.
    """

    role: Optional[CodeableConcept] = None  # Type of association.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Name of associated party.
    period: Optional[List[Period]] = field(default_factory=list)  # Identifies the start date and the end date of the associated party in the role.
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # A categorization other than role for the associated party.
    party: Optional[Reference] = None  # Individual or organization associated with study (use practitionerRole to specify their organisat...

@dataclass
class ResearchStudyProgressStatus:
    """
    ResearchStudyProgressStatus nested class.
    """

    state: Optional[CodeableConcept] = None  # Label for status or state (e.g. recruitment status).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    actual: Optional[bool] = None  # An indication of whether or not the date is a known date when the state changed or will change. A...
    period: Optional[Period] = None  # Date range.

@dataclass
class ResearchStudyRecruitment:
    """
    ResearchStudyRecruitment nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    targetNumber: Optional[int] = None  # Estimated total number of participants to be enrolled.
    actualNumber: Optional[int] = None  # Actual total number of participants enrolled in study.
    eligibility: Optional[Reference] = None  # Inclusion and exclusion criteria.
    actualGroup: Optional[Reference] = None  # Group of participants who were enrolled in study.

@dataclass
class ResearchStudyComparisonGroup:
    """
    ResearchStudyComparisonGroup nested class.
    """

    name: Optional[str] = None  # Unique, human-readable label for this comparisonGroup of the study.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # Allows the comparisonGroup for the study and the comparisonGroup for the subject to be linked eas...
    type: Optional[CodeableConcept] = None  # Categorization of study comparisonGroup, e.g. experimental, active comparator, placebo comparater.
    description: Optional[str] = None  # A succinct description of the path through the study that would be followed by a subject adhering...
    intendedExposure: Optional[List[Reference]] = field(default_factory=list)  # Interventions or exposures in this comparisonGroup or cohort.
    observedGroup: Optional[Reference] = None  # Group of participants who were enrolled in study comparisonGroup.

@dataclass
class ResearchStudyObjective:
    """
    ResearchStudyObjective nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Unique, human-readable label for this objective of the study.
    type: Optional[CodeableConcept] = None  # The kind of study objective.
    description: Optional[str] = None  # Free text description of the objective of the study.  This is what the study is trying to achieve...

@dataclass
class ResearchStudyOutcomeMeasure:
    """
    ResearchStudyOutcomeMeasure nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Label for the outcome.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The parameter or characteristic being assessed as one of the values by which the study is assessed.
    description: Optional[str] = None  # Description of the outcome.
    reference: Optional[Reference] = None  # Structured outcome definition.


@dataclass
class ResearchStudy(FHIRResource):
    """
    A scientific study of nature that sometimes includes processes involved in health and disease. For example, clinical trials are research studies that involve people. These studies may be related to new ways to screen, prevent, diagnose, and treat disease. They may also study certain outcomes and certain groups of people by looking at data collected in the past or future.
    """

    status: Optional[str] = None  # The publication state of the resource (not of the study).
    resourceType: str = "ResearchStudy"
    url: Optional[str] = None  # Canonical identifier for this study resource, represented as a globally unique URI.
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers assigned to this research study by the sponsor or other systems.
    version: Optional[str] = None  # The business version for the study record.
    name: Optional[str] = None  # Name for this study (computer friendly).
    title: Optional[str] = None  # The human readable name of the research study.
    label: Optional[List[BackboneElement]] = field(default_factory=list)  # Additional names for the study.
    protocol: Optional[List[Reference]] = field(default_factory=list)  # The set of steps expected to be performed as part of the execution of the study.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger research study of which this particular study is a component or step.
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Citations, references, URLs and other related documents.  When using relatedArtifact to share URL...
    date: Optional[str] = None  # The date (and optionally time) when the ResearchStudy Resource was last significantly changed. Th...
    primaryPurposeType: Optional[CodeableConcept] = None  # The type of study based upon the intent of the study activities. A classification of the intent o...
    phase: Optional[CodeableConcept] = None  # The stage in the progression of a therapy from initial experimental use in humans in clinical tri...
    studyDesign: Optional[List[CodeableConcept]] = field(default_factory=list)  # Codes categorizing the type of study such as investigational vs. observational, type of blinding,...
    focus: Optional[List[Any]] = field(default_factory=list)  # The medication(s), food(s), therapy(ies), device(s) or other concerns or interventions that the s...
    condition: Optional[List[CodeableConcept]] = field(default_factory=list)  # The condition that is the focus of the study.  For example, In a study to examine risk factors fo...
    keyword: Optional[List[CodeableConcept]] = field(default_factory=list)  # Key terms to aid in searching for or filtering the study.
    region: Optional[List[CodeableConcept]] = field(default_factory=list)  # A country, state or other area where the study is taking place rather than its precise geographic...
    descriptionSummary: Optional[str] = None  # A brief text for explaining the study.
    description: Optional[str] = None  # A detailed and human-readable narrative of the study. E.g., study abstract.
    period: Optional[Period] = None  # Identifies the start date and the expected (or actual, depending on status) end date for the study.
    site: Optional[List[Reference]] = field(default_factory=list)  # A facility in which study activities are conducted.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the study by the performer, subject or other participants.
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Additional grouping mechanism or categorization of a research study. Example: FDA regulated devic...
    associatedParty: Optional[List[BackboneElement]] = field(default_factory=list)  # Sponsors, collaborators, and other parties.
    progressStatus: Optional[List[BackboneElement]] = field(default_factory=list)  # Status of study with time for that status.
    whyStopped: Optional[CodeableConcept] = None  # A description and/or code explaining the premature termination of the study.
    recruitment: Optional[BackboneElement] = None  # Target or actual group of participants enrolled in study.
    comparisonGroup: Optional[List[BackboneElement]] = field(default_factory=list)  # Describes an expected event or sequence of events for one of the subjects of a study. E.g. for a ...
    objective: Optional[List[BackboneElement]] = field(default_factory=list)  # A goal that the study is aiming to achieve in terms of a scientific question to be answered by th...
    outcomeMeasure: Optional[List[BackboneElement]] = field(default_factory=list)  # An \"outcome measure\", \"endpoint\", \"effect measure\" or \"measure of effect\" is a specific m...
    result: Optional[List[Reference]] = field(default_factory=list)  # Link to one or more sets of results generated by the study.  Could also link to a research regist...