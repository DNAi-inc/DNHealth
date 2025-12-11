# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message type validation.

Validates messages against HL7 v2.x message type specifications,
checking required segments, segment order, and cardinality.
"""

import logging
from datetime import datetime
from typing import List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import Message

# Get logger with timestamp formatting
logger = logging.getLogger(__name__)


def get_message_type(message: Message) -> Optional[str]:
    """
    Extract message type from MSH-9 field.
    
    Returns message type in format "MESSAGE_CODE^TRIGGER_EVENT" or None if not found.
    
    Args:
        message: HL7 v2 message
        
    Returns:
        Message type string (e.g., "ADT^A01") or None
    """
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        return None
    
    msh = msh_segments[0]
    if len(msh.fields) < 8:
        return None
    
    # MSH-9 is Message Type, but MSH-1 (field separator) is not stored as a regular field
    # so MSH-9 is at index 8 in the fields array (0-based indexing in field() method uses 1-based)
    msg_type_field = msh.field(8)
    if not msg_type_field or not msg_type_field.components:
        return None
    
    # MSH-9 format: MESSAGE_CODE^TRIGGER_EVENT^MESSAGE_STRUCTURE
    msg_code = msg_type_field.component(1).value() if len(msg_type_field.components) > 0 else ""
    trigger_event = msg_type_field.component(2).value() if len(msg_type_field.components) > 1 else ""
    
    if not msg_code:
        return None
    
    if trigger_event:
        return f"{msg_code}^{trigger_event}"
    return msg_code



# Current Time at End of Operations: 2025-12-11 08:12:03

def validate_adt_a01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A01 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A01 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A01 validation failed: cannot determine message type")
    elif msg_type != "ADT^A01":
        errors.append(f"ADT^A01 validation: expected message type ADT^A01, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A01 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a02(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A02 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A02 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A02 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A02 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A02 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A02 validation failed: cannot determine message type")
    elif msg_type != "ADT^A02":
        errors.append(f"ADT^A02 validation: expected message type ADT^A02, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A02 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A02 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a03(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A03 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A03 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A03 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A03 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A03 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A03 validation failed: cannot determine message type")
    elif msg_type != "ADT^A03":
        errors.append(f"ADT^A03 validation: expected message type ADT^A03, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A03 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A03 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a04(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A04 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A04 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A04 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A04 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A04 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A04 validation failed: cannot determine message type")
    elif msg_type != "ADT^A04":
        errors.append(f"ADT^A04 validation: expected message type ADT^A04, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A04 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A04 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a05(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A05 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A05 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A05 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A05 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A05 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A05 validation failed: cannot determine message type")
    elif msg_type != "ADT^A05":
        errors.append(f"ADT^A05 validation: expected message type ADT^A05, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A05 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A05 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a06(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A06 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A06 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A06 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A06 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A06 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A06 validation failed: cannot determine message type")
    elif msg_type != "ADT^A06":
        errors.append(f"ADT^A06 validation: expected message type ADT^A06, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A06 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A06 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a07(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A07 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A07 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A07 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A07 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A07 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A07 validation failed: cannot determine message type")
    elif msg_type != "ADT^A07":
        errors.append(f"ADT^A07 validation: expected message type ADT^A07, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A07 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A07 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a08(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A08 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A08 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A08 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A08 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A08 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A08 validation failed: cannot determine message type")
    elif msg_type != "ADT^A08":
        errors.append(f"ADT^A08 validation: expected message type ADT^A08, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A08 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A08 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a09(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A09 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A09 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A09 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A09 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A09 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A09 validation failed: cannot determine message type")
    elif msg_type != "ADT^A09":
        errors.append(f"ADT^A09 validation: expected message type ADT^A09, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A09 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A09 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a10(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A10 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A10 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A10 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A10 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A10 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A10 validation failed: cannot determine message type")
    elif msg_type != "ADT^A10":
        errors.append(f"ADT^A10 validation: expected message type ADT^A10, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A10 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A10 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a11(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A11 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A11 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A11 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A11 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A11 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A11 validation failed: cannot determine message type")
    elif msg_type != "ADT^A11":
        errors.append(f"ADT^A11 validation: expected message type ADT^A11, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A11 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A11 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a12(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A12 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A12 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A12 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A12 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A12 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A12 validation failed: cannot determine message type")
    elif msg_type != "ADT^A12":
        errors.append(f"ADT^A12 validation: expected message type ADT^A12, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A12 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A12 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a13(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A13 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A13 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A13 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A13 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A13 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A13 validation failed: cannot determine message type")
    elif msg_type != "ADT^A13":
        errors.append(f"ADT^A13 validation: expected message type ADT^A13, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A13 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A13 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a14(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A14 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A14 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A14 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A14 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A14 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A14 validation failed: cannot determine message type")
    elif msg_type != "ADT^A14":
        errors.append(f"ADT^A14 validation: expected message type ADT^A14, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A14 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A14 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a15(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A15 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A15 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A15 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A15 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A15 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A15 validation failed: cannot determine message type")
    elif msg_type != "ADT^A15":
        errors.append(f"ADT^A15 validation: expected message type ADT^A15, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A15 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A15 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a16(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A16 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A16 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A16 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A16 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A16 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A16 validation failed: cannot determine message type")
    elif msg_type != "ADT^A16":
        errors.append(f"ADT^A16 validation: expected message type ADT^A16, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A16 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A16 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a17(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A17 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A17 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A17 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A17 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A17 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A17 validation failed: cannot determine message type")
    elif msg_type != "ADT^A17":
        errors.append(f"ADT^A17 validation: expected message type ADT^A17, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A17 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A17 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a18(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A18 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A18 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A18 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A18 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A18 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A18 validation failed: cannot determine message type")
    elif msg_type != "ADT^A18":
        errors.append(f"ADT^A18 validation: expected message type ADT^A18, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A18 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A18 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a20(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A20 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A20 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A20 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A20 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A20 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A20 validation failed: cannot determine message type")
    elif msg_type != "ADT^A20":
        errors.append(f"ADT^A20 validation: expected message type ADT^A20, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A20 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A20 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a21(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A21 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A21 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A21 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A21 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A21 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A21 validation failed: cannot determine message type")
    elif msg_type != "ADT^A21":
        errors.append(f"ADT^A21 validation: expected message type ADT^A21, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A21 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A21 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a22(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A22 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A22 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A22 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A22 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A22 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A22 validation failed: cannot determine message type")
    elif msg_type != "ADT^A22":
        errors.append(f"ADT^A22 validation: expected message type ADT^A22, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A22 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A22 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a23(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A23 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A23 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A23 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A23 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A23 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A23 validation failed: cannot determine message type")
    elif msg_type != "ADT^A23":
        errors.append(f"ADT^A23 validation: expected message type ADT^A23, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A23 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A23 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a24(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A24 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A24 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A24 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A24 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A24 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A24 validation failed: cannot determine message type")
    elif msg_type != "ADT^A24":
        errors.append(f"ADT^A24 validation: expected message type ADT^A24, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A24 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A24 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a25(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A25 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A25 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A25 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A25 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A25 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A25 validation failed: cannot determine message type")
    elif msg_type != "ADT^A25":
        errors.append(f"ADT^A25 validation: expected message type ADT^A25, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A25 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A25 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a26(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A26 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A26 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A26 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A26 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A26 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A26 validation failed: cannot determine message type")
    elif msg_type != "ADT^A26":
        errors.append(f"ADT^A26 validation: expected message type ADT^A26, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A26 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A26 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a27(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A27 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A27 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A27 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A27 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A27 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A27 validation failed: cannot determine message type")
    elif msg_type != "ADT^A27":
        errors.append(f"ADT^A27 validation: expected message type ADT^A27, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A27 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A27 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a28(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A28 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A28 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A28 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A28 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A28 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A28 validation failed: cannot determine message type")
    elif msg_type != "ADT^A28":
        errors.append(f"ADT^A28 validation: expected message type ADT^A28, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A28 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A28 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a29(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A29 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A29 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A29 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A29 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A29 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A29 validation failed: cannot determine message type")
    elif msg_type != "ADT^A29":
        errors.append(f"ADT^A29 validation: expected message type ADT^A29, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A29 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A29 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a30(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A30 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A30 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A30 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A30 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A30 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A30 validation failed: cannot determine message type")
    elif msg_type != "ADT^A30":
        errors.append(f"ADT^A30 validation: expected message type ADT^A30, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A30 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A30 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a31(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A31 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A31 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A31 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A31 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A31 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A31 validation failed: cannot determine message type")
    elif msg_type != "ADT^A31":
        errors.append(f"ADT^A31 validation: expected message type ADT^A31, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A31 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A31 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a32(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A32 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A32 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A32 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A32 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A32 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A32 validation failed: cannot determine message type")
    elif msg_type != "ADT^A32":
        errors.append(f"ADT^A32 validation: expected message type ADT^A32, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A32 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A32 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a33(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A33 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A33 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A33 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A33 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A33 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A33 validation failed: cannot determine message type")
    elif msg_type != "ADT^A33":
        errors.append(f"ADT^A33 validation: expected message type ADT^A33, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A33 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A33 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a34(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A34 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A34 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A34 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A34 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A34 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A34 validation failed: cannot determine message type")
    elif msg_type != "ADT^A34":
        errors.append(f"ADT^A34 validation: expected message type ADT^A34, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A34 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A34 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a35(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A35 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A35 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A35 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A35 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A35 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A35 validation failed: cannot determine message type")
    elif msg_type != "ADT^A35":
        errors.append(f"ADT^A35 validation: expected message type ADT^A35, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A35 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A35 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a36(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A36 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A36 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A36 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A36 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A36 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A36 validation failed: cannot determine message type")
    elif msg_type != "ADT^A36":
        errors.append(f"ADT^A36 validation: expected message type ADT^A36, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A36 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A36 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a37(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A37 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A37 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A37 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A37 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A37 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A37 validation failed: cannot determine message type")
    elif msg_type != "ADT^A37":
        errors.append(f"ADT^A37 validation: expected message type ADT^A37, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A37 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A37 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a38(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A38 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A38 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A38 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A38 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A38 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A38 validation failed: cannot determine message type")
    elif msg_type != "ADT^A38":
        errors.append(f"ADT^A38 validation: expected message type ADT^A38, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A38 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A38 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a39(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A39 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A39 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A39 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A39 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A39 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A39 validation failed: cannot determine message type")
    elif msg_type != "ADT^A39":
        errors.append(f"ADT^A39 validation: expected message type ADT^A39, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A39 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A39 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a40(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A40 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A40 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A40 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A40 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A40 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A40 validation failed: cannot determine message type")
    elif msg_type != "ADT^A40":
        errors.append(f"ADT^A40 validation: expected message type ADT^A40, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A40 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A40 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a41(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A41 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A41 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A41 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A41 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A41 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A41 validation failed: cannot determine message type")
    elif msg_type != "ADT^A41":
        errors.append(f"ADT^A41 validation: expected message type ADT^A41, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A41 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A41 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a42(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A42 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A42 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A42 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A42 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A42 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A42 validation failed: cannot determine message type")
    elif msg_type != "ADT^A42":
        errors.append(f"ADT^A42 validation: expected message type ADT^A42, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A42 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A42 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a43(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A43 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A43 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A43 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A43 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A43 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A43 validation failed: cannot determine message type")
    elif msg_type != "ADT^A43":
        errors.append(f"ADT^A43 validation: expected message type ADT^A43, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A43 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A43 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a44(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A44 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A44 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A44 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A44 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A44 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A44 validation failed: cannot determine message type")
    elif msg_type != "ADT^A44":
        errors.append(f"ADT^A44 validation: expected message type ADT^A44, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A44 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A44 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a45(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A45 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A45 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A45 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A45 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A45 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A45 validation failed: cannot determine message type")
    elif msg_type != "ADT^A45":
        errors.append(f"ADT^A45 validation: expected message type ADT^A45, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A45 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A45 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a46(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A46 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A46 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A46 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A46 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A46 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A46 validation failed: cannot determine message type")
    elif msg_type != "ADT^A46":
        errors.append(f"ADT^A46 validation: expected message type ADT^A46, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A46 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A46 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a47(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A47 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A47 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A47 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A47 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A47 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A47 validation failed: cannot determine message type")
    elif msg_type != "ADT^A47":
        errors.append(f"ADT^A47 validation: expected message type ADT^A47, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A47 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A47 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a48(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A48 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A48 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A48 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A48 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A48 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A48 validation failed: cannot determine message type")
    elif msg_type != "ADT^A48":
        errors.append(f"ADT^A48 validation: expected message type ADT^A48, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A48 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A48 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a49(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A49 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A49 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A49 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A49 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A49 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A49 validation failed: cannot determine message type")
    elif msg_type != "ADT^A49":
        errors.append(f"ADT^A49 validation: expected message type ADT^A49, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A49 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A49 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a50(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A50 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A50 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A50 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A50 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A50 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A50 validation failed: cannot determine message type")
    elif msg_type != "ADT^A50":
        errors.append(f"ADT^A50 validation: expected message type ADT^A50, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A50 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A50 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors

def validate_adt_a51(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A51 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A51 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A51 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A51 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A51 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A51 validation failed: cannot determine message type")
    elif msg_type != "ADT^A51":
        errors.append(f"ADT^A51 validation: expected message type ADT^A51, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A51 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A51 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a52(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A52 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A52 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A52 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A52 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A52 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A52 validation failed: cannot determine message type")
    elif msg_type != "ADT^A52":
        errors.append(f"ADT^A52 validation: expected message type ADT^A52, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A52 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A52 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a53(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A53 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A53 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A53 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A53 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A53 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A53 validation failed: cannot determine message type")
    elif msg_type != "ADT^A53":
        errors.append(f"ADT^A53 validation: expected message type ADT^A53, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A53 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A53 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a54(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A54 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A54 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A54 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A54 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A54 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A54 validation failed: cannot determine message type")
    elif msg_type != "ADT^A54":
        errors.append(f"ADT^A54 validation: expected message type ADT^A54, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A54 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A54 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a55(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A55 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A55 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A55 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A55 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A55 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A55 validation failed: cannot determine message type")
    elif msg_type != "ADT^A55":
        errors.append(f"ADT^A55 validation: expected message type ADT^A55, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A55 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A55 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a60(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A60 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A60 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A60 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A60 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A60 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A60 validation failed: cannot determine message type")
    elif msg_type != "ADT^A60":
        errors.append(f"ADT^A60 validation: expected message type ADT^A60, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A60 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A60 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a61(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A61 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A61 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A61 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A61 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A61 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A61 validation failed: cannot determine message type")
    elif msg_type != "ADT^A61":
        errors.append(f"ADT^A61 validation: expected message type ADT^A61, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A61 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A61 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_adt_a62(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ADT^A62 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT^A62 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ADT^A62 message missing required MSH segment")
        logger.error(f"[{current_time}] ADT^A62 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ADT^A62 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ADT^A62 validation failed: cannot determine message type")
    elif msg_type != "ADT^A62":
        errors.append(f"ADT^A62 validation: expected message type ADT^A62, got {msg_type}")
        logger.warning(f"[{current_time}] ADT^A62 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ADT^A62 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bar_p01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BAR^P01 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BAR^P01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BAR^P01 message missing required MSH segment")
        logger.error(f"[{current_time}] BAR^P01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BAR^P01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BAR^P01 validation failed: cannot determine message type")
    elif msg_type != "BAR^P01":
        errors.append(f"BAR^P01 validation: expected message type BAR^P01, got {msg_type}")
        logger.warning(f"[{current_time}] BAR^P01 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BAR^P01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bar_p02(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BAR^P02 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BAR^P02 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BAR^P02 message missing required MSH segment")
        logger.error(f"[{current_time}] BAR^P02 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BAR^P02 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BAR^P02 validation failed: cannot determine message type")
    elif msg_type != "BAR^P02":
        errors.append(f"BAR^P02 validation: expected message type BAR^P02, got {msg_type}")
        logger.warning(f"[{current_time}] BAR^P02 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BAR^P02 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bar_p05(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BAR^P05 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BAR^P05 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BAR^P05 message missing required MSH segment")
        logger.error(f"[{current_time}] BAR^P05 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BAR^P05 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BAR^P05 validation failed: cannot determine message type")
    elif msg_type != "BAR^P05":
        errors.append(f"BAR^P05 validation: expected message type BAR^P05, got {msg_type}")
        logger.warning(f"[{current_time}] BAR^P05 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BAR^P05 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bar_p06(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BAR^P06 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BAR^P06 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BAR^P06 message missing required MSH segment")
        logger.error(f"[{current_time}] BAR^P06 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BAR^P06 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BAR^P06 validation failed: cannot determine message type")
    elif msg_type != "BAR^P06":
        errors.append(f"BAR^P06 validation: expected message type BAR^P06, got {msg_type}")
        logger.warning(f"[{current_time}] BAR^P06 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BAR^P06 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bar_p10(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BAR^P10 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BAR^P10 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BAR^P10 message missing required MSH segment")
        logger.error(f"[{current_time}] BAR^P10 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BAR^P10 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BAR^P10 validation failed: cannot determine message type")
    elif msg_type != "BAR^P10":
        errors.append(f"BAR^P10 validation: expected message type BAR^P10, got {msg_type}")
        logger.warning(f"[{current_time}] BAR^P10 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BAR^P10 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bar_p12(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BAR^P12 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BAR^P12 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BAR^P12 message missing required MSH segment")
        logger.error(f"[{current_time}] BAR^P12 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BAR^P12 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BAR^P12 validation failed: cannot determine message type")
    elif msg_type != "BAR^P12":
        errors.append(f"BAR^P12 validation: expected message type BAR^P12, got {msg_type}")
        logger.warning(f"[{current_time}] BAR^P12 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BAR^P12 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bps_o29(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BPS^O29 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BPS^O29 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BPS^O29 message missing required MSH segment")
        logger.error(f"[{current_time}] BPS^O29 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BPS^O29 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BPS^O29 validation failed: cannot determine message type")
    elif msg_type != "BPS^O29":
        errors.append(f"BPS^O29 validation: expected message type BPS^O29, got {msg_type}")
        logger.warning(f"[{current_time}] BPS^O29 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BPS^O29 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_brp_o30(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BRP^O30 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BRP^O30 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BRP^O30 message missing required MSH segment")
        logger.error(f"[{current_time}] BRP^O30 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BRP^O30 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BRP^O30 validation failed: cannot determine message type")
    elif msg_type != "BRP^O30":
        errors.append(f"BRP^O30 validation: expected message type BRP^O30, got {msg_type}")
        logger.warning(f"[{current_time}] BRP^O30 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BRP^O30 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_brt_o32(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BRT^O32 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BRT^O32 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BRT^O32 message missing required MSH segment")
        logger.error(f"[{current_time}] BRT^O32 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BRT^O32 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BRT^O32 validation failed: cannot determine message type")
    elif msg_type != "BRT^O32":
        errors.append(f"BRT^O32 validation: expected message type BRT^O32, got {msg_type}")
        logger.warning(f"[{current_time}] BRT^O32 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BRT^O32 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_bts_o31(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate BTS^O31 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting BTS^O31 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("BTS^O31 message missing required MSH segment")
        logger.error(f"[{current_time}] BTS^O31 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("BTS^O31 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] BTS^O31 validation failed: cannot determine message type")
    elif msg_type != "BTS^O31":
        errors.append(f"BTS^O31 validation: expected message type BTS^O31, got {msg_type}")
        logger.warning(f"[{current_time}] BTS^O31 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] BTS^O31 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C01 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C01 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C01 validation failed: cannot determine message type")
    elif msg_type != "CRM^C01":
        errors.append(f"CRM^C01 validation: expected message type CRM^C01, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C01 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c02(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C02 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C02 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C02 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C02 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C02 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C02 validation failed: cannot determine message type")
    elif msg_type != "CRM^C02":
        errors.append(f"CRM^C02 validation: expected message type CRM^C02, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C02 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C02 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c03(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C03 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C03 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C03 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C03 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C03 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C03 validation failed: cannot determine message type")
    elif msg_type != "CRM^C03":
        errors.append(f"CRM^C03 validation: expected message type CRM^C03, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C03 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C03 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c04(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C04 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C04 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C04 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C04 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C04 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C04 validation failed: cannot determine message type")
    elif msg_type != "CRM^C04":
        errors.append(f"CRM^C04 validation: expected message type CRM^C04, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C04 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C04 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c05(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C05 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C05 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C05 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C05 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C05 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C05 validation failed: cannot determine message type")
    elif msg_type != "CRM^C05":
        errors.append(f"CRM^C05 validation: expected message type CRM^C05, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C05 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C05 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c06(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C06 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C06 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C06 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C06 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C06 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C06 validation failed: cannot determine message type")
    elif msg_type != "CRM^C06":
        errors.append(f"CRM^C06 validation: expected message type CRM^C06, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C06 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C06 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c07(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C07 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C07 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C07 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C07 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C07 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C07 validation failed: cannot determine message type")
    elif msg_type != "CRM^C07":
        errors.append(f"CRM^C07 validation: expected message type CRM^C07, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C07 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C07 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_crm_c08(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CRM^C08 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CRM^C08 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CRM^C08 message missing required MSH segment")
        logger.error(f"[{current_time}] CRM^C08 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CRM^C08 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CRM^C08 validation failed: cannot determine message type")
    elif msg_type != "CRM^C08":
        errors.append(f"CRM^C08 validation: expected message type CRM^C08, got {msg_type}")
        logger.warning(f"[{current_time}] CRM^C08 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CRM^C08 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_csu_c09(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CSU^C09 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CSU^C09 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CSU^C09 message missing required MSH segment")
        logger.error(f"[{current_time}] CSU^C09 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CSU^C09 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CSU^C09 validation failed: cannot determine message type")
    elif msg_type != "CSU^C09":
        errors.append(f"CSU^C09 validation: expected message type CSU^C09, got {msg_type}")
        logger.warning(f"[{current_time}] CSU^C09 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CSU^C09 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_csu_c10(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CSU^C10 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CSU^C10 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CSU^C10 message missing required MSH segment")
        logger.error(f"[{current_time}] CSU^C10 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CSU^C10 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CSU^C10 validation failed: cannot determine message type")
    elif msg_type != "CSU^C10":
        errors.append(f"CSU^C10 validation: expected message type CSU^C10, got {msg_type}")
        logger.warning(f"[{current_time}] CSU^C10 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CSU^C10 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_csu_c11(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CSU^C11 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CSU^C11 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CSU^C11 message missing required MSH segment")
        logger.error(f"[{current_time}] CSU^C11 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CSU^C11 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CSU^C11 validation failed: cannot determine message type")
    elif msg_type != "CSU^C11":
        errors.append(f"CSU^C11 validation: expected message type CSU^C11, got {msg_type}")
        logger.warning(f"[{current_time}] CSU^C11 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CSU^C11 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_csu_c12(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate CSU^C12 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CSU^C12 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("CSU^C12 message missing required MSH segment")
        logger.error(f"[{current_time}] CSU^C12 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("CSU^C12 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] CSU^C12 validation failed: cannot determine message type")
    elif msg_type != "CSU^C12":
        errors.append(f"CSU^C12 validation: expected message type CSU^C12, got {msg_type}")
        logger.warning(f"[{current_time}] CSU^C12 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] CSU^C12 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_dbc_o41(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate DBC^O41 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DBC^O41 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("DBC^O41 message missing required MSH segment")
        logger.error(f"[{current_time}] DBC^O41 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("DBC^O41 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] DBC^O41 validation failed: cannot determine message type")
    elif msg_type != "DBC^O41":
        errors.append(f"DBC^O41 validation: expected message type DBC^O41, got {msg_type}")
        logger.warning(f"[{current_time}] DBC^O41 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] DBC^O41 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_dbu_o42(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate DBU^O42 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DBU^O42 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("DBU^O42 message missing required MSH segment")
        logger.error(f"[{current_time}] DBU^O42 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("DBU^O42 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] DBU^O42 validation failed: cannot determine message type")
    elif msg_type != "DBU^O42":
        errors.append(f"DBU^O42 validation: expected message type DBU^O42, got {msg_type}")
        logger.warning(f"[{current_time}] DBU^O42 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] DBU^O42 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_description_c(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate DESCRIPTION^C message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DESCRIPTION^C message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("DESCRIPTION^C message missing required MSH segment")
        logger.error(f"[{current_time}] DESCRIPTION^C validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("DESCRIPTION^C message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] DESCRIPTION^C validation failed: cannot determine message type")
    elif msg_type != "DESCRIPTION^C":
        errors.append(f"DESCRIPTION^C validation: expected message type DESCRIPTION^C, got {msg_type}")
        logger.warning(f"[{current_time}] DESCRIPTION^C validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] DESCRIPTION^C validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_dft_p03(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate DFT^P03 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DFT^P03 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("DFT^P03 message missing required MSH segment")
        logger.error(f"[{current_time}] DFT^P03 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("DFT^P03 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] DFT^P03 validation failed: cannot determine message type")
    elif msg_type != "DFT^P03":
        errors.append(f"DFT^P03 validation: expected message type DFT^P03, got {msg_type}")
        logger.warning(f"[{current_time}] DFT^P03 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] DFT^P03 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_dft_p11(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate DFT^P11 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DFT^P11 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("DFT^P11 message missing required MSH segment")
        logger.error(f"[{current_time}] DFT^P11 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("DFT^P11 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] DFT^P11 validation failed: cannot determine message type")
    elif msg_type != "DFT^P11":
        errors.append(f"DFT^P11 validation: expected message type DFT^P11, got {msg_type}")
        logger.warning(f"[{current_time}] DFT^P11 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] DFT^P11 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_dsr_q03(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate DSR^Q03 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DSR^Q03 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("DSR^Q03 message missing required MSH segment")
        logger.error(f"[{current_time}] DSR^Q03 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("DSR^Q03 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] DSR^Q03 validation failed: cannot determine message type")
    elif msg_type != "DSR^Q03":
        errors.append(f"DSR^Q03 validation: expected message type DSR^Q03, got {msg_type}")
        logger.warning(f"[{current_time}] DSR^Q03 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] DSR^Q03 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_eac_u07(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate EAC^U07 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EAC^U07 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("EAC^U07 message missing required MSH segment")
        logger.error(f"[{current_time}] EAC^U07 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("EAC^U07 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] EAC^U07 validation failed: cannot determine message type")
    elif msg_type != "EAC^U07":
        errors.append(f"EAC^U07 validation: expected message type EAC^U07, got {msg_type}")
        logger.warning(f"[{current_time}] EAC^U07 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] EAC^U07 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_ean_u09(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate EAN^U09 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EAN^U09 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("EAN^U09 message missing required MSH segment")
        logger.error(f"[{current_time}] EAN^U09 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("EAN^U09 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] EAN^U09 validation failed: cannot determine message type")
    elif msg_type != "EAN^U09":
        errors.append(f"EAN^U09 validation: expected message type EAN^U09, got {msg_type}")
        logger.warning(f"[{current_time}] EAN^U09 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] EAN^U09 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_ear_u08(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate EAR^U08 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EAR^U08 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("EAR^U08 message missing required MSH segment")
        logger.error(f"[{current_time}] EAR^U08 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("EAR^U08 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] EAR^U08 validation failed: cannot determine message type")
    elif msg_type != "EAR^U08":
        errors.append(f"EAR^U08 validation: expected message type EAR^U08, got {msg_type}")
        logger.warning(f"[{current_time}] EAR^U08 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] EAR^U08 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_edit_e10(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate EDIT^E10 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EDIT^E10 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("EDIT^E10 message missing required MSH segment")
        logger.error(f"[{current_time}] EDIT^E10 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("EDIT^E10 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] EDIT^E10 validation failed: cannot determine message type")
    elif msg_type != "EDIT^E10":
        errors.append(f"EDIT^E10 validation: expected message type EDIT^E10, got {msg_type}")
        logger.warning(f"[{current_time}] EDIT^E10 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] EDIT^E10 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_edr_r07(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate EDR^R07 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EDR^R07 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("EDR^R07 message missing required MSH segment")
        logger.error(f"[{current_time}] EDR^R07 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("EDR^R07 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] EDR^R07 validation failed: cannot determine message type")
    elif msg_type != "EDR^R07":
        errors.append(f"EDR^R07 validation: expected message type EDR^R07, got {msg_type}")
        logger.warning(f"[{current_time}] EDR^R07 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] EDR^R07 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_eqq_q04(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate EQQ^Q04 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EQQ^Q04 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("EQQ^Q04 message missing required MSH segment")
        logger.error(f"[{current_time}] EQQ^Q04 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("EQQ^Q04 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] EQQ^Q04 validation failed: cannot determine message type")
    elif msg_type != "EQQ^Q04":
        errors.append(f"EQQ^Q04 validation: expected message type EQQ^Q04, got {msg_type}")
        logger.warning(f"[{current_time}] EQQ^Q04 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] EQQ^Q04 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_erp_r09(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ERP^R09 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ERP^R09 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ERP^R09 message missing required MSH segment")
        logger.error(f"[{current_time}] ERP^R09 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ERP^R09 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ERP^R09 validation failed: cannot determine message type")
    elif msg_type != "ERP^R09":
        errors.append(f"ERP^R09 validation: expected message type ERP^R09, got {msg_type}")
        logger.warning(f"[{current_time}] ERP^R09 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ERP^R09 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_esr_u02(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ESR^U02 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ESR^U02 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ESR^U02 message missing required MSH segment")
        logger.error(f"[{current_time}] ESR^U02 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ESR^U02 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ESR^U02 validation failed: cannot determine message type")
    elif msg_type != "ESR^U02":
        errors.append(f"ESR^U02 validation: expected message type ESR^U02, got {msg_type}")
        logger.warning(f"[{current_time}] ESR^U02 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ESR^U02 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_esu_u01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ESU^U01 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ESU^U01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ESU^U01 message missing required MSH segment")
        logger.error(f"[{current_time}] ESU^U01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ESU^U01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ESU^U01 validation failed: cannot determine message type")
    elif msg_type != "ESU^U01":
        errors.append(f"ESU^U01 validation: expected message type ESU^U01, got {msg_type}")
        logger.warning(f"[{current_time}] ESU^U01 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] ESU^U01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_inr_u06(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate INR^U06 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting INR^U06 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("INR^U06 message missing required MSH segment")
        logger.error(f"[{current_time}] INR^U06 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("INR^U06 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] INR^U06 validation failed: cannot determine message type")
    elif msg_type != "INR^U06":
        errors.append(f"INR^U06 validation: expected message type INR^U06, got {msg_type}")
        logger.warning(f"[{current_time}] INR^U06 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] INR^U06 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_inr_u14(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate INR^U14 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting INR^U14 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("INR^U14 message missing required MSH segment")
        logger.error(f"[{current_time}] INR^U14 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("INR^U14 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] INR^U14 validation failed: cannot determine message type")
    elif msg_type != "INR^U14":
        errors.append(f"INR^U14 validation: expected message type INR^U14, got {msg_type}")
        logger.warning(f"[{current_time}] INR^U14 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] INR^U14 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_inu_u05(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate INU^U05 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting INU^U05 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("INU^U05 message missing required MSH segment")
        logger.error(f"[{current_time}] INU^U05 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("INU^U05 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] INU^U05 validation failed: cannot determine message type")
    elif msg_type != "INU^U05":
        errors.append(f"INU^U05 validation: expected message type INU^U05, got {msg_type}")
        logger.warning(f"[{current_time}] INU^U05 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] INU^U05 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_lsr_u13(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate LSR^U13 message.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting LSR^U13 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("LSR^U13 message missing required MSH segment")
        logger.error(f"[{current_time}] LSR^U13 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("LSR^U13 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] LSR^U13 validation failed: cannot determine message type")
    elif msg_type != "LSR^U13":
        errors.append(f"LSR^U13 validation: expected message type LSR^U13, got {msg_type}")
        logger.warning(f"[{current_time}] LSR^U13 validation warning: message type mismatch ({msg_type})")
    
    # Basic validation - can be extended with specific segment requirements
    logger.info(f"[{current_time}] LSR^U13 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


# ============================================================================
# Common Missing Message Type Validations
# ============================================================================

def validate_ack(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ACK (General Acknowledgment) message.
    
    ACK messages require MSH and MSA segments.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ACK message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ACK message missing required MSH segment")
        logger.error(f"[{current_time}] ACK validation failed: missing MSH segment")
        return False, errors
    
    # Check MSA segment exists (required for ACK)
    msa_segments = message.get_segments("MSA")
    if not msa_segments:
        errors.append("ACK message missing required MSA segment")
        logger.warning(f"[{current_time}] ACK validation warning: missing MSA segment")
    
    # Verify message type
    msg_type = get_message_type(message)
    if msg_type and msg_type not in ("ACK", "ACK^ACK"):
        logger.warning(f"[{current_time}] ACK validation warning: unexpected message type ({msg_type})")
    
    logger.info(f"[{current_time}] ACK validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_orm_o01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ORM^O01 (Order Message) message.
    
    ORM messages require MSH, ORC segments and order detail segments.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ORM^O01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ORM^O01 message missing required MSH segment")
        logger.error(f"[{current_time}] ORM^O01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ORM^O01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ORM^O01 validation failed: cannot determine message type")
    elif msg_type != "ORM^O01":
        errors.append(f"ORM^O01 validation: expected message type ORM^O01, got {msg_type}")
        logger.warning(f"[{current_time}] ORM^O01 validation warning: message type mismatch ({msg_type})")
    
    # Check ORC segment exists (required for order messages)
    orc_segments = message.get_segments("ORC")
    if not orc_segments:
        errors.append("ORM^O01 message missing required ORC segment")
        logger.warning(f"[{current_time}] ORM^O01 validation warning: missing ORC segment")
    
    logger.info(f"[{current_time}] ORM^O01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_oru_r01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate ORU^R01 (Observation Result) message.
    
    ORU messages require MSH, OBR, and OBX segments.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ORU^R01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("ORU^R01 message missing required MSH segment")
        logger.error(f"[{current_time}] ORU^R01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("ORU^R01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] ORU^R01 validation failed: cannot determine message type")
    elif msg_type != "ORU^R01":
        errors.append(f"ORU^R01 validation: expected message type ORU^R01, got {msg_type}")
        logger.warning(f"[{current_time}] ORU^R01 validation warning: message type mismatch ({msg_type})")
    
    # Check OBR segment exists (required for observation results)
    obr_segments = message.get_segments("OBR")
    if not obr_segments:
        errors.append("ORU^R01 message missing required OBR segment")
        logger.warning(f"[{current_time}] ORU^R01 validation warning: missing OBR segment")
    
    # Check OBX segment exists (required for observation results)
    obx_segments = message.get_segments("OBX")
    if not obx_segments:
        errors.append("ORU^R01 message missing required OBX segment")
        logger.warning(f"[{current_time}] ORU^R01 validation warning: missing OBX segment")
    
    logger.info(f"[{current_time}] ORU^R01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_mdm_t01(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate MDM^T01 (Document Management) message.
    
    MDM messages require MSH and TXA segments.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MDM^T01 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("MDM^T01 message missing required MSH segment")
        logger.error(f"[{current_time}] MDM^T01 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("MDM^T01 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] MDM^T01 validation failed: cannot determine message type")
    elif msg_type != "MDM^T01":
        errors.append(f"MDM^T01 validation: expected message type MDM^T01, got {msg_type}")
        logger.warning(f"[{current_time}] MDM^T01 validation warning: message type mismatch ({msg_type})")
    
    # Check TXA segment exists (required for document management)
    txa_segments = message.get_segments("TXA")
    if not txa_segments:
        errors.append("MDM^T01 message missing required TXA segment")
        logger.warning(f"[{current_time}] MDM^T01 validation warning: missing TXA segment")
    
    logger.info(f"[{current_time}] MDM^T01 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


def validate_siu_s12(message: Message) -> Tuple[bool, List[str]]:
    """
    Validate SIU^S12 (Notification of Appointment Modification) message.
    
    SIU messages require MSH and SCH segments.
    
    Args:
        message: HL7 v2 message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting SIU^S12 message validation")
    
    # Check MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("SIU^S12 message missing required MSH segment")
        logger.error(f"[{current_time}] SIU^S12 validation failed: missing MSH segment")
        return False, errors
    
    # Verify message type
    msg_type = get_message_type(message)
    if not msg_type:
        errors.append("SIU^S12 message: cannot determine message type from MSH-9")
        logger.error(f"[{current_time}] SIU^S12 validation failed: cannot determine message type")
    elif msg_type != "SIU^S12":
        errors.append(f"SIU^S12 validation: expected message type SIU^S12, got {msg_type}")
        logger.warning(f"[{current_time}] SIU^S12 validation warning: message type mismatch ({msg_type})")
    
    # Check SCH segment exists (required for scheduling messages)
    sch_segments = message.get_segments("SCH")
    if not sch_segments:
        errors.append("SIU^S12 message missing required SCH segment")
        logger.warning(f"[{current_time}] SIU^S12 validation warning: missing SCH segment")
    
    logger.info(f"[{current_time}] SIU^S12 validation completed with {len(errors)} errors")
    return len(errors) == 0, errors


# Helper function to create standard message validation functions
def _create_message_validator(msg_code: str, trigger: str, required_segments: List[str] = None):
    """
    Create a standard message validation function.
    
    Args:
        msg_code: Message code (e.g., "ORM")
        trigger: Trigger event (e.g., "O01")
        required_segments: List of required segment names (default: ["MSH"])
        
    Returns:
        Validation function
    """
    if required_segments is None:
        required_segments = ["MSH"]
    
    msg_type = f"{msg_code}^{trigger}"
    func_name = f"validate_{msg_code.lower()}_{trigger.lower()}"
    
    def validator(message: Message) -> Tuple[bool, List[str]]:
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Starting {msg_type} message validation")
        
        # Check required segments
        for seg_name in required_segments:
            segs = message.get_segments(seg_name)
            if not segs:
                if seg_name == "MSH":
                    errors.append(f"{msg_type} message missing required {seg_name} segment")
                    logger.error(f"[{current_time}] {msg_type} validation failed: missing {seg_name} segment")
                    return False, errors
                else:
                    errors.append(f"{msg_type} message missing required {seg_name} segment")
                    logger.warning(f"[{current_time}] {msg_type} validation warning: missing {seg_name} segment")
        
        # Verify message type
        detected_type = get_message_type(message)
        if not detected_type:
            errors.append(f"{msg_type} message: cannot determine message type from MSH-9")
            logger.error(f"[{current_time}] {msg_type} validation failed: cannot determine message type")
        elif detected_type != msg_type:
            errors.append(f"{msg_type} validation: expected message type {msg_type}, got {detected_type}")
            logger.warning(f"[{current_time}] {msg_type} validation warning: message type mismatch ({detected_type})")
        
        logger.info(f"[{current_time}] {msg_type} validation completed with {len(errors)} errors")
        return len(errors) == 0, errors
    
    validator.__name__ = func_name
    validator.__doc__ = f"Validate {msg_type} message."
    return validator


# Add more ORM message types (O02-O08)
validate_orm_o02 = _create_message_validator("ORM", "O02", ["MSH", "ORC"])
validate_orm_o03 = _create_message_validator("ORM", "O03", ["MSH", "ORC"])
validate_orm_o04 = _create_message_validator("ORM", "O04", ["MSH", "ORC"])
validate_orm_o05 = _create_message_validator("ORM", "O05", ["MSH", "ORC"])
validate_orm_o06 = _create_message_validator("ORM", "O06", ["MSH", "ORC"])
validate_orm_o07 = _create_message_validator("ORM", "O07", ["MSH", "ORC"])
validate_orm_o08 = _create_message_validator("ORM", "O08", ["MSH", "ORC"])

# Add more ORU message types (R02-R04)
validate_oru_r02 = _create_message_validator("ORU", "R02", ["MSH", "OBR", "OBX"])
validate_oru_r03 = _create_message_validator("ORU", "R03", ["MSH", "OBR", "OBX"])
validate_oru_r04 = _create_message_validator("ORU", "R04", ["MSH", "OBR", "OBX"])

# Add more MDM message types (T02-T11)
validate_mdm_t02 = _create_message_validator("MDM", "T02", ["MSH", "TXA"])
validate_mdm_t03 = _create_message_validator("MDM", "T03", ["MSH", "TXA"])
validate_mdm_t04 = _create_message_validator("MDM", "T04", ["MSH", "TXA"])
validate_mdm_t05 = _create_message_validator("MDM", "T05", ["MSH", "TXA"])
validate_mdm_t06 = _create_message_validator("MDM", "T06", ["MSH", "TXA"])
validate_mdm_t07 = _create_message_validator("MDM", "T07", ["MSH", "TXA"])
validate_mdm_t08 = _create_message_validator("MDM", "T08", ["MSH", "TXA"])
validate_mdm_t09 = _create_message_validator("MDM", "T09", ["MSH", "TXA"])
validate_mdm_t10 = _create_message_validator("MDM", "T10", ["MSH", "TXA"])
validate_mdm_t11 = _create_message_validator("MDM", "T11", ["MSH", "TXA"])

# Add more SIU message types (S11-S26, excluding S12 which is already defined)
validate_siu_s11 = _create_message_validator("SIU", "S11", ["MSH", "SCH"])
validate_siu_s13 = _create_message_validator("SIU", "S13", ["MSH", "SCH"])
validate_siu_s14 = _create_message_validator("SIU", "S14", ["MSH", "SCH"])
validate_siu_s15 = _create_message_validator("SIU", "S15", ["MSH", "SCH"])
validate_siu_s16 = _create_message_validator("SIU", "S16", ["MSH", "SCH"])
validate_siu_s17 = _create_message_validator("SIU", "S17", ["MSH", "SCH"])
validate_siu_s18 = _create_message_validator("SIU", "S18", ["MSH", "SCH"])
validate_siu_s19 = _create_message_validator("SIU", "S19", ["MSH", "SCH"])
validate_siu_s20 = _create_message_validator("SIU", "S20", ["MSH", "SCH"])
validate_siu_s21 = _create_message_validator("SIU", "S21", ["MSH", "SCH"])
validate_siu_s22 = _create_message_validator("SIU", "S22", ["MSH", "SCH"])
validate_siu_s23 = _create_message_validator("SIU", "S23", ["MSH", "SCH"])
validate_siu_s24 = _create_message_validator("SIU", "S24", ["MSH", "SCH"])
validate_siu_s26 = _create_message_validator("SIU", "S26", ["MSH", "SCH"])

# Add common ADT message types that are missing (A19, A56-A59)
validate_adt_a19 = _create_message_validator("ADT", "A19", ["MSH", "EVN", "PID", "PV1"])
validate_adt_a56 = _create_message_validator("ADT", "A56", ["MSH", "EVN", "PID", "PV1"])
validate_adt_a57 = _create_message_validator("ADT", "A57", ["MSH", "EVN", "PID", "PV1"])
validate_adt_a58 = _create_message_validator("ADT", "A58", ["MSH", "EVN", "PID", "PV1"])
validate_adt_a59 = _create_message_validator("ADT", "A59", ["MSH", "EVN", "PID", "PV1"])

# Log completion timestamp at end of operations
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
