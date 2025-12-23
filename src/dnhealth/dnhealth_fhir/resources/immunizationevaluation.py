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
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # completed | entered-in-error (required in FHIR)
    # Patient
    # Note: patient is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce patient is provided.
    patient: Optional[Reference] = None  # Who this evaluation is for (required)
    # Date
    date: Optional[str] = None  # Date evaluation was performed
    # Authority
    authority: Optional[Reference] = None  # Who is responsible for publishing the recommendations
    # Target Disease
    # Note: targetDisease is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce targetDisease is provided.
    targetDisease: Optional[CodeableConcept] = None  # Vaccine preventable disease being evaluated against (required)
    # Immunization Event
    # Note: immunizationEvent is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce immunizationEvent is provided.
    immunizationEvent: Optional[Reference] = None  # Immunization being evaluated (required)
    # Dose Status
    # Note: doseStatus is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce doseStatus is provided.
    doseStatus: Optional[CodeableConcept] = None  # Status of the dose relative to published recommendations (required)
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


