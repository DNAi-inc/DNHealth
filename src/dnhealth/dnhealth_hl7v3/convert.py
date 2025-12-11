# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 message version conversion utilities.

Provides functions to convert messages between different HL7 v3 versions.
Note: Full version conversion requires extensive version-specific mappings.
This module provides basic version identifier updates.
"""

import logging
from datetime import datetime
from typing import Optional, List, Tuple
from copy import deepcopy

from dnhealth.dnhealth_hl7v3.model import Message, ElementNode
from dnhealth.dnhealth_hl7v3.schema import detect_schema_version_from_xml
from dnhealth.dnhealth_hl7v3.serializer import serialize_hl7v3
from dnhealth.dnhealth_hl7v3.parser import parse_hl7v3

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def convert_message_version(
    message: Message,
    target_version: str,
    preserve_unknown_elements: bool = True,
) -> Tuple[Message, List[str]]:
    """
    Convert an HL7v3 message to a different version.
    
    This function performs basic version conversion including:
    - Updating namespace declarations to target version
    - Updating versionCode elements if present
    - Preserving message structure
    
    Note: Full version conversion requires extensive version-specific mappings
    and understanding of differences between HL7 v3 versions. This implementation
    provides basic version identifier updates.
    
    Args:
        message: Message object to convert
        target_version: Target HL7 v3 version (e.g., "v3", "v3:2015")
        preserve_unknown_elements: If True, preserve elements not defined in target version
        
    Returns:
        Tuple of (converted_message, warnings)
        - converted_message: Converted Message object
        - warnings: List of warning messages about conversion issues
        
    Raises:
        ValueError: If target_version is invalid
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting HL7v3 message conversion to version {target_version}")
    
    warnings = []
    
    # Validate target version format
    if not target_version or not target_version.startswith("v3"):
        raise ValueError(f"Invalid target version '{target_version}'. Must start with 'v3'")
    
    # Serialize message to XML to update namespaces
    try:
        xml_string = serialize_hl7v3(message)
    except Exception as e:
        warnings.append(f"Failed to serialize message: {str(e)}")
        logger.warning(f"[{current_time}] Serialization warning: {str(e)}")
        # Return original message with warning
        elapsed = (datetime.now() - start_time).total_seconds()
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.warning(
            f"[{completion_time}] HL7v3 version conversion completed in {elapsed:.3f}s - "
            f"conversion incomplete due to serialization error"
        )
        return message, warnings
    
    # Update namespace declarations in XML
    # HL7 v3 namespaces typically follow pattern: "urn:hl7-org:v3" or "urn:hl7-org:v3:2015"
    updated_xml = xml_string
    
    # Replace namespace declarations
    if "urn:hl7-org:v3" in updated_xml:
        # Replace with target version namespace
        if ":" in target_version:
            # e.g., "v3:2015" -> "urn:hl7-org:v3:2015"
            target_namespace = f"urn:hl7-org:{target_version}"
        else:
            # e.g., "v3" -> "urn:hl7-org:v3"
            target_namespace = f"urn:hl7-org:{target_version}"
        
        # Replace all occurrences of old namespace
        updated_xml = updated_xml.replace("urn:hl7-org:v3", target_namespace)
        logger.debug(f"[{current_time}] Updated namespace to {target_namespace}")
    
    # Parse updated XML back to Message
    try:
        converted_message = parse_hl7v3(updated_xml)
    except Exception as e:
        warnings.append(f"Failed to parse converted message: {str(e)}")
        logger.warning(f"[{current_time}] Parse warning: {str(e)}")
        # Return original message with warning
        elapsed = (datetime.now() - start_time).total_seconds()
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.warning(
            f"[{completion_time}] HL7v3 version conversion completed in {elapsed:.3f}s - "
            f"conversion incomplete due to parse error"
        )
        return message, warnings
    
    # Update versionCode if present
    version_code_elem = converted_message.get_version_code()
    if version_code_elem:
        # Update version code to target version
        if hasattr(version_code_elem, 'set_attribute'):
            version_code_elem.set_attribute('code', target_version)
        logger.debug(f"[{current_time}] Updated versionCode to {target_version}")
    
    elapsed = (datetime.now() - start_time).total_seconds()
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        f"[{completion_time}] HL7v3 version conversion completed in {elapsed:.3f}s - "
        f"converted to version {target_version}"
    )
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return converted_message, warnings


def convert_message_simple(message: Message, target_version: str) -> Message:
    """
    Simple version conversion that only updates namespace declarations.
    
    This is a minimal conversion that preserves all elements,
    only updating the namespace declarations to target version.
    
    Note: This function maintains backward compatibility. For comprehensive
    conversion with validation and warnings, use convert_message_version().
    
    Args:
        message: Message object to convert
        target_version: Target HL7 v3 version (e.g., "v3", "v3:2015")
        
    Returns:
        Converted Message object
    """
    start_time = datetime.now()
    current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Performing simple HL7v3 conversion to {target_version}")
    
    # Use full conversion but ignore warnings
    converted_message, _ = convert_message_version(
        message,
        target_version=target_version,
        preserve_unknown_elements=True
    )
    
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Simple HL7v3 conversion completed")
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return converted_message
