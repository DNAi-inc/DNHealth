# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ConditionDefinition resource.

A definition of a condition and information relevant to managing it.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Quantity, Reference, UsageContext
from typing import Any, List, Optional

@dataclass
class ConditionDefinitionObservation:
    """
    ConditionDefinitionObservation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # Category that is relevant.
    code: Optional[CodeableConcept] = None  # Code for relevant Observation.

@dataclass
class ConditionDefinitionMedication:
    """
    ConditionDefinitionMedication nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # Category that is relevant.
    code: Optional[CodeableConcept] = None  # Code for relevant Medication.

@dataclass
class ConditionDefinitionPrecondition:
    """
    ConditionDefinitionPrecondition nested class.
    """

    type: Optional[str] = None  # Kind of pre-condition.
    code: Optional[CodeableConcept] = None  # Code for relevant Observation.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # Value of Observation.

@dataclass
class ConditionDefinitionQuestionnaire:
    """
    ConditionDefinitionQuestionnaire nested class.
    """

    purpose: Optional[str] = None  # Use of the questionnaire.
    reference: Optional[Reference] = None  # Specific Questionnaire.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ConditionDefinitionPlan:
    """
    ConditionDefinitionPlan nested class.
    """

    reference: Optional[Reference] = None  # The actual plan.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    role: Optional[CodeableConcept] = None  # Use for the plan.


@dataclass
class ConditionDefinition(FHIRResource):
    """
    A definition of a condition and information relevant to managing it.
    """

    status: Optional[str] = None  # The status of this condition definition. Enables tracking the life-cycle of the content.
    code: Optional[CodeableConcept] = None  # Identification of the condition, problem or diagnosis.
    resourceType: str = "ConditionDefinition"
    url: Optional[str] = None  # An absolute URI that is used to identify this condition definition when it is referenced in a spe...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this condition definition when it is represented in ...
    version: Optional[str] = None  # The identifier that is used to identify this version of the condition definition when it is refer...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the condition definition. This name should be usable as an id...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the condition definition.
    subtitle: Optional[str] = None  # An explanatory or alternate title for the event definition giving additional information about it...
    experimental: Optional[bool] = None  # A Boolean value to indicate that this condition definition is authored for testing purposes (or e...
    date: Optional[str] = None  # The date  (and optionally time) when the condition definition was last significantly changed. The...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the condition definition from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the condition definition is intended to be used.
    severity: Optional[CodeableConcept] = None  # A subjective assessment of the severity of the condition as evaluated by the clinician.
    bodySite: Optional[CodeableConcept] = None  # The anatomical location where this condition manifests itself.
    stage: Optional[CodeableConcept] = None  # Clinical stage or grade of a condition. May include formal severity assessments.
    hasSeverity: Optional[bool] = None  # Whether Severity is appropriate to collect for this condition.
    hasBodySite: Optional[bool] = None  # Whether bodySite is appropriate to collect for this condition.
    hasStage: Optional[bool] = None  # Whether stage is appropriate to collect for this condition.
    definition: Optional[List[str]] = field(default_factory=list)  # Formal definitions of the condition. These may be references to ontologies, published clinical pr...
    observation: Optional[List[BackboneElement]] = field(default_factory=list)  # Observations particularly relevant to this condition.
    medication: Optional[List[BackboneElement]] = field(default_factory=list)  # Medications particularly relevant for this condition.
    precondition: Optional[List[BackboneElement]] = field(default_factory=list)  # An observation that suggests that this condition applies.
    team: Optional[List[Reference]] = field(default_factory=list)  # Appropriate team for this condition.
    questionnaire: Optional[List[BackboneElement]] = field(default_factory=list)  # Questionnaire for this condition.
    plan: Optional[List[BackboneElement]] = field(default_factory=list)  # Plan that is appropriate.