# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 REST API Client.

Provides a client library for interacting with FHIR REST API servers.
All operations include timestamps in logs for traceability.
"""

import json
from datetime import datetime
from typing import Dict, Optional, Any, List, Iterator
from urllib.parse import urlencode, urljoin

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

from dnhealth.dnhealth_fhir.parser_json import parse_resource
from dnhealth.dnhealth_fhir.serializer_json import serialize_resource
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry
from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
from dnhealth.dnhealth_fhir.search import SearchParameters, format_search_parameters
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class FHIRClientError(Exception):
    """Exception raised for FHIR client errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, operation_outcome: Optional[OperationOutcome] = None):
        """
        Initialize FHIR client error.
        
        Args:
            message: Error message
            status_code: HTTP status code (if available)
            operation_outcome: OperationOutcome resource (if available)
        """
        super().__init__(message)
        self.status_code = status_code
        self.operation_outcome = operation_outcome


class FHIRRestClient:
    """
    FHIR R4 REST API Client.
    
    Provides methods for interacting with FHIR REST API servers.
    All operations include timestamps in logs.
    """
    
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        verify: bool = True
    ):
        """
        Initialize the FHIR REST API client.
        
        Args:
            base_url: Base URL of the FHIR server (e.g., "http://localhost:8080/fhir")
            headers: Optional default headers
            timeout: Request timeout in seconds (default: 30)
            verify: Verify SSL certificates (default: True)
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests library is required for REST API client. "
                "Install with: pip install requests"
            )
        
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify = verify
        
        # Default headers
        self.headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
        }
        if headers:
            self.headers.update(headers)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] FHIR REST API Client initialized (base_url: {self.base_url})")
    
    def _make_request(
        self,
        method: str,
        path: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Make an HTTP request to the FHIR server.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            path: Path relative to base URL
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            requests.Response object
            
        Raises:
            FHIRClientError: If request fails
        """
        url = urljoin(self.base_url + "/", path.lstrip("/"))
        
        # Merge headers
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] {method} {url}")
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=request_headers, timeout=self.timeout, verify=self.verify)
            elif method == "POST":
                response = requests.post(url, json=data, params=params, headers=request_headers, timeout=self.timeout, verify=self.verify)
            elif method == "PUT":
                response = requests.put(url, json=data, params=params, headers=request_headers, timeout=self.timeout, verify=self.verify)
            elif method == "DELETE":
                response = requests.delete(url, params=params, headers=request_headers, timeout=self.timeout, verify=self.verify)
            elif method == "PATCH":
                response = requests.patch(url, json=data, params=params, headers=request_headers, timeout=self.timeout, verify=self.verify)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check for errors
            if response.status_code >= 400:
                self._handle_error_response(response)
            
            return response
            
        except requests.exceptions.RequestException as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Request failed: {e}")
            raise FHIRClientError(f"Request failed: {str(e)}")
    
    def _handle_error_response(self, response: requests.Response):
        """
        Handle error response from server.
        
        Args:
            response: requests.Response object with error status
            
        Raises:
            FHIRClientError: With appropriate error details
        """
        try:
            error_data = response.json()
            outcome = parse_resource(error_data)
            if isinstance(outcome, OperationOutcome):
                # Extract error message from OperationOutcome
                issues = outcome.issue or []
                messages = []
                for issue in issues:
                    if issue.diagnostics:
                        messages.append(issue.diagnostics)
                    elif issue.details and issue.details.text:
                        messages.append(issue.details.text)
                
                error_message = "; ".join(messages) if messages else f"HTTP {response.status_code}"
                raise FHIRClientError(error_message, response.status_code, outcome)
        except (ValueError, AttributeError, KeyError):
            pass
        
        # Fallback to generic error
        raise FHIRClientError(
            f"HTTP {response.status_code}: {response.text[:200]}",
            response.status_code
        )
    
    def read(
        self,
        resource_type: str,
        resource_id: str,        version: Optional[str] = None
    ) -> FHIRResource:
        """
        Read a resource by type and ID.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            version: Optional version ID (for versioned read)
            
        Returns:
            FHIRResource object
            
        Raises:
            FHIRClientError: If resource not found or request fails
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Reading resource {resource_type}/{resource_id}")
        
        if version:
            path = f"{resource_type}/{resource_id}/_history/{version}"
        else:
            path = f"{resource_type}/{resource_id}"
        
        response = self._make_request("GET", path)
        data = response.json()
        resource = parse_resource(data)
        
        logger.info(f"[{current_time}] Successfully read resource {resource_type}/{resource_id}")
        return resource
    
    def create(self, resource: FHIRResource, conditional: Optional[str] = None) -> FHIRResource:
        """
        Create a new resource.
        
        Args:
            resource: FHIR resource to create
            conditional: Optional conditional header value (If-None-Match)
            
        Returns:
            Created FHIRResource object
            
        Raises:
            FHIRClientError: If creation fails
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Creating resource of type {resource.resourceType}")
        
        path = resource.resourceType
        
        headers = {}
        if conditional:
            headers["If-None-Match"] = conditional
        
        data = serialize_resource(resource)
        response = self._make_request("POST", path, data=data, headers=headers)
        created_data = response.json()
        created_resource = parse_resource(created_data)

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        
        logger.info(f"[{current_time}] Successfully created resource {resource.resourceType}/{created_resource.id}")
        return created_resource
    
    def update(
        self,
        resource: FHIRResource,
        conditional: Optional[str] = None
    ) -> FHIRResource:
        """
        Update an existing resource.
        
        Args:
            resource: FHIR resource to update (must have id)
            conditional: Optional conditional header value (If-Match)
            
        Returns:
            Updated FHIRResource object
            
        Raises:
            FHIRClientError: If update fails
        """
        if not resource.id:
            raise ValueError("Resource must have an id for update")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Updating resource {resource.resourceType}/{resource.id}")
        
        path = f"{resource.resourceType}/{resource.id}"
        
        headers = {}
        if conditional:
            headers["If-Match"] = conditional
        
        data = serialize_resource(resource)

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        response = self._make_request("PUT", path, data=data, headers=headers)
        updated_data = response.json()
        updated_resource = parse_resource(updated_data)
        
        logger.info(f"[{current_time}] Successfully updated resource {resource.resourceType}/{resource.id}")
        return updated_resource
    
    def delete(
        self,
        resource_type: str,
        resource_id: str,
        conditional: Optional[str] = None
    ) -> None:
        """
        Delete a resource.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            conditional: Optional conditional header value (If-Match)
            
        Raises:
            FHIRClientError: If deletion fails
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Deleting resource {resource_type}/{resource_id}")
        
        path = f"{resource_type}/{resource_id}"
        
        headers = {}
        if conditional:
            headers["If-Match"] = conditional
        
        self._make_request("DELETE", path, headers=headers)
        
        logger.info(f"[{current_time}] Successfully deleted resource {resource_type}/{resource_id}")
    
    def patch(
        self,
        resource_type: str,
        resource_id: str,
        patch_operations: List[Dict[str, Any]],
        conditional: Optional[str] = None
    ) -> FHIRResource:
        """
        Partially update a resource using PATCH.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            patch_operations: List of patch operations (JSON Patch format)
            conditional: Optional conditional header value (If-Match)
            
        Returns:
            Patched FHIRResource object
            
        Raises:
            FHIRClientError: If patch fails
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Patching resource {resource_type}/{resource_id}")
        
        path = f"{resource_type}/{resource_id}"
        
        headers = {}
        if conditional:
            headers["If-Match"] = conditional
        
        response = self._make_request("PATCH", path, data=patch_operations, headers=headers)
        patched_data = response.json()
        patched_resource = parse_resource(patched_data)
        
        logger.info(f"[{current_time}] Successfully patched resource {resource_type}/{resource_id}")
        return patched_resource
    
    def search(
        self,
        resource_type: str,
        search_params: Optional[SearchParameters] = None,
        **kwargs
    ) -> Bundle:
        """
        Search for resources.
        
        Args:
            resource_type: FHIR resource type
            search_params: Optional SearchParameters object
            **kwargs: Search parameters as keyword arguments (e.g., status="active", name="John")
            
        Returns:
            Bundle containing search results
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Searching resources of type {resource_type}")
        
        # Build search parameters
        if search_params is None:
            from dnhealth.dnhealth_fhir.search import SearchParameters as SP
            search_params = SP()
        
        # Add kwargs as search parameters
        for key, value in kwargs.items():
            from dnhealth.dnhealth_fhir.search import SearchParameter
            param = SearchParameter(name=key, value=str(value))
            search_params.parameters.append(param)
        
        # Format search parameters as query string
        query_string = format_search_parameters(search_params)
        
        path = f"{resource_type}?{query_string}" if query_string else resource_type

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        
        response = self._make_request("GET", path)
        bundle_data = response.json()
        bundle = parse_resource(bundle_data)
        
        if not isinstance(bundle, Bundle):
            raise FHIRClientError(f"Expected Bundle, got {type(bundle)}")
        
        logger.info(f"[{current_time}] Search completed: found {bundle.total or len(bundle.entry or [])} resources")
        return bundle
    
    def search_all(
        self,
        resource_type: str,
        search_params: Optional[SearchParameters] = None,
        **kwargs
    ) -> Iterator[FHIRResource]:
        """
        Search for all resources, following pagination links.
        
        Args:
            resource_type: FHIR resource type
            search_params: Optional SearchParameters object
            **kwargs: Search parameters as keyword arguments
            
        Yields:
            FHIRResource objects
        """
        bundle = self.search(resource_type, search_params, **kwargs)
        
        # Yield resources from first page
        for entry in bundle.entry or []:
            if entry.resource:
                yield entry.resource
        
        # Follow next links
        if bundle.link:
            for link in bundle.link:
                if link.relation == "next" and link.url:
                    # Parse next URL and make request
                    next_bundle = self._follow_link(link.url)
                    for entry in next_bundle.entry or []:
                        if entry.resource:
                            yield entry.resource
    
    def _follow_link(self, url: str) -> Bundle:
        """
        Follow a pagination link.
        
        Args:
            url: Full URL to follow
            
        Returns:
            Bundle from the link
        """
        # Extract path from URL
        if self.base_url in url:
            path = url.replace(self.base_url, "").lstrip("/")
        else:
            path = url
        
        response = self._make_request("GET", path)
        bundle_data = response.json()
        bundle = parse_resource(bundle_data)
        
        if not isinstance(bundle, Bundle):
            raise FHIRClientError(f"Expected Bundle, got {type(bundle)}")
        
        return bundle
    
    def history(
        self,
        resource_type: str,
        resource_id: Optional[str] = None,
        count: Optional[int] = None,
        since: Optional[datetime] = None
    ) -> Bundle:
        """
        Get resource history.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Optional resource ID (for resource history)
            count: Optional maximum number of versions
            since: Optional datetime to get versions since
            
        Returns:
            Bundle containing history
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Getting history for {resource_type}" + (f"/{resource_id}" if resource_id else ""))
        
        if resource_id:
            path = f"{resource_type}/{resource_id}/_history"
        else:
            path = f"{resource_type}/_history"
        
        params = {}
        if count:
            params["_count"] = count
        if since:
            params["_since"] = since.isoformat()
        
        response = self._make_request("GET", path, params=params)
        bundle_data = response.json()
        bundle = parse_resource(bundle_data)
        
        if not isinstance(bundle, Bundle):
            raise FHIRClientError(f"Expected Bundle, got {type(bundle)}")
        
        logger.info(f"[{current_time}] History retrieved: {bundle.total or len(bundle.entry or [])} versions")
        return bundle
    
    def batch(self, bundle: Bundle) -> Bundle:
        """
        Execute a batch request.
        
        Args:
            bundle: Bundle with batch entries
            
        Returns:
            Bundle with batch response
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Executing batch request")
        
        bundle.type = "batch"
        data = serialize_resource(bundle)
        
        response = self._make_request("POST", "", data=data)
        response_data = response.json()
        response_bundle = parse_resource(response_data)
        
        if not isinstance(response_bundle, Bundle):
            raise FHIRClientError(f"Expected Bundle, got {type(response_bundle)}")
        
        logger.info(f"[{current_time}] Batch completed: {len(response_bundle.entry or [])} entries processed")
        return response_bundle
    
    def transaction(self, bundle: Bundle) -> Bundle:
        """
        Execute a transaction request.
        
        Args:
            bundle: Bundle with transaction entries
            

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        Returns:
            Bundle with transaction response
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Executing transaction request")
        
        bundle.type = "transaction"
        data = serialize_resource(bundle)
        
        response = self._make_request("POST", "", data=data)
        response_data = response.json()
        response_bundle = parse_resource(response_data)
        
        if not isinstance(response_bundle, Bundle):
            raise FHIRClientError(f"Expected Bundle, got {type(response_bundle)}")
        
        logger.info(f"[{current_time}] Transaction completed: {len(response_bundle.entry or [])} entries processed")
        return response_bundle
    
    def get_metadata(self) -> Any:
        """
        Get server metadata (CapabilityStatement).
        
        Returns:
            CapabilityStatement resource
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Getting server metadata")
        
        response = self._make_request("GET", "metadata")
        metadata_data = response.json()
        metadata = parse_resource(metadata_data)
        
        logger.info(f"[{current_time}] Metadata retrieved")
        return metadata
