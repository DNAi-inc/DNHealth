# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Code System definitions.

Common code systems used for validation.
"""

import logging
from datetime import datetime
from typing import Dict, Set, Optional, List
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept

logger = logging.getLogger(__name__)


# Common FHIR code systems with their known codes
CODE_SYSTEMS: Dict[str, Set[str]] = {
    # Observation status code system
    "http://hl7.org/fhir/observation-status": {
        "registered", "preliminary", "final", "amended", "corrected",
        "cancelled", "entered-in-error", "unknown"
    },
    # Encounter status code system
    "http://hl7.org/fhir/encounter-status": {
        "planned", "arrived", "triaged", "in-progress", "onleave",
        "finished", "cancelled", "entered-in-error", "unknown"
    },
    # Administrative gender code system
    "http://hl7.org/fhir/administrative-gender": {
        "male", "female", "other", "unknown"
    },
    # Condition clinical status code system
    "http://terminology.hl7.org/CodeSystem/condition-clinical": {
        "active", "recurrence", "relapse", "inactive", "remission",
        "resolved", "unknown"
    },
    # Condition verification status code system
    "http://terminology.hl7.org/CodeSystem/condition-ver-status": {
        "unconfirmed", "provisional", "differential", "confirmed",
        "refuted", "entered-in-error", "unknown"
    },
    # Bundle type code system
    "http://hl7.org/fhir/bundle-type": {
        "document", "message", "transaction", "transaction-response",
        "batch", "batch-response", "history", "searchset", "collection"
    },
    # Operation outcome issue severity code system
    "http://hl7.org/fhir/issue-severity": {
        "fatal", "error", "warning", "information"
    },
    # Operation outcome issue code system
    "http://hl7.org/fhir/issue-type": {
        "invalid", "structure", "required", "value", "invariant",
        "security", "login", "unknown", "expired", "forbidden",
        "suppressed", "processing", "not-supported", "duplicate",
        "multiple-matches", "not-found", "too-long", "code-invalid",
        "extension", "too-costly", "business-rule", "conflict",
        "transient", "lock-error", "no-store", "exception",
        "timeout", "incomplete", "throttled", "informational"
    },
    # LOINC (commonly used for observations)
    "http://loinc.org": set(),  # Empty set means we don't validate specific codes, just that system is recognized
    # SNOMED CT (commonly used for conditions)
    "http://snomed.info/sct": set(),  # Empty set means we don't validate specific codes
    # ICD-10
    "http://hl7.org/fhir/sid/icd-10": set(),
    # ICD-10-CM
    "http://hl7.org/fhir/sid/icd-10-cm": set(),
    # ICD-10-PCS
    "http://www.icd10data.com/icd10pcs": set(),
    # CPT
    "http://www.ama-assn.org/go/cpt": set(),
    # RxNorm
    "http://www.nlm.nih.gov/research/umls/rxnorm": set(),
    # UCUM (units of measure)
    "http://unitsofmeasure.org": set(),
}


def get_code_system(system_url: str) -> Optional[Set[str]]:
    """
    Get a code system by URL.
    
    Args:
        system_url: Code system URL
        
    Returns:
        Set of valid codes, or None if code system not found.
        Empty set means system is recognized but codes are not validated.
    """
    return CODE_SYSTEMS.get(system_url)


def is_code_system_recognized(system_url: str) -> bool:
    """
    Check if a code system URL is recognized.
    
    Args:
        system_url: Code system URL
        
    Returns:
        True if code system is recognized, False otherwise
    """
    return system_url in CODE_SYSTEMS


def is_code_in_code_system(code: str, system_url: str) -> bool:
    """
    Check if a code is in a code system.
    
    Args:
        code: Code to check
        system_url: Code system URL
        
    Returns:
        True if code is in code system, False otherwise.
        Returns True if code system is recognized but has empty code set (codes not validated).
    """
    code_system = get_code_system(system_url)
    if code_system is None:
        return False
    
    # If code system has empty set, it means we recognize the system but don't validate codes
    if len(code_system) == 0:
        return True

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    return code in code_system


def validate_coding_code_system(coding: Coding) -> List[str]:
    """
    Validate a Coding's code against its code system.
    
    Args:
        coding: Coding to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if not coding.system:
        # No system specified - this is allowed in FHIR, but we can't validate
        return errors
    
    if not coding.code:
        # No code specified - this is allowed in FHIR
        return errors
    
    # Check if code system is recognized
    if not is_code_system_recognized(coding.system):
        # Code system not recognized - this is a warning, not an error
        # In a real implementation, you might want to check against external terminology servers
        return errors
    
    # Check if code is in code system
    if not is_code_in_code_system(coding.code, coding.system):
        errors.append(
            f"Code '{coding.code}' is not valid in code system '{coding.system}'"
        )

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def validate_codeable_concept_code_systems(concept: CodeableConcept) -> List[str]:
    """
    Validate a CodeableConcept's codings against their code systems.
    
    Args:
        concept: CodeableConcept to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if not concept.coding:
        # No codings to validate
        return errors
    
    for i, coding in enumerate(concept.coding):
        coding_errors = validate_coding_code_system(coding)
        for error in coding_errors:
            errors.append(f"Coding[{i}]: {error}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] CodeableConcept code system validation completed")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors

