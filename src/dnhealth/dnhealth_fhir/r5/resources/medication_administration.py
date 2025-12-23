# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MedicationAdministration resource.

Describes the event of a patient consuming or otherwise being administered a medication.  This may be as simple as swallowing a tablet or it may be a long running infusion. Related resources tie this event to the authorizing prescription, and the specific encounter between patient and health care practitioner. This event can also be used to record waste using a status of not-done and the appropriate statusReason.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Ratio, Reference, Timing
from typing import Any, List, Optional

@dataclass
class MedicationAdministrationPerformer:
    """
    MedicationAdministrationPerformer nested class.
    """

    actor: Optional[Any] = None  # Indicates who or what performed the medication administration.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of involvement of the performer in the medication administration.

@dataclass
class MedicationAdministrationDosage:
    """
    MedicationAdministrationDosage nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    text: Optional[str] = None  # Free text dosage can be used for cases where the dosage administered is too complex to code. When...
    site: Optional[CodeableConcept] = None  # A coded specification of the anatomic site where the medication first entered the body.  For exam...
    route: Optional[CodeableConcept] = None  # A code specifying the route or physiological path of administration of a therapeutic agent into o...
    method: Optional[CodeableConcept] = None  # A coded value indicating the method by which the medication is intended to be or was introduced i...
    dose: Optional[Quantity] = None  # The amount of the medication given at one administration event.   Use this value when the adminis...
    rate: Optional[Any] = None  # Identifies the speed with which the medication was or will be introduced into the patient.  Typic...


@dataclass
class MedicationAdministration(FHIRResource):
    """
    Describes the event of a patient consuming or otherwise being administered a medication.  This may be as simple as swallowing a tablet or it may be a long running infusion. Related resources tie this event to the authorizing prescription, and the specific encounter between patient and health care practitioner. This event can also be used to record waste using a status of not-done and the appropriate statusReason.
    """

    status: Optional[str] = None  # Will generally be set to show that the administration has been completed.  For some long running ...
    medication: Optional[Any] = None  # Identifies the medication that was administered. This is either a link to a resource representing...
    subject: Optional[Reference] = None  # The person or animal or group receiving the medication.
    occurence: Optional[Any] = None  # A specific date/time or interval of time during which the administration took place (or did not t...
    resourceType: str = "MedicationAdministration"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers associated with this Medication Administration that are defined by business processes...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan that is fulfilled in whole or in part by this MedicationAdministration.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular event is a component or step.
    statusReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # A code indicating why the administration was not performed.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # The type of medication administration (for example, drug classification like ATC, where meds woul...
    encounter: Optional[Reference] = None  # The visit, admission, or other contact between patient and health care provider during which the ...
    supportingInformation: Optional[List[Reference]] = field(default_factory=list)  # Additional information (for example, patient height and weight) that supports the administration ...
    recorded: Optional[str] = None  # The date the occurrence of the  MedicationAdministration was first captured in the record - poten...
    isSubPotent: Optional[bool] = None  # An indication that the full dose was not administered.
    subPotentReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # The reason or reasons why the full dose was not administered.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # The performer of the medication treatment.  For devices this is the device that performed the adm...
    reason: Optional[List[Any]] = field(default_factory=list)  # A code, Condition or observation that supports why the medication was administered.
    request: Optional[Reference] = None  # The original request, instruction or authority to perform the administration.
    device: Optional[List[Any]] = field(default_factory=list)  # The device that is to be used for the administration of the medication (for example, PCA Pump).
    note: Optional[List[Annotation]] = field(default_factory=list)  # Extra information about the medication administration that is not conveyed by the other attributes.
    dosage: Optional[BackboneElement] = None  # Describes the medication dosage information details e.g. dose, rate, site, route, etc.
    eventHistory: Optional[List[Reference]] = field(default_factory=list)  # A summary of the events of interest that have occurred, such as when the administration was verif...