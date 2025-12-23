# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Version-aware FHIR resource registry.

Provides version-aware resource class lookup for R4 and R5 resources.
Supports lazy loading and maintains backward compatibility.
"""

import logging
from typing import Dict, Optional, Type, TypeVar
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.version import FHIRVersion, DEFAULT_VERSION

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=FHIRResource)

# R4 resource type mapping (lazy-loaded for some resources)
_R4_RESOURCE_MAP: Dict[str, Optional[Type[FHIRResource]]] = {
    "Patient": None,  # Will be loaded lazily
    "Observation": None,
    "Encounter": None,
    "Bundle": None,
    "Condition": None,
    "OperationOutcome": None,
    "StructureDefinition": None,
    "ValueSet": None,
    "CodeSystem": None,
    "ConceptMap": None,
    "Task": None,  # Task resource for workflow management
}

# R5 resource type mapping (will be populated when R5 resources are generated)
_R5_RESOURCE_MAP: Dict[str, Optional[Type[FHIRResource]]] = {
    # R5 resources will be added here when generated
    # For now, this is empty and will fall back to R4
}

# Cache for loaded resource classes
_LOADED_R4_CLASSES: Dict[str, Type[FHIRResource]] = {}
_LOADED_R5_CLASSES: Dict[str, Type[FHIRResource]] = {}


def _load_r4_resource_class(resource_type: str) -> Optional[Type[FHIRResource]]:
    """
    Lazily load an R4 resource class.
    
    Args:
        resource_type: Resource type name (e.g., "Patient", "Observation")
        
    Returns:
        Resource class or None if not found
    """
    if resource_type in _LOADED_R4_CLASSES:
        return _LOADED_R4_CLASSES[resource_type]
    
    try:
        # Common resources
        if resource_type == "Patient":
            from dnhealth.dnhealth_fhir.resources.patient import Patient
            _LOADED_R4_CLASSES[resource_type] = Patient
            return Patient
        elif resource_type == "Observation":
            from dnhealth.dnhealth_fhir.resources.observation import Observation
            _LOADED_R4_CLASSES[resource_type] = Observation
            return Observation
        elif resource_type == "Encounter":
            from dnhealth.dnhealth_fhir.resources.encounter import Encounter
            _LOADED_R4_CLASSES[resource_type] = Encounter
            return Encounter
        elif resource_type == "Bundle":
            from dnhealth.dnhealth_fhir.resources.bundle import Bundle
            _LOADED_R4_CLASSES[resource_type] = Bundle
            return Bundle
        elif resource_type == "Condition":
            from dnhealth.dnhealth_fhir.resources.condition import Condition
            _LOADED_R4_CLASSES[resource_type] = Condition
            return Condition
        elif resource_type == "OperationOutcome":
            from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome
            _LOADED_R4_CLASSES[resource_type] = OperationOutcome
            return OperationOutcome
        elif resource_type == "StructureDefinition":
            from dnhealth.dnhealth_fhir.resources.structuredefinition import StructureDefinition
            _LOADED_R4_CLASSES[resource_type] = StructureDefinition
            return StructureDefinition
        elif resource_type == "ValueSet":
            from dnhealth.dnhealth_fhir.resources.valueset import ValueSet
            _LOADED_R4_CLASSES[resource_type] = ValueSet
            return ValueSet
        elif resource_type == "CodeSystem":
            from dnhealth.dnhealth_fhir.resources.codesystem import CodeSystem
            _LOADED_R4_CLASSES[resource_type] = CodeSystem
            return CodeSystem
        elif resource_type == "ConceptMap":
            from dnhealth.dnhealth_fhir.resources.conceptmap import ConceptMap
            _LOADED_R4_CLASSES[resource_type] = ConceptMap
            return ConceptMap
        elif resource_type == "Task":
            from dnhealth.dnhealth_fhir.resources.task import Task
            _LOADED_R4_CLASSES[resource_type] = Task
            return Task
        else:
            # Try to import from resources module
            try:
                resources_module = __import__(
                    f"dnhealth.dnhealth_fhir.resources.{resource_type.lower()}",
                    fromlist=[resource_type]
                )
                resource_class = getattr(resources_module, resource_type)
                _LOADED_R4_CLASSES[resource_type] = resource_class
                return resource_class
            except (ImportError, AttributeError):
                logger.debug(f"R4 resource class not found: {resource_type}")
                return None
    except Exception as e:
        logger.warning(f"Error loading R4 resource class {resource_type}: {e}")
        return None


def _load_r5_resource_class(resource_type: str) -> Optional[Type[FHIRResource]]:
    """
    Lazily load an R5 resource class.
    
    Args:
        resource_type: Resource type name (e.g., "Patient", "Observation")
        
    Returns:
        Resource class or None if not found (falls back to R4)
    """
    if resource_type in _LOADED_R5_CLASSES:
        return _LOADED_R5_CLASSES[resource_type]
    
    # Try to load R5 resource from r5.resources module
    try:
        # Import the r5.resources module dynamically
        from dnhealth.dnhealth_fhir.r5 import resources as r5_resources
        
        # Get the resource class by name
        resource_class = getattr(r5_resources, resource_type, None)
        
        if resource_class is not None:
            _LOADED_R5_CLASSES[resource_type] = resource_class
            _R5_RESOURCE_MAP[resource_type] = resource_class
            logger.debug(f"Loaded R5 resource class: {resource_type}")
            return resource_class
        
        # Resource not found in R5 module
        logger.debug(f"R5 resource class not found: {resource_type}, falling back to R4")
        return None
    except ImportError as e:
        # R5 resources module not available or not yet generated
        logger.debug(f"R5 resources module not available: {e}, falling back to R4")
        return None
    except Exception as e:
        logger.debug(f"Error loading R5 resource class {resource_type}: {e}")
        return None


def get_resource_class(
    resource_type: str,
    fhir_version: Optional[FHIRVersion] = None
) -> Optional[Type[FHIRResource]]:
    """
    Get resource class for a given resource type and FHIR version.
    
    This is the main entry point for version-aware resource lookup.
    Supports both R4 and R5, with automatic fallback to R4 for backward compatibility.
    
    Args:
        resource_type: Resource type name (e.g., "Patient", "Observation")
        fhir_version: FHIR version (R4 or R5). If None, defaults to R4 for backward compatibility.
        
    Returns:
        Resource class or None if not found
        
    Examples:
        >>> patient_class = get_resource_class("Patient", FHIRVersion.R4)
        >>> r5_patient_class = get_resource_class("Patient", FHIRVersion.R5)  # Falls back to R4 for now
    """
    # Normalize version
    if fhir_version is None:
        fhir_version = DEFAULT_VERSION
    
    # Try R5 first if requested
    if fhir_version == FHIRVersion.R5:
        r5_class = _load_r5_resource_class(resource_type)
        if r5_class is not None:
            return r5_class
        # Fall back to R4 if R5 not available
        logger.debug(f"R5 resource {resource_type} not available, falling back to R4")
    
    # Use R4 (default or fallback)
    return _load_r4_resource_class(resource_type)


def register_resource_class(
    resource_type: str,
    resource_class: Type[FHIRResource],
    fhir_version: Optional[FHIRVersion] = None
) -> None:
    """
    Register a resource class for a specific version.
    
    This allows dynamic registration of resource classes, useful for
    custom resources or when R5 resources are generated.
    
    Args:
        resource_type: Resource type name (e.g., "Patient")
        resource_class: Resource class to register
        fhir_version: FHIR version (R4 or R5). If None, defaults to R4.
    """
    if fhir_version is None:
        fhir_version = DEFAULT_VERSION
    
    if fhir_version == FHIRVersion.R5:
        _LOADED_R5_CLASSES[resource_type] = resource_class
        _R5_RESOURCE_MAP[resource_type] = resource_class
        logger.debug(f"Registered R5 resource class: {resource_type}")
    else:
        _LOADED_R4_CLASSES[resource_type] = resource_class
        _R4_RESOURCE_MAP[resource_type] = resource_class
        logger.debug(f"Registered R4 resource class: {resource_type}")


def list_resource_types(fhir_version: Optional[FHIRVersion] = None) -> list:
    """
    List all available resource types for a given version.
    
    Args:
        fhir_version: FHIR version (R4 or R5). If None, returns R4 types.
        
    Returns:
        List of resource type names
    """
    if fhir_version == FHIRVersion.R5:
        # When R5 resources are available, return R5 types
        # For now, return empty list
        return list(_R5_RESOURCE_MAP.keys())
    else:
        # Return all R4 resource types from resources module
        try:
            from dnhealth.dnhealth_fhir.resources import __all__ as r4_resources
            # Filter to get resource type names (exclude nested classes)
            resource_types = [
                name for name in r4_resources
                if name[0].isupper() and not name.startswith("_")
            ]
            return sorted(set(resource_types))
        except ImportError:
            # Fallback to hardcoded list
            return list(_R4_RESOURCE_MAP.keys())


def is_resource_type_available(
    resource_type: str,
    fhir_version: Optional[FHIRVersion] = None
) -> bool:
    """
    Check if a resource type is available for a given version.
    
    Args:
        resource_type: Resource type name
        fhir_version: FHIR version (R4 or R5). If None, checks R4.
        
    Returns:
        True if resource type is available, False otherwise
    """
    resource_class = get_resource_class(resource_type, fhir_version)
    return resource_class is not None
