# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Organization resource.

Complete Organization resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Address,
    ContactPoint,
    HumanName,
)


@dataclass
class OrganizationContact:
    """
    Contact for the organization.
    
    Contact for the organization for a certain purpose.
    """

    purpose: Optional[CodeableConcept] = None
    name: Optional[HumanName] = None
    telecom: List[ContactPoint] = field(default_factory=list)
    address: Optional[Address] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Organization(FHIRResource):
    """
    FHIR R4 Organization resource.

    Represents a formally or informally recognized grouping of people or
    organizations formed for the purpose of achieving some form of collective
    action.
    """

    resourceType: str = "Organization"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Active
    active: Optional[bool] = None
    # Type
    type: List[CodeableConcept] = field(default_factory=list)
    # Name
    name: Optional[str] = None
    # Alias
    alias: List[str] = field(default_factory=list)
    # Telecom
    telecom: List[ContactPoint] = field(default_factory=list)
    # Address
    address: List[Address] = field(default_factory=list)
    # Part of
    partOf: Optional[Reference] = None
    # Contact
    contact: List[OrganizationContact] = field(default_factory=list)
    # Endpoint
    endpoint: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
