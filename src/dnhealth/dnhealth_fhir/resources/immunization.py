# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Immunization resource.

Immunization represents a record of immunization.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Annotation, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ImmunizationPerformer:
    """
    FHIR Immunization.performer complex type.
    
    Who performed the immunization.
    """
    
    function: Optional[CodeableConcept] = None  # What type of performance was done
    # Note: actor is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce actor is provided.
    actor: Optional[Reference] = None  # Individual or organization who was performing (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImmunizationEducation:
    """
    FHIR Immunization.education complex type.
    
    Educational material presented to the patient (or guardian) at the time of vaccine administration.
    """
    
    documentType: Optional[str] = None  # Educational material document identifier
    reference: Optional[str] = None  # Educational material reference pointer
    publicationDate: Optional[str] = None  # Educational material publication date
    presentationDate: Optional[str] = None  # Educational material presentation date
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImmunizationReaction:
    """
    FHIR Immunization.reaction complex type.
    
    Categorical data indicating that an adverse event is associated with a particular immunization.
    """
    
    date: Optional[str] = None  # When reaction started
    detail: Optional[Reference] = None  # Additional information on reaction
    reported: Optional[bool] = None  # Indicates self-reported reaction
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImmunizationProtocolApplied:
    """
    FHIR Immunization.protocolApplied complex type.
    
    The protocol (set of recommendations) being followed by the provider who administered the dose.
    """
    
    series: Optional[str] = None  # Name of vaccine series
    authority: Optional[Reference] = None  # Who is responsible for publishing the recommendations
    targetDisease: List[CodeableConcept] = field(default_factory=list)  # Vaccine preventatable disease being targeted
    doseNumberPositiveInt: Optional[int] = None  # Dose number within series
    doseNumberString: Optional[str] = None  # Dose number within series
    seriesDosesPositiveInt: Optional[int] = None  # Recommended number of doses for immunity
    seriesDosesString: Optional[str] = None  # Recommended number of doses for immunity
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Immunization(DomainResource):
    """
    FHIR R4 Immunization resource.
    
    Represents a record of immunization.
    Extends DomainResource.
    """
    
    resourceType: str = "Immunization"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # completed | entered-in-error | not-done (required in FHIR)
    # Status Reason
    statusReason: Optional[CodeableConcept] = None  # Reason not done
    # Vaccine Code
    # Note: vaccineCode is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce vaccineCode is provided.
    vaccineCode: Optional[CodeableConcept] = None  # Vaccine product administered (required)
    # Patient
    # Note: patient is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce patient is provided.
    patient: Optional[Reference] = None  # Who was immunized (required)
    # Encounter
    encounter: Optional[Reference] = None  # Encounter immunization was part of
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # Vaccine administration date
    # Occurrence String
    occurrenceString: Optional[str] = None  # Vaccine administration date
    # Recorded
    recorded: Optional[str] = None  # When the immunization was first captured in the subject's record
    # Primary Source
    primarySource: Optional[bool] = None  # Indicates context the data was recorded in
    # Report Origin
    reportOrigin: Optional[CodeableConcept] = None  # Indicates the source of a secondarily reported record
    # Location
    location: Optional[Reference] = None  # Where immunization occurred
    # Manufacturer
    manufacturer: Optional[Reference] = None  # Vaccine manufacturer
    # Lot Number
    lotNumber: Optional[str] = None  # Vaccine lot number
    # Expiration Date
    expirationDate: Optional[str] = None  # Vaccine expiration date
    # Site
    site: Optional[CodeableConcept] = None  # Body site vaccine was administered
    # Route
    route: Optional[CodeableConcept] = None  # How vaccine entered body
    # Dose Quantity
    doseQuantity: Optional[Quantity] = None  # Amount of vaccine administered
    # Performer
    performer: List[ImmunizationPerformer] = field(default_factory=list)  # Who performed the immunization
    # Note
    note: List[Annotation] = field(default_factory=list)  # Additional immunization notes
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why immunization occurred
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why immunization occurred
    # Is Subpotent
    isSubpotent: Optional[bool] = None  # Indicates if the immunization was given subpotently
    # Subpotent Reason
    subpotentReason: List[CodeableConcept] = field(default_factory=list)  # Reason vaccine was administered subpotently
    # Education
    education: List[ImmunizationEducation] = field(default_factory=list)  # Educational material presented to patient
    # Program Eligibility
    programEligibility: List[CodeableConcept] = field(default_factory=list)  # Patient eligibility for a vaccination program
    # Funding Source
    fundingSource: Optional[CodeableConcept] = None  # Funding source for the vaccine
    # Reaction
    reaction: List[ImmunizationReaction] = field(default_factory=list)  # Details of a reaction that follows immunization
    # Protocol Applied
    protocolApplied: List[ImmunizationProtocolApplied] = field(default_factory=list)  # Protocol followed by the provider

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


