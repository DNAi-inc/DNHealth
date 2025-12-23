# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ChargeItem resource.

The resource ChargeItem describes the provision of healthcare provider products for a certain patient, therefore referring not only to the product, but containing in addition details of the provision, like date, time, amounts and participating organizations and persons. Main Usage of the ChargeItem is to enable the billing process and internal cost allocation.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Reference, Timing
from typing import Any, List, Optional

@dataclass
class ChargeItemPerformer:
    """
    ChargeItemPerformer nested class.
    """

    actor: Optional[Reference] = None  # The device, practitioner, etc. who performed or participated in the service.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Describes the type of performance or participation(e.g. primary surgeon, anesthesiologiest, etc.).


@dataclass
class ChargeItem(FHIRResource):
    """
    The resource ChargeItem describes the provision of healthcare provider products for a certain patient, therefore referring not only to the product, but containing in addition details of the provision, like date, time, amounts and participating organizations and persons. Main Usage of the ChargeItem is to enable the billing process and internal cost allocation.
    """

    status: Optional[str] = None  # The current state of the ChargeItem.
    code: Optional[CodeableConcept] = None  # A code that identifies the charge, like a billing code.
    subject: Optional[Reference] = None  # The individual or set of individuals the action is being or was performed on.
    resourceType: str = "ChargeItem"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers assigned to this event performer or other systems.
    definitionUri: Optional[List[str]] = field(default_factory=list)  # References the (external) source of pricing information, rules of application for the code this C...
    definitionCanonical: Optional[List[str]] = field(default_factory=list)  # References the source of pricing information, rules of application for the code this ChargeItem u...
    partOf: Optional[List[Reference]] = field(default_factory=list)  # ChargeItems can be grouped to larger ChargeItems covering the whole set.
    encounter: Optional[Reference] = None  # This ChargeItem has the details of how the associated Encounter should be billed or otherwise be ...
    occurrence: Optional[Any] = None  # Date/time(s) or duration when the charged service was applied.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what performed or participated in the charged service.
    performingOrganization: Optional[Reference] = None  # The organization performing the service.
    requestingOrganization: Optional[Reference] = None  # The organization requesting the service.
    costCenter: Optional[Reference] = None  # The financial cost center permits the tracking of charge attribution.
    quantity: Optional[Quantity] = None  # Quantity of which the charge item has been serviced.
    bodysite: Optional[List[CodeableConcept]] = field(default_factory=list)  # The anatomical location where the related service has been applied.
    unitPriceComponent: Optional[Any] = None  # The unit price of the chargable item.
    totalPriceComponent: Optional[Any] = None  # The total price for the chargable item, accounting for the quantity.
    overrideReason: Optional[CodeableConcept] = None  # If the list price or the rule-based factor associated with the code is overridden, this attribute...
    enterer: Optional[Reference] = None  # The device, practitioner, etc. who entered the charge item.
    enteredDate: Optional[str] = None  # Date the charge item was entered.
    reason: Optional[List[CodeableConcept]] = field(default_factory=list)  # Describes why the event occurred in coded or textual form.
    service: Optional[List[Any]] = field(default_factory=list)  # Indicated the rendered service that caused this charge.
    product: Optional[List[Any]] = field(default_factory=list)  # Identifies the device, food, drug or other product being charged either by type code or reference...
    account: Optional[List[Reference]] = field(default_factory=list)  # Account into which this ChargeItems belongs.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments made about the event by the performer, subject or other participants.
    supportingInformation: Optional[List[Reference]] = field(default_factory=list)  # Further information supporting this charge.