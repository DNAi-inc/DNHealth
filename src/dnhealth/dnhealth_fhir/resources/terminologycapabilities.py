# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 TerminologyCapabilities resource.

TerminologyCapabilities describes the capabilities of a terminology server.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class TerminologyCapabilitiesSoftware:
    """
    FHIR TerminologyCapabilities.software complex type.
    
    Software that is covered by this capability statement.
    """
    
    name: str  # Name of the software (required)
    version: Optional[str] = None  # Version of the software
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilitiesImplementation:
    """
    FHIR TerminologyCapabilities.implementation complex type.
    
    Information about the specific installation.
    """
    
    description: str  # Description of the implementation (required)
    url: Optional[str] = None  # Base URL for the installation
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilitiesCodeSystem:
    """
    FHIR TerminologyCapabilities.codeSystem complex type.
    
    Information about code systems supported by the server.
    """
    
    uri: Optional[str] = None  # Canonical URL for code system
    version: List[Dict[str, Any]] = field(default_factory=list)  # Version of Code System supported
    subsumption: Optional[bool] = None  # Whether subsumption is supported
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilitiesExpansion:
    """
    FHIR TerminologyCapabilities.expansion complex type.
    
    Information about the ValueSet expansion.
    """
    
    hierarchical: Optional[bool] = None  # Whether the server can return nested value sets
    paging: Optional[bool] = None  # Whether the server supports paging on expansion
    incomplete: Optional[bool] = None  # Whether the server supports the incomplete parameter
    parameter: List[Dict[str, Any]] = field(default_factory=list)  # Supported expansion parameter
    textFilter: Optional[str] = None  # Documentation about text searching works
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilitiesValidateCode:
    """
    FHIR TerminologyCapabilities.validateCode complex type.
    
    Information about code validation.
    """
    
    translations: bool  # Whether translations are supported (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilitiesTranslation:
    """
    FHIR TerminologyCapabilities.translation complex type.
    
    Information about translation.
    """
    
    needsMap: bool  # Whether the client must identify the map (required)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilitiesClosure:
    """
    FHIR TerminologyCapabilities.closure complex type.
    
    Information about closure.
    """
    
    translation: Optional[bool] = None  # If cross-system closure is supported
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class TerminologyCapabilities(CanonicalResource):
    """
    FHIR R4 TerminologyCapabilities resource.
    
    Describes the capabilities of a terminology server.
    Extends CanonicalResource.
    """
    
    resourceType: str = "TerminologyCapabilities"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this terminology capabilities
    # Title
    title: Optional[str] = None  # Title for this terminology capabilities
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
    purpose: Optional[str] = None  # Why this terminology capabilities is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Kind
    kind: Optional[str] = None  # instance | capability | requirements (required, validated in __post_init__)
    # Software
    software: Optional[TerminologyCapabilitiesSoftware] = None  # Software that is covered
    # Implementation
    implementation: Optional[TerminologyCapabilitiesImplementation] = None  # Information about the installation
    # Locked Date
    lockedDate: Optional[bool] = None  # Whether lockedDate is supported
    # Code System
    codeSystem: List[TerminologyCapabilitiesCodeSystem] = field(default_factory=list)  # Information about code systems
    # Expansion
    expansion: Optional[TerminologyCapabilitiesExpansion] = None  # Information about the ValueSet expansion
    # Code Search
    codeSearch: Optional[str] = None  # explicit | all
    # Validate Code
    validateCode: Optional[TerminologyCapabilitiesValidateCode] = None  # Information about code validation
    # Translation
    translation: Optional[TerminologyCapabilitiesTranslation] = None  # Information about translation
    # Closure
    closure: Optional[TerminologyCapabilitiesClosure] = None  # Information about closure
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.kind is None:
            raise ValueError("TerminologyCapabilities.kind is required but was not provided")


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
