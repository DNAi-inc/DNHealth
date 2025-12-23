# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 RiskEvidenceSynthesis resource.

RiskEvidenceSynthesis describes the likelihood of an outcome in a population.
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
class RiskEvidenceSynthesisSampleSize:
    """
    FHIR RiskEvidenceSynthesis.sampleSize complex type.
    
    What sample size was involved.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    description: Optional[str] = None  # Description of sample size
    numberOfStudies: Optional[int] = None  # How many studies
    numberOfParticipants: Optional[int] = None  # How many participants


@dataclass
class RiskEvidenceSynthesisRiskEstimate:
    """
    FHIR RiskEvidenceSynthesis.riskEstimate complex type.
    
    What was the estimated risk.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    description: Optional[str] = None  # Description of risk estimate
    type: Optional[CodeableConcept] = None  # Type of risk estimate
    value: Optional[float] = None  # The point estimate of the risk estimate
    unitOfMeasure: Optional[CodeableConcept] = None  # What unit is the outcome described in
    denominatorCount: Optional[int] = None  # Sample size for group used to estimate risk
    numeratorCount: Optional[int] = None  # Number with the outcome
    precisionEstimate: List["RiskEvidenceSynthesisRiskEstimatePrecisionEstimate"] = field(default_factory=list)  # How precise the estimate is


@dataclass
class RiskEvidenceSynthesisRiskEstimatePrecisionEstimate:
    """
    FHIR RiskEvidenceSynthesis.riskEstimate.precisionEstimate complex type.
    
    How precise the estimate is.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: Optional[CodeableConcept] = None  # Type of precision estimate
    level: Optional[float] = None  # Level of confidence interval
    from_: Optional[float] = None  # Lower bound
    to: Optional[float] = None  # Upper bound


@dataclass
class RiskEvidenceSynthesisCertainty:
    """
    FHIR RiskEvidenceSynthesis.certainty complex type.
    
    Certainty or quality of the evidence.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    rating: List[CodeableConcept] = field(default_factory=list)  # Certainty rating
    note: List[Any] = field(default_factory=list)  # Certainty note (Annotation)
    certaintySubcomponent: List["RiskEvidenceSynthesisCertaintyCertaintySubcomponent"] = field(default_factory=list)  # A component that contributes to the overall certainty


@dataclass
class RiskEvidenceSynthesisCertaintyCertaintySubcomponent:
    """
    FHIR RiskEvidenceSynthesis.certainty.certaintySubcomponent complex type.
    
    A component that contributes to the overall certainty.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    type: Optional[CodeableConcept] = None  # Type of subcomponent of certainty rating
    rating: List[CodeableConcept] = field(default_factory=list)  # Subcomponent certainty rating
    note: List[Any] = field(default_factory=list)  # Used for footnotes (Annotation)


@dataclass
class RiskEvidenceSynthesis(MetadataResource):
    """
    FHIR R4 RiskEvidenceSynthesis resource.
    
    Describes the likelihood of an outcome in a population.
    Extends MetadataResource.
    """
    
    resourceType: str = "RiskEvidenceSynthesis"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this risk evidence synthesis (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this risk evidence synthesis (inherited from CanonicalResource)
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
    note: List[Any] = field(default_factory=list)  # Used for footnotes or explanatory notes (Annotation)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the risk evidence synthesis was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the risk evidence synthesis is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the risk evidence synthesis (inherited from MetadataResource)
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
    # Synthesis Type
    synthesisType: Optional[CodeableConcept] = None  # Type of synthesis
    # Study Type
    studyType: Optional[CodeableConcept] = None  # Type of study
    # Population
    # Note: population is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce population is provided.
    population: Optional[Reference] = None  # What population? (required)
    # Exposure
    exposure: Optional[Reference] = None  # What exposure?
    # Outcome
    # Note: outcome is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce outcome is provided.
    outcome: Optional[Reference] = None  # What outcome? (required)
    # Sample Size
    sampleSize: Optional[RiskEvidenceSynthesisSampleSize] = None  # What sample size was involved
    # Risk Estimate
    riskEstimate: Optional[RiskEvidenceSynthesisRiskEstimate] = None  # What was the estimated risk
    # Certainty
    certainty: List[RiskEvidenceSynthesisCertainty] = field(default_factory=list)  # Certainty or quality of the evidence

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
