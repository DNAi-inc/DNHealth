# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Library resource.

Library represents a library of knowledge assets such as logic, definitions, and value sets.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, ContactDetail, UsageContext, RelatedArtifact, Attachment


@dataclass
class Library(MetadataResource):
    """
    FHIR R4 Library resource.
    
    Represents a library of knowledge assets such as logic, definitions, and value sets.
    Extends MetadataResource.
    """
    
    resourceType: str = "Library"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifier (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this library (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Name for this library (inherited from CanonicalResource)
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the library
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Type
    type: CodeableConcept  # logic-library | model-definition | asset-collection | module-definition (required)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of individual the library content focuses on
    # Subject Reference
    subjectReference: Optional[Reference] = None  # Type of individual the library content focuses on
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
    purpose: Optional[str] = None  # Why this library is defined (inherited from CanonicalResource)
    # Usage
    usage: Optional[str] = None  # Describes the clinical usage of the library
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the library was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the library is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the library (inherited from MetadataResource)
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
    # Parameter
    parameter: List[Any] = field(default_factory=list)  # Parameters defined by the library
    # Data Requirement
    dataRequirement: List[Any] = field(default_factory=list)  # What data is referenced by this library
    # Content
    content: List[Attachment] = field(default_factory=list)  # Contents of the library

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
