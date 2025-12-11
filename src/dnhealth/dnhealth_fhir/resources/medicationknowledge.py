# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 MedicationKnowledge resource.

Complete MedicationKnowledge resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Reference,
    CodeableConcept,
    Quantity,
    Ratio,
    Duration,
    Money,
)


@dataclass
class MedicationKnowledgeRelatedMedicationKnowledge:
    """
    Associated or related medication information.
    """

    type: CodeableConcept  # Category of medicationKnowledge (required)
    reference: List[Reference] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeMonograph:
    """
    Associated documentation about the medication.
    """

    type: Optional[CodeableConcept] = None
    source: Optional[Reference] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeIngredient:
    """
    Active or inactive ingredient.
    """

    itemCodeableConcept: Optional[CodeableConcept] = None
    itemReference: Optional[Reference] = None
    isActive: Optional[bool] = None
    strength: Optional[Ratio] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeCost:
    """
    The pricing of the medication.
    """

    type: CodeableConcept  # The category of the cost information (required)
    source: Optional[str] = None  # The source or owner for the price information
    cost: Money  # The price of the medication (required)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeMonitoringProgram:
    """
    Program under which a medication is monitored.
    """

    type: Optional[CodeableConcept] = None
    name: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeAdministrationGuidelines:
    """
    Guidelines for administration of the medication.
    """

    dosage: List[Any] = field(default_factory=list)  # Dosage for the medication for the specific guidelines
    indicationCodeableConcept: Optional[CodeableConcept] = None
    indicationReference: Optional[Reference] = None
    patientCharacteristics: List[Any] = field(default_factory=list)  # Characteristics of the patient that are relevant to the administration guidelines
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeMedicineClassification:
    """
    Categorization of the medication within a formulary or classification system.
    """

    type: CodeableConcept  # The type of category for the medication (required)
    classification: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgePackaging:
    """
    Packaging, storage and handling.
    """

    type: Optional[CodeableConcept] = None
    quantity: Optional[Quantity] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeDrugCharacteristic:
    """
    Specifies descriptive properties of the medicine.
    """

    type: Optional[CodeableConcept] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueQuantity: Optional[Quantity] = None
    valueBase64Binary: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeRegulatory:
    """
    Regulatory information about a medication.
    """

    regulatoryAuthority: Reference  # Specifies the authority of the regulation (required)
    substitution: List[Any] = field(default_factory=list)  # Specifies if changes are allowed when dispensing a medication from a regulatory perspective
    schedule: List[CodeableConcept] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledgeKinetics:
    """
    The time course of drug action.
    """

    areaUnderCurve: List[Quantity] = field(default_factory=list)
    lethalDose50: List[Quantity] = field(default_factory=list)
    halfLifePeriod: Optional["Duration"] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class MedicationKnowledge(FHIRResource):
    """
    FHIR R4 MedicationKnowledge resource.

    Represents information about a medication that is used to support knowledge
    about the medication.
    """

    resourceType: str = "MedicationKnowledge"
    # Code
    code: Optional[CodeableConcept] = None
    # Status
    status: Optional[str] = None  # active | entered-in-error | inactive
    # Manufacturer
    manufacturer: Optional[Reference] = None
    # Dose form
    doseForm: Optional[CodeableConcept] = None
    # Amount
    amount: Optional[Quantity] = None
    # Synonym
    synonym: List[str] = field(default_factory=list)
    # Related medication knowledge
    relatedMedicationKnowledge: List[MedicationKnowledgeRelatedMedicationKnowledge] = field(default_factory=list)
    # Associated medication
    associatedMedication: List[Reference] = field(default_factory=list)
    # Product type
    productType: List[CodeableConcept] = field(default_factory=list)
    # Monograph
    monograph: List[MedicationKnowledgeMonograph] = field(default_factory=list)
    # Ingredient
    ingredient: List[MedicationKnowledgeIngredient] = field(default_factory=list)
    # Preparation instruction
    preparationInstruction: Optional[str] = None
    # Intended route
    intendedRoute: List[CodeableConcept] = field(default_factory=list)
    # Cost
    cost: List[MedicationKnowledgeCost] = field(default_factory=list)
    # Monitoring program
    monitoringProgram: List[MedicationKnowledgeMonitoringProgram] = field(default_factory=list)
    # Administration guidelines
    administrationGuidelines: List[MedicationKnowledgeAdministrationGuidelines] = field(default_factory=list)
    # Medicine classification
    medicineClassification: List[MedicationKnowledgeMedicineClassification] = field(default_factory=list)
    # Packaging
    packaging: Optional[MedicationKnowledgePackaging] = None
    # Drug characteristic
    drugCharacteristic: List[MedicationKnowledgeDrugCharacteristic] = field(default_factory=list)
    # Contraindication
    contraindication: List[Reference] = field(default_factory=list)
    # Regulatory
    regulatory: List[MedicationKnowledgeRegulatory] = field(default_factory=list)
    # Kinetics
    kinetics: List[MedicationKnowledgeKinetics] = field(default_factory=list)

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
