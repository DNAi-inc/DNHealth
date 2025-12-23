# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R5 resource definitions.

This module provides R5-specific resource classes and types.
R5 resources are designed to be compatible with R4 while supporting
R5-specific features and changes.
"""

from dnhealth.dnhealth_fhir.r5.base import (
    Resource as R5Resource,
    DomainResource as R5DomainResource,
    CanonicalResource as R5CanonicalResource,
    MetadataResource as R5MetadataResource,
    Meta as R5Meta,
    FHIRResource as R5FHIRResource,
)

# Import resources module for dynamic loading
try:
    from dnhealth.dnhealth_fhir.r5 import resources
except ImportError:
    # R5 resources not yet generated
    resources = None

__all__ = [
    "R5Resource",
    "R5DomainResource",
    "R5CanonicalResource",
    "R5MetadataResource",
    "R5Meta",
    "R5FHIRResource",
    "resources",
]
