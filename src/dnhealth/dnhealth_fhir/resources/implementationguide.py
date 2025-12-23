# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ImplementationGuide resource.

ImplementationGuide describes how to use FHIR resources in a particular context.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class ImplementationGuideDependsOn:
    """
    FHIR ImplementationGuide.dependsOn complex type.
    
    Another implementation guide this depends on.
    """
    
    uri: str  # Canonical URL (required)
    packageId: Optional[str] = None  # NPM package name
    version: Optional[str] = None  # Version of the dependency
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImplementationGuideGlobal:
    """
    FHIR ImplementationGuide.global complex type.
    
    A global profile that all resources must conform to.
    """
    
    type: str  # Type this profile applies to (required)
    profile: str  # Profile that all resources must conform to (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImplementationGuideDefinition:
    """
    FHIR ImplementationGuide.definition complex type.
    
    Information needed to build the IG.
    """
    
    grouping: List[Dict[str, Any]] = field(default_factory=list)  # Grouping used to organize related resources
    resource: List[Dict[str, Any]] = field(default_factory=list)  # Resource in the implementation guide
    page: Optional[Dict[str, Any]] = None  # Page/Section in the implementation guide
    parameter: List[Dict[str, Any]] = field(default_factory=list)  # Defines how IG is built by tools
    template: List[Dict[str, Any]] = field(default_factory=list)  # A template for building resources
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImplementationGuideManifest:
    """
    FHIR ImplementationGuide.manifest complex type.
    
    Information about an assembled IG.
    """
    
    rendering: Optional[str] = None  # Location of rendered implementation guide
    resource: List[Dict[str, Any]] = field(default_factory=list)  # Resource in the implementation guide
    page: List[Dict[str, Any]] = field(default_factory=list)  # HTML page within the parent IG
    image: List[str] = field(default_factory=list)  # Image within the IG
    other: List[str] = field(default_factory=list)  # Additional linkable file in IG
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ImplementationGuide(MetadataResource):
    """
    FHIR R4 ImplementationGuide resource.
    
    Describes how to use FHIR resources in a particular context.
    Extends MetadataResource.
    """
    
    resourceType: str = "ImplementationGuide"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this implementation guide
    # Title
    title: Optional[str] = None  # Title for this implementation guide
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
    purpose: Optional[str] = None  # Why this implementation guide is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Package ID
    packageId: Optional[str] = None  # NPM package name (required, validated in __post_init__)
    # License
    license: Optional[str] = None  # SPDX license code
    # Fhir Version
    fhirVersion: List[str] = field(default_factory=list)  # FHIR version(s) this Implementation Guide targets
    # Depends On
    dependsOn: List[ImplementationGuideDependsOn] = field(default_factory=list)  # Another implementation guide this depends on
    # Global
    global_: List[ImplementationGuideGlobal] = field(default_factory=list)  # Profiles that apply globally (global is Python keyword)
    # Definition
    definition: Optional[ImplementationGuideDefinition] = None  # Information needed to build the IG
    # Manifest
    manifest: Optional[ImplementationGuideManifest] = None  # Information about an assembled IG
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.packageId is None:
            raise ValueError("ImplementationGuide.packageId is required but was not provided")


        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
