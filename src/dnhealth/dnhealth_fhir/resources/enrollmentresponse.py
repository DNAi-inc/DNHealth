# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 EnrollmentResponse resource.

EnrollmentResponse represents a response to an enrollment request.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, Reference, CodeableConcept
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class EnrollmentResponse(DomainResource):
    """
    FHIR R4 EnrollmentResponse resource.
    
    Represents a response to an enrollment request.
    Extends DomainResource.
    """
    
    resourceType: str = "EnrollmentResponse"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier
    # Status
    status: Optional[str] = None  # active | cancelled | draft | entered-in-error
    # Request
    request: Optional[Reference] = None  # Claim reference
    # Outcome
    outcome: Optional[str] = None  # queued | complete | error | partial
    # Disposition
    disposition: Optional[str] = None  # Disposition Message
    # Created
    created: Optional[str] = None  # Creation date
    # Organization
    organization: Optional[Reference] = None  # Insurer
    # Request Provider
    requestProvider: Optional[Reference] = None  # Responsible practitioner

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


