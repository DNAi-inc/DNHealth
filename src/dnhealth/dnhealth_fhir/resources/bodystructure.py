# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 BodyStructure resource.

BodyStructure represents a specific structure of the human body.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Attachment
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class BodyStructure(DomainResource):
    """
    FHIR R4 BodyStructure resource.
    
    Represents a specific structure of the human body.
    Extends DomainResource.
    """
    
    resourceType: str = "BodyStructure"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Bodystructure identifier
    # Active
    active: Optional[bool] = None  # Whether this record is in active use
    # Morphology
    morphology: Optional[CodeableConcept] = None  # Kind of structure
    # Location
    location: Optional[CodeableConcept] = None  # Body site
    # Location Qualifier
    locationQualifier: List[CodeableConcept] = field(default_factory=list)  # Body site modifier
    # Description
    description: Optional[str] = None  # Text description
    # Image
    image: List[Attachment] = field(default_factory=list)  # Attached images
    # Patient
    patient: Optional[Reference] = None  # Who this is about (required)
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.patient is None:
            raise ValueError("patient is required for BodyStructure")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
