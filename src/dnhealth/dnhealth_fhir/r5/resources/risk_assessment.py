# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 RiskAssessment resource.

An assessment of the likely outcome(s) for a patient or other subject as well as the likelihood of each outcome.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Range, Reference
from typing import Any, List, Optional

@dataclass
class RiskAssessmentPrediction:
    """
    RiskAssessmentPrediction nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    outcome: Optional[CodeableConcept] = None  # One of the potential outcomes for the patient (e.g. remission, death,  a particular condition).
    probability: Optional[Any] = None  # Indicates how likely the outcome is (in the specified timeframe).
    qualitativeRisk: Optional[CodeableConcept] = None  # Indicates how likely the outcome is (in the specified timeframe), expressed as a qualitative valu...
    relativeRisk: Optional[float] = None  # Indicates the risk for this particular subject (with their specific characteristics) divided by t...
    when: Optional[Any] = None  # Indicates the period of time or age range of the subject to which the specified probability applies.
    rationale: Optional[str] = None  # Additional information explaining the basis for the prediction.


@dataclass
class RiskAssessment(FHIRResource):
    """
    An assessment of the likely outcome(s) for a patient or other subject as well as the likelihood of each outcome.
    """

    status: Optional[str] = None  # The status of the RiskAssessment, using the same statuses as an Observation.
    subject: Optional[Reference] = None  # The patient or group the risk assessment applies to.
    resourceType: str = "RiskAssessment"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier assigned to the risk assessment.
    basedOn: Optional[Reference] = None  # A reference to the request that is fulfilled by this risk assessment.
    parent: Optional[Reference] = None  # A reference to a resource that this risk assessment is part of, such as a Procedure.
    method: Optional[CodeableConcept] = None  # The algorithm, process or mechanism used to evaluate the risk.
    code: Optional[CodeableConcept] = None  # The type of the risk assessment performed.
    encounter: Optional[Reference] = None  # The encounter where the assessment was performed.
    occurrence: Optional[Any] = None  # The date (and possibly time) the risk assessment was performed.
    condition: Optional[Reference] = None  # For assessments or prognosis specific to a particular condition, indicates the condition being as...
    performer: Optional[Reference] = None  # The provider, patient, related person, or software application that performed the assessment.
    reason: Optional[List[Any]] = field(default_factory=list)  # The reason the risk assessment was performed.
    basis: Optional[List[Reference]] = field(default_factory=list)  # Indicates the source data considered as part of the assessment (for example, FamilyHistory, Obser...
    prediction: Optional[List[BackboneElement]] = field(default_factory=list)  # Describes the expected outcome for the subject.
    mitigation: Optional[str] = None  # A description of the steps that might be taken to reduce the identified risk(s).
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional comments about the risk assessment.