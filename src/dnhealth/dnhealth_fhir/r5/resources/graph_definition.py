# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 GraphDefinition resource.

A formal computable definition of a graph of resources - that is, a coherent set of resources that form a graph by following references. The Graph Definition resource defines a set and makes rules about the set.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, UsageContext
from typing import Any, List, Optional

@dataclass
class GraphDefinitionNode:
    """
    GraphDefinitionNode nested class.
    """

    nodeId: Optional[str] = None  # Internal ID of node - target for link references.
    type: Optional[str] = None  # Type of resource this link refers to.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Information about why this node is of interest in this graph definition.
    profile: Optional[str] = None  # Profile for the target resource.

@dataclass
class GraphDefinitionLink:
    """
    GraphDefinitionLink nested class.
    """

    sourceId: Optional[str] = None  # The source node for this link.
    targetId: Optional[str] = None  # The target node for this link.
    use: Optional[str] = None  # Defines how the compartment rule is used - whether it it is used to test whether resources are su...
    rule: Optional[str] = None  # identical | matching | different | no-rule | custom.
    code: Optional[str] = None  # Identifies the compartment.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Information about why this link is of interest in this graph definition.
    min: Optional[int] = None  # Minimum occurrences for this link.
    max: Optional[str] = None  # Maximum occurrences for this link.
    path: Optional[str] = None  # A FHIRPath expression that identifies one of FHIR References to other resources.
    sliceName: Optional[str] = None  # Which slice (if profiled).
    params: Optional[str] = None  # A set of parameters to look up.
    compartment: Optional[List[BackboneElement]] = field(default_factory=list)  # Compartment Consistency Rules.
    expression: Optional[str] = None  # Custom rule, as a FHIRPath expression.

@dataclass
class GraphDefinitionLinkCompartment:
    """
    GraphDefinitionLinkCompartment nested class.
    """

    use: Optional[str] = None  # Defines how the compartment rule is used - whether it it is used to test whether resources are su...
    rule: Optional[str] = None  # identical | matching | different | no-rule | custom.
    code: Optional[str] = None  # Identifies the compartment.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    expression: Optional[str] = None  # Custom rule, as a FHIRPath expression.
    description: Optional[str] = None  # Documentation for FHIRPath expression.


@dataclass
class GraphDefinition(FHIRResource):
    """
    A formal computable definition of a graph of resources - that is, a coherent set of resources that form a graph by following references. The Graph Definition resource defines a set and makes rules about the set.
    """

    name: Optional[str] = None  # A natural language name identifying the graph definition. This name should be usable as an identi...
    status: Optional[str] = None  # The status of this graph definition. Enables tracking the life-cycle of the content.
    resourceType: str = "GraphDefinition"
    url: Optional[str] = None  # An absolute URI that is used to identify this graph definition when it is referenced in a specifi...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this GraphDefinition when it is represented in other...
    version: Optional[str] = None  # The identifier that is used to identify this version of the graph definition when it is reference...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the capability statement.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this graph definition is authored for testing purposes (or educa...
    date: Optional[str] = None  # The date  (and optionally time) when the graph definition was last significantly changed. The dat...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the graph definition from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the graph definition is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this graph definition is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the graph definition and/or its contents. Copyright statements ...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    start: Optional[str] = None  # The Node at which instances of this graph start. If there is no nominated start, the graph can st...
    node: Optional[List[BackboneElement]] = field(default_factory=list)  # Potential target for the link.
    link: Optional[List[BackboneElement]] = field(default_factory=list)  # Links this graph makes rules about.