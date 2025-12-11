# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Message transformation utilities for DNHealth library.
logger = logging.getLogger(__name__)

Provides configurable message transformation for HL7v2, HL7v3, and FHIR messages.
Supports field mapping, value transformation, version conversion, and custom transformations.
All transformation operations include timestamps in logs for traceability.
"""

import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union
from copy import deepcopy

from dnhealth.util.logging import get_logger

logger = get_logger(__name__)


class TransformationRule:
    """
    Defines a transformation rule for messages.

    Applies transformations to messages based on matching conditions.
    """

    def __init__(
        self,
        name: str,
        condition: Callable[[Any], bool],
        transform_func: Callable[[Any], Any],
        priority: int = 0,
        description: Optional[str] = None,
    ):
        """
        Initialize transformation rule.

        Args:
            name: Unique name for the rule
            condition: Function that takes a message and returns True if rule applies
            transform_func: Function that transforms the message
            priority: Rule priority (higher priority rules are applied first)
            description: Optional description of the rule
        """
        self.name = name
        self.condition = condition
        self.transform_func = transform_func
        self.priority = priority
        self.description = description

    def applies_to(self, message: Any) -> bool:
        """
        Check if transformation rule applies to message.

        Args:
            message: Message to check

        Returns:
            True if rule applies, False otherwise
        """
        try:
            return self.condition(message)
        except Exception as e:
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error evaluating "
                f"transformation rule '{self.name}': {str(e)}"
            )
            return False

    def apply(self, message: Any) -> Any:
        """
        Apply transformation to message.

        Args:
            message: Message to transform

        Returns:
            Transformed message
        """
        try:
            return self.transform_func(message)
        except Exception as e:
            logger.error(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error applying "
                f"transformation rule '{self.name}': {str(e)}"
            )
            raise


class MessageTransformer:
    """
    Message transformer for transforming HL7v2, HL7v3, and FHIR messages.

    Supports multiple transformation rules, field mapping, value transformation,
    and custom transformation functions. All transformations are logged with timestamps.
    """

    def __init__(self):
        """Initialize message transformer."""
        self.rules: List[TransformationRule] = []
        self.transformation_history: List[Dict[str, Any]] = []
        self.transformed_count = 0
        self.failed_count = 0

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - MessageTransformer initialized"
        )

    def add_rule(
        self,
        name: str,
        condition: Callable[[Any], bool],
        transform_func: Callable[[Any], Any],
        priority: int = 0,
        description: Optional[str] = None,
    ) -> None:
        """
        Add a transformation rule.

        Args:
            name: Unique name for the rule
            condition: Function that takes a message and returns True if rule applies
            transform_func: Function that transforms the message
            priority: Rule priority (higher priority rules are applied first)
            description: Optional description of the rule
        """
        rule = TransformationRule(name, condition, transform_func, priority, description)
        self.rules.append(rule)
        # Sort rules by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Added transformation rule "
            f"'{name}' with priority {priority}"
        )

    def remove_rule(self, name: str) -> bool:
        """
        Remove a transformation rule by name.

        Args:
            name: Name of the rule to remove

        Returns:
            True if rule was removed, False if not found
        """
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r.name != name]
        removed = len(self.rules) < initial_count

        if removed:
            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Removed transformation rule '{name}'"
            )
        else:
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Transformation rule '{name}' not found"
            )

        return removed

    def transform(self, message: Any) -> Any:
        """
        Transform a message using applicable rules.

        Args:
            message: Message to transform (HL7v2 Message, HL7v3 Message, FHIR Resource, etc.)

        Returns:
            Transformed message
        """
        timestamp = datetime.now()
        transformed_message = deepcopy(message)
        applied_rules = []

        # Apply rules in priority order
        for rule in self.rules:
            if rule.applies_to(transformed_message):
                try:
                    transformed_message = rule.apply(transformed_message)
                    applied_rules.append(rule.name)
                    logger.debug(
                        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Applied transformation rule "
                        f"'{rule.name}'"
                    )
                except Exception as e:
                    logger.error(
                        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Failed to apply "
                        f"transformation rule '{rule.name}': {str(e)}"
                    )
                    self.failed_count += 1
                    raise

        completion_time = datetime.now()
        elapsed_time = (completion_time - timestamp).total_seconds()
        
        if applied_rules:
            self.transformed_count += 1
            self.transformation_history.append(
                {
                    "timestamp": timestamp.isoformat(),
                    "completion_time": completion_time.isoformat(),
                    "elapsed_seconds": elapsed_time,
                    "applied_rules": applied_rules,
                    "message_type": self._detect_message_type(message),
                }
            )
            logger.info(
                f"{completion_time.strftime('%Y-%m-%d %H:%M:%S')} - Message transformation completed "
                f"using rules: {', '.join(applied_rules)} (elapsed: {elapsed_time:.3f}s)"
            )
        else:
            logger.debug(
                f"{completion_time.strftime('%Y-%m-%d %H:%M:%S')} - No transformation rules applied "
                f"(elapsed: {elapsed_time:.3f}s)"
            )


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return transformed_message

    def add_field_mapping(
        self,
        name: str,
        field_mapping: Dict[str, str],
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a field mapping transformation rule.

        Args:
            name: Unique name for the rule
            field_mapping: Dictionary mapping source field paths to target field paths
            condition: Optional condition function (if None, applies to all messages)
            priority: Rule priority
        """
        def transform_func(msg: Any) -> Any:
            """Apply field mapping transformation."""

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return self._apply_field_mapping(msg, field_mapping)

        if condition is None:
            condition = lambda m: True

        self.add_rule(
            name=name,
            condition=condition,
            transform_func=transform_func,
            priority=priority,
            description=f"Field mapping: {len(field_mapping)} fields",
        )

    def add_value_transformation(
        self,
        name: str,
        field_path: str,
        transform_func: Callable[[Any], Any],
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a value transformation rule for a specific field.

        Args:
            name: Unique name for the rule
            field_path: Path to the field to transform (e.g., "PID.5.1" for HL7v2, "name.family" for FHIR)
            transform_func: Function to transform the field value
            condition: Optional condition function
            priority: Rule priority
        """
        def wrapper(msg: Any) -> Any:
            """Apply value transformation."""
            return self._apply_value_transformation(msg, field_path, transform_func)

        if condition is None:
            condition = lambda m: True

        self.add_rule(
            name=name,
            condition=condition,
            transform_func=wrapper,
            priority=priority,
            description=f"Value transformation for field: {field_path}",
        )

    def add_version_conversion(
        self,
        name: str,
        target_version: str,
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a version conversion transformation rule.

        Args:
            name: Unique name for the rule
            target_version: Target version to convert to
            condition: Optional condition function
            priority: Rule priority
        """
        def transform_func(msg: Any) -> Any:
            """Apply version conversion."""

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return self._apply_version_conversion(msg, target_version)

        if condition is None:
            condition = lambda m: True

        self.add_rule(
            name=name,
            condition=condition,
            transform_func=transform_func,
            priority=priority,
            description=f"Version conversion to {target_version}",
        )

    def _apply_field_mapping(self, message: Any, field_mapping: Dict[str, str]) -> Any:
        """
        Apply field mapping to message.

        Args:
            message: Message to transform
            field_mapping: Dictionary mapping source paths to target paths

        Returns:
            Transformed message
        """
        msg_type = self._detect_message_type(message)

        if msg_type == "hl7v2":
            return self._apply_hl7v2_field_mapping(message, field_mapping)
        elif msg_type == "hl7v3":
            return self._apply_hl7v3_field_mapping(message, field_mapping)
        elif msg_type == "fhir":
            return self._apply_fhir_field_mapping(message, field_mapping)
        else:
            raise ValueError(f"Unsupported message type: {msg_type}")

    def _apply_hl7v2_field_mapping(
        self, message: Any, field_mapping: Dict[str, str]
    ) -> Any:
        """Apply field mapping to HL7v2 message."""
        # Import here to avoid circular dependencies
        from dnhealth.dnhealth_hl7v2.model import Message, Segment

        for source_path, target_path in field_mapping.items():
            # Parse paths like "PID.5.1" -> segment "PID", field 5, component 1
            source_seg, source_field, source_comp = self._parse_hl7v2_path(source_path)
            target_seg, target_field, target_comp = self._parse_hl7v2_path(target_path)

            # Get source value
            segments = message.get_segments(source_seg)
            if segments:
                seg = segments[0]
                if len(seg.fields) > source_field:
                    field = seg.field(source_field + 1)
                    if source_comp is not None:
                        if len(field.components) > source_comp:
                            value = field.component(source_comp + 1).value()
                        else:
                            continue
                    else:
                        value = field.value()

                    # Set target value
                    target_segments = message.get_segments(target_seg)
                    if not target_segments:
                        # Create segment if it doesn't exist
                        target_seg_obj = Segment(target_seg)
                        message.add_segment(target_seg_obj)
                        target_segments = [target_seg_obj]
                    else:
                        target_seg_obj = target_segments[0]

                    # Ensure field exists
                    while len(target_seg_obj.fields) <= target_field:
                        from dnhealth.dnhealth_hl7v2.model import Field
                        target_seg_obj.add_field(Field())

                    target_field_obj = target_seg_obj.field(target_field + 1)
                    if target_comp is not None:
                        # Set component value
                        while len(target_field_obj.components) <= target_comp:
                            from dnhealth.dnhealth_hl7v2.model import Component
                            target_field_obj.add_component(Component())
                        target_field_obj.component(target_comp + 1).set_value(value)
                    else:
                        target_field_obj.set_value(value)

        return message

    def _apply_hl7v3_field_mapping(
        self, message: Any, field_mapping: Dict[str, str]
    ) -> Any:
        """Apply field mapping to HL7v3 message."""
        # HL7v3 uses XPath for field access
        # This is a simplified implementation
        for source_path, target_path in field_mapping.items():
            # Get value from source XPath
            source_value = self._get_xpath_value(message, source_path)
            if source_value is not None:
                # Set value at target XPath
                self._set_xpath_value(message, target_path, source_value)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return message

    def _apply_fhir_field_mapping(
        self, message: Any, field_mapping: Dict[str, str]
    ) -> Any:
        """Apply field mapping to FHIR resource."""
        # Import here to avoid circular dependencies
        from dnhealth.dnhealth_fhir.transform import transform_resource

        return transform_resource(message, field_mapping)

    def _apply_value_transformation(
        self, message: Any, field_path: str, transform_func: Callable[[Any], Any]
    ) -> Any:
        """
        Apply value transformation to a specific field.

        Args:
            message: Message to transform
            field_path: Path to the field
            transform_func: Function to transform the value

        Returns:
            Transformed message
        """
        msg_type = self._detect_message_type(message)
        value = self._get_field_value(message, field_path, msg_type)

        if value is not None:
            transformed_value = transform_func(value)
            self._set_field_value(message, field_path, transformed_value, msg_type)


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return message

    def _apply_version_conversion(self, message: Any, target_version: str) -> Any:
        """
        Apply version conversion to message.

        Args:
            message: Message to convert
            target_version: Target version

        Returns:
            Converted message
        """
        start_time = datetime.now()
        current_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Starting version conversion to {target_version}")
        
        msg_type = self._detect_message_type(message)

        if msg_type == "hl7v2":
            from dnhealth.dnhealth_hl7v2.convert import convert_message_version
            converted_message, warnings = convert_message_version(message, target_version)
            if warnings:
                for warning in warnings:
                    logger.warning(f"[{current_time}] Conversion warning: {warning}")
            return converted_message
        elif msg_type == "hl7v3":
            from dnhealth.dnhealth_hl7v3.convert import convert_message_version
            converted_message, warnings = convert_message_version(message, target_version)
            if warnings:
                for warning in warnings:
                    logger.warning(f"[{current_time}] Conversion warning: {warning}")
            return converted_message
        elif msg_type == "fhir":
            from dnhealth.dnhealth_fhir.convert import convert_resource_version
            converted_resource, warnings = convert_resource_version(message, target_version)
            if warnings:
                for warning in warnings:
                    logger.warning(f"[{current_time}] Conversion warning: {warning}")
            return converted_resource
        else:
            elapsed = (datetime.now() - start_time).total_seconds()
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(
                f"[{completion_time}] Version conversion failed: unsupported message type '{msg_type}' "
                f"(elapsed: {elapsed:.3f}s)"
            )
            # Log completion timestamp at end of operation
            logger.info(f"Current Time at End of Operations: {completion_time}")
            raise ValueError(f"Unsupported message type: {msg_type}")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{completion_time}] Version conversion completed in {elapsed:.3f}s")
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {completion_time}")

    def _parse_hl7v2_path(self, path: str) -> tuple[str, int, Optional[int]]:
        """
        Parse HL7v2 field path like "PID.5.1" into segment, field, component.

        Returns:
            Tuple of (segment_name, field_index, component_index)
        """
        parts = path.split(".")
        segment = parts[0]
        field = int(parts[1]) - 1 if len(parts) > 1 else 0
        component = int(parts[2]) - 1 if len(parts) > 2 else None

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return segment, field, component

    def _get_xpath_value(self, message: Any, xpath: str) -> Any:
        """
        Get value from HL7v3 message using XPath.
        
        Args:
            message: HL7v3 Message object
            xpath: XPath expression to find element
            
        Returns:
            Value from the element (text content or attribute value) or None
        """
        start_time = datetime.now()
        from dnhealth.dnhealth_hl7v3.xpath import find_by_xpath
        
        try:
            # Get root element from message
            if hasattr(message, 'root'):
                root = message.root
            elif hasattr(message, 'get_root'):
                root = message.get_root()
            else:
                root = message
            
            # Find elements matching XPath
            nodes = find_by_xpath(root, xpath)
            
            if nodes:
                # Return text content of first matching node
                node = nodes[0]
                if node.text:
                    result = node.text
                elif node.attributes:
                    # If no text, return first attribute value as fallback
                    result = list(node.attributes.values())[0] if node.attributes else None
                else:
                    result = None
            else:
                result = None
            
            # Log completion timestamp at end of operation
            elapsed = (datetime.now() - start_time).total_seconds()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{current_time}] XPath value retrieval completed in {elapsed:.3f}s")
            logger.info(f"Current Time at End of Operations: {current_time}")
            
            return result
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.warning(
                f"[{current_time}] Error getting XPath value '{xpath}': {str(e)}"
            )
            logger.info(f"Current Time at End of Operations: {current_time}")
            return None

    def _set_xpath_value(self, message: Any, xpath: str, value: Any) -> None:
        """
        Set value in HL7v3 message using XPath.
        
        Args:
            message: HL7v3 Message object
            xpath: XPath expression to find element
            value: Value to set (string for text content)
        """
        start_time = datetime.now()
        from dnhealth.dnhealth_hl7v3.xpath import find_by_xpath
        
        try:
            # Get root element from message
            if hasattr(message, 'root'):
                root = message.root
            elif hasattr(message, 'get_root'):
                root = message.get_root()
            else:
                root = message
            
            # Find elements matching XPath
            nodes = find_by_xpath(root, xpath)
            
            if not nodes:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(
                    f"[{current_time}] XPath '{xpath}' did not match any elements, cannot set value"
                )
                logger.info(f"Current Time at End of Operations: {current_time}")
                return
            
            # Set value on all matching nodes
            for node in nodes:
                # Set text content
                node.text = str(value) if value is not None else None
                # Clear mixed content if setting text
                if node.text and not node.mixed_content:
                    node.mixed_content = []
            
            # Log completion timestamp at end of operation
            elapsed = (datetime.now() - start_time).total_seconds()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(
                f"[{current_time}] XPath value setting completed in {elapsed:.3f}s "
                f"(set value on {len(nodes)} node(s))"
            )
            logger.info(f"Current Time at End of Operations: {current_time}")
            
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(
                f"[{current_time}] Error setting XPath value '{xpath}': {str(e)}"
            )
            logger.info(f"Current Time at End of Operations: {current_time}")
            raise

    def _get_field_value(self, message: Any, field_path: str, msg_type: str) -> Any:
        """Get field value from message."""
        if msg_type == "hl7v2":
            segment, field, component = self._parse_hl7v2_path(field_path)
            segments = message.get_segments(segment)
            if segments:
                seg = segments[0]
                if len(seg.fields) > field:
                    field_obj = seg.field(field + 1)
                    if component is not None:
                        if len(field_obj.components) > component:
                            return field_obj.component(component + 1).value()
                    else:
                        return field_obj.value()
        elif msg_type == "fhir":
            # Use dot notation for FHIR paths
            parts = field_path.split(".")
            value = message
            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                elif isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            return value

        return None

    def _set_field_value(
        self, message: Any, field_path: str, value: Any, msg_type: str
    ) -> None:
        """Set field value in message."""
        if msg_type == "hl7v2":
            segment, field, component = self._parse_hl7v2_path(field_path)
            segments = message.get_segments(segment)
            if segments:
                seg = segments[0]
                if len(seg.fields) > field:
                    field_obj = seg.field(field + 1)
                    if component is not None:
                        while len(field_obj.components) <= component:
                            from dnhealth.dnhealth_hl7v2.model import Component
                            field_obj.add_component(Component())
                        field_obj.component(component + 1).set_value(value)
                    else:
                        field_obj.set_value(value)
        elif msg_type == "fhir":
            # Use dot notation for FHIR paths
            parts = field_path.split(".")
            obj = message
            for part in parts[:-1]:
                if hasattr(obj, part):
                    obj = getattr(obj, part)
                elif isinstance(obj, dict):
                    obj = obj.get(part, {})
                    if not isinstance(obj, dict):
                        return
                else:
                    return
            setattr(obj, parts[-1], value)

    def _detect_message_type(self, message: Any) -> str:
        """
        Detect message type.

        Args:
            message: Message to detect type for

        Returns:
            Message type string: "hl7v2", "hl7v3", or "fhir"
        """
        # Check for HL7v2 Message
        if hasattr(message, "segments") and hasattr(message, "encoding_chars"):
            return "hl7v2"

        # Check for HL7v3 Message
        if hasattr(message, "interaction_id") or (
            isinstance(message, dict) and "interactionId" in message
        ):
            return "hl7v3"

        # Check for FHIR Resource
        if hasattr(message, "resourceType") or (
            isinstance(message, dict) and "resourceType" in message
        ):
            return "fhir"

        # Default to unknown
        return "unknown"

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get transformation statistics.

        Returns:
            Dictionary with transformation statistics
        """
        stats = {
            "total_rules": len(self.rules),
            "transformed_count": self.transformed_count,
            "failed_count": self.failed_count,
            "success_rate": (
                self.transformed_count / (self.transformed_count + self.failed_count)
                if (self.transformed_count + self.failed_count) > 0
                else 0.0
            ),
            "history_size": len(self.transformation_history),
        }
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return stats

    def clear_history(self) -> None:
        """Clear transformation history."""
        current_time = datetime.now()
        self.transformation_history.clear()
        logger.info(
            f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Transformation history cleared"
        )

    def transform_field(
        self,
        message: Any,
        segment_name: str,
        field_index: int,
        transform_func: Callable[[Any], Any],
        component_index: Optional[int] = None,
    ) -> Any:
        """
        Transform a specific field in an HL7v2 message.
        
        Args:
            message: HL7v2 message to transform
            segment_name: Name of the segment (e.g., "PID")
            field_index: Field index (1-based)
            transform_func: Function to transform the field value
            component_index: Optional component index (1-based) for component-level transformation
            
        Returns:
            Transformed message
        """
        start_time = datetime.now()
        logger.debug(
            f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Starting field-level transformation "
            f"for {segment_name}-{field_index}"
        )
        
        try:
            from dnhealth.dnhealth_hl7v2.model import Message, Segment, Field, Component
            
            if not isinstance(message, Message):
                raise ValueError("Field-level transformation only supports HL7v2 messages")
            
            segments = message.get_segments(segment_name)
            if not segments:
                logger.warning(
                    f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Segment {segment_name} not found"
                )
                return message
            
            segment = segments[0]
            if len(segment.fields) < field_index:
                logger.warning(
                    f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Field {field_index} not found "
                    f"in segment {segment_name}"
                )
                return message
            
            field = segment.field(field_index)
            
            if component_index is not None:
                # Transform component
                if len(field.components) < component_index:
                    logger.warning(
                        f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Component {component_index} "
                        f"not found in {segment_name}-{field_index}"
                    )
                    return message
                
                component = field.component(component_index)
                current_value = component.value()
                transformed_value = transform_func(current_value)
                component.set_value(transformed_value)
            else:
                # Transform entire field
                current_value = field.value()
                transformed_value = transform_func(current_value)
                field.set_value(transformed_value)
            
            completion_time = datetime.now()
            elapsed_time = (completion_time - start_time).total_seconds()
            logger.info(
                f"{completion_time.strftime('%Y-%m-%d %H:%M:%S')} - Field-level transformation "
                f"completed for {segment_name}-{field_index} (elapsed: {elapsed_time:.3f}s)"
            )
            
            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return message
            
        except Exception as e:
            completion_time = datetime.now()
            elapsed_time = (completion_time - start_time).total_seconds()
            logger.error(
                f"{completion_time.strftime('%Y-%m-%d %H:%M:%S')} - Field-level transformation "
                f"failed for {segment_name}-{field_index}: {str(e)} (elapsed: {elapsed_time:.3f}s)"
            )
            raise

    def transform_segment(
        self,
        message: Any,
        segment_name: str,
        transform_func: Callable[[Any], Any],
        segment_index: int = 0,
    ) -> Any:
        """
        Transform a specific segment in an HL7v2 message.
        
        Args:
            message: HL7v2 message to transform
            segment_name: Name of the segment (e.g., "PID")
            transform_func: Function to transform the segment (takes Segment, returns Segment)
            segment_index: Index of segment if multiple segments with same name (0-based)
            
        Returns:
            Transformed message
        """
        start_time = datetime.now()
        logger.debug(
            f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Starting segment-level transformation "
            f"for {segment_name}[{segment_index}]"
        )
        
        try:
            from dnhealth.dnhealth_hl7v2.model import Message
            
            if not isinstance(message, Message):
                raise ValueError("Segment-level transformation only supports HL7v2 messages")
            
            segments = message.get_segments(segment_name)
            if not segments or len(segments) <= segment_index:
                logger.warning(
                    f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - Segment {segment_name}[{segment_index}] "
                    f"not found"
                )
                return message
            
            segment = segments[segment_index]
            transformed_segment = transform_func(segment)
            
            # Replace the segment in the message
            # Find the index of the segment in message.segments
            segment_positions = [
                i for i, seg in enumerate(message.segments) 
                if seg.name == segment_name
            ]
            if segment_positions and len(segment_positions) > segment_index:
                message.segments[segment_positions[segment_index]] = transformed_segment
            
            completion_time = datetime.now()
            elapsed_time = (completion_time - start_time).total_seconds()
            logger.info(
                f"{completion_time.strftime('%Y-%m-%d %H:%M:%S')} - Segment-level transformation "
                f"completed for {segment_name}[{segment_index}] (elapsed: {elapsed_time:.3f}s)"
            )
            
            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return message
            
        except Exception as e:
            completion_time = datetime.now()
            elapsed_time = (completion_time - start_time).total_seconds()
            logger.error(
                f"{completion_time.strftime('%Y-%m-%d %H:%M:%S')} - Segment-level transformation "
                f"failed for {segment_name}[{segment_index}]: {str(e)} (elapsed: {elapsed_time:.3f}s)"
            )
            raise

    def add_segment_transformation_rule(
        self,
        name: str,
        segment_name: str,
        transform_func: Callable[[Any], Any],
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a segment-level transformation rule.
        
        Args:
            name: Unique name for the rule
            segment_name: Name of the segment to transform
            transform_func: Function to transform the segment
            condition: Optional condition function
            priority: Rule priority
        """
        def wrapper(msg: Any) -> Any:
            """Apply segment transformation."""
            return self.transform_segment(msg, segment_name, transform_func)
        
        if condition is None:
            condition = lambda m: (
                self._detect_message_type(m) == "hl7v2" and 
                len(m.get_segments(segment_name)) > 0
            )
        
        self.add_rule(
            name=name,
            condition=condition,
            transform_func=wrapper,
            priority=priority,
            description=f"Segment-level transformation for {segment_name}",
        )
        
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Added segment transformation rule "
            f"'{name}' for segment {segment_name}"
        )

    def add_field_transformation_rule(
        self,
        name: str,
        segment_name: str,
        field_index: int,
        transform_func: Callable[[Any], Any],
        component_index: Optional[int] = None,
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a field-level transformation rule.
        
        Args:
            name: Unique name for the rule
            segment_name: Name of the segment
            field_index: Field index (1-based)
            transform_func: Function to transform the field value
            component_index: Optional component index (1-based)
            condition: Optional condition function
            priority: Rule priority
        """
        def wrapper(msg: Any) -> Any:
            """Apply field transformation."""
            return self.transform_field(
                msg, segment_name, field_index, transform_func, component_index
            )
        
        if condition is None:
            condition = lambda m: (
                self._detect_message_type(m) == "hl7v2" and 
                len(m.get_segments(segment_name)) > 0
            )
        
        field_path = f"{segment_name}-{field_index}"
        if component_index:
            field_path += f".{component_index}"
        
        self.add_rule(
            name=name,
            condition=condition,
            transform_func=wrapper,
            priority=priority,
            description=f"Field-level transformation for {field_path}",
        )
        
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Added field transformation rule "
            f"'{name}' for {field_path}"
        )
