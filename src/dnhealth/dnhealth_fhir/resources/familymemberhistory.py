# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 FamilyMemberHistory resource.

FamilyMemberHistory represents information about a patient's family member's health history.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Age, Range
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class FamilyMemberHistoryCondition:
    """
    FHIR FamilyMemberHistory.condition complex type.
    
    Condition that the family member had.
    """
    
    code: CodeableConcept  # Condition suffered by relation (required)
    outcome: Optional[CodeableConcept] = None  # deceased | permanent disability | etc.
    contributedToDeath: Optional[bool] = None  # Whether the condition contributed to the cause of death
    onsetAge: Optional[Age] = None  # When condition first manifested
    onsetRange: Optional[Range] = None  # When condition first manifested
    onsetPeriod: Optional[Period] = None  # When condition first manifested
    onsetString: Optional[str] = None  # When condition first manifested
    note: List[Annotation] = field(default_factory=list)  # Extra information about condition
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class FamilyMemberHistory(DomainResource):
    """
    FHIR R4 FamilyMemberHistory resource.
    
    Represents information about a patient's family member's health history.
    Extends DomainResource.
    """
    
    resourceType: str = "FamilyMemberHistory"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External Id(s) for this record
    # Instantiates Canonical
    instantiatesCanonical: List[str] = field(default_factory=list)  # Instantiates FHIR protocol or definition
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)  # Instantiates external protocol or definition
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # partial | completed | entered-in-error | health-unknown (required in FHIR)
    # Data Absent Reason
    dataAbsentReason: Optional[CodeableConcept] = None  # subject-unknown | withheld | unable-to-obtain | deferred
    # Patient
    # Note: patient is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce patient is provided.
    patient: Optional[Reference] = None  # Patient history is about (required)
    # Date
    date: Optional[str] = None  # When history was recorded or last updated
    # Name
    name: Optional[str] = None  # The family member described
    # Relationship
    # Note: relationship is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce relationship is provided.
    relationship: Optional[CodeableConcept] = None  # Relationship to the subject (required)
    # Sex
    sex: Optional[CodeableConcept] = None  # male | female | other | unknown
    # Born Period
    bornPeriod: Optional[Period] = None  # (approximate) date of birth
    # Born Date
    bornDate: Optional[str] = None  # (approximate) date of birth
    # Born String
    bornString: Optional[str] = None  # (approximate) date of birth
    # Age Age
    ageAge: Optional[Age] = None  # (approximate) age
    # Age Range
    ageRange: Optional[Range] = None  # (approximate) age
    # Age String
    ageString: Optional[str] = None  # (approximate) age
    # Estimated Age
    estimatedAge: Optional[bool] = None  # Age is estimated?
    # Deceased Boolean
    deceasedBoolean: Optional[bool] = None  # Dead? How old/when?
    # Deceased Age
    deceasedAge: Optional[Age] = None  # Dead? How old/when?
    # Deceased Range
    deceasedRange: Optional[Range] = None  # Dead? How old/when?
    # Deceased Date
    deceasedDate: Optional[str] = None  # Dead? How old/when?
    # Deceased String
    deceasedString: Optional[str] = None  # Dead? How old/when?
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why was family member history performed?
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why was family member history performed?
    # Note
    note: List[Annotation] = field(default_factory=list)  # General note about related person
    # Condition
    condition: List[FamilyMemberHistoryCondition] = field(default_factory=list)  # Condition that the family member had

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


