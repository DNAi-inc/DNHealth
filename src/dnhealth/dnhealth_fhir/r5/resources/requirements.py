# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Requirements resource.

The Requirements resource is used to describe an actor - a human or an application that plays a role in data exchange, and that may have obligations associated with the role the actor plays.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Reference, UsageContext
from typing import Any, List, Optional

@dataclass
class RequirementsStatement:
    """
    RequirementsStatement nested class.
    """

    key: Optional[str] = None  # Key that identifies this statement (unique within this resource).
    requirement: Optional[str] = None  # The actual requirement for human consumption.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    label: Optional[str] = None  # A short human usable label for this statement.
    conformance: Optional[List[str]] = field(default_factory=list)  # A short human usable label for this statement.
    conditionality: Optional[bool] = None  # This boolean flag is set to true of the text of the requirement is conditional on something e.g. ...
    derivedFrom: Optional[str] = None  # Another statement on one of the requirements that this requirement clarifies or restricts.
    parent: Optional[str] = None  # A larger requirement that this requirement helps to refine and enable.
    satisfiedBy: Optional[List[str]] = field(default_factory=list)  # A reference to another artifact that satisfies this requirement. This could be a Profile, extensi...
    reference: Optional[List[str]] = field(default_factory=list)  # A reference to another artifact that created this requirement. This could be a Profile, etc., or ...
    source: Optional[List[Reference]] = field(default_factory=list)  # Who asked for this statement to be a requirement. By default, it's assumed that the publisher kno...


@dataclass
class Requirements(FHIRResource):
    """
    The Requirements resource is used to describe an actor - a human or an application that plays a role in data exchange, and that may have obligations associated with the role the actor plays.
    """

    status: Optional[str] = None  # The status of this Requirements. Enables tracking the life-cycle of the content.
    resourceType: str = "Requirements"
    url: Optional[str] = None  # An absolute URI that is used to identify this Requirements when it is referenced in a specificati...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this Requirements when it is represented in other fo...
    version: Optional[str] = None  # The identifier that is used to identify this version of the Requirements when it is referenced in...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the Requirements. This name should be usable as an identifier...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the Requirements.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this Requirements is authored for testing purposes (or education...
    date: Optional[str] = None  # The date  (and optionally time) when the Requirements was published. The date must change when th...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the requirements.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the Requirements is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this Requirements is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the Requirements and/or its contents. Copyright statements are ...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    derivedFrom: Optional[List[str]] = field(default_factory=list)  # Another set of Requirements that this set of Requirements builds on and updates.
    reference: Optional[List[str]] = field(default_factory=list)  # A reference to another artifact that created this set of requirements. This could be a Profile, e...
    actor: Optional[List[str]] = field(default_factory=list)  # An actor these requirements are in regard to.
    statement: Optional[List[BackboneElement]] = field(default_factory=list)  # The actual statement of requirement, in markdown format.