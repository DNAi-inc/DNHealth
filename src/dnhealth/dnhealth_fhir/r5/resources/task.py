# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Task resource.

A task to be performed.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import Address, Age, Annotation, Attachment, BackboneElement, CodeableConcept, Coding, ContactDetail, ContactPoint, Count, DataRequirement, Distance, Dosage, Duration, Expression, Extension, HumanName, Identifier, Money, ParameterDefinition, Period, Quantity, Range, Ratio, Reference, RelatedArtifact, SampledData, Signature, Timing, TriggerDefinition, UsageContext
from typing import Any, List, Optional

@dataclass
class TaskPerformer:
    """
    TaskPerformer nested class.
    """

    actor: Optional[Reference] = None  # The actor or entity who performed the task.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # A code or description of the performer of the task.

@dataclass
class TaskRestriction:
    """
    TaskRestriction nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    repetitions: Optional[int] = None  # Indicates the number of times the requested action should occur.
    period: Optional[Period] = None  # The time-period for which fulfillment is sought. This must fall within the overall time period au...
    recipient: Optional[List[Reference]] = field(default_factory=list)  # For requests that are targeted to more than one potential recipient/target, to identify who is fu...

@dataclass
class TaskInput:
    """
    TaskInput nested class.
    """

    type: Optional[CodeableConcept] = None  # A code or description indicating how the input is intended to be used as part of the task execution.
    value: Optional[Any] = None  # The value of the input parameter as a basic type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class TaskOutput:
    """
    TaskOutput nested class.
    """

    type: Optional[CodeableConcept] = None  # The name of the Output parameter.
    value: Optional[Any] = None  # The value of the Output parameter as a basic type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Task(FHIRResource):
    """
    A task to be performed.
    """

    status: Optional[str] = None  # The current status of the task.
    intent: Optional[str] = None  # Indicates the \"level\" of actionability associated with the Task, i.e. i+R[9]Cs this a proposed ...
    resourceType: str = "Task"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The business identifier for this task.
    instantiatesCanonical: Optional[str] = None  # The URL pointing to a *FHIR*-defined protocol, guideline, orderset or other definition that is ad...
    instantiatesUri: Optional[str] = None  # The URL pointing to an *externally* maintained  protocol, guideline, orderset or other definition...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # BasedOn refers to a higher-level authorization that triggered the creation of the task.  It refer...
    groupIdentifier: Optional[Identifier] = None  # A shared identifier common to multiple independent Task and Request instances that were activated...
    partOf: Optional[List[Reference]] = field(default_factory=list)  # Task that this particular task is part of.
    statusReason: Optional[Any] = None  # An explanation as to why this task is held, failed, was refused, etc.
    businessStatus: Optional[CodeableConcept] = None  # Contains business-specific nuances of the business state.
    priority: Optional[str] = None  # Indicates how quickly the Task should be addressed with respect to other requests.
    doNotPerform: Optional[bool] = None  # If true indicates that the Task is asking for the specified action to *not* occur.
    code: Optional[CodeableConcept] = None  # A name or code (or both) briefly describing what the task involves.
    description: Optional[str] = None  # A free-text description of what is to be performed.
    focus: Optional[Reference] = None  # The request being fulfilled or the resource being manipulated (changed, suspended, etc.) by this ...
    for_: Optional[Reference] = None  # The entity who benefits from the performance of the service specified in the task (e.g., the pati...
    encounter: Optional[Reference] = None  # The healthcare event  (e.g. a patient and healthcare provider interaction) during which this task...
    requestedPeriod: Optional[Period] = None  # Indicates the start and/or end of the period of time when completion of the task is desired to ta...
    executionPeriod: Optional[Period] = None  # Identifies the time action was first taken against the task (start) and/or the time final action ...
    authoredOn: Optional[str] = None  # The date and time this task was created.
    lastModified: Optional[str] = None  # The date and time of last modification to this task.
    requester: Optional[Reference] = None  # The creator of the task.
    requestedPerformer: Optional[List[Any]] = field(default_factory=list)  # The kind of participant or specific participant that should perform the task.
    owner: Optional[Reference] = None  # Party responsible for managing task execution.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # The entity who performed the requested task.
    location: Optional[Reference] = None  # Principal physical location where this task is performed.
    reason: Optional[List[Any]] = field(default_factory=list)  # A description, code, or reference indicating why this task needs to be performed.
    insurance: Optional[List[Reference]] = field(default_factory=list)  # Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be re...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Free-text information captured about the task as it progresses.
    relevantHistory: Optional[List[Reference]] = field(default_factory=list)  # Links to Provenance records for past versions of this Task that identify key state transitions or...
    restriction: Optional[BackboneElement] = None  # If the Task.focus is a request resource and the task is seeking fulfillment (i.e. is asking for t...
    input: Optional[List[BackboneElement]] = field(default_factory=list)  # Additional information that may be needed in the execution of the task.
    output: Optional[List[BackboneElement]] = field(default_factory=list)  # Outputs produced by the Task.