# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CatalogEntry resource.

CatalogEntry represents an entry in a catalog.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class CatalogEntryRelatedEntry:
    """
    FHIR CatalogEntry.relatedEntry complex type.
    
    Used for example, to point to a substance, or to a device used to administer a medication.
    """
    
    relationtype: Optional[str] = None  # triggers | is-replaced-by (required)
    item: Optional[Reference] = None  # The reference to the related item (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        if self.relationtype is None:
            raise ValueError("relationtype is required for CatalogEntryRelatedEntry")
        if self.item is None:
            raise ValueError("item is required for CatalogEntryRelatedEntry")



        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
@dataclass
class CatalogEntry(DomainResource):
    """
    FHIR R4 CatalogEntry resource.
    
    Represents an entry in a catalog.
    Extends DomainResource.
    """
    
    resourceType: str = "CatalogEntry"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Unique identifier of the catalog item
    # Type
    type: Optional[CodeableConcept] = None  # The type of item - medication, device, service, etc.
    # Orderable
    orderable: Optional[bool] = None  # Whether the entry represents an orderable item (required)
    # Referenced Item
    referencedItem: Optional[Reference] = None  # The item that is being defined (required)
    # Additional Identifier
    additionalIdentifier: List[Identifier] = field(default_factory=list)  # Any additional identifier(s) for the catalog item
    # Classification
    classification: List[CodeableConcept] = field(default_factory=list)  # Classification of the catalog entry
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown
    # Validity Period
    validityPeriod: Optional[Period] = None  # The time period in which this catalog entry is expected to be active
    # Valid To
    validTo: Optional[str] = None  # The date until which this catalog entry is expected to be active
    # Last Updated
    lastUpdated: Optional[str] = None  # When was this catalog last updated
    # Additional Characteristic
    additionalCharacteristic: List[CodeableConcept] = field(default_factory=list)  # Additional characteristics of the catalog entry
    # Additional Classification
    additionalClassification: List[CodeableConcept] = field(default_factory=list)  # Additional classification of the catalog entry
    # Related Entry
    relatedEntry: List[CatalogEntryRelatedEntry] = field(default_factory=list)  # Used for example, to point to a substance, or to a device used to administer a medication
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.orderable is None:
            raise ValueError("orderable is required for CatalogEntry")
        if self.referencedItem is None:
            raise ValueError("referencedItem is required for CatalogEntry")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
