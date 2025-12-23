# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Encounter resource.

An interaction between healthcare provider(s), and/or patient(s) for the purpose of providing healthcare service(s) or assessing the health status of patient(s).
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Duration, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class EncounterParticipant:
    """
    EncounterParticipant nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Role of participant in encounter.
    period: Optional[Period] = None  # The period of time that the specified participant participated in the encounter. These can overla...
    actor: Optional[Reference] = None  # Person involved in the encounter, the patient/group is also included here to indicate that the pa...

@dataclass
class EncounterReason:
    """
    EncounterReason nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    use: Optional[List[CodeableConcept]] = field(default_factory=list)  # What the reason value should be used as e.g. Chief Complaint, Health Concern, Health Maintenance ...
    value: Optional[List[Any]] = field(default_factory=list)  # Reason the encounter takes place, expressed as a code or a reference to another resource. For adm...

@dataclass
class EncounterDiagnosis:
    """
    EncounterDiagnosis nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    condition: Optional[List[Any]] = field(default_factory=list)  # The coded diagnosis or a reference to a Condition (with other resources referenced in the evidenc...
    use: Optional[List[CodeableConcept]] = field(default_factory=list)  # Role that this diagnosis has within the encounter (e.g. admission, billing, discharge …).

@dataclass
class EncounterAdmission:
    """
    EncounterAdmission nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    preAdmissionIdentifier: Optional[Identifier] = None  # Pre-admission identifier.
    origin: Optional[Reference] = None  # The location/organization from which the patient came before admission.
    admitSource: Optional[CodeableConcept] = None  # From where patient was admitted (physician referral, transfer).
    reAdmission: Optional[CodeableConcept] = None  # Indicates that this encounter is directly related to a prior admission, often because the conditi...
    destination: Optional[Reference] = None  # Location/organization to which the patient is discharged.
    dischargeDisposition: Optional[CodeableConcept] = None  # Category or kind of location after discharge.

@dataclass
class EncounterLocation:
    """
    EncounterLocation nested class.
    """

    location: Optional[Reference] = None  # The location where the encounter takes place.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    status: Optional[str] = None  # The status of the participants' presence at the specified location during the period specified. I...
    form: Optional[CodeableConcept] = None  # This will be used to specify the required levels (bed/ward/room/etc.) desired to be recorded to s...
    period: Optional[Period] = None  # Time period during which the patient was present at the location.


@dataclass
class Encounter(FHIRResource):
    """
    An interaction between healthcare provider(s), and/or patient(s) for the purpose of providing healthcare service(s) or assessing the health status of patient(s).
    """

    status: Optional[str] = None  # The current state of the encounter (not the state of the patient within the encounter - that is s...
    resourceType: str = "Encounter"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier(s) by which this encounter is known.
    class_: Optional[List[CodeableConcept]] = field(default_factory=list)  # Concepts representing classification of patient encounter such as ambulatory (outpatient), inpati...
    priority: Optional[CodeableConcept] = None  # Indicates the urgency of the encounter.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specific type of encounter (e.g. e-mail consultation, surgical day-care, skilled nursing, rehabil...
    serviceType: Optional[List[Any]] = field(default_factory=list)  # Broad categorization of the service that is to be provided (e.g. cardiology).
    subject: Optional[Reference] = None  # The patient or group related to this encounter. In some use-cases the patient MAY not be present,...
    subjectStatus: Optional[CodeableConcept] = None  # The subjectStatus value can be used to track the patient's status within the encounter. It detail...
    episodeOfCare: Optional[List[Reference]] = field(default_factory=list)  # Where a specific encounter should be classified as a part of a specific episode(s) of care this f...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # The request this encounter satisfies (e.g. incoming referral or procedure request).
    careTeam: Optional[List[Reference]] = field(default_factory=list)  # The group(s) of individuals, organizations that are allocated to participate in this encounter. T...
    partOf: Optional[Reference] = None  # Another Encounter of which this encounter is a part of (administratively or in time).
    serviceProvider: Optional[Reference] = None  # The organization that is primarily responsible for this Encounter's services. This MAY be the sam...
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # The list of people responsible for providing the service.
    appointment: Optional[List[Reference]] = field(default_factory=list)  # The appointment that scheduled this encounter.
    virtualService: Optional[List[Any]] = field(default_factory=list)  # Connection details of a virtual service (e.g. conference call).
    actualPeriod: Optional[Period] = None  # The actual start and end time of the encounter.
    plannedStartDate: Optional[str] = None  # The planned start date/time (or admission date) of the encounter.
    plannedEndDate: Optional[str] = None  # The planned end date/time (or discharge date) of the encounter.
    length: Optional[Duration] = None  # Actual quantity of time the encounter lasted. This excludes the time during leaves of absence.


    reason: Optional[List[BackboneElement]] = field(default_factory=list)  # The list of medical reasons that are expected to be addressed during the episode of care.
    diagnosis: Optional[List[BackboneElement]] = field(default_factory=list)  # The list of diagnosis relevant to this encounter.
    account: Optional[List[Reference]] = field(default_factory=list)  # The set of accounts that may be used for billing for this Encounter.
    dietPreference: Optional[List[CodeableConcept]] = field(default_factory=list)  # Diet preferences reported by the patient.
    specialArrangement: Optional[List[CodeableConcept]] = field(default_factory=list)  # Any special requests that have been made for this encounter, such as the provision of specific eq...
    specialCourtesy: Optional[List[CodeableConcept]] = field(default_factory=list)  # Special courtesies that may be provided to the patient during the encounter (VIP, board member, p...
    admission: Optional[BackboneElement] = None  # Details about the stay during which a healthcare service is provided.
    location: Optional[List[BackboneElement]] = field(default_factory=list)  # List of locations where  the patient has been during this encounter.