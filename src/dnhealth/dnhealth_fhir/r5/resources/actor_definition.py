# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ActorDefinition resource.

The ActorDefinition resource is used to describe an actor - a human or an application that plays a role in data exchange, and that may have obligations associated with the role the actor plays.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Coding, ContactDetail, Identifier, UsageContext
from typing import Any, List, Optional

@dataclass
class ActorDefinition(FHIRResource):
    """
    The ActorDefinition resource is used to describe an actor - a human or an application that plays a role in data exchange, and that may have obligations associated with the role the actor plays.
    """

    status: Optional[str] = None  # The status of this actor definition. Enables tracking the life-cycle of the content.
    type: Optional[str] = None  # Whether the actor represents a human or an appliction.
    resourceType: str = "ActorDefinition"
    url: Optional[str] = None  # An absolute URI that is used to identify this actor definition when it is referenced in a specifi...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this actor definition when it is represented in othe...
    version: Optional[str] = None  # The identifier that is used to identify this version of the actor definition when it is reference...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the actor definition. This name should be usable as an identi...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the actor definition.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this actor definition is authored for testing purposes (or educa...
    date: Optional[str] = None  # The date  (and optionally time) when the actor definition was last significantly changed. The dat...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the actor.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the actor definition is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this actor definition is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the actor definition and/or its contents. Copyright statements ...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    documentation: Optional[str] = None  # Documentation about the functionality of the actor.
    reference: Optional[List[str]] = field(default_factory=list)  # A reference to additional documentation about the actor, but description and documentation.
    capabilities: Optional[str] = None  # The capability statement for the actor (if the concept is applicable).
    derivedFrom: Optional[List[str]] = field(default_factory=list)  # A url that identifies the definition of this actor in another IG (which IG must be listed in the ...