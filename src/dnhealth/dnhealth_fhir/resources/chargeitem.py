# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ChargeItem resource.

ChargeItem represents the charge for a product or service.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money, Quantity
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ChargeItemPerformer:
    """
    FHIR ChargeItem.performer complex type.
    
    Who performed charged service.
    """
    
    actor: Reference  # Who performed the service (required)
    function: Optional[CodeableConcept] = None  # What type of performance was done
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ChargeItem(DomainResource):
    """
    FHIR R4 ChargeItem resource.
    
    Represents the charge for a product or service.
    Extends DomainResource.
    """
    
    resourceType: str = "ChargeItem"
    # Required fields (must be Optional when extending DomainResource which has default fields)
    # Status
    status: Optional[str] = None  # planned | billable | not-billable | aborted | billed | entered-in-error | unknown (required in FHIR, but Optional here due to dataclass inheritance)
    # Code
    code: Optional[CodeableConcept] = None  # A code that identifies the charge, like a billing code (required in FHIR, but Optional here due to dataclass inheritance)
    # Subject
    subject: Optional[Reference] = None  # Individual service was done for/to (required in FHIR, but Optional here due to dataclass inheritance)
    # Optional fields after required fields
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business Identifier for item
    # Definition URI
    definitionUri: List[str] = field(default_factory=list)  # Defining information about the pricing of the charge
    # Definition Canonical
    definitionCanonical: List[str] = field(default_factory=list)  # Defining information about the pricing of the charge
    # Part Of
    partOf: List[Reference] = field(default_factory=list)  # Part of referenced ChargeItem
    # Context
    context: Optional[Reference] = None  # Encounter / Episode associated with event
    # Occurrence DateTime
    occurrenceDateTime: Optional[str] = None  # When the charge was applied
    # Occurrence Period
    occurrencePeriod: Optional[Period] = None  # When the charge was applied
    # Occurrence Timing
    occurrenceTiming: Optional[Any] = None  # When the charge was applied
    # Performer
    performer: List[ChargeItemPerformer] = field(default_factory=list)  # Who performed charged service
    # Performing Organization
    performingOrganization: Optional[Reference] = None  # Organization providing the charged service
    # Requesting Organization
    requestingOrganization: Optional[Reference] = None  # Organization requesting the charged service
    # Cost Center
    costCenter: Optional[Reference] = None  # Organization that has ownership of the (potential) revenue
    # Quantity
    quantity: Optional[Quantity] = None  # Quantity of which the charge item has been serviced
    # Bodysite
    bodysite: List[CodeableConcept] = field(default_factory=list)  # Anatomical location, if relevant
    # Factor Override
    factorOverride: Optional[float] = None  # Factor overriding the associated rules
    # Price Override
    priceOverride: Optional[Money] = None  # Price overriding the associated rules
    # Override Reason
    overrideReason: Optional[str] = None  # Reason for overriding the list price/factor
    # Enterer
    enterer: Optional[Reference] = None  # Individual who was entering
    # Entered Date
    enteredDate: Optional[str] = None  # Date the charge was entered
    # Reason
    reason: List[CodeableConcept] = field(default_factory=list)  # Why was the chargeitem created
    # Service
    service: List[Reference] = field(default_factory=list)  # Which rendered service is being charged
    # Product Reference
    productReference: Optional[Reference] = None  # Product charged
    # Product CodeableConcept
    productCodeableConcept: Optional[CodeableConcept] = None  # Product charged
    # Account
    account: List[Reference] = field(default_factory=list)  # Account to place this charge
    # Note
    note: List[Any] = field(default_factory=list)  # Comments made about the ChargeItem
    # Supporting Information
    supportingInformation: List[Reference] = field(default_factory=list)  # Further information supporting this charge

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


