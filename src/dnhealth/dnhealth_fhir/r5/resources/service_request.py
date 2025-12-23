# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ServiceRequest resource.

A record of a request for service such as diagnostic investigations, treatments, or operations to be performed.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Range, Ratio, Reference, Timing
from typing import Any, List, Optional

@dataclass
class ServiceRequestOrderDetail:
    """
    ServiceRequestOrderDetail nested class.
    """

    parameter: List[BackboneElement] = field(default_factory=list)  # The parameter details for the service being requested.
    code: Optional[CodeableConcept] = None  # A value representing the additional detail or instructions for the order (e.g., catheter insertio...
    value: Optional[Any] = None  # Indicates a value for the order detail.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    parameterFocus: Optional[Any] = None  # Indicates the context of the order details by reference.

@dataclass
class ServiceRequestOrderDetailParameter:
    """
    ServiceRequestOrderDetailParameter nested class.
    """

    code: Optional[CodeableConcept] = None  # A value representing the additional detail or instructions for the order (e.g., catheter insertio...
    value: Optional[Any] = None  # Indicates a value for the order detail.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ServiceRequestPatientInstruction:
    """
    ServiceRequestPatientInstruction nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    instruction: Optional[Any] = None  # Instructions in terms that are understood by the patient or consumer.


@dataclass
class ServiceRequest(FHIRResource):
    """
    A record of a request for service such as diagnostic investigations, treatments, or operations to be performed.
    """

    status: Optional[str] = None  # The status of the order.
    intent: Optional[str] = None  # Whether the request is a proposal, plan, an original order or a reflex order.
    subject: Optional[Reference] = None  # On whom or what the service is to be performed. This is usually a human patient, but can also be ...
    resourceType: str = "ServiceRequest"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers assigned to this order instance by the orderer and/or the receiver and/or order fulfi...
    instantiatesCanonical: Optional[List[str]] = field(default_factory=list)  # The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhe...
    instantiatesUri: Optional[List[str]] = field(default_factory=list)  # The URL pointing to an externally maintained protocol, guideline, orderset or other definition th...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Plan/proposal/order fulfilled by this request.
    replaces: Optional[List[Reference]] = field(default_factory=list)  # The request takes the place of the referenced completed or terminated request(s).
    requisition: Optional[Identifier] = None  # A shared identifier common to all service requests that were authorized more or less simultaneous...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A code that classifies the service for searching, sorting and display purposes (e.g. \"Surgical P...
    priority: Optional[str] = None  # Indicates how quickly the ServiceRequest should be addressed with respect to other requests.
    doNotPerform: Optional[bool] = None  # Set this to true if the record is saying that the service/procedure should NOT be performed.
    code: Optional[Any] = None  # A code or reference that identifies a particular service (i.e., procedure, diagnostic investigati...
    orderDetail: Optional[List[BackboneElement]] = field(default_factory=list)  # Additional details and instructions about the how the services are to be delivered.   For example...
    quantity: Optional[Any] = None  # An amount of service being requested which can be a quantity ( for example $1,500 home modificati...
    focus: Optional[List[Reference]] = field(default_factory=list)  # The actual focus of a service request when it is not the subject of record representing something...
    encounter: Optional[Reference] = None  # An encounter that provides additional information about the healthcare context in which this requ...
    occurrence: Optional[Any] = None  # The date/time at which the requested service should occur.
    asNeeded: Optional[Any] = None  # If a CodeableConcept is present, it indicates the pre-condition for performing the service.  For ...
    authoredOn: Optional[str] = None  # When the request transitioned to being actionable.
    requester: Optional[Reference] = None  # The individual who initiated the request and has responsibility for its activation.
    performerType: Optional[CodeableConcept] = None  # Desired type of performer for doing the requested service.
    performer: Optional[List[Reference]] = field(default_factory=list)  # The desired performer for doing the requested service.  For example, the surgeon, dermatopatholog...
    location: Optional[List[Any]] = field(default_factory=list)  # The preferred location(s) where the procedure should actually happen in coded or free text form. ...
    reason: Optional[List[Any]] = field(default_factory=list)  # An explanation or justification for why this service is being requested in coded or textual form....
    insurance: Optional[List[Reference]] = field(default_factory=list)  # Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be ne...
    supportingInfo: Optional[List[Any]] = field(default_factory=list)  # Additional clinical information about the patient or specimen that may influence the services or ...
    specimen: Optional[List[Reference]] = field(default_factory=list)  # One or more specimens that the laboratory procedure will use.
    bodySite: Optional[List[CodeableConcept]] = field(default_factory=list)  # Anatomic location where the procedure should be performed. This is the target site.
    bodyStructure: Optional[Reference] = None  # Anatomic location where the procedure should be performed. This is the target site.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Any other notes and comments made about the service request. For example, internal billing notes.
    patientInstruction: Optional[List[BackboneElement]] = field(default_factory=list)  # Instructions in terms that are understood by the patient or consumer.
    relevantHistory: Optional[List[Reference]] = field(default_factory=list)  # Key events in the history of the request.