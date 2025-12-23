# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Composition resource.

The Clinical Document profile constrains Composition to specify a clinical document (matching CDA). 

The base Composition is a general resource for compositions or documents about any kind of subject that might be encountered in healthcare including such things as guidelines, medicines, etc. A clinical document is focused on documents related to the provision of care process, where the subject is a patient, a group of patients, or a closely related concept. A clinical document has additional requirements around confidentiality that do not apply in the same way to other kinds of documents.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Narrative, Period, Reference, RelatedArtifact, UsageContext
from typing import Any, List, Optional

@dataclass
class CompositionAttester:
    """
    CompositionAttester nested class.
    """

    mode: Optional[CodeableConcept] = None  # The type of attestation the authenticator offers.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    time: Optional[str] = None  # When the composition was attested by the party.
    party: Optional[Reference] = None  # Who attested the composition in the specified way.

@dataclass
class CompositionEvent:
    """
    CompositionEvent nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    period: Optional[Period] = None  # The period of time covered by the documentation. There is no assertion that the documentation is ...
    detail: Optional[List[Any]] = field(default_factory=list)  # Represents the main clinical acts, such as a colonoscopy or an appendectomy, being documented. In...

@dataclass
class CompositionSection:
    """
    CompositionSection nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    title: Optional[str] = None  # The label for this particular section.  This will be part of the rendered content for the documen...
    code: Optional[CodeableConcept] = None  # A code identifying the kind of content contained within the section. This must be consistent with...
    author: Optional[List[Reference]] = field(default_factory=list)  # Identifies who is responsible for the information in this section, not necessarily who typed it in.
    focus: Optional[Reference] = None  # The actual focus of the section when it is not the subject of the composition, but instead repres...
    text: Optional[Narrative] = None  # A human-readable narrative that contains the attested content of the section, used to represent t...
    orderedBy: Optional[CodeableConcept] = None  # Specifies the order applied to the items in the section entries.
    entry: Optional[List[Reference]] = field(default_factory=list)  # A reference to the actual resource from which the narrative in the section is derived.
    emptyReason: Optional[CodeableConcept] = None  # If the section is empty, why the list is empty. An empty section typically has some text explaini...
    section: Optional[List[Any]] = field(default_factory=list)  # A nested sub-section within this section.


@dataclass
class Composition(FHIRResource):
    """
    The Clinical Document profile constrains Composition to specify a clinical document (matching CDA). 

The base Composition is a general resource for compositions or documents about any kind of subject that might be encountered in healthcare including such things as guidelines, medicines, etc. A clinical document is focused on documents related to the provision of care process, where the subject is a patient, a group of patients, or a closely related concept. A clinical document has additional requirements around confidentiality that do not apply in the same way to other kinds of documents.
    """

    status: Optional[str] = None  # The workflow/clinical status of this composition. The status is a marker for the clinical standin...
    type: Optional[CodeableConcept] = None  # Specifies the particular kind of composition (e.g. History and Physical, Discharge Summary, Progr...
    date: Optional[str] = None  # The composition editing time, when the composition was last logically changed by the author.
    author: List[Reference] = field(default_factory=list)  # Identifies who is responsible for the information in the composition, not necessarily who typed i...
    title: Optional[str] = None  # Official human-readable label for the composition.
    resourceType: str = "Composition"
    url: Optional[str] = None  # An absolute URI that is used to identify this Composition when it is referenced in a specificatio...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A version-independent identifier for the Composition. This identifier stays constant as the compo...
    version: Optional[str] = None  # An explicitly assigned identifer of a variation of the content in the Composition.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A categorization for the type of the composition - helps for indexing and searching. This may be ...
    subject: Optional[List[Reference]] = field(default_factory=list)  # Who or what the composition is about. The composition can be about a person, (patient or healthca...
    encounter: Optional[Reference] = None  # Describes the clinical encounter or type of care this documentation is associated with.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    name: Optional[str] = None  # A natural language name identifying the {{title}}. This name should be usable as an identifier fo...
    note: Optional[List[Annotation]] = field(default_factory=list)  # For any additional notes.
    attester: Optional[List[BackboneElement]] = field(default_factory=list)  # A participant who has attested to the accuracy of the composition/document.
    custodian: Optional[Reference] = None  # Identifies the organization or group who is responsible for ongoing maintenance of and access to ...
    relatesTo: Optional[List[RelatedArtifact]] = field(default_factory=list)  # Relationships that this composition has with other compositions or documents that already exist.
    event: Optional[List[BackboneElement]] = field(default_factory=list)  # The clinical service, such as a colonoscopy or an appendectomy, being documented.
    section: Optional[List[BackboneElement]] = field(default_factory=list)  # The root of the sections that make up the composition.
