# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 RequestOrchestration resource.

Defines a RequestOrchestration that can represent a CDS Hooks response
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Age, Annotation, BackboneElement, CodeableConcept, DataRequirement, Duration, Expression, Extension, Identifier, Period, Range, Reference, RelatedArtifact, Timing
from typing import Any, List, Optional

@dataclass
class RequestOrchestrationAction:
    """
    RequestOrchestrationAction nested class.
    """

    kind: Optional[str] = None  # The kind of condition.
    targetId: Optional[str] = None  # The element id of the target related action.
    relationship: Optional[str] = None  # The relationship of this action to the related action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # The linkId of the action from the PlanDefinition that corresponds to this action in the RequestOr...
    prefix: Optional[str] = None  # A user-visible prefix for the action. For example a section or item numbering such as 1. or A.
    title: Optional[str] = None  # The title of the action displayed to a user.
    description: Optional[str] = None  # A short description of the action used to provide a summary to display to the user.
    textEquivalent: Optional[str] = None  # A text equivalent of the action to be performed. This provides a human-interpretable description ...
    priority: Optional[str] = None  # Indicates how quickly the action should be addressed with respect to other actions.
    code: Optional[List[CodeableConcept]] = field(default_factory=list)  # A code that provides meaning for the action or action group. For example, a section may have a LO...
    documentation: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Didactic or other informational resources associated with the action that can be provided to the ...
    goal: Optional[List[Reference]] = field(default_factory=list)  # Goals that are intended to be achieved by following the requests in this action.
    condition: Optional[List[BackboneElement]] = field(default_factory=list)  # An expression that describes applicability criteria, or start/stop conditions for the action.
    expression: Optional[Expression] = None  # An expression that returns true or false, indicating whether or not the condition is satisfied.
    input: Optional[List[BackboneElement]] = field(default_factory=list)  # Defines input data requirements for the action.
    requirement: Optional[DataRequirement] = None  # Defines the data that is to be provided as input to the action.
    relatedData: Optional[str] = None  # Points to an existing input or output element that provides data to this input.
    output: Optional[List[BackboneElement]] = field(default_factory=list)  # Defines the outputs of the action, if any.
    relatedAction: Optional[List[BackboneElement]] = field(default_factory=list)  # A relationship to another action such as \"before\" or \"30-60 minutes after start of\".
    endRelationship: Optional[str] = None  # The relationship of the end of this action to the related action.
    offset: Optional[Any] = None  # A duration or range of durations to apply to the relationship. For example, 30-60 minutes before.
    timing: Optional[Any] = None  # An optional value describing when the action should be performed.
    location: Optional[Any] = None  # Identifies the facility where the action will occur; e.g. home, hospital, specific clinic, etc.
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # The participant that should perform or be responsible for this action.
    type: Optional[str] = None  # The type of participant in the action.
    typeCanonical: Optional[str] = None  # The type of participant in the action.
    typeReference: Optional[Reference] = None  # The type of participant in the action.
    role: Optional[CodeableConcept] = None  # The role the participant should play in performing the described action.
    function: Optional[CodeableConcept] = None  # Indicates how the actor will be involved in the action - author, reviewer, witness, etc.
    actor: Optional[Any] = None  # A reference to the actual participant.
    groupingBehavior: Optional[str] = None  # Defines the grouping behavior for the action and its children.
    selectionBehavior: Optional[str] = None  # Defines the selection behavior for the action and its children.
    requiredBehavior: Optional[str] = None  # Defines expectations around whether an action is required.
    precheckBehavior: Optional[str] = None  # Defines whether the action should usually be preselected.
    cardinalityBehavior: Optional[str] = None  # Defines whether the action can be selected multiple times.
    resource: Optional[Reference] = None  # The resource that is the target of the action (e.g. CommunicationRequest).
    definition: Optional[Any] = None  # A reference to an ActivityDefinition that describes the action to be taken in detail, a PlanDefin...
    transform: Optional[str] = None  # A reference to a StructureMap resource that defines a transform that can be executed to produce t...
    dynamicValue: Optional[List[BackboneElement]] = field(default_factory=list)  # Customizations that should be applied to the statically defined resource. For example, if the dos...
    path: Optional[str] = None  # The path to the element to be customized. This is the path on the resource that will hold the res...
    action: Optional[List[Any]] = field(default_factory=list)  # Sub actions.

@dataclass
class RequestOrchestrationActionCondition:
    """
    RequestOrchestrationActionCondition nested class.
    """

    kind: Optional[str] = None  # The kind of condition.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    expression: Optional[Expression] = None  # An expression that returns true or false, indicating whether or not the condition is satisfied.

@dataclass
class RequestOrchestrationActionInput:
    """
    RequestOrchestrationActionInput nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # A human-readable label for the data requirement used to label data flows in BPMN or similar diagr...
    requirement: Optional[DataRequirement] = None  # Defines the data that is to be provided as input to the action.
    relatedData: Optional[str] = None  # Points to an existing input or output element that provides data to this input.

@dataclass
class RequestOrchestrationActionOutput:
    """
    RequestOrchestrationActionOutput nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # A human-readable label for the data requirement used to label data flows in BPMN or similar diagr...
    requirement: Optional[DataRequirement] = None  # Defines the data that results as output from the action.
    relatedData: Optional[str] = None  # Points to an existing input or output element that is results as output from the action.

@dataclass
class RequestOrchestrationActionRelatedAction:
    """
    RequestOrchestrationActionRelatedAction nested class.
    """

    targetId: Optional[str] = None  # The element id of the target related action.
    relationship: Optional[str] = None  # The relationship of this action to the related action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    endRelationship: Optional[str] = None  # The relationship of the end of this action to the related action.
    offset: Optional[Any] = None  # A duration or range of durations to apply to the relationship. For example, 30-60 minutes before.

@dataclass
class RequestOrchestrationActionParticipant:
    """
    RequestOrchestrationActionParticipant nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[str] = None  # The type of participant in the action.
    typeCanonical: Optional[str] = None  # The type of participant in the action.
    typeReference: Optional[Reference] = None  # The type of participant in the action.
    role: Optional[CodeableConcept] = None  # The role the participant should play in performing the described action.
    function: Optional[CodeableConcept] = None  # Indicates how the actor will be involved in the action - author, reviewer, witness, etc.
    actor: Optional[Any] = None  # A reference to the actual participant.

@dataclass
class RequestOrchestrationActionDynamicValue:
    """
    RequestOrchestrationActionDynamicValue nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    path: Optional[str] = None  # The path to the element to be customized. This is the path on the resource that will hold the res...
    expression: Optional[Expression] = None  # An expression specifying the value of the customized element.


@dataclass
class RequestOrchestration(FHIRResource):
    """
    Defines a RequestOrchestration that can represent a CDS Hooks response
    """

    identifier: Optional[Identifier] = None  # Allows a service to provide a unique, business identifier for the request.
    instantiatesUri: Optional[str] = None  # A URL referencing an externally defined protocol, guideline, orderset or other definition that is...
    status: Optional[str] = None  # The current state of the request. For request orchestrations, the status reflects the status of a...
    intent: Optional[str] = None  # Indicates the level of authority/intentionality associated with the request and where the request...
    resourceType: str = "RequestOrchestration"
    instantiatesCanonical: Optional[List[str]] = field(default_factory=list)  # A canonical URL referencing a FHIR-defined protocol, guideline, orderset or other definition that...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan, proposal or order that is fulfilled in whole or in part by this request.
    replaces: Optional[List[Reference]] = field(default_factory=list)  # Completed or terminated request(s) whose function is taken by this new request.
    groupIdentifier: Optional[Identifier] = None  # A shared identifier common to multiple independent Request instances that were activated/authoriz...
    priority: Optional[str] = None  # Indicates how quickly the request should be addressed with respect to other requests.
    code: Optional[CodeableConcept] = None  # A code that identifies what the overall request orchestration is.
    subject: Optional[Reference] = None  # The subject for which the request orchestration was created.
    encounter: Optional[Reference] = None  # Describes the context of the request orchestration, if any.
    authoredOn: Optional[str] = None  # Indicates when the request orchestration was created.
    author: Optional[Reference] = None  # Provides a reference to the author of the request orchestration.
    reason: Optional[List[Any]] = field(default_factory=list)  # Describes the reason for the request orchestration in coded or textual form.
    goal: Optional[List[Reference]] = field(default_factory=list)  # Goals that are intended to be achieved by following the requests in this RequestOrchestration.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Provides a mechanism to communicate additional information about the response.
    action: Optional[List[BackboneElement]] = field(default_factory=list)  # The actions, if any, produced by the evaluation of the artifact.