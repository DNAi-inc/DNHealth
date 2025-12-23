# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CapabilityStatement resource.

CapabilityStatement describes the capabilities of a FHIR server or client.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class CapabilityStatementSoftware:
    """
    FHIR CapabilityStatement.software complex type.
    
    Software that is covered by this capability statement.
    """
    
    name: str  # Name of the software (required)
    version: Optional[str] = None  # Version of the software
    releaseDate: Optional[str] = None  # Date of release
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CapabilityStatementImplementation:
    """
    FHIR CapabilityStatement.implementation complex type.
    
    Information about the specific installation.
    """
    
    description: str  # Description of the implementation (required)
    url: Optional[str] = None  # Base URL for the installation
    custodian: Optional[Reference] = None  # Organization that manages the data
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CapabilityStatementRestResource:
    """
    FHIR CapabilityStatement.rest.resource complex type.
    
    Resource served on the REST interface.
    """
    
    type: str  # Type of resource (required)
    profile: Optional[str] = None  # Profile for the resource
    supportedProfile: List[str] = field(default_factory=list)  # Supported profiles
    documentation: Optional[str] = None  # Additional documentation
    interaction: List[Dict[str, Any]] = field(default_factory=list)  # What operations are supported
    versioning: Optional[str] = None  # no-version | versioned | versioned-update
    readHistory: Optional[bool] = None  # Whether vRead can return past versions
    updateCreate: Optional[bool] = None  # Whether update can create new resources
    conditionalCreate: Optional[bool] = None  # Whether conditional create is supported
    conditionalRead: Optional[str] = None  # not-supported | modified-since | not-match | full-support
    conditionalUpdate: Optional[bool] = None  # Whether conditional update is supported
    conditionalDelete: Optional[str] = None  # not-supported | single | multiple
    referencePolicy: List[str] = field(default_factory=list)  # literal | logical | resolves | enforced | local
    searchInclude: List[str] = field(default_factory=list)  # _include values supported
    searchRevInclude: List[str] = field(default_factory=list)  # _revinclude values supported
    searchParam: List[Dict[str, Any]] = field(default_factory=list)  # Search parameters supported
    operation: List[Dict[str, Any]] = field(default_factory=list)  # Operations supported
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CapabilityStatementRest:
    """
    FHIR CapabilityStatement.rest complex type.
    
    REST interface definition.
    """
    
    mode: str  # client | server (required)
    documentation: Optional[str] = None  # General documentation
    security: Optional[Dict[str, Any]] = None  # Security configuration
    resource: List[CapabilityStatementRestResource] = field(default_factory=list)  # Resources served
    interaction: List[Dict[str, Any]] = field(default_factory=list)  # What operations are supported
    searchParam: List[Dict[str, Any]] = field(default_factory=list)  # Search parameters
    operation: List[Dict[str, Any]] = field(default_factory=list)  # Operations
    compartment: List[str] = field(default_factory=list)  # Compartments supported
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CapabilityStatement(CanonicalResource):
    """
    FHIR R4 CapabilityStatement resource.
    
    Describes the capabilities of a FHIR server or client.
    Extends CanonicalResource.
    """
    
    resourceType: str = "CapabilityStatement"
    # Kind (required field - validated in __post_init__)
    kind: Optional[str] = None  # instance | capability | requirements (required)
    # Fhir Version (required field - validated in __post_init__)
    fhirVersion: Optional[str] = None  # FHIR version (required): 4.0.0 | 4.0.1
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this capability statement
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Purpose
    purpose: Optional[str] = None  # Why this capability statement is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this capability statement
    # Instantiates
    instantiates: List[str] = field(default_factory=list)  # Canonical URLs of capability statements
    # Imports
    imports: List[str] = field(default_factory=list)  # Canonical URLs of capability statements to import
    # Software
    software: Optional[CapabilityStatementSoftware] = None  # Software that is covered
    # Implementation
    implementation: Optional[CapabilityStatementImplementation] = None  # Information about the installation
    # Format
    format: List[str] = field(default_factory=list)  # Formats supported: json | xml | ttl | mime
    # Patch Format
    patchFormat: List[str] = field(default_factory=list)  # Patch formats supported
    # Implementation Guide
    implementationGuide: List[str] = field(default_factory=list)  # Implementation guides supported
    # Rest
    rest: List[CapabilityStatementRest] = field(default_factory=list)  # REST interface definition
    # Messaging
    messaging: List[Dict[str, Any]] = field(default_factory=list)  # Messaging interface definition
    # Document
    document: List[Dict[str, Any]] = field(default_factory=list)  # Document definition

    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.kind is None:
            raise ValueError("CapabilityStatement.kind is required")
        if self.fhirVersion is None:
            raise ValueError("CapabilityStatement.fhirVersion is required")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
