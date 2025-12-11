# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Composition resource.

Composition represents a set of resources composed into a single coherent clinical statement.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Attachment, Narrative
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class CompositionAttester:
    """
    FHIR Composition.attester complex type.
    
    Attests to accuracy of composition.
    """
    
    mode: str  # personal | professional | legal | official (required)
    time: Optional[str] = None  # When the composition was attested
    party: Optional[Reference] = None  # Who attested the composition
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CompositionRelatesTo:
    """
    FHIR Composition.relatesTo complex type.
    
    Relationships that this composition has with other compositions or documents.
    """
    
    code: str  # replaces | transforms | signs | appends (required)
    targetIdentifier: Optional[Identifier] = None  # Target of the relationship
    targetReference: Optional[Reference] = None  # Target of the relationship
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CompositionEvent:
    """
    FHIR Composition.event complex type.
    
    The clinical service, such as a colonoscopy or an appendectomy, being documented.
    """
    
    code: List[CodeableConcept] = field(default_factory=list)  # Code(s) that apply to the event being documented
    period: Optional[Period] = None  # The period covered by the documentation
    detail: List[Reference] = field(default_factory=list)  # The event(s) being documented
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CompositionSection:
    """
    FHIR Composition.section complex type.
    
    The root of the sections that make up the composition.
    """
    
    title: Optional[str] = None  # Label for section
    code: Optional[CodeableConcept] = None  # Classification of section
    author: List[Reference] = field(default_factory=list)  # Who and/or what authored the section
    focus: Optional[Reference] = None  # Who/what the section is about
    text: Optional[Narrative] = None  # Text summary of the section (Narrative type)
    mode: Optional[str] = None  # working | snapshot | changes
    orderedBy: Optional[CodeableConcept] = None  # Order of section entries
    entry: List[Reference] = field(default_factory=list)  # A reference to data that supports this section
    emptyReason: Optional[CodeableConcept] = None  # Why the section is empty
    section: List["CompositionSection"] = field(default_factory=list)  # Nested sections
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Composition(DomainResource):
    """
    FHIR R4 Composition resource.
    
    Represents a set of resources composed into a single coherent clinical statement.
    Extends DomainResource.
    """
    
    resourceType: str = "Composition"
    # Identifier
    identifier: Optional[Identifier] = None  # Version-independent identifier for the Composition
    # Status
    status: str  # preliminary | final | amended | entered-in-error (required)
    # Type
    type: CodeableConcept  # Kind of composition (required)
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Categorization of Composition
    # Subject
    subject: Optional[Reference] = None  # Who and/or what the composition is about
    # Encounter
    encounter: Optional[Reference] = None  # Context of the Composition
    # Date
    date: str  # Composition editing time (required)
    # Author
    author: List[Reference] = field(default_factory=list)  # Who and/or what authored the composition
    # Title
    title: str  # Human Readable name of the composition (required)
    # Confidentiality
    confidentiality: Optional[str] = None  # As defined by affinity domain
    # Attester
    attester: List[CompositionAttester] = field(default_factory=list)  # Attests to accuracy of composition
    # Custodian
    custodian: Optional[Reference] = None  # Organization which maintains the composition
    # Relates To
    relatesTo: List[CompositionRelatesTo] = field(default_factory=list)  # Relationships to other compositions/documents
    # Event
    event: List[CompositionEvent] = field(default_factory=list)  # The clinical service(s) being documented
    # Section
    section: List[CompositionSection] = field(default_factory=list)  # Composition is broken into sections

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


