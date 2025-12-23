# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 AdverseEvent resource.

An event (i.e. any change to current patient status) that may be related to unintended effects on a patient or research participant. The unintended effects may require additional monitoring, treatment, hospitalization, or may result in death. The AdverseEvent resource also extends to potential or avoided events that could have had such effects. There are two major domains where the AdverseEvent resource is expected to be used. One is in clinical care reported adverse events and the other is in reporting adverse events in clinical  research trial management.  Adverse events can be reported by healthcare providers, patients, caregivers or by medical products manufacturers.  Given the differences between these two concepts, we recommend consulting the domain specific implementation guides when implementing the AdverseEvent Resource. The implementation guides include specific extensions, value sets and constraints.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference, Timing
from typing import Any, List, Optional

@dataclass
class AdverseEventParticipant:
    """
    AdverseEventParticipant nested class.
    """

    actor: Optional[Reference] = None  # Indicates who or what participated in the event.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the actor in the adverse event, such as contributor or i...

@dataclass
class AdverseEventSuspectEntity:
    """
    AdverseEventSuspectEntity nested class.
    """

    instance: Optional[Any] = None  # Identifies the actual instance of what caused the adverse event.  May be a substance, medication,...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    causality: Optional[BackboneElement] = None  # Information on the possible cause of the event.
    assessmentMethod: Optional[CodeableConcept] = None  # The method of evaluating the relatedness of the suspected entity to the event.
    entityRelatedness: Optional[CodeableConcept] = None  # The result of the assessment regarding the relatedness of the suspected entity to the event.
    author: Optional[Reference] = None  # The author of the information on the possible cause of the event.

@dataclass
class AdverseEventSuspectEntityCausality:
    """
    AdverseEventSuspectEntityCausality nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    assessmentMethod: Optional[CodeableConcept] = None  # The method of evaluating the relatedness of the suspected entity to the event.
    entityRelatedness: Optional[CodeableConcept] = None  # The result of the assessment regarding the relatedness of the suspected entity to the event.
    author: Optional[Reference] = None  # The author of the information on the possible cause of the event.

@dataclass
class AdverseEventContributingFactor:
    """
    AdverseEventContributingFactor nested class.
    """

    item: Optional[Any] = None  # The item that is suspected to have increased the probability or severity of the adverse event.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class AdverseEventPreventiveAction:
    """
    AdverseEventPreventiveAction nested class.
    """

    item: Optional[Any] = None  # The action that contributed to avoiding the adverse event.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class AdverseEventMitigatingAction:
    """
    AdverseEventMitigatingAction nested class.
    """

    item: Optional[Any] = None  # The ameliorating action taken after the adverse event occured in order to reduce the extent of harm.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class AdverseEventSupportingInfo:
    """
    AdverseEventSupportingInfo nested class.
    """

    item: Optional[Any] = None  # Relevant past history for the subject. In a clinical care context, an example being a patient had...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class AdverseEvent(FHIRResource):
    """
    An event (i.e. any change to current patient status) that may be related to unintended effects on a patient or research participant. The unintended effects may require additional monitoring, treatment, hospitalization, or may result in death. The AdverseEvent resource also extends to potential or avoided events that could have had such effects. There are two major domains where the AdverseEvent resource is expected to be used. One is in clinical care reported adverse events and the other is in reporting adverse events in clinical  research trial management.  Adverse events can be reported by healthcare providers, patients, caregivers or by medical products manufacturers.  Given the differences between these two concepts, we recommend consulting the domain specific implementation guides when implementing the AdverseEvent Resource. The implementation guides include specific extensions, value sets and constraints.
    """

    status: Optional[str] = None  # The current state of the adverse event or potential adverse event.
    actuality: Optional[str] = None  # Whether the event actually happened or was a near miss. Note that this is independent of whether ...
    subject: Optional[Reference] = None  # This subject or group impacted by the event.
    resourceType: str = "AdverseEvent"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this adverse event by the performer or other systems which remai...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # The overall type of event, intended for search and filtering purposes.
    code: Optional[CodeableConcept] = None  # Specific event that occurred or that was averted, such as patient fall, wrong organ removed, or w...
    encounter: Optional[Reference] = None  # The Encounter associated with the start of the AdverseEvent.
    occurrence: Optional[Any] = None  # The date (and perhaps time) when the adverse event occurred.
    detected: Optional[str] = None  # Estimated or actual date the AdverseEvent began, in the opinion of the reporter.
    recordedDate: Optional[str] = None  # The date on which the existence of the AdverseEvent was first recorded.
    resultingEffect: Optional[List[Reference]] = field(default_factory=list)  # Information about the condition that occurred as a result of the adverse event, such as hives due...
    location: Optional[Reference] = None  # The information about where the adverse event occurred.
    seriousness: Optional[CodeableConcept] = None  # Assessment whether this event, or averted event, was of clinical importance.
    outcome: Optional[List[CodeableConcept]] = field(default_factory=list)  # Describes the type of outcome from the adverse event, such as resolved, recovering, ongoing, reso...
    recorder: Optional[Reference] = None  # Information on who recorded the adverse event.  May be the patient or a practitioner.
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what participated in the adverse event and how they were involved.
    study: Optional[List[Reference]] = field(default_factory=list)  # The research study that the subject is enrolled in.
    expectedInResearchStudy: Optional[bool] = None  # Considered likely or probable or anticipated in the research study.  Whether the reported event m...
    suspectEntity: Optional[List[BackboneElement]] = field(default_factory=list)  # Describes the entity that is suspected to have caused the adverse event.
    contributingFactor: Optional[List[BackboneElement]] = field(default_factory=list)  # The contributing factors suspected to have increased the probability or severity of the adverse e...
    preventiveAction: Optional[List[BackboneElement]] = field(default_factory=list)  # Preventive actions that contributed to avoiding the adverse event.
    mitigatingAction: Optional[List[BackboneElement]] = field(default_factory=list)  # The ameliorating action taken after the adverse event occured in order to reduce the extent of harm.
    supportingInfo: Optional[List[BackboneElement]] = field(default_factory=list)  # Supporting information relevant to the event.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the adverse event by the performer, subject or other participants.