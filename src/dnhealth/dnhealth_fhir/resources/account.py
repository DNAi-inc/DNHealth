# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Account resource.

Account represents a financial account for tracking healthcare costs and payments.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Money
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AccountCoverage:
    """
    FHIR Account.coverage complex type.
    
    The party(s) that are responsible for covering the payment of this account.
    """
    
    coverage: Reference  # The party(s) that are responsible for covering the payment (required)
    priority: Optional[int] = None  # The priority of the coverage in the context of this account
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class AccountGuarantor:
    """
    FHIR Account.guarantor complex type.
    
    Parties responsible for balancing the account if other payment options fall short.
    """
    
    party: Reference  # The entity who is responsible (required)
    onHold: Optional[bool] = None  # Credit or other hold applied
    period: Optional[Period] = None  # The timeframe during which the guarantor accepts responsibility
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Account(DomainResource):
    """
    FHIR R4 Account resource.
    
    Represents a financial account for tracking healthcare costs and payments.
    Extends DomainResource.
    """
    
    resourceType: str = "Account"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Account number
    # Status
    status: Optional[str] = None  # active | inactive | entered-in-error | on-hold | unknown
    # Type
    type: Optional[CodeableConcept] = None  # E.g., patient, expense, depreciation
    # Name
    name: Optional[str] = None  # Human-readable label
    # Subject
    subject: List[Reference] = field(default_factory=list)  # The entity that caused the expenses
    # Service Period
    servicePeriod: Optional[Period] = None  # Transaction window
    # Coverage
    coverage: List[AccountCoverage] = field(default_factory=list)  # The party(s) that are responsible for covering the payment
    # Owner
    owner: Optional[Reference] = None  # Entity managing the Account
    # Description
    description: Optional[str] = None  # Explanation of purpose/use
    # Guarantor
    guarantor: List[AccountGuarantor] = field(default_factory=list)  # Parties responsible for balancing the account
    # Part Of
    partOf: Optional[Reference] = None  # Reference to a parent Account

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


