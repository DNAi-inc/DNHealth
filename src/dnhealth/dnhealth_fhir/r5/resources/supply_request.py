# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SupplyRequest resource.

A record of a non-patient specific request for a medication, substance, device, certain types of biologically derived product, and nutrition product used in the healthcare setting.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Range, Reference, Timing
from typing import Any, List, Optional

@dataclass
class SupplyRequestParameter:
    """
    SupplyRequestParameter nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[CodeableConcept] = None  # A code or string that identifies the device detail being asserted.
    value: Optional[Any] = None  # The value of the device detail.


@dataclass
class SupplyRequest(FHIRResource):
    """
    A record of a non-patient specific request for a medication, substance, device, certain types of biologically derived product, and nutrition product used in the healthcare setting.
    """

    item: Optional[Any] = None  # The item that is requested to be supplied. This is either a link to a resource representing the d...
    quantity: Optional[Quantity] = None  # The amount that is being ordered of the indicated item.
    resourceType: str = "SupplyRequest"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this SupplyRequest by the author and/or other systems. These ide...
    status: Optional[str] = None  # Status of the supply request.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Plan/proposal/order fulfilled by this request.
    category: Optional[CodeableConcept] = None  # Category of supply, e.g.  central, non-stock, etc. This is used to support work flows associated ...
    priority: Optional[str] = None  # Indicates how quickly this SupplyRequest should be addressed with respect to other requests.
    deliverFor: Optional[Reference] = None  # The patient to whom the supply will be given or for whom they will be used.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Specific parameters for the ordered item.  For example, the size of the indicated item.
    occurrence: Optional[Any] = None  # When the request should be fulfilled.
    authoredOn: Optional[str] = None  # When the request was made.
    requester: Optional[Reference] = None  # The device, practitioner, etc. who initiated the request.
    supplier: Optional[List[Reference]] = field(default_factory=list)  # Who is intended to fulfill the request.
    reason: Optional[List[Any]] = field(default_factory=list)  # The reason why the supply item was requested.
    deliverFrom: Optional[Reference] = None  # Where the supply is expected to come from.
    deliverTo: Optional[Reference] = None  # Where the supply is destined to go.