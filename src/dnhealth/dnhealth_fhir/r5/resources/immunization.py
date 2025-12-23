# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Immunization resource.

Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class ImmunizationPerformer:
    """
    ImmunizationPerformer nested class.
    """

    actor: Optional[Reference] = None  # The practitioner or organization who performed the action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Describes the type of performance (e.g. ordering provider, administering provider, etc.).

@dataclass
class ImmunizationProgramEligibility:
    """
    ImmunizationProgramEligibility nested class.
    """

    program: Optional[CodeableConcept] = None  # Indicates which program the patient had their eligility evaluated for.
    programStatus: Optional[CodeableConcept] = None  # Indicates the patient's eligility status for for a specific payment program.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class ImmunizationReaction:
    """
    ImmunizationReaction nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    date: Optional[str] = None  # Date of reaction to the immunization.
    manifestation: Optional[Any] = None  # Details of the reaction.
    reported: Optional[bool] = None  # Self-reported indicator.

@dataclass
class ImmunizationProtocolApplied:
    """
    ImmunizationProtocolApplied nested class.
    """

    doseNumber: Optional[str] = None  # Nominal position in a series as intended by the practitioner administering the dose.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    series: Optional[str] = None  # One possible path to achieve presumed immunity against a disease - within the context of an autho...
    authority: Optional[Reference] = None  # Indicates the authority who published the protocol (e.g. ACIP) that is being followed.
    targetDisease: Optional[List[CodeableConcept]] = field(default_factory=list)  # The vaccine preventable disease the dose is being administered against.
    seriesDoses: Optional[str] = None  # The recommended number of doses to achieve immunity as intended by the practitioner administering...


@dataclass
class Immunization(FHIRResource):
    """
    Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.
    """

    status: Optional[str] = None  # Indicates the current status of the immunization event.
    vaccineCode: Optional[CodeableConcept] = None  # Vaccine that was administered or was to be administered.
    patient: Optional[Reference] = None  # The patient who either received or did not receive the immunization.
    occurrence: Optional[Any] = None  # Date vaccine administered or was to be administered.
    resourceType: str = "Immunization"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A unique identifier assigned to this immunization record.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A plan, order or recommendation fulfilled in whole or in part by this immunization.
    statusReason: Optional[CodeableConcept] = None  # Indicates the reason the immunization event was not performed.
    administeredProduct: Optional[Any] = None  # An indication of which product was administered to the patient. This is typically a more detailed...
    manufacturer: Optional[Any] = None  # Name of vaccine manufacturer.
    lotNumber: Optional[str] = None  # Lot number of the  vaccine product.
    expirationDate: Optional[str] = None  # Date vaccine batch expires.
    encounter: Optional[Reference] = None  # The visit or admission or other contact between patient and health care provider the immunization...
    supportingInformation: Optional[List[Reference]] = field(default_factory=list)  # Additional information that is relevant to the immunization (e.g. for a vaccine recipient who is ...
    primarySource: Optional[bool] = None  # Indicates whether the data contained in the resource was captured by the individual/organization ...
    informationSource: Optional[Any] = None  # Typically the source of the data when the report of the immunization event is not based on inform...
    location: Optional[Reference] = None  # The service delivery location where the vaccine administration occurred.
    site: Optional[CodeableConcept] = None  # Body site where vaccine was administered.
    route: Optional[CodeableConcept] = None  # The path by which the vaccine product is taken into the body.
    doseQuantity: Optional[Quantity] = None  # The quantity of vaccine product that was administered.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who performed the immunization event.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Extra information about the immunization that is not conveyed by the other attributes.
    reason: Optional[List[Any]] = field(default_factory=list)  # Describes why the immunization occurred in coded or textual form, or Indicates another resource (...
    isSubpotent: Optional[bool] = None  # Indication if a dose is considered to be subpotent. By default, a dose should be considered to be...
    subpotentReason: Optional[List[CodeableConcept]] = field(default_factory=list)  # Reason why a dose is considered to be subpotent.
    programEligibility: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates a patient's eligibility for a funding program.
    fundingSource: Optional[CodeableConcept] = None  # Indicates the source of the vaccine actually administered. This may be different than the patient...
    reaction: Optional[List[BackboneElement]] = field(default_factory=list)  # Categorical data indicating that an adverse event is associated in time to an immunization.
    protocolApplied: Optional[List[BackboneElement]] = field(default_factory=list)  # The protocol (set of recommendations) being followed by the provider who administered the dose.