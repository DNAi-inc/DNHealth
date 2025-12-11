# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CompartmentDefinition resource.

CompartmentDefinition defines how resources are organized into compartments.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class CompartmentDefinitionResource:
    """
    FHIR CompartmentDefinition.resource complex type.
    
    Information about how a resource is related to the compartment.
    """
    
    code: str  # Name of resource type (required)
    param: List[str] = field(default_factory=list)  # Search parameter name, or chained parameters
    documentation: Optional[str] = None  # Additional documentation about the resource
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CompartmentDefinition(CanonicalResource):
    """
    FHIR R4 CompartmentDefinition resource.
    
    Defines how resources are organized into compartments.
    Extends CanonicalResource.
    """
    
    resourceType: str = "CompartmentDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this compartment definition (required, validated in __post_init__)
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
    # Purpose
    purpose: Optional[str] = None  # Why this compartment definition is defined (inherited from CanonicalResource)
    # Code
    code: Optional[str] = None  # Patient | Encounter | RelatedPerson | Practitioner | Device (required, validated in __post_init__)
    # Search
    search: Optional[bool] = None  # Whether the search syntax is supported (required, validated in __post_init__)
    # Resource
    resource: List[CompartmentDefinitionResource] = field(default_factory=list)  # How a resource is related to the compartment
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.name is None:
            raise ValueError("CompartmentDefinition.name is required but was not provided")
        if self.code is None:
            raise ValueError("CompartmentDefinition.code is required but was not provided")
        if self.search is None:
            raise ValueError("CompartmentDefinition.search is required but was not provided")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
