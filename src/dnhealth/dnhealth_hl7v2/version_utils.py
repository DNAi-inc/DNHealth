# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Version-Specific Utilities.

Provides utilities for handling version-specific differences in HL7 v2.x messages,
segments, fields, and data types across versions 2.1 through 2.9.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# Supported HL7 v2.x versions
SUPPORTED_VERSIONS = ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"]

# Version comparison mapping
VERSION_ORDER = {v: i for i, v in enumerate(SUPPORTED_VERSIONS)}


def is_version_supported(version: str) -> bool:
    """
    Check if a version is supported.
    
    Args:
        version: HL7 version string (e.g., "2.5")
        
    Returns:
        True if version is supported, False otherwise
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking if version {version} is supported")
    return version in SUPPORTED_VERSIONS


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two HL7 versions.
    
    Args:
        version1: First version string
        version2: Second version string
        
    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Comparing versions {version1} and {version2}")
    
    if version1 not in VERSION_ORDER or version2 not in VERSION_ORDER:
        logger.warning(f"[{current_time}] One or both versions not in supported list: {version1}, {version2}")
        return 0
    
    order1 = VERSION_ORDER[version1]
    order2 = VERSION_ORDER[version2]
    
    if order1 < order2:
        return -1
    elif order1 > order2:
        return 1
    else:
        return 0


def is_version_gte(version: str, min_version: str) -> bool:
    """
    Check if version is greater than or equal to minimum version.
    
    Args:
        version: Version to check
        min_version: Minimum version required
        
    Returns:
        True if version >= min_version, False otherwise
    """
    return compare_versions(version, min_version) >= 0


def is_version_lte(version: str, max_version: str) -> bool:
    """
    Check if version is less than or equal to maximum version.
    
    Args:
        version: Version to check
        max_version: Maximum version allowed
        
    Returns:
        True if version <= max_version, False otherwise
    """
    return compare_versions(version, max_version) <= 0


def is_version_in_range(version: str, min_version: Optional[str] = None, max_version: Optional[str] = None) -> bool:
    """
    Check if version is within specified range.
    
    Args:
        version: Version to check
        min_version: Optional minimum version (inclusive)
        max_version: Optional maximum version (inclusive)
        
    Returns:
        True if version is within range, False otherwise
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Checking if version {version} is in range [{min_version}, {max_version}]")
    
    if not is_version_supported(version):
        return False
    
    if min_version and not is_version_gte(version, min_version):
        return False
    
    if max_version and not is_version_lte(version, max_version):
        return False
    
    return True


def get_version_specific_field(
    segment_name: str,
    field_index: int,
    version: str,    default_value: Optional[any] = None
) -> Optional[any]:
    """
    Get version-specific field value from field definition.
    
    Args:
        segment_name: Segment name (e.g., "EVN")
        field_index: Field index (1-based)
        version: HL7 version
        default_value: Default value if version-specific value not found
        
    Returns:
        Version-specific field value or default
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting version-specific field {segment_name}-{field_index} for version {version}")
    
    try:
        from dnhealth.dnhealth_hl7v2.segment_definitions import get_field_definition
        
        field_def = get_field_definition(segment_name, field_index, version=version)
        if field_def is None:
            logger.warning(f"[{current_time}] Field definition not found for {segment_name}-{field_index}")
            return default_value
        
        # Check if version-specific override exists
        if version in field_def.version_specific:
            override = field_def.version_specific[version]
            logger.debug(f"[{current_time}] Found version-specific override for {segment_name}-{field_index} in version {version}")
            return override
        
        return default_value
    except Exception as e:
        logger.error(f"[{current_time}] Error getting version-specific field: {e}")
        return default_value


def get_segments_available_in_version(version: str) -> Set[str]:
    """
    Get set of segments available in a specific version.
    
    Args:
        version: HL7 version
        
    Returns:
        Set of segment names available in this version
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting segments available in version {version}")
    
    # Base segments available in all versions
    base_segments = {
        "MSH", "EVN", "PID", "PV1", "OBR", "OBX", "NTE", "AL1", "DG1", "PR1",
        "ORC", "IN1", "IN2", "IN3", "NK1", "PD1", "PV2", "GT1", "MSA", "ERR"
    }
    
    # Segments added in later versions
    if is_version_gte(version, "2.3"):
        base_segments.update({"QRD", "QRF", "QAK"})
    
    if is_version_gte(version, "2.4"):
        base_segments.update({"QPD", "RGS", "SPM"})
    
    if is_version_gte(version, "2.5"):
        base_segments.update({"DSC", "RCP", "RF1"})
    
    if is_version_gte(version, "2.6"):
        base_segments.update({"ROL", "CTD", "ACC"})
    
    if is_version_gte(version, "2.7"):
        base_segments.update({"SCH", "TXA", "RMI"})
    
    logger.debug(f"[{current_time}] Found {len(base_segments)} segments available in version {version}")
    return base_segments


def validate_version_compatibility(
    source_version: str,
    target_version: str,
    segment_name: Optional[str] = None
) -> Tuple[bool, List[str]]:
    """
    Validate if a message/segment from source_version is compatible with target_version.
    
    Args:
        source_version: Source HL7 version
        target_version: Target HL7 version
        segment_name: Optional segment name to check compatibility for
        
    Returns:
        Tuple of (is_compatible, list_of_warnings)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Validating version compatibility: {source_version} -> {target_version}")
    
    warnings = []
    
    if not is_version_supported(source_version):
        warnings.append(f"Source version {source_version} is not supported")
        logger.warning(f"[{current_time}] Source version {source_version} not supported")
    
    if not is_version_supported(target_version):
        warnings.append(f"Target version {target_version} is not supported")
        logger.warning(f"[{current_time}] Target version {target_version} not supported")
        return False, warnings
    
    # Check segment availability if specified
    if segment_name:
        source_segments = get_segments_available_in_version(source_version)
        target_segments = get_segments_available_in_version(target_version)
        
        if segment_name in source_segments and segment_name not in target_segments:
            warnings.append(f"Segment {segment_name} exists in {source_version} but not in {target_version}")
            logger.warning(f"[{current_time}] Segment {segment_name} not available in target version")
        elif segment_name not in source_segments and segment_name in target_segments:
            warnings.append(f"Segment {segment_name} does not exist in {source_version} but exists in {target_version}")
            logger.warning(f"[{current_time}] Segment {segment_name} not available in source version")
    
    is_compatible = len(warnings) == 0
    if is_compatible:
        logger.info(f"[{current_time}] Version compatibility check passed")
    else:
        logger.warning(f"[{current_time}] Version compatibility check found {len(warnings)} warning(s)")
    
    return is_compatible, warnings


def get_version_differences(version1: str, version2: str) -> Dict[str, List[str]]:
    """
    Get differences between two HL7 versions.
    
    Args:
        version1: First version
        version2: Second version
        
    Returns:
        Dictionary with differences categorized by type
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting version differences between {version1} and {version2}")
    
    differences = {
        "segments_added": [],
        "segments_removed": [],
        "fields_added": [],
        "fields_removed": [],
        "data_type_changes": [],
        "table_changes": [],
    }
    
    if not is_version_supported(version1) or not is_version_supported(version2):
        logger.warning(f"[{current_time}] One or both versions not supported")
        return differences
    
    # Get segments available in each version
    segments_v1 = get_segments_available_in_version(version1)
    segments_v2 = get_segments_available_in_version(version2)
    
    # Find segments added/removed
    differences["segments_added"] = list(segments_v2 - segments_v1)
    differences["segments_removed"] = list(segments_v1 - segments_v2)
    
    logger.debug(f"[{current_time}] Found {len(differences['segments_added'])} segments added, {len(differences['segments_removed'])} segments removed")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return differences


def get_version_specific_field_definition(
    segment_name: str,
    field_index: int,
    version: str
) -> Optional[Dict[str, any]]:
    """
    Get version-specific field definition with all overrides applied.
    
    This function retrieves the base field definition and applies version-specific
    overrides to return the complete field definition for the specified version.
    
    Args:
        segment_name: Segment name (e.g., "EVN")
        field_index: Field index (1-based)
        version: HL7 version (e.g., "2.5")
        
    Returns:
        Dictionary with complete field definition for the version, or None if not found
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting version-specific field definition for {segment_name}-{field_index} in version {version}")
    
    try:
        from dnhealth.dnhealth_hl7v2.segment_definitions import get_field_definition
        
        # Get base field definition
        field_def = get_field_definition(segment_name, field_index)
        if field_def is None:
            logger.warning(f"[{current_time}] Field definition not found for {segment_name}-{field_index}")
            return None
        
        # Build result dictionary with base definition
        result = {
            "field_index": field_def.field_index,
            "field_name": field_def.field_name,
            "data_type": field_def.data_type,
            "length": field_def.length,
            "min_length": field_def.min_length,
            "required": field_def.required,
            "optional": field_def.optional,
            "repeating": field_def.repeating,
            "table_binding": field_def.table_binding,
            "description": field_def.description,
        }
        
        # Apply version-specific overrides if they exist
        if version in field_def.version_specific:
            override = field_def.version_specific[version]
            result.update(override)
            logger.debug(f"[{current_time}] Applied version-specific overrides for {segment_name}-{field_index} in version {version}")
        
        logger.debug(f"[{current_time}] Retrieved complete field definition for {segment_name}-{field_index} in version {version}")
        return result
        
    except Exception as e:
        logger.error(f"[{current_time}] Error getting version-specific field definition: {e}")
        return None


def get_all_version_specific_differences(
    segment_name: str,
    field_index: int
) -> Dict[str, Dict[str, any]]:
    """
    Get all version-specific differences for a field across all supported versions.
    
    Args:
        segment_name: Segment name (e.g., "EVN")
        field_index: Field index (1-based)
        
    Returns:
        Dictionary mapping version strings to their specific field definitions
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting all version-specific differences for {segment_name}-{field_index}")
    
    version_definitions = {}
    
    for version in SUPPORTED_VERSIONS:
        field_def = get_version_specific_field_definition(segment_name, field_index, version)
        if field_def:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            version_definitions[version] = field_def
    
    logger.debug(f"[{current_time}] Found version-specific definitions for {len(version_definitions)} versions")
    return version_definitions


def get_version_specific_data_type(
    data_type: str,
    version: str
) -> Optional[Dict[str, any]]:
    """
    Get version-specific data type definition.
    
    Different HL7 versions may have different data type definitions, including:
    - Different component structures
    - Different length constraints
    - Different format requirements
    
    Args:
        data_type: Data type name (e.g., "ST", "TS", "CE", "XCN")
        version: HL7 version (e.g., "2.5")
        
    Returns:
        Dictionary with version-specific data type definition, or None if not found
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting version-specific data type {data_type} for version {version}")
    
    try:
        from dnhealth.dnhealth_hl7v2.profiles import get_profile
        
        profile = get_profile(version)
        data_type_def = profile.get_data_type_definition(data_type)
        
        if data_type_def:
            logger.debug(f"[{current_time}] Found data type definition for {data_type} in version {version}")
            return data_type_def
        else:
            logger.warning(f"[{current_time}] Data type definition not found for {data_type} in version {version}")
            return None
            
    except Exception as e:
        logger.error(f"[{current_time}] Error getting version-specific data type: {e}")
        return None


def get_data_type_version_differences(
    data_type: str,
    version1: str,
    version2: str
) -> Dict[str, any]:
    """
    Get differences in data type definition between two versions.
    
    Args:
        data_type: Data type name (e.g., "ST", "TS", "CE")
        version1: First version
        version2: Second version
        
    Returns:
        Dictionary with differences:
        - "version1_definition": Definition in version1
        - "version2_definition": Definition in version2
        - "differences": List of specific differences
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting data type differences for {data_type} between {version1} and {version2}")
    
    result = {
        "version1_definition": None,
        "version2_definition": None,
        "differences": []
    }
    
    def1 = get_version_specific_data_type(data_type, version1)
    def2 = get_version_specific_data_type(data_type, version2)
    
    result["version1_definition"] = def1
    result["version2_definition"] = def2
    
    if def1 is None and def2 is None:
        result["differences"].append(f"Data type {data_type} not found in either version")
    elif def1 is None:
        result["differences"].append(f"Data type {data_type} not found in {version1}")
    elif def2 is None:
        result["differences"].append(f"Data type {data_type} not found in {version2}")
    else:
        # Compare definitions
        if def1.get("max_length") != def2.get("max_length"):
            result["differences"].append(
                f"max_length changed from {def1.get('max_length')} to {def2.get('max_length')}"
            )
        
        if def1.get("components") != def2.get("components"):
            result["differences"].append("Component structure changed")
        

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        if def1.get("format") != def2.get("format"):
            result["differences"].append(
                f"Format changed from {def1.get('format')} to {def2.get('format')}"
            )
    
    logger.debug(f"[{current_time}] Found {len(result['differences'])} differences for {data_type}")
    return result


def get_version_specific_table_value(
    table_id: str,
    code: str,
    version: str
) -> Optional[str]:
    """
    Get version-specific table value description.
    
    Table codes and descriptions may differ between HL7 versions.
    
    Args:
        table_id: Table identifier (e.g., "0001", "0008")
        code: Code value to look up
        version: HL7 version (e.g., "2.5")
        
    Returns:
        Description string if code exists in table for this version, None otherwise
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting table value for table {table_id}, code {code} in version {version}")
    
    try:
        from dnhealth.dnhealth_hl7v2.profiles import get_profile
        
        profile = get_profile(version)
        description = profile.get_table_value(table_id, code)
        
        if description:
            logger.debug(f"[{current_time}] Found table value for {table_id}/{code} in version {version}")
            return description
        else:
            logger.warning(f"[{current_time}] Table value not found for {table_id}/{code} in version {version}")
            return None
            
    except Exception as e:
        logger.error(f"[{current_time}] Error getting version-specific table value: {e}")
        return None


def validate_table_value_for_version(
    table_id: str,
    code: str,
    version: str
) -> Tuple[bool, Optional[str]]:
    """
    Validate a table code against version-specific table definition.
    
    Args:
        table_id: Table identifier (e.g., "0001", "0008")
        code: Code value to validate
        version: HL7 version (e.g., "2.5")
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if code is valid for this version, False otherwise
        - error_message: None if valid, error description if invalid
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Validating table value {table_id}/{code} for version {version}")
    
    try:
        from dnhealth.dnhealth_hl7v2.profiles import get_profile
        
        profile = get_profile(version)
        is_valid, error_msg = profile.validate_table_value(table_id, code)
        
        if is_valid:
            logger.debug(f"[{current_time}] Table value {table_id}/{code} is valid for version {version}")
        else:
            logger.warning(f"[{current_time}] Table value {table_id}/{code} is invalid for version {version}: {error_msg}")
        
        return is_valid, error_msg
        
    except Exception as e:
        logger.error(f"[{current_time}] Error validating table value: {e}")
        return False, str(e)


def get_table_version_differences(
    table_id: str,
    version1: str,
    version2: str
) -> Dict[str, any]:
    """
    Get differences in table definition between two versions.
    
    Args:
        table_id: Table identifier (e.g., "0001", "0008")
        version1: First version
        version2: Second version
        
    Returns:
        Dictionary with differences:
        - "version1_table": Table definition in version1
        - "version2_table": Table definition in version2
        - "codes_added": List of codes added in version2
        - "codes_removed": List of codes removed in version2
        - "codes_changed": List of codes with changed descriptions
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting table differences for {table_id} between {version1} and {version2}")
    
    result = {
        "version1_table": None,
        "version2_table": None,
        "codes_added": [],
        "codes_removed": [],
        "codes_changed": []
    }
    
    try:
        from dnhealth.dnhealth_hl7v2.profiles import get_profile
        
        profile1 = get_profile(version1)
        profile2 = get_profile(version2)
        
        table1 = profile1.get_table_definition(table_id)
        table2 = profile2.get_table_definition(table_id)
        
        result["version1_table"] = table1
        result["version2_table"] = table2
        
        if table1 is None and table2 is None:
            logger.warning(f"[{current_time}] Table {table_id} not found in either version")
            return result
        elif table1 is None:
            result["codes_added"] = list(table2.keys()) if table2 else []
            logger.debug(f"[{current_time}] Table {table_id} not found in {version1}, all codes are new")
            return result
        elif table2 is None:
            result["codes_removed"] = list(table1.keys()) if table1 else []
            logger.debug(f"[{current_time}] Table {table_id} not found in {version2}, all codes removed")
            return result
        
        # Compare codes
        codes1 = set(table1.keys())
        codes2 = set(table2.keys())
        
        result["codes_added"] = sorted(list(codes2 - codes1))
        result["codes_removed"] = sorted(list(codes1 - codes2))
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        # Find codes with changed descriptions
        common_codes = codes1 & codes2
        for code in common_codes:
            if table1[code] != table2[code]:
                result["codes_changed"].append(code)
        
        logger.debug(
            f"[{current_time}] Found {len(result['codes_added'])} codes added, "
            f"{len(result['codes_removed'])} codes removed, "
            f"{len(result['codes_changed'])} codes changed"
        )
        
    except Exception as e:
        logger.error(f"[{current_time}] Error getting table version differences: {e}")
    
    return result


def get_version_specific_segment_definition(
    segment_name: str,
    version: str
) -> Optional[Dict[str, any]]:
    """
    Get version-specific segment definition with all fields and metadata.
    
    This function retrieves the complete segment definition for a specific version,
    including all field definitions, version-specific overrides, and metadata.
    
    Args:
        segment_name: Segment name (e.g., "EVN", "PID")
        version: HL7 version (e.g., "2.5")
        
    Returns:
        Dictionary with complete segment definition for the version, or None if not found
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting version-specific segment definition for {segment_name} in version {version}")
    
    try:
        from dnhealth.dnhealth_hl7v2.segment_definitions import get_segment_fields
        
        # Get all field definitions for this segment
        fields = get_segment_fields(segment_name, version=version)
        if not fields:
            logger.warning(f"[{current_time}] No field definitions found for segment {segment_name}")
            return None
        
        # Build segment definition dictionary
        segment_def = {
            "segment_name": segment_name,
            "version": version,
            "fields": {},
            "field_count": len(fields),
            "available_in_version": True
        }
        
        # Add each field definition
        for field_index, field_def in fields.items():

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            segment_def["fields"][field_index] = {
                "field_index": field_def.field_index,
                "field_name": field_def.field_name,
                "data_type": field_def.data_type,
                "length": field_def.length,
                "min_length": field_def.min_length,
                "required": field_def.required,
                "optional": field_def.optional,
                "repeating": field_def.repeating,
                "table_binding": field_def.table_binding,
                "description": field_def.description,
            }
        
        logger.debug(f"[{current_time}] Retrieved segment definition for {segment_name} with {len(fields)} fields")
        return segment_def
        
    except Exception as e:
        logger.error(f"[{current_time}] Error getting version-specific segment definition: {e}")
        return None


def get_segment_version_differences(
    segment_name: str,
    version1: str,
    version2: str
) -> Dict[str, any]:
    """
    Get differences in segment definition between two versions.
    
    This function compares segment definitions across versions and identifies:
    - Fields added/removed/changed
    - Data type changes
    - Required/optional status changes
    - Table binding changes
    - Length constraint changes
    
    Args:
        segment_name: Segment name (e.g., "EVN", "PID")
        version1: First version
        version2: Second version
        
    Returns:
        Dictionary with differences:
        - "version1_definition": Segment definition in version1
        - "version2_definition": Segment definition in version2
        - "fields_added": List of field indices added in version2
        - "fields_removed": List of field indices removed in version2
        - "fields_changed": List of field indices with changes
        - "data_type_changes": Dict mapping field indices to (old_type, new_type)
        - "required_status_changes": Dict mapping field indices to (old_status, new_status)
        - "table_binding_changes": Dict mapping field indices to (old_table, new_table)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Getting segment differences for {segment_name} between {version1} and {version2}")
    
    result = {
        "version1_definition": None,
        "version2_definition": None,
        "fields_added": [],
        "fields_removed": [],
        "fields_changed": [],
        "data_type_changes": {},
        "required_status_changes": {},
        "table_binding_changes": {},
    }
    
    def1 = get_version_specific_segment_definition(segment_name, version1)
    def2 = get_version_specific_segment_definition(segment_name, version2)
    
    result["version1_definition"] = def1
    result["version2_definition"] = def2
    
    if def1 is None and def2 is None:
        logger.warning(f"[{current_time}] Segment {segment_name} not found in either version")
        return result
    elif def1 is None:
        # All fields are new in version2
        if def2 and "fields" in def2:
            result["fields_added"] = sorted(list(def2["fields"].keys()))
        logger.debug(f"[{current_time}] Segment {segment_name} not found in {version1}, all fields are new")
        return result
    elif def2 is None:
        # All fields removed in version2
        if def1 and "fields" in def1:
            result["fields_removed"] = sorted(list(def1["fields"].keys()))
        logger.debug(f"[{current_time}] Segment {segment_name} not found in {version2}, all fields removed")
        return result
    
    # Compare fields
    fields1 = set(def1.get("fields", {}).keys()) if def1 else set()
    fields2 = set(def2.get("fields", {}).keys()) if def2 else set()
    
    result["fields_added"] = sorted(list(fields2 - fields1))
    result["fields_removed"] = sorted(list(fields1 - fields2))
    
    # Compare common fields
    common_fields = fields1 & fields2
    for field_idx in common_fields:
        field1 = def1["fields"][field_idx]
        field2 = def2["fields"][field_idx]
        
        changed = False
        
        # Check data type changes
        if field1.get("data_type") != field2.get("data_type"):
            result["data_type_changes"][field_idx] = (
                field1.get("data_type"),
                field2.get("data_type")
            )
            changed = True
        
        # Check required status changes
        if field1.get("required") != field2.get("required"):
            result["required_status_changes"][field_idx] = (
                field1.get("required"),
                field2.get("required")
            )
            changed = True
        
        # Check table binding changes
        if field1.get("table_binding") != field2.get("table_binding"):
            result["table_binding_changes"][field_idx] = (
                field1.get("table_binding"),
                field2.get("table_binding")
            )
            changed = True
        
        # Check length changes
        if field1.get("length") != field2.get("length"):
            changed = True
        
        if changed:
            result["fields_changed"].append(field_idx)
    
    logger.debug(
        f"[{current_time}] Found {len(result['fields_added'])} fields added, "
        f"{len(result['fields_removed'])} fields removed, "
        f"{len(result['fields_changed'])} fields changed"
    )
    return result


def create_version_migration_plan(
    source_version: str,
    target_version: str,
    segment_name: Optional[str] = None
) -> Dict[str, any]:
    """
    Create a migration plan for converting messages from source_version to target_version.
    
    This function analyzes the differences between versions and creates a detailed
    migration plan including:
    - Segments that need to be added/removed/modified
    - Fields that need to be added/removed/modified
    - Data type conversions needed
    - Table value mappings needed
    
    Args:
        source_version: Source HL7 version
        target_version: Target HL7 version
        segment_name: Optional segment name to create plan for specific segment
    
    Returns:
        Dictionary with migration plan:
        - "segments_to_add": List of segments to add
        - "segments_to_remove": List of segments to remove
        - "segments_to_modify": List of segments that need modification
        - "fields_to_add": Dict mapping segment names to lists of field indices
        - "fields_to_remove": Dict mapping segment names to lists of field indices
        - "data_type_conversions": List of data type conversions needed
        - "table_mappings": Dict mapping table IDs to code mappings
        - "warnings": List of warnings about potential data loss or issues
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Creating migration plan from {source_version} to {target_version}")
    
    plan = {
        "segments_to_add": [],
        "segments_to_remove": [],
        "segments_to_modify": [],
        "fields_to_add": {},
        "fields_to_remove": {},
        "data_type_conversions": [],
        "table_mappings": {},
        "warnings": []
    }
    
    if not is_version_supported(source_version) or not is_version_supported(target_version):
        plan["warnings"].append(f"One or both versions not supported: {source_version}, {target_version}")
        logger.warning(f"[{current_time}] One or both versions not supported")
        return plan
    
    # Get version differences
    differences = get_version_differences(source_version, target_version)
    plan["segments_to_add"] = differences["segments_added"]
    plan["segments_to_remove"] = differences["segments_removed"]
    
    # If specific segment requested, get detailed differences
    if segment_name:
        segment_diffs = get_segment_version_differences(segment_name, source_version, target_version)
        if segment_diffs["fields_added"]:
            plan["fields_to_add"][segment_name] = segment_diffs["fields_added"]
        if segment_diffs["fields_removed"]:
            plan["fields_to_remove"][segment_name] = segment_diffs["fields_removed"]
        if segment_diffs["data_type_changes"]:
            plan["data_type_conversions"].append({
                "segment": segment_name,
                "changes": segment_diffs["data_type_changes"]
            })
        if segment_diffs["fields_changed"]:
            plan["segments_to_modify"].append(segment_name)
    
    # Check compatibility
    is_compatible, warnings = validate_version_compatibility(source_version, target_version, segment_name)
    plan["warnings"].extend(warnings)
    
    if not is_compatible:
        plan["warnings"].append("Version compatibility check failed - migration may result in data loss")
    
    logger.info(f"[{current_time}] Migration plan created with {len(plan['segments_to_add'])} segments to add, "
                f"{len(plan['segments_to_remove'])} segments to remove")
    
    return plan
