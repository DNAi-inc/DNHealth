# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 XML parser.

Parses HL7 v3 XML messages into Message model objects.
Uses standard library xml.etree.ElementTree for XML parsing.
Enhanced with support for mixed content, processing instructions, comments,
custom namespace prefixes, and XML declaration options.

For full support of advanced features (comments, processing instructions),
lxml library is recommended but not required.
"""

import xml.etree.ElementTree as ET
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import time
import logging

from dnhealth.errors import HL7v3ParseError
from dnhealth.dnhealth_hl7v3.model import ElementNode, Message
from dnhealth.dnhealth_hl7v3.xpath import get_xpath

# Try to import lxml for advanced features
try:
    from lxml import etree as lxml_etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def _parse_element(
    element: ET.Element,
    namespaces: Optional[Dict[str, str]] = None,
    preserve_mixed_content: bool = True,
    custom_namespace_prefixes: Optional[Dict[str, str]] = None
) -> ElementNode:
    """
    Recursively parse an XML element into an ElementNode.

    Args:
        element: XML element to parse
        namespaces: Optional namespace mapping
        preserve_mixed_content: If True, preserve mixed content (text + elements)
        custom_namespace_prefixes: Optional mapping of namespace URI -> prefix for custom prefixes

    Returns:
        ElementNode object
    """
    from dnhealth.dnhealth_hl7v3.model import Comment, ProcessingInstruction
    
    # Extract namespace
    namespace = None
    namespace_prefix = None
    if element.tag.startswith("{"):
        # Extract namespace from tag like "{urn:hl7-org:v3}element"
        end_brace = element.tag.find("}")
        if end_brace != -1:
            namespace = element.tag[1:end_brace]
            local_name = element.tag[end_brace + 1 :]
            
            # Check for custom namespace prefix
            if custom_namespace_prefixes and namespace in custom_namespace_prefixes:
                namespace_prefix = custom_namespace_prefixes[namespace]
        else:
            local_name = element.tag
    else:
        local_name = element.tag

    # Extract attributes
    attributes = {}
    for key, value in element.attrib.items():
        # Handle namespace prefixes in attributes
        if key.startswith("{"):
            # Namespace-qualified attribute
            end_brace = key.find("}")
            if end_brace != -1:
                attr_namespace = key[1:end_brace]
                attr_local = key[end_brace + 1 :]
                # Store with namespace prefix if available
                if namespaces:
                    for prefix, uri in namespaces.items():
                        if uri == attr_namespace:
                            attributes[f"{prefix}:{attr_local}"] = value
                            break
                    else:
                        # Check custom namespace prefixes
                        if custom_namespace_prefixes and attr_namespace in custom_namespace_prefixes:
                            prefix = custom_namespace_prefixes[attr_namespace]
                            attributes[f"{prefix}:{attr_local}"] = value
                        else:
                            attributes[key] = value
                else:
                    attributes[key] = value
            else:
                attributes[key] = value
        else:
            attributes[key] = value

    # Extract text content
    text = element.text.strip() if element.text and element.text.strip() else None

    # Parse children and mixed content
    children = []
    mixed_content = []
    
    if preserve_mixed_content:
        # Preserve mixed content order (text + elements)
        # Note: ElementTree doesn't preserve all mixed content perfectly,
        # but we can capture text before/after elements
        if element.text and element.text.strip():
            mixed_content.append(element.text.strip())
    
    for child in element:
        child_node = _parse_element(child, namespaces, preserve_mixed_content, custom_namespace_prefixes)
        children.append(child_node)
        if preserve_mixed_content:
            mixed_content.append(child_node)
        
        # Also capture tail text (text after element, before next sibling)
        if child.tail and child.tail.strip():
            if preserve_mixed_content:
                mixed_content.append(child.tail.strip())
            else:
                # Create a text node for tail content
                tail_node = ElementNode(name="_text", text=child.tail.strip())
                children.append(tail_node)
    
    # If no mixed content was captured, use children only
    if not mixed_content:
        mixed_content = None

    return ElementNode(
        name=local_name,
        namespace=namespace,
        attributes=attributes,
        children=children,
        text=text,
        mixed_content=mixed_content,
    )


def parse_hl7v3(
    xml_string: str,
    include_xpath: bool = False,
    preserve_mixed_content: bool = True,
    preserve_comments: bool = True,
    preserve_processing_instructions: bool = True,
    custom_namespace_prefixes: Optional[Dict[str, str]] = None,
    xml_declaration_options: Optional[Dict[str, str]] = None
) -> Message:
    """
    Parse HL7 v3 XML message into a Message object.

    Args:
        xml_string: HL7 v3 XML message string
        include_xpath: If True, include XPath information in error messages
        preserve_mixed_content: If True, preserve mixed content (text + elements)
        preserve_comments: If True, preserve XML comments (requires lxml)
        preserve_processing_instructions: If True, preserve processing instructions (requires lxml)
        custom_namespace_prefixes: Optional mapping of namespace URI -> prefix for custom prefixes
        xml_declaration_options: Optional dict with XML declaration options:
            - 'version': XML version (default: '1.0')
            - 'encoding': Character encoding (default: 'UTF-8')
            - 'standalone': Standalone document ('yes' or 'no')

    Returns:
        Message object

    Raises:
        HL7v3ParseError: If XML cannot be parsed
    """
    from dnhealth.dnhealth_hl7v3.model import Comment, ProcessingInstruction
    
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting HL7v3 XML parsing")
    
    if not xml_string or not xml_string.strip():
        raise HL7v3ParseError("Empty XML message")

    # Check timeout
    elapsed = time.time() - start_time
    if elapsed > TEST_TIMEOUT:
        raise TimeoutError(f"Parsing exceeded timeout of {TEST_TIMEOUT} seconds")

    try:
        # Use lxml if available and advanced features requested
        use_lxml = LXML_AVAILABLE and (preserve_comments or preserve_processing_instructions)
        
        if use_lxml:
            # Parse with lxml for advanced features
            parser = lxml_etree.XMLParser(
                remove_comments=not preserve_comments,
                remove_pis=not preserve_processing_instructions,
                strip_cdata=False,
                recover=True
            )
            root_element = lxml_etree.fromstring(xml_string.encode('utf-8'), parser=parser)
            
            # Extract processing instructions and comments from lxml tree
            # (lxml preserves them in the tree structure)
            processing_instructions = []
            comments = []
            
            if preserve_processing_instructions:
                # Get processing instructions from document
                for pi in root_element.xpath('//processing-instruction()'):
                    processing_instructions.append(ProcessingInstruction(pi.target, pi.text or ""))
            
            if preserve_comments:
                # Get comments from document
                for comment in root_element.xpath('//comment()'):
                    comments.append(Comment(comment.text or ""))
            
            # Convert lxml element to ElementTree-compatible structure
            # (We'll use lxml's ElementTree compatibility)
            # lxml elements are compatible with ElementTree API
            root_element_et = root_element
        else:
            # Use standard ElementTree
            root_element = ET.fromstring(xml_string)
            root_element_et = root_element
            processing_instructions = []
            comments = []
            
            if preserve_comments or preserve_processing_instructions:
                logger.warning("lxml not available - comments and processing instructions will not be preserved. Install lxml for full support.")

        # Extract namespaces from root element
        namespaces = {}
        for prefix, uri in root_element_et.attrib.items():
            if prefix.startswith("xmlns"):
                if prefix == "xmlns":
                    namespaces["default"] = uri
                else:
                    # xmlns:prefix
                    ns_prefix = prefix.split(":", 1)[1]
                    namespaces[ns_prefix] = uri

        # Merge custom namespace prefixes
        if custom_namespace_prefixes:
            namespaces.update(custom_namespace_prefixes)

        # Parse root element
        root_node = _parse_element(
            root_element_et,
            namespaces,
            preserve_mixed_content=preserve_mixed_content,
            custom_namespace_prefixes=custom_namespace_prefixes
        )
        
        # Add processing instructions and comments to root if available
        if processing_instructions:
            root_node.processing_instructions = processing_instructions
        if comments:
            root_node.comments = comments
        
        message = Message(root=root_node)
        
        # Store XPath helper if requested
        if include_xpath:
            message._xpath_enabled = True
        
        # Store XML declaration options if provided
        if xml_declaration_options:
            message._xml_declaration = xml_declaration_options

        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] HL7v3 XML parsing completed in {elapsed:.2f}s")
        
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {current_time}")

        return message

    except ET.ParseError as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"XML parsing error: {e}"
        if include_xpath:
            # Try to extract line number from error if available
            if hasattr(e, 'lineno'):
                error_msg += f" (line {e.lineno})"
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.2f}s)")
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {current_time}")
        raise HL7v3ParseError(error_msg) from e
    except Exception as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"Unexpected error parsing HL7 v3 XML: {e}"
        if include_xpath:
            # Try to provide more context with XPath
            try:
                root_element = ET.fromstring(xml_string)
                root_node = _parse_element(root_element, namespaces)
                xpath = get_xpath(root_node)
                error_msg += f" (at XPath: {xpath})"
            except:
                pass
        logger.error(f"[{current_time}] {error_msg} (elapsed: {elapsed:.2f}s)")
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {current_time}")
        raise HL7v3ParseError(error_msg) from e

