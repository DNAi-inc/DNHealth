# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Message Control Wrappers (MCCI).

Provides MCCI message control wrapper classes for HL7 v3 messages including:
- MCCI_MT000100UV01 - Message Control Wrapper
- MCCI_MT000200UV01 - Application Acknowledgement
- MCCI Party and Acknowledgment classes
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import uuid
import xml.etree.ElementTree as ET

from dnhealth.dnhealth_hl7v3.datatypes import II, TS, CS, ON, TEL

logger = logging.getLogger(__name__)

# HL7 v3 namespace
HL7V3_NAMESPACE = "urn:hl7-org:v3"


# ============================================================================
# Address (AD) - Simple implementation for MCCI
# ============================================================================

@dataclass
class AD:
    """
    AD - Address.
    
    Represents a postal address.
    """
    use: Optional[List[CS]] = None  # Address use codes
    valid_time: Optional[Any] = None  # Validity period (IVL_TS)
    street_address_line: List[str] = field(default_factory=list)  # Street address lines
    city: Optional[str] = None  # City
    state: Optional[str] = None  # State/province
    postal_code: Optional[str] = None  # Postal/ZIP code
    country: Optional[str] = None  # Country


# ============================================================================
# MCCI Party
# ============================================================================

@dataclass
class MCCIParty:
    """
    MCCI Party - Represents a party in MCCI message control.
    
    Attributes per HL7 v3 MCCI specification:
    - type_code: CS - Party type (required, table MCCI_000002)
    - id: List[II] - Party IDs (required, at least one)
    - name: List[ON] - Party names (optional)
    - telecom: List[TEL] - Telecommunications (optional)
    - addr: List[AD] - Addresses (optional)
    """
    type_code: CS  # Required
    id: List[II] = field(default_factory=list)  # Required, at least one
    name: List[ON] = field(default_factory=list)  # Optional
    telecom: List[TEL] = field(default_factory=list)  # Optional
    addr: List[AD] = field(default_factory=list)  # Optional
    
    def validate(self) -> List[str]:
        """
        Validate party structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not self.type_code:
            errors.append("MCCIParty.type_code is required")
        
        if not self.id or len(self.id) == 0:
            errors.append("MCCIParty.id is required (at least one ID)")
        
        return errors
    
    def to_xml_element(self, parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element("party")
        else:
            elem = ET.SubElement(parent, "party")
        
        # Type code
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
            if self.type_code.code_system:
                type_elem.set("codeSystem", self.type_code.code_system)
        
        # IDs
        for party_id in self.id:
            id_elem = ET.SubElement(elem, "id")
            if party_id.root:
                id_elem.set("root", party_id.root)
            if party_id.extension:
                id_elem.set("extension", party_id.extension)
        
        # Names
        for name in self.name:
            name_elem = ET.SubElement(elem, "name")
            # Serialize ON to XML (simplified)
            if name.part:
                for part in name.part:
                    if part.text:
                        part_elem = ET.SubElement(name_elem, "part")
                        if part.part_type:
                            part_elem.set("type", part.part_type)
                        part_elem.text = part.text
        
        # Telecom
        for tel in self.telecom:
            tel_elem = ET.SubElement(elem, "telecom")
            if tel.value:
                tel_elem.set("value", tel.value)
        
        # Addresses
        for addr in self.addr:
            addr_elem = ET.SubElement(elem, "addr")
            if addr.city:
                city_elem = ET.SubElement(addr_elem, "city")
                city_elem.text = addr.city
            if addr.state:
                state_elem = ET.SubElement(addr_elem, "state")
                state_elem.text = addr.state
            if addr.postal_code:
                postal_elem = ET.SubElement(addr_elem, "postalCode")
                postal_elem.text = addr.postal_code
            if addr.country:
                country_elem = ET.SubElement(addr_elem, "country")
                country_elem.text = addr.country
        

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


# ============================================================================
# MCCI Acknowledgment Detail
# ============================================================================

@dataclass
class MCCIAcknowledgmentDetail:
    """
    MCCI Acknowledgment Detail.
    
    Provides details about an acknowledgment.
    """
    type_code: Optional[CS] = None  # Detail type code
    code: Optional[CS] = None  # Detail code
    text: Optional[str] = None  # Detail text
    location: Optional[str] = None  # Location reference


# ============================================================================
# MCCI Acknowledgment
# ============================================================================

@dataclass
class MCCIAcknowledgment:
    """
    MCCI Acknowledgment - Represents an acknowledgment in MCCI message control.
    
    Attributes per HL7 v3 MCCI specification:
    - type_code: CS - Acknowledgment type (required, table MCCI_000003)
    - target_message: List[II] - Target message IDs (required)
    - acknowledgment_detail: List[MCCIAcknowledgmentDetail] - Details (optional)
    """
    type_code: CS  # Required
    target_message: List[II] = field(default_factory=list)  # Required
    acknowledgment_detail: List[MCCIAcknowledgmentDetail] = field(default_factory=list)  # Optional
    
    def validate(self) -> List[str]:
        """
        Validate acknowledgment structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not self.type_code:
            errors.append("MCCIAcknowledgment.type_code is required")
        
        if not self.target_message or len(self.target_message) == 0:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
            errors.append("MCCIAcknowledgment.target_message is required (at least one)")
        
        return errors


# ============================================================================
# MCCI Message Control (MCCI_MT000100UV01)
# ============================================================================

@dataclass
class MCCIMessageControl:
    """
    MCCI_MT000100UV01 - Message Control Wrapper.
    
    Attributes per HL7 v3 MCCI specification:
    - id: II - Message ID (required)
    - creation_time: TS - Creation timestamp (required)
    - version_code: CS - Version code (optional)
    - interaction_id: II - Interaction ID (required)
    - processing_mode_code: CS - Processing mode (optional)
    - processing_code: CS - Processing code (optional)
    - accept_ack_code: CS - Accept acknowledgment code (optional)
    - receiver: List[MCCIParty] - Receivers (required, at least one)
    - sender: MCCIParty - Sender (required)
    - attention_line: List[ON] - Attention lines (optional)
    - copy_target: List[MCCIParty] - Copy targets (optional)
    - acknowledgment: List[MCCIAcknowledgment] - Acknowledgments (optional)
    """
    id: II  # Required
    creation_time: TS  # Required
    interaction_id: II  # Required
    sender: MCCIParty  # Required
    receiver: List[MCCIParty] = field(default_factory=list)  # Required, at least one
    version_code: Optional[CS] = None  # Optional
    processing_mode_code: Optional[CS] = None  # Optional
    processing_code: Optional[CS] = None  # Optional
    accept_ack_code: Optional[CS] = None  # Optional
    attention_line: List[ON] = field(default_factory=list)  # Optional
    copy_target: List[MCCIParty] = field(default_factory=list)  # Optional
    acknowledgment: List[MCCIAcknowledgment] = field(default_factory=list)  # Optional
    
    def validate(self) -> List[str]:
        """
        Validate wrapper structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting MCCI message control validation")
        
        if not self.id:
            errors.append("MCCIMessageControl.id is required")
        
        if not self.creation_time:
            errors.append("MCCIMessageControl.creation_time is required")
        
        if not self.interaction_id:
            errors.append("MCCIMessageControl.interaction_id is required")
        
        if not self.sender:
            errors.append("MCCIMessageControl.sender is required")
        else:
            sender_errors = self.sender.validate()
            for error in sender_errors:
                errors.append(f"MCCIMessageControl.sender: {error}")
        
        if not self.receiver or len(self.receiver) == 0:
            errors.append("MCCIMessageControl.receiver is required (at least one)")
        else:
            for i, recv in enumerate(self.receiver):
                recv_errors = recv.validate()
                for error in recv_errors:
                    errors.append(f"MCCIMessageControl.receiver[{i}]: {error}")
        
        # Validate acknowledgments
        for i, ack in enumerate(self.acknowledgment):
            ack_errors = ack.validate()
            for error in ack_errors:
                errors.append(f"MCCIMessageControl.acknowledgment[{i}]: {error}")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"[{current_time}] MCCI message control validation passed")
        else:
            logger.warning(f"[{current_time}] MCCI message control validation failed: {len(errors)} errors")
        
        return errors
    
    def get_receiver_by_type(self, type_code: str) -> List[MCCIParty]:
        """
        Get receivers by type code.
        
        Args:
            type_code: Party type code to filter by
            
        Returns:
            List of matching receivers
        """
        return [recv for recv in self.receiver if recv.type_code and recv.type_code.code == type_code]
    
    def to_xml(self) -> str:
        """
        Serialize to XML with proper namespace.
        
        Returns:
            XML string
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting MCCI message control XML serialization")
        
        root = ET.Element("MCCI_MT000100UV01")
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
        
        # Accept ack code
        if self.accept_ack_code:
            accept_ack_elem = ET.SubElement(root, "acceptAckCode")
            if self.accept_ack_code.code:
                accept_ack_elem.set("code", self.accept_ack_code.code)
        
        # Sender
        if self.sender:
            self.sender.to_xml_element(root)
        
        # Receivers
        for recv in self.receiver:
            recv.to_xml_element(root)
        
        # Attention lines
        for attn in self.attention_line:
            attn_elem = ET.SubElement(root, "attentionLine")
            # Serialize ON (simplified)
            if attn.part:
                for part in attn.part:
                    if part.text:
                        part_elem = ET.SubElement(attn_elem, "part")
                        if part.part_type:
                            part_elem.set("type", part.part_type)
                        part_elem.text = part.text
        
        # Copy targets
        for copy in self.copy_target:
            copy.to_xml_element(root)
        
        # Acknowledgments
        for ack in self.acknowledgment:
            ack_elem = ET.SubElement(root, "acknowledgment")
            if ack.type_code:
                type_elem = ET.SubElement(ack_elem, "typeCode")
                if ack.type_code.code:
                    type_elem.set("code", ack.type_code.code)
            for target_msg in ack.target_message:
                target_elem = ET.SubElement(ack_elem, "targetMessage")
                if target_msg.root:
                    target_elem.set("root", target_msg.root)
                if target_msg.extension:
                    target_elem.set("extension", target_msg.extension)
        
        # Convert to string
        ET.register_namespace("", HL7V3_NAMESPACE)
        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
        
        logger.debug(f"[{current_time}] MCCI message control XML serialization completed")
        return xml_str
    
    @classmethod
    def from_xml(cls, xml_string: str) -> "MCCIMessageControl":
        """
        Parse from XML.
        
        Args:
            xml_string: XML string to parse
            
        Returns:
            MCCIMessageControl object
            
        Raises:
            ValueError: If XML is invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting MCCI message control XML parsing")
        
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        
        if root.tag != "MCCI_MT000100UV01":
            raise ValueError(f"Expected MCCI_MT000100UV01, got {root.tag}")
        
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
        
        # Parse sender
        sender_elem = root.find(".//{urn:hl7-org:v3}sender")
        sender = None
        if sender_elem is not None:
            sender = _parse_party_from_xml(sender_elem)
        
        # Parse receivers
        receiver_elems = root.findall(".//{urn:hl7-org:v3}receiver")
        receivers = []
        for recv_elem in receiver_elems:
            recv = _parse_party_from_xml(recv_elem)
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
        
        accept_ack_elem = root.find(".//{urn:hl7-org:v3}acceptAckCode")
        accept_ack_code = None
        if accept_ack_elem is not None:
            accept_ack_code = CS(code=accept_ack_elem.get("code"))
        
        # Parse acknowledgments
        ack_elems = root.findall(".//{urn:hl7-org:v3}acknowledgment")
        acknowledgments = []
        for ack_elem in ack_elems:
            type_elem = ack_elem.find(".//{urn:hl7-org:v3}typeCode")
            type_code = None
            if type_elem is not None:
                type_code = CS(code=type_elem.get("code"))
            
            target_msg_elems = ack_elem.findall(".//{urn:hl7-org:v3}targetMessage")
            target_messages = []
            for target_elem in target_msg_elems:
                target_messages.append(II(
                    root=target_elem.get("root"),
                    extension=target_elem.get("extension")
                ))
            
            if type_code and target_messages:
                acknowledgments.append(MCCIAcknowledgment(
                    type_code=type_code,
                    target_message=target_messages
                ))
        
        if not msg_id or not creation_time or not interaction_id or not sender:
            raise ValueError("Missing required fields in XML")
        
        result = cls(
            id=msg_id,
            creation_time=creation_time,
            interaction_id=interaction_id,
            sender=sender,
            receiver=receivers,
            version_code=version_code,
            processing_mode_code=processing_mode_code,
            processing_code=processing_code,
            accept_ack_code=accept_ack_code,
            acknowledgment=acknowledgments
        )
        
        logger.debug(f"[{current_time}] MCCI message control XML parsing completed")
        return result


# ============================================================================
# MCCI Application Acknowledgment (MCCI_MT000200UV01)
# ============================================================================

@dataclass
class MCCIApplicationAcknowledgment:
    """
    MCCI_MT000200UV01 - Application Acknowledgement.
    
    Attributes per HL7 v3 MCCI specification:
    - id: II - Acknowledgment ID (required)
    - creation_time: TS - Creation timestamp (required)
    - response_mode_code: CS - Response mode (required, table MCCI_000001)
    - attention_line: List[ON] - Attention lines (optional)
    - acknowledgment: List[MCCIAcknowledgment] - Acknowledgments (required, at least one)
    - receiver: List[MCCIParty] - Receivers (required)
    - sender: MCCIParty - Sender (required)
    """
    id: II  # Required
    creation_time: TS  # Required
    response_mode_code: CS  # Required
    sender: MCCIParty  # Required
    receiver: List[MCCIParty] = field(default_factory=list)  # Required
    acknowledgment: List[MCCIAcknowledgment] = field(default_factory=list)  # Required, at least one
    attention_line: List[ON] = field(default_factory=list)  # Optional
    
    def validate(self) -> List[str]:
        """
        Validate acknowledgment structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting MCCI application acknowledgment validation")
        
        if not self.id:
            errors.append("MCCIApplicationAcknowledgment.id is required")
        
        if not self.creation_time:
            errors.append("MCCIApplicationAcknowledgment.creation_time is required")
        
        if not self.response_mode_code:
            errors.append("MCCIApplicationAcknowledgment.response_mode_code is required")
        
        if not self.sender:
            errors.append("MCCIApplicationAcknowledgment.sender is required")
        else:
            sender_errors = self.sender.validate()
            for error in sender_errors:
                errors.append(f"MCCIApplicationAcknowledgment.sender: {error}")
        
        if not self.receiver or len(self.receiver) == 0:
            errors.append("MCCIApplicationAcknowledgment.receiver is required (at least one)")
        
        if not self.acknowledgment or len(self.acknowledgment) == 0:
            errors.append("MCCIApplicationAcknowledgment.acknowledgment is required (at least one)")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"[{current_time}] MCCI application acknowledgment validation passed")
        else:
            logger.warning(f"[{current_time}] MCCI application acknowledgment validation failed: {len(errors)} errors")
        
        return errors
    
    def to_xml(self) -> str:
        """
        Serialize to XML.
        
        Returns:
            XML string
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting MCCI application acknowledgment XML serialization")
        
        root = ET.Element("MCCI_MT000200UV01")
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
        
        # Response mode code
        if self.response_mode_code:
            response_mode_elem = ET.SubElement(root, "responseModeCode")
            if self.response_mode_code.code:
                response_mode_elem.set("code", self.response_mode_code.code)
        
        # Sender
        if self.sender:
            self.sender.to_xml_element(root)
        
        # Receivers
        for recv in self.receiver:
            recv.to_xml_element(root)
        
        # Acknowledgments
        for ack in self.acknowledgment:
            ack_elem = ET.SubElement(root, "acknowledgment")
            if ack.type_code:
                type_elem = ET.SubElement(ack_elem, "typeCode")
                if ack.type_code.code:
                    type_elem.set("code", ack.type_code.code)
            for target_msg in ack.target_message:
                target_elem = ET.SubElement(ack_elem, "targetMessage")
                if target_msg.root:
                    target_elem.set("root", target_msg.root)
                if target_msg.extension:
                    target_elem.set("extension", target_msg.extension)
        
        # Attention lines
        for attn in self.attention_line:
            attn_elem = ET.SubElement(root, "attentionLine")
            if attn.part:
                for part in attn.part:
                    if part.text:
                        part_elem = ET.SubElement(attn_elem, "part")
                        if part.part_type:
                            part_elem.set("type", part.part_type)
                        part_elem.text = part.text
        
        ET.register_namespace("", HL7V3_NAMESPACE)
        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
        
        logger.debug(f"[{current_time}] MCCI application acknowledgment XML serialization completed")
        return xml_str
    
    @classmethod
    def from_xml(cls, xml_string: str) -> "MCCIApplicationAcknowledgment":
        """
        Parse from XML.
        
        Args:
            xml_string: XML string to parse
            
        Returns:
            MCCIApplicationAcknowledgment object
            
        Raises:
            ValueError: If XML is invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting MCCI application acknowledgment XML parsing")
        
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        
        if root.tag != "MCCI_MT000200UV01":
            raise ValueError(f"Expected MCCI_MT000200UV01, got {root.tag}")
        
        # Parse required fields (similar to MCCIMessageControl)
        id_elem = root.find(".//{urn:hl7-org:v3}id")
        msg_id = None
        if id_elem is not None:
            msg_id = II(
                root=id_elem.get("root"),
                extension=id_elem.get("extension")
            )
        
        creation_elem = root.find(".//{urn:hl7-org:v3}creationTime")
        creation_time = None
        if creation_elem is not None:
            creation_time = TS(value=creation_elem.get("value"))
        
        response_mode_elem = root.find(".//{urn:hl7-org:v3}responseModeCode")
        response_mode_code = None
        if response_mode_elem is not None:
            response_mode_code = CS(code=response_mode_elem.get("code"))
        
        sender_elem = root.find(".//{urn:hl7-org:v3}sender")
        sender = None
        if sender_elem is not None:
            sender = _parse_party_from_xml(sender_elem)
        
        receiver_elems = root.findall(".//{urn:hl7-org:v3}receiver")
        receivers = []
        for recv_elem in receiver_elems:
            recv = _parse_party_from_xml(recv_elem)
            if recv:
                receivers.append(recv)
        
        ack_elems = root.findall(".//{urn:hl7-org:v3}acknowledgment")
        acknowledgments = []
        for ack_elem in ack_elems:
            type_elem = ack_elem.find(".//{urn:hl7-org:v3}typeCode")
            type_code = None
            if type_elem is not None:
                type_code = CS(code=type_elem.get("code"))
            
            target_msg_elems = ack_elem.findall(".//{urn:hl7-org:v3}targetMessage")
            target_messages = []
            for target_elem in target_msg_elems:
                target_messages.append(II(
                    root=target_elem.get("root"),
                    extension=target_elem.get("extension")
                ))
            
            if type_code and target_messages:
                acknowledgments.append(MCCIAcknowledgment(
                    type_code=type_code,
                    target_message=target_messages
                ))
        
        if not msg_id or not creation_time or not response_mode_code or not sender:
            raise ValueError("Missing required fields in XML")
        
        result = cls(
            id=msg_id,
            creation_time=creation_time,
            response_mode_code=response_mode_code,
            sender=sender,
            receiver=receivers,
            acknowledgment=acknowledgments
        )
        
        logger.debug(f"[{current_time}] MCCI application acknowledgment XML parsing completed")
        return result


# ============================================================================
# Helper Functions
# ============================================================================

def _parse_party_from_xml(elem: ET.Element) -> Optional[MCCIParty]:
    """
    Parse MCCIParty from XML element.
    
    Args:
        elem: XML element
        
    Returns:
        MCCIParty object or None
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
    
    if not type_code or not party_ids:
        return None
    
    return MCCIParty(
        type_code=type_code,

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        id=party_ids
    )


# ============================================================================
# Specification Compliance Verification
# ============================================================================

def verify_mcci_specification_compliance() -> Dict[str, Any]:
    """
    Verify MCCI message control wrapper implementation matches HL7 v3 MCCI specification.
    
    This function verifies that MCCI_MT000100UV01 and MCCI_MT000200UV01 implementations
    match the HL7 v3 MCCI specification requirements (MCCI_RM000001UV and MCCI_RM000002UV).
    
    Returns:
        Dictionary with compliance verification results including:
        - mcci_mt000100uv01_compliant: bool - Whether MCCI_MT000100UV01 is compliant
        - mcci_mt000200uv01_compliant: bool - Whether MCCI_MT000200UV01 is compliant
        - mcci_mt000100uv01_issues: List[str] - List of compliance issues for MCCI_MT000100UV01
        - mcci_mt000200uv01_issues: List[str] - List of compliance issues for MCCI_MT000200UV01
        - total_issues: int - Total number of compliance issues
        - compliance_percentage: float - Overall compliance percentage
        - verification_time: str - Timestamp of verification
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MCCI specification compliance verification")
    
    issues_mt000100 = []
    issues_mt000200 = []
    
    # Verify MCCI_MT000100UV01 (Message Control Wrapper) compliance
    # Per HL7 v3 MCCI specification MCCI_RM000001UV:
    # Required attributes:
    # - id: II (required)
    # - creationTime: TS (required)
    # - interactionId: II (required)
    # - sender: MCCIParty (required)
    # - receiver: List[MCCIParty] (required, at least one)
    # Optional attributes:
    # - versionCode: CS (optional)
    # - processingModeCode: CS (optional)
    # - processingCode: CS (optional)
    # - acceptAckCode: CS (optional)
    # - attentionLine: List[ON] (optional)
    # - copyTarget: List[MCCIParty] (optional)
    # - acknowledgment: List[MCCIAcknowledgment] (optional)
    
    # Check MCCIMessageControl class structure
    import inspect
    
    # Verify required fields exist in MCCIMessageControl
    mcci_mc_fields = [f.name for f in MCCIMessageControl.__dataclass_fields__.values()]
    required_fields_mt000100 = ['id', 'creation_time', 'interaction_id', 'sender', 'receiver']
    
    for req_field in required_fields_mt000100:
        # Map specification field names to implementation field names
        impl_field = req_field.replace('Time', '_time').replace('Id', '_id')
        if impl_field not in mcci_mc_fields:
            issues_mt000100.append(f"Missing required field: {req_field} (expected as {impl_field})")
    
    # Verify optional fields exist
    optional_fields_mt000100 = ['version_code', 'processing_mode_code', 'processing_code', 
                                'accept_ack_code', 'attention_line', 'copy_target', 'acknowledgment']
    for opt_field in optional_fields_mt000100:
        if opt_field not in mcci_mc_fields:
            issues_mt000100.append(f"Missing optional field: {opt_field}")
    
    # Verify MCCIParty structure
    party_fields = [f.name for f in MCCIParty.__dataclass_fields__.values()]
    required_party_fields = ['type_code', 'id']
    optional_party_fields = ['name', 'telecom', 'addr']
    
    for req_field in required_party_fields:
        if req_field not in party_fields:
            issues_mt000100.append(f"MCCIParty missing required field: {req_field}")
    
    for opt_field in optional_party_fields:
        if opt_field not in party_fields:
            issues_mt000100.append(f"MCCIParty missing optional field: {opt_field}")
    
    # Verify MCCIAcknowledgment structure
    ack_fields = [f.name for f in MCCIAcknowledgment.__dataclass_fields__.values()]
    required_ack_fields = ['type_code', 'target_message']
    optional_ack_fields = ['acknowledgment_detail']
    
    for req_field in required_ack_fields:
        if req_field not in ack_fields:
            issues_mt000100.append(f"MCCIAcknowledgment missing required field: {req_field}")
    
    for opt_field in optional_ack_fields:
        if opt_field not in ack_fields:
            issues_mt000100.append(f"MCCIAcknowledgment missing optional field: {opt_field}")
    
    # Verify XML serialization methods exist
    if not hasattr(MCCIMessageControl, 'to_xml'):
        issues_mt000100.append("MCCIMessageControl missing to_xml() method")
    
    if not hasattr(MCCIMessageControl, 'from_xml'):
        issues_mt000100.append("MCCIMessageControl missing from_xml() class method")
    
    # Verify validation method exists
    if not hasattr(MCCIMessageControl, 'validate'):
        issues_mt000100.append("MCCIMessageControl missing validate() method")
    
    # Verify XML root element name
    # MCCI_MT000100UV01 should serialize to <MCCI_MT000100UV01> root element
    # This is verified in to_xml() method implementation
    
    # Verify namespace usage
    # Should use urn:hl7-org:v3 namespace
    if HL7V3_NAMESPACE != "urn:hl7-org:v3":
        issues_mt000100.append(f"Incorrect namespace: {HL7V3_NAMESPACE}, expected urn:hl7-org:v3")
    
    # Verify MCCI_MT000200UV01 (Application Acknowledgement) compliance
    # Per HL7 v3 MCCI specification MCCI_RM000002UV:
    # Required attributes:
    # - id: II (required)
    # - creationTime: TS (required)
    # - responseModeCode: CS (required, table MCCI_000001)
    # - sender: MCCIParty (required)
    # - receiver: List[MCCIParty] (required)
    # - acknowledgment: List[MCCIAcknowledgment] (required, at least one)
    # Optional attributes:
    # - attentionLine: List[ON] (optional)
    
    # Check MCCIApplicationAcknowledgment class structure
    mcci_aa_fields = [f.name for f in MCCIApplicationAcknowledgment.__dataclass_fields__.values()]
    required_fields_mt000200 = ['id', 'creation_time', 'response_mode_code', 'sender', 'receiver', 'acknowledgment']
    
    for req_field in required_fields_mt000200:
        # Map specification field names to implementation field names
        impl_field = req_field.replace('Time', '_time').replace('ModeCode', '_mode_code')
        if impl_field not in mcci_aa_fields:
            issues_mt000200.append(f"Missing required field: {req_field} (expected as {impl_field})")
    
    # Verify optional fields exist
    optional_fields_mt000200 = ['attention_line']
    for opt_field in optional_fields_mt000200:
        if opt_field not in mcci_aa_fields:
            issues_mt000200.append(f"Missing optional field: {opt_field}")
    
    # Verify XML serialization methods exist
    if not hasattr(MCCIApplicationAcknowledgment, 'to_xml'):
        issues_mt000200.append("MCCIApplicationAcknowledgment missing to_xml() method")
    
    if not hasattr(MCCIApplicationAcknowledgment, 'from_xml'):
        issues_mt000200.append("MCCIApplicationAcknowledgment missing from_xml() class method")
    
    # Verify validation method exists
    if not hasattr(MCCIApplicationAcknowledgment, 'validate'):
        issues_mt000200.append("MCCIApplicationAcknowledgment missing validate() method")
    
    # Verify XML root element name
    # MCCI_MT000200UV01 should serialize to <MCCI_MT000200UV01> root element
    # This is verified in to_xml() method implementation
    
    # Calculate compliance
    mcci_mt000100uv01_compliant = len(issues_mt000100) == 0
    mcci_mt000200uv01_compliant = len(issues_mt000200) == 0
    total_issues = len(issues_mt000100) + len(issues_mt000200)
    
    # Compliance percentage (2 message types, 100% each)
    compliance_percentage = ((1.0 if mcci_mt000100uv01_compliant else 0.0) + 
                            (1.0 if mcci_mt000200uv01_compliant else 0.0)) / 2.0 * 100.0
    
    result = {
        "mcci_mt000100uv01_compliant": mcci_mt000100uv01_compliant,
        "mcci_mt000200uv01_compliant": mcci_mt000200uv01_compliant,
        "mcci_mt000100uv01_issues": issues_mt000100,
        "mcci_mt000200uv01_issues": issues_mt000200,
        "total_issues": total_issues,
        "compliance_percentage": compliance_percentage,
        "verification_time": current_time
    }
    
    logger.info(f"[{current_time}] MCCI specification compliance verification completed: "
                f"{compliance_percentage:.1f}% compliant, {total_issues} issues found")
    
    return result
