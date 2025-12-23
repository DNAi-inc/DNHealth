# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DeviceRequest resource.

Represents a request a device to be provided to a specific patient. The device may be an implantable device to be subsequently implanted, or an external assistive device, such as a walker, to be delivered and subsequently be used.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Range, Reference, Timing
from typing import Any, List, Optional

@dataclass
class DeviceRequestParameter:
    """
    DeviceRequestParameter nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[CodeableConcept] = None  # A code or string that identifies the device detail being asserted.
    value: Optional[Any] = None  # The value of the device detail.


@dataclass
class DeviceRequest(FHIRResource):
    """
    Represents a request a device to be provided to a specific patient. The device may be an implantable device to be subsequently implanted, or an external assistive device, such as a walker, to be delivered and subsequently be used.
    """

    intent: Optional[str] = None  # Whether the request is a proposal, plan, an original order or a reflex order.
    code: Optional[Any] = None  # The details of the device to be used.
    subject: Optional[Reference] = None  # The patient who will use the device.
    resourceType: str = "DeviceRequest"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers assigned to this order by the orderer or by the receiver.
    instantiatesCanonical: Optional[List[str]] = field(default_factory=list)  # The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhe...
    instantiatesUri: Optional[List[str]] = field(default_factory=list)  # The URL pointing to an externally maintained protocol, guideline, orderset or other definition th...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Plan/proposal/order fulfilled by this request.
    replaces: Optional[List[Reference]] = field(default_factory=list)  # The request takes the place of the referenced completed or terminated request(s).
    groupIdentifier: Optional[Identifier] = None  # A shared identifier common to multiple independent Request instances that were activated/authoriz...
    status: Optional[str] = None  # The status of the request.
    priority: Optional[str] = None  # Indicates how quickly the request should be addressed with respect to other requests.
    doNotPerform: Optional[bool] = None  # If true, indicates that the provider is asking for the patient to either stop using or to not sta...
    quantity: Optional[int] = None  # The number of devices to be provided.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Specific parameters for the ordered item.  For example, the prism value for lenses.
    encounter: Optional[Reference] = None  # An encounter that provides additional context in which this request is made.
    occurrence: Optional[Any] = None  # The timing schedule for the use of the device. The Schedule data type allows many different expre...
    authoredOn: Optional[str] = None  # When the request transitioned to being actionable.
    requester: Optional[Reference] = None  # The individual or entity who initiated the request and has responsibility for its activation.
    performer: Optional[Any] = None  # The desired individual or entity to provide the device to the subject of the request (e.g., patie...
    reason: Optional[List[Any]] = field(default_factory=list)  # Reason or justification for the use of this device.
    asNeeded: Optional[bool] = None  # This status is to indicate whether the request is a PRN or may be given as needed.
    asNeededFor: Optional[CodeableConcept] = None  # The reason for using the device.
    insurance: Optional[List[Reference]] = field(default_factory=list)  # Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be re...
    supportingInfo: Optional[List[Reference]] = field(default_factory=list)  # Additional clinical information about the patient that may influence the request fulfilment.  For...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Details about this request that were not represented at all or sufficiently in one of the attribu...
    relevantHistory: Optional[List[Reference]] = field(default_factory=list)  # Key events in the history of the request.