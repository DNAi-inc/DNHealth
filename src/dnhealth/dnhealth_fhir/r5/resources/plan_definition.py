# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 PlanDefinition resource.

This resource allows for the definition of various types of plans as a sharable, consumable, and executable artifact. The resource is general enough to support the description of a broad range of clinical and non-clinical artifacts such as clinical decision support rules, order sets, protocols, and drug quality specifications.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Age, BackboneElement, CodeableConcept, Coding, ContactDetail, DataRequirement, Duration, Expression, Extension, Identifier, Period, Quantity, Range, Ratio, Reference, RelatedArtifact, Timing, TriggerDefinition, UsageContext
from typing import Any, List, Optional

@dataclass
class PlanDefinitionGoal:
    """
    PlanDefinitionGoal nested class.
    """

    description: Optional[CodeableConcept] = None  # Human-readable and/or coded description of a specific desired objective of care, such as \"contro...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # Indicates a category the goal falls within.
    priority: Optional[CodeableConcept] = None  # Identifies the expected level of importance associated with reaching/sustaining the defined goal.
    start: Optional[CodeableConcept] = None  # The event after which the goal should begin being pursued.
    addresses: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies problems, conditions, issues, or concerns the goal is intended to address.
    documentation: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Didactic or other informational resources associated with the goal that provide further supportin...
    target: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates what should be done and within what timeframe.
    measure: Optional[CodeableConcept] = None  # The parameter whose value is to be tracked, e.g. body weight, blood pressure, or hemoglobin A1c l...
    detail: Optional[Any] = None  # The target value of the measure to be achieved to signify fulfillment of the goal, e.g. 150 pound...
    due: Optional[Duration] = None  # Indicates the timeframe after the start of the goal in which the goal should be met.

@dataclass
class PlanDefinitionGoalTarget:
    """
    PlanDefinitionGoalTarget nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    measure: Optional[CodeableConcept] = None  # The parameter whose value is to be tracked, e.g. body weight, blood pressure, or hemoglobin A1c l...
    detail: Optional[Any] = None  # The target value of the measure to be achieved to signify fulfillment of the goal, e.g. 150 pound...
    due: Optional[Duration] = None  # Indicates the timeframe after the start of the goal in which the goal should be met.

@dataclass
class PlanDefinitionActor:
    """
    PlanDefinitionActor nested class.
    """

    option: List[BackboneElement] = field(default_factory=list)  # The characteristics of the candidates that could serve as the actor.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # A descriptive label for the actor.
    description: Optional[str] = None  # A description of how the actor fits into the overall actions of the plan definition.
    type: Optional[str] = None  # The type of participant in the action.
    typeCanonical: Optional[str] = None  # The type of participant in the action.
    typeReference: Optional[Reference] = None  # The type of participant in the action.
    role: Optional[CodeableConcept] = None  # The role the participant should play in performing the described action.

@dataclass
class PlanDefinitionActorOption:
    """
    PlanDefinitionActorOption nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[str] = None  # The type of participant in the action.
    typeCanonical: Optional[str] = None  # The type of participant in the action.
    typeReference: Optional[Reference] = None  # The type of participant in the action.
    role: Optional[CodeableConcept] = None  # The role the participant should play in performing the described action.

@dataclass
class PlanDefinitionAction:
    """
    PlanDefinitionAction nested class.
    """

    kind: Optional[str] = None  # The kind of condition.
    targetId: Optional[str] = None  # The element id of the target related action.
    relationship: Optional[str] = None  # The relationship of the start of this action to the related action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # An identifier that is unique within the PlanDefinition to allow linkage within the realized CareP...
    prefix: Optional[str] = None  # A user-visible prefix for the action. For example a section or item numbering such as 1. or A.
    title: Optional[str] = None  # The textual description of the action displayed to a user. For example, when the action is a test...
    description: Optional[str] = None  # A brief description of the action used to provide a summary to display to the user.
    textEquivalent: Optional[str] = None  # A text equivalent of the action to be performed. This provides a human-interpretable description ...
    priority: Optional[str] = None  # Indicates how quickly the action should be addressed with respect to other actions.
    code: Optional[CodeableConcept] = None  # A code that provides a meaning, grouping, or classification for the action or action group. For e...
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # A description of why this action is necessary or appropriate.
    documentation: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Didactic or other informational resources associated with the action that can be provided to the ...
    goalId: Optional[List[str]] = field(default_factory=list)  # Identifies goals that this action supports. The reference must be to a goal element defined withi...
    subject: Optional[Any] = None  # A code, group definition, or canonical reference that describes the intended subject of the actio...
    trigger: Optional[List[TriggerDefinition]] = field(default_factory=list)  # A description of when the action should be triggered. When multiple triggers are specified on an ...
    condition: Optional[List[BackboneElement]] = field(default_factory=list)  # An expression that describes applicability criteria or start/stop conditions for the action.
    expression: Optional[Expression] = None  # An expression that returns true or false, indicating whether the condition is satisfied.
    input: Optional[List[BackboneElement]] = field(default_factory=list)  # Defines input data requirements for the action.
    requirement: Optional[DataRequirement] = None  # Defines the data that is to be provided as input to the action.
    relatedData: Optional[str] = None  # Points to an existing input or output element that provides data to this input.
    output: Optional[List[BackboneElement]] = field(default_factory=list)  # Defines the outputs of the action, if any.
    relatedAction: Optional[List[BackboneElement]] = field(default_factory=list)  # A relationship to another action such as \"before\" or \"30-60 minutes after start of\".
    endRelationship: Optional[str] = None  # The relationship of the end of this action to the related action.
    offset: Optional[Any] = None  # A duration or range of durations to apply to the relationship. For example, 30-60 minutes before.
    timing: Optional[Any] = None  # An optional value describing when the action should be performed.
    location: Optional[Any] = None  # Identifies the facility where the action will occur; e.g. home, hospital, specific clinic, etc.
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who should participate in performing the action described.
    actorId: Optional[str] = None  # A reference to the id element of the actor who will participate in this action.
    type: Optional[str] = None  # The type of participant in the action.
    typeCanonical: Optional[str] = None  # The type of participant in the action.
    typeReference: Optional[Reference] = None  # The type of participant in the action.
    role: Optional[CodeableConcept] = None  # The role the participant should play in performing the described action.
    function: Optional[CodeableConcept] = None  # Indicates how the actor will be involved in the action - author, reviewer, witness, etc.
    groupingBehavior: Optional[str] = None  # Defines the grouping behavior for the action and its children.
    selectionBehavior: Optional[str] = None  # Defines the selection behavior for the action and its children.
    requiredBehavior: Optional[str] = None  # Defines the required behavior for the action.
    precheckBehavior: Optional[str] = None  # Defines whether the action should usually be preselected.
    cardinalityBehavior: Optional[str] = None  # Defines whether the action can be selected multiple times.
    definition: Optional[Any] = None  # A reference to an ActivityDefinition that describes the action to be taken in detail, a MessageDe...
    transform: Optional[str] = None  # A reference to a StructureMap resource that defines a transform that can be executed to produce t...
    dynamicValue: Optional[List[BackboneElement]] = field(default_factory=list)  # Customizations that should be applied to the statically defined resource. For example, if the dos...
    path: Optional[str] = None  # The path to the element to be customized. This is the path on the resource that will hold the res...
    action: Optional[List[Any]] = field(default_factory=list)  # Sub actions that are contained within the action. The behavior of this action determines the func...

@dataclass
class PlanDefinitionActionCondition:
    """
    PlanDefinitionActionCondition nested class.
    """

    kind: Optional[str] = None  # The kind of condition.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    expression: Optional[Expression] = None  # An expression that returns true or false, indicating whether the condition is satisfied.

@dataclass
class PlanDefinitionActionInput:
    """
    PlanDefinitionActionInput nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # A human-readable label for the data requirement used to label data flows in BPMN or similar diagr...
    requirement: Optional[DataRequirement] = None  # Defines the data that is to be provided as input to the action.
    relatedData: Optional[str] = None  # Points to an existing input or output element that provides data to this input.

@dataclass
class PlanDefinitionActionOutput:
    """
    PlanDefinitionActionOutput nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # A human-readable label for the data requirement used to label data flows in BPMN or similar diagr...
    requirement: Optional[DataRequirement] = None  # Defines the data that results as output from the action.
    relatedData: Optional[str] = None  # Points to an existing input or output element that is results as output from the action.

@dataclass
class PlanDefinitionActionRelatedAction:
    """
    PlanDefinitionActionRelatedAction nested class.
    """

    targetId: Optional[str] = None  # The element id of the target related action.
    relationship: Optional[str] = None  # The relationship of the start of this action to the related action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    endRelationship: Optional[str] = None  # The relationship of the end of this action to the related action.
    offset: Optional[Any] = None  # A duration or range of durations to apply to the relationship. For example, 30-60 minutes before.

@dataclass
class PlanDefinitionActionParticipant:
    """
    PlanDefinitionActionParticipant nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    actorId: Optional[str] = None  # A reference to the id element of the actor who will participate in this action.
    type: Optional[str] = None  # The type of participant in the action.
    typeCanonical: Optional[str] = None  # The type of participant in the action.
    typeReference: Optional[Reference] = None  # The type of participant in the action.
    role: Optional[CodeableConcept] = None  # The role the participant should play in performing the described action.
    function: Optional[CodeableConcept] = None  # Indicates how the actor will be involved in the action - author, reviewer, witness, etc.

@dataclass
class PlanDefinitionActionDynamicValue:
    """
    PlanDefinitionActionDynamicValue nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    path: Optional[str] = None  # The path to the element to be customized. This is the path on the resource that will hold the res...
    expression: Optional[Expression] = None  # An expression specifying the value of the customized element.


@dataclass
class PlanDefinition(FHIRResource):
    """
    This resource allows for the definition of various types of plans as a sharable, consumable, and executable artifact. The resource is general enough to support the description of a broad range of clinical and non-clinical artifacts such as clinical decision support rules, order sets, protocols, and drug quality specifications.
    """

    status: Optional[str] = None  # The status of this plan definition. Enables tracking the life-cycle of the content.
    resourceType: str = "PlanDefinition"
    url: Optional[str] = None  # An absolute URI that is used to identify this plan definition when it is referenced in a specific...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this plan definition when it is represented in other...
    version: Optional[str] = None  # The identifier that is used to identify this version of the plan definition when it is referenced...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the plan definition. This name should be usable as an identif...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the plan definition.
    subtitle: Optional[str] = None  # An explanatory or alternate title for the plan definition giving additional information about its...
    type: Optional[CodeableConcept] = None  # A high-level category for the plan definition that distinguishes the kinds of systems that would ...
    experimental: Optional[bool] = None  # A Boolean value to indicate that this plan definition is authored for testing purposes (or educat...
    subject: Optional[Any] = None  # A code, group definition, or canonical reference that describes  or identifies the intended subje...
    date: Optional[str] = None  # The date  (and optionally time) when the plan definition was last significantly changed. The date...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the plan definition from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the plan definition is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this plan definition is needed and why it has been designed as it has.
    usage: Optional[str] = None  # A detailed description of how the plan definition is used from a clinical perspective.
    copyright: Optional[str] = None  # A copyright statement relating to the plan definition and/or its contents. Copyright statements a...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    approvalDate: Optional[str] = None  # The date on which the resource content was approved by the publisher. Approval happens once when ...
    lastReviewDate: Optional[str] = None  # The date on which the resource content was last reviewed. Review happens periodically after appro...
    effectivePeriod: Optional[Period] = None  # The period during which the plan definition content was or is planned to be in active use.
    topic: Optional[List[CodeableConcept]] = field(default_factory=list)  # Descriptive topics related to the content of the plan definition. Topics provide a high-level cat...
    author: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual or organization primarily involved in the creation and maintenance of the content.
    editor: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization primarily responsible for internal coherence of the content.
    reviewer: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization asserted by the publisher to be primarily responsible for review of...
    endorser: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization asserted by the publisher to be responsible for officially endorsin...
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Related artifacts such as additional documentation, justification, or bibliographic references.
    library: Optional[List[str]] = field(default_factory=list)  # A reference to a Library resource containing any formal logic used by the plan definition.
    goal: Optional[List[BackboneElement]] = field(default_factory=list)  # A goal describes an expected outcome that activities within the plan are intended to achieve. For...
    actor: Optional[List[BackboneElement]] = field(default_factory=list)  # Actors represent the individuals or groups involved in the execution of the defined set of activi...
    action: Optional[List[BackboneElement]] = field(default_factory=list)  # An action or group of actions to be taken as part of the plan. For example, in clinical care, an ...
    asNeeded: Optional[Any] = None  # If a CodeableConcept is present, it indicates the pre-condition for performing the service.  For ...