# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Provenance resource.

Guidance on using Provenance for related history elements to provide key events that have happened over the lifespan of the resource  - see the use of this pattern in the [Request Pattern](request.html#history)
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Reference, Signature
from typing import Any, List, Optional

@dataclass
class ProvenanceAgent:
    """
    ProvenanceAgent nested class.
    """

    type: Optional[CodeableConcept] = None  # The Functional Role of the agent with respect to the activity.
    who: Optional[Reference] = None  # Indicates who or what performed in the event.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    role: Optional[List[CodeableConcept]] = field(default_factory=list)  # The structural roles of the agent indicating the agent's competency. The security role enabling t...
    onBehalfOf: Optional[Reference] = None  # The agent that delegated authority to perform the activity performed by the agent.who element.

@dataclass
class ProvenanceEntity:
    """
    ProvenanceEntity nested class.
    """

    role: Optional[str] = None  # How the entity was used during the activity.
    what: Optional[Reference] = None  # Identity of the  Entity used. May be a logical or physical uri and maybe absolute or relative.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    agent: Optional[List[Any]] = field(default_factory=list)  # The entity is attributed to an agent to express the agent's responsibility for that entity, possi...


@dataclass
class Provenance(FHIRResource):
    """
    Guidance on using Provenance for related history elements to provide key events that have happened over the lifespan of the resource  - see the use of this pattern in the [Request Pattern](request.html#history)
    """

    target: List[Reference] = field(default_factory=list)  # This points to the version of the resource that was created as a result of this historical record...
    occurred: Optional[str] = None  # This indicates the time the resource action (creation, revision, deletion, etc.) occurred.
    activity: Optional[CodeableConcept] = None  # Indicates what action occurred to the referenced resource.
    agent: List[BackboneElement] = field(default_factory=list)  # Who was involved with change.
    resourceType: str = "Provenance"
    recorded: Optional[str] = None  # The instant of time at which the activity was recorded.
    policy: Optional[List[str]] = field(default_factory=list)  # Policy or plan the activity was defined by. Typically, a single activity may have multiple applic...
    location: Optional[Reference] = None  # Where the activity occurred, if relevant.
    authorization: Optional[List[Any]] = field(default_factory=list)  # The authorization (e.g., PurposeOfUse) that was used during the event being recorded.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Allows tracing of authorizatino for the events and tracking whether proposals/recommendations wer...
    patient: Optional[Reference] = None  # The patient element is available to enable deterministic tracking of activities that involve the ...
    encounter: Optional[Reference] = None  # This will typically be the encounter the event occurred, but some events may be initiated prior t...
    entity: Optional[List[BackboneElement]] = field(default_factory=list)  # An entity used in this activity.
    signature: Optional[List[Signature]] = field(default_factory=list)  # A digital signature on the target Reference(s). The signer should match a Provenance.agent. The p...