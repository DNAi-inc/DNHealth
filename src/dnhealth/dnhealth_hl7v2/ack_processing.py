# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x acknowledgment message processing.

Provides functionality to process and handle received ACK (acknowledgment) messages,
including status extraction, correlation with original messages, and error handling.
"""

import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import Message

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class AcknowledgmentProcessor:
    """
    Process and handle received ACK (acknowledgment) messages.
    
    This class provides functionality to:
    - Process received ACK messages
    - Extract acknowledgment status
    - Correlate ACK with original message
    - Handle errors from ACK messages
    """

    def __init__(self):
        """Initialize the acknowledgment processor."""
        self.start_time = time.time()
        logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] AcknowledgmentProcessor initialized")

    def process_ack(        self, ack_message: Message, original_message_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Process a received ACK message.
        
        Args:
            ack_message: The ACK message to process
            original_message_id: Optional original message ID for correlation
            
        Returns:
            Dictionary containing:
            - status: ACK status code (AA, AE, AR)
            - status_text: Optional status text from MSA-3
            - original_message_id: Original message control ID from MSA-2
            - errors: List of error messages if status is AE or AR
            - timestamp: Processing timestamp
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Processing ACK message")
        
        result = {
            "status": None,
            "status_text": None,
            "original_message_id": None,
            "errors": [],
            "timestamp": current_time,
        }
        
        try:
            # Extract ACK status
            status, status_text = self.extract_ack_status(ack_message)
            result["status"] = status
            result["status_text"] = status_text
            
            # Extract original message ID from MSA-2
            msa_segments = ack_message.get_segments("MSA")
            if msa_segments:
                msa = msa_segments[0]
                if len(msa.fields) >= 2:
                    original_id = msa.field(2).value()
                    result["original_message_id"] = original_id
                    if original_message_id and original_id != original_message_id:
                        logger.warning(
                            f"[{current_time}] ACK original message ID mismatch: "
                            f"expected {original_message_id}, got {original_id}"
                        )
            
            # Handle errors if status is AE or AR
            if status in ("AE", "AR"):
                errors = self.handle_ack_error(ack_message)
                result["errors"] = errors
                logger.warning(
                    f"[{current_time}] ACK processing found errors: {len(errors)} error(s)"
                )
            
            elapsed_time = time.time() - start_time
            logger.info(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ACK processing completed "
                f"in {elapsed_time:.3f} seconds"
            )
            
        except Exception as e:
            logger.error(f"[{current_time}] Error processing ACK: {e}")
            result["errors"].append(f"Error processing ACK: {str(e)}")
            result["status"] = "AE"
        

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
        return result

    def extract_ack_status(self, ack_message: Message) -> Tuple[str, Optional[str]]:
        """
        Extract acknowledgment status from ACK message.
        
        Args:
            ack_message: The ACK message
            
        Returns:
            Tuple of (status_code, status_text):
            - status_code: AA (Application Accept), AE (Application Error), or AR (Application Reject)
            - status_text: Optional text message from MSA-3
            
        Raises:
            ValueError: If ACK message is invalid or missing MSA segment
        """
        msa_segments = ack_message.get_segments("MSA")
        if not msa_segments:
            raise ValueError("ACK message missing required MSA segment")
        
        msa = msa_segments[0]
        
        # Extract MSA-1: Acknowledgment Code
        if not msa.fields or len(msa.fields) < 1:
            raise ValueError("MSA segment missing acknowledgment code (MSA-1)")
        
        status_code = msa.field(1).value() or ""
        if not status_code:
            raise ValueError("MSA-1 (Acknowledgment Code) is empty")
        
        valid_codes = {"AA", "AE", "AR", "CA", "CE", "CR"}
        if status_code not in valid_codes:
            logger.warning(
                f"Unknown acknowledgment code: {status_code}. "
                f"Expected one of {valid_codes}"
            )
        
        # Extract MSA-3: Text Message (optional)
        status_text = None
        if len(msa.fields) >= 3:
            status_text = msa.field(3).value()
        
        return status_code, status_text

    def correlate_ack_with_original(
        self, ack_message: Message, message_store: Dict[str, Message]
    ) -> Optional[Message]:
        """
        Correlate ACK message with original message from message store.
        
        Args:
            ack_message: The ACK message
            message_store: Dictionary mapping message control IDs to original messages
            
        Returns:
            Original message if found, None otherwise
        """
        msa_segments = ack_message.get_segments("MSA")
        if not msa_segments:
            return None
        
        msa = msa_segments[0]
        if len(msa.fields) < 2:
            return None
        
        original_message_id = msa.field(2).value()
        if not original_message_id:
            return None
        
        return message_store.get(original_message_id)

    def handle_ack_error(self, ack_message: Message) -> List[str]:
        """
        Extract error details from ACK message.
        
        Args:
            ack_message: The ACK message (should have status AE or AR)
            
        Returns:
            List of error messages extracted from ERR segments and MSA fields
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract errors from ERR segments
        err_segments = ack_message.get_segments("ERR")
        for err in err_segments:
            # ERR-4: Error Code (HL7 Error Code)
            if len(err.fields) >= 4:
                error_code = err.field(4).value()
                if error_code:
                    errors.append(f"Error Code: {error_code}")
            
            # ERR-7: Error Text
            if len(err.fields) >= 7:
                error_text = err.field(7).value()
                if error_text:
                    errors.append(f"Error Text: {error_text}")
        
        # Extract error from MSA-3 (Text Message)
        msa_segments = ack_message.get_segments("MSA")
        if msa_segments:
            msa = msa_segments[0]
            if len(msa.fields) >= 3:
                text_message = msa.field(3).value()
                if text_message:
                    errors.append(f"MSA Text Message: {text_message}")
            
            # Extract error from MSA-6 (Error Condition) if present
            if len(msa.fields) >= 6:
                error_condition = msa.field(6).value()
                if error_condition:
                    errors.append(f"Error Condition: {error_condition}")
        
        if not errors:
            errors.append("ACK indicates error (AE/AR) but no error details found")
        
        logger.info(f"[{current_time}] Extracted {len(errors)} error(s) from ACK message")
        
        return errors


def extract_ack_errors(ack_message: Message) -> List[str]:
    """
    Extract error messages from ACK message.
    
    Convenience function that uses AcknowledgmentProcessor to extract errors.
    
    Args:
        ack_message: The ACK message
        
    Returns:
        List of error messages
    """
    processor = AcknowledgmentProcessor()
    return processor.handle_ack_error(ack_message)


class AcknowledgmentTracker:
    """
    Track sent messages and their acknowledgment status.
    
    This class provides functionality to:
    - Track sent messages and wait for their ACKs
    - Store original messages for correlation
    - Provide status queries
    - Support timeout-based waiting
    """

    def __init__(self):
        """Initialize the acknowledgment tracker."""
        self._message_store: Dict[str, Message] = {}
        self._ack_status: Dict[str, Optional[str]] = {}
        self._ack_messages: Dict[str, Message] = {}
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] AcknowledgmentTracker initialized")

    def track_message(self, message_id: str, original_message: Message) -> None:
        """
        Track a sent message and wait for its ACK.
        
        Args:
            message_id: Message control ID (MSH-10)
            original_message: The original message that was sent
        """
        with self._lock:
            self._message_store[message_id] = original_message
            self._ack_status[message_id] = None
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(
                f"[{current_time}] Tracking message {message_id} for acknowledgment"
            )

    def get_ack_status(self, message_id: str) -> Optional[str]:
        """
        Get the ACK status for a tracked message.
        
        Args:
            message_id: Message control ID
            
        Returns:
            ACK status code (AA, AE, AR) if ACK received, None if not yet received
        """
        with self._lock:
            return self._ack_status.get(message_id)

    def record_ack(self, ack_message: Message) -> Optional[str]:
        """
        Record an ACK message for a tracked message.
        
        Args:
            ack_message: The received ACK message
            
        Returns:
            Original message ID if found and ACK recorded, None otherwise
        """
        processor = AcknowledgmentProcessor()
        status, _ = processor.extract_ack_status(ack_message)
        
        msa_segments = ack_message.get_segments("MSA")
        if not msa_segments:
            return None
        
        msa = msa_segments[0]
        if len(msa.fields) < 2:
            return None
        
        original_message_id = msa.field(2).value()
        if not original_message_id:
            return None
        
        with self._lock:
            if original_message_id in self._message_store:
                self._ack_status[original_message_id] = status
                self._ack_messages[original_message_id] = ack_message
                self._condition.notify_all()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{current_time}] Recorded ACK {status} for message {original_message_id}"
                )
                return original_message_id
        
        return None

    def wait_for_ack(
        self, message_id: str, timeout: int = 30
    ) -> Optional[Message]:
        """
        Wait for ACK message for a tracked message.
        
        Args:
            message_id: Message control ID
            timeout: Timeout in seconds (default: 30)
            
        Returns:
            ACK message if received within timeout, None otherwise
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Waiting for ACK for message {message_id} "
            f"(timeout: {timeout}s)"
        )
        
        with self._condition:
            # Check if already received
            if message_id in self._ack_messages:
                elapsed = time.time() - start_time
                logger.info(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ACK already received "
                    f"for message {message_id} (waited {elapsed:.3f}s)"
                )
                return self._ack_messages[message_id]
            
            # Wait for ACK with timeout
            remaining_timeout = timeout
            while remaining_timeout > 0:
                wait_result = self._condition.wait(timeout=min(remaining_timeout, 1.0))
                elapsed = time.time() - start_time
                remaining_timeout = timeout - elapsed
                
                # Check if ACK received
                if message_id in self._ack_messages:
                    logger.info(
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ACK received "
                        f"for message {message_id} after {elapsed:.3f}s"
                    )
                    return self._ack_messages[message_id]
                
                # Check timeout
                if elapsed >= timeout:

                        # Log completion timestamp at end of operation
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logger.info(f"Current Time at End of Operations: {current_time}")
                    logger.warning(
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Timeout waiting "
                        f"for ACK for message {message_id} after {timeout}s"
                    )
                    break
        
        return None

    def get_original_message(self, message_id: str) -> Optional[Message]:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        """
        Get the original message for a tracked message ID.
        
        Args:
            message_id: Message control ID
            
        Returns:
            Original message if found, None otherwise
        """
        with self._lock:
            return self._message_store.get(message_id)

    def get_ack_message(self, message_id: str) -> Optional[Message]:
        """
        Get the ACK message for a tracked message ID.
        
        Args:
            message_id: Message control ID
            
        Returns:
            ACK message if received, None otherwise
        """
        with self._lock:
            return self._ack_messages.get(message_id)
