# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 DocumentManifest resource.

DocumentManifest is a manifest that provides a summary of the set of documents included in a package.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation


@dataclass
class DocumentManifestRelated:
    """
    FHIR DocumentManifest.related complex type.
    
    Related identifiers or resources associated with the DocumentManifest.
    """
    
    identifier: Optional[Identifier] = None  # Related identifier
    ref: Optional[Reference] = None  # Related Resource
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class DocumentManifest(DomainResource):
    """
    FHIR R4 DocumentManifest resource.
    
    A manifest that provides a summary of the set of documents included in a package.
    Extends DomainResource.
    """
    
    resourceType: str = "DocumentManifest"
    # Master Identifier
    masterIdentifier: Optional[Identifier] = None  # Unique Identifier for the set of documents
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Other identifiers for the manifest
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass
    # Validation should enforce status is provided.
    status: Optional[str] = None  # current | superseded | entered-in-error (required in FHIR)
    # Type
    type: Optional[CodeableConcept] = None  # Kind of document set
    # Subject
    subject: Optional[Reference] = None  # Subject of the set of documents
    # Created
    created: Optional[str] = None  # When this document manifest was created
    # Author
    author: List[Reference] = field(default_factory=list)  # Who and/or what authored the manifest
    # Recipient
    recipient: List[Reference] = field(default_factory=list)  # Intended to get notified about this set of documents
    # Source
    source: Optional[str] = None  # The source system/application/software
    # Description
    description: Optional[str] = None  # Human-readable description (summary)
    # Content
    content: List[Reference] = field(default_factory=list)  # Items in manifest (required)
    # Related
    related: List[DocumentManifestRelated] = field(default_factory=list)  # Related things

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


