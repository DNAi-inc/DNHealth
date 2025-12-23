# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Parameters resource.

This resource is used to pass information into and back from an operation (whether invoked directly from REST or within a messaging environment).  It is not persisted or allowed to be referenced by other resources except as described in the definition of the Parameters resource.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta, Resource
from dnhealth.dnhealth_fhir.types import Address, Age, Annotation, Attachment, BackboneElement, CodeableConcept, Coding, ContactDetail, ContactPoint, Count, DataRequirement, Distance, Dosage, Duration, Expression, Extension, HumanName, Identifier, Money, ParameterDefinition, Period, Quantity, Range, Ratio, Reference, RelatedArtifact, SampledData, Signature, Timing, TriggerDefinition, UsageContext
from typing import Any, List, Optional

@dataclass
class ParametersParameter:
    """
    ParametersParameter nested class.
    """

    name: Optional[str] = None  # The name of the parameter (reference to the operation definition).
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # Conveys the content if the parameter is a data type.
    resource: Optional[Resource] = None  # Conveys the content if the parameter is a whole resource.
    part: Optional[List[Any]] = field(default_factory=list)  # A named part of a multi-part parameter.


@dataclass
class Parameters(FHIRResource):
    """
    This resource is used to pass information into and back from an operation (whether invoked directly from REST or within a messaging environment).  It is not persisted or allowed to be referenced by other resources except as described in the definition of the Parameters resource.
    """

    resourceType: str = "Parameters"
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # A parameter passed to or received from the operation.