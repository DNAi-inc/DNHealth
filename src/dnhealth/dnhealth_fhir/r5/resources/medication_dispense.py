# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MedicationDispense resource.

Indicates that a medication product is to be or has been dispensed for a named person/patient.  This includes a description of the medication product (supply) provided and the instructions for administering the medication.  The medication dispense is the result of a pharmacy system responding to a medication order.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Dosage, Extension, Identifier, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class MedicationDispensePerformer:
    """
    MedicationDispensePerformer nested class.
    """

    actor: Optional[Reference] = None  # The device, practitioner, etc. who performed the action.  It should be assumed that the actor is ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Distinguishes the type of performer in the dispense.  For example, date enterer, packager, final ...

@dataclass
class MedicationDispenseSubstitution:
    """
    MedicationDispenseSubstitution nested class.
    """

    wasSubstituted: Optional[bool] = None  # True if the dispenser dispensed a different drug or product from what was prescribed.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # A code signifying whether a different drug was dispensed from what was prescribed.
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # Indicates the reason for the substitution (or lack of substitution) from what was prescribed.
    responsibleParty: Optional[Reference] = None  # The person or organization that has primary responsibility for the substitution.


@dataclass
class MedicationDispense(FHIRResource):
    """
    Indicates that a medication product is to be or has been dispensed for a named person/patient.  This includes a description of the medication product (supply) provided and the instructions for administering the medication.  The medication dispense is the result of a pharmacy system responding to a medication order.
    """

    status: Optional[str] = None  # A code specifying the state of the set of dispense events.
    medication: Optional[Any] = None  # Identifies the medication supplied. This is either a link to a resource representing the details ...
    subject: Optional[Reference] = None  # A link to a resource representing the person or the group to whom the medication will be given.
    resourceType: str = "MedicationDispense"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers associated with this Medication Dispense that are defined by business processes and/o...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan that is fulfilled in whole or in part by this MedicationDispense.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # The procedure or medication administration that triggered the dispense.
    notPerformedReason: Optional[Any] = None  # Indicates the reason why a dispense was not performed.
    statusChanged: Optional[str] = None  # The date (and maybe time) when the status of the dispense record changed.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Indicates the type of medication dispense (for example, drug classification like ATC, where meds ...
    encounter: Optional[Reference] = None  # The encounter that establishes the context for this event.
    supportingInformation: Optional[List[Reference]] = field(default_factory=list)  # Additional information that supports the medication being dispensed.  For example, there may be r...
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what performed the event.
    location: Optional[Reference] = None  # The principal physical location where the dispense was performed.
    authorizingPrescription: Optional[List[Reference]] = field(default_factory=list)  # Indicates the medication order that is being dispensed against.
    type: Optional[CodeableConcept] = None  # Indicates the type of dispensing event that is performed. For example, Trial Fill, Completion of ...
    quantity: Optional[Quantity] = None  # The amount of medication that has been dispensed. Includes unit of measure.
    daysSupply: Optional[Quantity] = None  # The amount of medication expressed as a timing amount.
    recorded: Optional[str] = None  # The date (and maybe time) when the dispense activity started if whenPrepared or whenHandedOver is...
    whenPrepared: Optional[str] = None  # The time when the dispensed product was packaged and reviewed.
    whenHandedOver: Optional[str] = None  # The time the dispensed product was provided to the patient or their representative.
    destination: Optional[Reference] = None  # Identification of the facility/location where the medication was/will be shipped to, as part of t...
    receiver: Optional[List[Reference]] = field(default_factory=list)  # Identifies the person who picked up the medication or the location of where the medication was de...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Extra information about the dispense that could not be conveyed in the other attributes.
    renderedDosageInstruction: Optional[str] = None  # The full representation of the dose of the medication included in all dosage instructions.  To be...
    dosageInstruction: Optional[List[Dosage]] = field(default_factory=list)  # Indicates how the medication is to be used by the patient.
    substitution: Optional[BackboneElement] = None  # Indicates whether or not substitution was made as part of the dispense.  In some cases, substitut...
    eventHistory: Optional[List[Reference]] = field(default_factory=list)  # A summary of the events of interest that have occurred, such as when the dispense was verified.