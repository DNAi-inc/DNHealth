# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 EpisodeOfCare resource.

An association between a patient and an organization / healthcare provider(s) during which time encounters may occur. The managing organization assumes a level of responsibility for the patient during this time.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class EpisodeOfCareStatusHistory:
    """
    EpisodeOfCareStatusHistory nested class.
    """

    status: Optional[str] = None  # planned | waitlist | active | onhold | finished | cancelled.
    period: Optional[Period] = None  # The period during this EpisodeOfCare that the specific status applied.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class EpisodeOfCareReason:
    """
    EpisodeOfCareReason nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    use: Optional[CodeableConcept] = None  # What the reason value should be used as e.g. Chief Complaint, Health Concern, Health Maintenance ...
    value: Optional[List[Any]] = field(default_factory=list)  # The medical reason that is expected to be addressed during the episode of care, expressed as a te...

@dataclass
class EpisodeOfCareDiagnosis:
    """
    EpisodeOfCareDiagnosis nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    condition: Optional[List[Any]] = field(default_factory=list)  # The medical condition that was addressed during the episode of care, expressed as a text, code or...
    use: Optional[CodeableConcept] = None  # Role that this diagnosis has within the episode of care (e.g. admission, billing, discharge …).


@dataclass
class EpisodeOfCare(FHIRResource):
    """
    An association between a patient and an organization / healthcare provider(s) during which time encounters may occur. The managing organization assumes a level of responsibility for the patient during this time.
    """

    status: Optional[str] = None  # planned | waitlist | active | onhold | finished | cancelled.
    patient: Optional[Reference] = None  # The patient who is the focus of this episode of care.
    resourceType: str = "EpisodeOfCare"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The EpisodeOfCare may be known by different identifiers for different contexts of use, such as wh...
    statusHistory: Optional[List[BackboneElement]] = field(default_factory=list)  # The history of statuses that the EpisodeOfCare has been through (without requiring processing the...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # A classification of the type of episode of care; e.g. specialist referral, disease management, ty...
    reason: Optional[List[BackboneElement]] = field(default_factory=list)  # The list of medical reasons that are expected to be addressed during the episode of care.
    diagnosis: Optional[List[BackboneElement]] = field(default_factory=list)  # The list of medical conditions that were addressed during the episode of care.
    managingOrganization: Optional[Reference] = None  # The organization that has assumed the specific responsibilities for care coordination, care deliv...
    period: Optional[Period] = None  # The interval during which the managing organization assumes the defined responsibility.
    referralRequest: Optional[List[Reference]] = field(default_factory=list)  # Referral Request(s) that are fulfilled by this EpisodeOfCare, incoming referrals.
    careManager: Optional[Reference] = None  # The practitioner that is the care manager/care coordinator for this patient.
    careTeam: Optional[List[Reference]] = field(default_factory=list)  # The list of practitioners that may be facilitating this episode of care for specific purposes.
    account: Optional[List[Reference]] = field(default_factory=list)  # The set of accounts that may be used for billing for this EpisodeOfCare.