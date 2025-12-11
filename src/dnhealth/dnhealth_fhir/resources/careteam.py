# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CareTeam resource.

CareTeam represents a team of healthcare providers who work together to provide care.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CareTeamParticipant:
    """
    FHIR CareTeam.participant complex type.
    
    Identifies all people and organizations who are expected to be involved in the care team.
    """
    
    role: List[CodeableConcept] = field(default_factory=list)  # Type of involvement
    member: Optional[Reference] = None  # Who is involved
    onBehalfOf: Optional[Reference] = None  # Organization of the person
    period: Optional[Period] = None  # Time period of participant
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CareTeam(DomainResource):
    """
    FHIR R4 CareTeam resource.
    
    Represents a team of healthcare providers who work together to provide care.
    Extends DomainResource.
    """
    
    resourceType: str = "CareTeam"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External Ids for this team
    # Status
    status: Optional[str] = None  # proposed | active | suspended | inactive | entered-in-error
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Type of team
    # Name
    name: Optional[str] = None  # Name of the team
    # Subject
    subject: Optional[Reference] = None  # Who care team is for
    # Encounter
    encounter: Optional[Reference] = None  # Encounter created as part of
    # Period
    period: Optional[Period] = None  # Time period team covers
    # Participant
    participant: List[CareTeamParticipant] = field(default_factory=list)  # Members of the team
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # Why the care team exists
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # Why the care team exists
    # Managing Organization
    managingOrganization: List[Reference] = field(default_factory=list)  # Organization responsible for the care team
    # Telecom
    telecom: List[Any] = field(default_factory=list)  # Contact details for the care team
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments made about the CareTeam

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


