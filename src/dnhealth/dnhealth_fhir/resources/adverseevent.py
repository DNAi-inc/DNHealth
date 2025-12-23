# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 AdverseEvent resource.

AdverseEvent describes an event that occurred during the care of a patient.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdverseEventSuspectEntity:
    """
    FHIR AdverseEvent.suspectEntity complex type.
    
    Describes the entity that is suspected to have caused the adverse event.
    """
    
    instance: Reference  # Refers to the specific entity that caused the adverse event (required)
    causality: List[Dict[str, Any]] = field(default_factory=list)  # Information on the possible cause of the event
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class AdverseEvent(DomainResource):
    """
    FHIR R4 AdverseEvent resource.
    
    Describes an event that occurred during the care of a patient.
    Extends DomainResource.
    """
    
    resourceType: str = "AdverseEvent"
    # Identifier
    identifier: Optional[Identifier] = None  # Business identifier for the event
    # Actuality
    actuality: Optional[str] = None  # actual | potential (required, validated in __post_init__)
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # product-problem | product-quality | product-use-error | wrong-dose | incorrect-prescribing-information | wrong-technique | wrong-route-of-administration | wrong-rate | wrong-duration | wrong-time | expired-drug | medical-device-use-error | problem-different-manufacturer | unsafe-physical-environment
    # Event
    event: Optional[CodeableConcept] = None  # Type of the event itself in relation to the subject
    # Subject
    subject: Optional[Reference] = None  # Subject impacted by event (required, validated in __post_init__)
    # Encounter
    encounter: Optional[Reference] = None  # Encounter created as part of
    # Date
    date: Optional[str] = None  # When the event occurred
    # Detected
    detected: Optional[str] = None  # When the event was detected
    # Recorded Date
    recordedDate: Optional[str] = None  # When the event was recorded
    # Resulting Condition
    resultingCondition: List[Reference] = field(default_factory=list)  # Effect on the subject due to this event
    # Location
    location: Optional[Reference] = None  # Location where adverse event occurred
    # Seriousness
    seriousness: Optional[CodeableConcept] = None  # Seriousness of the event
    # Severity
    severity: Optional[CodeableConcept] = None  # mild | moderate | severe
    # Outcome
    outcome: Optional[CodeableConcept] = None  # resolved | recovering | ongoing | resolvedWithSequelae | fatal | unknown
    # Recorder
    recorder: Optional[Reference] = None  # Who recorded the adverse event
    # Contributor
    contributor: List[Reference] = field(default_factory=list)  # Parties that may or should contribute or have contributed information to the adverse event
    # Suspect Entity
    suspectEntity: List[AdverseEventSuspectEntity] = field(default_factory=list)  # Describes the entity that is suspected to have caused the adverse event
    # Subject Medical History
    subjectMedicalHistory: List[Reference] = field(default_factory=list)  # AdverseEvent.subjectMedicalHistory
    # Reference Document
    referenceDocument: List[Reference] = field(default_factory=list)  # AdverseEvent.referenceDocument
    # Study
    study: List[Reference] = field(default_factory=list)  # AdverseEvent.study

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


