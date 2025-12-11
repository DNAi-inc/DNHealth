# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ImmunizationRecommendation resource.

ImmunizationRecommendation represents a patient's immunization recommendation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ImmunizationRecommendationRecommendation:
    """
    FHIR ImmunizationRecommendation.recommendation complex type.
    
    Vaccine administration recommendations.
    """
    
    vaccineCode: List[CodeableConcept] = field(default_factory=list)  # Vaccine(s) or vaccine group that pertain to the recommendation
    targetDisease: Optional[CodeableConcept] = None  # Disease to be immunized against
    contraindicatedVaccineCode: List[CodeableConcept] = field(default_factory=list)  # Vaccine which is contraindicated to fulfill the recommendation
    forecastStatus: CodeableConcept  # Vaccine recommendation status (required)
    forecastReason: List[CodeableConcept] = field(default_factory=list)  # Vaccine administration status reason
    dateCriterion: List[Any] = field(default_factory=list)  # Dates governing proposed immunization
    description: Optional[str] = None  # Protocol details
    series: Optional[str] = None  # Name of vaccination series
    doseNumberPositiveInt: Optional[int] = None  # Recommended dose number within series
    doseNumberString: Optional[str] = None  # Recommended dose number within series
    seriesDosesPositiveInt: Optional[int] = None  # Recommended number of doses for immunity
    seriesDosesString: Optional[str] = None  # Recommended number of doses for immunity
    supportingImmunization: List[Reference] = field(default_factory=list)  # Past immunizations supporting recommendation
    supportingPatientInformation: List[Reference] = field(default_factory=list)  # Patient observations supporting recommendation
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImmunizationRecommendation(DomainResource):
    """
    FHIR R4 ImmunizationRecommendation resource.
    
    Represents a patient's immunization recommendation.
    Extends DomainResource.
    """
    
    resourceType: str = "ImmunizationRecommendation"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Patient
    patient: Reference  # Who this profile is for (required)
    # Date
    date: str  # Date recommendation created (required)
    # Authority
    authority: Optional[Reference] = None  # Who is responsible for protocol
    # Recommendation
    recommendation: List[ImmunizationRecommendationRecommendation] = field(default_factory=list)  # Vaccine administration recommendations (required)

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


