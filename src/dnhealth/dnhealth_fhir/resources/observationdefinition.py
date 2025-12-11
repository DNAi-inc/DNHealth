# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 ObservationDefinition resource.

ObservationDefinition defines the characteristics of an observation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    ContactDetail,
    UsageContext,
    RelatedArtifact,
    Quantity,
)


@dataclass
class ObservationDefinitionQuantitativeDetails:
    """
    FHIR ObservationDefinition.quantitativeDetails complex type.
    
    Characteristics for quantitative results.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    customaryUnit: Optional[CodeableConcept] = None  # Customary unit for quantitative results
    unit: Optional[CodeableConcept] = None  # SI unit for quantitative results
    conversionFactor: Optional[float] = None  # SI to Customary unit conversion factor
    decimalPrecision: Optional[int] = None  # Decimal precision of observation quantitative results


@dataclass
class ObservationDefinitionQualifiedInterval:
    """
    FHIR ObservationDefinition.qualifiedInterval complex type.
    
    Qualified range for continuous and ordinal observation results.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    category: Optional[str] = None  # reference | critical | absolute
    range: Optional[Any] = None  # The interval itself, for continuous or ordinal observations (Range)
    context: Optional[CodeableConcept] = None  # Range context qualifier
    appliesTo: List[CodeableConcept] = field(default_factory=list)  # Targetted population of the range
    gender: Optional[str] = None  # male | female | other | unknown
    age: Optional[Any] = None  # Applicable age range (Range)
    gestationalAge: Optional[Any] = None  # Applicable gestational age range (Range)
    condition: Optional[str] = None  # Condition associated with the reference range


@dataclass
class ObservationDefinition(MetadataResource):
    """
    FHIR R4 ObservationDefinition resource.
    
    Defines the characteristics of an observation.
    Extends MetadataResource.
    """
    
    resourceType: str = "ObservationDefinition"
    # URL
    url: Optional[str] = None  # Canonical URL (inherited from CanonicalResource)
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Additional identifiers (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: Optional[str] = None  # Name for this observation definition (inherited from CanonicalResource)
    # Title
    title: Optional[str] = None  # Title for this observation definition (inherited from CanonicalResource)
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
    purpose: Optional[str] = None  # Why this observation definition is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the observation definition was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the observation definition is expected to be in use (inherited from MetadataResource)
    # Derived From Canonical
    derivedFromCanonical: List[str] = field(default_factory=list)  # Based on FHIR definition of another observation (canonical references)
    # Derived From URI
    derivedFromUri: List[str] = field(default_factory=list)  # Based on external definition of another observation (URIs)
    # Subject CodeableConcept
    subjectCodeableConcept: Optional[CodeableConcept] = None  # Type of subject for the observation
    # Subject Reference
    subjectReference: Optional[Reference] = None  # Type of subject for the observation
    # Permitted Data Type
    permittedDataType: List[str] = field(default_factory=list)  # Quantity | CodeableConcept | string | boolean | integer | Range | Ratio | SampledData | time | dateTime | Period
    # Multiple Results Allowed
    multipleResultsAllowed: Optional[bool] = None  # Multiple results allowed
    # Body Site
    bodySite: Optional[CodeableConcept] = None  # Body part to be observed
    # Method
    method: Optional[CodeableConcept] = None  # Method used to produce the observation
    # Specimen
    specimen: List[Reference] = field(default_factory=list)  # Kind of specimen used by this type of observation
    # Device
    device: List[Reference] = field(default_factory=list)  # Measurement device
    # Preferred Report Name
    preferredReportName: Optional[str] = None  # Preferred name to use in report
    # Quantitative Details
    quantitativeDetails: Optional[ObservationDefinitionQuantitativeDetails] = None  # Characteristics for quantitative results
    # Qualified Interval
    qualifiedInterval: List[ObservationDefinitionQualifiedInterval] = field(default_factory=list)  # Qualified range for continuous and ordinal observation results
    # Valid Coded Value Set
    validCodedValueSet: Optional[Reference] = None  # Value set of valid coded values for the observations conforming to this ObservationDefinition
    # Normal Coded Value Set
    normalCodedValueSet: Optional[Reference] = None  # Value set of normal coded values for the observations conforming to this ObservationDefinition
    # Abnormal Coded Value Set
    abnormalCodedValueSet: Optional[Reference] = None  # Value set of abnormal coded values for the observations conforming to this ObservationDefinition
    # Critical Coded Value Set
    criticalCodedValueSet: Optional[Reference] = None  # Value set of critical coded values for the observations conforming to this ObservationDefinition

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
