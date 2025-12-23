# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR version detection and routing.

Provides version detection from resource JSON/XML and routing to appropriate
version-specific handlers. Supports FHIR R4 and R5 simultaneously.
"""

import json
import logging
import re
from typing import Optional, Literal, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

# FHIR version constants
class FHIRVersion(str, Enum):
    """FHIR version enumeration."""
    R4 = "4.0"
    R5 = "5.0"
    UNKNOWN = "unknown"

# Version string mappings
VERSION_STRINGS = {
    "4.0": FHIRVersion.R4,
    "4.0.0": FHIRVersion.R4,
    "4.0.1": FHIRVersion.R4,
    "R4": FHIRVersion.R4,
    "5.0": FHIRVersion.R5,
    "5.0.0": FHIRVersion.R5,
    "R5": FHIRVersion.R5,
}

# Default version for backward compatibility
DEFAULT_VERSION = FHIRVersion.R4


def detect_version_from_json(json_data: Dict[str, Any]) -> FHIRVersion:
    """
    Detect FHIR version from JSON resource data.
    
    Checks multiple indicators:
    1. Explicit fhirVersion field
    2. Meta.versionId patterns (if available)
    3. Resource structure patterns
    4. Defaults to R4 for backward compatibility
    
    Args:
        json_data: Parsed JSON dictionary
        
    Returns:
        Detected FHIR version
    """
    # Check explicit fhirVersion field
    if "fhirVersion" in json_data:
        version_str = str(json_data["fhirVersion"]).upper()
        if version_str in VERSION_STRINGS:
            return VERSION_STRINGS[version_str]
        # Try partial match
        if "4" in version_str:
            return FHIRVersion.R4
        if "5" in version_str:
            return FHIRVersion.R5
    
    # Check meta.fhirVersion
    if "meta" in json_data and isinstance(json_data["meta"], dict):
        if "fhirVersion" in json_data["meta"]:
            version_str = str(json_data["meta"]["fhirVersion"]).upper()
            if version_str in VERSION_STRINGS:
                return VERSION_STRINGS[version_str]
            if "4" in version_str:
                return FHIRVersion.R4
            if "5" in version_str:
                return FHIRVersion.R5
    
    # Check for R5-specific resource types or fields
    # R5 introduces new resources and changes some structures
    # This is a heuristic - may need refinement based on actual R5 profiles
    resource_type = json_data.get("resourceType", "")
    
    # Check if this is an R5-only resource (exists in R5 but not in R4)
    # If the resource exists in R5 but not in R4, default to R5
    if resource_type:
        try:
            from dnhealth.dnhealth_fhir.resource_registry import (
                get_resource_class,
                _load_r4_resource_class,
                _load_r5_resource_class,
            )
            
            # Check if resource exists in R5 but not in R4
            r5_class = _load_r5_resource_class(resource_type)
            r4_class = _load_r4_resource_class(resource_type)
            
            # If R5 resource exists but R4 doesn't, this is an R5-only resource
            if r5_class is not None and r4_class is None:
                logger.debug(f"Detected R5-only resource: {resource_type}")
                return FHIRVersion.R5
            
            # Check for R5-specific structural differences
            # Some resources have different field structures between R4 and R5
            # For example, Consent.provision is a single object in R4 but a list in R5
            if resource_type == "Consent" and "provision" in json_data:
                if isinstance(json_data["provision"], list):
                    # R5 has provision as a list, R4 has it as a single object
                    logger.debug("Detected R5 Consent structure (provision is a list)")
                    return FHIRVersion.R5
            
            # Appointment.patientInstruction is a string in R4 but a list in R5
            if resource_type == "Appointment" and "patientInstruction" in json_data:
                if isinstance(json_data["patientInstruction"], list):
                    # R5 has patientInstruction as a list, R4 has it as a string
                    logger.debug("Detected R5 Appointment structure (patientInstruction is a list)")
                    return FHIRVersion.R5
            
            # ServiceRequest.patientInstruction is a list in R5 (different structure than R4)
            if resource_type == "ServiceRequest" and "patientInstruction" in json_data:
                if isinstance(json_data["patientInstruction"], list):
                    # R5 has patientInstruction as a list
                    logger.debug("Detected R5 ServiceRequest structure (patientInstruction is a list)")
                    return FHIRVersion.R5
            
            # SupplyDelivery.suppliedItem is a single object in R4 but a list in R5
            if resource_type == "SupplyDelivery" and "suppliedItem" in json_data:
                if isinstance(json_data["suppliedItem"], list):
                    logger.debug("Detected R5 SupplyDelivery structure (suppliedItem is a list)")
                    return FHIRVersion.R5
            
            # Organization.contact.name is a single HumanName in R4 but a list in R5
            if resource_type == "Organization" and "contact" in json_data:
                if isinstance(json_data["contact"], list) and len(json_data["contact"]) > 0:
                    first_contact = json_data["contact"][0]
                    if isinstance(first_contact, dict) and "name" in first_contact:
                        if isinstance(first_contact["name"], list):
                            logger.debug("Detected R5 Organization structure (contact.name is a list)")
                            return FHIRVersion.R5
            
            # Endpoint.connectionType structure differences
            if resource_type == "Endpoint" and "connectionType" in json_data:
                if isinstance(json_data["connectionType"], list):
                    logger.debug("Detected R5 Endpoint structure (connectionType is a list)")
                    return FHIRVersion.R5
            
            # General check: if a field is a list but R4 expects a single value, it's likely R5
            # This is a fallback for resources we haven't explicitly handled
            if r4_class is not None:
                try:
                    from typing import get_origin, get_args
                    r4_fields = r4_class.__dataclass_fields__
                    for field_name, field_value in json_data.items():
                        if field_name in r4_fields and isinstance(field_value, list):
                            r4_field_type = r4_fields[field_name].type
                            origin = get_origin(r4_field_type)
                            # If R4 expects single value (not List) but JSON has list, it might be R5
                            # But be careful - some fields are lists in both versions
                            # Only flag if we're confident it's a structural difference
                            if origin is not list and len(field_value) > 0:
                                # Check if first item is a dict (complex type) when R4 expects single dict
                                if isinstance(field_value[0], dict) and hasattr(r4_field_type, "__dataclass_fields__"):
                                    logger.debug(f"Detected possible R5 {resource_type} structure ({field_name} is a list when R4 expects single value)")
                                    return FHIRVersion.R5
                except Exception:
                    pass
            
            # DeviceMetric.measurementFrequency is Timing in R4 but Quantity in R5
            if resource_type == "DeviceMetric" and "measurementFrequency" in json_data:
                measurement_freq = json_data["measurementFrequency"]
                # R5 has measurementFrequency as Quantity (has value, unit, system, code)
                # R4 has measurementFrequency as Timing (has event, repeat, code)
                if isinstance(measurement_freq, dict):
                    # If it has 'value' and 'code' as string, it's Quantity (R5)
                    # If it has 'event' or 'repeat', it's Timing (R4)
                    if "value" in measurement_freq and "code" in measurement_freq and isinstance(measurement_freq.get("code"), str):
                        logger.debug("Detected R5 DeviceMetric structure (measurementFrequency is Quantity)")
                        return FHIRVersion.R5
                    elif "event" in measurement_freq or "repeat" in measurement_freq:
                        logger.debug("Detected R4 DeviceMetric structure (measurementFrequency is Timing)")
                        return FHIRVersion.R4
            
            # ExampleScenario.actor structure differences
            # R4 has actorId (required), R5 has key, type, title
            if resource_type == "ExampleScenario" and "actor" in json_data:
                if isinstance(json_data["actor"], list) and len(json_data["actor"]) > 0:
                    first_actor = json_data["actor"][0]
                    if isinstance(first_actor, dict):
                        # R5 has 'key' field, R4 has 'actorId' field
                        if "key" in first_actor and "actorId" not in first_actor:
                            logger.debug("Detected R5 ExampleScenario structure (actor has key instead of actorId)")
                            return FHIRVersion.R5
                        elif "actorId" in first_actor and "key" not in first_actor:
                            logger.debug("Detected R4 ExampleScenario structure (actor has actorId)")
                            return FHIRVersion.R4
            
            # DocumentReference.context is single value in R4 but list in R5
            if resource_type == "DocumentReference" and "context" in json_data:
                context_value = json_data["context"]
                if isinstance(context_value, list):
                    logger.debug("Detected R5 DocumentReference structure (context is a list)")
                    return FHIRVersion.R5
                elif isinstance(context_value, dict):
                    logger.debug("Detected R4 DocumentReference structure (context is a single object)")
                    return FHIRVersion.R4
            
            # Composition.relatesTo structure differences
            # R4 has 'code' (required) and 'targetIdentifier'/'targetReference'
            # R5 has 'type' and 'resourceReference'
            if resource_type == "Composition" and "relatesTo" in json_data:
                relates_to = json_data["relatesTo"]
                if isinstance(relates_to, list) and len(relates_to) > 0:
                    first_relates = relates_to[0]
                    if isinstance(first_relates, dict):
                        # R5 has 'type' and 'resourceReference', R4 has 'code' and 'targetIdentifier'/'targetReference'
                        if "type" in first_relates and "resourceReference" in first_relates and "code" not in first_relates:
                            logger.debug("Detected R5 Composition structure (relatesTo has type/resourceReference)")
                            return FHIRVersion.R5
                        elif "code" in first_relates and ("targetIdentifier" in first_relates or "targetReference" in first_relates):
                            logger.debug("Detected R4 Composition structure (relatesTo has code/targetIdentifier/targetReference)")
                            return FHIRVersion.R4
            
            # Check for other R5-specific field patterns
            # R5 often uses arrays where R4 used single values
            r5_array_fields = {
                "Consent": ["sourceAttachment", "sourceReference"],  # R5 uses arrays
                "Medication": ["ingredient"],  # R5 may have different structure
            }
            if resource_type in r5_array_fields:
                for field_name in r5_array_fields[resource_type]:
                    if field_name in json_data and isinstance(json_data[field_name], list):
                        # Check if R4 class expects a single value
                        if r4_class is not None:
                            try:
                                from typing import get_origin, get_args
                                import inspect
                                r4_fields = r4_class.__dataclass_fields__
                                if field_name in r4_fields:
                                    r4_field_type = r4_fields[field_name].type
                                    # If R4 expects single value (not List) but JSON has list, it's R5
                                    origin = get_origin(r4_field_type)
                                    if origin is not list:
                                        logger.debug(f"Detected R5 {resource_type} structure ({field_name} is a list)")
                                        return FHIRVersion.R5
                            except Exception:
                                pass
            
            # Check for R5-specific type differences
            # Substance.instance is bool in R5 but List[SubstanceInstance] in R4
            if resource_type == "Substance" and "instance" in json_data:
                instance_value = json_data["instance"]
                if isinstance(instance_value, bool):
                    # R5 has instance as boolean
                    logger.debug("Detected R5 Substance structure (instance is boolean)")
                    return FHIRVersion.R5
                elif isinstance(instance_value, list):
                    # R4 has instance as list
                    logger.debug("Detected R4 Substance structure (instance is list)")
                    return FHIRVersion.R4
            
            # Check contained resources for version indicators
            # If contained resources have R5-specific structures, parent is likely R5
            if "contained" in json_data and isinstance(json_data["contained"], list):
                for contained_resource in json_data["contained"]:
                    if isinstance(contained_resource, dict):
                        contained_type = contained_resource.get("resourceType")
                        if contained_type == "Substance" and "instance" in contained_resource:
                            if isinstance(contained_resource["instance"], bool):
                                logger.debug("Detected R5 Medication structure (contained Substance has boolean instance)")
                                return FHIRVersion.R5
        except Exception:
            # If there's any error checking, fall back to default
            pass
    
    # For now, default to R4 for backward compatibility
    # When R5 resources are fully implemented, we can add more sophisticated detection
    return DEFAULT_VERSION


def detect_version_from_json_string(json_string: str) -> FHIRVersion:
    """
    Detect FHIR version from JSON string.
    
    Args:
        json_string: JSON string representation
        
    Returns:
        Detected FHIR version
    """
    try:
        data = json.loads(json_string)
        return detect_version_from_json(data)
    except (json.JSONDecodeError, TypeError):
        logger.warning("Failed to parse JSON for version detection, defaulting to R4")
        return DEFAULT_VERSION


def detect_version_from_xml(xml_string: str) -> FHIRVersion:
    """
    Detect FHIR version from XML resource data.
    
    Checks for version indicators in XML:
    1. fhirVersion attribute
    2. Meta element with version information
    3. Resource structure patterns
    
    Args:
        xml_string: XML string representation
        
    Returns:
        Detected FHIR version
    """
    # Check for explicit fhirVersion attribute
    fhir_version_match = re.search(r'fhirVersion=["\']([^"\']+)["\']', xml_string, re.IGNORECASE)
    if fhir_version_match:
        version_str = fhir_version_match.group(1).upper()
        if version_str in VERSION_STRINGS:
            return VERSION_STRINGS[version_str]
        if "4" in version_str:
            return FHIRVersion.R4
        if "5" in version_str:
            return FHIRVersion.R5
    
    # Check meta element for version information
    meta_match = re.search(r'<meta[^>]*>.*?</meta>', xml_string, re.DOTALL | re.IGNORECASE)
    if meta_match:
        meta_content = meta_match.group(0)
        version_match = re.search(r'fhirVersion=["\']([^"\']+)["\']', meta_content, re.IGNORECASE)
        if version_match:
            version_str = version_match.group(1).upper()
            if version_str in VERSION_STRINGS:
                return VERSION_STRINGS[version_str]
            if "4" in version_str:
                return FHIRVersion.R4
            if "5" in version_str:
                return FHIRVersion.R5
    
    # Default to R4 for backward compatibility
    return DEFAULT_VERSION


def get_version_string(version: FHIRVersion) -> str:
    """
    Get version string representation.
    
    Args:
        version: FHIR version enum
        
    Returns:
        Version string (e.g., "4.0", "5.0")
    """
    return version.value


def is_r4(version: FHIRVersion) -> bool:
    """Check if version is R4."""
    return version == FHIRVersion.R4


def is_r5(version: FHIRVersion) -> bool:
    """Check if version is R5."""
    return version == FHIRVersion.R5


def normalize_version(version: Optional[str]) -> FHIRVersion:
    """
    Normalize version string to FHIRVersion enum.
    
    Args:
        version: Version string (can be None, "4.0", "R4", "5.0", "R5", etc.)
        
    Returns:
        Normalized FHIRVersion enum
    """
    if version is None:
        return DEFAULT_VERSION
    
    version_upper = str(version).upper().strip()
    
    # Direct mapping
    if version_upper in VERSION_STRINGS:
        return VERSION_STRINGS[version_upper]
    
    # Pattern matching
    if "4" in version_upper or "R4" in version_upper:
        return FHIRVersion.R4
    if "5" in version_upper or "R5" in version_upper:
        return FHIRVersion.R5
    
    # Default
    return DEFAULT_VERSION
