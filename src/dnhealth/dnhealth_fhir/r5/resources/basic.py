# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Basic resource.

Basic is used for handling concepts not yet defined in FHIR, narrative-only resources that don't map to an existing resource, and custom resources not appropriate for inclusion in the FHIR specification.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Reference
from typing import List, Optional

@dataclass
class Basic(FHIRResource):
    """
    Basic is used for handling concepts not yet defined in FHIR, narrative-only resources that don't map to an existing resource, and custom resources not appropriate for inclusion in the FHIR specification.
    """

    code: Optional[CodeableConcept] = None  # Identifies the 'type' of resource - equivalent to the resource name for other resources.
    resourceType: str = "Basic"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier assigned to the resource for business purposes, outside the context of FHIR.
    subject: Optional[Reference] = None  # Identifies the patient, practitioner, device or any other resource that is the \"focus\" of this ...
    created: Optional[str] = None  # Identifies when the resource was first created.
    author: Optional[Reference] = None  # Indicates who was responsible for creating the resource instance.