# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR structural validation (version-aware).

Provides basic structural validation for FHIR resources.
Supports both R4 and R5 versions with version-aware validation rules.

All validation operations include timestamp logging at the end of operations.
"""

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, get_args, get_origin, get_type_hints
import inspect
import time
from datetime import datetime
import hashlib
import json
from enum import Enum
from dataclasses import dataclass, field

from dnhealth.errors import FHIRValidationError
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.valuesets import (
    get_field_value_set,
    validate_codeable_concept_against_value_set,
    validate_coding_against_value_set,
)
from dnhealth.dnhealth_fhir.codesystems import (
    validate_coding_code_system,
    validate_codeable_concept_code_systems,
)
from dnhealth.dnhealth_fhir.reference_validation import (
    validate_reference_format,
    validate_reference_exists,
    get_resources_by_id,
)
from dnhealth.dnhealth_fhir.types import CodeableConcept, Coding, Reference, Extension
from dnhealth.dnhealth_fhir.extension import (
    ExtensionDefinition,
    validate_extension_value,
    find_extension_definition,
    validate_modifier_extensions,
    get_modifier_extensions,
    is_modifier_extension,
)
from dnhealth.dnhealth_fhir.fhirpath import (
    FHIRPathConstraint,
    parse_constraint,
    validate_constraints as validate_fhirpath_constraints,
)
from dnhealth.dnhealth_fhir.structuredefinition import ElementDefinition
from dnhealth.dnhealth_fhir.polymorphic_types import validate_value_x_fields
from dnhealth.dnhealth_fhir.polymorphic_types import validate_value_x_fields
from dnhealth.dnhealth_fhir.version import (
    FHIRVersion,
    detect_version_from_json,
    normalize_version,
    DEFAULT_VERSION,
)


def validate_resource(
    resource: FHIRResource,
    check_required_fields: bool = True,
    check_cardinality: bool = True,
    check_data_types: bool = True,
    check_value_sets: bool = True,
    check_code_systems: bool = True,
    check_references: bool = True,
    check_extensions: bool = True,
    check_constraints: bool = False,
    extension_definitions: Optional[Dict[str, "ExtensionDefinition"]] = None,
    element_definitions: Optional[List[ElementDefinition]] = None,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None,
    fhir_version: Optional[str] = None,
) -> List[str]:
    """
    Validate a FHIR resource structure (version-aware).

    Supports both R4 and R5 versions. Version is auto-detected from resource
    or can be explicitly specified.

    Args:
        resource: FHIR resource to validate
        check_required_fields: If True, validate required fields (default: True)
        check_cardinality: If True, validate cardinality constraints (default: True)
        check_data_types: If True, validate data types (default: True)
        check_value_sets: If True, validate value set bindings (default: True)
        check_code_systems: If True, validate code systems (default: True)
        check_references: If True, validate references (default: True)
        check_extensions: If True, validate extensions (default: True)
        check_constraints: If True, validate FHIRPath constraints (default: False)
        extension_definitions: Optional dictionary of ExtensionDefinition objects by URL
        element_definitions: Optional list of ElementDefinition objects for constraint validation
        bundle: Optional Bundle containing resources for reference validation
        resources: Optional list of resources for reference validation
        fhir_version: Optional FHIR version override ("4.0", "R4", "5.0", "R5", etc.)
                     If None, version is auto-detected from resource

    Returns:
        List of validation error messages (empty if valid)
    """
    start_time = time.time()
    errors = []
    
    # Detect or normalize version
    version = DEFAULT_VERSION
    if fhir_version is not None:
        version = normalize_version(fhir_version)
    else:
        # Try to detect version from resource
        # For now, default to R4 (R5 resources not yet fully implemented)
        # When R5 resources are available, we can detect from resource structure
        version = DEFAULT_VERSION

    # Check resourceType
    if not resource.resourceType:
        errors.append("resourceType is required")

    # Validate required fields if requested
    if check_required_fields:
        errors.extend(validate_required_fields(resource))

    # Validate cardinality if requested
    if check_cardinality:
        errors.extend(validate_cardinality(resource))

    # Validate data types if requested
    if check_data_types:
        errors.extend(validate_data_types(resource))

    # Validate value sets if requested
    if check_value_sets:
        errors.extend(validate_value_set_bindings(resource))

    # Validate code systems if requested
    if check_code_systems:
        errors.extend(validate_code_systems(resource))

    # Validate references if requested
    if check_references:
        errors.extend(validate_references(resource, bundle, resources))

    # Validate extensions if requested
    if check_extensions and extension_definitions:
        errors.extend(validate_extensions(resource, extension_definitions))
        # Also validate modifier extensions
        modifier_errors = validate_modifier_extensions(resource, extension_definitions)
        errors.extend(modifier_errors)

    # Validate FHIRPath constraints if requested
    if check_constraints and element_definitions:
        errors.extend(validate_fhirpath_constraints_from_elements(resource, element_definitions))

    # Validate polymorphic choice types (value[x])
    errors.extend(validate_value_x_fields(resource))
    # Also validate value[x] in nested structures (e.g., ObservationComponent)
    if hasattr(resource, "__dataclass_fields__"):
        for field_name, field_value in resource.__dict__.items():
            if field_name.startswith("_"):
                continue
            if isinstance(field_value, list):
                for item in field_value:
                    if hasattr(item, "__dataclass_fields__"):
                        errors.extend(validate_value_x_fields(item))
            elif hasattr(field_value, "__dataclass_fields__"):
                errors.extend(validate_value_x_fields(field_value))

    # Resource-specific validation
    if resource.resourceType == "Patient":
        errors.extend(_validate_patient(resource))
    elif resource.resourceType == "Observation":
        errors.extend(_validate_observation(resource))
    elif resource.resourceType == "Encounter":
        errors.extend(_validate_encounter(resource))
    elif resource.resourceType == "Bundle":
        errors.extend(_validate_bundle(resource))
    elif resource.resourceType == "Condition":
        errors.extend(_validate_condition(resource))

    # Log completion with timestamp
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    import logging
    logger = logging.getLogger(__name__)
    if elapsed > 0.1:  # Log if validation took more than 100ms
        logger.debug(f"[{current_time}] Validation completed for {resource.resourceType} in {elapsed:.3f}s (errors: {len(errors)})")
    
    # Always log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {current_time}")

    return errors


def _validate_patient(patient) -> List[str]:
    """Validate Patient resource."""
    errors = []
    # Patient-specific rules can be added here
    # For now, basic structure is validated by dataclass
    return errors


def _validate_observation(observation) -> List[str]:
    """Validate Observation resource."""
    errors = []
    # Check required fields
    if not hasattr(observation, "status") or not observation.status:
        errors.append("Observation.status is required")
    if not hasattr(observation, "code") or not observation.code:
        errors.append("Observation.code is required")
    return errors


def _validate_encounter(encounter) -> List[str]:
    """Validate Encounter resource."""
    errors = []
    # Check required fields
    if not hasattr(encounter, "status") or not encounter.status:
        errors.append("Encounter.status is required")
    return errors


def _validate_bundle(bundle) -> List[str]:
    """Validate Bundle resource."""
    errors = []
    # Check required fields
    if not hasattr(bundle, "type") or not bundle.type:
        errors.append("Bundle.type is required")
    return errors


def _validate_condition(condition) -> List[str]:
    """Validate Condition resource."""
    errors = []
    # Check required fields per FHIR R4 spec
    # Condition.subject is required
    if not hasattr(condition, "subject") or not condition.subject:
        errors.append("Condition.subject is required")
    return errors


def validate_required_fields(resource: FHIRResource) -> List[str]:
    """
    Validate required fields for a FHIR resource.
    
    Uses introspection to check for required fields based on FHIR R4 specifications.
    
    Args:
        resource: FHIR resource to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Get resource type
    resource_type = resource.resourceType
    
    # Define required fields per resource type (FHIR R4 spec)
    required_fields = {
        "Observation": ["status", "code"],
        "Encounter": ["status"],
        "Bundle": ["type"],
        "Condition": ["subject"],
        "Patient": [],  # No required fields beyond resourceType
    }
    
    # Check required fields
    if resource_type in required_fields:
        for field_name in required_fields[resource_type]:
            field_value = getattr(resource, field_name, None)
            if field_value is None:
                errors.append(f"{resource_type}.{field_name} is required")
            elif isinstance(field_value, list) and len(field_value) == 0:
                # For list fields, check if empty list is allowed
                # Most FHIR list fields are optional, but some have min cardinality > 0
                pass  # For now, empty lists are allowed
    
    return errors


def validate_cardinality(resource: FHIRResource) -> List[str]:
    """
    Validate cardinality constraints for a FHIR resource.
    
    Checks that fields have the correct number of values (min/max cardinality).
    
    Args:
        resource: FHIR resource to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    resource_type = resource.resourceType
    
    # Define cardinality constraints per resource type and field
    # Format: (min, max) where max=None means unbounded
    cardinality_rules = {
        "Observation": {
            "status": (1, 1),  # Exactly 1 required
            "code": (1, 1),  # Exactly 1 required
            "category": (0, None),  # 0..*
            "identifier": (0, None),
            "note": (0, None),
            "component": (0, None),
        },
        "Encounter": {
            "status": (1, 1),  # Exactly 1 required
            "subject": (0, 1),  # 0..1 optional
            "participant": (0, None),
            "location": (0, None),
        },
        "Bundle": {
            "type": (1, 1),  # Exactly 1 required
            "entry": (0, None),
        },
        "Condition": {
            "subject": (1, 1),  # Exactly 1 required
            "code": (0, 1),  # 0..1 optional
            "category": (0, None),
            "evidence": (0, None),
        },
        "Patient": {
            "identifier": (0, None),
            "name": (0, None),
            "telecom": (0, None),
            "address": (0, None),
        },
    }
    
    if resource_type not in cardinality_rules:
        return errors
    
    rules = cardinality_rules[resource_type]
    
    for field_name, (min_card, max_card) in rules.items():
        field_value = getattr(resource, field_name, None)
        
        if field_value is None:
            # Field not present
            if min_card > 0:
                errors.append(f"{resource_type}.{field_name} has cardinality {min_card}..{max_card if max_card else '*'}, but field is missing")
        elif isinstance(field_value, list):
            # List field
            count = len(field_value)
            if count < min_card:
                errors.append(f"{resource_type}.{field_name} has cardinality {min_card}..{max_card if max_card else '*'}, but found {count} value(s)")
            if max_card is not None and count > max_card:
                errors.append(f"{resource_type}.{field_name} has cardinality {min_card}..{max_card}, but found {count} value(s)")
        else:
            # Single value field
            if min_card > 1:
                errors.append(f"{resource_type}.{field_name} has cardinality {min_card}..{max_card if max_card else '*'}, but found single value")
            if max_card is not None and max_card < 1:
                errors.append(f"{resource_type}.{field_name} has cardinality {min_card}..{max_card}, but found value (should be empty)")
    
    return errors


def validate_data_types(resource: FHIRResource) -> List[str]:
    """
    Validate data types for a FHIR resource.
    
    Checks that field values match their expected Python types.
    
    Args:
        resource: FHIR resource to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    resource_type = resource.resourceType
    
    # Get type hints for the resource class
    try:
        resource_class = type(resource)
        type_hints = get_type_hints(resource_class)
    except Exception:
        # If we can't get type hints, skip data type validation
        return errors
    
    # Check each field
    for field_name, expected_type in type_hints.items():
        if field_name.startswith("_"):
            continue  # Skip private fields
        
        field_value = getattr(resource, field_name, None)
        if field_value is None:
            continue  # Skip None values (handled by required field validation)
        
        # Handle Optional types
        origin = get_origin(expected_type)
        if origin is not None:
            args = get_args(expected_type)
            if len(args) == 2 and type(None) in args:
                # Optional type - get the actual type
                expected_type = args[0] if args[0] is not type(None) else args[1]
                origin = get_origin(expected_type)
        
        # Handle List types
        if origin is list:
            if not isinstance(field_value, list):
                errors.append(f"{resource_type}.{field_name} should be a list, got {type(field_value).__name__}")
                continue
            
            args = get_args(expected_type)
            item_type = args[0] if args else Any
            
            # Validate each item in the list
            for i, item in enumerate(field_value):
                if item is None:
                    continue
                if not _check_type_match(item, item_type):
                    errors.append(f"{resource_type}.{field_name}[{i}] should be {item_type.__name__}, got {type(item).__name__}")
        else:
            # Single value field
            if not _check_type_match(field_value, expected_type):
                errors.append(f"{resource_type}.{field_name} should be {expected_type.__name__}, got {type(field_value).__name__}")
    
    return errors


def _check_type_match(value: Any, expected_type: Any) -> bool:
    """
    Check if a value matches an expected type.
    
    Args:
        value: Value to check
        expected_type: Expected type
        
    Returns:
        True if value matches type, False otherwise
    """
    # Handle None
    if value is None:
        return True
    
    # Handle string types (str, FHIRString, etc.)
    if expected_type == str:
        return isinstance(value, str)
    
    # Handle bool
    if expected_type == bool:
        return isinstance(value, bool)
    
    # Handle int
    if expected_type == int:
        return isinstance(value, int)
    
    # Handle float
    if expected_type == float:
        return isinstance(value, (int, float))  # Allow int for float fields
    
    # Handle dataclass types (check by class name or isinstance)
    if inspect.isclass(expected_type):
        return isinstance(value, expected_type)
    
    # Handle type hints with origin (Optional, List, etc.)
    origin = get_origin(expected_type)
    if origin is not None:
        # For now, allow any value for complex types
        return True
    
    # Default: allow if it's a class we recognize
    if inspect.isclass(expected_type):
        return isinstance(value, expected_type)
    
    # Unknown type - allow it
    return True


def validate_value_set_bindings(resource: FHIRResource) -> List[str]:
    """
    Validate value set bindings for a FHIR resource.
    
    Checks that coded values (codes, CodeableConcepts) match their bound value sets.
    
    Args:
        resource: FHIR resource to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    resource_type = resource.resourceType
    
    # Get type hints for the resource class
    try:
        resource_class = type(resource)
        type_hints = get_type_hints(resource_class)
    except Exception:
        # If we can't get type hints, skip value set validation
        return errors
    
    # Check each field
    for field_name, field_type in type_hints.items():
        if field_name.startswith("_"):
            continue  # Skip private fields
        
        field_value = getattr(resource, field_name, None)
        if field_value is None:
            continue  # Skip None values
        
        # Get value set URL for this field
        value_set_url = get_field_value_set(resource_type, field_name)
        if value_set_url is None:
            continue  # No value set binding for this field
        
        # Handle List types
        origin = get_origin(field_type)
        if origin is list:
            if not isinstance(field_value, list):
                continue  # Skip non-list values
            
            for i, item in enumerate(field_value):
                if item is None:
                    continue
                item_errors = _validate_field_value_against_value_set(
                    item, value_set_url, f"{resource_type}.{field_name}[{i}]"
                )
                errors.extend(item_errors)
        else:
            # Single value field
            # Handle string fields (like status)
            if isinstance(field_value, str):
                from dnhealth.dnhealth_fhir.valuesets import is_code_in_value_set
                if not is_code_in_value_set(field_value, value_set_url):
                    errors.append(
                        f"{resource_type}.{field_name} code '{field_value}' is not in value set '{value_set_url}'"
                    )
            else:
                # Handle CodeableConcept or Coding
                item_errors = _validate_field_value_against_value_set(
                    field_value, value_set_url, f"{resource_type}.{field_name}"
                )
                errors.extend(item_errors)
    
    return errors


def _validate_field_value_against_value_set(value: Any, value_set_url: str, field_path: str) -> List[str]:
    """
    Validate a field value against a value set.
    
    Args:
        value: Field value (CodeableConcept, Coding, or str)
        value_set_url: Value set URL
        field_path: Field path for error messages
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if isinstance(value, CodeableConcept):
        concept_errors = validate_codeable_concept_against_value_set(value, value_set_url)
        # Update error messages with field path
        for error in concept_errors:
            errors.append(f"{field_path}: {error}")
    elif isinstance(value, Coding):
        coding_errors = validate_coding_against_value_set(value, value_set_url)
        for error in coding_errors:
            errors.append(f"{field_path}: {error}")
    elif isinstance(value, str):
        from dnhealth.dnhealth_fhir.valuesets import is_code_in_value_set
        if not is_code_in_value_set(value, value_set_url):
            errors.append(f"{field_path} code '{value}' is not in value set '{value_set_url}'")
    
    return errors


def validate_code_systems(resource: FHIRResource) -> List[str]:
    """
    Validate code systems for a FHIR resource.
    
    Checks that codes in Coding and CodeableConcept fields belong to their declared code systems.
    
    Args:
        resource: FHIR resource to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    resource_type = resource.resourceType
    
    # Get type hints for the resource class
    try:
        resource_class = type(resource)
        type_hints = get_type_hints(resource_class)
    except Exception:
        # If we can't get type hints, skip code system validation
        return errors
    
    # Check each field
    for field_name, field_type in type_hints.items():
        if field_name.startswith("_"):
            continue  # Skip private fields
        
        field_value = getattr(resource, field_name, None)
        if field_value is None:
            continue  # Skip None values
        
        # Handle List types
        origin = get_origin(field_type)
        if origin is list:
            if not isinstance(field_value, list):
                continue  # Skip non-list values
            
            for i, item in enumerate(field_value):
                if item is None:
                    continue
                item_errors = _validate_field_value_code_systems(
                    item, f"{resource_type}.{field_name}[{i}]"
                )
                errors.extend(item_errors)
        else:
            # Single value field
            item_errors = _validate_field_value_code_systems(
                field_value, f"{resource_type}.{field_name}"
            )
            errors.extend(item_errors)
    
    return errors


def _validate_field_value_code_systems(value: Any, field_path: str) -> List[str]:
    """
    Validate a field value's code systems.
    
    Args:
        value: Field value (CodeableConcept, Coding, or other)
        field_path: Field path for error messages
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if isinstance(value, CodeableConcept):
        concept_errors = validate_codeable_concept_code_systems(value)
        # Update error messages with field path
        for error in concept_errors:
            errors.append(f"{field_path}: {error}")
    elif isinstance(value, Coding):
        coding_errors = validate_coding_code_system(value)
        for error in coding_errors:
            errors.append(f"{field_path}: {error}")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def validate_references(
    resource: FHIRResource,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None
) -> List[str]:
    """
    Validate references in a FHIR resource.
    
    Checks that references have valid format and optionally that they point to existing resources.
    Also validates logical references (identifier-based references).
    
    Args:
        resource: FHIR resource to validate
        bundle: Optional Bundle containing resources for reference validation
        resources: Optional list of resources for reference validation
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Import logical reference utilities
    from dnhealth.dnhealth_fhir.logical_reference import (
        is_logical_reference,
        validate_logical_reference
    )
    
    resource_type = resource.resourceType
    
    # Get type hints for the resource class
    try:
        resource_class = type(resource)
        type_hints = get_type_hints(resource_class)
    except Exception:
        # If we can't get type hints, skip reference validation
        return errors
    
    # Field to expected resource types mapping
    # This defines which resource types are expected for each reference field
    expected_types_map: Dict[str, Dict[str, Set[str]]] = {
        "Observation": {
            "subject": {"Patient", "Group", "Device", "Location"},
            "encounter": {"Encounter"},
            "performer": {"Practitioner", "PractitionerRole", "Organization", "CareTeam", "Patient", "RelatedPerson"},
            "basedOn": {"CarePlan", "DeviceRequest", "ImmunizationRecommendation", "MedicationRequest", "NutritionOrder", "ServiceRequest"},
            "partOf": {"Observation", "MedicationAdministration", "MedicationDispense", "MedicationStatement", "Procedure", "Immunization", "ImagingStudy"},
        },
        "Encounter": {
            "subject": {"Patient", "Group"},
            "participant.individual": {"Practitioner", "PractitionerRole", "RelatedPerson"},
            "serviceProvider": {"Organization"},
        },
        "Condition": {
            "subject": {"Patient", "Group"},
            "encounter": {"Encounter"},
            "recorder": {"Practitioner", "PractitionerRole", "Patient", "RelatedPerson"},
            "asserter": {"Practitioner", "PractitionerRole", "Patient", "RelatedPerson", "RelatedPerson"},
        },
        "Patient": {
            "managingOrganization": {"Organization"},
            "generalPractitioner": {"Organization", "Practitioner", "PractitionerRole"},
        },
    }
    
    # Check each field
    for field_name, field_type in type_hints.items():
        if field_name.startswith("_"):
            continue  # Skip private fields
        
        field_value = getattr(resource, field_name, None)
        if field_value is None:
            continue  # Skip None values
        
        # Get expected resource types for this field
        expected_types = None
        if resource_type in expected_types_map:
            expected_types = expected_types_map[resource_type].get(field_name)
        
        # Handle List types
        origin = get_origin(field_type)
        if origin is list:
            if not isinstance(field_value, list):
                continue  # Skip non-list values
            
            for i, item in enumerate(field_value):
                if item is None:
                    continue
                item_errors = _validate_field_value_references(
                    item, f"{resource_type}.{field_name}[{i}]", expected_types, bundle, resources
                )
                errors.extend(item_errors)
        else:
            # Single value field
            item_errors = _validate_field_value_references(
                field_value, f"{resource_type}.{field_name}", expected_types, bundle, resources
            )
            errors.extend(item_errors)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return errors


def _validate_field_value_references(
    value: Any,
    field_path: str,
    expected_types: Optional[Set[str]],
    bundle: Optional["Bundle"],
    resources: Optional[List[FHIRResource]]
) -> List[str]:
    """
    Validate references in a field value.
    
    Args:
        value: Field value (Reference, CodeableReference, or other)
        field_path: Field path for error messages
        expected_types: Optional set of expected resource types
        bundle: Optional Bundle for reference validation
        resources: Optional list of resources for reference validation
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if isinstance(value, Reference):
        # Import logical reference utilities
        from dnhealth.dnhealth_fhir.logical_reference import (
            is_logical_reference,
            validate_logical_reference
        )
        
        # Validate logical references
        if is_logical_reference(value):
            logical_errors = validate_logical_reference(value)
            for error in logical_errors:
                errors.append(f"{field_path}: {error}")
        
        # Validate reference format
        format_errors = validate_reference_format(value)
        for error in format_errors:
            errors.append(f"{field_path}: {error}")
        
        # Validate reference exists if bundle/resources provided

            # Log completion timestamp at end of operation
        if bundle or resources:
            existence_errors = validate_reference_exists(
                value, bundle, resources, expected_types
            )
            for error in existence_errors:
                errors.append(f"{field_path}: {error}")
    
    return errors


def validate_extensions(
    resource: FHIRResource,
    extension_definitions: Dict[str, "ExtensionDefinition"]
) -> List[str]:
    """
    Validate extensions on a FHIR resource.
    
    Checks that extensions have valid URLs and values match their definitions.
    
    Args:
        resource: FHIR resource to validate
        extension_definitions: Dictionary of ExtensionDefinition objects by URL
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Get all extensions from resource
    extensions = _get_all_extensions(resource)
    
    for ext in extensions:
        if not ext.url:
            errors.append("Extension missing required 'url' field")
            continue
        
        # Find extension definition
        ext_def = find_extension_definition(ext.url, extension_definitions)
        if not ext_def:
            # Unknown extension - this is a warning, not an error
            # Extensions can be used without definitions
            continue
        
        # Validate extension value
        ext_value = _get_extension_value(ext)
        if ext_value is not None:
            value_errors = validate_extension_value(ext.url, ext_value, ext_def)
            for error in value_errors:
                errors.append(f"Extension '{ext.url}': {error}")
        elif ext_def.cardinality_min and ext_def.cardinality_min > 0:
            # Extension value is required
            errors.append(f"Extension '{ext.url}' is required (min={ext_def.cardinality_min})")
    
    return errors


def _get_all_extensions(resource: FHIRResource) -> List[Extension]:
    """
    Get all extensions from a resource (including nested extensions).
    
    Recursively traverses the resource to find all extensions, including
    nested extensions within extensions.
    
    Args:
        resource: FHIR resource
        
    Returns:
        List of Extension objects (including nested ones)
    """
    extensions = []
    
    # Get extension field
    if hasattr(resource, "extension") and resource.extension:
        extensions.extend(resource.extension)
        # Recursively get nested extensions
        for ext in resource.extension:
            extensions.extend(_get_nested_extensions(ext))
    
    # Get modifierExtension field
    if hasattr(resource, "modifierExtension") and resource.modifierExtension:
        extensions.extend(resource.modifierExtension)
        # Recursively get nested extensions
        for ext in resource.modifierExtension:
            extensions.extend(_get_nested_extensions(ext))
    
    # Traverse all fields to find extensions in nested structures
    if hasattr(resource, "__dataclass_fields__"):
        for field_name, field_value in resource.__dict__.items():
            if field_name.startswith("_"):
                continue
            
            # Skip extension fields (already handled above)
            if field_name in ("extension", "modifierExtension"):
                continue
            
            # Recursively process nested structures
            if field_value is not None:
                nested_extensions = _get_extensions_from_value(field_value)
                extensions.extend(nested_extensions)
    
    return extensions


def _get_nested_extensions(extension: Extension) -> List[Extension]:
    """
    Recursively get all nested extensions from an Extension.
    
    Args:
        extension: Extension object
        
    Returns:
        List of nested Extension objects
    """
    nested = []
    
    if hasattr(extension, "extension") and extension.extension:
        nested.extend(extension.extension)
        # Recursively process nested extensions
        for nested_ext in extension.extension:
            nested.extend(_get_nested_extensions(nested_ext))
    
    return nested


def _get_extensions_from_value(value: Any) -> List[Extension]:
    """
    Recursively extract extensions from a value (list, dict, dataclass, etc.).
    
    Args:
        value: Any value that might contain extensions
        
    Returns:
        List of Extension objects found
    """
    from dnhealth.dnhealth_fhir.types import Extension
    
    extensions = []
    
    if isinstance(value, Extension):
        # This is an extension - get its nested extensions
        extensions.extend(_get_nested_extensions(value))
    elif isinstance(value, list):
        # Process list items
        for item in value:
            extensions.extend(_get_extensions_from_value(item))
    elif hasattr(value, "__dataclass_fields__"):
        # This is a dataclass - check for extension fields
        if hasattr(value, "extension") and value.extension:
            extensions.extend(value.extension)
            for ext in value.extension:
                extensions.extend(_get_nested_extensions(ext))
        if hasattr(value, "modifierExtension") and value.modifierExtension:
            extensions.extend(value.modifierExtension)
            for ext in value.modifierExtension:
                extensions.extend(_get_nested_extensions(ext))
        # Recursively process all fields
        for field_value in value.__dict__.values():
            if field_value is not None and not isinstance(field_value, (str, int, float, bool)):
                extensions.extend(_get_extensions_from_value(field_value))
    elif isinstance(value, dict):
        # Process dictionary values
        for dict_value in value.values():
            extensions.extend(_get_extensions_from_value(dict_value))
    
    return extensions


def _get_extension_value(extension: Extension) -> Any:
    """
    Get the value from an Extension object.
    
    Args:
        extension: Extension object
        
    Returns:
        Extension value or None
    """
    # Check all value fields
    value_fields = [
        "valueString", "valueBoolean", "valueInteger", "valueDecimal",
        "valueDate", "valueDateTime", "valueUri", "valueCode",
        "valueBase64Binary", "valueCanonical", "valueId", "valueInstant",
        "valueMarkdown", "valueOid", "valuePositiveInt", "valueTime",
        "valueUnsignedInt", "valueUrl", "valueUuid"
    ]
    
    for field in value_fields:
        if hasattr(extension, field):
            value = getattr(extension, field)
            if value is not None:
                return value
    

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
    return None


def validate_and_raise(resource: FHIRResource) -> None:
    """
    Validate a FHIR resource and raise exception if invalid.

    Args:
        resource: FHIR resource to validate

    Raises:
        FHIRValidationError: If validation fails
    """
    errors = validate_resource(resource)
    if errors:
        error_msg = "; ".join(errors)
        raise FHIRValidationError(
            error_msg,
            resource_type=resource.resourceType,
        )


def validate_to_operation_outcome(resource: FHIRResource, **kwargs) -> "OperationOutcome":
    """
    Validate a FHIR resource and return OperationOutcome with validation results.

    Args:
        resource: FHIR resource to validate
        **kwargs: Additional arguments passed to validate_resource

    Returns:
        OperationOutcome resource with validation issues
    """
    from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
    from dnhealth.dnhealth_fhir.types import CodeableConcept, Coding
    
    errors = validate_resource(resource, **kwargs)
    
    issues = []
    for error_msg in errors:
        # Determine severity based on error type
        if "required" in error_msg.lower() or "cardinality" in error_msg.lower():
            severity = "error"
        else:
            severity = "warning"
        
        issue = OperationOutcomeIssue(
            severity=severity,
            code="invalid",  # Standard FHIR issue code
            details=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/operation-outcome",
                    code="MSG_PARAM_INVALID",
                    display="Invalid parameter value"
                )],
                text=error_msg
            ),
            diagnostics=error_msg
        )
        issues.append(issue)

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    # If no errors, add success issue
    if not issues:
        issue = OperationOutcomeIssue(
            severity="information",
            code="informational",
            details=CodeableConcept(
                text="Validation passed"
            )
        )
        issues.append(issue)
    
    return OperationOutcome(
        resourceType="OperationOutcome",
        issue=issues
    )


def validate_fhirpath_constraints_from_elements(
    resource: FHIRResource,
    element_definitions: List[ElementDefinition]
) -> List[str]:
    """
    Validate FHIRPath constraints from ElementDefinition objects.
    
    Args:
        resource: FHIR resource to validate
        element_definitions: List of ElementDefinition objects with constraints
        
    Returns:
        List of validation error messages (empty if all constraints pass)
    """
    errors = []
    
    # Collect all constraints from element definitions
    constraints: List[FHIRPathConstraint] = []
    
    for element in element_definitions:
        if element.constraint:
            for constraint_data in element.constraint:
                if isinstance(constraint_data, dict):
                    constraint = parse_constraint(constraint_data)
                    constraints.append(constraint)
    
    # Validate constraints
    if constraints:
        constraint_errors = validate_fhirpath_constraints(constraints, resource)
        errors.extend(constraint_errors)
    
    return errors


# ============================================================================
# Enhanced Validation Framework Features
# ============================================================================

import logging

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation error severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFORMATION = "information"


@dataclass
class ValidationIssue:
    """
    Enhanced validation issue with severity and metadata.
    
    Attributes:
        message: Validation error/warning message
        severity: Issue severity (error, warning, information)
        field_path: Path to the field causing the issue (e.g., "Patient.name[0].given")
        resource_type: Type of resource being validated
        rule_id: Optional identifier for the validation rule
    """
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    field_path: Optional[str] = None
    resource_type: Optional[str] = None
    rule_id: Optional[str] = None


@dataclass
class ValidationResult:
    """
    Comprehensive validation result with metadata.
    
    Attributes:
        is_valid: True if resource passed validation
        issues: List of validation issues
        resource_type: Type of resource validated
        validation_time: Time taken for validation (seconds)
        timestamp: Timestamp when validation completed
        cached: Whether result was retrieved from cache
    """
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    resource_type: Optional[str] = None
    validation_time: float = 0.0
    timestamp: str = ""
    cached: bool = False


class ValidationCache:
    """
    Cache for validation results to improve performance.
    
    Caches validation results based on resource content hash to avoid
    re-validating identical resources.
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: Optional[int] = None):
        """
        Initialize validation cache.
        
        Args:
            max_size: Maximum number of cached results (default: 1000)
            ttl_seconds: Time-to-live for cache entries in seconds (None = no expiration)
        """
        self._cache: Dict[str, Tuple[ValidationResult, float]] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Validation cache initialized (max_size={max_size}, ttl={ttl_seconds})")
    
    def _get_resource_hash(self, resource: FHIRResource) -> str:
        """
        Generate hash for resource content.
        
        Args:
            resource: FHIR resource to hash
            
        Returns:
            SHA256 hash of resource content
        """
        # Serialize resource to JSON for hashing
        try:
            if hasattr(resource, "to_dict"):
                resource_dict = resource.to_dict()
            else:
                resource_dict = resource.__dict__
            resource_json = json.dumps(resource_dict, sort_keys=True, default=str)
            return hashlib.sha256(resource_json.encode()).hexdigest()
        except Exception:
            # If serialization fails, use object id as fallback
            return str(id(resource))
    
    def get(self, resource: FHIRResource, validation_options: Dict[str, Any]) -> Optional[ValidationResult]:
        """
        Get cached validation result if available.
        
        Args:
            resource: FHIR resource
            validation_options: Options used for validation (affects cache key)
            
        Returns:
            Cached ValidationResult or None if not found/expired
        """
        cache_key = self._get_cache_key(resource, validation_options)
        
        if cache_key not in self._cache:
            return None
        
        result, cached_time = self._cache[cache_key]
        
        # Check TTL
        if self.ttl_seconds is not None:
            elapsed = time.time() - cached_time
            if elapsed > self.ttl_seconds:
                # Expired - remove from cache
                del self._cache[cache_key]
                return None
        
        # Mark as cached
        result.cached = True
        return result
    
    def put(self, resource: FHIRResource, validation_options: Dict[str, Any], result: ValidationResult) -> None:
        """
        Store validation result in cache.
        
        Args:
            resource: FHIR resource
            validation_options: Options used for validation
            result: Validation result to cache
        """
        # Enforce max size
        if len(self._cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        cache_key = self._get_cache_key(resource, validation_options)
        self._cache[cache_key] = (result, time.time())
    
    def _get_cache_key(self, resource: FHIRResource, validation_options: Dict[str, Any]) -> str:
        """
        Generate cache key from resource and options.
        
        Args:
            resource: FHIR resource
            validation_options: Validation options
            
        Returns:
            Cache key string
        """
        resource_hash = self._get_resource_hash(resource)
        options_hash = hashlib.sha256(
            json.dumps(validation_options, sort_keys=True).encode()
        ).hexdigest()
        return f"{resource_hash}:{options_hash}"
    
    def clear(self) -> None:
        """Clear all cached results."""
        self._cache.clear()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Validation cache cleared")
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


# Global validation cache instance
_validation_cache: Optional[ValidationCache] = None


def get_validation_cache() -> ValidationCache:
    """
    Get or create global validation cache instance.
    
    Returns:
        Global ValidationCache instance
    """
    global _validation_cache
    if _validation_cache is None:
        _validation_cache = ValidationCache()
    return _validation_cache


def validate_resource_enhanced(
    resource: FHIRResource,
    check_required_fields: bool = True,
    check_cardinality: bool = True,
    check_data_types: bool = True,
    check_value_sets: bool = True,
    check_code_systems: bool = True,
    check_references: bool = True,
    check_extensions: bool = True,
    check_constraints: bool = False,
    extension_definitions: Optional[Dict[str, "ExtensionDefinition"]] = None,
    element_definitions: Optional[List[ElementDefinition]] = None,
    bundle: Optional["Bundle"] = None,
    resources: Optional[List[FHIRResource]] = None,
    use_cache: bool = True,
    custom_rules: Optional[List[Callable[[FHIRResource], List[ValidationIssue]]]] = None
) -> ValidationResult:
    """
    Enhanced validation with comprehensive result reporting and caching.
    
    Args:
        resource: FHIR resource to validate
        check_required_fields: If True, validate required fields (default: True)
        check_cardinality: If True, validate cardinality constraints (default: True)
        check_data_types: If True, validate data types (default: True)
        check_value_sets: If True, validate value set bindings (default: True)
        check_code_systems: If True, validate code systems (default: True)
        check_references: If True, validate references (default: True)
        check_extensions: If True, validate extensions (default: True)
        check_constraints: If True, validate FHIRPath constraints (default: False)
        extension_definitions: Optional dictionary of ExtensionDefinition objects by URL
        element_definitions: Optional list of ElementDefinition objects for constraint validation
        bundle: Optional Bundle containing resources for reference validation
        resources: Optional list of resources for reference validation
        use_cache: If True, use validation cache (default: True)
        custom_rules: Optional list of custom validation rule functions
        
    Returns:
        ValidationResult with comprehensive validation information
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build validation options for cache key
    validation_options = {
        "check_required_fields": check_required_fields,
        "check_cardinality": check_cardinality,
        "check_data_types": check_data_types,
        "check_value_sets": check_value_sets,
        "check_code_systems": check_code_systems,
        "check_references": check_references,
        "check_extensions": check_extensions,
        "check_constraints": check_constraints,
    }
    
    # Try cache first
    if use_cache:
        cache = get_validation_cache()
        cached_result = cache.get(resource, validation_options)
        if cached_result is not None:
            return cached_result
    
    # Perform validation
    error_messages = validate_resource(
        resource,
        check_required_fields=check_required_fields,
        check_cardinality=check_cardinality,
        check_data_types=check_data_types,
        check_value_sets=check_value_sets,
        check_code_systems=check_code_systems,
        check_references=check_references,
        check_extensions=check_extensions,
        check_constraints=check_constraints,
        extension_definitions=extension_definitions,
        element_definitions=element_definitions,
        bundle=bundle,
        resources=resources
    )
    
    # Convert error messages to ValidationIssue objects
    issues = []
    for error_msg in error_messages:
        # Determine severity
        severity = ValidationSeverity.ERROR
        if "warning" in error_msg.lower() or "suggested" in error_msg.lower():
            severity = ValidationSeverity.WARNING
        elif "information" in error_msg.lower() or "note" in error_msg.lower():
            severity = ValidationSeverity.INFORMATION
        
        # Extract field path if present
        field_path = None
        if "." in error_msg:
            # Try to extract field path (e.g., "Patient.name[0].given")
            parts = error_msg.split(":")[0].split(".")
            if len(parts) > 1:
                field_path = ".".join(parts[1:])
        
        issue = ValidationIssue(
            message=error_msg,
            severity=severity,
            field_path=field_path,
            resource_type=resource.resourceType
        )
        issues.append(issue)
    
    # Apply custom validation rules
    if custom_rules:
        for rule_func in custom_rules:
            try:
                custom_issues = rule_func(resource)
                issues.extend(custom_issues)
            except Exception as e:
                # Log rule execution error but don't fail validation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{current_time}] Custom validation rule failed: {e}")
    
    # Create result
    elapsed = time.time() - start_time
    result = ValidationResult(
        is_valid=len(issues) == 0,
        issues=issues,
        resource_type=resource.resourceType,
        validation_time=elapsed,
        timestamp=current_time,
        cached=False
    )
    
    # Store in cache
    if use_cache:
        cache = get_validation_cache()
        cache.put(resource, validation_options, result)
    
    # Log completion
    logger.debug(f"[{current_time}] Enhanced validation completed for {resource.resourceType} in {elapsed:.3f}s (issues: {len(issues)})")
    
    return result


def validate_resources_batch(
    resources: List[FHIRResource],
    **validation_kwargs
) -> Dict[str, ValidationResult]:
    """
    Validate multiple resources in batch.
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    Args:
        resources: List of FHIR resources to validate
        **validation_kwargs: Additional arguments passed to validate_resource_enhanced
        
    Returns:
        Dictionary mapping resource IDs (or indices) to ValidationResult objects
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting batch validation of {len(resources)} resources")
    
    results = {}
    
    for i, resource in enumerate(resources):
        # Get resource identifier
        resource_id = None
        if hasattr(resource, "id") and resource.id:
            resource_id = resource.id
        else:
            resource_id = f"resource_{i}"
        
        # Validate resource
        result = validate_resource_enhanced(resource, **validation_kwargs)
        results[resource_id] = result
    
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Batch validation completed in {elapsed:.3f}s ({len(resources)} resources)")
    
    return results


def get_validation_statistics(results: Dict[str, ValidationResult]) -> Dict[str, Any]:
    """
    Generate validation statistics from batch results.
    
    Args:
        results: Dictionary of ValidationResult objects
        
    Returns:
        Dictionary with validation statistics
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    total_resources = len(results)
    valid_resources = sum(1 for r in results.values() if r.is_valid)
    invalid_resources = total_resources - valid_resources
    
    total_issues = sum(len(r.issues) for r in results.values())
    error_count = sum(
        sum(1 for issue in r.issues if issue.severity == ValidationSeverity.ERROR)
        for r in results.values()
    )
    warning_count = sum(
        sum(1 for issue in r.issues if issue.severity == ValidationSeverity.WARNING)
        for r in results.values()
    )
    
    total_validation_time = sum(r.validation_time for r in results.values())
    cached_count = sum(1 for r in results.values() if r.cached)
    
    stats = {
        "total_resources": total_resources,
        "valid_resources": valid_resources,
        "invalid_resources": invalid_resources,
        "validation_rate": valid_resources / total_resources if total_resources > 0 else 0.0,
        "total_issues": total_issues,
        "error_count": error_count,
        "warning_count": warning_count,
        "total_validation_time": total_validation_time,
        "average_validation_time": total_validation_time / total_resources if total_resources > 0 else 0.0,
        "cached_results": cached_count,
        "cache_hit_rate": cached_count / total_resources if total_resources > 0 else 0.0,
        "timestamp": current_time
    }
    
    return stats

