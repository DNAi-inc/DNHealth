# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 List resource.

A List is a curated collection of resources, for things such as problem lists, allergy lists, facility list, organization list, etc.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Reference
from typing import List, Optional

@dataclass
class ListEntry:
    """
    ListEntry nested class.
    """

    item: Optional[Reference] = None  # A reference to the actual resource from which data was derived.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    flag: Optional[CodeableConcept] = None  # The flag allows the system constructing the list to indicate the role and significance of the ite...
    deleted: Optional[bool] = None  # True if this item is marked as deleted in the list.
    date: Optional[str] = None  # When this item was added to the list.


@dataclass
class List(FHIRResource):
    """
    A List is a curated collection of resources, for things such as problem lists, allergy lists, facility list, organization list, etc.
    """

    status: Optional[str] = None  # Indicates the current state of this list.
    mode: Optional[str] = None  # How this list was prepared - whether it is a working list that is suitable for being maintained o...
    resourceType: str = "List"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for the List assigned for business purposes outside the context of FHIR.
    title: Optional[str] = None  # A label for the list assigned by the author.
    code: Optional[CodeableConcept] = None  # This code defines the purpose of the list - why it was created.
    subject: Optional[List[Reference]] = field(default_factory=list)  # The common subject(s) (or patient(s)) of the resources that are in the list if there is one (or a...
    encounter: Optional[Reference] = None  # The encounter that is the context in which this list was created.
    date: Optional[str] = None  # Date list was last reviewed/revised and determined to be 'current'.
    source: Optional[Reference] = None  # The entity responsible for deciding what the contents of the list were. Where the list was create...
    orderedBy: Optional[CodeableConcept] = None  # What order applies to the items in the list.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments that apply to the overall list.
    entry: Optional[List[BackboneElement]] = field(default_factory=list)  # Entries in this list.
    emptyReason: Optional[CodeableConcept] = None  # If the list is empty, why the list is empty.