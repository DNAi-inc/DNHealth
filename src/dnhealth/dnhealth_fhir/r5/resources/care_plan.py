# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 CarePlan resource.

Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community for a period of time, possibly limited to care for a specific condition or set of conditions.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class CarePlanActivity:
    """
    CarePlanActivity nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    performedActivity: Optional[List[Any]] = field(default_factory=list)  # Identifies the activity that was performed. For example, an activity could be patient education, ...
    progress: Optional[List[Annotation]] = field(default_factory=list)  # Notes about the adherence/status/progress of the activity.
    plannedActivityReference: Optional[Reference] = None  # The details of the proposed activity represented in a specific resource.


@dataclass
class CarePlan(FHIRResource):
    """
    Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community for a period of time, possibly limited to care for a specific condition or set of conditions.
    """

    status: Optional[str] = None  # Indicates whether the plan is currently being acted upon, represents future intentions or is now ...
    intent: Optional[str] = None  # Indicates the level of authority/intentionality associated with the care plan and where the care ...
    subject: Optional[Reference] = None  # Identifies the patient or group whose intended care is described by the plan.
    resourceType: str = "CarePlan"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this care plan by the performer or other systems which remain co...
    instantiatesCanonical: Optional[List[str]] = field(default_factory=list)  # The URL pointing to a FHIR-defined protocol, guideline, questionnaire or other definition that is...
    instantiatesUri: Optional[List[str]] = field(default_factory=list)  # The URL pointing to an externally maintained protocol, guideline, questionnaire or other definiti...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A higher-level request resource (i.e. a plan, proposal or order) that is fulfilled in whole or in...
    replaces: Optional[List[Reference]] = field(default_factory=list)  # Completed or terminated care plan whose function is taken by this new care plan.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger care plan of which this particular care plan is a component or step.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Identifies what \"kind\" of plan this is to support differentiation between multiple co-existing ...
    title: Optional[str] = None  # Human-friendly name for the care plan.
    description: Optional[str] = None  # A description of the scope and nature of the plan.
    encounter: Optional[Reference] = None  # The Encounter during which this CarePlan was created or to which the creation of this record is t...
    period: Optional[Period] = None  # Indicates when the plan did (or is intended to) come into effect and end.
    created: Optional[str] = None  # Represents when this particular CarePlan record was created in the system, which is often a syste...
    custodian: Optional[Reference] = None  # When populated, the custodian is responsible for the care plan. The care plan is attributed to th...
    contributor: Optional[List[Reference]] = field(default_factory=list)  # Identifies the individual(s), organization or device who provided the contents of the care plan.
    careTeam: Optional[List[Reference]] = field(default_factory=list)  # Identifies all people and organizations who are expected to be involved in the care envisioned by...
    addresses: Optional[List[Any]] = field(default_factory=list)  # Identifies the conditions/problems/concerns/diagnoses/etc. whose management and/or mitigation are...
    supportingInfo: Optional[List[Reference]] = field(default_factory=list)  # Identifies portions of the patient's record that specifically influenced the formation of the pla...
    goal: Optional[List[Reference]] = field(default_factory=list)  # Describes the intended objective(s) of carrying out the care plan.
    activity: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies an action that has occurred or is a planned action to occur as part of the plan. For e...
    note: Optional[List[Annotation]] = field(default_factory=list)  # General notes about the care plan not covered elsewhere.