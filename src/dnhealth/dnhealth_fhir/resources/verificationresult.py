# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 VerificationResult resource.

VerificationResult represents the result of a verification process.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource

logger = logging.getLogger(__name__)
from dnhealth.dnhealth_fhir.types import (
    Extension,
    CodeableConcept,
    Reference,
    Period,
    Signature,
)


@dataclass
class VerificationResultAttestation:
    """
    FHIR VerificationResult.attestation complex type.
    
    Information about the entity attesting to information.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    who: Optional[Reference] = None  # The individual or organization attesting to information
    onBehalfOf: Optional[Reference] = None  # When the who is asserting on behalf of another
    communicationMethod: Optional[CodeableConcept] = None  # The method by which attested information was submitted/retrieved
    date: Optional[str] = None  # The date the information was attested to
    sourceIdentityCertificate: Optional[str] = None  # A digital identity certificate
    proxyIdentityCertificate: Optional[str] = None  # A digital identity certificate used by the proxy
    proxySignature: Optional[Signature] = None  # Proxy signature
    sourceSignature: Optional[Signature] = None  # Attester signature


@dataclass
class VerificationResultValidator:
    """
    FHIR VerificationResult.validator complex type.
    
    Information about the entity validating information.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: organization is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce organization is provided.
    organization: Optional[Reference] = None  # Reference to the organization validating information (required)
    identityCertificate: Optional[str] = None  # A digital identity certificate associated with the validator
    attestationSignature: Optional[Signature] = None  # Validator signature


@dataclass
class VerificationResult(DomainResource):
    """
    FHIR R4 VerificationResult resource.
    
    Represents the result of a verification process.
    Extends DomainResource.
    """
    
    resourceType: str = "VerificationResult"
    # Status (required - using field(default=None) to fix dataclass field ordering with parent classes)
    status: Optional[str] = field(default=None)  # attested | validated | in-process | req-revalid | val-fail | reval-fail (required)
    # Target
    target: List[Reference] = field(default_factory=list)  # A resource that was validated
    # Target Location
    targetLocation: List[str] = field(default_factory=list)  # The fhirpath location(s) within the resource that was validated
    # Need
    need: Optional[CodeableConcept] = None  # none | initial | periodic
    # Status Date
    statusDate: Optional[str] = None  # When the validation status was updated
    # Validation Type
    validationType: Optional[CodeableConcept] = None  # nothing | primary | multiple
    # Validation Process
    validationProcess: List[CodeableConcept] = field(default_factory=list)  # The primary process by which the target is validated
    # Frequency
    frequency: Optional[Period] = None  # Frequency of revalidation
    # Last Performed
    lastPerformed: Optional[str] = None  # The date/time validation was last performed
    # Next Scheduled
    nextScheduled: Optional[str] = None  # The date when target is next validated
    # Failure Action
    failureAction: Optional[CodeableConcept] = None  # fatal | warn | rec-only | none
    # Primary Source
    primarySource: List["VerificationResultPrimarySource"] = field(default_factory=list)  # Information about the primary source(s) involved in validation
    # Attestation
    attestation: Optional[VerificationResultAttestation] = None  # Information about the entity attesting to information
    # Validator
    validator: List[VerificationResultValidator] = field(default_factory=list)  # Information about the entity validating information
    
    def __post_init__(self):
        """Validate required fields."""
        if self.status is None:
            raise ValueError("status is required")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")


@dataclass
class VerificationResultPrimarySource:
    """
    FHIR VerificationResult.primarySource complex type.
    
    Information about the primary source(s) involved in validation.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    who: Optional[Reference] = None  # Reference to the primary source
    type: List[CodeableConcept] = field(default_factory=list)  # Type of primary source
    communicationMethod: List[CodeableConcept] = field(default_factory=list)  # Method for exchanging information
    validationStatus: Optional[CodeableConcept] = None  # successful | failed | unknown
    validationDate: Optional[str] = None  # When the validation was performed
    canPushUpdates: Optional[CodeableConcept] = None  # yes | no | undetermined
    pushTypeAvailable: List[CodeableConcept] = field(default_factory=list)  # specific | any | source
