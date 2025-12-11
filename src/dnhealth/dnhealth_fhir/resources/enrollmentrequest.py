# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 EnrollmentRequest resource.

EnrollmentRequest represents a request to enroll a patient in a health insurance plan.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class EnrollmentRequest(DomainResource):
    """
    FHIR R4 EnrollmentRequest resource.
    
    Represents a request to enroll a patient in a health insurance plan.
    Extends DomainResource.
    """
    
    resourceType: str = "EnrollmentRequest"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier
    # Status
    status: Optional[str] = None  # active | cancelled | draft | entered-in-error
    # Created
    created: Optional[str] = None  # Creation date
    # Insurer
    insurer: Optional[Reference] = None  # Target
    # Provider
    provider: Optional[Reference] = None  # Responsible practitioner
    # Candidate
    candidate: Optional[Reference] = None  # The subject to be enrolled
    # Coverage
    coverage: Optional[Reference] = None  # Insurance information

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


