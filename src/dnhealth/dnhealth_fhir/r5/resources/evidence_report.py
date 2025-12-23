# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 EvidenceReport resource.

The EvidenceReport Resource is a specialized container for a collection of resources and codeable concepts, adapted to support compositions of Evidence, EvidenceVariable, and Citation resources and related concepts.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, ContactDetail, Extension, Identifier, Narrative, Period, Quantity, Range, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class EvidenceReportSubject:
    """
    EvidenceReportSubject nested class.
    """

    code: Optional[CodeableConcept] = None  # Characteristic code.
    value: Optional[Any] = None  # Characteristic value.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    characteristic: Optional[List[BackboneElement]] = field(default_factory=list)  # Characteristic.
    exclude: Optional[bool] = None  # Is used to express not the characteristic.
    period: Optional[Period] = None  # Timeframe for the characteristic.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Used for general notes and annotations not coded elsewhere.

@dataclass
class EvidenceReportSubjectCharacteristic:
    """
    EvidenceReportSubjectCharacteristic nested class.
    """

    code: Optional[CodeableConcept] = None  # Characteristic code.
    value: Optional[Any] = None  # Characteristic value.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    exclude: Optional[bool] = None  # Is used to express not the characteristic.
    period: Optional[Period] = None  # Timeframe for the characteristic.

@dataclass
class EvidenceReportRelatesTo:
    """
    EvidenceReportRelatesTo nested class.
    """

    code: Optional[str] = None  # The type of relationship that this composition has with anther composition or document.
    target: Optional[BackboneElement] = None  # The target composition/document of this relationship.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    url: Optional[str] = None  # Target of the relationship URL.
    identifier: Optional[Identifier] = None  # Target of the relationship Identifier.
    display: Optional[str] = None  # Target of the relationship Display.
    resource: Optional[Reference] = None  # Target of the relationship Resource reference.

@dataclass
class EvidenceReportRelatesToTarget:
    """
    EvidenceReportRelatesToTarget nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    url: Optional[str] = None  # Target of the relationship URL.
    identifier: Optional[Identifier] = None  # Target of the relationship Identifier.
    display: Optional[str] = None  # Target of the relationship Display.
    resource: Optional[Reference] = None  # Target of the relationship Resource reference.

@dataclass
class EvidenceReportSection:
    """
    EvidenceReportSection nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # The label for this particular section.  This will be part of the rendered content for the documen...
    focus: Optional[CodeableConcept] = None  # A code identifying the kind of content contained within the section. This should be consistent wi...
    focusReference: Optional[Reference] = None  # A definitional Resource identifying the kind of content contained within the section. This should...
    author: Optional[List[Reference]] = field(default_factory=list)  # Identifies who is responsible for the information in this section, not necessarily who typed it in.
    text: Optional[Narrative] = None  # A human-readable narrative that contains the attested content of the section, used to represent t...
    mode: Optional[str] = None  # How the entry list was prepared - whether it is a working list that is suitable for being maintai...
    orderedBy: Optional[CodeableConcept] = None  # Specifies the order applied to the items in the section entries.
    entryClassifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Specifies any type of classification of the evidence report.
    entryReference: Optional[List[Reference]] = field(default_factory=list)  # A reference to the actual resource from which the narrative in the section is derived.
    entryQuantity: Optional[List[Quantity]] = field(default_factory=list)  # Quantity as content.
    emptyReason: Optional[CodeableConcept] = None  # If the section is empty, why the list is empty. An empty section typically has some text explaini...
    section: Optional[List[Any]] = field(default_factory=list)  # A nested sub-section within this section.


@dataclass
class EvidenceReport(FHIRResource):
    """
    The EvidenceReport Resource is a specialized container for a collection of resources and codeable concepts, adapted to support compositions of Evidence, EvidenceVariable, and Citation resources and related concepts.
    """

    status: Optional[str] = None  # The status of this summary. Enables tracking the life-cycle of the content.
    subject: Optional[BackboneElement] = None  # Specifies the subject or focus of the report. Answers \"What is this report about?\".
    resourceType: str = "EvidenceReport"
    url: Optional[str] = None  # An absolute URI that is used to identify this EvidenceReport when it is referenced in a specifica...
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this EvidenceReport when it is represented in other ...
    relatedIdentifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify things closely related to this EvidenceReport.
    citeAs: Optional[Any] = None  # Citation Resource or display of suggested citation for this report.
    type: Optional[CodeableConcept] = None  # Specifies the kind of report, such as grouping of classifiers, search results, or human-compiled ...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Used for footnotes and annotations.
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Link, description or reference to artifact associated with the report.
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    author: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device primarily involved in the creation and maintenance of the...
    editor: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device primarily responsible for internal coherence of the content.
    reviewer: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device primarily responsible for review of some aspect of the co...
    endorser: Optional[List[ContactDetail]] = field(default_factory=list)  # An individiual, organization, or device responsible for officially endorsing the content for use ...
    relatesTo: Optional[List[BackboneElement]] = field(default_factory=list)  # Relationships that this composition has with other compositions or documents that already exist.
    section: Optional[List[BackboneElement]] = field(default_factory=list)  # The root of the sections that make up the composition.