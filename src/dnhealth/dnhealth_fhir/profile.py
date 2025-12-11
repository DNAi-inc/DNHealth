# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Profile conformance checking.

Validates that resources conform to StructureDefinition profiles.
"""

from typing import Dict, List, Optional, Set, Any
from datetime import datetime
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.structuredefinition import (
    StructureDefinition,
    ElementDefinition,
    get_element_definitions,
    get_element_by_path,
    get_required_fields,
)
from dnhealth.dnhealth_fhir.fhirpath import (
    FHIRPathConstraint,
    parse_constraint,
    validate_constraints,
    evaluate_fhirpath_expression,
)
from dnhealth.dnhealth_fhir.slicing import (
    parse_slicing_definition,
    validate_slicing,
    get_sliced_elements,
    apply_slicing_discriminator,
)
from dnhealth.dnhealth_fhir.terminology_service import (
    TerminologyService,
    BINDING_STRENGTH_REQUIRED,
    BINDING_STRENGTH_EXTENSIBLE,
    BINDING_STRENGTH_PREFERRED,
    BINDING_STRENGTH_EXAMPLE,
)
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


def check_profile_conformance(
    resource: FHIRResource,
    profile: StructureDefinition,    strict: bool = False
) -> List[str]:
    """
    Check if a resource conforms to a StructureDefinition profile.
    
    Args:
        resource: FHIR resource to validate
        profile: StructureDefinition profile to check against
        strict: If True, enforce all constraints strictly
        
    Returns:
        List of conformance error messages (empty if conformant)
    """
    errors = []
    
    # Check resource type matches
    if profile.type and resource.resourceType != profile.type:
        errors.append(
            f"Resource type '{resource.resourceType}' does not match profile type '{profile.type}'"
        )
        return errors  # Can't continue if type doesn't match
    
    # Get element definitions from profile
    elements = get_element_definitions(profile)
    if not elements:
        # No elements defined, basic conformance check
        return errors
    
    # Check required fields
    required_fields = get_required_fields(profile)
    for field_path in required_fields:
        if not _has_field(resource, field_path):
            errors.append(f"Required field '{field_path}' is missing")
    
    # Check cardinality constraints
    for element in elements:
        if element.path and element.min is not None:
            field_path = element.path
            if field_path == profile.type:
                continue  # Skip root element
            
            # Get field value
            field_value = _get_field_value(resource, field_path)
            
            # Check minimum cardinality
            if element.min > 0:
                if field_value is None or (isinstance(field_value, list) and len(field_value) == 0):
                    errors.append(
                        f"Field '{field_path}' has minimum cardinality {element.min}, but value is missing or empty"
                    )
            
            # Check maximum cardinality
            if element.max and element.max != "*":
                try:
                    max_value = int(element.max)
                    if isinstance(field_value, list) and len(field_value) > max_value:
                        errors.append(
                            f"Field '{field_path}' has maximum cardinality {max_value}, but found {len(field_value)} values"
                        )
                except ValueError:
                    pass  # Invalid max value, skip
    
    # Check fixed values if strict mode
    if strict:
        for element in elements:
            if element.path and _has_fixed_value(element):
                field_path = element.path
                if field_path == profile.type:
                    continue  # Skip root element
                
                field_value = _get_field_value(resource, field_path)
                fixed_value = _get_fixed_value(element)
                
                if field_value != fixed_value:
                    errors.append(
                        f"Field '{field_path}' has fixed value '{fixed_value}', but found '{field_value}'"
                    )
    
    # Check slicing constraints
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking slicing constraints for profile '{profile.url or profile.id}'")
    
    for element in elements:
        if element.path and element.slicing:
            field_path = element.path
            if field_path == profile.type:
                continue  # Skip root element
            
            # Parse slicing definition
            slicing_def = parse_slicing_definition(element)
            if slicing_def:
                field_value = _get_field_value(resource, field_path)
                slicing_errors = validate_slicing(resource, element, slicing_def, field_value, all_elements=elements)
                errors.extend(slicing_errors)
    
    # Check binding strength constraints
    logger.debug(f"[{current_time}] Checking binding strength constraints for profile '{profile.url or profile.id}'")
    
    terminology_service = TerminologyService()
    for element in elements:
        if element.path and element.binding:
            field_path = element.path
            if field_path == profile.type:
                continue  # Skip root element
            
            # Get binding strength
            binding_strength = None
            if isinstance(element.binding, dict):
                binding_strength = element.binding.get("strength")
                value_set_url = element.binding.get("valueSet")
            else:
                continue
            
            if binding_strength and value_set_url:
                field_value = _get_field_value(resource, field_path)
                binding_errors = _validate_binding_strength(
                    resource, field_path, field_value, binding_strength, value_set_url, terminology_service
                )
                errors.extend(binding_errors)
    
    # Check FHIRPath constraints
    logger.debug(f"[{current_time}] Checking FHIRPath constraints for profile '{profile.url or profile.id}'")
    
    for element in elements:
        if element.path and element.constraint:
            field_path = element.path
            if field_path == profile.type:
                continue  # Skip root element
            
            # Parse and validate constraints
            for constraint_data in element.constraint:
                try:
                    constraint = parse_constraint(constraint_data)
                    if constraint.expression:
                        # Evaluate constraint
                        field_value = _get_field_value(resource, field_path)
                        is_valid, error_msg = _validate_fhirpath_constraint(
                            constraint, resource, field_value, field_path
                        )
                        if not is_valid:
                            if constraint.severity == "error":
                                errors.append(error_msg)
                            elif constraint.severity == "warning":
                                logger.warning(f"[{current_time}] {error_msg}")
                except Exception as e:
                    logger.warning(f"[{current_time}] Error evaluating constraint on '{field_path}': {str(e)}")
    
    # Log completion with current timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Profile conformance check completed with {len(errors)} errors")
    return errors


def _has_field(resource: FHIRResource, field_path: str) -> bool:
    """
    Check if a resource has a field at the given path.
    
    Args:
        resource: FHIR resource
        field_path: Field path (e.g., "Patient.name")
        
    Returns:
        True if field exists, False otherwise
    """
    # Remove resource type prefix if present
    if "." in field_path:
        parts = field_path.split(".", 1)
        if parts[0] == resource.resourceType:
            field_path = parts[1]
    
    # Check if field exists
    return hasattr(resource, field_path)


def _get_field_value(resource: FHIRResource, field_path: str) -> Any:
    """
    Get field value from resource by path.
    
    Args:
        resource: FHIR resource
        field_path: Field path (e.g., "Patient.name")
        
    Returns:
        Field value or None
    """
    # Remove resource type prefix if present
    if "." in field_path:
        parts = field_path.split(".", 1)
        if parts[0] == resource.resourceType:
            field_path = parts[1]
    
    # Get field value
    if hasattr(resource, field_path):
        return getattr(resource, field_path)
    return None


def _has_fixed_value(element: ElementDefinition) -> bool:
    """
    Check if an element has a fixed value.
    
    Args:
        element: ElementDefinition
        
    Returns:
        True if element has fixed value, False otherwise
    """
    # Check all fixed value fields
    fixed_fields = [
        "fixedString", "fixedBoolean", "fixedInteger", "fixedDecimal",
        "fixedDate", "fixedDateTime", "fixedUri", "fixedCode"
    ]
    for field in fixed_fields:
        if hasattr(element, field) and getattr(element, field) is not None:
            return True

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return False


def _get_fixed_value(element: ElementDefinition) -> Any:
    """
    Get fixed value from element definition.
    
    Args:
        element: ElementDefinition
        
    Returns:
        Fixed value or None
    """
    # Check all fixed value fields in order
    fixed_fields = [
        "fixedString", "fixedBoolean", "fixedInteger", "fixedDecimal",
        "fixedDate", "fixedDateTime", "fixedUri", "fixedCode"
    ]

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
    for field in fixed_fields:
        if hasattr(element, field):
            value = getattr(element, field)
            if value is not None:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
                return value
    return None


def validate_against_profile(
    resource: FHIRResource,
    profile_url: str,
    profiles: Dict[str, StructureDefinition]
) -> List[str]:
    """
    Validate a resource against a profile by URL.
    
    Args:
        resource: FHIR resource to validate
        profile_url: Profile URL
        profiles: Dictionary mapping profile URLs to StructureDefinition objects
        
    Returns:
        List of validation error messages (empty if valid)
    """
    profile = profiles.get(profile_url)
    if not profile:
        return [f"Profile '{profile_url}' not found"]
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return check_profile_conformance(resource, profile)


def get_profile_constraints(profile: StructureDefinition) -> Dict[str, Any]:
    """
    Get constraints from a profile.
    
    Args:
        profile: StructureDefinition profile
        
    Returns:
        Dictionary of constraints by element path
    """
    constraints = {}
    elements = get_element_definitions(profile)
    
    for element in elements:
        if element.path:
            element_constraints = {}
            

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
            if element.min is not None:
                element_constraints["min"] = element.min
            if element.max:
                element_constraints["max"] = element.max
            if element.mustSupport:
                element_constraints["mustSupport"] = element.mustSupport
            if element.isModifier:
                element_constraints["isModifier"] = element.isModifier
            if element.binding:
                element_constraints["binding"] = element.binding
            if element.constraint:
                element_constraints["constraint"] = element.constraint
            
            if element_constraints:
                constraints[element.path] = element_constraints
    
    return constraints


def _validate_fhirpath_constraint(
    constraint: FHIRPathConstraint,
    resource: Any,
    field_value: Any,
    field_path: str
) -> tuple[bool, Optional[str]]:
    """
    Validate a FHIRPath constraint against a field value.
    
    Args:
        constraint: FHIRPathConstraint to validate
        resource: FHIR resource being validated
        field_value: Value of the field being validated
        field_path: Path to the field
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Evaluate constraint expression

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        result = evaluate_fhirpath_expression(constraint.expression, resource)
        
        # Result should be boolean or truthy/falsy
        if isinstance(result, bool):
            is_valid = result
        elif isinstance(result, list):
            is_valid = len(result) > 0
        else:
            is_valid = bool(result)
        
        if not is_valid:
            error_msg = constraint.human or f"FHIRPath constraint '{constraint.key}' failed on '{field_path}': {constraint.expression}"
            return False, error_msg
        
        return True, None
    except Exception as e:
        # If evaluation fails, consider it a validation error
        error_msg = f"FHIRPath constraint '{constraint.key}' evaluation error on '{field_path}': {str(e)}"
        return False, error_msg


def _validate_binding_strength(
    resource: FHIRResource,
    field_path: str,
    field_value: Any,
    binding_strength: str,
    value_set_url: str,
    terminology_service: TerminologyService
) -> List[str]:
    """
    Validate binding strength constraints for a field.
    
    Args:
        resource: FHIR resource being validated
        field_path: Path to the field
        field_value: Value of the field
        binding_strength: Binding strength (required, extensible, preferred, example)
        value_set_url: ValueSet URL to validate against
        terminology_service: TerminologyService instance
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if field_value is None:
        return errors  # Skip validation if field is not present
    
    # Extract code from field value
    code = None
    system = None
    
    if isinstance(field_value, str):
        code = field_value
    elif isinstance(field_value, dict):
        code = field_value.get("code") or field_value.get("value")
        system = field_value.get("system")
    elif hasattr(field_value, "code"):
        code = field_value.code
        system = getattr(field_value, "system", None)
    elif isinstance(field_value, list):
        # Handle list of codes
        for item in field_value:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            item_errors = _validate_binding_strength(
                resource, field_path, item, binding_strength, value_set_url, terminology_service
            )
            errors.extend(item_errors)
        return errors
    
    if code is None:
        return errors  # Can't validate without a code
    
    # Validate code against ValueSet with binding strength
    try:
        is_valid, error_msg = terminology_service.validate_code_with_binding_strength(
            code=code,
            valueset_url=value_set_url,
            binding_strength=binding_strength,
            system=system
        )
        
        if not is_valid:
            if binding_strength in [BINDING_STRENGTH_REQUIRED, BINDING_STRENGTH_EXTENSIBLE]:
                errors.append(f"Field '{field_path}': {error_msg}")
            elif binding_strength == BINDING_STRENGTH_PREFERRED:
                logger.warning(f"[{current_time}] Field '{field_path}': {error_msg}")
    except Exception as e:
        logger.warning(f"[{current_time}] Error validating binding strength for '{field_path}': {str(e)}")
    
    return errors


def validate_profile_with_fhirpath(
    resource: FHIRResource,
    profile: StructureDefinition
) -> List[str]:
    """
    Validate a resource against a profile including FHIRPath constraints, slicing, and binding strength.
    
    This is an enhanced version that includes all validation features.
    
    Args:
        resource: FHIR resource to validate
        profile: StructureDefinition profile to check against
        
    Returns:
        List of validation error messages (empty if conformant)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Validating resource '{resource.resourceType}' against profile '{profile.url or profile.id}'")
    
    # Use the enhanced check_profile_conformance which includes all validation features
    errors = check_profile_conformance(resource, profile, strict=True)
    
    logger.info(f"[{current_time}] Profile validation completed with {len(errors)} errors")
    return errors

