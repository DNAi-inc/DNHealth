# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 EvidenceVariable resource.

The EvidenceVariable resource describes an element that knowledge (Evidence) is about.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Coding, ContactDetail, Expression, Extension, Identifier, Period, Quantity, Range, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class EvidenceVariableCharacteristic:
    """
    EvidenceVariableCharacteristic nested class.
    """

    type: Optional[CodeableConcept] = None  # Used to express the type of characteristic.
    value: Optional[Any] = None  # Defines the characteristic when paired with characteristic.type.
    code: Optional[str] = None  # Used to specify if two or more characteristics are combined with OR or AND.
    characteristic: List[Any] = field(default_factory=list)  # A defining factor of the characteristic.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    linkId: Optional[str] = None  # Label used for when a characteristic refers to another characteristic.
    description: Optional[str] = None  # A short, natural language description of the characteristic that could be used to communicate the...
    note: Optional[List[Annotation]] = field(default_factory=list)  # A human-readable string to clarify or explain concepts about the characteristic.
    exclude: Optional[bool] = None  # When true, this characteristic is an exclusion criterion. In other words, not matching this chara...
    definitionReference: Optional[Reference] = None  # Defines the characteristic using a Reference.
    definitionCanonical: Optional[str] = None  # Defines the characteristic using Canonical.
    definitionCodeableConcept: Optional[CodeableConcept] = None  # Defines the characteristic using CodeableConcept.
    definitionExpression: Optional[Expression] = None  # Defines the characteristic using Expression.
    definitionId: Optional[str] = None  # Defines the characteristic using id.
    definitionByTypeAndValue: Optional[BackboneElement] = None  # Defines the characteristic using both a type and value[x] elements.
    method: Optional[List[CodeableConcept]] = field(default_factory=list)  # Method for how the characteristic value was determined.
    device: Optional[Reference] = None  # Device used for determining characteristic.
    offset: Optional[CodeableConcept] = None  # Defines the reference point for comparison when valueQuantity or valueRange is not compared to zero.
    definitionByCombination: Optional[BackboneElement] = None  # Defines the characteristic as a combination of two or more characteristics.
    threshold: Optional[int] = None  # Provides the value of \"n\" when \"at-least\" or \"at-most\" codes are used.
    instances: Optional[Any] = None  # Number of occurrences meeting the characteristic.
    duration: Optional[Any] = None  # Length of time in which the characteristic is met.
    timeFromEvent: Optional[List[BackboneElement]] = field(default_factory=list)  # Timing in which the characteristic is determined.
    event: Optional[Any] = None  # The event used as a base point (reference point) in time.
    quantity: Optional[Quantity] = None  # Used to express the observation at a defined amount of time before or after the event.
    range: Optional[Range] = None  # Used to express the observation within a period before and/or after the event.

@dataclass
class EvidenceVariableCharacteristicDefinitionByTypeAndValue:
    """
    EvidenceVariableCharacteristicDefinitionByTypeAndValue nested class.
    """

    type: Optional[CodeableConcept] = None  # Used to express the type of characteristic.
    value: Optional[Any] = None  # Defines the characteristic when paired with characteristic.type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    method: Optional[List[CodeableConcept]] = field(default_factory=list)  # Method for how the characteristic value was determined.
    device: Optional[Reference] = None  # Device used for determining characteristic.
    offset: Optional[CodeableConcept] = None  # Defines the reference point for comparison when valueQuantity or valueRange is not compared to zero.

@dataclass
class EvidenceVariableCharacteristicDefinitionByCombination:
    """
    EvidenceVariableCharacteristicDefinitionByCombination nested class.
    """

    code: Optional[str] = None  # Used to specify if two or more characteristics are combined with OR or AND.
    characteristic: List[Any] = field(default_factory=list)  # A defining factor of the characteristic.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    threshold: Optional[int] = None  # Provides the value of \"n\" when \"at-least\" or \"at-most\" codes are used.

@dataclass
class EvidenceVariableCharacteristicTimeFromEvent:
    """
    EvidenceVariableCharacteristicTimeFromEvent nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Human readable description.
    note: Optional[List[Annotation]] = field(default_factory=list)  # A human-readable string to clarify or explain concepts about the timeFromEvent.
    event: Optional[Any] = None  # The event used as a base point (reference point) in time.
    quantity: Optional[Quantity] = None  # Used to express the observation at a defined amount of time before or after the event.
    range: Optional[Range] = None  # Used to express the observation within a period before and/or after the event.

@dataclass
class EvidenceVariableCategory:
    """
    EvidenceVariableCategory nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Description of the grouping.
    value: Optional[Any] = None  # Definition of the grouping.


@dataclass
class EvidenceVariable(FHIRResource):
    """
    The EvidenceVariable resource describes an element that knowledge (Evidence) is about.
    """

    status: Optional[str] = None  # The status of this evidence variable. Enables tracking the life-cycle of the content.
    resourceType: str = "EvidenceVariable"
    url: Optional[str] = None  # An absolute URI that is used to identify this evidence variable when it is referenced in a specif...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this evidence variable when it is represented in oth...
    version: Optional[str] = None  # The identifier that is used to identify this version of the evidence variable when it is referenc...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the evidence variable. This name should be usable as an ident...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the evidence variable.
    shortTitle: Optional[str] = None  # The short title provides an alternate title for use in informal descriptive contexts where the fu...
    experimental: Optional[bool] = None  # A Boolean value to indicate that this resource is authored for testing purposes (or education/eva...
    date: Optional[str] = None  # The date  (and optionally time) when the evidence variable was last significantly changed. The da...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the evidence variable from a consumer's perspective.
    note: Optional[List[Annotation]] = field(default_factory=list)  # A human-readable string to clarify or explain concepts about the resource.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    purpose: Optional[str] = None  # Explanation of why this EvidenceVariable is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the resource and/or its contents. Copyright statements are gene...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    approvalDate: Optional[str] = None  # The date on which the resource content was approved by the publisher. Approval happens once when ...
    lastReviewDate: Optional[str] = None  # The date on which the resource content was last reviewed. Review happens periodically after appro...
    effectivePeriod: Optional[Period] = None  # The period during which the resource content was or is planned to be in active use.
    author: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual or organization primarily involved in the creation and maintenance of the content.
    editor: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization primarily responsible for internal coherence of the content.
    reviewer: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization asserted by the publisher to be primarily responsible for review of...
    endorser: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization asserted by the publisher to be responsible for officially endorsin...
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Related artifacts such as additional documentation, justification, or bibliographic references.
    actual: Optional[bool] = None  # True if the actual variable measured, false if a conceptual representation of the intended variable.
    characteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # A defining factor of the EvidenceVariable. Multiple characteristics are applied with \"and\" sema...
    handling: Optional[str] = None  # The method of handling in statistical analysis.
    category: Optional[List[BackboneElement]] = field(default_factory=list)  # A grouping for ordinal or polychotomous variables.