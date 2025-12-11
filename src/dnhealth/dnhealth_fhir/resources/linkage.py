# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Linkage resource.

Linkage represents links between resources that have the same "logical" identity.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Reference
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class LinkageItem:
    """
    FHIR Linkage.item complex type.
    
    Identifies which record considered as the reference to the same real-world occurrence.
    """
    
    type: str  # source | alternate | historical (required)
    resource: Reference  # Resource being linked (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Linkage(DomainResource):
    """
    FHIR R4 Linkage resource.
    
    Represents links between resources that have the same "logical" identity.
    Extends DomainResource.
    """
    
    resourceType: str = "Linkage"
    # Active
    active: Optional[bool] = None  # Whether this linkage assertion is active or not
    # Author
    author: Optional[Reference] = None  # Who is responsible for linkages
    # Item
    item: List[LinkageItem] = field(default_factory=list)  # Identifies which record considered as the reference to the same real-world occurrence (required)

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()



