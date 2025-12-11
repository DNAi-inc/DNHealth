# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 PlanDefinition resource.

PlanDefinition defines a plan for a series of actions to be taken.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    ContactDetail,
    UsageContext,
    RelatedArtifact,
    Timing,
    Duration,
)


@dataclass
class PlanDefinitionGoal:
    """
    FHIR PlanDefinition.goal complex type.
    
    What the plan is trying to accomplish.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    category: Optional[CodeableConcept] = None  # E.g. Treatment, dietary, behavioral, etc.
    description: Optional[CodeableConcept] = None  # Code or text describing the goal
    priority: Optional[CodeableConcept] = None  # high-priority | medium-priority | low-priority
    start: Optional[CodeableConcept] = None  # When goal pursuit begins
    addresses: List[CodeableConcept] = field(default_factory=list)  # What does the goal address
    documentation: List[RelatedArtifact] = field(default_factory=list)  # Supporting documentation for the goal
    target: List["PlanDefinitionGoalTarget"] = field(default_factory=list)  # Target outcome for the goal


@dataclass
class PlanDefinitionGoalTarget:
    """
    FHIR PlanDefinition.goal.target complex type.
    
    Target outcome for the goal.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    measure: Optional[CodeableConcept] = None  # The parameter whose value is to be tracked
    detailQuantity: Optional[Any] = None  # The target value to be achieved (Quantity)
    detailRange: Optional[Any] = None  # The target value to be achieved (Range)
    detailCodeableConcept: Optional[CodeableConcept] = None  # The target value to be achieved
    due: Optional[Duration] = None  # Reach goal within


@dataclass
class PlanDefinitionAction:
    """
    FHIR PlanDefinition.action complex type.
    
    Action defined by the plan.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    prefix: Optional[str] = None  # User-visible prefix for the action
    title: Optional[str] = None  # User-visible title
    description: Optional[str] = None  # Brief description of the action
    textEquivalent: Optional[str] = None  # Static text equivalent of the action
    priority: Optional[str] = None  # routine | urgent | asap | stat
    code: List[CodeableConcept] = field(default_factory=list)  # Code representing the meaning of the action
    reason: List[CodeableConcept] = field(default_factory=list)  # Why the action should be performed
    documentation: List[RelatedArtifact] = field(default_factory=list)  # Supporting documentation
    goalId: List[str] = field(default_factory=list)  # What goals this action supports
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of individual the action is focused on
    subjectReference: Optional[Reference] = None  # Type of individual the action is focused on
    trigger: List[Any] = field(default_factory=list)  # When the action should be triggered (TriggerDefinition)
    condition: List["PlanDefinitionActionCondition"] = field(default_factory=list)  # Whether or not the action is applicable
    input: List["PlanDefinitionActionInput"] = field(default_factory=list)  # Input data requirements
    output: List["PlanDefinitionActionOutput"] = field(default_factory=list)  # Output data requirements
    relatedAction: List["PlanDefinitionActionRelatedAction"] = field(default_factory=list)  # Relationship to another action
    timingDateTime: Optional[str] = None  # When the action should take place
    timingAge: Optional[Any] = None  # When the action should take place (Age)
    timingPeriod: Optional[Period] = None  # When the action should take place
    timingDuration: Optional[Duration] = None  # When the action should take place
    timingRange: Optional[Any] = None  # When the action should take place (Range)
    timingTiming: Optional[Timing] = None  # When the action should take place
    participant: List["PlanDefinitionActionParticipant"] = field(default_factory=list)  # Who should participate in the action
    type: Optional[CodeableConcept] = None  # create | update | remove | fire-event | generate-report
    groupingBehavior: Optional[str] = None  # visual-group | logical-group | sentence-group
    selectionBehavior: Optional[str] = None  # any | all | all-or-none | exactly-one | at-most-one | one-or-more
    requiredBehavior: Optional[str] = None  # must | could | must-unless-documented
    precheckBehavior: Optional[str] = None  # yes | no
    cardinalityBehavior: Optional[str] = None  # single | multiple
    definitionCanonical: Optional[str] = None  # Description of the activity to be performed (canonical reference)
    definitionUri: Optional[str] = None  # Description of the activity to be performed (URI)
    transform: Optional[str] = None  # Transform to apply the template (canonical reference)
    dynamicValue: List["PlanDefinitionActionDynamicValue"] = field(default_factory=list)  # Dynamic aspects of the definition
    action: List["PlanDefinitionAction"] = field(default_factory=list)  # A sub-action


@dataclass
class PlanDefinitionActionCondition:
    """
    FHIR PlanDefinition.action.condition complex type.
    
    Whether or not the action is applicable.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    kind: str  # applicability | start | stop (required)
    expression: Optional[Any] = None  # Boolean-valued expression (Expression)


@dataclass
class PlanDefinitionActionInput:
    """
    FHIR PlanDefinition.action.input complex type.
    
    Input data requirements.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    title: Optional[str] = None  # User-visible title
    requirement: Optional[Any] = None  # What data is provided (DataRequirement)
    relatedData: Optional[str] = None  # What data is provided


@dataclass
class PlanDefinitionActionOutput:
    """
    FHIR PlanDefinition.action.output complex type.
    
    Output data requirements.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    title: Optional[str] = None  # User-visible title
    requirement: Optional[Any] = None  # What data is provided (DataRequirement)
    relatedData: Optional[str] = None  # What data is provided


@dataclass
class PlanDefinitionActionRelatedAction:
    """
    FHIR PlanDefinition.action.relatedAction complex type.
    
    Relationship to another action.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    actionId: str  # What action is this related to (required)
    relationship: str  # before-start | before | before-end | concurrent-with-start | concurrent | concurrent-with-end | after-start | after | after-end (required)
    offsetDuration: Optional[Duration] = None  # Time offset for the relationship
    offsetRange: Optional[Any] = None  # Time offset for the relationship (Range)


@dataclass
class PlanDefinitionActionParticipant:
    """
    FHIR PlanDefinition.action.participant complex type.
    
    Who should participate in the action.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: Optional[str] = None  # patient | practitioner | related-person | device
    role: Optional[CodeableConcept] = None  # E.g. Nurse, Surgeon, Parent, etc.


@dataclass
class PlanDefinitionActionDynamicValue:
    """
    FHIR PlanDefinition.action.dynamicValue complex type.
    
    Dynamic aspects of the definition.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    path: Optional[str] = None  # The path to the element to be customized
    expression: Optional[Any] = None  # An expression that provides the dynamic value for the customization (Expression)


@dataclass
class PlanDefinition(MetadataResource):
    """
    FHIR R4 PlanDefinition resource.
    
    Defines a plan for a series of actions to be taken.
    Extends MetadataResource.
    """
    
    resourceType: str = "PlanDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this plan definition (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this plan definition (inherited from CanonicalResource)
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the plan definition
    # Type
    type: Optional[CodeableConcept] = None  # order-set | clinical-protocol | eca-rule | workflow-definition
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of individual the plan definition is focused on
    # Subject Reference
    subjectReference: Optional[Reference] = None  # Type of individual the plan definition is focused on
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Purpose
    purpose: Optional[str] = None  # Why this plan definition is defined (inherited from CanonicalResource)
    # Usage
    usage: Optional[str] = None  # Describes the clinical usage of the plan definition
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the plan definition was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the plan definition is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the plan definition (inherited from MetadataResource)
    # Author
    author: List[Reference] = field(default_factory=list)  # Who authored the content (inherited from MetadataResource)
    # Editor
    editor: List[Reference] = field(default_factory=list)  # Who edited the content (inherited from MetadataResource)
    # Reviewer
    reviewer: List[Reference] = field(default_factory=list)  # Who reviewed the content (inherited from MetadataResource)
    # Endorser
    endorser: List[Reference] = field(default_factory=list)  # Who endorsed the content (inherited from MetadataResource)
    # Related Artifact
    relatedArtifact: List[RelatedArtifact] = field(default_factory=list)  # Additional documentation, citations, etc. (inherited from MetadataResource)
    # Library
    library: List[str] = field(default_factory=list)  # Logic used by the plan definition (canonical references)
    # Goal
    goal: List[PlanDefinitionGoal] = field(default_factory=list)  # What the plan is trying to accomplish
    # Action
    action: List[PlanDefinitionAction] = field(default_factory=list)  # Action defined by the plan

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

