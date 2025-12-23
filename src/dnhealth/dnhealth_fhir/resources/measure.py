# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Measure resource.

Measure defines a quality measure specification.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
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
class MeasureGroup:
    """
    FHIR Measure.group complex type.
    
    A group of population criteria for the measure.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # Meaning of the group
    description: Optional[str] = None  # Summary description
    population: List["MeasureGroupPopulation"] = field(default_factory=list)  # Population criteria
    stratifier: List["MeasureGroupStratifier"] = field(default_factory=list)  # Stratification criteria


@dataclass
class MeasureGroupPopulation:
    """
    FHIR Measure.group.population complex type.
    
    A population criteria for the measure.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # initial-population | numerator | numerator-exclusion | denominator | denominator-exclusion | denominator-exception | measure-population | measure-population-exclusion | measure-observation
    description: Optional[str] = None  # The human readable description of this population criteria
    # Note: criteria is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce criteria is provided.
    criteria: Optional[Any] = None  # The criteria that defines this population (Expression)


@dataclass
class MeasureGroupStratifier:
    """
    FHIR Measure.group.stratifier complex type.
    
    Stratification criteria for the measure.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # Meaning of the stratifier
    description: Optional[str] = None  # The human readable description of this stratifier
    criteria: Optional[Any] = None  # How the measure should be stratified (Expression)
    component: List["MeasureGroupStratifierComponent"] = field(default_factory=list)  # Stratifier component


@dataclass
class MeasureGroupStratifierComponent:
    """
    FHIR Measure.group.stratifier.component complex type.
    
    A component of the stratifier criteria.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # Meaning of the stratifier component
    description: Optional[str] = None  # The human readable description of this stratifier component
    # Note: criteria is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce criteria is provided.
    criteria: Optional[Any] = None  # Component criteria (Expression)


@dataclass
class MeasureSupplementalData:
    """
    FHIR Measure.supplementalData complex type.
    
    Supplemental data for the measure.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # Meaning of the supplemental data
    usage: List[CodeableConcept] = field(default_factory=list)  # supplemental-data | risk-adjustment-factor
    description: Optional[str] = None  # The human readable description of this supplemental data
    # Note: criteria is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce criteria is provided.
    criteria: Optional[Any] = None  # Expression describing additional data to be reported (Expression)


@dataclass
class Measure(MetadataResource):
    """
    FHIR R4 Measure resource.
    
    Defines a quality measure specification.
    Extends MetadataResource.
    """
    
    resourceType: str = "Measure"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this measure (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this measure (inherited from CanonicalResource)
    # Subtitle
    subtitle: Optional[str] = None  # Subordinate title of the measure
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device
    # Subject Reference
    subjectReference: Optional[Reference] = None  # E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device
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
    purpose: Optional[str] = None  # Why this measure is defined (inherited from CanonicalResource)
    # Usage
    usage: Optional[str] = None  # Describes the clinical usage of the measure
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the measure was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the measure is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the measure (inherited from MetadataResource)
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
    library: List[str] = field(default_factory=list)  # Logic used by the measure (canonical references)
    # Disclaimer
    disclaimer: Optional[str] = None  # Disclaimer for use of the measure or its referenced content
    # Scoring
    scoring: Optional[CodeableConcept] = None  # proportion | ratio | continuous-variable | cohort
    # Scoring Unit
    scoringUnit: Optional[CodeableConcept] = None  # Unit of measure for the score
    # Rate Aggregate
    rateAggregate: Optional[str] = None  # How is rate aggregation performed for this measure
    # Rationale
    rationale: Optional[str] = None  # Detailed description of why the measure exists
    # Clinical Recommendation Statement
    clinicalRecommendationStatement: Optional[str] = None  # Summary of clinical guidelines
    # Improvement Notation
    improvementNotation: Optional[CodeableConcept] = None  # increase | decrease
    # Term
    term: List["MeasureTerm"] = field(default_factory=list)  # Defined terms used in the measure documentation
    # Guidance
    guidance: Optional[str] = None  # Additional guidance for implementers
    # Group
    group: List[MeasureGroup] = field(default_factory=list)  # Population criteria group
    # Supplemental Data
    supplementalData: List[MeasureSupplementalData] = field(default_factory=list)  # What other data should be reported


@dataclass
class MeasureTerm:
    """
    FHIR Measure.term complex type.
    
    Defined terms used in the measure documentation.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # The term code
    definition: Optional[str] = None  # The term definition

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
