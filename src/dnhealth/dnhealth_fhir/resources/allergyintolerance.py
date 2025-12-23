# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 AllergyIntolerance resource.

AllergyIntolerance represents a risk of harmful or undesirable physiological response
which is specific to an individual and associated with exposure to a substance.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Annotation,
    Age,
    Range,
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AllergyIntoleranceReaction:
    """
    FHIR AllergyIntolerance.reaction complex type.
    
    Details about each adverse reaction event linked to exposure to the identified substance.
    """
    
    # Manifestation (required)
    manifestation: List[CodeableConcept] = field(default_factory=list)  # Clinical symptoms/signs
    # Substance
    substance: Optional[CodeableConcept] = None  # Specific substance that was considered to be responsible
    # Description
    description: Optional[str] = None  # Description of the reaction as a whole
    # Onset
    onset: Optional[str] = None  # Date(/time) when manifestations showed
    # Severity
    severity: Optional[str] = None  # mild | moderate | severe
    # Exposure Route
    exposureRoute: Optional[CodeableConcept] = None  # How the subject was exposed to the substance
    # Note
    note: List[Annotation] = field(default_factory=list)  # Text about event not captured in other fields


@dataclass
class AllergyIntolerance(DomainResource):
    """
    FHIR R4 AllergyIntolerance resource.
    
    Represents a risk of harmful or undesirable physiological response which is specific
    to an individual and associated with exposure to a substance.
    Extends DomainResource.
    """
    
    resourceType: str = "AllergyIntolerance"
    # Patient (required)
    patient: Optional[Reference] = None  # Who the sensitivity is for
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Clinical Status
    clinicalStatus: Optional[CodeableConcept] = None  # active | inactive | resolved
    # Verification Status
    verificationStatus: Optional[CodeableConcept] = None  # unconfirmed | confirmed | refuted | entered-in-error
    # Type
    type: Optional[str] = None  # allergy | intolerance
    # Category
    category: List[str] = field(default_factory=list)  # food | medication | environment | biologic
    # Criticality
    criticality: Optional[str] = None  # low | high | unable-to-assess
    # Code
    code: Optional[CodeableConcept] = None  # Code that identifies the allergy or intolerance
    # Encounter
    encounter: Optional[Reference] = None  # Encounter when the allergy or intolerance was asserted
    # Onset (mutually exclusive options)
    onsetDateTime: Optional[str] = None  # When allergy or intolerance was identified
    onsetAge: Optional[Age] = None  # When allergy or intolerance was identified
    onsetPeriod: Optional[Period] = None  # When allergy or intolerance was identified
    onsetRange: Optional[Range] = None  # When allergy or intolerance was identified
    onsetString: Optional[str] = None  # When allergy or intolerance was identified
    # Recorded Date
    recordedDate: Optional[str] = None  # Date first version of the resource instance was recorded
    # Recorder
    recorder: Optional[Reference] = None  # Who recorded the sensitivity
    # Asserter
    asserter: Optional[Reference] = None  # Source of the information about the allergy
    # Last Occurrence
    lastOccurrence: Optional[str] = None  # Date(/time) of last known occurrence of a reaction
    # Note
    note: List[Annotation] = field(default_factory=list)  # Additional text not captured in other fields
    # Reaction
    reaction: List[AllergyIntoleranceReaction] = field(default_factory=list)  # Adverse Reaction Events
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.patient is None:
            raise ValueError("patient is required for AllergyIntolerance")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
