# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 OperationOutcome resource.

Complete OperationOutcome resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
)


@dataclass
class OperationOutcomeIssue:
    """
    FHIR OperationOutcome.issue complex type.
    
    A single issue associated with the action.
    """

    severity: str  # fatal | error | warning | information
    code: str  # Issue type code
    details: Optional[CodeableConcept] = None
    diagnostics: Optional[str] = None
    location: List[str] = field(default_factory=list)  # XPath or JSONPath expressions
    expression: List[str] = field(default_factory=list)  # FHIRPath expressions
    extension: List[Extension] = field(default_factory=list)


@dataclass
class OperationOutcome(FHIRResource):
    """
    FHIR R4 OperationOutcome resource.

    Represents a collection of errors, warnings, or information messages
    that result from a system operation.
    """

    resourceType: str = "OperationOutcome"
    # Issue
    issue: List[OperationOutcomeIssue] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
