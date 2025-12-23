# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 CareTeam resource.

The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, ContactPoint, Extension, Identifier, Period, Reference, Timing
from typing import Any, List, Optional

@dataclass
class CareTeamParticipant:
    """
    CareTeamParticipant nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    role: Optional[CodeableConcept] = None  # Indicates specific responsibility of an individual within the care team, such as \"Primary care p...
    member: Optional[Reference] = None  # The specific person or organization who is participating/expected to participate in the care team.
    onBehalfOf: Optional[Reference] = None  # The organization of the practitioner.
    coverage: Optional[Any] = None  # When the member is generally available within this care team.


@dataclass
class CareTeam(FHIRResource):
    """
    The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care.
    """

    resourceType: str = "CareTeam"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this care team by the performer or other systems which remain co...
    status: Optional[str] = None  # Indicates the current state of the care team.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies what kind of team.  This is to support differentiation between multiple co-existing te...
    name: Optional[str] = None  # A label for human use intended to distinguish like teams.  E.g. the \"red\" vs. \"green\" trauma ...
    subject: Optional[Reference] = None  # Identifies the patient or group whose intended care is handled by the team.
    period: Optional[Period] = None  # Indicates when the team did (or is intended to) come into effect and end.
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies all people and organizations who are expected to be involved in the care team.
    reason: Optional[List[Any]] = field(default_factory=list)  # Describes why the care team exists.
    managingOrganization: Optional[List[Reference]] = field(default_factory=list)  # The organization responsible for the care team.
    telecom: Optional[List[ContactPoint]] = field(default_factory=list)  # A central contact detail for the care team (that applies to all members).
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the CareTeam.