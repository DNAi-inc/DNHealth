# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Schedule resource.

Complete Schedule resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
)


@dataclass
class Schedule(FHIRResource):
    """
    FHIR R4 Schedule resource.

    Represents a container for slots of time that may be available for
    booking appointments.
    """

    resourceType: str = "Schedule"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Active
    active: Optional[bool] = None
    # Service category
    serviceCategory: List[CodeableConcept] = field(default_factory=list)
    # Service type
    serviceType: List[CodeableConcept] = field(default_factory=list)
    # Specialty
    specialty: List[CodeableConcept] = field(default_factory=list)
    # Actor
    actor: List[Reference] = field(default_factory=list)  # Resource(s) that availability information is about (required)
    # Planning horizon
    planningHorizon: Optional[Period] = None
    # Comment
    comment: Optional[str] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
