# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 TerminologyCapabilities resource.

A TerminologyCapabilities resource documents a set of capabilities (behaviors) of a FHIR Terminology Server that may be used as a statement of actual server functionality or a statement of required or desired server implementation.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, UsageContext
from typing import Any, List, Optional

@dataclass
class TerminologyCapabilitiesSoftware:
    """
    TerminologyCapabilitiesSoftware nested class.
    """

    name: Optional[str] = None  # Name the software is known by.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    version: Optional[str] = None  # The version identifier for the software covered by this statement.

@dataclass
class TerminologyCapabilitiesImplementation:
    """
    TerminologyCapabilitiesImplementation nested class.
    """

    description: Optional[str] = None  # Information about the specific installation that this terminology capability statement relates to.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    url: Optional[str] = None  # An absolute base URL for the implementation.

@dataclass
class TerminologyCapabilitiesCodeSystem:
    """
    TerminologyCapabilitiesCodeSystem nested class.
    """

    op: List[str] = field(default_factory=list)  # Operations supported for the property.
    content: Optional[str] = None  # The extent of the content of the code system (the concepts and codes it defines) are represented ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    uri: Optional[str] = None  # Canonical identifier for the code system, represented as a URI.
    version: Optional[List[BackboneElement]] = field(default_factory=list)  # For the code system, a list of versions that are supported by the server.
    code: Optional[str] = None  # For version-less code systems, there should be a single version with no identifier.
    isDefault: Optional[bool] = None  # If this is the default version for this code system.
    compositional: Optional[bool] = None  # If the compositional grammar defined by the code system is supported.
    language: Optional[List[str]] = field(default_factory=list)  # Language Displays supported.
    filter: Optional[List[BackboneElement]] = field(default_factory=list)  # Filter Properties supported.
    property: Optional[List[str]] = field(default_factory=list)  # Properties supported for $lookup.
    subsumption: Optional[bool] = None  # True if subsumption is supported for this version of the code system.

@dataclass
class TerminologyCapabilitiesCodeSystemVersion:
    """
    TerminologyCapabilitiesCodeSystemVersion nested class.
    """

    op: List[str] = field(default_factory=list)  # Operations supported for the property.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    code: Optional[str] = None  # For version-less code systems, there should be a single version with no identifier.
    isDefault: Optional[bool] = None  # If this is the default version for this code system.
    compositional: Optional[bool] = None  # If the compositional grammar defined by the code system is supported.
    language: Optional[List[str]] = field(default_factory=list)  # Language Displays supported.
    filter: Optional[List[BackboneElement]] = field(default_factory=list)  # Filter Properties supported.
    property: Optional[List[str]] = field(default_factory=list)  # Properties supported for $lookup.

@dataclass
class TerminologyCapabilitiesCodeSystemVersionFilter:
    """
    TerminologyCapabilitiesCodeSystemVersionFilter nested class.
    """

    code: Optional[str] = None  # Code of the property supported.
    op: List[str] = field(default_factory=list)  # Operations supported for the property.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class TerminologyCapabilitiesExpansion:
    """
    TerminologyCapabilitiesExpansion nested class.
    """

    name: Optional[str] = None  # Name of the supported expansion parameter.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    hierarchical: Optional[bool] = None  # Whether the server can return nested value sets.
    paging: Optional[bool] = None  # Whether the server supports paging on expansion.
    incomplete: Optional[bool] = None  # True if requests for incomplete expansions are allowed.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Supported expansion parameter.
    documentation: Optional[str] = None  # Description of support for parameter.
    textFilter: Optional[str] = None  # Documentation about text searching works.

@dataclass
class TerminologyCapabilitiesExpansionParameter:
    """
    TerminologyCapabilitiesExpansionParameter nested class.
    """

    name: Optional[str] = None  # Name of the supported expansion parameter.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    documentation: Optional[str] = None  # Description of support for parameter.

@dataclass
class TerminologyCapabilitiesValidateCode:
    """
    TerminologyCapabilitiesValidateCode nested class.
    """

    translations: Optional[bool] = None  # Whether translations are validated.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class TerminologyCapabilitiesTranslation:
    """
    TerminologyCapabilitiesTranslation nested class.
    """

    needsMap: Optional[bool] = None  # Whether the client must identify the map.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class TerminologyCapabilitiesClosure:
    """
    TerminologyCapabilitiesClosure nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    translation: Optional[bool] = None  # If cross-system closure is supported.


@dataclass
class TerminologyCapabilities(FHIRResource):
    """
    A TerminologyCapabilities resource documents a set of capabilities (behaviors) of a FHIR Terminology Server that may be used as a statement of actual server functionality or a statement of required or desired server implementation.
    """

    status: Optional[str] = None  # The status of this terminology capabilities. Enables tracking the life-cycle of the content.
    date: Optional[str] = None  # The date  (and optionally time) when the terminology capabilities was last significantly changed....
    kind: Optional[str] = None  # The way that this statement is intended to be used, to describe an actual running instance of sof...
    resourceType: str = "TerminologyCapabilities"
    url: Optional[str] = None  # An absolute URI that is used to identify this terminology capabilities when it is referenced in a...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this terminology capabilities when it is represented...
    version: Optional[str] = None  # The identifier that is used to identify this version of the terminology capabilities when it is r...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the terminology capabilities. This name should be usable as a...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the terminology capabilities.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this terminology capabilities is authored for testing purposes (...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the terminology capabilities from a consumer's perspe...
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the terminology capabilities is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this terminology capabilities is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the terminology capabilities and/or its contents. Copyright sta...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    software: Optional[BackboneElement] = None  # Software that is covered by this terminology capability statement.  It is used when the statement...
    implementation: Optional[BackboneElement] = None  # Identifies a specific implementation instance that is described by the terminology capability sta...
    lockedDate: Optional[bool] = None  # Whether the server supports lockedDate.
    codeSystem: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies a code system that is supported by the server. If there is a no code system URL, then ...
    expansion: Optional[BackboneElement] = None  # Information about the [ValueSet/$expand](valueset-operation-expand.html) operation.
    codeSearch: Optional[str] = None  # The degree to which the server supports the code search parameter on ValueSet, if it is supported.
    validateCode: Optional[BackboneElement] = None  # Information about the [ValueSet/$validate-code](valueset-operation-validate-code.html) operation.
    translation: Optional[BackboneElement] = None  # Information about the [ConceptMap/$translate](conceptmap-operation-translate.html) operation.
    closure: Optional[BackboneElement] = None  # Whether the $closure operation is supported.