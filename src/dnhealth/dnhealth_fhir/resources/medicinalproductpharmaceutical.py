# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicinalProductPharmaceutical resource.

Complete MedicinalProductPharmaceutical resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Reference,
    CodeableConcept,
    Quantity,
    Ratio,
)


@dataclass
class MedicinalProductPharmaceuticalCharacteristics:
    """
    Characteristics e.g. a products onset of action.
    """

    code: CodeableConcept  # A coded characteristic (required)
    status: Optional[CodeableConcept] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPharmaceuticalRouteOfAdministration:
    """
    The path by which the pharmaceutical product is taken into or makes contact with the body.
    """

    code: CodeableConcept  # Coded expression for the route (required)
    firstDose: Optional[Quantity] = None
    maxSingleDose: Optional[Quantity] = None
    maxDosePerDay: Optional[Quantity] = None
    maxDosePerTreatmentPeriod: Optional[Ratio] = None
    maxTreatmentPeriod: Optional[Quantity] = None
    targetSpecies: List["MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies:
    """
    A species for which this route applies.
    """

    code: CodeableConcept  # Coded expression for the species (required)
    withdrawalPeriod: List["MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod"] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod:
    """
    A species specific time during which consumption of animal product is not appropriate.
    """

    tissue: CodeableConcept  # Coded expression for the type of tissue for which the withdrawal period applies (required)
    value: Quantity  # A value for the time (required)
    supportingInformation: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicinalProductPharmaceutical(FHIRResource):
    """
    FHIR R4 MedicinalProductPharmaceutical resource.

    A pharmaceutical product described in terms of its composition and dose form.
    """

    resourceType: str = "MedicinalProductPharmaceutical"
    # Identifiers
    identifier: List[Reference] = field(default_factory=list)
    # Administrable Dose Form
    # Note: administrableDoseForm is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce administrableDoseForm is provided.
    administrableDoseForm: Optional[CodeableConcept] = None  # The administrable dose form, after necessary reconstitution (required)
    # Unit of Presentation
    unitOfPresentation: Optional[CodeableConcept] = None
    # Ingredient
    ingredient: List[Reference] = field(default_factory=list)
    # Device
    device: List[Reference] = field(default_factory=list)
    # Characteristics
    characteristics: List[MedicinalProductPharmaceuticalCharacteristics] = field(default_factory=list)
    # Route of Administration
    routeOfAdministration: List[MedicinalProductPharmaceuticalRouteOfAdministration] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
