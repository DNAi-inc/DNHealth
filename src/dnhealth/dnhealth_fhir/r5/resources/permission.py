# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Permission resource.

Permission resource holds access rules for a given data and context.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, Expression, Extension, Period, Reference
from typing import List, Optional

@dataclass
class PermissionJustification:
    """
    PermissionJustification nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    basis: Optional[List[CodeableConcept]] = field(default_factory=list)  # This would be a codeableconcept, or a coding, which can be constrained to , for example, the 6 gr...
    evidence: Optional[List[Reference]] = field(default_factory=list)  # Justifing rational.

@dataclass
class PermissionRule:
    """
    PermissionRule nested class.
    """

    meaning: Optional[str] = None  # How the resource reference is interpreted when testing consent restrictions.
    reference: Optional[Reference] = None  # A reference to a specific resource that defines which resources are covered by this consent.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[str] = None  # deny | permit.
    data: Optional[List[BackboneElement]] = field(default_factory=list)  # A description or definition of which activities are allowed to be done on the data.
    resource: Optional[List[BackboneElement]] = field(default_factory=list)  # Explicit FHIR Resource references.
    security: Optional[List[Coding]] = field(default_factory=list)  # The data in scope are those with the given codes present in that data .meta.security element.
    period: Optional[List[Period]] = field(default_factory=list)  # Clinical or Operational Relevant period of time that bounds the data controlled by this rule.
    expression: Optional[Expression] = None  # Used when other data selection elements are insufficient.
    activity: Optional[List[BackboneElement]] = field(default_factory=list)  # A description or definition of which activities are allowed to be done on the data.
    actor: Optional[List[Reference]] = field(default_factory=list)  # The actor(s) authorized for the defined activity.
    action: Optional[List[CodeableConcept]] = field(default_factory=list)  # Actions controlled by this Rule.
    purpose: Optional[List[CodeableConcept]] = field(default_factory=list)  # The purpose for which the permission is given.
    limit: Optional[List[CodeableConcept]] = field(default_factory=list)  # What limits apply to the use of the data.

@dataclass
class PermissionRuleData:
    """
    PermissionRuleData nested class.
    """

    meaning: Optional[str] = None  # How the resource reference is interpreted when testing consent restrictions.
    reference: Optional[Reference] = None  # A reference to a specific resource that defines which resources are covered by this consent.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    resource: Optional[List[BackboneElement]] = field(default_factory=list)  # Explicit FHIR Resource references.
    security: Optional[List[Coding]] = field(default_factory=list)  # The data in scope are those with the given codes present in that data .meta.security element.
    period: Optional[List[Period]] = field(default_factory=list)  # Clinical or Operational Relevant period of time that bounds the data controlled by this rule.
    expression: Optional[Expression] = None  # Used when other data selection elements are insufficient.

@dataclass
class PermissionRuleDataResource:
    """
    PermissionRuleDataResource nested class.
    """

    meaning: Optional[str] = None  # How the resource reference is interpreted when testing consent restrictions.
    reference: Optional[Reference] = None  # A reference to a specific resource that defines which resources are covered by this consent.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class PermissionRuleActivity:
    """
    PermissionRuleActivity nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    actor: Optional[List[Reference]] = field(default_factory=list)  # The actor(s) authorized for the defined activity.
    action: Optional[List[CodeableConcept]] = field(default_factory=list)  # Actions controlled by this Rule.
    purpose: Optional[List[CodeableConcept]] = field(default_factory=list)  # The purpose for which the permission is given.


@dataclass
class Permission(FHIRResource):
    """
    Permission resource holds access rules for a given data and context.
    """

    status: Optional[str] = None  # Status.
    combining: Optional[str] = None  # Defines a procedure for arriving at an access decision given the set of rules.
    resourceType: str = "Permission"
    asserter: Optional[Reference] = None  # The person or entity that asserts the permission.
    date: Optional[List[str]] = field(default_factory=list)  # The date that permission was asserted.
    validity: Optional[Period] = None  # The period in which the permission is active.
    justification: Optional[BackboneElement] = None  # The asserted justification for using the data.
    rule: Optional[List[BackboneElement]] = field(default_factory=list)  # A set of rules.