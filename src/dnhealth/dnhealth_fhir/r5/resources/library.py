# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Library resource.

The logic library profile sets the minimum expectations for computable and/or executable libraries, including support for terminology and dependency declaration, parameters, and data requirements
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, CodeableConcept, Coding, ContactDetail, DataRequirement, Extension, Identifier, ParameterDefinition, Period, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class LibraryRelatedArtifact:
    """
    LibraryRelatedArtifact nested class.
    """

    type: Optional[str] = None  # The type of relationship to the related artifact.
    resource: Optional[str] = None  # The related artifact, such as a library, value set, profile, or other knowledge resource.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Provides additional classifiers of the related artifact.
    label: Optional[str] = None  # A short label that can be used to reference the citation from elsewhere in the containing artifac...
    display: Optional[str] = None  # A brief description of the document or knowledge resource being referenced, suitable for display ...
    citation: Optional[str] = None  # A bibliographic citation for the related artifact. This text SHOULD be formatted according to an ...
    document: Optional[Attachment] = None  # The document being referenced, represented as an attachment. This is exclusive with the resource ...
    resourceReference: Optional[Reference] = None  # The related artifact, if the artifact is not a canonical resource, or a resource reference to a c...
    publicationStatus: Optional[str] = None  # The publication status of the artifact being referred to.
    publicationDate: Optional[str] = None  # The date of publication of the artifact being referred to.

@dataclass
class LibraryContent:
    """
    LibraryContent nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    contentType: Optional[str] = None  # Identifies the type of the data in the attachment and allows a method to be chosen to interpret o...
    language: Optional[str] = None  # The human language of the content. The value can be any valid value according to BCP 47.
    data: Optional[str] = None  # The actual data of the attachment - a sequence of bytes, base64 encoded.
    url: Optional[str] = None  # A location where the data can be accessed.
    size: Optional[Any] = None  # The number of bytes of data that make up this attachment (before base64 encoding, if that is done).
    hash: Optional[str] = None  # The calculated hash of the data using SHA-1. Represented using base64.
    title: Optional[str] = None  # A label or set of text to display in place of the data.
    creation: Optional[str] = None  # The date that the attachment was first created.
    height: Optional[int] = None  # Height of the image in pixels (photo/video).
    width: Optional[int] = None  # Width of the image in pixels (photo/video).
    frames: Optional[int] = None  # The number of frames in a photo. This is used with a multi-page fax, or an imaging acquisition co...
    duration: Optional[float] = None  # The duration of the recording in seconds - for audio and video.
    pages: Optional[int] = None  # The number of pages when printed.


@dataclass
class Library(FHIRResource):
    """
    The logic library profile sets the minimum expectations for computable and/or executable libraries, including support for terminology and dependency declaration, parameters, and data requirements
    """

    url: Optional[str] = None  # An absolute URI that is used to identify this library when it is referenced in a specification, m...
    version: Optional[str] = None  # The identifier that is used to identify this version of the library when it is referenced in a sp...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the library.
    status: Optional[str] = None  # The status of this library. Enables tracking the life-cycle of the content.
    type: Optional[CodeableConcept] = None  # Identifies the type of library such as a Logic Library, Model Definition, Asset Collection, or Mo...
    description: Optional[str] = None  # A free text natural language description of the library from a consumer's perspective.
    resourceType: str = "Library"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this library when it is represented in other formats...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the library. This name should be usable as an identifier for ...
    subtitle: Optional[str] = None  # An explanatory or alternate title for the library giving additional information about its content.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this library is authored for testing purposes (or education/eval...
    subject: Optional[Any] = None  # A code or group definition that describes the intended subject of the contents of the library.
    date: Optional[str] = None  # The date  (and optionally time) when the library was last significantly changed. The date must ch...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the library is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this library is needed and why it has been designed as it has.
    usage: Optional[str] = None  # A detailed description of how the library is used from a clinical perspective.
    copyright: Optional[str] = None  # A copyright statement relating to the library and/or its contents. Copyright statements are gener...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    approvalDate: Optional[str] = None  # The date on which the resource content was approved by the publisher. Approval happens once when ...
    lastReviewDate: Optional[str] = None  # The date on which the resource content was last reviewed. Review happens periodically after appro...
    effectivePeriod: Optional[Period] = None  # The period during which the library content was or is planned to be in active use.
    topic: Optional[List[CodeableConcept]] = field(default_factory=list)  # Descriptive topics related to the content of the library. Topics provide a high-level categorizat...
    author: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual or organization primarily involved in the creation and maintenance of the content.
    editor: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization primarily responsible for internal coherence of the content.
    reviewer: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization asserted by the publisher to be primarily responsible for review of...
    endorser: Optional[List[ContactDetail]] = field(default_factory=list)  # An individual or organization asserted by the publisher to be responsible for officially endorsin...
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Related artifacts such as additional documentation, justification, or bibliographic references.
    parameter: Optional[List[ParameterDefinition]] = field(default_factory=list)  # The parameter element defines parameters used by the library.
    dataRequirement: Optional[List[DataRequirement]] = field(default_factory=list)  # Describes a set of data that must be provided in order to be able to successfully perform the com...
    content: Optional[List[Attachment]] = field(default_factory=list)  # The content of the library as an Attachment. The content may be a reference to a url, or may be d...