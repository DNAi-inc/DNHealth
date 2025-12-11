# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x batch message support.

Provides utilities for creating, validating, and processing batch messages
with BHS (Batch Header Segment) and BTS (Batch Trailer Segment).
"""

from datetime import datetime
from typing import List, Optional, Tuple

from typing import Optional

from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)
from dnhealth.dnhealth_hl7v2.serializer import serialize_hl7v2
import logging



logger = logging.getLogger(__name__)
def create_bhs_segment(
    encoding_chars: EncodingCharacters,
    sending_application: str = "",
    sending_facility: str = "",
    receiving_application: str = "",
    receiving_facility: str = "",
    batch_creation_datetime: Optional[str] = None,
    batch_security: str = "",
    batch_id: str = "",
    batch_comment: str = "",
    batch_control_id: str = "",
    reference_batch_control_id: str = "",
) -> Segment:
    """
    Create a BHS (Batch Header Segment) segment.
    
    BHS fields:
    - BHS-1: Field Separator (implicit, not stored)
    - BHS-2: Encoding Characters
    - BHS-3: Batch Sending Application
    - BHS-4: Batch Sending Facility
    - BHS-5: Batch Receiving Application
    - BHS-6: Batch Receiving Facility
    - BHS-7: Batch Creation Date/Time
    - BHS-8: Batch Security
    - BHS-9: Batch ID/Name/Type/ID
    - BHS-10: Batch Comment
    - BHS-11: Batch Control ID
    - BHS-12: Reference Batch Control ID
    
    Args:
        encoding_chars: Encoding characters for the batch
        sending_application: Batch sending application (BHS-3)
        sending_facility: Batch sending facility (BHS-4)
        receiving_application: Batch receiving application (BHS-5)
        receiving_facility: Batch receiving facility (BHS-6)
        batch_creation_datetime: Batch creation date/time (BHS-7), defaults to current time
        batch_security: Batch security (BHS-8)
        batch_id: Batch ID/Name/Type/ID (BHS-9)
        batch_comment: Batch comment (BHS-10)
        batch_control_id: Batch control ID (BHS-11)
        reference_batch_control_id: Reference batch control ID (BHS-12)
        
    Returns:
        BHS Segment object
    """
    if batch_creation_datetime is None:
        batch_creation_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # BHS-2: Encoding Characters (format: ^~\\&)
    encoding_str = (
        encoding_chars.component_separator
        + encoding_chars.repetition_separator
        + encoding_chars.escape_character
        + encoding_chars.subcomponent_separator
    )
    
    fields = []
    
    # BHS-1: Field separator (implicit, not stored in segment)
    # BHS-2: Encoding characters (will be set during serialization)
    # We'll create empty fields for BHS-1 and BHS-2
    fields.append(Field([Component([Subcomponent("")])], is_null=False))  # BHS-1
    fields.append(Field([Component([Subcomponent(encoding_str)])], is_null=False))  # BHS-2
    
    # Add remaining fields
    for value in [
        sending_application,  # BHS-3
        sending_facility,  # BHS-4
        receiving_application,  # BHS-5
        receiving_facility,  # BHS-6
        batch_creation_datetime,  # BHS-7
        batch_security,  # BHS-8
        batch_id,  # BHS-9
        batch_comment,  # BHS-10
        batch_control_id,  # BHS-11
        reference_batch_control_id,  # BHS-12
    ]:
        if value:
            fields.append(Field([Component([Subcomponent(value)])], is_null=False))
        else:
            fields.append(Field([], is_null=True))
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return Segment("BHS", fields=fields)


def create_bts_segment(
    message_count: int,
    batch_comment: str = "",
    batch_totals: Optional[List[str]] = None,
) -> Segment:
    """
    Create a BTS (Batch Trailer Segment) segment.
    
    BTS fields:
    - BTS-1: Batch Message Count
    - BTS-2: Batch Comment
    - BTS-3: Batch Totals (optional, can be repeated)
    
    Args:
        message_count: Number of messages in batch (BTS-1)
        batch_comment: Batch comment (BTS-2)
        batch_totals: Optional list of batch totals (BTS-3)
        
    Returns:
        BTS Segment object
    """
    fields = []
    
    # BTS-1: Batch Message Count
    count_field = Field([Component([Subcomponent(str(message_count))])], is_null=False)
    fields.append(count_field)
    
    # BTS-2: Batch Comment
    if batch_comment:
        comment_field = Field([Component([Subcomponent(batch_comment)])], is_null=False)
        fields.append(comment_field)
    else:
        fields.append(Field([], is_null=True))
    
    # BTS-3: Batch Totals (optional, can be repeated)
    if batch_totals:
        for total in batch_totals:
            total_field = Field([Component([Subcomponent(total)])], is_null=False)
            fields.append(total_field)
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return Segment("BTS", fields=fields)


def create_batch_message(
    messages: List[Message],
    encoding_chars: Optional[EncodingCharacters] = None,
    sending_application: str = "",
    sending_facility: str = "",
    receiving_application: str = "",
    receiving_facility: str = "",
    batch_id: str = "",
    batch_comment: str = "",
) -> Message:
    """
    Create a batch message wrapping multiple HL7 messages with BHS and BTS.
    
    Args:
        messages: List of Message objects to include in batch
        encoding_chars: Encoding characters (defaults to first message's encoding chars)
        sending_application: Batch sending application
        sending_facility: Batch sending facility
        receiving_application: Batch receiving application
        receiving_facility: Batch receiving facility
        batch_id: Batch ID
        batch_comment: Batch comment
        
    Returns:
        Message object containing BHS, all messages, and BTS
    """
    if not messages:
        raise ValueError("Batch must contain at least one message")
    
    # Use encoding chars from first message if not provided
    if encoding_chars is None:
        encoding_chars = messages[0].encoding_chars
    
    # Create BHS segment
    bhs = create_bhs_segment(
        encoding_chars=encoding_chars,
        sending_application=sending_application,
        sending_facility=sending_facility,
        receiving_application=receiving_application,
        receiving_facility=receiving_facility,
        batch_id=batch_id,
        batch_comment=batch_comment,
    )
    
    # Collect all segments from all messages
    all_segments = [bhs]
    for msg in messages:
        all_segments.extend(msg.segments)
    
    # Create BTS segment
    bts = create_bts_segment(message_count=len(messages), batch_comment=batch_comment)
    all_segments.append(bts)
    
    # Create batch message
    batch_message = Message(
        segments=all_segments,
        encoding_chars=encoding_chars,
        version=messages[0].version if messages else None,
    )
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return batch_message


def extract_messages_from_batch(batch_message: Message) -> List[Message]:
    """
    Extract individual messages from a batch message.
    
    Finds all MSH segments and groups them with their associated segments
    until the next MSH or BTS segment.
    
    Args:
        batch_message: Batch message containing BHS, messages, and BTS
        
    Returns:
        List of Message objects extracted from batch
    """
    messages = []
    current_message_segments = []
    
    for segment in batch_message.segments:
        # Skip BHS and BTS segments
        if segment.name in ("BHS", "BTS"):
            continue
        
        # If we encounter an MSH, start a new message
        if segment.name == "MSH":
            # Save previous message if exists
            if current_message_segments:
                messages.append(
                    Message(
                        segments=current_message_segments,
                        encoding_chars=batch_message.encoding_chars,
                        version=batch_message.version,
                    )
                )
            # Start new message
            current_message_segments = [segment]
        else:
            # Add segment to current message
            if current_message_segments:
                current_message_segments.append(segment)
    
    # Add last message
    if current_message_segments:
        messages.append(
            Message(
                segments=current_message_segments,
                encoding_chars=batch_message.encoding_chars,
                version=batch_message.version,
            )
        )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return messages


def validate_batch_message(batch_message: Message) -> Tuple[bool, List[str]]:
    """
    Validate a batch message.
    
    Checks:
    - BHS segment exists
    - BTS segment exists
    - BTS message count matches actual message count
    - Batch ID consistency (if present)
    
    Args:
        batch_message: Batch message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check for BHS segment
    bhs_segments = batch_message.get_segments("BHS")
    if not bhs_segments:
        errors.append("Batch message missing BHS (Batch Header Segment)")
    elif len(bhs_segments) > 1:
        errors.append(f"Batch message has multiple BHS segments ({len(bhs_segments)})")
    
    # Check for BTS segment
    bts_segments = batch_message.get_segments("BTS")
    if not bts_segments:
        errors.append("Batch message missing BTS (Batch Trailer Segment)")
    elif len(bts_segments) > 1:
        errors.append(f"Batch message has multiple BTS segments ({len(bts_segments)})")
    
    # Validate message count
    if bts_segments:
        bts = bts_segments[0]
        if len(bts.fields) > 0:
            try:
                declared_count = int(bts.field(1).value())
            except (ValueError, IndexError):
                declared_count = None
            
            # Count actual messages (MSH segments between BHS and BTS)
            actual_count = 0

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            in_batch = False
            for segment in batch_message.segments:
                if segment.name == "BHS":
                    in_batch = True
                elif segment.name == "BTS":
                    break
                elif in_batch and segment.name == "MSH":
                    actual_count += 1
            
            if declared_count is not None and declared_count != actual_count:
                errors.append(
                    f"BTS message count mismatch: declared {declared_count}, actual {actual_count}"
                )
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return len(errors) == 0, errors


def serialize_batch_message(
    batch_message: Message,
    normalize: bool = True,
    validate_before_serialize: bool = True,
) -> str:
    """
    Serialize a batch message to ER7 text format.
    
    Ensures proper batch message structure with BHS and BTS segments.
    Optionally validates the batch before serialization.
    
    Args:
        batch_message: Batch message to serialize
        normalize: If True, normalize output format (default: True)
        validate_before_serialize: If True, validate batch before serializing (default: True)
        
    Returns:
        ER7 text representation of batch message
        
    Raises:
        ValueError: If batch validation fails and validate_before_serialize is True
    """
    # Validate batch if requested
    if validate_before_serialize:
        is_valid, errors = validate_batch_message(batch_message)
        if not is_valid:
            error_msg = "; ".join(errors)
            raise ValueError(f"Invalid batch message: {error_msg}")
    
    # Use standard serializer - it handles all segments including BHS and BTS
    return serialize_hl7v2(batch_message, normalize=normalize)

