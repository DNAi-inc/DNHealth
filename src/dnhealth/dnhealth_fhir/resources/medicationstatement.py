# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicationStatement resource.

Complete MedicationStatement resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Period,
)


@dataclass
class MedicationStatement(FHIRResource):
    """
    FHIR R4 MedicationStatement resource.

    Represents a record of a medication that is being consumed by a patient.
    """

    resourceType: str = "MedicationStatement"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # active | completed | entered-in-error | intended | stopped | on-hold | unknown | not-taken (required in FHIR)
    # Status reason
    statusReason: List[CodeableConcept] = field(default_factory=list)
    # Category
    category: Optional[CodeableConcept] = None
    # Medication codeable concept
    medicationCodeableConcept: Optional[CodeableConcept] = None
    # Medication reference
    medicationReference: Optional[Reference] = None
    # Subject
    # Note: subject is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce subject is provided.
    subject: Optional[Reference] = None  # Who is/was taking the medication (required)
    # Context
    context: Optional[Reference] = None
    # Effective dateTime
    effectiveDateTime: Optional[str] = None  # ISO 8601 dateTime
    # Effective period
    effectivePeriod: Optional[Period] = None
    # Date asserted
    dateAsserted: Optional[str] = None  # ISO 8601 dateTime
    # Information source
    informationSource: Optional[Reference] = None
    # Derived from
    derivedFrom: List[Reference] = field(default_factory=list)
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Dosage (Dosage complex type - using Any for now)
    dosage: List[Any] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
