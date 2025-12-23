# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MessageDefinition resource.

Defines the characteristics of a message that can be shared between systems, including the type of event that initiates the message, the content to be transmitted and what response(s), if any, are permitted.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, UsageContext
from typing import Any, List, Optional

@dataclass
class MessageDefinitionFocus:
    """
    MessageDefinitionFocus nested class.
    """

    code: Optional[str] = None  # The kind of resource that must be the focus for this message.
    min: Optional[int] = None  # Identifies the minimum number of resources of this type that must be pointed to by a message in o...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    profile: Optional[str] = None  # A profile that reflects constraints for the focal resource (and potentially for related resources).
    max: Optional[str] = None  # Identifies the maximum number of resources of this type that must be pointed to by a message in o...

@dataclass
class MessageDefinitionAllowedResponse:
    """
    MessageDefinitionAllowedResponse nested class.
    """

    message: Optional[str] = None  # A reference to the message definition that must be adhered to by this supported response.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    situation: Optional[str] = None  # Provides a description of the circumstances in which this response should be used (as opposed to ...


@dataclass
class MessageDefinition(FHIRResource):
    """
    Defines the characteristics of a message that can be shared between systems, including the type of event that initiates the message, the content to be transmitted and what response(s), if any, are permitted.
    """

    status: Optional[str] = None  # The status of this message definition. Enables tracking the life-cycle of the content.
    date: Optional[str] = None  # The date  (and optionally time) when the message definition was last significantly changed. The d...
    event: Optional[Any] = None  # Event code or link to the EventDefinition.
    resourceType: str = "MessageDefinition"
    url: Optional[str] = None  # The business identifier that is used to reference the MessageDefinition and *is* expected to be c...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this message definition when it is represented in ot...
    version: Optional[str] = None  # The identifier that is used to identify this version of the message definition when it is referen...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the message definition. This name should be usable as an iden...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the message definition.
    replaces: Optional[List[str]] = field(default_factory=list)  # A MessageDefinition that is superseded by this definition.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this message definition is authored for testing purposes (or edu...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the message definition from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the message definition is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this message definition is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the message definition and/or its contents. Copyright statement...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    base: Optional[str] = None  # The MessageDefinition that is the basis for the contents of this resource.
    parent: Optional[List[str]] = field(default_factory=list)  # Identifies a protocol or workflow that this MessageDefinition represents a step in.
    category: Optional[str] = None  # The impact of the content of the message.
    focus: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies the resource (or resources) that are being addressed by the event.  For example, the E...
    responseRequired: Optional[str] = None  # Declare at a message definition level whether a response is required or only upon error or succes...
    allowedResponse: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates what types of messages may be sent as an application-level response to this message.
    graph: Optional[str] = None  # Graph is Canonical reference to a GraphDefinition. If a URL is provided, it is the canonical refe...