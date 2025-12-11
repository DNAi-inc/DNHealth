# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message version conversion utilities.

Provides functions to convert messages between different HL7 v2.x versions.
"""

import logging
from datetime import datetime
from typing import List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import Component, Field, Message, Segment, Subcomponent
from dnhealth.dnhealth_hl7v2.profiles import get_profile
from dnhealth.dnhealth_hl7v2.version_utils import (
    create_version_migration_plan,
    get_data_type_version_differences,
    get_table_version_differences,
    get_version_specific_data_type,
    get_version_specific_field_definition,
    is_version_supported,
    validate_table_value_for_version,
)

logger = logging.getLogger(__name__)


def convert_message_version(
    message: Message,
    target_version: str,
    preserve_unknown_segments: bool = True,    validate_table_values: bool = True,
) -> Tuple[Message, List[str]]:
    """
    Convert an HL7v2 message to a different version.

    This function performs comprehensive version conversion including:
    - Updating MSH-12 (Version ID)
    - Converting segments based on version-specific definitions
    - Converting fields based on version-specific field definitions
    - Validating table values against target version tables
    - Handling data type differences between versions

    Args:
        message: Message object to convert
        target_version: Target HL7 version (e.g., "2.5", "2.6")
        preserve_unknown_segments: If True, preserve segments not defined in target version
        validate_table_values: If True, validate table values against target version tables

    Returns:
        Tuple of (converted_message, warnings)
        - converted_message: Converted Message object
        - warnings: List of warning messages about conversion issues

    Raises:
        ValueError: If target_version is invalid or message version is not set
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting message conversion from {message.version} to {target_version}")
    
    warnings = []
    
    if not message.version:
        raise ValueError("Source message version must be set for conversion")
    
    if not is_version_supported(target_version):
        raise ValueError(f"Target version {target_version} is not supported")
    
    if not is_version_supported(message.version):
        warnings.append(f"Source version {message.version} is not fully supported - conversion may be incomplete")
        logger.warning(f"[{current_time}] Source version {message.version} not fully supported")
    
    # Create migration plan
    migration_plan = create_version_migration_plan(message.version, target_version)
    warnings.extend(migration_plan.get("warnings", []))
    
    # Get source and target profiles
    source_profile = get_profile(message.version)
    target_profile = get_profile(target_version)

    # Create new message with target version
    converted_segments = []
    encoding_chars = message.encoding_chars

    for segment in message.segments:
        if segment.name == "MSH":
            # Convert MSH segment - update version field
            msh_fields = []
            for field_repetitions in segment._field_repetitions:
                msh_fields.append(field_repetitions)

            # Update MSH-12 (Version ID) to target version
            if len(msh_fields) >= 12:
                # Replace MSH-12 with target version
                version_field = Field([Component([Subcomponent(target_version)])])
                msh_fields[11] = [version_field]  # 0-based index for field 12
            elif len(msh_fields) < 12:
                # Add missing fields up to MSH-12
                while len(msh_fields) < 12:
                    msh_fields.append([Field()])
                msh_fields[11] = [Field([Component([Subcomponent(target_version)])])]

            converted_msh = Segment("MSH", field_repetitions=msh_fields)
            converted_segments.append(converted_msh)
        else:
            # Check if segment exists in target version
            target_seg_def = target_profile.get_segment_definition(segment.name)

            if target_seg_def or preserve_unknown_segments:
                # Convert segment fields based on target profile
                converted_segment, segment_warnings = _convert_segment(
                    segment, source_profile, target_profile, message.version, target_version, validate_table_values
                )
                converted_segments.append(converted_segment)
                warnings.extend(segment_warnings)
            elif segment.name in migration_plan.get("segments_to_remove", []):
                warnings.append(f"Segment {segment.name} removed during conversion (not available in {target_version})")
                logger.warning(f"[{current_time}] Segment {segment.name} removed during conversion")
            # If segment doesn't exist in target and preserve_unknown_segments is False, skip it

    converted_message = Message(
        segments=converted_segments,
        encoding_chars=encoding_chars,
        version=target_version,
    )
    
    logger.info(f"[{current_time}] Message conversion completed with {len(warnings)} warning(s)")
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {completion_time}")
    return converted_message, warnings


def _convert_segment(
    segment: Segment,
    source_profile,
    target_profile,
    source_version: str,
    target_version: str,
    validate_table_values: bool = True,
) -> Tuple[Segment, List[str]]:
    """
    Convert a segment from source version to target version.

    This function performs comprehensive segment conversion including:
    - Checking if fields exist in target version
    - Converting data types if needed
    - Validating table values against target version tables
    - Handling version-specific field differences

    Args:
        segment: Segment to convert
        source_profile: Source version profile
        target_profile: Target version profile
        source_version: Source HL7 version string
        target_version: Target HL7 version string
        validate_table_values: If True, validate table values against target version

    Returns:
        Tuple of (converted_segment, warnings)
        - converted_segment: Converted Segment
        - warnings: List of warning messages
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Converting segment {segment.name} from {source_version} to {target_version}")
    
    warnings = []
    converted_fields = []

    for field_repetitions in segment._field_repetitions:
        # Get field index (1-based)
        field_index = len(converted_fields) + 1

        # Get version-specific field definitions
        source_field_def = get_version_specific_field_definition(segment.name, field_index, source_version)
        target_field_def = get_version_specific_field_definition(segment.name, field_index, target_version)

        if target_field_def:
            # Field exists in target version - check for differences
            if source_field_def:
                # Check for data type changes
                if source_field_def.get("data_type") != target_field_def.get("data_type"):
                    warnings.append(
                        f"Segment {segment.name} field {field_index}: data type changed from "
                        f"{source_field_def.get('data_type')} to {target_field_def.get('data_type')}"
                    )
                    logger.warning(
                        f"[{current_time}] Data type change detected for {segment.name}-{field_index}: "
                        f"{source_field_def.get('data_type')} -> {target_field_def.get('data_type')}"
                    )
                
                # Check for table binding changes
                source_table = source_field_def.get("table_binding")
                target_table = target_field_def.get("table_binding")
                if source_table != target_table:
                    warnings.append(
                        f"Segment {segment.name} field {field_index}: table binding changed from "
                        f"{source_table} to {target_table}"
                    )
                    logger.warning(
                        f"[{current_time}] Table binding change detected for {segment.name}-{field_index}: "
                        f"{source_table} -> {target_table}"
                    )
                    
                    # Validate table values if requested
                    if validate_table_values and target_table and field_repetitions:
                        for field_rep in field_repetitions:
                            if field_rep and field_rep.components:
                                for component in field_rep.components:
                                    if component and component.subcomponents:
                                        code_value = component.subcomponents[0].value() if component.subcomponents else None
                                        if code_value:
                                            is_valid, error_msg = validate_table_value_for_version(
                                                target_table, code_value, target_version
                                            )
                                            if not is_valid:
                                                warnings.append(
                                                    f"Segment {segment.name} field {field_index}: "
                                                    f"table value {code_value} invalid for table {target_table} "
                                                    f"in version {target_version}: {error_msg}"
                                                )
                                                logger.warning(
                                                    f"[{current_time}] Invalid table value {code_value} "
                                                    f"for {segment.name}-{field_index} in version {target_version}"
                                                )
            
            # Preserve field (with potential data type conversion handled by validation)
            converted_fields.append(field_repetitions)
        elif source_field_def:
            # Field exists in source but not in target
            warnings.append(
                f"Segment {segment.name} field {field_index} removed during conversion "
                f"(not available in {target_version})"
            )
            logger.warning(
                f"[{current_time}] Field {segment.name}-{field_index} removed during conversion"
            )
            # Skip this field
        else:
            # Field doesn't exist in either version - preserve it
            converted_fields.append(field_repetitions)

    converted_segment = Segment(segment.name, field_repetitions=converted_fields)
    logger.debug(f"[{current_time}] Segment {segment.name} conversion completed with {len(warnings)} warning(s)")
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"Current Time at End of Operations: {completion_time}")
    return converted_segment, warnings


def convert_message_simple(message: Message, target_version: str) -> Message:
    """
    Simple version conversion that only updates MSH-12.

    This is a minimal conversion that preserves all segments and fields,
    only updating the version identifier in MSH-12.
    
    Note: This function maintains backward compatibility. For comprehensive
    conversion with validation and warnings, use convert_message_version().

    Args:
        message: Message object to convert
        target_version: Target HL7 version (e.g., "2.5", "2.6")

    Returns:
        Converted Message object
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Performing simple conversion to {target_version}")
    
    # Create a copy of the message
    converted_segments = []

    for segment in message.segments:
        if segment.name == "MSH":
            # Update MSH-12 with target version
            msh_fields = []
            for field_repetitions in segment._field_repetitions:
                msh_fields.append(field_repetitions)

            # Ensure MSH-12 exists
            while len(msh_fields) < 12:
                msh_fields.append([Field()])

            # Update MSH-12
            version_field = Field([Component([Subcomponent(target_version)])])
            msh_fields[11] = [version_field]  # 0-based index for field 12

            converted_msh = Segment("MSH", field_repetitions=msh_fields)
            converted_segments.append(converted_msh)
        else:
            # Preserve segment as-is
            converted_segments.append(segment)

    converted_message = Message(
        segments=converted_segments,
        encoding_chars=message.encoding_chars,
        version=target_version,
    )
    
    logger.debug(f"[{current_time}] Simple conversion completed")
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"Current Time at End of Operations: {completion_time}")
    return converted_message

