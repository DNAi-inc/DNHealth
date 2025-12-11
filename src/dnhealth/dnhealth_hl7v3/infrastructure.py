# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Message Infrastructure.

Provides utilities for message ID generation, timestamp generation,
security token handling, and correlation ID management.
"""

import uuid
import re
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from dataclasses import dataclass, field
import logging

from .datatypes import II, TS
from .model import Message

logger = logging.getLogger(__name__)

# Default OID root for HL7 assigned identifiers
DEFAULT_OID_ROOT = "2.16.840.1.113883.3.72"


def generate_message_id(oid_root: Optional[str] = None) -> II:
    """
    Generate a unique message ID.
    
    Creates a UUID-based message ID using the II (Instance Identifier) data type.
    The ID uses a default OID root (HL7 assigned) or a custom OID root.
    
    Args:
        oid_root: Optional OID root. If None, uses DEFAULT_OID_ROOT.
        
    Returns:
        II (Instance Identifier) with root and extension
        
    Example:
        >>> msg_id = generate_message_id()
        >>> print(msg_id.root)
        2.16.840.1.113883.3.72
        >>> print(msg_id.extension)
        550e8400-e29b-41d4-a716-446655440000
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Generating message ID")
    
    # Use default OID root if not provided
    root = oid_root or DEFAULT_OID_ROOT
    
    # Generate UUID
    message_uuid = str(uuid.uuid4())
    
    # Validate UUID format (8-4-4-4-12 hex digits)
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    if not uuid_pattern.match(message_uuid):
        raise ValueError(f"Generated UUID has invalid format: {message_uuid}")
    
    # Create II instance
    message_id = II(
        root=root,
        extension=message_uuid,
        assigning_authority_name="HL7"
    )
    
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{end_time}] Generated message ID: root={root}, extension={message_uuid}")
    return message_id


def generate_timestamp() -> TS:
    """
    Generate current timestamp in ISO 8601 format.
    
    Creates a timestamp using the TS (Time Stamp) data type.
    The timestamp includes timezone offset (preferred) or UTC.
    
    Returns:
        TS (Time Stamp) with ISO 8601 formatted value
        
    Example:
        >>> ts = generate_timestamp()
        >>> print(ts.value)
        20250101120000.000+0500
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Generating timestamp")
    
    # Get current datetime with timezone
    now = datetime.now(timezone.utc)
    
    # Format as HL7 v3 TS format: YYYYMMDDHHmmss[.s[s[s[s]]]][+/-ZZzz]
    # Or ISO 8601 format: YYYY-MM-DDTHH:mm:ss[.s[s[s[s]]]][+/-ZZzz]
    
    # Use ISO 8601 format with timezone
    timestamp_str = now.strftime("%Y%m%d%H%M%S.%f")
    # Remove microseconds beyond 4 digits if present
    if '.' in timestamp_str:
        parts = timestamp_str.split('.')
        if len(parts[1]) > 4:
            parts[1] = parts[1][:4]
        timestamp_str = '.'.join(parts)
    
    # Add timezone offset
    tz_offset = now.strftime("%z")
    if tz_offset:
        # Format: +0500 or -0500
        timestamp_str += tz_offset
    
    # Validate timestamp format
    # Basic validation: should match ISO 8601 pattern
    ts_pattern = re.compile(
        r'^\d{8}\d{6}(\.\d{1,4})?([+-]\d{4}|Z)?$'
    )
    if not ts_pattern.match(timestamp_str.replace('-', '').replace(':', '')):
        # Fallback to simpler format
        timestamp_str = now.strftime("%Y%m%d%H%M%S")
        tz_offset = now.strftime("%z")
        if tz_offset:
            timestamp_str += tz_offset
    
    # Create TS instance
    timestamp = TS(value=timestamp_str)
    
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{end_time}] Generated timestamp: {timestamp_str}")
    return timestamp


@dataclass
class SecurityToken:
    """
    Security token for HL7 v3 message authentication.
    
    Supports various token types including Bearer, SAML, and X.509 certificates.
    """
    type: str  # Token type (e.g., "Bearer", "SAML", "X.509")
    value: str  # Token value (base64 encoded if binary)
    expiration: Optional[TS] = None  # Expiration timestamp
    issuer: Optional[str] = None  # Token issuer
    
    def to_xml(self) -> str:
        """
        Serialize security token to XML.
        
        Returns:
            XML string representation of security token
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Serializing security token to XML")
        
        xml_parts = ['<securityToken xmlns="urn:hl7-org:v3">']
        xml_parts.append(f'<type>{self.type}</type>')
        xml_parts.append(f'<value>{self.value}</value>')
        
        if self.expiration:
            xml_parts.append(f'<expiration value="{self.expiration.value}"/>')
        
        if self.issuer:
            xml_parts.append(f'<issuer>{self.issuer}</issuer>')
        
        xml_parts.append('</securityToken>')
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{end_time}] Serialized security token to XML")
        return '\n'.join(xml_parts)
    
    def from_xml(self, xml_string: str) -> "SecurityToken":
        """
        Parse security token from XML.
        
        Args:
            xml_string: XML string representation
            
        Returns:
            SecurityToken instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Parsing security token from XML")
        
        # Simple XML parsing (for production, use proper XML parser)
        import re
        
        type_match = re.search(r'<type>(.*?)</type>', xml_string, re.DOTALL)
        value_match = re.search(r'<value>(.*?)</value>', xml_string, re.DOTALL)
        expiration_match = re.search(r'<expiration value="(.*?)"/>', xml_string)
        issuer_match = re.search(r'<issuer>(.*?)</issuer>', xml_string, re.DOTALL)
        
        token_type = type_match.group(1) if type_match else ""
        token_value = value_match.group(1) if value_match else ""
        expiration_value = expiration_match.group(1) if expiration_match else None
        issuer_value = issuer_match.group(1) if issuer_match else None
        
        expiration_ts = TS(value=expiration_value) if expiration_value else None
        
        token = SecurityToken(
            type=token_type,
            value=token_value,
            expiration=expiration_ts,
            issuer=issuer_value
        )
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{end_time}] Parsed security token from XML")
        return token
    
    def is_valid(self) -> bool:
        """
        Check if token is valid (not expired).
        
        Returns:
            True if token is valid, False if expired
        """
        if self.expiration is None:
            return True  # No expiration means always valid
        
        current_time = datetime.now(timezone.utc)
        expiration_time = self.expiration.to_datetime()
        
        if expiration_time is None:
            return True  # Can't parse expiration, assume valid
        
        return current_time < expiration_time
    
    def is_expired(self) -> bool:
        """
        Check if token is expired.
        
        Returns:
            True if token is expired, False otherwise
        """
        return not self.is_valid()



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def generate_correlation_id() -> str:
    """
    Generate a unique correlation ID for message tracking.
    
    Creates a UUID-based correlation ID for tracking related messages
    in a conversation.
    
    Returns:
        UUID string
        
    Example:
        >>> corr_id = generate_correlation_id()
        >>> print(corr_id)
        550e8400-e29b-41d4-a716-446655440000
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Generating correlation ID")
    
    correlation_id = str(uuid.uuid4())
    
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{end_time}] Generated correlation ID: {correlation_id}")
    return correlation_id


def extract_correlation_id(message: Message) -> Optional[str]:
    """
    Extract correlation ID from message.
    
    Looks for correlation ID in message metadata or transmission wrapper.
    
    Args:
        message: HL7 v3 Message object
        
    Returns:
        Correlation ID string or None if not found
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Extracting correlation ID from message")
    
    # Check message metadata first
    if hasattr(message, 'metadata') and isinstance(message.metadata, dict):
        corr_id = message.metadata.get('correlation_id')
        if corr_id:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{end_time}] Found correlation ID in metadata: {corr_id}")
            return corr_id
    
    # Check transmission wrapper
    if hasattr(message, 'get_control_act_process'):
        try:
            control_act = message.get_control_act_process()
            if control_act and hasattr(control_act, 'correlation_id'):
                corr_id = control_act.correlation_id
                if corr_id:
                    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"[{end_time}] Found correlation ID in control act: {corr_id}")
                    return corr_id
        except Exception as e:
            logger.debug(f"Error extracting correlation ID from control act: {e}")
    
    # Check root element attributes
    if hasattr(message, 'root') and message.root:
        if hasattr(message.root, 'attributes'):
            corr_id = message.root.attributes.get('correlationId')
            if corr_id:
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{end_time}] Found correlation ID in root attributes: {corr_id}")
                return corr_id
    
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{end_time}] Correlation ID not found in message")
    return None


def set_correlation_id(message: Message, correlation_id: str) -> None:
    """
    Set correlation ID in message.
    
    Stores correlation ID in message metadata or transmission wrapper.
    
    Args:
        message: HL7 v3 Message object
        correlation_id: Correlation ID string
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Setting correlation ID in message: {correlation_id}")
    
    # Validate correlation ID format (UUID)
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    if not uuid_pattern.match(correlation_id):
        raise ValueError(f"Invalid correlation ID format: {correlation_id}")
    
    # Set in message metadata
    if not hasattr(message, 'metadata'):
        message.metadata = {}
    
    if not isinstance(message.metadata, dict):
        message.metadata = {}
    
    message.metadata['correlation_id'] = correlation_id
    
    # Also set in root element attributes if available
    if hasattr(message, 'root') and message.root:
        if not hasattr(message.root, 'attributes'):
            message.root.attributes = {}
        message.root.attributes['correlationId'] = correlation_id
    
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{end_time}] Correlation ID set successfully")
