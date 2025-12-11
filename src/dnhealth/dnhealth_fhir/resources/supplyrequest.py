# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SupplyRequest resource.

SupplyRequest represents a request for a supply item.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Timing,
    Annotation,
)


logger = logging.getLogger(__name__)


@dataclass
class SupplyRequestParameter:
    """
    FHIR SupplyRequest.parameter complex type.
    
    Ordered item details.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    code: Optional[CodeableConcept] = None  # Item detail
    valueCodeableConcept: Optional[CodeableConcept] = None  # Value of detail
    valueQuantity: Optional[Any] = None  # Value of detail (Quantity)
    valueRange: Optional[Any] = None  # Value of detail (Range)
    valueBoolean: Optional[bool] = None  # Value of detail


@dataclass
class SupplyRequest(DomainResource):
    """
    FHIR R4 SupplyRequest resource.
    
    Represents a request for a supply item.
    Extends DomainResource.
    """
    
    resourceType: str = "SupplyRequest"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier
    # Status
    status: Optional[str] = None  # draft | active | suspended | cancelled | completed | entered-in-error | unknown
    # Category
    category: Optional[CodeableConcept] = None  # Category of supply
    # Priority
    priority: Optional[str] = None  # routine | urgent | asap | stat
    # Item CodeableConcept
    itemCodeableConcept: Optional[CodeableConcept] = None  # The requested item
    # Item Reference
    itemReference: Optional[Reference] = None  # The requested item
    # Quantity
    quantity: Any  # The requested amount (Quantity, required)
    # Parameter
    parameter: List[SupplyRequestParameter] = field(default_factory=list)  # Ordered item details
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # When the request should be fulfilled
    # Occurrence Period
    occurrencePeriod: Optional[Period] = None  # When the request should be fulfilled
    # Occurrence Timing
    occurrenceTiming: Optional[Timing] = None  # When the request should be fulfilled
    # Authored On
    authoredOn: Optional[str] = None  # When the request was made
    # Requester
    requester: Optional[Reference] = None  # Individual making the request
    # Supplier
    supplier: List[Reference] = field(default_factory=list)  # Who is intended to fulfill the request
    # Reason Code
    reasonCode: List[CodeableConcept] = field(default_factory=list)  # The reason the supply item was requested
    # Reason Reference
    reasonReference: List[Reference] = field(default_factory=list)  # The reason the supply item was requested
    # Deliver From
    deliverFrom: Optional[Reference] = None  # The origin of the supply
    # Deliver To
    deliverTo: Optional[Reference] = None  # The destination of the supply
    # Note
    note: List[Annotation] = field(default_factory=list)  # Additional notes

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

