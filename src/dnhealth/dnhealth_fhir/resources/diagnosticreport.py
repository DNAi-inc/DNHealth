# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DiagnosticReport resource.

DiagnosticReport represents the findings and interpretation of diagnostic tests performed on patients, groups of patients, devices, and locations.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Attachment
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class DiagnosticReportMedia:
    """
    FHIR DiagnosticReport.media complex type.
    
    A list of key images associated with this report.
    """
    
    comment: Optional[str] = None  # Comment about the image
    # Note: link is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce link is provided.
    link: Optional[Reference] = None  # Reference to the image source (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DiagnosticReport(DomainResource):
    """
    FHIR R4 DiagnosticReport resource.
    
    Represents the findings and interpretation of diagnostic tests performed on patients, groups of patients, devices, and locations.
    Extends DomainResource.
    """
    
    resourceType: str = "DiagnosticReport"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier for report
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # What was requested
    # Status
    status: Optional[str] = None  # registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown (required)
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Service category
    # Code
    code: Optional[CodeableConcept] = None  # Name/Code for this diagnostic report (required)
    # Subject
    subject: Optional[Reference] = None  # The subject of the report
    # Encounter
    encounter: Optional[Reference] = None  # Health care event when test ordered
    # Effective DateTime
    effectiveDateTime: Optional[str] = None  # Clinically relevant time/time-period for report
    # Effective Period
    effectivePeriod: Optional[Period] = None  # Clinically relevant time/time-period for report
    # Issued
    issued: Optional[str] = None  # DateTime this version was made
    # Performer
    performer: List[Reference] = field(default_factory=list)  # Responsible Diagnostic Service
    # Results Interpreter
    resultsInterpreter: List[Reference] = field(default_factory=list)  # Primary result interpreter
    # Specimen
    specimen: List[Reference] = field(default_factory=list)  # Specimens this report is based on
    # Result
    result: List[Reference] = field(default_factory=list)  # Observations
    # Imaging Study
    imagingStudy: List[Reference] = field(default_factory=list)  # Reference to full details of imaging associated with the diagnostic report
    # Media
    media: List[DiagnosticReportMedia] = field(default_factory=list)  # Key images associated with this report
    # Conclusion
    conclusion: Optional[str] = None  # Clinical conclusion (interpretation) of test results
    # Conclusion Code
    conclusionCode: List[CodeableConcept] = field(default_factory=list)  # Codes for the clinical conclusion of test results
    # Presented Form
    presentedForm: List[Attachment] = field(default_factory=list)  # Entire report as issued
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.status is None:
            raise ValueError("status is required for DiagnosticReport")
        if self.code is None:
            raise ValueError("code is required for DiagnosticReport")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
