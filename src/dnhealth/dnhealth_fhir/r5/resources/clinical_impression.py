# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ClinicalImpression resource.

A record of a clinical assessment performed to determine what problem(s) may affect the patient and before planning the treatments or management strategies that are best to manage a patient's condition. Assessments are often 1:1 with a clinical consultation / encounter,  but this varies greatly depending on the clinical workflow. This resource is called "ClinicalImpression" rather than "ClinicalAssessment" to avoid confusion with the recording of assessment tools such as Apgar score.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class ClinicalImpressionFinding:
    """
    ClinicalImpressionFinding nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    item: Optional[Any] = None  # Specific text, code or reference for finding or diagnosis, which may include ruled-out or resolve...
    basis: Optional[str] = None  # Which investigations support finding or diagnosis.


@dataclass
class ClinicalImpression(FHIRResource):
    """
    A record of a clinical assessment performed to determine what problem(s) may affect the patient and before planning the treatments or management strategies that are best to manage a patient's condition. Assessments are often 1:1 with a clinical consultation / encounter,  but this varies greatly depending on the clinical workflow. This resource is called "ClinicalImpression" rather than "ClinicalAssessment" to avoid confusion with the recording of assessment tools such as Apgar score.
    """

    status: Optional[str] = None  # Identifies the workflow status of the assessment.
    subject: Optional[Reference] = None  # The patient or group of individuals assessed as part of this record.
    resourceType: str = "ClinicalImpression"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this clinical impression by the performer or other systems which...
    statusReason: Optional[CodeableConcept] = None  # Captures the reason for the current state of the ClinicalImpression.
    description: Optional[str] = None  # A summary of the context and/or cause of the assessment - why / where it was performed, and what ...
    encounter: Optional[Reference] = None  # The Encounter during which this ClinicalImpression was created or to which the creation of this r...
    effective: Optional[Any] = None  # The point in time or period over which the subject was assessed.
    date: Optional[str] = None  # Indicates when the documentation of the assessment was complete.
    performer: Optional[Reference] = None  # The clinician performing the assessment.
    previous: Optional[Reference] = None  # A reference to the last assessment that was conducted on this patient. Assessments are often/usua...
    problem: Optional[List[Reference]] = field(default_factory=list)  # A list of the relevant problems/conditions for a patient.
    changePattern: Optional[CodeableConcept] = None  # Change in the status/pattern of a subject's condition since previously assessed, such as worsenin...
    protocol: Optional[List[str]] = field(default_factory=list)  # Reference to a specific published clinical protocol that was followed during this assessment, and...
    summary: Optional[str] = None  # A text summary of the investigations and the diagnosis.
    finding: Optional[List[BackboneElement]] = field(default_factory=list)  # Specific findings or diagnoses that were considered likely or relevant to ongoing treatment.
    prognosisCodeableConcept: Optional[List[CodeableConcept]] = field(default_factory=list)  # Estimate of likely outcome.
    prognosisReference: Optional[List[Reference]] = field(default_factory=list)  # RiskAssessment expressing likely outcome.
    supportingInfo: Optional[List[Reference]] = field(default_factory=list)  # Information supporting the clinical impression, which can contain investigation results.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Commentary about the impression, typically recorded after the impression itself was made, though ...