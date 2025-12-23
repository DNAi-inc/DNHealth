# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ArtifactAssessment resource.

Represents justification for a recommendation
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference, RelatedArtifact
from typing import Any, List, Optional

@dataclass
class ArtifactAssessmentContent:
    """
    ArtifactAssessmentContent nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    informationType: Optional[str] = None  # The type of information this component of the content represents.
    summary: Optional[str] = None  # A brief summary of the content of this component.
    type: Optional[CodeableConcept] = None  # Indicates what type of content this component represents.
    classifier: Optional[List[CodeableConcept]] = field(default_factory=list)  # Represents a rating, classifier, or assessment of the artifact.
    quantity: Optional[Quantity] = None  # A quantitative rating of the artifact.
    author: Optional[Reference] = None  # Indicates who or what authored the content.
    path: Optional[List[str]] = field(default_factory=list)  # A URI that points to what the comment is about, such as a line of text in the CQL, or a specific ...
    relatedArtifact: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Additional related artifacts that provide supporting documentation, additional evidence, or furth...
    freeToShare: Optional[bool] = None  # Acceptable to publicly share the comment, classifier or rating.
    component: Optional[List[Any]] = field(default_factory=list)  # If the informationType is container, the components of the content.


@dataclass
class ArtifactAssessment(FHIRResource):
    """
    Represents justification for a recommendation
    """

    artifact: Optional[Any] = None  # A reference to a resource, canonical resource, or non-FHIR resource which is the recommendation t...
    resourceType: str = "ArtifactAssessment"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this artifact assessment when it is represented in o...
    title: Optional[str] = None  # A short title for the assessment for use in displaying and selecting.
    citeAs: Optional[Any] = None  # Display of or reference to the bibliographic citation of the recommendation.
    date: Optional[str] = None  # The date  (and optionally time) when the artifact assessment was published. The date must change ...
    copyright: Optional[str] = None  # A copyright statement relating to the artifact assessment and/or its contents. Copyright statemen...
    approvalDate: Optional[str] = None  # The date on which the resource content was approved by the publisher. Approval happens once when ...
    lastReviewDate: Optional[str] = None  # The date on which the resource content was last reviewed. Review happens periodically after appro...
    content: Optional[List[BackboneElement]] = field(default_factory=list)  # A component comment, classifier, or rating of the artifact.
    workflowStatus: Optional[str] = None  # Indicates the workflow status of the comment or change request.
    disposition: Optional[str] = None  # Indicates the disposition of the responsible party to the comment or change request.