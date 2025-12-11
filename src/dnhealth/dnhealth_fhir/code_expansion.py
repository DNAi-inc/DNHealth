# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Code expansion utilities.

Provides functions to expand ValueSets to get all codes they contain.
"""

from typing import List, Optional, Set, Dict, Any
from datetime import datetime
from dnhealth.dnhealth_fhir.valueset_resource import (
    ValueSet,
    ValueSetCompose,
    ValueSetComposeInclude,
    ValueSetComposeIncludeConcept,
    ValueSetExpansion,
    ValueSetExpansionContains,
    get_codes_from_valueset
)
from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystem, get_codes_from_codesystem


def expand_valueset(
    valueset: ValueSet,
    codesystems: Optional[Dict[str, CodeSystem]] = None,
    nested_valuesets: Optional[Dict[str, ValueSet]] = None,# Log completion timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
    include_designations: bool = False
) -> ValueSetExpansion:
    """
    Expand a ValueSet to get all codes it contains.
    
    Args:
        valueset: ValueSet resource to expand
        codesystems: Optional dictionary of CodeSystem URL -> CodeSystem for expanding includes
        nested_valuesets: Optional dictionary of ValueSet URL -> ValueSet for nested ValueSet references
        include_designations: Whether to include designations in expansion
        
    Returns:
        ValueSetExpansion object with all codes
    """
    # If ValueSet already has an expansion, use it
    if valueset.expansion and valueset.expansion.contains:
        return valueset.expansion
    
    # Otherwise, expand from compose
    if not valueset.compose:
        # No compose section - return empty expansion
        return ValueSetExpansion(
            identifier=None,
            timestamp=datetime.now().isoformat(),
            total=0,
            contains=[]
        )
    
    codes: Set[str] = set()
    code_details: Dict[str, Dict[str, Any]] = {}  # code -> {system, display, ...}
    
    # Expand includes
    for include in valueset.compose.include:
        _expand_include(
            include,
            codes,
            code_details,
            codesystems=codesystems,
            nested_valuesets=nested_valuesets,
            include_designations=include_designations
        )
    
    # Exclude codes
    for exclude in valueset.compose.exclude:
        _expand_exclude(
            exclude,
            codes,
            code_details,
            codesystems=codesystems,
            nested_valuesets=nested_valuesets
        )
    
    # Convert to ValueSetExpansionContains
    contains = []
    for code in sorted(codes):
        details = code_details.get(code, {})
        contains.append(ValueSetExpansionContains(
            system=details.get("system"),
            code=code,
            display=details.get("display"),
            designation=details.get("designation", []) if include_designations else []
        ))
    
    return ValueSetExpansion(
        identifier=None,
        timestamp=datetime.now().isoformat(),
        total=len(contains),
        contains=contains
    )


def _expand_include(
    include: ValueSetComposeInclude,    codes: Set[str],
    code_details: Dict[str, Dict[str, Any]],
    codesystems: Optional[Dict[str, CodeSystem]] = None,
    nested_valuesets: Optional[Dict[str, ValueSet]] = None,
    include_designations: bool = False
) -> None:
    """
    Expand a ValueSet compose include section.
    
    Args:
        include: ValueSetComposeInclude to expand
        codes: Set to add codes to
        code_details: Dictionary to add code details to
        codesystems: Optional CodeSystem dictionary
        nested_valuesets: Optional ValueSet dictionary
        include_designations: Whether to include designations
    """
    # Handle direct concepts
    for concept in include.concept:
        if concept.code:
            codes.add(concept.code)
            code_details[concept.code] = {
                "system": include.system,
                "display": concept.display,
                "designation": concept.designation if include_designations else []
            }
    
    # Handle filters (simplified - just include all codes from system if filter matches)
    if include.filter:
        # For now, if there are filters, we'd need to apply them
        # This is a simplified implementation
        if include.system and codesystems:
            codesystem = codesystems.get(include.system)
            if codesystem:
                system_codes = get_codes_from_codesystem(codesystem)
                for code in system_codes:
                    if _apply_filters(code, include.filter, codesystem):
                        codes.add(code)
                        if code not in code_details:
                            code_details[code] = {
                                "system": include.system,
                                "display": None
                            }
    
    # Handle valueSet references (nested ValueSets)
    if include.valueSet:
        for valueset_url in include.valueSet:
            if nested_valuesets:
                nested_valueset = nested_valuesets.get(valueset_url)
                if nested_valueset:
                    # Recursively expand nested ValueSet
                    nested_expansion = expand_valueset(
                        nested_valueset,
                        codesystems=codesystems,
                        nested_valuesets=nested_valuesets,
                        include_designations=include_designations
                    )
                    # Add codes from nested expansion
                    for contains_item in nested_expansion.contains:
                        if contains_item.code:
                            codes.add(contains_item.code)
                            if contains_item.code not in code_details:
                                code_details[contains_item.code] = {
                                    "system": contains_item.system or include.system,
                                    "display": contains_item.display,
                                    "designation": contains_item.designation if include_designations else []
                                }
                        # Handle nested contains recursively
                        if contains_item.contains:
                            _add_nested_contains(
                                contains_item.contains,
                                codes,
                                code_details,
                                include.system,
                                include_designations

                                    # Log completion timestamp at end of operation
                                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    logger.info(f"Current Time at End of Operations: {current_time}")
                            )


def _expand_exclude(
    exclude: ValueSetComposeInclude,
    codes: Set[str],
    code_details: Dict[str, Dict[str, Any]],
    codesystems: Optional[Dict[str, CodeSystem]] = None,
    nested_valuesets: Optional[Dict[str, ValueSet]] = None
) -> None:
    """
    Expand a ValueSet compose exclude section and remove codes.
    
    Args:
        exclude: ValueSetComposeInclude to expand for exclusion
        codes: Set to remove codes from
        code_details: Dictionary to remove code details from
        codesystems: Optional CodeSystem dictionary
        nested_valuesets: Optional ValueSet dictionary
    """
    # Handle direct concepts
    for concept in exclude.concept:
        if concept.code and concept.code in codes:
            codes.remove(concept.code)
            if concept.code in code_details:
                del code_details[concept.code]
    
    # Handle valueSet references
    if exclude.valueSet:
        for valueset_url in exclude.valueSet:
            if nested_valuesets:
                nested_valueset = nested_valuesets.get(valueset_url)
                if nested_valueset:
                    # Recursively expand nested ValueSet to get all codes to exclude
                    nested_expansion = expand_valueset(
                        nested_valueset,
                        codesystems=codesystems,
                        nested_valuesets=nested_valuesets
                    )
                    # Remove codes from nested expansion
                    for contains_item in nested_expansion.contains:
                        if contains_item.code and contains_item.code in codes:
                            codes.remove(contains_item.code)
                        if contains_item.code and contains_item.code in code_details:
                            del code_details[contains_item.code]
                        # Handle nested contains recursively
                        if contains_item.contains:
                            _remove_nested_contains(
                                contains_item.contains,
                                codes,
                                code_details
                            )


def _apply_filters(
    code: str,
    filters: List[Any],
    codesystem: CodeSystem
) -> bool:
    """
    Apply filters to determine if a code should be included.
    
    Supports common filter operators:
    - = : exact match
    - is-a : code is a descendant of filter value
    - descendent-of : code is a descendant of filter value
    - is-not-a : code is not a descendant of filter value
    - regex : regular expression match
    - in : code is in list of values
    - not-in : code is not in list of values
    - exists : property exists
    
    Args:
        code: Code to check
        filters: List of ValueSetComposeIncludeFilter objects
        codesystem: CodeSystem to check against
        
    Returns:
        True if code passes all filters, False otherwise
    """
    from dnhealth.dnhealth_fhir.valueset_resource import ValueSetComposeIncludeFilter
    from dnhealth.dnhealth_fhir.codesystem_resource import get_concept_by_code, CodeSystemConcept
    import re
    
    # If no filters, include all codes
    if not filters:
        return True
    
    # All filters must pass (AND logic)
    for filter_obj in filters:
        if not isinstance(filter_obj, ValueSetComposeIncludeFilter):
            continue
        
        property_name = filter_obj.property
        operator = filter_obj.op
        filter_value = filter_obj.value
        
        if not property_name or not operator:
            # Invalid filter - skip it
            continue
        
        # Get the concept for this code
        concept = get_concept_by_code(codesystem, code)
        if not concept:
            # Code not found - filter fails
            return False
        
        # Handle different operators
        if operator == "=":
            # Exact match on property value
            prop_value = _get_property_value(concept, property_name)
            if prop_value != filter_value:
                return False
        
        elif operator == "is-a" or operator == "descendent-of":
            # Code must be a descendant of filter_value
            if not _is_descendant_of(codesystem, code, filter_value):
                return False
        
        elif operator == "is-not-a":
            # Code must not be a descendant of filter_value
            if _is_descendant_of(codesystem, code, filter_value):
                return False
        
        elif operator == "regex":
            # Regular expression match on code or property
            if property_name == "code":
                if not re.match(filter_value, code):
                    return False
            else:
                prop_value = _get_property_value(concept, property_name)
                if prop_value and not re.match(filter_value, str(prop_value)):
                    return False
        
        elif operator == "in":
            # Code or property value must be in comma-separated list
            value_list = [v.strip() for v in filter_value.split(",")]
            if property_name == "code":
                if code not in value_list:
                    return False
            else:
                prop_value = _get_property_value(concept, property_name)
                if prop_value not in value_list:
                    return False
        
        elif operator == "not-in":
            # Code or property value must not be in comma-separated list
            value_list = [v.strip() for v in filter_value.split(",")]
            if property_name == "code":
                if code in value_list:
                    return False
            else:
                prop_value = _get_property_value(concept, property_name)
                if prop_value in value_list:
                    return False
        
        elif operator == "exists":
            # Property must exist
            prop_value = _get_property_value(concept, property_name)
            if prop_value is None:
                return False
        
        else:
            # Unknown operator - for safety, exclude the code
            return False
    
    # All filters passed
    return True


def _get_property_value(concept: "CodeSystemConcept", property_name: str) -> Optional[str]:
    """
    Get a property value from a concept.
    
    Args:
        concept: CodeSystemConcept to get property from
        property_name: Name of the property
        
    Returns:
        Property value as string, or None if not found
    """
    from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystemConcept
    
    # Special property: "code" returns the code itself
    if property_name == "code":
        return concept.code
    
    # Check concept properties
    for prop in concept.property:
        if prop.code == property_name:
            # Return the first matching property value
            if prop.valueCode:
                return prop.valueCode
            elif prop.valueString:
                return prop.valueString
            elif prop.valueInteger is not None:
                return str(prop.valueInteger)
            elif prop.valueBoolean is not None:
                return str(prop.valueBoolean)
            elif prop.valueDecimal is not None:
                return str(prop.valueDecimal)
            elif prop.valueDateTime:
                return prop.valueDateTime
    
    return None


def _is_descendant_of(codesystem: CodeSystem, code: str, ancestor_code: str) -> bool:
    """
    Check if a code is a descendant of another code in the CodeSystem hierarchy.
    
    Args:
        codesystem: CodeSystem containing the codes
        code: Code to check
        ancestor_code: Potential ancestor code
        
    Returns:
        True if code is a descendant of ancestor_code, False otherwise
    """
    from dnhealth.dnhealth_fhir.codesystem_resource import get_concept_by_code, CodeSystemConcept
    
    # If codes are the same, it's not a descendant (it's the same)
    if code == ancestor_code:
        return False
    
    # Find the ancestor concept
    ancestor_concept = get_concept_by_code(codesystem, ancestor_code)
    if not ancestor_concept:
        return False
    
    # Recursively check if code is in the descendant tree
    return _is_code_in_descendants(ancestor_concept, code)


def _is_code_in_descendants(concept: "CodeSystemConcept", target_code: str) -> bool:
    """
    Recursively check if target_code is in the descendant tree of concept.
    
    Args:
        concept: Parent concept to search from
        target_code: Code to find
        
    Returns:
        True if target_code is found in descendants, False otherwise
    """
    from dnhealth.dnhealth_fhir.codesystem_resource import CodeSystemConcept
    
    # Check nested concepts
    for nested_concept in concept.concept:
        if nested_concept.code == target_code:
            return True
        # Recursively check descendants
        if _is_code_in_descendants(nested_concept, target_code):

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            return True
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return False


def get_expanded_codes(
    valueset: ValueSet,
    codesystems: Optional[Dict[str, CodeSystem]] = None,
    nested_valuesets: Optional[Dict[str, ValueSet]] = None
) -> Set[str]:
    """
    Get all codes from an expanded ValueSet.
    
    Convenience function that expands a ValueSet and returns just the codes.
    
    Args:
        valueset: ValueSet resource to expand
        codesystems: Optional CodeSystem dictionary
        nested_valuesets: Optional ValueSet dictionary
        
    Returns:
        Set of code strings
    """
    expansion = expand_valueset(valueset, codesystems=codesystems, nested_valuesets=nested_valuesets)
    codes = set()
    for contains in expansion.contains:
        if contains.code:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
            codes.add(contains.code)
        # Handle nested contains
        if contains.contains:
            for nested in contains.contains:

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
                if nested.code:
                    codes.add(nested.code)
    return codes


def expand_valueset_to_expansion(
    valueset: ValueSet,
    codesystems: Optional[Dict[str, CodeSystem]] = None,
    nested_valuesets: Optional[Dict[str, ValueSet]] = None
) -> ValueSet:
    """
    Expand a ValueSet and add the expansion to it.
    
    Args:
        valueset: ValueSet resource to expand
        codesystems: Optional CodeSystem dictionary
        nested_valuesets: Optional ValueSet dictionary
        
    Returns:
        ValueSet with expansion added
    """

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
    from copy import deepcopy
import logging
    

logger = logging.getLogger(__name__)
    expanded = deepcopy(valueset)
    expansion = expand_valueset(
        valueset,
        codesystems=codesystems,
        nested_valuesets=nested_valuesets
    )
    expanded.expansion = expansion
    return expanded


def _add_nested_contains(
    contains_list: List[ValueSetExpansionContains],
    codes: Set[str],
    code_details: Dict[str, Dict[str, Any]],
    default_system: Optional[str],
    include_designations: bool
) -> None:
    """
    Recursively add codes from nested ValueSetExpansionContains.
    
    Args:
        contains_list: List of ValueSetExpansionContains objects
        codes: Set to add codes to
        code_details: Dictionary to add code details to
        default_system: Default system to use if contains item has no system
        include_designations: Whether to include designations

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
    """
    for contains_item in contains_list:
        if contains_item.code:
            codes.add(contains_item.code)
            if contains_item.code not in code_details:
                code_details[contains_item.code] = {
                    "system": contains_item.system or default_system,
                    "display": contains_item.display,
                    "designation": contains_item.designation if include_designations else []
                }
        # Recursively handle nested contains
        if contains_item.contains:
            _add_nested_contains(
                contains_item.contains,
                codes,
                code_details,
                default_system,
                include_designations
            )


def _remove_nested_contains(
    contains_list: List[ValueSetExpansionContains],
    codes: Set[str],
    code_details: Dict[str, Dict[str, Any]]
) -> None:
    """
    Recursively remove codes from nested ValueSetExpansionContains.
    
    Args:
        contains_list: List of ValueSetExpansionContains objects
        codes: Set to remove codes from
        code_details: Dictionary to remove code details from
    """
    for contains_item in contains_list:
        if contains_item.code:
            if contains_item.code in codes:
                codes.remove(contains_item.code)
            if contains_item.code in code_details:
                del code_details[contains_item.code]
        # Recursively handle nested contains
        if contains_item.contains:
            _remove_nested_contains(
                contains_item.contains,
                codes,
                code_details
            )

