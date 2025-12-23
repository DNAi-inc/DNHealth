# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ClinicalUseDefinition resource.

A single issue - either an indication, contraindication, interaction or an undesirable effect for a medicinal product, medication, device or procedure.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Expression, Extension, Identifier, Range, Reference
from typing import Any, List, Optional

@dataclass
class ClinicalUseDefinitionContraindication:
    """
    ClinicalUseDefinitionContraindication nested class.
    """

    relationshipType: Optional[CodeableConcept] = None  # The type of relationship between the medicinal product indication or contraindication and another...
    treatment: Optional[Any] = None  # Reference to a specific medication (active substance, medicinal product or class of products, bio...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    diseaseSymptomProcedure: Optional[Any] = None  # The situation that is being documented as contraindicating against this item.
    diseaseStatus: Optional[Any] = None  # The status of the disease or symptom for the contraindication, for example \"chronic\" or \"metas...
    comorbidity: Optional[List[Any]] = field(default_factory=list)  # A comorbidity (concurrent condition) or coinfection.
    indication: Optional[List[Reference]] = field(default_factory=list)  # The indication which this is a contraidication for.
    applicability: Optional[Expression] = None  # An expression that returns true or false, indicating whether the indication is applicable or not,...
    otherTherapy: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about the use of the medicinal product in relation to other therapies described as pa...

@dataclass
class ClinicalUseDefinitionContraindicationOtherTherapy:
    """
    ClinicalUseDefinitionContraindicationOtherTherapy nested class.
    """

    relationshipType: Optional[CodeableConcept] = None  # The type of relationship between the medicinal product indication or contraindication and another...
    treatment: Optional[Any] = None  # Reference to a specific medication (active substance, medicinal product or class of products, bio...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ClinicalUseDefinitionIndication:
    """
    ClinicalUseDefinitionIndication nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    diseaseSymptomProcedure: Optional[Any] = None  # The situation that is being documented as an indicaton for this item.
    diseaseStatus: Optional[Any] = None  # The status of the disease or symptom for the indication, for example \"chronic\" or \"metastatic\".
    comorbidity: Optional[List[Any]] = field(default_factory=list)  # A comorbidity (concurrent condition) or coinfection as part of the indication.
    intendedEffect: Optional[Any] = None  # The intended effect, aim or strategy to be achieved.
    duration: Optional[Any] = None  # Timing or duration information, that may be associated with use with the indicated condition e.g....
    undesirableEffect: Optional[List[Reference]] = field(default_factory=list)  # An unwanted side effect or negative outcome that may happen if you use the drug (or other subject...
    applicability: Optional[Expression] = None  # An expression that returns true or false, indicating whether the indication is applicable or not,...
    otherTherapy: Optional[List[Any]] = field(default_factory=list)  # Information about the use of the medicinal product in relation to other therapies described as pa...

@dataclass
class ClinicalUseDefinitionInteraction:
    """
    ClinicalUseDefinitionInteraction nested class.
    """

    item: Optional[Any] = None  # The specific medication, product, food, substance etc. or laboratory test that interacts.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    interactant: Optional[List[BackboneElement]] = field(default_factory=list)  # The specific medication, product, food, substance etc. or laboratory test that interacts.
    type: Optional[CodeableConcept] = None  # The type of the interaction e.g. drug-drug interaction, drug-food interaction, drug-lab test inte...
    effect: Optional[Any] = None  # The effect of the interaction, for example \"reduced gastric absorption of primary medication\".
    incidence: Optional[CodeableConcept] = None  # The incidence of the interaction, e.g. theoretical, observed.
    management: Optional[List[CodeableConcept]] = field(default_factory=list)  # Actions for managing the interaction.

@dataclass
class ClinicalUseDefinitionInteractionInteractant:
    """
    ClinicalUseDefinitionInteractionInteractant nested class.
    """

    item: Optional[Any] = None  # The specific medication, product, food, substance etc. or laboratory test that interacts.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ClinicalUseDefinitionUndesirableEffect:
    """
    ClinicalUseDefinitionUndesirableEffect nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    symptomConditionEffect: Optional[Any] = None  # The situation in which the undesirable effect may manifest.
    classification: Optional[CodeableConcept] = None  # High level classification of the effect.
    frequencyOfOccurrence: Optional[CodeableConcept] = None  # How often the effect is seen.

@dataclass
class ClinicalUseDefinitionWarning:
    """
    ClinicalUseDefinitionWarning nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # A textual definition of this warning, with formatting.
    code: Optional[CodeableConcept] = None  # A coded or unformatted textual definition of this warning.


@dataclass
class ClinicalUseDefinition(FHIRResource):
    """
    A single issue - either an indication, contraindication, interaction or an undesirable effect for a medicinal product, medication, device or procedure.
    """

    type: Optional[str] = None  # indication | contraindication | interaction | undesirable-effect | warning.
    resourceType: str = "ClinicalUseDefinition"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for this issue.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A categorisation of the issue, primarily for dividing warnings into subject heading areas such as...
    subject: Optional[List[Reference]] = field(default_factory=list)  # The medication, product, substance, device, procedure etc. for which this is an indication.
    status: Optional[CodeableConcept] = None  # Whether this is a current issue or one that has been retired etc.
    contraindication: Optional[BackboneElement] = None  # Specifics for when this is a contraindication.
    indication: Optional[BackboneElement] = None  # Specifics for when this is an indication.
    interaction: Optional[BackboneElement] = None  # Specifics for when this is an interaction.
    population: Optional[List[Reference]] = field(default_factory=list)  # The population group to which this applies.
    library: Optional[List[str]] = field(default_factory=list)  # Logic used by the clinical use definition.
    undesirableEffect: Optional[BackboneElement] = None  # Describe the possible undesirable effects (negative outcomes) from the use of the medicinal produ...
    warning: Optional[BackboneElement] = None  # A critical piece of information about environmental, health or physical risks or hazards that ser...