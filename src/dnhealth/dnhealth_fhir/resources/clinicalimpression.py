# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ClinicalImpression resource.

ClinicalImpression represents a record of a clinical assessment performed to determine what problem(s) may affect the patient.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ClinicalImpressionInvestigation:
    """
    FHIR ClinicalImpression.investigation complex type.
    
    One or more sets of investigations (signs, symptoms, etc.).
    """
    
    code: CodeableConcept  # A name/code for the group (required)
    item: List[Reference] = field(default_factory=list)  # Record of a specific investigation
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClinicalImpressionFinding:
    """
    FHIR ClinicalImpression.finding complex type.
    
    Specific findings or diagnoses that were considered likely or relevant to ongoing treatment.
    """
    
    itemCodeableConcept: Optional[CodeableConcept] = None  # What was found
    itemReference: Optional[Reference] = None  # What was found
    basis: Optional[str] = None  # Which investigations support finding
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ClinicalImpression(DomainResource):
    """
    FHIR R4 ClinicalImpression resource.
    
    Represents a record of a clinical assessment performed to determine what problem(s) may affect the patient.
    Extends DomainResource.
    """
    
    resourceType: str = "ClinicalImpression"
    # Status (required - using Optional with None default to satisfy dataclass ordering, validated in __post_init__)
    status: Optional[str] = None  # in-progress | completed | entered-in-error (required)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Status Reason
    statusReason: Optional[CodeableConcept] = None  # Reason for current status
    # Code
    code: Optional[CodeableConcept] = None  # Kind of assessment performed
    # Description
    description: Optional[str] = None  # Why/how the assessment was performed
    # Subject (required - using Optional with None default to satisfy dataclass ordering, validated in __post_init__)
    subject: Optional[Reference] = None  # Patient or group assessed (required)
    # Encounter
    encounter: Optional[Reference] = None  # Encounter created during
    # Effective DateTime
    effectiveDateTime: Optional[str] = None  # Time of assessment
    # Effective Period
    effectivePeriod: Optional[Period] = None  # Time of assessment
    # Date
    date: Optional[str] = None  # When the assessment was documented
    # Assessor
    assessor: Optional[Reference] = None  # The clinician performing the assessment
    # Previous
    previous: Optional[Reference] = None  # Reference to last assessment
    # Problem
    problem: List[Reference] = field(default_factory=list)  # Relevant impressions of patient state
    # Investigation
    investigation: List[ClinicalImpressionInvestigation] = field(default_factory=list)  # One or more sets of investigations
    # Protocol
    protocol: List[str] = field(default_factory=list)  # Clinical Protocol followed
    # Summary
    summary: Optional[str] = None  # Summary of the assessment
    # Finding
    finding: List[ClinicalImpressionFinding] = field(default_factory=list)  # Possible or likely findings and diagnoses
    # Prognosis CodeableConcept
    prognosisCodeableConcept: List[CodeableConcept] = field(default_factory=list)  # Estimate of likely outcome
    # Prognosis Reference
    prognosisReference: List[Reference] = field(default_factory=list)  # RiskAssessment expressing likely outcome
    # Supporting Info
    supportingInfo: List[Reference] = field(default_factory=list)  # Information supporting the clinical impression
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about the ClinicalImpression

    def __post_init__(self):
        """Validate required fields."""
        if self.status is None:
            raise ValueError("status is required for ClinicalImpression")
        if self.subject is None:
            raise ValueError("subject is required for ClinicalImpression")

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


