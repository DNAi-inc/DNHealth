# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ChargeItemDefinition resource.

ChargeItemDefinition defines the characteristics of a charge item.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, ContactDetail, UsageContext, Period, Money, Quantity


@dataclass
class ChargeItemDefinitionApplicability:
    """
    FHIR ChargeItemDefinition.applicability complex type.
    
    Expressions that describe applicability criteria for the billing code.
    """
    
    description: Optional[str] = None  # Natural language description of the condition
    language: Optional[str] = None  # Language of the expression
    expression: Optional[str] = None  # Boolean-valued expression
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ChargeItemDefinitionPropertyGroup:
    """
    FHIR ChargeItemDefinition.propertyGroup complex type.
    
    Group of properties which are applicable under the same conditions.
    """
    
    applicability: List[ChargeItemDefinitionApplicability] = field(default_factory=list)  # Conditions under which the priceComponent is applicable
    priceComponent: List[Dict[str, Any]] = field(default_factory=list)  # Components of total line item price
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class ChargeItemDefinition(MetadataResource):
    """
    FHIR R4 ChargeItemDefinition resource.
    
    Defines the characteristics of a charge item.
    Extends MetadataResource.
    """
    
    resourceType: str = "ChargeItemDefinition"
    # URL
    url: str  # Canonical URL (required)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this charge item definition (inherited from CanonicalResource)
    # Derived From URI
    derivedFromUri: List[str] = field(default_factory=list)  # Underlying externally-defined charge item definition
    # Part Of
    partOf: List[str] = field(default_factory=list)  # A larger definition of which this particular definition is a component or step
    # Replaces
    replaces: List[str] = field(default_factory=list)  # Completed or terminated charge item definition
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
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # When last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When resource is valid (inherited from MetadataResource)
    # Code
    code: Optional[CodeableConcept] = None  # Billing code or product type this definition applies to
    # Instance
    instance: List[Reference] = field(default_factory=list)  # Instances this definition applies to
    # Applicability
    applicability: List[ChargeItemDefinitionApplicability] = field(default_factory=list)  # Whether or not the billing code is applicable
    # Property Group
    propertyGroup: List[ChargeItemDefinitionPropertyGroup] = field(default_factory=list)  # Group of properties which are applicable under the same conditions

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
