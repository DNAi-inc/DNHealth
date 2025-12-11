# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x acknowledgment message generation.

Provides functions to generate ACK (acknowledgment) messages from received messages.
"""

from datetime import datetime
from typing import Optional
import logging

from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)

logger = logging.getLogger(__name__)


def generate_ack(
    original_message: Message,
    acknowledgment_code: str = "AA",
    text_message: Optional[str] = None,
    application_name: Optional[str] = None,
    facility_name: Optional[str] = None,
) -> Message:
    """
    Generate an ACK (acknowledgment) message from an original message.

    Args:
        original_message: The original message to acknowledge
        acknowledgment_code: Acknowledgment code (AA=Application Accept, AE=Application Error, AR=Application Reject)
        text_message: Optional text message for MSA-3
        application_name: Optional application name for MSH-3 (default: from original MSH-5)
        facility_name: Optional facility name for MSH-4 (default: from original MSH-6)

    Returns:
        ACK Message object

    Raises:
        ValueError: If acknowledgment_code is invalid or original message has no MSH segment
    """
    valid_codes = {"AA", "AE", "AR"}
    if acknowledgment_code not in valid_codes:
        raise ValueError(f"Invalid acknowledgment code: {acknowledgment_code}. Must be one of {valid_codes}")

    # Get original MSH segment
    msh_segments = original_message.get_segments("MSH")
    if not msh_segments:
        raise ValueError("Original message must have an MSH segment")

    original_msh = msh_segments[0]
    encoding_chars = original_message.encoding_chars
    version = original_message.version or "2.5"

    # Extract original message control ID (MSH-10)
    original_control_id = ""
    if len(original_msh.fields) >= 10:
        original_control_id = original_msh.field(10).value()

    # Extract original sending/receiving application and facility
    original_sending_app = ""
    original_sending_facility = ""
    original_receiving_app = ""
    original_receiving_facility = ""

    if len(original_msh.fields) >= 3:
        original_sending_app = original_msh.field(3).value()
    if len(original_msh.fields) >= 4:
        original_sending_facility = original_msh.field(4).value()
    if len(original_msh.fields) >= 5:
        original_receiving_app = original_msh.field(5).value()
    if len(original_msh.fields) >= 6:
        original_receiving_facility = original_msh.field(6).value()

    # Use provided names or swap sending/receiving from original
    ack_sending_app = application_name or original_receiving_app or "ACK_APP"
    ack_sending_facility = facility_name or original_receiving_facility or "ACK_FAC"
    ack_receiving_app = original_sending_app or "ORIG_APP"
    ack_receiving_facility = original_sending_facility or "ORIG_FAC"

    # Generate new message control ID (timestamp-based)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_control_id = f"ACK{timestamp}"

    # Build MSH segment for ACK
    # MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|DateTime||ACK^original_msg_type^ACK|ControlID|P|Version|
    msh_fields = []
    
    # MSH-2: Encoding characters (already in encoding_chars)
    msh2_value = (
        encoding_chars.component_separator +
        encoding_chars.repetition_separator +
        encoding_chars.escape_character +
        encoding_chars.subcomponent_separator
    )
    msh_fields.append([Field([Component([Subcomponent(msh2_value)])])])
    
    # MSH-3: Sending Application
    msh_fields.append([Field([Component([Subcomponent(ack_sending_app)])])])
    
    # MSH-4: Sending Facility
    msh_fields.append([Field([Component([Subcomponent(ack_sending_facility)])])])
    
    # MSH-5: Receiving Application
    msh_fields.append([Field([Component([Subcomponent(ack_receiving_app)])])])
    
    # MSH-6: Receiving Facility
    msh_fields.append([Field([Component([Subcomponent(ack_receiving_facility)])])])
    
    # MSH-7: Date/Time
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    msh_fields.append([Field([Component([Subcomponent(datetime_str)])])])
    
    # MSH-8: Security (empty)
    msh_fields.append([Field([Component([Subcomponent()])])])
    
    # MSH-9: Message Type (ACK^original_message_type^ACK)
    original_msg_type = ""
    original_trigger_event = ""
    if len(original_msh.fields) >= 9:
        msg_type_field = original_msh.field(9)
        if msg_type_field.components:
            original_msg_type = msg_type_field.component(1).value()
            if len(msg_type_field.components) > 1:
                original_trigger_event = msg_type_field.component(2).value()
    
    ack_msg_type = f"ACK^{original_msg_type}^{original_trigger_event}"
    msh_fields.append([Field([Component([Subcomponent(ack_msg_type)])])])
    
    # MSH-10: Message Control ID
    msh_fields.append([Field([Component([Subcomponent(new_control_id)])])])
    
    # MSH-11: Processing ID (from original or default to P)
    processing_id = "P"
    if len(original_msh.fields) >= 11:
        processing_id = original_msh.field(11).value() or "P"
    msh_fields.append([Field([Component([Subcomponent(processing_id)])])])
    
    # MSH-12: Version ID
    msh_fields.append([Field([Component([Subcomponent(version)])])])
    
    msh_segment = Segment("MSH", field_repetitions=msh_fields)

    # Build MSA segment
    # MSA|AcknowledgmentCode|MessageControlID|TextMessage|ExpectedSequenceNumber|DelayedAckType|ErrorCondition|
    msa_fields = []
    
    # MSA-1: Acknowledgment Code
    msa_fields.append([Field([Component([Subcomponent(acknowledgment_code)])])])
    
    # MSA-2: Message Control ID (from original message)
    msa_fields.append([Field([Component([Subcomponent(original_control_id)])])])
    
    # MSA-3: Text Message (optional)
    if text_message:
        msa_fields.append([Field([Component([Subcomponent(text_message)])])])
    else:
        msa_fields.append([Field([Component([Subcomponent()])])])
    
    # MSA-4: Expected Sequence Number (optional, empty)
    msa_fields.append([Field([Component([Subcomponent()])])])
    
    # MSA-5: Delayed Acknowledgment Type (optional, empty)
    msa_fields.append([Field([Component([Subcomponent()])])])
    
    # MSA-6: Error Condition (optional, empty)
    msa_fields.append([Field([Component([Subcomponent()])])])
    
    msa_segment = Segment("MSA", field_repetitions=msa_fields)

    # Create ACK message
    ack_message = Message(
        segments=[msh_segment, msa_segment],
        encoding_chars=encoding_chars,
        version=version,
    )

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

    return ack_message

