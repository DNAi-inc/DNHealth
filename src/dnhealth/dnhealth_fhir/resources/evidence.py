# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Evidence resource.

Evidence represents a single piece of evidence that informs a clinical decision.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, ContactDetail, UsageContext, RelatedArtifact


@dataclass
class EvidenceStatistic:
    """
    FHIR Evidence.statistic complex type.
    
    A statistical expression of the evidence.
    """
    
    description: Optional[str] = None  # Description of content
    note: List[Annotation] = field(default_factory=list)  # Footnotes and/or explanatory notes
    statisticType: Optional[CodeableConcept] = None  # Type of statistic
    category: Optional[CodeableConcept] = None  # Associated category for statistic
    quantity: Optional[Any] = None  # Statistic value
    numberOfEvents: Optional[int] = None  # Number of events involved in the statistic
    numberAffected: Optional[int] = None  # Number of affected participants
    sampleSize: Optional[Any] = None  # Sample size
    attributeEstimate: List[Any] = field(default_factory=list)  # An attribute of the statistic
    modelCharacteristic: List[Any] = field(default_factory=list)  # An aspect of statistical model
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EvidenceCertainty:
    """
    FHIR Evidence.certainty complex type.
    
    Assessment of certainty of the evidence.
    """
    
    description: Optional[str] = None  # Textual description of certainty
    note: List[Annotation] = field(default_factory=list)  # Footnotes and/or explanatory notes
    type: Optional[CodeableConcept] = None  # Aspect of certainty being rated
    rating: List[CodeableConcept] = field(default_factory=list)  # Assessment or judgement of the aspect
    rater: Optional[Reference] = None  # Individual or group who did the rating
    subcomponent: List[Any] = field(default_factory=list)  # A domain or subdomain of certainty
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Evidence(MetadataResource):
    """
    FHIR R4 Evidence resource.
    
    Represents a single piece of evidence that informs a clinical decision.
    Extends MetadataResource.
    """
    
    resourceType: str = "Evidence"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this evidence (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for use in informal contexts (inherited from MetadataResource)
    # Short Title
    shortTitle: Optional[str] = None  # Title for use in informal contexts
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the Evidence
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Note
    note: List[Annotation] = field(default_factory=list)  # Used for footnotes and explanatory notes
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the evidence was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the evidence is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the Evidence (inherited from MetadataResource)
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
    # Exposure Background
    exposureBackground: Optional[Reference] = None  # What population?
    # Exposure Variant
    exposureVariant: List[Reference] = field(default_factory=list)  # What exposure?
    # Outcome
    outcome: List[Reference] = field(default_factory=list)  # What outcome?

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
