# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Group resource.

Enforces a descriptive group that can be used in definitional resources
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Range, Reference
from typing import Any, List, Optional

@dataclass
class GroupCharacteristic:
    """
    GroupCharacteristic nested class.
    """

    code: Optional[CodeableConcept] = None  # A code that identifies the kind of trait being asserted.
    value: Optional[Any] = None  # The value of the trait that holds (or does not hold - see 'exclude') for members of the group.
    exclude: Optional[bool] = None  # If true, indicates the characteristic is one that is NOT held by members of the group.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    period: Optional[Period] = None  # The period over which the characteristic is tested; e.g. the patient had an operation during the ...

@dataclass
class GroupMember:
    """
    GroupMember nested class.
    """

    entity: Optional[Reference] = None  # A reference to the entity that is a member of the group. Must be consistent with Group.type. If t...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    period: Optional[Period] = None  # The period that the member was in the group, if known.
    inactive: Optional[bool] = None  # A flag to indicate that the member is no longer in the group, but previously may have been a member.


@dataclass
class Group(FHIRResource):
    """
    Enforces a descriptive group that can be used in definitional resources
    """

    type: Optional[str] = None  # Identifies the broad classification of the kind of resources the group includes.
    membership: Optional[str] = None  # Basis for membership in the Group:  * 'definitional': The Group.characteristics specified are bot...
    characteristic: List[BackboneElement] = field(default_factory=list)  # Identifies traits whose presence r absence is shared by members of the group.
    resourceType: str = "Group"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this participant by one of the applications involved.  These ide...
    active: Optional[bool] = None  # Indicates whether the record for the group is available for use or is merely being retained for h...
    code: Optional[CodeableConcept] = None  # Provides a specific type of resource the group includes; e.g. \"cow\", \"syringe\", etc.
    name: Optional[str] = None  # A label assigned to the group for human identification and communication.
    description: Optional[str] = None  # Explanation of what the group represents and how it is intended to be used.
    quantity: Optional[int] = None  # A count of the number of resource instances that are part of the group.
    managingEntity: Optional[Reference] = None  # Entity responsible for defining and maintaining Group characteristics and/or registered members.
    member: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies the resource instances that are members of the group.