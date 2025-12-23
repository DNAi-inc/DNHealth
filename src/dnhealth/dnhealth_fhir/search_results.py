# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Search result formatting.

Formats search results into Bundle resources with proper structure.
All operations include timestamps in logs for traceability.
"""

import json
import base64
import copy
import dataclasses
from typing import List, Optional, Dict, Any, Tuple, Set
from datetime import datetime
from dnhealth.dnhealth_fhir.resources.base import FHIRResource, DomainResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry, BundleLink
from dnhealth.dnhealth_fhir.search import SearchParameters, SearchParameter
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


def format_search_results(
    resources: List[FHIRResource],
    search_params: Optional[SearchParameters] = None,
    total: Optional[int] = None,
    self_url: Optional[str] = None,
    first_url: Optional[str] = None,
    previous_url: Optional[str] = None,
    next_url: Optional[str] = None,
    last_url: Optional[str] = None
) -> Bundle:
    """
    Format a list of resources into a search result Bundle.
    
    Args:
        resources: List of FHIR resources to include in search results
        search_params: Optional SearchParameters used for the search
        total: Optional total number of results (if known)
        self_url: Optional self link URL
        first_url: Optional first page link URL
        previous_url: Optional previous page link URL
        next_url: Optional next page link URL
        last_url: Optional last page link URL
        
    Returns:
        Bundle resource containing search results
    """
    # Create bundle entries
    entries = []
    for resource in resources:
        entry = BundleEntry(
            fullUrl=_get_resource_url(resource),
            resource=resource
        )
        entries.append(entry)
    
    # Create bundle links
    links = []
    if self_url:
        links.append(BundleLink(relation="self", url=self_url))
    if first_url:
        links.append(BundleLink(relation="first", url=first_url))
    if previous_url:
        links.append(BundleLink(relation="previous", url=previous_url))
    if next_url:
        links.append(BundleLink(relation="next", url=next_url))
    if last_url:
        links.append(BundleLink(relation="last", url=last_url))
    
    # Determine total
    if total is None:
        total = len(resources)
    
    # Create bundle
    bundle = Bundle(
        resourceType="Bundle",
        type="searchset",
        total=total,
        link=links,
        entry=entries,
        timestamp=datetime.now().isoformat()
    )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return bundle


def apply_summary(resource: FHIRResource, summary_mode: str) -> FHIRResource:
    """
    Apply summary mode to a single resource.
    
    Summary modes per FHIR R4 specification:
    - "true": Return only summary elements (id, meta, and key identifying fields)
    - "text": Return only text narrative (resource.text)
    - "data": Return data elements only (remove narrative)
    - "count": Not applicable to individual resources (handled at bundle level)
    
    Args:
        resource: FHIR resource to apply summary to
        summary_mode: Summary mode (true, text, data)
        
    Returns:
        Resource with summary applied (new copy)
        
    Example:
        >>> patient_summary = apply_summary(patient, "true")
        >>> # Returns resource with only summary fields
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Applying summary mode '{summary_mode}' to resource {resource.resourceType}/{resource.id}")
    
    if summary_mode == "text":
        # Return only text narrative
        if isinstance(resource, DomainResource) and resource.text:
            # Create minimal resource with only text
            summary_resource = copy.deepcopy(resource)
            # Remove all fields except resourceType, id, meta, and text
            for field in dataclasses.fields(summary_resource):
                if field.name not in ["resourceType", "id", "meta", "text"]:
                    setattr(summary_resource, field.name, None)
            # Clear lists
            if hasattr(summary_resource, "extension"):
                summary_resource.extension = []
            if hasattr(summary_resource, "modifierExtension"):
                summary_resource.modifierExtension = []
            if hasattr(summary_resource, "contained"):
                summary_resource.contained = []
            logger.info(f"[{current_time}] Applied text summary to resource {resource.resourceType}/{resource.id}")
            return summary_resource
        else:
            # No text available, return minimal resource
            summary_resource = copy.deepcopy(resource)
            for field in dataclasses.fields(summary_resource):
                if field.name not in ["resourceType", "id", "meta"]:
                    setattr(summary_resource, field.name, None)
            return summary_resource
    
    elif summary_mode == "data":
        # Return data elements only (remove narrative)
        summary_resource = copy.deepcopy(resource)
        if isinstance(summary_resource, DomainResource):
            summary_resource.text = None
        logger.info(f"[{current_time}] Applied data summary to resource {resource.resourceType}/{resource.id}")
        return summary_resource
    
    elif summary_mode == "true":
        # Return summary elements only (id, meta, and key identifying fields)
        summary_resource = copy.deepcopy(resource)
        
        # Keep only summary fields: resourceType, id, meta
        # Plus key identifying fields based on resource type
        summary_fields = {"resourceType", "id", "meta"}
        
        # Add resource-type-specific summary fields
        resource_type = resource.resourceType
        if resource_type == "Patient":
            summary_fields.update({"name", "identifier", "gender", "birthDate"})
        elif resource_type == "Observation":
            summary_fields.update({"status", "code", "subject", "effectiveDateTime", "valueQuantity", "valueString"})
        elif resource_type == "Encounter":
            summary_fields.update({"status", "class", "type", "subject", "period"})
        elif resource_type == "Condition":
            summary_fields.update({"status", "code", "subject", "onsetDateTime"})
        elif resource_type == "Procedure":
            summary_fields.update({"status", "code", "subject", "performedDateTime"})
        elif resource_type == "MedicationRequest":
            summary_fields.update({"status", "medicationCodeableConcept", "subject", "authoredOn"})
        elif resource_type == "DiagnosticReport":
            summary_fields.update({"status", "code", "subject", "effectiveDateTime"})
        elif resource_type == "ServiceRequest":
            summary_fields.update({"status", "code", "subject", "authoredOn"})
        elif resource_type == "Practitioner":
            summary_fields.update({"name", "identifier"})
        elif resource_type == "Organization":
            summary_fields.update({"name", "identifier"})
        else:
            # For unknown resource types, keep common fields
            summary_fields.update({"status", "name", "identifier"})
        
        # Remove all fields not in summary_fields
        for field in dataclasses.fields(summary_resource):
            if field.name not in summary_fields:
                # Set to None or empty list
                if field.default_factory is not None:
                    setattr(summary_resource, field.name, field.default_factory())
                else:
                    setattr(summary_resource, field.name, None)
        
        logger.info(f"[{current_time}] Applied true summary to resource {resource.resourceType}/{resource.id}")
        return summary_resource
    
    else:
        # Unknown summary mode, return full resource
        logger.warning(f"[{current_time}] Unknown summary mode '{summary_mode}', returning full resource")
        return copy.deepcopy(resource)


def format_search_results_with_summary(
    resources: List[FHIRResource],
    search_params: Optional[SearchParameters] = None,
    summary_mode: Optional[str] = None
) -> Bundle:
    """
    Format search results with summary mode applied.
    
    Args:
        resources: List of FHIR resources to include in search results
        search_params: Optional SearchParameters used for the search
        summary_mode: Summary mode (true, text, data, count)
        
    Returns:
        Bundle resource with summary applied
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Formatting search results with summary mode '{summary_mode}' ({len(resources)} resources)")
    
    if summary_mode == "count":
        # Return only count, no resources
        bundle = Bundle(
            resourceType="Bundle",
            type="searchset",
            total=len(resources),
            entry=[]
        )
        logger.info(f"[{current_time}] Returned count-only bundle with total={len(resources)}")
        return bundle
    
    # Apply summary to each resource
    if summary_mode and summary_mode != "count":
        summarized_resources = [apply_summary(resource, summary_mode) for resource in resources]
        logger.info(f"[{current_time}] Applied summary mode '{summary_mode}' to {len(summarized_resources)} resources")
        return format_search_results(summarized_resources, search_params)
    else:
        # No summary mode, return full results
        return format_search_results(resources, search_params)


def apply_elements(resource: FHIRResource, elements: List[str]) -> FHIRResource:
    """
    Apply element filtering to a single resource, keeping only specified elements.
    
    Element paths can be simple field names or nested paths (e.g., "name.given").
    Always includes resourceType, id, and meta (required fields).
    
    Args:
        resource: FHIR resource to filter
        elements: List of element paths to include (e.g., ["id", "name", "name.given", "status"])
        
    Returns:
        Resource with only specified elements (new copy)
        
    Example:
        >>> patient_filtered = apply_elements(patient, ["id", "name", "name.given", "birthDate"])
        >>> # Returns resource with only id, name (with given), and birthDate
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Applying element filter to resource {resource.resourceType}/{resource.id} with {len(elements)} elements")
    
    # Always include required fields
    required_fields = {"resourceType", "id", "meta"}
    
    # Parse element paths into field sets
    # Simple fields: "id", "name", "status"
    # Nested fields: "name.given", "name.family"
    simple_fields: Set[str] = set()
    nested_fields: Dict[str, Set[str]] = {}  # Maps parent field to set of child fields
    
    for element_path in elements:
        if "." in element_path:
            # Nested field: "name.given"
            parts = element_path.split(".", 1)
            parent = parts[0]
            child = parts[1]
            if parent not in nested_fields:
                nested_fields[parent] = set()
            nested_fields[parent].add(child)
            simple_fields.add(parent)  # Include parent field
        else:
            # Simple field: "id", "name"
            simple_fields.add(element_path)
    
    # Combine with required fields
    all_fields = required_fields | simple_fields
    
    # Create filtered copy
    filtered_resource = copy.deepcopy(resource)
    
    # Remove fields not in all_fields
    for field in dataclasses.fields(filtered_resource):
        if field.name not in all_fields:
            # Remove field
            if field.default_factory is not None:
                setattr(filtered_resource, field.name, field.default_factory())
            else:
                setattr(filtered_resource, field.name, None)
        elif field.name in nested_fields:
            # Field is included but needs nested filtering
            field_value = getattr(filtered_resource, field.name, None)
            if field_value is not None:
                # Filter nested fields
                if isinstance(field_value, list):
                    # List of objects - filter each
                    filtered_list = []
                    for item in field_value:
                        filtered_item = _filter_nested_object(item, nested_fields[field.name])
                        if filtered_item is not None:
                            filtered_list.append(filtered_item)
                    setattr(filtered_resource, field.name, filtered_list)
                elif hasattr(field_value, "__dict__"):
                    # Single object - filter it
                    filtered_item = _filter_nested_object(field_value, nested_fields[field.name])
                    setattr(filtered_resource, field.name, filtered_item)
    
    logger.info(f"[{current_time}] Applied element filter to resource {resource.resourceType}/{resource.id}, kept {len(all_fields)} fields")
    return filtered_resource


def _filter_nested_object(obj: Any, allowed_fields: Set[str]) -> Any:
    """
    Filter a nested object to keep only specified fields.
    
    Args:
        obj: Object to filter (dataclass instance or dict)
        allowed_fields: Set of field names to keep
        
    Returns:
        Filtered object (new copy) or None if object becomes empty
    """
    if obj is None:
        return None
    
    if isinstance(obj, dict):
        # Dictionary - filter keys
        filtered = {}
        for key, value in obj.items():
            if key in allowed_fields:
                filtered[key] = copy.deepcopy(value)
        return filtered if filtered else None
    
    elif hasattr(obj, "__dict__") or dataclasses.is_dataclass(obj):
        # Dataclass or object - filter attributes
        filtered = copy.deepcopy(obj)
        for field in dataclasses.fields(filtered) if dataclasses.is_dataclass(filtered) else []:
            if field.name not in allowed_fields:
                if field.default_factory is not None:
                    setattr(filtered, field.name, field.default_factory())
                else:
                    setattr(filtered, field.name, None)
        return filtered
    
    else:
        # Primitive type - return as is
        return copy.deepcopy(obj)


def format_search_results_with_elements(
    resources: List[FHIRResource],
    elements: List[str],
    search_params: Optional[SearchParameters] = None
) -> Bundle:
    """
    Format search results with only specified elements included.
    
    Args:
        resources: List of FHIR resources to include in search results
        elements: List of element paths to include (e.g., ["id", "name", "status"])
        search_params: Optional SearchParameters used for the search
        
    Returns:
        Bundle resource with filtered elements
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Formatting search results with element filter ({len(elements)} elements, {len(resources)} resources)")
    
    # Apply element filter to each resource
    filtered_resources = [apply_elements(resource, elements) for resource in resources]
    logger.info(f"[{current_time}] Applied element filter to {len(filtered_resources)} resources")
    
    return format_search_results(filtered_resources, search_params)


def format_search_results_paginated(
    resources: List[FHIRResource],
    search_params: SearchParameters,
    base_url: str,
    total: Optional[int] = None
) -> Bundle:
    """
    Format search results with pagination links.
    
    Args:
        resources: List of FHIR resources to include in search results
        search_params: SearchParameters used for the search
        base_url: Base URL for constructing pagination links
        total: Optional total number of results
        
    Returns:
        Bundle resource with pagination links
    """
    # Calculate pagination URLs
    count = search_params._count or len(resources)
    offset = search_params._offset or 0
    
    self_url = _build_search_url(base_url, search_params)
    
    # First page
    first_params = search_params
    first_params._offset = 0
    first_url = _build_search_url(base_url, first_params)
    
    # Previous page
    previous_url = None
    if offset > 0:
        previous_params = search_params
        previous_params._offset = max(0, offset - count)
        previous_url = _build_search_url(base_url, previous_params)
    
    # Next page
    next_url = None
    if total is None or offset + count < total:
        next_params = search_params
        next_params._offset = offset + count
        next_url = _build_search_url(base_url, next_params)
    
    # Last page
    last_url = None
    if total is not None:
        last_params = search_params
        last_params._offset = max(0, total - count)
        last_url = _build_search_url(base_url, last_params)
    
    return format_search_results(
        resources=resources,
        search_params=search_params,
        total=total,
        self_url=self_url,
        first_url=first_url,
        previous_url=previous_url,
        next_url=next_url,
        last_url=last_url
    )


def _get_resource_url(resource: FHIRResource) -> Optional[str]:
    """
    Get the URL for a resource.
    
    Args:
        resource: FHIR resource
        
    Returns:
        Resource URL or None
    """
    if resource.id:
        return f"{resource.resourceType}/{resource.id}"
    
    return None


def _build_search_url(base_url: str, search_params: SearchParameters) -> str:
    """
    Build a search URL from base URL and search parameters.
    
    Args:
        base_url: Base URL
        search_params: SearchParameters
        
    Returns:
        Complete search URL
    """
    from dnhealth.dnhealth_fhir.search import format_search_parameters
    
    query_string = format_search_parameters(search_params)
    if query_string:
        return f"{base_url}?{query_string}"
    return base_url


def create_continuation_token(
    search_params: SearchParameters,
    offset: int,
    total: Optional[int] = None,
    resource_type: Optional[str] = None
) -> str:
    """
    Create a continuation token for search pagination.
    
    Continuation tokens encode search state to allow resuming paginated searches.
    The token is an opaque string that contains encoded search parameters and
    pagination state.
    
    Args:
        search_params: SearchParameters used for the search
        offset: Current offset (number of results skipped)
        total: Optional total number of results (if known)
        resource_type: Optional resource type being searched
        
    Returns:
        Base64-encoded continuation token string
        
    Example:
        >>> params = SearchParameters(parameters=[SearchParameter("name", "John")], _count=10)
        >>> token = create_continuation_token(params, offset=10, total=50, resource_type="Patient")
        >>> # Token can be used to resume search from offset 10
    """
    # Create token data structure
    token_data = {
        "offset": offset,
        "total": total,
        "resource_type": resource_type,
        "count": search_params._count,
        "parameters": [
            {
                "name": p.name,
                "value": p.value,
                "modifier": p.modifier,
                "prefix": p.prefix
            }
            for p in search_params.parameters
        ],
        "include": search_params._include,
        "revinclude": search_params._revinclude,
        "sort": search_params._sort,
        "summary": search_params._summary,
        "elements": search_params._elements,
        "contained": search_params._contained,
        "containedType": search_params._containedType
    }
    
    # Encode as JSON then base64
    json_str = json.dumps(token_data, sort_keys=True)
    token_bytes = json_str.encode('utf-8')
    token = base64.urlsafe_b64encode(token_bytes).decode('ascii')
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return token


def parse_continuation_token(token: str) -> Tuple[SearchParameters, int, Optional[int], Optional[str]]:
    """
    Parse a continuation token to extract search parameters and pagination state.
    
    Args:
        token: Base64-encoded continuation token string
        
    Returns:
        Tuple of (SearchParameters, offset, total, resource_type)
        
    Raises:
        ValueError: If token is invalid or cannot be parsed
        
    Example:
        >>> token = "eyJvZmZzZXQiOjEwfQ=="
        >>> params, offset, total, resource_type = parse_continuation_token(token)
        >>> # Resume search with these parameters from offset
    """
    try:
        # Decode base64
        token_bytes = base64.urlsafe_b64decode(token.encode('ascii'))
        json_str = token_bytes.decode('utf-8')
        token_data = json.loads(json_str)
        
        # Extract pagination state
        offset = token_data.get("offset", 0)
        total = token_data.get("total")
        resource_type = token_data.get("resource_type")
        
        # Reconstruct SearchParameters
        search_params = SearchParameters(
            parameters=[
                SearchParameter(
                    name=p["name"],
                    value=p["value"],
                    modifier=p.get("modifier"),
                    prefix=p.get("prefix")
                )
                for p in token_data.get("parameters", [])
            ],
            _include=token_data.get("include", []),
            _revinclude=token_data.get("revinclude", []),
            _sort=token_data.get("sort", []),
            _count=token_data.get("count"),
            _offset=offset,  # Set offset from token
            _summary=token_data.get("summary"),
            _elements=token_data.get("elements", []),
            _contained=token_data.get("contained"),
            _containedType=token_data.get("containedType")
        )
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return search_params, offset, total, resource_type
        
    except (ValueError, json.JSONDecodeError, base64.binascii.Error) as e:
        raise ValueError(f"Invalid continuation token: {e}")


def build_search_bundle(
    results: List[FHIRResource],
    search_params: SearchParameters,
    total: int,
    continuation_token: Optional[str] = None,
    base_url: Optional[str] = None,
    resource_type: Optional[str] = None
) -> Bundle:
    """
    Build a search result Bundle with continuation token support.
    
    Creates a Bundle with type="searchset" containing search results and
    pagination links. If there are more results, includes a continuation token
    in the next link.
    
    Args:
        results: List of FHIR resources matching the search
        search_params: SearchParameters used for the search
        total: Total number of matching results
        continuation_token: Optional continuation token for next page
        base_url: Optional base URL for constructing pagination links
        resource_type: Optional resource type being searched
        
    Returns:
        Bundle resource with search results and pagination links
        
    Example:
        >>> patients = [Patient(id=f"p{i}") for i in range(10)]
        >>> params = SearchParameters(parameters=[], _count=5)
        >>> bundle = build_search_bundle(patients[:5], params, total=10, base_url="/fhir/Patient")
        >>> # Bundle contains first 5 patients with next link for remaining 5
    """
    # Create bundle entries
    entries = []
    for resource in results:
        entry = BundleEntry(
            fullUrl=_get_resource_url(resource),
            resource=resource
        )
        entries.append(entry)
    
    # Create bundle links
    links = []
    
    # Self link
    if base_url:
        self_url = _build_search_url(base_url, search_params)
        links.append(BundleLink(relation="self", url=self_url))
    
    # Pagination links
    count = search_params._count or len(results)
    offset = search_params._offset or 0
    
    # First page link
    if base_url and offset > 0:
        first_params = SearchParameters(
            parameters=search_params.parameters.copy(),
            _include=search_params._include.copy(),
            _revinclude=search_params._revinclude.copy(),
            _sort=search_params._sort.copy(),
            _count=count,
            _offset=0,
            _summary=search_params._summary,
            _elements=search_params._elements.copy(),
            _contained=search_params._contained,
            _containedType=search_params._containedType
        )
        first_url = _build_search_url(base_url, first_params)
        links.append(BundleLink(relation="first", url=first_url))
    
    # Previous page link
    if base_url and offset > 0:
        prev_offset = max(0, offset - count)
        prev_params = SearchParameters(
            parameters=search_params.parameters.copy(),
            _include=search_params._include.copy(),
            _revinclude=search_params._revinclude.copy(),
            _sort=search_params._sort.copy(),
            _count=count,
            _offset=prev_offset,
            _summary=search_params._summary,
            _elements=search_params._elements.copy(),
            _contained=search_params._contained,
            _containedType=search_params._containedType
        )
        prev_url = _build_search_url(base_url, prev_params)
        links.append(BundleLink(relation="previous", url=prev_url))
    
    # Next page link (with continuation token if available)
    if offset + count < total:
        if continuation_token:
            # Use continuation token in next link
            if base_url:
                next_url = f"{base_url}?_token={continuation_token}"
            else:
                next_url = f"?_token={continuation_token}"
        else:
            # Create continuation token for next page
            next_offset = offset + count
            next_params = SearchParameters(
                parameters=search_params.parameters.copy(),
                _include=search_params._include.copy(),
                _revinclude=search_params._revinclude.copy(),
                _sort=search_params._sort.copy(),
                _count=count,
                _offset=next_offset,
                _summary=search_params._summary,
                _elements=search_params._elements.copy(),
                _contained=search_params._contained,
                _containedType=search_params._containedType
            )
            next_token = create_continuation_token(
                next_params,
                offset=next_offset,
                total=total,
                resource_type=resource_type
            )
            if base_url:
                next_url = f"{base_url}?_token={next_token}"
            else:
                next_url = f"?_token={next_token}"
        
        links.append(BundleLink(relation="next", url=next_url))
    
    # Last page link
    if base_url and total > count:
        last_offset = max(0, total - count)
        last_params = SearchParameters(
            parameters=search_params.parameters.copy(),
            _include=search_params._include.copy(),
            _revinclude=search_params._revinclude.copy(),
            _sort=search_params._sort.copy(),
            _count=count,
            _offset=last_offset,
            _summary=search_params._summary,
            _elements=search_params._elements.copy(),
            _contained=search_params._contained,
            _containedType=search_params._containedType
        )
        last_url = _build_search_url(base_url, last_params)
        links.append(BundleLink(relation="last", url=last_url))
    
    # Create bundle
    bundle = Bundle(
        resourceType="Bundle",
        type="searchset",
        total=total,
        link=links if links else None,
        entry=entries,
        timestamp=datetime.now().isoformat()
    )
    
    return bundle

