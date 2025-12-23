# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Resource resource.

This is the base resource type for everything.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from typing import List, Optional

@dataclass
class Resource(FHIRResource):
    """
    This is the base resource type for everything.
    """

    resourceType: str = "Resource"