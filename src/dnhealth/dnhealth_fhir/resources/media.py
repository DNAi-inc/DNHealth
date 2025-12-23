# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Media resource.

Complete Media resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Attachment,
    Period,
    Annotation,
)


@dataclass
class Media(FHIRResource):
    """
    FHIR R4 Media resource.

    Represents a photo, video, or audio recording acquired or used in
    healthcare.
    """

    resourceType: str = "Media"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown (required in FHIR)
    # Type
    type: Optional[CodeableConcept] = None
    # Modality
    modality: Optional[CodeableConcept] = None
    # View
    view: Optional[CodeableConcept] = None
    # Subject
    subject: Optional[Reference] = None
    # Encounter
    encounter: Optional[Reference] = None
    # Created dateTime
    createdDateTime: Optional[str] = None  # ISO 8601 dateTime
    # Created period
    createdPeriod: Optional[Period] = None
    # Issued
    issued: Optional[str] = None  # ISO 8601 instant
    # Operator
    operator: Optional[Reference] = None
    # Reason code
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    # Body site
    bodySite: Optional[CodeableConcept] = None
    # Device name
    deviceName: Optional[str] = None
    # Height
    height: Optional[int] = None  # Height of the image in pixels (photo/video)
    # Width
    width: Optional[int] = None  # Width of the image in pixels (photo/video)
    # Frames
    frames: Optional[int] = None  # Number of frames if > 1 (photo)
    # Duration
    duration: Optional[float] = None  # Length in seconds (audio / video)
    # Content
    # Note: content is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce content is provided.
    content: Optional[Attachment] = None  # Actual media - file or stream (required)
    # Note
    note: List[Annotation] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
