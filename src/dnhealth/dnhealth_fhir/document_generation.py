# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR document generation workflow (version-aware, supports R4 and R5).

Provides functionality to generate FHIR document Bundles from resources,
including Composition generation, related resource discovery, and document Bundle creation.
Version-aware: supports both FHIR R4 and R5 document generation.
"""

import logging
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry
from dnhealth.dnhealth_fhir.resources.composition import Composition, CompositionSection
from dnhealth.dnhealth_fhir.types import CodeableConcept, Narrative, Reference
from dnhealth.dnhealth_fhir.version import (
    FHIRVersion,
    normalize_version,
    DEFAULT_VERSION
)

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class DocumentGenerator:
    """
    Generate FHIR document Bundles from resources.
    
    This class provides functionality to:
    - Generate Composition resources from source resources
    - Find and include related resources
    - Generate narrative for Composition
    - Create document Bundles
    """

    def __init__(
        self, 
        resource_loader: Optional[Callable[[str], Optional[FHIRResource]]] = None,
        storage: Optional[Any] = None
    ):
        """
        Initialize the document generator.
        
        Args:
            resource_loader: Optional function to load resources by reference
            storage: Optional ResourceStorage instance for persisting documents
        """
        self._resource_loader = resource_loader
        self._storage = storage
        self._resource_cache: Dict[str, FHIRResource] = {}
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] DocumentGenerator initialized")

    def generate_document(
        self,
        resource: FHIRResource,
        document_type: CodeableConcept,
        persist: bool = False,
        max_depth: int = 3,
        fhir_version: Optional[str] = None
    ) -> Bundle:
        """
        Generate a document Bundle from a resource.
        
        Version-aware: supports both FHIR R4 and R5 document generation.
        Defaults to R4 for backward compatibility.
        
        Args:
            resource: Source resource
            document_type: Type of document to generate
            persist: Whether to persist the document
            max_depth: Maximum depth for related resource discovery
            fhir_version: Optional FHIR version (R4 or R5). If not provided, defaults to R4.
            
        Returns:
            Document Bundle (type="document")
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Generating document for resource {resource.resourceType}"
        )
        
        # Normalize version (defaults to R4 for backward compatibility)
        version = normalize_version(fhir_version)
        
        # Find related resources
        related_resources = self.find_related_resources(resource, max_depth=max_depth)
        
        # Create Composition
        composition = self.create_composition(
            resource, related_resources, document_type
        )
        
        # Create document Bundle
        document_bundle = self.create_document_bundle(composition, [resource] + related_resources)
        
        # Persist if requested
        if persist:
            self._persist_document(document_bundle)
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Document generation "
            f"completed in {elapsed:.3f}s"
        )
        
        return document_bundle

    def find_related_resources(
        self, resource: FHIRResource, max_depth: int = 3, current_depth: int = 0
    ) -> List[FHIRResource]:
        """
        Find related resources for a resource.
        
        Args:
            resource: Source resource
            max_depth: Maximum depth for recursive discovery
            current_depth: Current depth (for recursion)
            
        Returns:
            List of related resources
        """
        if current_depth >= max_depth:
            return []
        
        start_time = time.time()
        related_resources = []
        visited_refs = set()
        
        # Extract references from resource
        references = self._extract_references(resource)
        
        # Load referenced resources
        for ref in references:
            if ref in visited_refs:
                continue
            visited_refs.add(ref)
            
            # Load resource
            loaded_resource = self._load_resource(ref)
            if loaded_resource:
                related_resources.append(loaded_resource)
                
                # Recursively find related resources
                if current_depth < max_depth - 1:
                    nested_resources = self.find_related_resources(
                        loaded_resource, max_depth, current_depth + 1
                    )
                    related_resources.extend(nested_resources)
        
        elapsed = time.time() - start_time
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(related_resources)} "
            f"related resources in {elapsed:.3f}s"
        )
        

            # Log completion timestamp at end of operation
        return related_resources

    def create_composition(
        self,
        resource: FHIRResource,
        related_resources: List[FHIRResource],
        document_type: CodeableConcept,
    ) -> Composition:
        """
        Create Composition resource from source resource and related resources.
        
        Args:
            resource: Source resource
            related_resources: List of related resources
            document_type: Type of document
            
        Returns:
            Composition resource
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Creating Composition")
        
        # Create sections
        sections = []
        
        # Main section for source resource
        main_section = CompositionSection(
            title=f"{resource.resourceType} Information",
            code=CodeableConcept(text=resource.resourceType),
            entry=[Reference(reference=f"{resource.resourceType}/{resource.id}")] if hasattr(resource, "id") and resource.id else [],
            text=Narrative(
                status="generated",
                div=f"<div>Information about {resource.resourceType}</div>"
            ),
        )
        sections.append(main_section)
        
        # Sections for related resources (grouped by type)
        resource_groups: Dict[str, List[FHIRResource]] = {}
        for rel_resource in related_resources:
            resource_type = rel_resource.resourceType
            if resource_type not in resource_groups:
                resource_groups[resource_type] = []
            resource_groups[resource_type].append(rel_resource)
        
        for resource_type, resources in resource_groups.items():
            section = CompositionSection(
                title=f"{resource_type} Information",
                code=CodeableConcept(text=resource_type),
                entry=[
                    Reference(reference=f"{r.resourceType}/{r.id}")
                    for r in resources
                    if hasattr(r, "id") and r.id
                ],
                text=Narrative(
                    status="generated",
                    div=f"<div>Information about {len(resources)} {resource_type} resource(s)</div>"
                ),
            )
            sections.append(section)
        
        # Create Composition
        composition = Composition(
            resourceType="Composition",
            status="final",
            type=document_type,
            date=datetime.now().isoformat(),
            title=f"Document for {resource.resourceType}",
            section=sections,
        )
        
        # Set subject if resource has subject
        if hasattr(resource, "subject") and resource.subject:
            composition.subject = resource.subject
        elif hasattr(resource, "patient") and resource.patient:
            composition.subject = resource.patient
        
        elapsed = time.time() - start_time

            # Log completion timestamp at end of operation
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Composition creation "
            f"completed in {elapsed:.3f}s"
        )
        
        return composition

    def create_document_bundle(
        self, composition: Composition, resources: List[FHIRResource]
    ) -> Bundle:
        """
        Create document Bundle from Composition and resources.
        
        Args:
            composition: Composition resource
            resources: List of resources to include
            
        Returns:
            Document Bundle (type="document")
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Creating document Bundle")
        
        # Create entries
        entries = []
        
        # Add Composition as first entry
        entries.append(BundleEntry(resource=composition))
        
        # Add all resources
        for resource in resources:
            entries.append(BundleEntry(resource=resource))
        
        # Create document Bundle
        document_bundle = Bundle(
            resourceType="Bundle",
            type="document",
            entry=entries,
            timestamp=datetime.now().isoformat(),
        )
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Document Bundle creation "
            f"completed in {elapsed:.3f}s"
        )
        
        return document_bundle

    def _extract_references(self, resource: FHIRResource) -> List[str]:
        """Extract reference strings from a resource."""
        references = []
        
        # Recursively extract references from resource fields
        def extract_from_value(value: Any) -> None:
            if isinstance(value, Reference):
                if value.reference:
                    references.append(value.reference)
            elif isinstance(value, list):
                for item in value:
                    extract_from_value(item)
            elif isinstance(value, dict):
                for v in value.values():
                    extract_from_value(v)
            elif hasattr(value, "__dict__"):
                for v in value.__dict__.values():
                    extract_from_value(v)
        
        # Extract from resource
        if hasattr(resource, "__dict__"):
            for value in resource.__dict__.values():
                extract_from_value(value)
        
        return references

    def _load_resource(self, reference: str) -> Optional[FHIRResource]:
        """Load a resource by reference."""
        # Check cache
        if reference in self._resource_cache:
            return self._resource_cache[reference]
        
        # Use resource loader if available
        if self._resource_loader:
            resource = self._resource_loader(reference)
            if resource:
                self._resource_cache[reference] = resource
            return resource
        
        return None

    def _persist_document(self, document_bundle: Bundle) -> None:
        """
        Persist document Bundle to storage.
        
        Args:
            document_bundle: Document Bundle to persist
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Persisting document Bundle")
        
        # Try to persist using storage if available
        if self._storage:
            try:
                # Extract Composition from Bundle (if present)
                composition = None
                for entry in document_bundle.entry or []:
                    if entry.resource and entry.resource.resourceType == "Composition":
                        composition = entry.resource
                        break
                
                # Persist Composition if found
                if composition:
                    if not composition.id:
                        # Generate ID if not present
                        import uuid
                        composition.id = str(uuid.uuid4())
                    
                    # Persist Composition
                    persisted = self._storage.create(composition)
                    logger.info(f"[{current_time}] Persisted Composition {persisted.id}")
                
                # Persist Bundle itself
                if not document_bundle.id:
                    import uuid
                    document_bundle.id = str(uuid.uuid4())
                
                persisted_bundle = self._storage.create(document_bundle)
                logger.info(f"[{current_time}] Persisted document Bundle {persisted_bundle.id}")
                
            except Exception as e:
                logger.warning(f"[{current_time}] Error persisting document Bundle: {e}")
                # Continue execution even if persistence fails
        else:
            logger.info(f"[{current_time}] No storage available - document Bundle not persisted (storage not configured)")
