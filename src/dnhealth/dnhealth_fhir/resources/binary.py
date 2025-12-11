# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Binary resource.

Binary resource is used to represent binary content (images, documents, etc.).
"""

from dataclasses import dataclass, field
from typing import Optional, Any

from dnhealth.dnhealth_fhir.resources.base import Resource
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class Binary(Resource):
    """
    FHIR R4 Binary resource.
    
    Represents binary content such as images, documents, or other non-XML/non-JSON content.
    Extends Resource (not DomainResource, as per FHIR spec).
    """
    
    resourceType: str = "Binary"
    contentType: str = ""  # MIME type of the binary content (required)
    securityContext: Optional[Any] = None  # Reference to a resource that provides context
    data: Optional[str] = None  # Base64-encoded binary content
    
    def __post_init__(self):
        """Validate Binary after initialization."""
        super().__post_init__()
        if not self.contentType:
            raise ValueError("Binary contentType is required")


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
