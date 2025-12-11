# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Basic resource.

Basic is used for handling resources not covered by any of the other resource types.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class Basic(DomainResource):
    """
    FHIR R4 Basic resource.
    
    Basic is used for handling resources not covered by any of the other resource types.
    Extends DomainResource.
    """
    
    resourceType: str = "Basic"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Code
    code: Optional[CodeableConcept] = None  # Kind of Resource the basic resource represents (required)
    # Subject
    subject: Optional[Reference] = None  # Identifies the focus of this resource
    # Created
    created: Optional[str] = None  # When created
    # Author
    author: Optional[Reference] = None  # Who created
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.code is None:
            raise ValueError("code is required for Basic")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
