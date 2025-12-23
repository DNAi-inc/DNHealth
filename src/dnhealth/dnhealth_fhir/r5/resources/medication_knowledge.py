# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MedicationKnowledge resource.

Information about a medication that is used to support knowledge.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Dosage, Duration, Extension, Identifier, Money, Period, Quantity, Range, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class MedicationKnowledgeRelatedMedicationKnowledge:
    """
    MedicationKnowledgeRelatedMedicationKnowledge nested class.
    """

    type: Optional[CodeableConcept] = None  # The category of the associated medication knowledge reference.
    reference: List[Reference] = field(default_factory=list)  # Associated documentation about the associated medication knowledge.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class MedicationKnowledgeMonograph:
    """
    MedicationKnowledgeMonograph nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The category of documentation about the medication. (e.g. professional monograph, patient educati...
    source: Optional[Reference] = None  # Associated documentation about the medication.

@dataclass
class MedicationKnowledgeCost:
    """
    MedicationKnowledgeCost nested class.
    """

    type: Optional[CodeableConcept] = None  # The category of the cost information.  For example, manufacturers' cost, patient cost, claim reim...
    cost: Optional[Any] = None  # The price or representation of the cost (for example, Band A, Band B or $, $$) of the medication.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    effectiveDate: Optional[List[Period]] = field(default_factory=list)  # The date range for which the cost information of the medication is effective.
    source: Optional[str] = None  # The source or owner that assigns the price to the medication.

@dataclass
class MedicationKnowledgeMonitoringProgram:
    """
    MedicationKnowledgeMonitoringProgram nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Type of program under which the medication is monitored.
    name: Optional[str] = None  # Name of the reviewing program.

@dataclass
class MedicationKnowledgeIndicationGuideline:
    """
    MedicationKnowledgeIndicationGuideline nested class.
    """

    type: Optional[CodeableConcept] = None  # The type or category of dosage for a given medication (for example, prophylaxis, maintenance, the...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    indication: Optional[List[Any]] = field(default_factory=list)  # Indication or reason for use of the medication that applies to the specific administration guidel...
    dosingGuideline: Optional[List[BackboneElement]] = field(default_factory=list)  # The guidelines for the dosage of the medication for the indication.
    treatmentIntent: Optional[CodeableConcept] = None  # The overall intention of the treatment, for example, prophylactic, supporative, curative, etc.
    dosage: Optional[List[BackboneElement]] = field(default_factory=list)  # Dosage for the medication for the specific guidelines.
    administrationTreatment: Optional[CodeableConcept] = None  # The type of the treatment that the guideline applies to, for example, long term therapy, first li...
    patientCharacteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # Characteristics of the patient that are relevant to the administration guidelines (for example, h...
    value: Optional[Any] = None  # The specific characteristic (e.g. height, weight, gender, etc.).

@dataclass
class MedicationKnowledgeIndicationGuidelineDosingGuideline:
    """
    MedicationKnowledgeIndicationGuidelineDosingGuideline nested class.
    """

    type: Optional[CodeableConcept] = None  # The type or category of dosage for a given medication (for example, prophylaxis, maintenance, the...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    treatmentIntent: Optional[CodeableConcept] = None  # The overall intention of the treatment, for example, prophylactic, supporative, curative, etc.
    dosage: Optional[List[BackboneElement]] = field(default_factory=list)  # Dosage for the medication for the specific guidelines.
    administrationTreatment: Optional[CodeableConcept] = None  # The type of the treatment that the guideline applies to, for example, long term therapy, first li...
    patientCharacteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # Characteristics of the patient that are relevant to the administration guidelines (for example, h...
    value: Optional[Any] = None  # The specific characteristic (e.g. height, weight, gender, etc.).

@dataclass
class MedicationKnowledgeIndicationGuidelineDosingGuidelineDosage:
    """
    MedicationKnowledgeIndicationGuidelineDosingGuidelineDosage nested class.
    """

    type: Optional[CodeableConcept] = None  # The type or category of dosage for a given medication (for example, prophylaxis, maintenance, the...
    dosage: List[Dosage] = field(default_factory=list)  # Dosage for the medication for the specific guidelines.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class MedicationKnowledgeIndicationGuidelineDosingGuidelinePatientCharacteristic:
    """
    MedicationKnowledgeIndicationGuidelineDosingGuidelinePatientCharacteristic nested class.
    """

    type: Optional[CodeableConcept] = None  # The categorization of the specific characteristic that is relevant to the administration guidelin...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # The specific characteristic (e.g. height, weight, gender, etc.).

@dataclass
class MedicationKnowledgeMedicineClassification:
    """
    MedicationKnowledgeMedicineClassification nested class.
    """

    type: Optional[CodeableConcept] = None  # The type of category for the medication (for example, therapeutic classification, therapeutic sub...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    source: Optional[Any] = None  # Either a textual source of the classification or a reference to an online source.
    classification: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specific category assigned to the medication (e.g. anti-infective, anti-hypertensive, antibiotic,...

@dataclass
class MedicationKnowledgePackaging:
    """
    MedicationKnowledgePackaging nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    cost: Optional[List[Any]] = field(default_factory=list)  # The cost of the packaged medication.
    packagedProduct: Optional[Reference] = None  # A reference to a PackagedProductDefinition that provides the details of the product that is in th...

@dataclass
class MedicationKnowledgeStorageGuideline:
    """
    MedicationKnowledgeStorageGuideline nested class.
    """

    type: Optional[CodeableConcept] = None  # Identifies the category or type of setting (e.g., type of location, temperature, humidity).
    value: Optional[Any] = None  # Value associated to the setting. E.g., 40° – 50°F for temperature.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    reference: Optional[str] = None  # Reference to additional information about the storage guidelines.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional notes about the storage.
    stabilityDuration: Optional[Duration] = None  # Duration that the medication remains stable if the environmentalSetting is respected.
    environmentalSetting: Optional[List[BackboneElement]] = field(default_factory=list)  # Describes a setting/value on the environment for the adequate storage of the medication and other...

@dataclass
class MedicationKnowledgeStorageGuidelineEnvironmentalSetting:
    """
    MedicationKnowledgeStorageGuidelineEnvironmentalSetting nested class.
    """

    type: Optional[CodeableConcept] = None  # Identifies the category or type of setting (e.g., type of location, temperature, humidity).
    value: Optional[Any] = None  # Value associated to the setting. E.g., 40° – 50°F for temperature.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class MedicationKnowledgeRegulatory:
    """
    MedicationKnowledgeRegulatory nested class.
    """

    regulatoryAuthority: Optional[Reference] = None  # The authority that is specifying the regulations.
    type: Optional[CodeableConcept] = None  # Specifies the type of substitution allowed.
    allowed: Optional[bool] = None  # Specifies if regulation allows for changes in the medication when dispensing.
    quantity: Optional[Quantity] = None  # The maximum number of units of the medication that can be dispensed.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    substitution: Optional[List[BackboneElement]] = field(default_factory=list)  # Specifies if changes are allowed when dispensing a medication from a regulatory perspective.
    schedule: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specifies the schedule of a medication in jurisdiction.
    maxDispense: Optional[BackboneElement] = None  # The maximum number of units of the medication that can be dispensed in a period.
    period: Optional[Duration] = None  # The period that applies to the maximum number of units.

@dataclass
class MedicationKnowledgeRegulatorySubstitution:
    """
    MedicationKnowledgeRegulatorySubstitution nested class.
    """

    type: Optional[CodeableConcept] = None  # Specifies the type of substitution allowed.
    allowed: Optional[bool] = None  # Specifies if regulation allows for changes in the medication when dispensing.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class MedicationKnowledgeRegulatoryMaxDispense:
    """
    MedicationKnowledgeRegulatoryMaxDispense nested class.
    """

    quantity: Optional[Quantity] = None  # The maximum number of units of the medication that can be dispensed.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    period: Optional[Duration] = None  # The period that applies to the maximum number of units.

@dataclass
class MedicationKnowledgeDefinitional:
    """
    MedicationKnowledgeDefinitional nested class.
    """

    item: Optional[Any] = None  # A reference to the resource that provides information about the ingredient.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    definition: Optional[List[Reference]] = field(default_factory=list)  # Associated definitions for this medication.
    doseForm: Optional[CodeableConcept] = None  # Describes the form of the item.  Powder; tablets; capsule.
    intendedRoute: Optional[List[CodeableConcept]] = field(default_factory=list)  # The intended or approved route of administration.
    ingredient: Optional[List[BackboneElement]] = field(default_factory=list)  # Identifies a particular constituent of interest in the product.
    type: Optional[CodeableConcept] = None  # Indication of whether this ingredient affects the therapeutic action of the drug.
    strength: Optional[Any] = None  # Specifies how many (or how much) of the items there are in this Medication.  For example, 250 mg ...
    drugCharacteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # Specifies descriptive properties of the medicine, such as color, shape, imprints, etc.
    value: Optional[Any] = None  # Description of the characteristic.

@dataclass
class MedicationKnowledgeDefinitionalIngredient:
    """
    MedicationKnowledgeDefinitionalIngredient nested class.
    """

    item: Optional[Any] = None  # A reference to the resource that provides information about the ingredient.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Indication of whether this ingredient affects the therapeutic action of the drug.
    strength: Optional[Any] = None  # Specifies how many (or how much) of the items there are in this Medication.  For example, 250 mg ...

@dataclass
class MedicationKnowledgeDefinitionalDrugCharacteristic:
    """
    MedicationKnowledgeDefinitionalDrugCharacteristic nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # A code specifying which characteristic of the medicine is being described (for example, colour, s...
    value: Optional[Any] = None  # Description of the characteristic.


@dataclass
class MedicationKnowledge(FHIRResource):
    """
    Information about a medication that is used to support knowledge.
    """

    resourceType: str = "MedicationKnowledge"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for this medication.
    code: Optional[CodeableConcept] = None  # A code that specifies this medication, or a textual description if no code is available. Usage no...
    status: Optional[str] = None  # A code to indicate if the medication referred to by this MedicationKnowledge is in active use wit...
    author: Optional[Reference] = None  # The creator or owner of the knowledge or information about the medication.
    intendedJurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # Lists the jurisdictions that this medication knowledge was written for.
    name: Optional[List[str]] = field(default_factory=list)  # All of the names for a medication, for example, the name(s) given to a medication in different co...
    relatedMedicationKnowledge: Optional[List[BackboneElement]] = field(default_factory=list)  # Associated or related medications. For example, if the medication is a branded product (e.g. Cres...
    associatedMedication: Optional[List[Reference]] = field(default_factory=list)  # Links to associated medications that could be prescribed, dispensed or administered.
    productType: Optional[List[CodeableConcept]] = field(default_factory=list)  # Category of the medication or product (e.g. branded product, therapeutic moeity, generic product,...
    monograph: Optional[List[BackboneElement]] = field(default_factory=list)  # Associated documentation about the medication.
    preparationInstruction: Optional[str] = None  # The instructions for preparing the medication.
    cost: Optional[List[BackboneElement]] = field(default_factory=list)  # The price of the medication.
    monitoringProgram: Optional[List[BackboneElement]] = field(default_factory=list)  # The program under which the medication is reviewed.
    indicationGuideline: Optional[List[BackboneElement]] = field(default_factory=list)  # Guidelines or protocols that are applicable for the administration of the medication based on ind...
    medicineClassification: Optional[List[BackboneElement]] = field(default_factory=list)  # Categorization of the medication within a formulary or classification system.
    packaging: Optional[List[BackboneElement]] = field(default_factory=list)  # Information that only applies to packages (not products).
    clinicalUseIssue: Optional[List[Reference]] = field(default_factory=list)  # Potential clinical issue with or between medication(s) (for example, drug-drug interaction, drug-...
    storageGuideline: Optional[List[BackboneElement]] = field(default_factory=list)  # Information on how the medication should be stored, for example, refrigeration temperatures and l...
    regulatory: Optional[List[BackboneElement]] = field(default_factory=list)  # Regulatory information about a medication.
    definitional: Optional[BackboneElement] = None  # Along with the link to a Medicinal Product Definition resource, this information provides common ...