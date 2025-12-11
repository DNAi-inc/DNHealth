# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Message Envelope.

Provides Message Envelope classes for wrapping HL7 v3 messages including:
- MessageEnvelope - Main envelope class for wrapping messages
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import xml.etree.ElementTree as ET

from dnhealth.dnhealth_hl7v3.model import Message
from dnhealth.dnhealth_hl7v3.transmission import TransmissionWrapper
from dnhealth.dnhealth_hl7v3.parser import parse_message

logger = logging.getLogger(__name__)

# HL7 v3 namespace
HL7V3_NAMESPACE = "urn:hl7-org:v3"


# ============================================================================
# Message Envelope
# ============================================================================

@dataclass
class MessageEnvelope:
    """
    MessageEnvelope - Envelope for wrapping HL7 v3 messages.
    
    Structure per HL7 v3 specification:
    ```xml
    <envelope xmlns="urn:hl7-org:v3">
      <transmission>
        <id>...</id>
        <creationTime>...</creationTime>
        <interactionId>...</interactionId>
        <sender>...</sender>
        <receiver>...</receiver>
        <controlActProcess>
          <classCode>...</classCode>
          <moodCode>...</moodCode>
          <code>...</code>
          <subject>...</subject>
        </controlActProcess>
      </transmission>
    </envelope>
    ```
    """
    transmission: TransmissionWrapper  # Required transmission wrapper
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    def validate(self) -> List[str]:
        """
        Validate envelope structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Message envelope validation")
        
        if not self.transmission:
            errors.append("MessageEnvelope.transmission is required")
        else:
            transmission_errors = self.transmission.validate()
            for error in transmission_errors:
                errors.append(f"MessageEnvelope.transmission: {error}")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"[{current_time}] Message envelope validation passed")
        else:
            logger.warning(f"[{current_time}] Message envelope validation failed: {len(errors)} errors")
        
        return errors
    
    @classmethod
    def wrap_message(cls, message: Message, transmission: TransmissionWrapper) -> "MessageEnvelope":
        """
        Wrap a message in envelope.
        
        Args:
            message: Message to wrap
            transmission: Transmission wrapper to use
            
        Returns:
            MessageEnvelope object
            
        Note:
            The message content should be included in the transmission wrapper's
            control act wrapper subjects. This is a simplified implementation.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Wrapping message in envelope")
        
        # Create envelope with transmission wrapper
        # The message content is expected to be in the control act wrapper
        envelope = cls(transmission=transmission)
        
        logger.debug(f"[{current_time}] Message wrapped in envelope")
        return envelope
    
    def unwrap_message(self) -> Optional[Message]:
        """
        Extract message from envelope.
        
        Returns:
            Message object or None if extraction fails
            
        Note:
            This extracts the message content from the transmission wrapper's
            control act wrapper. This is a simplified implementation.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Unwrapping message from envelope")
        
        # Extract message from control act wrapper
        # This is a simplified implementation - in practice, the message
        # content would be extracted from the control act wrapper's subjects
        try:
            # Serialize transmission wrapper to XML
            transmission_xml = self.transmission.to_xml()
            
            # Parse the XML to extract message content
            # In a full implementation, this would extract the actual message payload
            # For now, we'll create a simple message from the transmission wrapper
            root = ET.fromstring(transmission_xml)
            
            # Create a message from the root element
            # This is simplified - in practice, you'd extract the actual message payload
            from dnhealth.dnhealth_hl7v3.model import ElementNode
            element_node = ElementNode(name=root.tag, attributes={})
            message = Message(root=element_node)
            
            logger.debug(f"[{current_time}] Message unwrapped from envelope")
            return message
        except Exception as e:
            logger.error(f"[{current_time}] Error unwrapping message: {e}")
            return None
    
    def to_xml(self) -> str:
        """
        Serialize to XML with proper namespace.
        
        Returns:
            XML string
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Message envelope XML serialization")
        
        root = ET.Element("envelope")
        root.set("xmlns", HL7V3_NAMESPACE)
        
        # Add transmission wrapper
        if self.transmission:
            # Serialize transmission wrapper to XML
            transmission_xml = self.transmission.to_xml()
            transmission_root = ET.fromstring(transmission_xml)
            
            # Remove XML declaration if present and add as sub-element
            if transmission_root.tag == "transmission":
                root.append(transmission_root)
        
        # Convert to string
        ET.register_namespace("", HL7V3_NAMESPACE)
        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
        
        logger.debug(f"[{current_time}] Message envelope XML serialization completed")
        return xml_str
    
    @classmethod
    def from_xml(cls, xml_string: str) -> "MessageEnvelope":
        """
        Parse from XML.
        
        Args:
            xml_string: XML string to parse
            
        Returns:
            MessageEnvelope object
            
        Raises:
            ValueError: If XML is invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Message envelope XML parsing")
        
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        
        if root.tag != "envelope":
            raise ValueError(f"Expected envelope, got {root.tag}")
        
        # Parse transmission wrapper
        transmission_elem = root.find(".//{urn:hl7-org:v3}transmission")
        transmission = None
        if transmission_elem is not None:
            from dnhealth.dnhealth_hl7v3.transmission import TransmissionWrapper
            transmission_xml = ET.tostring(transmission_elem, encoding="unicode")
            transmission = TransmissionWrapper.from_xml(transmission_xml)
        
        if not transmission:
            raise ValueError("Missing transmission wrapper in XML")
        
        result = cls(transmission=transmission)
        
        logger.debug(f"[{current_time}] Message envelope XML parsing completed")
        return result
