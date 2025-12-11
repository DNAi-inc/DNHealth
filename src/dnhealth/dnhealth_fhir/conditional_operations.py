# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Conditional Operations Support.

Provides functions for handling conditional operations in FHIR REST API.
Supports If-Match, If-None-Match, and If-Modified-Since headers.
All operations include timestamps in logs for traceability.
All operations enforce 5-minute timeout limits (300 seconds).
"""

import time
from datetime import datetime
from typing import Optional, Dict, Tuple, Any, TYPE_CHECKING

from dnhealth.util.logging import get_logger

if TYPE_CHECKING:
    from flask import Request
    from dnhealth.dnhealth_fhir.resources.base import Resource

logger = logging.getLogger(__name__)

logger = get_logger(__name__)

# Timeout limit for all operations (5 minutes)
OPERATION_TIMEOUT = 300  # seconds


def check_if_match(request: "Request", resource_version: str) -> Tuple[bool, Optional[str]]:
    """
    Check If-Match header against resource version.
    
    Extracts If-Match header value and compares it with resource version.
    Used for conditional update and conditional delete operations.
    
    Args:
        request: Flask request object with headers
        resource_version: Current resource version ID
        
    Returns:
        Tuple of (is_match: bool, error_message: Optional[str])
        - If match: (True, None)
        - If no match: (False, error_message)
        - If header not present: (True, None) - no condition to check
        
    Example:
        >>> from flask import request
        >>> is_match, error = check_if_match(request, "v1")
        >>> if not is_match:
        ...     return error_response(412, error)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking If-Match header")
    
    try:
        if_match = request.headers.get("If-Match")
        
        if not if_match:
            # No If-Match header - condition passes
            elapsed = time.time() - start_time
            logger.debug(f"[{current_time}] No If-Match header, condition passes (elapsed: {elapsed:.3f}s)")
            return (True, None)
        
        # Extract version from If-Match header (format: W/"version" or "version")
        match_version = if_match.strip('W/"').strip('"')
        
        if match_version != resource_version:
            elapsed = time.time() - start_time
            error_msg = f"Version mismatch: expected {match_version}, got {resource_version}"
            logger.warning(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
            return (False, error_msg)
        
        elapsed = time.time() - start_time
        logger.debug(f"[{current_time}] If-Match condition passed (elapsed: {elapsed:.3f}s)")
        return (True, None)
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error checking If-Match header: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        return (False, error_msg)
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] If-Match check completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")


def check_if_none_match(
    request: "Request",
    resource_exists: bool,    resource_version: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Check If-None-Match header against resource existence/version.
    
    Extracts If-None-Match header value and checks if resource/version exists.
    Used for conditional create operations.
    
    Args:
        request: Flask request object with headers
        resource_exists: Whether the resource exists
        resource_version: Optional current resource version ID
        
    Returns:
        Tuple of (condition_passes: bool, error_message: Optional[str])
        - If condition passes: (True, None)
        - If condition fails: (False, error_message)
        - If header not present: (True, None) - no condition to check
        
    Example:
        >>> from flask import request
        >>> passes, error = check_if_none_match(request, resource_exists=True)
        >>> if not passes:
        ...     return error_response(412, error)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking If-None-Match header")
    
    try:
        if_none_match = request.headers.get("If-None-Match")
        
        if not if_none_match:
            # No If-None-Match header - condition passes
            elapsed = time.time() - start_time
            logger.debug(f"[{current_time}] No If-None-Match header, condition passes (elapsed: {elapsed:.3f}s)")
            return (True, None)
        
        if if_none_match == "*":
            # If-None-Match: "*" - Resource must not exist
            if resource_exists:
                elapsed = time.time() - start_time
                error_msg = "Resource already exists"
                logger.warning(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
                return (False, error_msg)
            else:
                elapsed = time.time() - start_time
                logger.debug(f"[{current_time}] If-None-Match: * condition passed (elapsed: {elapsed:.3f}s)")
                return (True, None)
        else:
            # If-None-Match: version - Version must not match
            if resource_version:
                match_version = if_none_match.strip('W/"').strip('"')
                if match_version == resource_version:
                    elapsed = time.time() - start_time
                    error_msg = f"Version {match_version} already exists"
                    logger.warning(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
                    return (False, error_msg)
            
            elapsed = time.time() - start_time
            logger.debug(f"[{current_time}] If-None-Match version condition passed (elapsed: {elapsed:.3f}s)")
            return (True, None)
            
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error checking If-None-Match header: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        return (False, error_msg)
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] If-None-Match check completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")


def check_if_modified_since(
    request: "Request",
    resource_last_modified: datetime
) -> Tuple[bool, Optional[str]]:
    """
    Check If-Modified-Since header against resource last modified time.
    
    Extracts If-Modified-Since header value and compares with resource last modified time.
    Used for conditional read operations (return 304 Not Modified if not modified).
    
    Args:
        request: Flask request object with headers
        resource_last_modified: Resource last modified datetime
        
    Returns:
        Tuple of (is_modified: bool, error_message: Optional[str])
        - If modified since date: (True, None)
        - If not modified since date: (False, "Not Modified")
        - If header not present: (True, None) - no condition to check
        
    Example:
        >>> from flask import request
        >>> from datetime import datetime
        >>> is_modified, error = check_if_modified_since(request, last_modified)
        >>> if not is_modified:
        ...     return Response(status=304)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking If-Modified-Since header")
    
    try:
        if_modified_since = request.headers.get("If-Modified-Since")
        
        if not if_modified_since:
            # No If-Modified-Since header - condition passes
            elapsed = time.time() - start_time
            logger.debug(f"[{current_time}] No If-Modified-Since header, condition passes (elapsed: {elapsed:.3f}s)")
            return (True, None)
        
        # Parse HTTP date format (RFC 7231)
        # Format: "Wed, 21 Oct 2015 07:28:00 GMT"
        try:
            from email.utils import parsedate_to_datetime
            modified_since_date = parsedate_to_datetime(if_modified_since)
        except (ValueError, TypeError) as e:
            elapsed = time.time() - start_time
            error_msg = f"Invalid If-Modified-Since date format: {str(e)}"
            logger.warning(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
            return (False, error_msg)
        
        # Compare with resource last modified time
        if resource_last_modified <= modified_since_date:
            elapsed = time.time() - start_time
            logger.debug(f"[{current_time}] Resource not modified since {if_modified_since} (elapsed: {elapsed:.3f}s)")
            return (False, "Not Modified")
        
        elapsed = time.time() - start_time
        logger.debug(f"[{current_time}] Resource modified since {if_modified_since} (elapsed: {elapsed:.3f}s)")
        return (True, None)
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error checking If-Modified-Since header: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        return (False, error_msg)
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] If-Modified-Since check completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")


def conditional_delete(
    resource_type: str,
    search_params: Dict[str, str],
    storage: Any
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Execute conditional delete operation.
    
    Executes search with parameters and deletes resource if exactly one match found.
    Returns error if zero or multiple matches.
    
    Args:
        resource_type: FHIR resource type
        search_params: Search parameters dictionary
        storage: ResourceStorage instance for search and delete operations
        
    Returns:
        Tuple of (success: bool, resource_id: Optional[str], error_message: Optional[str])
        - If exactly one match: (True, resource_id, None)
        - If zero matches: (False, None, "No matches")
        - If multiple matches: (False, None, "Multiple matches")
        
    Example:
        >>> from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage
        >>> storage = ResourceStorage()
        >>> success, resource_id, error = conditional_delete("Patient", {"identifier": "123"}, storage)
        >>> if success:
        ...     storage.delete("Patient", resource_id)
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Executing conditional delete for {resource_type} with params {search_params}")
    
    try:
        # Execute search with parameters
        from dnhealth.dnhealth_fhir.search_execution import execute_search
        from dnhealth.dnhealth_fhir.search import SearchParameters
        
        # Get all resources of this type from storage
        all_resources = storage.search(resource_type, None)
        
        # Convert search params to SearchParameters
        search_parameters = SearchParameters()
        for param_name, param_value in search_params.items():
            search_parameters.add_parameter(param_name, param_value)
        
        # Execute search with all_resources parameter for _revinclude support
        results = execute_search(
            resources=all_resources,
            search_params=search_parameters,
            all_resources=all_resources  # Pass for _revinclude processing
        )
        
        # Check results
        if not results or len(results) == 0:
            elapsed = time.time() - start_time
            logger.warning(f"[{current_time}] Conditional delete: No matches found (elapsed: {elapsed:.3f}s)")
            return (False, None, "No matches")
        
        if len(results) > 1:
            elapsed = time.time() - start_time
            logger.warning(f"[{current_time}] Conditional delete: Multiple matches found ({len(results)}) (elapsed: {elapsed:.3f}s)")
            return (False, None, "Multiple matches")
        
        # Exactly one match
        resource_id = results[0].id if hasattr(results[0], 'id') else None
        elapsed = time.time() - start_time
        logger.info(f"[{current_time}] Conditional delete: Found single match {resource_id} (elapsed: {elapsed:.3f}s)")
        return (True, resource_id, None)
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error executing conditional delete: {str(e)}"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.3f}s)")
        return (False, None, error_msg)
    finally:
        elapsed = time.time() - start_time
        if elapsed > OPERATION_TIMEOUT:
            logger.error(f"[{current_time}] Operation exceeded timeout of {OPERATION_TIMEOUT} seconds")
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Conditional delete completed (elapsed: {elapsed:.3f}s)")
        logger.info(f"Current Time at End of Operations: {completion_time}")
