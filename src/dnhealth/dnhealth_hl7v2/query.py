# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Query Message Construction and Handling.

Provides utilities for creating, parsing, and handling query messages including:
- QRD (Query Definition) - Original-style queries
- QRF (Query Filter) - Query filter parameters
- QAK (Query Acknowledgment) - Query response status
- QPD (Query Parameter Definition) - Enhanced queries
- Query message construction and parsing
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)
from dnhealth.dnhealth_hl7v2.parser import parse_hl7v2
from dnhealth.dnhealth_hl7v2.serializer import serialize_hl7v2

logger = logging.getLogger(__name__)


def create_qrd_segment(
    encoding_chars: EncodingCharacters,
    query_date_time: Optional[str] = None,
    query_format_code: str = "R",
    query_priority: str = "I",
    query_id: str = "",
    deferred_response_type: Optional[str] = None,
    deferred_response_date_time: Optional[str] = None,
    quantity_limited_request: Optional[str] = None,
    who_subject_filter: Optional[List[str]] = None,
    what_subject_filter: Optional[List[str]] = None,
    what_department_data_code: Optional[List[str]] = None,
    what_data_code_value_qual: Optional[List[str]] = None,
    query_results_level: Optional[str] = None,
    where_subject_filter: Optional[List[str]] = None,
    when_data_start_date_time: Optional[str] = None,
    when_data_end_date_time: Optional[str] = None,
    what_user_qualifier: Optional[List[str]] = None,
    other_qry_subject_filter: Optional[List[str]] = None,
    which_date_time_qualifier: Optional[str] = None,
    which_date_time_status_qualifier: Optional[str] = None,
    date_time_selection_qualifier: Optional[str] = None,
) -> Segment:
    """
    Create a QRD (Query Definition) segment for original-style queries.
    
    QRD fields (per HL7 v2.x specification):
    - QRD-1: Query Date/Time (TS) - required
    - QRD-2: Query Format Code (ID) - required, table 0106 (R=Record, D=Display, T=Tabular)
    - QRD-3: Query Priority (ID) - required, table 0091 (I=Immediate, D=Deferred)
    - QRD-4: Query ID (ST) - required
    - QRD-5 through QRD-20: Optional fields
    
    Args:
        encoding_chars: Encoding characters for the message
        query_date_time: Query date/time (QRD-1), defaults to current time if not provided
        query_format_code: Query format code (QRD-2), must be R, D, or T
        query_priority: Query priority (QRD-3), must be I or D
        query_id: Query ID (QRD-4), required
        deferred_response_type: Deferred response type (QRD-5)
        deferred_response_date_time: Deferred response date/time (QRD-6)
        quantity_limited_request: Quantity limited request (QRD-7)
        who_subject_filter: Who subject filter (QRD-8), can repeat
        what_subject_filter: What subject filter (QRD-9), can repeat
        what_department_data_code: What department data code (QRD-10), can repeat
        what_data_code_value_qual: What data code value qualifier (QRD-11), can repeat
        query_results_level: Query results level (QRD-12)
        where_subject_filter: Where subject filter (QRD-13), can repeat
        when_data_start_date_time: When data start date/time (QRD-14)
        when_data_end_date_time: When data end date/time (QRD-15)
        what_user_qualifier: What user qualifier (QRD-16), can repeat
        other_qry_subject_filter: Other query subject filter (QRD-17), can repeat
        which_date_time_qualifier: Which date/time qualifier (QRD-18)
        which_date_time_status_qualifier: Which date/time status qualifier (QRD-19)
        date_time_selection_qualifier: Date/time selection qualifier (QRD-20)
        
    Returns:
        QRD Segment object
        
    Raises:
        ValueError: If required fields are missing or invalid values provided
    """
    # Validate required fields
    if not query_id:
        raise ValueError("QRD-4 (Query ID) is required")
    
    if query_format_code not in ("R", "D", "T"):
        raise ValueError(f"QRD-2 (Query Format Code) must be R, D, or T, got: {query_format_code}")
    
    if query_priority not in ("I", "D"):
        raise ValueError(f"QRD-3 (Query Priority) must be I or D, got: {query_priority}")
    
    # Set default query date/time if not provided
    if query_date_time is None:
        query_date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    fields = []
    
    # QRD-1: Query Date/Time (required)
    fields.append(Field([Component([Subcomponent(query_date_time)])], is_null=False))
    
    # QRD-2: Query Format Code (required)
    fields.append(Field([Component([Subcomponent(query_format_code)])], is_null=False))
    
    # QRD-3: Query Priority (required)
    fields.append(Field([Component([Subcomponent(query_priority)])], is_null=False))
    
    # QRD-4: Query ID (required)
    fields.append(Field([Component([Subcomponent(query_id)])], is_null=False))
    
    # QRD-5: Deferred Response Type (optional)
    if deferred_response_type:
        fields.append(Field([Component([Subcomponent(deferred_response_type)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-6: Deferred Response Date/Time (optional)
    if deferred_response_date_time:
        fields.append(Field([Component([Subcomponent(deferred_response_date_time)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-7: Quantity Limited Request (optional)
    if quantity_limited_request:
        fields.append(Field([Component([Subcomponent(quantity_limited_request)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-8: Who Subject Filter (optional, repeating)
    if who_subject_filter:
        # For repeating fields, we need to handle repetitions
        # For now, we'll create a single field with the first value
        # Full repetition support would require field_repetitions parameter
        fields.append(Field([Component([Subcomponent(who_subject_filter[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-9: What Subject Filter (optional, repeating)
    if what_subject_filter:
        fields.append(Field([Component([Subcomponent(what_subject_filter[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-10: What Department Data Code (optional, repeating)
    if what_department_data_code:
        fields.append(Field([Component([Subcomponent(what_department_data_code[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-11: What Data Code Value Qualifier (optional, repeating)
    if what_data_code_value_qual:
        fields.append(Field([Component([Subcomponent(what_data_code_value_qual[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-12: Query Results Level (optional)
    if query_results_level:
        fields.append(Field([Component([Subcomponent(query_results_level)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-13: Where Subject Filter (optional, repeating)
    if where_subject_filter:
        fields.append(Field([Component([Subcomponent(where_subject_filter[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-14: When Data Start Date/Time (optional)
    if when_data_start_date_time:
        fields.append(Field([Component([Subcomponent(when_data_start_date_time)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-15: When Data End Date/Time (optional)
    if when_data_end_date_time:
        fields.append(Field([Component([Subcomponent(when_data_end_date_time)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-16: What User Qualifier (optional, repeating)
    if what_user_qualifier:
        fields.append(Field([Component([Subcomponent(what_user_qualifier[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-17: Other Query Subject Filter (optional, repeating)
    if other_qry_subject_filter:
        fields.append(Field([Component([Subcomponent(other_qry_subject_filter[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-18: Which Date/Time Qualifier (optional)
    if which_date_time_qualifier:
        fields.append(Field([Component([Subcomponent(which_date_time_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-19: Which Date/Time Status Qualifier (optional)
    if which_date_time_status_qualifier:
        fields.append(Field([Component([Subcomponent(which_date_time_status_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRD-20: Date/Time Selection Qualifier (optional)
    if date_time_selection_qualifier:
        fields.append(Field([Component([Subcomponent(date_time_selection_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    return Segment("QRD", fields=fields)


def create_qrf_segment(
    encoding_chars: EncodingCharacters,
    where_subject_filter: Optional[List[str]] = None,
    when_data_start_date_time: Optional[str] = None,
    when_data_end_date_time: Optional[str] = None,
    what_user_qualifier: Optional[List[str]] = None,
    other_qry_subject_filter: Optional[List[str]] = None,
    which_date_time_qualifier: Optional[str] = None,
    which_date_time_status_qualifier: Optional[str] = None,
    date_time_selection_qualifier: Optional[str] = None,
    when_quantity_timing_qualifier: Optional[str] = None,
    search_confidence_threshold: Optional[str] = None,
) -> Segment:
    """
    Create a QRF (Query Filter) segment.
    
    QRF fields (all optional per HL7 v2.x specification):
    - QRF-1: Where Subject Filter (ST, repeating)
    - QRF-2: When Data Start Date/Time (TS)
    - QRF-3: When Data End Date/Time (TS)
    - QRF-4: What User Qualifier (ST, repeating)
    - QRF-5: Other Query Subject Filter (ST, repeating)
    - QRF-6: Which Date/Time Qualifier (ID)
    - QRF-7: Which Date/Time Status Qualifier (ID)
    - QRF-8: Date/Time Selection Qualifier (ID)
    - QRF-9: When Quantity/Timing Qualifier (TQ)
    - QRF-10: Search Confidence Threshold (NM)
    
    Args:
        encoding_chars: Encoding characters for the message
        where_subject_filter: Where subject filter (QRF-1), can repeat
        when_data_start_date_time: When data start date/time (QRF-2)
        when_data_end_date_time: When data end date/time (QRF-3)
        what_user_qualifier: What user qualifier (QRF-4), can repeat
        other_qry_subject_filter: Other query subject filter (QRF-5), can repeat
        which_date_time_qualifier: Which date/time qualifier (QRF-6)
        which_date_time_status_qualifier: Which date/time status qualifier (QRF-7)
        date_time_selection_qualifier: Date/time selection qualifier (QRF-8)
        when_quantity_timing_qualifier: When quantity/timing qualifier (QRF-9)
        search_confidence_threshold: Search confidence threshold (QRF-10)
        
    Returns:
        QRF Segment object
    """
    fields = []
    
    # QRF-1: Where Subject Filter (optional, repeating)
    if where_subject_filter:
        fields.append(Field([Component([Subcomponent(where_subject_filter[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-2: When Data Start Date/Time (optional)
    if when_data_start_date_time:
        fields.append(Field([Component([Subcomponent(when_data_start_date_time)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-3: When Data End Date/Time (optional)
    if when_data_end_date_time:
        fields.append(Field([Component([Subcomponent(when_data_end_date_time)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-4: What User Qualifier (optional, repeating)
    if what_user_qualifier:
        fields.append(Field([Component([Subcomponent(what_user_qualifier[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-5: Other Query Subject Filter (optional, repeating)
    if other_qry_subject_filter:
        fields.append(Field([Component([Subcomponent(other_qry_subject_filter[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-6: Which Date/Time Qualifier (optional)
    if which_date_time_qualifier:
        fields.append(Field([Component([Subcomponent(which_date_time_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-7: Which Date/Time Status Qualifier (optional)
    if which_date_time_status_qualifier:
        fields.append(Field([Component([Subcomponent(which_date_time_status_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-8: Date/Time Selection Qualifier (optional)
    if date_time_selection_qualifier:
        fields.append(Field([Component([Subcomponent(date_time_selection_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-9: When Quantity/Timing Qualifier (optional)
    if when_quantity_timing_qualifier:
        fields.append(Field([Component([Subcomponent(when_quantity_timing_qualifier)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QRF-10: Search Confidence Threshold (optional)
    if search_confidence_threshold:
        fields.append(Field([Component([Subcomponent(search_confidence_threshold)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    return Segment("QRF", fields=fields)


def create_qak_segment(
    encoding_chars: EncodingCharacters,
    query_tag: Optional[str] = None,
    query_response_status: Optional[str] = None,
    message_query_name: Optional[str] = None,
    hit_count_total: Optional[int] = None,
    this_payload: Optional[int] = None,    hits_remaining: Optional[int] = None,
) -> Segment:
    """
    Create a QAK (Query Acknowledgment) segment.
    
    QAK fields (all optional per HL7 v2.x specification):
    - QAK-1: Query Tag (ST) - echoes QPD-2 or QRD-4
    - QAK-2: Query Response Status (ID) - table 0208 (OK, NF, AE, AR, etc.)
    - QAK-3: Message Query Name (CE) - echoes QPD-1
    - QAK-4: Hit Count Total (NM)
    - QAK-5: This payload (NM)
    - QAK-6: Hits remaining (NM)
    
    Args:
        encoding_chars: Encoding characters for the message
        query_tag: Query tag (QAK-1), echoes QPD-2 or QRD-4
        query_response_status: Query response status (QAK-2), table 0208
        message_query_name: Message query name (QAK-3), echoes QPD-1
        hit_count_total: Hit count total (QAK-4)
        this_payload: This payload (QAK-5)
        hits_remaining: Hits remaining (QAK-6)
        
    Returns:
        QAK Segment object
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Creating QAK segment")
    fields = []
    
    # QAK-1: Query Tag (optional)
    if query_tag:
        fields.append(Field([Component([Subcomponent(query_tag)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QAK-2: Query Response Status (optional)
    if query_response_status:
        fields.append(Field([Component([Subcomponent(query_response_status)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QAK-3: Message Query Name (optional)
    if message_query_name:
        fields.append(Field([Component([Subcomponent(message_query_name)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QAK-4: Hit Count Total (optional)
    if hit_count_total is not None:
        fields.append(Field([Component([Subcomponent(str(hit_count_total))])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QAK-5: This payload (optional)
    if this_payload is not None:
        fields.append(Field([Component([Subcomponent(str(this_payload))])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QAK-6: Hits remaining (optional)
    if hits_remaining is not None:
        fields.append(Field([Component([Subcomponent(str(hits_remaining))])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    segment = Segment("QAK", fields=fields)
    
    # Log operation completion timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{completion_time}] QAK segment created successfully")
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return segment


def create_qpd_segment(
    encoding_chars: EncodingCharacters,
    message_query_name: str,
    query_tag: Optional[str] = None,
    stored_procedure_name: Optional[str] = None,
    input_parameter_list: Optional[List[str]] = None,
) -> Segment:
    """
    Create a QPD (Query Parameter Definition) segment for enhanced queries.
    
    QPD fields (per HL7 v2.x specification):
    - QPD-1: Message Query Name (CE) - required
    - QPD-2: Query Tag (ST) - optional
    - QPD-3: Stored Procedure Name (CE) - optional
    - QPD-4: Input Parameter List (QIP) - optional, repeating
    
    Args:
        encoding_chars: Encoding characters for the message
        message_query_name: Message query name (QPD-1), required
        query_tag: Query tag (QPD-2), optional unique identifier
        stored_procedure_name: Stored procedure name (QPD-3), optional
        input_parameter_list: Input parameter list (QPD-4), optional, can repeat
        
    Returns:
        QPD Segment object
        
    Raises:
        ValueError: If message_query_name is missing
    """
    if not message_query_name:
        raise ValueError("QPD-1 (Message Query Name) is required")
    
    fields = []
    
    # QPD-1: Message Query Name (required)
    fields.append(Field([Component([Subcomponent(message_query_name)])], is_null=False))
    
    # QPD-2: Query Tag (optional)
    if query_tag:
        fields.append(Field([Component([Subcomponent(query_tag)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QPD-3: Stored Procedure Name (optional)
    if stored_procedure_name:
        fields.append(Field([Component([Subcomponent(stored_procedure_name)])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    
    # QPD-4: Input Parameter List (optional, repeating)
    if input_parameter_list:
        # For repeating fields, we'll use the first value
        # Full repetition support would require field_repetitions parameter
        fields.append(Field([Component([Subcomponent(input_parameter_list[0])])], is_null=False))
    else:
        fields.append(Field([], is_null=True))
    

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
    return Segment("QPD", fields=fields)


def create_query_message(
    message_type: str,
    sending_application: str,
    sending_facility: str,
    receiving_application: str,
    receiving_facility: str,
    qrd_segment: Optional[Segment] = None,
    qrf_segment: Optional[Segment] = None,
    qpd_segment: Optional[Segment] = None,
    rcp_segment: Optional[Segment] = None,
    message_control_id: Optional[str] = None,
    processing_id: str = "P",
    version: str = "2.5",
    encoding_chars: Optional[EncodingCharacters] = None,
) -> Message:
    """
    Create a query message (QBP, QCN, QRY, etc.).
    
    Query message structure per HL7 v2.x specification:
    - MSH (Message Header) - required
    - QRD (Query Definition) - required for original-style queries
    - QRF (Query Filter) - optional for original-style queries
    - QPD (Query Parameter Definition) - required for enhanced queries
    - RCP (Response Control Parameter) - optional
    - DSC (Continuation Pointer) - optional for continuation
    
    Args:
        message_type: Message type (e.g., "QBP^Q11", "QBP^Q13", "QCN^J01", "QRY^R02")
        sending_application: Sending application (MSH-3)
        sending_facility: Sending facility (MSH-4)
        receiving_application: Receiving application (MSH-5)
        receiving_facility: Receiving facility (MSH-6)
        qrd_segment: QRD segment (for original-style queries)
        qrf_segment: QRF segment (optional, used with QRD)
        qpd_segment: QPD segment (for enhanced queries)
        rcp_segment: RCP segment (optional)
        message_control_id: Message control ID (MSH-10), defaults to timestamp-based ID
        processing_id: Processing ID (MSH-11), defaults to "P"
        version: HL7 version (MSH-12), defaults to "2.5"
        encoding_chars: Encoding characters, defaults to standard EncodingCharacters()
    
    Returns:
        Query Message object
    
    Raises:
        ValueError: If message structure is invalid (neither QRD nor QPD provided, or both provided)
    """
    # Validate message structure
    if not qrd_segment and not qpd_segment:
        raise ValueError("Query message must have either QRD (original-style) or QPD (enhanced) segment")
    
    if qrd_segment and qpd_segment:
        raise ValueError("Query message cannot have both QRD (original-style) and QPD (enhanced) segments")
    
    # Set default encoding characters if not provided
    if encoding_chars is None:
        encoding_chars = EncodingCharacters()
    
    # Generate message control ID if not provided
    if message_control_id is None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        message_control_id = f"QUERY{timestamp}"
    
    # Build MSH segment
    # MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|DateTime||MessageType|ControlID|P|Version|
    msh_fields = []
    
    # MSH-2: Encoding characters
    msh2_value = (
        encoding_chars.component_separator +
        encoding_chars.repetition_separator +
        encoding_chars.escape_character +
        encoding_chars.subcomponent_separator
    )
    msh_fields.append([Field([Component([Subcomponent(msh2_value)])])])
    
    # MSH-3: Sending Application
    msh_fields.append([Field([Component([Subcomponent(sending_application)])])])
    
    # MSH-4: Sending Facility
    msh_fields.append([Field([Component([Subcomponent(sending_facility)])])])
    
    # MSH-5: Receiving Application
    msh_fields.append([Field([Component([Subcomponent(receiving_application)])])])
    
    # MSH-6: Receiving Facility
    msh_fields.append([Field([Component([Subcomponent(receiving_facility)])])])
    
    # MSH-7: Date/Time
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    msh_fields.append([Field([Component([Subcomponent(datetime_str)])])])
    
    # MSH-8: Security (empty)
    msh_fields.append([Field([Component([Subcomponent()])])])
    
    # MSH-9: Message Type
    msh_fields.append([Field([Component([Subcomponent(message_type)])])])
    
    # MSH-10: Message Control ID
    msh_fields.append([Field([Component([Subcomponent(message_control_id)])])])
    
    # MSH-11: Processing ID
    msh_fields.append([Field([Component([Subcomponent(processing_id)])])])
    
    # MSH-12: Version ID
    msh_fields.append([Field([Component([Subcomponent(version)])])])
    
    msh_segment = Segment("MSH", field_repetitions=msh_fields)
    
    # Build message segments
    segments = [msh_segment]
    
    # Add QRD if provided (original-style query)
    if qrd_segment:
        segments.append(qrd_segment)
        if qrf_segment:
            segments.append(qrf_segment)
    
    # Add QPD if provided (enhanced query)
    if qpd_segment:
        segments.append(qpd_segment)
    
    # Add RCP if provided
    if rcp_segment:
        segments.append(rcp_segment)
    
    # Create message
    result = Message(
        segments=segments,
        encoding_chars=encoding_chars,
        version=version,
    )
    
    # Log operation completion timestamp
    logging.debug(f"create_query_message completed at {datetime.now().isoformat()}")
    
    return result


def create_query_response_message(
    original_query: Message,
    query_response_status: str,
    hit_count_total: Optional[int] = None,
    this_payload: Optional[int] = None,
    hits_remaining: Optional[int] = None,
    response_segments: Optional[List[Segment]] = None,
    continuation_pointer: Optional[str] = None,
    acknowledgment_code: str = "AA",
    text_message: Optional[str] = None,
    application_name: Optional[str] = None,
    facility_name: Optional[str] = None,
) -> Message:
    """
    Create a query response message (RSP, RTB, etc.).
    
    Query response structure per HL7 v2.x specification:
    - MSH (Message Header) - required
    - MSA (Message Acknowledgment) - required
    - QAK (Query Acknowledgment) - optional but recommended
    - QRD (Query Definition) - echo of original query (if original had QRD)
    - QRF (Query Filter) - echo of original query (if original had QRF)
    - QPD (Query Parameter Definition) - echo of original query (if original had QPD)
    - Response segments (e.g., PID, OBR, OBX for patient data queries)
    - DSC (Continuation Pointer) - optional for continuation
    
    Args:
        original_query: Original query message
        query_response_status: Response status (QAK-2), table 0208 (OK, NF, AE, AR, etc.)
        hit_count_total: Total hits (QAK-4)
        this_payload: Hits in this response (QAK-5)
        hits_remaining: Hits remaining (QAK-6)
        response_segments: Response data segments (e.g., PID, OBR, OBX)
        continuation_pointer: Continuation pointer for pagination (DSC-1)
        acknowledgment_code: Acknowledgment code (MSA-1), defaults to "AA"
        text_message: Text message (MSA-3), optional
        application_name: Application name for MSH-3 (default: from original MSH-5)
        facility_name: Facility name for MSH-4 (default: from original MSH-6)
    
    Returns:
        Query Response Message object
    
    Raises:
        ValueError: If original_query has no MSH segment or acknowledgment_code is invalid
    """
    valid_ack_codes = {"AA", "AE", "AR"}
    if acknowledgment_code not in valid_ack_codes:
        raise ValueError(f"Invalid acknowledgment code: {acknowledgment_code}. Must be one of {valid_ack_codes}")
    
    # Get original MSH segment
    msh_segments = original_query.get_segments("MSH")
    if not msh_segments:
        raise ValueError("Original query message must have an MSH segment")
    
    original_msh = msh_segments[0]
    encoding_chars = original_query.encoding_chars
    version = original_query.version or "2.5"
    
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
    
    # Determine response message type from original
    original_msg_type = ""
    original_trigger_event = ""
    if len(original_msh.fields) >= 9:
        msg_type_field = original_msh.field(9)
        if msg_type_field.components:
            original_msg_type = msg_type_field.component(1).value()
            if len(msg_type_field.components) > 1:
                original_trigger_event = msg_type_field.component(2).value()
    
    # Map query message type to response message type
    # QBP^Q11 -> RSP^K11, QBP^Q13 -> RSP^K13, etc.
    response_msg_type = original_msg_type
    if original_msg_type == "QBP":
        response_msg_type = "RSP"
    elif original_msg_type == "QRY":
        response_msg_type = "RTB"
    elif original_msg_type == "QCN":
        response_msg_type = "ACK"  # Cancel query acknowledgment
    
    # Use provided names or swap sending/receiving from original
    resp_sending_app = application_name or original_receiving_app or "RESP_APP"
    resp_sending_facility = facility_name or original_receiving_facility or "RESP_FAC"
    resp_receiving_app = original_sending_app or "ORIG_APP"
    resp_receiving_facility = original_sending_facility or "ORIG_FAC"
    
    # Generate new message control ID
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_control_id = f"RESP{timestamp}"
    
    # Build MSH segment for response
    msh_fields = []
    
    # MSH-2: Encoding characters
    msh2_value = (
        encoding_chars.component_separator +
        encoding_chars.repetition_separator +
        encoding_chars.escape_character +
        encoding_chars.subcomponent_separator
    )
    msh_fields.append([Field([Component([Subcomponent(msh2_value)])])])
    
    # MSH-3: Sending Application
    msh_fields.append([Field([Component([Subcomponent(resp_sending_app)])])])
    
    # MSH-4: Sending Facility
    msh_fields.append([Field([Component([Subcomponent(resp_sending_facility)])])])
    
    # MSH-5: Receiving Application
    msh_fields.append([Field([Component([Subcomponent(resp_receiving_app)])])])
    
    # MSH-6: Receiving Facility
    msh_fields.append([Field([Component([Subcomponent(resp_receiving_facility)])])])
    
    # MSH-7: Date/Time
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    msh_fields.append([Field([Component([Subcomponent(datetime_str)])])])
    
    # MSH-8: Security (empty)
    msh_fields.append([Field([Component([Subcomponent()])])])
    
    # MSH-9: Message Type
    response_msg_type_full = f"{response_msg_type}^{original_trigger_event}"
    msh_fields.append([Field([Component([Subcomponent(response_msg_type_full)])])])
    
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
    
    msa_segment = Segment("MSA", field_repetitions=msa_fields)
    
    # Build QAK segment (optional but recommended)
    # Extract query tag and message query name from original query
    query_tag = None
    message_query_name = None
    
    # Check for QPD (enhanced query)
    qpd_segments = original_query.get_segments("QPD")
    if qpd_segments:
        qpd = qpd_segments[0]
        if qpd.field(2):  # QPD-2: Query Tag
            query_tag = qpd.field(2).value()
        if qpd.field(1):  # QPD-1: Message Query Name
            message_query_name = qpd.field(1).value()
    
    # Check for QRD (original-style query)
    qrd_segments = original_query.get_segments("QRD")
    if qrd_segments:
        qrd = qrd_segments[0]
        if qrd.field(4):  # QRD-4: Query ID (used as query tag)
            query_tag = qrd.field(4).value()
    
    qak_segment = create_qak_segment(
        encoding_chars=encoding_chars,
        query_tag=query_tag,
        query_response_status=query_response_status,
        message_query_name=message_query_name,
        hit_count_total=hit_count_total,
        this_payload=this_payload,
        hits_remaining=hits_remaining,
    )
    
    # Build message segments
    segments = [msh_segment, msa_segment, qak_segment]
    
    # Echo original query segments (QRD, QRF, or QPD)
    if qrd_segments:
        segments.append(qrd_segments[0])
        qrf_segments = original_query.get_segments("QRF")
        if qrf_segments:
            segments.append(qrf_segments[0])
    elif qpd_segments:
        segments.append(qpd_segments[0])
    
    # Add response segments
    if response_segments:
        segments.extend(response_segments)
    
    # Add DSC segment if continuation pointer provided
    if continuation_pointer:
        from dnhealth.dnhealth_hl7v2.segment_definitions import DSC_FIELD_DEFINITIONS
        dsc_fields = []
        dsc_fields.append(Field([Component([Subcomponent(continuation_pointer)])], is_null=False))
        dsc_segment = Segment("DSC", fields=dsc_fields)
        segments.append(dsc_segment)
    
    # Create response message
    result = Message(
        segments=segments,

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        encoding_chars=encoding_chars,
        version=version,
    )
    
    # Log operation completion timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{completion_time}] Query response message created successfully")
    logging.debug(f"create_query_response_message completed at {datetime.now().isoformat()}")
    
    return result


def parse_query_message(message: Message) -> Dict[str, Any]:
    """
    Parse a query message and extract query information.
    
    Args:
        message: HL7 v2 message to parse
        
    Returns:
        Dictionary with parsed query information:
        - message_type: Message type (e.g., "QBP^Q11")
        - query_type: "original-style" or "enhanced"
        - qrd: QRD segment if present
        - qrf: QRF segment if present
        - qpd: QPD segment if present
        - rcp: RCP segment if present
    """
    result = {
        "message_type": None,
        "query_type": None,
        "qrd": None,
        "qrf": None,
        "qpd": None,
        "rcp": None,
    }
    
    # Get message type from MSH-9
    msh_segments = message.get_segments("MSH")
    if msh_segments:
        msh = msh_segments[0]
        if msh.field(9):
            msg_type_field = msh.field(9)
            if msg_type_field and msg_type_field.components:
                msg_type_comp = msg_type_field.components[0]
                if msg_type_comp and msg_type_comp.subcomponents:
                    result["message_type"] = msg_type_comp.subcomponents[0].value
    
    # Check for QRD (original-style) or QPD (enhanced)
    qrd_segments = message.get_segments("QRD")
    qpd_segments = message.get_segments("QPD")
    
    if qrd_segments:
        result["query_type"] = "original-style"
        result["qrd"] = qrd_segments[0]
        
        # Check for QRF
        qrf_segments = message.get_segments("QRF")
        if qrf_segments:
            result["qrf"] = qrf_segments[0]
    elif qpd_segments:
        result["query_type"] = "enhanced"
        result["qpd"] = qpd_segments[0]

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    else:
        result["query_type"] = "unknown"
    
    # Check for RCP
    rcp_segments = message.get_segments("RCP")
    if rcp_segments:
        result["rcp"] = rcp_segments[0]
    
    # Log operation completion timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{completion_time}] Query message parsed successfully")
    logging.debug(f"parse_query_message completed at {datetime.now().isoformat()}")
    
    return result


def parse_query_response(message: Message) -> Dict[str, Any]:
    """
    Parse a query response message and extract response information.
    
    Args:
        message: HL7 v2 message to parse
        
    Returns:
        Dictionary with parsed response information:
        - msa: MSA segment if present
        - qak: QAK segment if present
        - query_status: Query status from QAK-2
        - hit_count_total: Hit count total from QAK-4
        - this_payload: This payload from QAK-5
        - hits_remaining: Hits remaining from QAK-6
        - response_segments: List of response segments
        - continuation_pointer: Continuation pointer from DSC segment
    """
    result = {
        "msa": None,
        "qak": None,
        "query_status": None,
        "hit_count_total": None,
        "this_payload": None,
        "hits_remaining": None,
        "response_segments": [],
        "continuation_pointer": None,
    }
    
    # Get MSA segment
    msa_segments = message.get_segments("MSA")
    if msa_segments:
        result["msa"] = msa_segments[0]
    
    # Get QAK segment
    qak_segments = message.get_segments("QAK")
    if qak_segments:
        qak = qak_segments[0]
        result["qak"] = qak
        
        # Extract QAK fields
        if qak.field(2):
            qak2 = qak.field(2)
            if qak2 and qak2.components:
                comp = qak2.components[0]
                if comp and comp.subcomponents:
                    result["query_status"] = comp.subcomponents[0].value
        
        if qak.field(4):
            qak4 = qak.field(4)
            if qak4 and qak4.components:
                comp = qak4.components[0]
                if comp and comp.subcomponents:
                    try:
                        result["hit_count_total"] = int(comp.subcomponents[0].value)
                    except (ValueError, AttributeError):
                        pass
        
        if qak.field(5):
            qak5 = qak.field(5)
            if qak5 and qak5.components:
                comp = qak5.components[0]
                if comp and comp.subcomponents:
                    try:
                        result["this_payload"] = int(comp.subcomponents[0].value)
                    except (ValueError, AttributeError):
                        pass
        
        if qak.field(6):
            qak6 = qak.field(6)
            if qak6 and qak6.components:
                comp = qak6.components[0]
                if comp and comp.subcomponents:
                    try:
                        result["hits_remaining"] = int(comp.subcomponents[0].value)
                    except (ValueError, AttributeError):
                        pass
    
    # Get DSC segment for continuation pointer
    dsc_segments = message.get_segments("DSC")
    if dsc_segments:
        dsc = dsc_segments[0]
        if dsc.field(1):
            dsc1 = dsc.field(1)
            if dsc1 and dsc1.components:
                comp = dsc1.components[0]
                if comp and comp.subcomponents:
                    result["continuation_pointer"] = comp.subcomponents[0].value
    
    # Collect response segments (everything after QAK/QPD echo, before DSC)
    all_segments = message.flatten_segments()
    response_started = False
    for segment in all_segments:
        if segment.name in ("MSH", "MSA", "ERR"):
            continue
        if segment.name in ("QAK", "QRD", "QRF", "QPD"):
            response_started = True
            continue
        if segment.name == "DSC":
            break
        if response_started:
            result["response_segments"].append(segment)
    
    # Log operation completion timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{completion_time}] Query response message parsed successfully")
    logging.debug(f"parse_query_response completed at {datetime.now().isoformat()}")
    
    return result
