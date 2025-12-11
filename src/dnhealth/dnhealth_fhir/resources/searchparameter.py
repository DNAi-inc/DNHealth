# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 SearchParameter resource.

SearchParameter defines a search parameter that can be used to search for resources.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class SearchParameterComponent:
    """
    FHIR SearchParameter.component complex type.
    
    Used to define the parts of a composite search parameter.
    """
    
    definition: str  # Canonical URL to another search parameter (required)
    expression: Optional[str] = None  # Sub-expression within the expression
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class SearchParameter(CanonicalResource):
    """
    FHIR R4 SearchParameter resource.
    
    Defines a search parameter that can be used to search for resources.
    Extends CanonicalResource.
    """
    
    resourceType: str = "SearchParameter"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this search parameter (required, validated in __post_init__)
    # Title
    title: Optional[str] = None  # Title for this search parameter
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
    purpose: Optional[str] = None  # Why this search parameter is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Code
    code: Optional[str] = None  # Code used in URL (required, validated in __post_init__)
    # Base
    base: List[str] = field(default_factory=list)  # The resource type(s) this search parameter applies to (required)
    # Type
    type: Optional[str] = None  # number | date | string | token | reference | composite | quantity | uri | special (required, validated in __post_init__)
    # Expression
    expression: Optional[str] = None  # FHIRPath expression that extracts the values
    # XPath
    xpath: Optional[str] = None  # XPath that extracts the values
    # XPath Usage
    xpathUsage: Optional[str] = None  # normal | phonetic | nearby | distance | other
    # Target
    target: List[str] = field(default_factory=list)  # Types of resource (if a reference)
    # Multiple Or
    multipleOr: Optional[bool] = None  # Allow multiple values
    # Multiple And
    multipleAnd: Optional[bool] = None  # Allow multiple values (AND)
    # Comparator
    comparator: List[str] = field(default_factory=list)  # eq | ne | gt | lt | ge | le | sa | eb | ap
    # Modifier
    modifier: List[str] = field(default_factory=list)  # missing | exact | contains | not | text | in | not-in | below | above | type | identifier | ofType
    # Chain
    chain: List[str] = field(default_factory=list)  # Chained names supported
    # Component
    component: List[SearchParameterComponent] = field(default_factory=list)  # For composite parameters
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.name is None:
            raise ValueError("SearchParameter.name is required but was not provided")
        if self.code is None:
            raise ValueError("SearchParameter.code is required but was not provided")
        if self.type is None:
            raise ValueError("SearchParameter.type is required but was not provided")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")


def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()
