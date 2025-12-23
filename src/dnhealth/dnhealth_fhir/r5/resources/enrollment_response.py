# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 EnrollmentResponse resource.

This resource provides enrollment and plan details from the processing of an EnrollmentRequest resource.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Identifier, Reference
from typing import List, Optional

@dataclass
class EnrollmentResponse(FHIRResource):
    """
    This resource provides enrollment and plan details from the processing of an EnrollmentRequest resource.
    """

    resourceType: str = "EnrollmentResponse"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The Response business identifier.
    status: Optional[str] = None  # The status of the resource instance.
    request: Optional[Reference] = None  # Original request resource reference.
    outcome: Optional[str] = None  # Processing status: error, complete.
    disposition: Optional[str] = None  # A description of the status of the adjudication.
    created: Optional[str] = None  # The date when the enclosed suite of services were performed or completed.
    organization: Optional[Reference] = None  # The Insurer who produced this adjudicated response.
    requestProvider: Optional[Reference] = None  # The practitioner who is responsible for the services rendered to the patient.