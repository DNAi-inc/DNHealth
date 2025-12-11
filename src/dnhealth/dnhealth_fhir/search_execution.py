# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Search execution engine.

Implements search execution logic for matching resources against search parameters.
All operations include timestamps in logs for traceability.
"""

from typing import Any, List, Optional, Dict, Set
from datetime import datetime, date
import re
from dnhealth.dnhealth_fhir.search import (
    SearchParameter,
    SearchParameters,
    parse_token_value,
    parse_quantity_value,
    parse_reference_value,
    is_chained_parameter,
    is_reverse_chain_parameter,
)
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.fhirpath import evaluate_fhirpath_expression
from dnhealth.util.logging import get_logger

logger = get_logger(__name__)

# Import ValueSet utilities for :in and :not-in modifiers
try:
    from dnhealth.dnhealth_fhir.valueset_resource import ValueSet, get_codes_from_valueset, get_value_set_by_url
    from dnhealth.dnhealth_fhir.terminology_service import TerminologyService
    VALUESET_SUPPORT_AVAILABLE = True
except ImportError:
    VALUESET_SUPPORT_AVAILABLE = False
    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet support not available, :in and :not-in modifiers will have limited functionality")

# Global terminology service instance (can be set by caller)
_terminology_service: Optional[Any] = None


def set_terminology_service(service: Any) -> None:
    """
    Set the global terminology service for ValueSet operations.
    
    Args:
        service: TerminologyService instance or compatible object
    """
    global _terminology_service
    _terminology_service = service
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Terminology service set for search operations")


def execute_search(
    resources: List[FHIRResource],
    search_params: SearchParameters,
    param_type_map: Optional[Dict[str, str]] = None,
    resource_resolver: Optional[callable] = None,
    all_resources: Optional[List[FHIRResource]] = None
) -> List[FHIRResource]:
    """
    Execute a FHIR search against a list of resources.
    
    Args:
        resources: List of FHIR resources to search
        search_params: Search parameters to apply
        param_type_map: Optional mapping of parameter names to types
                       (e.g., {"status": "token", "date": "date"})
        resource_resolver: Optional function to resolve references for chained searches
                          Function signature: (reference: str) -> Optional[FHIRResource]
        all_resources: Optional list of all resources in the system (required for _revinclude processing)
    
    Returns:
        List of matching resources
    
    Examples:
        >>> resources = [patient1, patient2]
        >>> params = parse_search_string("status=active&name=John")
        >>> results = execute_search(resources, params)
    """
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Executing search on {len(resources)} resources")
    
    # Validate _count parameter (FHIR spec: must be positive integer >= 1)
    if search_params._count is not None:
        if search_params._count < 1:
            raise ValueError(
                f"Invalid _count value: {search_params._count}. "
                "_count must be a positive integer (>= 1) per FHIR specification."
            )
    
    # Validate _offset parameter (FHIR spec: must be non-negative integer >= 0)
    if search_params._offset is not None:
        if search_params._offset < 0:
            raise ValueError(
                f"Invalid _offset value: {search_params._offset}. "
                "_offset must be a non-negative integer (>= 0) per FHIR specification."
            )
    
    # Handle FHIRPath query if present
    if search_params._fhirpath:
        matching = _execute_fhirpath_query(resources, search_params._fhirpath)
    else:
        # Handle reverse chaining first (requires access to all resources)
        if any(is_reverse_chain_parameter(p.name) for p in search_params.parameters):
            resources = _apply_reverse_chaining(
                resources, 
                search_params, 
                param_type_map, 
                all_resources=all_resources,
                resource_resolver=resource_resolver
            )
        
        if not search_params.parameters:
            # No search parameters, return all resources (after pagination)
            matching = resources
        else:
            # Filter resources based on search parameters
            matching = []
            for resource in resources:
                if resource_matches_search(resource, search_params, param_type_map, resource_resolver):
                    matching.append(resource)
    
    # Apply sorting
    if search_params._sort:
        matching = sort_search_results(matching, search_params._sort, param_type_map)
    
    # Apply pagination
    if search_params._offset:
        matching = matching[search_params._offset:]
    if search_params._count is not None:
        matching = matching[:search_params._count]
    
    # Apply _include processing
    if search_params._include and resource_resolver:
        matching = process_include(matching, search_params._include, resource_resolver)
    
    # Apply _revinclude processing (requires all resources)
    if search_params._revinclude:
        # Use all_resources if provided, otherwise fall back to resources (limited functionality)
        revinclude_resources = all_resources if all_resources is not None else resources
        if revinclude_resources:
            matching = process_revinclude(matching, search_params._revinclude, revinclude_resources)
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Applied _revinclude processing: {len(matching)} total resources")
        else:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - _revinclude requires all_resources parameter, skipping _revinclude processing")
    
    # Apply _summary mode if specified
    if search_params._summary:
        from dnhealth.dnhealth_fhir.search_results import apply_summary
        matching = [apply_summary(resource, search_params._summary) for resource in matching]
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Applied _summary mode '{search_params._summary}' to {len(matching)} resources")
    
    # Apply _elements filter if specified
    if search_params._elements:
        from dnhealth.dnhealth_fhir.search_results import apply_elements
        matching = [apply_elements(resource, search_params._elements) for resource in matching]
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Applied _elements filter to {len(matching)} resources")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{current_time} - Search completed: {len(matching)} matches found")
    logger.info(f"{current_time} - Current Time at End of Operations: {current_time}")
    return matching


def resource_matches_search(
    resource: FHIRResource,
    search_params: SearchParameters,
    param_type_map: Optional[Dict[str, str]] = None,
    resource_resolver: Optional[callable] = None
) -> bool:
    """
    Check if a resource matches all search parameters.
    
    Args:
        resource: FHIR resource to check
        search_params: Search parameters
        param_type_map: Optional mapping of parameter names to types
        resource_resolver: Optional function to resolve references for chained searches
    
    Returns:
        True if resource matches all parameters, False otherwise
    """
    # All parameters must match (AND logic)
    for param in search_params.parameters:
        if not resource_matches_parameter(resource, param, param_type_map, resource_resolver):
            return False
    return True


def resource_matches_parameter(
    resource: FHIRResource,
    param: SearchParameter,
    param_type_map: Optional[Dict[str, str]] = None,
    resource_resolver: Optional[callable] = None
) -> bool:
    """
    Check if a resource matches a single search parameter.
    
    Args:
        resource: FHIR resource to check
        param: Search parameter
        param_type_map: Optional mapping of parameter names to types
        resource_resolver: Optional function to resolve references for chained searches
    
    Returns:
        True if resource matches parameter, False otherwise
    """
    # Handle special search parameters (_tag, _security)
    if param.name == "_tag":
        return _matches_tag_search(resource, param)
    elif param.name == "_security":
        return _matches_security_search(resource, param)
    
    # Handle chained parameters
    if is_chained_parameter(param.name):
        return _matches_chained_parameter(resource, param, param_type_map, resource_resolver)
    
    # Reverse chain parameters are handled at execute_search level
    if is_reverse_chain_parameter(param.name):
        # Should not reach here - reverse chaining is pre-processed
        return False
    
    # Determine parameter type
    param_type = _get_parameter_type(param.name, param_type_map)
    
    # Get field value from resource
    field_value = _get_field_value(resource, param.name)
    
    # Handle missing modifier
    if param.modifier == "missing":
        is_missing = (field_value is None or 
                     (isinstance(field_value, list) and len(field_value) == 0))
        return (param.value.lower() == "true") == is_missing
    
    # If field is missing and modifier is not "missing", it doesn't match
    if field_value is None:
        return False
    
    # Execute search based on parameter type
    if param_type == "token":
        return _matches_token_search(field_value, param)
    elif param_type == "reference":
        return _matches_reference_search(field_value, param)
    elif param_type == "date":
        return _matches_date_search(field_value, param)
    elif param_type == "number":
        return _matches_number_search(field_value, param)
    elif param_type == "quantity":
        return _matches_quantity_search(field_value, param)
    elif param_type == "uri":
        return _matches_uri_search(field_value, param)
    elif param_type == "composite":
        return _matches_composite_search(field_value, param)
    else:
        # Default to string search
        return _matches_string_search(field_value, param)


def _get_parameter_type(param_name: str, param_type_map: Optional[Dict[str, str]]) -> str:
    """
    Get the type of a search parameter.
    
    Args:
        param_name: Parameter name
        param_type_map: Optional mapping of parameter names to types
    
    Returns:
        Parameter type (default: "string")
    """
    if param_type_map and param_name in param_type_map:
        return param_type_map[param_name]
    
    # Try to infer from common parameter names
    if param_name in ["_id", "_lastUpdated"]:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return "special"
    
    # Default to string
    return "string"


def _execute_fhirpath_query(
    resources: List[FHIRResource],
    fhirpath_expression: str
) -> List[FHIRResource]:
    """
    Execute a FHIRPath query against a list of resources.
    
    FHIRPath expressions used for queries should evaluate to a boolean result.
    Resources where the expression evaluates to True (or truthy) are included.
    
    Args:
        resources: List of FHIR resources to query
        fhirpath_expression: FHIRPath expression to evaluate
        
    Returns:
        List of resources that match the FHIRPath expression
        
    Examples:
        >>> resources = [patient1, patient2]
        >>> results = _execute_fhirpath_query(resources, "status = 'active'")
        >>> results = _execute_fhirpath_query(resources, "name.family.exists()")
        >>> results = _execute_fhirpath_query(resources, "birthDate > '2000-01-01'")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{current_time} - Executing FHIRPath query: {fhirpath_expression}")
    
    matching = []
    
    for resource in resources:
        try:
            # Evaluate FHIRPath expression on resource
            result = evaluate_fhirpath_expression(fhirpath_expression, resource)
            
            # Result should be boolean or truthy/falsy
            if isinstance(result, bool):
                if result:
                    matching.append(resource)
            elif isinstance(result, list):
                # If result is a list, consider it a match if list is non-empty
                if len(result) > 0:
                    matching.append(resource)
            else:
                # Truthy values are considered matches
                if result:
                    matching.append(resource)
        except Exception as e:
            # If evaluation fails, log warning and exclude resource
            logger.warning(f"{current_time} - Error evaluating FHIRPath expression on resource {resource.id}: {str(e)}")
            continue
    
    logger.info(f"{current_time} - FHIRPath query completed: {len(matching)} matches found")
    return matching


def _get_field_value(resource: FHIRResource, field_path: str) -> Any:
    """
    Get field value from resource by path.
    
    Supports nested paths like "name.family" or "address.city".
    
    Args:
        resource: FHIR resource
        field_path: Field path (e.g., "status" or "name.family")
    
    Returns:
        Field value or None
    """
    parts = field_path.split(".")
    current = resource
    
    for part in parts:
        if current is None:
            return None
        
        if hasattr(current, part):
            current = getattr(current, part)
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    
    return current


def _matches_string_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute string search matching.
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    search_value = param.value.lower()
    
    # Handle list of values
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_string_value(item, search_value, param.modifier):
                return True
        return False
    
    # Handle single value
    return _matches_string_value(field_value, search_value, param.modifier)


def _matches_string_value(value: Any, search_value: str, modifier: Optional[str]) -> bool:
    """
    Match a single string value against search criteria.
    
    Args:
        value: Value to check
        search_value: Search value (lowercase)
        modifier: Search modifier
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Convert to string
    str_value = str(value).lower()
    
    # Handle modifiers
    if modifier == "exact":
        return str_value == search_value
    elif modifier == "contains":
        return search_value in str_value
    elif modifier == "text":
        # Text search - similar to contains but may search in multiple fields
        return search_value in str_value
    else:
        # Default: contains
        return search_value in str_value


def _matches_token_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute token search matching.
    
    Token search matches codes (with optional system).
    Format: system|code or just code
    
    Supports modifiers:
    - :text - Text search in display names
    - :not - Not equal
    - :above - Is-a hierarchy (code is above in hierarchy)
    - :below - Has-a hierarchy (code is below in hierarchy)
    - :in - In ValueSet
    - :not-in - Not in ValueSet
    - :of-type - Of type (for references)
    - :missing - Missing (true/false)
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    # Handle missing modifier
    if param.modifier == "missing":
        is_missing = (field_value is None or 
                     (isinstance(field_value, list) and len(field_value) == 0))
        return (param.value.lower() == "true") == is_missing
    
    # Handle :not modifier (not equal)
    if param.modifier == "not":
        search_system, search_code = parse_token_value(param.value)
        search_code_lower = search_code.lower() if search_code else None
        
        if isinstance(field_value, list):
            # For lists, return True if NONE match
            for item in field_value:
                if _matches_token_value(item, search_system, search_code_lower):
                    return False
            return True
        else:
            return not _matches_token_value(field_value, search_system, search_code_lower)
    
    # Handle :text modifier (text search in display names)
    if param.modifier == "text":
        search_text = param.value.lower()
        if isinstance(field_value, list):
            for item in field_value:
                if _matches_token_text(item, search_text):
                    return True
            return False
        else:
            return _matches_token_text(field_value, search_text)
    
    # Handle :in modifier (code is in ValueSet)
    if param.modifier == "in":
        return _matches_token_in_valueset(field_value, param.value)
    
    # Handle :not-in modifier (code is not in ValueSet)
    if param.modifier == "not-in":
        return not _matches_token_in_valueset(field_value, param.value)
    
    # Handle :of-type modifier for tokens (for references - check resource type)
    if param.modifier == "of-type":
        # For token search with :of-type, the value should be ResourceType|id or ResourceType
        # Extract resource type from value
        if "|" in param.value:
            search_resource_type, _ = param.value.split("|", 1)
        else:
            search_resource_type = param.value
        
        # Extract resource type from field value (if it's a reference)
        if isinstance(field_value, list):
            for item in field_value:
                ref_type = _get_reference_type_from_token(item)
                if ref_type and ref_type == search_resource_type:
                    return True
            return False
        else:
            ref_type = _get_reference_type_from_token(field_value)
            return ref_type == search_resource_type if ref_type else False
    
    # Handle :above and :below modifiers
    # These require hierarchy resolution which may not be available
    # For now, log a warning and fall back to basic matching
    if param.modifier in ["above", "below"]:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Modifier :{param.modifier} requires hierarchy resolution, falling back to basic matching")
        # Fall through to basic matching
    
    search_system, search_code = parse_token_value(param.value)
    search_code_lower = search_code.lower() if search_code else None
    
    # Handle list of values
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_token_value(item, search_system, search_code_lower):
                return True
        return False
    
    # Handle single value
    return _matches_token_value(field_value, search_system, search_code_lower)


def _matches_token_value(value: Any, search_system: Optional[str], search_code: Optional[str]) -> bool:
    """
    Match a single token value against search criteria.
    
    Args:
        value: Value to check (can be CodeableConcept, Coding, string, etc.)
        search_system: Search system (optional)
        search_code: Search code (required)
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Handle CodeableConcept
    if hasattr(value, "coding") and value.coding:
        for coding in value.coding:
            if _matches_coding(coding, search_system, search_code):
                return True
        return False
    
    # Handle Coding
    if hasattr(value, "system") and hasattr(value, "code"):
        return _matches_coding(value, search_system, search_code)
    
    # Handle string code
    if isinstance(value, str):
        if search_system:
            # System specified, but value is just a string - no match
            return False
        return value.lower() == search_code
    
    # Handle dict representation
    if isinstance(value, dict):
        code = value.get("code")
        system = value.get("system")
        if code:
            if search_system:
                return system == search_system and code.lower() == search_code
            else:
                return code.lower() == search_code
    
    return False


def _matches_token_text(value: Any, search_text: str) -> bool:
    """
    Match a token value using text search (searches in display names).
    
    Args:
        value: Value to check (can be CodeableConcept, Coding, string, etc.)
        search_text: Search text (lowercase)
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Handle CodeableConcept
    if hasattr(value, "coding") and value.coding:
        # Check text field first
        if hasattr(value, "text") and value.text:
            if search_text in value.text.lower():
                return True
        # Check display names in codings
        for coding in value.coding:
            if _matches_coding_text(coding, search_text):
                return True
        return False
    
    # Handle Coding
    if hasattr(value, "system") or hasattr(value, "code"):
        return _matches_coding_text(value, search_text)
    
    # Handle string - search in the string itself
    if isinstance(value, str):
        return search_text in value.lower()
    
    # Handle dict representation
    if isinstance(value, dict):
        # Check text field
        text = value.get("text")
        if text and search_text in str(text).lower():
            return True
        # Check display field
        display = value.get("display")
        if display and search_text in str(display).lower():
            return True
        # Check code field as fallback
        code = value.get("code")
        if code and search_text in str(code).lower():
            return True
    
    return False


def _matches_tag_search(resource: FHIRResource, param: SearchParameter) -> bool:
    """
    Check if a resource matches a _tag search parameter.
    
    The _tag parameter searches for resources with specific tags in meta.tag.
    Format: _tag={system}|{code} or _tag={system}|{code}|{display}
    
    Args:
        resource: FHIR resource to check
        param: Search parameter with name="_tag"
    
    Returns:
        True if resource has matching tag, False otherwise
    """
    from dnhealth.dnhealth_fhir.tagging import get_tags, has_tag
    
    # Parse tag value (format: system|code or system|code|display)
    value = param.value
    if not value:
        return False
    
    parts = value.split("|")
    if len(parts) < 2:
        # Invalid format, no match
        return False
    
    tag_system = parts[0]
    tag_code = parts[1]
    
    # Check if resource has the tag
    return has_tag(resource, tag_system, tag_code)


def _matches_security_search(resource: FHIRResource, param: SearchParameter) -> bool:
    """
    Check if a resource matches a _security search parameter.
    
    The _security parameter searches for resources with specific security labels in meta.security.
    Format: _security={system}|{code} or _security={system}|{code}|{display}
    
    Args:
        resource: FHIR resource to check
        param: Search parameter with name="_security"
    
    Returns:
        True if resource has matching security label, False otherwise
    """
    from dnhealth.dnhealth_fhir.security import get_security_labels, has_security_label
    
    # Parse security label value (format: system|code or system|code|display)
    value = param.value
    if not value:
        return False
    
    parts = value.split("|")
    if len(parts) < 2:
        # Invalid format, no match
        return False
    
    label_system = parts[0]
    label_code = parts[1]
    
    # Check if resource has the security label
    # Note: has_security_label function may not exist, so we'll implement inline
    if not hasattr(resource, "meta") or not resource.meta:
        return False
    
    if not hasattr(resource.meta, "security") or not resource.meta.security:
        return False
    
    # Check each security label
    for label in resource.meta.security:
        label_sys = None
        label_cd = None
        
        if hasattr(label, "system"):
            label_sys = label.system
        elif isinstance(label, dict):
            label_sys = label.get("system")
        
        if hasattr(label, "code"):
            label_cd = label.code
        elif isinstance(label, dict):
            label_cd = label.get("code")
        
        if label_sys == label_system and label_cd and label_cd.lower() == label_code.lower():
            return True
    
    return False


def _matches_coding_text(coding: Any, search_text: str) -> bool:
    """
    Match a Coding object using text search (searches in display name).
    
    Args:
        coding: Coding object
        search_text: Search text (lowercase)
    
    Returns:
        True if matches, False otherwise
    """
    # Check display field
    display = None
    if hasattr(coding, "display"):
        display = coding.display
    elif isinstance(coding, dict):
        display = coding.get("display")
    
    if display and search_text in str(display).lower():
        return True
    
    # Fallback to code if display not available
    code = None
    if hasattr(coding, "code"):
        code = coding.code
    elif isinstance(coding, dict):
        code = coding.get("code")
    
    if code and search_text in str(code).lower():
        return True
    
    return False


def _matches_coding(coding: Any, search_system: Optional[str], search_code: Optional[str]) -> bool:
    """
    Match a Coding object against search criteria.
    
    Args:
        coding: Coding object
        search_system: Search system (optional)
        search_code: Search code (required)
    
    Returns:
        True if matches, False otherwise
    """
    if not search_code:
        return False
    
    coding_code = None
    coding_system = None
    
    if hasattr(coding, "code"):
        coding_code = coding.code
    elif isinstance(coding, dict):
        coding_code = coding.get("code")
    
    if hasattr(coding, "system"):
        coding_system = coding.system
    elif isinstance(coding, dict):
        coding_system = coding.get("system")
    
    if not coding_code:
        return False
    
    # Match code
    if coding_code.lower() != search_code:
        return False
    
    # If system specified, must match
    if search_system:
        return coding_system == search_system
    
    # System not specified, code matches
    return True


def _matches_reference_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute reference search matching.
    
    Reference search matches resource references.
    Format: ResourceType/id or URL
    
    Supports modifiers:
    - :above - Above in hierarchy (reference is above target)
    - :below - Below in hierarchy (reference is below target)
    - :of-type - Of type (reference type matches)
    - :missing - Missing (true/false)
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    # Handle missing modifier
    if param.modifier == "missing":
        is_missing = (field_value is None or 
                     (isinstance(field_value, list) and len(field_value) == 0))
        return (param.value.lower() == "true") == is_missing
    
    # Handle :of-type modifier (match resource type only)
    if param.modifier == "of-type":
        search_resource_type, _ = parse_reference_value(param.value)
        if not search_resource_type:
            return False
        
        if isinstance(field_value, list):
            for item in field_value:
                ref_type = _get_reference_type(item)
                if ref_type == search_resource_type:
                    return True
            return False
        else:
            ref_type = _get_reference_type(field_value)
            return ref_type == search_resource_type
    
    # Handle :above and :below modifiers
    # These require hierarchy resolution which may not be available
    # For now, log a warning and fall back to basic matching
    if param.modifier in ["above", "below"]:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Modifier :{param.modifier} requires hierarchy resolution, falling back to basic matching")
        # Fall through to basic matching
    
    search_resource_type, search_resource_id = parse_reference_value(param.value)
    
    if not search_resource_type or not search_resource_id:
        return False
    
    # Handle list of references
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_reference_value(item, search_resource_type, search_resource_id):
                return True
        return False
    
    # Handle single reference
    return _matches_reference_value(field_value, search_resource_type, search_resource_id)


def _matches_reference_value(value: Any, resource_type: str, resource_id: str) -> bool:
    """
    Match a single reference value against search criteria.
    
    Args:
        value: Reference value (can be Reference object, string, dict)
        resource_type: Expected resource type
        resource_id: Expected resource ID
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Handle Reference object
    if hasattr(value, "reference"):
        ref_str = value.reference
        ref_type, ref_id = parse_reference_value(ref_str)
        if ref_type and ref_id:
            # Check type match (if specified in search)
            if resource_type and ref_type.lower() != resource_type.lower():
                return False
            return ref_id == resource_id
    
    # Handle string reference
    if isinstance(value, str):
        ref_type, ref_id = parse_reference_value(value)
        if ref_type and ref_id:
            if resource_type and ref_type.lower() != resource_type.lower():
                return False
            return ref_id == resource_id
    
    # Handle dict representation
    if isinstance(value, dict):
        ref_str = value.get("reference")
        if ref_str:
            ref_type, ref_id = parse_reference_value(ref_str)
            if ref_type and ref_id:
                if resource_type and ref_type.lower() != resource_type.lower():
                    return False
                return ref_id == resource_id
    
    return False


def _get_reference_type(value: Any) -> Optional[str]:
    """
    Extract resource type from a reference value.
    
    Args:
        value: Reference value (can be Reference object, string, dict)
    
    Returns:
        Resource type or None
    """
    if value is None:
        return None
    
    # Handle Reference object
    if hasattr(value, "reference"):
        ref_str = value.reference
        ref_type, _ = parse_reference_value(ref_str)
        return ref_type
    
    # Handle string reference
    if isinstance(value, str):
        ref_type, _ = parse_reference_value(value)
        return ref_type
    
    # Handle dict representation
    if isinstance(value, dict):
        ref_str = value.get("reference")
        if ref_str:
            ref_type, _ = parse_reference_value(ref_str)
            return ref_type
    
    return None


def _get_reference_type_from_token(value: Any) -> Optional[str]:
    """
    Extract resource type from a token value (for :of-type modifier on token searches).
    
    Token values for references may be in format: ResourceType|id or just ResourceType.
    
    Args:
        value: Token value (can be Coding, CodeableConcept, string, dict)
    
    Returns:
        Resource type or None
    """
    if value is None:
        return None
    
    # Handle string - check if it's a reference format
    if isinstance(value, str):
        # Check if it contains | (ResourceType|id format)
        if "|" in value:
            ref_type, _ = value.split("|", 1)
            return ref_type
        # Check if it's a reference string (ResourceType/id)
        if "/" in value:
            ref_type, _ = parse_reference_value(value)
            return ref_type
        return None
    
    # Handle Coding - check if code looks like a reference
    if hasattr(value, "code"):
        code = value.code
        if isinstance(code, str):
            if "|" in code:
                ref_type, _ = code.split("|", 1)
                return ref_type
            if "/" in code:
                ref_type, _ = parse_reference_value(code)
                return ref_type
    
    # Handle dict representation
    if isinstance(value, dict):
        code = value.get("code")
        if code and isinstance(code, str):
            if "|" in code:
                ref_type, _ = code.split("|", 1)
                return ref_type
            if "/" in code:
                ref_type, _ = parse_reference_value(code)
                return ref_type
    
    return None


def _extract_codes_from_value(value: Any) -> List[str]:
    """
    Extract all codes from a value (Coding, CodeableConcept, string, etc.).
    
    Args:
        value: Value to extract codes from
    
    Returns:
        List of code strings
    """
    codes = []
    
    if value is None:
        return codes
    
    # Handle CodeableConcept
    if hasattr(value, "coding") and value.coding:
        for coding in value.coding:
            code = _extract_code_from_coding(coding)
            if code:
                codes.append(code)
        return codes
    
    # Handle Coding
    if hasattr(value, "code") or hasattr(value, "system"):
        code = _extract_code_from_coding(value)
        if code:
            codes.append(code)
        return codes
    
    # Handle string
    if isinstance(value, str):
        codes.append(value)
        return codes
    
    # Handle dict representation
    if isinstance(value, dict):
        # Check for CodeableConcept structure
        if "coding" in value:
            for coding in value.get("coding", []):
                code = coding.get("code") if isinstance(coding, dict) else (coding.code if hasattr(coding, "code") else None)
                if code:
                    codes.append(str(code))
        # Check for Coding structure
        elif "code" in value:
            code = value.get("code")
            if code:
                codes.append(str(code))
        return codes
    
    return codes


def _extract_code_from_coding(coding: Any) -> Optional[str]:
    """
    Extract code from a Coding object.
    
    Args:
        coding: Coding object
    
    Returns:
        Code string or None
    """
    if coding is None:
        return None
    
    if hasattr(coding, "code"):
        return str(coding.code) if coding.code else None
    
    if isinstance(coding, dict):
        return str(coding.get("code")) if coding.get("code") else None
    
    return None


def _matches_token_in_valueset(field_value: Any, valueset_url: str) -> bool:
    """
    Check if codes in field_value are in the specified ValueSet.
    
    Args:
        field_value: Field value (can be Coding, CodeableConcept, string, list, etc.)
        valueset_url: ValueSet URL
    
    Returns:
        True if at least one code is in the ValueSet, False otherwise
    """
    if not VALUESET_SUPPORT_AVAILABLE:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet support not available, cannot check :in modifier for '{valueset_url}'")
        return False
    
    # Try to get ValueSet
    valueset = None
    
    # Try global terminology service first
    if _terminology_service:
        try:
            valueset = _terminology_service.get_valueset(valueset_url)
        except Exception as e:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error getting ValueSet from terminology service: {e}")
    
    # If not found, try direct import
    if not valueset:
        try:
            # Try to get ValueSet using get_value_set_by_url if available
            # This requires a list of ValueSets, which we don't have access to here
            # So we'll log a warning and return False
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet '{valueset_url}' not found in terminology service")
            return False
        except Exception as e:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error loading ValueSet '{valueset_url}': {e}")
            return False
    
    # Extract codes from field value
    codes = _extract_codes_from_value(field_value)
    
    if not codes:
        return False
    
    # Get codes from ValueSet
    try:
        valueset_codes = get_codes_from_valueset(valueset)
        
        # Check if any code is in the ValueSet
        for code in codes:
            if code in valueset_codes:
                logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' found in ValueSet '{valueset_url}'")
                return True
        
        logger.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - None of codes {codes} found in ValueSet '{valueset_url}'")
        return False
    except Exception as e:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error checking codes against ValueSet '{valueset_url}': {e}")
        return False


def _matches_date_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute date search matching.
    
    Date search matches dates/datetimes with optional prefixes.
    Prefixes: eq, ne, gt, lt, ge, le, sa, eb, ap
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    search_date = _parse_date_value(param.value)
    if search_date is None:
        return False
    
    prefix = param.prefix or "eq"
    
    # Handle list of dates
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_date_value(item, search_date, prefix):
                return True
        return False
    
    # Handle single date
    return _matches_date_value(field_value, search_date, prefix)


def _parse_date_value(date_str: str) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_str: Date string (YYYY-MM-DD or dateTime format)
    
    Returns:
        datetime object or None if invalid
    """
    try:
        # Try date format (YYYY-MM-DD)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return datetime.strptime(date_str, "%Y-%m-%d")
        
        # Try dateTime format
        # Remove timezone info for comparison
        date_str_clean = re.sub(r'[+\-]\d{2}:\d{2}$', '', date_str)
        date_str_clean = re.sub(r'Z$', '', date_str_clean)
        
        # Try various formats
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str_clean, fmt)
            except ValueError:
                continue
        
        return None
    except Exception:
        return None


def _matches_date_value(value: Any, search_date: datetime, prefix: str) -> bool:
    """
    Match a single date value against search criteria.
    
    Args:
        value: Date value (can be date, dateTime, Period, etc.)
        search_date: Search date
        prefix: Search prefix (eq, gt, lt, etc.)
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Handle datetime objects
    if isinstance(value, datetime):
        return _compare_dates(value, search_date, prefix)
    
    # Handle date objects
    if isinstance(value, date):
        value_dt = datetime.combine(value, datetime.min.time())
        return _compare_dates(value_dt, search_date, prefix)
    
    # Handle string dates
    if isinstance(value, str):
        value_date = _parse_date_value(value)
        if value_date:
            return _compare_dates(value_date, search_date, prefix)
    
    # Handle Period
    if hasattr(value, "start") or (isinstance(value, dict) and "start" in value):
        # Period search - check if search date is within period
        start = None
        end = None
        
        if hasattr(value, "start"):
            start = _parse_date_value(value.start) if isinstance(value.start, str) else value.start
        elif isinstance(value, dict):
            start = _parse_date_value(value.get("start")) if isinstance(value.get("start"), str) else value.get("start")
        
        if hasattr(value, "end"):
            end = _parse_date_value(value.end) if isinstance(value.end, str) else value.end
        elif isinstance(value, dict):
            end = _parse_date_value(value.get("end")) if isinstance(value.get("end"), str) else value.get("end")
        
        if start and end:
            if prefix == "eq":
                return start <= search_date <= end
            elif prefix == "ne":
                return not (start <= search_date <= end)
            elif prefix == "gt":
                return search_date > end
            elif prefix == "lt":
                return search_date < start
            elif prefix == "ge":
                return search_date >= end
            elif prefix == "le":
                return search_date <= start
            elif prefix == "sa":
                return search_date > end
            elif prefix == "eb":
                return search_date < start
            elif prefix == "ap":
                # Approximately - within 1 day
                return abs((search_date - start).days) <= 1 or abs((search_date - end).days) <= 1
        
        if start:
            # Only start date
            return _compare_dates(start, search_date, prefix)
        if end:
            # Only end date
            return _compare_dates(end, search_date, prefix)
    
    # Handle dict representation
    if isinstance(value, dict):
        if "start" in value or "end" in value:
            # Period
            return _matches_date_value(value, search_date, prefix)
        else:
            # Try to parse as date string
            value_date = _parse_date_value(str(value))
            if value_date:
                return _compare_dates(value_date, search_date, prefix)
    
    return False


def _compare_dates(value_date: datetime, search_date: datetime, prefix: str) -> bool:
    """
    Compare two dates using a prefix.
    
    Args:
        value_date: Value date
        search_date: Search date
        prefix: Comparison prefix (eq, ne, gt, lt, ge, le, sa, eb, ap)
    
    Returns:
        True if comparison matches, False otherwise
    """
    if prefix == "eq":
        return value_date.date() == search_date.date()
    elif prefix == "ne":
        return value_date.date() != search_date.date()
    elif prefix == "gt":
        return value_date > search_date
    elif prefix == "lt":
        return value_date < search_date
    elif prefix == "ge":
        return value_date >= search_date
    elif prefix == "le":
        return value_date <= search_date
    elif prefix == "sa":
        return value_date > search_date
    elif prefix == "eb":
        return value_date < search_date
    elif prefix == "ap":
        # Approximately - within 1 day
        diff = abs((value_date - search_date).days)
        return diff <= 1
    else:
        # Default to eq
        return value_date.date() == search_date.date()


def _matches_number_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute number search matching.
    
    Number search matches numeric values with optional prefixes.
    Prefixes: eq, ne, gt, lt, ge, le, sa, eb, ap
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    try:
        search_number = float(param.value)
    except ValueError:
        return False
    
    prefix = param.prefix or "eq"
    
    # Handle list of numbers
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_number_value(item, search_number, prefix):
                return True
        return False
    
    # Handle single number
    return _matches_number_value(field_value, search_number, prefix)


def _matches_number_value(value: Any, search_number: float, prefix: str) -> bool:
    """
    Match a single number value against search criteria.
    
    Args:
        value: Number value
        search_number: Search number
        prefix: Comparison prefix
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Extract numeric value
    number = None
    
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return False
    elif hasattr(value, "value"):
        # Quantity or similar
        if isinstance(value.value, (int, float)):
            number = float(value.value)
        elif isinstance(value.value, str):
            try:
                number = float(value.value)
            except ValueError:
                return False
    elif isinstance(value, dict):
        val = value.get("value")
        if isinstance(val, (int, float)):
            number = float(val)
        elif isinstance(val, str):
            try:
                number = float(val)
            except ValueError:
                return False
    
    if number is None:
        return False
    
    # Compare using prefix
    return _compare_numbers(number, search_number, prefix)


def _compare_numbers(value: float, search_value: float, prefix: str) -> bool:
    """
    Compare two numbers using a prefix.
    
    Args:
        value: Value number
        search_value: Search number
        prefix: Comparison prefix (eq, ne, gt, lt, ge, le, sa, eb, ap)
    
    Returns:
        True if comparison matches, False otherwise
    """
    if prefix == "eq":
        return abs(value - search_value) < 0.0001  # Floating point comparison
    elif prefix == "ne":
        return abs(value - search_value) >= 0.0001
    elif prefix == "gt":
        return value > search_value
    elif prefix == "lt":
        return value < search_value
    elif prefix == "ge":
        return value >= search_value
    elif prefix == "le":
        return value <= search_value
    elif prefix == "sa":
        return value > search_value
    elif prefix == "eb":
        return value < search_value
    elif prefix == "ap":
        # Approximately - within 10% or 0.1, whichever is larger
        diff = abs(value - search_value)
        tolerance = max(abs(search_value) * 0.1, 0.1)
        return diff <= tolerance
    else:
        # Default to eq
        return abs(value - search_value) < 0.0001


def _matches_quantity_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute quantity search matching.
    
    Quantity search matches quantities (number with optional system/code).
    Format: number|system|code or just number
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    search_number, search_system, search_code = parse_quantity_value(param.value)
    
    if search_number is None:
        return False
    
    prefix = param.prefix or "eq"
    
    # Handle list of quantities
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_quantity_value(item, search_number, search_system, search_code, prefix):

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
                return True

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return False
    
    # Handle single quantity
    return _matches_quantity_value(field_value, search_number, search_system, search_code, prefix)


def _matches_quantity_value(
    value: Any,
    search_number: float,
    search_system: Optional[str],
    search_code: Optional[str],
    prefix: str
) -> bool:
    """
    Match a single quantity value against search criteria.
    
    Args:
        value: Quantity value
        search_number: Search number
        search_system: Search system (optional)
        search_code: Search code (optional)
        prefix: Comparison prefix
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Extract quantity components
    number = None
    system = None
    code = None
    
    if hasattr(value, "value"):
        number = float(value.value) if isinstance(value.value, (int, float)) else None
    if hasattr(value, "system"):
        system = value.system
    if hasattr(value, "code"):
        code = value.code
    
    if isinstance(value, dict):
        val = value.get("value")
        number = float(val) if isinstance(val, (int, float)) else None
        system = value.get("system")
        code = value.get("code")
    
    if number is None:
        return False
    
    # Compare number first
    if not _compare_numbers(number, search_number, prefix):
        return False
    
    # If system/code specified, must match
    if search_system and system != search_system:
        return False
    if search_code and code != search_code:
        return False
    
    return True


def _matches_uri_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute URI search matching.
    
    URI search matches URIs (exact match).
    
    Supports modifiers:
    - :above - Above in hierarchy (URI is above target)
    - :below - Below in hierarchy (URI is below target)
    - :missing - Missing (true/false)
    
    Args:
        field_value: Field value from resource
        param: Search parameter
    
    Returns:
        True if matches, False otherwise
    """
    # Handle missing modifier
    if param.modifier == "missing":
        is_missing = (field_value is None or 
                     (isinstance(field_value, list) and len(field_value) == 0))
        return (param.value.lower() == "true") == is_missing
    
    # Handle :above and :below modifiers
    # These require hierarchy resolution which may not be available
    # For now, log a warning and fall back to basic matching
    if param.modifier in ["above", "below"]:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Modifier :{param.modifier} requires hierarchy resolution, falling back to basic matching")
        # Fall through to basic matching
    
    search_uri = param.value
    
    # Handle list of URIs
    if isinstance(field_value, list):
        for item in field_value:
            if _matches_uri_value(item, search_uri):
                return True
        return False
    
    # Handle single URI
    return _matches_uri_value(field_value, search_uri)


def _matches_uri_value(value: Any, search_uri: str) -> bool:
    """
    Match a single URI value against search criteria.
    
    Args:
        value: URI value
        search_uri: Search URI
    
    Returns:
        True if matches, False otherwise
    """
    if value is None:
        return False
    
    # Extract URI
    uri = None
    
    if isinstance(value, str):
        uri = value
    elif hasattr(value, "value"):
        uri = value.value
    elif isinstance(value, dict):
        uri = value.get("value") or value.get("url")
    
    if uri is None:
        return False
    
    # Exact match
    return uri == search_uri


def _matches_composite_search(field_value: Any, param: SearchParameter) -> bool:
    """
    Execute composite search matching.
    
    Composite search matches composite parameters (format depends on definition).
    Format: value1$value2$value3 (components separated by $)
    
    Composite search parameters combine multiple search criteria. Common patterns:
    - CodeableConcept: code$system (e.g., "active$http://hl7.org/fhir/observation-status")
    - Quantity: value$system$code (e.g., "5.0$http://unitsofmeasure.org$mg")
    - Date range: start$end (e.g., "2020-01-01$2020-12-31")
    
    Args:
        field_value: Field value from resource (can be complex type like CodeableConcept, Quantity, Period)
        param: Search parameter with composite value (format: value1$value2$...)
    
    Returns:
        True if matches, False otherwise
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Parse composite value (components separated by $)
    composite_parts = param.value.split("$")
    if not composite_parts:
        logger.warning(f"[{current_time}] Invalid composite search value (empty): {param.name}")
        return False
    
    # Handle None or empty field value
    if field_value is None:
        return False
    
    # Normalize field_value to list for iteration
    field_values = field_value if isinstance(field_value, list) else [field_value]
    
    # Try to match against any value in the list
    for fv in field_values:
        if _matches_composite_value(fv, composite_parts, param.name):
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.debug(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Composite search matched in {elapsed:.3f}s: {param.name}")
            return True
    
    elapsed = (datetime.now() - start_time).total_seconds()
    logger.debug(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Composite search did not match in {elapsed:.3f}s: {param.name}")
    return False


def _matches_composite_value(field_value: Any, composite_parts: List[str], param_name: str) -> bool:
    """
    Match a single field value against composite search parts.
    
    Args:
        field_value: Single field value (CodeableConcept, Quantity, Period, etc.)
        composite_parts: List of composite value parts (e.g., ["code", "system"])
        param_name: Parameter name for logging
    
    Returns:
        True if matches, False otherwise
    """
    # Handle dict-based complex types (JSON representation)
    if isinstance(field_value, dict):
        return _matches_composite_dict(field_value, composite_parts, param_name)
    
    # Handle object-based complex types (Python objects with attributes)
    if hasattr(field_value, '__dict__') or hasattr(field_value, '__class__'):
        return _matches_composite_object(field_value, composite_parts, param_name)
    
    # Handle string/primitive types - try to match first part
    if len(composite_parts) > 0:
        str_value = str(field_value) if field_value is not None else ""
        return str_value == composite_parts[0] or composite_parts[0] in str_value
    
    return False


def _matches_composite_dict(field_value: Dict[str, Any], composite_parts: List[str], param_name: str) -> bool:
    """
    Match a dict-based complex type against composite search parts.
    
    Common patterns:
    - CodeableConcept: {"code": "...", "system": "..."} matches code$system
    - Quantity: {"value": ..., "system": "...", "code": "..."} matches value$system$code
    - Period: {"start": "...", "end": "..."} matches start$end
    
    Args:
        field_value: Dict representation of complex type
        composite_parts: List of composite value parts
        param_name: Parameter name for logging
    
    Returns:
        True if matches, False otherwise
    """
    # Pattern 1: CodeableConcept (code$system)
    if len(composite_parts) >= 2 and "code" in field_value:
        code_match = str(field_value.get("code", "")) == composite_parts[0]
        system_match = str(field_value.get("system", "")) == composite_parts[1] if len(composite_parts) > 1 else True
        if code_match and (len(composite_parts) == 1 or system_match):
            return True
    
    # Pattern 2: Quantity (value$system$code)
    if len(composite_parts) >= 1 and "value" in field_value:
        value_match = str(field_value.get("value", "")) == composite_parts[0]
        system_match = (str(field_value.get("system", "")) == composite_parts[1]) if len(composite_parts) > 1 else True
        code_match = (str(field_value.get("code", "")) == composite_parts[2]) if len(composite_parts) > 2 else True
        if value_match and (len(composite_parts) == 1 or (system_match and (len(composite_parts) == 2 or code_match))):
            return True
    
    # Pattern 3: Period (start$end)
    if len(composite_parts) >= 1 and ("start" in field_value or "end" in field_value):
        start_match = (str(field_value.get("start", "")) == composite_parts[0]) if len(composite_parts) > 0 else True
        end_match = (str(field_value.get("end", "")) == composite_parts[1]) if len(composite_parts) > 1 else True
        if start_match and (len(composite_parts) == 1 or end_match):
            return True
    
    # Pattern 4: Coding (code$system$version$display)
    if len(composite_parts) >= 1 and "code" in field_value:
        code_match = str(field_value.get("code", "")) == composite_parts[0]
        system_match = (str(field_value.get("system", "")) == composite_parts[1]) if len(composite_parts) > 1 else True
        if code_match and (len(composite_parts) == 1 or system_match):
            return True
    
    # Pattern 5: Identifier (value$system or value$system$type)
    if len(composite_parts) >= 1 and "value" in field_value:
        value_match = str(field_value.get("value", "")) == composite_parts[0]
        system_match = (str(field_value.get("system", "")) == composite_parts[1]) if len(composite_parts) > 1 else True
        if value_match and (len(composite_parts) == 1 or system_match):
            return True
    
    # Generic matching: try to match parts against any dict values
    dict_values = [str(v) for v in field_value.values() if v is not None]
    if len(composite_parts) <= len(dict_values):
        # Check if all composite parts match some dict values
        matches = 0
        for part in composite_parts:
            if any(part in val or val == part for val in dict_values):
                matches += 1
        return matches == len(composite_parts)
    
    return False


def _matches_composite_object(field_value: Any, composite_parts: List[str], param_name: str) -> bool:
    """
    Match an object-based complex type against composite search parts.
    
    Args:
        field_value: Object with attributes (e.g., CodeableConcept, Quantity objects)
        composite_parts: List of composite value parts
        param_name: Parameter name for logging
    
    Returns:
        True if matches, False otherwise
    """
    # Try to access common attributes
    # Pattern 1: CodeableConcept (code$system)
    if hasattr(field_value, 'code') and hasattr(field_value, 'system'):
        code_match = str(getattr(field_value, 'code', '')) == composite_parts[0]
        system_match = (str(getattr(field_value, 'system', '')) == composite_parts[1]) if len(composite_parts) > 1 else True
        if code_match and (len(composite_parts) == 1 or system_match):
            return True
    
    # Pattern 2: Quantity (value$system$code)
    if hasattr(field_value, 'value'):
        value_match = str(getattr(field_value, 'value', '')) == composite_parts[0]
        system_match = (str(getattr(field_value, 'system', '')) == composite_parts[1]) if len(composite_parts) > 1 else True
        code_match = (str(getattr(field_value, 'code', '')) == composite_parts[2]) if len(composite_parts) > 2 else True
        if value_match and (len(composite_parts) == 1 or (system_match and (len(composite_parts) == 2 or code_match))):
            return True
    
    # Pattern 3: Period (start$end)
    if hasattr(field_value, 'start') or hasattr(field_value, 'end'):
        start_match = (str(getattr(field_value, 'start', '')) == composite_parts[0]) if len(composite_parts) > 0 else True
        end_match = (str(getattr(field_value, 'end', '')) == composite_parts[1]) if len(composite_parts) > 1 else True
        if start_match and (len(composite_parts) == 1 or end_match):
            return True
    
    # Pattern 4: Coding (code$system)
    if hasattr(field_value, 'code'):
        code_match = str(getattr(field_value, 'code', '')) == composite_parts[0]
        system_match = (str(getattr(field_value, 'system', '')) == composite_parts[1]) if len(composite_parts) > 1 else True
        if code_match and (len(composite_parts) == 1 or system_match):
            return True
    
    # Pattern 5: Identifier (value$system)
    if hasattr(field_value, 'value'):
        value_match = str(getattr(field_value, 'value', '')) == composite_parts[0]
        system_match = (str(getattr(field_value, 'system', '')) == composite_parts[1]) if len(composite_parts) > 1 else True
        if value_match and (len(composite_parts) == 1 or system_match):
            return True
    
    return False


def _matches_chained_parameter(
    resource: FHIRResource,
    param: SearchParameter,
    param_type_map: Optional[Dict[str, str]],
    resource_resolver: Optional[callable] = None
) -> bool:
    """
    Match a chained search parameter.
    
    Chained parameters have format: resourceType.parameterName
    Example: patient.name=John
    
    Args:
        resource: Resource to check
        param: Chained search parameter
        param_type_map: Optional parameter type map
        resource_resolver: Optional function to resolve references (reference: str) -> Optional[FHIRResource]
    
    Returns:
        True if matches, False otherwise
    """
    # Parse chain
    parts = param.name.split(".", 1)
    if len(parts) != 2:
        return False
    
    reference_field = parts[0]  # e.g., "patient"
    chained_param_name = parts[1]  # e.g., "name"
    
    # Get reference field value
    reference_value = _get_field_value(resource, reference_field)
    
    if reference_value is None:
        return False
    
    # Handle list of references
    references = reference_value if isinstance(reference_value, list) else [reference_value]
    
    # Resolve each reference and check if it matches
    if not resource_resolver:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Chained search requires resource_resolver: {param.name}")
        return False
    
    for ref in references:
        # Extract reference string
        ref_str = None
        if isinstance(ref, str):
            ref_str = ref
        elif hasattr(ref, "reference"):
            ref_str = ref.reference
        elif isinstance(ref, dict):
            ref_str = ref.get("reference")
        
        if not ref_str:
            continue
        
        # Resolve reference
        referenced_resource = resource_resolver(ref_str)
        if referenced_resource is None:
            continue
        
        # Check if referenced resource matches chained parameter
        chained_param = SearchParameter(
            name=chained_param_name,
            value=param.value,
            modifier=param.modifier,
            prefix=param.prefix
        )
        if resource_matches_parameter(referenced_resource, chained_param, param_type_map, resource_resolver):
            return True
    
    return False


def _apply_reverse_chaining(
    resources: List[FHIRResource],
    search_params: SearchParameters,
    param_type_map: Optional[Dict[str, str]] = None,
    all_resources: Optional[List[FHIRResource]] = None,
    resource_resolver: Optional[callable] = None
) -> List[FHIRResource]:
    """
    Apply reverse chain search parameters to filter resources.
    
    Reverse chain format: _has:ResourceType:parameterName=value
    Example: _has:Observation:code=718-7 finds Patients that have Observations with code 718-7
    
    Args:
        resources: List of resources to filter
        search_params: Search parameters (may contain reverse chain parameters)
        param_type_map: Optional parameter type map
        all_resources: Optional list of all resources in the system (required for reverse chaining)
        resource_resolver: Optional function to resolve references
    
    Returns:
        Filtered list of resources
    """
    from dnhealth.dnhealth_fhir.search import parse_reverse_chain_parameter
    
    # Find all reverse chain parameters
    reverse_chain_params = [p for p in search_params.parameters if is_reverse_chain_parameter(p.name)]
    
    if not reverse_chain_params:
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return resources
    
    # For each reverse chain parameter, filter resources
    filtered = resources
    for param in reverse_chain_params:
        resource_type, parameter_name = parse_reverse_chain_parameter(param.name)
        if not resource_type or not parameter_name:
            continue
        
        # Create a search parameter for the reverse chain parameter
        # The parameter name is the actual search parameter on the referenced resource type
        reverse_param = SearchParameter(
            name=parameter_name,
            value=param.value,
            modifier=param.modifier,
            prefix=param.prefix
        )
        
        # Find all resources of the specified type that match the parameter
        # Use all_resources if provided, otherwise use resources (limited functionality)
        searchable_resources = all_resources if all_resources is not None else resources
        
        # Filter resources of the specified type
        matching_referenced_resources = []
        for res in searchable_resources:
            # Check if resource is of the specified type
            if res.resource_type == resource_type:
                # Check if this resource matches the reverse chain parameter
                if resource_matches_parameter(res, reverse_param, param_type_map, resource_resolver):
                    matching_referenced_resources.append(res)
        
        # Now find which of the filtered resources are referenced by the matching resources
        # Extract references from matching resources that point to filtered resources
        referenced_resource_ids = set()
        
        for matching_res in matching_referenced_resources:
            # Get all reference fields from the matching resource
            # Look for references that point to resources in the filtered list
            refs = _extract_references_from_resource(matching_res)
            
            for ref in refs:
                # Check if this reference points to any resource in the filtered list
                for filtered_res in filtered:
                    ref_id = f"{filtered_res.resource_type}/{filtered_res.id}" if filtered_res.id else None
                    if ref_id and (ref == ref_id or ref.endswith(f"/{filtered_res.id}")):
                        referenced_resource_ids.add(filtered_res.id if filtered_res.id else "")
        
        # Filter to only include resources that are referenced
        if referenced_resource_ids:
            filtered = [r for r in filtered if r.id and r.id in referenced_resource_ids]
        else:
            # No matches found, return empty list
            filtered = []
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Reverse chaining applied: {len(filtered)} resources match _has:{resource_type}:{parameter_name}={param.value}")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return filtered


def _extract_references_from_resource(resource: FHIRResource) -> List[str]:
    """
    Extract all reference values from a FHIR resource.
    
    This function recursively searches through the resource to find all reference fields
    and extract their values.
    
    Args:
        resource: FHIR resource to extract references from
    
    Returns:
        List of reference strings (e.g., ["Patient/123", "Organization/456"])
    """
    references = []
    
    def extract_from_value(value: Any) -> None:
        """Recursively extract references from a value."""
        if value is None:
            return
        
        if isinstance(value, dict):
            # Check if this is a Reference object
            if "reference" in value:
                ref_str = value["reference"]
                if ref_str:
                    references.append(ref_str)
            # Recursively process dictionary values
            for v in value.values():
                extract_from_value(v)
        elif isinstance(value, list):
            # Process list items
            for item in value:
                extract_from_value(item)
        elif hasattr(value, "__dict__"):
            # Process object attributes
            for attr_name, attr_value in value.__dict__.items():
                # Skip private attributes
                if not attr_name.startswith("_"):
                    extract_from_value(attr_value)
    
    # Extract references from resource
    if hasattr(resource, "__dict__"):
        for attr_name, attr_value in resource.__dict__.items():
            if not attr_name.startswith("_"):
                extract_from_value(attr_value)
    elif isinstance(resource, dict):
        extract_from_value(resource)
    
    return references


def sort_search_results(
    resources: List[FHIRResource],
    sort_params: List[str],
    param_type_map: Optional[Dict[str, str]] = None
) -> List[FHIRResource]:
    """
    Sort search results by specified parameters.
    
    Sort format: parameter or -parameter (descending)
    Example: _sort=name,-birthDate sorts by name ascending, then birthDate descending
    
    Args:
        resources: List of resources to sort
        sort_params: List of sort parameters (e.g., ["name", "-birthDate"])
        param_type_map: Optional parameter type map
    
    Returns:
        Sorted list of resources
    """
    if not sort_params or not resources:
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return resources
    
    def get_sort_key(resource: FHIRResource) -> tuple:
        """Get sort key for a resource."""
        keys = []
        for sort_param in sort_params:
            # Check if descending
            descending = sort_param.startswith("-")
            param_name = sort_param[1:] if descending else sort_param
            
            # Get field value
            value = _get_field_value(resource, param_name)
            
            # Convert to sortable value
            if value is None:
                sort_value = None
            elif isinstance(value, list) and len(value) > 0:
                # Use first value for sorting
                sort_value = _get_sortable_value(value[0])
            else:
                sort_value = _get_sortable_value(value)
            
            # For descending, invert the value
            if descending:
                keys.append((sort_value is not None, sort_value))
            else:
                keys.append((sort_value is not None, sort_value))
        
        return tuple(keys)
    
    try:
        sorted_resources = sorted(resources, key=get_sort_key)
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return sorted_resources
    except Exception as e:
        logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error sorting results: {e}")
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return resources


def _get_sortable_value(value: Any) -> Any:
    """
    Convert a value to a sortable format.
    
    Args:
        value: Value to convert
    
    Returns:
        Sortable value
    """
    if value is None:
        return None
    
    # Handle strings
    if isinstance(value, str):
        return value.lower()
    
    # Handle numbers
    if isinstance(value, (int, float)):
        return value
    
    # Handle dates
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    
    # Handle objects with value attributes
    if hasattr(value, "value"):
        return _get_sortable_value(value.value)
    
    # Handle dicts
    if isinstance(value, dict):
        # Try common fields
        for field in ["value", "code", "display", "text"]:
            if field in value:
                return _get_sortable_value(value[field])
        # Use string representation
        return str(value).lower()
    
    # Default: convert to string
    return str(value).lower()


def process_include(
    search_results: List[FHIRResource],
    include_params: List[str],
    resource_resolver: Optional[callable] = None
) -> List[FHIRResource]:
    """
    Process _include parameters to add referenced resources to results.
    
    Include format: ResourceType:searchParam
    Example: _include=Observation:subject includes Patient resources referenced by Observation.subject
    
    Args:
        search_results: Original search results
        include_params: List of include parameters (e.g., ["Observation:subject"])
        resource_resolver: Optional function to resolve references (reference: str) -> Optional[FHIRResource]
    
    Returns:
        Combined list of resources (original + included)
    """
    if not include_params or not resource_resolver:
        return search_results
    
    included_resources = []
    included_ids = set()  # Track already included resources
    
    for include_param in include_params:
        if ":" not in include_param:
            continue
        
        resource_type, search_param = include_param.split(":", 1)
        
        # Find references in search results
        for resource in search_results:
            # Get field value for search parameter
            field_value = _get_field_value(resource, search_param)
            
            if field_value is None:
                continue

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            
            # Handle list of references
            references = field_value if isinstance(field_value, list) else [field_value]
            
            for ref in references:
                # Extract reference string
                ref_str = None
                if isinstance(ref, str):
                    ref_str = ref
                elif hasattr(ref, "reference"):
                    ref_str = ref.reference
                elif isinstance(ref, dict):
                    ref_str = ref.get("reference")
                
                if not ref_str:
                    continue
                
                # Resolve reference
                referenced_resource = resource_resolver(ref_str)
                if referenced_resource and referenced_resource.id:
                    resource_id = f"{referenced_resource.resourceType}/{referenced_resource.id}"
                    if resource_id not in included_ids:
                        included_resources.append(referenced_resource)
                        included_ids.add(resource_id)
    
    return search_results + included_resources


def process_revinclude(
    search_results: List[FHIRResource],
    revinclude_params: List[str],
    all_resources: Optional[List[FHIRResource]] = None
) -> List[FHIRResource]:
    """
    Process _revinclude parameters to add resources that reference search results.
    
    Revinclude format: ResourceType:searchParam
    Example: _revinclude=Observation:subject includes Observations that reference Patient
    
    Args:
        search_results: Original search results
        revinclude_params: List of revinclude parameters (e.g., ["Observation:subject"])
        all_resources: Optional list of all resources to search for references
    
    Returns:
        Combined list of resources (original + revincluded)
    """
    if not revinclude_params or not all_resources:
        return search_results
    
    revincluded_resources = []
    result_ids = {f"{r.resourceType}/{r.id}" for r in search_results if r.id}
    
    for revinclude_param in revinclude_params:
        if ":" not in revinclude_param:
            continue
        
        resource_type, search_param = revinclude_param.split(":", 1)
        
        # Find resources of specified type that reference search results
        for resource in all_resources:
            if resource.resourceType != resource_type:
                continue
            
            # Get field value for search parameter
            field_value = _get_field_value(resource, search_param)
            
            if field_value is None:
                continue
            
            # Handle list of references
            references = field_value if isinstance(field_value, list) else [field_value]
            
            # Check if any reference matches search results
            for ref in references:
                ref_str = None
                if isinstance(ref, str):
                    ref_str = ref
                elif hasattr(ref, "reference"):
                    ref_str = ref.reference
                elif isinstance(ref, dict):
                    ref_str = ref.get("reference")
                
                if ref_str and ref_str in result_ids:
                    revincluded_resources.append(resource)
                    break
    
    return search_results + revincluded_resources
