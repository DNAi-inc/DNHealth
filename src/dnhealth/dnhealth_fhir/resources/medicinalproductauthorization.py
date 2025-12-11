# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductAuthorization resource.

Complete MedicinalProductAuthorization resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
)


@dataclass
class MedicinalProductAuthorizationJurisdictionalAuthorization:
    """
    Authorization in areas within a country.
    """

    identifier: List[Identifier] = field(default_factory=list)
    country: Optional[CodeableConcept] = None
    jurisdiction: List[CodeableConcept] = field(default_factory=list)
    legalStatusOfSupply: Optional[CodeableConcept] = None
    validityPeriod: Optional[Period] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductAuthorizationProcedure:
    """
    The regulatory procedure for granting or amending a marketing authorization.
    """

    identifier: Optional[Identifier] = None
    type: CodeableConcept  # Type of procedure (required)
    datePeriod: Optional[Period] = None
    dateDateTime: Optional[str] = None  # ISO 8601 dateTime
    application: List["MedicinalProductAuthorizationProcedure"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductAuthorization(FHIRResource):
    """
    FHIR R4 MedicinalProductAuthorization resource.

    The regulatory authorization of a medicinal product.
    """

    resourceType: str = "MedicinalProductAuthorization"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Subject
    subject: Optional[Reference] = None
    # Country
    country: List[CodeableConcept] = field(default_factory=list)
    # Jurisdictional Authorization
    jurisdictionalAuthorization: List[MedicinalProductAuthorizationJurisdictionalAuthorization] = field(default_factory=list)
    # Legal Status of Supply
    legalStatusOfSupply: Optional[CodeableConcept] = None
    # Status
    status: Optional[CodeableConcept] = None
    # Status Date
    statusDate: Optional[str] = None  # ISO 8601 dateTime
    # Restore Date
    restoreDate: Optional[str] = None  # ISO 8601 dateTime
    # Validity Period
    validityPeriod: Optional[Period] = None
    # Data Exclusivity Period
    dataExclusivityPeriod: Optional[Period] = None
    # Date of First Authorization
    dateOfFirstAuthorization: Optional[str] = None  # ISO 8601 dateTime
    # International Birth Date
    internationalBirthDate: Optional[str] = None  # ISO 8601 dateTime
    # Legal Basis
    legalBasis: Optional[CodeableConcept] = None
    # Jurisdictional Procedure
    jurisdictionalProcedure: List[CodeableConcept] = field(default_factory=list)
    # Procedure
    procedure: Optional[MedicinalProductAuthorizationProcedure] = None

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
