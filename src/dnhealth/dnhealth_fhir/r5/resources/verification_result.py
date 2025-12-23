# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 VerificationResult resource.

Describes validation requirements, source(s), status and dates for one or more elements.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Reference, Signature, Timing
from typing import List, Optional

@dataclass
class VerificationResultPrimarySource:
    """
    VerificationResultPrimarySource nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    who: Optional[Reference] = None  # Reference to the primary source.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Type of primary source (License Board; Primary Education; Continuing Education; Postal Service; R...
    communicationMethod: Optional[List[CodeableConcept]] = field(default_factory=list)  # Method for communicating with the primary source (manual; API; Push).
    validationStatus: Optional[CodeableConcept] = None  # Status of the validation of the target against the primary source (successful; failed; unknown).
    validationDate: Optional[str] = None  # When the target was validated against the primary source.
    canPushUpdates: Optional[CodeableConcept] = None  # Ability of the primary source to push updates/alerts (yes; no; undetermined).
    pushTypeAvailable: Optional[List[CodeableConcept]] = field(default_factory=list)  # Type of alerts/updates the primary source can send (specific requested changes; any changes; as d...

@dataclass
class VerificationResultAttestation:
    """
    VerificationResultAttestation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    who: Optional[Reference] = None  # The individual or organization attesting to information.
    onBehalfOf: Optional[Reference] = None  # When the who is asserting on behalf of another (organization or individual).
    communicationMethod: Optional[CodeableConcept] = None  # The method by which attested information was submitted/retrieved (manual; API; Push).
    date: Optional[str] = None  # The date the information was attested to.
    sourceIdentityCertificate: Optional[str] = None  # A digital identity certificate associated with the attestation source.
    proxyIdentityCertificate: Optional[str] = None  # A digital identity certificate associated with the proxy entity submitting attested information o...
    proxySignature: Optional[Signature] = None  # Signed assertion by the proxy entity indicating that they have the right to submit attested infor...
    sourceSignature: Optional[Signature] = None  # Signed assertion by the attestation source that they have attested to the information.

@dataclass
class VerificationResultValidator:
    """
    VerificationResultValidator nested class.
    """

    organization: Optional[Reference] = None  # Reference to the organization validating information.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identityCertificate: Optional[str] = None  # A digital identity certificate associated with the validator.
    attestationSignature: Optional[Signature] = None  # Signed assertion by the validator that they have validated the information.


@dataclass
class VerificationResult(FHIRResource):
    """
    Describes validation requirements, source(s), status and dates for one or more elements.
    """

    status: Optional[str] = None  # The validation status of the target (attested; validated; in process; requires revalidation; vali...
    resourceType: str = "VerificationResult"
    target: Optional[List[Reference]] = field(default_factory=list)  # A resource that was validated.
    targetLocation: Optional[List[str]] = field(default_factory=list)  # The fhirpath location(s) within the resource that was validated.
    need: Optional[CodeableConcept] = None  # The frequency with which the target must be validated (none; initial; periodic).
    statusDate: Optional[str] = None  # When the validation status was updated.
    validationType: Optional[CodeableConcept] = None  # What the target is validated against (nothing; primary source; multiple sources).
    validationProcess: Optional[List[CodeableConcept]] = field(default_factory=list)  # The primary process by which the target is validated (edit check; value set; primary source; mult...
    frequency: Optional[Timing] = None  # Frequency of revalidation.
    lastPerformed: Optional[str] = None  # The date/time validation was last completed (including failed validations).
    nextScheduled: Optional[str] = None  # The date when target is next validated, if appropriate.
    failureAction: Optional[CodeableConcept] = None  # The result if validation fails (fatal; warning; record only; none).
    primarySource: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about the primary source(s) involved in validation.
    attestation: Optional[BackboneElement] = None  # Information about the entity attesting to information.
    validator: Optional[List[BackboneElement]] = field(default_factory=list)  # Information about the entity validating information.