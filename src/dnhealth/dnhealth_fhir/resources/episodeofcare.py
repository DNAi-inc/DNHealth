# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 EpisodeOfCare resource.

EpisodeOfCare represents an association of a Patient with an Organization and/or Healthcare Provider(s) for a period of time.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class EpisodeOfCareStatusHistory:
    """
    FHIR EpisodeOfCare.statusHistory complex type.
    
    The history of statuses that the EpisodeOfCare has been through.
    """
    
    status: str  # planned | waitlist | active | onhold | finished | cancelled | entered-in-error (required)
    period: Period  # Duration the EpisodeOfCare was in the specified status (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EpisodeOfCareDiagnosis:
    """
    FHIR EpisodeOfCare.diagnosis complex type.
    
    The list of diagnosis relevant to this episode of care.
    """
    
    condition: Reference  # Conditions/problems/diagnoses this episode of care addresses (required)
    role: Optional[CodeableConcept] = None  # Role that this diagnosis has within the episode of care
    rank: Optional[int] = None  # Ranking of the diagnosis (for each role type)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class EpisodeOfCare(DomainResource):
    """
    FHIR R4 EpisodeOfCare resource.
    
    Represents an association of a Patient with an Organization and/or Healthcare Provider(s) for a period of time.
    Extends DomainResource.
    """
    
    resourceType: str = "EpisodeOfCare"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier(s) relevant for this EpisodeOfCare
    # Status
    status: str  # planned | waitlist | active | onhold | finished | cancelled | entered-in-error (required)
    # Status History
    statusHistory: List[EpisodeOfCareStatusHistory] = field(default_factory=list)  # The history of statuses that the EpisodeOfCare has been through
    # Type
    type: List[CodeableConcept] = field(default_factory=list)  # Type/class - e.g. specialist referral, disease management
    # Diagnosis
    diagnosis: List[EpisodeOfCareDiagnosis] = field(default_factory=list)  # The list of diagnosis relevant to this episode of care
    # Patient
    patient: Reference  # The patient who is the focus of this episode of care (required)
    # Managing Organization
    managingOrganization: Optional[Reference] = None  # Organization that assumes care
    # Period
    period: Optional[Period] = None  # Interval during responsibility is assumed
    # Referral Request
    referralRequest: List[Reference] = field(default_factory=list)  # Originating Referral Request(s)
    # Care Manager
    careManager: Optional[Reference] = None  # Care manager/care coordinator for the patient
    # Team
    team: List[Reference] = field(default_factory=list)  # Other practitioners facilitating this episode of care
    # Account
    account: List[Reference] = field(default_factory=list)  # The set of accounts that may be used for billing for this EpisodeOfCare

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


