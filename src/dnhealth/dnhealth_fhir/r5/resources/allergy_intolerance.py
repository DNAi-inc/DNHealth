# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 AllergyIntolerance resource.

Risk of harmful or undesirable, physiological response which is unique to an individual and associated with exposure to a substance.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Age, Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Range, Reference
from typing import Any, List, Optional

@dataclass
class AllergyIntoleranceParticipant:
    """
    AllergyIntoleranceParticipant nested class.
    """

    actor: Optional[Reference] = None  # Indicates who or what participated in the activities related to the allergy or intolerance.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the actor in the activities related to the allergy or in...

@dataclass
class AllergyIntoleranceReaction:
    """
    AllergyIntoleranceReaction nested class.
    """

    manifestation: List[Any] = field(default_factory=list)  # Clinical symptoms and/or signs that are observed or associated with the adverse reaction event.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    substance: Optional[CodeableConcept] = None  # Identification of the specific substance (or pharmaceutical product) considered to be responsible...
    description: Optional[str] = None  # Text description about the reaction as a whole, including details of the manifestation if required.
    onset: Optional[str] = None  # Record of the date and/or time of the onset of the Reaction.
    severity: Optional[str] = None  # Clinical assessment of the severity of the reaction event as a whole, potentially considering mul...
    exposureRoute: Optional[CodeableConcept] = None  # Identification of the route by which the subject was exposed to the substance.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional text about the adverse reaction event not captured in other fields.


@dataclass
class AllergyIntolerance(FHIRResource):
    """
    Risk of harmful or undesirable, physiological response which is unique to an individual and associated with exposure to a substance.
    """

    patient: Optional[Reference] = None  # The patient who has the allergy or intolerance.
    resourceType: str = "AllergyIntolerance"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this AllergyIntolerance by the performer or other systems which ...
    clinicalStatus: Optional[CodeableConcept] = None  # The clinical status of the allergy or intolerance.
    verificationStatus: Optional[CodeableConcept] = None  # Assertion about certainty associated with the propensity, or potential risk, of a reaction to the...
    type: Optional[CodeableConcept] = None  # Identification of the underlying physiological mechanism for the reaction risk.
    category: Optional[List[str]] = field(default_factory=list)  # Category of the identified substance.
    criticality: Optional[str] = None  # Estimate of the potential clinical harm, or seriousness, of the reaction to the identified substa...
    code: Optional[CodeableConcept] = None  # Code for an allergy or intolerance statement (either a positive or a negated/excluded statement)....
    encounter: Optional[Reference] = None  # The encounter when the allergy or intolerance was asserted.
    onset: Optional[Any] = None  # Estimated or actual date,  date-time, or age when allergy or intolerance was identified.
    recordedDate: Optional[str] = None  # The recordedDate represents when this particular AllergyIntolerance record was created in the sys...
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what participated in the activities related to the allergy or intolerance and ho...
    lastOccurrence: Optional[str] = None  # Represents the date and/or time of the last known occurrence of a reaction event.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional narrative about the propensity for the Adverse Reaction, not captured in other fields.
    reaction: Optional[List[BackboneElement]] = field(default_factory=list)  # Details about each adverse reaction event linked to exposure to the identified substance.