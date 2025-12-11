# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 OrganizationAffiliation resource.

Complete OrganizationAffiliation resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    ContactPoint,
    Address,
    Period,
)


@dataclass
class OrganizationAffiliation(FHIRResource):
    """
    FHIR R4 OrganizationAffiliation resource.

    Represents a relationship between two or more organizations, including
    the role each organization plays in the relationship.
    """

    resourceType: str = "OrganizationAffiliation"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Active
    active: Optional[bool] = None
    # Period
    period: Optional[Period] = None
    # Organization
    organization: Optional[Reference] = None
    # Participating organization
    participatingOrganization: Optional[Reference] = None
    # Network
    network: List[Reference] = field(default_factory=list)
    # Code
    code: List[CodeableConcept] = field(default_factory=list)
    # Specialty
    specialty: List[CodeableConcept] = field(default_factory=list)
    # Location
    location: List[Reference] = field(default_factory=list)
    # Healthcare service
    healthcareService: List[Reference] = field(default_factory=list)
    # Telecom
    telecom: List[ContactPoint] = field(default_factory=list)
    # Endpoint
    endpoint: List[Reference] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
