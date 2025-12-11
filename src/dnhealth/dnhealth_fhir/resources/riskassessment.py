# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 RiskAssessment resource.

RiskAssessment identifies potential future events and their probability.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Annotation,
)


logger = logging.getLogger(__name__)


@dataclass
class RiskAssessmentPrediction:
    """
    FHIR RiskAssessment.prediction complex type.
    
    Outcome predicted.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    outcome: Optional[CodeableConcept] = None  # Possible outcome for the subject
    probabilityDecimal: Optional[float] = None  # Likelihood of specified outcome
    probabilityRange: Optional[Any] = None  # Likelihood of specified outcome (Range)
    qualitativeRisk: Optional[CodeableConcept] = None  # Likelihood of specified outcome as a qualitative value
    relativeRisk: Optional[float] = None  # Relative likelihood
    whenPeriod: Optional[Period] = None  # Timeframe or age range
    whenRange: Optional[Any] = None  # Timeframe or age range (Range)
    rationale: Optional[str] = None  # Explanation of prediction


@dataclass
class RiskAssessment(DomainResource):
    """
    FHIR R4 RiskAssessment resource.
    
    Identifies potential future events and their probability.
    Extends DomainResource.
    """
    
    resourceType: str = "RiskAssessment"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Unique identifier for the assessment
    # Based On
    basedOn: Optional[Reference] = None  # Request fulfilled by this assessment
    # Parent
    parent: Optional[Reference] = None  # Part of this occurrence
    # Status
    status: str  # registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown (required)
    # Method
    method: Optional[CodeableConcept] = None  # Evaluation mechanism
    # Code
    code: Optional[CodeableConcept] = None  # Type of assessment
    # Subject
    subject: Reference  # Who/what does assessment apply to (required)
    # Encounter
    encounter: Optional[Reference] = None  # Where was assessment performed
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # When was assessment made
    # Occurrence Period
    occurrencePeriod: Optional[Period] = None  # When was assessment made
    # Condition
    condition: Optional[Reference] = None  # Condition assessed
    # Performer
    performer: Optional[Reference] = None  # Who did assessment
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why the assessment was necessary
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why the assessment was necessary
    # Basis
    basis: List[Reference] = field(default_factory=list)  # Information used in assessment
    # Prediction
    prediction: List[RiskAssessmentPrediction] = field(default_factory=list)  # Outcome predicted
    # Mitigation
    mitigation: Optional[str] = None  # How to reduce risk
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments on the risk assessment

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

