# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ResearchElementDefinition resource.

ResearchElementDefinition defines a research element definition.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
import logging
from datetime import datetime

from dnhealth.dnhealth_fhir.resources.base import MetadataResource

logger = logging.getLogger(__name__)
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    ContactDetail,
    UsageContext,
    RelatedArtifact,
)


@dataclass
class ResearchElementDefinitionCharacteristic:
    """
    FHIR ResearchElementDefinition.characteristic complex type.
    
    What defines the members of the research element.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    definitionCodeableConcept: Optional[CodeableConcept] = None  # What code or expression defines members
    definitionCanonical: Optional[str] = None  # What code or expression defines members (canonical reference)
    definitionExpression: Optional[Any] = None  # What code or expression defines members (Expression)
    definitionDataRequirement: Optional[Any] = None  # What code or expression defines members (DataRequirement)
    usageContext: List[UsageContext] = field(default_factory=list)  # What value or set of values is used
    exclude: Optional[bool] = None  # Whether the characteristic includes or excludes members
    unitOfMeasure: Optional[CodeableConcept] = None  # Unit of measure for the characteristic
    studyEffectiveDescription: Optional[str] = None  # Description of study effective time
    studyEffectiveDateTime: Optional[str] = None  # Study effective time
    studyEffectivePeriod: Optional[Period] = None  # Study effective time
    studyEffectiveDuration: Optional[Any] = None  # Study effective time (Duration)
    studyEffectiveTiming: Optional[Any] = None  # Study effective time (Timing)
    studyEffectiveTimeFromStart: Optional[Any] = None  # Study effective time from start (Duration)
    studyEffectiveGroupMeasure: Optional[str] = None  # mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median
    participantEffectiveDescription: Optional[str] = None  # Description of participant effective time
    participantEffectiveDateTime: Optional[str] = None  # Participant effective time
    participantEffectivePeriod: Optional[Period] = None  # Participant effective time
    participantEffectiveDuration: Optional[Any] = None  # Participant effective time (Duration)
    participantEffectiveTiming: Optional[Any] = None  # Participant effective time (Timing)
    participantEffectiveTimeFromStart: Optional[Any] = None  # Participant effective time from start (Duration)
    participantEffectiveGroupMeasure: Optional[str] = None  # mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median


@dataclass
class ResearchElementDefinition(MetadataResource):
    """
    FHIR R4 ResearchElementDefinition resource.
    
    Defines a research element definition.
    Extends MetadataResource.
    """
    
    resourceType: str = "ResearchElementDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this research element definition (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this research element definition (inherited from CanonicalResource)
    # Short Title
    shortTitle: Optional[str] = None  # Short title
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the research element definition
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of subject for the research element definition
    # Subject Reference
    subjectReference: Optional[Reference] = None  # Type of subject for the research element definition
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Comment
    comment: List[str] = field(default_factory=list)  # Used for footnotes or explanatory notes
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Purpose
    purpose: Optional[str] = None  # Why this research element definition is defined (inherited from CanonicalResource)
    # Usage
    usage: Optional[str] = None  # Describes the clinical usage of the research element definition
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the research element definition was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the research element definition is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the research element definition (inherited from MetadataResource)
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
    library: List[str] = field(default_factory=list)  # Logic used by the research element definition (canonical references)
    # Type
    type: str  # Population | Exposure | Outcome (required)
    # Variable Type
    variableType: Optional[CodeableConcept] = None  # dichotomous | continuous | descriptive
    # Characteristic
    characteristic: List[ResearchElementDefinitionCharacteristic] = field(default_factory=list)  # What defines the members of the research element


# Log completion timestamp at end of operations
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
