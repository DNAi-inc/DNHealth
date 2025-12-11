# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message sequencing support.

Provides functionality to manage and validate message sequence numbers (MSH-13),
including sequence number generation, validation, and gap detection.
"""

import logging
import threading
import time
from datetime import datetime
from typing import List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import Message

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class SequenceNumberManager:
    """
    Manage sequence numbers for HL7 v2.x messages.
    
    This class provides functionality to:
    - Generate sequence numbers for outgoing messages
    - Validate sequence numbers in incoming messages
    - Detect sequence gaps (missing messages)
    """

    def __init__(self, initial_sequence: int = 1):
        """
        Initialize the sequence number manager.
        
        Args:
            initial_sequence: Starting sequence number (default: 1)
        """
        self._current_sequence = initial_sequence
        self._lock = threading.Lock()
        self._received_sequences: List[int] = []
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] SequenceNumberManager initialized "
            f"with initial sequence: {initial_sequence}"
        )

    def get_next_sequence_number(self) -> int:
        """
        Get the next sequence number for an outgoing message.
        
        Returns:
            Next sequence number
        """
        with self._lock:
            sequence = self._current_sequence
            self._current_sequence += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(
                f"[{current_time}] Generated sequence number: {sequence}"
            )
            return sequence

    def validate_sequence_number(        self, message: Message, expected_sequence: Optional[int] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate sequence number in a message.
        
        Args:
            message: The message to validate
            expected_sequence: Optional expected sequence number
            
        Returns:
            Tuple of (is_valid, error_message):
            - is_valid: True if sequence is valid, False otherwise
            - error_message: Error message if invalid, None if valid
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract MSH segment
        msh_segments = message.get_segments("MSH")
        if not msh_segments:
            return False, "Message missing MSH segment"
        
        msh = msh_segments[0]
        
        # Extract MSH-13: Sequence Number
        if len(msh.fields) < 13:
            # MSH-13 is optional, so missing is valid
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sequence validation "
                f"completed in {elapsed:.3f}s (no sequence number)"
            )
            return True, None
        
        sequence_field = msh.field(13)
        sequence_str = sequence_field.value() if sequence_field else None
        
        if not sequence_str:
            # Empty sequence number is valid (optional field)
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sequence validation "
                f"completed in {elapsed:.3f}s (empty sequence number)"
            )
            return True, None
        
        try:
            sequence = int(sequence_str)
        except (ValueError, TypeError):
            return False, f"Invalid sequence number format: {sequence_str}"
        
        # If expected sequence provided, validate against it
        if expected_sequence is not None:
            if sequence != expected_sequence:
                return (
                    False,
                    f"Sequence number mismatch: expected {expected_sequence}, got {sequence}",
                )
        
        # Track received sequence
        with self._lock:
            if sequence not in self._received_sequences:
                self._received_sequences.append(sequence)
                self._received_sequences.sort()
        
        elapsed = time.time() - start_time
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sequence validation "
            f"completed in {elapsed:.3f}s (sequence: {sequence})"
        )

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        
        return True, None

    def check_sequence_gap(
        self, message: Message, last_sequence: Optional[int] = None
    ) -> Tuple[bool, Optional[int]]:
        """
        Check for sequence gaps (missing messages).
        
        Args:
            message: The current message
            last_sequence: Optional last received sequence number
            
        Returns:
            Tuple of (has_gap, gap_size):
            - has_gap: True if gap detected, False otherwise
            - gap_size: Size of gap if detected, None otherwise
        """
        # Extract sequence from message
        msh_segments = message.get_segments("MSH")
        if not msh_segments or len(msh_segments[0].fields) < 13:
            return False, None
        
        sequence_field = msh_segments[0].field(13)
        sequence_str = sequence_field.value() if sequence_field else None
        
        if not sequence_str:
            return False, None
        
        try:
            current_sequence = int(sequence_str)
        except (ValueError, TypeError):
            return False, None
        
        # Check gap against last sequence
        if last_sequence is not None:
            gap_size = current_sequence - last_sequence
            if gap_size > 1:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(
                    f"[{current_time}] Sequence gap detected: "
                    f"last={last_sequence}, current={current_sequence}, gap={gap_size-1}"
                )
                return True, gap_size - 1
        
        # Check gap against received sequences
        with self._lock:
            if self._received_sequences:
                max_received = max(self._received_sequences)
                if current_sequence > max_received + 1:
                    gap_size = current_sequence - max_received - 1
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(
                        f"[{current_time}] Sequence gap detected: "
                        f"max_received={max_received}, current={current_sequence}, gap={gap_size}"
                    )
                    return True, gap_size
        
        return False, None


def validate_message_sequence(
    message: Message, expected_sequence: Optional[int] = None
) -> Tuple[bool, List[str]]:
    """
    Validate message sequence number.
    
    Args:
        message: The message to validate
        expected_sequence: Optional expected sequence number
        
    Returns:
        Tuple of (is_valid, list_of_errors):
        - is_valid: True if valid, False otherwise
        - list_of_errors: List of error messages
    """
    start_time = time.time()
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Validating message sequence")
    
    manager = SequenceNumberManager()
    is_valid, error_msg = manager.validate_sequence_number(message, expected_sequence)
    
    if not is_valid and error_msg:
        errors.append(error_msg)
    
    # Check for gaps
    has_gap, gap_size = manager.check_sequence_gap(message)
    if has_gap and gap_size:
        errors.append(f"Sequence gap detected: {gap_size} message(s) missing")
    
    elapsed = time.time() - start_time

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    logger.info(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message sequence validation "
        f"completed in {elapsed:.3f}s (valid: {is_valid}, errors: {len(errors)})"
    )
    
    return is_valid, errors


def handle_sequence_gap(missing_sequences: List[int]) -> List[str]:
    """
    Handle sequence gap by generating gap report.
    
    Args:
        missing_sequences: List of missing sequence numbers
        
    Returns:
        List of gap information messages
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Handling sequence gap: {len(missing_sequences)} missing sequence(s)")
    
    if not missing_sequences:
        return []
    
    gap_info = []
    
    # Sort sequences
    sorted_sequences = sorted(missing_sequences)
    
    # Group consecutive sequences
    ranges = []
    start = sorted_sequences[0]
    end = sorted_sequences[0]
    
    for seq in sorted_sequences[1:]:
        if seq == end + 1:
            end = seq
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = seq
            end = seq
    
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")
    
    gap_info.append(f"Missing sequence numbers: {', '.join(ranges)}")
    gap_info.append(f"Total missing messages: {len(missing_sequences)}")
    
    elapsed = time.time() - start_time
    logger.info(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sequence gap handling "
        f"completed in {elapsed:.3f}s"
    )
    
    return gap_info
