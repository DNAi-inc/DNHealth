# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Procedure resource.

Complete Procedure resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Period,
    Age,
    Range,
)


@dataclass
class ProcedurePerformer:
    """
    Who performed the procedure.
    
    Limited to "real" people rather than equipment.
    """

    function: Optional[CodeableConcept] = None
    # Note: actor is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce actor is provided.
    actor: Optional[Reference] = None  # The practitioner who performed the procedure (required)
    onBehalfOf: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class ProcedureFocalDevice:
    """
    Device changed in procedure.
    
    A device that is implanted, removed, or otherwise manipulated (calibration,
    battery replacement, fitting a prosthesis, attaching a wound-vac, etc.)
    as a focal portion of the Procedure.
    """

    action: Optional[CodeableConcept] = None
    # Note: manipulated is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce manipulated is provided.
    manipulated: Optional[Reference] = None  # Device that was changed (required)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Procedure(FHIRResource):
    """
    FHIR R4 Procedure resource.

    Represents an action that is or was performed on or for a patient.
    """

    resourceType: str = "Procedure"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Instantiates canonical
    instantiatesCanonical: List[str] = field(default_factory=list)
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown (required in FHIR)
    # Status reason
    statusReason: Optional[CodeableConcept] = None
    # Category
    category: Optional[CodeableConcept] = None
    # Code
    code: Optional[CodeableConcept] = None
    # Subject
    # Note: subject is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce subject is provided.
    subject: Optional[Reference] = None  # Who the procedure was performed on (required)
    # Encounter
    encounter: Optional[Reference] = None
    # Performed dateTime
    performedDateTime: Optional[str] = None  # ISO 8601 dateTime
    # Performed period
    performedPeriod: Optional["Period"] = None
    # Performed string
    performedString: Optional[str] = None
    # Performed age
    performedAge: Optional["Age"] = None
    # Performed range
    performedRange: Optional["Range"] = None
    # Recorder
    recorder: Optional[Reference] = None
    # Asserter
    asserter: Optional[Reference] = None
    # Performer
    performer: List[ProcedurePerformer] = field(default_factory=list)
    # Location
    location: Optional[Reference] = None
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Reason reference
    reasonReference: List[Reference] = field(default_factory=list)
    # Body site
    bodySite: List[CodeableConcept] = field(default_factory=list)
    # Outcome
    outcome: Optional[CodeableConcept] = None
    # Report
    report: List[Reference] = field(default_factory=list)
    # Complication
    complication: List[CodeableConcept] = field(default_factory=list)
    # Complication detail
    complicationDetail: List[Reference] = field(default_factory=list)
    # Follow up
    followUp: List[CodeableConcept] = field(default_factory=list)
    # Note
    note: List[Annotation] = field(default_factory=list)
    # Focal device
    focalDevice: List[ProcedureFocalDevice] = field(default_factory=list)
    # Used reference
    usedReference: List[Reference] = field(default_factory=list)
    # Used code
    usedCode: List[CodeableConcept] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
