# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 CompartmentDefinition resource.

A compartment definition that defines how resources are accessed on a server.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, Coding, ContactDetail, Extension, UsageContext
from typing import Any, List, Optional

@dataclass
class CompartmentDefinitionResource:
    """
    CompartmentDefinitionResource nested class.
    """

    code: Optional[str] = None  # The name of a resource supported by the server.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    param: Optional[List[str]] = field(default_factory=list)  # The name of a search parameter that represents the link to the compartment. More than one may be ...
    documentation: Optional[str] = None  # Additional documentation about the resource and compartment.
    startParam: Optional[str] = None  # Search Parameter for mapping requests made with $everything.start (e.g. on [Patient.$everything](...
    endParam: Optional[str] = None  # Search Parameter for mapping requests made with $everything.end (e.g. on [Patient.$everything](pa...


@dataclass
class CompartmentDefinition(FHIRResource):
    """
    A compartment definition that defines how resources are accessed on a server.
    """

    url: Optional[str] = None  # An absolute URI that is used to identify this compartment definition when it is referenced in a s...
    name: Optional[str] = None  # A natural language name identifying the compartment definition. This name should be usable as an ...
    status: Optional[str] = None  # The status of this compartment definition. Enables tracking the life-cycle of the content.
    code: Optional[str] = None  # Which compartment this definition describes.
    search: Optional[bool] = None  # Whether the search syntax is supported,.
    resourceType: str = "CompartmentDefinition"
    version: Optional[str] = None  # The identifier that is used to identify this version of the compartment definition when it is ref...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the capability statement.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this compartment definition is authored for testing purposes (or...
    date: Optional[str] = None  # The date  (and optionally time) when the compartment definition was last significantly changed. T...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the compartment definition from a consumer's perspect...
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    purpose: Optional[str] = None  # Explanation of why this compartment definition is needed and why it has been designed as it has.
    resource: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about how a resource is related to the compartment.