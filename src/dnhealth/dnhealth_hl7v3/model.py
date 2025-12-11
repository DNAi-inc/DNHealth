# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 XML message model classes.

Represents HL7 v3 messages as trees of XML elements with namespace support.
"""

from typing import Dict, List, Optional, Union
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
class ProcessingInstruction:
    """
    Represents an XML processing instruction.
    
    Processing instructions have the form: <?target data?>
    """
    
    def __init__(self, target: str, data: str = ""):
        """
        Initialize processing instruction.
        
        Args:
            target: Processing instruction target
            data: Processing instruction data
        """
        self.target = target
        self.data = data
    
    def __repr__(self) -> str:
        """String representation."""
        return f"ProcessingInstruction(target='{self.target}', data='{self.data}')"
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, ProcessingInstruction):
            return False
        return self.target == other.target and self.data == other.data


class Comment:
    """
    Represents an XML comment.
    
    Comments have the form: <!-- text -->
    """
    
    def __init__(self, text: str):
        """
        Initialize comment.
        
        Args:
            text: Comment text content
        """
        self.text = text
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Comment(text='{self.text[:50]}...' if len(self.text) > 50 else f'Comment(text=\"{self.text}\")')"
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Comment):
            return False
        return self.text == other.text


class ElementNode:
    """
    Represents a generic XML element in an HL7 v3 message.

    Preserves all attributes, namespaces, children, text content, mixed content,
    processing instructions, and comments.
    """

    def __init__(
        self,
        name: str,
        namespace: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        children: Optional[List[Union["ElementNode", Comment, ProcessingInstruction]]] = None,
        text: Optional[str] = None,
        mixed_content: Optional[List[Union[str, "ElementNode", Comment, ProcessingInstruction]]] = None,
        comments: Optional[List[Comment]] = None,
        processing_instructions: Optional[List[ProcessingInstruction]] = None,
    ):
        """
        Initialize element node.

        Args:
            name: Element name (local name)
            namespace: XML namespace URI
            attributes: Dictionary of attribute name -> value
            children: List of child ElementNode objects (or mixed content items)
            text: Text content of element (for simple text-only elements)
            mixed_content: List of mixed content items (text, elements, comments, PIs)
            comments: List of Comment objects associated with this element
            processing_instructions: List of ProcessingInstruction objects associated with this element
        """
        self.name = name
        self.namespace = namespace
        self.attributes = attributes or {}
        self.children = children or []
        self.text = text
        self.mixed_content = mixed_content or []
        self.comments = comments or []
        self.processing_instructions = processing_instructions or []

    def get_attribute(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get attribute value by name.

        Args:
            name: Attribute name
            default: Default value if attribute not found

        Returns:
            Attribute value or default
        """
        result = self.attributes.get(name, default)
        
        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result

    def get_children(self, name: Optional[str] = None) -> List["ElementNode"]:
        """
        Get child elements, optionally filtered by name.
        
        Only returns ElementNode objects, not comments or processing instructions.

        Args:
            name: Optional child element name to filter by

        Returns:
            List of matching child elements
        """
        element_children = [child for child in self.children if isinstance(child, ElementNode)]
        if name is None:
            return element_children

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return [child for child in element_children if child.name == name]
    
    def get_mixed_content(self) -> List[Union[str, "ElementNode", Comment, ProcessingInstruction]]:
        """
        Get mixed content items (text, elements, comments, processing instructions).
        
        Returns:
            List of mixed content items in order
        """

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self.mixed_content if self.mixed_content else self.children
    
    def get_comments(self) -> List[Comment]:
        """
        Get all comments associated with this element.
        
        Returns:
            List of Comment objects
        """
        return self.comments
    
    def get_processing_instructions(self) -> List[ProcessingInstruction]:
        """
        Get all processing instructions associated with this element.
        
        Returns:
            List of ProcessingInstruction objects
        """

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self.processing_instructions

    def get_first_child(self, name: str) -> Optional["ElementNode"]:
        """
        Get first child element with given name.

        Args:
            name: Child element name

        Returns:
            First matching child element or None
        """
        for child in self.children:
            if child.name == name:
                return child
        return None

    def __repr__(self) -> str:
        """String representation."""
        ns_str = f" xmlns='{self.namespace}'" if self.namespace else ""
        attrs_str = " ".join(f"{k}='{v}'" for k, v in self.attributes.items())
        attrs_str = f" {attrs_str}" if attrs_str else ""
        children_str = f" [{len(self.children)} children]" if self.children else ""
        text_str = f" text='{self.text[:20]}...'" if self.text and len(self.text) > 20 else (f" text='{self.text}'" if self.text else "")
        return f"ElementNode(name='{self.name}'{ns_str}{attrs_str}{text_str}{children_str})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, ElementNode):
            return False

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return (
            self.name == other.name
            and self.namespace == other.namespace
            and self.attributes == other.attributes
            and self.children == other.children
            and self.text == other.text
            and self.mixed_content == other.mixed_content
            and self.comments == other.comments
            and self.processing_instructions == other.processing_instructions
        )


class Message:
    """
    Represents a complete HL7 v3 XML message.


    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    Contains root element and provides convenience accessors for common constructs.
    """

    def __init__(self, root: ElementNode):
        """
        Initialize message.

        Args:
            root: Root element node
        """
        self.root = root

    @property
    def root_name(self) -> str:
        """Get root element name."""

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self.root.name

    def get_control_act_process(self) -> Optional[ElementNode]:
        """
        Get controlActProcess element (common HL7 v3 construct).

        Returns:
            controlActProcess element or None
        """
        return self.root.get_first_child("controlActProcess")

    def get_subject(self) -> Optional[ElementNode]:
        """
        Get subject element (common HL7 v3 construct).

        Returns:
            subject element or None
        """
        control_act = self.get_control_act_process()
        if control_act:
            return control_act.get_first_child("subject")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return None
    
    # Type-safe accessors for common HL7v3 constructs
    
    def get_message_id(self) -> Optional[str]:
        """
        Get message ID from common HL7v3 message structure.
        
        Returns:
            Message ID string or None
        """
        # Try common locations for message ID
        id_elem = self.root.get_first_child("id")
        if id_elem:
            return id_elem.get_attribute("root") or id_elem.text
        
        # Try in controlActProcess
        control_act = self.get_control_act_process()
        if control_act:
            id_elem = control_act.get_first_child("id")
            if id_elem:
                result = id_elem.get_attribute("root") or id_elem.text
                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
                return result
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return None
    
    def get_creation_time(self) -> Optional[str]:
        """
        Get creation timestamp from common HL7v3 message structure.
        
        Returns:
            Timestamp string (TS format) or None
        """
        # Try common locations for creation time
        creation_time_elem = self.root.get_first_child("creationTime")
        if creation_time_elem:
            return creation_time_elem.get_attribute("value") or creation_time_elem.text
        
        # Try in controlActProcess

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        control_act = self.get_control_act_process()
        if control_act:
            creation_time_elem = control_act.get_first_child("effectiveTime")
            if creation_time_elem:
                return creation_time_elem.get_attribute("value") or creation_time_elem.text
        

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return None
    
    def get_interaction_id(self) -> Optional[str]:
        """
        Get interaction ID from common HL7v3 message structure.
        
        Returns:
            Interaction ID string or None
        """
        interaction_elem = self.root.get_first_child("interactionId")
        if interaction_elem:
            return interaction_elem.get_attribute("root") or interaction_elem.text

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return None
    
    def get_version_code(self) -> Optional[str]:
        """
        Get version code from common HL7v3 message structure.
        
        Returns:
            Version code string or None
        """
        version_elem = self.root.get_first_child("versionCode")
        if version_elem:
            result = version_elem.get_attribute("code") or version_elem.text
            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return result
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return None
    
    def get_sender(self) -> Optional[ElementNode]:
        """
        Get sender element from common HL7v3 message structure.
        
        Returns:
            Sender element or None
        """
        result = self.root.get_first_child("sender")
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return result
    
    def get_receiver(self) -> Optional[ElementNode]:
        """
        Get receiver element from common HL7v3 message structure.
        
        Returns:
            Receiver element or None
        """
        return self.root.get_first_child("receiver")
    
    def get_acknowledgment(self) -> Optional[ElementNode]:
        """
        Get acknowledgment element from common HL7v3 message structure.
        
        Returns:
            Acknowledgment element or None
        """
        return self.root.get_first_child("acknowledgment")
    
    def get_query_by_parameter(self) -> Optional[ElementNode]:
        """
        Get queryByParameter element (for query messages).
        
        Returns:
            QueryByParameter element or None
        """
        control_act = self.get_control_act_process()
        if control_act:
            return control_act.get_first_child("queryByParameter")
        return None
    
    def get_query_acknowledgment(self) -> Optional[ElementNode]:
        """
        Get queryAcknowledgment element (for query response messages).
        
        Returns:
            QueryAcknowledgment element or None
        """
        control_act = self.get_control_act_process()
        if control_act:
            return control_act.get_first_child("queryAcknowledgment")
        return None

    def __repr__(self) -> str:
        """String representation."""
        return f"Message(root={self.root_name})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Message):
            return False
        return self.root == other.root

