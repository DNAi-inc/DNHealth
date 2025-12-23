# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DocumentReference resource.

DocumentReference is a reference to a document.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, Attachment
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@dataclass
class DocumentReferenceRelatesTo:
    """
    FHIR DocumentReference.relatesTo complex type.
    
    Relationships that this document has with other document references.
    """
    
    code: str  # replaces | transforms | signs | appends (required)
    target: Reference  # Target of the relationship (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DocumentReferenceContent:
    """
    FHIR DocumentReference.content complex type.
    
    The document and format referenced.
    """
    
    attachment: Attachment  # Where to access the document (required)
    format: Optional[CodeableConcept] = None  # Format/content rules for the document
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DocumentReferenceContext:
    """
    FHIR DocumentReference.context complex type.
    
    The clinical context in which the document was created.
    """
    
    encounter: List[Reference] = field(default_factory=list)  # Context of the document content
    event: List[CodeableConcept] = field(default_factory=list)  # Main clinical acts documented
    period: Optional[Period] = None  # Time of service that is being documented
    facilityType: Optional[CodeableConcept] = None  # Kind of facility where patient was seen
    practiceSetting: Optional[CodeableConcept] = None  # Additional details about where the content was created
    sourcePatientInfo: Optional[Reference] = None  # Patient demographics from source
    related: List[Reference] = field(default_factory=list)  # Related identifiers or resources
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DocumentReference(DomainResource):
    """
    FHIR R4 DocumentReference resource.
    
    A reference to a document.
    Extends DomainResource.
    """
    
    resourceType: str = "DocumentReference"
    # Master Identifier
    masterIdentifier: Optional[Identifier] = None  # Master Version Specific Identifier
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Other identifiers for the document
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # current | superseded | entered-in-error (required in FHIR)
    # Doc Status
    docStatus: Optional[str] = None  # preliminary | final | amended | entered-in-error
    # Type
    type: Optional[CodeableConcept] = None  # Kind of document (LOINC if possible)
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Categorization of document
    # Subject
    subject: Optional[Reference] = None  # Who/what is the subject of the document
    # Date
    date: Optional[str] = None  # When this document reference was created
    # Author
    author: List[Reference] = field(default_factory=list)  # Who and/or what authored the document
    # Authenticator
    authenticator: Optional[Reference] = None  # Who/what authenticated the document
    # Custodian
    custodian: Optional[Reference] = None  # Organization which maintains the document
    # Relates To
    relatesTo: List[DocumentReferenceRelatesTo] = field(default_factory=list)  # Relationships to other documents
    # Description
    description: Optional[str] = None  # Human-readable description (title)
    # Security Label
    securityLabel: List[CodeableConcept] = field(default_factory=list)  # Document security-tags
    # Content
    content: List[DocumentReferenceContent] = field(default_factory=list)  # Document referenced (required)
    # Context
    context: Optional[DocumentReferenceContext] = None  # Clinical context of the document

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


