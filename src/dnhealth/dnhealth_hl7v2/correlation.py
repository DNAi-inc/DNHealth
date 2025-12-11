# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message correlation support.

Provides functionality to track and correlate related messages in conversations,
including query/response pairs, request/acknowledgment pairs, and multi-message conversations.
"""

import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from dnhealth.dnhealth_hl7v2.model import Message

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class MessageCorrelationTracker:
    """
    Track and correlate related messages in conversations.
    
    This class provides functionality to:
    - Correlate messages (e.g., query/response pairs)
    - Track message conversations
    - Link related messages
    - Provide conversation history
    """

    def __init__(self):
        """Initialize the message correlation tracker."""
        self._correlations: Dict[str, List[Message]] = {}
        self._conversations: Dict[str, List[Message]] = {}
        self._message_to_conversation: Dict[str, str] = {}
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] MessageCorrelationTracker initialized")

    def correlate_messages(
        self, original_message: Message, response_message: Message
    ) -> str:
        """
        Correlate two messages (e.g., query and response).
        
        Args:
            original_message: The original message (e.g., query)
            response_message: The response message (e.g., query response)
            
        Returns:
            Correlation ID linking the two messages
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate correlation ID
        correlation_id = generate_correlation_id()
        
        # Extract message control IDs
        original_id = extract_message_control_id(original_message)
        response_id = extract_message_control_id(response_message)
        
        # Store correlation
        self._correlations[correlation_id] = [original_message, response_message]
        
        # Also track in conversations if applicable
        if original_id:
            self._message_to_conversation[original_id] = correlation_id
        if response_id:
            self._message_to_conversation[response_id] = correlation_id
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Correlated messages "
            f"{original_id} and {response_id} with correlation ID {correlation_id} "
            f"(elapsed: {elapsed:.3f}s)"
        )
        
        return correlation_id

    def get_correlated_messages(self, correlation_id: str) -> List[Message]:
        """
        Get all messages correlated with a correlation ID.
        
        Args:
            correlation_id: The correlation ID
            
        Returns:
            List of correlated messages
        """
        return self._correlations.get(correlation_id, [])

    def track_message_conversation(self, initial_message: Message) -> str:
        """
        Start tracking a message conversation.
        
        Args:
            initial_message: The initial message in the conversation
            
        Returns:
            Conversation ID
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate conversation ID
        conversation_id = generate_correlation_id()
        
        # Initialize conversation with initial message
        self._conversations[conversation_id] = [initial_message]
        
        # Track message to conversation mapping
        message_id = extract_message_control_id(initial_message)
        if message_id:
            self._message_to_conversation[message_id] = conversation_id
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Started conversation "
            f"{conversation_id} with message {message_id} (elapsed: {elapsed:.3f}s)"
        )
        
        return conversation_id

    def add_to_conversation(self, conversation_id: str, message: Message) -> None:
        """
        Add a message to an existing conversation.
        
        Args:
            conversation_id: The conversation ID
            message: The message to add
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if conversation_id not in self._conversations:
            logger.warning(
                f"[{current_time}] Conversation {conversation_id} not found, creating new conversation"
            )
            self._conversations[conversation_id] = []
        
        self._conversations[conversation_id].append(message)
        
        # Track message to conversation mapping
        message_id = extract_message_control_id(message)
        if message_id:
            self._message_to_conversation[message_id] = conversation_id
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Added message {message_id} "
            f"to conversation {conversation_id} (elapsed: {elapsed:.3f}s)"
        )

    def get_conversation(self, conversation_id: str) -> List[Message]:
        """
        Get all messages in a conversation.
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            List of messages in the conversation
        """
        return self._conversations.get(conversation_id, [])

    def get_conversation_for_message(self, message_id: str) -> Optional[str]:
        """
        Get the conversation ID for a message.
        
        Args:
            message_id: Message control ID
            
        Returns:
            Conversation ID if found, None otherwise
        """
        return self._message_to_conversation.get(message_id)

    def get_all_conversations(self) -> Dict[str, List[Message]]:
        """
        Get all tracked conversations.
        
        Returns:
            Dictionary mapping conversation IDs to message lists
        """

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self._conversations.copy()


def generate_correlation_id() -> str:
    """
    Generate a unique correlation ID.
    
    Returns:
        Unique correlation ID string

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    """
    return f"CORR-{uuid.uuid4().hex[:16].upper()}"


def extract_correlation_id(message: Message) -> Optional[str]:
    """
    Extract correlation ID from message metadata.
    
    Note: HL7 v2.x doesn't have a standard correlation ID field.
    This function can be extended to extract from custom fields or metadata.
    
    Args:
        message: The message
        
    Returns:
        Correlation ID if found, None otherwise
    """
    # Check if message has correlation ID in metadata

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    if hasattr(message, "metadata") and isinstance(message.metadata, dict):
        return message.metadata.get("correlation_id")
    
    # Could also check custom fields or extensions
    # For now, return None as standard HL7 v2.x doesn't have this
    return None


def extract_message_control_id(message: Message) -> Optional[str]:
    """
    Extract message control ID (MSH-10) from message.
    
    Args:
        message: The message
        
    Returns:
        Message control ID if found, None otherwise
    """
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        return None
    
    msh = msh_segments[0]
    if len(msh.fields) < 10:
        return None
    
    control_id_field = msh.field(10)
    if not control_id_field:
        return None
    
    return control_id_field.value()
