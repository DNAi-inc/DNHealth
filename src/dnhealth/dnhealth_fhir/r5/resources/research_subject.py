# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ResearchSubject resource.

A ResearchSubject is a participant or object which is the recipient of investigative activities in a research study.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import List, Optional

@dataclass
class ResearchSubjectProgress:
    """
    ResearchSubjectProgress nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Identifies the aspect of the subject's journey that the state refers to.
    subjectState: Optional[CodeableConcept] = None  # The current state of the subject.
    milestone: Optional[CodeableConcept] = None  # The milestones the subject has passed through.
    reason: Optional[CodeableConcept] = None  # The reason for the state change.  If coded it should follow the formal subject state model.
    startDate: Optional[str] = None  # The date when the new status started.
    endDate: Optional[str] = None  # The date when the state ended.


@dataclass
class ResearchSubject(FHIRResource):
    """
    A ResearchSubject is a participant or object which is the recipient of investigative activities in a research study.
    """

    status: Optional[str] = None  # The publication state of the resource (not of the subject).
    study: Optional[Reference] = None  # Reference to the study the subject is participating in.
    subject: Optional[Reference] = None  # The record of the person, animal or other entity involved in the study.
    resourceType: str = "ResearchSubject"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers assigned to this research subject for a study.
    progress: Optional[List[BackboneElement]] = field(default_factory=list)  # The current state (status) of the subject and resons for status change where appropriate.
    period: Optional[Period] = None  # The dates the subject began and ended their participation in the study.
    assignedComparisonGroup: Optional[str] = None  # The name of the arm in the study the subject is expected to follow as part of this study.
    actualComparisonGroup: Optional[str] = None  # The name of the arm in the study the subject actually followed as part of this study.
    consent: Optional[List[Reference]] = field(default_factory=list)  # A record of the patient's informed agreement to participate in the study.