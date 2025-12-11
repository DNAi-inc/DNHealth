# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Message routing utilities for DNHealth library.

Provides configurable message routing based on message type, content, or custom rules.
Supports routing for HL7v2, HL7v3, and FHIR messages to different handlers or destinations.
All routing operations include timestamps in logs for traceability.
"""

import re
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class MessageType(Enum):
    """Types of messages that can be routed."""

    HL7V2 = "hl7v2"
    HL7V3 = "hl7v3"
    FHIR = "fhir"


class RoutingRule:
    """
    Defines a routing rule for messages.

    Routes messages to a destination based on matching conditions.
    """

    def __init__(
        self,
        name: str,
        destination: str,
        condition: Callable[[Any], bool],
        priority: int = 0,
        description: Optional[str] = None,
    ):
        """
        Initialize routing rule.

        Args:
            name: Unique name for the rule
            destination: Destination identifier (handler name, endpoint, etc.)
            condition: Function that takes a message and returns True if rule matches
            priority: Rule priority (higher priority rules are evaluated first)
            description: Optional description of the rule
        """
        self.name = name
        self.destination = destination
        self.condition = condition
        self.priority = priority
        self.description = description

    def matches(self, message: Any) -> bool:
        """
        Check if message matches this rule.

        Args:
            message: Message to check

        Returns:
            True if message matches rule condition, False otherwise
        """
        try:
            return self.condition(message)
        except Exception as e:
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error evaluating rule "
                f"'{self.name}': {str(e)}"
            )
            return False


class MessageRouter:
    """
    Message router for routing messages to different handlers based on rules.

    Supports routing for HL7v2, HL7v3, and FHIR messages. All routing operations
    are logged with timestamps for audit and debugging purposes.
    """

    def __init__(self, default_destination: Optional[str] = None):
        """
        Initialize message router.

        Args:
            default_destination: Default destination for messages that don't match any rule
        """
        self.rules: List[RoutingRule] = []
        self.default_destination = default_destination
        self.routing_history: List[Dict[str, Any]] = []
        self.routed_count = 0
        self.unrouted_count = 0

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - MessageRouter initialized "
            f"with default_destination={default_destination}"
        )

    def add_rule(
        self,
        name: str,
        destination: str,
        condition: Callable[[Any], bool],
        priority: int = 0,        description: Optional[str] = None,
    ) -> None:
        """
        Add a routing rule.

        Args:
            name: Unique name for the rule
            destination: Destination identifier
            condition: Function that takes a message and returns True if rule matches
            priority: Rule priority (higher priority rules are evaluated first)
            description: Optional description of the rule
        """
        rule = RoutingRule(name, destination, condition, priority, description)
        self.rules.append(rule)
        # Sort rules by priority (descending)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Added routing rule '{name}' "
            f"with priority {priority} to destination '{destination}'"
        )

    def add_hl7v2_message_type_rule(
        self,
        name: str,
        destination: str,
        message_types: List[str],
        priority: int = 0,
    ) -> None:
        """
        Add routing rule for HL7v2 message types.

        Args:
            name: Unique name for the rule
            destination: Destination identifier
            message_types: List of HL7v2 message types to route (e.g., ['ADT^A01', 'ADT^A04'])
            priority: Rule priority
        """
        def condition(message):
            try:
                # Check if message has segments (HL7v2 Message object)
                if hasattr(message, 'segments'):
                    msh_segment = None
                    for segment in message.segments:
                        if segment.name == "MSH":
                            msh_segment = segment
                            break

                    if msh_segment and len(msh_segment._field_repetitions) > 8:
                        # MSH-9 is message type (field index 8, 0-based)
                        field_reps = msh_segment._field_repetitions[8]
                        if field_reps:
                            msg_type_field = field_reps[0]
                            if msg_type_field.components:
                                msg_type = msg_type_field.components[0].subcomponents[0].value
                                return msg_type in message_types
            except Exception:
                pass

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return False

        self.add_rule(name, destination, condition, priority, f"Route HL7v2 message types: {message_types}")

    def add_hl7v2_segment_rule(
        self,
        name: str,
        destination: str,
        segment_name: str,
        priority: int = 0,
    ) -> None:
        """
        Add routing rule for HL7v2 messages containing a specific segment.

        Args:
            name: Unique name for the rule
            destination: Destination identifier
            segment_name: Name of segment to match (e.g., 'OBX', 'OBR')
            priority: Rule priority
        """
        def condition(message):
            try:
                if hasattr(message, 'segments'):
                    for segment in message.segments:
                        if segment.name == segment_name:
                            return True
            except Exception:
                pass

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return False

        self.add_rule(
            name,
            destination,
            condition,
            priority,
            f"Route HL7v2 messages containing segment: {segment_name}",
        )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def add_fhir_resource_type_rule(
        self,
        name: str,
        destination: str,
        resource_types: List[str],
        priority: int = 0,
    ) -> None:
        """
        Add routing rule for FHIR resource types.

        Args:
            name: Unique name for the rule
            destination: Destination identifier
            resource_types: List of FHIR resource types to route (e.g., ['Patient', 'Observation'])
            priority: Rule priority
        """
        def condition(resource):
            try:
                if hasattr(resource, 'resourceType'):
                    return resource.resourceType in resource_types
                elif isinstance(resource, dict):
                    return resource.get('resourceType') in resource_types
            except Exception:
                pass

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return False

        self.add_rule(
            name,
            destination,
            condition,
            priority,
            f"Route FHIR resource types: {resource_types}",
        )

    def add_custom_rule(
        self,
        name: str,
        destination: str,
        condition: Callable[[Any], bool],
        priority: int = 0,
        description: Optional[str] = None,
    ) -> None:
        """
        Add custom routing rule.

        Args:
            name: Unique name for the rule
            destination: Destination identifier
            condition: Function that takes a message and returns True if rule matches
            priority: Rule priority
            description: Optional description of the rule
        """
        self.add_rule(name, destination, condition, priority, description)

    def route(self, message: Any) -> Optional[str]:
        """
        Route a message based on configured rules.

        Args:
            message: Message to route (HL7v2 Message, HL7v3 Message, FHIR Resource, etc.)

        Returns:
            Destination identifier if message matched a rule, None otherwise
        """
        timestamp = datetime.now()
        destination = None

        # Evaluate rules in priority order
        for rule in self.rules:
            if rule.matches(message):
                destination = rule.destination
                self.routed_count += 1

                logger.info(
                    f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Message routed to '{destination}' "
                    f"by rule '{rule.name}'"
                )

                self.routing_history.append(
                    {
                        "timestamp": timestamp.isoformat(),
                        "rule_name": rule.name,
                        "destination": destination,
                        "message_type": self._detect_message_type(message),
                    }
                )
                return destination

        # No rule matched
        if self.default_destination:
            destination = self.default_destination
            self.routed_count += 1
            logger.info(
                f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Message routed to default destination "
                f"'{destination}'"
            )
        else:
            self.unrouted_count += 1
            logger.warning(
                f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Message did not match any routing rule "
                f"and no default destination configured"
            )

        self.routing_history.append(
            {
                "timestamp": timestamp.isoformat(),
                "rule_name": None,
                "destination": destination,
                "message_type": self._detect_message_type(message),
            }
        )
        return destination

    def route_to_handler(
        self,
        message: Any,
        handlers: Dict[str, Callable[[Any], Any]],
    ) -> Optional[Any]:
        """
        Route message to a handler function.

        Args:
            message: Message to route
            handlers: Dictionary mapping destination names to handler functions

        Returns:
            Result from handler function, or None if no handler found
        """
        destination = self.route(message)

        if destination and destination in handlers:
            handler = handlers[destination]
            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Executing handler "
                f"'{destination}' for routed message"
            )
            return handler(message)

        logger.warning(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No handler found for destination "
            f"'{destination}'"
        )
        return None

    def _detect_message_type(self, message: Any) -> Optional[str]:
        """Detect message type from message object."""
        try:
            if hasattr(message, 'segments'):
                return MessageType.HL7V2.value
            elif hasattr(message, 'resourceType'):
                return MessageType.FHIR.value
            elif isinstance(message, dict) and 'resourceType' in message:
                return MessageType.FHIR.value
            elif isinstance(message, str) and message.strip().startswith('MSH'):
                return MessageType.HL7V2.value
            elif isinstance(message, str) and message.strip().startswith('<'):
                return MessageType.HL7V3.value
        except Exception:
            pass
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get routing statistics.

        Returns:
            Dictionary with routing statistics
        """
        result = {
            "total_routed": self.routed_count,
            "total_unrouted": self.unrouted_count,
            "total_messages": self.routed_count + self.unrouted_count,
            "routing_rate": (
                self.routed_count / (self.routed_count + self.unrouted_count)
                if (self.routed_count + self.unrouted_count) > 0
                else 0.0
            ),
            "rule_count": len(self.rules),
            "default_destination": self.default_destination,
            "history_count": len(self.routing_history),
        }
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result

    def clear_history(self) -> None:
        """Clear routing history."""
        self.routing_history.clear()
        self.routed_count = 0
        self.unrouted_count = 0
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Routing history cleared"
        )

    def remove_rule(self, name: str) -> bool:
        """
        Remove a routing rule by name.

        Args:
            name: Name of rule to remove

        Returns:
            True if rule was removed, False if not found
        """
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                self.rules.pop(i)
                logger.info(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Removed routing rule '{name}'"
                )
                return True
        return False
