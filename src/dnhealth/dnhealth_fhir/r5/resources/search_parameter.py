# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SearchParameter resource.

A search parameter that defines a named search item that can be used to search/filter on a resource.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, UsageContext
from typing import Any, List, Optional

@dataclass
class SearchParameterComponent:
    """
    SearchParameterComponent nested class.
    """

    definition: Optional[str] = None  # The definition of the search parameter that describes this part.
    expression: Optional[str] = None  # A sub-expression that defines how to extract values for this component from the output of the mai...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class SearchParameter(FHIRResource):
    """
    A search parameter that defines a named search item that can be used to search/filter on a resource.
    """

    url: Optional[str] = None  # An absolute URI that is used to identify this search parameter when it is referenced in a specifi...
    name: Optional[str] = None  # A natural language name identifying the search parameter. This name should be usable as an identi...
    status: Optional[str] = None  # The status of this search parameter. Enables tracking the life-cycle of the content.
    description: Optional[str] = None  # And how it used.
    code: Optional[str] = None  # The label that is recommended to be used in the URL or the parameter name in a parameters resourc...
    base: List[str] = field(default_factory=list)  # The base resource type(s) that this search parameter can be used against.
    type: Optional[str] = None  # The type of value that a search parameter may contain, and how the content is interpreted.
    resourceType: str = "SearchParameter"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this search parameter when it is represented in othe...
    version: Optional[str] = None  # The identifier that is used to identify this version of the search parameter when it is reference...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the search parameter.
    derivedFrom: Optional[str] = None  # Where this search parameter is originally defined. If a derivedFrom is provided, then the details...
    experimental: Optional[bool] = None  # A Boolean value to indicate that this search parameter is authored for testing purposes (or educa...
    date: Optional[str] = None  # The date  (and optionally time) when the search parameter was last significantly changed. The dat...
    publisher: Optional[str] = None  # The name of the organization or individual tresponsible for the release and ongoing maintenance o...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the search parameter is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this search parameter is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the search parameter and/or its contents. Copyright statements ...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    expression: Optional[str] = None  # A FHIRPath expression that returns a set of elements for the search parameter.
    processingMode: Optional[str] = None  # How the search parameter relates to the set of elements returned by evaluating the expression query.
    constraint: Optional[str] = None  # FHIRPath expression that defines/sets a complex constraint for when this SearchParameter is appli...
    target: Optional[List[str]] = field(default_factory=list)  # Types of resource (if a resource is referenced).
    multipleOr: Optional[bool] = None  # Whether multiple values are allowed for each time the parameter exists. Values are separated by c...
    multipleAnd: Optional[bool] = None  # Whether multiple parameters are allowed - e.g. more than one parameter with the same name. The se...
    comparator: Optional[List[str]] = field(default_factory=list)  # Comparators supported for the search parameter.
    modifier: Optional[List[str]] = field(default_factory=list)  # A modifier supported for the search parameter.
    chain: Optional[List[str]] = field(default_factory=list)  # Contains the names of any search parameters which may be chained to the containing search paramet...
    component: Optional[List[BackboneElement]] = field(default_factory=list)  # Used to define the parts of a composite search parameter.