# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Provenance resource.

Complete Provenance resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Reference,
    CodeableConcept,
    Signature,
    Period,
)


@dataclass
class ProvenanceAgent:
    """
    Actor involved.
    
    An actor taking a role in an activity for which it can be assigned
    some degree of responsibility for the activity taking place.
    """

    type: Optional[CodeableConcept] = None
    role: List[CodeableConcept] = field(default_factory=list)
    # Note: who is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce who is provided.
    who: Optional[Reference] = None  # Who performed the activity (required)
    onBehalfOf: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class ProvenanceEntity:
    """
    An entity used in this activity.
    """

    # Note: role is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce role is provided.
    role: Optional[str] = None  # derivation | revision | quotation | source | removal (required)
    # Note: what is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce what is provided.
    what: Optional[Reference] = None  # Identity of entity (required)
    agent: List[ProvenanceAgent] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Provenance(FHIRResource):
    """
    FHIR R4 Provenance resource.

    Represents who performed what action on what resource.
    """

    resourceType: str = "Provenance"
    # Target
    target: List[Reference] = field(default_factory=list)  # Target Reference(s) (usually version specific) (required)
    # Occurred period
    occurredPeriod: Optional[Period] = None
    # Occurred dateTime
    occurredDateTime: Optional[str] = None  # ISO 8601 dateTime
    # Recorded
    # Note: recorded is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce recorded is provided.
    recorded: Optional[str] = None  # When the activity was recorded / updated (required) - ISO 8601 instant
    # Policy
    policy: List[str] = field(default_factory=list)  # Policy or plan the activity was defined by
    # Location
    location: Optional[Reference] = None
    # Reason
    reason: List[CodeableConcept] = field(default_factory=list)
    # Activity
    activity: Optional[CodeableConcept] = None
    # Agent
    agent: List[ProvenanceAgent] = field(default_factory=list)
    # Entity
    entity: List[ProvenanceEntity] = field(default_factory=list)
    # Signature
    signature: List[Signature] = field(default_factory=list)


logger = logging.getLogger(__name__)


def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()
