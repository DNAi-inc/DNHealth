# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DetectedIssue resource.

DetectedIssue represents a clinical judgment about a potential or actual issue with a patient, provider, organization, or data.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class DetectedIssueMitigation:
    """
    FHIR DetectedIssue.mitigation complex type.
    
    Indicates an action that has been taken or is committed to reduce or eliminate the likelihood of the risk identified by the detected issue.
    """
    
    action: CodeableConcept  # What mitigation? (required)
    date: Optional[str] = None  # Date committed
    author: Optional[Reference] = None  # Who is committing?
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DetectedIssue(DomainResource):
    """
    FHIR R4 DetectedIssue resource.
    
    Represents a clinical judgment about a potential or actual issue with a patient, provider, organization, or data.
    Extends DomainResource.
    """
    
    resourceType: str = "DetectedIssue"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Unique id for the detected issue
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown (required in FHIR)
    # Category
    category: Optional[CodeableConcept] = None  # Issue Category, e.g. drug-drug, duplicate therapy, etc.
    # Severity
    severity: Optional[str] = None  # high | moderate | low
    # Patient
    patient: Optional[Reference] = None  # Associated patient
    # Date
    date: Optional[str] = None  # When identified
    # Author
    author: Optional[Reference] = None  # The provider or device that identified the issue
    # Implicated
    implicated: List[Reference] = field(default_factory=list)  # Problem resource
    # Evidence
    evidence: List[Any] = field(default_factory=list)  # Supporting evidence
    # Detail
    detail: Optional[str] = None  # Description and context
    # Reference
    reference: Optional[str] = None  # Authority for issue
    # Mitigation
    mitigation: List[DetectedIssueMitigation] = field(default_factory=list)  # Step taken to address

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


