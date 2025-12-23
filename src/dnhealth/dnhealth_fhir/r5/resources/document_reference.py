# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DocumentReference resource.

A reference to a document of any kind for any purpose. While the term “document” implies a more narrow focus, for this resource this “document” encompasses *any* serialized object with a mime-type, it includes formal patient-centric documents (CDA), clinical notes, scanned paper, non-patient specific documents like policy text, as well as a photo, video, or audio recording acquired or used in healthcare.  The DocumentReference resource provides metadata about the document so that the document can be discovered and managed.  The actual content may be inline base64 encoded data or provided by direct reference.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Coding, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class DocumentReferenceAttester:
    """
    DocumentReferenceAttester nested class.
    """

    mode: Optional[CodeableConcept] = None  # The type of attestation the authenticator offers.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    time: Optional[str] = None  # When the document was attested by the party.
    party: Optional[Reference] = None  # Who attested the document in the specified way.

@dataclass
class DocumentReferenceRelatesTo:
    """
    DocumentReferenceRelatesTo nested class.
    """

    code: Optional[CodeableConcept] = None  # The type of relationship that this document has with anther document.
    target: Optional[Reference] = None  # The target document of this relationship.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DocumentReferenceContent:
    """
    DocumentReferenceContent nested class.
    """

    attachment: Optional[Attachment] = None  # The document or URL of the document along with critical metadata to prove content has integrity.
    value: Optional[Any] = None  # Code|uri|canonical.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    profile: Optional[List[BackboneElement]] = field(default_factory=list)  # An identifier of the document constraints, encoding, structure, and template that the document co...

@dataclass
class DocumentReferenceContentProfile:
    """
    DocumentReferenceContentProfile nested class.
    """

    value: Optional[Any] = None  # Code|uri|canonical.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class DocumentReference(FHIRResource):
    """
    A reference to a document of any kind for any purpose. While the term “document” implies a more narrow focus, for this resource this “document” encompasses *any* serialized object with a mime-type, it includes formal patient-centric documents (CDA), clinical notes, scanned paper, non-patient specific documents like policy text, as well as a photo, video, or audio recording acquired or used in healthcare.  The DocumentReference resource provides metadata about the document so that the document can be discovered and managed.  The actual content may be inline base64 encoded data or provided by direct reference.
    """

    status: Optional[str] = None  # The status of this document reference.
    content: List[BackboneElement] = field(default_factory=list)  # The document and format referenced.  If there are multiple content element repetitions, these mus...
    resourceType: str = "DocumentReference"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Other business identifiers associated with the document, including version independent identifiers.
    version: Optional[str] = None  # An explicitly assigned identifer of a variation of the content in the DocumentReference.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # A procedure that is fulfilled in whole or in part by the creation of this media.
    docStatus: Optional[str] = None  # The status of the underlying document.
    modality: Optional[List[CodeableConcept]] = field(default_factory=list)  # Imaging modality used. This may include both acquisition and non-acquisition modalities.
    type: Optional[CodeableConcept] = None  # Specifies the particular kind of document referenced  (e.g. History and Physical, Discharge Summa...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A categorization for the type of document referenced - helps for indexing and searching. This may...
    subject: Optional[Reference] = None  # Who or what the document is about. The document can be about a person, (patient or healthcare pra...
    context: Optional[List[Reference]] = field(default_factory=list)  # Describes the clinical encounter or type of care that the document content is associated with.
    event: Optional[List[Any]] = field(default_factory=list)  # This list of codes represents the main clinical acts, such as a colonoscopy or an appendectomy, b...
    bodySite: Optional[List[Any]] = field(default_factory=list)  # The anatomic structures included in the document.
    facilityType: Optional[CodeableConcept] = None  # The kind of facility where the patient was seen.
    practiceSetting: Optional[CodeableConcept] = None  # This property may convey specifics about the practice setting where the content was created, ofte...
    period: Optional[Period] = None  # The time period over which the service that is described by the document was provided.
    date: Optional[str] = None  # When the document reference was created.
    author: Optional[List[Reference]] = field(default_factory=list)  # Identifies who is responsible for adding the information to the document.
    attester: Optional[List[BackboneElement]] = field(default_factory=list)  # A participant who has authenticated the accuracy of the document.
    custodian: Optional[Reference] = None  # Identifies the organization or group who is responsible for ongoing maintenance of and access to ...
    relatesTo: Optional[List[BackboneElement]] = field(default_factory=list)  # Relationships that this document has with other document references that already exist.
    description: Optional[str] = None  # Human-readable description of the source document.
    securityLabel: Optional[List[CodeableConcept]] = field(default_factory=list)  # A set of Security-Tag codes specifying the level of privacy/security of the Document found at Doc...