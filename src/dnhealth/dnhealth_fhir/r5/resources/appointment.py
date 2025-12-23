# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Appointment resource.

A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class AppointmentParticipant:
    """
    AppointmentParticipant nested class.
    """

    status: Optional[str] = None  # Participation status of the actor.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Role of participant in the appointment.
    period: Optional[Period] = None  # Participation period of the actor.
    actor: Optional[Reference] = None  # The individual, device, location, or service participating in the appointment.
    required: Optional[bool] = None  # Whether this participant is required to be present at the meeting. If false, the participant is o...

@dataclass
class AppointmentRecurrenceTemplate:
    """
    AppointmentRecurrenceTemplate nested class.
    """

    recurrenceType: Optional[CodeableConcept] = None  # How often the appointment series should recur.
    monthInterval: Optional[int] = None  # Indicates that recurring appointments should occur every nth month.
    yearInterval: Optional[int] = None  # Appointment recurs every nth year.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    timezone: Optional[CodeableConcept] = None  # The timezone of the recurring appointment occurrences.
    lastOccurrenceDate: Optional[str] = None  # Recurring appointments will not occur after this date.
    occurrenceCount: Optional[int] = None  # How many appointments are planned in the recurrence.
    occurrenceDate: Optional[List[str]] = field(default_factory=list)  # The list of specific dates that will have appointments generated.
    weeklyTemplate: Optional[BackboneElement] = None  # Information about weekly recurring appointments.
    monday: Optional[bool] = None  # Indicates that recurring appointments should occur on Mondays.
    tuesday: Optional[bool] = None  # Indicates that recurring appointments should occur on Tuesdays.
    wednesday: Optional[bool] = None  # Indicates that recurring appointments should occur on Wednesdays.
    thursday: Optional[bool] = None  # Indicates that recurring appointments should occur on Thursdays.
    friday: Optional[bool] = None  # Indicates that recurring appointments should occur on Fridays.
    saturday: Optional[bool] = None  # Indicates that recurring appointments should occur on Saturdays.
    sunday: Optional[bool] = None  # Indicates that recurring appointments should occur on Sundays.
    weekInterval: Optional[int] = None  # The interval defines if the recurrence is every nth week. The default is every week, so it is exp...
    monthlyTemplate: Optional[BackboneElement] = None  # Information about monthly recurring appointments.
    dayOfMonth: Optional[int] = None  # Indicates that appointments in the series of recurring appointments should occur on a specific da...
    nthWeekOfMonth: Optional[Coding] = None  # Indicates which week within a month the appointments in the series of recurring appointments shou...
    dayOfWeek: Optional[Coding] = None  # Indicates which day of the week the recurring appointments should occur each nth week.
    yearlyTemplate: Optional[BackboneElement] = None  # Information about yearly recurring appointments.
    excludingDate: Optional[List[str]] = field(default_factory=list)  # Any dates, such as holidays, that should be excluded from the recurrence.
    excludingRecurrenceId: Optional[List[int]] = field(default_factory=list)  # Any dates, such as holidays, that should be excluded from the recurrence.

@dataclass
class AppointmentRecurrenceTemplateWeeklyTemplate:
    """
    AppointmentRecurrenceTemplateWeeklyTemplate nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    monday: Optional[bool] = None  # Indicates that recurring appointments should occur on Mondays.
    tuesday: Optional[bool] = None  # Indicates that recurring appointments should occur on Tuesdays.
    wednesday: Optional[bool] = None  # Indicates that recurring appointments should occur on Wednesdays.
    thursday: Optional[bool] = None  # Indicates that recurring appointments should occur on Thursdays.
    friday: Optional[bool] = None  # Indicates that recurring appointments should occur on Fridays.
    saturday: Optional[bool] = None  # Indicates that recurring appointments should occur on Saturdays.
    sunday: Optional[bool] = None  # Indicates that recurring appointments should occur on Sundays.
    weekInterval: Optional[int] = None  # The interval defines if the recurrence is every nth week. The default is every week, so it is exp...

@dataclass
class AppointmentRecurrenceTemplateMonthlyTemplate:
    """
    AppointmentRecurrenceTemplateMonthlyTemplate nested class.
    """

    monthInterval: Optional[int] = None  # Indicates that recurring appointments should occur every nth month.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    dayOfMonth: Optional[int] = None  # Indicates that appointments in the series of recurring appointments should occur on a specific da...
    nthWeekOfMonth: Optional[Coding] = None  # Indicates which week within a month the appointments in the series of recurring appointments shou...
    dayOfWeek: Optional[Coding] = None  # Indicates which day of the week the recurring appointments should occur each nth week.

@dataclass
class AppointmentRecurrenceTemplateYearlyTemplate:
    """
    AppointmentRecurrenceTemplateYearlyTemplate nested class.
    """

    yearInterval: Optional[int] = None  # Appointment recurs every nth year.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Appointment(FHIRResource):
    """
    A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).
    """

    status: Optional[str] = None  # The overall status of the Appointment. Each of the participants has their own participation statu...
    participant: List[BackboneElement] = field(default_factory=list)  # List of participants involved in the appointment.
    resourceType: str = "Appointment"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # This records identifiers associated with this appointment concern that are defined by business pr...
    cancellationReason: Optional[CodeableConcept] = None  # The coded reason for the appointment being cancelled. This is often used in reporting/billing/fut...
    class_: Optional[List[CodeableConcept]] = field(default_factory=list)  # Concepts representing classification of patient encounter such as ambulatory (outpatient), inpati...
    serviceCategory: Optional[List[CodeableConcept]] = field(default_factory=list)  # A broad categorization of the service that is to be performed during this appointment.
    serviceType: Optional[List[Any]] = field(default_factory=list)  # The specific service that is to be performed during this appointment.
    specialty: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specialty of a practitioner that would be required to perform the service requested in this a...
    appointmentType: Optional[CodeableConcept] = None  # The style of appointment or patient that has been booked in the slot (not service type).
    reason: Optional[List[Any]] = field(default_factory=list)  # The reason that this appointment is being scheduled. This is more clinical than administrative. T...
    priority: Optional[CodeableConcept] = None  # The priority of the appointment. Can be used to make informed decisions if needing to re-prioriti...
    description: Optional[str] = None  # The brief description of the appointment as would be shown on a subject line in a meeting request...
    replaces: Optional[List[Reference]] = field(default_factory=list)  # Appointment replaced by this Appointment in cases where there is a cancellation, the details of t...
    virtualService: Optional[List[Any]] = field(default_factory=list)  # Connection details of a virtual service (e.g. conference call).
    supportingInformation: Optional[List[Reference]] = field(default_factory=list)  # Additional information to support the appointment provided when making the appointment.
    previousAppointment: Optional[Reference] = None  # The previous appointment in a series of related appointments.
    originatingAppointment: Optional[Reference] = None  # The originating appointment in a recurring set of related appointments.
    start: Optional[str] = None  # Date/Time that the appointment is to take place.
    end: Optional[str] = None  # Date/Time that the appointment is to conclude.
    minutesDuration: Optional[int] = None  # Number of minutes that the appointment is to take. This can be less than the duration between the...
    requestedPeriod: Optional[List[Period]] = field(default_factory=list)  # A set of date ranges (potentially including times) that the appointment is preferred to be schedu...
    slot: Optional[List[Reference]] = field(default_factory=list)  # The slots from the participants' schedules that will be filled by the appointment.
    account: Optional[List[Reference]] = field(default_factory=list)  # The set of accounts that is expected to be used for billing the activities that result from this ...
    created: Optional[str] = None  # The date that this appointment was initially created. This could be different to the meta.lastMod...
    cancellationDate: Optional[str] = None  # The date/time describing when the appointment was cancelled.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional notes/comments about the appointment.
    patientInstruction: Optional[List[Any]] = field(default_factory=list)  # While Appointment.note contains information for internal use, Appointment.patientInstructions is ...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # The request this appointment is allocated to assess (e.g. incoming referral or procedure request).
    subject: Optional[Reference] = None  # The patient or group associated with the appointment, if they are to be present (usually) then th...
    recurrenceId: Optional[int] = None  # The sequence number that identifies a specific appointment in a recurring pattern.
    occurrenceChanged: Optional[bool] = None  # This appointment varies from the recurring pattern.
    recurrenceTemplate: Optional[List[BackboneElement]] = field(default_factory=list)  # The details of the recurrence pattern or template that is used to generate recurring appointments.