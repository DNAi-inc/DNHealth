# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicationAdministration resource.

Complete MedicationAdministration resource with all R4 elements.
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
    Quantity,
    Ratio,
    Period,
)


@dataclass
class MedicationAdministrationPerformer:
    """
    Who performed the medication administration and what they did.
    """

    function: Optional[CodeableConcept] = None
    actor: Reference  # Who performed the medication administration (required)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationAdministrationDosage:
    """
    Details of how medication was taken.
    
    Describes the medication dosage information.
    """

    text: Optional[str] = None
    site: Optional[CodeableConcept] = None
    route: Optional[CodeableConcept] = None
    method: Optional[CodeableConcept] = None
    dose: Optional[Quantity] = None
    rateRatio: Optional["Ratio"] = None
    rateQuantity: Optional[Quantity] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationAdministration(FHIRResource):
    """
    FHIR R4 MedicationAdministration resource.

    Represents the administration of a medication to a patient.
    """

    resourceType: str = "MedicationAdministration"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Instantiates
    instantiates: List[str] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    status: str  # in-progress | not-done | on-hold | completed | entered-in-error | stopped | unknown
    # Status reason
    statusReason: List[CodeableConcept] = field(default_factory=list)
    # Category
    category: Optional[CodeableConcept] = None
    # Medication codeable concept
    medicationCodeableConcept: Optional[CodeableConcept] = None
    # Medication reference
    medicationReference: Optional[Reference] = None
    # Subject
    subject: Reference  # Who received the medication (required)
    # Context
    context: Optional[Reference] = None
    # Supporting information
    supportingInformation: List[Reference] = field(default_factory=list)
    # Effective dateTime
    effectiveDateTime: Optional[str] = None  # ISO 8601 dateTime
    # Effective period
    effectivePeriod: Optional["Period"] = None
    # Performer
    performer: List[MedicationAdministrationPerformer] = field(default_factory=list)
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Request
    request: Optional[Reference] = None
    # Device
    device: List[Reference] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Dosage
    dosage: Optional[MedicationAdministrationDosage] = None
    # Event history
    eventHistory: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
