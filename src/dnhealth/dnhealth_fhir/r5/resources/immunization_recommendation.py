# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ImmunizationRecommendation resource.

A patient's point-in-time set of recommendations (i.e. forecasting) according to a published schedule with optional supporting justification.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Reference
from typing import List, Optional

@dataclass
class ImmunizationRecommendationRecommendation:
    """
    ImmunizationRecommendationRecommendation nested class.
    """

    forecastStatus: Optional[CodeableConcept] = None  # Indicates the patient status with respect to the path to immunity for the target disease.
    code: Optional[CodeableConcept] = None  # Date classification of recommendation.  For example, earliest date to give, latest date to give, ...
    value: Optional[str] = None  # The date whose meaning is specified by dateCriterion.code.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    vaccineCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Vaccine(s) or vaccine group that pertain to the recommendation.
    targetDisease: Optional[List[CodeableConcept]] = field(default_factory=list)  # The targeted disease for the recommendation.
    contraindicatedVaccineCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # Vaccine(s) which should not be used to fulfill the recommendation.
    forecastReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reason for the assigned forecast status.
    dateCriterion: Optional[List[BackboneElement]] = field(default_factory=list)  # Vaccine date recommendations.  For example, earliest date to administer, latest date to administe...
    description: Optional[str] = None  # Contains the description about the protocol under which the vaccine was administered.
    series: Optional[str] = None  # One possible path to achieve presumed immunity against a disease - within the context of an autho...
    doseNumber: Optional[str] = None  # Nominal position of the recommended dose in a series as determined by the evaluation and forecast...
    seriesDoses: Optional[str] = None  # The recommended number of doses to achieve immunity as determined by the evaluation and forecasti...
    supportingImmunization: Optional[List[Reference]] = field(default_factory=list)  # Immunization event history and/or evaluation that supports the status and recommendation.
    supportingPatientInformation: Optional[List[Reference]] = field(default_factory=list)  # Patient Information that supports the status and recommendation.  This includes patient observati...

@dataclass
class ImmunizationRecommendationRecommendationDateCriterion:
    """
    ImmunizationRecommendationRecommendationDateCriterion nested class.
    """

    code: Optional[CodeableConcept] = None  # Date classification of recommendation.  For example, earliest date to give, latest date to give, ...
    value: Optional[str] = None  # The date whose meaning is specified by dateCriterion.code.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class ImmunizationRecommendation(FHIRResource):
    """
    A patient's point-in-time set of recommendations (i.e. forecasting) according to a published schedule with optional supporting justification.
    """

    patient: Optional[Reference] = None  # The patient the recommendation(s) are for.
    date: Optional[str] = None  # The date the immunization recommendation(s) were created.
    recommendation: List[BackboneElement] = field(default_factory=list)  # Vaccine administration recommendations.
    resourceType: str = "ImmunizationRecommendation"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this particular recommendation record.
    authority: Optional[Reference] = None  # Indicates the authority who published the protocol (e.g. ACIP).