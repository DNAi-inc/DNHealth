# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ResearchDefinition resource.

ResearchDefinition defines a research study definition.
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
class ResearchDefinition(MetadataResource):
    """
    FHIR R4 ResearchDefinition resource.
    
    Defines a research study definition.
    Extends MetadataResource.
    """
    
    resourceType: str = "ResearchDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this research definition (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this research definition (inherited from CanonicalResource)
    # Short Title
    shortTitle: Optional[str] = None  # Short title
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the research definition
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of subject for the research definition
    # Subject Reference
    subjectReference: Optional[Reference] = None  # Type of subject for the research definition
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
    purpose: Optional[str] = None  # Why this research definition is defined (inherited from CanonicalResource)
    # Usage
    usage: Optional[str] = None  # Describes the clinical usage of the research definition
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the research definition was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the research definition is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the research definition (inherited from MetadataResource)
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
    library: List[str] = field(default_factory=list)  # Logic used by the research definition (canonical references)
    # Type
    type: Optional[CodeableConcept] = None  # The type of research element
    # Variable Type
    variableType: Optional[str] = None  # dichotomous | continuous | descriptive
    # Outcome
    outcome: Optional[Reference] = None  # What outcome


# Log completion timestamp at end of operations
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
