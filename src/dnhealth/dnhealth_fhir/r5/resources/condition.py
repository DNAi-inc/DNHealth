# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Condition resource.

A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Age, Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Range, Reference
from typing import Any, List, Optional

@dataclass
class ConditionParticipant:
    """
    ConditionParticipant nested class.
    """

    actor: Optional[Reference] = None  # Indicates who or what participated in the activities related to the condition.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the actor in the activities related to the condition.

@dataclass
class ConditionStage:
    """
    ConditionStage nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    summary: Optional[CodeableConcept] = None  # A simple summary of the stage such as \"Stage 3\" or \"Early Onset\". The determination of the st...
    assessment: Optional[List[Reference]] = field(default_factory=list)  # Reference to a formal record of the evidence on which the staging assessment is based.
    type: Optional[CodeableConcept] = None  # The kind of staging, such as pathological or clinical staging.


@dataclass
class Condition(FHIRResource):
    """
    A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.
    """

    clinicalStatus: Optional[CodeableConcept] = None  # The clinical status of the condition.
    subject: Optional[Reference] = None  # Indicates the patient or group who the condition record is associated with.
    resourceType: str = "Condition"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this condition by the performer or other systems which remain co...
    verificationStatus: Optional[CodeableConcept] = None  # The verification status to support the clinical status of the condition.  The verification status...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A category assigned to the condition.
    severity: Optional[CodeableConcept] = None  # A subjective assessment of the severity of the condition as evaluated by the clinician.
    code: Optional[CodeableConcept] = None  # Identification of the condition, problem or diagnosis.
    bodySite: Optional[List[CodeableConcept]] = field(default_factory=list)  # The anatomical location where this condition manifests itself.
    encounter: Optional[Reference] = None  # The Encounter during which this Condition was created or to which the creation of this record is ...
    onset: Optional[Any] = None  # Estimated or actual date or date-time  the condition began, in the opinion of the clinician.
    abatement: Optional[Any] = None  # The date or estimated date that the condition resolved or went into remission. This is called \"a...
    recordedDate: Optional[str] = None  # The recordedDate represents when this particular Condition record was created in the system, whic...
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what participated in the activities related to the condition and how they were i...
    stage: Optional[List[BackboneElement]] = field(default_factory=list)  # A simple summary of the stage such as \"Stage 3\" or \"Early Onset\". The determination of the st...
    evidence: Optional[List[Any]] = field(default_factory=list)  # Supporting evidence / manifestations that are the basis of the Condition's verification status, s...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional information about the Condition. This is a general notes/comments entry  for descripti...