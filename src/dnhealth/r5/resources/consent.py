# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Consent resource.

A record of a healthcare consumer’s  choices  or choices made on their behalf by a third party, which permits or denies identified recipient(s) or recipient role(s) to perform one or more actions within a given policy context, for specific purposes and periods of time.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Coding, Expression, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class ConsentPolicyBasis:
    """
    ConsentPolicyBasis nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    reference: Optional[Reference] = None  # A Reference that identifies the policy the organization will enforce for this Consent.
    url: Optional[str] = None  # A URL that links to a computable version of the policy the organization will enforce for this Con...

@dataclass
class ConsentVerification:
    """
    ConsentVerification nested class.
    """

    verified: Optional[bool] = None  # Has the instruction been verified.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    verificationType: Optional[CodeableConcept] = None  # Extensible list of verification type starting with verification and re-validation.
    verifiedBy: Optional[Reference] = None  # The person who conducted the verification/validation of the Grantor decision.
    verifiedWith: Optional[Reference] = None  # Who verified the instruction (Patient, Relative or other Authorized Person).
    verificationDate: Optional[List[str]] = field(default_factory=list)  # Date(s) verification was collected.

@dataclass
class ConsentProvision:
    """
    ConsentProvision nested class.
    """

    meaning: Optional[str] = None  # How the resource reference is interpreted when testing consent restrictions.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    period: Optional[Period] = None  # Timeframe for this provision.
    actor: Optional[List[BackboneElement]] = field(default_factory=list)  # Who or what is controlled by this provision. Use group to identify a set of actors by some proper...
    role: Optional[CodeableConcept] = None  # How the individual is involved in the resources content that is described in the exception.
    reference: Optional[Reference] = None  # The resource that identifies the actor. To identify actors by type, use group to identify a set o...
    action: Optional[List[CodeableConcept]] = field(default_factory=list)  # Actions controlled by this provision.
    securityLabel: Optional[List[Coding]] = field(default_factory=list)  # A security label, comprised of 0..* security label fields (Privacy tags), which define which reso...
    purpose: Optional[List[Coding]] = field(default_factory=list)  # The context of the activities a user is taking - why the user is accessing the data - that are co...
    documentType: Optional[List[Coding]] = field(default_factory=list)  # The documentType(s) covered by this provision. The type can be a CDA document, or some other type...
    resourceType: Optional[List[Coding]] = field(default_factory=list)  # The resourceType(s) covered by this provision. The type can be a FHIR resource type or a profile ...
    code: Optional[List[CodeableConcept]] = field(default_factory=list)  # If this code is found in an instance, then the provision applies.
    dataPeriod: Optional[Period] = None  # Clinical or Operational Relevant period of time that bounds the data controlled by this provision.
    data: Optional[List[BackboneElement]] = field(default_factory=list)  # The resources controlled by this provision if specific resources are referenced.
    expression: Optional[Expression] = None  # A computable (FHIRPath or other) definition of what is controlled by this consent.
    provision: Optional[List[Any]] = field(default_factory=list)  # Provisions which provide exceptions to the base provision or subprovisions.

@dataclass
class ConsentProvisionActor:
    """
    ConsentProvisionActor nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    role: Optional[CodeableConcept] = None  # How the individual is involved in the resources content that is described in the exception.
    reference: Optional[Reference] = None  # The resource that identifies the actor. To identify actors by type, use group to identify a set o...

@dataclass
class ConsentProvisionData:
    """
    ConsentProvisionData nested class.
    """

    meaning: Optional[str] = None  # How the resource reference is interpreted when testing consent restrictions.
    reference: Optional[Reference] = None  # A reference to a specific resource that defines which resources are covered by this consent.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Consent(FHIRResource):
    """
    A record of a healthcare consumer’s  choices  or choices made on their behalf by a third party, which permits or denies identified recipient(s) or recipient role(s) to perform one or more actions within a given policy context, for specific purposes and periods of time.
    """

    status: Optional[str] = None  # Indicates the current state of this Consent resource.
    resourceType: str = "Consent"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique identifier for this copy of the Consent Statement.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A classification of the type of consents found in the statement. This element supports indexing a...
    subject: Optional[Reference] = None  # The patient/healthcare practitioner or group of persons to whom this consent applies.
    date: Optional[str] = None  # Date the consent instance was agreed to.
    period: Optional[Period] = None  # Effective period for this Consent Resource and all provisions unless specified in that provision.
    grantor: Optional[List[Reference]] = field(default_factory=list)  # The entity responsible for granting the rights listed in a Consent Directive.
    grantee: Optional[List[Reference]] = field(default_factory=list)  # The entity responsible for complying with the Consent Directive, including any obligations or lim...
    manager: Optional[List[Reference]] = field(default_factory=list)  # The actor that manages the consent through its lifecycle.
    controller: Optional[List[Reference]] = field(default_factory=list)  # The actor that controls/enforces the access according to the consent.
    sourceAttachment: Optional[List[Attachment]] = field(default_factory=list)  # The source on which this consent statement is based. The source might be a scanned original paper...
    sourceReference: Optional[List[Reference]] = field(default_factory=list)  # A reference to a consent that links back to such a source, a reference to a document repository (...
    regulatoryBasis: Optional[List[CodeableConcept]] = field(default_factory=list)  # A set of codes that indicate the regulatory basis (if any) that this consent supports.
    policyBasis: Optional[BackboneElement] = None  # A Reference or URL used to uniquely identify the policy the organization will enforce for this Co...
    policyText: Optional[List[Reference]] = field(default_factory=list)  # A Reference to the human readable policy explaining the basis for the Consent.
    verification: Optional[List[BackboneElement]] = field(default_factory=list)  # Whether a treatment instruction (e.g. artificial respiration: yes or no) was verified with the pa...
    decision: Optional[str] = None  # Action to take - permit or deny - as default.
    provision: Optional[List[BackboneElement]] = field(default_factory=list)  # An exception to the base policy of this consent. An exception can be an addition or removal of ac...
