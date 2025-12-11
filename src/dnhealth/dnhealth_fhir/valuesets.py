# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Value Set definitions.

Common value sets used for validation.
"""

import logging
from datetime import datetime
from typing import Dict, Set, Optional, List
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept

logger = logging.getLogger(__name__)


# Common FHIR value sets
VALUE_SETS: Dict[str, Set[str]] = {
    # Observation status
    "http://hl7.org/fhir/ValueSet/observation-status": {
        "registered", "preliminary", "final", "amended", "corrected",
        "cancelled", "entered-in-error", "unknown"
    },
    # Encounter status
    "http://hl7.org/fhir/ValueSet/encounter-status": {
        "planned", "arrived", "triaged", "in-progress", "onleave",
        "finished", "cancelled", "entered-in-error", "unknown"
    },
    # Administrative gender
    "http://hl7.org/fhir/ValueSet/administrative-gender": {
        "male", "female", "other", "unknown"
    },
    # Condition clinical status
    "http://terminology.hl7.org/ValueSet/condition-clinical": {
        "active", "recurrence", "relapse", "inactive", "remission",
        "resolved", "unknown"
    },
    # Condition verification status
    "http://terminology.hl7.org/ValueSet/condition-ver-status": {
        "unconfirmed", "provisional", "differential", "confirmed",
        "refuted", "entered-in-error", "unknown"
    },
    # Bundle type
    "http://hl7.org/fhir/ValueSet/bundle-type": {
        "document", "message", "transaction", "transaction-response",
        "batch", "batch-response", "history", "searchset", "collection"
    },
    # Operation outcome issue severity
    "http://hl7.org/fhir/ValueSet/issue-severity": {
        "fatal", "error", "warning", "information"
    },
    # Operation outcome issue code
    "http://hl7.org/fhir/ValueSet/issue-type": {
        "invalid", "structure", "required", "value", "invariant",
        "security", "login", "unknown", "expired", "forbidden",
        "suppressed", "processing", "not-supported", "duplicate",
        "multiple-matches", "not-found", "too-long", "code-invalid",
        "extension", "too-costly", "business-rule", "conflict",
        "transient", "lock-error", "no-store", "exception",
        "timeout", "incomplete", "throttled", "informational"
    },
}

# Field to value set mappings for common fields
FIELD_VALUE_SET_MAP: Dict[str, Dict[str, str]] = {
    "Observation": {
        "status": "http://hl7.org/fhir/ValueSet/observation-status",
    },
    "Encounter": {
        "status": "http://hl7.org/fhir/ValueSet/encounter-status",
    },
    "Patient": {
        "gender": "http://hl7.org/fhir/ValueSet/administrative-gender",
    },
    "Condition": {
        "clinicalStatus": "http://terminology.hl7.org/ValueSet/condition-clinical",
        "verificationStatus": "http://terminology.hl7.org/ValueSet/condition-ver-status",
    },
    "Bundle": {
        "type": "http://hl7.org/fhir/ValueSet/bundle-type",
    },
    "OperationOutcome": {
        "issue.severity": "http://hl7.org/fhir/ValueSet/issue-severity",
        "issue.code": "http://hl7.org/fhir/ValueSet/issue-type",
    },
}



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def get_value_set(url: str) -> Optional[Set[str]]:
    """
    Get a value set by URL.
    
    Args:
        url: Value set URL
        
    Returns:
        Set of valid codes, or None if value set not found
    """
    return VALUE_SETS.get(url)


def is_code_in_value_set(code: str, value_set_url: str) -> bool:
    """
    Check if a code is in a value set.
    
    Args:
        code: Code to check
        value_set_url: Value set URL
        
    Returns:
        True if code is in value set, False otherwise
    """
    value_set = get_value_set(value_set_url)
    if value_set is None:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        return False
    return code in value_set


def validate_coding_against_value_set(coding: Coding, value_set_url: str) -> List[str]:
    """
    Validate a Coding against a value set.
    
    Args:
        coding: Coding to validate
        value_set_url: Value set URL
        
    Returns:
        List of validation error messages (empty if valid)
    """
    start_time = datetime.now()
    errors = []
    
    if not coding.code:
        # Log completion timestamp at end of operation
        completion_time = datetime.now()
        current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Coding validation completed (no code to validate)")
        return errors  # No code to validate
    
    value_set = get_value_set(value_set_url)
    if value_set is None:
        # Value set not found - skip validation
        completion_time = datetime.now()
        current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Coding validation completed (value set not found)")
        return errors
    
    if coding.code not in value_set:
        errors.append(f"Code '{coding.code}' is not in value set '{value_set_url}'")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Coding validation completed in {elapsed:.3f} seconds ({len(errors)} errors)")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def validate_codeable_concept_against_value_set(concept: CodeableConcept, value_set_url: str) -> List[str]:
    """
    Validate a CodeableConcept against a value set.
    
    Args:
        concept: CodeableConcept to validate
        value_set_url: Value set URL
        
    Returns:
        List of validation error messages (empty if valid)
    """
    start_time = datetime.now()
    errors = []
    
    if not concept.coding:
        # No codings to validate
        completion_time = datetime.now()
        current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] CodeableConcept validation completed (no codings to validate)")
        return errors
    
    value_set = get_value_set(value_set_url)
    if value_set is None:
        # Value set not found - skip validation
        completion_time = datetime.now()
        current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] CodeableConcept validation completed (value set not found)")
        return errors
    
    # Check if at least one coding has a valid code
    valid_codes = []
    for coding in concept.coding:
        if coding.code and coding.code in value_set:
            valid_codes.append(coding.code)
    
    if not valid_codes:
        # None of the codings have valid codes
        codes = [c.code for c in concept.coding if c.code]
        if codes:
            errors.append(f"None of the codes {codes} are in value set '{value_set_url}'")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now()
    elapsed = (completion_time - start_time).total_seconds()
    current_time = completion_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] CodeableConcept validation completed in {elapsed:.3f} seconds ({len(errors)} errors)")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def get_field_value_set(resource_type: str, field_path: str) -> Optional[str]:
    """
    Get the value set URL for a field in a resource.
    
    Args:
        resource_type: Resource type (e.g., "Observation")
        field_path: Field path (e.g., "status" or "issue.severity")
        
    Returns:
        Value set URL, or None if not found
    """
    resource_map = FIELD_VALUE_SET_MAP.get(resource_type)
    if resource_map is None:
        return None
    return resource_map.get(field_path)

