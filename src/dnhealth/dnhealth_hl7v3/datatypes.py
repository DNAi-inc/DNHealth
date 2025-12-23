# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 data types implementation.

Provides all standard HL7 v3 data types including primitive types
and complex types as specified in the HL7 v3 specification.
Enhanced with XML serialization and deserialization support.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import xml.etree.ElementTree as ET
import base64
import time
import logging

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


# ============================================================================
# Primitive Types
# ============================================================================

class ANY:
    """
    ANY - Any type.
    
    Represents any HL7 v3 data type.
    """
    def __init__(self, value: Any = None):
        """Initialize ANY type."""
        self.value = value
    
    def __repr__(self) -> str:
        return f"ANY({self.value})"
    
    def to_xml_element(self, element_name: str = "any", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "any")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        # Serialize value if it has to_xml_element method
        if hasattr(self.value, 'to_xml_element'):
            child = self.value.to_xml_element(element_name="value", parent=elem)
        elif self.value is not None:
            elem.text = str(self.value)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "any") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "any")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "ANY":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            ANY instance
        """
        value = xml_element.text if xml_element.text else None
        return cls(value=value)


class BL:
    """
    BL - Boolean.
    
    Represents a boolean value (true/false).
    """
    def __init__(self, value: Optional[bool] = None):
        """Initialize boolean type."""
        self.value = value
    
    def __bool__(self) -> bool:
        return bool(self.value) if self.value is not None else False
    
    def __repr__(self) -> str:
        return f"BL({self.value})"
    
    def to_xml_element(self, element_name: str = "bl", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "bl")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            elem.set("value", "true" if self.value else "false")
        

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "bl") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "bl")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "BL":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            BL instance
        """
        value_str = xml_element.get("value") or xml_element.text
        if value_str:
            value = value_str.lower() in ("true", "1", "yes")
        else:
            value = None
        return cls(value=value)


class BN:
    """
    BN - Boolean Non-Null.
    
    Represents a boolean value that cannot be null.
    """
    def __init__(self, value: bool):
        """Initialize boolean non-null type."""
        if value is None:
            raise ValueError("BN cannot be None")
        self.value = value
    
    def __bool__(self) -> bool:
        return self.value
    
    def __repr__(self) -> str:
        return f"BN({self.value})"
    
    def to_xml_element(self, element_name: str = "bn", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "bn")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        elem.set("value", "true" if self.value else "false")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return elem
    
    def to_xml(self, element_name: str = "bn") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "bn")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "BN":
        """
        Deserialize from XML Element.

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            BN instance
        """
        value_str = xml_element.get("value") or xml_element.text
        if value_str:
            value = value_str.lower() in ("true", "1", "yes")
        else:
            raise ValueError("BN cannot be None")

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(value=value)


class BAG:
    """
    BAG - Bag (unordered collection).
    
    Represents an unordered collection of items.
    """
    def __init__(self, items: Optional[List[Any]] = None):
        """Initialize bag type."""
        self.items = items or []
    
    def add(self, item: Any) -> None:
        """Add item to bag."""
        self.items.append(item)
    
    def __repr__(self) -> str:
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return f"BAG({len(self.items)} items)"
    
    def to_xml_element(self, element_name: str = "bag", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "bag")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element(element_name="item", parent=elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "bag") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "bag")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "BAG":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            BAG instance
        """
        items = []
        for item_elem in xml_element.findall("item"):
            # Try to parse as data type if possible
            if item_elem.text:
                items.append(item_elem.text)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(items=items)


class LIST:
    """
    LIST - List (ordered collection).
    
    Represents an ordered collection of items.
    """
    def __init__(self, items: Optional[List[Any]] = None):
        """Initialize list type."""
        self.items = items or []
    
    def add(self, item: Any) -> None:
        """Add item to list."""
        self.items.append(item)
    
    def __getitem__(self, index: int) -> Any:
        return self.items[index]
    
    def __repr__(self) -> str:
        return f"LIST({len(self.items)} items)"
    
    def to_xml_element(self, element_name: str = "list", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "list")
            parent: Optional parent element
            
        Returns:
            XML Element

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element(element_name="item", parent=elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "list") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "list")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "LIST":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            LIST instance
        """
        items = []
        for item_elem in xml_element.findall("item"):
            if item_elem.text:
                items.append(item_elem.text)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(items=items)


class SET:
    """
    SET - Set (unordered collection with unique items).
    
    Represents an unordered collection of unique items.
    """
    def __init__(self, items: Optional[List[Any]] = None):
        """Initialize set type."""
        self.items = list(set(items)) if items else []
    
    def add(self, item: Any) -> None:
        """Add item to set (if not already present)."""
        if item not in self.items:
            self.items.append(item)
    
    def __repr__(self) -> str:
        return f"SET({len(self.items)} items)"
    
    def to_xml_element(self, element_name: str = "set", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "set")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element(element_name="item", parent=elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        return elem
    
    def to_xml(self, element_name: str = "set") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "set")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "SET":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            SET instance
        """
        items = []
        for item_elem in xml_element.findall("item"):
            if item_elem.text:
                items.append(item_elem.text)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(items=items)


# ============================================================================
# Complex Types
# ============================================================================

def _serialize_coded_type_to_xml(
    elem: ET.Element,
    code: Optional[str] = None,
    code_system: Optional[str] = None,
    code_system_name: Optional[str] = None,
    code_system_version: Optional[str] = None,
    display_name: Optional[str] = None,
    original_text: Optional[str] = None
) -> None:
    """
    Helper function to serialize coded type attributes to XML element.
    
    Args:
        elem: XML element to add attributes to
        code: Code value
        code_system: Code system
        code_system_name: Code system name
        code_system_version: Code system version
        display_name: Display name
        original_text: Original text
    """
    if code is not None:
        elem.set("code", code)
    if code_system is not None:
        elem.set("codeSystem", code_system)
    if code_system_name is not None:
        elem.set("codeSystemName", code_system_name)
    if code_system_version is not None:
        elem.set("codeSystemVersion", code_system_version)
    if display_name is not None:
        elem.set("displayName", display_name)
    if original_text is not None:
        orig_elem = ET.SubElement(elem, "originalText")
        orig_elem.text = original_text


@dataclass
class CD:
    """
    CD - Concept Descriptor.
    
    Represents a coded concept with optional qualifiers.
    """
    code: Optional[str] = None
    code_system: Optional[str] = None
    code_system_name: Optional[str] = None
    code_system_version: Optional[str] = None
    display_name: Optional[str] = None
    original_text: Optional[str] = None
    qualifier: List["CD"] = field(default_factory=list)
    translation: List["CD"] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "cd", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "cd")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        _serialize_coded_type_to_xml(
            elem,
            self.code,
            self.code_system,
            self.code_system_name,
            self.code_system_version,
            self.display_name,
            self.original_text
        )
        
        # Serialize qualifiers
        for qual in self.qualifier:

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            qual.to_xml_element(element_name="qualifier", parent=elem)
        
        # Serialize translations
        for trans in self.translation:
            trans.to_xml_element(element_name="translation", parent=elem)
        

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "cd") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "cd")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "CD":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
        Returns:
            CD instance
        """
        code = xml_element.get("code")
        code_system = xml_element.get("codeSystem")
        code_system_name = xml_element.get("codeSystemName")

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        code_system_version = xml_element.get("codeSystemVersion")
        display_name = xml_element.get("displayName")
        
        original_text_elem = xml_element.find("originalText")
        original_text = original_text_elem.text if original_text_elem is not None else None
        
        qualifiers = []
        for qual_elem in xml_element.findall("qualifier"):
            qualifiers.append(CD.from_xml(qual_elem))
        
        translations = []
        for trans_elem in xml_element.findall("translation"):
            translations.append(CD.from_xml(trans_elem))
        

        return cls(
            code=code,
            code_system=code_system,
            code_system_name=code_system_name,
            code_system_version=code_system_version,
            display_name=display_name,
            original_text=original_text,
            qualifier=qualifiers,
            translation=translations
        )


@dataclass
class CE:
    """
    CE - Coded Element.
    
    Represents a coded value with code system.
    """
    code: Optional[str] = None
    code_system: Optional[str] = None
    code_system_name: Optional[str] = None
    code_system_version: Optional[str] = None
    display_name: Optional[str] = None
    original_text: Optional[str] = None
    
    def to_xml_element(self, element_name: str = "ce", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        _serialize_coded_type_to_xml(elem, self.code, self.code_system, self.code_system_name,
                                     self.code_system_version, self.display_name, self.original_text)
        return elem
    
    def to_xml(self, element_name: str = "ce") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "CE":
        """Deserialize from XML Element."""
        original_text_elem = xml_element.find("originalText")

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(
            code=xml_element.get("code"),
            code_system=xml_element.get("codeSystem"),
            code_system_name=xml_element.get("codeSystemName"),
            code_system_version=xml_element.get("codeSystemVersion"),
            display_name=xml_element.get("displayName"),
            original_text=original_text_elem.text if original_text_elem is not None else None
        )


@dataclass
class CS:
    """
    CS - Coded Simple Value.
    
    Represents a simple coded value.
    """
    code: Optional[str] = None
    
    def to_xml_element(self, element_name: str = "cs", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.code is not None:
            elem.set("code", self.code)
        return elem
    
    def to_xml(self, element_name: str = "cs") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "CS":
        """Deserialize from XML Element."""
        return cls(code=xml_element.get("code") or xml_element.text)


@dataclass
class CV:
    """
    CV - Coded Value.
    
    Represents a coded value (similar to CE but simpler).
    """
    code: Optional[str] = None
    code_system: Optional[str] = None
    code_system_name: Optional[str] = None
    code_system_version: Optional[str] = None
    display_name: Optional[str] = None
    original_text: Optional[str] = None
    
    def to_xml_element(self, element_name: str = "cv", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        _serialize_coded_type_to_xml(elem, self.code, self.code_system, self.code_system_name,
                                     self.code_system_version, self.display_name, self.original_text)
        return elem
    
    def to_xml(self, element_name: str = "cv") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "CV":
        """Deserialize from XML Element."""
        original_text_elem = xml_element.find("originalText")

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(
            code=xml_element.get("code"),
            code_system=xml_element.get("codeSystem"),
            code_system_name=xml_element.get("codeSystemName"),
            code_system_version=xml_element.get("codeSystemVersion"),
            display_name=xml_element.get("displayName"),
            original_text=original_text_elem.text if original_text_elem is not None else None
        )


@dataclass
class ED:
    """
    ED - Encapsulated Data.
    
    Represents binary or text data.
    """
    media_type: Optional[str] = None  # MIME type
    charset: Optional[str] = None
    language: Optional[str] = None
    compression: Optional[str] = None
    reference: Optional[str] = None  # URI reference
    integrity_check: Optional[str] = None  # Base64 encoded
    integrity_check_algorithm: Optional[str] = None
    data: Optional[bytes] = None  # Base64 encoded data
    text: Optional[str] = None  # Plain text data
    
    def to_xml_element(self, element_name: str = "ed", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.media_type:
            elem.set("mediaType", self.media_type)
        if self.charset:
            elem.set("charset", self.charset)
        if self.language:
            elem.set("language", self.language)
        if self.compression:
            elem.set("compression", self.compression)
        if self.reference:
            elem.set("reference", self.reference)
        if self.integrity_check:
            elem.set("integrityCheck", self.integrity_check)
        if self.integrity_check_algorithm:
            elem.set("integrityCheckAlgorithm", self.integrity_check_algorithm)
        if self.data:
            data_elem = ET.SubElement(elem, "data")
            data_elem.text = base64.b64encode(self.data).decode('utf-8')
        if self.text:
            text_elem = ET.SubElement(elem, "text")
            text_elem.text = self.text
        return elem
    
    def to_xml(self, element_name: str = "ed") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "ED":
        """Deserialize from XML Element."""
        data_elem = xml_element.find("data")
        data = None
        if data_elem is not None and data_elem.text:
            data = base64.b64decode(data_elem.text)
        text_elem = xml_element.find("text")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return cls(
            media_type=xml_element.get("mediaType"),
            charset=xml_element.get("charset"),
            language=xml_element.get("language"),
            compression=xml_element.get("compression"),
            reference=xml_element.get("reference"),
            integrity_check=xml_element.get("integrityCheck"),
            integrity_check_algorithm=xml_element.get("integrityCheckAlgorithm"),
            data=data,
            text=text_elem.text if text_elem is not None else None
        )


@dataclass
class EIVL:
    """
    EIVL - Event-related Interval.
    
    Represents an interval related to an event.
    """
    event: Optional[CS] = None  # Event code
    offset: Optional["IVL"] = None  # Offset interval
    width: Optional["IVL"] = None  # Width interval
    
    def to_xml_element(self, element_name: str = "eivl", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.event:
            self.event.to_xml_element(element_name="event", parent=elem)
        if self.offset:
            self.offset.to_xml_element(element_name="offset", parent=elem)
        if self.width:
            self.width.to_xml_element(element_name="width", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "eivl") -> str:
        """Serialize to XML string."""

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "EIVL":
        """Deserialize from XML Element."""
        event_elem = xml_element.find("event")
        event = CS.from_xml(event_elem) if event_elem is not None else None
        offset_elem = xml_element.find("offset")
        offset = IVL.from_xml(offset_elem) if offset_elem is not None else None

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        width_elem = xml_element.find("width")
        width = IVL.from_xml(width_elem) if width_elem is not None else None
        return cls(event=event, offset=offset, width=width)


@dataclass
class EN:
    """
    EN - Entity Name.
    
    Represents a name with parts.
    """
    use: Optional[List[CS]] = None  # Name use codes
    valid_time: Optional["IVL"] = None  # Validity period
    part: List["ENXP"] = field(default_factory=list)  # Name parts
    
    def to_xml_element(self, element_name: str = "en", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.use:
            for use_code in self.use:
                use_code.to_xml_element(element_name="use", parent=elem)
        if self.valid_time:
            self.valid_time.to_xml_element(element_name="validTime", parent=elem)
        for part in self.part:
            part.to_xml_element(element_name="part", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "en") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "EN":
        """Deserialize from XML Element."""
        uses = []
        for use_elem in xml_element.findall("use"):
            uses.append(CS.from_xml(use_elem))
        
        valid_time_elem = xml_element.find("validTime")
        valid_time = IVL.from_xml(valid_time_elem) if valid_time_elem is not None else None
        parts = []
        for part_elem in xml_element.findall("part"):
            parts.append(ENXP.from_xml(part_elem))
        return cls(use=uses if uses else None, valid_time=valid_time, part=parts)


@dataclass
class ENXP:
    """
    ENXP - Entity Name Part.
    
    Represents a part of an entity name.
    """
    part_type: Optional[str] = None  # Type of name part
    qualifier: Optional[List[CS]] = None  # Qualifiers
    text: Optional[str] = None  # Text content
    
    def to_xml_element(self, element_name: str = "part", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.part_type:
            elem.set("type", self.part_type)
        if self.qualifier:
            for qual in self.qualifier:
                qual.to_xml_element(element_name="qualifier", parent=elem)
        if self.text:
            elem.text = self.text
        return elem
    
    def to_xml(self, element_name: str = "part") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "ENXP":
        """Deserialize from XML Element."""
        qualifiers = []
        for qual_elem in xml_element.findall("qualifier"):
            qualifiers.append(CS.from_xml(qual_elem))

        result = cls(
            part_type=xml_element.get("type"),
            qualifier=qualifiers if qualifiers else None,
            text=xml_element.text
        )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result


@dataclass
class GTS:
    """
    GTS - General Timing Specification.
    
    Represents a timing specification.
    """
    value: Optional[str] = None  # Timing expression (e.g., "R2/2008-03-01T13:00:00Z/P1Y2M10DT2H30M")
    
    def to_xml_element(self, element_name: str = "gts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value:
            elem.set("value", self.value)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "gts") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "GTS":
        """Deserialize from XML Element."""

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return cls(value=xml_element.get("value") or xml_element.text)


@dataclass
class II:
    """
    II - Instance Identifier.
    
    Represents a unique identifier.
    """
    root: Optional[str] = None  # Root OID or UUID
    extension: Optional[str] = None  # Extension value
    assigning_authority_name: Optional[str] = None
    displayable: Optional[bool] = None
    
    def to_xml_element(self, element_name: str = "id", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.root is not None:
            elem.set("root", self.root)
        if self.extension is not None:
            elem.set("extension", self.extension)
        if self.assigning_authority_name is not None:
            elem.set("assigningAuthorityName", self.assigning_authority_name)
        if self.displayable is not None:
            elem.set("displayable", "true" if self.displayable else "false")
        return elem
    
    def to_xml(self, element_name: str = "id") -> str:
        """Serialize to XML string."""

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "II":
        """Deserialize from XML Element."""
        displayable_str = xml_element.get("displayable")
        displayable = None
        if displayable_str:
            displayable = displayable_str.lower() in ("true", "1", "yes")
        return cls(
            root=xml_element.get("root"),
            extension=xml_element.get("extension"),
            assigning_authority_name=xml_element.get("assigningAuthorityName"),
            displayable=displayable
        )


@dataclass
class INT:
    """
    INT - Integer Number.
    
    Represents an integer value.
    """
    value: Optional[int] = None
    
    def __int__(self) -> int:
        return self.value if self.value is not None else 0
    
    def to_xml_element(self, element_name: str = "int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", str(self.value))
        return elem
    
    def to_xml(self, element_name: str = "int") -> str:
        """Serialize to XML string."""

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "INT":
        """Deserialize from XML Element."""
        value_str = xml_element.get("value") or xml_element.text
        value = int(value_str) if value_str else None
        return cls(value=value)


@dataclass
class IVL:
    """
    IVL - Interval.
    
    Represents an interval of values.
    """
    low: Optional[Any] = None  # Lower bound
    high: Optional[Any] = None  # Upper bound
    low_closed: Optional[bool] = None  # Is lower bound included?
    high_closed: Optional[bool] = None  # Is upper bound included?
    width: Optional[Any] = None  # Width of interval
    center: Optional[Any] = None  # Center of interval
    
    def to_xml_element(self, element_name: str = "ivl", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.low is not None:
            low_elem = ET.SubElement(elem, "low")
            if hasattr(self.low, 'to_xml_element'):
                self.low.to_xml_element(element_name="value", parent=low_elem)
            else:
                low_elem.set("value", str(self.low))
            if self.low_closed is not None:
                low_elem.set("inclusive", "true" if self.low_closed else "false")
        if self.high is not None:
            high_elem = ET.SubElement(elem, "high")
            if hasattr(self.high, 'to_xml_element'):
                self.high.to_xml_element(element_name="value", parent=high_elem)
            else:
                high_elem.set("value", str(self.high))
            if self.high_closed is not None:
                high_elem.set("inclusive", "true" if self.high_closed else "false")
        if self.width is not None:
            width_elem = ET.SubElement(elem, "width")
            if hasattr(self.width, 'to_xml_element'):
                self.width.to_xml_element(element_name="value", parent=width_elem)
            else:
                width_elem.set("value", str(self.width))
        if self.center is not None:
            center_elem = ET.SubElement(elem, "center")
            if hasattr(self.center, 'to_xml_element'):
                self.center.to_xml_element(element_name="value", parent=center_elem)
            else:
                center_elem.set("value", str(self.center))
        return elem
    
    def to_xml(self, element_name: str = "ivl") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "IVL":
        """Deserialize from XML Element."""
        low_elem = xml_element.find("low")
        low = None
        low_closed = None
        if low_elem is not None:
            low = low_elem.get("value") or low_elem.text
            inclusive = low_elem.get("inclusive")
            low_closed = inclusive.lower() == "true" if inclusive else None
        high_elem = xml_element.find("high")
        high = None
        high_closed = None
        if high_elem is not None:
            high = high_elem.get("value") or high_elem.text
            inclusive = high_elem.get("inclusive")
            high_closed = inclusive.lower() == "true" if inclusive else None
        width_elem = xml_element.find("width")
        width = width_elem.get("value") or width_elem.text if width_elem is not None else None
        center_elem = xml_element.find("center")
        center = center_elem.get("value") or center_elem.text if center_elem is not None else None
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return cls(low=low, high=high, low_closed=low_closed, high_closed=high_closed, width=width, center=center)


@dataclass
class MO:
    """
    MO - Money.
    
    Represents a monetary amount.
    """
    value: Optional[float] = None
    currency: Optional[str] = None  # ISO 4217 currency code
    
    def to_xml_element(self, element_name: str = "mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", str(self.value))
        if self.currency:
            elem.set("currency", self.currency)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return elem
    
    def to_xml(self, element_name: str = "mo") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "MO":
        """Deserialize from XML Element."""
        value_str = xml_element.get("value") or xml_element.text
        value = float(value_str) if value_str else None
        return cls(value=value, currency=xml_element.get("currency"))


@dataclass
class ON:
    """
    ON - Organization Name.
    
    Represents an organization name.
    """
    use: Optional[List[CS]] = None  # Name use codes
    valid_time: Optional[IVL] = None  # Validity period
    part: List[ENXP] = field(default_factory=list)  # Name parts
    
    def to_xml_element(self, element_name: str = "on", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.use:
            for use_code in self.use:
                use_code.to_xml_element(element_name="use", parent=elem)
        if self.valid_time:
            self.valid_time.to_xml_element(element_name="validTime", parent=elem)
        for part in self.part:
            part.to_xml_element(element_name="part", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "on") -> str:
        """Serialize to XML string."""

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "ON":
        """Deserialize from XML Element."""
        uses = []
        for use_elem in xml_element.findall("use"):
            uses.append(CS.from_xml(use_elem))
        valid_time_elem = xml_element.find("validTime")
        valid_time = IVL.from_xml(valid_time_elem) if valid_time_elem is not None else None
        parts = []
        for part_elem in xml_element.findall("part"):
            parts.append(ENXP.from_xml(part_elem))
        return cls(use=uses if uses else None, valid_time=valid_time, part=parts)


@dataclass
class PIVL:
    """
    PIVL - Periodic Interval.
    
    Represents a periodic interval.
    """
    phase: Optional[IVL] = None  # Phase interval
    period: Optional["PQ"] = None  # Period quantity
    frequency: Optional[INT] = None  # Frequency
    alignment: Optional[CS] = None  # Alignment code
    
    def to_xml_element(self, element_name: str = "pivl", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.phase:
            self.phase.to_xml_element(element_name="phase", parent=elem)
        if self.period:
            self.period.to_xml_element(element_name="period", parent=elem)
        if self.frequency:
            self.frequency.to_xml_element(element_name="frequency", parent=elem)
        if self.alignment:
            self.alignment.to_xml_element(element_name="alignment", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "pivl") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "PIVL":
        """Deserialize from XML Element."""
        phase_elem = xml_element.find("phase")
        phase = IVL.from_xml(phase_elem) if phase_elem is not None else None
        period_elem = xml_element.find("period")
        period = PQ.from_xml(period_elem) if period_elem is not None else None
        frequency_elem = xml_element.find("frequency")
        frequency = INT.from_xml(frequency_elem) if frequency_elem is not None else None
        alignment_elem = xml_element.find("alignment")
        alignment = CS.from_xml(alignment_elem) if alignment_elem is not None else None
        return cls(phase=phase, period=period, frequency=frequency, alignment=alignment)


@dataclass
class PN:
    """
    PN - Person Name.
    
    Represents a person's name.
    """
    use: Optional[List[CS]] = None  # Name use codes
    valid_time: Optional[IVL] = None  # Validity period
    part: List[ENXP] = field(default_factory=list)  # Name parts
    
    def to_xml_element(self, element_name: str = "pn", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        if self.use:
            for use_code in self.use:
                use_code.to_xml_element(element_name="use", parent=elem)
        if self.valid_time:
            self.valid_time.to_xml_element(element_name="validTime", parent=elem)
        for part in self.part:
            part.to_xml_element(element_name="part", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "pn") -> str:
        """Serialize to XML string."""
        result = ET.tostring(self.to_xml_element(element_name), encoding="unicode")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "PN":
        """Deserialize from XML Element."""
        uses = []
        for use_elem in xml_element.findall("use"):
            uses.append(CS.from_xml(use_elem))
        valid_time_elem = xml_element.find("validTime")
        valid_time = IVL.from_xml(valid_time_elem) if valid_time_elem is not None else None
        parts = []

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        for part_elem in xml_element.findall("part"):
            parts.append(ENXP.from_xml(part_elem))
        return cls(use=uses if uses else None, valid_time=valid_time, part=parts)


@dataclass
class PQ:
    """
    PQ - Physical Quantity.
    
    Represents a physical quantity with units.
    """
    value: Optional[float] = None
    unit: Optional[str] = None  # Unit code
    translation: Optional[List["PQ"]] = None  # Translated quantities
    
    def to_xml_element(self, element_name: str = "pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", str(self.value))
        if self.unit:
            elem.set("unit", self.unit)
        if self.translation:
            for trans in self.translation:
                trans.to_xml_element(element_name="translation", parent=elem)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "pq") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "PQ":
        """Deserialize from XML Element."""
        value_str = xml_element.get("value") or xml_element.text
        value = float(value_str) if value_str else None
        translations = []

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        for trans_elem in xml_element.findall("translation"):
            translations.append(PQ.from_xml(trans_elem))
        return cls(value=value, unit=xml_element.get("unit"), translation=translations if translations else None)


@dataclass
class QTY:
    """
    QTY - Quantity.
    
    Base class for quantity types.
    """
    value: Optional[float] = None
    
    def to_xml_element(self, element_name: str = "qty", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", str(self.value))
        return elem
    
    def to_xml(self, element_name: str = "qty") -> str:
        """Serialize to XML string."""
        result = ET.tostring(self.to_xml_element(element_name), encoding="unicode")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "QTY":
        """Deserialize from XML Element."""
        value_str = xml_element.get("value") or xml_element.text
        value = float(value_str) if value_str else None
        return cls(value=value)


@dataclass
class REAL:
    """
    REAL - Real Number.
    
    Represents a real (floating-point) number.
    """
    value: Optional[float] = None
    
    def __float__(self) -> float:
        return self.value if self.value is not None else 0.0
    
    def to_xml_element(self, element_name: str = "real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", str(self.value))

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "real") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "REAL":
        """Deserialize from XML Element."""
        value_str = xml_element.get("value") or xml_element.text
        value = float(value_str) if value_str else None
        return cls(value=value)


@dataclass
class RTO:
    """
    RTO - Ratio.
    
    Represents a ratio of two quantities.
    """
    numerator: Optional[QTY] = None
    denominator: Optional[QTY] = None
    
    def to_xml_element(self, element_name: str = "rto", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.numerator:
            self.numerator.to_xml_element(element_name="numerator", parent=elem)
        if self.denominator:
            self.denominator.to_xml_element(element_name="denominator", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "rto") -> str:
        """Serialize to XML string."""
        result = ET.tostring(self.to_xml_element(element_name), encoding="unicode")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "RTO":
        """Deserialize from XML Element."""
        num_elem = xml_element.find("numerator")
        numerator = QTY.from_xml(num_elem) if num_elem is not None else None
        den_elem = xml_element.find("denominator")
        denominator = QTY.from_xml(den_elem) if den_elem is not None else None
        return cls(numerator=numerator, denominator=denominator)


@dataclass
class SC:
    """
    SC - String Coded.
    
    Represents a coded string value.
    """
    code: Optional[str] = None
    code_system: Optional[str] = None
    code_system_name: Optional[str] = None
    code_system_version: Optional[str] = None
    display_name: Optional[str] = None
    original_text: Optional[str] = None
    
    def to_xml_element(self, element_name: str = "sc", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        _serialize_coded_type_to_xml(elem, self.code, self.code_system, self.code_system_name,
                                     self.code_system_version, self.display_name, self.original_text)
        return elem
    
    def to_xml(self, element_name: str = "sc") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "SC":
        """Deserialize from XML Element."""
        original_text_elem = xml_element.find("originalText")
        return cls(
            code=xml_element.get("code"),
            code_system=xml_element.get("codeSystem"),
            code_system_name=xml_element.get("codeSystemName"),
            code_system_version=xml_element.get("codeSystemVersion"),
            display_name=xml_element.get("displayName"),
            original_text=original_text_elem.text if original_text_elem is not None else None
        )


@dataclass
class ST:
    """
    ST - String.
    
    Represents a character string.
    """
    value: Optional[str] = None
    language: Optional[str] = None  # Language code
    
    def __str__(self) -> str:
        return self.value if self.value is not None else ""
    
    def __repr__(self) -> str:
        return f"ST('{self.value}')"
    
    def to_xml_element(self, element_name: str = "st", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.language is not None:
            elem.set("language", self.language)
        if self.value is not None:
            elem.text = self.value

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "st") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "ST":
        """Deserialize from XML Element."""
        return cls(value=xml_element.text, language=xml_element.get("language"))


@dataclass
class TEL:
    """
    TEL - Telecommunication Address.
    
    Represents a telecommunication address (phone, email, etc.).
    """
    value: Optional[str] = None  # Address value
    use: Optional[List[CS]] = None  # Use codes
    useable_period: Optional[IVL] = None  # Usable period
    
    def to_xml_element(self, element_name: str = "tel", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value:
            elem.set("value", self.value)
        if self.use:
            for use_code in self.use:
                use_code.to_xml_element(element_name="use", parent=elem)
        if self.useable_period:
            self.useable_period.to_xml_element(element_name="useablePeriod", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "tel") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "TEL":
        """Deserialize from XML Element."""
        uses = []
        for use_elem in xml_element.findall("use"):
            uses.append(CS.from_xml(use_elem))
        period_elem = xml_element.find("useablePeriod")
        period = IVL.from_xml(period_elem) if period_elem is not None else None
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return cls(value=xml_element.get("value"), use=uses if uses else None, useable_period=period)


@dataclass
class TS:
    """
    TS - Time Stamp.
    
    Represents a point in time.
    """
    value: Optional[str] = None  # ISO 8601 timestamp
    
    def to_datetime(self) -> Optional[datetime]:
        """
        Convert to Python datetime object.
        
        Returns:
            datetime object or None
        """
        if self.value:
            try:
                # Try parsing ISO 8601 format
                return datetime.fromisoformat(self.value.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return None
        return None
    
    def to_xml_element(self, element_name: str = "ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", self.value)
        return elem
    
    def to_xml(self, element_name: str = "ts") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "TS":
        """Deserialize from XML Element."""
        return cls(value=xml_element.get("value") or xml_element.text)


@dataclass
class URL:
    """
    URL - Universal Resource Locator.
    
    Represents a URL.
    """
    value: Optional[str] = None  # URL string
    
    def to_xml_element(self, element_name: str = "url", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value:
            elem.set("value", self.value)
        return elem
    
    def to_xml(self, element_name: str = "url") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "URL":
        """Deserialize from XML Element."""
        return cls(value=xml_element.get("value") or xml_element.text)


@dataclass
class UVP:
    """
    UVP - Uncertain Value Probabilistic.
    
    Represents a value with uncertainty.
    """
    value: Optional[float] = None
    probability: Optional[float] = None  # Probability (0.0 to 1.0)
    distribution_type: Optional[str] = None  # Distribution type
    
    def to_xml_element(self, element_name: str = "uvp", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            elem.set("value", str(self.value))
        if self.probability is not None:
            elem.set("probability", str(self.probability))
        if self.distribution_type:
            elem.set("distributionType", self.distribution_type)
        return elem
    
    def to_xml(self, element_name: str = "uvp") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "UVP":
        """Deserialize from XML Element."""
        value_str = xml_element.get("value")
        value = float(value_str) if value_str else None
        prob_str = xml_element.get("probability")
        prob = float(prob_str) if prob_str else None
        return cls(value=value, probability=prob, distribution_type=xml_element.get("distributionType"))


@dataclass
class ADXP:
    """
    ADXP - Address Part.
    
    Represents a part of an address (e.g., street name, building number, etc.).
    Can be used independently or as part of AD (Address).
    """
    def __init__(
        self,
        value: Optional[str] = None,
        part_type: Optional[str] = None,  # Type of address part (e.g., "SAL", "BNR", "BNN", etc.)
        qualifier: Optional[List[CS]] = None
    ):
        """
        Initialize ADXP.
        
        Args:
            value: The address part value
            part_type: Type of address part (e.g., "SAL" for salutation, "BNR" for building number range)
            qualifier: Optional qualifiers for the address part
        """
        self.value = value
        self.part_type = part_type
        self.qualifier = qualifier or []
    
    def __repr__(self) -> str:
        return f"ADXP(value={self.value}, part_type={self.part_type})"
    
    def to_xml_element(self, element_name: str = "addrPart", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "addrPart")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.part_type:
            elem.set("partType", self.part_type)
        
        if self.value:
            elem.text = str(self.value)
        
        if self.qualifier:
            for qual in self.qualifier:
                qual.to_xml_element(element_name="qualifier", parent=elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    def to_xml(self, element_name: str = "addrPart") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "addrPart")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "ADXP":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            ADXP instance
        """
        value = xml_element.text if xml_element.text else None
        part_type = xml_element.get("partType")
        qualifiers = []
        for qual_elem in xml_element.findall("qualifier"):
            qualifiers.append(CS.from_xml(qual_elem))
        return cls(
            value=value,
            part_type=part_type,
            qualifier=qualifiers if qualifiers else None
        )


class AD:
    """
    AD - Address.
    
    Represents a postal address.
    """
    use: Optional[List[CS]] = None  # Address use codes (e.g., H, HP, HV, WP)
    valid_time: Optional[IVL] = None  # Validity period
    street_address_line: Optional[List[ST]] = None  # Street address lines
    city: Optional[ST] = None  # City name
    state: Optional[ST] = None  # State or province
    postal_code: Optional[ST] = None  # Postal/ZIP code
    country: Optional[ST] = None  # Country code
    county: Optional[ST] = None  # County or parish
    census_tract: Optional[List[ST]] = None  # Census tract
    
    def to_xml_element(self, element_name: str = "addr", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.use:
            for use_code in self.use:
                use_code.to_xml_element(element_name="use", parent=elem)
        if self.valid_time:
            self.valid_time.to_xml_element(element_name="validTime", parent=elem)
        if self.street_address_line:
            for street in self.street_address_line:
                street.to_xml_element(element_name="streetAddressLine", parent=elem)
        if self.city:
            self.city.to_xml_element(element_name="city", parent=elem)
        if self.state:
            self.state.to_xml_element(element_name="state", parent=elem)
        if self.postal_code:
            self.postal_code.to_xml_element(element_name="postalCode", parent=elem)
        if self.country:
            self.country.to_xml_element(element_name="country", parent=elem)
        if self.county:
            self.county.to_xml_element(element_name="county", parent=elem)
        if self.census_tract:
            for tract in self.census_tract:
                tract.to_xml_element(element_name="censusTract", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "addr") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "AD":
        """Deserialize from XML Element."""
        uses = []
        for use_elem in xml_element.findall("use"):
            uses.append(CS.from_xml(use_elem))
        valid_time_elem = xml_element.find("validTime")
        valid_time = IVL.from_xml(valid_time_elem) if valid_time_elem is not None else None
        street_lines = []
        for street_elem in xml_element.findall("streetAddressLine"):
            street_lines.append(ST.from_xml(street_elem))
        city_elem = xml_element.find("city")
        city = ST.from_xml(city_elem) if city_elem is not None else None
        state_elem = xml_element.find("state")
        state = ST.from_xml(state_elem) if state_elem is not None else None
        postal_elem = xml_element.find("postalCode")
        postal_code = ST.from_xml(postal_elem) if postal_elem is not None else None
        country_elem = xml_element.find("country")
        country = ST.from_xml(country_elem) if country_elem is not None else None
        county_elem = xml_element.find("county")
        county = ST.from_xml(county_elem) if county_elem is not None else None
        census_tracts = []
        for tract_elem in xml_element.findall("censusTract"):
            census_tracts.append(ST.from_xml(tract_elem))
        return cls(
            use=uses if uses else None,
            valid_time=valid_time,
            street_address_line=street_lines if street_lines else None,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            county=county,
            census_tract=census_tracts if census_tracts else None
        )


@dataclass
class CO:
    """
    CO - Coded Ordinal.
    
    Represents a coded value with an ordinal position.
    """
    code: Optional[str] = None
    code_system: Optional[str] = None
    code_system_name: Optional[str] = None
    code_system_version: Optional[str] = None
    display_name: Optional[str] = None
    original_text: Optional[str] = None
    value: Optional[int] = None  # Ordinal value
    
    def to_xml_element(self, element_name: str = "co", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        _serialize_coded_type_to_xml(elem, self.code, self.code_system, self.code_system_name,
                                     self.code_system_version, self.display_name, self.original_text)
        if self.value is not None:
            elem.set("value", str(self.value))
        return elem
    
    def to_xml(self, element_name: str = "co") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "CO":
        """Deserialize from XML Element."""
        original_text_elem = xml_element.find("originalText")
        value_str = xml_element.get("value")
        value = int(value_str) if value_str else None
        return cls(
            code=xml_element.get("code"),
            code_system=xml_element.get("codeSystem"),
            code_system_name=xml_element.get("codeSystemName"),
            code_system_version=xml_element.get("codeSystemVersion"),
            display_name=xml_element.get("displayName"),
            original_text=original_text_elem.text if original_text_elem is not None else None,
            value=value
        )


@dataclass
class CR:
    """
    CR - Coded Ratio.
    
    Represents a ratio with coded numerator and denominator.
    """
    numerator: Optional[CD] = None  # Coded numerator
    denominator: Optional[CD] = None  # Coded denominator
    
    def to_xml_element(self, element_name: str = "cr", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.numerator:
            self.numerator.to_xml_element(element_name="numerator", parent=elem)
        if self.denominator:
            self.denominator.to_xml_element(element_name="denominator", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "cr") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "CR":
        """Deserialize from XML Element."""
        num_elem = xml_element.find("numerator")
        numerator = CD.from_xml(num_elem) if num_elem is not None else None
        den_elem = xml_element.find("denominator")
        denominator = CD.from_xml(den_elem) if den_elem is not None else None
        return cls(numerator=numerator, denominator=denominator)



@dataclass
class IVL_PQ:
    """
    IVL_PQ - Interval of Physical Quantities.
    
    Represents an interval of physical quantities (PQ).
    """
    low: Optional[PQ] = None
    high: Optional[PQ] = None
    width: Optional[PQ] = None
    center: Optional[PQ] = None
    
    def to_xml_element(self, element_name: str = "ivl_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            low_elem = self.low.to_xml_element("low", elem)
            elem.append(low_elem)
        
        if self.high is not None:
            high_elem = self.high.to_xml_element("high", elem)
            elem.append(high_elem)
        
        if self.width is not None:
            width_elem = self.width.to_xml_element("width", elem)
            elem.append(width_elem)
        
        if self.center is not None:
            center_elem = self.center.to_xml_element("center", elem)
            elem.append(center_elem)
        
        return elem



@dataclass
class PQR(CD):
    """
    PQR - Physical Quantity with Range.
    
    Represents a physical quantity with a range of values.
    """
    value: Optional[PQ] = None
    
    def to_xml_element(self, element_name: str = "pqr", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        elem = super().to_xml_element(element_name, parent)
        if self.value is not None:
            value_elem = self.value.to_xml_element("value", elem)
            elem.append(value_elem)
        return elem



class UUID(II):
    """
    UUID - Universally Unique Identifier.
    
    Represents a UUID using the II (Instance Identifier) data type.
    """
    def __init__(self, root: Optional[str] = None, extension: Optional[str] = None):
        """
        Initialize UUID.
        
        Args:
            root: Root OID (typically "2.25" for UUIDs)
            extension: UUID string (8-4-4-4-12 hex format)
        """
        if root is None:
            root = "2.25"  # Standard OID for UUIDs
        super().__init__(root=root, extension=extension)
    
    def __repr__(self) -> str:
        return f"UUID(root={self.root}, extension={self.extension})"
    
    def to_xml_element(self, element_name: str = "uuid", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        return super().to_xml_element(element_name, parent)



class ANYNonNull(ANY):
    """
    ANYNonNull - Any non-null type.
    
    Represents any HL7 v3 data type that cannot be null.
    """
    def __init__(self, value: Any):
        """Initialize ANYNonNull type."""
        if value is None:
            raise ValueError("ANYNonNull cannot be None")
        super().__init__(value)
    
    def __repr__(self) -> str:
        return f"ANYNonNull({self.value})"
    
    def to_xml_element(self, element_name: str = "anyNonNull", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        if self.value is not None:
            elem.text = str(self.value)
        return elem



@dataclass
class URG(PQ):
    """
    URG - Urgency.
    
    Represents urgency as a physical quantity.
    """
    pass


@dataclass
class UVC:
    """
    UVC - Uncertain Value Coded.
    
    Represents a coded value with uncertainty.
    Used when a coded value has uncertainty or probability associated with it.
    """
    code: Optional[str] = None  # The coded value
    code_system: Optional[str] = None  # Code system OID or identifier
    code_system_name: Optional[str] = None  # Code system name
    display_name: Optional[str] = None  # Display name for the code
    probability: Optional[REAL] = None  # Probability (0.0 to 1.0)
    distribution_type: Optional[str] = None  # Distribution type
    
    def to_xml_element(self, element_name: str = "uvc", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "uvc")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.code is not None:
            elem.set("code", self.code)
        
        if self.code_system is not None:
            elem.set("codeSystem", self.code_system)
        
        if self.code_system_name is not None:
            elem.set("codeSystemName", self.code_system_name)
        
        if self.display_name is not None:
            elem.set("displayName", self.display_name)
        
        if self.probability is not None:
            prob_elem = self.probability.to_xml_element("probability", elem)
            elem.append(prob_elem)
        
        if self.distribution_type is not None:
            elem.set("distributionType", self.distribution_type)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")
        
        return elem
    
    def to_xml(self, element_name: str = "uvc") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "uvc")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")
        
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "UVC":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            UVC instance
        """
        code = xml_element.get("code")
        code_system = xml_element.get("codeSystem")
        code_system_name = xml_element.get("codeSystemName")
        display_name = xml_element.get("displayName")
        distribution_type = xml_element.get("distributionType")
        
        # Parse probability if present
        probability = None
        prob_elem = xml_element.find("probability")
        if prob_elem is not None:
            try:
                from dnhealth.dnhealth_hl7v3.datatypes import REAL
                probability = REAL.from_xml(prob_elem)
            except:
                pass
        
        return cls(
            code=code,
            code_system=code_system,
            code_system_name=code_system_name,
            display_name=display_name,
            probability=probability,
            distribution_type=distribution_type
        )


@dataclass
class IVL_TS:
    """
    IVL_TS - Interval of Timestamps.
    
    Represents an interval of timestamps (TS).
    """
    low: Optional[TS] = None
    high: Optional[TS] = None
    width: Optional[PQ] = None
    center: Optional[TS] = None
    
    def to_xml_element(self, element_name: str = "ivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            low_elem = self.low.to_xml_element("low", elem)
            elem.append(low_elem)
        
        if self.high is not None:
            high_elem = self.high.to_xml_element("high", elem)
            elem.append(high_elem)
        
        if self.width is not None:
            width_elem = self.width.to_xml_element("width", elem)
            elem.append(width_elem)
        
        if self.center is not None:
            center_elem = self.center.to_xml_element("center", elem)
            elem.append(center_elem)
        
        return elem


# TN - Telephone Number (alias for TEL)
TN = TEL


@dataclass
class UVN_TS:
    """
    UVN_TS - Uncertain Value Non-null Timestamp.
    
    Represents an uncertain timestamp value that cannot be null.
    """
    value: TS  # Required (non-null)
    uncertainty: Optional[PQ] = None  # Uncertainty in the timestamp
    
    def to_xml_element(self, element_name: str = "uvn_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.value is not None:
            value_elem = self.value.to_xml_element("value", elem)
            elem.append(value_elem)
        
        if self.uncertainty is not None:
            uncertainty_elem = self.uncertainty.to_xml_element("uncertainty", elem)
            elem.append(uncertainty_elem)
        
        return elem


@dataclass
class PIVL_TS:
    """
    PIVL_TS - Periodic Interval Timestamp.
    
    Represents a periodic interval of timestamps.
    """
    phase: Optional[IVL_TS] = None  # Phase of the periodic interval
    period: Optional[PQ] = None  # Period of the interval
    frequency: Optional[INT] = None  # Frequency of occurrence
    
    def to_xml_element(self, element_name: str = "pivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.phase is not None:
            phase_elem = self.phase.to_xml_element("phase", elem)
            elem.append(phase_elem)
        
        if self.period is not None:
            period_elem = self.period.to_xml_element("period", elem)
            elem.append(period_elem)
        
        if self.frequency is not None:
            frequency_elem = self.frequency.to_xml_element("frequency", elem)
            elem.append(frequency_elem)
        
        return elem


@dataclass
class IVL_INT:
    """
    IVL_INT - Interval of Integers.
    
    Represents an interval of integer values.
    """
    low: Optional[INT] = None
    high: Optional[INT] = None
    width: Optional[INT] = None
    center: Optional[INT] = None
    
    def to_xml_element(self, element_name: str = "ivl_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            low_elem = self.low.to_xml_element("low", elem)
            elem.append(low_elem)
        
        if self.high is not None:
            high_elem = self.high.to_xml_element("high", elem)
            elem.append(high_elem)
        
        if self.width is not None:
            width_elem = self.width.to_xml_element("width", elem)
            elem.append(width_elem)
        
        if self.center is not None:
            center_elem = self.center.to_xml_element("center", elem)
            elem.append(center_elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_MO:
    """
    IVL_MO - Interval of Monetary Amounts.
    
    Represents an interval of monetary amounts (MO).
    """
    low: Optional[MO] = None
    high: Optional[MO] = None
    width: Optional[MO] = None
    center: Optional[MO] = None
    
    def to_xml_element(self, element_name: str = "ivl_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            low_elem = self.low.to_xml_element("low", elem)
            elem.append(low_elem)
        
        if self.high is not None:
            high_elem = self.high.to_xml_element("high", elem)
            elem.append(high_elem)
        
        if self.width is not None:
            width_elem = self.width.to_xml_element("width", elem)
            elem.append(width_elem)
        
        if self.center is not None:
            center_elem = self.center.to_xml_element("center", elem)
            elem.append(center_elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_REAL:
    """
    IVL_REAL - Interval of Real Numbers.
    
    Represents an interval of real (floating-point) values.
    """
    low: Optional[REAL] = None
    high: Optional[REAL] = None
    width: Optional[REAL] = None
    center: Optional[REAL] = None
    
    def to_xml_element(self, element_name: str = "ivl_real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            low_elem = self.low.to_xml_element("low", elem)
            elem.append(low_elem)
        
        if self.high is not None:
            high_elem = self.high.to_xml_element("high", elem)
            elem.append(high_elem)
        
        if self.width is not None:
            width_elem = self.width.to_xml_element("width", elem)
            elem.append(width_elem)
        
        if self.center is not None:
            center_elem = self.center.to_xml_element("center", elem)
            elem.append(center_elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class LIST_INT:
    """
    LIST_INT - List of Integers.
    
    Represents an ordered list of integer values.
    """
    items: List[INT] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "list_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class LIST_MO:
    """
    LIST_MO - List of Monetary Amounts.
    
    Represents an ordered list of monetary amounts.
    """
    items: List[MO] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "list_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class LIST_PQ:
    """
    LIST_PQ - List of Physical Quantities.
    
    Represents an ordered list of physical quantities.
    """
    items: List[PQ] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "list_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class LIST_TS:
    """
    LIST_TS - List of Timestamps.
    
    Represents an ordered list of timestamps.
    """
    items: List[TS] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "list_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class LIST_CE:
    """
    LIST_CE - List of Coded Elements.
    
    Represents an ordered list of coded elements (CE data type).
    """
    items: List[CE] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "list_ce", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class LIST_II:
    """
    LIST_II - List of Instance Identifiers.
    
    Represents an ordered list of instance identifiers (II data type).
    """
    items: List[II] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "list_ii", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
            else:
                item_elem = ET.SubElement(elem, "item")
                item_elem.text = str(item)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class QTY_QTY:
    """
    QTY_QTY - Quantity of Quantities.
    
    Represents a quantity where the value itself is a quantity.
    """
    value: Optional[QTY] = None
    
    def to_xml_element(self, element_name: str = "qty_qty", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
            else:
                value_elem = ET.SubElement(elem, "value")
                value_elem.text = str(self.value)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class RTO_MO_PQ:
    """
    RTO_MO_PQ - Ratio of Monetary Amount to Physical Quantity.
    
    Represents a ratio where the numerator is a monetary amount and the denominator is a physical quantity.
    """
    numerator: Optional[MO] = None
    denominator: Optional[PQ] = None
    
    def to_xml_element(self, element_name: str = "rto_mo_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.numerator is not None:
            num_elem = self.numerator.to_xml_element("numerator", elem)
            elem.append(num_elem)
        
        if self.denominator is not None:
            den_elem = self.denominator.to_xml_element("denominator", elem)
            elem.append(den_elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class RTO_PQ_PQ:
    """
    RTO_PQ_PQ - Ratio of Physical Quantity to Physical Quantity.
    
    Represents a ratio where both numerator and denominator are physical quantities.
    """
    numerator: Optional[PQ] = None
    denominator: Optional[PQ] = None
    
    def to_xml_element(self, element_name: str = "rto_pq_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.numerator is not None:
            num_elem = self.numerator.to_xml_element("numerator", elem)
            elem.append(num_elem)
        
        if self.denominator is not None:
            den_elem = self.denominator.to_xml_element("denominator", elem)
            elem.append(den_elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class URG_PQ(URG):
    """
    URG_PQ - Uncertain Range for Physical Quantity.
    
    Represents an uncertain range where the value is a physical quantity.
    """
    def __init__(self, value: Optional[PQ] = None, low: Optional[PQ] = None, high: Optional[PQ] = None):
        """Initialize URG_PQ type."""
        super().__init__(value=value, low=low, high=high)


@dataclass
class EIVL_TS:
    """
    EIVL_TS - Event Interval Timestamp.
    
    Represents an event-based interval of timestamps.
    """
    event: Optional[CD] = None  # Event code
    offset: Optional[IVL_PQ] = None  # Offset from event
    
    def to_xml_element(self, element_name: str = "eivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.event is not None:
            event_elem = self.event.to_xml_element("event", elem)
            elem.append(event_elem)
        
        if self.offset is not None:
            offset_elem = self.offset.to_xml_element("offset", elem)
            elem.append(offset_elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class GLIST:
    """
    GLIST - Gap List.
    
    Represents a list with gaps (missing values).
    """
    head: Optional[Any] = None  # First value
    increment: Optional[PQ] = None  # Increment between values
    period: Optional[int] = None  # Period of the gap list
    denominator: Optional[int] = None  # Denominator for fractional periods
    
    def to_xml_element(self, element_name: str = "glist", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.head is not None:
            if hasattr(self.head, 'to_xml_element'):
                self.head.to_xml_element("head", elem)
            else:
                head_elem = ET.SubElement(elem, "head")
                head_elem.text = str(self.head)
        
        if self.increment is not None:
            inc_elem = self.increment.to_xml_element("increment", elem)
            elem.append(inc_elem)
        
        if self.period is not None:
            period_elem = ET.SubElement(elem, "period")
            period_elem.text = str(self.period)
        
        if self.denominator is not None:
            den_elem = ET.SubElement(elem, "denominator")
            den_elem.text = str(self.denominator)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SLIST:
    """
    SLIST - Sequence List.
    
    Represents an ordered sequence of values.
    """
    head: Optional[Any] = None  # First value
    increment: Optional[PQ] = None  # Increment between values
    digits: Optional[int] = None  # Number of digits
    
    def to_xml_element(self, element_name: str = "slist", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.head is not None:
            if hasattr(self.head, 'to_xml_element'):
                self.head.to_xml_element("head", elem)
            else:
                head_elem = ET.SubElement(elem, "head")
                head_elem.text = str(self.head)
        
        if self.increment is not None:
            inc_elem = self.increment.to_xml_element("increment", elem)
            elem.append(inc_elem)
        
        if self.digits is not None:
            digits_elem = ET.SubElement(elem, "digits")
            digits_elem.text = str(self.digits)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SLIST_PQ:
    """
    SLIST_PQ - Sequence List for Physical Quantities.
    
    Represents an ordered sequence of physical quantities.
    """
    head: Optional[PQ] = None  # First value
    increment: Optional[PQ] = None  # Increment between values
    digits: Optional[int] = None  # Number of digits
    
    def to_xml_element(self, element_name: str = "slist_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.head is not None:
            if hasattr(self.head, 'to_xml_element'):
                self.head.to_xml_element("head", elem)
            else:
                head_elem = ET.SubElement(elem, "head")
                head_elem.text = str(self.head)
        
        if self.increment is not None:
            inc_elem = self.increment.to_xml_element("increment", elem)
            elem.append(inc_elem)
        
        if self.digits is not None:
            digits_elem = ET.SubElement(elem, "digits")
            digits_elem.text = str(self.digits)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SLIST_TS:
    """
    SLIST_TS - Sequence List for Timestamps.
    
    Represents an ordered sequence of timestamps.
    """
    head: Optional[TS] = None  # First value
    increment: Optional[PQ] = None  # Increment between values (as duration)
    digits: Optional[int] = None  # Number of digits
    
    def to_xml_element(self, element_name: str = "slist_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.head is not None:
            if hasattr(self.head, 'to_xml_element'):
                self.head.to_xml_element("head", elem)
            else:
                head_elem = ET.SubElement(elem, "head")
                head_elem.text = str(self.head)
        
        if self.increment is not None:
            inc_elem = self.increment.to_xml_element("increment", elem)
            elem.append(inc_elem)
        
        if self.digits is not None:
            digits_elem = ET.SubElement(elem, "digits")
            digits_elem.text = str(self.digits)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SXPR_TS:
    """
    SXPR_TS - Set Expression Timestamp.
    
    Represents a set expression where components are timestamps.
    """
    components: List[SXCM_TS] = field(default_factory=list)
    
    def to_xml_element(self, element_name: str = "sxpr_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element("comp", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class ANYNonNull(ANY):
    """
    ANYNonNull - Any Non-null Type.
    
    Represents any HL7 v3 data type that cannot be null.
    """
    def __init__(self, value: Any):
        """
        Initialize ANYNonNull type.
        
        Args:
            value: Non-null value (required)
        """
        if value is None:
            raise ValueError("ANYNonNull value cannot be None")
        super().__init__(value=value)




@dataclass
class HXIT:
    """
    HXIT - History with Interval.
    
    Represents a historical value with an interval.
    """
    value: Optional[Any] = None  # Historical value
    valid_time: Optional[IVL] = None  # Validity interval
    
    def to_xml_element(self, element_name: str = "hxit", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element(element_name="value", parent=elem)
            else:
                value_elem = ET.SubElement(elem, "value")
                value_elem.text = str(self.value)
        if self.valid_time:
            self.valid_time.to_xml_element(element_name="validTime", parent=elem)
        return elem
    
    def to_xml(self, element_name: str = "hxit") -> str:
        """Serialize to XML string."""
        return ET.tostring(self.to_xml_element(element_name), encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "HXIT":
        """Deserialize from XML Element."""
        value_elem = xml_element.find("value")
        value = value_elem.text if value_elem is not None and value_elem.text else None
        valid_time_elem = xml_element.find("validTime")
        valid_time = IVL.from_xml(valid_time_elem) if valid_time_elem is not None else None
        return cls(value=value, valid_time=valid_time)


class HXIT_CD(HXIT):
    """
    HXIT_CD - History with Interval for Coded Data.
    
    Represents a historical coded value with an interval.
    """
    def __init__(self, value: Optional[CD] = None, valid_time: Optional[IVL_TS] = None):
        """Initialize HXIT_CD type."""
        super().__init__(value=value, valid_time=valid_time)


class HXIT_CE(HXIT):
    """
    HXIT_CE - History with Interval for Coded with Equivalents.
    
    Represents a historical coded value with equivalents and an interval.
    """
    def __init__(self, value: Optional[CE] = None, valid_time: Optional[IVL_TS] = None):
        """Initialize HXIT_CE type."""
        super().__init__(value=value, valid_time=valid_time)


class HXIT_CO(HXIT):
    """
    HXIT_CO - History with Interval for Coded Ordinal.
    
    Represents a historical coded ordinal value with an interval.
    """
    def __init__(self, value: Optional[CO] = None, valid_time: Optional[IVL_TS] = None):
        """Initialize HXIT_CO type."""
        super().__init__(value=value, valid_time=valid_time)


class HXIT_CV(HXIT):
    """
    HXIT_CV - History with Interval for Coded Value.
    
    Represents a historical coded value with an interval.
    """
    def __init__(self, value: Optional[CV] = None, valid_time: Optional[IVL_TS] = None):
        """Initialize HXIT_CV type."""
        super().__init__(value=value, valid_time=valid_time)


class HXIT_PQ(HXIT):
    """
    HXIT_PQ - History with Interval for Physical Quantity.
    
    Represents a historical physical quantity with an interval.
    """
    def __init__(self, value: Optional[PQ] = None, valid_time: Optional[IVL_TS] = None):
        """Initialize HXIT_PQ type."""
        super().__init__(value=value, valid_time=valid_time)


class HXIT_TS(HXIT):
    """
    HXIT_TS - History with Interval for Timestamp.
    
    Represents a historical timestamp with an interval.
    """
    def __init__(self, value: Optional[TS] = None, valid_time: Optional[IVL_TS] = None):
        """Initialize HXIT_TS type."""
        super().__init__(value=value, valid_time=valid_time)


@dataclass
class TN:
    """
    TN - Telephone Number.
    
    Represents a telephone number in HL7 v3 format.
    Similar to TEL but specifically for telephone numbers.
    """
    value: Optional[str] = None  # Telephone number value
    use: Optional[str] = None  # Use code (e.g., "H" for home, "W" for work)
    
    def to_xml_element(self, element_name: str = "tn", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "tn")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            elem.text = str(self.value)
        
        if self.use is not None:
            elem.set("use", self.use)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")
        
        return elem
    
    def to_xml(self, element_name: str = "tn") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "tn")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")
        
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "TN":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            TN instance
        """
        value = xml_element.text if xml_element.text else None
        use = xml_element.get("use")
        return cls(value=value, use=use)


@dataclass
class UVP_TS:
    """
    UVP_TS - Uncertain Value Probabilistic Time Stamp.
    
    Represents a time stamp with uncertain/probabilistic value.
    Combines UVP (Uncertain Value Probabilistic) with TS (Time Stamp).
    """
    value: Optional[TS] = None  # Time stamp value
    probability: Optional[REAL] = None  # Probability value
    distribution_type: Optional[str] = None  # Distribution type
    
    def to_xml_element(self, element_name: str = "uvp_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serialize to XML Element.
        
        Args:
            element_name: XML element name (default: "uvp_ts")
            parent: Optional parent element
            
        Returns:
            XML Element
        """
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            value_elem = self.value.to_xml_element("value", elem)
            elem.append(value_elem)
        
        if self.probability is not None:
            prob_elem = self.probability.to_xml_element("probability", elem)
            elem.append(prob_elem)
        
        if self.distribution_type is not None:
            elem.set("distributionType", self.distribution_type)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")
        
        return elem
    
    def to_xml(self, element_name: str = "uvp_ts") -> str:
        """
        Serialize to XML string.
        
        Args:
            element_name: XML element name (default: "uvp_ts")
            
        Returns:
            XML string
        """
        elem = self.to_xml_element(element_name)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Current Time at End of Operations: {current_time}")
        
        return ET.tostring(elem, encoding="unicode")
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "UVP_TS":
        """
        Deserialize from XML Element.
        
        Args:
            xml_element: XML Element to parse
            
        Returns:
            UVP_TS instance
        """
        value_elem = xml_element.find("value")
        value = TS.from_xml(value_elem) if value_elem is not None else None
        
        prob_elem = xml_element.find("probability")
        probability = REAL.from_xml(prob_elem) if prob_elem is not None else None
        
        distribution_type = xml_element.get("distributionType")
        
        return cls(value=value, probability=probability, distribution_type=distribution_type)


# ============================================================================
# Additional Data Types
# ============================================================================

@dataclass
class BIN:
    """
    BIN - Binary Data.
    
    Represents binary data (e.g., images, documents, etc.).
    Typically encoded as base64 in XML.
    """
    value: Optional[bytes] = None
    media_type: Optional[str] = None  # MIME type (e.g., "image/png", "application/pdf")
    
    def to_xml_element(self, element_name: str = "bin", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.media_type:
            elem.set("mediaType", self.media_type)
        
        if self.value is not None:
            # Encode binary data as base64
            encoded = base64.b64encode(self.value).decode('utf-8')
            elem.text = encoded
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return elem
    
    def to_xml(self, element_name: str = "bin") -> str:
        """Serialize to XML string."""
        result = ET.tostring(self.to_xml_element(element_name), encoding="unicode")
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "BIN":
        """Deserialize from XML Element."""
        media_type = xml_element.get("mediaType")
        value = None
        
        if xml_element.text:
            # Decode base64 data
            try:
                value = base64.b64decode(xml_element.text)
            except Exception as e:
                logger.warning(f"Error decoding BIN data: {e}")
        
        return cls(value=value, media_type=media_type)


# QTY_PQ and QTY_TS are type aliases for IVL_PQ and IVL_TS respectively
# They represent quantity intervals for Physical Quantities and Timestamps
QTY_PQ = IVL_PQ  # Quantity interval for Physical Quantities
QTY_TS = IVL_TS  # Quantity interval for Timestamps


# ============================================================================
# Additional HL7 v3 Data Types
# ============================================================================

class CF(CD):
    """
    CF - Coded Float.
    
    A coded value with an associated floating-point number.
    Extends CD to include a numeric value.
    """
    def __init__(self, code: Optional[str] = None, code_system: Optional[str] = None,
                 display_name: Optional[str] = None, value: Optional[float] = None):
        """Initialize CF type."""
        super().__init__(code=code, code_system=code_system, display_name=display_name)
        self.value = value
    
    def __repr__(self) -> str:
        return f"CF(code={self.code}, value={self.value})"


class PPD:
    """
    PPD - Probability Distribution.
    
    Represents a probability distribution with mean and standard deviation.
    """
    def __init__(self, mean: Optional[float] = None, standard_deviation: Optional[float] = None,
                 distribution_type: Optional[str] = None):
        """
        Initialize PPD type.
        
        Args:
            mean: Mean value of the distribution
            standard_deviation: Standard deviation of the distribution
            distribution_type: Type of distribution (e.g., "normal", "uniform")
        """
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.distribution_type = distribution_type
    
    def __repr__(self) -> str:
        return f"PPD(mean={self.mean}, stddev={self.standard_deviation})"
    
    def to_xml_element(self, element_name: str = "ppd", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.mean is not None:
            mean_elem = ET.SubElement(elem, "mean")
            mean_elem.text = str(self.mean)
        
        if self.standard_deviation is not None:
            stddev_elem = ET.SubElement(elem, "standardDeviation")
            stddev_elem.text = str(self.standard_deviation)
        
        if self.distribution_type is not None:
            elem.set("distributionType", self.distribution_type)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "PPD":
        """Deserialize from XML Element."""
        mean = None
        stddev = None
        dist_type = xml_element.get("distributionType")
        
        mean_elem = xml_element.find("mean")
        if mean_elem is not None and mean_elem.text:
            mean = float(mean_elem.text)
        
        stddev_elem = xml_element.find("standardDeviation")
        if stddev_elem is not None and stddev_elem.text:
            stddev = float(stddev_elem.text)
        
        return cls(mean=mean, standard_deviation=stddev, distribution_type=dist_type)


class PPD_CD(PPD):
    """
    PPD_CD - Probability Distribution for Coded Data.
    
    A probability distribution where the value is a coded element.
    """
    def __init__(self, code: Optional[CD] = None, mean: Optional[float] = None,
                 standard_deviation: Optional[float] = None):
        """Initialize PPD_CD type."""
        super().__init__(mean=mean, standard_deviation=standard_deviation)
        self.code = code


class PPD_PQ(PPD):
    """
    PPD_PQ - Probability Distribution for Physical Quantity.
    
    A probability distribution where the value is a physical quantity.
    """
    def __init__(self, quantity: Optional[PQ] = None, mean: Optional[float] = None,
                 standard_deviation: Optional[float] = None):
        """Initialize PPD_PQ type."""
        super().__init__(mean=mean, standard_deviation=standard_deviation)
        self.quantity = quantity


class PPD_TS(PPD):
    """
    PPD_TS - Probability Distribution for Timestamp.
    
    A probability distribution where the value is a timestamp.
    """
    def __init__(self, timestamp: Optional[TS] = None, mean: Optional[float] = None,
                 standard_deviation: Optional[float] = None):
        """Initialize PPD_TS type."""
        super().__init__(mean=mean, standard_deviation=standard_deviation)
        self.timestamp = timestamp


class NPPD:
    """
    NPPD - Non-parametric Probability Distribution.
    
    Represents a non-parametric probability distribution (histogram-based).
    """
    def __init__(self, histogram: Optional[List[Tuple[float, float]]] = None,
                 distribution_type: Optional[str] = None):
        """
        Initialize NPPD type.
        
        Args:
            histogram: List of (value, probability) tuples representing the distribution
            distribution_type: Type of distribution (e.g., "histogram", "kernel")
        """
        self.histogram = histogram or []
        self.distribution_type = distribution_type
    
    def __repr__(self) -> str:
        return f"NPPD(type={self.distribution_type}, bins={len(self.histogram)})"
    
    def to_xml_element(self, element_name: str = "nppd", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.distribution_type is not None:
            elem.set("distributionType", self.distribution_type)
        
        for value, probability in self.histogram:
            bin_elem = ET.SubElement(elem, "bin")
            value_elem = ET.SubElement(bin_elem, "value")
            value_elem.text = str(value)
            prob_elem = ET.SubElement(bin_elem, "probability")
            prob_elem.text = str(probability)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "NPPD":
        """Deserialize from XML Element."""
        distribution_type = xml_element.get("distributionType")
        histogram = []
        
        for bin_elem in xml_element.findall("bin"):
            value_elem = bin_elem.find("value")
            prob_elem = bin_elem.find("probability")
            if value_elem is not None and prob_elem is not None:
                value = float(value_elem.text) if value_elem.text else 0.0
                prob = float(prob_elem.text) if prob_elem.text else 0.0
                histogram.append((value, prob))
        
        return cls(histogram=histogram, distribution_type=distribution_type)


class PRPA:
    """
    PRPA - Probability Distribution Parameter.
    
    Represents parameters for a probability distribution.
    """
    def __init__(self, parameter_name: Optional[str] = None,
                 parameter_value: Optional[Union[float, str]] = None,
                 parameter_type: Optional[str] = None):
        """
        Initialize PRPA type.
        
        Args:
            parameter_name: Name of the parameter (e.g., "mean", "variance", "shape")
            parameter_value: Value of the parameter
            parameter_type: Type of the parameter value ("real", "string", etc.)
        """
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.parameter_type = parameter_type
    
    def __repr__(self) -> str:
        return f"PRPA(name={self.parameter_name}, value={self.parameter_value})"
    
    def to_xml_element(self, element_name: str = "prpa", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.parameter_name is not None:
            elem.set("name", self.parameter_name)
        
        if self.parameter_type is not None:
            elem.set("type", self.parameter_type)
        
        if self.parameter_value is not None:
            elem.text = str(self.parameter_value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "PRPA":
        """Deserialize from XML Element."""
        parameter_name = xml_element.get("name")
        parameter_type = xml_element.get("type")
        parameter_value = None
        
        if xml_element.text:
            if parameter_type == "real":
                try:
                    parameter_value = float(xml_element.text)
                except ValueError:
                    parameter_value = xml_element.text
            else:
                parameter_value = xml_element.text
        
        return cls(parameter_name=parameter_name, parameter_value=parameter_value,
                   parameter_type=parameter_type)


class IVXB:
    """
    IVXB - Interval Boundary.
    
    Represents a boundary of an interval (inclusive or exclusive).
    """
    def __init__(self, value: Any = None, inclusive: bool = True):
        """
        Initialize IVXB type.
        
        Args:
            value: The boundary value
            inclusive: Whether the boundary is inclusive (True) or exclusive (False)
        """
        self.value = value
        self.inclusive = inclusive
    
    def __repr__(self) -> str:
        incl_str = "inclusive" if self.inclusive else "exclusive"
        return f"IVXB(value={self.value}, {incl_str})"
    
    def to_xml_element(self, element_name: str = "ivxb", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if not self.inclusive:
            elem.set("inclusive", "false")
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element(element_name="value", parent=elem)
            else:
                elem.text = str(self.value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "IVXB":
        """Deserialize from XML Element."""
        inclusive = xml_element.get("inclusive", "true").lower() == "true"
        value_elem = xml_element.find("value")
        value = None
        
        if value_elem is not None:
            if value_elem.text:
                value = value_elem.text
        elif xml_element.text:
            value = xml_element.text
        
        return cls(value=value, inclusive=inclusive)


class IVXB_INT(IVXB):
    """IVXB_INT - Interval Boundary for Integer."""
    def __init__(self, value: Optional[int] = None, inclusive: bool = True):
        """Initialize IVXB_INT type."""
        super().__init__(value=value, inclusive=inclusive)


class IVXB_PPD_TS(IVXB):
    """IVXB_PPD_TS - Interval Boundary for Probability Distribution Timestamp."""
    def __init__(self, value: Optional[PPD_TS] = None, inclusive: bool = True):
        """Initialize IVXB_PPD_TS type."""
        super().__init__(value=value, inclusive=inclusive)


class IVXB_PQ(IVXB):
    """IVXB_PQ - Interval Boundary for Physical Quantity."""
    def __init__(self, value: Optional[PQ] = None, inclusive: bool = True):
        """Initialize IVXB_PQ type."""
        super().__init__(value=value, inclusive=inclusive)


class IVXB_REAL(IVXB):
    """IVXB_REAL - Interval Boundary for Real number."""
    def __init__(self, value: Optional[float] = None, inclusive: bool = True):
        """Initialize IVXB_REAL type."""
        super().__init__(value=value, inclusive=inclusive)


class IVXB_TS(IVXB):
    """IVXB_TS - Interval Boundary for Timestamp."""
    def __init__(self, value: Optional[TS] = None, inclusive: bool = True):
        """Initialize IVXB_TS type."""
        super().__init__(value=value, inclusive=inclusive)


class IVXB_MO(IVXB):
    """
    IVXB_MO - Interval Boundary for Monetary Amount.
    
    Represents a boundary of an interval where the value is a monetary amount.
    """
    def __init__(self, value: Optional[MO] = None, inclusive: bool = True):
        """Initialize IVXB_MO type."""
        super().__init__(value=value, inclusive=inclusive)


class QSC:
    """
    QSC - Query Selection Criteria.
    
    Represents selection criteria for queries.
    """
    def __init__(self, name: Optional[str] = None, value: Optional[str] = None,
                 operator: Optional[str] = None):
        """
        Initialize QSC type.
        
        Args:
            name: Name of the field to query
            value: Value to match
            operator: Comparison operator (e.g., "EQ", "NE", "GT", "LT", "GE", "LE")
        """
        self.name = name
        self.value = value
        self.operator = operator
    
    def __repr__(self) -> str:
        return f"QSC(name={self.name}, operator={self.operator}, value={self.value})"
    
    def to_xml_element(self, element_name: str = "qsc", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.name is not None:
            elem.set("name", self.name)
        if self.operator is not None:
            elem.set("operator", self.operator)
        if self.value is not None:
            elem.text = str(self.value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "QSC":
        """Deserialize from XML Element."""
        name = xml_element.get("name")
        operator = xml_element.get("operator")
        value = xml_element.text if xml_element.text else None
        return cls(name=name, value=value, operator=operator)


class QSD:
    """
    QSD - Query Sort Definition.
    
    Defines how query results should be sorted.
    """
    def __init__(self, field_name: Optional[str] = None, sort_order: Optional[str] = None):
        """
        Initialize QSD type.
        
        Args:
            field_name: Name of the field to sort by
            sort_order: Sort order ("ASC" for ascending, "DESC" for descending)
        """
        self.field_name = field_name
        self.sort_order = sort_order or "ASC"
    
    def __repr__(self) -> str:
        return f"QSD(field={self.field_name}, order={self.sort_order})"


class QSET:
    """
    QSET - Query Set.
    
    Represents a set of query criteria combined with set operators.
    """
    def __init__(self, operator: Optional[str] = None, terms: Optional[List[Any]] = None):
        """
        Initialize QSET type.
        
        Args:
            operator: Set operator ("AND", "OR", "NOT")
            terms: List of query terms (QSC, QSET, etc.)
        """
        self.operator = operator or "AND"
        self.terms = terms or []
    
    def __repr__(self) -> str:
        return f"QSET(operator={self.operator}, terms={len(self.terms)})"


class QSI:
    """
    QSI - Query Sort Instruction.
    
    Instruction for sorting query results.
    """
    def __init__(self, sort_field: Optional[str] = None, direction: Optional[str] = None):
        """
        Initialize QSI type.
        
        Args:
            sort_field: Field name to sort by
            direction: Sort direction ("ASC" or "DESC")
        """
        self.sort_field = sort_field
        self.direction = direction or "ASC"
    
    def __repr__(self) -> str:
        return f"QSI(field={self.sort_field}, direction={self.direction})"


class QSP:
    """
    QSP - Query Sort Parameter.
    
    Parameter for query sorting.
    """
    def __init__(self, name: Optional[str] = None, value: Optional[str] = None):
        """
        Initialize QSP type.
        
        Args:
            name: Parameter name
            value: Parameter value
        """
        self.name = name
        self.value = value
    
    def __repr__(self) -> str:
        return f"QSP(name={self.name}, value={self.value})"


class QSS:
    """
    QSS - Query Sort Specification.
    
    Specification for query result sorting.
    """
    def __init__(self, sort_fields: Optional[List[QSI]] = None):
        """
        Initialize QSS type.
        
        Args:
            sort_fields: List of sort instructions
        """
        self.sort_fields = sort_fields or []
    
    def __repr__(self) -> str:
        return f"QSS(fields={len(self.sort_fields)})"


class QSU:
    """
    QSU - Query Sort Using.
    
    Defines sort criteria using field names and directions.
    """
    def __init__(self, field: Optional[str] = None, direction: Optional[str] = None):
        """
        Initialize QSU type.
        
        Args:
            field: Field name to sort by
            direction: Sort direction ("ASC" or "DESC")
        """
        self.field = field
        self.direction = direction or "ASC"
    
    def __repr__(self) -> str:
        return f"QSU(field={self.field}, direction={self.direction})"


class SXCM:
    """
    SXCM - Set Component.
    
    Represents a component of a set expression.
    """
    def __init__(self, operator: Optional[str] = None, value: Any = None):
        """
        Initialize SXCM type.
        
        Args:
            operator: Set operator ("I" for include, "E" for exclude, "A" for assert)
            value: The component value
        """
        self.operator = operator or "I"
        self.value = value
    
    def __repr__(self) -> str:
        return f"SXCM(operator={self.operator}, value={self.value})"
    
    def to_xml_element(self, element_name: str = "sxcm", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.operator:
            elem.set("operator", self.operator)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element(element_name="value", parent=elem)
            else:
                elem.text = str(self.value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "SXCM":
        """Deserialize from XML Element."""
        operator = xml_element.get("operator", "I")
        value_elem = xml_element.find("value")
        value = None
        
        if value_elem is not None:
            if value_elem.text:
                value = value_elem.text
        elif xml_element.text:
            value = xml_element.text
        
        return cls(operator=operator, value=value)


class SXCM_TS(SXCM):
    """
    SXCM_TS - Set Component Timestamp.
    
    Represents a set component where the value is a timestamp.
    """
    def __init__(self, operator: Optional[str] = None, value: Optional[TS] = None):
        """Initialize SXCM_TS type."""
        super().__init__(operator=operator, value=value)


class SXPR:
    """
    SXPR - Set Expression.
    
    Represents a set expression combining multiple set components.
    """
    def __init__(self, components: Optional[List[SXCM]] = None):
        """
        Initialize SXPR type.
        
        Args:
            components: List of set components
        """
        self.components = components or []
    
    def __repr__(self) -> str:
        return f"SXPR(components={len(self.components)})"
    
    def to_xml_element(self, element_name: str = "sxpr", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element(element_name="component", parent=elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "SXPR":
        """Deserialize from XML Element."""
        components = []
        for comp_elem in xml_element.findall("component"):
            comp = SXCM.from_xml(comp_elem)
            components.append(comp)
        return cls(components=components)


class SXPR_TS:
    """
    SXPR_TS - Set Expression Timestamp.
    
    Represents a set expression where components are timestamps.
    """
    def __init__(self, components: Optional[List[SXCM_TS]] = None):
        """
        Initialize SXPR_TS type.
        
        Args:
            components: List of set component timestamps
        """
        self.components = components or []
    
    def to_xml_element(self, element_name: str = "sxpr_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element("comp", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


# Type aliases for convenience
ConceptDescriptor = CD
CodedElement = CE
CodedSimple = CS
CodedValue = CV
EncapsulatedData = ED
EventInterval = EIVL
EntityName = EN
EntityNamePart = ENXP
GeneralTimingSpec = GTS
InstanceIdentifier = II
Integer = INT
Interval = IVL
Money = MO
OrganizationName = ON
PeriodicInterval = PIVL
PersonName = PN
PhysicalQuantity = PQ
Quantity = QTY
Real = REAL
Ratio = RTO
StringCoded = SC
String = ST
TelecomAddress = TEL
TimeStamp = TS
UniversalResourceLocator = URL
UncertainValueProbabilistic = UVP
Address = AD
AddressPart = ADXP
CodedOrdinal = CO
CodedRatio = CR
HistoryWithInterval = HXIT
TelephoneNumber = TN
UncertainValueProbabilisticTimeStamp = UVP_TS
Binary = BIN


# ============================================================================
# Specialized Interval Types - IVL_PIVL and IVL_EIVL variants
# ============================================================================

@dataclass
class IVL_PIVL_TS:
    """
    IVL_PIVL_TS - Interval of Periodic Intervals of Timestamps.
    
    Represents an interval where the bounds are periodic intervals of timestamps.
    """
    low: Optional[PIVL] = None
    high: Optional[PIVL] = None
    width: Optional[PIVL] = None
    center: Optional[PIVL] = None
    
    def to_xml_element(self, element_name: str = "ivl_pivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            self.low.to_xml_element("low", elem)
        if self.high is not None:
            self.high.to_xml_element("high", elem)
        if self.width is not None:
            self.width.to_xml_element("width", elem)
        if self.center is not None:
            self.center.to_xml_element("center", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_PIVL_INT:
    """
    IVL_PIVL_INT - Interval of Periodic Intervals of Integers.
    
    Represents an interval where the bounds are periodic intervals of integers.
    """
    low: Optional[PIVL] = None
    high: Optional[PIVL] = None
    width: Optional[PIVL] = None
    center: Optional[PIVL] = None
    
    def to_xml_element(self, element_name: str = "ivl_pivl_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            self.low.to_xml_element("low", elem)
        if self.high is not None:
            self.high.to_xml_element("high", elem)
        if self.width is not None:
            self.width.to_xml_element("width", elem)
        if self.center is not None:
            self.center.to_xml_element("center", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_PIVL_REAL:
    """
    IVL_PIVL_REAL - Interval of Periodic Intervals of Real Numbers.
    
    Represents an interval where the bounds are periodic intervals of real numbers.
    """
    low: Optional[PIVL] = None
    high: Optional[PIVL] = None
    width: Optional[PIVL] = None
    center: Optional[PIVL] = None
    
    def to_xml_element(self, element_name: str = "ivl_pivl_real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            self.low.to_xml_element("low", elem)
        if self.high is not None:
            self.high.to_xml_element("high", elem)
        if self.width is not None:
            self.width.to_xml_element("width", elem)
        if self.center is not None:
            self.center.to_xml_element("center", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_PIVL_PQ:
    """
    IVL_PIVL_PQ - Interval of Periodic Intervals of Physical Quantities.
    
    Represents an interval where the bounds are periodic intervals of physical quantities.
    """
    low: Optional[PIVL] = None
    high: Optional[PIVL] = None
    width: Optional[PIVL] = None
    center: Optional[PIVL] = None
    
    def to_xml_element(self, element_name: str = "ivl_pivl_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            self.low.to_xml_element("low", elem)
        if self.high is not None:
            self.high.to_xml_element("high", elem)
        if self.width is not None:
            self.width.to_xml_element("width", elem)
        if self.center is not None:
            self.center.to_xml_element("center", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_PIVL_MO:
    """
    IVL_PIVL_MO - Interval of Periodic Intervals of Monetary Amounts.
    
    Represents an interval where the bounds are periodic intervals of monetary amounts.
    """
    low: Optional[PIVL] = None
    high: Optional[PIVL] = None
    width: Optional[PIVL] = None
    center: Optional[PIVL] = None
    
    def to_xml_element(self, element_name: str = "ivl_pivl_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            self.low.to_xml_element("low", elem)
        if self.high is not None:
            self.high.to_xml_element("high", elem)
        if self.width is not None:
            self.width.to_xml_element("width", elem)
        if self.center is not None:
            self.center.to_xml_element("center", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class IVL_EIVL_TS:
    """
    IVL_EIVL_TS - Interval of Event-related Intervals of Timestamps.
    
    Represents an interval where the bounds are event-related intervals of timestamps.
    """
    low: Optional[EIVL] = None
    high: Optional[EIVL] = None
    width: Optional[EIVL] = None
    center: Optional[EIVL] = None
    
    def to_xml_element(self, element_name: str = "ivl_eivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.low is not None:
            self.low.to_xml_element("low", elem)
        if self.high is not None:
            self.high.to_xml_element("high", elem)
        if self.width is not None:
            self.width.to_xml_element("width", elem)
        if self.center is not None:
            self.center.to_xml_element("center", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


# ============================================================================
# Set Component Types - SXCM variants
# ============================================================================

@dataclass
class SXCM_PIVL_TS:
    """
    SXCM_PIVL_TS - Set Component of Periodic Interval of Timestamps.
    
    Represents a set component where the value is a periodic interval of timestamps.
    """
    value: Optional[PIVL] = None
    operator: Optional[CS] = None  # Set operator (I, E, A, etc.)
    
    def to_xml_element(self, element_name: str = "sxcm_pivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.operator is not None:
            elem.set("operator", str(self.operator))
        
        if self.value is not None:
            self.value.to_xml_element("value", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SXCM_PIVL_INT:
    """
    SXCM_PIVL_INT - Set Component of Periodic Interval of Integers.
    
    Represents a set component where the value is a periodic interval of integers.
    """
    value: Optional[PIVL] = None
    operator: Optional[CS] = None  # Set operator (I, E, A, etc.)
    
    def to_xml_element(self, element_name: str = "sxcm_pivl_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.operator is not None:
            elem.set("operator", str(self.operator))
        
        if self.value is not None:
            self.value.to_xml_element("value", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SXCM_PIVL_REAL:
    """
    SXCM_PIVL_REAL - Set Component of Periodic Interval of Real Numbers.
    
    Represents a set component where the value is a periodic interval of real numbers.
    """
    value: Optional[PIVL] = None
    operator: Optional[CS] = None  # Set operator (I, E, A, etc.)
    
    def to_xml_element(self, element_name: str = "sxcm_pivl_real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.operator is not None:
            elem.set("operator", str(self.operator))
        
        if self.value is not None:
            self.value.to_xml_element("value", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SXCM_PIVL_PQ:
    """
    SXCM_PIVL_PQ - Set Component of Periodic Interval of Physical Quantities.
    
    Represents a set component where the value is a periodic interval of physical quantities.
    """
    value: Optional[PIVL] = None
    operator: Optional[CS] = None  # Set operator (I, E, A, etc.)
    
    def to_xml_element(self, element_name: str = "sxcm_pivl_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.operator is not None:
            elem.set("operator", str(self.operator))
        
        if self.value is not None:
            self.value.to_xml_element("value", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SXCM_PIVL_MO:
    """
    SXCM_PIVL_MO - Set Component of Periodic Interval of Monetary Amounts.
    
    Represents a set component where the value is a periodic interval of monetary amounts.
    """
    value: Optional[PIVL] = None
    operator: Optional[CS] = None  # Set operator (I, E, A, etc.)
    
    def to_xml_element(self, element_name: str = "sxcm_pivl_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.operator is not None:
            elem.set("operator", str(self.operator))
        
        if self.value is not None:
            self.value.to_xml_element("value", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


@dataclass
class SXCM_EIVL_TS:
    """
    SXCM_EIVL_TS - Set Component of Event-related Interval of Timestamps.
    
    Represents a set component where the value is an event-related interval of timestamps.
    """
    value: Optional[EIVL] = None
    operator: Optional[CS] = None  # Set operator (I, E, A, etc.)
    
    def to_xml_element(self, element_name: str = "sxcm_eivl_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is not None:
            elem = ET.SubElement(parent, element_name)
        else:
            elem = ET.Element(element_name)
        
        if self.operator is not None:
            elem.set("operator", str(self.operator))
        
        if self.value is not None:
            self.value.to_xml_element("value", elem)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


# ============================================================================
# Missing HL7 v3 Data Types - Additional Implementations
# ============================================================================

class ANYNonNull(ANY):
    """
    ANYNonNull - Any Non-Null Type.
    
    Represents any HL7 v3 data type that is guaranteed to be non-null.
    Extends ANY but enforces non-null constraint.
    """
    def __init__(self, value: Any = None):
        """Initialize ANYNonNull type."""
        if value is None:
            raise ValueError("ANYNonNull cannot be None")
        super().__init__(value=value)


class EDL:
    """
    EDL - Encapsulated Data List.
    
    Represents a list of encapsulated data elements.
    """
    def __init__(self, items: Optional[List[ED]] = None):
        """
        Initialize EDL type.
        
        Args:
            items: List of encapsulated data elements
        """
        self.items = items or []
    
    def __repr__(self) -> str:
        return f"EDL(items={len(self.items)})"
    
    def to_xml_element(self, element_name: str = "edl", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for item in self.items:
            if hasattr(item, 'to_xml_element'):
                item.to_xml_element("item", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "EDL":
        """Deserialize from XML Element."""
        items = []
        for item_elem in xml_element.findall("item"):
            item = ED.from_xml(item_elem)
            items.append(item)
        return cls(items=items)


class EDL_TS(EDL):
    """EDL_TS - Encapsulated Data List for Timestamps."""
    def __init__(self, items: Optional[List[TS]] = None):
        """Initialize EDL_TS type."""
        super().__init__(items=items or [])


class EDL_PQ(EDL):
    """EDL_PQ - Encapsulated Data List for Physical Quantities."""
    def __init__(self, items: Optional[List[PQ]] = None):
        """Initialize EDL_PQ type."""
        super().__init__(items=items or [])


class EDL_MO(EDL):
    """EDL_MO - Encapsulated Data List for Monetary Amounts."""
    def __init__(self, items: Optional[List[MO]] = None):
        """Initialize EDL_MO type."""
        super().__init__(items=items or [])


class EDL_INT(EDL):
    """EDL_INT - Encapsulated Data List for Integers."""
    def __init__(self, items: Optional[List[int]] = None):
        """Initialize EDL_INT type."""
        super().__init__(items=items or [])


class EDL_REAL(EDL):
    """EDL_REAL - Encapsulated Data List for Real Numbers."""
    def __init__(self, items: Optional[List[float]] = None):
        """Initialize EDL_REAL type."""
        super().__init__(items=items or [])


class PIVL_PQ:
    """
    PIVL_PQ - Periodic Interval for Physical Quantities.
    
    Represents a periodic interval where the period is a physical quantity.
    """
    def __init__(self, period: Optional[PQ] = None, phase: Optional[PQ] = None):
        """
        Initialize PIVL_PQ type.
        
        Args:
            period: Period as a physical quantity
            phase: Phase offset as a physical quantity
        """
        self.period = period
        self.phase = phase
    
    def __repr__(self) -> str:
        return f"PIVL_PQ(period={self.period}, phase={self.phase})"
    
    def to_xml_element(self, element_name: str = "pivl_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.period is not None:
            if hasattr(self.period, 'to_xml_element'):
                self.period.to_xml_element("period", elem)
        
        if self.phase is not None:
            if hasattr(self.phase, 'to_xml_element'):
                self.phase.to_xml_element("phase", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class PIVL_MO:
    """
    PIVL_MO - Periodic Interval for Monetary Amounts.
    
    Represents a periodic interval where the period is a monetary amount.
    """
    def __init__(self, period: Optional[MO] = None, phase: Optional[MO] = None):
        """
        Initialize PIVL_MO type.
        
        Args:
            period: Period as a monetary amount
            phase: Phase offset as a monetary amount
        """
        self.period = period
        self.phase = phase
    
    def __repr__(self) -> str:
        return f"PIVL_MO(period={self.period}, phase={self.phase})"
    
    def to_xml_element(self, element_name: str = "pivl_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.period is not None:
            if hasattr(self.period, 'to_xml_element'):
                self.period.to_xml_element("period", elem)
        
        if self.phase is not None:
            if hasattr(self.phase, 'to_xml_element'):
                self.phase.to_xml_element("phase", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class PPD_MO(PPD):
    """
    PPD_MO - Probability Distribution for Monetary Amount.
    
    A probability distribution where the value is a monetary amount.
    """
    def __init__(self, amount: Optional[MO] = None, mean: Optional[float] = None,
                 standard_deviation: Optional[float] = None):
        """Initialize PPD_MO type."""
        super().__init__(mean=mean, standard_deviation=standard_deviation)
        self.amount = amount


class PPD_INT(PPD):
    """
    PPD_INT - Probability Distribution for Integer.
    
    A probability distribution where the value is an integer.
    """
    def __init__(self, value: Optional[int] = None, mean: Optional[float] = None,
                 standard_deviation: Optional[float] = None):
        """Initialize PPD_INT type."""
        super().__init__(mean=mean, standard_deviation=standard_deviation)
        self.value = value


class PPD_REAL(PPD):
    """
    PPD_REAL - Probability Distribution for Real Number.
    
    A probability distribution where the value is a real number.
    """
    def __init__(self, value: Optional[float] = None, mean: Optional[float] = None,
                 standard_deviation: Optional[float] = None):
        """Initialize PPD_REAL type."""
        super().__init__(mean=mean, standard_deviation=standard_deviation)
        self.value = value


class QSET:
    """
    QSET - Qualified Set.
    
    Represents a set with qualification criteria.
    """
    def __init__(self, elements: Optional[List[Any]] = None, qualification: Optional[str] = None):
        """
        Initialize QSET type.
        
        Args:
            elements: List of elements in the set
            qualification: Qualification criteria
        """
        self.elements = elements or []
        self.qualification = qualification
    
    def __repr__(self) -> str:
        return f"QSET(elements={len(self.elements)}, qualification={self.qualification})"
    
    def to_xml_element(self, element_name: str = "qset", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.qualification is not None:
            elem.set("qualification", self.qualification)
        
        for element in self.elements:
            if hasattr(element, 'to_xml_element'):
                element.to_xml_element("element", elem)
            else:
                elem_elem = ET.SubElement(elem, "element")
                elem_elem.text = str(element)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class QSET_TS(QSET):
    """QSET_TS - Qualified Set for Timestamps."""
    def __init__(self, elements: Optional[List[TS]] = None, qualification: Optional[str] = None):
        """Initialize QSET_TS type."""
        super().__init__(elements=elements or [], qualification=qualification)


class QSET_PQ(QSET):
    """QSET_PQ - Qualified Set for Physical Quantities."""
    def __init__(self, elements: Optional[List[PQ]] = None, qualification: Optional[str] = None):
        """Initialize QSET_PQ type."""
        super().__init__(elements=elements or [], qualification=qualification)


class QSET_MO(QSET):
    """QSET_MO - Qualified Set for Monetary Amounts."""
    def __init__(self, elements: Optional[List[MO]] = None, qualification: Optional[str] = None):
        """Initialize QSET_MO type."""
        super().__init__(elements=elements or [], qualification=qualification)


class RTO_INT_INT:
    """
    RTO_INT_INT - Ratio of Integers.
    
    Represents a ratio where both numerator and denominator are integers.
    """
    def __init__(self, numerator: Optional[int] = None, denominator: Optional[int] = None):
        """
        Initialize RTO_INT_INT type.
        
        Args:
            numerator: Numerator value
            denominator: Denominator value
        """
        self.numerator = numerator
        self.denominator = denominator
    
    def __repr__(self) -> str:
        return f"RTO_INT_INT({self.numerator}/{self.denominator})"
    
    def to_xml_element(self, element_name: str = "rto_int_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.numerator is not None:
            num_elem = ET.SubElement(elem, "numerator")
            num_elem.text = str(self.numerator)
        
        if self.denominator is not None:
            den_elem = ET.SubElement(elem, "denominator")
            den_elem.text = str(self.denominator)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class RTO_MO_MO:
    """
    RTO_MO_MO - Ratio of Monetary Amounts.
    
    Represents a ratio where both numerator and denominator are monetary amounts.
    """
    def __init__(self, numerator: Optional[MO] = None, denominator: Optional[MO] = None):
        """
        Initialize RTO_MO_MO type.
        
        Args:
            numerator: Numerator monetary amount
            denominator: Denominator monetary amount
        """
        self.numerator = numerator
        self.denominator = denominator
    
    def __repr__(self) -> str:
        return f"RTO_MO_MO({self.numerator}/{self.denominator})"
    
    def to_xml_element(self, element_name: str = "rto_mo_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.numerator is not None:
            if hasattr(self.numerator, 'to_xml_element'):
                self.numerator.to_xml_element("numerator", elem)
        
        if self.denominator is not None:
            if hasattr(self.denominator, 'to_xml_element'):
                self.denominator.to_xml_element("denominator", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class RTO_INT_PQ:
    """
    RTO_INT_PQ - Ratio of Integer to Physical Quantity.
    
    Represents a ratio where numerator is an integer and denominator is a physical quantity.
    """
    def __init__(self, numerator: Optional[int] = None, denominator: Optional[PQ] = None):
        """
        Initialize RTO_INT_PQ type.
        
        Args:
            numerator: Numerator integer value
            denominator: Denominator physical quantity
        """
        self.numerator = numerator
        self.denominator = denominator
    
    def __repr__(self) -> str:
        return f"RTO_INT_PQ({self.numerator}/{self.denominator})"
    
    def to_xml_element(self, element_name: str = "rto_int_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.numerator is not None:
            num_elem = ET.SubElement(elem, "numerator")
            num_elem.text = str(self.numerator)
        
        if self.denominator is not None:
            if hasattr(self.denominator, 'to_xml_element'):
                self.denominator.to_xml_element("denominator", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SLIST_INT:
    """
    SLIST_INT - Sequence List for Integers.
    
    Represents an ordered sequence of integer values.
    """
    def __init__(self, values: Optional[List[int]] = None):
        """
        Initialize SLIST_INT type.
        
        Args:
            values: List of integer values
        """
        self.values = values or []
    
    def __repr__(self) -> str:
        return f"SLIST_INT(values={len(self.values)})"
    
    def to_xml_element(self, element_name: str = "slist_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for value in self.values:
            val_elem = ET.SubElement(elem, "value")
            val_elem.text = str(value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SLIST_MO:
    """
    SLIST_MO - Sequence List for Monetary Amounts.
    
    Represents an ordered sequence of monetary amounts.
    """
    def __init__(self, values: Optional[List[MO]] = None):
        """
        Initialize SLIST_MO type.
        
        Args:
            values: List of monetary amounts
        """
        self.values = values or []
    
    def __repr__(self) -> str:
        return f"SLIST_MO(values={len(self.values)})"
    
    def to_xml_element(self, element_name: str = "slist_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for value in self.values:
            if hasattr(value, 'to_xml_element'):
                value.to_xml_element("value", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXCM_INT:
    """
    SXCM_INT - Set Component for Integer.
    
    Represents a set component where the value is an integer.
    """
    def __init__(self, value: Optional[int] = None, operator: Optional[str] = None):
        """
        Initialize SXCM_INT type.
        
        Args:
            value: Integer value
            operator: Set operator (e.g., "I", "E", "P")
        """
        self.value = value
        self.operator = operator
    
    def __repr__(self) -> str:
        return f"SXCM_INT(value={self.value}, operator={self.operator})"
    
    def to_xml_element(self, element_name: str = "sxcm_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.operator is not None:
            elem.set("operator", self.operator)
        
        if self.value is not None:
            elem.text = str(self.value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXCM_MO:
    """
    SXCM_MO - Set Component for Monetary Amount.
    
    Represents a set component where the value is a monetary amount.
    """
    def __init__(self, value: Optional[MO] = None, operator: Optional[str] = None):
        """
        Initialize SXCM_MO type.
        
        Args:
            value: Monetary amount value
            operator: Set operator (e.g., "I", "E", "P")
        """
        self.value = value
        self.operator = operator
    
    def __repr__(self) -> str:
        return f"SXCM_MO(value={self.value}, operator={self.operator})"
    
    def to_xml_element(self, element_name: str = "sxcm_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.operator is not None:
            elem.set("operator", self.operator)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXCM_REAL:
    """
    SXCM_REAL - Set Component for Real Number.
    
    Represents a set component where the value is a real number.
    """
    def __init__(self, value: Optional[float] = None, operator: Optional[str] = None):
        """
        Initialize SXCM_REAL type.
        
        Args:
            value: Real number value
            operator: Set operator (e.g., "I", "E", "P")
        """
        self.value = value
        self.operator = operator
    
    def __repr__(self) -> str:
        return f"SXCM_REAL(value={self.value}, operator={self.operator})"
    
    def to_xml_element(self, element_name: str = "sxcm_real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.operator is not None:
            elem.set("operator", self.operator)
        
        if self.value is not None:
            elem.text = str(self.value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXPR_INT:
    """
    SXPR_INT - Set Expression for Integer.
    
    Represents a set expression combining multiple integer set components.
    """
    def __init__(self, components: Optional[List[SXCM_INT]] = None):
        """
        Initialize SXPR_INT type.
        
        Args:
            components: List of integer set components
        """
        self.components = components or []
    
    def __repr__(self) -> str:
        return f"SXPR_INT(components={len(self.components)})"
    
    def to_xml_element(self, element_name: str = "sxpr_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element("component", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXPR_MO:
    """
    SXPR_MO - Set Expression for Monetary Amount.
    
    Represents a set expression combining multiple monetary amount set components.
    """
    def __init__(self, components: Optional[List[SXCM_MO]] = None):
        """
        Initialize SXPR_MO type.
        
        Args:
            components: List of monetary amount set components
        """
        self.components = components or []
    
    def __repr__(self) -> str:
        return f"SXPR_MO(components={len(self.components)})"
    
    def to_xml_element(self, element_name: str = "sxpr_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element("component", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXPR_PQ:
    """
    SXPR_PQ - Set Expression for Physical Quantity.
    
    Represents a set expression combining multiple physical quantity set components.
    """
    def __init__(self, components: Optional[List[SXCM_PQ]] = None):
        """
        Initialize SXPR_PQ type.
        
        Args:
            components: List of physical quantity set components
        """
        self.components = components or []
    
    def __repr__(self) -> str:
        return f"SXPR_PQ(components={len(self.components)})"
    
    def to_xml_element(self, element_name: str = "sxpr_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element("component", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXPR_REAL:
    """
    SXPR_REAL - Set Expression for Real Number.
    
    Represents a set expression combining multiple real number set components.
    """
    def __init__(self, components: Optional[List[SXCM_REAL]] = None):
        """
        Initialize SXPR_REAL type.
        
        Args:
            components: List of real number set components
        """
        self.components = components or []
    
    def __repr__(self) -> str:
        return f"SXPR_REAL(components={len(self.components)})"
    
    def to_xml_element(self, element_name: str = "sxpr_real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for component in self.components:
            if hasattr(component, 'to_xml_element'):
                component.to_xml_element("component", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class HXIT_TS:
    """
    HXIT_TS - History with Interval for Timestamp.
    
    Represents history information with an interval where the value is a timestamp.
    """
    def __init__(self, value: Optional[TS] = None, valid_time: Optional[IVL_TS] = None):
        """
        Initialize HXIT_TS type.
        
        Args:
            value: Timestamp value
            valid_time: Valid time interval
        """
        self.value = value
        self.valid_time = valid_time
    
    def __repr__(self) -> str:
        return f"HXIT_TS(value={self.value}, valid_time={self.valid_time})"
    
    def to_xml_element(self, element_name: str = "hxit_ts", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
        
        if self.valid_time is not None:
            if hasattr(self.valid_time, 'to_xml_element'):
                self.valid_time.to_xml_element("validTime", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class HXIT_PQ:
    """
    HXIT_PQ - History with Interval for Physical Quantity.
    
    Represents history information with an interval where the value is a physical quantity.
    """
    def __init__(self, value: Optional[PQ] = None, valid_time: Optional[IVL_TS] = None):
        """
        Initialize HXIT_PQ type.
        
        Args:
            value: Physical quantity value
            valid_time: Valid time interval
        """
        self.value = value
        self.valid_time = valid_time
    
    def __repr__(self) -> str:
        return f"HXIT_PQ(value={self.value}, valid_time={self.valid_time})"
    
    def to_xml_element(self, element_name: str = "hxit_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
        
        if self.valid_time is not None:
            if hasattr(self.valid_time, 'to_xml_element'):
                self.valid_time.to_xml_element("validTime", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class HXIT_MO:
    """
    HXIT_MO - History with Interval for Monetary Amount.
    
    Represents history information with an interval where the value is a monetary amount.
    """
    def __init__(self, value: Optional[MO] = None, valid_time: Optional[IVL_TS] = None):
        """
        Initialize HXIT_MO type.
        
        Args:
            value: Monetary amount value
            valid_time: Valid time interval
        """
        self.value = value
        self.valid_time = valid_time
    
    def __repr__(self) -> str:
        return f"HXIT_MO(value={self.value}, valid_time={self.valid_time})"
    
    def to_xml_element(self, element_name: str = "hxit_mo", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
        
        if self.valid_time is not None:
            if hasattr(self.valid_time, 'to_xml_element'):
                self.valid_time.to_xml_element("validTime", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class HXIT_INT:
    """
    HXIT_INT - History with Interval for Integer.
    
    Represents history information with an interval where the value is an integer.
    """
    def __init__(self, value: Optional[int] = None, valid_time: Optional[IVL_TS] = None):
        """
        Initialize HXIT_INT type.
        
        Args:
            value: Integer value
            valid_time: Valid time interval
        """
        self.value = value
        self.valid_time = valid_time
    
    def __repr__(self) -> str:
        return f"HXIT_INT(value={self.value}, valid_time={self.valid_time})"
    
    def to_xml_element(self, element_name: str = "hxit_int", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            val_elem = ET.SubElement(elem, "value")
            val_elem.text = str(self.value)
        
        if self.valid_time is not None:
            if hasattr(self.valid_time, 'to_xml_element'):
                self.valid_time.to_xml_element("validTime", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class HXIT_REAL:
    """
    HXIT_REAL - History with Interval for Real Number.
    
    Represents history information with an interval where the value is a real number.
    """
    def __init__(self, value: Optional[float] = None, valid_time: Optional[IVL_TS] = None):
        """
        Initialize HXIT_REAL type.
        
        Args:
            value: Real number value
            valid_time: Valid time interval
        """
        self.value = value
        self.valid_time = valid_time
    
    def __repr__(self) -> str:
        return f"HXIT_REAL(value={self.value}, valid_time={self.valid_time})"
    
    def to_xml_element(self, element_name: str = "hxit_real", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.value is not None:
            val_elem = ET.SubElement(elem, "value")
            val_elem.text = str(self.value)
        
        if self.valid_time is not None:
            if hasattr(self.valid_time, 'to_xml_element'):
                self.valid_time.to_xml_element("validTime", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class GLIST:
    """
    GLIST - Generated List.
    
    Represents a generated list of values following a pattern.
    """
    def __init__(self, start: Optional[Any] = None, increment: Optional[Any] = None,
                 count: Optional[int] = None):
        """
        Initialize GLIST type.
        
        Args:
            start: Starting value
            increment: Increment value
            count: Number of values to generate
        """
        self.start = start
        self.increment = increment
        self.count = count
    
    def __repr__(self) -> str:
        return f"GLIST(start={self.start}, increment={self.increment}, count={self.count})"
    
    def to_xml_element(self, element_name: str = "glist", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.start is not None:
            if hasattr(self.start, 'to_xml_element'):
                self.start.to_xml_element("start", elem)
            else:
                start_elem = ET.SubElement(elem, "start")
                start_elem.text = str(self.start)
        
        if self.increment is not None:
            if hasattr(self.increment, 'to_xml_element'):
                self.increment.to_xml_element("increment", elem)
            else:
                inc_elem = ET.SubElement(elem, "increment")
                inc_elem.text = str(self.increment)
        
        if self.count is not None:
            count_elem = ET.SubElement(elem, "count")
            count_elem.text = str(self.count)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class GLIST_TS(GLIST):
    """GLIST_TS - Generated List for Timestamps."""
    def __init__(self, start: Optional[TS] = None, increment: Optional[PQ] = None,
                 count: Optional[int] = None):
        """Initialize GLIST_TS type."""
        super().__init__(start=start, increment=increment, count=count)


class GLIST_PQ(GLIST):
    """GLIST_PQ - Generated List for Physical Quantities."""
    def __init__(self, start: Optional[PQ] = None, increment: Optional[PQ] = None,
                 count: Optional[int] = None):
        """Initialize GLIST_PQ type."""
        super().__init__(start=start, increment=increment, count=count)


class GLIST_MO(GLIST):
    """GLIST_MO - Generated List for Monetary Amounts."""
    def __init__(self, start: Optional[MO] = None, increment: Optional[MO] = None,
                 count: Optional[int] = None):
        """Initialize GLIST_MO type."""
        super().__init__(start=start, increment=increment, count=count)


class GLIST_INT(GLIST):
    """GLIST_INT - Generated List for Integers."""
    def __init__(self, start: Optional[int] = None, increment: Optional[int] = None,
                 count: Optional[int] = None):
        """Initialize GLIST_INT type."""
        super().__init__(start=start, increment=increment, count=count)


class BLIST:
    """
    BLIST - Bounded List.
    
    Represents a bounded list of values.
    """
    def __init__(self, values: Optional[List[Any]] = None, lower_bound: Optional[Any] = None,
                 upper_bound: Optional[Any] = None):
        """
        Initialize BLIST type.
        
        Args:
            values: List of values
            lower_bound: Lower bound value
            upper_bound: Upper bound value
        """
        self.values = values or []
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    
    def __repr__(self) -> str:
        return f"BLIST(values={len(self.values)}, bounds=[{self.lower_bound}, {self.upper_bound}])"
    
    def to_xml_element(self, element_name: str = "blist", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.lower_bound is not None:
            if hasattr(self.lower_bound, 'to_xml_element'):
                self.lower_bound.to_xml_element("lowerBound", elem)
            else:
                lb_elem = ET.SubElement(elem, "lowerBound")
                lb_elem.text = str(self.lower_bound)
        
        if self.upper_bound is not None:
            if hasattr(self.upper_bound, 'to_xml_element'):
                self.upper_bound.to_xml_element("upperBound", elem)
            else:
                ub_elem = ET.SubElement(elem, "upperBound")
                ub_elem.text = str(self.upper_bound)
        
        for value in self.values:
            if hasattr(value, 'to_xml_element'):
                value.to_xml_element("value", elem)
            else:
                val_elem = ET.SubElement(elem, "value")
                val_elem.text = str(value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class BLIST_TS(BLIST):
    """BLIST_TS - Bounded List for Timestamps."""
    def __init__(self, values: Optional[List[TS]] = None, lower_bound: Optional[TS] = None,
                 upper_bound: Optional[TS] = None):
        """Initialize BLIST_TS type."""
        super().__init__(values=values or [], lower_bound=lower_bound, upper_bound=upper_bound)


class BLIST_PQ(BLIST):
    """BLIST_PQ - Bounded List for Physical Quantities."""
    def __init__(self, values: Optional[List[PQ]] = None, lower_bound: Optional[PQ] = None,
                 upper_bound: Optional[PQ] = None):
        """Initialize BLIST_PQ type."""
        super().__init__(values=values or [], lower_bound=lower_bound, upper_bound=upper_bound)


class BLIST_MO(BLIST):
    """BLIST_MO - Bounded List for Monetary Amounts."""
    def __init__(self, values: Optional[List[MO]] = None, lower_bound: Optional[MO] = None,
                 upper_bound: Optional[MO] = None):
        """Initialize BLIST_MO type."""
        super().__init__(values=values or [], lower_bound=lower_bound, upper_bound=upper_bound)


class BLIST_INT(BLIST):
    """BLIST_INT - Bounded List for Integers."""
    def __init__(self, values: Optional[List[int]] = None, lower_bound: Optional[int] = None,
                 upper_bound: Optional[int] = None):
        """Initialize BLIST_INT type."""
        super().__init__(values=values or [], lower_bound=lower_bound, upper_bound=upper_bound)


class COLL:
    """
    COLL - Collection.
    
    Represents a collection of values (unordered set).
    """
    def __init__(self, values: Optional[List[Any]] = None):
        """
        Initialize COLL type.
        
        Args:
            values: List of values in the collection
        """
        self.values = values or []
    
    def __repr__(self) -> str:
        return f"COLL(values={len(self.values)})"
    
    def to_xml_element(self, element_name: str = "coll", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        for value in self.values:
            if hasattr(value, 'to_xml_element'):
                value.to_xml_element("value", elem)
            else:
                val_elem = ET.SubElement(elem, "value")
                val_elem.text = str(value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class COLL_TS(COLL):
    """COLL_TS - Collection for Timestamps."""
    def __init__(self, values: Optional[List[TS]] = None):
        """Initialize COLL_TS type."""
        super().__init__(values=values or [])


class COLL_PQ(COLL):
    """COLL_PQ - Collection for Physical Quantities."""
    def __init__(self, values: Optional[List[PQ]] = None):
        """Initialize COLL_PQ type."""
        super().__init__(values=values or [])


class COLL_MO(COLL):
    """COLL_MO - Collection for Monetary Amounts."""
    def __init__(self, values: Optional[List[MO]] = None):
        """Initialize COLL_MO type."""
        super().__init__(values=values or [])


class COLL_INT(COLL):
    """COLL_INT - Collection for Integers."""
    def __init__(self, values: Optional[List[int]] = None):
        """Initialize COLL_INT type."""
        super().__init__(values=values or [])


class QSP:
    """
    QSP - Query Selection Parameter.
    
    Represents a query selection parameter.
    """
    def __init__(self, name: Optional[str] = None, value: Optional[Any] = None):
        """
        Initialize QSP type.
        
        Args:
            name: Parameter name
            value: Parameter value
        """
        self.name = name
        self.value = value
    
    def __repr__(self) -> str:
        return f"QSP(name={self.name}, value={self.value})"
    
    def to_xml_element(self, element_name: str = "qsp", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.name is not None:
            elem.set("name", self.name)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
            else:
                elem.text = str(self.value)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class QSD:
    """
    QSD - Query Sort Direction.
    
    Represents query sort direction specification.
    """
    def __init__(self, field: Optional[str] = None, direction: Optional[str] = None):
        """
        Initialize QSD type.
        
        Args:
            field: Field name to sort by
            direction: Sort direction ("ASC" or "DESC")
        """
        self.field = field
        self.direction = direction
    
    def __repr__(self) -> str:
        return f"QSD(field={self.field}, direction={self.direction})"
    
    def to_xml_element(self, element_name: str = "qsd", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.field is not None:
            elem.set("field", self.field)
        
        if self.direction is not None:
            elem.set("direction", self.direction)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class SXCM_PQ:
    """
    SXCM_PQ - Set Component for Physical Quantity.
    
    Represents a set component where the value is a physical quantity.
    """
    def __init__(self, value: Optional[PQ] = None, operator: Optional[str] = None):
        """
        Initialize SXCM_PQ type.
        
        Args:
            value: Physical quantity value
            operator: Set operator (e.g., "I", "E", "P")
        """
        self.value = value
        self.operator = operator
    
    def __repr__(self) -> str:
        return f"SXCM_PQ(value={self.value}, operator={self.operator})"
    
    def to_xml_element(self, element_name: str = "sxcm_pq", parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize to XML Element."""
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        
        if self.operator is not None:
            elem.set("operator", self.operator)
        
        if self.value is not None:
            if hasattr(self.value, 'to_xml_element'):
                self.value.to_xml_element("value", elem)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


# ============================================================================
# Missing HL7 v3 Data Types - Additional Implementations (from REMAINING_WORK.md)
# ============================================================================

class BAG_MO(BAG):
    """BAG_MO - Bag of Monetary Amounts."""
    def __init__(self, items: Optional[List[MO]] = None):
        super().__init__(items=items or [])


class BAG_PQ(BAG):
    """BAG_PQ - Bag of Physical Quantities."""
    def __init__(self, items: Optional[List[PQ]] = None):
        super().__init__(items=items or [])


class BAG_TS(BAG):
    """BAG_TS - Bag of Timestamps."""
    def __init__(self, items: Optional[List[TS]] = None):
        super().__init__(items=items or [])


class LIST_REAL(LIST):
    """LIST_REAL - List of Real Numbers."""
    def __init__(self, items: Optional[List[REAL]] = None):
        super().__init__(items=items or [])


class PIVL_INT(PIVL):
    """PIVL_INT - Periodic Interval for Integers."""
    def __init__(self, period: Optional[INT] = None, phase: Optional[INT] = None):
        self.period = period
        self.phase = phase
    
    def __repr__(self) -> str:
        return f"PIVL_INT(period={self.period}, phase={self.phase})"
    
    def to_xml_element(self, element_name: str = "pivl_int", parent: Optional[ET.Element] = None) -> ET.Element:
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.period is not None:
            if hasattr(self.period, 'to_xml_element'):
                self.period.to_xml_element("period", elem)
            else:
                period_elem = ET.SubElement(elem, "period")
                period_elem.text = str(self.period)
        if self.phase is not None:
            if hasattr(self.phase, 'to_xml_element'):
                self.phase.to_xml_element("phase", elem)
            else:
                phase_elem = ET.SubElement(elem, "phase")
                phase_elem.text = str(self.phase)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class PIVL_REAL(PIVL):
    """PIVL_REAL - Periodic Interval for Real Numbers."""
    def __init__(self, period: Optional[REAL] = None, phase: Optional[REAL] = None):
        self.period = period
        self.phase = phase
    
    def __repr__(self) -> str:
        return f"PIVL_REAL(period={self.period}, phase={self.phase})"
    
    def to_xml_element(self, element_name: str = "pivl_real", parent: Optional[ET.Element] = None) -> ET.Element:
        if parent is None:
            elem = ET.Element(element_name)
        else:
            elem = ET.SubElement(parent, element_name)
        if self.period is not None:
            if hasattr(self.period, 'to_xml_element'):
                self.period.to_xml_element("period", elem)
            else:
                period_elem = ET.SubElement(elem, "period")
                period_elem.text = str(self.period)
        if self.phase is not None:
            if hasattr(self.phase, 'to_xml_element'):
                self.phase.to_xml_element("phase", elem)
            else:
                phase_elem = ET.SubElement(elem, "phase")
                phase_elem.text = str(self.phase)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return elem


class QSET_INT(QSET):
    """QSET_INT - Qualified Set for Integers."""
    def __init__(self, elements: Optional[List[INT]] = None, qualification: Optional[str] = None):
        super().__init__(elements=elements or [], qualification=qualification)


class QSET_REAL(QSET):
    """QSET_REAL - Qualified Set for Real Numbers."""
    def __init__(self, elements: Optional[List[REAL]] = None, qualification: Optional[str] = None):
        super().__init__(elements=elements or [], qualification=qualification)


class QTY_INT(QTY):
    """QTY_INT - Quantity for Integers."""
    def __init__(self, value: Optional[INT] = None, unit: Optional[str] = None):
        super().__init__(value=value, unit=unit)


class QTY_MO(QTY):
    """QTY_MO - Quantity for Monetary Amounts."""
    def __init__(self, value: Optional[MO] = None, unit: Optional[str] = None):
        super().__init__(value=value, unit=unit)


class QTY_REAL(QTY):
    """QTY_REAL - Quantity for Real Numbers."""
    def __init__(self, value: Optional[REAL] = None, unit: Optional[str] = None):
        super().__init__(value=value, unit=unit)


class RTO_PQ_REAL(RTO):
    """RTO_PQ_REAL - Ratio of Physical Quantity to Real Number."""
    def __init__(self, numerator: Optional[PQ] = None, denominator: Optional[REAL] = None):
        super().__init__(numerator=numerator, denominator=denominator)


class RTO_REAL_PQ(RTO):
    """RTO_REAL_PQ - Ratio of Real Number to Physical Quantity."""
    def __init__(self, numerator: Optional[REAL] = None, denominator: Optional[PQ] = None):
        super().__init__(numerator=numerator, denominator=denominator)


class RTO_REAL_REAL(RTO):
    """RTO_REAL_REAL - Ratio of Real Number to Real Number."""
    def __init__(self, numerator: Optional[REAL] = None, denominator: Optional[REAL] = None):
        super().__init__(numerator=numerator, denominator=denominator)


class SET_MO(SET):
    """SET_MO - Set of Monetary Amounts."""
    def __init__(self, items: Optional[List[MO]] = None):
        super().__init__(items=items or [])


class SET_PQ(SET):
    """SET_PQ - Set of Physical Quantities."""
    def __init__(self, items: Optional[List[PQ]] = None):
        super().__init__(items=items or [])


class SET_TS(SET):
    """SET_TS - Set of Timestamps."""
    def __init__(self, items: Optional[List[TS]] = None):
        super().__init__(items=items or [])


class SLIST_REAL(SLIST):
    """SLIST_REAL - Sequence List for Real Numbers."""
    def __init__(self, origin: Optional[REAL] = None, scale: Optional[REAL] = None, digits: Optional[List[int]] = None):
        super().__init__(origin=origin, scale=scale, digits=digits or [])
