# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DetectedIssue resource.

Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, gaps in care, etc.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class DetectedIssueEvidence:
    """
    DetectedIssueEvidence nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[List[CodeableConcept]] = field(default_factory=list)  # A manifestation that led to the recording of this detected issue.
    detail: Optional[List[Reference]] = field(default_factory=list)  # Links to resources that constitute evidence for the detected issue such as a GuidanceResponse or ...

@dataclass
class DetectedIssueMitigation:
    """
    DetectedIssueMitigation nested class.
    """

    action: Optional[CodeableConcept] = None  # Describes the action that was taken or the observation that was made that reduces/eliminates the ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    date: Optional[str] = None  # Indicates when the mitigating action was documented.
    author: Optional[Reference] = None  # Identifies the practitioner who determined the mitigation and takes responsibility for the mitiga...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Clinicians may add additional notes or justifications about the mitigation action. For example, p...


@dataclass
class DetectedIssue(FHIRResource):
    """
    Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, gaps in care, etc.
    """

    status: Optional[str] = None  # Indicates the status of the detected issue.
    resourceType: str = "DetectedIssue"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier associated with the detected issue record.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A code that classifies the general type of detected issue.
    code: Optional[CodeableConcept] = None  # Identifies the specific type of issue identified.
    severity: Optional[str] = None  # Indicates the degree of importance associated with the identified issue based on the potential im...
    subject: Optional[Reference] = None  # Indicates the subject whose record the detected issue is associated with.
    encounter: Optional[Reference] = None  # The encounter during which this issue was detected.
    identified: Optional[Any] = None  # The date or period when the detected issue was initially identified.
    author: Optional[Reference] = None  # Individual or device responsible for the issue being raised.  For example, a decision support app...
    implicated: Optional[List[Reference]] = field(default_factory=list)  # Indicates the resource representing the current activity or proposed activity that is potentially...
    evidence: Optional[List[BackboneElement]] = field(default_factory=list)  # Supporting evidence or manifestations that provide the basis for identifying the detected issue s...
    detail: Optional[str] = None  # A textual explanation of the detected issue.
    reference: Optional[str] = None  # The literature, knowledge-base or similar reference that describes the propensity for the detecte...
    mitigation: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates an action that has been taken or is committed to reduce or eliminate the likelihood of ...