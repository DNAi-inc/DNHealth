# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 StructureMap resource.

StructureMap defines how to transform one structure into another.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext


@dataclass
class StructureMapStructure:
    """
    FHIR StructureMap.structure complex type.
    
    Structure Definition used by this map.
    """
    
    url: str  # Canonical URL (required)
    mode: str  # source | queried | target | produced (required)
    alias: Optional[str] = None  # Name for type in this map
    documentation: Optional[str] = None  # Documentation on use of structure
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class StructureMapGroup:
    """
    FHIR StructureMap.group complex type.
    
    Named sections for reader convenience.
    """
    
    name: Optional[str] = None  # Human-readable label
    extends: Optional[str] = None  # Another group that this group adds rules to
    typeMode: Optional[str] = None  # types | type-and-types
    documentation: Optional[str] = None  # Additional description/explanation
    input: List[Dict[str, Any]] = field(default_factory=list)  # Named instance provided as input
    rule: List[Dict[str, Any]] = field(default_factory=list)  # Transform Rule from source to target
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class StructureMap(MetadataResource):
    """
    FHIR R4 StructureMap resource.
    
    Defines how to transform one structure into another.
    Extends MetadataResource.
    """
    
    resourceType: str = "StructureMap"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Any] = field(default_factory=list)  # Additional identifiers
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this structure map (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this structure map
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Purpose
    purpose: Optional[str] = None  # Why this structure map is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Structure
    structure: List[StructureMapStructure] = field(default_factory=list)  # Structure Definition used by this map
    # Import
    import_: List[str] = field(default_factory=list)  # Other maps used by this map (import is Python keyword)
    # Group
    group: List[StructureMapGroup] = field(default_factory=list)  # Named sections for reader convenience


def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

