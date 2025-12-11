# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 ControlAct Wrapper.

Provides ControlAct wrapper classes for HL7 v3 messages including:
- ControlActWrapper - Main control act wrapper class
- Supporting classes for Author, DataEnterer, Informant, Custodian, Subject, QueryEventControl, QueryAcknowledgment
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import xml.etree.ElementTree as ET

from dnhealth.dnhealth_hl7v3.datatypes import II, TS, CS, CE, IVL

logger = logging.getLogger(__name__)

# HL7 v3 namespace
HL7V3_NAMESPACE = "urn:hl7-org:v3"


# ============================================================================
# IVL_TS - Interval of Timestamps
# ============================================================================

@dataclass
class IVL_TS:
    """
    IVL_TS - Interval of Timestamps.
    
    Represents an interval of timestamp values.
    """
    low: Optional[TS] = None  # Lower bound timestamp
    high: Optional[TS] = None  # Upper bound timestamp
    low_closed: Optional[bool] = None  # Is lower bound included?
    high_closed: Optional[bool] = None  # Is upper bound included?
    width: Optional[TS] = None  # Width of interval
    center: Optional[TS] = None  # Center of interval


# ============================================================================
# Author
# ============================================================================

@dataclass
class Author:
    """
    Author - Represents an author of a control act.
    
    Simplified implementation for ControlAct wrapper.
    """
    type_code: Optional[CS] = None  # Author type code
    time: Optional[TS] = None  # Time of authorship
    assigned_author: Optional[Any] = None  # Assigned author entity (simplified)
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "author")
        
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
        
        if self.time:
            time_elem = ET.SubElement(elem, "time")
            if self.time.value:
                time_elem.set("value", self.time.value)
        
        return elem


# ============================================================================
# DataEnterer
# ============================================================================

@dataclass
class DataEnterer:
    """
    DataEnterer - Represents a data enterer of a control act.
    
    Simplified implementation for ControlAct wrapper.
    """
    type_code: Optional[CS] = None  # Data enterer type code
    time: Optional[TS] = None  # Time of data entry
    assigned_data_enterer: Optional[Any] = None  # Assigned data enterer entity (simplified)
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "dataEnterer")
        
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
        
        if self.time:
            time_elem = ET.SubElement(elem, "time")
            if self.time.value:
                time_elem.set("value", self.time.value)
        
        return elem


# ============================================================================
# Informant
# ============================================================================

@dataclass
class Informant:
    """
    Informant - Represents an informant of a control act.
    
    Simplified implementation for ControlAct wrapper.
    """
    type_code: Optional[CS] = None  # Informant type code
    assigned_informant: Optional[Any] = None  # Assigned informant entity (simplified)
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "informant")
        
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
        
        return elem


# ============================================================================
# Custodian
# ============================================================================

@dataclass
class Custodian:
    """
    Custodian - Represents a custodian of a control act.
    
    Simplified implementation for ControlAct wrapper.
    """
    type_code: Optional[CS] = None  # Custodian type code
    assigned_custodian: Optional[Any] = None  # Assigned custodian entity (simplified)
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "custodian")
        
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
        
        return elem


# ============================================================================
# Subject
# ============================================================================

@dataclass
class Subject:
    """
    Subject - Represents a subject of a control act.
    
    Simplified implementation for ControlAct wrapper.
    """
    type_code: Optional[CS] = None  # Subject type code
    registration_event: Optional[Any] = None  # Registration event (simplified)
    related_subject: Optional[Any] = None  # Related subject (simplified)
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "subject")
        
        if self.type_code:
            type_elem = ET.SubElement(elem, "typeCode")
            if self.type_code.code:
                type_elem.set("code", self.type_code.code)
        
        return elem


# ============================================================================
# QueryEventControl
# ============================================================================

@dataclass
class QueryEventControl:
    """
    QueryEventControl - Represents query event control information.
    
    Simplified implementation for ControlAct wrapper.
    """
    query_id: Optional[II] = None  # Query ID
    query_response_mode_code: Optional[CS] = None  # Response mode code
    query_priority_code: Optional[CS] = None  # Priority code
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "queryEventControl")
        
        if self.query_id:
            id_elem = ET.SubElement(elem, "queryId")
            if self.query_id.root:
                id_elem.set("root", self.query_id.root)
            if self.query_id.extension:
                id_elem.set("extension", self.query_id.extension)
        
        if self.query_response_mode_code:
            mode_elem = ET.SubElement(elem, "queryResponseModeCode")
            if self.query_response_mode_code.code:
                mode_elem.set("code", self.query_response_mode_code.code)
        
        if self.query_priority_code:
            priority_elem = ET.SubElement(elem, "queryPriorityCode")
            if self.query_priority_code.code:
                priority_elem.set("code", self.query_priority_code.code)
        
        return elem


# ============================================================================
# QueryAcknowledgment
# ============================================================================

@dataclass
class QueryAcknowledgment:
    """
    QueryAcknowledgment - Represents query acknowledgment information.
    
    Simplified implementation for ControlAct wrapper.
    """
    query_response_code: Optional[CS] = None  # Response code
    result_current_quantity: Optional[int] = None  # Current result quantity
    result_remaining_quantity: Optional[int] = None  # Remaining result quantity
    
    def to_xml_element(self, parent: ET.Element) -> ET.Element:
        """
        Convert to XML Element.
        
        Args:
            parent: Parent element
            
        Returns:
            XML Element
        """
        elem = ET.SubElement(parent, "queryAcknowledgment")
        
        if self.query_response_code:
            code_elem = ET.SubElement(elem, "queryResponseCode")
            if self.query_response_code.code:
                code_elem.set("code", self.query_response_code.code)
        
        if self.result_current_quantity is not None:
            qty_elem = ET.SubElement(elem, "resultCurrentQuantity")
            qty_elem.set("value", str(self.result_current_quantity))
        
        if self.result_remaining_quantity is not None:
            rem_elem = ET.SubElement(elem, "resultRemainingQuantity")
            rem_elem.set("value", str(self.result_remaining_quantity))
        
        return elem


# ============================================================================
# ControlAct Wrapper
# ============================================================================

@dataclass
class ControlActWrapper:
    """
    ControlActWrapper - Control Act Wrapper for HL7 v3 messages.
    
    Attributes per HL7 v3 ControlAct specification:
    - class_code: CS - Class code (required, typically "CACT")
    - mood_code: CS - Mood code (required, typically "EVN")
    - code: CE - Control act code (required)
    - effective_time: IVL_TS - Effective time (optional)
    - reason: List[CE] - Reasons (optional)
    - author: List[Author] - Authors (optional)
    - data_enterer: List[DataEnterer] - Data enterers (optional)
    - informant: List[Informant] - Informants (optional)
    - custodian: List[Custodian] - Custodians (optional)
    - subject: List[Subject] - Subjects (required, at least one)
    - query_event_control: QueryEventControl - Query event control (optional)
    - query_acknowledgment: QueryAcknowledgment - Query acknowledgment (optional)
    """
    class_code: CS  # Required
    mood_code: CS  # Required
    code: CE  # Required
    subject: List[Subject] = field(default_factory=list)  # Required, at least one
    effective_time: Optional[IVL_TS] = None  # Optional
    reason: List[CE] = field(default_factory=list)  # Optional
    author: List[Author] = field(default_factory=list)  # Optional
    data_enterer: List[DataEnterer] = field(default_factory=list)  # Optional
    informant: List[Informant] = field(default_factory=list)  # Optional
    custodian: List[Custodian] = field(default_factory=list)  # Optional
    query_event_control: Optional[QueryEventControl] = None  # Optional
    query_acknowledgment: Optional[QueryAcknowledgment] = None  # Optional
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    def validate(self) -> List[str]:
        """
        Validate wrapper structure.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting ControlAct wrapper validation")
        
        if not self.class_code:
            errors.append("ControlActWrapper.class_code is required")
        
        if not self.mood_code:
            errors.append("ControlActWrapper.mood_code is required")
        
        if not self.code:
            errors.append("ControlActWrapper.code is required")
        
        if not self.subject or len(self.subject) == 0:
            errors.append("ControlActWrapper.subject is required (at least one)")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"[{current_time}] ControlAct wrapper validation passed")
        else:
            logger.warning(f"[{current_time}] ControlAct wrapper validation failed: {len(errors)} errors")
        
        return errors
    
    def get_subject(self) -> List[Subject]:
        """
        Get subjects.
        
        Returns:

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            List of subjects
        """
        return self.subject
    
    def add_subject(self, subject: Subject) -> None:
        """
        Add subject.
        
        Args:
            subject: Subject to add
        """
        self.subject.append(subject)
    
    def to_xml(self) -> str:
        """
        Serialize to XML with proper namespace.
        
        Returns:
            XML string
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting ControlAct wrapper XML serialization")
        
        root = ET.Element("controlActProcess")
        root.set("xmlns", HL7V3_NAMESPACE)
        
        # Class code
        if self.class_code:
            class_elem = ET.SubElement(root, "classCode")
            if self.class_code.code:
                class_elem.set("code", self.class_code.code)
        
        # Mood code
        if self.mood_code:
            mood_elem = ET.SubElement(root, "moodCode")
            if self.mood_code.code:
                mood_elem.set("code", self.mood_code.code)
        
        # Code
        if self.code:
            code_elem = ET.SubElement(root, "code")
            if self.code.code:
                code_elem.set("code", self.code.code)
            if self.code.code_system:
                code_elem.set("codeSystem", self.code.code_system)
            if self.code.display_name:
                code_elem.set("displayName", self.code.display_name)
        
        # Effective time
        if self.effective_time:
            eff_time_elem = ET.SubElement(root, "effectiveTime")
            if self.effective_time.low:
                low_elem = ET.SubElement(eff_time_elem, "low")
                if self.effective_time.low.value:
                    low_elem.set("value", self.effective_time.low.value)
            if self.effective_time.high:
                high_elem = ET.SubElement(eff_time_elem, "high")
                if self.effective_time.high.value:
                    high_elem.set("value", self.effective_time.high.value)
        
        # Reasons
        for reason in self.reason:
            reason_elem = ET.SubElement(root, "reasonCode")
            if reason.code:
                reason_elem.set("code", reason.code)
            if reason.code_system:
                reason_elem.set("codeSystem", reason.code_system)
        
        # Authors
        for author in self.author:
            author.to_xml_element(root)
        
        # Data enterers
        for data_enterer in self.data_enterer:
            data_enterer.to_xml_element(root)
        
        # Informants
        for informant in self.informant:
            informant.to_xml_element(root)
        
        # Custodians
        for custodian in self.custodian:
            custodian.to_xml_element(root)
        
        # Subjects
        for subject in self.subject:
            subject.to_xml_element(root)
        
        # Query event control
        if self.query_event_control:
            self.query_event_control.to_xml_element(root)
        
        # Query acknowledgment
        if self.query_acknowledgment:
            self.query_acknowledgment.to_xml_element(root)
        
        # Convert to string
        ET.register_namespace("", HL7V3_NAMESPACE)
        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
        
        logger.debug(f"[{current_time}] ControlAct wrapper XML serialization completed")
        return xml_str
    
    @classmethod
    def from_xml(cls, xml_string: str) -> "ControlActWrapper":
        """
        Parse from XML.
        
        Args:
            xml_string: XML string to parse
            
        Returns:
            ControlActWrapper object
            
        Raises:
            ValueError: If XML is invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting ControlAct wrapper XML parsing")
        
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        
        if root.tag != "controlActProcess":
            raise ValueError(f"Expected controlActProcess, got {root.tag}")
        
        # Parse class code
        class_elem = root.find(".//{urn:hl7-org:v3}classCode")
        class_code = None
        if class_elem is not None:
            class_code = CS(code=class_elem.get("code"))
        
        # Parse mood code
        mood_elem = root.find(".//{urn:hl7-org:v3}moodCode")
        mood_code = None
        if mood_elem is not None:
            mood_code = CS(code=mood_elem.get("code"))
        
        # Parse code
        code_elem = root.find(".//{urn:hl7-org:v3}code")
        code = None
        if code_elem is not None:
            code = CE(
                code=code_elem.get("code"),
                code_system=code_elem.get("codeSystem"),
                display_name=code_elem.get("displayName")
            )
        
        # Parse effective time
        eff_time_elem = root.find(".//{urn:hl7-org:v3}effectiveTime")
        effective_time = None
        if eff_time_elem is not None:
            from dnhealth.dnhealth_hl7v3.datatypes import TS
            low_elem = eff_time_elem.find(".//{urn:hl7-org:v3}low")
            high_elem = eff_time_elem.find(".//{urn:hl7-org:v3}high")
            low_ts = None
            high_ts = None
            if low_elem is not None:
                low_ts = TS(value=low_elem.get("value"))
            if high_elem is not None:
                high_ts = TS(value=high_elem.get("value"))
            if low_ts or high_ts:
                effective_time = IVL_TS(low=low_ts, high=high_ts)
        
        # Parse reasons
        reason_elems = root.findall(".//{urn:hl7-org:v3}reasonCode")
        reasons = []
        for reason_elem in reason_elems:
            reasons.append(CE(
                code=reason_elem.get("code"),
                code_system=reason_elem.get("codeSystem")
            ))
        
        # Parse subjects
        subject_elems = root.findall(".//{urn:hl7-org:v3}subject")
        subjects = []
        for subject_elem in subject_elems:
            type_elem = subject_elem.find(".//{urn:hl7-org:v3}typeCode")
            type_code = None
            if type_elem is not None:
                type_code = CS(code=type_elem.get("code"))
            subjects.append(Subject(type_code=type_code))
        
        if not class_code or not mood_code or not code or not subjects:
            raise ValueError("Missing required fields in XML")
        
        result = cls(
            class_code=class_code,
            mood_code=mood_code,
            code=code,
            subject=subjects,
            effective_time=effective_time,
            reason=reasons
        )
        
        logger.debug(f"[{current_time}] ControlAct wrapper XML parsing completed")
        return result
