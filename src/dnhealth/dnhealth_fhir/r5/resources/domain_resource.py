# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DomainResource resource.

A resource that includes narrative, extensions, and contained resources.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from typing import List, Optional

@dataclass
class DomainResource(FHIRResource):
    """
    A resource that includes narrative, extensions, and contained resources.
    """

    resourceType: str = "DomainResource"