# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Parameters resource.

Parameters resource is used to pass parameters to and from operations.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import Resource
from dnhealth.dnhealth_fhir.types import Extension
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class ParametersParameter:
    """
    FHIR Parameters.parameter complex type.
    
    A single parameter within a Parameters resource.
    """
    
    name: str  # Name of the parameter (required)
    valueBase64Binary: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueCanonical: Optional[str] = None
    valueCode: Optional[str] = None
    valueDate: Optional[str] = None
    valueDateTime: Optional[str] = None
    valueDecimal: Optional[float] = None
    valueId: Optional[str] = None
    valueInstant: Optional[str] = None
    valueInteger: Optional[int] = None
    valueMarkdown: Optional[str] = None
    valueOid: Optional[str] = None
    valuePositiveInt: Optional[int] = None
    valueString: Optional[str] = None
    valueTime: Optional[str] = None
    valueUnsignedInt: Optional[int] = None
    valueUri: Optional[str] = None
    valueUrl: Optional[str] = None
    valueUuid: Optional[str] = None
    valueAddress: Optional[Any] = None  # Address type
    valueAge: Optional[Any] = None  # Age type
    valueAnnotation: Optional[Any] = None  # Annotation type
    valueAttachment: Optional[Any] = None  # Attachment type
    valueCodeableConcept: Optional[Any] = None  # CodeableConcept type
    valueCoding: Optional[Any] = None  # Coding type
    valueContactPoint: Optional[Any] = None  # ContactPoint type
    valueCount: Optional[Any] = None  # Count type
    valueDistance: Optional[Any] = None  # Distance type
    valueDuration: Optional[Any] = None  # Duration type
    valueHumanName: Optional[Any] = None  # HumanName type
    valueIdentifier: Optional[Any] = None  # Identifier type
    valueMoney: Optional[Any] = None  # Money type
    valuePeriod: Optional[Any] = None  # Period type
    valueQuantity: Optional[Any] = None  # Quantity type
    valueRange: Optional[Any] = None  # Range type
    valueRatio: Optional[Any] = None  # Ratio type
    valueReference: Optional[Any] = None  # Reference type
    valueSampledData: Optional[Any] = None  # SampledData type
    valueSignature: Optional[Any] = None  # Signature type
    valueTiming: Optional[Any] = None  # Timing type
    valueContactDetail: Optional[Any] = None  # ContactDetail type
    valueContributor: Optional[Any] = None  # Contributor type
    valueDataRequirement: Optional[Any] = None  # DataRequirement type
    valueExpression: Optional[Any] = None  # Expression type
    valueParameterDefinition: Optional[Any] = None  # ParameterDefinition type
    valueRelatedArtifact: Optional[Any] = None  # RelatedArtifact type
    valueTriggerDefinition: Optional[Any] = None  # TriggerDefinition type
    valueUsageContext: Optional[Any] = None  # UsageContext type
    valueDosage: Optional[Any] = None  # Dosage type
    valueMeta: Optional[Any] = None  # Meta type
    resource: Optional[Any] = None  # Any FHIR resource
    part: List["ParametersParameter"] = field(default_factory=list)  # Nested parameters
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class Parameters(Resource):
    """
    FHIR R4 Parameters resource.
    
    Used to pass parameters to and from operations.
    Extends Resource (not DomainResource).
    """
    
    resourceType: str = "Parameters"
    parameter: List[ParametersParameter] = field(default_factory=list)
    
    def get_parameter(self, name: str) -> List[ParametersParameter]:
        """Get all parameters with the given name."""
        return [p for p in self.parameter if p.name == name]
    
    def get_parameter_value(self, name: str) -> Optional[Any]:
        """Get the first parameter value with the given name."""
        params = self.get_parameter(name)
        if not params:
            return None
        
        param = params[0]
        # Return the first non-None value field
        for attr_name in dir(param):
            if attr_name.startswith("value") and not attr_name.startswith("value_"):
                value = getattr(param, attr_name, None)
                if value is not None:
                    return value
        return None
    
    def has_parameter(self, name: str) -> bool:
        """Check if a parameter exists."""
        return any(p.name == name for p in self.parameter)

