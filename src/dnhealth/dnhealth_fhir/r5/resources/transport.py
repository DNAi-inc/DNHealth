# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Transport resource.

Record of transport.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import Address, Age, Annotation, Attachment, BackboneElement, CodeableConcept, Coding, ContactDetail, ContactPoint, Count, DataRequirement, Distance, Dosage, Duration, Expression, Extension, HumanName, Identifier, Money, ParameterDefinition, Period, Quantity, Range, Ratio, Reference, RelatedArtifact, SampledData, Signature, Timing, TriggerDefinition, UsageContext
from typing import Any, List, Optional

@dataclass
class TransportRestriction:
    """
    TransportRestriction nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    repetitions: Optional[int] = None  # Indicates the number of times the requested action should occur.
    period: Optional[Period] = None  # Over what time-period is fulfillment sought.
    recipient: Optional[List[Reference]] = field(default_factory=list)  # For requests that are targeted to more than one potential recipient/target, to identify who is fu...

@dataclass
class TransportInput:
    """
    TransportInput nested class.
    """

    type: Optional[CodeableConcept] = None  # A code or description indicating how the input is intended to be used as part of the transport ex...
    value: Optional[Any] = None  # The value of the input parameter as a basic type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class TransportOutput:
    """
    TransportOutput nested class.
    """

    type: Optional[CodeableConcept] = None  # The name of the Output parameter.
    value: Optional[Any] = None  # The value of the Output parameter as a basic type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Transport(FHIRResource):
    """
    Record of transport.
    """

    intent: Optional[str] = None  # Indicates the \"level\" of actionability associated with the Transport, i.e. i+R[9]Cs this a prop...
    requestedLocation: Optional[Reference] = None  # The desired or final location for the transport.
    currentLocation: Optional[Reference] = None  # The current location for the entity to be transported.
    resourceType: str = "Transport"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for the transport event that is used to identify it across multiple disparate systems.
    instantiatesCanonical: Optional[str] = None  # The URL pointing to a *FHIR*-defined protocol, guideline, orderset or other definition that is ad...
    instantiatesUri: Optional[str] = None  # The URL pointing to an *externally* maintained  protocol, guideline, orderset or other definition...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # BasedOn refers to a higher-level authorization that triggered the creation of the transport.  It ...
    groupIdentifier: Optional[Identifier] = None  # A shared identifier common to multiple independent Request instances that were activated/authoriz...
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular event is a component or step.
    status: Optional[str] = None  # A code specifying the state of the transport event.
    statusReason: Optional[CodeableConcept] = None  # An explanation as to why this transport is held, failed, was refused, etc.
    priority: Optional[str] = None  # Indicates how quickly the Transport should be addressed with respect to other requests.
    code: Optional[CodeableConcept] = None  # A name or code (or both) briefly describing what the transport involves.
    description: Optional[str] = None  # A free-text description of what is to be performed.
    focus: Optional[Reference] = None  # The request being actioned or the resource being manipulated by this transport.
    for_: Optional[Reference] = None  # The entity who benefits from the performance of the service specified in the transport (e.g., the...
    encounter: Optional[Reference] = None  # The healthcare event  (e.g. a patient and healthcare provider interaction) during which this tran...
    completionTime: Optional[str] = None  # Identifies the completion time of the event (the occurrence).
    authoredOn: Optional[str] = None  # The date and time this transport was created.
    lastModified: Optional[str] = None  # The date and time of last modification to this transport.
    requester: Optional[Reference] = None  # The creator of the transport.
    performerType: Optional[List[CodeableConcept]] = field(default_factory=list)  # The kind of participant that should perform the transport.
    owner: Optional[Reference] = None  # Individual organization or Device currently responsible for transport execution.
    location: Optional[Reference] = None  # Principal physical location where this transport is performed.
    insurance: Optional[List[Reference]] = field(default_factory=list)  # Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be re...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Free-text information captured about the transport as it progresses.
    relevantHistory: Optional[List[Reference]] = field(default_factory=list)  # Links to Provenance records for past versions of this Transport that identify key state transitio...
    restriction: Optional[BackboneElement] = None  # If the Transport.focus is a request resource and the transport is seeking fulfillment (i.e. is as...
    input: Optional[List[BackboneElement]] = field(default_factory=list)  # Additional information that may be needed in the execution of the transport.
    output: Optional[List[BackboneElement]] = field(default_factory=list)  # Outputs produced by the Transport.
    reason: Optional[Any] = None  # A resource reference indicating why this transport needs to be performed.
    history: Optional[Reference] = None  # The transport event prior to this one.