# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Code validation utilities.

Provides functions to validate codes against ValueSets and CodeSystems.
"""

from typing import List, Optional, Set, Tuple
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.valueset_resource import ValueSet, get_codes_from_valueset
from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystem, get_codes_from_codesystem
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept

logger = logging.getLogger(__name__)


def validate_code_against_valueset(
    code: str,
    valueset: ValueSet,    system: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate a code against a ValueSet resource.
    
    Args:
        code: Code to validate
        valueset: ValueSet resource
        system: Optional code system URL to filter by
        
    Returns:
        Tuple of (is_valid, error_message)
        is_valid: True if code is valid, False otherwise
        error_message: Error message if invalid, None if valid
    """
    if not code:
        return False, "Code is empty"
    
    # Get all codes from the ValueSet
    codes = get_codes_from_valueset(valueset)
    
    # If ValueSet has compose, check if code system matches
    if valueset.compose and system:
        # Check if the system is included in compose
        system_found = False
        for include in valueset.compose.include:
            if include.system == system:
                system_found = True
                # Check if code is in this include
                for concept in include.concept:
                    if concept.code == code:
                        return True, None
                # Code system matches but code not found in concepts
                return False, f"Code '{code}' not found in code system '{system}'"
        
        if not system_found:
            return False, f"Code system '{system}' not found in ValueSet"
    
    # Check if code is in the ValueSet
    if code in codes:
        return True, None
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return False, f"Code '{code}' is not in ValueSet '{valueset.url or 'unknown'}'"


def validate_coding_against_valueset(
    coding: Coding,
    valueset: ValueSet
) -> Tuple[bool, Optional[str]]:
    """
    Validate a Coding against a ValueSet resource.
    
    Args:
        coding: Coding to validate
        valueset: ValueSet resource
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not coding.code:
        return False, "Coding.code is empty"
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return validate_code_against_valueset(
        coding.code,
        valueset,
        system=coding.system
    )


def validate_codeable_concept_against_valueset(
    concept: CodeableConcept,
    valueset: ValueSet
) -> Tuple[bool, Optional[str]]:
    """
    Validate a CodeableConcept against a ValueSet resource.
    
    A CodeableConcept is valid if at least one Coding is valid.
    
    Args:
        concept: CodeableConcept to validate
        valueset: ValueSet resource
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not concept.coding:
        return False, "CodeableConcept has no codings"
    
    errors = []
    for coding in concept.coding:
        is_valid, error = validate_coding_against_valueset(coding, valueset)
        if is_valid:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
            return True, None
        if error:
            errors.append(error)
    
    # None of the codings are valid
    error_msg = f"None of the codings are valid: {', '.join(errors)}"
    return False, error_msg


def validate_code_against_codesystem(
    code: str,
    codesystem: CodeSystem,
    system: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate a code against a CodeSystem resource.
    
    Args:
        code: Code to validate
        codesystem: CodeSystem resource
        system: Optional code system URL to verify matches
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not code:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        return False, "Code is empty"
    
    # Verify system matches if provided
    if system and codesystem.url and codesystem.url != system:
        return False, f"Code system '{system}' does not match CodeSystem URL '{codesystem.url}'"
    
    # Get all codes from the CodeSystem
    codes = get_codes_from_codesystem(codesystem)
    
    # Check if code is in the CodeSystem
    if code in codes:
        return True, None
    
    return False, f"Code '{code}' is not in CodeSystem '{codesystem.url or 'unknown'}'"


def validate_coding_against_codesystem(
    coding: Coding,
    codesystem: CodeSystem
) -> Tuple[bool, Optional[str]]:
    """
    Validate a Coding against a CodeSystem resource.

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    Args:
        coding: Coding to validate
        codesystem: CodeSystem resource
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not coding.code:
        return False, "Coding.code is empty"
    
    return validate_code_against_codesystem(
        coding.code,
        codesystem,
        system=coding.system
    )


def validate_codeable_concept_against_codesystem(
    concept: CodeableConcept,
    codesystem: CodeSystem
) -> Tuple[bool, Optional[str]]:
    """
    Validate a CodeableConcept against a CodeSystem resource.
    
    A CodeableConcept is valid if at least one Coding is valid.
    
    Args:
        concept: CodeableConcept to validate
        codesystem: CodeSystem resource

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not concept.coding:
        return False, "CodeableConcept has no codings"
    
    errors = []
    for coding in concept.coding:
        is_valid, error = validate_coding_against_codesystem(coding, codesystem)
        if is_valid:
            return True, None
        if error:
            errors.append(error)
    
    # None of the codings are valid
    error_msg = f"None of the codings are valid: {', '.join(errors)}"
    return False, error_msg


def get_validation_errors(
    code: str,
    valueset: Optional[ValueSet] = None,
    codesystem: Optional[CodeSystem] = None,
    system: Optional[str] = None
) -> List[str]:
    """
    Get validation errors for a code against ValueSet and/or CodeSystem.
    
    Args:
        code: Code to validate
        valueset: Optional ValueSet resource
        codesystem: Optional CodeSystem resource
        system: Optional code system URL
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if valueset:
        is_valid, error = validate_code_against_valueset(code, valueset, system=system)
        if not is_valid and error:
            errors.append(f"ValueSet validation: {error}")
    
    if codesystem:
        is_valid, error = validate_code_against_codesystem(code, codesystem, system=system)
        if not is_valid and error:
            errors.append(f"CodeSystem validation: {error}")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Code validation completed: {len(errors)} errors found")
    
    return errors

