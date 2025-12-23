# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProduct resource.

Complete MedicinalProduct resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
)


@dataclass
class MedicinalProductName:
    """
    The product's name, including full name and possibly coded parts.
    """

    productName: str  # The full product name (required)
    namePart: List["MedicinalProductNamePart"] = field(default_factory=list)
    countryLanguage: List["MedicinalProductCountryLanguage"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductNamePart:
    """
    Coding words or phrases of the name.
    """

    part: str  # A fragment of a product name (required)
    type: CodeableConcept  # Idenifying type for this part of the name (required)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductCountryLanguage:
    """
    Country where the name applies.
    """

    # Note: country is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce country is provided.
    country: Optional[CodeableConcept] = None  # Country code for where this name applies (required)
    jurisdiction: Optional[CodeableConcept] = None
    # Note: language is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce language is provided.
    language: Optional[CodeableConcept] = None  # Language code for this name (required)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductManufacturingBusinessOperation:
    """
    An operation applied to the product, for manufacturing or adminsitrative purpose.
    """

    operationType: Optional[CodeableConcept] = None
    authorisationReferenceNumber: Optional[Identifier] = None
    effectiveDate: Optional[Period] = None
    confidentialityIndicator: Optional[CodeableConcept] = None
    manufacturer: List[Reference] = field(default_factory=list)
    regulator: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MarketingStatus:
    """
    The marketing status describes the date when a medicinal product is actually put on the market
    or the date as of which it is no longer available.
    """

    country: Optional[CodeableConcept] = None
    jurisdiction: Optional[CodeableConcept] = None
    # Note: status is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce status is provided.
    status: Optional[CodeableConcept] = None  # The date when the Medicinal Product is placed on the market (required)
    dateRange: Optional[Period] = None
    restoreDate: Optional[str] = None  # ISO 8601 dateTime
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductSpecialDesignation:
    """
    Indicates if the medicinal product has an orphan designation for the treatment of a rare disease.
    """

    identifier: List[Identifier] = field(default_factory=list)
    type: Optional[CodeableConcept] = None
    intendedUse: Optional[CodeableConcept] = None
    indicationCodeableConcept: Optional[CodeableConcept] = None
    indicationReference: Optional[Reference] = None
    status: Optional[CodeableConcept] = None
    date: Optional[str] = None  # ISO 8601 dateTime
    species: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProduct(FHIRResource):
    """
    FHIR R4 MedicinalProduct resource.

    Detailed definition of a medicinal product, typically for uses other than direct
    patient care (e.g. regulatory use, drug catalogs).
    """

    resourceType: str = "MedicinalProduct"
    # Identifiers
    identifier: List[Identifier] = field(default_factory=list)
    # Type
    type: Optional[CodeableConcept] = None
    # Domain
    domain: Optional[CodeableConcept] = None
    # Combined Pharmaceutical Dose Form
    combinedPharmaceuticalDoseForm: Optional[CodeableConcept] = None
    # Legal Status of Supply
    legalStatusOfSupply: Optional[CodeableConcept] = None
    # Additional Monitoring Indicator
    additionalMonitoringIndicator: Optional[CodeableConcept] = None
    # Special Measures
    specialMeasures: List[str] = field(default_factory=list)
    # Paediatric Use Indicator
    paediatricUseIndicator: Optional[CodeableConcept] = None
    # Product Classification
    productClassification: List[CodeableConcept] = field(default_factory=list)
    # Marketing Status
    marketingStatus: List[MarketingStatus] = field(default_factory=list)
    # Pharmaceutical Product
    pharmaceuticalProduct: List[Reference] = field(default_factory=list)
    # Packaged Medicinal Product
    packagedMedicinalProduct: List[Reference] = field(default_factory=list)
    # Attached Document
    attachedDocument: List[Reference] = field(default_factory=list)
    # Master File
    masterFile: List[Reference] = field(default_factory=list)
    # Contact
    contact: List[Reference] = field(default_factory=list)
    # Clinical Trial
    clinicalTrial: List[Reference] = field(default_factory=list)
    # Name
    name: List[MedicinalProductName] = field(default_factory=list)
    # Cross Reference
    crossReference: List[Identifier] = field(default_factory=list)
    # Manufacturing Business Operation
    manufacturingBusinessOperation: List[MedicinalProductManufacturingBusinessOperation] = field(default_factory=list)
    # Special Designation
    specialDesignation: List[MedicinalProductSpecialDesignation] = field(default_factory=list)


def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()
