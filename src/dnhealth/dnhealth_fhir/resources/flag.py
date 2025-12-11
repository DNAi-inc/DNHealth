# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Flag resource.

Flag represents a flag or alert for a patient.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class Flag(DomainResource):
    """
    FHIR R4 Flag resource.
    
    Represents a flag or alert for a patient.
    Extends DomainResource.
    """
    
    resourceType: str = "Flag"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier
    # Status
    status: Optional[str] = None  # active | inactive | entered-in-error (required)
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Clinical, administrative, etc.
    # Code
    code: Optional[CodeableConcept] = None  # Coded or textual message to display to user (required)
    # Subject
    subject: Optional[Reference] = None  # Who/What is flag about? (required)
    # Period
    period: Optional[Period] = None  # Time period when flag is active
    # Encounter
    encounter: Optional[Reference] = None  # Alert relevant during encounter
    # Author
    author: Optional[Reference] = None  # Flag creator
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.status is None:
            raise ValueError("status is required for Flag")
        if self.code is None:
            raise ValueError("code is required for Flag")
        if self.subject is None:
            raise ValueError("subject is required for Flag")
