# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ExampleScenario resource.

ExampleScenario represents example scenarios for testing and documentation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, ContactDetail, UsageContext, RelatedArtifact


@dataclass
class ExampleScenarioActor:
    """
    FHIR ExampleScenario.actor complex type.
    
    Actor participating in the scenario.
    """
    
    actorId: str  # ID or acronym of the actor (required)
    type: str  # person | entity (required)
    name: Optional[str] = None  # Name of the actor
    description: Optional[str] = None  # Description of the actor
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioInstance:
    """
    FHIR ExampleScenario.instance complex type.
    
    Each resource and each version that is present in the workflow.
    """
    
    resourceId: str  # ID of the resource for referencing (required)
    resourceType: str  # The type of the resource (required)
    name: Optional[str] = None  # A short name for the instance resource
    description: Optional[str] = None  # Human-readable description of the instance resource
    version: List["ExampleScenarioInstanceVersion"] = field(default_factory=list)  # A specific version of the resource
    containedInstance: List["ExampleScenarioInstanceContainedInstance"] = field(default_factory=list)  # Resources contained in the instance
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioInstanceVersion:
    """
    FHIR ExampleScenario.instance.version complex type.
    
    A specific version of the resource.
    """
    
    versionId: str  # ID of the version of the resource (required)
    description: str  # Description of the resource version (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioInstanceContainedInstance:
    """
    FHIR ExampleScenario.instance.containedInstance complex type.
    
    Resources contained in the instance.
    """
    
    resourceId: str  # Each resource contained in the instance (required)
    versionId: Optional[str] = None  # A specific version of a resource contained in the instance
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioProcess:
    """
    FHIR ExampleScenario.process complex type.
    
    Each major process - a group of operations.
    """
    
    title: str  # The diagram title of the group of operations (required)
    description: Optional[str] = None  # A longer description of the group of operations
    preConditions: Optional[str] = None  # Description of initial status before the process starts
    postConditions: Optional[str] = None  # Description of final status after the process completed
    step: List["ExampleScenarioProcessStep"] = field(default_factory=list)  # Each step of the process
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioProcessStep:
    """
    FHIR ExampleScenario.process.step complex type.
    
    Each step of the process.
    """
    
    process: List["ExampleScenarioProcess"] = field(default_factory=list)  # Nested process
    pause: Optional[bool] = None  # If there is a pause in the flow
    operation: Optional["ExampleScenarioProcessStepOperation"] = None  # Each interaction or action
    alternative: List["ExampleScenarioProcessStepAlternative"] = field(default_factory=list)  # Indicates an alternative step that can be taken instead of the base step
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioProcessStepOperation:
    """
    FHIR ExampleScenario.process.step.operation complex type.
    
    Each interaction or action.
    """
    
    number: str  # The sequential number of the interaction (required)
    type: Optional[str] = None  # The type of operation - HTTP verb
    name: Optional[str] = None  # The human-friendly name of the interaction
    initiator: Optional[str] = None  # Who starts the transaction
    receiver: Optional[str] = None  # Who receives the transaction
    description: Optional[str] = None  # A comment to be inserted in the diagram
    initiatorActive: Optional[bool] = None  # Whether the initiator is deactivated right after the transaction
    receiverActive: Optional[bool] = None  # Whether the receiver is deactivated right after the transaction
    request: Optional["ExampleScenarioInstanceContainedInstance"] = None  # Each resource instance used by the initiator
    response: Optional["ExampleScenarioInstanceContainedInstance"] = None  # Each resource instance used by the responder
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenarioProcessStepAlternative:
    """
    FHIR ExampleScenario.process.step.alternative complex type.
    
    Indicates an alternative step that can be taken instead of the base step.
    """
    
    title: str  # Label for alternative (required)
    description: Optional[str] = None  # A human-readable description of the alternative option
    step: List["ExampleScenarioProcessStep"] = field(default_factory=list)  # What happens in each alternative option
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ExampleScenario(MetadataResource):
    """
    FHIR R4 ExampleScenario resource.
    
    Represents example scenarios for testing and documentation.
    Extends MetadataResource.
    """
    
    resourceType: str = "ExampleScenario"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this example scenario (inherited from CanonicalResource)
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the example scenario was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the example scenario is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the ExampleScenario (inherited from MetadataResource)
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
    # Actor
    actor: List[ExampleScenarioActor] = field(default_factory=list)  # Actor participating in the scenario
    # Instance
    instance: List[ExampleScenarioInstance] = field(default_factory=list)  # Each resource and each version that is present in the workflow
    # Process
    process: List[ExampleScenarioProcess] = field(default_factory=list)  # Each major process - a group of operations
    # Workflow
    workflow: List[str] = field(default_factory=list)  # Another nested scenario

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


