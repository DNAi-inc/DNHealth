# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR Search parameter parsing and handling (version-aware).

Supports parsing FHIR search parameters from query strings.
Supports both R4 and R5 versions with version-aware search parameter handling.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from urllib.parse import parse_qs, urlparse
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class SearchParameter:
    """
    Represents a single FHIR search parameter.
    
    Examples:
        - name=value
        - name:exact=value
        - name:contains=value
    """
    
    name: str
    value: str
    modifier: Optional[str] = None  # exact, contains, text, etc.
    prefix: Optional[str] = None  # eq, ne, gt, lt, ge, le, sa, eb, ap (for dates/numbers)
    
    def __str__(self) -> str:
        """String representation of search parameter."""
        parts = [self.name]
        if self.modifier:
            parts.append(f":{self.modifier}")
        if self.prefix:
            parts.insert(1, f":{self.prefix}")
        return f"{':'.join(parts)}={self.value}"


@dataclass
class SearchParameters:
    """
    Collection of FHIR search parameters.
    
    Includes special parameters like _include, _revinclude, _sort, _count, _offset, etc.
    """
    
    parameters: List[SearchParameter] = field(default_factory=list)
    _include: List[str] = field(default_factory=list)
    _revinclude: List[str] = field(default_factory=list)
    _sort: List[str] = field(default_factory=list)
    _count: Optional[int] = None
    _offset: Optional[int] = None
    _summary: Optional[str] = None
    _elements: List[str] = field(default_factory=list)
    _contained: Optional[str] = None
    _containedType: Optional[str] = None
    _format: Optional[str] = None
    _pretty: Optional[str] = None
    _fhirpath: Optional[str] = None  # FHIRPath expression for query support
    
    def get_parameter(self, name: str) -> List[SearchParameter]:
        """Get all parameters with the given name."""
        return [p for p in self.parameters if p.name == name]
    
    def get_parameter_value(self, name: str) -> Optional[str]:
        """Get the first parameter value with the given name."""
        params = self.get_parameter(name)
        return params[0].value if params else None
    
    def has_parameter(self, name: str) -> bool:
        """Check if a parameter exists."""

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return any(p.name == name for p in self.parameters)


# Common search parameter types
SEARCH_PARAMETER_TYPES = {
    "string": str,
    "token": str,  # system|code or just code
    "reference": str,  # ResourceType/id or URL
    "date": str,  # date, dateTime, or Period
    "number": float,
    "quantity": str,  # number|system|code
    "uri": str,
    "special": str,  # _id, _lastUpdated, etc.
    "composite": str,  # Composite parameters
}


def validate_search_parameter_type(param: SearchParameter, param_type: str) -> List[str]:
    """
    Validate a search parameter value against its type.
    
    Args:
        param: SearchParameter to validate
        param_type: Parameter type (string, token, reference, date, number, quantity, uri, special, composite)
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if param_type == "string":
        # String type - any string is valid
        pass
    elif param_type == "token":
        # Token type - format: system|code or just code
        if "|" in param.value:
            parts = param.value.split("|", 1)
            if len(parts) != 2:
                errors.append(f"Token parameter '{param.name}' has invalid format: '{param.value}'")
        # Just code is also valid
    elif param_type == "reference":
        # Reference type - format: ResourceType/id or URL
        if not param.value:
            errors.append(f"Reference parameter '{param.name}' cannot be empty")
        elif not ("/" in param.value or param.value.startswith("http://") or param.value.startswith("https://")):
            errors.append(f"Reference parameter '{param.name}' has invalid format: '{param.value}'")
    elif param_type == "date":
        # Date type - should be date, dateTime, or Period format
        # Basic validation - check if it looks like a date
        import re
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',  # dateTime
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}',  # dateTime with timezone
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',  # dateTime UTC
        ]
        if not any(re.match(pattern, param.value) for pattern in date_patterns):
            # Could be a Period or prefix format, so don't error
            pass
    elif param_type == "number":
        # Number type - should be numeric
        try:
            float(param.value)
        except ValueError:
            errors.append(f"Number parameter '{param.name}' has invalid value: '{param.value}'")
    elif param_type == "quantity":
        # Quantity type - format: number|system|code or just number
        if "|" in param.value:
            parts = param.value.split("|")
            if len(parts) > 3:
                errors.append(f"Quantity parameter '{param.name}' has invalid format: '{param.value}'")
            else:
                # First part should be numeric
                try:
                    float(parts[0])
                except ValueError:
                    errors.append(f"Quantity parameter '{param.name}' has invalid number: '{parts[0]}'")
        else:
            # Just number is valid
            try:
                float(param.value)
            except ValueError:
                errors.append(f"Quantity parameter '{param.name}' has invalid value: '{param.value}'")
    elif param_type == "uri":
        # URI type - should be a valid URI
        if param.value and not (param.value.startswith("http://") or param.value.startswith("https://") or param.value.startswith("urn:")):
            # Could be a relative URI, so don't error
            pass
    elif param_type == "special":
        # Special type - _id, _lastUpdated, etc.
        pass
    elif param_type == "composite":
        # Composite type - format depends on composite definition
        # For now, just check it's not empty
        if not param.value:
            errors.append(f"Composite parameter '{param.name}' cannot be empty")
    
    return errors


def parse_token_value(token_str: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a token value into system and code.
    
    Args:
        token_str: Token string (format: system|code or just code)
        
    Returns:
        Tuple of (system, code) or (None, code) if no system
    """
    if "|" in token_str:
        parts = token_str.split("|", 1)
        return parts[0], parts[1]
    return None, token_str


def parse_quantity_value(quantity_str: str) -> tuple[Optional[float], Optional[str], Optional[str]]:
    """
    Parse a quantity value into number, system, and code.
    
    Args:
        quantity_str: Quantity string (format: number|system|code or just number)
        
    Returns:
        Tuple of (number, system, code) or (number, None, None) if just number
    """
    if "|" in quantity_str:
        parts = quantity_str.split("|")
        number = float(parts[0]) if parts[0] else None
        system = parts[1] if len(parts) > 1 else None
        code = parts[2] if len(parts) > 2 else None
        return number, system, code
    else:
        number = float(quantity_str) if quantity_str else None
        return number, None, None


def parse_reference_value(reference_str: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a reference value into resource type and id.
    
    Args:
        reference_str: Reference string (format: ResourceType/id or URL)
        
    Returns:
        Tuple of (resource_type, resource_id) or (None, None) if invalid
    """
    if not reference_str:
        return None, None
    
    # Handle URL references
    if reference_str.startswith("http://") or reference_str.startswith("https://"):
        # Extract resource type and id from URL
        parts = reference_str.rstrip("/").split("/")
        if len(parts) >= 2:
            resource_id = parts[-1]
            resource_type = parts[-2]
            return resource_type, resource_id
        return None, None
    
    # Handle relative references (ResourceType/id)
    if "/" in reference_str:
        parts = reference_str.split("/", 1)
        if len(parts) == 2:
            resource_type, resource_id = parts
            return resource_type, resource_id
    
    return None, None


def parse_chained_parameter(param_name: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a chained search parameter name.
    
    Chained parameters have the format: resourceType.parameterName
    Examples:
        - patient.name=John
        - subject.organization.name=Hospital
    
    Args:
        param_name: Parameter name (may be chained)
        
    Returns:
        Tuple of (resource_type, parameter_name) or (None, param_name) if not chained
    """
    if "." in param_name:
        parts = param_name.split(".", 1)
        if len(parts) == 2:
            resource_type, parameter_name = parts
            return resource_type, parameter_name
    return None, param_name


def is_chained_parameter(param_name: str) -> bool:
    """
    Check if a parameter name represents a chained search.
    
    Args:
        param_name: Parameter name to check
        
    Returns:
        True if parameter is chained, False otherwise
    """
    return "." in param_name


def parse_reverse_chain_parameter(param_name: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a reverse chain search parameter name.
    
    Reverse chain parameters have the format: _has:ResourceType:parameterName
    Examples:
        - _has:Observation:subject=Patient/123
        - _has:Condition:subject=Patient/123
    
    Args:
        param_name: Parameter name (may be reverse chained)
        
    Returns:
        Tuple of (resource_type, parameter_name) or (None, None) if not reverse chained
    """
    if param_name.startswith("_has:"):
        parts = param_name[5:].split(":", 1)  # Remove "_has:" prefix
        if len(parts) == 2:
            resource_type, parameter_name = parts
            return resource_type, parameter_name

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return None, None


def is_reverse_chain_parameter(param_name: str) -> bool:
    """
    Check if a parameter name represents a reverse chain search.
    
    Args:
        param_name: Parameter name to check
        
    Returns:
        True if parameter is reverse chained, False otherwise
    """
    return param_name.startswith("_has:")


@dataclass
class ChainedSearchParameter:
    """
    Represents a chained search parameter.
    
    Examples:
        - patient.name=John -> resource_type="patient", parameter="name", value="John"
        - subject.organization.name=Hospital -> resource_type="subject", parameter="organization.name", value="Hospital"
    """
    
    resource_type: str
    parameter: str
    value: str
    modifier: Optional[str] = None
    prefix: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of chained search parameter."""
        parts = [f"{self.resource_type}.{self.parameter}"]
        if self.prefix:
            parts.insert(1, f":{self.prefix}")
        if self.modifier:
            parts.append(f":{self.modifier}")
        return f"{':'.join(parts)}={self.value}"


def parse_chained_search_parameter(param: SearchParameter) -> Optional[ChainedSearchParameter]:
    """
    Parse a SearchParameter into a ChainedSearchParameter if it's chained.
    
    Args:
        param: SearchParameter to parse
        
    Returns:
        ChainedSearchParameter if chained, None otherwise
    """
    if not is_chained_parameter(param.name):
        return None
    
    resource_type, parameter_name = parse_chained_parameter(param.name)
    if resource_type:

            # Log completion timestamp at end of operation
        return ChainedSearchParameter(
            resource_type=resource_type,
            parameter=parameter_name,
            value=param.value,
            modifier=param.modifier,
            prefix=param.prefix
        )
    return None


# Common search modifiers
SEARCH_MODIFIERS = {
    "exact",  # Exact match
    "contains",  # Contains substring
    "text",  # Text search
    "above",  # Above in hierarchy
    "below",  # Below in hierarchy
    "in",  # In value set
    "not-in",  # Not in value set
    "of-type",  # Of type (for references)
    "missing",  # Missing (true/false)
    "type",  # Type modifier
}


# Common search prefixes (for dates/numbers)
SEARCH_PREFIXES = {
    "eq",  # equals
    "ne",  # not equals
    "gt",  # greater than
    "lt",  # less than
    "ge",  # greater than or equal
    "le",  # less than or equal
    "sa",  # starts after
    "eb",  # ends before
    "ap",  # approximately
}


def parse_search_string(query_string: str) -> SearchParameters:
    """
    Parse a FHIR search query string into SearchParameters.
    
    Args:
        query_string: Query string (e.g., "name=John&status=active&_count=10")
        
    Returns:
        SearchParameters object
        
    Examples:
        >>> params = parse_search_string("name=John&status=active")
        >>> params.get_parameter_value("name")
        'John'
        >>> params.get_parameter_value("status")
        'active'
    """
    # Parse query string
    parsed = parse_qs(query_string, keep_blank_values=True)
    
    search_params = SearchParameters()
    
    for key, values in parsed.items():
        # Handle special parameters
        if key == "_include":
            search_params._include = values
        elif key == "_revinclude":
            search_params._revinclude = values
        elif key == "_sort":
            # Sort can be comma-separated or multiple parameters
            sort_values = []
            for v in values:
                sort_values.extend(v.split(","))
            search_params._sort = sort_values
        elif key == "_count":
            if values and values[0]:
                try:
                    count_value = int(values[0])
                    # FHIR spec: _count must be a positive integer (>= 1)
                    if count_value < 1:
                        raise ValueError(
                            f"Invalid _count value: {count_value}. "
                            "_count must be a positive integer (>= 1) per FHIR specification."
                        )
                    search_params._count = count_value
                except ValueError as e:
                    # Re-raise if it's our validation error, otherwise raise new error for invalid format
                    if "Invalid _count value" in str(e):
                        raise
                    raise ValueError(
                        f"Invalid _count value: '{values[0]}'. "
                        "_count must be a positive integer per FHIR specification."
                    )
        elif key == "_offset":
            if values and values[0]:
                try:
                    offset_value = int(values[0])
                    # FHIR spec: _offset must be a non-negative integer (>= 0)
                    if offset_value < 0:
                        raise ValueError(
                            f"Invalid _offset value: {offset_value}. "
                            "_offset must be a non-negative integer (>= 0) per FHIR specification."
                        )
                    search_params._offset = offset_value
                except ValueError as e:
                    # Re-raise if it's our validation error, otherwise raise new error for invalid format
                    if "Invalid _offset value" in str(e):
                        raise
                    raise ValueError(
                        f"Invalid _offset value: '{values[0]}'. "
                        "_offset must be a non-negative integer per FHIR specification."
                    )
        elif key == "_summary":
            if values and values[0]:
                search_params._summary = values[0]
        elif key == "_elements":
            # Elements can be comma-separated
            elements = []
            for v in values:
                elements.extend(v.split(","))
            search_params._elements = elements
        elif key == "_contained":
            if values and values[0]:
                search_params._contained = values[0]
        elif key == "_containedType":
            if values and values[0]:
                search_params._containedType = values[0]
        elif key == "_format":
            if values and values[0]:
                search_params._format = values[0]
        elif key == "_pretty":
            if values and values[0]:
                search_params._pretty = values[0]
        elif key == "_fhirpath":
            # FHIRPath expression for query support
            if values and values[0]:
                search_params._fhirpath = values[0]
        else:
            # Regular search parameter
            for value in values:
                param = _parse_parameter(key, value)
                if param:
                    search_params.parameters.append(param)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Search string parsing completed successfully")
    
    return search_params


def _parse_parameter(name: str, value: str) -> Optional[SearchParameter]:
    """
    Parse a single search parameter.
    
    Args:
        name: Parameter name (may include modifier and prefix)
        value: Parameter value
        
    Returns:
        SearchParameter object or None if invalid
    """
    if not name or not value:
        return None
    
    modifier = None
    prefix = None
    
    # Check for modifier (name:modifier)
    if ":" in name:
        parts = name.split(":", 1)
        name_part = parts[0]
        modifier_part = parts[1]
        
        # Check if modifier_part is a prefix or modifier
        if modifier_part in SEARCH_PREFIXES:
            prefix = modifier_part
        elif modifier_part in SEARCH_MODIFIERS:
            modifier = modifier_part
        else:
            # Unknown modifier, treat as modifier
            modifier = modifier_part
        
        name = name_part
    
    # Check for prefix in name (name:prefix:modifier)
    if ":" in name and prefix is None:
        parts = name.split(":", 1)
        if parts[1] in SEARCH_PREFIXES:
            name = parts[0]
            prefix = parts[1]
    
    return SearchParameter(
        name=name,
        value=value,
        modifier=modifier,
        prefix=prefix
    )


def parse_search_url(url: str) -> SearchParameters:
    """

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    Parse a FHIR search URL into SearchParameters.
    
    Args:
        url: Full URL or query string
        
    Returns:
        SearchParameters object
        
    Examples:
        >>> params = parse_search_url("http://example.com/fhir/Patient?name=John&status=active")
        >>> params.get_parameter_value("name")
        'John'
    """
    parsed = urlparse(url)
    query_string = parsed.query
    result = parse_search_string(query_string)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Search URL parsing completed successfully")
    
    return result


def format_search_parameters(params: SearchParameters) -> str:
    """
    Format SearchParameters back into a query string.
    
    Args:
        params: SearchParameters object
        
    Returns:
        Query string
    """
    parts = []
    
    # Add regular parameters
    for param in params.parameters:
        parts.append(str(param))
    
    # Add special parameters
    for include in params._include:
        parts.append(f"_include={include}")
    
    for revinclude in params._revinclude:
        parts.append(f"_revinclude={revinclude}")
    
    if params._sort:
        parts.append(f"_sort={','.join(params._sort)}")
    
    if params._count is not None:
        parts.append(f"_count={params._count}")
    
    if params._offset is not None:
        parts.append(f"_offset={params._offset}")
    
    if params._summary:
        parts.append(f"_summary={params._summary}")
    
    if params._elements:
        parts.append(f"_elements={','.join(params._elements)}")
    
    if params._contained:
        parts.append(f"_contained={params._contained}")
    
    if params._containedType:
        parts.append(f"_containedType={params._containedType}")
    
    if params._format:
        parts.append(f"_format={params._format}")
    
    if params._pretty:
        parts.append(f"_pretty={params._pretty}")
    
    return "&".join(parts)

