# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Person resource.

Complete Person resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    HumanName,
    ContactPoint,
    Address,
    Attachment,
    Period,
)


@dataclass
class PersonLink:
    """
    Link to a resource that concerns the same actual person.
    """

    target: Reference  # The resource to which this actual person is associated (required)
    assurance: Optional[str] = None  # level1 | level2 | level3 | level4
    extension: List[Extension] = field(default_factory=list)


@dataclass
class Person(FHIRResource):
    """
    FHIR R4 Person resource.

    Represents demographics and administrative information about a person
    independent of a specific health-related context.
    """

    resourceType: str = "Person"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Name
    name: List[HumanName] = field(default_factory=list)
    # Telecom
    telecom: List[ContactPoint] = field(default_factory=list)
    # Gender
    gender: Optional[str] = None  # male | female | other | unknown
    # Birth date
    birthDate: Optional[str] = None  # YYYY-MM-DD
    # Address
    address: List[Address] = field(default_factory=list)
    # Photo
    photo: Optional[Attachment] = None
    # Managing organization
    managingOrganization: Optional[Reference] = None
    # Active
    active: Optional[bool] = None
    # Link
    link: List[PersonLink] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
