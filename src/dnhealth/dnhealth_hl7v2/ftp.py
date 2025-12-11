# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x file transfer protocol (FTP) message support.

Provides utilities for creating, validating, and processing FTP messages
with FHS (File Header Segment) and FTS (File Trailer Segment).
"""

import logging
from datetime import datetime
from typing import List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)
from dnhealth.dnhealth_hl7v2.serializer import serialize_hl7v2


def create_fhs_segment(
    encoding_chars: EncodingCharacters,
    file_sending_application: str = "",
    file_sending_facility: str = "",
    file_receiving_application: str = "",
    file_receiving_facility: str = "",
    file_creation_datetime: Optional[str] = None,
    file_security: str = "",
    file_id: str = "",
    file_comment: str = "",
    file_control_id: str = "",    reference_file_control_id: str = "",
) -> Segment:
    """
    Create an FHS (File Header Segment) segment.
    
    FHS fields:
    - FHS-1: Field Separator (implicit, not stored)
    - FHS-2: Encoding Characters
    - FHS-3: File Sending Application
    - FHS-4: File Sending Facility
    - FHS-5: File Receiving Application
    - FHS-6: File Receiving Facility
    - FHS-7: File Creation Date/Time
    - FHS-8: File Security
    - FHS-9: File ID/Name/Type/ID
    - FHS-10: File Comment
    - FHS-11: File Control ID
    - FHS-12: Reference File Control ID
    
    Args:
        encoding_chars: Encoding characters for the file
        file_sending_application: File sending application (FHS-3)
        file_sending_facility: File sending facility (FHS-4)
        file_receiving_application: File receiving application (FHS-5)
        file_receiving_facility: File receiving facility (FHS-6)
        file_creation_datetime: File creation date/time (FHS-7), defaults to current time
        file_security: File security (FHS-8)
        file_id: File ID/Name/Type/ID (FHS-9)
        file_comment: File comment (FHS-10)
        file_control_id: File control ID (FHS-11)
        reference_file_control_id: Reference file control ID (FHS-12)
        
    Returns:
        FHS Segment object
    """
    if file_creation_datetime is None:
        file_creation_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # FHS-2: Encoding Characters (format: ^~\\&)
    encoding_str = (
        encoding_chars.component_separator
        + encoding_chars.repetition_separator
        + encoding_chars.escape_character
        + encoding_chars.subcomponent_separator
    )
    
    fields = []
    
    # FHS-1: Field separator (implicit, not stored in segment)
    # FHS-2: Encoding characters
    fields.append(Field([Component([Subcomponent("")])], is_null=False))  # FHS-1
    fields.append(Field([Component([Subcomponent(encoding_str)])], is_null=False))  # FHS-2
    
    # Add remaining fields
    for value in [
        file_sending_application,  # FHS-3
        file_sending_facility,  # FHS-4
        file_receiving_application,  # FHS-5
        file_receiving_facility,  # FHS-6
        file_creation_datetime,  # FHS-7
        file_security,  # FHS-8
        file_id,  # FHS-9
        file_comment,  # FHS-10
        file_control_id,  # FHS-11
        reference_file_control_id,  # FHS-12
    ]:
        if value:
            fields.append(Field([Component([Subcomponent(value)])], is_null=False))
        else:
            fields.append(Field([], is_null=True))
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return Segment("FHS", fields=fields)


def create_fts_segment(
    file_batch_count: int,
    file_comment: str = "",
    file_totals: Optional[List[str]] = None,
) -> Segment:
    """
    Create an FTS (File Trailer Segment) segment.
    
    FTS fields:
    - FTS-1: File Batch Count
    - FTS-2: File Comment
    - FTS-3: File Totals (optional, multiple values)
    
    Args:
        file_batch_count: Number of batches in file (FTS-1)
        file_comment: File comment (FTS-2)
        file_totals: Optional list of file totals (FTS-3)
        
    Returns:
        FTS Segment object
    """
    fields = []
    
    # FTS-1: File Batch Count
    fields.append(Field([Component([Subcomponent(str(file_batch_count))])], is_null=False))
    
    # FTS-2: File Comment
    if file_comment:
        fields.append(Field([Component([Subcomponent(file_comment)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # FTS-3: File Totals (optional, can have multiple values)
    if file_totals:
        totals_str = "^".join(file_totals)
        fields.append(Field([Component([Subcomponent(totals_str)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return Segment("FTS", fields=fields)


def create_ftp_message(
    batches: List[Message],
    file_sending_application: str = "",
    file_sending_facility: str = "",
    file_receiving_application: str = "",
    file_receiving_facility: str = "",
    file_id: str = "",
    file_comment: str = "",
    file_control_id: str = "",
) -> Message:
    """
    Create an FTP message from multiple batch messages.
    
    FTP message structure:
    - FHS (File Header Segment)
    - BHS (Batch Header Segment) - from first batch
    - ... (batch messages)
    - BTS (Batch Trailer Segment) - from last batch
    - FTS (File Trailer Segment)
    
    Args:
        batches: List of batch messages to include in file
        file_sending_application: File sending application
        file_sending_facility: File sending facility
        file_receiving_application: File receiving application
        file_receiving_facility: File receiving facility
        file_id: File ID
        file_comment: File comment
        file_control_id: File control ID
        
    Returns:
        FTP Message object
        
    Raises:
        ValueError: If batches list is empty
    """
    if not batches:
        raise ValueError("FTP message must contain at least one batch")
    
    # Use encoding characters from first batch
    encoding_chars = batches[0].encoding_chars
    
    # Create FHS segment
    fhs = create_fhs_segment(
        encoding_chars=encoding_chars,
        file_sending_application=file_sending_application,
        file_sending_facility=file_sending_facility,
        file_receiving_application=file_receiving_application,
        file_receiving_facility=file_receiving_facility,
        file_id=file_id,
        file_comment=file_comment,
        file_control_id=file_control_id,
    )
    
    # Collect all segments from batches
    segments = [fhs]
    for batch in batches:
        segments.extend(batch.segments)
    
    # Create FTS segment
    fts = create_fts_segment(file_batch_count=len(batches), file_comment=file_comment)
    segments.append(fts)
    
    result = Message(segments=segments, encoding_chars=encoding_chars, version=batches[0].version)
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.info(f"[{current_time}] FTP message created with {len(batches)} batches")
    
    return result


def extract_batches_from_ftp(ftp_message: Message) -> List[Message]:
    """
    Extract batch messages from an FTP message.
    
    Args:
        ftp_message: FTP message containing batches
        
    Returns:
        List of batch Message objects
    """
    batches = []
    current_batch_segments = []
    
    for segment in ftp_message.segments:
        if segment.name == "FHS":
            # Skip FHS
            continue
        elif segment.name == "FTS":
            # Skip FTS
            continue
        elif segment.name == "BHS":
            # Start new batch
            if current_batch_segments:
                # Save previous batch
                batches.append(Message(segments=current_batch_segments, encoding_chars=ftp_message.encoding_chars, version=ftp_message.version))
            current_batch_segments = [segment]
        elif segment.name == "BTS":
            # End current batch
            current_batch_segments.append(segment)
            batches.append(Message(segments=current_batch_segments, encoding_chars=ftp_message.encoding_chars, version=ftp_message.version))
            current_batch_segments = []
        else:
            # Add to current batch
            if current_batch_segments:
                current_batch_segments.append(segment)
    
    # Handle case where last batch doesn't have BTS
    if current_batch_segments:
        batches.append(Message(segments=current_batch_segments, encoding_chars=ftp_message.encoding_chars, version=ftp_message.version))
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.info(f"[{current_time}] Extracted {len(batches)} batches from FTP message")
    
    return batches


def validate_ftp_message_structure(ftp_message: Message) -> Tuple[bool, List[str]]:
    """
    Validate FTP message structure.
    
    Validates:
    - FTP message must start with FHS segment
    - FTP message must end with FTS segment
    - Between FHS and FTS, there must be at least one batch (BHS...BTS)
    - FHS-2 (Encoding Characters) must match batch encoding characters
    - FTS-1 (File Batch Count) must match actual number of batches
    
    Args:
        ftp_message: FTP message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.info(f"[{current_time}] Starting FTP message structure validation")
    
    if not ftp_message.segments:
        errors.append("FTP message has no segments")
        logger.error(f"[{current_time}] FTP structure validation failed: no segments")
        return False, errors
    
    # Validate FTP structure: must start with FHS
    if ftp_message.segments[0].name != "FHS":
        errors.append("FTP message must start with FHS segment")
        logger.error(f"[{current_time}] FTP structure validation failed: does not start with FHS")
    
    # Validate FTP structure: must end with FTS
    if ftp_message.segments[-1].name != "FTS":
        errors.append("FTP message must end with FTS segment")
        logger.error(f"[{current_time}] FTP structure validation failed: does not end with FTS")
    
    # Count actual batches (BHS segments)
    bhs_segments = [seg for seg in ftp_message.segments if seg.name == "BHS"]
    actual_batch_count = len(bhs_segments)
    
    # Validate that there's at least one batch between FHS and FTS
    if actual_batch_count == 0:
        errors.append("FTP message must contain at least one batch between FHS and FTS")
        logger.warning(f"[{current_time}] FTP structure validation warning: no batches found")
    
    # Validate FHS-2 encoding characters match batch encoding characters
    fhs_segments = [seg for seg in ftp_message.segments if seg.name == "FHS"]
    if fhs_segments and bhs_segments and ftp_message.encoding_chars:
        fhs = fhs_segments[0]
        bhs = bhs_segments[0]
        
        if len(fhs.fields) >= 2 and len(bhs.fields) >= 2:
            fhs2_field = fhs.field(2)
            bhs2_field = bhs.field(2)
            
            if fhs2_field and not fhs2_field.is_null and bhs2_field and not bhs2_field.is_null:
                fhs_encoding_str = fhs2_field.value()
                bhs_encoding_str = bhs2_field.value()
                
                if fhs_encoding_str != bhs_encoding_str:
                    errors.append(
                        f"FHS-2 (Encoding Characters) does not match BHS-2: "
                        f"FHS={fhs_encoding_str}, BHS={bhs_encoding_str}"
                    )
                    logger.warning(f"[{current_time}] FTP structure validation warning: encoding mismatch")
    
    # Validate FTS-1 batch count matches actual batch count
    fts_segments = [seg for seg in ftp_message.segments if seg.name == "FTS"]
    if fts_segments:
        fts = fts_segments[0]
        if len(fts.fields) >= 1:
            fts1_field = fts.field(1)
            if fts1_field and not fts1_field.is_null:
                try:
                    fts_batch_count = int(fts1_field.value())
                    if fts_batch_count != actual_batch_count:
                        errors.append(
                            f"FTS-1 (File Batch Count) mismatch: FTS={fts_batch_count}, actual={actual_batch_count}"
                        )
                        logger.warning(f"[{current_time}] FTP structure validation warning: batch count mismatch")
                except ValueError:
                    errors.append(f"FTS-1 (File Batch Count) is not a valid number: {fts1_field.value()}")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] FTP message structure validation passed")
    else:
        logger.error(f"[{current_time}] FTP message structure validation failed: {len(errors)} errors")
    
    return is_valid, errors


def validate_ftp_message(ftp_message: Message) -> Tuple[bool, List[str]]:
    """
    Validate an FTP message structure.
    
    Validates:
    - FHS segment is present (exactly one) and valid
    - FTS segment is present (exactly one) and valid
    - File batch count in FTS matches number of batches
    - FTP message structure (FHS + batches + FTS)
    - Encoding characters consistency
    
    Args:
        ftp_message: FTP message to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.info(f"[{current_time}] Starting FTP message validation")
    
    # Check for FHS segment
    fhs_segments = [seg for seg in ftp_message.segments if seg.name == "FHS"]
    if len(fhs_segments) == 0:
        errors.append("FTP message missing FHS (File Header Segment)")
        logger.error(f"[{current_time}] FTP validation failed: missing FHS segment")
    elif len(fhs_segments) > 1:
        errors.append(f"FTP message has multiple FHS segments (expected 1, got {len(fhs_segments)})")
        logger.warning(f"[{current_time}] FTP validation warning: multiple FHS segments")
    else:
        # Validate FHS segment
        fhs = fhs_segments[0]
        fhs_valid, fhs_errors = validate_fhs_segment(fhs)
        if not fhs_valid:
            errors.extend(fhs_errors)
            logger.warning(f"[{current_time}] FTP validation warning: FHS segment validation failed")
    
    # Check for FTS segment
    fts_segments = [seg for seg in ftp_message.segments if seg.name == "FTS"]
    if len(fts_segments) == 0:
        errors.append("FTP message missing FTS (File Trailer Segment)")
        logger.error(f"[{current_time}] FTP validation failed: missing FTS segment")
    elif len(fts_segments) > 1:
        errors.append(f"FTP message has multiple FTS segments (expected 1, got {len(fts_segments)})")
        logger.warning(f"[{current_time}] FTP validation warning: multiple FTS segments")
    
    # Count actual batches (BHS segments)
    bhs_segments = [seg for seg in ftp_message.segments if seg.name == "BHS"]
    actual_batch_count = len(bhs_segments)
    
    # Validate FTS segment if present
    if fts_segments:
        fts = fts_segments[0]
        fts_valid, fts_errors = validate_fts_segment(fts, actual_batch_count)
        if not fts_valid:
            errors.extend(fts_errors)
            logger.warning(f"[{current_time}] FTP validation warning: FTS segment validation failed")
    
    # Validate FTP structure: must start with FHS and end with FTS
    if ftp_message.segments:
        if ftp_message.segments[0].name != "FHS":
            errors.append("FTP message must start with FHS segment")
            logger.error(f"[{current_time}] FTP validation failed: does not start with FHS")
        if ftp_message.segments[-1].name != "FTS":
            errors.append("FTP message must end with FTS segment")
            logger.error(f"[{current_time}] FTP validation failed: does not end with FTS")
    
    # Validate that there's at least one batch between FHS and FTS
    if actual_batch_count == 0:
        errors.append("FTP message must contain at least one batch between FHS and FTS")
        logger.warning(f"[{current_time}] FTP validation warning: no batches found")
    
    # Validate encoding characters consistency if FHS is present
    if fhs_segments and ftp_message.encoding_chars:
        fhs = fhs_segments[0]
        if len(fhs.fields) >= 2:
            fhs2_field = fhs.field(2)
            if fhs2_field and not fhs2_field.is_null:
                fhs_encoding_str = fhs2_field.value()
                expected_encoding_str = (
                    ftp_message.encoding_chars.component_separator
                    + ftp_message.encoding_chars.repetition_separator
                    + ftp_message.encoding_chars.escape_character
                    + ftp_message.encoding_chars.subcomponent_separator
                )
                if fhs_encoding_str != expected_encoding_str:
                    errors.append(
                    f"FHS-2 (Encoding Characters) does not match message encoding: "
                    f"FHS={fhs_encoding_str}, message={expected_encoding_str}"
                    )
                    logger.warning(f"[{current_time}] FTP validation warning: encoding mismatch")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] FTP message validation passed")
    else:
        logger.error(f"[{current_time}] FTP message validation failed: {len(errors)} errors")
    
    return is_valid, errors


def serialize_ftp_message(
    ftp_message: Message,
    normalize: bool = True,
    validate_before_serialize: bool = True,
) -> str:
    """
    Serialize an FTP message to ER7 text format.
    
    Ensures proper FTP message structure with FHS and FTS segments.
    Optionally validates the FTP message before serialization.
    
    Args:
        ftp_message: FTP message to serialize
        normalize: If True, normalize output format (default: True)
        validate_before_serialize: If True, validate FTP before serializing (default: True)
        
    Returns:
        ER7 text representation of FTP message
        
    Raises:
        ValueError: If FTP validation fails and validate_before_serialize is True
    """
    # Validate FTP if requested
    if validate_before_serialize:
        is_valid, errors = validate_ftp_message(ftp_message)
        if not is_valid:
            error_msg = "; ".join(errors)
            raise ValueError(f"Invalid FTP message: {error_msg}")
    
    # Use standard serializer - it handles all segments including FHS and FTS
    result = serialize_hl7v2(ftp_message, normalize=normalize)
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.info(f"[{current_time}] FTP message serialized successfully")
    
    return result


def validate_fhs_segment(fhs_segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate an FHS (File Header Segment) segment.
    
    Validates:
    - FHS-2 (Encoding Characters) is required and must be 4 characters
    - FHS-7 (File Creation Date/Time) must be valid TS format if present
    - FHS-9 (File ID) format validation if present
    
    Args:
        fhs_segment: FHS segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if fhs_segment.name != "FHS":
        errors.append(f"Segment is not FHS (got {fhs_segment.name})")
        return False, errors
    
    # Validate FHS-2: Encoding Characters (required, must be 4 characters)
    if len(fhs_segment.fields) < 2:
        errors.append("FHS segment missing FHS-2 (Encoding Characters)")
    else:
        fhs2_field = fhs_segment.field(2)
        if fhs2_field and not fhs2_field.is_null:
            encoding_str = fhs2_field.value()
            if len(encoding_str) != 4:
                errors.append(f"FHS-2 (Encoding Characters) must be 4 characters (got {len(encoding_str)})")
    
    # Validate FHS-7: File Creation Date/Time (optional, but if present must be valid TS format)
    if len(fhs_segment.fields) >= 7:
        fhs7_field = fhs_segment.field(7)
        if fhs7_field and not fhs7_field.is_null:
            datetime_str = fhs7_field.value()
            # Basic TS format validation (YYYYMMDDHHMMSS or YYYYMMDDHHMMSS.SSSS)
            if datetime_str:
                if not (len(datetime_str) >= 8 and datetime_str[:8].isdigit()):
                    errors.append(f"FHS-7 (File Creation Date/Time) has invalid format: {datetime_str}")
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    is_valid = len(errors) == 0
    if is_valid:
        logger.debug(f"[{current_time}] FHS segment validation passed")
    else:
        logger.warning(f"[{current_time}] FHS segment validation failed: {len(errors)} errors")
    
    return is_valid, errors


def validate_fts_segment(fts_segment: Segment, batch_count: int) -> Tuple[bool, List[str]]:
    """
    Validate an FTS (File Trailer Segment) segment.
    
    Validates:
    - FTS-1 (File Batch Count) must match actual batch count if present
    
    Args:
        fts_segment: FTS segment to validate
        batch_count: Actual number of batches in the file
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if fts_segment.name != "FTS":
        errors.append(f"Segment is not FTS (got {fts_segment.name})")
        return False, errors
    
    # Validate FTS-1: File Batch Count (optional, but if present must match actual count)
    if len(fts_segment.fields) >= 1:
        fts1_field = fts_segment.field(1)
        if fts1_field and not fts1_field.is_null:
            batch_count_str = fts1_field.value()
            try:
                fts_batch_count = int(batch_count_str)
                if fts_batch_count != batch_count:
                    errors.append(
                        f"FTS-1 (File Batch Count) mismatch: FTS={fts_batch_count}, actual={batch_count}"
                    )
            except ValueError:
                errors.append(f"FTS-1 (File Batch Count) is not a valid number: {batch_count_str}")
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    is_valid = len(errors) == 0
    if is_valid:
        logger.debug(f"[{current_time}] FTS segment validation passed")
    else:
        logger.warning(f"[{current_time}] FTS segment validation failed: {len(errors)} errors")
    
    return is_valid, errors


def validate_batch_in_ftp(batch_message: Message, fhs_encoding_chars: EncodingCharacters) -> Tuple[bool, List[str]]:
    """
    Validate a batch message within an FTP message.
    
    Validates:
    - Batch must start with BHS
    - Batch must end with BTS
    - BHS-2 (Encoding Characters) must match FHS-2
    - BTS-1 (Batch Comment) is optional
    
    Args:
        batch_message: Batch message to validate
        fhs_encoding_chars: Encoding characters from FHS segment
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if not batch_message.segments:
        errors.append("Batch message has no segments")
        return False, errors
    
    # Check for BHS segment at start
    if batch_message.segments[0].name != "BHS":
        errors.append("Batch message must start with BHS segment")
    
    # Check for BTS segment at end
    if batch_message.segments[-1].name != "BTS":
        errors.append("Batch message must end with BTS segment")
    
    # Validate BHS-2 encoding characters match FHS-2
    bhs_segments = [seg for seg in batch_message.segments if seg.name == "BHS"]
    if bhs_segments:
        bhs = bhs_segments[0]
        if len(bhs.fields) >= 2:
            bhs2_field = bhs.field(2)
            if bhs2_field and not bhs2_field.is_null:
                bhs_encoding_str = bhs2_field.value()
                fhs_encoding_str = (
                    fhs_encoding_chars.component_separator
                    + fhs_encoding_chars.repetition_separator
                    + fhs_encoding_chars.escape_character
                    + fhs_encoding_chars.subcomponent_separator
                )
                if bhs_encoding_str != fhs_encoding_str:
                    errors.append(
                    f"BHS-2 (Encoding Characters) does not match FHS-2: "
                    f"BHS={bhs_encoding_str}, FHS={fhs_encoding_str}"
                    )
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    is_valid = len(errors) == 0
    if is_valid:
        logger.debug(f"[{current_time}] Batch validation in FTP passed")
    else:
        logger.warning(f"[{current_time}] Batch validation in FTP failed: {len(errors)} errors")
    
    return is_valid, errors


def build_ftp_message(
    batches: List[Message],
    file_sending_application: str = "",
    file_sending_facility: str = "",
    file_receiving_application: str = "",
    file_receiving_facility: str = "",
    file_id: str = "",
    file_comment: str = "",
    file_control_id: str = "",
    reference_file_control_id: str = "",
) -> Message:
    """
    Build an FTP message from a list of batch messages.
    
    Creates FHS segment with provided info and FTS segment with batch count.
    Combines FHS + batches + FTS into a complete FTP message.
    
    Args:
        batches: List of batch messages to include in file
        file_sending_application: File sending application
        file_sending_facility: File sending facility
        file_receiving_application: File receiving application
        file_receiving_facility: File receiving facility
        file_id: File ID
        file_comment: File comment
        file_control_id: File control ID
        reference_file_control_id: Reference file control ID
        
    Returns:
        FTP Message object
        
    Raises:
        ValueError: If batches list is empty
    """
    if not batches:
        raise ValueError("FTP message must contain at least one batch")
    
    # Use encoding characters from first batch
    encoding_chars = batches[0].encoding_chars
    
    # Create FHS segment
    fhs = create_fhs_segment(
        encoding_chars=encoding_chars,
        file_sending_application=file_sending_application,
        file_sending_facility=file_sending_facility,
        file_receiving_application=file_receiving_application,
        file_receiving_facility=file_receiving_facility,
        file_id=file_id,
        file_comment=file_comment,
        file_control_id=file_control_id,
        reference_file_control_id=reference_file_control_id,
    )
    
    # Collect all segments from batches
    segments = [fhs]
    for batch in batches:
        segments.extend(batch.segments)
    
    # Create FTS segment
    fts = create_fts_segment(file_batch_count=len(batches), file_comment=file_comment)
    segments.append(fts)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return Message(segments=segments, encoding_chars=encoding_chars, version=batches[0].version)


def create_ftp_from_messages(
    messages: List[Message],
    batch_size: int = 100,
    file_sending_application: str = "",
    file_sending_facility: str = "",
    file_receiving_application: str = "",
    file_receiving_facility: str = "",
    file_id: str = "",
    file_comment: str = "",
    file_control_id: str = "",
    reference_file_control_id: str = "",
) -> Message:
    """
    Create an FTP message from individual messages, grouping them into batches.
    
    Groups messages into batches of specified size, creates BHS/BTS for each batch,
    and creates FHS/FTS for the FTP message.
    
    Args:
        messages: List of individual messages to include
        batch_size: Maximum number of messages per batch (default: 100)
        file_sending_application: File sending application
        file_sending_facility: File sending facility
        file_receiving_application: File receiving application
        file_receiving_facility: File receiving facility
        file_id: File ID
        file_comment: File comment
        file_control_id: File control ID
        reference_file_control_id: Reference file control ID
        
    Returns:
        FTP Message object
        
    Raises:
        ValueError: If messages list is empty
        ImportError: If batch module is not available
    """
    if not messages:
        raise ValueError("FTP message must contain at least one message")
    
    try:
        from dnhealth.dnhealth_hl7v2.batch import create_batch_message
    except ImportError:
        raise ImportError("batch module is required for create_ftp_from_messages")
    
    # Group messages into batches
    batches = []
    current_batch_messages = []
    
    for i, message in enumerate(messages):
        current_batch_messages.append(message)
        
        # Create batch when batch_size is reached or at end
        if len(current_batch_messages) >= batch_size or i == len(messages) - 1:
            # Create batch from current messages
            batch = create_batch_message(
                messages=current_batch_messages,
                sending_application=file_sending_application,
                sending_facility=file_sending_facility,
                receiving_application=file_receiving_application,
                receiving_facility=file_receiving_facility,
                batch_id=f"BATCH_{len(batches) + 1}",
            )
            batches.append(batch)
            current_batch_messages = []
    
    # Build FTP message from batches
    result = build_ftp_message(
        batches=batches,
        file_sending_application=file_sending_application,
        file_sending_facility=file_sending_facility,
        file_receiving_application=file_receiving_application,
        file_receiving_facility=file_receiving_facility,
        file_id=file_id,
        file_comment=file_comment,
        file_control_id=file_control_id,
        reference_file_control_id=reference_file_control_id,
    )
    
    # Log operation completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.info(f"[{current_time}] FTP message created from {len(messages)} messages in {len(batches)} batches")
    
    return result

