# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ResearchStudy resource.

ResearchStudy represents a process where a researcher or organization plans and then executes a series of steps.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Annotation,
    ContactDetail,
)


@dataclass
class ResearchStudyArm:
    """
    FHIR ResearchStudy.arm complex type.
    
    Defined path through the study for a subject.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    name: str  # Label for study arm (required)
    type: Optional[CodeableConcept] = None  # Categorization of study arm
    description: Optional[str] = None  # Short explanation of study path


@dataclass
class ResearchStudyObjective:
    """
    FHIR ResearchStudy.objective complex type.
    
    A goal for the study.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    name: Optional[str] = None  # Label for the objective
    type: Optional[CodeableConcept] = None  # primary | secondary | exploratory


@dataclass
class ResearchStudy(DomainResource):
    """
    FHIR R4 ResearchStudy resource.
    
    Represents a process where a researcher or organization plans and then executes a series of steps.
    Extends DomainResource.
    """
    
    resourceType: str = "ResearchStudy"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for study
    # Title
    title: Optional[str] = None  # Name for this research study
    # Protocol
    protocol: List[Reference] = field(default_factory=list)  # Steps followed in executing study
    # Part Of
    partOf: List[Reference] = field(default_factory=list)  # Part of larger study
    # Status
    status: str  # active | administratively-completed | approved | closed-to-accrual | closed-to-accrual-and-intervention | completed | disapproved | in-review | temporarily-closed-to-accrual | temporarily-closed-to-accrual-and-intervention | withdrawn (required)
    # Primary Purpose Type
    primaryPurposeType: Optional[CodeableConcept] = None  # treatment | prevention | diagnostic | supportive-care | screening | health-services-research | basic-science | device-feasibility
    # Phase
    phase: Optional[CodeableConcept] = None  # n-a | early-phase-1 | phase-1 | phase-1-phase-2 | phase-2 | phase-2-phase-3 | phase-3 | phase-4
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Classifications for the study
    # Focus
    focus: List[CodeableConcept] = field(default_factory=list)  # Drugs, devices, conditions, etc. under study
    # Condition
    condition: List[CodeableConcept] = field(default_factory=list)  # Condition being studied
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details for the study
    # Keyword
    keyword: List[CodeableConcept] = field(default_factory=list)  # Used to search for the study
    # Location
    location: List[CodeableConcept] = field(default_factory=list)  # Geographic region(s) for study
    # Description
    description: Optional[str] = None  # What this is study doing
    # Enrollment
    enrollment: List[Reference] = field(default_factory=list)  # Inclusion & exclusion criteria
    # Period
    period: Optional[Period] = None  # When the study began and ended
    # Sponsor
    sponsor: Optional[Reference] = None  # Organization that initiates and is legally responsible
    # Principal Investigator
    principalInvestigator: Optional[Reference] = None  # Researcher who oversees multiple aspects
    # Site
    site: List[Reference] = field(default_factory=list)  # Facility where study activities are conducted
    # Reason Stopped
    reasonStopped: Optional[CodeableConcept] = None  # accrual-goal-met | closed-due-to-toxicity | closed-due-to-lack-of-study-progress | temporarily-closed-per-study-design
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about the study
    # Arm
    arm: List[ResearchStudyArm] = field(default_factory=list)  # Defined path through the study for a subject
    # Objective
    objective: List[ResearchStudyObjective] = field(default_factory=list)  # A goal for the study

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

