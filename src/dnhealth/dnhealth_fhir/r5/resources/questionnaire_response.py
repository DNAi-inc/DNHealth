# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 QuestionnaireResponse resource.

A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, Coding, Extension, Identifier, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class QuestionnaireResponseItem:
    """
    QuestionnaireResponseItem nested class.
    """

    linkId: Optional[str] = None  # The item from the Questionnaire that corresponds to this item in the QuestionnaireResponse resource.
    value: Optional[Any] = None  # The answer (or one of the answers) provided by the respondent to the question.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    definition: Optional[str] = None  # A reference to an [ElementDefinition](elementdefinition.html) that provides the details for the i...
    text: Optional[str] = None  # Text that is displayed above the contents of the group or as the text of the question being answe...
    answer: Optional[List[BackboneElement]] = field(default_factory=list)  # The respondent's answer(s) to the question.
    item: Optional[List[Any]] = field(default_factory=list)  # Nested groups and/or questions found within this particular answer.

@dataclass
class QuestionnaireResponseItemAnswer:
    """
    QuestionnaireResponseItemAnswer nested class.
    """

    value: Optional[Any] = None  # The answer (or one of the answers) provided by the respondent to the question.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    item: Optional[List[Any]] = field(default_factory=list)  # Nested groups and/or questions found within this particular answer.


@dataclass
class QuestionnaireResponse(FHIRResource):
    """
    A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.
    """

    questionnaire: Optional[str] = None  # The Questionnaire that defines and organizes the questions for which answers are being provided.
    status: Optional[str] = None  # The current state of the questionnaire response.
    resourceType: str = "QuestionnaireResponse"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this questionnaire response by the performer and/or other system...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan, proposal or order that is fulfilled in whole or in part by this questionnaire response.  ...
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A procedure or observation that this questionnaire was performed as part of the execution of.  Fo...
    subject: Optional[Reference] = None  # The subject of the questionnaire response.  This could be a patient, organization, practitioner, ...
    encounter: Optional[Reference] = None  # The Encounter during which this questionnaire response was created or to which the creation of th...
    authored: Optional[str] = None  # The date and/or time that this questionnaire response was last modified by the user - e.g. changi...
    author: Optional[Reference] = None  # The individual or device that received the answers to the questions in the QuestionnaireResponse ...
    source: Optional[Reference] = None  # The individual or device that answered the questions about the subject.
    item: Optional[List[BackboneElement]] = field(default_factory=list)  # A group or question item from the original questionnaire for which answers are provided.