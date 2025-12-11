# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Condition resource.

Complete Condition resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    Annotation,
)
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ConditionStage:
    """
    FHIR Condition.stage complex type.
    
    Clinical stage or grade of a condition.
    """

    summary: Optional[CodeableConcept] = None
    type: Optional[CodeableConcept] = None
    assessment: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class ConditionEvidence:
    """
    FHIR Condition.evidence complex type.
    
    Supporting evidence for the condition.
    """

    code: List[CodeableConcept] = field(default_factory=list)
    detail: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Condition(FHIRResource):
    """
    FHIR R4 Condition resource.

    Represents a clinical condition, problem, diagnosis, or other event,
    situation, issue, or clinical concept that has risen to a level of concern.
    """

    resourceType: str = "Condition"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Clinical status
    clinicalStatus: Optional[CodeableConcept] = None
    # Verification status
    verificationStatus: Optional[CodeableConcept] = None
    # Category
    category: List[CodeableConcept] = field(default_factory=list)
    # Severity
    severity: Optional[CodeableConcept] = None
    # Code
    code: Optional[CodeableConcept] = None
    # Body site
    bodySite: List[CodeableConcept] = field(default_factory=list)
    # Subject (required field - validated in __post_init__)
    subject: Optional[Reference] = None
    # Encounter
    encounter: Optional[Reference] = None
    # Onset
    onsetDateTime: Optional[str] = None
    onsetAge: Optional[Any] = None  # Age type
    onsetPeriod: Optional[Period] = None
    onsetRange: Optional[Any] = None  # Range type
    onsetString: Optional[str] = None
    # Abatement
    abatementDateTime: Optional[str] = None
    abatementAge: Optional[Any] = None  # Age type
    abatementPeriod: Optional[Period] = None
    abatementRange: Optional[Any] = None  # Range type
    abatementString: Optional[str] = None
    # Recorded date
    recordedDate: Optional[str] = None
    # Recorder
    recorder: Optional[Reference] = None
    # Asserter
    asserter: Optional[Reference] = None
    # Stage
    stage: List[ConditionStage] = field(default_factory=list)
    # Evidence
    evidence: List[ConditionEvidence] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)

    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.subject is None:
            raise ValueError("Condition.subject is required")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
