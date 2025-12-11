# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 QuestionnaireResponse resource.

Complete QuestionnaireResponse resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Attachment,
    Period,
    Quantity,
    Coding,
)


@dataclass
class QuestionnaireResponseItemAnswer:
    """
    The response(s) to the question.
    
    The respondent's answer(s) to the question.
    """

    valueBoolean: Optional[bool] = None
    valueDecimal: Optional[float] = None
    valueInteger: Optional[int] = None
    valueDate: Optional[str] = None  # YYYY-MM-DD
    valueDateTime: Optional[str] = None  # ISO 8601 dateTime
    valueTime: Optional[str] = None  # HH:MM:SS
    valueString: Optional[str] = None
    valueUri: Optional[str] = None
    valueAttachment: Optional[Attachment] = None
    valueCoding: Optional["Coding"] = None
    valueQuantity: Optional[Quantity] = None
    valueReference: Optional[Reference] = None
    item: List["QuestionnaireResponseItem"] = field(default_factory=list)  # Nested questionnaire response items
    extension: List[Extension] = field(default_factory=list)


@dataclass
class QuestionnaireResponseItem:
    """
    Groups and questions.
    
    A group or question item from the original questionnaire for which answers
    are provided.
    """

    linkId: str  # Pointer to specific item from Questionnaire (required)
    definition: Optional[str] = None  # ElementDefinition - details of the item
    text: Optional[str] = None  # Name for group or question text
    answer: List[QuestionnaireResponseItemAnswer] = field(default_factory=list)  # The response(s) to the question
    item: List["QuestionnaireResponseItem"] = field(default_factory=list)  # Nested questionnaire response items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class QuestionnaireResponse(FHIRResource):
    """
    FHIR R4 QuestionnaireResponse resource.

    Represents a structured set of answers to questions, filled out when
    responding to a structured questionnaire.
    """

    resourceType: str = "QuestionnaireResponse"
    # Identifiers
    identifier: Optional[Identifier] = None
    # Based on
    basedOn: List[Reference] = field(default_factory=list)
    # Part of
    partOf: List[Reference] = field(default_factory=list)
    # Questionnaire
    questionnaire: Optional[str] = None  # Canonical URL to Questionnaire
    # Status
    status: str  # in-progress | completed | amended | entered-in-error | stopped (required)
    # Subject
    subject: Optional[Reference] = None
    # Encounter
    encounter: Optional[Reference] = None
    # Authored
    authored: Optional[str] = None  # ISO 8601 dateTime
    # Author
    author: Optional[Reference] = None
    # Source
    source: Optional[Reference] = None
    # Item
    item: List[QuestionnaireResponseItem] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
