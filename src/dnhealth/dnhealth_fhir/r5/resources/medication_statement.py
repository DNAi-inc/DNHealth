# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 MedicationStatement resource.

A record of a medication that is being consumed by a patient.   A MedicationStatement may indicate that the patient may be taking the medication now or has taken the medication in the past or will be taking the medication in the future.  The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician.  A common scenario where this information is captured is during the history taking process during a patient visit or stay.   The medication information may come from sources such as the patient's memory, from a prescription bottle,  or from a list of medications the patient, clinician or other party maintains.

The primary difference between a medicationstatement and a medicationadministration is that the medication administration has complete administration information and is based on actual administration information from the person who administered the medication.  A medicationstatement is often, if not always, less specific.  There is no required date/time when the medication was administered, in fact we only know that a source has reported the patient is taking this medication, where details such as time, quantity, or rate or even medication product may be incomplete or missing or less precise.  As stated earlier, the Medication Statement information may come from the patient's memory, from a prescription bottle or from a list of medications the patient, clinician or other party maintains.  Medication administration is more formal and is not missing detailed information.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Dosage, Extension, Identifier, Period, Reference, Timing
from typing import Any, List, Optional

@dataclass
class MedicationStatementAdherence:
    """
    MedicationStatementAdherence nested class.
    """

    code: Optional[CodeableConcept] = None  # Type of the adherence for the medication.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    reason: Optional[CodeableConcept] = None  # Captures the reason for the current use or adherence of a medication.


@dataclass
class MedicationStatement(FHIRResource):
    """
    A record of a medication that is being consumed by a patient.   A MedicationStatement may indicate that the patient may be taking the medication now or has taken the medication in the past or will be taking the medication in the future.  The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician.  A common scenario where this information is captured is during the history taking process during a patient visit or stay.   The medication information may come from sources such as the patient's memory, from a prescription bottle,  or from a list of medications the patient, clinician or other party maintains.

The primary difference between a medicationstatement and a medicationadministration is that the medication administration has complete administration information and is based on actual administration information from the person who administered the medication.  A medicationstatement is often, if not always, less specific.  There is no required date/time when the medication was administered, in fact we only know that a source has reported the patient is taking this medication, where details such as time, quantity, or rate or even medication product may be incomplete or missing or less precise.  As stated earlier, the Medication Statement information may come from the patient's memory, from a prescription bottle or from a list of medications the patient, clinician or other party maintains.  Medication administration is more formal and is not missing detailed information.
    """

    status: Optional[str] = None  # A code representing the status of recording the medication statement.
    medication: Optional[Any] = None  # Identifies the medication being administered. This is either a link to a resource representing th...
    subject: Optional[Reference] = None  # The person, animal or group who is/was taking the medication.
    resourceType: str = "MedicationStatement"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers associated with this Medication Statement that are defined by business processes and/...
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular MedicationStatement is a component or step.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Type of medication statement (for example, drug classification like ATC, where meds would be admi...
    encounter: Optional[Reference] = None  # The encounter that establishes the context for this MedicationStatement.
    effective: Optional[Any] = None  # The interval of time during which it is being asserted that the patient is/was/will be taking the...
    dateAsserted: Optional[str] = None  # The date when the Medication Statement was asserted by the information source.
    informationSource: Optional[List[Reference]] = field(default_factory=list)  # The person or organization that provided the information about the taking of this medication. Not...
    derivedFrom: Optional[List[Reference]] = field(default_factory=list)  # Allows linking the MedicationStatement to the underlying MedicationRequest, or to other informati...
    reason: Optional[List[Any]] = field(default_factory=list)  # A concept, Condition or observation that supports why the medication is being/was taken.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Provides extra information about the Medication Statement that is not conveyed by the other attri...
    relatedClinicalInformation: Optional[List[Reference]] = field(default_factory=list)  # Link to information that is relevant to a medication statement, for example, illicit drug use, ge...
    renderedDosageInstruction: Optional[str] = None  # The full representation of the dose of the medication included in all dosage instructions.  To be...
    dosage: Optional[List[Dosage]] = field(default_factory=list)  # Indicates how the medication is/was or should be taken by the patient.
    adherence: Optional[BackboneElement] = None  # Indicates whether the medication is or is not being consumed or administered.