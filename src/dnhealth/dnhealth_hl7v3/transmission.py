# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Transmission Wrapper.

Provides Transmission wrapper classes for HL7 v3 messages including:
- TransmissionWrapper - Main transmission wrapper class
- TransmissionParty - Party class for transmission wrapper
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import xml.etree.ElementTree as ET

from dnhealth.dnhealth_hl7v3.datatypes import II, TS, CS
from dnhealth.dnhealth_hl7v3.control_act import ControlActWrapper
from dnhealth.dnhealth_hl7v3.message_control import MCCIParty

logger = logging.getLogger(__name__)

# HL7 v3 namespace
HL7V3_NAMESPACE = "urn:hl7-org:v3"


# ============================================================================
# Transmission Party
# ============================================================================

@dataclass
class TransmissionParty:
    """
    TransmissionParty - Represents a party in transmission wrapper.
    
    Similar to MCCIParty but for transmission wrapper.
    """
    type_code: CS  # Required
    id: List[II] = field(default_factory=list)  # Required, at least one
    name: Optional[str] = None  # Optional party name
    
    def validate(self) -> List[str]:
        """
        Validate party structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not self.type_code:
            errors.append("TransmissionParty.type_code is required")
        
        if not self.id or len(self.id) == 0:
            errors.append("TransmissionParty.id is required (at least one ID)")
        
        return errors
    
    def to_xml_element(self, parent: ET.Element, tag_name: str = "party") -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            tag_name: Tag name for the element (default: "party")
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, tag_name)
        
        # Type code
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
        
        # IDs
        for party_id in self.id:
            id_elem = ET.SubElement(elem, "id")
            if party_id.root:
                id_elem.set("root", party_id.root)
            if party_id.extension:
                id_elem.set("extension", party_id.extension)
        
        # Name
        if self.name:
            name_elem = ET.SubElement(elem, "name")
            name_elem.text = self.name
        

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


# ============================================================================
# Transmission Wrapper
# ============================================================================

@dataclass
class TransmissionWrapper:
    """
    TransmissionWrapper - Transmission Wrapper for HL7 v3 messages.
    
    Attributes per HL7 v3 Transmission specification:
    - id: II - Transmission ID (required)
    - creation_time: TS - Creation timestamp (required)
    - version_code: CS - Version code (optional)
    - interaction_id: II - Interaction ID (required)
    - processing_mode_code: CS - Processing mode (optional, table MCCI_000004)
    - processing_code: CS - Processing code (optional, table MCCI_000005)
    - processing_id: CS - Processing ID (optional)
    - accept_ack_code: CS - Accept acknowledgment code (optional, table MCCI_000006)
    - application_ack_code: CS - Application acknowledgment code (optional, table MCCI_000007)
    - receiver: List[TransmissionParty] - Receivers (required, at least one)
    - sender: TransmissionParty - Sender (required)
    - control_act_wrapper: ControlActWrapper - Control act wrapper (required)
    """
    id: II  # Required
    creation_time: TS  # Required
    interaction_id: II  # Required
    sender: TransmissionParty  # Required
    receiver: List[TransmissionParty] = field(default_factory=list)  # Required, at least one
    control_act_wrapper: ControlActWrapper  # Required
    version_code: Optional[CS] = None  # Optional
    processing_mode_code: Optional[CS] = None  # Optional
    processing_code: Optional[CS] = None  # Optional
    processing_id: Optional[CS] = None  # Optional
    accept_ack_code: Optional[CS] = None  # Optional
    application_ack_code: Optional[CS] = None  # Optional
    
    def validate(self) -> List[str]:
        """
        Validate wrapper structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Transmission wrapper validation")
        
        if not self.id:
            errors.append("TransmissionWrapper.id is required")
        
        if not self.creation_time:
            errors.append("TransmissionWrapper.creation_time is required")
        
        if not self.interaction_id:
            errors.append("TransmissionWrapper.interaction_id is required")
        
        if not self.sender:
            errors.append("TransmissionWrapper.sender is required")
        else:
            sender_errors = self.sender.validate()
            for error in sender_errors:
                errors.append(f"TransmissionWrapper.sender: {error}")
        
        if not self.receiver or len(self.receiver) == 0:
            errors.append("TransmissionWrapper.receiver is required (at least one)")
        else:
            for i, recv in enumerate(self.receiver):
                recv_errors = recv.validate()
                for error in recv_errors:
                    errors.append(f"TransmissionWrapper.receiver[{i}]: {error}")
        
        if not self.control_act_wrapper:
            errors.append("TransmissionWrapper.control_act_wrapper is required")
        else:
            control_act_errors = self.control_act_wrapper.validate()
            for error in control_act_errors:
                errors.append(f"TransmissionWrapper.control_act_wrapper: {error}")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"[{current_time}] Transmission wrapper validation passed")
        else:
            logger.warning(f"[{current_time}] Transmission wrapper validation failed: {len(errors)} errors")
        
        return errors
    
    def get_control_act(self) -> ControlActWrapper:
        """
        Get control act wrapper.
        
        Returns:
            ControlActWrapper object
        """
        return self.control_act_wrapper
    
    def to_xml(self) -> str:
        """
        Serialize to XML.
        
        Returns:
            XML string
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Transmission wrapper XML serialization")
        
        root = ET.Element("transmission")
        root.set("xmlns", HL7V3_NAMESPACE)
        
        # ID
        if self.id:
            id_elem = ET.SubElement(root, "id")
            if self.id.root:
                id_elem.set("root", self.id.root)
            if self.id.extension:
                id_elem.set("extension", self.id.extension)
        
        # Creation time
        if self.creation_time:
            creation_elem = ET.SubElement(root, "creationTime")
            if self.creation_time.value:
                creation_elem.set("value", self.creation_time.value)
        
        # Version code
        if self.version_code:
            version_elem = ET.SubElement(root, "versionCode")
            if self.version_code.code:
                version_elem.set("code", self.version_code.code)
        
        # Interaction ID
        if self.interaction_id:
            interaction_elem = ET.SubElement(root, "interactionId")
            if self.interaction_id.root:
                interaction_elem.set("root", self.interaction_id.root)
            if self.interaction_id.extension:
                interaction_elem.set("extension", self.interaction_id.extension)
        
        # Processing mode code
        if self.processing_mode_code:
            proc_mode_elem = ET.SubElement(root, "processingModeCode")
            if self.processing_mode_code.code:
                proc_mode_elem.set("code", self.processing_mode_code.code)
        
        # Processing code
        if self.processing_code:
            proc_code_elem = ET.SubElement(root, "processingCode")
            if self.processing_code.code:
                proc_code_elem.set("code", self.processing_code.code)
        
        # Processing ID
        if self.processing_id:
            proc_id_elem = ET.SubElement(root, "processingId")
            if self.processing_id.code:
                proc_id_elem.set("code", self.processing_id.code)
        
        # Accept ack code
        if self.accept_ack_code:
            accept_ack_elem = ET.SubElement(root, "acceptAckCode")
            if self.accept_ack_code.code:
                accept_ack_elem.set("code", self.accept_ack_code.code)
        
        # Application ack code
        if self.application_ack_code:
            app_ack_elem = ET.SubElement(root, "applicationAckCode")
            if self.application_ack_code.code:
                app_ack_elem.set("code", self.application_ack_code.code)
        
        # Sender
        if self.sender:
            self.sender.to_xml_element(root, tag_name="sender")
        
        # Receivers
        for recv in self.receiver:
            recv.to_xml_element(root, tag_name="receiver")
        
        # Control act wrapper
        if self.control_act_wrapper:
            # Parse the control act XML and add as sub-element
            control_act_xml = self.control_act_wrapper.to_xml()
            control_act_root = ET.fromstring(control_act_xml)
            # Remove XML declaration if present
            if control_act_root.tag == "controlActProcess":
                root.append(control_act_root)
        
        # Convert to string
        ET.register_namespace("", HL7V3_NAMESPACE)
        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
        
        logger.debug(f"[{current_time}] Transmission wrapper XML serialization completed")
        return xml_str
    
    @classmethod
    def from_xml(cls, xml_string: str) -> "TransmissionWrapper":
        """
        Parse from XML.
        
        Args:
            xml_string: XML string to parse
            
        Returns:
            TransmissionWrapper object
            
        Raises:
            ValueError: If XML is invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Transmission wrapper XML parsing")
        
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        
        if root.tag != "transmission":
            raise ValueError(f"Expected transmission, got {root.tag}")
        
        # Parse ID
        id_elem = root.find(".//{urn:hl7-org:v3}id")
        msg_id = None
        if id_elem is not None:
            msg_id = II(
                root=id_elem.get("root"),
                extension=id_elem.get("extension")
            )
        
        # Parse creation time
        creation_elem = root.find(".//{urn:hl7-org:v3}creationTime")
        creation_time = None
        if creation_elem is not None:
            creation_time = TS(value=creation_elem.get("value"))
        
        # Parse interaction ID
        interaction_elem = root.find(".//{urn:hl7-org:v3}interactionId")
        interaction_id = None
        if interaction_elem is not None:
            interaction_id = II(
                root=interaction_elem.get("root"),
                extension=interaction_elem.get("extension")
            )
        
        # Parse sender (look for direct child first, then anywhere)
        sender_elem = root.find("{urn:hl7-org:v3}sender")
        if sender_elem is None:
            sender_elem = root.find(".//{urn:hl7-org:v3}sender")
        sender = None
        if sender_elem is not None:
            sender = _parse_transmission_party_from_xml(sender_elem)
        
        # Parse receivers (look for direct children first, then anywhere)
        receiver_elems = root.findall("{urn:hl7-org:v3}receiver")
        if not receiver_elems:
            receiver_elems = root.findall(".//{urn:hl7-org:v3}receiver")
        receivers = []
        for recv_elem in receiver_elems:
            recv = _parse_transmission_party_from_xml(recv_elem)
            if recv:
                receivers.append(recv)
        
        # Parse optional fields
        version_elem = root.find(".//{urn:hl7-org:v3}versionCode")
        version_code = None
        if version_elem is not None:
            version_code = CS(code=version_elem.get("code"))
        
        proc_mode_elem = root.find(".//{urn:hl7-org:v3}processingModeCode")
        processing_mode_code = None
        if proc_mode_elem is not None:
            processing_mode_code = CS(code=proc_mode_elem.get("code"))
        
        proc_code_elem = root.find(".//{urn:hl7-org:v3}processingCode")
        processing_code = None
        if proc_code_elem is not None:
            processing_code = CS(code=proc_code_elem.get("code"))
        
        proc_id_elem = root.find(".//{urn:hl7-org:v3}processingId")
        processing_id = None
        if proc_id_elem is not None:
            processing_id = CS(code=proc_id_elem.get("code"))
        
        accept_ack_elem = root.find(".//{urn:hl7-org:v3}acceptAckCode")
        accept_ack_code = None
        if accept_ack_elem is not None:
            accept_ack_code = CS(code=accept_ack_elem.get("code"))
        
        app_ack_elem = root.find(".//{urn:hl7-org:v3}applicationAckCode")
        application_ack_code = None
        if app_ack_elem is not None:
            application_ack_code = CS(code=app_ack_elem.get("code"))
        
        # Parse control act wrapper (look for direct child first, then anywhere)
        control_act_elem = root.find("{urn:hl7-org:v3}controlActProcess")
        if control_act_elem is None:
            control_act_elem = root.find(".//{urn:hl7-org:v3}controlActProcess")
        control_act_wrapper = None
        if control_act_elem is not None:
            control_act_xml = ET.tostring(control_act_elem, encoding="unicode")
            control_act_wrapper = ControlActWrapper.from_xml(control_act_xml)
        
        if not msg_id or not creation_time or not interaction_id or not sender or not control_act_wrapper:
            raise ValueError("Missing required fields in XML")
        
        result = cls(
            id=msg_id,
            creation_time=creation_time,
            interaction_id=interaction_id,
            sender=sender,
            receiver=receivers,
            control_act_wrapper=control_act_wrapper,
            version_code=version_code,
            processing_mode_code=processing_mode_code,
            processing_code=processing_code,
            processing_id=processing_id,
            accept_ack_code=accept_ack_code,
            application_ack_code=application_ack_code
        )
        
        logger.debug(f"[{current_time}] Transmission wrapper XML parsing completed")
        return result



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
# ============================================================================
# Helper Functions
# ============================================================================

def _parse_transmission_party_from_xml(elem: ET.Element) -> Optional[TransmissionParty]:
    """
    Parse TransmissionParty from XML element.
    
    Args:
        elem: XML element
        
    Returns:
        TransmissionParty object or None
    """
    type_elem = elem.find(".//{urn:hl7-org:v3}typeCode")
    type_code = None
    if type_elem is not None:
        type_code = CS(code=type_elem.get("code"))
    
    id_elems = elem.findall(".//{urn:hl7-org:v3}id")
    party_ids = []
    for id_elem in id_elems:
        party_ids.append(II(
            root=id_elem.get("root"),
            extension=id_elem.get("extension")
        ))
    
    name_elem = elem.find(".//{urn:hl7-org:v3}name")
    name = None
    if name_elem is not None and name_elem.text:
        name = name_elem.text
    
    if not type_code or not party_ids:
        return None
    
    return TransmissionParty(
        type_code=type_code,
        id=party_ids,
        name=name
    )
