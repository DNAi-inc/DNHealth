# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 GuidanceResponse resource.

A guidance response is the formal response to a guidance request, including any output parameters returned by the evaluation, as well as the description of any proposed actions to be taken.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, CodeableConcept, DataRequirement, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class GuidanceResponse(FHIRResource):
    """
    A guidance response is the formal response to a guidance request, including any output parameters returned by the evaluation, as well as the description of any proposed actions to be taken.
    """

    module: Optional[Any] = None  # An identifier, CodeableConcept or canonical reference to the guidance that was requested.
    status: Optional[str] = None  # The status of the response. If the evaluation is completed successfully, the status will indicate...
    resourceType: str = "GuidanceResponse"
    requestIdentifier: Optional[Identifier] = None  # The identifier of the request associated with this response. If an identifier was given as part o...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Allows a service to provide  unique, business identifiers for the response.
    subject: Optional[Reference] = None  # The patient for which the request was processed.
    encounter: Optional[Reference] = None  # The encounter during which this response was created or to which the creation of this record is t...
    occurrenceDateTime: Optional[str] = None  # Indicates when the guidance response was processed.
    performer: Optional[Reference] = None  # Provides a reference to the device that performed the guidance.
    reason: Optional[List[Any]] = field(default_factory=list)  # Describes the reason for the guidance response in coded or textual form, or Indicates the reason ...
    note: Optional[List[Annotation]] = field(default_factory=list)  # Provides a mechanism to communicate additional information about the response.
    evaluationMessage: Optional[Reference] = None  # Messages resulting from the evaluation of the artifact or artifacts. As part of evaluating the re...
    outputParameters: Optional[Reference] = None  # The output parameters of the evaluation, if any. Many modules will result in the return of specif...
    result: Optional[List[Reference]] = field(default_factory=list)  # The actions, if any, produced by the evaluation of the artifact.
    dataRequirement: Optional[List[DataRequirement]] = field(default_factory=list)  # If the evaluation could not be completed due to lack of information, or additional information wo...