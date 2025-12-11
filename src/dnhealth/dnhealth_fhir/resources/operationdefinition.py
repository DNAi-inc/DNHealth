# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 OperationDefinition resource.

OperationDefinition defines a named operation that can be invoked on a resource.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import CanonicalResource
from dnhealth.dnhealth_fhir.types import Extension, CodeableConcept, Reference, ContactDetail, UsageContext
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class OperationDefinitionParameter:
    """
    FHIR OperationDefinition.parameter complex type.
    
    Parameters for the operation.
    """
    
    name: str  # Name in Parameters.parameter.name or Parameters.parameter.part.name (required)
    use: str  # in | out (required)
    min: int  # Minimum cardinality (required)
    max: str  # Maximum cardinality (required)
    documentation: Optional[str] = None  # Description of meaning/use
    type: Optional[str] = None  # What type this parameter has
    targetProfile: List[str] = field(default_factory=list)  # Profile on the type
    searchType: Optional[str] = None  # number | date | string | token | reference | composite | quantity | uri | special
    binding: Optional[Dict[str, Any]] = None  # ValueSet details if this is a coded parameter
    referencedFrom: List[Dict[str, Any]] = field(default_factory=list)  # References to this parameter
    part: List["OperationDefinitionParameter"] = field(default_factory=list)  # Parts of a nested parameter
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class OperationDefinitionOverload:
    """
    FHIR OperationDefinition.overload complex type.
    
    Define overloaded variants for when generating code.
    """
    
    parameterName: List[str] = field(default_factory=list)  # Name of parameter to include in overload
    comment: Optional[str] = None  # Comments to go on overload
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class OperationDefinition(CanonicalResource):
    """
    FHIR R4 OperationDefinition resource.
    
    Defines a named operation that can be invoked on a resource.
    Extends CanonicalResource.
    """
    
    resourceType: str = "OperationDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this operation definition (required, validated in __post_init__)
    # Title
    title: Optional[str] = None  # Title for this operation definition
    # Status
    status: Optional[str] = None  # draft | active | retired | unknown (inherited from CanonicalResource)
    # Kind
    kind: Optional[str] = None  # operation | query (required, validated in __post_init__)
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
    purpose: Optional[str] = None  # Why this operation definition is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Affects State
    affectsState: Optional[bool] = None  # Whether content is changed by the operation
    # Code
    code: Optional[str] = None  # Name used to invoke the operation (required, validated in __post_init__)
    # Comment
    comment: Optional[str] = None  # Additional information about use
    # Base
    base: Optional[str] = None  # Marks this as a profile of the base
    # Resource
    resource: List[str] = field(default_factory=list)  # Types this operation applies to
    # System
    system: Optional[bool] = None  # Invoke at the system level (required, validated in __post_init__)
    # Type
    type: Optional[bool] = None  # Invoke at the type level (required, validated in __post_init__)
    # Instance
    instance: Optional[bool] = None  # Invoke on an instance (required, validated in __post_init__)
    # Input Profile
    inputProfile: Optional[str] = None  # Validation information for in parameters
    # Output Profile
    outputProfile: Optional[str] = None  # Validation information for out parameters
    # Parameter
    parameter: List[OperationDefinitionParameter] = field(default_factory=list)  # Parameters for the operation
    # Overload
    overload: List[OperationDefinitionOverload] = field(default_factory=list)  # Define overloaded variants
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.name is None:
            raise ValueError("OperationDefinition.name is required but was not provided")
        if self.kind is None:
            raise ValueError("OperationDefinition.kind is required but was not provided")
        if self.code is None:
            raise ValueError("OperationDefinition.code is required but was not provided")
        if self.system is None:
            raise ValueError("OperationDefinition.system is required but was not provided")
        if self.type is None:
            raise ValueError("OperationDefinition.type is required but was not provided")
        if self.instance is None:
            raise ValueError("OperationDefinition.instance is required but was not provided")


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
