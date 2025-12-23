# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 StructureMap resource.

A Map of relationships between 2 structures that can be used to transform data.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, UsageContext
from typing import Any, List, Optional

@dataclass
class StructureMapStructure:
    """
    StructureMapStructure nested class.
    """

    url: Optional[str] = None  # The canonical reference to the structure.
    mode: Optional[str] = None  # How the referenced structure is used in this mapping.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    alias: Optional[str] = None  # The name used for this type in the map.
    documentation: Optional[str] = None  # Documentation that describes how the structure is used in the mapping.

@dataclass
class StructureMapConst:
    """
    StructureMapConst nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Other maps used by this map (canonical URLs).
    value: Optional[str] = None  # A FHIRPath expression that is the value of this variable.

@dataclass
class StructureMapGroup:
    """
    StructureMapGroup nested class.
    """

    name: Optional[str] = None  # A unique name for the group for the convenience of human readers.
    input: List[BackboneElement] = field(default_factory=list)  # A name assigned to an instance of data. The instance must be provided when the mapping is invoked.
    mode: Optional[str] = None  # Mode for this instance of data.
    source: List[BackboneElement] = field(default_factory=list)  # Source inputs to the mapping.
    context: Optional[str] = None  # Type or variable this rule applies to.
    value: Optional[Any] = None  # Parameter value - variable or literal.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    extends: Optional[str] = None  # Another group that this group adds rules to.
    typeMode: Optional[str] = None  # If this is the default rule set to apply for the source type or this combination of types.
    documentation: Optional[str] = None  # Additional supporting documentation that explains the purpose of the group and the types of mappi...
    type: Optional[str] = None  # Type for this instance of data.
    rule: Optional[List[BackboneElement]] = field(default_factory=list)  # Transform Rule from source to target.
    min: Optional[int] = None  # Specified minimum cardinality for the element. This is optional; if present, it acts an implicit ...
    max: Optional[str] = None  # Specified maximum cardinality for the element - a number or a \"*\". This is optional; if present...
    defaultValue: Optional[str] = None  # A value to use if there is no existing value in the source object.
    element: Optional[str] = None  # Optional field for this source.
    listMode: Optional[str] = None  # How to handle the list mode for this element.
    variable: Optional[str] = None  # Named context for field, if a field is specified.
    condition: Optional[str] = None  # FHIRPath expression  - must be true or the rule does not apply.
    check: Optional[str] = None  # FHIRPath expression  - must be true or the mapping engine throws an error instead of completing.
    logMessage: Optional[str] = None  # A FHIRPath expression which specifies a message to put in the transform log when content matching...
    target: Optional[List[BackboneElement]] = field(default_factory=list)  # Content to create because of this mapping rule.
    listRuleId: Optional[str] = None  # Internal rule reference for shared list items.
    transform: Optional[str] = None  # How the data is copied / created.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Parameters to the transform.
    dependent: Optional[List[BackboneElement]] = field(default_factory=list)  # Which other rules to apply in the context of this rule.

@dataclass
class StructureMapGroupInput:
    """
    StructureMapGroupInput nested class.
    """

    name: Optional[str] = None  # Name for this instance of data.
    mode: Optional[str] = None  # Mode for this instance of data.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[str] = None  # Type for this instance of data.
    documentation: Optional[str] = None  # Documentation for this instance of data.

@dataclass
class StructureMapGroupRule:
    """
    StructureMapGroupRule nested class.
    """

    source: List[BackboneElement] = field(default_factory=list)  # Source inputs to the mapping.
    context: Optional[str] = None  # Type or variable this rule applies to.
    value: Optional[Any] = None  # Parameter value - variable or literal.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # Name of the rule for internal references.
    min: Optional[int] = None  # Specified minimum cardinality for the element. This is optional; if present, it acts an implicit ...
    max: Optional[str] = None  # Specified maximum cardinality for the element - a number or a \"*\". This is optional; if present...
    type: Optional[str] = None  # Specified type for the element. This works as a condition on the mapping - use for polymorphic el...
    defaultValue: Optional[str] = None  # A value to use if there is no existing value in the source object.
    element: Optional[str] = None  # Optional field for this source.
    listMode: Optional[str] = None  # How to handle the list mode for this element.
    variable: Optional[str] = None  # Named context for field, if a field is specified.
    condition: Optional[str] = None  # FHIRPath expression  - must be true or the rule does not apply.
    check: Optional[str] = None  # FHIRPath expression  - must be true or the mapping engine throws an error instead of completing.
    logMessage: Optional[str] = None  # A FHIRPath expression which specifies a message to put in the transform log when content matching...
    target: Optional[List[BackboneElement]] = field(default_factory=list)  # Content to create because of this mapping rule.
    listRuleId: Optional[str] = None  # Internal rule reference for shared list items.
    transform: Optional[str] = None  # How the data is copied / created.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Parameters to the transform.
    rule: Optional[List[Any]] = field(default_factory=list)  # Rules contained in this rule.
    dependent: Optional[List[BackboneElement]] = field(default_factory=list)  # Which other rules to apply in the context of this rule.
    documentation: Optional[str] = None  # Documentation for this instance of data.

@dataclass
class StructureMapGroupRuleSource:
    """
    StructureMapGroupRuleSource nested class.
    """

    context: Optional[str] = None  # Type or variable this rule applies to.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    min: Optional[int] = None  # Specified minimum cardinality for the element. This is optional; if present, it acts an implicit ...
    max: Optional[str] = None  # Specified maximum cardinality for the element - a number or a \"*\". This is optional; if present...
    type: Optional[str] = None  # Specified type for the element. This works as a condition on the mapping - use for polymorphic el...
    defaultValue: Optional[str] = None  # A value to use if there is no existing value in the source object.
    element: Optional[str] = None  # Optional field for this source.
    listMode: Optional[str] = None  # How to handle the list mode for this element.
    variable: Optional[str] = None  # Named context for field, if a field is specified.
    condition: Optional[str] = None  # FHIRPath expression  - must be true or the rule does not apply.
    check: Optional[str] = None  # FHIRPath expression  - must be true or the mapping engine throws an error instead of completing.
    logMessage: Optional[str] = None  # A FHIRPath expression which specifies a message to put in the transform log when content matching...

@dataclass
class StructureMapGroupRuleTarget:
    """
    StructureMapGroupRuleTarget nested class.
    """

    value: Optional[Any] = None  # Parameter value - variable or literal.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    context: Optional[str] = None  # Variable this rule applies to.
    element: Optional[str] = None  # Field to create in the context.
    variable: Optional[str] = None  # Named context for field, if desired, and a field is specified.
    listMode: Optional[List[str]] = field(default_factory=list)  # If field is a list, how to manage the list.
    listRuleId: Optional[str] = None  # Internal rule reference for shared list items.
    transform: Optional[str] = None  # How the data is copied / created.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Parameters to the transform.

@dataclass
class StructureMapGroupRuleTargetParameter:
    """
    StructureMapGroupRuleTargetParameter nested class.
    """

    value: Optional[Any] = None  # Parameter value - variable or literal.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class StructureMapGroupRuleDependent:
    """
    StructureMapGroupRuleDependent nested class.
    """

    name: Optional[str] = None  # Name of a rule or group to apply.
    parameter: List[Any] = field(default_factory=list)  # Parameter to pass to the rule or group.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class StructureMap(FHIRResource):
    """
    A Map of relationships between 2 structures that can be used to transform data.
    """

    url: Optional[str] = None  # An absolute URI that is used to identify this structure map when it is referenced in a specificat...
    name: Optional[str] = None  # A natural language name identifying the structure map. This name should be usable as an identifie...
    status: Optional[str] = None  # The status of this structure map. Enables tracking the life-cycle of the content.
    group: List[BackboneElement] = field(default_factory=list)  # Organizes the mapping into managable chunks for human review/ease of maintenance.
    resourceType: str = "StructureMap"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this structure map when it is represented in other f...
    version: Optional[str] = None  # The identifier that is used to identify this version of the structure map when it is referenced i...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the structure map.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this structure map is authored for testing purposes (or educatio...
    date: Optional[str] = None  # The date  (and optionally time) when the structure map was last significantly changed. The date m...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the structure map from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the structure map is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this structure map is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the structure map and/or its contents. Copyright statements are...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    structure: Optional[List[BackboneElement]] = field(default_factory=list)  # A structure definition used by this map. The structure definition may describe instances that are...
    import_: Optional[List[str]] = field(default_factory=list)  # Other maps used by this map (canonical URLs).
    const: Optional[List[BackboneElement]] = field(default_factory=list)  # Definition of a constant value used in the map rules.