# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 EvidenceVariable resource.

EvidenceVariable represents a population, exposure, or outcome.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, ContactDetail, UsageContext, RelatedArtifact


@dataclass
class EvidenceVariableCharacteristic:
    """
    FHIR EvidenceVariable.characteristic complex type.
    
    A defining factor of the EvidenceVariable.
    """
    
    description: Optional[str] = None  # Natural language description of the characteristic
    definitionReference: Optional[Reference] = None  # Defines the characteristic
    definitionCanonical: Optional[str] = None  # Defines the characteristic
    definitionCodeableConcept: Optional[CodeableConcept] = None  # Defines the characteristic
    definitionExpression: Optional[Any] = None  # Defines the characteristic (Expression)
    definitionTriggerDefinition: Optional[Any] = None  # Defines the characteristic (TriggerDefinition)
    definitionDataRequirement: Optional[Any] = None  # Defines the characteristic (DataRequirement)
    method: Optional[CodeableConcept] = None  # Method used for describing characteristic
    device: Optional[Reference] = None  # Device used for determining characteristic
    exclude: Optional[bool] = None  # Whether the characteristic is an exclusion criterion
    timeFromStart: Optional[Any] = None  # Timeframe for the characteristic (Duration)
    groupMeasure: Optional[str] = None  # mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EvidenceVariable(MetadataResource):
    """
    FHIR R4 EvidenceVariable resource.
    
    Represents a population, exposure, or outcome.
    Extends MetadataResource.
    """
    
    resourceType: str = "EvidenceVariable"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this evidence variable (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for use in informal contexts (inherited from MetadataResource)
    # Short Title
    shortTitle: Optional[str] = None  # Title for use in informal contexts
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the EvidenceVariable
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
    approvalDate: Optional[str] = None  # When the evidence variable was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the evidence variable is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the EvidenceVariable (inherited from MetadataResource)
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
    # Type
    type: Optional[str] = None  # dichotomous | continuous | descriptive
    # Characteristic
    characteristic: List[EvidenceVariableCharacteristic] = field(default_factory=list)  # A defining factor of the EvidenceVariable (required)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
