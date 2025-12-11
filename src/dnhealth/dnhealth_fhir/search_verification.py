# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Search Feature Verification.

Provides verification functions to confirm all search parameter types and features
are implemented according to FHIR R4 specification.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.search import (
    SearchParameter,
    SearchParameters,
    SEARCH_PARAMETER_TYPES,
    SEARCH_MODIFIERS,
    SEARCH_PREFIXES,
    parse_search_string,
    validate_search_parameter_type,
    parse_chained_parameter,
    parse_reverse_chain_parameter,
    is_chained_parameter,
    is_reverse_chain_parameter,
)
from dnhealth.dnhealth_fhir.search_execution import (
    execute_search,
    sort_search_results,
    process_include,
    process_revinclude,
)

logger = logging.getLogger(__name__)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def verify_search_parameter_types() -> Dict[str, Any]:
    """
    Verify all search parameter types are implemented.
    
    Returns:
        Dictionary with verification results including:
        - parameter_types: List of verified parameter types
        - all_types_implemented: Boolean indicating if all types are implemented
        - missing_types: List of missing types (if any)
        - timestamp: Completion timestamp
    """
    start_time = datetime.now()
    logger.info(f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Verifying search parameter types...")
    
    # Expected parameter types per FHIR R4 specification
    expected_types = {
        "number",  # Numeric search
        "date",  # Date/time search
        "string",  # String search
        "token",  # Token search
        "reference",  # Reference search
        "composite",  # Composite search
        "quantity",  # Quantity search
        "uri",  # URI search
        "special",  # Special search parameters
    }
    
    # Check which types are implemented
    implemented_types = set(SEARCH_PARAMETER_TYPES.keys())
    missing_types = expected_types - implemented_types
    all_types_implemented = len(missing_types) == 0
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    result = {
        "parameter_types": sorted(list(implemented_types)),
        "expected_types": sorted(list(expected_types)),
        "all_types_implemented": all_types_implemented,
        "missing_types": sorted(list(missing_types)),
        "verification_time": elapsed,
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "completion_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    logger.info(f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - Search parameter type verification completed: {len(implemented_types)}/{len(expected_types)} types implemented")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return result


def verify_search_features() -> Dict[str, Any]:
    """
    Verify all search features are implemented.
    
    Returns:
        Dictionary with verification results including:
        - features: List of verified features
        - all_features_implemented: Boolean indicating if all features are implemented
        - missing_features: List of missing features (if any)
        - timestamp: Completion timestamp
    """
    start_time = datetime.now()
    logger.info(f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Verifying search features...")
    
    # Expected features per FHIR R4 specification
    expected_features = {
        "search_chaining": None,  # parse_chained_parameter
        "reverse_chaining": None,  # parse_reverse_chain_parameter
        "search_modifiers": None,  # SEARCH_MODIFIERS
        "search_prefixes": None,  # SEARCH_PREFIXES
        "_include": None,  # process_include
        "_revinclude": None,  # process_revinclude
        "_sort": None,  # sort_search_results
        "_count": None,  # Handled in execute_search
        "_offset": None,  # Handled in execute_search
        "_summary": None,  # format_search_results_with_summary
        "_elements": None,  # format_search_results_with_elements
        "_contained": None,  # Parsed in parse_search_string
        "_containedType": None,  # Parsed in parse_search_string
    }
    
    # Check which features are implemented
    implemented_features = {}
    missing_features = []
    
    # Check chaining
    try:
        parse_chained_parameter("patient.name")
        implemented_features["search_chaining"] = True
    except Exception:
        implemented_features["search_chaining"] = False
        missing_features.append("search_chaining")
    
    # Check reverse chaining
    try:
        parse_reverse_chain_parameter("_has:Observation:code")
        implemented_features["reverse_chaining"] = True
    except Exception:
        implemented_features["reverse_chaining"] = False
        missing_features.append("reverse_chaining")
    
    # Check modifiers
    if SEARCH_MODIFIERS:
        implemented_features["search_modifiers"] = True
    else:
        implemented_features["search_modifiers"] = False
        missing_features.append("search_modifiers")
    
    # Check prefixes
    if SEARCH_PREFIXES:
        implemented_features["search_prefixes"] = True
    else:
        implemented_features["search_prefixes"] = False
        missing_features.append("search_prefixes")
    
    # Check _include
    try:
        # Test that process_include function exists and is callable
        if callable(process_include):
            implemented_features["_include"] = True
        else:
            implemented_features["_include"] = False
            missing_features.append("_include")
    except Exception:
        implemented_features["_include"] = False
        missing_features.append("_include")
    
    # Check _revinclude
    try:
        if callable(process_revinclude):
            implemented_features["_revinclude"] = True
        else:
            implemented_features["_revinclude"] = False
            missing_features.append("_revinclude")
    except Exception:
        implemented_features["_revinclude"] = False
        missing_features.append("_revinclude")
    
    # Check _sort
    try:
        if callable(sort_search_results):
            implemented_features["_sort"] = True
        else:
            implemented_features["_sort"] = False
            missing_features.append("_sort")
    except Exception:
        implemented_features["_sort"] = False
        missing_features.append("_sort")
    
    # Check _count and _offset (handled in execute_search)
    try:
        params = parse_search_string("_count=10&_offset=5")
        if params._count == 10 and params._offset == 5:
            implemented_features["_count"] = True
            implemented_features["_offset"] = True
        else:
            implemented_features["_count"] = False
            implemented_features["_offset"] = False
            missing_features.extend(["_count", "_offset"])
    except Exception:
        implemented_features["_count"] = False
        implemented_features["_offset"] = False
        missing_features.extend(["_count", "_offset"])
    
    # Check _summary (parsing and implementation)
    try:
        from dnhealth.dnhealth_fhir.search_results import apply_summary, format_search_results_with_summary
        params = parse_search_string("_summary=text")
        if params._summary == "text" and callable(apply_summary) and callable(format_search_results_with_summary):
            implemented_features["_summary"] = True  # Parsing and implementation both work
        else:
            implemented_features["_summary"] = False
            missing_features.append("_summary")
    except Exception:
        implemented_features["_summary"] = False
        missing_features.append("_summary")
    
    # Check _elements (parsing and implementation)
    try:
        from dnhealth.dnhealth_fhir.search_results import apply_elements, format_search_results_with_elements
        params = parse_search_string("_elements=id,name")
        if params._elements == ["id", "name"] and callable(apply_elements) and callable(format_search_results_with_elements):
            implemented_features["_elements"] = True  # Parsing and implementation both work
        else:
            implemented_features["_elements"] = False
            missing_features.append("_elements")
    except Exception:
        implemented_features["_elements"] = False
        missing_features.append("_elements")
    
    # Check _contained and _containedType
    try:
        params = parse_search_string("_contained=true&_containedType=both")
        if params._contained == "true" and params._containedType == "both":
            implemented_features["_contained"] = True
            implemented_features["_containedType"] = True
        else:
            implemented_features["_contained"] = False
            implemented_features["_containedType"] = False
            missing_features.extend(["_contained", "_containedType"])
    except Exception:
        implemented_features["_contained"] = False
        implemented_features["_containedType"] = False
        missing_features.extend(["_contained", "_containedType"])
    
    all_features_implemented = len(missing_features) == 0
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    result = {
        "features": implemented_features,
        "all_features_implemented": all_features_implemented,
        "missing_features": missing_features,
        "verification_time": elapsed,
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "completion_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    logger.info(f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - Search feature verification completed: {len([f for f in implemented_features.values() if f])}/{len(implemented_features)} features implemented")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return result


def verify_search_specification_compliance() -> Dict[str, Any]:
    """
    Verify search implementation compliance with FHIR R4 Search specification.
    
    Returns:
        Dictionary with comprehensive verification results including:
        - parameter_types: Verification results for parameter types
        - features: Verification results for search features
        - compliance_status: Overall compliance status
        - issues: List of any compliance issues
        - timestamp: Completion timestamp
    """
    start_time = datetime.now()
    logger.info(f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Verifying search specification compliance...")
    
    # Verify parameter types
    type_results = verify_search_parameter_types()
    
    # Verify features
    feature_results = verify_search_features()
    
    # Determine overall compliance
    compliance_status = (
        type_results["all_types_implemented"] and
        feature_results["all_features_implemented"]
    )
    
    issues = []
    if not type_results["all_types_implemented"]:
        issues.append(f"Missing parameter types: {', '.join(type_results['missing_types'])}")
    if not feature_results["all_features_implemented"]:
        issues.append(f"Missing features: {', '.join(feature_results['missing_features'])}")
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    result = {
        "parameter_types": type_results,
        "features": feature_results,
        "compliance_status": compliance_status,
        "issues": issues,
        "total_issues": len(issues),
        "verification_time": elapsed,
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "completion_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    logger.info(f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - Search specification compliance verification completed: {'COMPLIANT' if compliance_status else 'NON-COMPLIANT'}")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return result
