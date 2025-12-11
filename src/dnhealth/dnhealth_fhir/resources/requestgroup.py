# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 RequestGroup resource.

RequestGroup represents a group of related requests.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Annotation,
)


@dataclass
class RequestGroupAction:
    """
    FHIR RequestGroup.action complex type.
    
    The actions, if any, produced by the evaluation of the artifact.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    prefix: Optional[str] = None  # User-visible prefix for the action
    title: Optional[str] = None  # User-visible title
    description: Optional[str] = None  # Short description of the action
    textEquivalent: Optional[str] = None  # Static text equivalent of the action
    priority: Optional[str] = None  # routine | urgent | asap | stat
    code: List[CodeableConcept] = field(default_factory=list)  # The meaning of the action
    documentation: List[Any] = field(default_factory=list)  # Supporting documentation (RelatedArtifact)
    condition: List["RequestGroupActionCondition"] = field(default_factory=list)  # Whether or not the action is applicable
    relatedAction: List["RequestGroupActionRelatedAction"] = field(default_factory=list)  # Relationship to another action
    timingDateTime: Optional[str] = None  # When the action should take place
    timingAge: Optional[Any] = None  # When the action should take place (Age)
    timingPeriod: Optional[Any] = None  # When the action should take place (Period)
    timingDuration: Optional[Any] = None  # When the action should take place (Duration)
    timingRange: Optional[Any] = None  # When the action should take place (Range)
    timingTiming: Optional[Any] = None  # When the action should take place (Timing)
    participant: List[Reference] = field(default_factory=list)  # Who should perform the action
    type: Optional[CodeableConcept] = None  # create | update | remove | fire-event
    groupingBehavior: Optional[str] = None  # visual-group | logical-group | sentence-group
    selectionBehavior: Optional[str] = None  # any | all | all-or-none | exactly-one | at-most-one | one-or-more
    requiredBehavior: Optional[str] = None  # must | could | must-unless-documented
    precheckBehavior: Optional[str] = None  # yes | no
    cardinalityBehavior: Optional[str] = None  # single | multiple
    resource: Optional[Reference] = None  # The target of the action
    action: List["RequestGroupAction"] = field(default_factory=list)  # Sub actions


@dataclass
class RequestGroupActionCondition:
    """
    FHIR RequestGroup.action.condition complex type.
    
    Whether or not the action is applicable.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    kind: str  # applicability | start | stop (required)
    expression: Optional[Any] = None  # Boolean-valued expression (Expression)


@dataclass
class RequestGroupActionRelatedAction:
    """
    FHIR RequestGroup.action.relatedAction complex type.
    
    Relationship to another action.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    actionId: str  # What action this is related to (required)
    relationship: str  # before-start | before | before-end | concurrent-with-start | concurrent | concurrent-with-end | after-start | after | after-end (required)
    offsetDuration: Optional[Any] = None  # Time offset for the relationship (Duration)
    offsetRange: Optional[Any] = None  # Time offset for the relationship (Range)


@dataclass
class RequestGroup(DomainResource):
    """
    FHIR R4 RequestGroup resource.
    
    Represents a group of related requests.
    Extends DomainResource.
    """
    
    resourceType: str = "RequestGroup"
    # Required fields (must come before optional fields in dataclasses)
    status: str  # draft | active | on-hold | revoked | completed | entered-in-error | unknown (required)
    intent: str  # proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option (required)
    priority: str  # routine | urgent | asap | stat (required)
    # Optional fields (with defaults)
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    instantiatesCanonical: List[str] = field(default_factory=list)  # Instantiates FHIR protocol or definition (canonical references)
    instantiatesUri: List[str] = field(default_factory=list)  # Instantiates external protocol or definition (URIs)
    basedOn: List[Reference] = field(default_factory=list)  # Fulfills plan, proposal, or order
    replaces: List[Reference] = field(default_factory=list)  # Request(s) replaced by this request
    groupIdentifier: Optional[Identifier] = None  # Composite request this is part of
    # Code
    code: Optional[CodeableConcept] = None  # What's being requested/ordered
    # Subject
    subject: Optional[Reference] = None  # Who the request group is about
    # Encounter
    encounter: Optional[Reference] = None  # Encounter request created during
    # Authored On
    authoredOn: Optional[str] = None  # When the request group was authored
    # Author
    author: Optional[Reference] = None  # Device or practitioner that authored the request group
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why the request group is needed
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why the request group is needed
    # Note
    note: List[Annotation] = field(default_factory=list)  # Additional notes about the response
    # Action
    action: List[RequestGroupAction] = field(default_factory=list)  # The actions, if any, produced by the evaluation of the artifact

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

