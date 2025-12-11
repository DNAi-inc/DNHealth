# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 canonical reference utilities.

Canonical references are URIs that refer to resources by their canonical URL.
Format: <url>|<version>#<fragment> or <url>|<version> or just <url>
Fragments can be used to reference specific elements within a resource.
"""

import logging
from datetime import datetime
from typing import Optional, Tuple, List, Dict
import re
from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


def parse_canonical(canonical_str: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parse a canonical reference into URL, version, and fragment.
    
    Canonical references have the format: <url>|<version>#<fragment>
    Version and fragment are optional.
    
    Args:
        canonical_str: Canonical reference string (e.g., "http://hl7.org/fhir/ValueSet/example|1.0.0#element")
        
    Returns:
        Tuple of (url, version, fragment) or (None, None, None) if invalid
    """
    if not canonical_str or not isinstance(canonical_str, str):
        return None, None, None
    
    # Extract fragment first (if present)
    fragment = None
    if "#" in canonical_str:
        parts = canonical_str.split("#", 1)
        canonical_str = parts[0]
        fragment = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
    
    # Split on | to separate URL and version
    if "|" in canonical_str:
        parts = canonical_str.split("|", 1)
        url = parts[0].strip()
        version = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
        return url, version, fragment
    else:
        # No version specified

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
        return canonical_str.strip(), None, fragment


def format_canonical(url: str, version: Optional[str] = None, fragment: Optional[str] = None) -> str:
    """
    Format a canonical reference from URL, version, and fragment.
    
    Args:
        url: Canonical URL
        version: Optional version string
        fragment: Optional fragment identifier
        
    Returns:
        Formatted canonical reference string
    """
    if not url:
        return ""
    
    result = url
    if version:
        result = f"{result}|{version}"
    if fragment:
        result = f"{result}#{fragment}"
    return result


def validate_canonical_format(canonical_str: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the format of a canonical reference.
    
    Canonical references must be valid URIs. They may optionally include a version
    separated by | and a fragment separated by #.
    
    Args:
        canonical_str: Canonical reference string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if format is valid, False otherwise
        - error_message: Error message if invalid, None if valid
    """
    if not canonical_str or not isinstance(canonical_str, str):
        return False, "Canonical reference must be a non-empty string"
    
    # Parse to get URL, version, and fragment
    url, version, fragment = parse_canonical(canonical_str)
    
    if not url:
        return False, "Canonical reference must contain a URL"
    
    # Validate URL format (basic URI validation)
    # Canonical URLs should be valid URIs
    uri_pattern = r'^[a-zA-Z][a-zA-Z0-9+.-]*:.*$'  # Basic URI pattern (scheme:...)
    if not re.match(uri_pattern, url):
        # Also allow relative URLs (starting with /)
        if not url.startswith("/"):
            return False, f"Canonical URL must be a valid URI, got: {url}"
    
    # Validate version format if present (should be a valid version string)
    if version:
        # Version should match semantic versioning or similar (alphanumeric, dots, dashes)
        version_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$'
        if not re.match(version_pattern, version):
            return False, f"Canonical version must be a valid version string, got: {version}"
    
    # Validate fragment format if present (should be a valid fragment identifier)
    if fragment:
        # Fragment should be a valid identifier (alphanumeric, dots, dashes, underscores)
        fragment_pattern = r'^[a-zA-Z0-9._-]+$'
        if not re.match(fragment_pattern, fragment):
            return False, f"Canonical fragment must be a valid identifier, got: {fragment}"
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def is_canonical_reference(value: str) -> bool:
    """
    Check if a string looks like a canonical reference.
    
    Canonical references are typically URIs that may include a version.
    This is a heuristic check - not definitive validation.
    
    Args:
        value: String to check
        
    Returns:
        True if string appears to be a canonical reference
    """
    if not value or not isinstance(value, str):
        return False
    
    # Check if it contains a URI scheme or starts with http/https
    if value.startswith(("http://", "https://", "urn:", "/")):
        return True
    
    # Check if it contains | (version separator)
    if "|" in value:
        url_part = value.split("|")[0]
        if url_part.startswith(("http://", "https://", "urn:", "/")):
            return True
    
    return False


def get_canonical_url(canonical_str: str) -> Optional[str]:
    """
    Extract just the URL part from a canonical reference.
    
    Args:
        canonical_str: Canonical reference string
        
    Returns:
        URL part of canonical reference, or None if invalid
    """
    url, _, _ = parse_canonical(canonical_str)
    return url


def get_canonical_version(canonical_str: str) -> Optional[str]:
    """
    Extract just the version part from a canonical reference.
    
    Args:
        canonical_str: Canonical reference string
        
    Returns:
        Version part of canonical reference, or None if not present or invalid
    """
    _, version, _ = parse_canonical(canonical_str)
    return version


def get_canonical_fragment(canonical_str: str) -> Optional[str]:
    """
    Extract just the fragment part from a canonical reference.
    
    Args:
        canonical_str: Canonical reference string
        
    Returns:
        Fragment part of canonical reference, or None if not present or invalid
    """
    _, _, fragment = parse_canonical(canonical_str)

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return fragment


def resolve_canonical_reference(
    canonical_str: str,
    resources: List[FHIRResource],
    resource_type: Optional[str] = None
) -> Optional[FHIRResource]:
    """
    Resolve a canonical reference by finding a resource with matching canonical URL.
    
    Canonical references are resolved by matching the canonical URL (url field)
    of resources. If a version is specified, it must also match.
    
    Args:
        canonical_str: Canonical reference string to resolve
        resources: List of resources to search
        resource_type: Optional resource type to filter by
        
    Returns:
        Matching resource if found, None otherwise
    """
    if not canonical_str:
        return None
    
    url, version, fragment = parse_canonical(canonical_str)
    if not url:
        return None
    
    # Search for matching resource
    for resource in resources:
        # Filter by resource type if specified
        if resource_type and hasattr(resource, "resourceType"):
            if resource.resourceType != resource_type:
                continue
        
        # Check if resource has url field (canonical resources have url)
        if hasattr(resource, "url") and resource.url:
            resource_url = resource.url
            
            # Parse resource URL to compare
            resource_url_base, resource_version, _ = parse_canonical(resource_url)
            
            # Match URL (base part)
            if resource_url_base == url:
                # If version is specified in canonical, it must match
                if version:
                    if resource_version == version:
                        return resource
                else:
                    # No version specified, match by URL only
                    return resource
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return None


def resolve_canonical_references(
    canonical_strs: List[str],
    resources: List[FHIRResource],
    resource_type: Optional[str] = None
) -> Dict[str, Optional[FHIRResource]]:
    """
    Resolve multiple canonical references.
    
    Args:
        canonical_strs: List of canonical reference strings to resolve
        resources: List of resources to search
        resource_type: Optional resource type to filter by
        
    Returns:
        Dictionary mapping canonical strings to resolved resources (None if not found)
    """
    results = {}
    for canonical_str in canonical_strs:
        results[canonical_str] = resolve_canonical_reference(
            canonical_str, resources, resource_type
        )
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Canonical references resolution completed")
    

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return results
