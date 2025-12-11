# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ImmunizationEvaluation resource.

ImmunizationEvaluation represents a patient's evaluation of their immunization status.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ImmunizationEvaluation(DomainResource):
    """
    FHIR R4 ImmunizationEvaluation resource.
    
    Represents a patient's evaluation of their immunization status.
    Extends DomainResource.
    """
    
    resourceType: str = "ImmunizationEvaluation"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Status
    status: str  # completed | entered-in-error (required)
    # Patient
    patient: Reference  # Who this evaluation is for (required)
    # Date
    date: Optional[str] = None  # Date evaluation was performed
    # Authority
    authority: Optional[Reference] = None  # Who is responsible for publishing the recommendations
    # Target Disease
    targetDisease: CodeableConcept  # Vaccine preventable disease being evaluated against (required)
    # Immunization Event
    immunizationEvent: Reference  # Immunization being evaluated (required)
    # Dose Status
    doseStatus: CodeableConcept  # Status of the dose relative to published recommendations (required)
    # Dose Status Reason
    doseStatusReason: List[CodeableConcept] = field(default_factory=list)  # Reason for the dose status
    # Description
    description: Optional[str] = None  # Evaluation notes
    # Series
    series: Optional[str] = None  # Name of vaccine series
    # Dose Number Positive Int
    doseNumberPositiveInt: Optional[int] = None  # Dose number within series
    # Dose Number String
    doseNumberString: Optional[str] = None  # Dose number within series
    # Series Doses Positive Int
    seriesDosesPositiveInt: Optional[int] = None  # Recommended number of doses for immunity
    # Series Doses String
    seriesDosesString: Optional[str] = None  # Recommended number of doses for immunity

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


