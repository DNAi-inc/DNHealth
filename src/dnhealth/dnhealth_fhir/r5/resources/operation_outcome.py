# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 OperationOutcome resource.

A collection of error, warning, or information messages that result from a system action.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension
from typing import List, Optional

@dataclass
class OperationOutcomeIssue:
    """
    OperationOutcomeIssue nested class.
    """

    severity: Optional[str] = None  # Indicates whether the issue indicates a variation from successful processing.
    code: Optional[str] = None  # Describes the type of the issue. The system that creates an OperationOutcome SHALL choose the mos...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    details: Optional[CodeableConcept] = None  # Additional details about the error. This may be a text description of the error or a system code ...
    diagnostics: Optional[str] = None  # Additional diagnostic information about the issue.
    location: Optional[List[str]] = field(default_factory=list)  # This element is deprecated because it is XML specific. It is replaced by issue.expression, which ...
    expression: Optional[List[str]] = field(default_factory=list)  # A [simple subset of FHIRPath](fhirpath.html#simple) limited to element names, repetition indicato...


@dataclass
class OperationOutcome(FHIRResource):
    """
    A collection of error, warning, or information messages that result from a system action.
    """

    issue: List[BackboneElement] = field(default_factory=list)  # An error, warning, or information message that results from a system action.
    resourceType: str = "OperationOutcome"