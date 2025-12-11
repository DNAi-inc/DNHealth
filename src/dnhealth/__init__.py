# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
DNHealth: Production-grade Python library for HL7v2, HL7v3, and FHIR R4.

This package provides complete read/write support for healthcare integration standards.
"""

__version__ = "0.1.0"

from dnhealth.errors import (
    DNHealthError,
    HL7v2ParseError,
    HL7v3ParseError,
    FHIRParseError,
    FHIRValidationError,
)

__all__ = [
    "__version__",
    "DNHealthError",
    "HL7v2ParseError",
    "HL7v3ParseError",
    "FHIRParseError",
    "FHIRValidationError",
]

