# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 REST API storage backend.

Provides in-memory storage for FHIR resources. Can be replaced with database backend.
All operations include timestamps in logs for traceability.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from threading import Lock

from dnhealth.dnhealth_fhir.resources.base import FHIRResource, Meta
from dnhealth.dnhealth_fhir.search import SearchParameters, parse_search_string
from dnhealth.dnhealth_fhir.search_execution import execute_search
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class ResourceStorage:
    """
    In-memory storage for FHIR resources.
    
    Provides thread-safe storage with versioning support.
    All operations include timestamps in logs.
    """
    
    def __init__(self):
        """Initialize the storage backend."""
        self._resources: Dict[str, Dict[str, Dict[str, any]]] = {}  # resource_type -> resource_id -> versions
        self._deleted: Dict[str, Dict[str, datetime]] = {}  # resource_type -> resource_id -> deleted_at
        self._lock = Lock()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] ResourceStorage initialized (in-memory backend)")
    
    def _get_resource_key(self, resource_type: str, resource_id: str) -> str:
        """Get storage key for resource."""

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return f"{resource_type}/{resource_id}"
    
    def read(
        self,
        resource_type: str,
        resource_id: str,
        version: Optional[str] = None
    ) -> Optional[FHIRResource]:
        """
        Read a resource by type, id, and optionally version.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            version: Optional version ID
            
        Returns:
            Resource if found, None otherwise
        """
        with self._lock:
            if resource_type not in self._resources:
                return None
            
            if resource_id not in self._resources[resource_type]:
                return None
            
            versions = self._resources[resource_type][resource_id]
            
            if version:
                if version in versions:
                    return versions[version]["resource"]
                return None
            
            # Return latest version
            if versions:
                latest = max(versions.keys(), key=lambda v: versions[v]["timestamp"])
                return versions[latest]["resource"]
            
            return None
    
    def create(self, resource: FHIRResource) -> FHIRResource:
        """
        Create a new resource.
        
        Generates ID if not provided, sets meta.lastUpdated and meta.versionId.
        
        Args:
            resource: FHIR resource to create
            
        Returns:
            Created resource with generated metadata
        """
        with self._lock:
            # Generate ID if not provided
            if not resource.id:
                resource.id = str(uuid.uuid4())
            
            # Set or update meta
            if not resource.meta:
                resource.meta = Meta()
            
            now = datetime.now().isoformat()
            resource.meta.lastUpdated = now
            resource.meta.versionId = "1"
            
            resource_type = resource.resourceType
            resource_id = resource.id
            
            # Initialize storage for this resource type if needed
            if resource_type not in self._resources:
                self._resources[resource_type] = {}
            
            # Initialize versions for this resource if needed
            if resource_id not in self._resources[resource_type]:
                self._resources[resource_type][resource_id] = {}
            
            # Store version
            version_id = resource.meta.versionId
            self._resources[resource_type][resource_id][version_id] = {
                "resource": resource,
                "timestamp": now
            }
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{current_time}] Created resource {resource_type}/{resource_id} version {version_id}")
            
            return resource
    
    def update(
        self,
        resource_type: str,
        resource_id: str,
        resource: FHIRResource
    ) -> FHIRResource:
        """
        Update an existing resource.
        
        Creates a new version with incremented versionId.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            resource: Updated resource
            
        Returns:
            Updated resource with new version
            
        Raises:
            ValueError: If resource doesn't exist
        """
        with self._lock:
            if resource_type not in self._resources:
                raise ValueError(f"Resource {resource_type}/{resource_id} not found")
            
            if resource_id not in self._resources[resource_type]:
                raise ValueError(f"Resource {resource_type}/{resource_id} not found")
            
            # Check if deleted
            if resource_type in self._deleted and resource_id in self._deleted[resource_type]:
                raise ValueError(f"Resource {resource_type}/{resource_id} is deleted")
            
            versions = self._resources[resource_type][resource_id]
            
            # Get current version number
            if versions:
                latest_version = max(versions.keys(), key=lambda v: int(v) if v.isdigit() else 0)
                try:
                    next_version = str(int(latest_version) + 1)
                except ValueError:
                    next_version = "1"
            else:
                next_version = "1"
            
            # Set or update meta
            if not resource.meta:
                resource.meta = Meta()
            
            now = datetime.now().isoformat()
            resource.meta.lastUpdated = now
            resource.meta.versionId = next_version
            
            # Store new version
            versions[next_version] = {
                "resource": resource,
                "timestamp": now
            }
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{current_time}] Updated resource {resource_type}/{resource_id} to version {next_version}")
            
            return resource
    
    def delete(
        self,
        resource_type: str,
        resource_id: str
    ) -> bool:
        """
        Delete a resource (soft delete).
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if resource_type not in self._resources:
                return False
            
            if resource_id not in self._resources[resource_type]:
                return False
            
            # Mark as deleted
            if resource_type not in self._deleted:
                self._deleted[resource_type] = {}
            
            self._deleted[resource_type][resource_id] = datetime.now()
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{current_time}] Deleted resource {resource_type}/{resource_id}")
            
            return True
    
    def is_deleted(
        self,
        resource_type: str,
        resource_id: str
    ) -> bool:
        """
        Check if a resource is deleted.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            
        Returns:
            True if deleted, False otherwise
        """
        with self._lock:
            if resource_type not in self._deleted:
                return False
            

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return resource_id in self._deleted[resource_type]
    
    def get_history(
        self,
        resource_type: str,
        resource_id: str,
        count: Optional[int] = None,
        since: Optional[datetime] = None
    ) -> List[Tuple[str, FHIRResource, datetime]]:
        """
        Get version history for a resource.
        
        Args:
            resource_type: FHIR resource type
            resource_id: Resource ID
            count: Maximum number of versions to return
            since: Only return versions after this date
            
        Returns:
            List of (version_id, resource, timestamp) tuples
        """
        with self._lock:
            if resource_type not in self._resources:
                return []
            
            if resource_id not in self._resources[resource_type]:
                return []
            
            versions = self._resources[resource_type][resource_id]
            
            # Build history list
            history = []
            for version_id, version_data in versions.items():
                timestamp_str = version_data["timestamp"]
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except (ValueError, AttributeError):
                    timestamp = datetime.now()
                
                if since and timestamp <= since:
                    continue
                
                history.append((version_id, version_data["resource"], timestamp))
            
            # Sort by timestamp descending
            history.sort(key=lambda x: x[2], reverse=True)
            
            # Apply count limit
            if count:
                history = history[:count]
            
            return history
    
    def search(
        self,
        resource_type: str,
        filters: Optional[Dict[str, any]] = None,
        search_params: Optional[SearchParameters] = None
    ) -> List[FHIRResource]:
        """
        Search for resources by type and optional filters.
        
        Args:
            resource_type: FHIR resource type
            filters: Optional search filters (deprecated, use search_params instead)
            search_params: Optional SearchParameters object with parsed search parameters
            
        Returns:
            List of matching resources (latest version of each)
        """
        with self._lock:
            if resource_type not in self._resources:
                return []
            
            results = []
            for resource_id, versions in self._resources[resource_type].items():
                # Skip deleted resources
                if self.is_deleted(resource_type, resource_id):
                    continue
                
                # Get latest version
                if versions:
                    latest = max(versions.keys(), key=lambda v: versions[v]["timestamp"])
                    results.append(versions[latest]["resource"])
            
            # Apply search filters if provided
            if search_params:
                # Use search execution engine to filter resources
                try:
                    # Pass results as all_resources for _revinclude processing support
                    # Note: In this context, all_resources is limited to this resource_type
                    results = execute_search(
                        resources=results,
                        search_params=search_params,
                        param_type_map=None,  # Can be enhanced to use SearchParameter resources
                        resource_resolver=self._resolve_reference,
                        all_resources=results  # Pass for _revinclude support (limited to this resource_type)
                    )
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"[{current_time}] Applied search filters: {len(results)} resources match")
                except Exception as e:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.error(f"[{current_time}] Error applying search filters: {e}")
                    # Return unfiltered results on error
                    pass
            elif filters:
                # Legacy filter support (convert dict to SearchParameters)
                # This is a simplified implementation for backward compatibility
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{current_time}] Using legacy filters parameter, consider using search_params instead")
                # For now, return all results if legacy filters are used
                # Full implementation would convert filters dict to SearchParameters
            
            return results
    
    def _resolve_reference(self, reference: str) -> Optional[FHIRResource]:
        """
        Resolve a FHIR reference to a resource.
        
        Used by search execution for chained searches.
        
        Args:
            reference: FHIR reference (e.g., "Patient/123" or "http://example.com/Patient/123")
            
        Returns:
            Resource if found, None otherwise
        """
        # Parse reference format: ResourceType/id or URL
        if "/" in reference:
            parts = reference.split("/")
            if len(parts) >= 2:
                # Handle URL format: http://example.com/fhir/Patient/123
                if parts[0].startswith("http"):
                    # Extract resource type and ID from URL
                    resource_type = None
                    resource_id = None
                    for i, part in enumerate(parts):
                        if part in self._resources:  # Check if this part is a resource type
                            resource_type = part
                            if i + 1 < len(parts):
                                resource_id = parts[i + 1]
                                break
                    if resource_type and resource_id:

                                    # Log completion timestamp at end of operation
                                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    logger.info(f"Current Time at End of Operations: {current_time}")
                        return self.read(resource_type, resource_id)
                else:
                    # Handle simple format: Patient/123
                    resource_type = parts[-2]
                    resource_id = parts[-1]
                    return self.read(resource_type, resource_id)
        
        return None
    
    def get_compartment(
        self,
        resource_type: str,
        resource_id: str,
        compartment: str,
        search_params: Optional[Dict[str, any]] = None
    ) -> List[FHIRResource]:
        """
        Get resources in a compartment.
        
        Args:
            resource_type: FHIR resource type of the compartment owner
            resource_id: Resource ID of the compartment owner
            compartment: Compartment name (e.g., "Patient", "Encounter")
            search_params: Optional search parameters
            
        Returns:
            List of resources in the compartment
        """
        with self._lock:
            # Verify compartment owner exists
            owner = self.read(resource_type, resource_id)
            if not owner:
                return []
            
            # Get all resources of types that can be in this compartment
            # This is a simplified implementation - full implementation would
            # check compartment definitions and reference relationships
            compartment_resource_types = {
                "Patient": ["Observation", "Condition", "Procedure", "Encounter", "MedicationRequest"],
                "Encounter": ["Observation", "Procedure", "MedicationRequest"],
                "Practitioner": ["Encounter", "Observation", "Procedure"],
                "Device": ["Observation", "Procedure"],
                "RelatedPerson": ["Observation", "Condition"]
            }
            
            types_to_search = compartment_resource_types.get(compartment, [])
            results = []
            
            for comp_type in types_to_search:
                if comp_type not in self._resources:
                    continue
                
                for comp_id, versions in self._resources[comp_type].items():
                    if self.is_deleted(comp_type, comp_id):
                        continue
                    
                    if versions:
                        latest = max(versions.keys(), key=lambda v: versions[v]["timestamp"])
                        comp_resource = versions[latest]["resource"]
                        
                        # Check if resource references the compartment owner
                        if self._resource_in_compartment(comp_resource, resource_type, resource_id):
                            results.append(comp_resource)
            
            return results
    
    def _resource_in_compartment(
        self,
        resource: FHIRResource,
        owner_type: str,
        owner_id: str
    ) -> bool:
        """
        Check if a resource belongs to a compartment.
        
        Args:
            resource: Resource to check
            owner_type: Compartment owner resource type
            owner_id: Compartment owner resource ID
            
        Returns:
            True if resource is in compartment
        """
        # Check subject reference
        if hasattr(resource, "subject") and resource.subject:
            if hasattr(resource.subject, "reference"):
                ref = resource.subject.reference
                if ref == f"{owner_type}/{owner_id}":
                    return True
        
        # Check patient reference
        if hasattr(resource, "patient") and resource.patient:
            if hasattr(resource.patient, "reference"):
                ref = resource.patient.reference
                if ref == f"{owner_type}/{owner_id}":
                    return True
        
        # Check encounter reference
        if hasattr(resource, "encounter") and resource.encounter:
            if hasattr(resource.encounter, "reference"):
                ref = resource.encounter.reference
                if ref == f"{owner_type}/{owner_id}":

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
                    return True
        
        # Check context reference
        if hasattr(resource, "context") and resource.context:
            if hasattr(resource.context, "reference"):
                ref = resource.context.reference
                if ref == f"{owner_type}/{owner_id}":
                    return True
        
        return False
    
    def get_type_history(
        self,
        resource_type: str,
        count: Optional[int] = None,
        since: Optional[datetime] = None
    ) -> List[Tuple[str, FHIRResource, datetime]]:
        """
        Get version history for all resources of a type.
        
        Args:
            resource_type: FHIR resource type
            count: Maximum number of versions to return
            since: Only return versions after this date
            
        Returns:
            List of (version_id, resource, timestamp) tuples
        """
        with self._lock:
            if resource_type not in self._resources:
                return []
            
            history = []
            for resource_id, versions in self._resources[resource_type].items():
                for version_id, version_data in versions.items():
                    timestamp_str = version_data["timestamp"]
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                    except (ValueError, AttributeError):
                        timestamp = datetime.now()
                    
                    if since and timestamp <= since:
                        continue
                    
                    history.append((version_id, version_data["resource"], timestamp))
            
            # Sort by timestamp descending
            history.sort(key=lambda x: x[2], reverse=True)
            
            # Apply count limit
            if count:
                history = history[:count]
            
            return history
    
    def get_system_history(
        self,
        count: Optional[int] = None,
        since: Optional[datetime] = None
    ) -> List[Tuple[str, FHIRResource, datetime]]:
        """
        Get version history for all resources.
        
        Args:
            count: Maximum number of versions to return
            since: Only return versions after this date
            
        Returns:
            List of (version_id, resource, timestamp) tuples
        """
        with self._lock:
            history = []
            
            for resource_type, resources in self._resources.items():
                for resource_id, versions in resources.items():
                    for version_id, version_data in versions.items():
                        timestamp_str = version_data["timestamp"]
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str)
                        except (ValueError, AttributeError):
                            timestamp = datetime.now()
                        
                        if since and timestamp <= since:
                            continue
                        
                        history.append((version_id, version_data["resource"], timestamp))
            
            # Sort by timestamp descending
            history.sort(key=lambda x: x[2], reverse=True)
            
            # Apply count limit
            if count:
                history = history[:count]
            
            return history
