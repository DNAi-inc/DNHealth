# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Goal resource.

Goal represents a desired outcome for a patient.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class GoalTarget:
    """
    FHIR Goal.target complex type.
    
    Target outcome for the goal.
    """
    
    measure: Optional[CodeableConcept] = None  # The parameter whose value is being tracked
    detailQuantity: Optional[Quantity] = None  # The target value to be achieved
    detailRange: Optional[Any] = None  # The target value to be achieved (Range)
    detailCodeableConcept: Optional[CodeableConcept] = None  # The target value to be achieved
    detailString: Optional[str] = None  # The target value to be achieved
    detailBoolean: Optional[bool] = None  # The target value to be achieved
    detailInteger: Optional[int] = None  # The target value to be achieved
    detailRatio: Optional[Any] = None  # The target value to be achieved (Ratio)
    dueDate: Optional[str] = None  # Reach goal on or before
    dueDuration: Optional[Any] = None  # Reach goal on or before (Duration)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Goal(DomainResource):
    """
    FHIR R4 Goal resource.
    
    Represents a desired outcome for a patient.
    Extends DomainResource.
    """
    
    resourceType: str = "Goal"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External Ids for this goal
    # Lifecycle Status
    lifecycleStatus: str  # proposed | planned | accepted | active | on-hold | completed | cancelled | entered-in-error | rejected (required)
    # Achievement Status
    achievementStatus: Optional[CodeableConcept] = None  # in-progress | improving | worsening | no-change | achieved | sustaining | not-achieved | no-progress | not-attainable
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # E.g. Treatment, dietary, behavioral, etc.
    # Priority
    priority: Optional[CodeableConcept] = None  # high | medium | low
    # Description
    description: CodeableConcept  # Code or text describing goal (required)
    # Subject
    subject: Reference  # Who this goal is intended for (required)
    # Start Date
    startDate: Optional[str] = None  # When goal pursuit begins
    # Start CodeableConcept
    startCodeableConcept: Optional[CodeableConcept] = None  # When goal pursuit begins
    # Target
    target: List[GoalTarget] = field(default_factory=list)  # Target outcome for the goal
    # Status Date
    statusDate: Optional[str] = None  # When goal status took effect
    # Status Reason
    statusReason: Optional[str] = None  # Reason for current status
    # Expressed By
    expressedBy: Optional[Reference] = None  # Who's responsible for creating Goal?
    # Addresses
    addresses: List[Reference] = field(default_factory=list)  # Issues addressed by this goal
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments about the goal
    # Outcome Code
    outcomeCode: List[CodeableConcept] = field(default_factory=list)  # What result was achieved regarding the goal?
    # Outcome Reference
    outcomeReference: List[Reference] = field(default_factory=list)  # Observation that resulted from goal

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


