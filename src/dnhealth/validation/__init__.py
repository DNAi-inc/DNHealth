# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Official HL7/FHIR Validation Module.

Provides validation functions that compare implemented features with official
definitions from HL7Documentation/definitions.json.
"""

from .official_validation import (
    validate_hl7v2_tables_against_official,
    validate_hl7v3_codesystems_against_official,
    validate_valuesets_against_official,
    validate_profiles_against_official,
    validate_search_parameters_against_official,
    validate_extensions_against_official,
    run_official_test_cases,
    validate_internationalization,
    run_all_official_validations,
    get_current_time,
    OPERATION_TIMEOUT
)

__all__ = [
    "validate_hl7v2_tables_against_official",
    "validate_hl7v3_codesystems_against_official",
    "validate_valuesets_against_official",
    "validate_profiles_against_official",
    "validate_search_parameters_against_official",
    "validate_extensions_against_official",
    "run_official_test_cases",
    "validate_internationalization",
    "run_all_official_validations",
    "get_current_time",
    "OPERATION_TIMEOUT"
]
