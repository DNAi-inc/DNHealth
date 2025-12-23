# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 EncounterHistory resource.

A record of significant events/milestones key data throughout the history of an Encounter
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Duration, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class EncounterHistoryLocation:
    """
    EncounterHistoryLocation nested class.
    """

    location: Optional[Reference] = None  # The location where the encounter takes place.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    form: Optional[CodeableConcept] = None  # This will be used to specify the required levels (bed/ward/room/etc.) desired to be recorded to s...


@dataclass
class EncounterHistory(FHIRResource):
    """
    A record of significant events/milestones key data throughout the history of an Encounter
    """

    status: Optional[str] = None  # planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-...
    class: Optional[CodeableConcept] = None  # Concepts representing classification of patient encounter such as ambulatory (outpatient), inpati...
    resourceType: str = "EncounterHistory"
    encounter: Optional[Reference] = None  # The Encounter associated with this set of historic values.
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier(s) by which this encounter is known.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specific type of encounter (e.g. e-mail consultation, surgical day-care, skilled nursing, rehabil...
    serviceType: Optional[List[Any]] = field(default_factory=list)  # Broad categorization of the service that is to be provided (e.g. cardiology).
    subject: Optional[Reference] = None  # The patient or group related to this encounter. In some use-cases the patient MAY not be present,...
    subjectStatus: Optional[CodeableConcept] = None  # The subjectStatus value can be used to track the patient's status within the encounter. It detail...
    actualPeriod: Optional[Period] = None  # The start and end time associated with this set of values associated with the encounter, may be d...
    plannedStartDate: Optional[str] = None  # The planned start date/time (or admission date) of the encounter.
    plannedEndDate: Optional[str] = None  # The planned end date/time (or discharge date) of the encounter.
    length: Optional[Duration] = None  # Actual quantity of time the encounter lasted. This excludes the time during leaves of absence.W...
    location: Optional[List[BackboneElement]] = field(default_factory=list)  # The location of the patient at this point in the encounter, the multiple cardinality permits de-n...
