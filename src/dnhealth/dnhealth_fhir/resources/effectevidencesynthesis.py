# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 EffectEvidenceSynthesis resource.

EffectEvidenceSynthesis describes the comparison of an intervention and a comparator.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, ContactDetail, UsageContext, RelatedArtifact, Period, Annotation


@dataclass
class EffectEvidenceSynthesisSampleSize:
    """
    FHIR EffectEvidenceSynthesis.sampleSize complex type.
    
    A description of the size of the sample involved in the synthesis.
    """
    
    description: Optional[str] = None  # Description of sample size
    numberOfStudies: Optional[int] = None  # How many studies?
    numberOfParticipants: Optional[int] = None  # How many participants?
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EffectEvidenceSynthesisResultsByExposure:
    """
    FHIR EffectEvidenceSynthesis.resultsByExposure complex type.
    
    A description of the results for each exposure considered in the effect estimate.
    """
    
    description: Optional[str] = None  # Description of results by exposure
    exposureState: Optional[str] = None  # exposure | exposure-alternative
    variantState: Optional[CodeableConcept] = None  # Variant exposure states
    # Note: riskEvidenceSynthesis is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce riskEvidenceSynthesis is provided.
    riskEvidenceSynthesis: Optional[Reference] = None  # Risk evidence synthesis (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EffectEvidenceSynthesisEffectEstimatePrecisionEstimate:
    """
    FHIR EffectEvidenceSynthesis.effectEstimate.precisionEstimate complex type.
    
    A description of the precision of the estimate for the effect.
    """
    
    type: Optional[CodeableConcept] = None  # Type of precision estimate
    level: Optional[float] = None  # Level of confidence interval
    from_: Optional[float] = None  # Lower bound
    to: Optional[float] = None  # Upper bound
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EffectEvidenceSynthesisEffectEstimate:
    """
    FHIR EffectEvidenceSynthesis.effectEstimate complex type.
    
    The estimated effect of the exposure variant.
    """
    
    description: Optional[str] = None  # Description of effect estimate
    type: Optional[CodeableConcept] = None  # Type of effect estimate
    variantState: Optional[CodeableConcept] = None  # Variant exposure states
    value: Optional[float] = None  # Point estimate
    unitOfMeasure: Optional[CodeableConcept] = None  # Unit of measure for the estimate
    precisionEstimate: List[EffectEvidenceSynthesisEffectEstimatePrecisionEstimate] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EffectEvidenceSynthesisCertaintyCertaintySubcomponent:
    """
    FHIR EffectEvidenceSynthesis.certainty.certaintySubcomponent complex type.
    
    A component that contributes to the overall certainty.
    """
    
    type: Optional[CodeableConcept] = None  # Type of subcomponent of certainty
    rating: List[CodeableConcept] = field(default_factory=list)  # Subcomponent certainty rating
    note: List[Annotation] = field(default_factory=list)  # Used for footnotes and explanatory notes
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EffectEvidenceSynthesisCertainty:
    """
    FHIR EffectEvidenceSynthesis.certainty complex type.
    
    A description of the certainty of the effect estimate.
    """
    
    rating: List[CodeableConcept] = field(default_factory=list)  # Certainty rating
    note: List[Annotation] = field(default_factory=list)  # Used for footnotes and explanatory notes
    certaintySubcomponent: List[EffectEvidenceSynthesisCertaintyCertaintySubcomponent] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EffectEvidenceSynthesis(MetadataResource):
    """
    FHIR R4 EffectEvidenceSynthesis resource.
    
    Describes the comparison of an intervention and a comparator.
    Extends MetadataResource.
    """
    
    resourceType: str = "EffectEvidenceSynthesis"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifier (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this effect evidence synthesis (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for use in informal contexts (inherited from MetadataResource)
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
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the effect evidence synthesis was approved (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # When the effect evidence synthesis was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the effect evidence synthesis is expected to be used (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the EffectEvidenceSynthesis (inherited from MetadataResource)
    # Author
    author: List[Any] = field(default_factory=list)  # Who authored the content (inherited from MetadataResource)
    # Editor
    editor: List[Any] = field(default_factory=list)  # Who edited the content (inherited from MetadataResource)
    # Reviewer
    reviewer: List[Any] = field(default_factory=list)  # Who reviewed the content (inherited from MetadataResource)
    # Endorser
    endorser: List[Any] = field(default_factory=list)  # Who endorsed the content (inherited from MetadataResource)
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
    # Exposure Alternative
    exposureAlternative: Optional[Reference] = None  # What comparison exposure?
    # Outcome
    # Note: outcome is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce outcome is provided.
    outcome: Optional[Reference] = None  # What outcome? (required)
    # Sample Size
    sampleSize: Optional[EffectEvidenceSynthesisSampleSize] = None  # What sample size was involved?
    # Results By Exposure
    resultsByExposure: List[EffectEvidenceSynthesisResultsByExposure] = field(default_factory=list)  # What was the result per exposure?
    # Effect Estimate
    effectEstimate: List[EffectEvidenceSynthesisEffectEstimate] = field(default_factory=list)  # What was the estimated effect?
    # Certainty
    certainty: List[EffectEvidenceSynthesisCertainty] = field(default_factory=list)  # How certain is the effect?

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
