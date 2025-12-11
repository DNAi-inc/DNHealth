# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Group resource.

Group represents a group of resources that share common characteristics.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class GroupCharacteristic:
    """
    FHIR Group.characteristic complex type.
    
    Trait of group members.
    """
    
    code: CodeableConcept  # Kind of characteristic (required)
    valueCodeableConcept: Optional[CodeableConcept] = None  # Value held by characteristic
    valueBoolean: Optional[bool] = None  # Value held by characteristic
    valueQuantity: Optional[Quantity] = None  # Value held by characteristic
    valueRange: Optional[Any] = None  # Value held by characteristic (Range)
    valueReference: Optional[Reference] = None  # Value held by characteristic
    exclude: bool  # Group includes or excludes (required)
    period: Optional[Period] = None  # Period over which characteristic is tested
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class GroupMember:
    """
    FHIR Group.member complex type.
    
    Identifies the resource instances that are members of the group.
    """
    
    entity: Reference  # Reference to the group member (required)
    period: Optional[Period] = None  # Period member belonged to the group
    inactive: Optional[bool] = None  # If member is no longer in group
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Group(DomainResource):
    """
    FHIR R4 Group resource.
    
    Represents a group of resources that share common characteristics.
    Extends DomainResource.
    """
    
    resourceType: str = "Group"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Unique id
    # Active
    active: Optional[bool] = None  # Whether this group record is in active use
    # Type
    type: str  # person | animal | practitioner | device | medication | substance (required)
    # Actual
    actual: bool  # Descriptive or actual (required)
    # Code
    code: Optional[CodeableConcept] = None  # Kind of Group members
    # Name
    name: Optional[str] = None  # Label for Group
    # Quantity
    quantity: Optional[int] = None  # Number of members
    # Managing Entity
    managingEntity: Optional[Reference] = None  # Entity that is the custodian of the Group's definition
    # Characteristic
    characteristic: List[GroupCharacteristic] = field(default_factory=list)  # Trait of group members
    # Member
    member: List[GroupMember] = field(default_factory=list)  # Identifies the resource instances that are members of the group

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


