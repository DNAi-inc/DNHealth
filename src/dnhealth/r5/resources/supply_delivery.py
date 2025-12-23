# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SupplyDelivery resource.

Record of delivery of what is supplied.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Reference, Timing
from typing import Any, List, Optional

@dataclass
class SupplyDeliverySuppliedItem:
    """
    SupplyDeliverySuppliedItem nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    quantity: Optional[Quantity] = None  # The amount of the item that has been supplied.  Unit of measure may be included.
    item: Optional[Any] = None  # Identifies the medication, substance, device or biologically derived product being supplied. This...


@dataclass
class SupplyDelivery(FHIRResource):
    """
    Record of delivery of what is supplied.
    """

    resourceType: str = "SupplyDelivery"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for the supply delivery event that is used to identify it across multiple disparate sy...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan, proposal or order that is fulfilled in whole or in part by this event.
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular event is a component or step.
    status: Optional[str] = None  # A code specifying the state of the dispense event.
    patient: Optional[Reference] = None  # A link to a resource representing the person whom the delivered item is for.
    type: Optional[CodeableConcept] = None  # Indicates the type of supply being provided.  Examples include: Medication, Device, Biologically ...
    suppliedItem: Optional[List[BackboneElement]] = field(default_factory=list)  # The item that is being delivered or has been supplied.
    occurrence: Optional[Any] = None  # The date or time(s) the activity occurred.
    supplier: Optional[Reference] = None  # The individual or organization responsible for supplying the delivery.
    destination: Optional[Reference] = None  # Identification of the facility/location where the delivery was shipped to.
    receiver: Optional[List[Reference]] = field(default_factory=list)  # Identifies the individual or organization that received the delivery.
