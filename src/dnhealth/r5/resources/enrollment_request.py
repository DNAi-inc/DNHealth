# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 EnrollmentRequest resource.

This resource provides the insurance enrollment details to the insurer regarding a specified coverage.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Identifier, Reference
from typing import List, Optional

@dataclass
class EnrollmentRequest(FHIRResource):
    """
    This resource provides the insurance enrollment details to the insurer regarding a specified coverage.
    """

    resourceType: str = "EnrollmentRequest"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # The Response business identifier.
    status: Optional[str] = None  # The status of the resource instance.
    created: Optional[str] = None  # The date when this resource was created.
    insurer: Optional[Reference] = None  # The Insurer who is target  of the request.
    provider: Optional[Reference] = None  # The practitioner who is responsible for the services rendered to the patient.
    candidate: Optional[Reference] = None  # Patient Resource.
    coverage: Optional[Reference] = None  # Reference to the program or plan identification, underwriter or payor.
