# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Base classes for FHIR resources.

FHIR resource hierarchy:
- Resource: Base abstract class (id, meta, implicitRules, language)
- DomainResource: Extends Resource (adds text, contained, extension, modifierExtension)
- CanonicalResource: Extends DomainResource (adds canonical fields like url, version, status)
- MetadataResource: Extends CanonicalResource (adds metadata fields like approvalDate, topic)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from dnhealth.dnhealth_fhir.types import Extension, Narrative, Coding
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class Meta:
    """
    FHIR Meta element.

    Metadata about the resource.
    """

    versionId: Optional[str] = None
    lastUpdated: Optional[str] = None
    source: Optional[str] = None
    profile: List[str] = field(default_factory=list)
    security: List[Coding] = field(default_factory=list)
    tag: List[Coding] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Resource:
    """
    FHIR Resource base class.
    
    Base abstract class for all FHIR resources.
    All resources have: resourceType, id, meta, implicitRules, language
    """

    resourceType: str
    id: Optional[str] = None
    meta: Optional[Meta] = None
    implicitRules: Optional[str] = None  # URI for set of rules
    language: Optional[str] = None  # Language code (BCP-47)
    # For unknown extensions and fields
    _unknown_fields: Dict[str, Any] = field(default_factory=dict)
    # For primitive extensions (_element fields like _id, _status, etc.)
    # Maps field name (without underscore) to list of Extension objects
    _primitive_extensions: Dict[str, List[Extension]] = field(default_factory=dict)

    def __post_init__(self):
        """Validate resource after initialization."""
        if not self.resourceType:
            raise ValueError("resourceType is required")



        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
@dataclass
class DomainResource(Resource):
    """
    FHIR DomainResource base class.
    
    Extends Resource with domain-specific fields.
    Adds: text, contained, extension, modifierExtension
    Most FHIR resources inherit from DomainResource.
    """

    text: Optional[Narrative] = None  # Human-readable summary
    contained: List[Any] = field(default_factory=list)  # Contained resources
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CanonicalResource(DomainResource):
    """
    FHIR CanonicalResource base class.
    
    Extends DomainResource with canonical fields.
    Adds: url, identifier, version, status, experimental, date, publisher, contact,
          description, useContext, jurisdiction, purpose, copyright
    Used for resources that can be referenced canonically (profiles, value sets, etc.)
    """

    url: Optional[str] = None  # Canonical URL
    identifier: List[Any] = field(default_factory=list)  # Additional identifiers
    version: Optional[str] = None  # Business version
    status: Optional[str] = None  # draft | active | retired | unknown
    experimental: Optional[bool] = None  # For testing purposes
    date: Optional[str] = None  # Date last changed
    publisher: Optional[str] = None  # Name of publisher
    contact: List[Any] = field(default_factory=list)  # Contact details
    description: Optional[str] = None  # Natural language description
    useContext: List[Any] = field(default_factory=list)  # Context of use
    jurisdiction: List[Any] = field(default_factory=list)  # Intended jurisdiction
    purpose: Optional[str] = None  # Why this resource is defined
    copyright: Optional[str] = None  # Use and/or publishing restrictions


@dataclass
class MetadataResource(CanonicalResource):
    """
    FHIR MetadataResource base class.
    
    Extends CanonicalResource with metadata fields.
    Adds: approvalDate, lastReviewDate, effectivePeriod, topic, author, editor,
          reviewer, endorser, relatedArtifact
    Used for resources that describe other resources (profiles, implementation guides, etc.)
    """

    approvalDate: Optional[str] = None  # When approved by publisher
    lastReviewDate: Optional[str] = None  # When last reviewed
    effectivePeriod: Optional[Any] = None  # When resource is valid (Period)
    topic: List[Any] = field(default_factory=list)  # Topics for this resource
    author: List[Any] = field(default_factory=list)  # Who authored the content
    editor: List[Any] = field(default_factory=list)  # Who edited the content
    reviewer: List[Any] = field(default_factory=list)  # Who reviewed the content
    endorser: List[Any] = field(default_factory=list)  # Who endorsed the content
    relatedArtifact: List[Any] = field(default_factory=list)  # Related artifacts


# Alias for backward compatibility
FHIRResource = DomainResource

