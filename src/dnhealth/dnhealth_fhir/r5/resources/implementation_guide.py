# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ImplementationGuide resource.

A set of rules of how a particular interoperability or standards problem is solved - typically through the use of FHIR resources. This resource is used to gather all the parts of an implementation guide into a logical whole and to publish a computable definition of all the parts.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Reference, UsageContext
from typing import Any, List, Optional

@dataclass
class ImplementationGuideDependsOn:
    """
    ImplementationGuideDependsOn nested class.
    """

    uri: Optional[str] = None  # A canonical reference to the Implementation guide for the dependency.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    packageId: Optional[str] = None  # The NPM package name for the Implementation Guide that this IG depends on.
    version: Optional[str] = None  # The version of the IG that is depended on, when the correct version is required to understand the...
    reason: Optional[str] = None  # A description explaining the nature of the dependency on the listed IG.

@dataclass
class ImplementationGuideGlobal:
    """
    ImplementationGuideGlobal nested class.
    """

    type: Optional[str] = None  # The type of resource that all instances must conform to.
    profile: Optional[str] = None  # A reference to the profile that all instances must conform to.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ImplementationGuideDefinition:
    """
    ImplementationGuideDefinition nested class.
    """

    name: Optional[str] = None  # The human-readable title to display for the package of resources when rendering the implementatio...
    reference: Optional[Reference] = None  # Where this resource is found.
    title: Optional[str] = None  # A short title used to represent this page in navigational structures such as table of contents, b...
    generation: Optional[str] = None  # A code that indicates how the page is generated.
    code: Optional[Coding] = None  # A tool-specific code that defines the parameter.
    value: Optional[str] = None  # Value for named type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    grouping: Optional[List[BackboneElement]] = field(default_factory=list)  # A logical group of resources. Logical groups can be used when building pages.
    description: Optional[str] = None  # Human readable text describing the package.
    resource: Optional[List[BackboneElement]] = field(default_factory=list)  # A resource that is part of the implementation guide. Conformance resources (value set, structure ...
    fhirVersion: Optional[List[str]] = field(default_factory=list)  # Indicates the FHIR Version(s) this artifact is intended to apply to. If no versions are specified...
    isExample: Optional[bool] = None  # If true, indicates the resource is an example instance.
    profile: Optional[List[str]] = field(default_factory=list)  # If present, indicates profile(s) the instance is valid against.
    groupingId: Optional[str] = None  # Reference to the id of the grouping this resource appears in.
    page: Optional[BackboneElement] = None  # A page / section in the implementation guide. The root page is the implementation guide home page.
    source: Optional[Any] = None  # Indicates the URL or the actual content to provide for the page.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # A set of parameters that defines how the implementation guide is built. The parameters are define...
    template: Optional[List[BackboneElement]] = field(default_factory=list)  # A template for building resources.
    scope: Optional[str] = None  # The scope in which the template applies.

@dataclass
class ImplementationGuideDefinitionGrouping:
    """
    ImplementationGuideDefinitionGrouping nested class.
    """

    name: Optional[str] = None  # The human-readable title to display for the package of resources when rendering the implementatio...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Human readable text describing the package.

@dataclass
class ImplementationGuideDefinitionResource:
    """
    ImplementationGuideDefinitionResource nested class.
    """

    reference: Optional[Reference] = None  # Where this resource is found.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    fhirVersion: Optional[List[str]] = field(default_factory=list)  # Indicates the FHIR Version(s) this artifact is intended to apply to. If no versions are specified...
    name: Optional[str] = None  # A human assigned name for the resource. All resources SHOULD have a name, but the name may be ext...
    description: Optional[str] = None  # A description of the reason that a resource has been included in the implementation guide.
    isExample: Optional[bool] = None  # If true, indicates the resource is an example instance.
    profile: Optional[List[str]] = field(default_factory=list)  # If present, indicates profile(s) the instance is valid against.
    groupingId: Optional[str] = None  # Reference to the id of the grouping this resource appears in.

@dataclass
class ImplementationGuideDefinitionPage:
    """
    ImplementationGuideDefinitionPage nested class.
    """

    name: Optional[str] = None  # The url by which the page should be known when published.
    title: Optional[str] = None  # A short title used to represent this page in navigational structures such as table of contents, b...
    generation: Optional[str] = None  # A code that indicates how the page is generated.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    source: Optional[Any] = None  # Indicates the URL or the actual content to provide for the page.
    page: Optional[List[Any]] = field(default_factory=list)  # Nested Pages/Sections under this page.

@dataclass
class ImplementationGuideDefinitionParameter:
    """
    ImplementationGuideDefinitionParameter nested class.
    """

    code: Optional[Coding] = None  # A tool-specific code that defines the parameter.
    value: Optional[str] = None  # Value for named type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ImplementationGuideDefinitionTemplate:
    """
    ImplementationGuideDefinitionTemplate nested class.
    """

    code: Optional[str] = None  # Type of template specified.
    source: Optional[str] = None  # The source location for the template.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    scope: Optional[str] = None  # The scope in which the template applies.

@dataclass
class ImplementationGuideManifest:
    """
    ImplementationGuideManifest nested class.
    """

    resource: List[BackboneElement] = field(default_factory=list)  # A resource that is part of the implementation guide. Conformance resources (value set, structure ...
    reference: Optional[Reference] = None  # Where this resource is found.
    name: Optional[str] = None  # Relative path to the page.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    rendering: Optional[str] = None  # A pointer to official web page, PDF or other rendering of the implementation guide.
    isExample: Optional[bool] = None  # If true, indicates the resource is an example instance.
    profile: Optional[List[str]] = field(default_factory=list)  # If present, indicates profile(s) the instance is valid against.
    relativePath: Optional[str] = None  # The relative path for primary page for this resource within the IG.
    page: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about a page within the IG.
    title: Optional[str] = None  # Label for the page intended for human display.
    anchor: Optional[List[str]] = field(default_factory=list)  # The name of an anchor available on the page.
    image: Optional[List[str]] = field(default_factory=list)  # Indicates a relative path to an image that exists within the IG.
    other: Optional[List[str]] = field(default_factory=list)  # Indicates the relative path of an additional non-page, non-image file that is part of the IG - e....

@dataclass
class ImplementationGuideManifestResource:
    """
    ImplementationGuideManifestResource nested class.
    """

    reference: Optional[Reference] = None  # Where this resource is found.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    isExample: Optional[bool] = None  # If true, indicates the resource is an example instance.
    profile: Optional[List[str]] = field(default_factory=list)  # If present, indicates profile(s) the instance is valid against.
    relativePath: Optional[str] = None  # The relative path for primary page for this resource within the IG.

@dataclass
class ImplementationGuideManifestPage:
    """
    ImplementationGuideManifestPage nested class.
    """

    name: Optional[str] = None  # Relative path to the page.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # Label for the page intended for human display.
    anchor: Optional[List[str]] = field(default_factory=list)  # The name of an anchor available on the page.


@dataclass
class ImplementationGuide(FHIRResource):
    """
    A set of rules of how a particular interoperability or standards problem is solved - typically through the use of FHIR resources. This resource is used to gather all the parts of an implementation guide into a logical whole and to publish a computable definition of all the parts.
    """

    url: Optional[str] = None  # An absolute URI that is used to identify this implementation guide when it is referenced in a spe...
    name: Optional[str] = None  # A natural language name identifying the implementation guide. This name should be usable as an id...
    status: Optional[str] = None  # The status of this implementation guide. Enables tracking the life-cycle of the content.
    packageId: Optional[str] = None  # The NPM package name for this Implementation Guide, used in the NPM package distribution, which i...
    fhirVersion: List[str] = field(default_factory=list)  # The version(s) of the FHIR specification that this ImplementationGuide targets - e.g. describes h...
    resourceType: str = "ImplementationGuide"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this implementation guide when it is represented in ...
    version: Optional[str] = None  # The identifier that is used to identify this version of the implementation guide when it is refer...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the implementation guide.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this implementation guide is authored for testing purposes (or e...
    date: Optional[str] = None  # The date  (and optionally time) when the implementation guide was last significantly changed. The...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the implementation guide from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the implementation guide is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this implementation guide is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the implementation guide and/or its contents. Copyright stateme...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    license: Optional[str] = None  # The license that applies to this Implementation Guide, using an SPDX license code, or 'not-open-s...
    dependsOn: Optional[List[BackboneElement]] = field(default_factory=list)  # Another implementation guide that this implementation depends on. Typically, an implementation gu...
    global_: Optional[List[BackboneElement]] = field(default_factory=list)  # A set of profiles that all resources covered by this implementation guide must conform to.
    definition: Optional[BackboneElement] = None  # The information needed by an IG publisher tool to publish the whole implementation guide.
    manifest: Optional[BackboneElement] = None  # Information about an assembled implementation guide, created by the publication tooling.