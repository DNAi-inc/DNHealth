# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 List resource.

List represents a list of items.
"""

from dataclasses import dataclass, field
from typing import List as ListType, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ListEntry:
    """
    FHIR List.entry complex type.
    
    Entries in the list.
    """
    
    flag: Optional[CodeableConcept] = None  # Status/Workflow information about this item
    deleted: Optional[bool] = None  # If this item is actually marked as deleted
    date: Optional[str] = None  # When item added to list
    item: Reference  # Actual item (required)
    extension: ListType[Extension] = field(default_factory=list)
    modifierExtension: ListType[Extension] = field(default_factory=list)


@dataclass
class ListResource(DomainResource):
    """
    FHIR R4 List resource.
    
    Represents a list of items.
    Extends DomainResource.
    """
    
    resourceType: str = "List"
    # Identifier
    identifier: ListType[Identifier] = field(default_factory=list)  # Business identifier
    # Status
    status: str  # current | retired | entered-in-error (required)
    # Mode
    mode: str  # working | snapshot | changes (required)
    # Title
    title: Optional[str] = None  # Descriptive name for the list
    # Code
    code: Optional[CodeableConcept] = None  # What the purpose of this list is
    # Subject
    subject: Optional[Reference] = None  # If all resources have the same subject
    # Encounter
    encounter: Optional[Reference] = None  # Context in which list created
    # Date
    date: Optional[str] = None  # When the list was prepared
    # Source
    source: Optional[Reference] = None  # Who and/or what defined the list contents
    # Ordered By
    orderedBy: Optional[CodeableConcept] = None  # What order the list has
    # Note
    note: ListType[Annotation] = field(default_factory=list)  # Comments about the list
    # Entry
    entry: ListType[ListEntry] = field(default_factory=list)  # Entries in the list
    # Empty Reason
    emptyReason: Optional[CodeableConcept] = None  # Why list is empty

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


