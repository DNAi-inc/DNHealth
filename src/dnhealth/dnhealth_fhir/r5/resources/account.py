# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Account resource.

A financial tool for tracking value accrued for a particular purpose.  In the healthcare field, used to track charges for a patient, cost centers, etc.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Money, Period, Reference
from typing import Any, List, Optional

@dataclass
class AccountCoverage:
    """
    AccountCoverage nested class.
    """

    coverage: Optional[Reference] = None  # The party(s) that contribute to payment (or part of) of the charges applied to this account (incl...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    priority: Optional[int] = None  # The priority of the coverage in the context of this account.

@dataclass
class AccountGuarantor:
    """
    AccountGuarantor nested class.
    """

    party: Optional[Reference] = None  # The entity who is responsible.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    onHold: Optional[bool] = None  # A guarantor may be placed on credit hold or otherwise have their role temporarily suspended.
    period: Optional[Period] = None  # The timeframe during which the guarantor accepts responsibility for the account.

@dataclass
class AccountDiagnosis:
    """
    AccountDiagnosis nested class.
    """

    condition: Optional[Any] = None  # The diagnosis relevant to the account.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    sequence: Optional[int] = None  # Ranking of the diagnosis (for each type).
    dateOfDiagnosis: Optional[str] = None  # Ranking of the diagnosis (for each type).
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Type that this diagnosis has relevant to the account (e.g. admission, billing, discharge …).
    onAdmission: Optional[bool] = None  # Was the Diagnosis present on Admission in the related Encounter.
    packageCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # The package code can be used to group diagnoses that may be priced or delivered as a single produ...

@dataclass
class AccountProcedure:
    """
    AccountProcedure nested class.
    """

    code: Optional[Any] = None  # The procedure relevant to the account.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    sequence: Optional[int] = None  # Ranking of the procedure (for each type).
    dateOfService: Optional[str] = None  # Date of the procedure when using a coded procedure. If using a reference to a procedure, then the...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # How this procedure value should be used in charging the account.
    packageCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # The package code can be used to group procedures that may be priced or delivered as a single prod...
    device: Optional[List[Reference]] = field(default_factory=list)  # Any devices that were associated with the procedure relevant to the account.

@dataclass
class AccountRelatedAccount:
    """
    AccountRelatedAccount nested class.
    """

    account: Optional[Reference] = None  # Reference to an associated Account.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    relationship: Optional[CodeableConcept] = None  # Relationship of the associated Account.

@dataclass
class AccountBalance:
    """
    AccountBalance nested class.
    """

    amount: Optional[Money] = None  # The actual balance value calculated for the age defined in the term property.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    aggregate: Optional[CodeableConcept] = None  # Who is expected to pay this part of the balance.
    term: Optional[CodeableConcept] = None  # The term of the account balances - The balance value is the amount that was outstanding for this ...
    estimate: Optional[bool] = None  # The amount is only an estimated value - this is likely common for `current` term balances, but no...


@dataclass
class Account(FHIRResource):
    """
    A financial tool for tracking value accrued for a particular purpose.  In the healthcare field, used to track charges for a patient, cost centers, etc.
    """

    status: Optional[str] = None  # Indicates whether the account is presently used/usable or not.
    resourceType: str = "Account"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique identifier used to reference the account.  Might or might not be intended for human use (e...
    billingStatus: Optional[CodeableConcept] = None  # The BillingStatus tracks the lifecycle of the account through the billing process. It indicates h...
    type: Optional[CodeableConcept] = None  # Categorizes the account for reporting and searching purposes.
    name: Optional[str] = None  # Name used for the account when displaying it to humans in reports, etc.
    subject: Optional[List[Reference]] = field(default_factory=list)  # Identifies the entity which incurs the expenses. While the immediate recipients of services or go...
    servicePeriod: Optional[Period] = None  # The date range of services associated with this account.
    coverage: Optional[List[BackboneElement]] = field(default_factory=list)  # The party(s) that are responsible for covering the payment of this account, and what order should...
    owner: Optional[Reference] = None  # Indicates the service area, hospital, department, etc. with responsibility for managing the Account.
    description: Optional[str] = None  # Provides additional information about what the account tracks and how it is used.
    guarantor: Optional[List[BackboneElement]] = field(default_factory=list)  # The parties responsible for balancing the account if other payment options fall short.
    diagnosis: Optional[List[BackboneElement]] = field(default_factory=list)  # When using an account for billing a specific Encounter the set of diagnoses that are relevant for...
    procedure: Optional[List[BackboneElement]] = field(default_factory=list)  # When using an account for billing a specific Encounter the set of procedures that are relevant fo...
    relatedAccount: Optional[List[BackboneElement]] = field(default_factory=list)  # Other associated accounts related to this account.
    currency: Optional[CodeableConcept] = None  # The default currency for the account.
    balance: Optional[List[BackboneElement]] = field(default_factory=list)  # The calculated account balances - these are calculated and processed by the finance system.


    calculatedAt: Optional[str] = None  # Time the balance amount was calculated.