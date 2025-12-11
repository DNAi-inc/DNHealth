# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Consent resource.

Consent represents a healthcare consumer's choices to permit or deny recipients or roles to perform actions for specific purposes and periods of time.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Attachment
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class ConsentPolicy:
    """
    FHIR Consent.policy complex type.
    
    Policies covered by this consent.
    """
    
    authority: Optional[str] = None  # Enforcement source for policy
    uri: Optional[str] = None  # Specific policy covered by this consent
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ConsentVerification:
    """
    FHIR Consent.verification complex type.
    
    Whether a treatment instruction (e.g. artificial respiration yes or no) was verified with the patient, his/her family or another authorized person.
    """
    
    verified: bool  # Has been verified (required)
    verifiedWith: Optional[Reference] = None  # Person who verified
    verificationDate: Optional[str] = None  # When consent verified
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ConsentProvisionActor:
    """
    FHIR Consent.provision.actor complex type.
    
    Who or what is controlled by this rule.
    """
    
    role: Optional[CodeableConcept] = None  # How the actor is involved
    reference: Reference  # Resource for the actor (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ConsentProvisionData:
    """
    FHIR Consent.provision.data complex type.
    
    Data controlled by this rule.
    """
    
    meaning: str  # instance | related | dependents | authoredby (required)
    reference: Reference  # The actual data reference (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ConsentProvision:
    """
    FHIR Consent.provision complex type.
    
    An exception to the base policy of this consent.
    """
    
    type: Optional[str] = None  # deny | permit
    period: Optional[Period] = None  # Timeframe for this provision
    actor: List[ConsentProvisionActor] = field(default_factory=list)  # Who|what controlled by this rule
    action: List[CodeableConcept] = field(default_factory=list)  # Actions controlled by this rule
    securityLabel: List[CodeableConcept] = field(default_factory=list)  # Security Labels that define affected resources
    purpose: List[CodeableConcept] = field(default_factory=list)  # Context of activities covered by this rule
    class_: List[CodeableConcept] = field(default_factory=list)  # e.g. Resource Type, Profile, CDA, etc.
    code: List[CodeableConcept] = field(default_factory=list)  # e.g. LOINC or SNOMED CT code, etc.
    dataPeriod: Optional[Period] = None  # Timeframe for data controlled by this rule
    data: List[ConsentProvisionData] = field(default_factory=list)  # Data controlled by this rule
    provision: List["ConsentProvision"] = field(default_factory=list)  # Nested exception rules
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Consent(DomainResource):
    """
    FHIR R4 Consent resource.
    
    Represents a healthcare consumer's choices to permit or deny recipients or roles to perform actions for specific purposes and periods of time.
    Extends DomainResource.
    """
    
    resourceType: str = "Consent"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Identifier for this record
    # Status
    status: str  # draft | proposed | active | rejected | inactive | entered-in-error (required)
    # Scope
    scope: CodeableConcept  # Which of the four areas this resource covers (required)
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Classification of the consent statement
    # Patient
    patient: Optional[Reference] = None  # Who the consent applies to
    # Date Time
    dateTime: Optional[str] = None  # When this Consent was created or indexed
    # Performer
    performer: List[Reference] = field(default_factory=list)  # Who is agreeing to the policy and rules
    # Organization
    organization: List[Reference] = field(default_factory=list)  # Custodian of the consent
    # Source Attachment
    sourceAttachment: Optional[Attachment] = None  # Source from which this consent is taken
    # Source Reference
    sourceReference: Optional[Reference] = None  # Source from which this consent is taken
    # Policy
    policy: List[ConsentPolicy] = field(default_factory=list)  # Policies covered by this consent
    # Policy Rule
    policyRule: Optional[CodeableConcept] = None  # Regulation that this consent adheres to
    # Verification
    verification: List[ConsentVerification] = field(default_factory=list)  # Consent Verified by patient or family
    # Provision
    provision: Optional[ConsentProvision] = None  # Constraints to the base Consent.policyRule

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


