# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 XML serializer.

Serializes Message model objects back to HL7 v3 XML format.
Enhanced with support for mixed content, processing instructions, comments,
custom namespace prefixes, and XML declaration options.
"""

import xml.etree.ElementTree as ET
from typing import Optional, Dict, List
from datetime import datetime
import time
import logging

from dnhealth.dnhealth_hl7v3.model import ElementNode, Message, Comment, ProcessingInstruction

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def _serialize_element(
    node: ElementNode,
    parent: Optional[ET.Element] = None,
    custom_namespace_prefixes: Optional[Dict[str, str]] = None
) -> ET.Element:
    """
    Recursively serialize an ElementNode to XML element.

    Args:
        node: ElementNode to serialize
        parent: Optional parent XML element
        custom_namespace_prefixes: Optional mapping of namespace URI -> prefix

    Returns:
        XML element
    """
    # Construct tag with namespace if present
    if node.namespace:
        # Use custom prefix if available
        if custom_namespace_prefixes and node.namespace in custom_namespace_prefixes:
            prefix = custom_namespace_prefixes[node.namespace]
            tag = f"{prefix}:{node.name}"
        else:
            tag = f"{{{node.namespace}}}{node.name}"
    else:
        tag = node.name

    # Create element
    element = ET.Element(tag)

    # Add namespace declaration if custom prefix used
    if node.namespace and custom_namespace_prefixes and node.namespace in custom_namespace_prefixes:
        prefix = custom_namespace_prefixes[node.namespace]
        element.set(f"xmlns:{prefix}", node.namespace)

    # Add attributes
    for attr_name, attr_value in node.attributes.items():
        # Handle namespace prefixes in attributes
        if ":" in attr_name:
            prefix, local = attr_name.split(":", 1)
            # Set namespace for prefix if needed
            if custom_namespace_prefixes:
                # Find namespace URI for this prefix
                for ns_uri, ns_prefix in custom_namespace_prefixes.items():
                    if ns_prefix == prefix:
                        element.set(f"xmlns:{prefix}", ns_uri)
                        break
            element.set(attr_name, attr_value)
        else:
            element.set(attr_name, attr_value)

    # Add text content
    if node.text:
        element.text = node.text

    # Handle mixed content if present
    if node.mixed_content:
        for item in node.mixed_content:
            if isinstance(item, str):
                # Text content
                if element.text:
                    element.text += item
                else:
                    element.text = item
            elif isinstance(item, Comment):
                # Comments - ElementTree doesn't support comments directly
                # We'll skip them or use a workaround
                logger.debug(f"Skipping comment during serialization: {item.text[:50]}")
            elif isinstance(item, ProcessingInstruction):
                # Processing instructions - ElementTree doesn't support PIs directly
                logger.debug(f"Skipping processing instruction during serialization: {item.target}")
            elif isinstance(item, ElementNode):
                # Child element
                child_element = _serialize_element(item, element, custom_namespace_prefixes)
                element.append(child_element)
    else:
        # Add children (backward compatibility)
        for child in node.children:
            if isinstance(child, Comment):
                logger.debug(f"Skipping comment during serialization: {child.text[:50]}")
            elif isinstance(child, ProcessingInstruction):
                logger.debug(f"Skipping processing instruction during serialization: {child.target}")
            elif isinstance(child, ElementNode):
                if child.name == "_text":
                    # Handle tail text nodes
                    if element.tail:
                        element.tail += child.text
                    else:
                        element.tail = child.text
                else:
                    child_element = _serialize_element(child, element, custom_namespace_prefixes)
                    element.append(child_element)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return element


def serialize_hl7v3(
    message: Message,
    encoding: str = "UTF-8",
    pretty: bool = False,
    indent: int = 2,
    custom_namespace_prefixes: Optional[Dict[str, str]] = None,
    xml_declaration_options: Optional[Dict[str, str]] = None
) -> str:
    """
    Serialize Message object to HL7 v3 XML format.

    Args:
        message: Message object to serialize
        encoding: XML encoding (default: UTF-8)
        pretty: If True, pretty-print XML with indentation (default: False)
        indent: Number of spaces per indentation level (default: 2)
        custom_namespace_prefixes: Optional mapping of namespace URI -> prefix
        xml_declaration_options: Optional dict with XML declaration options:
            - 'version': XML version (default: '1.0')
            - 'encoding': Character encoding (overrides encoding parameter)
            - 'standalone': Standalone document ('yes' or 'no')

    Returns:
        HL7 v3 XML string
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting HL7v3 XML serialization")
    
    # Get XML declaration options from message if available
    if xml_declaration_options is None and hasattr(message, '_xml_declaration'):
        xml_declaration_options = message._xml_declaration
    
    # Merge XML declaration options
    xml_version = xml_declaration_options.get('version', '1.0') if xml_declaration_options else '1.0'
    xml_encoding = xml_declaration_options.get('encoding', encoding) if xml_declaration_options else encoding
    xml_standalone = xml_declaration_options.get('standalone') if xml_declaration_options else None
    
    root_element = _serialize_element(message.root, custom_namespace_prefixes=custom_namespace_prefixes)

    # Serialize to string
    # Note: ET.tostring returns bytes, we need to decode
    xml_declaration = True
    if xml_standalone is not None:
        # ElementTree doesn't support standalone attribute directly
        # We'll add it manually after serialization
        xml_bytes = ET.tostring(root_element, encoding=xml_encoding, xml_declaration=False)
    else:
        xml_bytes = ET.tostring(root_element, encoding=xml_encoding, xml_declaration=True)
    
    xml_str = xml_bytes.decode(xml_encoding)
    
    # Add XML declaration with standalone if needed
    if xml_standalone is not None:
        xml_str = f'<?xml version="{xml_version}" encoding="{xml_encoding}" standalone="{xml_standalone}"?>\n{xml_str}'
    
    # Pretty-print if requested
    if pretty:
        xml_str = _pretty_print_xml(xml_str, indent=indent)
    
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] HL7v3 XML serialization completed in {elapsed:.2f}s")
    
    return xml_str


def _pretty_print_xml(xml_str: str, indent: int = 2) -> str:
    """
    Pretty-print XML string with indentation.

    Args:
        xml_str: XML string to pretty-print
        indent: Number of spaces per indentation level

    Returns:
        Pretty-printed XML string
    """
    # Parse the XML string
    try:
        root = ET.fromstring(xml_str)
        # Use ElementTree's indent function if available (Python 3.9+)
        if hasattr(ET, 'indent'):
            ET.indent(root, space=" " * indent)
            # Serialize back to string
            xml_bytes = ET.tostring(root, encoding='unicode', xml_declaration=False)
            # Add XML declaration if present in original
            if xml_str.strip().startswith("<?xml"):
                decl = xml_str.split("\n")[0] if "\n" in xml_str else xml_str.split(">")[0] + ">"
                return decl + "\n" + xml_bytes
            return xml_bytes
        else:
            # Manual pretty-printing for older Python versions
            return _manual_pretty_print(xml_str, indent=indent)
    except ET.ParseError:
        # If parsing fails, return original
        return xml_str


def _manual_pretty_print(xml_str: str, indent: int = 2) -> str:
    """
    Manually pretty-print XML string (for Python < 3.9).

    Args:
        xml_str: XML string to pretty-print
        indent: Number of spaces per indentation level

    Returns:
        Pretty-printed XML string
    """
    import re
    
    # Remove existing whitespace between tags
    xml_str = re.sub(r'>\s+<', '><', xml_str)
    
    # Add newlines and indentation
    level = 0
    result = []
    i = 0
    
    while i < len(xml_str):
        if xml_str[i:i+2] == '</':
            # Closing tag
            level -= 1
            result.append('\n' + ' ' * (level * indent))
            while i < len(xml_str) and xml_str[i] != '>':
                result.append(xml_str[i])
                i += 1
            result.append(xml_str[i])
            i += 1
        elif xml_str[i] == '<' and xml_str[i+1] != '/':
            # Opening tag
            if result and result[-1] != '\n':
                result.append('\n' + ' ' * (level * indent))
            while i < len(xml_str) and xml_str[i] != '>':
                result.append(xml_str[i])
                i += 1
            result.append(xml_str[i])
            i += 1
            # Check if self-closing
            if xml_str[i-2:i] == '/>':
                # Self-closing tag, don't increase level
                pass
            else:
                level += 1
        else:
            # Text content
            if xml_str[i].isspace():
                i += 1
            else:
                result.append(xml_str[i])
                i += 1
    
    return ''.join(result)

