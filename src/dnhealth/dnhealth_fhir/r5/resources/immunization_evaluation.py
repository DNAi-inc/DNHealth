# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ImmunizationEvaluation resource.

Describes a comparison of an immunization event against published recommendations to determine if the administration is "valid" in relation to those  recommendations.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Reference
from typing import List, Optional

@dataclass
class ImmunizationEvaluation(FHIRResource):
    """
    Describes a comparison of an immunization event against published recommendations to determine if the administration is "valid" in relation to those  recommendations.
    """

    status: Optional[str] = None  # Indicates the current status of the evaluation of the vaccination administration event.
    patient: Optional[Reference] = None  # The individual for whom the evaluation is being done.
    targetDisease: Optional[CodeableConcept] = None  # The vaccine preventable disease the dose is being evaluated against.
    immunizationEvent: Optional[Reference] = None  # The vaccine administration event being evaluated.
    doseStatus: Optional[CodeableConcept] = None  # Indicates if the dose is valid or not valid with respect to the published recommendations.
    resourceType: str = "ImmunizationEvaluation"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this immunization evaluation record.
    date: Optional[str] = None  # The date the evaluation of the vaccine administration event was performed.
    authority: Optional[Reference] = None  # Indicates the authority who published the protocol (e.g. ACIP).
    doseStatusReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # Provides an explanation as to why the vaccine administration event is valid or not relative to th...
    description: Optional[str] = None  # Additional information about the evaluation.
    series: Optional[str] = None  # One possible path to achieve presumed immunity against a disease - within the context of an autho...
    doseNumber: Optional[str] = None  # Nominal position in a series as determined by the outcome of the evaluation process.
    seriesDoses: Optional[str] = None  # The recommended number of doses to achieve immunity as determined by the outcome of the evaluatio...