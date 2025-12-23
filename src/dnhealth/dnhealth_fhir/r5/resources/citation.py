# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Citation resource.

The Citation Resource enables reference to any knowledge artifact for purposes of identification and attribution. The Citation Resource supports existing reference structures and developing publication practices such as versioning, expressing complex contributorship roles, and referencing computable resources.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Period, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class CitationSummary:
    """
    CitationSummary nested class.
    """

    text: Optional[str] = None  # The human-readable display of the citation summary.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    style: Optional[CodeableConcept] = None  # Format for display of the citation summary.

@dataclass
class CitationClassification:
    """
    CitationClassification nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The kind of classifier (e.g. publication type, keyword).
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specific classification value.

@dataclass
class CitationStatusDate:
    """
    CitationStatusDate nested class.
    """

    activity: Optional[CodeableConcept] = None  # The state or status of the citation record (that will be paired with the period).
    period: Optional[Period] = None  # When the status started and/or ended.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    actual: Optional[bool] = None  # Whether the status date is actual (has occurred) or expected (estimated or anticipated).

@dataclass
class CitationCitedArtifact:
    """
    CitationCitedArtifact nested class.
    """

    value: Optional[str] = None  # The version number or other version identifier.
    activity: Optional[CodeableConcept] = None  # A definition of the status associated with a date or period.
    period: Optional[Period] = None  # When the status started and/or ended.
    text: Optional[str] = None  # The title of the article or artifact.
    contributor: Optional[Reference] = None  # The identity of the individual contributor.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify the cited artifact when it is represented in other f...
    relatedIdentifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify things closely related to the cited artifact.
    dateAccessed: Optional[str] = None  # When the cited artifact was accessed.
    version: Optional[BackboneElement] = None  # The defined version of the cited artifact.
    baseCitation: Optional[Reference] = None  # Citation for the main version of the cited artifact.
    currentState: Optional[List[CodeableConcept]] = field(default_factory=list)  # The status of the cited artifact.
    statusDate: Optional[List[BackboneElement]] = field(default_factory=list)  # An effective date or period, historical or future, actual or expected, for a status of the cited ...
    actual: Optional[bool] = None  # Either occurred or expected.
    title: Optional[List[BackboneElement]] = field(default_factory=list)  # The title details of the article or artifact.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Used to express the reason for or classification of the title.
    language: Optional[CodeableConcept] = None  # Used to express the specific language of the title.
    abstract: Optional[List[BackboneElement]] = field(default_factory=list)  # The abstract may be used to convey article-contained abstracts, externally-created abstracts, or ...
    copyright: Optional[str] = None  # Copyright notice for the abstract.
    part: Optional[BackboneElement] = None  # The component of the article or artifact.
    relatesTo: Optional[List[BackboneElement]] = field(default_factory=list)  # The artifact related to the cited artifact.
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Provides additional classifiers of the related artifact.
    label: Optional[str] = None  # A short label that can be used to reference the related artifact from elsewhere in the containing...
    display: Optional[str] = None  # A brief description of the document or knowledge resource being referenced, suitable for display ...
    citation: Optional[str] = None  # A bibliographic citation for the related artifact. This text SHOULD be formatted according to an ...
    document: Optional[Attachment] = None  # The document being referenced, represented as an attachment. Do not use this element if using the...
    resource: Optional[str] = None  # The related artifact, such as a library, value set, profile, or other knowledge resource.
    resourceReference: Optional[Reference] = None  # The related artifact, if the artifact is not a canonical resource, or a resource reference to a c...
    publicationForm: Optional[List[BackboneElement]] = field(default_factory=list)  # If multiple, used to represent alternative forms of the article that are not separate citations.
    publishedIn: Optional[BackboneElement] = None  # The collection the cited article or artifact is published in.
    publisher: Optional[Reference] = None  # Name of or resource describing the publisher.
    publisherLocation: Optional[str] = None  # Geographic location of the publisher.
    citedMedium: Optional[CodeableConcept] = None  # Describes the form of the medium cited. Common codes are \"Internet\" or \"Print\". The CitedMedi...
    volume: Optional[str] = None  # Volume number of journal or other collection in which the article is published.
    issue: Optional[str] = None  # Issue, part or supplement of journal or other collection in which the article is published.
    articleDate: Optional[str] = None  # The date the article was added to the database, or the date the article was released.
    publicationDateText: Optional[str] = None  # Text representation of the date on which the issue of the cited artifact was published.
    publicationDateSeason: Optional[str] = None  # Spring, Summer, Fall/Autumn, Winter.
    lastRevisionDate: Optional[str] = None  # The date the article was last revised or updated in the database.
    accessionNumber: Optional[str] = None  # Entry number or identifier for inclusion in a database.
    pageString: Optional[str] = None  # Used for full display of pagination.
    firstPage: Optional[str] = None  # Used for isolated representation of first page.
    lastPage: Optional[str] = None  # Used for isolated representation of last page.
    pageCount: Optional[str] = None  # Actual or approximate number of pages or screens. Distinct from reporting the page numbers.
    webLocation: Optional[List[BackboneElement]] = field(default_factory=list)  # Used for any URL for the article or artifact cited.
    url: Optional[str] = None  # The specific URL.
    classification: Optional[List[BackboneElement]] = field(default_factory=list)  # The assignment to an organizing scheme.
    artifactAssessment: Optional[List[Reference]] = field(default_factory=list)  # Complex or externally created classification.
    contributorship: Optional[BackboneElement] = None  # This element is used to list authors and other contributors, their contact information, specific ...
    complete: Optional[bool] = None  # Indicates if the list includes all authors and/or contributors.
    entry: Optional[List[BackboneElement]] = field(default_factory=list)  # An individual entity named as a contributor, for example in the author list or contributor list.
    forenameInitials: Optional[str] = None  # For citation styles that use initials.
    affiliation: Optional[List[Reference]] = field(default_factory=list)  # Organization affiliated with the contributor.
    contributionType: Optional[List[CodeableConcept]] = field(default_factory=list)  # This element identifies the specific nature of an individual’s contribution with respect to the c...
    role: Optional[CodeableConcept] = None  # The role of the contributor (e.g. author, editor, reviewer, funder).
    contributionInstance: Optional[List[BackboneElement]] = field(default_factory=list)  # Contributions with accounting for time or number.
    time: Optional[str] = None  # The time that the contribution was made.
    correspondingContact: Optional[bool] = None  # Whether the contributor is the corresponding contributor for the role.
    rankingOrder: Optional[int] = None  # Provides a numerical ranking to represent the degree of contributorship relative to other contrib...
    summary: Optional[List[BackboneElement]] = field(default_factory=list)  # Used to record a display of the author/contributor list without separate data element for each li...
    style: Optional[CodeableConcept] = None  # The format for the display string, such as author last name with first letter capitalized followe...
    source: Optional[CodeableConcept] = None  # Used to code the producer or rule for creating the display string.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Any additional information or content for the article or artifact.

@dataclass
class CitationCitedArtifactVersion:
    """
    CitationCitedArtifactVersion nested class.
    """

    value: Optional[str] = None  # The version number or other version identifier.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    baseCitation: Optional[Reference] = None  # Citation for the main version of the cited artifact.

@dataclass
class CitationCitedArtifactStatusDate:
    """
    CitationCitedArtifactStatusDate nested class.
    """

    activity: Optional[CodeableConcept] = None  # A definition of the status associated with a date or period.
    period: Optional[Period] = None  # When the status started and/or ended.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    actual: Optional[bool] = None  # Either occurred or expected.

@dataclass
class CitationCitedArtifactTitle:
    """
    CitationCitedArtifactTitle nested class.
    """

    text: Optional[str] = None  # The title of the article or artifact.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # Used to express the reason for or classification of the title.
    language: Optional[CodeableConcept] = None  # Used to express the specific language of the title.

@dataclass
class CitationCitedArtifactAbstract:
    """
    CitationCitedArtifactAbstract nested class.
    """

    text: Optional[str] = None  # Abstract content.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Used to express the reason for or classification of the abstract.
    language: Optional[CodeableConcept] = None  # Used to express the specific language of the abstract.
    copyright: Optional[str] = None  # Copyright notice for the abstract.

@dataclass
class CitationCitedArtifactPart:
    """
    CitationCitedArtifactPart nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The kind of component.
    value: Optional[str] = None  # The specification of the component.
    baseCitation: Optional[Reference] = None  # The citation for the full article or artifact.

@dataclass
class CitationCitedArtifactRelatesTo:
    """
    CitationCitedArtifactRelatesTo nested class.
    """

    type: Optional[str] = None  # The type of relationship to the related artifact.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Provides additional classifiers of the related artifact.
    label: Optional[str] = None  # A short label that can be used to reference the related artifact from elsewhere in the containing...
    display: Optional[str] = None  # A brief description of the document or knowledge resource being referenced, suitable for display ...
    citation: Optional[str] = None  # A bibliographic citation for the related artifact. This text SHOULD be formatted according to an ...
    document: Optional[Attachment] = None  # The document being referenced, represented as an attachment. Do not use this element if using the...
    resource: Optional[str] = None  # The related artifact, such as a library, value set, profile, or other knowledge resource.
    resourceReference: Optional[Reference] = None  # The related artifact, if the artifact is not a canonical resource, or a resource reference to a c...

@dataclass
class CitationCitedArtifactPublicationForm:
    """
    CitationCitedArtifactPublicationForm nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    publishedIn: Optional[BackboneElement] = None  # The collection the cited article or artifact is published in.
    type: Optional[CodeableConcept] = None  # Kind of container (e.g. Periodical, database, or book).
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Journal identifiers include ISSN, ISO Abbreviation and NLMuniqueID; Book identifiers include ISBN.
    title: Optional[str] = None  # Name of the database or title of the book or journal.
    publisher: Optional[Reference] = None  # Name of or resource describing the publisher.
    publisherLocation: Optional[str] = None  # Geographic location of the publisher.
    citedMedium: Optional[CodeableConcept] = None  # Describes the form of the medium cited. Common codes are \"Internet\" or \"Print\". The CitedMedi...
    volume: Optional[str] = None  # Volume number of journal or other collection in which the article is published.
    issue: Optional[str] = None  # Issue, part or supplement of journal or other collection in which the article is published.
    articleDate: Optional[str] = None  # The date the article was added to the database, or the date the article was released.
    publicationDateText: Optional[str] = None  # Text representation of the date on which the issue of the cited artifact was published.
    publicationDateSeason: Optional[str] = None  # Spring, Summer, Fall/Autumn, Winter.
    lastRevisionDate: Optional[str] = None  # The date the article was last revised or updated in the database.
    language: Optional[List[CodeableConcept]] = field(default_factory=list)  # The language or languages in which this form of the article is published.
    accessionNumber: Optional[str] = None  # Entry number or identifier for inclusion in a database.
    pageString: Optional[str] = None  # Used for full display of pagination.
    firstPage: Optional[str] = None  # Used for isolated representation of first page.
    lastPage: Optional[str] = None  # Used for isolated representation of last page.
    pageCount: Optional[str] = None  # Actual or approximate number of pages or screens. Distinct from reporting the page numbers.
    copyright: Optional[str] = None  # Copyright notice for the full article or artifact.

@dataclass
class CitationCitedArtifactPublicationFormPublishedIn:
    """
    CitationCitedArtifactPublicationFormPublishedIn nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Kind of container (e.g. Periodical, database, or book).
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Journal identifiers include ISSN, ISO Abbreviation and NLMuniqueID; Book identifiers include ISBN.
    title: Optional[str] = None  # Name of the database or title of the book or journal.
    publisher: Optional[Reference] = None  # Name of or resource describing the publisher.
    publisherLocation: Optional[str] = None  # Geographic location of the publisher.

@dataclass
class CitationCitedArtifactWebLocation:
    """
    CitationCitedArtifactWebLocation nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # A characterization of the object expected at the web location.
    url: Optional[str] = None  # The specific URL.

@dataclass
class CitationCitedArtifactClassification:
    """
    CitationCitedArtifactClassification nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # The kind of classifier (e.g. publication type, keyword).
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # The specific classification value.
    artifactAssessment: Optional[List[Reference]] = field(default_factory=list)  # Complex or externally created classification.

@dataclass
class CitationCitedArtifactContributorship:
    """
    CitationCitedArtifactContributorship nested class.
    """

    contributor: Optional[Reference] = None  # The identity of the individual contributor.
    type: Optional[CodeableConcept] = None  # The specific contribution.
    value: Optional[str] = None  # The display string for the author list, contributor list, or contributorship statement.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    complete: Optional[bool] = None  # Indicates if the list includes all authors and/or contributors.
    entry: Optional[List[BackboneElement]] = field(default_factory=list)  # An individual entity named as a contributor, for example in the author list or contributor list.
    forenameInitials: Optional[str] = None  # For citation styles that use initials.
    affiliation: Optional[List[Reference]] = field(default_factory=list)  # Organization affiliated with the contributor.
    contributionType: Optional[List[CodeableConcept]] = field(default_factory=list)  # This element identifies the specific nature of an individual’s contribution with respect to the c...
    role: Optional[CodeableConcept] = None  # The role of the contributor (e.g. author, editor, reviewer, funder).
    contributionInstance: Optional[List[BackboneElement]] = field(default_factory=list)  # Contributions with accounting for time or number.
    time: Optional[str] = None  # The time that the contribution was made.
    correspondingContact: Optional[bool] = None  # Whether the contributor is the corresponding contributor for the role.
    rankingOrder: Optional[int] = None  # Provides a numerical ranking to represent the degree of contributorship relative to other contrib...
    summary: Optional[List[BackboneElement]] = field(default_factory=list)  # Used to record a display of the author/contributor list without separate data element for each li...
    style: Optional[CodeableConcept] = None  # The format for the display string, such as author last name with first letter capitalized followe...
    source: Optional[CodeableConcept] = None  # Used to code the producer or rule for creating the display string.

@dataclass
class CitationCitedArtifactContributorshipEntry:
    """
    CitationCitedArtifactContributorshipEntry nested class.
    """

    contributor: Optional[Reference] = None  # The identity of the individual contributor.
    type: Optional[CodeableConcept] = None  # The specific contribution.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    forenameInitials: Optional[str] = None  # For citation styles that use initials.
    affiliation: Optional[List[Reference]] = field(default_factory=list)  # Organization affiliated with the contributor.
    contributionType: Optional[List[CodeableConcept]] = field(default_factory=list)  # This element identifies the specific nature of an individual’s contribution with respect to the c...
    role: Optional[CodeableConcept] = None  # The role of the contributor (e.g. author, editor, reviewer, funder).
    contributionInstance: Optional[List[BackboneElement]] = field(default_factory=list)  # Contributions with accounting for time or number.
    time: Optional[str] = None  # The time that the contribution was made.
    correspondingContact: Optional[bool] = None  # Whether the contributor is the corresponding contributor for the role.
    rankingOrder: Optional[int] = None  # Provides a numerical ranking to represent the degree of contributorship relative to other contrib...

@dataclass
class CitationCitedArtifactContributorshipEntryContributionInstance:
    """
    CitationCitedArtifactContributorshipEntryContributionInstance nested class.
    """

    type: Optional[CodeableConcept] = None  # The specific contribution.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    time: Optional[str] = None  # The time that the contribution was made.

@dataclass
class CitationCitedArtifactContributorshipSummary:
    """
    CitationCitedArtifactContributorshipSummary nested class.
    """

    value: Optional[str] = None  # The display string for the author list, contributor list, or contributorship statement.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[CodeableConcept] = None  # Used most commonly to express an author list or a contributorship statement.
    style: Optional[CodeableConcept] = None  # The format for the display string, such as author last name with first letter capitalized followe...
    source: Optional[CodeableConcept] = None  # Used to code the producer or rule for creating the display string.


@dataclass
class Citation(FHIRResource):
    """
    The Citation Resource enables reference to any knowledge artifact for purposes of identification and attribution. The Citation Resource supports existing reference structures and developing publication practices such as versioning, expressing complex contributorship roles, and referencing computable resources.
    """

    status: Optional[str] = None  # The status of this summary. Enables tracking the life-cycle of the content.
    resourceType: str = "Citation"
    url: Optional[str] = None  # An absolute URI that is used to identify this citation record when it is referenced in a specific...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this citation record when it is represented in other...
    version: Optional[str] = None  # The identifier that is used to identify this version of the citation record when it is referenced...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the citation record. This name should be usable as an identif...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the citation record.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this citation record is authored for testing purposes (or educat...
    date: Optional[str] = None  # The date (and optionally time) when the citation record was last significantly changed. The date ...
    publisher: Optional[str] = None  # The name of the organization or individual that published the citation record.
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the citation from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the citation record is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this citation is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # Use and/or publishing restrictions for the citation record, not for the cited artifact.
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    approvalDate: Optional[str] = None  # The date on which the resource content was approved by the publisher. Approval happens once when ...
    lastReviewDate: Optional[str] = None  # The date on which the resource content was last reviewed. Review happens periodically after appro...
    effectivePeriod: Optional[Period] = None  # The period during which the citation record content was or is planned to be in active use.
    author: Optional[List[ContactDetail]] = field(default_factory=list)  # Who authored or created the citation record.
    editor: Optional[List[ContactDetail]] = field(default_factory=list)  # Who edited or revised the citation record.
    reviewer: Optional[List[ContactDetail]] = field(default_factory=list)  # Who reviewed the citation record.
    endorser: Optional[List[ContactDetail]] = field(default_factory=list)  # Who endorsed the citation record.
    summary: Optional[List[BackboneElement]] = field(default_factory=list)  # A human-readable display of key concepts to represent the citation.
    classification: Optional[List[BackboneElement]] = field(default_factory=list)  # The assignment to an organizing scheme.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Used for general notes and annotations not coded elsewhere.
    currentState: Optional[List[CodeableConcept]] = field(default_factory=list)  # The status of the citation record.
    statusDate: Optional[List[BackboneElement]] = field(default_factory=list)  # The state or status of the citation record paired with an effective date or period for that state.
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Artifact related to the citation record.
    citedArtifact: Optional[BackboneElement] = None  # The article or artifact being described.