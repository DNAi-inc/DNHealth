# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Goal resource.

Describes the intended objective(s) for a patient, group or organization care, for example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, etc.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Duration, Extension, Identifier, Quantity, Range, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class GoalTarget:
    """
    GoalTarget nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    measure: Optional[CodeableConcept] = None  # The parameter whose value is being tracked, e.g. body weight, blood pressure, or hemoglobin A1c l...
    detail: Optional[Any] = None  # The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pou...
    due: Optional[Any] = None  # Indicates either the date or the duration after start by which the goal should be met.


@dataclass
class Goal(FHIRResource):
    """
    Describes the intended objective(s) for a patient, group or organization care, for example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, etc.
    """

    lifecycleStatus: Optional[str] = None  # The state of the goal throughout its lifecycle.
    description: Optional[CodeableConcept] = None  # Human-readable and/or coded description of a specific desired objective of care, such as \"contro...
    subject: Optional[Reference] = None  # Identifies the patient, group or organization for whom the goal is being established.
    resourceType: str = "Goal"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this goal by the performer or other systems which remain constan...
    achievementStatus: Optional[CodeableConcept] = None  # Describes the progression, or lack thereof, towards the goal against the target.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Indicates a category the goal falls within.
    continuous: Optional[bool] = None  # After meeting the goal, ongoing activity is needed to sustain the goal objective.
    priority: Optional[CodeableConcept] = None  # Identifies the mutually agreed level of importance associated with reaching/sustaining the goal.
    start: Optional[Any] = None  # The date or event after which the goal should begin being pursued.
    target: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates what should be done by when.
    statusDate: Optional[str] = None  # Identifies when the current status.  I.e. When initially created, when achieved, when cancelled, ...
    statusReason: Optional[str] = None  # Captures the reason for the current status.
    source: Optional[Reference] = None  # Indicates whose goal this is - patient goal, practitioner goal, etc.
    addresses: Optional[List[Reference]] = field(default_factory=list)  # The identified conditions and other health record elements that are intended to be addressed by t...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Any comments related to the goal.
    outcome: Optional[List[Any]] = field(default_factory=list)  # Identifies the change (or lack of change) at the point when the status of the goal is assessed.