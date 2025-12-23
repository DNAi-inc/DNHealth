# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Lazy Loading Support.

Provides lazy loading capabilities for large FHIR resources, allowing resources
to be loaded incrementally or on-demand to reduce memory usage.

This is useful for:
- Large resources that don't need to be fully loaded
- Streaming resource processing
- Memory-efficient resource handling
"""

import json
from typing import Any, Dict, Optional, Type, TypeVar, Callable, Iterator
from datetime import datetime
import logging

from dnhealth.errors import FHIRParseError
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.parser_json import parse_resource

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300

T = TypeVar("T", bound=FHIRResource)


class LazyResource:
    """
    Lazy-loaded FHIR resource wrapper.
    
    This class wraps a resource that can be loaded on-demand, reducing
    memory usage for large resources that may not need to be fully loaded.
    """
    
    def __init__(
        self,
        resource_data: Optional[Dict[str, Any]] = None,
        loader: Optional[Callable[[], FHIRResource]] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None
    ):
        """
        Initialize lazy resource.
        
        Args:
            resource_data: Optional JSON data for the resource (will be parsed on access)
            loader: Optional callable that returns a FHIRResource (called on first access)
            resource_type: Optional resource type hint
            resource_id: Optional resource ID hint
        """
        self._resource_data = resource_data
        self._loader = loader
        self._resource: Optional[FHIRResource] = None
        self._resource_type = resource_type
        self._resource_id = resource_id
        self._loaded = False
        self._load_time: Optional[float] = None
        
        # Extract resource type and ID from data if not provided
        if resource_data and not resource_type:
            self._resource_type = resource_data.get("resourceType")
        if resource_data and not resource_id:
            self._resource_id = resource_data.get("id")
    
    def _load(self) -> FHIRResource:
        """Load the resource (called on first access)."""
        if self._loaded and self._resource is not None:
            return self._resource
        
        from time import time
        start_time = time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Loading lazy resource (type: {self._resource_type}, id: {self._resource_id})")
        
        try:
            if self._loader:
                # Use loader function
                self._resource = self._loader()
            elif self._resource_data:
                # Parse from data
                self._resource = parse_resource(self._resource_data)
            else:
                raise FHIRParseError("No resource data or loader provided for lazy resource")
            
            self._loaded = True
            elapsed = time() - start_time
            self._load_time = elapsed
            
            elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{elapsed_time}] Lazy resource loaded in {elapsed:.3f}s (type: {self._resource_type}, id: {self._resource_id})")
            
            return self._resource
            
        except Exception as e:
            elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{elapsed_time}] Failed to load lazy resource: {e}")
            raise
    
    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to loaded resource."""
        if name.startswith("_"):
            return super().__getattribute__(name)
        
        resource = self._load()
        return getattr(resource, name)
    
    def __getitem__(self, key: str) -> Any:
        """Delegate item access to loaded resource."""
        resource = self._load()
        return resource[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Delegate item setting to loaded resource."""
        resource = self._load()
        resource[key] = value
    
    def __repr__(self) -> str:
        """String representation."""
        if self._loaded:
            return f"<LazyResource loaded: {self._resource_type}/{self._resource_id}>"
        return f"<LazyResource unloaded: {self._resource_type}/{self._resource_id}>"
    
    @property
    def resource(self) -> FHIRResource:
        """Get the loaded resource."""
        return self._load()
    
    @property
    def is_loaded(self) -> bool:
        """Check if resource is loaded."""
        return self._loaded
    
    @property
    def load_time(self) -> Optional[float]:
        """Get time taken to load resource (in seconds)."""

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self._load_time


def parse_resource_lazy(
    data: Dict[str, Any],
    resource_type: Optional[Type[T]] = None
) -> LazyResource:
    """
    Parse a FHIR resource lazily (returns LazyResource wrapper).
    
    The resource will only be fully parsed when first accessed.
    
    Args:
        data: JSON data for the resource
        resource_type: Optional resource type hint
        
    Returns:
        LazyResource wrapper
        
    Example:
        >>> data = {"resourceType": "Patient", "id": "123", "name": [...]}
        >>> lazy_patient = parse_resource_lazy(data)
        >>> # Resource not loaded yet
        >>> print(lazy_patient.is_loaded)  # False
        >>> # Access triggers loading
        >>> name = lazy_patient.name  # Resource loaded here
        >>> print(lazy_patient.is_loaded)  # True
    """
    resource_type_str = data.get("resourceType") if isinstance(data, dict) else None
    resource_id = data.get("id") if isinstance(data, dict) else None
    
    return LazyResource(
        resource_data=data,
        resource_type=resource_type_str,
        resource_id=resource_id
    )

            # Log completion timestamp at end of operation


def parse_resources_lazy_stream(
    data_stream: Iterator[Dict[str, Any]],
    timeout: int = TEST_TIMEOUT
) -> Iterator[LazyResource]:
    """
    Parse a stream of FHIR resources lazily.
    
    Args:
        data_stream: Iterator yielding JSON dictionaries
        timeout: Maximum time in seconds for processing (default: 300)
        
    Yields:
        LazyResource wrappers for each resource
        
    Example:
        >>> def read_resources():
        ...     # Yield resource JSON dicts
        ...     yield {"resourceType": "Patient", "id": "1", ...}
        ...     yield {"resourceType": "Patient", "id": "2", ...}
        ...
        >>> for lazy_resource in parse_resources_lazy_stream(read_resources()):
        ...     # Resources are not loaded until accessed
        ...     if lazy_resource.resourceType == "Patient":
        ...         name = lazy_resource.name  # Loads here
    """
    from time import time
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting lazy resource stream parsing")
    
    count = 0
    try:
        for data in data_stream:
            # Check timeout
            elapsed = time() - start_time
            if elapsed > timeout:
                elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{elapsed_time}] Lazy resource stream parsing exceeded timeout of {timeout} seconds")
                raise TimeoutError(f"Lazy resource stream parsing exceeded timeout of {timeout} seconds")
            
            yield parse_resource_lazy(data)
            count += 1
        
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed = time() - start_time
        logger.debug(f"[{elapsed_time}] Lazy resource stream parsing completed: {count} resources in {elapsed:.3f}s")
        

            # Log completion timestamp at end of operation
    except Exception as e:
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{elapsed_time}] Error in lazy resource stream parsing: {e}")
        raise


def parse_bundle_lazy(
    bundle_data: Dict[str, Any],
    load_entries: bool = False
) -> Dict[str, Any]:
    """
    Parse a Bundle lazily, with optional lazy loading of entries.
    
    Args:
        bundle_data: JSON data for the Bundle
        load_entries: If True, entries are loaded as LazyResource objects (default: False)
        
    Returns:
        Dictionary with Bundle metadata and lazy entry wrappers
        
    Example:
        >>> bundle_data = {
        ...     "resourceType": "Bundle",
        ...     "entry": [
        ...         {"resource": {"resourceType": "Patient", "id": "1", ...}},
        ...         {"resource": {"resourceType": "Patient", "id": "2", ...}}
        ...     ]
        ... }
        >>> lazy_bundle = parse_bundle_lazy(bundle_data, load_entries=True)
        >>> # Entries are LazyResource objects
        >>> for entry in lazy_bundle["entry"]:
        ...     lazy_resource = entry["resource"]
        ...     # Resource not loaded until accessed
        ...     name = lazy_resource.name  # Loads here
    """
    if not isinstance(bundle_data, dict):
        raise FHIRParseError("Bundle data must be a dictionary")
    
    if bundle_data.get("resourceType") != "Bundle":
        raise FHIRParseError("Data is not a Bundle resource")
    
    result = {
        "resourceType": "Bundle",
        "type": bundle_data.get("type"),
        "total": bundle_data.get("total"),
        "link": bundle_data.get("link", []),
        "entry": []
    }
    
    if load_entries and "entry" in bundle_data:
        for entry_data in bundle_data.get("entry", []):
            if "resource" in entry_data:
                lazy_resource = parse_resource_lazy(entry_data["resource"])
                result["entry"].append({
                    "fullUrl": entry_data.get("fullUrl"),
                    "resource": lazy_resource,
                    "search": entry_data.get("search"),
                    "request": entry_data.get("request"),
                    "response": entry_data.get("response")
                })
            else:
                result["entry"].append(entry_data)
    else:
        result["entry"] = bundle_data.get("entry", [])
    
    return result
