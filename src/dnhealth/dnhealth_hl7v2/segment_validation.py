# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x segment validation.

Validates individual segments against HL7 v2.x segment specifications,
checking required fields, field data types, lengths, and constraints.
"""

import logging
from datetime import datetime
from typing import List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import Segment

# Get logger with timestamp formatting
logger = logging.getLogger(__name__)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def validate_msh_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate MSH (Message Header) segment.
    
    According to HL7 v2.x specification, MSH requires:
    - MSH-2 (Encoding Characters) - required
    - MSH-9 (Message Type) - required
    - MSH-10 (Message Control ID) - required
    
    Note: MSH-1 (Field Separator) is implicit and not stored as a regular field.
    
    Optional fields include: MSH-3 (Sending Application), MSH-4 (Sending Facility),
    MSH-5 (Receiving Application), MSH-6 (Receiving Facility), MSH-7 (Date/Time),
    MSH-8 (Security), MSH-11 (Processing ID), MSH-12 (Version ID), etc.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MSH segment validation")
    
    # Check segment name
    if segment.name != "MSH":
        errors.append(f"MSH segment validation: expected segment name MSH, got {segment.name}")
        logger.error(f"[{current_time}] MSH segment validation failed: wrong segment name")
        return False, errors
    
    # Check MSH-2 (Encoding Characters) - required
    # Note: MSH-1 is the field separator and is not stored as a field
    # So MSH-2 is at field index 1 (0-based) or field(2) (1-based)
    if len(segment.fields) < 1:
        errors.append("MSH segment missing required field MSH-2 (Encoding Characters)")
        logger.error(f"[{current_time}] MSH segment validation failed: missing MSH-2")
    else:
        msh_2 = segment.field(2)
        if not msh_2 or not msh_2.value():
            errors.append("MSH segment missing required field MSH-2 (Encoding Characters)")
            logger.error(f"[{current_time}] MSH segment validation failed: MSH-2 is empty")
        elif len(msh_2.value()) > 4:
            errors.append(f"MSH-2 (Encoding Characters) exceeds max length of 4 characters (got {len(msh_2.value())})")
            logger.warning(f"[{current_time}] MSH segment validation warning: MSH-2 length violation")
    
    # Check MSH-9 (Message Type) - required
    # MSH-9 is at field index 8 (0-based) or field(9) (1-based)
    if len(segment.fields) < 8:
        errors.append("MSH segment missing required field MSH-9 (Message Type)")
        logger.error(f"[{current_time}] MSH segment validation failed: missing MSH-9")
    else:
        msh_9 = segment.field(9)
        if not msh_9 or not msh_9.components or not msh_9.component(1).value():
            errors.append("MSH segment missing required field MSH-9 (Message Type)")
            logger.error(f"[{current_time}] MSH segment validation failed: MSH-9 is empty or invalid")
        else:
            # MSH-9 should have at least the message code (first component)
            msg_code = msh_9.component(1).value()
            if not msg_code:
                errors.append("MSH-9 (Message Type) must have a message code (first component)")
                logger.error(f"[{current_time}] MSH segment validation failed: MSH-9 message code missing")
    
    # Check MSH-10 (Message Control ID) - required
    # MSH-10 is at field index 9 (0-based) or field(10) (1-based)
    if len(segment.fields) < 9:
        errors.append("MSH segment missing required field MSH-10 (Message Control ID)")
        logger.error(f"[{current_time}] MSH segment validation failed: missing MSH-10")
    else:
        msh_10 = segment.field(10)
        if not msh_10 or not msh_10.value():
            errors.append("MSH segment missing required field MSH-10 (Message Control ID)")
            logger.error(f"[{current_time}] MSH segment validation failed: MSH-10 is empty")
    
    # Validate MSH-7 (Date/Time) format if present
    if len(segment.fields) >= 7:
        msh_7 = segment.field(7)
        if msh_7 and msh_7.value():
            # Basic validation: TS (Time Stamp) should be in format YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            dt_value = msh_7.value()
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"MSH-7 (Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] MSH segment validation warning: MSH-7 format may be invalid")
    
    # Validate MSH-12 (Version ID) if present
    if len(segment.fields) >= 12:
        msh_12 = segment.field(12)
        if msh_12 and msh_12.value():
            version = msh_12.value()
            # Valid HL7 versions: 2.1, 2.2, 2.3, 2.3.1, 2.4, 2.5, 2.5.1, 2.6, 2.7, 2.8, 2.8.1, 2.8.2, 2.9
            valid_versions = ["2.1", "2.2", "2.3", "2.3.1", "2.4", "2.5", "2.5.1", "2.6", "2.7", "2.8", "2.8.1", "2.8.2", "2.9"]
            if version not in valid_versions:
                errors.append(f"MSH-12 (Version ID) contains unrecognized version: {version}")
                logger.warning(f"[{current_time}] MSH segment validation warning: unrecognized version in MSH-12")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] MSH segment validation passed")
    else:
        logger.error(f"[{current_time}] MSH segment validation failed with {len(errors)} error(s)")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    return is_valid, errors


def validate_msa_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate MSA (Message Acknowledgment) segment.
    
    According to HL7 v2.x specification, MSA requires:
    - MSA-1 (Acknowledgment Code) - required (AA=Application Accept, AE=Application Error, AR=Application Reject)
    - MSA-2 (Message Control ID) - required
    
    Optional fields include: MSA-3 (Text Message), MSA-4 (Expected Sequence Number),
    MSA-5 (Delayed Acknowledgment Type), MSA-6 (Error Condition), etc.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MSA segment validation")
    
    # Check segment name
    if segment.name != "MSA":
        errors.append(f"MSA segment validation: expected segment name MSA, got {segment.name}")
        logger.error(f"[{current_time}] MSA segment validation failed: wrong segment name")
        return False, errors
    
    # Check MSA-1 (Acknowledgment Code) - required
    if len(segment.fields) < 1:
        errors.append("MSA segment missing required field MSA-1 (Acknowledgment Code)")
        logger.error(f"[{current_time}] MSA segment validation failed: missing MSA-1")
    else:
        msa_1 = segment.field(1)
        if not msa_1 or not msa_1.value():
            errors.append("MSA segment missing required field MSA-1 (Acknowledgment Code)")
            logger.error(f"[{current_time}] MSA segment validation failed: MSA-1 is empty")
        else:
            ack_code = msa_1.value()
            valid_codes = ["AA", "AE", "AR"]
            if ack_code not in valid_codes:
                errors.append(f"MSA-1 (Acknowledgment Code) must be one of {valid_codes}, got {ack_code}")
                logger.warning(f"[{current_time}] MSA segment validation warning: invalid acknowledgment code")
    
    # Check MSA-2 (Message Control ID) - required
    if len(segment.fields) < 2:
        errors.append("MSA segment missing required field MSA-2 (Message Control ID)")
        logger.error(f"[{current_time}] MSA segment validation failed: missing MSA-2")
    else:
        msa_2 = segment.field(2)
        if not msa_2 or not msa_2.value():
            errors.append("MSA segment missing required field MSA-2 (Message Control ID)")
            logger.error(f"[{current_time}] MSA segment validation failed: MSA-2 is empty")
    
    # Validate MSA-4 (Expected Sequence Number) format if present
    if len(segment.fields) >= 4:
        msa_4 = segment.field(4)
        if msa_4 and msa_4.value():
            seq_num = msa_4.value()
            # Should be numeric
            try:
                int(seq_num)
            except ValueError:
                errors.append(f"MSA-4 (Expected Sequence Number) should be numeric, got {seq_num}")
                logger.warning(f"[{current_time}] MSA segment validation warning: MSA-4 format may be invalid")
    
    is_valid = len(errors) == 0

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    if is_valid:
        logger.info(f"[{current_time}] MSA segment validation passed")
    else:
        logger.error(f"[{current_time}] MSA segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_evn_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate EVN (Event Type) segment.
    
    According to HL7 v2.x specification, EVN fields are generally optional:
    - EVN-1 (Event Type Code) - optional, should be from Table 0003 if present
    - EVN-2 (Recorded Date/Time) - optional, TS format if present
    - EVN-3 (Date/Time Planned Event) - optional, TS format if present
    - EVN-4 (Event Reason Code) - optional, should be from Table 0062 if present
    - EVN-5 (Operator ID) - optional
    - EVN-6 (Event Occurred) - optional (2.5+), TS format if present
    - EVN-7 (Event Facility) - optional (2.7+)
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EVN segment validation")
    
    # Check segment name
    if segment.name != "EVN":
        errors.append(f"EVN segment validation: expected segment name EVN, got {segment.name}")
        logger.error(f"[{current_time}] EVN segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # Validate EVN-1 (Event Type Code) if present - should be from Table 0003
    if len(segment.fields) >= 1:
        evn_1 = segment.field(1)
        if evn_1 and evn_1.value():
            event_code = evn_1.value()
            # Common event type codes from Table 0003 (A01-A62 for ADT messages, etc.)
            # We'll do basic validation - should be alphanumeric and typically 2-3 characters
            if not event_code or len(event_code) < 1:
                errors.append("EVN-1 (Event Type Code) should not be empty if present")
                logger.warning(f"[{current_time}] EVN segment validation warning: EVN-1 is empty at the end of the operations")
            elif len(event_code) > 3:
                errors.append(f"EVN-1 (Event Type Code) typically 1-3 characters, got {len(event_code)}")
                logger.warning(f"[{current_time}] EVN segment validation warning: EVN-1 length unusual at the end of the operations")
    
    # Validate EVN-2 (Recorded Date/Time) format if present
    if len(segment.fields) >= 2:
        evn_2 = segment.field(2)
        if evn_2 and evn_2.value():
            dt_value = evn_2.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"EVN-2 (Recorded Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] EVN segment validation warning: EVN-2 format may be invalid at the end of the operations")
    
    # Validate EVN-3 (Date/Time Planned Event) format if present
    if len(segment.fields) >= 3:
        evn_3 = segment.field(3)
        if evn_3 and evn_3.value():
            dt_value = evn_3.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"EVN-3 (Date/Time Planned Event) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] EVN segment validation warning: EVN-3 format may be invalid at the end of the operations")
    
    # Validate EVN-4 (Event Reason Code) if present - should be from Table 0062
    if len(segment.fields) >= 4:
        evn_4 = segment.field(4)
        if evn_4 and evn_4.value():
            reason_code = evn_4.value()
            # Table 0062 contains reason codes - basic validation
            if not reason_code or len(reason_code) < 1:
                errors.append("EVN-4 (Event Reason Code) should not be empty if present")
                logger.warning(f"[{current_time}] EVN segment validation warning: EVN-4 is empty at the end of the operations")
    
    # Validate EVN-6 (Event Occurred) format if present (2.5+)
    if len(segment.fields) >= 6:
        evn_6 = segment.field(6)
        if evn_6 and evn_6.value():
            dt_value = evn_6.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD

                    # Log completion timestamp at end of operation
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Current Time at End of Operations: {current_time}")
                errors.append(f"EVN-6 (Event Occurred) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] EVN segment validation warning: EVN-6 format may be invalid at the end of the operations")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] EVN segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] EVN segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_pid_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate PID (Patient Identification) segment.
    
    According to HL7 v2.x specification, PID fields are generally optional:
    - PID-1 (Set ID - PID) - optional
    - PID-2 (Patient ID) - optional, deprecated in 2.3+
    - PID-3 (Patient Identifier List) - optional, commonly used
    - PID-4 (Alternate Patient ID) - optional, deprecated in 2.3+
    - PID-5 (Patient Name) - optional
    - PID-6 (Mother's Maiden Name) - optional
    - PID-7 (Date/Time of Birth) - optional, TS format if present
    - PID-8 (Administrative Sex) - optional, should be from Table 0001 (M, F, O, U) if present
    - PID-9+ (various optional fields in 2.5+)
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PID segment validation")
    
    # Check segment name
    if segment.name != "PID":
        errors.append(f"PID segment validation: expected segment name PID, got {segment.name}")
        logger.error(f"[{current_time}] PID segment validation failed: wrong segment name")
        return False, errors
    
    # Validate PID-7 (Date/Time of Birth) format if present
    if len(segment.fields) >= 7:
        pid_7 = segment.field(7)
        if pid_7 and pid_7.value():
            dt_value = pid_7.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"PID-7 (Date/Time of Birth) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] PID segment validation warning: PID-7 format may be invalid")
    
    # Validate PID-8 (Administrative Sex) if present - should be from Table 0001
    if len(segment.fields) >= 8:
        pid_8 = segment.field(8)

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        if pid_8 and pid_8.value():
            sex_code = pid_8.value()
            valid_codes = ["M", "F", "O", "U"]  # Table 0001: M=Male, F=Female, O=Other, U=Unknown
            if sex_code not in valid_codes:
                errors.append(f"PID-8 (Administrative Sex) must be one of {valid_codes} (Table 0001), got {sex_code}")
                logger.warning(f"[{current_time}] PID segment validation warning: invalid administrative sex code")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] PID segment validation passed")
    else:
        logger.error(f"[{current_time}] PID segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_pd1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate PD1 (Patient Additional Demographic) segment.
    
    According to HL7 v2.x specification, PD1 fields are generally optional:
    - PD1-1 (Living Dependency) - optional
    - PD1-2 (Living Arrangement) - optional
    - PD1-3 (Patient Primary Facility) - optional
    - PD1-4 (Patient Primary Care Provider Name & ID No.) - optional
    - PD1-5 (Student Indicator) - optional
    - PD1-6 (Handicap) - optional
    - PD1-7 (Living Will Code) - optional
    - PD1-8 (Organ Donor Code) - optional
    - PD1-9 (Separate Bill) - optional, should be from Table 0136 (Y, N) if present
    - PD1-10 (Duplicate Patient) - optional
    - PD1-11 (Publicity Code) - optional
    - PD1-12 (Protection Indicator) - optional, should be from Table 0136 (Y, N) if present
    - PD1-13+ (various optional fields in 2.5+)
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PD1 segment validation")
    
    # Check segment name
    if segment.name != "PD1":
        errors.append(f"PD1 segment validation: expected segment name PD1, got {segment.name}")
        logger.error(f"[{current_time}] PD1 segment validation failed: wrong segment name")
        return False, errors
    
    # Validate PD1-9 (Separate Bill) if present - should be from Table 0136
    if len(segment.fields) >= 9:
        pd1_9 = segment.field(9)
        if pd1_9 and pd1_9.value():
            separate_bill = pd1_9.value()
            valid_codes = ["Y", "N"]  # Table 0136: Y=Yes, N=No
            if separate_bill not in valid_codes:
                errors.append(f"PD1-9 (Separate Bill) must be one of {valid_codes} (Table 0136), got {separate_bill}")
                logger.warning(f"[{current_time}] PD1 segment validation warning: invalid separate bill code")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Validate PD1-12 (Protection Indicator) if present - should be from Table 0136
    if len(segment.fields) >= 12:
        pd1_12 = segment.field(12)
        if pd1_12 and pd1_12.value():
            protection = pd1_12.value()
            valid_codes = ["Y", "N"]  # Table 0136: Y=Yes, N=No
            if protection not in valid_codes:
                errors.append(f"PD1-12 (Protection Indicator) must be one of {valid_codes} (Table 0136), got {protection}")
                logger.warning(f"[{current_time}] PD1 segment validation warning: invalid protection indicator code")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] PD1 segment validation passed")
    else:
        logger.error(f"[{current_time}] PD1 segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_pv1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate PV1 (Patient Visit) segment.
    
    According to HL7 v2.x specification, PV1 requires:
    - PV1-2 (Patient Class) - required
    
    Optional fields include: PV1-1 (Set ID - PV1), PV1-3 (Assigned Patient Location),
    PV1-4 (Admission Type), PV1-5 (Preadmit Number), PV1-6 (Prior Patient Location),
    PV1-7 (Attending Doctor), PV1-8 (Referring Doctor), PV1-9 (Consulting Doctor),
    PV1-10 (Hospital Service), PV1-11 (Temporary Location), PV1-12 (Preadmit Test Indicator),
    PV1-13+ (various optional fields), etc.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PV1 segment validation")
    
    # Check segment name
    if segment.name != "PV1":
        errors.append(f"PV1 segment validation: expected segment name PV1, got {segment.name}")
        logger.error(f"[{current_time}] PV1 segment validation failed: wrong segment name")
        return False, errors
    
    # Check PV1-2 (Patient Class) - required
    if len(segment.fields) < 2:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        errors.append("PV1 segment missing required field PV1-2 (Patient Class)")
        logger.error(f"[{current_time}] PV1 segment validation failed: missing PV1-2")
    else:
        pv1_2 = segment.field(2)
        if not pv1_2 or not pv1_2.value():
            errors.append("PV1 segment missing required field PV1-2 (Patient Class)")
            logger.error(f"[{current_time}] PV1 segment validation failed: PV1-2 is empty")
        else:
            # Table 0004: Common patient class codes: E=Emergency, I=Inpatient, O=Outpatient, P=Preadmit, R=Recurring patient, B=Obstetrics, C=Commercial Account, N=Not Applicable, U=Unknown
            patient_class = pv1_2.value()
            # Basic validation - should not be empty
            if not patient_class:
                errors.append("PV1-2 (Patient Class) should not be empty")
                logger.error(f"[{current_time}] PV1 segment validation failed: PV1-2 is empty")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] PV1 segment validation passed")
    else:
        logger.error(f"[{current_time}] PV1 segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_obx_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate OBX (Observation/Result) segment.
    
    According to HL7 v2.x specification, OBX requires:
    - OBX-2 (Value Type) - required, should be from Table 0125
    - OBX-3 (Observation Identifier) - required
    - OBX-11 (Observe Result Status) - required, should be from Table 0085
    
    Optional fields include: OBX-1 (Set ID - OBX), OBX-4 (Observation Sub-ID),
    OBX-5 (Observation Value), OBX-6 (Units), OBX-7 (References Range),
    OBX-8 (Interpretation Codes), OBX-9 (Probability), OBX-10 (Nature of Abnormal Test),
    OBX-12 (Date/Time of the Observation), OBX-13+ (various optional fields), etc.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting OBX segment validation")
    
    # Check segment name
    if segment.name != "OBX":
        errors.append(f"OBX segment validation: expected segment name OBX, got {segment.name}")
        logger.error(f"[{current_time}] OBX segment validation failed: wrong segment name")
        return False, errors
    
    # Check OBX-2 (Value Type) - required
    if len(segment.fields) < 2:
        errors.append("OBX segment missing required field OBX-2 (Value Type)")
        logger.error(f"[{current_time}] OBX segment validation failed: missing OBX-2")
    else:
        obx_2 = segment.field(2)
        if not obx_2 or not obx_2.value():
            errors.append("OBX segment missing required field OBX-2 (Value Type)")
            logger.error(f"[{current_time}] OBX segment validation failed: OBX-2 is empty")
        else:
            # Common value types: AD, AUI, CE, CF, CK, CN, CP, CQ, CWE, CX, DDI, DIN, DLD, DLN, DLT, DR, DT, DTM, ED, EI, EIP, ELD, ERL, FC, FN, FT, HD, ICD, ID, IS, JCC, LA1, LA2, LOC, MA, MO, MOC, MOP, MSG, NA, NDL, NM, NR, OCD, OSD, OSP, PIP, PL, PPN, PRL, PT, PTA, QIP, QSC, RCD, RFR, RI, RMC, RP, RPT, SAD, SCV, SI, SN, SPD, SPS, SRT, ST, TM, TN, TQ, TS, TX, UVC, VH, VID, VR, WVI, WVS, XAD, XCN, XON, XPN, XTN
            # Basic validation - should not be empty
            value_type = obx_2.value()
            if not value_type:
                errors.append("OBX-2 (Value Type) should not be empty")
                logger.error(f"[{current_time}] OBX segment validation failed: OBX-2 is empty")
    
    # Check OBX-3 (Observation Identifier) - required
    if len(segment.fields) < 3:
        errors.append("OBX segment missing required field OBX-3 (Observation Identifier)")
        logger.error(f"[{current_time}] OBX segment validation failed: missing OBX-3")
    else:
        obx_3 = segment.field(3)
        if not obx_3 or not obx_3.components or not obx_3.component(1).value():
            errors.append("OBX segment missing required field OBX-3 (Observation Identifier)")
            logger.error(f"[{current_time}] OBX segment validation failed: OBX-3 is empty or invalid")
    
    # Check OBX-11 (Observe Result Status) - required
    if len(segment.fields) < 11:
        errors.append("OBX segment missing required field OBX-11 (Observe Result Status)")
        logger.error(f"[{current_time}] OBX segment validation failed: missing OBX-11")
    else:
        obx_11 = segment.field(11)
        if not obx_11 or not obx_11.value():
            errors.append("OBX segment missing required field OBX-11 (Observe Result Status)")
            logger.error(f"[{current_time}] OBX segment validation failed: OBX-11 is empty")
        else:
            # Table 0085: Common result status codes: C (Corrected), D (Deleted), F (Final), I (Incomplete), P (Preliminary), R (Results Entered), S (Partial), X (Cancelled)
            result_status = obx_11.value()
            valid_codes = ["C", "D", "F", "I", "P", "R", "S", "X"]
            if result_status not in valid_codes:
                errors.append(f"OBX-11 (Observe Result Status) should be one of {valid_codes} (Table 0085), got {result_status}")
                logger.warning(f"[{current_time}] OBX segment validation warning: invalid result status code")
    
    # Validate OBX-12 (Date/Time of the Observation) format if present
    if len(segment.fields) >= 12:
        obx_12 = segment.field(12)
        if obx_12 and obx_12.value():
            dt_value = obx_12.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"OBX-12 (Date/Time of the Observation) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] OBX segment validation warning: OBX-12 format may be invalid")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] OBX segment validation passed")
    else:
        logger.error(f"[{current_time}] OBX segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_obr_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate OBR (Observation Request) segment.
    
    According to HL7 v2.x specification, OBR requires:
    - OBR-4 (Universal Service Identifier) - required
    
    Optional fields include: OBR-1 (Set ID - OBR), OBR-2 (Placer Order Number),
    OBR-3 (Filler Order Number), OBR-5 (Priority - OBR, from Table 0027),
    OBR-6 (Requested Date/Time), OBR-7 (Observation Date/Time), OBR-8 (Observation End Date/Time),
    OBR-9 (Collection Volume), OBR-10 (Collector Identifier), OBR-11 (Specimen Action Code, from Table 0065),
    OBR-12 (Danger Code), OBR-13 (Relevant Clinical Information), OBR-14 (Specimen Received Date/Time),
    OBR-15 (Specimen Source), OBR-16+ (various optional fields), etc.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting OBR segment validation")
    
    # Check segment name
    if segment.name != "OBR":
        errors.append(f"OBR segment validation: expected segment name OBR, got {segment.name}")
        logger.error(f"[{current_time}] OBR segment validation failed: wrong segment name")
        return False, errors
    
    # Check OBR-4 (Universal Service Identifier) - required
    if len(segment.fields) < 4:
        errors.append("OBR segment missing required field OBR-4 (Universal Service Identifier)")
        logger.error(f"[{current_time}] OBR segment validation failed: missing OBR-4")
    else:
        obr_4 = segment.field(4)
        if not obr_4 or not obr_4.components or not obr_4.component(1).value():
            errors.append("OBR segment missing required field OBR-4 (Universal Service Identifier)")
            logger.error(f"[{current_time}] OBR segment validation failed: OBR-4 is empty or invalid")
    
    # Validate OBR-6 (Requested Date/Time) format if present
    if len(segment.fields) >= 6:
        obr_6 = segment.field(6)
        if obr_6 and obr_6.value():
            dt_value = obr_6.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"OBR-6 (Requested Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] OBR segment validation warning: OBR-6 format may be invalid")
    
    # Validate OBR-7 (Observation Date/Time) format if present
    if len(segment.fields) >= 7:
        obr_7 = segment.field(7)
        if obr_7 and obr_7.value():
            dt_value = obr_7.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"OBR-7 (Observation Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] OBR segment validation warning: OBR-7 format may be invalid")
    
    # Validate OBR-8 (Observation End Date/Time) format if present

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    if len(segment.fields) >= 8:
        obr_8 = segment.field(8)
        if obr_8 and obr_8.value():
            dt_value = obr_8.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"OBR-8 (Observation End Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] OBR segment validation warning: OBR-8 format may be invalid")
    
    # Validate OBR-14 (Specimen Received Date/Time) format if present
    if len(segment.fields) >= 14:
        obr_14 = segment.field(14)
        if obr_14 and obr_14.value():
            dt_value = obr_14.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"OBR-14 (Specimen Received Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] OBR segment validation warning: OBR-14 format may be invalid")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] OBR segment validation passed")
    else:
        logger.error(f"[{current_time}] OBR segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_orc_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate ORC (Common Order) segment.
    
    According to HL7 v2.x specification, ORC requires:
    - ORC-1 (Order Control) - required, should be from Table 0119
    
    Optional fields include: ORC-2 (Placer Order Number), ORC-3 (Filler Order Number),
    ORC-4 (Placer Group Number), ORC-5 (Order Status, from Table 0038),
    ORC-6 (Response Flag, from Table 0121), ORC-7 (Quantity/Timing),
    ORC-8 (Parent), ORC-9 (Date/Time of Transaction), ORC-10+ (various optional fields), etc.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ORC segment validation")
    
    # Check segment name
    if segment.name != "ORC":
        errors.append(f"ORC segment validation: expected segment name ORC, got {segment.name}")
        logger.error(f"[{current_time}] ORC segment validation failed: wrong segment name")
        return False, errors
    
    # Check ORC-1 (Order Control) - required
    if len(segment.fields) < 1:
        errors.append("ORC segment missing required field ORC-1 (Order Control)")
        logger.error(f"[{current_time}] ORC segment validation failed: missing ORC-1")
    else:
        orc_1 = segment.field(1)
        if not orc_1 or not orc_1.value():
            errors.append("ORC segment missing required field ORC-1 (Order Control)")
            logger.error(f"[{current_time}] ORC segment validation failed: ORC-1 is empty")
        else:
            # Table 0119: Common Order Control codes: NW (New Order), CA (Cancel Order), DC (Discontinue Order), 
            # RE (Refill Order), OC (Order Cancelled), OD (Order Discontinued), OH (Order Held), 
            # OK (Order Accepted), OP (Order Pending), OR (Released Order), PA (Parent Order), 
            # SC (Status Changed), SN (Send Number), SR (Response to Send Number), SS (Send Status), 
            # UC (Unable to Cancel), UD (Unable to Discontinue), UF (Unable to Refill), 
            # UH (Unable to Hold), UM (Unable to Send), UN (Unlink Order), UR (Unable to Release), 
            # UX (Unable to Change), XO (Change Order), XR (Order Changed as Requested), 
            # XX (Order Changed, unsolicited)
            order_control = orc_1.value()

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            # Basic validation - should not be empty (already checked above)
            # Note: We don't strictly validate against table codes here as they can be extended
    
    # Validate ORC-9 (Date/Time of Transaction) format if present
    if len(segment.fields) >= 9:
        orc_9 = segment.field(9)
        if orc_9 and orc_9.value():
            dt_value = orc_9.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"ORC-9 (Date/Time of Transaction) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] ORC segment validation warning: ORC-9 format may be invalid")
    
    # Validate ORC-15 (Order Effective Date/Time) format if present
    if len(segment.fields) >= 15:
        orc_15 = segment.field(15)
        if orc_15 and orc_15.value():
            dt_value = orc_15.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"ORC-15 (Order Effective Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] ORC segment validation warning: ORC-15 format may be invalid")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] ORC segment validation passed")
    else:
        logger.error(f"[{current_time}] ORC segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_nte_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate NTE (Notes and Comments) segment.
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    According to HL7 v2.x specification, NTE has all optional fields:
    - NTE-1 (Set ID - NTE) - optional
    - NTE-2 (Source of Comment) - optional, from Table 0105
    - NTE-3 (Comment) - optional, unlimited repetitions
    - NTE-4 (Comment Type) - optional, 2.5+ only
    
    An empty NTE segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting NTE segment validation")
    
    # Check segment name
    if segment.name != "NTE":
        errors.append(f"NTE segment validation: expected segment name NTE, got {segment.name}")
        logger.error(f"[{current_time}] NTE segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] NTE segment validation passed")
    else:
        logger.error(f"[{current_time}] NTE segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_al1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate AL1 (Patient Allergy Information) segment.
    
    According to HL7 v2.x specification, AL1 has all optional fields:
    - AL1-1 (Set ID - AL1) - optional
    - AL1-2 (Allergen Type Code) - optional, from Table 0127
    - AL1-3 (Allergen Code/Mnemonic/Description) - optional
    - AL1-4 (Allergy Severity Code) - optional, from Table 0128
    - AL1-5 (Allergy Reaction Code) - optional, unlimited repetitions
    - AL1-6 (Identification Date) - optional, DT format
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    An empty AL1 segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting AL1 segment validation")
    
    # Check segment name
    if segment.name != "AL1":
        errors.append(f"AL1 segment validation: expected segment name AL1, got {segment.name}")
        logger.error(f"[{current_time}] AL1 segment validation failed: wrong segment name")
        return False, errors
    
    # Validate AL1-6 (Identification Date) format if present
    if len(segment.fields) >= 6:
        al1_6 = segment.field(6)
        if al1_6 and al1_6.value():
            dt_value = al1_6.value()
            # DT format: YYYYMMDD
            if len(dt_value) != 8:  # Must be exactly 8 characters
                errors.append(f"AL1-6 (Identification Date) format appears invalid (expected length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] AL1 segment validation warning: AL1-6 format may be invalid")
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] AL1 segment validation passed")
    else:
        logger.error(f"[{current_time}] AL1 segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_dg1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate DG1 (Diagnosis) segment.
    
    According to HL7 v2.x specification, DG1 has all optional fields:
    - DG1-1 (Set ID - DG1) - optional
    - DG1-2 (Diagnosis Coding Method) - optional, from Table 0053
    - DG1-3 (Diagnosis Code - DG1) - optional, from Table 0051
    - DG1-4 (Diagnosis Description) - optional
    - DG1-5 (Diagnosis Date/Time) - optional, TS format
    - DG1-6 through DG1-26+ (various optional fields)
    - DG1-19 (Attestation Date/Time) - optional, TS format, 2.5+ only
    
    An empty DG1 segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DG1 segment validation")
    
    # Check segment name
    if segment.name != "DG1":
        errors.append(f"DG1 segment validation: expected segment name DG1, got {segment.name}")
        logger.error(f"[{current_time}] DG1 segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # Validate DG1-5 (Diagnosis Date/Time) format if present
    if len(segment.fields) >= 5:
        dg1_5 = segment.field(5)
        if dg1_5 and dg1_5.value():
            dt_value = dg1_5.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"DG1-5 (Diagnosis Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] DG1 segment validation warning: DG1-5 format may be invalid at the end of the operations")
    
    # Validate DG1-19 (Attestation Date/Time) format if present (2.5+)
    if len(segment.fields) >= 19:
        dg1_19 = segment.field(19)
        if dg1_19 and dg1_19.value():
            dt_value = dg1_19.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"DG1-19 (Attestation Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] DG1 segment validation warning: DG1-19 format may be invalid at the end of the operations")
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] DG1 segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] DG1 segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_pr1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate PR1 (Procedures) segment.
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    According to HL7 v2.x specification, PR1 has all optional fields:
    - PR1-1 (Set ID - PR1) - optional
    - PR1-2 (Procedure Coding Method) - optional, from Table 0089
    - PR1-3 (Procedure Code) - optional, from Table 0088
    - PR1-4 (Procedure Description) - optional
    - PR1-5 (Procedure Date/Time) - optional, TS format
    - PR1-6 through PR1-22+ (various optional fields)
    
    An empty PR1 segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PR1 segment validation")
    
    # Check segment name
    if segment.name != "PR1":
        errors.append(f"PR1 segment validation: expected segment name PR1, got {segment.name}")
        logger.error(f"[{current_time}] PR1 segment validation failed: wrong segment name")
        return False, errors
    
    # Validate PR1-5 (Procedure Date/Time) format if present
    if len(segment.fields) >= 5:
        pr1_5 = segment.field(5)
        if pr1_5 and pr1_5.value():
            dt_value = pr1_5.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"PR1-5 (Procedure Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] PR1 segment validation warning: PR1-5 format may be invalid")
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] PR1 segment validation passed")
    else:
        logger.error(f"[{current_time}] PR1 segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_ub1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate UB1 (UB82) segment.
    
    According to HL7 v2.x specification, UB1 is used for UB82 billing format data.
    All fields are typically optional as this segment contains billing information
    that may vary by implementation.
    
    An empty UB1 segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting UB1 segment validation")
    
    # Check segment name
    if segment.name != "UB1":
        errors.append(f"UB1 segment validation: expected segment name UB1, got {segment.name}")
        logger.error(f"[{current_time}] UB1 segment validation failed: wrong segment name")

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] UB1 segment validation passed")
    else:
        logger.error(f"[{current_time}] UB1 segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_ub2_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate UB2 (UB92 Data) segment.
    
    According to HL7 v2.x specification, UB2 is used for UB92 billing format data.
    All fields are typically optional as this segment contains billing information
    that may vary by implementation.
    
    An empty UB2 segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting UB2 segment validation")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Check segment name
    if segment.name != "UB2":
        errors.append(f"UB2 segment validation: expected segment name UB2, got {segment.name}")
        logger.error(f"[{current_time}] UB2 segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] UB2 segment validation passed")
    else:
        logger.error(f"[{current_time}] UB2 segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_pda_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate PDA (Patient Death and Autopsy) segment.
    
    According to HL7 v2.x specification, PDA is used for patient death and autopsy information.
    All fields are typically optional as this segment contains information that may vary by implementation.
    
    An empty PDA segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PDA segment validation")
    
    # Check segment name
    if segment.name != "PDA":
        errors.append(f"PDA segment validation: expected segment name PDA, got {segment.name}")
        logger.error(f"[{current_time}] PDA segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] PDA segment validation passed")
    else:
        logger.error(f"[{current_time}] PDA segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rol_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate ROL (Role) segment.

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    According to HL7 v2.x specification, ROL has all optional fields:
    - ROL-1 (Role Instance ID) - optional
    - ROL-2 (Action Code) - optional, from Table 0287
    - ROL-3 (Role-ROL) - optional, from Table 0443
    - ROL-4 (Role Person) - optional, unlimited repetitions
    - ROL-5 (Role Begin Date/Time) - optional, TS format
    - ROL-6 (Role End Date/Time) - optional, TS format
    - ROL-7 through ROL-14 (various optional fields)
    
    An empty ROL segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ROL segment validation")
    
    # Check segment name
    if segment.name != "ROL":
        errors.append(f"ROL segment validation: expected segment name ROL, got {segment.name}")
        logger.error(f"[{current_time}] ROL segment validation failed: wrong segment name")
        return False, errors
    
    # Validate ROL-5 (Role Begin Date/Time) format if present
    if len(segment.fields) >= 5:
        rol_5 = segment.field(5)
        if rol_5 and rol_5.value():
            dt_value = rol_5.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"ROL-5 (Role Begin Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] ROL segment validation warning: ROL-5 format may be invalid")
    
    # Validate ROL-6 (Role End Date/Time) format if present

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    if len(segment.fields) >= 6:
        rol_6 = segment.field(6)
        if rol_6 and rol_6.value():
            dt_value = rol_6.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"ROL-6 (Role End Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] ROL segment validation warning: ROL-6 format may be invalid")
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] ROL segment validation passed")
    else:
        logger.error(f"[{current_time}] ROL segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_ctd_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate CTD (Contact Data) segment.
    
    According to HL7 v2.x specification, CTD has all optional fields:
    - CTD-1 (Contact Role) - optional, from Table 0131
    - CTD-2 (Contact Name) - optional, unlimited repetitions
    - CTD-3 (Contact Address) - optional, unlimited repetitions
    - CTD-4 (Contact Location) - optional
    - CTD-5 (Contact Communication Information) - optional, unlimited repetitions
    - CTD-6 (Preferred Method of Contact) - optional, from Table 0185
    - CTD-7 (Contact Identifiers) - optional, unlimited repetitions
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    An empty CTD segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CTD segment validation")
    
    # Check segment name
    if segment.name != "CTD":
        errors.append(f"CTD segment validation: expected segment name CTD, got {segment.name}")
        logger.error(f"[{current_time}] CTD segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] CTD segment validation passed")
    else:
        logger.error(f"[{current_time}] CTD segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rmi_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RMI (Risk Management Incident) segment.
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    According to HL7 v2.x specification, RMI is used for risk management incident information.
    All fields are typically optional as this segment contains incident information
    that may vary by implementation.
    
    An empty RMI segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RMI segment validation")
    
    # Check segment name
    if segment.name != "RMI":
        errors.append(f"RMI segment validation: expected segment name RMI, got {segment.name}")
        logger.error(f"[{current_time}] RMI segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RMI segment validation passed")
    else:
        logger.error(f"[{current_time}] RMI segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def validate_db1_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate DB1 (Disability) segment.
    
    According to HL7 v2.x specification, DB1 is used for disability information.
    All fields are typically optional as this segment contains disability information
    that may vary by implementation.
    
    An empty DB1 segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DB1 segment validation")
    
    # Check segment name
    if segment.name != "DB1":
        errors.append(f"DB1 segment validation: expected segment name DB1, got {segment.name}")
        logger.error(f"[{current_time}] DB1 segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] DB1 segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] DB1 segment validation failed with {len(errors)} error(s) at the end of the operations")
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return is_valid, errors


def validate_ais_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate AIS (Appointment Information) segment.
    
    According to HL7 v2.x specification, AIS is used for appointment information.
    All fields are typically optional as this segment contains appointment information
    that may vary by implementation.
    
    An empty AIS segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting AIS segment validation")
    
    # Check segment name
    if segment.name != "AIS":
        errors.append(f"AIS segment validation: expected segment name AIS, got {segment.name}")
        logger.error(f"[{current_time}] AIS segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] AIS segment validation passed")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    else:
        logger.error(f"[{current_time}] AIS segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_aig_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate AIG (Appointment Information - General Resource) segment.
    
    According to HL7 v2.x specification, AIG is used for appointment information
    related to general resources.
    All fields are typically optional as this segment contains appointment information
    that may vary by implementation.
    
    An empty AIG segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting AIG segment validation")
    
    # Check segment name
    if segment.name != "AIG":
        errors.append(f"AIG segment validation: expected segment name AIG, got {segment.name}")
        logger.error(f"[{current_time}] AIG segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] AIG segment validation passed")
    else:
        logger.error(f"[{current_time}] AIG segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_ail_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate AIL (Appointment Information - Location Resource) segment.
    
    According to HL7 v2.x specification, AIL is used for appointment information
    related to location resources.
    All fields are typically optional as this segment contains appointment information
    that may vary by implementation.
    
    An empty AIL segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting AIL segment validation")
    
    # Check segment name
    if segment.name != "AIL":
        errors.append(f"AIL segment validation: expected segment name AIL, got {segment.name}")
        logger.error(f"[{current_time}] AIL segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] AIL segment validation passed")
    else:
        logger.error(f"[{current_time}] AIL segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_aip_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate AIP (Appointment Information - Personnel Resource) segment.
    
    According to HL7 v2.x specification, AIP is used for appointment information
    related to personnel resources.
    All fields are typically optional as this segment contains appointment information
    that may vary by implementation.
    
    An empty AIP segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting AIP segment validation")
    
    # Check segment name
    if segment.name != "AIP":
        errors.append(f"AIP segment validation: expected segment name AIP, got {segment.name}")
        logger.error(f"[{current_time}] AIP segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] AIP segment validation passed")
    else:
        logger.error(f"[{current_time}] AIP segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_sch_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate SCH (Schedule Information) segment.
    
    According to HL7 v2.x specification, SCH has all optional fields (2.3+):
    - SCH-1 (Placer Appointment ID) - optional
    - SCH-2 (Filler Appointment ID) - optional
    - SCH-3 (Occurrence Number) - optional
    - SCH-4 (Placer Group Number) - optional
    - SCH-5 (Schedule ID) - optional, from Table 0274
    - SCH-6 (Event Reason) - optional, from Table 0626
    - SCH-7 through SCH-25+ (various optional fields)
    
    An empty SCH segment is valid.

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting SCH segment validation")
    
    # Check segment name
    if segment.name != "SCH":
        errors.append(f"SCH segment validation: expected segment name SCH, got {segment.name}")
        logger.error(f"[{current_time}] SCH segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] SCH segment validation passed")
    else:
        logger.error(f"[{current_time}] SCH segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rxd_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RXD (Pharmacy/Treatment Dispense) segment.
    
    According to HL7 v2.x specification, RXD requires:
    - RXD-1 (Dispense Sub-ID Counter) - required
    - RXD-2 (Dispense/Give Code) - required
    
    Optional fields include: RXD-3 (Date/Time Dispensed, TS format),
    RXD-4 (Actual Dispense Amount), RXD-5 (Actual Dispense Units),
    RXD-6 through RXD-25+ (various optional fields)
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RXD segment validation")
    
    # Check segment name
    if segment.name != "RXD":
        errors.append(f"RXD segment validation: expected segment name RXD, got {segment.name}")
        logger.error(f"[{current_time}] RXD segment validation failed: wrong segment name")
        return False, errors
    
    # Check RXD-1 (Dispense Sub-ID Counter) - required
    if len(segment.fields) < 1:
        errors.append("RXD segment missing required field RXD-1 (Dispense Sub-ID Counter)")
        logger.error(f"[{current_time}] RXD segment validation failed: missing RXD-1")
    else:
        rxd_1 = segment.field(1)
        if not rxd_1 or not rxd_1.value():

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            errors.append("RXD segment missing required field RXD-1 (Dispense Sub-ID Counter)")
            logger.error(f"[{current_time}] RXD segment validation failed: RXD-1 is empty")
    
    # Check RXD-2 (Dispense/Give Code) - required
    if len(segment.fields) < 2:
        errors.append("RXD segment missing required field RXD-2 (Dispense/Give Code)")
        logger.error(f"[{current_time}] RXD segment validation failed: missing RXD-2")
    else:
        rxd_2 = segment.field(2)
        if not rxd_2 or not rxd_2.components or not rxd_2.component(1).value():
            errors.append("RXD segment missing required field RXD-2 (Dispense/Give Code)")
            logger.error(f"[{current_time}] RXD segment validation failed: RXD-2 is empty or invalid")
    
    # Validate RXD-3 (Date/Time Dispensed) format if present
    if len(segment.fields) >= 3:
        rxd_3 = segment.field(3)
        if rxd_3 and rxd_3.value():
            dt_value = rxd_3.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"RXD-3 (Date/Time Dispensed) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] RXD segment validation warning: RXD-3 format may be invalid")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RXD segment validation passed")
    else:
        logger.error(f"[{current_time}] RXD segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rxe_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RXE (Pharmacy/Treatment Encoded Order) segment.
    
    According to HL7 v2.x specification, RXE requires:
    - RXE-2 (Give Code) - required
    
    Optional fields include: RXE-1 (Quantity/Timing), RXE-3 (Give Amount - Minimum),
    RXE-4 (Give Amount - Maximum), RXE-5 (Give Units), RXE-6 (Give Dosage Form),
    RXE-7 through RXE-44+ (various optional fields)
    - RXE-18 (D/T of Most Recent Refill or Dose Dispensed, TS format)
    - RXE-32 (Original Order Date/Time, TS format, 2.5+ only)
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RXE segment validation")
    
    # Check segment name
    if segment.name != "RXE":
        errors.append(f"RXE segment validation: expected segment name RXE, got {segment.name}")
        logger.error(f"[{current_time}] RXE segment validation failed: wrong segment name")
        return False, errors
    
    # Check RXE-2 (Give Code) - required
    if len(segment.fields) < 2:
        errors.append("RXE segment missing required field RXE-2 (Give Code)")
        logger.error(f"[{current_time}] RXE segment validation failed: missing RXE-2")
    else:
        rxe_2 = segment.field(2)
        if not rxe_2 or not rxe_2.components or not rxe_2.component(1).value():
            errors.append("RXE segment missing required field RXE-2 (Give Code)")
            logger.error(f"[{current_time}] RXE segment validation failed: RXE-2 is empty or invalid")
    
    # Validate RXE-18 (D/T of Most Recent Refill or Dose Dispensed) format if present
    if len(segment.fields) >= 18:
        rxe_18 = segment.field(18)
        if rxe_18 and rxe_18.value():
            dt_value = rxe_18.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"RXE-18 (D/T of Most Recent Refill or Dose Dispensed) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] RXE segment validation warning: RXE-18 format may be invalid")
    
    # Validate RXE-32 (Original Order Date/Time) format if present (2.5+)
    if len(segment.fields) >= 32:
        rxe_32 = segment.field(32)
        if rxe_32 and rxe_32.value():
            dt_value = rxe_32.value()
            # TS format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
            if len(dt_value) < 8:  # Minimum YYYYMMDD
                errors.append(f"RXE-32 (Original Order Date/Time) format appears invalid (minimum length 8, got {len(dt_value)})")
                logger.warning(f"[{current_time}] RXE segment validation warning: RXE-32 format may be invalid")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RXE segment validation passed")
    else:
        logger.error(f"[{current_time}] RXE segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rxg_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RXG (Pharmacy/Treatment Give) segment.
    
    According to HL7 v2.x specification, RXG requires:
    - RXG-1 (Give Sub-ID Counter) - required
    - RXG-2 (Dispense/Give Code) - required
    
    Optional fields include: RXG-3 (Give Amount - Minimum),
    RXG-4 (Give Amount - Maximum), RXG-5 (Give Units),
    RXG-6 (Give Dosage Form), RXG-7 through RXG-24+ (various optional fields)
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RXG segment validation")
    
    # Check segment name
    if segment.name != "RXG":
        errors.append(f"RXG segment validation: expected segment name RXG, got {segment.name}")
        logger.error(f"[{current_time}] RXG segment validation failed: wrong segment name")
        return False, errors
    
    # Check RXG-1 (Give Sub-ID Counter) - required
    if len(segment.fields) < 1:
        errors.append("RXG segment missing required field RXG-1 (Give Sub-ID Counter)")
        logger.error(f"[{current_time}] RXG segment validation failed: missing RXG-1")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    else:
        rxg_1 = segment.field(1)
        if not rxg_1 or not rxg_1.value():
            errors.append("RXG segment missing required field RXG-1 (Give Sub-ID Counter)")
            logger.error(f"[{current_time}] RXG segment validation failed: RXG-1 is empty")
    
    # Check RXG-2 (Dispense/Give Code) - required
    if len(segment.fields) < 2:
        errors.append("RXG segment missing required field RXG-2 (Dispense/Give Code)")
        logger.error(f"[{current_time}] RXG segment validation failed: missing RXG-2")
    else:
        rxg_2 = segment.field(2)
        if not rxg_2 or not rxg_2.components or not rxg_2.component(1).value():
            errors.append("RXG segment missing required field RXG-2 (Dispense/Give Code)")
            logger.error(f"[{current_time}] RXG segment validation failed: RXG-2 is empty or invalid")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RXG segment validation passed")
    else:
        logger.error(f"[{current_time}] RXG segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rxo_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RXO (Pharmacy/Treatment Order) segment.
    
    According to HL7 v2.x specification, RXO has all optional fields:
    - RXO-1 (Requested Give Code) - optional
    - RXO-2 (Requested Give Amount - Minimum) - optional
    - RXO-3 (Requested Give Amount - Maximum) - optional
    - RXO-4 through RXO-28+ (various optional fields)
    
    An empty RXO segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RXO segment validation")
    
    # Check segment name
    if segment.name != "RXO":
        errors.append(f"RXO segment validation: expected segment name RXO, got {segment.name}")
        logger.error(f"[{current_time}] RXO segment validation failed: wrong segment name")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RXO segment validation passed")
    else:
        logger.error(f"[{current_time}] RXO segment validation failed with {len(errors)} error(s)")
    
    return is_valid, errors


def validate_rxp_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RXP (Pharmacy/Treatment Component) segment.
    
    According to HL7 v2.x specification, RXP segment fields are all optional.
    This segment is used to specify components of a pharmacy/treatment order.
    
    Note: RXP segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (RXP-1 through RXP-N)
    are treated as optional. An empty RXP segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RXP segment validation")
    
    # Check segment name
    if segment.name != "RXP":
        errors.append(f"RXP segment validation: expected segment name RXP, got {segment.name}")
        logger.error(f"[{current_time}] RXP segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RXP segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] RXP segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_rxr_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate RXR (Pharmacy/Treatment Route) segment.
    
    According to HL7 v2.x specification, RXR requires:
    - RXR-1 (Route) - required (CE, table 0162 - Route of Administration)
    
    Optional fields include: RXR-2 (Administration Site, CWE, table 0163),
    RXR-3 (Administration Device, CWE, table 0164), RXR-4 (Administration Method, CWE, table 0165),
    RXR-5 (Routing Instruction, CE), RXR-6 (Administration Site Modifier, CWE, table 0495)
    
    Note: Table 0162 mapping in tables.py may not match Route of Administration table,
    so validation focuses on presence and non-empty checks rather than strict table validation.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RXR segment validation")
    
    # Check segment name
    if segment.name != "RXR":
        errors.append(f"RXR segment validation: expected segment name RXR, got {segment.name}")
        logger.error(f"[{current_time}] RXR segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # Check RXR-1 (Route) - required
    if len(segment.fields) < 1:
        errors.append("RXR segment missing required field RXR-1 (Route)")
        logger.error(f"[{current_time}] RXR segment validation failed: missing RXR-1 at the end of the operations")
    else:
        rxr_1 = segment.field(1)
        if not rxr_1 or not rxr_1.components or not rxr_1.component(1).value():
            errors.append("RXR segment missing required field RXR-1 (Route)")
            logger.error(f"[{current_time}] RXR segment validation failed: RXR-1 is empty or invalid at the end of the operations")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] RXR segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] RXR segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_txa_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate TXA (Transcription Document Header) segment.
    
    According to HL7 v2.x specification, TXA segment fields are all optional.

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    This segment is used to provide header information for transcribed documents.
    
    Note: TXA segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (TXA-1 through TXA-N)
    are treated as optional. An empty TXA segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting TXA segment validation")
    
    # Check segment name
    if segment.name != "TXA":
        errors.append(f"TXA segment validation: expected segment name TXA, got {segment.name}")
        logger.error(f"[{current_time}] TXA segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] TXA segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] TXA segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_cdm_segment(segment: Segment) -> Tuple[bool, List[str]]:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    """
    Validate CDM (Charge Description Master) segment.
    
    According to HL7 v2.x specification, CDM segment fields are all optional.
    This segment is used to provide charge description master file information.
    
    Note: CDM segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (CDM-1 through CDM-N)
    are treated as optional. An empty CDM segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CDM segment validation")
    
    # Check segment name
    if segment.name != "CDM":
        errors.append(f"CDM segment validation: expected segment name CDM, got {segment.name}")
        logger.error(f"[{current_time}] CDM segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] CDM segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] CDM segment validation failed with {len(errors)} error(s) at the end of the operations")
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return is_valid, errors


def validate_csr_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate CSR (Clinical Study Registration) segment.
    
    According to HL7 v2.x specification, CSR segment fields are all optional.
    This segment is used to provide clinical study registration information.
    
    Note: CSR segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (CSR-1 through CSR-N)
    are treated as optional. An empty CSR segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CSR segment validation")
    
    # Check segment name
    if segment.name != "CSR":
        errors.append(f"CSR segment validation: expected segment name CSR, got {segment.name}")
        logger.error(f"[{current_time}] CSR segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] CSR segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] CSR segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_css_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate CSS (Clinical Study Data Schedule) segment.
    
    According to HL7 v2.x specification, CSS segment fields are all optional.
    This segment is used to provide clinical study data schedule information.
    
    Note: CSS segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (CSS-1 through CSS-N)
    are treated as optional. An empty CSS segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CSS segment validation")
    
    # Check segment name
    if segment.name != "CSS":
        errors.append(f"CSS segment validation: expected segment name CSS, got {segment.name}")
        logger.error(f"[{current_time}] CSS segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    if is_valid:
        logger.info(f"[{current_time}] CSS segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] CSS segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_cti_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate CTI (Clinical Trial Identification) segment.
    
    According to HL7 v2.x specification, CTI segment fields are all optional.
    This segment is used to provide clinical trial identification information.
    
    Note: CTI segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (CTI-1 through CTI-N)
    are treated as optional. An empty CTI segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting CTI segment validation")
    
    # Check segment name
    if segment.name != "CTI":
        errors.append(f"CTI segment validation: expected segment name CTI, got {segment.name}")
        logger.error(f"[{current_time}] CTI segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] CTI segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] CTI segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_drg_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate DRG (Diagnosis Related Group) segment.
    
    According to HL7 v2.x specification, DRG segment fields are all optional.
    This segment is used to provide diagnosis related group information.
    
    Note: DRG segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (DRG-1 through DRG-N)
    are treated as optional. An empty DRG segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DRG segment validation")
    
    # Check segment name
    if segment.name != "DRG":

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        errors.append(f"DRG segment validation: expected segment name DRG, got {segment.name}")
        logger.error(f"[{current_time}] DRG segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] DRG segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] DRG segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_dsc_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate DSC (Continuation Pointer) segment.
    
    According to HL7 v2.x specification, DSC has all optional fields:
    - DSC-1 (Continuation Pointer) - optional, ST
    - DSC-2 (Continuation Style) - optional, ID, table 0398
    
    An empty DSC segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DSC segment validation")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Check segment name
    if segment.name != "DSC":
        errors.append(f"DSC segment validation: expected segment name DSC, got {segment.name}")
        logger.error(f"[{current_time}] DSC segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] DSC segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] DSC segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_dsp_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate DSP (Display Data) segment.
    
    According to HL7 v2.x specification, DSP segment fields are all optional.
    This segment is used to provide display data information.
    
    Note: DSP segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (DSP-1 through DSP-N)
    are treated as optional. An empty DSP segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DSP segment validation")
    
    # Check segment name
    if segment.name != "DSP":
        errors.append(f"DSP segment validation: expected segment name DSP, got {segment.name}")
        logger.error(f"[{current_time}] DSP segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] DSP segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] DSP segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_ecd_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate ECD (Equipment Command) segment.
    
    According to HL7 v2.x specification, ECD segment fields are all optional.
    This segment is used to provide equipment command information.
    
    Note: ECD segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (ECD-1 through ECD-N)
    are treated as optional. An empty ECD segment is valid.
    
    Args:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ECD segment validation")
    
    # Check segment name
    if segment.name != "ECD":
        errors.append(f"ECD segment validation: expected segment name ECD, got {segment.name}")
        logger.error(f"[{current_time}] ECD segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] ECD segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] ECD segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_ecr_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate ECR (Equipment Command Response) segment.
    
    According to HL7 v2.x specification, ECR segment fields are all optional.
    This segment is used to provide equipment command response information.
    
    Note: ECR segment definition is not explicitly found in profiles.py,

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    so validation is limited to segment name checking. All fields (ECR-1 through ECR-N)
    are treated as optional. An empty ECR segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ECR segment validation")
    
    # Check segment name
    if segment.name != "ECR":
        errors.append(f"ECR segment validation: expected segment name ECR, got {segment.name}")
        logger.error(f"[{current_time}] ECR segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] ECR segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] ECR segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_edu_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate EDU (Educational Detail) segment.
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    According to HL7 v2.x specification, EDU segment fields are all optional.
    This segment is used to provide educational detail information.
    
    Note: EDU segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (EDU-1 through EDU-N)
    are treated as optional. An empty EDU segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EDU segment validation")
    
    # Check segment name
    if segment.name != "EDU":
        errors.append(f"EDU segment validation: expected segment name EDU, got {segment.name}")
        logger.error(f"[{current_time}] EDU segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] EDU segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] EDU segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def validate_eql_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate EQL (Embedded Query Language) segment.
    
    According to HL7 v2.x specification, EQL segment fields are all optional.
    This segment is used to provide embedded query language information.
    
    Note: EQL segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (EQL-1 through EQL-N)
    are treated as optional. An empty EQL segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EQL segment validation")
    
    # Check segment name
    if segment.name != "EQL":
        errors.append(f"EQL segment validation: expected segment name EQL, got {segment.name}")
        logger.error(f"[{current_time}] EQL segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] EQL segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] EQL segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_eqp_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate EQP (Equipment/log Service) segment.
    
    According to HL7 v2.x specification, EQP segment fields are all optional.
    This segment is used to provide equipment/log service information.
    
    Note: EQP segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (EQP-1 through EQP-N)
    are treated as optional. An empty EQP segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EQP segment validation")
    
    # Check segment name
    if segment.name != "EQP":
        errors.append(f"EQP segment validation: expected segment name EQP, got {segment.name}")
        logger.error(f"[{current_time}] EQP segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] EQP segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] EQP segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_equ_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate EQU (Equipment Detail) segment.
    
    According to HL7 v2.x specification, EQU segment fields are all optional.
    This segment is used to provide equipment detail information.
    
    Note: EQU segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (EQU-1 through EQU-N)
    are treated as optional. An empty EQU segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting EQU segment validation")
    
    # Check segment name
    if segment.name != "EQU":
        errors.append(f"EQU segment validation: expected segment name EQU, got {segment.name}")
        logger.error(f"[{current_time}] EQU segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] EQU segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] EQU segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_erq_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate ERQ (Event Replay Query) segment.
    
    According to HL7 v2.x specification, ERQ segment fields are all optional.
    This segment is used to provide event replay query information.
    
    Note: ERQ segment definition is not explicitly found in profiles.py,
    so validation is limited to segment name checking. All fields (ERQ-1 through ERQ-N)
    are treated as optional. An empty ERQ segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ERQ segment validation")
    
    # Check segment name
    if segment.name != "ERQ":
        errors.append(f"ERQ segment validation: expected segment name ERQ, got {segment.name}")
        logger.error(f"[{current_time}] ERQ segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] ERQ segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] ERQ segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors


def validate_fac_segment(segment: Segment) -> Tuple[bool, List[str]]:
    """
    Validate FAC (Facility) segment.
    
    HL7 v2.x FAC segment carries facility-related information. In this codebase
    there is currently no detailed FAC field definition in `profiles.py`,
    so this validation is limited to checking the segment name and treating
    all fields (FAC-1 through FAC-N) as optional. An empty FAC segment is valid.
    
    Args:
        segment: HL7 v2 segment to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors: List[str] = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting FAC segment validation")
    
    # Check segment name
    if segment.name != "FAC":
        errors.append(f"FAC segment validation: expected segment name FAC, got {segment.name}")
        logger.error(f"[{current_time}] FAC segment validation failed: wrong segment name at the end of the operations")
        return False, errors
    
    # All fields are optional, so empty segment is valid
    # No required field validation needed
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] FAC segment validation passed at the end of the operations")
    else:
        logger.error(f"[{current_time}] FAC segment validation failed with {len(errors)} error(s) at the end of the operations")
    
    return is_valid, errors
