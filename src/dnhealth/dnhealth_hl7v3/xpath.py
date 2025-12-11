# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
XPath utilities for HL7 v3 messages.

Provides functions to generate XPath expressions for element locations
and to find elements by XPath.
"""

from typing import List, Optional

from dnhealth.dnhealth_hl7v3.model import ElementNode
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
def get_xpath(node: ElementNode, root: Optional[ElementNode] = None) -> str:
    """
    Generate XPath expression for an element node.

    Args:
        node: ElementNode to get XPath for
        root: Optional root node (for building path from root)

    Returns:
        XPath expression string
    """
    path_parts = []
    current = node
    
    # Build path from node to root
    while current:
        # Add namespace prefix if present
        name = current.name
        if current.namespace:
            # Use namespace prefix if available, otherwise use full namespace
            ns_prefix = _get_namespace_prefix(current.namespace)
            if ns_prefix:
                name = f"{ns_prefix}:{current.name}"
        
        # Add position if there are siblings with same name
        parent = _get_parent(current, root)
        if parent:
            siblings = [c for c in parent.children if c.name == current.name]
            if len(siblings) > 1:
                index = siblings.index(current) + 1
                name = f"{name}[{index}]"
        
        path_parts.insert(0, name)
        current = parent
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return "/" + "/".join(path_parts)


def _get_parent(node: ElementNode, root: Optional[ElementNode]) -> Optional[ElementNode]:
    """
    Get parent node of given node (helper function).

    Args:
        node: ElementNode to find parent for
        root: Root node to search from

    Returns:
        Parent ElementNode or None
    """
    if root is None:
        return None
    
    # Simple search - find node in tree and return its parent
    def find_parent(current: ElementNode, target: ElementNode, parent: Optional[ElementNode] = None) -> Optional[ElementNode]:
        if current == target:
            return parent
        
        for child in current.children:
            result = find_parent(child, target, current)
            if result is not None:
                return result
        
        return None
    
    result = find_parent(root, node)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return result


def _get_namespace_prefix(namespace: str) -> Optional[str]:
    """
    Get common namespace prefix for HL7 v3 namespaces.

    Args:
        namespace: Namespace URI

    Returns:
        Prefix string or None
    """
    namespace_prefixes = {
        "urn:hl7-org:v3": "hl7",
        "urn:hl7-org:v3:xml-msgs": "hl7",
        "http://www.w3.org/2001/XMLSchema": "xs",
        "http://www.w3.org/2001/XMLSchema-instance": "xsi",
    }
    
    return namespace_prefixes.get(namespace)


def find_by_xpath(root: ElementNode, xpath: str) -> List[ElementNode]:
    """
    Find elements by XPath expression (simplified implementation).

    Args:
        root: Root ElementNode to search from
        xpath: XPath expression (supports simple paths like /root/child/grandchild)

    Returns:
        List of matching ElementNode objects
    """
    # Simple XPath implementation - supports basic path expressions
    # Split by / and filter out empty strings
    parts = [p for p in xpath.split("/") if p]
    
    if not parts:

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return [root]
    
    # Handle absolute path (starts with /)
    if xpath.startswith("/"):
        current_nodes = [root]
    else:
        # Relative path - search from root
        current_nodes = [root]
    
    # Navigate through path parts
    for part in parts:
        next_nodes = []
        
        # Handle index notation like "element[1]"
        if "[" in part and "]" in part:
            name = part[:part.index("[")]
            try:
                index = int(part[part.index("[") + 1:part.index("]")]) - 1  # 1-based to 0-based
            except ValueError:
                name = part
                index = None
        else:
            name = part
            index = None
        
        # Find children with matching name
        for node in current_nodes:
            matching_children = [c for c in node.children if c.name == name]
            if index is not None:
                if 0 <= index < len(matching_children):
                    next_nodes.append(matching_children[index])
            else:
                next_nodes.extend(matching_children)
        
        current_nodes = next_nodes
        
        if not current_nodes:
            break
    
    return current_nodes

