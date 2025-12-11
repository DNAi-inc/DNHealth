# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 NamingSystem resource.

Complete NamingSystem resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    ContactDetail,
    UsageContext,
    Period,
)


@dataclass
class NamingSystemUniqueId:
    """
    Indicates how the system may be identified when referenced in electronic exchange.
    """

    type: str  # oid | uuid | uri | other (required)
    value: str  # The unique identifier (required)
    preferred: Optional[bool] = None
    comment: Optional[str] = None
    period: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class NamingSystem(MetadataResource):
    """
    FHIR R4 NamingSystem resource.

    A curated namespace that issues unique symbols within that namespace for the
    identification of concepts, people, devices, etc.
    """

    resourceType: str = "NamingSystem"
    # Name
    name: str  # Human-readable name (required)
    # Status
    status: str  # draft | active | retired | unknown (required, inherited from MetadataResource)
    # Kind
    kind: str  # codesystem | identifier | root (required)
    # Date
    date: str  # Date last changed (required, ISO 8601 dateTime, inherited from MetadataResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from MetadataResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from MetadataResource)
    # Responsible
    responsible: Optional[str] = None
    # Type
    type: Optional[CodeableConcept] = None
    # Description
    description: Optional[str] = None  # Natural language description (inherited from MetadataResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from MetadataResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from MetadataResource)
    # Usage
    usage: Optional[str] = None
    # Unique Id
    uniqueId: List[NamingSystemUniqueId] = field(default_factory=list)  # Unique identifiers used for system

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
