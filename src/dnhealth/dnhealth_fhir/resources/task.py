# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Task resource.

Complete Task resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Period,
)


@dataclass
class TaskInput:
    """
    Task inputs.
    
    Additional information that may be needed in the execution of the task.
    """

    type: CodeableConcept  # Label for the input (required)
    valueBase64Binary: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueCanonical: Optional[str] = None
    valueCode: Optional[str] = None
    valueDate: Optional[str] = None
    valueDateTime: Optional[str] = None
    valueDecimal: Optional[float] = None
    valueId: Optional[str] = None
    valueInstant: Optional[str] = None
    valueInteger: Optional[int] = None
    valueMarkdown: Optional[str] = None
    valueOid: Optional[str] = None
    valuePositiveInt: Optional[int] = None
    valueString: Optional[str] = None
    valueTime: Optional[str] = None
    valueUnsignedInt: Optional[int] = None
    valueUri: Optional[str] = None
    valueUrl: Optional[str] = None
    valueUuid: Optional[str] = None
    valueAddress: Optional[Any] = None
    valueAge: Optional[Any] = None
    valueAnnotation: Optional[Any] = None
    valueAttachment: Optional[Any] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueCoding: Optional[Any] = None
    valueContactPoint: Optional[Any] = None
    valueCount: Optional[Any] = None
    valueDistance: Optional[Any] = None
    valueDuration: Optional[Any] = None
    valueHumanName: Optional[Any] = None
    valueIdentifier: Optional[Any] = None
    valueMoney: Optional[Any] = None
    valuePeriod: Optional[Period] = None
    valueQuantity: Optional[Any] = None
    valueRange: Optional[Any] = None
    valueRatio: Optional[Any] = None
    valueReference: Optional[Reference] = None
    valueSampledData: Optional[Any] = None
    valueSignature: Optional[Any] = None
    valueTiming: Optional[Any] = None
    valueContactDetail: Optional[Any] = None
    valueContributor: Optional[Any] = None
    valueDataRequirement: Optional[Any] = None
    valueExpression: Optional[Any] = None
    valueParameterDefinition: Optional[Any] = None
    valueRelatedArtifact: Optional[Any] = None
    valueTriggerDefinition: Optional[Any] = None
    valueUsageContext: Optional[Any] = None
    valueDosage: Optional[Any] = None
    valueMeta: Optional[Any] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class TaskOutput:
    """
    Task outputs.
    
    Outputs produced by the Task.
    """

    type: CodeableConcept  # Label for the output (required)
    valueBase64Binary: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueCanonical: Optional[str] = None
    valueCode: Optional[str] = None
    valueDate: Optional[str] = None
    valueDateTime: Optional[str] = None
    valueDecimal: Optional[float] = None
    valueId: Optional[str] = None
    valueInstant: Optional[str] = None
    valueInteger: Optional[int] = None
    valueMarkdown: Optional[str] = None
    valueOid: Optional[str] = None
    valuePositiveInt: Optional[int] = None
    valueString: Optional[str] = None
    valueTime: Optional[str] = None
    valueUnsignedInt: Optional[int] = None
    valueUri: Optional[str] = None
    valueUrl: Optional[str] = None
    valueUuid: Optional[str] = None
    valueAddress: Optional[Any] = None
    valueAge: Optional[Any] = None
    valueAnnotation: Optional[Any] = None
    valueAttachment: Optional[Any] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueCoding: Optional[Any] = None
    valueContactPoint: Optional[Any] = None
    valueCount: Optional[Any] = None
    valueDistance: Optional[Any] = None
    valueDuration: Optional[Any] = None
    valueHumanName: Optional[Any] = None
    valueIdentifier: Optional[Any] = None
    valueMoney: Optional[Any] = None
    valuePeriod: Optional[Period] = None
    valueQuantity: Optional[Any] = None
    valueRange: Optional[Any] = None
    valueRatio: Optional[Any] = None
    valueReference: Optional[Reference] = None
    valueSampledData: Optional[Any] = None
    valueSignature: Optional[Any] = None
    valueTiming: Optional[Any] = None
    valueContactDetail: Optional[Any] = None
    valueContributor: Optional[Any] = None
    valueDataRequirement: Optional[Any] = None
    valueExpression: Optional[Any] = None
    valueParameterDefinition: Optional[Any] = None
    valueRelatedArtifact: Optional[Any] = None
    valueTriggerDefinition: Optional[Any] = None
    valueUsageContext: Optional[Any] = None
    valueDosage: Optional[Any] = None
    valueMeta: Optional[Any] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class TaskRestriction:
    """
    Constraints on fulfillment tasks.
    """

    repetitions: Optional[int] = None
    period: Optional[Period] = None
    recipient: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Task(FHIRResource):
    """
    FHIR R4 Task resource.

    Represents a task to be performed.
    """

    resourceType: str = "Task"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Instantiates canonical
    instantiatesCanonical: Optional[str] = None
    # Instantiates URI
    instantiatesUri: Optional[str] = None
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Group identifier
    groupIdentifier: Optional[Identifier] = None
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    status: str  # draft | requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error (required)
    # Status reason
    statusReason: Optional[CodeableConcept] = None
    # Business status
    businessStatus: Optional[CodeableConcept] = None
    # Intent
    intent: str  # unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option (required)
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Code
    code: Optional[CodeableConcept] = None
    # Description
    description: Optional[str] = None
    # Focus
    focus: Optional[Reference] = None
    # For
    for_: Optional[Reference] = None  # for is a Python keyword, so use for_
    # Encounter
    encounter: Optional[Reference] = None
    # Execution period
    executionPeriod: Optional[Period] = None
    # Authored on
    authoredOn: Optional[str] = None  # ISO 8601 dateTime
    # Last modified
    lastModified: Optional[str] = None  # ISO 8601 dateTime
    # Requester
    requester: Optional[Reference] = None
    # Performer type
    performerType: List[CodeableConcept] = field(default_factory=list)
    # Owner
    owner: Optional[Reference] = None
    # Location
    location: Optional[Reference] = None
    # Reason code
    reasonCode: Optional[CodeableConcept] = None
    # Reason reference
    reasonReference: Optional[Reference] = None
    # Insurance
    insurance: List[Reference] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Relevant history
    relevantHistory: List[Reference] = field(default_factory=list)
    # Restriction
    restriction: Optional[TaskRestriction] = None
    # Input
    input: List[TaskInput] = field(default_factory=list)
    # Output
    output: List[TaskOutput] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
