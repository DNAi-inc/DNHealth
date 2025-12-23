# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ResearchSubject resource.

ResearchSubject represents a physical entity which is the primary unit of interest in the study.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
)


logger = logging.getLogger(__name__)


@dataclass
class ResearchSubject(DomainResource):
    """
    FHIR R4 ResearchSubject resource.
    
    Represents a physical entity which is the primary unit of interest in the study.
    Extends DomainResource.
    """
    
    resourceType: str = "ResearchSubject"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for research subject
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # field ordering compatibility (identifier has default value).
    # Validation should enforce status is provided.
    status: Optional[str] = None  # candidate | eligible | follow-up | ineligible | not-registered | off-study | on-study | on-study-intervention | on-study-observation | pending-on-study | potential-candidate | screening | withdrawn (required in FHIR)
    # Period
    period: Optional[Period] = None  # Start and end of participation
    # Study
    # Note: study is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce study is provided.
    study: Optional[Reference] = None  # Study subject is part of (required) (required in FHIR)
    # Individual
    # Note: individual is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce individual is provided.
    individual: Optional[Reference] = None  # Who is part of study (required)
    # Assigned Arm
    assignedArm: Optional[str] = None  # The name of the arm in the study the subject is expected to follow
    # Actual Arm
    actualArm: Optional[str] = None  # The name of the arm in the study the subject actually followed
    # Consent
    consent: Optional[Reference] = None  # Agreement to participate in study

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

