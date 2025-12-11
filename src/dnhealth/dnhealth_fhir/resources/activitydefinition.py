# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ActivityDefinition resource.

ActivityDefinition describes the kind of activity that can be performed.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, ContactDetail, UsageContext, Period, Timing, Quantity, Range


@dataclass
class ActivityDefinitionParticipant:
    """
    FHIR ActivityDefinition.participant complex type.
    
    Indicates who should participate in performing the action described.
    """
    
    type: str  # patient | practitioner | related-person | device (required)
    role: Optional[CodeableConcept] = None  # E.g., nurse, physician, etc.
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ActivityDefinitionDynamicValue:
    """
    FHIR ActivityDefinition.dynamicValue complex type.
    
    Dynamic values that will be evaluated to produce values for elements of the resulting resource.
    """
    
    path: str  # The path to the element to be set dynamically (required)
    expression: Optional[Any] = None  # An expression that provides the dynamic value for the element
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ActivityDefinition(MetadataResource):
    """
    FHIR R4 ActivityDefinition resource.
    
    Describes the kind of activity that can be performed.
    Extends MetadataResource.
    """
    
    resourceType: str = "ActivityDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this activity definition (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this activity definition (inherited from CanonicalResource)
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the activity definition
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of individual the activity definition is focused on
    # Subject Reference
    subjectReference: Optional[Reference] = None  # Type of individual the activity definition is focused on
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
    purpose: Optional[str] = None  # Why this activity definition is defined (inherited from CanonicalResource)
    # Usage
    usage: Optional[str] = None  # Describes the clinical usage of the activity definition
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # When last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When resource is valid (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # Topics for this resource (inherited from MetadataResource)
    # Author
    author: List[Any] = field(default_factory=list)  # Who authored the content (inherited from MetadataResource)
    # Editor
    editor: List[Any] = field(default_factory=list)  # Who edited the content (inherited from MetadataResource)
    # Reviewer
    reviewer: List[Any] = field(default_factory=list)  # Who reviewed the content (inherited from MetadataResource)
    # Endorser
    endorser: List[Any] = field(default_factory=list)  # Who endorsed the content (inherited from MetadataResource)
    # Related Artifact
    relatedArtifact: List[Any] = field(default_factory=list)  # Related artifacts (inherited from MetadataResource)
    # Library
    library: List[str] = field(default_factory=list)  # Logic used by the activity definition
    # Kind
    kind: Optional[str] = None  # procedure | medication-request | medication-list | order | plan
    # Profile
    profile: Optional[str] = None  # What profile the resource needs to conform to
    # Code
    code: Optional[CodeableConcept] = None  # Detail type of activity
    # Intent
    intent: Optional[str] = None  # proposal | plan | order | option
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Do Not Perform
    doNotPerform: Optional[bool] = None  # True if the activity should not be performed
    # Timing Timing
    timingTiming: Optional[Timing] = None  # When the activity should occur
    # Timing DateTime
    timingDateTime: Optional[str] = None  # When the activity should occur
    # Timing Age
    timingAge: Optional[Any] = None  # When the activity should occur
    # Timing Period
    timingPeriod: Optional[Period] = None  # When the activity should occur
    # Timing Range
    timingRange: Optional[Range] = None  # When the activity should occur
    # Timing Duration
    timingDuration: Optional[Any] = None  # When the activity should occur
    # Location
    location: Optional[Reference] = None  # Where it should happen
    # Participant
    participant: List[ActivityDefinitionParticipant] = field(default_factory=list)  # Who should participate
    # Product Reference
    productReference: Optional[Reference] = None  # What's administered/supplied
    # Product CodeableConcept
    productCodeableConcept: Optional[CodeableConcept] = None  # What's administered/supplied
    # Quantity
    quantity: Optional[Quantity] = None  # How much is administered/consumed/supplied
    # Dosage
    dosage: List[Any] = field(default_factory=list)  # Detailed dosage instructions (Dosage complex type)
    # Body Site
    bodySite: List[CodeableConcept] = field(default_factory=list)  # What part of body to perform on
    # Specimen Requirement
    specimenRequirement: List[Reference] = field(default_factory=list)  # What specimens are required
    # Observation Requirement
    observationRequirement: List[Reference] = field(default_factory=list)  # What observations are required
    # Observation Result Requirement
    observationResultRequirement: List[Reference] = field(default_factory=list)  # What observations must be produced
    # Transform
    transform: Optional[str] = None  # Transform to apply the template
    # Dynamic Value
    dynamicValue: List[ActivityDefinitionDynamicValue] = field(default_factory=list)  # Dynamic values to be evaluated


def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

