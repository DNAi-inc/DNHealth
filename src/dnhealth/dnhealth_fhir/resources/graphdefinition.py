# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 GraphDefinition resource.

GraphDefinition defines a graph of resources.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class GraphDefinitionLinkTarget:
    """
    FHIR GraphDefinition.link.target complex type.
    
    Potential target for the link.
    """
    
    type: str  # Type of resource (required)
    params: Optional[str] = None  # Criteria for reverse lookup
    profile: Optional[str] = None  # Profile for the target resource
    compartment: List[Dict[str, Any]] = field(default_factory=list)  # Compartment rules
    link: List["GraphDefinitionLinkTarget"] = field(default_factory=list)  # Nested links
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class GraphDefinitionLink:
    """
    FHIR GraphDefinition.link complex type.
    
    Links this graph makes rules about.
    """
    
    path: Optional[str] = None  # Path in the resource that contains the link
    sliceName: Optional[str] = None  # Which slice (if profiled)
    min: Optional[int] = None  # Minimum occurrences for this link
    max: Optional[str] = None  # Maximum occurrences for this link
    description: Optional[str] = None  # Why this link is specified
    target: List[GraphDefinitionLinkTarget] = field(default_factory=list)  # Potential targets
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class GraphDefinition(CanonicalResource):
    """
    FHIR R4 GraphDefinition resource.
    
    Defines a graph of resources.
    Extends CanonicalResource.
    """
    
    resourceType: str = "GraphDefinition"
    # Start
    start: Optional[str] = None  # Starting node (required, validated in __post_init__)
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this graph definition
    # Title
    title: Optional[str] = None  # Title for this graph definition
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
    purpose: Optional[str] = None  # Why this graph definition is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Profile
    profile: Optional[str] = None  # Profile on base resource
    # Link
    link: List[GraphDefinitionLink] = field(default_factory=list)  # Links this graph makes rules about
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.start is None:
            raise ValueError("GraphDefinition.start is required but was not provided")
