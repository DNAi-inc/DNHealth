# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Bundle resource.

Complete Bundle resource with all R4 elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.types import Extension, Identifier, Reference, Signature
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class Bundle(FHIRResource):
    """
    FHIR R4 Bundle resource.

    Represents a collection of resources.
    """

    resourceType: str = "Bundle"
    # Type (required - default to empty string, validated in __post_init__)
    type: str = ""  # document, message, transaction, transaction-response, batch, batch-response, history, searchset, collection
    # Identifier
    identifier: Optional[Identifier] = None
    # Timestamp
    timestamp: Optional[str] = None
    # Total
    total: Optional[int] = None
    # Link
    link: List["BundleLink"] = field(default_factory=list)
    # Entry
    entry: List["BundleEntry"] = field(default_factory=list)
    # Signature
    signature: Optional[Signature] = None
    
    def __post_init__(self):
        """Validate Bundle after initialization."""
        super().__post_init__()
        if not self.type:
            raise ValueError("Bundle.type is required and cannot be empty")



        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
@dataclass
class BundleLink:
    """
    Link in a bundle.

    Links to related resources.
    """

    relation: str
    url: str
    extension: List[Extension] = field(default_factory=list)


@dataclass
class BundleEntry:
    """
    Entry in a bundle.

    Contains a resource or reference.
    """

    link: List[BundleLink] = field(default_factory=list)
    fullUrl: Optional[str] = None
    resource: Optional[Any] = None  # Can be any FHIR resource
    search: Optional["BundleEntrySearch"] = None
    request: Optional["BundleEntryRequest"] = None
    response: Optional["BundleEntryResponse"] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class BundleEntrySearch:
    """
    Search information for a bundle entry.
    """

    mode: Optional[str] = None  # match, include, outcome
    score: Optional[float] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class BundleEntryRequest:
    """
    Request information for a bundle entry.
    """

    method: str  # GET, HEAD, POST, PUT, DELETE, PATCH
    url: str
    ifNoneMatch: Optional[str] = None
    ifModifiedSince: Optional[str] = None
    ifMatch: Optional[str] = None
    ifNoneExist: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)


@dataclass
class BundleEntryResponse:
    """
    Response information for a bundle entry.
    """

    status: str
    location: Optional[str] = None
    etag: Optional[str] = None
    lastModified: Optional[str] = None
    outcome: Optional[Any] = None  # Can be any FHIR resource
    extension: List[Extension] = field(default_factory=list)


# Note: Signature type is imported from dnhealth.dnhealth_fhir.types

