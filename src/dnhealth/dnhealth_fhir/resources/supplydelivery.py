# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SupplyDelivery resource.

SupplyDelivery represents the delivery of a supply item.
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
class SupplyDeliverySuppliedItem:
    """
    FHIR SupplyDelivery.suppliedItem complex type.
    
    The item that is being delivered or has been supplied.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    quantity: Optional[Any] = None  # Amount dispensed (Quantity)
    itemCodeableConcept: Optional[CodeableConcept] = None  # Code for the item supplied
    itemReference: Optional[Reference] = None  # Code for the item supplied


@dataclass
class SupplyDelivery(DomainResource):
    """
    FHIR R4 SupplyDelivery resource.
    
    Represents the delivery of a supply item.
    Extends DomainResource.
    """
    
    resourceType: str = "SupplyDelivery"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External identifier
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # Fulfills plan, proposal or order
    # Part Of
    partOf: List[Reference] = field(default_factory=list)  # Part of referenced event
    # Status
    status: Optional[str] = None  # in-progress | completed | abandoned | entered-in-error
    # Patient
    patient: Optional[Reference] = None  # Patient for whom the item is supplied
    # Type
    type: Optional[CodeableConcept] = None  # Category of dispense event
    # Supplied Item
    suppliedItem: Optional[SupplyDeliverySuppliedItem] = None  # The item that is being delivered or has been supplied
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # When event occurred
    # Occurrence Period
    occurrencePeriod: Optional[Period] = None  # When event occurred
    # Occurrence Timing
    occurrenceTiming: Optional[Timing] = None  # When event occurred
    # Supplier
    supplier: Optional[Reference] = None  # Dispenser
    # Destination
    destination: Optional[Reference] = None  # Where the Supply was sent
    # Receiver
    receiver: List[Reference] = field(default_factory=list)  # Who collected the Supply
    # Note
    note: List[Annotation] = field(default_factory=list)  # Additional notes

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

