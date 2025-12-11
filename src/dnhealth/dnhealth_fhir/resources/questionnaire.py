# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Questionnaire resource.

Complete Questionnaire resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    ContactDetail,
    UsageContext,
    RelatedArtifact,
    Period,
)


@dataclass
class QuestionnaireItem:
    """
    Questions and sections within the questionnaire.
    
    A particular question, question group or display text that is part of
    the questionnaire.
    """

    linkId: str  # Unique id for item in questionnaire (required)
    definition: Optional[str] = None  # ElementDefinition - details of the item
    code: List[CodeableConcept] = field(default_factory=list)  # Corresponding concept for this item in a terminology
    prefix: Optional[str] = None  # E.g. "1.1", "2.5.3"
    text: Optional[str] = None  # Primary text for the item
    type: str  # group | display | boolean | decimal | integer | date | dateTime | time | string | text | url | choice | open-choice | attachment | reference | quantity (required)
    enableWhen: List[Any] = field(default_factory=list)  # Only allow data when
    enableBehavior: Optional[str] = None  # all | any
    required: Optional[bool] = None  # Whether the item must be included in data results
    repeats: Optional[bool] = None  # Whether the item may repeat
    readOnly: Optional[bool] = None  # Don't allow human editing
    maxLength: Optional[int] = None  # No more than this many characters
    answerValueSet: Optional[str] = None  # Valueset containing permitted answers
    answerOption: List[Any] = field(default_factory=list)  # Permitted answer
    initial: List[Any] = field(default_factory=list)  # Initial value(s) when item is first rendered
    item: List["QuestionnaireItem"] = field(default_factory=list)  # Nested questionnaire items
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Questionnaire(CanonicalResource):
    """
    FHIR R4 Questionnaire resource.

    Represents a structured set of questions intended to guide the collection
    of answers from end-users.
    """

    resourceType: str = "Questionnaire"
    # URL
    url: Optional[str] = None
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)
    # Version
    version: Optional[str] = None
    # Name
    name: Optional[str] = None
    # Title
    title: Optional[str] = None
    # Derived from
    derivedFrom: List[str] = field(default_factory=list)
    # Status
    status: str  # draft | active | retired | unknown (required)
    # Experimental
    experimental: Optional[bool] = None
    # Subject type
    subjectType: List[str] = field(default_factory=list)  # Resource that can be subject of QuestionnaireResponse
    # Date
    date: Optional[str] = None  # ISO 8601 dateTime
    # Publisher
    publisher: Optional[str] = None
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)
    # Description
    description: Optional[str] = None
    # Use context
    useContext: List[UsageContext] = field(default_factory=list)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)
    # Purpose
    purpose: Optional[str] = None
    # Copyright
    copyright: Optional[str] = None
    # Approval date
    approvalDate: Optional[str] = None  # YYYY-MM-DD
    # Last review date
    lastReviewDate: Optional[str] = None  # YYYY-MM-DD
    # Effective period
    effectivePeriod: Optional[Period] = None
    # Code
    code: List[CodeableConcept] = field(default_factory=list)
    # Item
    item: List[QuestionnaireItem] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
