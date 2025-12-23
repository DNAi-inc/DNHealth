# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 GuidanceResponse resource.

GuidanceResponse represents a guidance response from a decision support system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, Reference, CodeableConcept, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class GuidanceResponse(DomainResource):
    """
    FHIR R4 GuidanceResponse resource.
    
    Represents a guidance response from a decision support system.
    Extends DomainResource.
    """
    
    resourceType: str = "GuidanceResponse"
    # Request Identifier
    requestIdentifier: Optional[Identifier] = None  # The identifier of the request associated with this response
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Module URI
    moduleUri: Optional[str] = None  # What guidance was requested
    # Module Canonical
    moduleCanonical: Optional[str] = None  # What guidance was requested
    # Module CodeableConcept
    moduleCodeableConcept: Optional[CodeableConcept] = None  # What guidance was requested
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # success | data-requested | data-required | in-progress | failure | entered-in-error (required in FHIR)
    # Subject
    subject: Optional[Reference] = None  # Patient the request was performed for
    # Encounter
    encounter: Optional[Reference] = None  # Encounter during which the response was returned
    # Occurrence Date Time
    occurrenceDateTime: Optional[str] = None  # When the guidance response was processed
    # Performer
    performer: Optional[Reference] = None  # Device returning the guidance
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why guidance is needed
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why guidance is needed
    # Note
    note: List[Annotation] = field(default_factory=list)  # Additional notes about the response
    # Evaluation Message
    evaluationMessage: List[Reference] = field(default_factory=list)  # Messages resulting from the evaluation of the artifact or artifacts
    # Output Parameters
    outputParameters: Optional[Reference] = None  # The output parameters of the response
    # Result
    result: Optional[Reference] = None  # Proposed actions, if any
    # Data Requirement
    dataRequirement: List[Any] = field(default_factory=list)  # Additional required data

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


