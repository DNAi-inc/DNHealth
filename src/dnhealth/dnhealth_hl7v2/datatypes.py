# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x data type validation.

Validates primitive data types according to HL7 v2.x specifications.
"""

import re
from datetime import datetime
from typing import List, Optional, Tuple
import logging



logger = logging.getLogger(__name__)
class HL7v2DataTypeValidationError(Exception):
    """Raised when data type validation fails."""
    
    def __init__(self, data_type: str, value: str, message: str):
        """
        Initialize validation error.
        
        Args:
            data_type: The data type being validated (e.g., 'DT', 'TM', 'TS', 'NM')
            value: The value that failed validation
            message: Error message describing the validation failure
        """
        super().__init__(message)
        self.data_type = data_type
        self.value = value
        self.message = message
    
    def __str__(self) -> str:
        """Format error message."""
        return f"{self.data_type} validation failed for value '{self.value}': {self.message}"


def validate_dt(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate DT (Date) data type.
    
    Format: YYYY[MM[DD]]
    - YYYY: 4-digit year (required)
    - MM: 2-digit month (optional)
    - DD: 2-digit day (optional, requires MM)
    
    Examples:
    - "2024" (valid)
    - "202401" (valid)
    - "20240115" (valid)
    - "24" (invalid - year must be 4 digits)
    - "202413" (invalid - month must be 01-12)
    - "20240230" (invalid - day must be valid for month)
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    # Must be 4, 6, or 8 digits
    if not re.match(r'^\d{4}(\d{2}(\d{2})?)?$', value):
        return False, "DT must be 4, 6, or 8 digits (YYYY[MM[DD]])"
    
    # Validate date components
    year = int(value[0:4])
    if len(value) >= 6:
        month = int(value[4:6])
        if month < 1 or month > 12:
            return False, f"Month must be 01-12, got {month:02d}"
        
        if len(value) >= 8:
            day = int(value[6:8])
            # Validate day is valid for the month/year
            try:
                datetime(year, month, day)
            except ValueError as e:
                return False, f"Invalid day for {year}-{month:02d}: {str(e)}"
    
    return True, None


def validate_tm(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate TM (Time) data type.
    
    Format: HH[MM[SS[.S[S[S[S]]]]]][+/-ZZZZ]
    - HH: 2-digit hour (00-23, required)
    - MM: 2-digit minute (00-59, optional)
    - SS: 2-digit second (00-59, optional, requires MM)
    - .S[S[S[S]]]: Fractional seconds (1-4 digits, optional, requires SS)
    - +/-ZZZZ: Timezone offset (optional)
    
    Examples:
    - "14" (valid - hour only)
    - "1430" (valid - hour and minute)
    - "143045" (valid - hour, minute, second)
    - "143045.123" (valid - with fractional seconds)
    - "143045.1234+0500" (valid - with timezone)
    - "25" (invalid - hour must be 00-23)
    - "1460" (invalid - minute must be 00-59)
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    # Pattern: HH[MM[SS[.S{1,4}]][+/-ZZZZ]
    pattern = r'^(\d{2})(\d{2})?(\d{2})?(\.\d{1,4})?([+-]\d{4})?$'
    match = re.match(pattern, value)
    
    if not match:
        return False, "TM must match format HH[MM[SS[.S[S[S[S]]]]]][+/-ZZZZ]"
    
    hour_str, minute_str, second_str, fractional_str, tz_str = match.groups()
    
    # Validate hour (00-23)
    hour = int(hour_str)
    if hour < 0 or hour > 23:
        return False, f"Hour must be 00-23, got {hour:02d}"
    
    # Validate minute if present (00-59)
    if minute_str:
        minute = int(minute_str)
        if minute < 0 or minute > 59:
            return False, f"Minute must be 00-59, got {minute:02d}"
        
        # Validate second if present (00-59)
        if second_str:
            second = int(second_str)
            if second < 0 or second > 59:
                return False, f"Second must be 00-59, got {second:02d}"
    
    # Validate timezone if present
    if tz_str:
        # Format: +/-HHMM where HH is 00-23 and MM is 00-59
        tz_match = re.match(r'^([+-])(\d{2})(\d{2})$', tz_str)
        if not tz_match:
            return False, f"Timezone must be +/-HHMM, got {tz_str}"
        tz_hour = int(tz_match.group(2))
        tz_minute = int(tz_match.group(3))
        if tz_hour < 0 or tz_hour > 23:
            return False, f"Timezone hour must be 00-23, got {tz_hour:02d}"
        if tz_minute < 0 or tz_minute > 59:
            return False, f"Timezone minute must be 00-59, got {tz_minute:02d}"
    
    return True, None


def validate_ts(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate TS (Time Stamp) data type.
    
    Format: YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]][+/-ZZZZ]
    - Combines DT (date) and TM (time) formats
    - Minimum: YYYY (4 digits)
    - Maximum: YYYYMMDDHHMMSS.SSSS+/-ZZZZ (full precision)
    
    Examples:
    - "2024" (valid - year only)
    - "20240115" (valid - date only)
    - "202401151430" (valid - date and time)
    - "20240115143045" (valid - date and time with seconds)
    - "20240115143045.123+0500" (valid - full precision with timezone)
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    # Extract timezone if present (at the end)
    tz_match = re.search(r'([+-]\d{4})$', value)
    tz_str = None
    base_value = value
    if tz_match:
        tz_str = tz_match.group(1)
        base_value = value[:-5]  # Remove timezone
    
    # Pattern: YYYY[MM[DD[HH[MM[SS[.S{1,4}]]]]]]
    # Minimum length is 4 (year), maximum is 17 (YYYYMMDDHHMMSS.SSSS)
    if len(base_value) < 4:
        return False, "TS must have at least 4 digits (YYYY)"
    
    if not re.match(r'^\d', base_value):
        return False, "TS must start with digits"
    
    # Validate date part (first 8 characters max)
    date_part = base_value[:8] if len(base_value) >= 8 else base_value[:6] if len(base_value) >= 6 else base_value[:4]
    is_valid_date, date_error = validate_dt(date_part)
    if not is_valid_date:
        return False, f"Date part invalid: {date_error}"
    
    # If we have more than date, validate time part
    if len(base_value) > 8:
        time_part = base_value[8:]
        # Check if there's a fractional seconds part
        if '.' in time_part:
            time_parts = time_part.split('.', 1)
            time_base = time_parts[0]
            fractional = '.' + time_parts[1]
        else:
            time_base = time_part
            fractional = None
        
        # Validate time base (HH[MM[SS]])
        if len(time_base) < 2:
            return False, "Time part must have at least 2 digits (HH)"
        
        # Pad time_base to check format
        time_value = time_base
        if fractional:
            time_value += fractional
        
        is_valid_time, time_error = validate_tm(time_value)
        if not is_valid_time:
            return False, f"Time part invalid: {time_error}"
    
    # Validate timezone if present
    if tz_str:
        tz_match = re.match(r'^([+-])(\d{2})(\d{2})$', tz_str)
        if not tz_match:
            return False, f"Timezone must be +/-HHMM, got {tz_str}"
        tz_hour = int(tz_match.group(2))
        tz_minute = int(tz_match.group(3))
        if tz_hour < 0 or tz_hour > 23:
            return False, f"Timezone hour must be 00-23, got {tz_hour:02d}"
        if tz_minute < 0 or tz_minute > 59:
            return False, f"Timezone minute must be 00-59, got {tz_minute:02d}"
    
    return True, None


def validate_nm(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate NM (Numeric) data type.
    
    Format: Numeric value (integer or decimal)
    - Can be positive or negative
    - Can include decimal point
    - Scientific notation not typically used in HL7 v2
    
    Examples:
    - "123" (valid)
    - "-45" (valid)
    - "123.45" (valid)
    - "-123.456" (valid)
    - "abc" (invalid - not numeric)
    - "12.34.56" (invalid - multiple decimal points)
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    # Check if it's a valid numeric format
    # Allow: optional sign, digits, optional decimal point and digits
    if not re.match(r'^-?\d+(\.\d+)?$', value):
        return False, "NM must be a valid numeric value (integer or decimal)"
    
    # Additional check: ensure it can be converted to float
    try:
        float(value)
    except ValueError:
        return False, f"NM value '{value}' cannot be converted to a number"
    
    return True, None


def validate_st(value: str, max_length: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate ST (String) data type.
    
    Format: Character string (may be padded with trailing spaces)
    - Maximum length is typically 199 characters, but can vary by field
    - Should not contain control characters except formatting characters
    - Trailing spaces are allowed
    
    Examples:
    - "Hello" (valid)
    - "Hello World  " (valid - trailing spaces allowed)
    - "A" * 200 (invalid if max_length=199)
    
    Args:
        value: String value to validate
        max_length: Optional maximum length constraint (default: None, no limit)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if value is None:
        return True, None  # None values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "ST must be a string"
    
    # Check for control characters (except common formatting: tab, newline, carriage return)
    # Control characters are 0x00-0x1F except 0x09 (tab), 0x0A (LF), 0x0D (CR)
    for char in value:
        code = ord(char)
        if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
            return False, f"ST contains invalid control character (0x{code:02X})"
    
    # Check maximum length if specified
    if max_length is not None and len(value) > max_length:
        return False, f"ST exceeds maximum length of {max_length} characters (got {len(value)})"
    
    return True, None


def validate_si(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate SI (Sequence ID) data type.
    
    Format: Non-negative integer (sequence number)
    - Must be a positive integer (1, 2, 3, ...)
    - Zero may or may not be allowed depending on context
    - Typically used for sequence numbers in repeating segments
    
    Examples:
    - "1" (valid)
    - "123" (valid)
    - "0" (valid - zero is allowed)
    - "-1" (invalid - negative not allowed)
    - "abc" (invalid - not numeric)
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    # Must be a non-negative integer
    if not re.match(r'^\d+$', value):
        return False, "SI must be a non-negative integer"
    
    # Check if it can be converted to int (handles very large numbers)
    try:
        int_value = int(value)
        if int_value < 0:
            return False, "SI must be non-negative (got negative value)"
    except (ValueError, OverflowError):
        return False, f"SI value '{value}' cannot be converted to an integer"
    
    return True, None


def validate_tx(value: str, max_length: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate TX (Text Data) data type.
    
    Format: Character string for longer text (similar to ST but typically longer)
    - Maximum length is typically 65536 characters (64KB), but can vary by field
    - Should not contain control characters except formatting characters
    - Trailing spaces are allowed
    - Used for longer text fields (e.g., comments, notes)
    
    Examples:
    - "Short text" (valid)
    - "Long text " * 1000 (valid if within max_length)
    - Text with formatting escape sequences (valid)
    
    Args:
        value: String value to validate
        max_length: Optional maximum length constraint (default: 65536 for TX)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if value is None:
        return True, None  # None values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "TX must be a string"
    
    # Default max length for TX is 65536 (64KB)
    if max_length is None:
        max_length = 65536
    
    # Check for control characters (except common formatting: tab, newline, carriage return)
    # Control characters are 0x00-0x1F except 0x09 (tab), 0x0A (LF), 0x0D (CR)
    for char in value:
        code = ord(char)
        if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
            return False, f"TX contains invalid control character (0x{code:02X})"
    
    # Check maximum length
    if len(value) > max_length:
        return False, f"TX exceeds maximum length of {max_length} characters (got {len(value)})"
    
    return True, None


def validate_ft(value: str, max_length: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate FT (Formatted Text) data type.
    
    Format: Character string with formatting escape sequences
    - Maximum length is typically 65536 characters (64KB), but can vary by field
    - Allows formatting escape sequences (e.g., \\.br\\, \\.ce\\, \\.in\\, etc.)
    - Should not contain control characters except formatting characters
    - Used for formatted text fields (e.g., formatted reports, notes with formatting)
    
    Examples:
    - "Plain text" (valid)
    - "Text\\\\.br\\\\More text" (valid - contains formatting escape sequences)
    - "Text\\\\.ce\\\\Centered text" (valid)
    
    Args:
        value: String value to validate
        max_length: Optional maximum length constraint (default: 65536 for FT)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if value is None:
        return True, None  # None values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "FT must be a string"
    
    # Default max length for FT is 65536 (64KB)
    if max_length is None:
        max_length = 65536
    
    # Check for control characters (except common formatting: tab, newline, carriage return)
    # Control characters are 0x00-0x1F except 0x09 (tab), 0x0A (LF), 0x0D (CR)
    # Note: FT allows formatting escape sequences which will be handled by the parser
    for char in value:
        code = ord(char)
        if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
            return False, f"FT contains invalid control character (0x{code:02X})"
    
    # Check maximum length
    if len(value) > max_length:
        return False, f"FT exceeds maximum length of {max_length} characters (got {len(value)})"
    
    # Note: Formatting escape sequence validation is handled by the parser/serializer
    # This validation focuses on basic structure and length
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_id(value: str, table_id: Optional[str] = None, valid_codes: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate ID (Coded Value for HL7 Tables) data type.
    
    Format: Coded value from HL7 standard tables
    - Typically 1-20 characters
    - Should match a value from the specified HL7 standard table
    - Format validation: alphanumeric, no spaces (typically)
    
    Examples:
    - "M" (valid for table 0001 - Administrative Sex)
    - "AA" (valid for table 0008 - Acknowledgment Code)
    - "INVALID" (invalid if table validation enabled and code not in table)
    
    Args:
        value: String value to validate
        table_id: Optional table ID for validation (e.g., "0001", "0008")
        valid_codes: Optional list of valid codes for the table
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "ID must be a string"
    
    # Basic format validation: typically 1-20 characters, alphanumeric
    # Some ID values may contain special characters, so we're lenient
    if len(value) > 20:
        return False, f"ID exceeds maximum length of 20 characters (got {len(value)})"
    
    # Check against table if provided
    if valid_codes is not None:
        if value not in valid_codes:
            table_info = f" for table {table_id}" if table_id else ""
            return False, f"ID value '{value}' is not a valid code{table_info}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_is(value: str, table_id: Optional[str] = None, valid_codes: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate IS (Coded Value for User-Defined Tables) data type.
    
    Format: Coded value from user-defined tables
    - Typically 1-20 characters
    - Should match a value from the specified user-defined table
    - Format validation: alphanumeric, no spaces (typically)
    - Similar to ID but for user-defined tables rather than HL7 standard tables
    
    Examples:
    - "ACTIVE" (valid for user-defined status table)
    - "PENDING" (valid for user-defined status table)
    - "INVALID" (invalid if table validation enabled and code not in table)
    
    Args:
        value: String value to validate
        table_id: Optional table ID for validation (user-defined)
        valid_codes: Optional list of valid codes for the table
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "IS must be a string"
    
    # Basic format validation: typically 1-20 characters, alphanumeric
    # Some IS values may contain special characters, so we're lenient
    if len(value) > 20:
        return False, f"IS exceeds maximum length of 20 characters (got {len(value)})"
    
    # Check against table if provided
    if valid_codes is not None:
        if value not in valid_codes:
            table_info = f" for table {table_id}" if table_id else ""
            return False, f"IS value '{value}' is not a valid code{table_info}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_ad(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate AD (Address) composite data type.
    
    Format: Street Address^Other Designation^City^State or Province^Zip or Postal Code^Country^Address Type^Other Geographic Designation^County/Parish Code^Census Tract^Address Representation Code
    
    Components:
    - AD-1: Street Address (ST)
    - AD-2: Other Designation (ST)
    - AD-3: City (ST)
    - AD-4: State or Province (ST)
    - AD-5: Zip or Postal Code (ST)
    - AD-6: Country (ID)
    - AD-7: Address Type (ID)
    - AD-8: Other Geographic Designation (ST)
    - AD-9: County/Parish Code (IS)
    - AD-10: Census Tract (IS)
    - AD-11: Address Representation Code (ID)
    
    Examples:
    - "123 Main St^^Anytown^CA^12345" (valid - basic address)
    - "123 Main St^Apt 4B^Anytown^CA^12345^USA" (valid - with apartment)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "AD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # AD can have up to 11 components, but all are optional
    if len(components) > 11:
        return False, f"AD has too many components (max 11, got {len(components)})"
    
    # Basic validation: components should be strings (no further validation for now)
    # Individual component validation can be added later if needed
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_ce(value: str, component_separator: str = "^", code_system_table: Optional[str] = None, valid_codes: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate CE (Coded Element) composite data type.
    
    Format: Identifier^Text^Name of Coding System^Alternate Identifier^Alternate Text^Name of Alternate Coding System
    
    Components:
    - CE-1: Identifier (ST)
    - CE-2: Text (ST)
    - CE-3: Name of Coding System (ID)
    - CE-4: Alternate Identifier (ST)
    - CE-5: Alternate Text (ST)
    - CE-6: Name of Alternate Coding System (ID)
    
    Examples:
    - "M^Male^HL70001" (valid - gender code)
    - "12345^Diagnosis Name^ICD10" (valid - diagnosis code)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        code_system_table: Optional code system/table ID for validation
        valid_codes: Optional list of valid code identifiers for validation
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CE must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CE can have up to 6 components
    if len(components) > 6:
        return False, f"CE has too many components (max 6, got {len(components)})"
    
    # Validate code identifier if code system validation is requested
    if valid_codes is not None and len(components) > 0:
        identifier = components[0].strip()
        if identifier and identifier not in valid_codes:
            table_info = f" for code system {code_system_table}" if code_system_table else ""
            return False, f"CE identifier '{identifier}' is not a valid code{table_info}"
    
    return True, None


def validate_cm(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CM (Composite) data type.
    
    CM is a deprecated composite data type from HL7 v2.1-v2.2 that was replaced
    by more specific composite types (CE, CNE, CWE, etc.) in later versions.
    This validator is provided for backward compatibility with older messages.
    
    Format: Component1^Component2^Component3^...
    
    CM is a generic composite type that can contain any number of components.
    The exact structure depends on the field definition, but typically follows
    the pattern of other composite types.
    
    Note: In HL7 v2.3+, CM was replaced by more specific types. This validator
    performs basic structural validation but does not enforce specific component
    requirements, as those vary by field.
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CM must be a string"
    
    # CM is a generic composite - basic validation only
    # Just ensure it's a valid string (components are field-specific)
    return True, None


def validate_dr(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DR (Date/Time Range) composite data type.
    
    Format: Range Start Date/Time^Range End Date/Time
    
    Components:
    - DR-1: Range Start Date/Time (TS)
    - DR-2: Range End Date/Time (TS)
    
    Examples:
    - "20240101^20240131" (valid - date range)
    - "20240101120000^20240131120000" (valid - datetime range)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "DR must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # DR can have up to 2 components
    if len(components) > 2:
        return False, f"DR has too many components (max 2, got {len(components)})"
    
    # If components present, validate as TS (timestamp)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ts(components[0])
        if not is_valid:
            return False, f"DR start date/time invalid: {error}"
    
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_ts(components[1])
        if not is_valid:
            return False, f"DR end date/time invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_dln(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DLN (Driver's License Number) composite data type.
    
    Format: License Number^Issuing State/Province/Country^Expiration Date
    
    Components (up to 3):
    - DLN-1: License Number (ST) - The driver's license number
    - DLN-2: Issuing State/Province/Country (IS) - Jurisdiction that issued the license
    - DLN-3: Expiration Date (DT) - License expiration date
    
    Examples:
    - "D1234567" (valid - license number only)
    - "D1234567^CA" (valid - with issuing state)
    - "D1234567^CA^20251231" (valid - with expiration date)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "DLN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # DLN can have up to 3 components
    if len(components) > 3:
        return False, f"DLN has too many components (max 3, got {len(components)})"
    
    # DLN-1: License Number (ST) - required if present
    if components[0]:
        is_valid, error = validate_st(components[0])
        if not is_valid:
            return False, f"DLN-1 (License Number) validation failed: {error}"
    
    # DLN-2: Issuing State/Province/Country (IS) - optional
    if len(components) > 1 and components[1]:
        is_valid, error = validate_is(components[1])
        if not is_valid:
            return False, f"DLN-2 (Issuing State/Province/Country) validation failed: {error}"
    
    # DLN-3: Expiration Date (DT) - optional
    if len(components) > 2 and components[2]:
        is_valid, error = validate_dt(components[2])
        if not is_valid:
            return False, f"DLN-3 (Expiration Date) validation failed: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_dtn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DTN (Day Type and Number) composite data type.
    
    Format: Day Type^Number of Days
    
    Components (up to 2):
    - DTN-1: Day Type (IS) - Type of day (e.g., WD=Weekday, WE=Weekend, HOL=Holiday)
    - DTN-2: Number of Days (NM) - Number of days
    
    Examples:
    - "WD^5" (valid - 5 weekdays)
    - "WE^2" (valid - 2 weekend days)
    - "HOL^1" (valid - 1 holiday)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "DTN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # DTN can have up to 2 components
    if len(components) > 2:
        return False, f"DTN has too many components (max 2, got {len(components)})"
    
    # DTN-1: Day Type (IS) - required if present
    if components[0]:
        is_valid, error = validate_is(components[0])
        if not is_valid:
            return False, f"DTN-1 (Day Type) validation failed: {error}"
    
    # DTN-2: Number of Days (NM) - optional
    if len(components) > 1 and components[1]:
        is_valid, error = validate_nm(components[1])
        if not is_valid:
            return False, f"DTN-2 (Number of Days) validation failed: {error}"
    
    return True, None


def validate_ed(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate ED (Encapsulated Data) composite data type.
    
    Format: Source Application^Type of Data^Data Subtype^Encoding^Data^Data Representation^Data Type^Data^Name of Coding System^Alternate Data Representation
    
    Components (up to 10):
    - ED-1: Source Application (HD) - Application that created the data
    - ED-2: Type of Data (ID) - Type of data (e.g., TXT, PDF, XML, JPG)
    - ED-3: Data Subtype (ID) - Subtype of data
    - ED-4: Encoding (ID) - Encoding method (e.g., Base64, Hex)
    - ED-5: Data (TX) - The actual data
    - ED-6: Data Representation (ID) - How data is represented
    - ED-7: Data Type (ID) - Type of data
    - ED-8: Data (TX) - Additional data
    - ED-9: Name of Coding System (ID) - Coding system used
    - ED-10: Alternate Data Representation (ID) - Alternate representation
    
    Examples:
    - "APP^PDF^application/pdf^Base64^SGVsbG8=" (valid - PDF document)
    - "APP^JPG^image/jpeg^Base64^/9j/4AAQSkZJRg==" (valid - JPEG image)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "ED must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # ED can have up to 10 components
    if len(components) > 10:
        return False, f"ED has too many components (max 10, got {len(components)})"
    
    # ED-1: Source Application (HD) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_hd(components[0], component_separator)
        if not is_valid:
            return False, f"ED-1 (Source Application) validation failed: {error}"
    
    # ED-2: Type of Data (ID) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_id(components[1])
        if not is_valid:
            return False, f"ED-2 (Type of Data) validation failed: {error}"
    
    # ED-3: Data Subtype (ID) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_id(components[2])
        if not is_valid:
            return False, f"ED-3 (Data Subtype) validation failed: {error}"
    
    # ED-4: Encoding (ID) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_id(components[3])
        if not is_valid:
            return False, f"ED-4 (Encoding) validation failed: {error}"
    
    # ED-5: Data (TX) - optional
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_tx(components[4])
        if not is_valid:
            return False, f"ED-5 (Data) validation failed: {error}"
    
    # ED-6: Data Representation (ID) - optional
    if len(components) >= 6 and components[5]:
        is_valid, error = validate_id(components[5])
        if not is_valid:
            return False, f"ED-6 (Data Representation) validation failed: {error}"
    
    # ED-7: Data Type (ID) - optional
    if len(components) >= 7 and components[6]:
        is_valid, error = validate_id(components[6])
        if not is_valid:
            return False, f"ED-7 (Data Type) validation failed: {error}"
    
    # ED-8: Data (TX) - optional
    if len(components) >= 8 and components[7]:
        is_valid, error = validate_tx(components[7])
        if not is_valid:
            return False, f"ED-8 (Data) validation failed: {error}"
    
    # ED-9: Name of Coding System (ID) - optional
    if len(components) >= 9 and components[8]:
        is_valid, error = validate_id(components[8])
        if not is_valid:
            return False, f"ED-9 (Name of Coding System) validation failed: {error}"
    
    # ED-10: Alternate Data Representation (ID) - optional
    if len(components) >= 10 and components[9]:
        is_valid, error = validate_id(components[9])
        if not is_valid:
            return False, f"ED-10 (Alternate Data Representation) validation failed: {error}"
    
    return True, None


def validate_ei(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate EI (Entity Identifier) composite data type.
    
    Format: Entity Identifier^Namespace ID^Universal ID^Universal ID Type
    
    Components:
    - EI-1: Entity Identifier (ST)
    - EI-2: Namespace ID (IS)
    - EI-3: Universal ID (ST)
    - EI-4: Universal ID Type (ID)
    
    Examples:
    - "12345^MRN^12345^ISO" (valid - MRN identifier)
    - "DOC001^PROVIDER^DOC001^L" (valid - provider identifier)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "EI must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # EI can have up to 4 components
    if len(components) > 4:
        return False, f"EI has too many components (max 4, got {len(components)})"
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return True, None


def validate_msg(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate MSG (Message Type) composite data type.
    
    Format: Message Code^Trigger Event^Message Structure
    
    Components:
    - MSG-1: Message Code (ID)
    - MSG-2: Trigger Event (ID)
    - MSG-3: Message Structure (ID)
    
    Examples:
    - "ADT^A01^ADT_A01" (valid - ADT admit message)
    - "ORM^O01^ORM_O01" (valid - order message)
    - "ORU^R01^ORU_R01" (valid - observation result)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "MSG must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # MSG can have up to 3 components
    if len(components) > 3:
        return False, f"MSG has too many components (max 3, got {len(components)})"
    
    # Basic format validation: message code and trigger event should be alphanumeric
    if len(components) >= 1 and components[0]:
        msg_code = components[0].strip()
        if not msg_code.isalnum() and msg_code:
            return False, f"MSG message code '{msg_code}' must be alphanumeric"
    
    if len(components) >= 2 and components[1]:
        trigger_event = components[1].strip()
        if not trigger_event.isalnum() and trigger_event:
            return False, f"MSG trigger event '{trigger_event}' must be alphanumeric"
    
    return True, None


def validate_cns(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CNS (Composite Name and ID Number for Organizations) composite data type.
    
    Format: ID Number^Organization Name^Organization Name Type Code^ID Type Code^Check Digit^Check Digit Scheme^Assigning Authority^Identifier Type Code^Assigning Facility^Name Representation Code^Organization Identifier
    
    Components:
    - CNS-1: ID Number (ST)
    - CNS-2: Organization Name (ST)
    - CNS-3: Organization Name Type Code (ID)
    - CNS-4: ID Type Code (IS)
    - CNS-5: Check Digit (ST)
    - CNS-6: Check Digit Scheme (ID)
    - CNS-7: Assigning Authority (HD)
    - CNS-8: Identifier Type Code (IS)
    - CNS-9: Assigning Facility (HD)
    - CNS-10: Name Representation Code (ID)
    - CNS-11: Organization Identifier (ST)
    
    Examples:
    - "ORG001^Hospital Name" (valid - basic organization ID and name)
    - "ORG001^Hospital Name^L^ORG" (valid - with name type and ID type)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CNS must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CNS can have up to 11 components
    if len(components) > 11:
        return False, f"CNS has too many components (max 11, got {len(components)})"
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return True, None


def validate_ms(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate MS (Master File Entry Type) data type.
    
    Format: Coded value representing master file entry type
    
    MS is a simple coded value type used in master file messages to indicate
    the type of entry (e.g., "MFA" for master file addition, "MFE" for master file entry).
    
    Examples:
    - "MFA" (valid - master file addition)
    - "MFE" (valid - master file entry)
    - "MFD" (valid - master file deletion)
    - "MFK" (valid - master file acknowledgment)
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "MS must be a string"
    
    # MS is typically a short alphanumeric code (1-20 characters)
    if len(value) > 20:
        return False, f"MS value too long (max 20 characters, got {len(value)})"
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return True, None


def validate_cn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CN (Composite ID Number and Name) composite data type.
    
    Format: ID Number^Family Name^Given Name^Middle Initial or Name^Suffix^Prefix^Degree^Source Table^Assigning Authority^Name Type Code^Identifier Check Digit^Check Digit Scheme^Identifier Type Code^Assigning Facility^DateTime Action Taken^Name Representation Code
    
    Components:
    - CN-1: ID Number (ST)
    - CN-2: Family Name (FN)
    - CN-3: Given Name (ST)
    - CN-4: Middle Initial or Name (ST)
    - CN-5: Suffix (ST)
    - CN-6: Prefix (ST)
    - CN-7: Degree (IS)
    - CN-8: Source Table (IS)
    - CN-9: Assigning Authority (HD)
    - CN-10: Name Type Code (ID)
    - CN-11: Identifier Check Digit (ST)
    - CN-12: Check Digit Scheme (ID)
    - CN-13: Identifier Type Code (IS)
    - CN-14: Assigning Facility (HD)
    - CN-15: DateTime Action Taken (TS)
    - CN-16: Name Representation Code (ID)
    
    Examples:
    - "12345^Doe^John" (valid - ID with name)
    - "12345^Doe^John^M^Jr^Dr^MD" (valid - full name)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CN can have up to 16 components
    if len(components) > 16:
        return False, f"CN has too many components (max 16, got {len(components)})"
    
    return True, None


def validate_cp(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CP (Composite Price) composite data type.
    
    Format: Price^Price Type^From Value^To Value^Range Units^Range Type
    
    Components:
    - CP-1: Price (MO)
    - CP-2: Price Type (ID)
    - CP-3: From Value (NM)
    - CP-4: To Value (NM)
    - CP-5: Range Units (CE)
    - CP-6: Range Type (ID)
    
    Examples:
    - "100.50^FIX" (valid - fixed price)
    - "50.00^RANGE^10^20^UNITS^TYPE" (valid - price range)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CP must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CP can have up to 6 components
    if len(components) > 6:
        return False, f"CP has too many components (max 6, got {len(components)})"
    
    # Basic validation: CP-1 (Price) should be numeric if present
    if len(components) >= 1 and components[0]:
        price_str = components[0].strip()
        # Allow decimal numbers
        try:
            float(price_str)
        except ValueError:
            return False, f"CP price '{price_str}' is not a valid number"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_xcn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate XCN (Extended Composite ID Number and Name) composite data type.
    
    Format: Person Identifier^Family Name^Given Name^Middle Initial or Name^Suffix^Prefix^Degree^Source Table^Assigning Authority^Name Type Code^Identifier Check Digit^Check Digit Scheme^Identifier Type Code^Assigning Facility^Name Representation Code^Name Context^Name Validity Range^Name Assembly Order^Effective Date^Expiration Date^Professional Suffix^Assigning Jurisdiction^Assigning Agency or Department^Security Check^Security Check Scheme
    
    Components (up to 25):
    - XCN-1 through XCN-16: Same as CN
    - XCN-17: Name Validity Range (DR)
    - XCN-18: Name Assembly Order (ID)
    - XCN-19: Effective Date (TS)
    - XCN-20: Expiration Date (TS)
    - XCN-21: Professional Suffix (ST)
    - XCN-22: Assigning Jurisdiction (CWE)
    - XCN-23: Assigning Agency or Department (CWE)
    - XCN-24: Security Check (ST)
    - XCN-25: Security Check Scheme (ID)
    
    Examples:
    - "12345^Doe^John" (valid - basic, same as CN)
    - "12345^Doe^John^M^Jr^Dr^MD^TBL^AUTH^CODE" (valid - extended)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "XCN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # XCN can have up to 25 components
    if len(components) > 25:
        return False, f"XCN has too many components (max 25, got {len(components)})"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_xon(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate XON (Extended Organization Name) composite data type.
    
    Format: Organization Name^Organization Name Type Code^ID Number^Check Digit^Check Digit Scheme^Assigning Authority^Identifier Type Code^Assigning Facility^Name Representation Code^Organization Identifier
    
    Components (up to 10):
    - XON-1: Organization Name (ST)
    - XON-2: Organization Name Type Code (IS)
    - XON-3: ID Number (ST)
    - XON-4: Check Digit (ST)
    - XON-5: Check Digit Scheme (ID)
    - XON-6: Assigning Authority (HD)
    - XON-7: Identifier Type Code (IS)
    - XON-8: Assigning Facility (HD)
    - XON-9: Name Representation Code (ID)
    - XON-10: Organization Identifier (ST)
    
    Examples:
    - "Hospital Name" (valid - basic organization name)
    - "Hospital Name^TYPE^12345^CHECK^SCHEME" (valid - extended)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "XON must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # XON can have up to 10 components
    if len(components) > 10:
        return False, f"XON has too many components (max 10, got {len(components)})"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_xtn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate XTN (Extended Telecommunication Number) composite data type.
    
    Format: [NNN] [(999)]999-9999[X99999][B99999][C any text]^Telecommunication Use Code^Telecommunication Equipment Type^Email Address^Country Code^Area/City Code^Phone Number^Extension^Any Text^Extension Prefix^Speed Dial Code^Unformatted Telephone Number
    
    Components (up to 13):
    - XTN-1: [NNN] [(999)]999-9999[X99999][B99999][C any text] (TN)
    - XTN-2: Telecommunication Use Code (ID)
    - XTN-3: Telecommunication Equipment Type (ID)
    - XTN-4: Email Address (ST)
    - XTN-5: Country Code (NM)
    - XTN-6: Area/City Code (NM)
    - XTN-7: Phone Number (NM)
    - XTN-8: Extension (NM)
    - XTN-9: Any Text (ST)
    - XTN-10: Extension Prefix (ST)
    - XTN-11: Speed Dial Code (ST)
    - XTN-12: Unformatted Telephone Number (ST)
    - XTN-13: Effective Start Date (TS)
    
    Examples:
    - "555-1234" (valid - basic phone, same as TN)
    - "555-1234^PRN^PH^email@example.com" (valid - extended)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "XTN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # XTN can have up to 13 components
    if len(components) > 13:
        return False, f"XTN has too many components (max 13, got {len(components)})"
    
    # If first component exists, validate as TN (telephone number)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_tn(components[0], component_separator=component_separator)
        if not is_valid:
            return False, f"XTN telephone number invalid: {error}"
    
    return True, None


def validate_mo(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate MO (Money) composite data type.
    
    Format: Quantity^Denomination
    
    Components:
    - MO-1: Quantity (NM)
    - MO-2: Denomination (ID)
    
    Examples:
    - "100.50^USD" (valid - US dollars)
    - "50.00^EUR" (valid - Euros)
    - "100.50" (valid - quantity only)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "MO must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # MO can have up to 2 components
    if len(components) > 2:
        return False, f"MO has too many components (max 2, got {len(components)})"
    
    # Validate quantity (MO-1) is numeric if present
    if len(components) >= 1 and components[0]:
        quantity_str = components[0].strip()
        try:
            float(quantity_str)
        except ValueError:
            return False, f"MO quantity '{quantity_str}' is not a valid number"
    
    return True, None


def validate_cx(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CX (Extended Composite ID with Check Digit) composite data type.
    
    Format: ID^Check Digit^Check Digit Scheme^Assigning Authority^Identifier Type Code^Assigning Facility^Effective Date^Expiration Date^Assigning Jurisdiction^Assigning Agency or Department^Security Check^Security Check Scheme^Identifier Type Code^Assigning Facility Identifier^Name Type Code^Identifier Check Digit^Check Digit Scheme Code^Identifier Type Code^Assigning Facility^Name Representation Code^Name Context^Name Validity Range^Name Assembly Order^Effective Date^Expiration Date^Professional Suffix^Assigning Jurisdiction^Assigning Agency or Department^Security Check^Security Check Scheme
    
    Components (up to 30):
    - CX-1: ID Number (ST)
    - CX-2: Check Digit (ST)
    - CX-3: Check Digit Scheme (ID)
    - CX-4: Assigning Authority (HD)
    - CX-5: Identifier Type Code (IS)
    - CX-6: Assigning Facility (HD)
    - CX-7: Effective Date (TS)
    - CX-8: Expiration Date (TS)
    - CX-9: Assigning Jurisdiction (CWE)
    - CX-10: Assigning Agency or Department (CWE)
    - CX-11: Security Check (ST)
    - CX-12: Security Check Scheme (ID)
    - And more...
    
    Examples:
    - "12345" (valid - basic ID)
    - "12345^CHECK^SCHEME^AUTH^TYPE" (valid - extended)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CX must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CX can have up to 30 components (varies by version)
    if len(components) > 30:
        return False, f"CX has too many components (max 30, got {len(components)})"
    
    # If CX-7 or CX-8 present, validate as TS (timestamp)
    if len(components) >= 7 and components[6]:
        is_valid, error = validate_ts(components[6])
        if not is_valid:
            return False, f"CX effective date invalid: {error}"
    
    if len(components) >= 8 and components[7]:
        is_valid, error = validate_ts(components[7])
        if not is_valid:
            return False, f"CX expiration date invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_fc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate FC (Financial Class) composite data type.
    
    Format: Financial Class Code^Effective Date
    
    Components:
    - FC-1: Financial Class Code (IS)
    - FC-2: Effective Date (TS)
    
    Examples:
    - "01" (valid - financial class code only)
    - "01^20240101" (valid - with effective date)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "FC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # FC can have up to 2 components
    if len(components) > 2:
        return False, f"FC has too many components (max 2, got {len(components)})"
    
    # If FC-2 present, validate as TS (timestamp)
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_ts(components[1])
        if not is_valid:
            return False, f"FC effective date invalid: {error}"
    
    return True, None


def validate_cf(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CF (Coded Element with Formatted Values) composite data type.
    
    Format: Identifier^Formatted Text^Name of Coding System^Alternate Identifier^Alternate Formatted Text^Name of Alternate Coding System
    
    Components (up to 6):
    - CF-1: Identifier (ST)
    - CF-2: Formatted Text (FT)
    - CF-3: Name of Coding System (ID)
    - CF-4: Alternate Identifier (ST)
    - CF-5: Alternate Formatted Text (FT)
    - CF-6: Name of Alternate Coding System (ID)
    
    Examples:
    - "CODE" (valid - identifier only)
    - "CODE^Formatted Text^SYSTEM" (valid - with formatted text and system)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CF must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CF can have up to 6 components
    if len(components) > 6:
        return False, f"CF has too many components (max 6, got {len(components)})"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_ck(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CK (Composite ID with Check Digit) composite data type.
    
    Format: ID Number^Check Digit^Check Digit Scheme^Assigning Authority
    
    Components (up to 4):
    - CK-1: ID Number (NM) - The identifier
    - CK-2: Check Digit (NM) - Check digit for validation
    - CK-3: Check Digit Scheme (ID) - Algorithm used (e.g., M10, M11, ISO)
    - CK-4: Assigning Authority (HD) - Organization that assigned the ID
    
    Examples:
    - "12345" (valid - ID number only)
    - "12345^7^M10" (valid - with check digit and scheme)
    - "12345^7^M10^FACILITY" (valid - with assigning authority)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CK must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # CK can have up to 4 components
    if len(components) > 4:
        return False, f"CK has too many components (max 4, got {len(components)})"
    
    # CK-1: ID Number (NM) - required if present
    if components[0]:
        is_valid, error = validate_nm(components[0])
        if not is_valid:
            return False, f"CK-1 (ID Number) validation failed: {error}"
    
    # CK-2: Check Digit (NM) - optional
    if len(components) > 1 and components[1]:
        is_valid, error = validate_nm(components[1])
        if not is_valid:
            return False, f"CK-2 (Check Digit) validation failed: {error}"
    
    # CK-3: Check Digit Scheme (ID) - optional
    # Common schemes: M10 (Mod 10), M11 (Mod 11), ISO, NPI
    if len(components) > 2 and components[2]:
        is_valid, error = validate_id(components[2])
        if not is_valid:
            return False, f"CK-3 (Check Digit Scheme) validation failed: {error}"
    
    # CK-4: Assigning Authority (HD) - optional
    if len(components) > 3 and components[3]:
        is_valid, error = validate_hd(components[3], component_separator)
        if not is_valid:
            return False, f"CK-4 (Assigning Authority) validation failed: {error}"
    
    return True, None


def validate_jcc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate JCC (Job Code/Class) composite data type.
    
    Format: Job Code^Job Class^Job Description
    
    Components (up to 3):
    - JCC-1: Job Code (CE)
    - JCC-2: Job Class (CE)
    - JCC-3: Job Description (ST)
    
    Examples:
    - "CODE" (valid - job code only)
    - "CODE^CLASS^Description" (valid - full job code/class)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "JCC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # JCC can have up to 3 components
    if len(components) > 3:
        return False, f"JCC has too many components (max 3, got {len(components)})"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_la1(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate LA1 (Location with Address Variation 1) composite data type.
    
    Format: Point of Care^Room^Bed^Facility^Location Status^Person Location Type^Building^Floor^Location Description
    
    Components (up to 9):
    - LA1-1: Point of Care (IS) - Point of care identifier
    - LA1-2: Room (IS) - Room identifier
    - LA1-3: Bed (IS) - Bed identifier
    - LA1-4: Facility (HD) - Facility identifier
    - LA1-5: Location Status (IS) - Status of location
    - LA1-6: Person Location Type (IS) - Type of person location
    - LA1-7: Building (IS) - Building identifier
    - LA1-8: Floor (IS) - Floor identifier
    - LA1-9: Location Description (ST) - Description of location
    
    Examples:
    - "ICU^101^A^HOSPITAL" (valid - ICU room 101 bed A)
    - "WARD^201^B^HOSPITAL^O^P^BLDG1^FLOOR2^Main Ward" (valid - full location)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "LA1 must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # LA1 can have up to 9 components
    if len(components) > 9:
        return False, f"LA1 has too many components (max 9, got {len(components)})"
    
    # LA1-1: Point of Care (IS) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_is(components[0])
        if not is_valid:
            return False, f"LA1-1 (Point of Care) validation failed: {error}"
    
    # LA1-2: Room (IS) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_is(components[1])
        if not is_valid:
            return False, f"LA1-2 (Room) validation failed: {error}"
    
    # LA1-3: Bed (IS) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_is(components[2])
        if not is_valid:
            return False, f"LA1-3 (Bed) validation failed: {error}"
    
    # LA1-4: Facility (HD) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_hd(components[3], component_separator)
        if not is_valid:
            return False, f"LA1-4 (Facility) validation failed: {error}"
    
    # LA1-5: Location Status (IS) - optional
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_is(components[4])
        if not is_valid:
            return False, f"LA1-5 (Location Status) validation failed: {error}"
    
    # LA1-6: Person Location Type (IS) - optional
    if len(components) >= 6 and components[5]:
        is_valid, error = validate_is(components[5])
        if not is_valid:
            return False, f"LA1-6 (Person Location Type) validation failed: {error}"
    
    # LA1-7: Building (IS) - optional
    if len(components) >= 7 and components[6]:
        is_valid, error = validate_is(components[6])
        if not is_valid:
            return False, f"LA1-7 (Building) validation failed: {error}"
    
    # LA1-8: Floor (IS) - optional
    if len(components) >= 8 and components[7]:
        is_valid, error = validate_is(components[7])
        if not is_valid:
            return False, f"LA1-8 (Floor) validation failed: {error}"
    
    # LA1-9: Location Description (ST) - optional
    if len(components) >= 9 and components[8]:
        is_valid, error = validate_st(components[8])
        if not is_valid:
            return False, f"LA1-9 (Location Description) validation failed: {error}"
    
    return True, None


def validate_ma(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate MA (Multiplexed Array) composite data type.
    
    Format: Sample Y From Channel 1^Sample Y From Channel 2^...^Sample Y From Channel N
    
    Components (variable, up to N channels):
    - MA-1: Sample Y From Channel 1 (NM) - First channel sample value
    - MA-2: Sample Y From Channel 2 (NM) - Second channel sample value
    - MA-N: Sample Y From Channel N (NM) - Nth channel sample value
    
    Note: MA is used for multiplexed arrays where multiple channels are sampled simultaneously.
    The number of components depends on the number of channels in the array.
    
    Examples:
    - "1.5^2.3^3.7" (valid - 3-channel array)
    - "10.0" (valid - single channel)
    - "0.5^1.2^2.8^4.1^5.9" (valid - 5-channel array)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "MA must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # MA can have variable number of components (typically 1-256 channels)
    # We'll allow up to 256 components for practical purposes
    if len(components) > 256:
        return False, f"MA has too many components (max 256 channels, got {len(components)})"
    
    # Each component should be a numeric value (NM)
    for i, component in enumerate(components, start=1):
        if component:  # Empty components are allowed
            is_valid, error = validate_nm(component)
            if not is_valid:
                return False, f"MA-{i} (Sample from Channel {i}) validation failed: {error}"
    
    return True, None


def validate_moc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate MOC (Money and Charge Code) composite data type.
    
    Format: Monetary Amount^Charge Code
    
    Components (up to 2):
    - MOC-1: Monetary Amount (MO)
    - MOC-2: Charge Code (CE)
    
    Examples:
    - "100.50^CODE" (valid - money and charge code)
    - "100.50" (valid - money only)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "MOC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # MOC can have up to 2 components
    if len(components) > 2:
        return False, f"MOC has too many components (max 2, got {len(components)})"
    
    # If MOC-1 present, validate as MO (Money)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_mo(components[0])
        if not is_valid:
            return False, f"MOC monetary amount invalid: {error}"
    
    return True, None


def validate_mop(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate MOP (Money or Percentage) composite data type.
    
    Format: Money or Percentage Indicator^Money or Percentage Quantity
    
    Components (up to 2):
    - MOP-1: Money or Percentage Indicator (ID)
    - MOP-2: Money or Percentage Quantity (NM)
    
    Examples:
    - "M^100.50" (valid - money amount)
    - "P^15.5" (valid - percentage)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "MOP must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # MOP can have up to 2 components
    if len(components) > 2:
        return False, f"MOP has too many components (max 2, got {len(components)})"
    
    # Validate indicator if present
    if len(components) >= 1 and components[0]:
        indicator = components[0].strip().upper()
        if indicator not in ("M", "P", "MO", "PER"):
            return False, f"MOP indicator must be M, P, MO, or PER, got '{indicator}'"
    
    # Validate quantity if present (must be numeric)
    if len(components) >= 2 and components[1]:
        try:
            float(components[1].strip())
        except ValueError:
            return False, f"MOP quantity '{components[1]}' is not a valid number"
    
    return True, None


def validate_qak(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QAK (Query Acknowledgment) composite data type.
    
    Format: Query Tag^Query Response Status^Message Query Name^Hit Count Total^This payload^Hits remaining
    
    Components (up to 6):
    - QAK-1: Query Tag (ST)
    - QAK-2: Query Response Status (ID)
    - QAK-3: Message Query Name (CE)
    - QAK-4: Hit Count Total (NM)
    - QAK-5: This payload (NM)
    - QAK-6: Hits remaining (NM)
    
    Examples:
    - "QUERY123^OK" (valid - query tag and status)
    - "QUERY123^OK^QBP^Q11^10^5^5" (valid - full query acknowledgment)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QAK must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QAK can have up to 6 components
    if len(components) > 6:
        return False, f"QAK has too many components (max 6, got {len(components)})"
    
    # Validate NM components if present (QAK-4, QAK-5, QAK-6)
    nm_indices = [3, 4, 5]  # 0-based indices for NM components
    component_names = ["Hit Count Total", "This payload", "Hits remaining"]
    
    for idx, name in zip(nm_indices, component_names):
        if len(components) > idx and components[idx]:
            try:
                float(components[idx].strip())
            except ValueError:
                return False, f"QAK {name} '{components[idx]}' is not a valid number"
    
    return True, None


def validate_qid(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QID (Query Identification) composite data type.
    
    Format: Query Tag^Message Query Name^Query Priority^Query ID
    
    Components (up to 4):
    - QID-1: Query Tag (ST)
    - QID-2: Message Query Name (CE)
    - QID-3: Query Priority (ID)
    - QID-4: Query ID (ST)
    
    Examples:
    - "QUERY123" (valid - query tag only)
    - "QUERY123^QBP^Q11" (valid - query tag and message query name)
    - "QUERY123^QBP^Q11^I^QUERY456" (valid - full query identification)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QID must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QID can have up to 4 components
    if len(components) > 4:
        return False, f"QID has too many components (max 4, got {len(components)})"
    
    # All components are basic types (ST, CE, ID, ST), so no additional validation needed
    # beyond component count
    
    return True, None


def validate_qpd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QPD (Query Parameter Definition) composite data type.
    
    Format: Message Query Name^Query Tag^Stored Procedure Name^Input Parameter List^Output Parameter List
    
    Components (up to 5):
    - QPD-1: Message Query Name (CE)
    - QPD-2: Query Tag (ST)
    - QPD-3: Stored Procedure Name (CE)
    - QPD-4: Input Parameter List (QIP)
    - QPD-5: Output Parameter List (QSC)
    
    Examples:
    - "QBP^Q11" (valid - message query name)
    - "QBP^Q11^QUERY123" (valid - with query tag)
    - "QBP^Q11^QUERY123^SP_NAME" (valid - with stored procedure name)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QPD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QPD can have up to 5 components
    if len(components) > 5:
        return False, f"QPD has too many components (max 5, got {len(components)})"
    
    # All components are basic types (CE, ST, CE, QIP, QSC), so no additional validation needed
    # beyond component count
    
    return True, None


def validate_qip(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QIP (Query Input Parameter List) composite data type.
    
    Format: Segment Field Name^Value1&Value2&Value3
    
    Components (up to 2):
    - QIP-1: Segment Field Name (ST)
    - QIP-2: Values (ST) - Multiple values separated by &
    
    Examples:
    - "PID.3" (valid - field name only)
    - "PID.3^12345&67890" (valid - field name with values)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QIP must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QIP can have up to 2 components
    if len(components) > 2:
        return False, f"QIP has too many components (max 2, got {len(components)})"
    
    # QIP-1 should be in format SEGMENT.FIELD (e.g., PID.3)
    if len(components) >= 1 and components[0]:
        field_name = components[0].strip()
        if "." in field_name:
            parts = field_name.split(".", 1)
            if len(parts) != 2 or not parts[0] or not parts[1]:
                return False, f"QIP segment field name '{field_name}' must be in format SEGMENT.FIELD"
    
    return True, None


def validate_qrd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QRD (Original-Style Query Definition) composite data type.
    
    Format: Query Date/Time^Query Format Code^Query Priority^Query ID^Deferred Response Type^Deferred Response Date/Time^Quantity Limited Request^Who Subject Filter^What Subject Filter^What Department Data Code^What Data Code Value Qual^Query Results Level^Where Subject Filter^When Data Start Date/Time^When Data End Date/Time^What User Qualifier^Other QRY Subject Filter^Which Date/Time Qualifier^Which Date/Time Status Qualifier^Date/Time Selection Qualifier^When Quantity/ timing Qualifier^Search Confidence Threshold^Alternate Format Code^Location/Equipment^Match Reason^Derived Fields^Delayed Response Type^Delayed Response Date/Time^Quantity Limited Request^Who Subject Filter^What Subject Filter^What Department Data Code^What Data Code Value Qual^Query Results Level^Where Subject Filter^When Data Start Date/Time^When Data End Date/Time^What User Qualifier^Other QRY Subject Filter^Which Date/Time Qualifier^Which Date/Time Status Qualifier^Date/Time Selection Qualifier^When Quantity/ timing Qualifier^Search Confidence Threshold^Alternate Format Code^Location/Equipment^Match Reason^Derived Fields
    
    Components (up to 20):
    - QRD-1: Query Date/Time (TS)
    - QRD-2: Query Format Code (ID)
    - QRD-3: Query Priority (ID)
    - QRD-4: Query ID (ST)
    - QRD-5: Deferred Response Type (ID)
    - QRD-6: Deferred Response Date/Time (TS)
    - QRD-7: Quantity Limited Request (CQ)
    - QRD-8: Who Subject Filter (XCN)
    - QRD-9: What Subject Filter (CE)
    - QRD-10: What Department Data Code (CE)
    - QRD-11: What Data Code Value Qual (VR)
    - QRD-12: Query Results Level (ID)
    - QRD-13: Where Subject Filter (ST)
    - QRD-14: When Data Start Date/Time (TS)
    - QRD-15: When Data End Date/Time (TS)
    - QRD-16: What User Qualifier (ST)
    - QRD-17: Other QRY Subject Filter (ST)
    - QRD-18: Which Date/Time Qualifier (ID)
    - QRD-19: Which Date/Time Status Qualifier (ID)
    - QRD-20: Date/Time Selection Qualifier (ID)
    
    Examples:
    - "20250101120000^R" (valid - query date/time and format code)
    - "20250101120000^R^I^QUERY123" (valid - with priority and query ID)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QRD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QRD can have up to 20 components
    if len(components) > 20:
        return False, f"QRD has too many components (max 20, got {len(components)})"
    
    # Validate TS components if present (QRD-1, QRD-6, QRD-14, QRD-15)
    ts_indices = [0, 5, 13, 14]  # 0-based indices for TS components
    component_names = ["Query Date/Time", "Deferred Response Date/Time", 
                      "When Data Start Date/Time", "When Data End Date/Time"]
    
    for idx, name in zip(ts_indices, component_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                return False, f"QRD {name} invalid: {error}"
    
    return True, None


def validate_qrf(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QRF (Original Style Query Filter) composite data type.
    
    Format: Where Subject Filter^When Data Start Date/Time^When Data End Date/Time^What User Qualifier^Other QRY Subject Filter^Which Date/Time Qualifier^Which Date/Time Status Qualifier
    
    Components (up to 7):
    - QRF-1: Where Subject Filter (ST)
    - QRF-2: When Data Start Date/Time (TS)
    - QRF-3: When Data End Date/Time (TS)
    - QRF-4: What User Qualifier (ST)
    - QRF-5: Other QRY Subject Filter (ST)
    - QRF-6: Which Date/Time Qualifier (ID)
    - QRF-7: Which Date/Time Status Qualifier (ID)
    
    Examples:
    - "LOCATION1" (valid - where subject filter only)
    - "LOCATION1^20250101120000^20251231120000" (valid - with date range)
    - "LOCATION1^20250101120000^20251231120000^USER1" (valid - with user qualifier)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QRF must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QRF can have up to 7 components
    if len(components) > 7:
        return False, f"QRF has too many components (max 7, got {len(components)})"
    
    # Validate TS components if present (QRF-2, QRF-3)
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_ts(components[1])
        if not is_valid:
            return False, f"QRF when data start date/time invalid: {error}"
    
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_ts(components[2])
        if not is_valid:
            return False, f"QRF when data end date/time invalid: {error}"
    
    return True, None


def validate_qri(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QRI (Query Response Instance) composite data type.
    
    Format: Candidate Confidence^Match Reason Code^Algorithm Descriptor
    
    Components (up to 3):
    - QRI-1: Candidate Confidence (NM)
    - QRI-2: Match Reason Code (CE)
    - QRI-3: Algorithm Descriptor (CE)
    
    Examples:
    - "0.95" (valid - candidate confidence only)
    - "0.95^MATCH^ALG1" (valid - full query response instance)
    - "0.95^MATCH" (valid - with match reason code)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QRI must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QRI can have up to 3 components
    if len(components) > 3:
        return False, f"QRI has too many components (max 3, got {len(components)})"
    
    # Validate NM component if present (QRI-1: Candidate Confidence)
    if len(components) >= 1 and components[0]:
        try:
            confidence = float(components[0].strip())
            # Candidate confidence is typically between 0 and 1
            if confidence < 0 or confidence > 1:
                return False, f"QRI candidate confidence '{confidence}' should be between 0 and 1"
        except ValueError:
            return False, f"QRI candidate confidence '{components[0]}' is not a valid number"
    
    return True, None


def validate_qsc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate QSC (Query Selection Criteria) composite data type.
    
    Format: Segment Field Name^Relational Operator^Value^Relational Conjunction
    
    Components (up to 4):
    - QSC-1: Segment Field Name (ST)
    - QSC-2: Relational Operator (ID)
    - QSC-3: Value (ST)
    - QSC-4: Relational Conjunction (ID)
    
    Examples:
    - "PID.3" (valid - field name only)
    - "PID.3^EQ^12345" (valid - field name, operator, value)
    - "PID.3^EQ^12345^AND" (valid - full query selection criteria)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "QSC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # QSC can have up to 4 components
    if len(components) > 4:
        return False, f"QSC has too many components (max 4, got {len(components)})"
    
    # QSC-1 should be in format SEGMENT.FIELD (e.g., PID.3)
    if len(components) >= 1 and components[0]:
        field_name = components[0].strip()
        if "." in field_name:
            parts = field_name.split(".", 1)
            if len(parts) != 2 or not parts[0] or not parts[1]:
                return False, f"QSC segment field name '{field_name}' must be in format SEGMENT.FIELD"
    
    # QSC-2: Common relational operators: EQ, NE, GT, LT, GE, LE, etc.
    # We'll allow any ID value but validate structure
    
    # QSC-4: Common relational conjunctions: AND, OR
    # We'll allow any ID value but validate structure
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rdf(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RDF (Table Row Definition) composite data type.
    
    Format: Number of Columns per Row^Column Description
    
    Components (up to 2):
    - RDF-1: Number of Columns per Row (NM)
    - RDF-2: Column Description (RDT)
    
    Examples:
    - "5" (valid - number of columns only)
    - "5^COL1^COL2^COL3" (valid - with column descriptions)
    
    Note: RDF-2 is of type RDT (Table Row Data), which itself is a repeating field.
    For validation purposes, we validate RDF-1 as numeric and check component count.
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RDF must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RDF has at least 1 component (RDF-1), and RDF-2 can contain multiple RDT values
    # For simplicity, we'll validate that RDF-1 is numeric
    if len(components) >= 1 and components[0]:
        try:
            num_cols = int(components[0].strip())
            if num_cols < 0:
                return False, f"RDF number of columns per row '{num_cols}' must be non-negative"
        except ValueError:
            return False, f"RDF number of columns per row '{components[0]}' is not a valid integer"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rcd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RCD (Row Column Definition) composite data type.
    
    Format: Segment Field Name^HL7 Data Type^Maximum Column Width^Column Description
    
    Components (up to 4):
    - RCD-1: Segment Field Name (ST) - Name of the field
    - RCD-2: HL7 Data Type (ID) - Data type of the field
    - RCD-3: Maximum Column Width (NM) - Maximum width of the column
    - RCD-4: Column Description (ST) - Description of the column
    
    Examples:
    - "PID.3" (valid - segment field name only)
    - "PID.3^CX^20" (valid - with data type and width)
    - "PID.3^CX^20^Patient Identifier" (valid - full RCD)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RCD must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 4:
        return False, f"RCD has too many components (max 4, got {len(components)})"
    
    # RCD-1: Segment Field Name (ST) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_st(components[0])
        if not is_valid:
            return False, f"RCD-1 (Segment Field Name) validation failed: {error}"
    
    # RCD-2: HL7 Data Type (ID) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_id(components[1])
        if not is_valid:
            return False, f"RCD-2 (HL7 Data Type) validation failed: {error}"
    
    # RCD-3: Maximum Column Width (NM) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_nm(components[2])
        if not is_valid:
            return False, f"RCD-3 (Maximum Column Width) validation failed: {error}"
    
    # RCD-4: Column Description (ST) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_st(components[3])
        if not is_valid:
            return False, f"RCD-4 (Column Description) validation failed: {error}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rdt(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RDT (Table Row Data) composite data type.
    
    Format: Column Value
    
    Components (1):
    - RDT-1: Column Value (varies)
    
    Note: RDT is a simple data type that contains a single column value.
    The value can be of any type (string, number, etc.) depending on the column definition.
    For validation purposes, we accept any non-empty string value.
    
    Examples:
    - "Value1" (valid - column value)
    - "123" (valid - numeric column value)
    - "" (valid - empty column value allowed)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^, not used for RDT)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not isinstance(value, str):
        return False, "RDT must be a string"
    
    # RDT is a simple type that accepts any string value
    # Empty values are allowed (represents empty cell)
    return True, None


def validate_rf1(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RF1 (Referral Information) composite data type.
    
    Format: Referral Status^Referral Priority^Referral Type^Referral Disposition^Referral Category^Originating Referral Identifier^Effective Date^Expiration Date^Process Date^Referral Reason^External Referral Identifier^Referral Documentation Completion Status
    
    Components (up to 12):
    - RF1-1: Referral Status (CE)
    - RF1-2: Referral Priority (CE)
    - RF1-3: Referral Type (CE)
    - RF1-4: Referral Disposition (CE)
    - RF1-5: Referral Category (CE)
    - RF1-6: Originating Referral Identifier (EI)
    - RF1-7: Effective Date (TS)
    - RF1-8: Expiration Date (TS)
    - RF1-9: Process Date (TS)
    - RF1-10: Referral Reason (CE)
    - RF1-11: External Referral Identifier (EI)
    - RF1-12: Referral Documentation Completion Status (CE)
    
    Examples:
    - "A" (valid - referral status only)
    - "A^H^SPEC^APPROVED" (valid - with priority and type)
    - "A^H^SPEC^APPROVED^OUT^REF123^20250101^20251231" (valid - with dates)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RF1 must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RF1 can have up to 12 components
    if len(components) > 12:
        return False, f"RF1 has too many components (max 12, got {len(components)})"
    
    # Validate TS components if present (RF1-7: Effective Date, RF1-8: Expiration Date, RF1-9: Process Date)
    for idx, ts_name in [(6, "Effective Date"), (7, "Expiration Date"), (8, "Process Date")]:
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                return False, f"RF1 {ts_name.lower()} invalid: {error}"
    
    # Validate EI components if present (RF1-6: Originating Referral Identifier, RF1-11: External Referral Identifier)
    for idx, ei_name in [(5, "Originating Referral Identifier"), (10, "External Referral Identifier")]:
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ei(components[idx])
            if not is_valid:
                return False, f"RF1 {ei_name.lower()} invalid: {error}"
    
    return True, None


def validate_rgs(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RGS (Resource Group) composite data type.
    
    Format: Set ID - RGS^Segment Action Code^Resource Group ID
    
    Components (up to 3):
    - RGS-1: Set ID - RGS (SI)
    - RGS-2: Segment Action Code (ID)
    - RGS-3: Resource Group ID (CE)
    
    Examples:
    - "1" (valid - set ID only)
    - "1^U^GROUP123" (valid - with action code and group ID)
    - "1^U" (valid - with action code)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RGS must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RGS can have up to 3 components
    if len(components) > 3:
        return False, f"RGS has too many components (max 3, got {len(components)})"
    
    # RGS-1 is Set ID (SI), which is a sequence ID - typically a positive integer
    # We'll validate it as a non-empty string (SI allows any string)
    # RGS-2 is Segment Action Code (ID), no specific validation needed
    # RGS-3 is Resource Group ID (CE), no specific validation needed
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rmi(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RMI (Risk Management Incident) composite data type.
    
    Format: Risk Management Incident Code^Date/Time Incident^Incident Code^Date/Time Incident Reported^Incident Reported By^Incident Reported To^Incident Location^Incident Classification Code^Incident Class Code^Incident Description^Incident Description Narrative^Incident Description From Patient Indicator^Patient Involvement Indicator^Incident Code Sequence Number^Incident Entry Date/Time^Incident Entry By^Incident Entry Location^Incident Entry Method Code^Incident Entry Method Description^Incident Entry Date/Time Reported^Incident Entry Reported By^Incident Entry Reported To^Incident Entry Reported Location^Incident Entry Reported Method Code^Incident Entry Reported Method Description^Incident Entry Reported Date/Time^Incident Entry Reported By^Incident Entry Reported To^Incident Entry Reported Location^Incident Entry Reported Method Code^Incident Entry Reported Method Description
    
    Components (up to 31):
    - RMI-1: Risk Management Incident Code (CE)
    - RMI-2: Date/Time Incident (TS)
    - RMI-3: Incident Code (CE)
    - RMI-4: Date/Time Incident Reported (TS)
    - RMI-5: Incident Reported By (XCN)
    - RMI-6: Incident Reported To (XCN)
    - RMI-7: Incident Location (ST)
    - RMI-8: Incident Classification Code (CE)
    - RMI-9: Incident Class Code (CE)
    - RMI-10: Incident Description (ST)
    - RMI-11: Incident Description Narrative (TX)
    - RMI-12: Incident Description From Patient Indicator (ID)
    - RMI-13: Patient Involvement Indicator (ID)
    - RMI-14: Incident Code Sequence Number (NM)
    - RMI-15: Incident Entry Date/Time (TS)
    - RMI-16: Incident Entry By (XCN)
    - RMI-17: Incident Entry Location (ST)
    - RMI-18: Incident Entry Method Code (CE)
    - RMI-19: Incident Entry Method Description (ST)
    - RMI-20: Incident Entry Date/Time Reported (TS)
    - RMI-21: Incident Entry Reported By (XCN)
    - RMI-22: Incident Entry Reported To (XCN)
    - RMI-23: Incident Entry Reported Location (ST)
    - RMI-24: Incident Entry Reported Method Code (CE)
    - RMI-25: Incident Entry Reported Method Description (ST)
    - RMI-26: Incident Entry Reported Date/Time (TS)
    - RMI-27: Incident Entry Reported By (XCN)
    - RMI-28: Incident Entry Reported To (XCN)
    - RMI-29: Incident Entry Reported Location (ST)
    - RMI-30: Incident Entry Reported Method Code (CE)
    - RMI-31: Incident Entry Reported Method Description (ST)
    
    Examples:
    - "CODE123" (valid - incident code only)
    - "CODE123^20250101120000" (valid - with date/time)
    - "CODE123^20250101120000^INCIDENT^20250101130000" (valid - with incident code and reported date/time)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RMI must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RMI can have up to 31 components
    if len(components) > 31:
        return False, f"RMI has too many components (max 31, got {len(components)})"
    
    # Validate TS components if present
    # RMI-2: Date/Time Incident, RMI-4: Date/Time Incident Reported, RMI-15: Incident Entry Date/Time,
    # RMI-20: Incident Entry Date/Time Reported, RMI-26: Incident Entry Reported Date/Time
    ts_indices = [1, 3, 14, 19, 25]
    ts_names = ["Date/Time Incident", "Date/Time Incident Reported", "Incident Entry Date/Time",
                "Incident Entry Date/Time Reported", "Incident Entry Reported Date/Time"]
    
    for idx, name in zip(ts_indices, ts_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                return False, f"RMI {name.lower()} invalid: {error}"
    
    # Validate NM component if present (RMI-14: Incident Code Sequence Number)
    if len(components) >= 14 and components[13]:
        is_valid, error = validate_nm(components[13])
        if not is_valid:
            return False, f"RMI incident code sequence number invalid: {error}"
    
    return True, None


def validate_rol(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate ROL (Role) composite data type.
    
    Format: Role Instance ID^Action Code^Role-ROL^Role Person^Role Begin Date/Time^Role End Date/Time^Role Duration^Role Action Reason^Provider Type^Organization Unit Type^Office/Home Address/Birthplace^Phone^Person Location^Status
    
    Components (up to 14):
    - ROL-1: Role Instance ID (EI)
    - ROL-2: Action Code (ID)
    - ROL-3: Role-ROL (CE)
    - ROL-4: Role Person (XCN)
    - ROL-5: Role Begin Date/Time (TS)
    - ROL-6: Role End Date/Time (TS)
    - ROL-7: Role Duration (CE)
    - ROL-8: Role Action Reason (CE)
    - ROL-9: Provider Type (CE)
    - ROL-10: Organization Unit Type (CE)
    - ROL-11: Office/Home Address/Birthplace (XAD)
    - ROL-12: Phone (XTN)
    - ROL-13: Person Location (PL)
    - ROL-14: Status (IS)
    
    Examples:
    - "INST123" (valid - role instance ID only)
    - "INST123^A^ATTENDING" (valid - with action code and role)
    - "INST123^A^ATTENDING^DOC123^20250101^20251231" (valid - with dates)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "ROL must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # ROL can have up to 14 components
    if len(components) > 14:
        return False, f"ROL has too many components (max 14, got {len(components)})"
    
    # Validate EI component if present (ROL-1: Role Instance ID)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ei(components[0])
        if not is_valid:
            return False, f"ROL role instance ID invalid: {error}"
    
    # Validate TS components if present (ROL-5: Role Begin Date/Time, ROL-6: Role End Date/Time)
    for idx, ts_name in [(4, "Role Begin Date/Time"), (5, "Role End Date/Time")]:
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                return False, f"ROL {ts_name.lower()} invalid: {error}"
    
    return True, None


def validate_rq1(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RQ1 (Requisition Detail-1) composite data type.
    
    Format: Anticipated Price^Manufacturer ID^Manufacturer's Catalog^Vendor ID^Vendor Catalog^Vendor Catalog Item Number^Primary Vendor Indicator
    
    Components (up to 7):
    - RQ1-1: Anticipated Price (MO)
    - RQ1-2: Manufacturer ID (CE)
    - RQ1-3: Manufacturer's Catalog (ST)
    - RQ1-4: Vendor ID (CE)
    - RQ1-5: Vendor Catalog (ST)
    - RQ1-6: Vendor Catalog Item Number (ST)
    - RQ1-7: Primary Vendor Indicator (ID)
    
    Examples:
    - "100.00^USD" (valid - anticipated price only)
    - "100.00^USD^MAN123^CATALOG" (valid - with manufacturer ID and catalog)
    - "100.00^USD^MAN123^CATALOG^VEND123^VCATALOG^ITEM123^Y" (valid - full requisition detail)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RQ1 must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RQ1 can have up to 7 components
    if len(components) > 7:
        return False, f"RQ1 has too many components (max 7, got {len(components)})"
    
    # Validate MO component if present (RQ1-1: Anticipated Price)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_mo(components[0])
        if not is_valid:
            return False, f"RQ1 anticipated price invalid: {error}"
    
    return True, None


def validate_rqd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RQD (Requisition Detail) composite data type.
    
    Format: Requisition Line Number^Item Code - Internal^Item Code - External^Hospital Item Code^Requisition Quantity^Requisition Cost^Requisition Item Size^Requisition Unit of Measure^Dept Cost Center^Item Natural Account Code^Deliver To ID^Date Needed
    
    Components (up to 12):
    - RQD-1: Requisition Line Number (SI)
    - RQD-2: Item Code - Internal (CE)
    - RQD-3: Item Code - External (CE)
    - RQD-4: Hospital Item Code (CE)
    - RQD-5: Requisition Quantity (NM)
    - RQD-6: Requisition Cost (MO)
    - RQD-7: Requisition Item Size (NM)
    - RQD-8: Requisition Unit of Measure (CE)
    - RQD-9: Dept Cost Center (IS)
    - RQD-10: Item Natural Account Code (IS)
    - RQD-11: Deliver To ID (XCN)
    - RQD-12: Date Needed (DT)
    
    Examples:
    - "1" (valid - requisition line number only)
    - "1^ITEM123^EXT123^HOSP123" (valid - with item codes)
    - "1^ITEM123^EXT123^HOSP123^10^100.00^USD" (valid - with quantity and cost)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RQD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RQD can have up to 12 components
    if len(components) > 12:
        return False, f"RQD has too many components (max 12, got {len(components)})"
    
    # Validate NM component if present (RQD-5: Requisition Quantity)
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_nm(components[4])
        if not is_valid:
            return False, f"RQD requisition quantity invalid: {error}"
    
    # Validate MO component if present (RQD-6: Requisition Cost)
    # MO is "Quantity^Denomination", so if we have components[5] and components[6],
    # we need to check if components[6] is part of MO (currency) or RQD-7 (item size)
    # We'll try to validate as MO first if both exist
    if len(components) >= 6 and components[5]:
        mo_value = components[5]
        # If we have a 7th component and it's not numeric, it might be the currency denomination
        if len(components) >= 7 and components[6] and not components[6].replace('.', '').replace('-', '').isdigit():
            # Try validating as MO with denomination
            mo_value = f"{components[5]}^{components[6]}"
            is_valid, error = validate_mo(mo_value)
            if is_valid:
                # It's valid MO, so components[6] is the denomination
                # RQD-7 (item size) would be at components[7] if present
                pass
            else:
                # Not valid MO, so components[5] alone might be MO, and components[6] is RQD-7
                mo_value = components[5]
                is_valid, error = validate_mo(mo_value)
        else:
            # Validate as MO (might be quantity only or full MO if already combined)
            is_valid, error = validate_mo(mo_value)
        
        if not is_valid:
            return False, f"RQD requisition cost invalid: {error}"
    
    # Validate NM component if present (RQD-7: Requisition Item Size)
    # Skip if components[6] was used as MO denomination
    item_size_idx = 6
    if len(components) >= 7 and components[5] and components[6] and not components[6].replace('.', '').replace('-', '').isdigit():
        # components[6] was used as MO denomination, so item size is at components[7]
        item_size_idx = 7
    
    if len(components) > item_size_idx and components[item_size_idx]:
        is_valid, error = validate_nm(components[item_size_idx])
        if not is_valid:
            return False, f"RQD requisition item size invalid: {error}"
    
    # Validate DT component if present (RQD-12: Date Needed)
    if len(components) >= 12 and components[11]:
        is_valid, error = validate_dt(components[11])
        if not is_valid:
            return False, f"RQD date needed invalid: {error}"
    
    return True, None


def validate_sac(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SAC (Specimen Container Detail) composite data type.
    
    Format: External Container Identifier^Container Identifier^Carrier Identifier^Position in Carrier^Tray Identifier - SAC^Position in Tray^Location^Container Height^Container Diameter^Barrier Delta Height^Bottom Delta Height^Container Height/Diameter/Delta Units^Container Volume^Available Specimen Volume^Initial Specimen Volume^Specimen Component^Dilution Factor^Treatment^Temperature^Hemolysis Index^Hemolysis Index Units^Lipemia Index^Lipemia Index Units^Icterus Index^Icterus Index Units^Fibrin Index^Fibrin Index Units^System Induced Contaminants^Drug Interference^Artificial Blood^Special Handling Code^Other Environmental Factors
    
    Components (up to 31):
    - SAC-1: External Container Identifier (EI)
    - SAC-2: Container Identifier (EI)
    - SAC-3: Carrier Identifier (EI)
    - SAC-4: Position in Carrier (NM)
    - SAC-5: Tray Identifier - SAC (EI)
    - SAC-6: Position in Tray (NM)
    - SAC-7: Location (CE)
    - SAC-8: Container Height (NM)
    - SAC-9: Container Diameter (NM)
    - SAC-10: Barrier Delta Height (NM)
    - SAC-11: Bottom Delta Height (NM)
    - SAC-12: Container Height/Diameter/Delta Units (CE)
    - SAC-13: Container Volume (NM)
    - SAC-14: Available Specimen Volume (NM)
    - SAC-15: Initial Specimen Volume (NM)
    - SAC-16: Specimen Component (CE)
    - SAC-17: Dilution Factor (SN)
    - SAC-18: Treatment (CE)
    - SAC-19: Temperature (SN)
    - SAC-20: Hemolysis Index (NM)
    - SAC-21: Hemolysis Index Units (CE)
    - SAC-22: Lipemia Index (NM)
    - SAC-23: Lipemia Index Units (CE)
    - SAC-24: Icterus Index (NM)
    - SAC-25: Icterus Index Units (CE)
    - SAC-26: Fibrin Index (NM)
    - SAC-27: Fibrin Index Units (CE)
    - SAC-28: System Induced Contaminants (CE)
    - SAC-29: Drug Interference (CE)
    - SAC-30: Artificial Blood (CE)
    - SAC-31: Special Handling Code (CE)
    - SAC-32: Other Environmental Factors (CE)
    
    Examples:
    - "EXT123" (valid - external container identifier only)
    - "EXT123^CONT123^CARRIER123" (valid - with container and carrier identifiers)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SAC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SAC can have up to 32 components
    if len(components) > 32:
        return False, f"SAC has too many components (max 32, got {len(components)})"
    
    # Validate EI components if present (SAC-1, SAC-2, SAC-3, SAC-5)
    ei_indices = [0, 1, 2, 4]
    ei_names = ["External Container Identifier", "Container Identifier", "Carrier Identifier", "Tray Identifier"]
    
    for idx, name in zip(ei_indices, ei_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ei(components[idx])
            if not is_valid:
                return False, f"SAC {name.lower()} invalid: {error}"
    
    # Validate NM components if present (multiple NM fields)
    nm_indices = [3, 5, 7, 8, 9, 10, 12, 13, 14, 19, 21, 23, 25]
    nm_names = ["Position in Carrier", "Position in Tray", "Container Height", "Container Diameter",
                "Barrier Delta Height", "Bottom Delta Height", "Container Volume", "Available Specimen Volume",
                "Initial Specimen Volume", "Hemolysis Index", "Lipemia Index", "Icterus Index", "Fibrin Index"]
    
    for idx, name in zip(nm_indices, nm_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_nm(components[idx])
            if not is_valid:
                return False, f"SAC {name.lower()} invalid: {error}"
    
    return True, None


def validate_scd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SCD (Anti-Microbial Cycle Data) composite data type.
    
    Format: Cycle Start Time^Cycle Count^Temp Max^Temp Min^Load Number^Condition Time^Sterilization Time^Sterilization Type^Sterilization Cycle^Sterilization Cycle Time^Ionization Chamber Period^Text^Oxygen Tension^Cycle Status^Ozone Concentration^Ozone Concentration Units^Ozone Generation Time^Ozone Generation Time Units
    
    Components (up to 17):
    - SCD-1: Cycle Start Time (TS)
    - SCD-2: Cycle Count (NM)
    - SCD-3: Temp Max (SN)
    - SCD-4: Temp Min (SN)
    - SCD-5: Load Number (NM)
    - SCD-6: Condition Time (SN)
    - SCD-7: Sterilization Time (SN)
    - SCD-8: Sterilization Type (CE)
    - SCD-9: Sterilization Cycle (CE)
    - SCD-10: Sterilization Cycle Time (CQ)
    - SCD-11: Ionization Chamber Period (NM)
    - SCD-12: Text (TX)
    - SCD-13: Cycle Status (CE)
    - SCD-14: Ozone Concentration (SN)
    - SCD-15: Ozone Concentration Units (CE)
    - SCD-16: Ozone Generation Time (CQ)
    - SCD-17: Ozone Generation Time Units (CE)
    
    Examples:
    - "20250101120000" (valid - cycle start time only)
    - "20250101120000^1^100^50" (valid - with cycle count and temperatures)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SCD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SCD can have up to 17 components
    if len(components) > 17:
        return False, f"SCD has too many components (max 17, got {len(components)})"
    
    # Validate TS component if present (SCD-1: Cycle Start Time)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ts(components[0])
        if not is_valid:
            return False, f"SCD cycle start time invalid: {error}"
    
    # Validate NM components if present (SCD-2: Cycle Count, SCD-5: Load Number, SCD-11: Ionization Chamber Period)
    nm_indices = [1, 4, 10]
    nm_names = ["Cycle Count", "Load Number", "Ionization Chamber Period"]
    
    for idx, name in zip(nm_indices, nm_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_nm(components[idx])
            if not is_valid:
                return False, f"SCD {name.lower()} invalid: {error}"
    
    return True, None


def validate_sch(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SCH (Schedule Information) composite data type.
    
    Format: Placer Appointment ID^Filler Appointment ID^Occurrence Number^Placer Group Number^Schedule ID^Event Reason^Appointment Reason^Appointment Type^Appointment Duration^Appointment Duration Units^Appointment Timing Quantity^Appointment Priority^Placer Contact Person^Placer Contact Phone Number^Placer Contact Address^Placer Contact Location^Filler Contact Person^Filler Contact Phone Number^Filler Contact Address^Filler Contact Location^Entered By Person^Entered By Phone Number^Entered By Location^Parent Placer Appointment ID^Parent Filler Appointment ID^Filler Status Code^Placer Order Number^Filler Order Number
    
    Components (up to 28):
    - SCH-1: Placer Appointment ID (EI)
    - SCH-2: Filler Appointment ID (EI)
    - SCH-3: Occurrence Number (NM)
    - SCH-4: Placer Group Number (EI)
    - SCH-5: Schedule ID (CE)
    - SCH-6: Event Reason (CE)
    - SCH-7: Appointment Reason (CE)
    - SCH-8: Appointment Type (CE)
    - SCH-9: Appointment Duration (NM)
    - SCH-10: Appointment Duration Units (CE)
    - SCH-11: Appointment Timing Quantity (TQ)
    - SCH-12: Appointment Priority (NM)
    - SCH-13: Placer Contact Person (XCN)
    - SCH-14: Placer Contact Phone Number (XTN)
    - SCH-15: Placer Contact Address (XAD)
    - SCH-16: Placer Contact Location (PL)
    - SCH-17: Filler Contact Person (XCN)
    - SCH-18: Filler Contact Phone Number (XTN)
    - SCH-19: Filler Contact Address (XAD)
    - SCH-20: Filler Contact Location (PL)
    - SCH-21: Entered By Person (XCN)
    - SCH-22: Entered By Phone Number (XTN)
    - SCH-23: Entered By Location (PL)
    - SCH-24: Parent Placer Appointment ID (EI)
    - SCH-25: Parent Filler Appointment ID (EI)
    - SCH-26: Filler Status Code (CE)
    - SCH-27: Placer Order Number (EI)
    - SCH-28: Filler Order Number (EI)
    
    Examples:
    - "PLACER123" (valid - placer appointment ID only)
    - "PLACER123^FILLER123^1" (valid - with filler ID and occurrence number)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SCH must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SCH can have up to 28 components
    if len(components) > 28:
        return False, f"SCH has too many components (max 28, got {len(components)})"
    
    # Validate EI components if present (multiple EI fields)
    ei_indices = [0, 1, 3, 23, 24, 26, 27]
    ei_names = ["Placer Appointment ID", "Filler Appointment ID", "Placer Group Number",
                "Parent Placer Appointment ID", "Parent Filler Appointment ID", "Placer Order Number", "Filler Order Number"]
    
    for idx, name in zip(ei_indices, ei_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ei(components[idx])
            if not is_valid:
                return False, f"SCH {name.lower()} invalid: {error}"
    
    # Validate NM components if present (SCH-3: Occurrence Number, SCH-9: Appointment Duration, SCH-12: Appointment Priority)
    nm_indices = [2, 8, 11]
    nm_names = ["Occurrence Number", "Appointment Duration", "Appointment Priority"]
    
    for idx, name in zip(nm_indices, nm_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_nm(components[idx])
            if not is_valid:
                return False, f"SCH {name.lower()} invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_scp(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SCP (Sterilization Cycle Data) composite data type.
    
    Format: Cycle Start Time^Cycle Count^Temp Max^Temp Min^Load Number^Condition Time^Sterilization Time^Sterilization Type^Sterilization Cycle^Sterilization Cycle Time^Ionization Chamber Period^Text^Oxygen Tension^Cycle Status^Ozone Concentration^Ozone Concentration Units^Ozone Generation Time^Ozone Generation Time Units
    
    Components (up to 17):
    - SCP-1: Cycle Start Time (TS)
    - SCP-2: Cycle Count (NM)
    - SCP-3: Temp Max (SN)
    - SCP-4: Temp Min (SN)
    - SCP-5: Load Number (NM)
    - SCP-6: Condition Time (SN)
    - SCP-7: Sterilization Time (SN)
    - SCP-8: Sterilization Type (CE)
    - SCP-9: Sterilization Cycle (CE)
    - SCP-10: Sterilization Cycle Time (CQ)
    - SCP-11: Ionization Chamber Period (NM)
    - SCP-12: Text (TX)
    - SCP-13: Cycle Status (CE)
    - SCP-14: Ozone Concentration (SN)
    - SCP-15: Ozone Concentration Units (CE)
    - SCP-16: Ozone Generation Time (CQ)
    - SCP-17: Ozone Generation Time Units (CE)
    
    Examples:
    - "20250101120000" (valid - cycle start time only)
    - "20250101120000^1^100^50" (valid - with cycle count and temperatures)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SCP must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SCP can have up to 17 components
    if len(components) > 17:
        return False, f"SCP has too many components (max 17, got {len(components)})"
    
    # Validate TS component if present (SCP-1: Cycle Start Time)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ts(components[0])
        if not is_valid:
            return False, f"SCP cycle start time invalid: {error}"
    
    # Validate NM components if present (SCP-2: Cycle Count, SCP-5: Load Number, SCP-11: Ionization Chamber Period)
    nm_indices = [1, 4, 10]
    nm_names = ["Cycle Count", "Load Number", "Ionization Chamber Period"]
    
    for idx, name in zip(nm_indices, nm_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_nm(components[idx])
            if not is_valid:
                return False, f"SCP {name.lower()} invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_sdd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SDD (Sterilization Device Data) composite data type.
    
    Format: Lot Number^Device Number^Device Name^Device Data State^Load Status^Load ID
    
    Components (up to 6):
    - SDD-1: Lot Number (ST)
    - SDD-2: Device Number (EI)
    - SDD-3: Device Name (ST)
    - SDD-4: Device Data State (CE)
    - SDD-5: Load Status (CE)
    - SDD-6: Load ID (EI)
    
    Examples:
    - "LOT123" (valid - lot number only)
    - "LOT123^DEV123^DeviceName" (valid - with device number and name)
    - "LOT123^DEV123^DeviceName^STATE^STATUS^LOAD123" (valid - full sterilization device data)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SDD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SDD can have up to 6 components
    if len(components) > 6:
        return False, f"SDD has too many components (max 6, got {len(components)})"
    
    # Validate EI components if present (SDD-2: Device Number, SDD-6: Load ID)
    ei_indices = [1, 5]
    ei_names = ["Device Number", "Load ID"]
    
    for idx, name in zip(ei_indices, ei_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ei(components[idx])
            if not is_valid:
                return False, f"SDD {name.lower()} invalid: {error}"
    
    return True, None


def validate_sid(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SID (Substance Identifier) composite data type.
    
    Format: Substance Identifier^Substance Status^Substance Type^Substance Code^Substance Amount^Substance Units^Substance Notes^Substance Manufacturer^Substance Lot Number^Substance Expiration Date^Substance Expiration Time^Substance Expiration Date/Time^Substance Expiration Date/Time Offset^Substance Expiration Date/Time Offset Units^Substance Expiration Date/Time Offset Direction^Substance Expiration Date/Time Offset Value^Substance Expiration Date/Time Offset Value Units^Substance Expiration Date/Time Offset Value Direction^Substance Expiration Date/Time Offset Value Direction Units^Substance Expiration Date/Time Offset Value Direction Value^Substance Expiration Date/Time Offset Value Direction Value Units^Substance Expiration Date/Time Offset Value Direction Value Direction^Substance Expiration Date/Time Offset Value Direction Value Direction Units^Substance Expiration Date/Time Offset Value Direction Value Direction Value^Substance Expiration Date/Time Offset Value Direction Value Direction Value Units^Substance Expiration Date/Time Offset Value Direction Value Direction Value Direction^Substance Expiration Date/Time Offset Value Direction Value Direction Value Direction Units^Substance Expiration Date/Time Offset Value Direction Value Direction Value Direction Value^Substance Expiration Date/Time Offset Value Direction Value Direction Value Direction Value Units^Substance Expiration Date/Time Offset Value Direction Value Direction Value Direction Value Direction
    
    Components (up to 30):
    - SID-1: Substance Identifier (CE)
    - SID-2: Substance Status (CE)
    - SID-3: Substance Type (CE)
    - SID-4: Substance Code (CE)
    - SID-5: Substance Amount (CQ)
    - SID-6: Substance Units (CE)
    - SID-7: Substance Notes (TX)
    - SID-8: Substance Manufacturer (XON)
    - SID-9: Substance Lot Number (ST)
    - SID-10: Substance Expiration Date (DT)
    - SID-11: Substance Expiration Time (TM)
    - SID-12: Substance Expiration Date/Time (TS)
    - SID-13 through SID-30: Additional expiration date/time offset fields (various types)
    
    Examples:
    - "SUB123" (valid - substance identifier only)
    - "SUB123^ACTIVE^DRUG^CODE123" (valid - with status, type, and code)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SID must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SID can have up to 30 components
    if len(components) > 30:
        return False, f"SID has too many components (max 30, got {len(components)})"
    
    # Validate DT component if present (SID-10: Substance Expiration Date)
    if len(components) >= 10 and components[9]:
        is_valid, error = validate_dt(components[9])
        if not is_valid:
            return False, f"SID substance expiration date invalid: {error}"
    
    # Validate TM component if present (SID-11: Substance Expiration Time)
    if len(components) >= 11 and components[10]:
        is_valid, error = validate_tm(components[10])
        if not is_valid:
            return False, f"SID substance expiration time invalid: {error}"
    
    # Validate TS component if present (SID-12: Substance Expiration Date/Time)
    if len(components) >= 12 and components[11]:
        is_valid, error = validate_ts(components[11])
        if not is_valid:
            return False, f"SID substance expiration date/time invalid: {error}"
    
    return True, None


def validate_slt(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SLT (Sterilization Lot) composite data type.
    
    Format: Device Number^Device Name^Lot Number^Item Identifier^Bar Code^Device Type^Manufacturer Name^Manufacturer Address^Manufacturer ID^Manufacturer Catalog Number^Manufacturer Labeler Identification Code^Device Serial Number^Device Manufacture Date^Device Expiration Date^Device Implant Flag^Device Implant Date^Device Tracking Number^Device Tracking ID^Device Tracking ID Type^Device Tracking ID Format^Device Tracking ID Format Description^Device Tracking ID Format Description Code^Device Tracking ID Format Description Code System^Device Tracking ID Format Description Code System Version^Device Tracking ID Format Description Code System Name^Device Tracking ID Format Description Display Name^Device Tracking ID Format Description Original Text^Device Tracking ID Format Description Translation^Device Tracking ID Format Description Translation Language^Device Tracking ID Format Description Translation Code System^Device Tracking ID Format Description Translation Code System Version^Device Tracking ID Format Description Translation Code System Name^Device Tracking ID Format Description Translation Display Name^Device Tracking ID Format Description Translation Original Text
    
    Components (up to 34):
    - SLT-1: Device Number (EI)
    - SLT-2: Device Name (ST)
    - SLT-3: Lot Number (ST)
    - SLT-4: Item Identifier (EI)
    - SLT-5: Bar Code (ST)
    - SLT-6: Device Type (CE)
    - SLT-7: Manufacturer Name (XON)
    - SLT-8: Manufacturer Address (XAD)
    - SLT-9: Manufacturer ID (CE)
    - SLT-10: Manufacturer Catalog Number (ST)
    - SLT-11: Manufacturer Labeler Identification Code (CE)
    - SLT-12: Device Serial Number (ST)
    - SLT-13: Device Manufacture Date (DT)
    - SLT-14: Device Expiration Date (DT)
    - SLT-15: Device Implant Flag (ID)
    - SLT-16: Device Implant Date (DT)
    - SLT-17 through SLT-34: Device tracking ID fields (various types)
    
    Examples:
    - "DEV123" (valid - device number only)
    - "DEV123^DeviceName^LOT123" (valid - with device name and lot number)
    - "DEV123^DeviceName^LOT123^ITEM123^BARCODE^TYPE^MANUF^ADDR^MANUFID^CAT123^LABEL123^SERIAL123^20250101^20260101" (valid - with dates)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SLT must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SLT can have up to 34 components
    if len(components) > 34:
        return False, f"SLT has too many components (max 34, got {len(components)})"
    
    # Validate EI components if present (SLT-1: Device Number, SLT-4: Item Identifier)
    ei_indices = [0, 3]
    ei_names = ["Device Number", "Item Identifier"]
    
    for idx, name in zip(ei_indices, ei_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ei(components[idx])
            if not is_valid:
                return False, f"SLT {name.lower()} invalid: {error}"
    
    # Validate DT components if present (SLT-13: Device Manufacture Date, SLT-14: Device Expiration Date, SLT-16: Device Implant Date)
    dt_indices = [12, 13, 15]
    dt_names = ["Device Manufacture Date", "Device Expiration Date", "Device Implant Date"]
    
    for idx, name in zip(dt_indices, dt_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_dt(components[idx])
            if not is_valid:
                return False, f"SLT {name.lower()} invalid: {error}"
    
    return True, None


def validate_spm(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SPM (Specimen) composite data type.
    
    Format: Specimen ID^Specimen Parent IDs^Specimen Type^Specimen Type Modifier^Specimen Additives^Specimen Collection Method^Specimen Source Site^Specimen Source Site Modifier^Specimen Collection Site^Specimen Role^Specimen Collection Amount^Grouped Specimen Count^Specimen Description^Specimen Handling Code^Specimen Risk Code^Specimen Collection Date/Time^Specimen Received Date/Time^Specimen Expiration Date/Time^Specimen Availability^Specimen Reject Reason^Specimen Quality^Specimen Appropriateness^Specimen Condition^Specimen Current Quantity^Number of Specimen Containers^Container Type^Container Condition^Specimen Child Role
    
    Components (up to 28):
    - SPM-1: Specimen ID (EI)
    - SPM-2: Specimen Parent IDs (EI)
    - SPM-3: Specimen Type (CE)
    - SPM-4: Specimen Type Modifier (CE)
    - SPM-5: Specimen Additives (CE)
    - SPM-6: Specimen Collection Method (CE)
    - SPM-7: Specimen Source Site (CE)
    - SPM-8: Specimen Source Site Modifier (CE)
    - SPM-9: Specimen Collection Site (CE)
    - SPM-10: Specimen Role (CE)
    - SPM-11: Specimen Collection Amount (CQ)
    - SPM-12: Grouped Specimen Count (NM)
    - SPM-13: Specimen Description (TX)
    - SPM-14: Specimen Handling Code (CE)
    - SPM-15: Specimen Risk Code (CE)
    - SPM-16: Specimen Collection Date/Time (TS)
    - SPM-17: Specimen Received Date/Time (TS)
    - SPM-18: Specimen Expiration Date/Time (TS)
    - SPM-19: Specimen Availability (ID)
    - SPM-20: Specimen Reject Reason (CE)
    - SPM-21: Specimen Quality (CE)
    - SPM-22: Specimen Appropriateness (CE)
    - SPM-23: Specimen Condition (CE)
    - SPM-24: Specimen Current Quantity (CQ)
    - SPM-25: Number of Specimen Containers (NM)
    - SPM-26: Container Type (CE)
    - SPM-27: Container Condition (CE)
    - SPM-28: Specimen Child Role (CE)
    
    Examples:
    - "SP123" (valid - specimen ID only)
    - "SP123^PARENT123^BLOOD^MODIFIER" (valid - with parent IDs, type, and modifier)
    - "SP123^^BLOOD^^^METHOD^SITE^MODIFIER^COLLECTIONSITE^ROLE" (valid - with collection details)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SPM must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SPM can have up to 28 components
    if len(components) > 28:
        return False, f"SPM has too many components (max 28, got {len(components)})"
    
    # Validate EI components if present (SPM-1: Specimen ID, SPM-2: Specimen Parent IDs)
    ei_indices = [0, 1]
    ei_names = ["Specimen ID", "Specimen Parent IDs"]
    
    for idx, name in zip(ei_indices, ei_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ei(components[idx])
            if not is_valid:
                return False, f"SPM {name.lower()} invalid: {error}"
    
    # Validate TS components if present (SPM-16: Specimen Collection Date/Time, SPM-17: Specimen Received Date/Time, SPM-18: Specimen Expiration Date/Time)
    ts_indices = [15, 16, 17]
    ts_names = ["Specimen Collection Date/Time", "Specimen Received Date/Time", "Specimen Expiration Date/Time"]
    
    for idx, name in zip(ts_indices, ts_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                return False, f"SPM {name.lower()} invalid: {error}"
    
    # Validate NM components if present (SPM-12: Grouped Specimen Count, SPM-25: Number of Specimen Containers)
    nm_indices = [11, 24]
    nm_names = ["Grouped Specimen Count", "Number of Specimen Containers"]
    
    for idx, name in zip(nm_indices, nm_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_nm(components[idx])
            if not is_valid:
                return False, f"SPM {name.lower()} invalid: {error}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_spr(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SPR (Stored Procedure Request Definition) composite data type.
    
    Format: Query Name^Query ID^Query ID Type^Query Format^Query Response Format^Stored Procedure Name^Input Parameter List^Output Parameter List^Restriction^Selection Criteria^Selection Qualifier^Selection Qualifier Value^Selection Qualifier Value Type^Selection Qualifier Value Type Code^Selection Qualifier Value Type Code System^Selection Qualifier Value Type Code System Version^Selection Qualifier Value Type Code System Name^Selection Qualifier Value Type Display Name^Selection Qualifier Value Type Original Text^Selection Qualifier Value Type Translation^Selection Qualifier Value Type Translation Language^Selection Qualifier Value Type Translation Code System^Selection Qualifier Value Type Translation Code System Version^Selection Qualifier Value Type Translation Code System Name^Selection Qualifier Value Type Translation Display Name^Selection Qualifier Value Type Translation Original Text
    
    Components (up to 26):
    - SPR-1: Query Name (ST)
    - SPR-2: Query ID (ST)
    - SPR-3: Query ID Type (ID)
    - SPR-4: Query Format (ID)
    - SPR-5: Query Response Format (ID)
    - SPR-6: Stored Procedure Name (CE)
    - SPR-7: Input Parameter List (QIP)
    - SPR-8: Output Parameter List (QIP)
    - SPR-9: Restriction (QSC)
    - SPR-10: Selection Criteria (QSC)
    - SPR-11: Selection Qualifier (ST)
    - SPR-12: Selection Qualifier Value (ST)
    - SPR-13 through SPR-26: Selection Qualifier Value Type fields (various types)
    
    Examples:
    - "QUERY123" (valid - query name only)
    - "QUERY123^ID123^TYPE^FORMAT^RESPONSE^PROCEDURE" (valid - with query details)
    - "QUERY123^ID123^TYPE^FORMAT^RESPONSE^PROCEDURE^INPUT^OUTPUT^RESTRICTION^CRITERIA" (valid - with parameters and criteria)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SPR must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SPR can have up to 26 components
    if len(components) > 26:
        return False, f"SPR has too many components (max 26, got {len(components)})"
    
    # Validate QIP components if present (SPR-7: Input Parameter List, SPR-8: Output Parameter List)
    qip_indices = [6, 7]
    qip_names = ["Input Parameter List", "Output Parameter List"]
    
    for idx, name in zip(qip_indices, qip_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_qip(components[idx])
            if not is_valid:
                return False, f"SPR {name.lower()} invalid: {error}"
    
    # Validate QSC components if present (SPR-9: Restriction, SPR-10: Selection Criteria)
    qsc_indices = [8, 9]
    qsc_names = ["Restriction", "Selection Criteria"]
    
    for idx, name in zip(qsc_indices, qsc_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_qsc(components[idx])
            if not is_valid:
                return False, f"SPR {name.lower()} invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_stf(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate STF (Staff Identification) composite data type.
    
    Format: Primary Key Value^Staff ID Code^Staff Name^Staff Type^Administrative Sex^Date/Time of Birth^Active/Inactive Flag^Department^Hospital Service^Phone^Office/Home Address^Institution Activation Date^Institution Inactivation Date^Backup Person ID^E-mail Address^Preferred Method of Contact^Marital Status^Job Title^Job Code/Class^Employment Status^Additional Insured on Auto^Driver's License Number^Copy Auto Ins^Auto Ins Expires^Date Last DMV Review^Date Next DMV Review^Race^Ethnicity^Citizenship^Contact Reason^Contact Person's Name^Contact Person's Telephone Number^Contact Person's Address^Next of Kin/Associated Party's Identifiers^Job Status^Living Arrangement^Publicity Code^Protection Indicator^Student Indicator^Religion^Mother's Maiden Name^Nationality^Ethnic Group^Contact Person's Relationship^Patient Relationship^Job Title Code^Job Status Code^Living Dependency^Ambulatory Status^Citizenship Status^Primary Language^Living Arrangement Code^Publicity Code^Protection Indicator Code^Student Indicator Code^Religion Code^Mother's Maiden Name Code^Nationality Code^Ethnic Group Code^Contact Person's Relationship Code^Patient Relationship Code^Job Title Code^Job Status Code^Living Dependency Code^Ambulatory Status Code^Citizenship Status Code^Primary Language Code
    
    Components (up to 60):
    - STF-1: Primary Key Value (CE)
    - STF-2: Staff ID Code (CX)
    - STF-3: Staff Name (XPN)
    - STF-4: Staff Type (IS)
    - STF-5: Administrative Sex (IS)
    - STF-6: Date/Time of Birth (TS)
    - STF-7: Active/Inactive Flag (ID)
    - STF-8: Department (CE)
    - STF-9: Hospital Service (CE)
    - STF-10: Phone (XTN)
    - STF-11: Office/Home Address (XAD)
    - STF-12: Institution Activation Date (DT)
    - STF-13: Institution Inactivation Date (DT)
    - STF-14: Backup Person ID (CE)
    - STF-15: E-mail Address (ST)
    - STF-16: Preferred Method of Contact (CE)
    - STF-17: Marital Status (IS)
    - STF-18: Job Title (ST)
    - STF-19: Job Code/Class (JCC)
    - STF-20: Employment Status (IS)
    - STF-21 through STF-60: Additional fields (various types)
    
    Examples:
    - "KEY123" (valid - primary key value only)
    - "KEY123^ID123^LastName^FirstName^MiddleName^Suffix^Prefix^Type^Degree^Type^Source^Assigning^Authority" (valid - with staff ID and name)
    - "KEY123^ID123^Name^TYPE^M^20200101" (valid - with basic staff information)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "STF must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # STF can have up to 60 components
    if len(components) > 60:
        return False, f"STF has too many components (max 60, got {len(components)})"
    
    # Validate TS component if present (STF-6: Date/Time of Birth)
    if len(components) >= 6 and components[5]:
        is_valid, error = validate_ts(components[5])
        if not is_valid:
            return False, f"STF date/time of birth invalid: {error}"
    
    # Validate DT components if present (STF-12: Institution Activation Date, STF-13: Institution Inactivation Date)
    dt_indices = [11, 12]
    dt_names = ["Institution Activation Date", "Institution Inactivation Date"]
    
    for idx, name in zip(dt_indices, dt_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_dt(components[idx])
            if not is_valid:
                return False, f"STF {name.lower()} invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_tcc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate TCC (Test Code Configuration) composite data type.
    
    Format: Universal Service Identifier^Universal Service Type^Universal Service Subtype^Universal Service Priority^Universal Service Date/Time Range^Universal Service Amount^Universal Service Amount Units^Universal Service Interval^Universal Service Interval Units^Universal Service Interval Count^Universal Service Interval Sequence^Universal Service Interval Sequence Code^Universal Service Interval Sequence Code System^Universal Service Interval Sequence Code System Version^Universal Service Interval Sequence Code System Name^Universal Service Interval Sequence Display Name^Universal Service Interval Sequence Original Text^Universal Service Interval Sequence Translation^Universal Service Interval Sequence Translation Language^Universal Service Interval Sequence Translation Code System^Universal Service Interval Sequence Translation Code System Version^Universal Service Interval Sequence Translation Code System Name^Universal Service Interval Sequence Translation Display Name^Universal Service Interval Sequence Translation Original Text
    
    Components (up to 24):
    - TCC-1: Universal Service Identifier (CE)
    - TCC-2: Universal Service Type (ID)
    - TCC-3: Universal Service Subtype (ID)
    - TCC-4: Universal Service Priority (ID)
    - TCC-5: Universal Service Date/Time Range (DR)
    - TCC-6: Universal Service Amount (NM)
    - TCC-7: Universal Service Amount Units (CE)
    - TCC-8: Universal Service Interval (RI)
    - TCC-9: Universal Service Interval Units (CE)
    - TCC-10: Universal Service Interval Count (NM)
    - TCC-11: Universal Service Interval Sequence (IS)
    - TCC-12 through TCC-24: Universal Service Interval Sequence fields (various types)
    
    Examples:
    - "TEST123" (valid - universal service identifier only)
    - "TEST123^TYPE^SUBTYPE^PRIORITY" (valid - with type, subtype, and priority)
    - "TEST123^TYPE^SUBTYPE^PRIORITY^20200101-20201231^100^UNITS^INTERVAL^INTERVALUNITS^5^SEQUENCE" (valid - with date range, amount, and interval)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "TCC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # TCC can have up to 24 components
    if len(components) > 24:
        return False, f"TCC has too many components (max 24, got {len(components)})"
    
    # Validate DR component if present (TCC-5: Universal Service Date/Time Range)
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_dr(components[4])
        if not is_valid:
            return False, f"TCC universal service date/time range invalid: {error}"
    
    # Validate NM components if present (TCC-6: Universal Service Amount, TCC-10: Universal Service Interval Count)
    nm_indices = [5, 9]
    nm_names = ["Universal Service Amount", "Universal Service Interval Count"]
    
    for idx, name in zip(nm_indices, nm_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_nm(components[idx])
            if not is_valid:
                return False, f"TCC {name.lower()} invalid: {error}"
    
    # Validate RI component if present (TCC-8: Universal Service Interval)
    if len(components) >= 9 and components[7]:
        is_valid, error = validate_ri(components[7])
        if not is_valid:
            return False, f"TCC universal service interval invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_tcd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate TCD (Test Code Detail) composite data type.
    
    Format: Universal Service Identifier^Auto-Dilution Factor^Rerun Dilution Factor^Pre-Dilution Factor^Endogenous Content of Pre-Dilution Diluent^Automatic Repeat Allowed^Automatic Reflex Allowed^Automatic Order Cancellation Allowed^Automatic Order Cancellation Reason^Specimen Handling Requirements^Order Priority^Order Frequency^Order Frequency Units^Order Frequency Interval^Order Frequency Interval Units^Order Frequency Interval Count^Order Frequency Interval Sequence^Order Frequency Interval Sequence Code^Order Frequency Interval Sequence Code System^Order Frequency Interval Sequence Code System Version^Order Frequency Interval Sequence Code System Name^Order Frequency Interval Sequence Display Name^Order Frequency Interval Sequence Original Text^Order Frequency Interval Sequence Translation^Order Frequency Interval Sequence Translation Language^Order Frequency Interval Sequence Translation Code System^Order Frequency Interval Sequence Translation Code System Version^Order Frequency Interval Sequence Translation Code System Name^Order Frequency Interval Sequence Translation Display Name^Order Frequency Interval Sequence Translation Original Text
    
    Components (up to 30):
    - TCD-1: Universal Service Identifier (CE)
    - TCD-2: Auto-Dilution Factor (SN)
    - TCD-3: Rerun Dilution Factor (SN)
    - TCD-4: Pre-Dilution Factor (SN)
    - TCD-5: Endogenous Content of Pre-Dilution Diluent (SN)
    - TCD-6: Automatic Repeat Allowed (ID)
    - TCD-7: Automatic Reflex Allowed (ID)
    - TCD-8: Automatic Order Cancellation Allowed (ID)
    - TCD-9: Automatic Order Cancellation Reason (CE)
    - TCD-10: Specimen Handling Requirements (TX)
    - TCD-11: Order Priority (ID)
    - TCD-12: Order Frequency (ID)
    - TCD-13: Order Frequency Units (CE)
    - TCD-14: Order Frequency Interval (RI)
    - TCD-15: Order Frequency Interval Units (CE)
    - TCD-16: Order Frequency Interval Count (NM)
    - TCD-17: Order Frequency Interval Sequence (IS)
    - TCD-18 through TCD-30: Order Frequency Interval Sequence fields (various types)
    
    Examples:
    - "TEST123" (valid - universal service identifier only)
    - "TEST123^1.5^2.0^0.5^0.1" (valid - with dilution factors)
    - "TEST123^1.5^2.0^0.5^0.1^Y^N^N^REASON^REQUIREMENTS^PRIORITY^FREQ^UNITS^INTERVAL^INTERVALUNITS^5^SEQUENCE" (valid - with order frequency details)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "TCD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # TCD can have up to 30 components
    if len(components) > 30:
        return False, f"TCD has too many components (max 30, got {len(components)})"
    
    # Validate SN components if present (TCD-2: Auto-Dilution Factor, TCD-3: Rerun Dilution Factor, TCD-4: Pre-Dilution Factor, TCD-5: Endogenous Content)
    sn_indices = [1, 2, 3, 4]
    sn_names = ["Auto-Dilution Factor", "Rerun Dilution Factor", "Pre-Dilution Factor", "Endogenous Content of Pre-Dilution Diluent"]
    
    for idx, name in zip(sn_indices, sn_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_sn(components[idx])
            if not is_valid:
                return False, f"TCD {name.lower()} invalid: {error}"
    
    # Validate RI component if present (TCD-14: Order Frequency Interval)
    if len(components) >= 15 and components[13]:
        is_valid, error = validate_ri(components[13])
        if not is_valid:
            return False, f"TCD order frequency interval invalid: {error}"
    
    # Validate NM component if present (TCD-16: Order Frequency Interval Count)
    if len(components) >= 17 and components[15]:
        is_valid, error = validate_nm(components[15])
        if not is_valid:
            return False, f"TCD order frequency interval count invalid: {error}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_uac(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate UAC (User Authentication Credential) composite data type.
    
    Format: User Authentication Credential Type Code^User Authentication Credential^User Authentication Credential Expiration Date/Time^User Authentication Credential Expiration Date/Time Offset^User Authentication Credential Expiration Date/Time Offset Units^User Authentication Credential Expiration Date/Time Offset Value^User Authentication Credential Expiration Date/Time Offset Value Units^User Authentication Credential Expiration Date/Time Offset Value Direction^User Authentication Credential Expiration Date/Time Offset Value Direction Units^User Authentication Credential Expiration Date/Time Offset Value Direction Value^User Authentication Credential Expiration Date/Time Offset Value Direction Value Units^User Authentication Credential Expiration Date/Time Offset Value Direction Value Direction^User Authentication Credential Expiration Date/Time Offset Value Direction Value Direction Units^User Authentication Credential Expiration Date/Time Offset Value Direction Value Direction Value^User Authentication Credential Expiration Date/Time Offset Value Direction Value Direction Value Units^User Authentication Credential Expiration Date/Time Offset Value Direction Value Direction Value Direction
    
    Components (up to 16):
    - UAC-1: User Authentication Credential Type Code (CE)
    - UAC-2: User Authentication Credential (ED)
    - UAC-3: User Authentication Credential Expiration Date/Time (TS)
    - UAC-4 through UAC-16: User Authentication Credential Expiration Date/Time Offset fields (various types)
    
    Examples:
    - "PASSWORD" (valid - credential type code only)
    - "PASSWORD^CREDENTIAL123" (valid - with credential)
    - "PASSWORD^CREDENTIAL123^20250101120000" (valid - with expiration date/time)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "UAC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # UAC can have up to 16 components
    if len(components) > 16:
        return False, f"UAC has too many components (max 16, got {len(components)})"
    
    # Validate TS component if present (UAC-3: User Authentication Credential Expiration Date/Time)
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_ts(components[2])
        if not is_valid:
            return False, f"UAC user authentication credential expiration date/time invalid: {error}"
    
    return True, None


def validate_var(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate VAR (Variance) composite data type.
    
    Format: Variance Instance ID^Documented Date/Time^Stated Variance Date/Time^Variance Originator^Variance Classification^Variance Description
    
    Components (up to 6):
    - VAR-1: Variance Instance ID (EI)
    - VAR-2: Documented Date/Time (TS)
    - VAR-3: Stated Variance Date/Time (TS)
    - VAR-4: Variance Originator (XCN)
    - VAR-5: Variance Classification (CE)
    - VAR-6: Variance Description (ST)
    
    Examples:
    - "VAR123" (valid - variance instance ID only)
    - "VAR123^20250101120000^20250101120000" (valid - with documented and stated date/time)
    - "VAR123^20250101120000^20250101120000^ORIGINATOR^CLASSIFICATION^DESCRIPTION" (valid - full variance)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "VAR must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # VAR can have up to 6 components
    if len(components) > 6:
        return False, f"VAR has too many components (max 6, got {len(components)})"
    
    # Validate EI component if present (VAR-1: Variance Instance ID)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ei(components[0])
        if not is_valid:
            return False, f"VAR variance instance ID invalid: {error}"
    
    # Validate TS components if present (VAR-2: Documented Date/Time, VAR-3: Stated Variance Date/Time)
    ts_indices = [1, 2]
    ts_names = ["Documented Date/Time", "Stated Variance Date/Time"]
    
    for idx, name in zip(ts_indices, ts_names):
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                return False, f"VAR {name.lower()} invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rfr(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RFR (Reference Range) composite data type.
    
    Format: Numeric Range^Units^Reference Range^Numeric Range^Units
    
    Components (up to 5):
    - RFR-1: Numeric Range (NR)
    - RFR-2: Units (CE)
    - RFR-3: Reference Range (ST)
    - RFR-4: Numeric Range (NR)
    - RFR-5: Units (CE)
    
    Examples:
    - "10^20" (valid - numeric range only)
    - "10^20^mg/dL^Normal Range" (valid - with units and reference range)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RFR must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RFR can have up to 5 components
    if len(components) > 5:
        return False, f"RFR has too many components (max 5, got {len(components)})"
    
    # RFR-1 and RFR-4 are numeric ranges (NR), validate them
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_nr(components[0])
        if not is_valid:
            return False, f"RFR numeric range (RFR-1) invalid: {error}"
    
    # RFR-3 is a string description (ST), no validation needed
    # RFR-4 is a numeric range (NR), validate it
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_nr(components[3])
        if not is_valid:
            return False, f"RFR numeric range (RFR-4) invalid: {error}"
    
    return True, None


def validate_prl(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PRL (Parent Result Link) composite data type.
    
    Format: Parent Observation Value^Parent Observation Sub-ID^Parent Observation Value Type
    
    Components (up to 3):
    - PRL-1: Parent Observation Value (CE) - The parent observation value
    - PRL-2: Parent Observation Sub-ID (ST) - Sub-identifier for the parent observation
    - PRL-3: Parent Observation Value Type (ID) - Type of the parent observation value
    
    Examples:
    - "OBS001" (valid - parent observation value only)
    - "OBS001^SUB001" (valid - with sub-ID)
    - "OBS001^SUB001^TYPE" (valid - full PRL)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PRL must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 3:
        return False, f"PRL has too many components (max 3, got {len(components)})"
    
    # PRL-1: Parent Observation Value (CE) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ce(components[0])
        if not is_valid:
            return False, f"PRL-1 (Parent Observation Value) validation failed: {error}"
    
    # PRL-2: Parent Observation Sub-ID (ST) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_st(components[1])
        if not is_valid:
            return False, f"PRL-2 (Parent Observation Sub-ID) validation failed: {error}"
    
    # PRL-3: Parent Observation Value Type (ID) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_id(components[2])
        if not is_valid:
            return False, f"PRL-3 (Parent Observation Value Type) validation failed: {error}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rpt(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RPT (Repeat Pattern) composite data type.
    
    Format: Repeat Pattern Code^Calendar Alignment^Phase Range Begin Value^Phase Range End Value^Period Quantity^Period Units^Institution Specified Time^Event^Event Offset Units^General Timing Specification
    
    Components (up to 10):
    - RPT-1: Repeat Pattern Code (ID) - Code identifying the repeat pattern
    - RPT-2: Calendar Alignment (ID) - Calendar alignment for the pattern
    - RPT-3: Phase Range Begin Value (NM) - Beginning value of phase range
    - RPT-4: Phase Range End Value (NM) - Ending value of phase range
    - RPT-5: Period Quantity (NM) - Quantity of periods
    - RPT-6: Period Units (CE) - Units for the period
    - RPT-7: Institution Specified Time (ST) - Institution-specified time
    - RPT-8: Event (CE) - Event that triggers the pattern
    - RPT-9: Event Offset Units (CE) - Units for event offset
    - RPT-10: General Timing Specification (GTS) - General timing specification
    
    Examples:
    - "Q1H" (valid - repeat pattern code only)
    - "Q1H^D^0^0^1^H" (valid - with calendar alignment and period)
    - "Q1H^D^0^0^1^H^TIME^EVENT^UNITS^GTS" (valid - full RPT)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RPT must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 10:
        return False, f"RPT has too many components (max 10, got {len(components)})"
    
    # RPT-1: Repeat Pattern Code (ID) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_id(components[0])
        if not is_valid:
            return False, f"RPT-1 (Repeat Pattern Code) validation failed: {error}"
    
    # RPT-2: Calendar Alignment (ID) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_id(components[1])
        if not is_valid:
            return False, f"RPT-2 (Calendar Alignment) validation failed: {error}"
    
    # RPT-3: Phase Range Begin Value (NM) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_nm(components[2])
        if not is_valid:
            return False, f"RPT-3 (Phase Range Begin Value) validation failed: {error}"
    
    # RPT-4: Phase Range End Value (NM) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_nm(components[3])
        if not is_valid:
            return False, f"RPT-4 (Phase Range End Value) validation failed: {error}"
    
    # RPT-5: Period Quantity (NM) - optional
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_nm(components[4])
        if not is_valid:
            return False, f"RPT-5 (Period Quantity) validation failed: {error}"
    
    # RPT-6: Period Units (CE) - optional
    if len(components) >= 6 and components[5]:
        is_valid, error = validate_ce(components[5])
        if not is_valid:
            return False, f"RPT-6 (Period Units) validation failed: {error}"
    
    # RPT-7: Institution Specified Time (ST) - optional
    if len(components) >= 7 and components[6]:
        is_valid, error = validate_st(components[6])
        if not is_valid:
            return False, f"RPT-7 (Institution Specified Time) validation failed: {error}"
    
    # RPT-8: Event (CE) - optional
    if len(components) >= 8 and components[7]:
        is_valid, error = validate_ce(components[7])
        if not is_valid:
            return False, f"RPT-8 (Event) validation failed: {error}"
    
    # RPT-9: Event Offset Units (CE) - optional
    if len(components) >= 9 and components[8]:
        is_valid, error = validate_ce(components[8])
        if not is_valid:
            return False, f"RPT-9 (Event Offset Units) validation failed: {error}"
    
    # RPT-10: General Timing Specification (GTS) - optional
    # GTS is a complex type, but for validation purposes we'll accept any string
    # In practice, GTS validation would require more complex parsing
    if len(components) >= 10 and components[9]:
        # Basic validation: ensure it's a string (already checked)
        pass
    
    return True, None


def validate_rp(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RP (Reference Pointer) composite data type.
    
    Format: Pointer^Application ID^Type of Data^Subtype^Encoding^Data
    
    Components (up to 6):
    - RP-1: Pointer (ST)
    - RP-2: Application ID (HD)
    - RP-3: Type of Data (ID)
    - RP-4: Subtype (ID)
    - RP-5: Encoding (ID)
    - RP-6: Data (TX)
    
    Examples:
    - "POINTER" (valid - pointer only)
    - "POINTER^APP^TYPE^SUBTYPE^ENC^DATA" (valid - full reference pointer)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RP must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RP can have up to 6 components
    if len(components) > 6:
        return False, f"RP has too many components (max 6, got {len(components)})"
    
    return True, None


def validate_scv(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SCV (Scheduling Class Value Pair) composite data type.
    
    Format: Parameter Class^Parameter Value
    
    Components (up to 2):
    - SCV-1: Parameter Class (CE)
    - SCV-2: Parameter Value (ST)
    
    Examples:
    - "CLASS" (valid - parameter class only)
    - "CLASS^VALUE" (valid - parameter class and value)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SCV must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SCV can have up to 2 components
    if len(components) > 2:
        return False, f"SCV has too many components (max 2, got {len(components)})"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_sn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SN (Structured Numeric) composite data type.
    
    Format: Comparator^Num1^Separator/Suffix^Num2
    
    Components (up to 4):
    - SN-1: Comparator (ST)
    - SN-2: Num1 (NM)
    - SN-3: Separator/Suffix (ST)
    - SN-4: Num2 (NM)
    
    Examples:
    - "LT^10" (valid - comparator and number)
    - "LT^10^-^20" (valid - comparator, number, separator, number)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SN can have up to 4 components
    if len(components) > 4:
        return False, f"SN has too many components (max 4, got {len(components)})"
    
    # Validate numeric values if present
    if len(components) >= 2 and components[1]:
        try:
            float(components[1].strip())
        except ValueError:
            return False, f"SN Num1 '{components[1]}' is not a valid number"
    
    if len(components) >= 4 and components[3]:
        try:
            float(components[3].strip())
        except ValueError:
            return False, f"SN Num2 '{components[3]}' is not a valid number"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_sps(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SPS (Specimen Source) composite data type.
    
    Format: Source Name or Code^Additives^Freetext^Body Site^Site Modifier^Collection Method Modifier Code^Specimen Role
    
    Components (up to 7):
    - SPS-1: Source Name or Code (CE)
    - SPS-2: Additives (CE)
    - SPS-3: Freetext (ST)
    - SPS-4: Body Site (CE)
    - SPS-5: Site Modifier (CE)
    - SPS-6: Collection Method Modifier Code (CE)
    - SPS-7: Specimen Role (CE)
    
    Examples:
    - "BLOOD" (valid - source name only)
    - "BLOOD^HEPARIN^Venous^ARM^LEFT^VENIPUNCTURE^PATIENT" (valid - full specimen source)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SPS must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SPS can have up to 7 components
    if len(components) > 7:
        return False, f"SPS has too many components (max 7, got {len(components)})"
    
    return True, None


def validate_cnn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CNN (Composite ID Number and Name) composite data type.
    
    Format: ID Number^Family Name^Given Name^Second and Further Given Names or Initials^Suffix^Prefix^Degree^Source Table^Assigning Authority Namespace ID^Assigning Authority Universal ID^Assigning Authority Universal ID Type
    
    Components (up to 11):
    - CNN-1: ID Number (ST)
    - CNN-2: Family Name (ST)
    - CNN-3: Given Name (ST)
    - CNN-4: Second and Further Given Names or Initials (ST)
    - CNN-5: Suffix (ST)
    - CNN-6: Prefix (ST)
    - CNN-7: Degree (ST)
    - CNN-8: Source Table (IS)
    - CNN-9: Assigning Authority Namespace ID (IS)
    - CNN-10: Assigning Authority Universal ID (ST)
    - CNN-11: Assigning Authority Universal ID Type (ID)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "CNN must be a string"
    
    components = value.split(component_separator)
    if len(components) > 11:
        return False, f"CNN has too many components (max 11, got {len(components)})"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_ddi(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DDI (Daily Deductible Information) composite data type.
    
    Format: Delay Days^Amount^Type
    
    Components (up to 3):
    - DDI-1: Delay Days (NM)
    - DDI-2: Amount (MO)
    - DDI-3: Type (ID)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "DDI must be a string"
    
    components = value.split(component_separator)
    if len(components) > 3:
        return False, f"DDI has too many components (max 3, got {len(components)})"
    
    if len(components) >= 1 and components[0]:
        try:
            int(components[0].strip())
        except ValueError:
            return False, f"DDI delay days '{components[0]}' is not a valid number"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_din(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DIN (Date and Institution Name) composite data type.
    
    Format: Date^Institution Name
    
    Components (up to 2):
    - DIN-1: Date (TS)
    - DIN-2: Institution Name (CE)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "DIN must be a string"
    
    components = value.split(component_separator)
    if len(components) > 2:
        return False, f"DIN has too many components (max 2, got {len(components)})"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_dld(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DLD (Discharge to Location and Date) composite data type.
    
    Format: Discharge to Location^Effective Date
    
    Components (up to 2):
    - DLD-1: Discharge to Location (CE)
    - DLD-2: Effective Date (TS)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "DLD must be a string"
    
    components = value.split(component_separator)
    if len(components) > 2:
        return False, f"DLD has too many components (max 2, got {len(components)})"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_eld(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate ELD (Error Location and Description) composite data type.
    
    Format: Segment ID^Segment Sequence^Field Position^Field Repetition^Component Number^Sub-Component Number^Error Code
    
    Components (up to 7):
    - ELD-1: Segment ID (ST)
    - ELD-2: Segment Sequence (NM)
    - ELD-3: Field Position (NM)
    - ELD-4: Field Repetition (NM)
    - ELD-5: Component Number (NM)
    - ELD-6: Sub-Component Number (NM)
    - ELD-7: Error Code (CE)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "ELD must be a string"
    
    components = value.split(component_separator)
    if len(components) > 7:
        return False, f"ELD has too many components (max 7, got {len(components)})"
    
    # Validate numeric components if present
    numeric_indices = [1, 2, 3, 4, 5]  # Indices 2-6 (0-based: 1-5)
    for idx in numeric_indices:
        if len(components) > idx and components[idx]:
            try:
                int(components[idx].strip())
            except ValueError:
                return False, f"ELD component {idx+1} '{components[idx]}' is not a valid number"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_rmc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RMC (Room Coverage) composite data type.
    
    Format: Room Type^Amount Type^Coverage Amount
    
    Components (up to 3):
    - RMC-1: Room Type (CE)
    - RMC-2: Amount Type (CE)
    - RMC-3: Coverage Amount (MO)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "RMC must be a string"
    
    components = value.split(component_separator)
    if len(components) > 3:
        return False, f"RMC has too many components (max 3, got {len(components)})"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_srt(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SRT (Sort Order) composite data type.
    
    Format: Sort By Field^Sequencing^Order By Value
    
    Components (up to 3):
    - SRT-1: Sort By Field (ST)
    - SRT-2: Sequencing (ID)
    - SRT-3: Order By Value (ST)
    
    Examples:
    - "FIELD" (valid - sort by field only)
    - "FIELD^ASC^VALUE" (valid - sort by field, sequencing, and order by value)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SRT must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SRT can have up to 3 components
    if len(components) > 3:
        return False, f"SRT has too many components (max 3, got {len(components)})"
    
    # Common sequencing values: ASC (Ascending), DESC (Descending)
    # We'll allow any ID value but validate structure
    
    return True, None


def validate_uvc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate UVC (UB Value Code and Amount) composite data type.
    
    Format: Value Code^Value Amount
    
    Components (up to 2):
    - UVC-1: Value Code (IS)
    - UVC-2: Value Amount (NM)
    
    Examples:
    - "01" (valid - value code only)
    - "01^100.50" (valid - value code and amount)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "UVC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # UVC can have up to 2 components
    if len(components) > 2:
        return False, f"UVC has too many components (max 2, got {len(components)})"
    
    # Validate numeric amount if present
    if len(components) >= 2 and components[1]:
        try:
            float(components[1].strip())
        except ValueError:
            return False, f"UVC value amount '{components[1]}' is not a valid number"
    
    return True, None


def validate_vh(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate VH (Visiting Hours) composite data type.
    
    Format: Start Hour Range^End Hour Range^Day of Week
    
    Components (up to 3):
    - VH-1: Start Hour Range (TM)
    - VH-2: End Hour Range (TM)
    - VH-3: Day of Week (IS)
    
    Examples:
    - "0900" (valid - start hour only)
    - "0900^1700" (valid - start and end hours)
    - "0900^1700^MON" (valid - full visiting hours)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "VH must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # VH can have up to 3 components
    if len(components) > 3:
        return False, f"VH has too many components (max 3, got {len(components)})"
    
    # If VH-1 or VH-2 present, validate as TM (Time)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_tm(components[0])
        if not is_valid:
            return False, f"VH start hour range invalid: {error}"
    
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_tm(components[1])
        if not is_valid:
            return False, f"VH end hour range invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_wvs(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate WVS (Waveform Source) composite data type.
    
    Format: Source One Name^Source Two Name
    
    Components (up to 2):
    - WVS-1: Source One Name (ST)
    - WVS-2: Source Two Name (ST)
    
    Examples:
    - "ECG" (valid - source one name only)
    - "ECG^LEAD_II" (valid - source one and two names)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "WVS must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # WVS can have up to 2 components
    if len(components) > 2:
        return False, f"WVS has too many components (max 2, got {len(components)})"
    
    # Both components are ST (String) type, so basic string validation is sufficient
    # No additional validation needed beyond component count
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_wvi(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate WVI (Channel Identifier) composite data type.
    
    Format: Channel Number^Channel Name
    
    Components (up to 2):
    - WVI-1: Channel Number (NM)
    - WVI-2: Channel Name (ST)
    
    Examples:
    - "1" (valid - channel number only)
    - "1^ECG" (valid - channel number and name)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "WVI must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # WVI can have up to 2 components
    if len(components) > 2:
        return False, f"WVI has too many components (max 2, got {len(components)})"
    
    # Validate numeric channel number if present
    if len(components) >= 1 and components[0]:
        try:
            float(components[0].strip())
        except ValueError:
            return False, f"WVI channel number '{components[0]}' is not a valid number"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_vid(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate VID (Version Identifier) composite data type.
    
    Format: Version ID^Internationalization Code^International Version ID
    
    Components (up to 3):
    - VID-1: Version ID (ID)
    - VID-2: Internationalization Code (CE)
    - VID-3: International Version ID (CE)
    
    Examples:
    - "2.5" (valid - version ID only)
    - "2.5^en-US" (valid - version ID and internationalization code)
    - "2.5^en-US^2.5.1" (valid - full version identifier)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "VID must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # VID can have up to 3 components
    if len(components) > 3:
        return False, f"VID has too many components (max 3, got {len(components)})"
    
    # Basic validation: Version ID should be present if VID is not empty
    # Version ID format is typically like "2.5", "2.5.1", etc.
    # We'll do basic format checking - should contain at least one alphanumeric character
    if len(components) >= 1 and components[0]:
        version_id = components[0].strip()
        if not version_id:
            return True, None  # Empty component is allowed
        
        # Basic format check: should contain at least one alphanumeric or dot/dash
        if not any(c.isalnum() or c in '.-_' for c in version_id):
            return False, f"VID version ID '{version_id}' does not appear to be a valid version identifier"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_vr(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate VR (Value Range) composite data type.
    
    Format: First Data Code Value^Last Data Code Value
    
    Components (up to 2):
    - VR-1: First Data Code Value (ST)
    - VR-2: Last Data Code Value (ST)
    
    Examples:
    - "A" (valid - first value only)
    - "A^Z" (valid - value range)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "VR must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # VR can have up to 2 components
    if len(components) > 2:
        return False, f"VR has too many components (max 2, got {len(components)})"
    
    return True, None


def validate_spd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SPD (Specialty Description) composite data type.
    
    Format: Specialty Name^Governing Board^Phone Number^Email Address^Web Address
    
    Components (up to 5):
    - SPD-1: Specialty Name (ST)
    - SPD-2: Governing Board (ST)
    - SPD-3: Phone Number (TN)
    - SPD-4: Email Address (ST)
    - SPD-5: Web Address (ST)
    
    Examples:
    - "Cardiology" (valid - specialty name only)
    - "Cardiology^ABIM^555-1234^cardio@example.com^www.example.com" (valid - full specialty description)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SPD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SPD can have up to 5 components
    if len(components) > 5:
        return False, f"SPD has too many components (max 5, got {len(components)})"
    
    # If SPD-3 present, validate as TN (Telephone Number)
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_tn(components[2])
        if not is_valid:
            return False, f"SPD phone number invalid: {error}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_sad(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate SAD (Street Address) composite data type.
    
    Format: Street or Mailing Address^Street Name^Dwelling Number
    
    Components (up to 3):
    - SAD-1: Street or Mailing Address (ST)
    - SAD-2: Street Name (ST)
    - SAD-3: Dwelling Number (ST)
    
    Examples:
    - "123 Main St" (valid - street address only)
    - "123 Main St^Main St^123" (valid - full street address)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "SAD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # SAD can have up to 3 components
    if len(components) > 3:
        return False, f"SAD has too many components (max 3, got {len(components)})"
    
    return True, None


def validate_rcp(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RCP (Response Control Parameter) composite data type.
    
    Format: Query Priority^Quantity Limited Request^Response Modality^Execution and Delivery Time^Modify Indicator^Sort-by Field^Segment group inclusion
    
    Components (up to 7):
    - RCP-1: Query Priority (ID)
    - RCP-2: Quantity Limited Request (CQ)
    - RCP-3: Response Modality (CE)
    - RCP-4: Execution and Delivery Time (TS)
    - RCP-5: Modify Indicator (ID)
    - RCP-6: Sort-by Field (SRT)
    - RCP-7: Segment group inclusion (ID)
    
    Examples:
    - "I" (valid - query priority only)
    - "I^10" (valid - with quantity limited request)
    - "I^10^R^20250101120000" (valid - with response modality and execution time)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RCP must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RCP can have up to 7 components
    if len(components) > 7:
        return False, f"RCP has too many components (max 7, got {len(components)})"
    
    # Validate TS component if present (RCP-4: Execution and Delivery Time)
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_ts(components[3])
        if not is_valid:
            return False, f"RCP execution and delivery time invalid: {error}"
    
    return True, None


def validate_ri(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate RI (Repeat Interval) composite data type.
    
    Format: Repeat Pattern^Explicit Time Interval^Explicit Time Interval Units
    
    Components (up to 3):
    - RI-1: Repeat Pattern (ST)
    - RI-2: Explicit Time Interval (NM)
    - RI-3: Explicit Time Interval Units (CE)
    
    Examples:
    - "Q1H" (valid - repeat pattern only)
    - "Q1H^1^H" (valid - with explicit time interval)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "RI must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # RI can have up to 3 components
    if len(components) > 3:
        return False, f"RI has too many components (max 3, got {len(components)})"
    
    # Validate numeric time interval if present
    if len(components) >= 2 and components[1]:
        try:
            float(components[1].strip())
        except ValueError:
            return False, f"RI explicit time interval '{components[1]}' is not a valid number"
    
    return True, None


def validate_prc(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PRC (Pricing) composite data type.
    
    Format: Price^Price Type^From Value^To Value^Range Units^Range Type^From Value^To Value^Range Units^Range Type^From Value^To Value^Range Units^Range Type^From Value^To Value^Range Units^Range Type^From Value^To Value^Range Units^Range Type
    
    Components (up to 25):
    - PRC-1: Price (MO)
    - PRC-2: Price Type (ID)
    - PRC-3: From Value (NM)
    - PRC-4: To Value (NM)
    - PRC-5: Range Units (CE)
    - PRC-6: Range Type (ID)
    - PRC-7 through PRC-25: Additional range pairs (From Value, To Value, Range Units, Range Type) repeated
    
    Examples:
    - "100.50^CHG" (valid - price and price type)
    - "100.50^CHG^10^20^UNIT^R" (valid - price with range)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PRC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PRC can have up to 25 components
    if len(components) > 25:
        return False, f"PRC has too many components (max 25, got {len(components)})"
    
    # Validate MO component if present (PRC-1: Price)
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_mo(components[0])
        if not is_valid:
            return False, f"PRC price invalid: {error}"
    
    # Validate NM components if present (PRC-3, PRC-4, and repeated From/To values)
    # Pattern: PRC-3, PRC-4, then groups of 4 (From, To, Units, Type) starting at PRC-7
    nm_indices = [2, 3]  # PRC-3 and PRC-4 (0-based indices 2, 3)
    # Additional From/To values at indices 6, 7, 10, 11, 14, 15, 18, 19, 22, 23
    for i in range(6, min(len(components), 25), 4):
        if i < len(components):
            nm_indices.append(i)  # From Value
        if i + 1 < len(components):
            nm_indices.append(i + 1)  # To Value
    
    for idx in nm_indices:
        if idx < len(components) and components[idx]:
            try:
                float(components[idx].strip())
            except ValueError:
                return False, f"PRC numeric value '{components[idx]}' is not a valid number"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_prb(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PRB (Problem Details) composite data type.
    
    Format: Action Code^Action Date/Time^Problem ID^Problem Instance ID^Episode of Care ID^Problem List Priority^Problem Established Date/Time^Anticipated Problem Resolution Date/Time^Actual Problem Resolution Date/Time^Problem Classification^Problem Management Discipline^Problem Persistence^Problem Confirmation Status^Problem Life Cycle Status^Problem Life Cycle Status Date/Time^Problem Date of Onset^Problem Onset Text^Problem Ranking^Certainty of Problem^Probability of Problem^Individual Awareness of Problem^Problem Awareness Date/Time^Prognosis Code^Individual Awareness of Prognosis^Prognosis/Prognostic Code Date/Time^Family Awareness of Problem/Prognosis^Security/Sensitivity Code^Problem Severity^Problem Perspective^Mood Code
    
    Components (up to 29):
    - PRB-1: Action Code (ID)
    - PRB-2: Action Date/Time (TS)
    - PRB-3: Problem ID (CE)
    - PRB-4: Problem Instance ID (EI)
    - PRB-5: Episode of Care ID (EI)
    - PRB-6: Problem List Priority (NM)
    - PRB-7: Problem Established Date/Time (TS)
    - PRB-8: Anticipated Problem Resolution Date/Time (TS)
    - PRB-9: Actual Problem Resolution Date/Time (TS)
    - PRB-10: Problem Classification (CE)
    - PRB-11: Problem Management Discipline (CE)
    - PRB-12: Problem Persistence (CE)
    - PRB-13: Problem Confirmation Status (CE)
    - PRB-14: Problem Life Cycle Status (CE)
    - PRB-15: Problem Life Cycle Status Date/Time (TS)
    - PRB-16: Problem Date of Onset (TS)
    - PRB-17: Problem Onset Text (ST)
    - PRB-18: Problem Ranking (CE)
    - PRB-19: Certainty of Problem (CE)
    - PRB-20: Probability of Problem (NM)
    - PRB-21: Individual Awareness of Problem (CE)
    - PRB-22: Problem Awareness Date/Time (TS)
    - PRB-23: Prognosis Code (CE)
    - PRB-24: Individual Awareness of Prognosis (CE)
    - PRB-25: Prognosis/Prognostic Code Date/Time (TS)
    - PRB-26: Family Awareness of Problem/Prognosis (CE)
    - PRB-27: Security/Sensitivity Code (CE)
    - PRB-28: Problem Severity (CE)
    - PRB-29: Mood Code (CNE)
    
    Examples:
    - "AD^20250101120000^I10^12345" (valid - action code, date/time, problem ID, instance ID)
    - "AD^20250101120000^I10^12345^^1" (valid - with priority)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PRB must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PRB can have up to 29 components
    if len(components) > 29:
        return False, f"PRB has too many components (max 29, got {len(components)})"
    
    # Validate TS components if present (PRB-2, PRB-7, PRB-8, PRB-9, PRB-15, PRB-16, PRB-22, PRB-25)
    ts_indices = [1, 6, 7, 8, 14, 15, 21, 24]  # 0-based indices for TS components
    for idx in ts_indices:
        if len(components) > idx and components[idx]:
            is_valid, error = validate_ts(components[idx])
            if not is_valid:
                component_name = ["Action Date/Time", "Problem Established Date/Time", 
                                 "Anticipated Problem Resolution Date/Time", "Actual Problem Resolution Date/Time",
                                 "Problem Life Cycle Status Date/Time", "Problem Date of Onset",
                                 "Problem Awareness Date/Time", "Prognosis/Prognostic Code Date/Time"][ts_indices.index(idx)]
                return False, f"PRB {component_name} invalid: {error}"
    
    # Validate NM components if present (PRB-6, PRB-20)
    nm_indices = [5, 19]  # 0-based indices for NM components
    for idx in nm_indices:
        if len(components) > idx and components[idx]:
            try:
                float(components[idx].strip())
            except ValueError:
                component_name = ["Problem List Priority", "Probability of Problem"][nm_indices.index(idx)]
                return False, f"PRB {component_name} '{components[idx]}' is not a valid number"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_prd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PRD (Provider Data) composite data type.
    
    Format: Provider Role^Provider Name^Provider Address^Provider Location^Provider Communication Information^Preferred Method of Contact^Provider Identifiers^Effective Start Date of Provider Role^Effective End Date of Provider Role
    
    Components (up to 9):
    - PRD-1: Provider Role (CE)
    - PRD-2: Provider Name (XPN)
    - PRD-3: Provider Address (XAD)
    - PRD-4: Provider Location (PL)
    - PRD-5: Provider Communication Information (XTN)
    - PRD-6: Preferred Method of Contact (CE)
    - PRD-7: Provider Identifiers (PLN)
    - PRD-8: Effective Start Date of Provider Role (TS)
    - PRD-9: Effective End Date of Provider Role (TS)
    
    Examples:
    - "RP^Doe^John" (valid - role and name)
    - "RP^Doe^John^^^PH^12345" (valid - with communication and identifiers)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PRD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PRD can have up to 9 components
    if len(components) > 9:
        return False, f"PRD has too many components (max 9, got {len(components)})"
    
    # Validate TS components if present (PRD-8 and PRD-9)
    if len(components) >= 8 and components[7]:
        is_valid, error = validate_ts(components[7])
        if not is_valid:
            return False, f"PRD effective start date invalid: {error}"
    
    if len(components) >= 9 and components[8]:
        is_valid, error = validate_ts(components[8])
        if not is_valid:
            return False, f"PRD effective end date invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_pip(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PIP (Practitioner Institutional Privileges) composite data type.
    
    Format: Privilege^Privilege Class^Expiration Date^Activation Date^Facility
    
    Components (up to 5):
    - PIP-1: Privilege (CE) - The privilege code
    - PIP-2: Privilege Class (CE) - The class of privilege
    - PIP-3: Expiration Date (DT) - When the privilege expires
    - PIP-4: Activation Date (DT) - When the privilege was activated
    - PIP-5: Facility (EI) - The facility where the privilege applies
    
    Examples:
    - "PRIV001" (valid - privilege code only)
    - "PRIV001^CLASS1" (valid - with privilege class)
    - "PRIV001^CLASS1^20251231^20240101^FAC001" (valid - full PIP)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PIP must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 5:
        return False, f"PIP has too many components (max 5, got {len(components)})"
    
    # PIP-1: Privilege (CE) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_ce(components[0])
        if not is_valid:
            return False, f"PIP-1 (Privilege) validation failed: {error}"
    
    # PIP-2: Privilege Class (CE) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_ce(components[1])
        if not is_valid:
            return False, f"PIP-2 (Privilege Class) validation failed: {error}"
    
    # PIP-3: Expiration Date (DT) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_dt(components[2])
        if not is_valid:
            return False, f"PIP-3 (Expiration Date) validation failed: {error}"
    
    # PIP-4: Activation Date (DT) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_dt(components[3])
        if not is_valid:
            return False, f"PIP-4 (Activation Date) validation failed: {error}"
    
    # PIP-5: Facility (EI) - optional
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_ei(components[4])
        if not is_valid:
            return False, f"PIP-5 (Facility) validation failed: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_pl(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PL (Person Location) composite data type.
    
    Format: Point of Care^Room^Bed^Facility^Location Status^Person Location Type^Building^Floor
    
    Components (up to 8):
    - PL-1: Point of Care (IS) - Point of care identifier
    - PL-2: Room (IS) - Room identifier
    - PL-3: Bed (IS) - Bed identifier
    - PL-4: Facility (HD) - Facility identifier
    - PL-5: Location Status (IS) - Status of location
    - PL-6: Person Location Type (IS) - Type of person location
    - PL-7: Building (IS) - Building identifier
    - PL-8: Floor (IS) - Floor identifier
    
    Examples:
    - "ICU^101^A^HOSPITAL" (valid - ICU room 101 bed A)
    - "WARD^201^B^HOSPITAL^O^P^BLDG1^FLOOR2" (valid - full PL)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PL must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 8:
        return False, f"PL has too many components (max 8, got {len(components)})"
    
    # PL-1: Point of Care (IS) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_is(components[0])
        if not is_valid:
            return False, f"PL-1 (Point of Care) validation failed: {error}"
    
    # PL-2: Room (IS) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_is(components[1])
        if not is_valid:
            return False, f"PL-2 (Room) validation failed: {error}"
    
    # PL-3: Bed (IS) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_is(components[2])
        if not is_valid:
            return False, f"PL-3 (Bed) validation failed: {error}"
    
    # PL-4: Facility (HD) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_hd(components[3])
        if not is_valid:
            return False, f"PL-4 (Facility) validation failed: {error}"
    
    # PL-5: Location Status (IS) - optional
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_is(components[4])
        if not is_valid:
            return False, f"PL-5 (Location Status) validation failed: {error}"
    
    # PL-6: Person Location Type (IS) - optional
    if len(components) >= 6 and components[5]:
        is_valid, error = validate_is(components[5])
        if not is_valid:
            return False, f"PL-6 (Person Location Type) validation failed: {error}"
    
    # PL-7: Building (IS) - optional
    if len(components) >= 7 and components[6]:
        is_valid, error = validate_is(components[6])
        if not is_valid:
            return False, f"PL-7 (Building) validation failed: {error}"
    
    # PL-8: Floor (IS) - optional
    if len(components) >= 8 and components[7]:
        is_valid, error = validate_is(components[7])
        if not is_valid:
            return False, f"PL-8 (Floor) validation failed: {error}"
    
    return True, None


def validate_ppn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PPN (Performing Person Time Stamp) composite data type.
    
    Format: Performing Person^Performing Person Time Stamp
    
    Components (up to 2):
    - PPN-1: Performing Person (XCN) - Person who performed the action
    - PPN-2: Performing Person Time Stamp (TS) - When the action was performed
    
    Note: In HL7 v2.x, when a composite type contains another composite type (like XCN),
    the components are flattened. So PPN-1 through PPN-25 correspond to XCN components,
    and PPN-26 corresponds to the timestamp.
    
    Components (up to 26 total):
    - PPN-1 through PPN-25: Performing Person (XCN components) - Person identifier
    - PPN-26: Performing Person Time Stamp (TS) - Timestamp when action was performed
    
    Examples:
    - "12345^Doe^John" (valid - performing person only)
    - "12345^Doe^John^20240101100000" (valid - with timestamp at position 3, typical usage)
    - "12345^Doe^John^M^Jr^Dr^MD^TBL^AUTH^CODE^CHECK^SCHEME^TYPE^FAC^REP^CTX^20240101100000" (valid - full XCN with timestamp)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PPN must be a string"
    
    components = value.split(component_separator)
    
    # PPN can have up to 26 components total (25 for XCN + 1 for timestamp)
    if len(components) > 26:
        return False, f"PPN has too many components (max 26, got {len(components)})"
    
    # Validate XCN part (components 0-24, if present)
    # In practice, XCN typically uses 1-3 components, then timestamp follows
    xcn_end = min(25, len(components))
    if xcn_end > 0:
        xcn_components = components[:xcn_end]
        xcn_value = component_separator.join(xcn_components)
        if xcn_value.strip():  # Only validate if XCN part is not empty
            is_valid, error = validate_xcn(xcn_value)
            if not is_valid:
                return False, f"PPN Performing Person (XCN) validation failed: {error}"
    
    # Validate timestamp - can appear at various positions after XCN
    # Common pattern: ID^Family^Given (3 components) then timestamp at index 3
    # Or timestamp at index 25 (PPN-26) if full XCN is used
    
    # Check position 25 (PPN-26) for timestamp
    if len(components) >= 26 and components[25]:
        is_valid, error = validate_ts(components[25])
        if not is_valid:
            return False, f"PPN-26 (Performing Person Time Stamp) validation failed: {error}"
    
    # Also check earlier positions (3+) that might be timestamp
    # This handles cases where XCN uses fewer than 25 components (typical case)
    # Common pattern: ID^Family^Given (3 components) then timestamp at index 3
    if len(components) >= 4 and components[3]:
        # Validate as TS if it looks like it could be a timestamp (length >= 4)
        # This will catch invalid timestamps even if they don't start with digits
        if len(components[3]) >= 4:
            is_valid, error = validate_ts(components[3])
            if not is_valid:
                # This position should be timestamp but validation failed
                return False, f"PPN Performing Person Time Stamp (at position 4) validation failed: {error}"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_pth(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PTH (Pathway) composite data type.
    
    Format: Pathway ID^Pathway Instance ID^Pathway Established Date/Time^Pathway Life Cycle Status^Change Pathway Life Cycle Status Date/Time
    
    Components (up to 5):
    - PTH-1: Pathway ID (CE)
    - PTH-2: Pathway Instance ID (EI)
    - PTH-3: Pathway Established Date/Time (TS)
    - PTH-4: Pathway Life Cycle Status (CE)
    - PTH-5: Change Pathway Life Cycle Status Date/Time (TS)
    
    Examples:
    - "CARDIAC^12345" (valid - pathway ID and instance ID)
    - "CARDIAC^12345^20250101120000^ACTIVE" (valid - with date and status)
    - "CARDIAC^12345^20250101120000^ACTIVE^20250102120000" (valid - full pathway)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PTH must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PTH can have up to 5 components
    if len(components) > 5:
        return False, f"PTH has too many components (max 5, got {len(components)})"
    
    # Validate TS components if present (PTH-3, PTH-5)
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_ts(components[2])
        if not is_valid:
            return False, f"PTH pathway established date/time invalid: {error}"
    
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_ts(components[4])
        if not is_valid:
            return False, f"PTH change pathway life cycle status date/time invalid: {error}"
    
    return True, None


def validate_pt(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PT (Processing Type) composite data type.
    
    Format: Processing ID^Processing Mode
    
    Components (up to 2):
    - PT-1: Processing ID (ID)
    - PT-2: Processing Mode (ID)
    
    Examples:
    - "P" (valid - processing ID only)
    - "P^T" (valid - processing ID and mode)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PT must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PT can have up to 2 components
    if len(components) > 2:
        return False, f"PT has too many components (max 2, got {len(components)})"
    
    # Common processing IDs: D (Debug), P (Production), T (Training)
    # Common processing modes: A (Archive), R (Restore), T (Test), I (Initial load)
    # We'll allow any ID values but validate structure
    
    return True, None


def validate_pta(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PTA (Price Type and Amount) composite data type.
    
    Format: Price Type^Amount
    
    Components (up to 2):
    - PTA-1: Price Type (ID) - Type of price (e.g., AP (Administrative Price), CP (Contract Price), DP (Department Price), HP (Hospital Price), SP (Stock Price), TP (Total Price), UP (Unit Price))
    - PTA-2: Amount (MO) - Monetary amount
    
    Examples:
    - "UP" (valid - unit price type only)
    - "UP^100.50" (valid - unit price with amount)
    - "CP^250.00" (valid - contract price with amount)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PTA must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PTA can have up to 2 components
    if len(components) > 2:
        return False, f"PTA has too many components (max 2, got {len(components)})"
    
    # PTA-1: Price Type (ID) - optional but common
    # Common price types: AP (Administrative Price), CP (Contract Price), 
    # DP (Department Price), HP (Hospital Price), SP (Stock Price), 
    # TP (Total Price), UP (Unit Price)
    # We'll allow any ID values but validate structure
    
    # PTA-2: Amount (MO) - optional, validate if present
    if len(components) >= 2 and components[1]:
        # MO (Money) format: amount^currency_code
        # Basic validation: should be numeric or numeric^currency
        amount_str = components[1]
        if "^" in amount_str:
            # Has currency code
            amount_parts = amount_str.split("^")
            if len(amount_parts) > 2:
                return False, "PTA-2 (Amount) has too many components (max 2 for MO: amount^currency)"
            try:
                float(amount_parts[0])
            except ValueError:
                return False, f"PTA-2 (Amount) must be a valid numeric value, got: {amount_parts[0]}"
        else:
            # Just amount, no currency
            try:
                float(amount_str)
            except ValueError:
                return False, f"PTA-2 (Amount) must be a valid numeric value, got: {amount_str}"
    
    return True, None


def validate_ocd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate OCD (Occurrence Code and Date) composite data type.
    
    Format: Occurrence Code^Occurrence Date
    
    Components (up to 2):
    - OCD-1: Occurrence Code (IS)
    - OCD-2: Occurrence Date (TS)
    
    Examples:
    - "01" (valid - occurrence code only)
    - "01^20240101" (valid - with occurrence date)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "OCD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # OCD can have up to 2 components
    if len(components) > 2:
        return False, f"OCD has too many components (max 2, got {len(components)})"
    
    # If OCD-2 present, validate as TS (timestamp)
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_ts(components[1])
        if not is_valid:
            return False, f"OCD occurrence date invalid: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_osd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate OSD (Order Sequence Definition) composite data type.
    
    Format: Sequence/Condition^Sequence Condition Value^Maximum Number of Repeats^Sequence/Condition Time^Sequence/Condition Time Code
    
    Components (up to 5):
    - OSD-1: Sequence/Condition (ID) - Sequence or condition code
    - OSD-2: Sequence Condition Value (ST) - Value for the sequence condition
    - OSD-3: Maximum Number of Repeats (NM) - Maximum number of times the sequence can repeat
    - OSD-4: Sequence/Condition Time (TS) - Time associated with sequence/condition
    - OSD-5: Sequence/Condition Time Code (ID) - Code indicating the type of time
    
    Examples:
    - "S" (valid - sequence code only)
    - "S^VALUE^5" (valid - sequence with condition value and max repeats)
    - "S^VALUE^5^20240101100000^BEFORE" (valid - full OSD)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "OSD must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 5:
        return False, f"OSD has too many components (max 5, got {len(components)})"
    
    # OSD-1: Sequence/Condition (ID) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_id(components[0])
        if not is_valid:
            return False, f"OSD-1 (Sequence/Condition) validation failed: {error}"
    
    # OSD-2: Sequence Condition Value (ST) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_st(components[1])
        if not is_valid:
            return False, f"OSD-2 (Sequence Condition Value) validation failed: {error}"
    
    # OSD-3: Maximum Number of Repeats (NM) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_nm(components[2])
        if not is_valid:
            return False, f"OSD-3 (Maximum Number of Repeats) validation failed: {error}"
    
    # OSD-4: Sequence/Condition Time (TS) - optional
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_ts(components[3])
        if not is_valid:
            return False, f"OSD-4 (Sequence/Condition Time) validation failed: {error}"
    
    # OSD-5: Sequence/Condition Time Code (ID) - optional
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_id(components[4])
        if not is_valid:
            return False, f"OSD-5 (Sequence/Condition Time Code) validation failed: {error}"
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_osp(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate OSP (Occurrence Span Code and Date) composite data type.
    
    Format: Occurrence Span Code^Occurrence Span Start Date^Occurrence Span End Date
    
    Components (up to 3):
    - OSP-1: Occurrence Span Code (IS) - Code identifying the occurrence span
    - OSP-2: Occurrence Span Start Date (TS) - Start date/time of the occurrence span
    - OSP-3: Occurrence Span End Date (TS) - End date/time of the occurrence span
    
    Examples:
    - "01" (valid - occurrence span code only)
    - "01^20240101" (valid - with start date)
    - "01^20240101^20240131" (valid - with start and end dates)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "OSP must be a string"
    
    components = value.split(component_separator)
    
    if len(components) > 3:
        return False, f"OSP has too many components (max 3, got {len(components)})"
    
    # OSP-1: Occurrence Span Code (IS) - optional
    if len(components) >= 1 and components[0]:
        is_valid, error = validate_is(components[0])
        if not is_valid:
            return False, f"OSP-1 (Occurrence Span Code) validation failed: {error}"
    
    # OSP-2: Occurrence Span Start Date (TS) - optional
    if len(components) >= 2 and components[1]:
        is_valid, error = validate_ts(components[1])
        if not is_valid:
            return False, f"OSP-2 (Occurrence Span Start Date) validation failed: {error}"
    
    # OSP-3: Occurrence Span End Date (TS) - optional
    if len(components) >= 3 and components[2]:
        is_valid, error = validate_ts(components[2])
        if not is_valid:
            return False, f"OSP-3 (Occurrence Span End Date) validation failed: {error}"
    
    return True, None


def validate_na(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate NA (Numeric Array) composite data type.
    
    Format: Value 1^Value 2^...^Value N
    
    Components (variable, up to N values):
    - NA-1: Value 1 (NM) - First numeric value
    - NA-2: Value 2 (NM) - Second numeric value
    - NA-N: Value N (NM) - Nth numeric value
    
    Note: NA is used for arrays of numeric values. Similar to MA but specifically
    for numeric data arrays.
    
    Examples:
    - "10.5" (valid - single value)
    - "1.5^2.3^3.7" (valid - three values)
    - "0.5^1.2^2.8^4.1^5.9" (valid - five values)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "NA must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # NA can have variable number of components (typically 1-256 values)
    # We'll allow up to 256 components for practical purposes
    if len(components) > 256:
        return False, f"NA has too many components (max 256 values, got {len(components)})"
    
    # Each component should be a numeric value (NM)
    for i, component in enumerate(components, start=1):
        if component:  # Empty components are allowed
            is_valid, error = validate_nm(component)
            if not is_valid:
                return False, f"NA-{i} (Value {i}) validation failed: {error}"
    
    return True, None


def validate_ndl(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate NDL (Name with Date and Location) composite data type.
    
    Format: Name Components (XCN, up to 25)^Start Date/Time^End Date/Time^Point of Care^Room^Bed^Facility^Location Status^Patient Location Type^Building^Floor
    
    Note: In HL7 v2.x, when a composite type contains another composite type (like XCN),
    the components are flattened. So NDL-1 through NDL-25 correspond to XCN components,
    and NDL-26 through NDL-35 correspond to the remaining NDL-specific components.
    
    Components (up to 35 total):
    - NDL-1 through NDL-25: Name (XCN components) - Name of person
    - NDL-26: Start Date/Time (TS) - Start date/time
    - NDL-27: End Date/Time (TS) - End date/time
    - NDL-28: Point of Care (IS) - Point of care identifier
    - NDL-29: Room (IS) - Room identifier
    - NDL-30: Bed (IS) - Bed identifier
    - NDL-31: Facility (HD) - Facility identifier
    - NDL-32: Location Status (IS) - Status of location
    - NDL-33: Patient Location Type (IS) - Type of patient location
    - NDL-34: Building (IS) - Building identifier
    - NDL-35: Floor (IS) - Floor identifier
    
    Examples:
    - "12345^Doe^John^20240101100000^20240115100000^ICU^101^A^HOSPITAL" (valid - name with dates and location)
    - "12345^Doe^John^20240101100000" (valid - name with start date only)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "NDL must be a string"
    
    components = value.split(component_separator)
    
    # NDL can have up to 35 components total (25 for XCN + 10 for NDL-specific)
    if len(components) > 35:
        return False, f"NDL has too many components (max 35, got {len(components)})"
    
    # Validate XCN components (NDL-1 through NDL-25, if present)
    # We validate the XCN part by reconstructing it up to the first non-XCN component
    # For simplicity, we'll validate XCN if we have at least one component
    # and validate individual components based on their position
    
    # NDL-26: Start Date/Time (TS) - optional (component index 25, 0-based)
    if len(components) >= 26 and components[25]:
        is_valid, error = validate_ts(components[25])
        if not is_valid:
            return False, f"NDL-26 (Start Date/Time) validation failed: {error}"
    
    # NDL-27: End Date/Time (TS) - optional (component index 26, 0-based)
    if len(components) >= 27 and components[26]:
        is_valid, error = validate_ts(components[26])
        if not is_valid:
            return False, f"NDL-27 (End Date/Time) validation failed: {error}"
    
    # NDL-28: Point of Care (IS) - optional (component index 27, 0-based)
    if len(components) >= 28 and components[27]:
        is_valid, error = validate_is(components[27])
        if not is_valid:
            return False, f"NDL-28 (Point of Care) validation failed: {error}"
    
    # NDL-29: Room (IS) - optional (component index 28, 0-based)
    if len(components) >= 29 and components[28]:
        is_valid, error = validate_is(components[28])
        if not is_valid:
            return False, f"NDL-29 (Room) validation failed: {error}"
    
    # NDL-30: Bed (IS) - optional (component index 29, 0-based)
    if len(components) >= 30 and components[29]:
        is_valid, error = validate_is(components[29])
        if not is_valid:
            return False, f"NDL-30 (Bed) validation failed: {error}"
    
    # NDL-31: Facility (HD) - optional (component index 30, 0-based)
    if len(components) >= 31 and components[30]:
        is_valid, error = validate_hd(components[30])
        if not is_valid:
            return False, f"NDL-31 (Facility) validation failed: {error}"
    
    # NDL-32: Location Status (IS) - optional (component index 31, 0-based)
    if len(components) >= 32 and components[31]:
        is_valid, error = validate_is(components[31])
        if not is_valid:
            return False, f"NDL-32 (Location Status) validation failed: {error}"
    
    # NDL-33: Patient Location Type (IS) - optional (component index 32, 0-based)
    if len(components) >= 33 and components[32]:
        is_valid, error = validate_is(components[32])
        if not is_valid:
            return False, f"NDL-33 (Patient Location Type) validation failed: {error}"
    
    # NDL-34: Building (IS) - optional (component index 33, 0-based)
    if len(components) >= 34 and components[33]:
        is_valid, error = validate_is(components[33])
        if not is_valid:
            return False, f"NDL-34 (Building) validation failed: {error}"
    
    # NDL-35: Floor (IS) - optional (component index 34, 0-based)
    if len(components) >= 35 and components[34]:
        is_valid, error = validate_is(components[34])
        if not is_valid:
            return False, f"NDL-35 (Floor) validation failed: {error}"
    
    # Validate XCN part (components 0-24) by validating as XCN if we have XCN components
    # For practical purposes, we'll validate XCN structure if present
    # XCN validation is lenient and just checks component count, so we can validate
    # the XCN portion by checking if we have at least some XCN components
    if len(components) > 0:
        # Validate XCN components (up to 25 components, indices 0-24)
        xcn_components = components[:25]  # Take first 25 components for XCN
        xcn_value = component_separator.join(xcn_components)
        if xcn_value:  # Only validate if XCN part is not empty
            is_valid, error = validate_xcn(xcn_value)
            if not is_valid:
                return False, f"NDL-1 through NDL-25 (Name/XCN) validation failed: {error}"
    
    # Also validate components in earlier positions (3+) that might be NDL-specific
    # This handles cases where XCN uses fewer than 25 components (typical case)
    # Common pattern: ID^Family^Given (3 components) then Start Date at index 3
    # Start Date/Time typically appears at index 3 (after ID^Family^Given)
    # We validate if the component is present and could be a date/time
    if len(components) >= 4 and components[3]:
        # Validate as TS - if it fails and looks like it should be a date (non-empty, reasonable length),
        # then it's an error. We check length >= 4 to avoid false positives on short XCN components.
        if len(components[3]) >= 4:
            is_valid, error = validate_ts(components[3])
            if not is_valid:
                # This position should be Start Date/Time but validation failed
                return False, f"NDL Start Date/Time (at position 4) validation failed: {error}"
    
    # End Date/Time typically appears at index 4 (after Start Date)
    if len(components) >= 5 and components[4]:
        # Validate as TS if it looks like it could be a date
        if len(components[4]) >= 4:
            is_valid, error = validate_ts(components[4])
            if not is_valid:
                # This position should be End Date/Time but validation failed
                return False, f"NDL End Date/Time (at position 5) validation failed: {error}"
    
    return True, None


def validate_nr(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate NR (Numeric Range) composite data type.
    
    Format: Low Value^High Value
    
    Components:
    - NR-1: Low Value (NM)
    - NR-2: High Value (NM)
    
    Examples:
    - "10" (valid - low value only)
    - "10^20" (valid - numeric range)
    - "10.5^20.5" (valid - decimal range)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "NR must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # NR can have up to 2 components
    if len(components) > 2:
        return False, f"NR has too many components (max 2, got {len(components)})"
    
    # Validate numeric values
    if len(components) >= 1 and components[0]:
        try:
            float(components[0].strip())
        except ValueError:
            return False, f"NR low value '{components[0]}' is not a valid number"
    
    if len(components) >= 2 and components[1]:
        try:
            float(components[1].strip())
        except ValueError:
            return False, f"NR high value '{components[1]}' is not a valid number"
    
    return True, None


def validate_tq(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate TQ (Timing/Quantity) composite data type.
    
    Format: Quantity^Interval^Duration^Start Date/Time^End Date/Time^Priority^Condition^Text^Conjunction^Order Sequencing^Occurrence Duration^Total Occurrences
    
    Components (up to 12):
    - TQ-1: Quantity (CQ)
    - TQ-2: Interval (RI)
    - TQ-3: Duration (ST)
    - TQ-4: Start Date/Time (TS)
    - TQ-5: End Date/Time (TS)
    - TQ-6: Priority (ST)
    - TQ-7: Condition (ST)
    - TQ-8: Text (TX)
    - TQ-9: Conjunction (ID)
    - TQ-10: Order Sequencing (OSD)
    - TQ-11: Occurrence Duration (CE)
    - TQ-12: Total Occurrences (NM)
    
    Examples:
    - "1^Q1H" (valid - quantity with interval)
    - "1^Q1H^DURATION^20240101^20240131" (valid - timing with dates)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "TQ must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # TQ can have up to 12 components
    if len(components) > 12:
        return False, f"TQ has too many components (max 12, got {len(components)})"
    
    # If TQ-4 or TQ-5 present, validate as TS (timestamp)
    if len(components) >= 4 and components[3]:
        is_valid, error = validate_ts(components[3])
        if not is_valid:
            return False, f"TQ start date/time invalid: {error}"
    
    if len(components) >= 5 and components[4]:
        is_valid, error = validate_ts(components[4])
        if not is_valid:
            return False, f"TQ end date/time invalid: {error}"
    
    return True, None


def validate_xpn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate XPN (Extended Person Name) composite data type.
    
    Format: Family Name^Given Name^Second and Further Given Names or Initials^Suffix^Prefix^Degree^Name Type Code^Name Representation Code^Name Context^Name Validity Range^Name Assembly Order^Effective Date^Expiration Date^Professional Suffix
    
    Components (up to 14):
    - XPN-1: Family Name (FN)
    - XPN-2: Given Name (ST)
    - XPN-3: Second and Further Given Names or Initials (ST)
    - XPN-4: Suffix (ST)
    - XPN-5: Prefix (ST)
    - XPN-6: Degree (IS)
    - XPN-7: Name Type Code (ID)
    - XPN-8: Name Representation Code (ID)
    - XPN-9: Name Context (CE)
    - XPN-10: Name Validity Range (DR)
    - XPN-11: Name Assembly Order (ID)
    - XPN-12: Effective Date (TS)
    - XPN-13: Expiration Date (TS)
    - XPN-14: Professional Suffix (ST)
    
    Examples:
    - "Doe^John" (valid - basic name, similar to PN)
    - "Doe^John^M^Jr^Dr^MD^L^A" (valid - extended)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "XPN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # XPN can have up to 14 components
    if len(components) > 14:
        return False, f"XPN has too many components (max 14, got {len(components)})"
    
    return True, None


def validate_xad(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate XAD (Extended Address) composite data type.
    
    Format: Street Address^Other Designation^City^State or Province^Zip or Postal Code^Country^Address Type^Other Geographic Designation^County/Parish Code^Census Tract^Address Representation Code^Address Validity Range^Effective Date^Expiration Date^Expiration Reason^Temporary Indicator^Bad Address Indicator^Address Usage^Addressee^Comment^Preference Order^Protection Code^Address Identifier
    
    Components (up to 23):
    - XAD-1 through XAD-11: Same as AD
    - XAD-12: Address Validity Range (DR)
    - XAD-13: Effective Date (TS)
    - XAD-14: Expiration Date (TS)
    - XAD-15: Expiration Reason (CE)
    - XAD-16: Temporary Indicator (ID)
    - XAD-17: Bad Address Indicator (ID)
    - XAD-18: Address Usage (ID)
    - XAD-19: Addressee (ST)
    - XAD-20: Comment (ST)
    - XAD-21: Preference Order (NM)
    - XAD-22: Protection Code (CE)
    - XAD-23: Address Identifier (EI)
    
    Examples:
    - "123 Main St^^Anytown^CA^12345" (valid - basic address, same as AD)
    - "123 Main St^^Anytown^CA^12345^USA^M^^^001^1234^A" (valid - extended)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "XAD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # XAD can have up to 23 components
    if len(components) > 23:
        return False, f"XAD has too many components (max 23, got {len(components)})"
    
    return True, None


def validate_fn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate FN (Family Name) composite data type.
    
    Format: Surname^Own Surname Prefix^Own Surname^Surname Prefix from Partner/Spouse^Surname from Partner/Spouse
    
    Components:
    - FN-1: Surname (ST)
    - FN-2: Own Surname Prefix (ST)
    - FN-3: Own Surname (ST)
    - FN-4: Surname Prefix from Partner/Spouse (ST)
    - FN-5: Surname from Partner/Spouse (ST)
    
    Examples:
    - "Doe" (valid - simple surname)
    - "Doe^van^der" (valid - surname with prefix)
    - "Smith^Jones" (valid - hyphenated surname)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "FN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # FN can have up to 5 components
    if len(components) > 5:
        return False, f"FN has too many components (max 5, got {len(components)})"
    
    return True, None


def validate_hd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate HD (Hierarchic Designator) composite data type.
    
    Format: Namespace ID^Universal ID^Universal ID Type
    
    Components:
    - HD-1: Namespace ID (IS)
    - HD-2: Universal ID (ST)
    - HD-3: Universal ID Type (ID)
    
    Examples:
    - "MRN^12345^ISO" (valid - MRN namespace)
    - "PROVIDER^DOC001^L" (valid - provider namespace)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "HD must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # HD can have up to 3 components
    if len(components) > 3:
        return False, f"HD has too many components (max 3, got {len(components)})"
    
    return True, None


def validate_tn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate TN (Telephone Number) composite data type.
    
    Format: [NNN] [(999)]999-9999[X99999][B99999][C any text]
    
    Components (when stored as composite):
    - TN-1: [NNN] (optional area code)
    - TN-2: [(999)]999-9999 (phone number)
    - TN-3: X99999 (extension)
    - TN-4: B99999 (beeper number)
    - TN-5: C any text (comment)
    
    However, TN is often stored as a single string value.
    Format validation: Should match phone number patterns.
    
    Examples:
    - "555-1234" (valid)
    - "(555)123-4567" (valid)
    - "555-1234X123" (valid - with extension)
    - "555-1234B456" (valid - with beeper)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "TN must be a string"
    
    # Check if value contains component separator (composite format)
    if component_separator in value:
        components = value.split(component_separator)
        if len(components) > 5:
            return False, f"TN has too many components (max 5, got {len(components)})"
        # Validate each component if needed
        # For now, just check structure
    
    # Basic format validation for phone numbers
    # Pattern: optional area code, phone number, optional extension/beeper/comment
    # Allow various formats: (555)123-4567, 555-1234, 5551234567, etc.
    # This is lenient to handle various real-world formats
    
    # Check for obviously invalid characters (but allow common phone number characters)
    invalid_chars = set(value) - set("0123456789()-+ xXbBcC. \t")
    if invalid_chars:
        return False, f"TN contains invalid characters: {''.join(sorted(invalid_chars))}"
    
    # Basic length check (phone numbers should be reasonable length)
    # Remove common separators for length check
    digits_only = re.sub(r'[^0-9]', '', value)
    if digits_only and (len(digits_only) < 7 or len(digits_only) > 15):
        return False, f"TN has invalid length (phone number should have 7-15 digits, got {len(digits_only)})"
    

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


def validate_pn(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PN (Person Name) composite data type.
    
    Format: Family Name^Given Name^Middle Name or Initial^Suffix^Prefix^Degree^Name Type Code^Name Representation Code^Name Context^Name Validity Range^Name Assembly Order
    
    Components:
    - PN-1: Family Name (FN)
    - PN-2: Given Name (ST)
    - PN-3: Middle Name or Initial (ST)
    - PN-4: Suffix (ST)
    - PN-5: Prefix (ST)
    - PN-6: Degree (IS)
    - PN-7: Name Type Code (ID)
    - PN-8: Name Representation Code (ID)
    - PN-9: Name Context (CE)
    - PN-10: Name Validity Range (DR)
    - PN-11: Name Assembly Order (ID)
    
    Examples:
    - "Doe^John^M" (valid - family, given, middle)
    - "Smith^Jane^^Jr" (valid - family, given, suffix)
    - "Doe^John^M^Jr^Dr" (valid - with prefix and suffix)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "PN must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # PN can have up to 11 components, but all are optional
    if len(components) > 11:
        return False, f"PN has too many components (max 11, got {len(components)})"
    
    # Basic validation: at least one component should have a value
    # (though empty PN is technically allowed)
    # Individual component validation can be added later if needed
    
    return True, None


def validate_aui(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate AUI (Authorization Information) composite data type.
    
    Format: Authorization Number^Date^Source
    Components:
    - AUI-1: Authorization Number (ST)
    - AUI-2: Date (DT)
    - AUI-3: Source (ST)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "AUI must be a string"
    
    components = value.split(component_separator)
    if len(components) > 3:
        return False, f"AUI has too many components (max 3, got {len(components)})"
    
    # Validate date component if present
    if len(components) > 1 and components[1]:
        is_valid, error = validate_dt(components[1])
        if not is_valid:
            return False, f"AUI date component invalid: {error}"
    
    return True, None


def validate_ccp(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CCP (Channel Calibration Parameters) composite data type.
    
    Format: Channel Calibration Sensitivity Correction Factor^Channel Calibration Baseline^Channel Calibration Time Skew
    Components:
    - CCP-1: Channel Calibration Sensitivity Correction Factor (NM)
    - CCP-2: Channel Calibration Baseline (NM)
    - CCP-3: Channel Calibration Time Skew (NM)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "CCP must be a string"
    
    components = value.split(component_separator)
    if len(components) > 3:
        return False, f"CCP has too many components (max 3, got {len(components)})"
    
    # Validate numeric components if present
    for i, comp in enumerate(components[:3], 1):
        if comp:
            is_valid, error = validate_nm(comp)
            if not is_valid:
                return False, f"CCP component {i} invalid: {error}"
    
    return True, None


def validate_cd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CD (Channel Definition) composite data type.
    
    Format: Channel Identifier^Waveform Source^Channel Sensitivity/Units^Channel Calibration Parameters^Channel Sampling Frequency^Minimum/Maximum Data Values
    Components:
    - CD-1: Channel Identifier (WVI)
    - CD-2: Waveform Source (WVS)
    - CD-3: Channel Sensitivity/Units (CSU)
    - CD-4: Channel Calibration Parameters (CCP)
    - CD-5: Channel Sampling Frequency (NM)
    - CD-6: Minimum/Maximum Data Values (NR)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "CD must be a string"
    
    components = value.split(component_separator)
    if len(components) > 6:
        return False, f"CD has too many components (max 6, got {len(components)})"
    
    # Basic structure validation - individual component validation can be added
    return True, None


def validate_ccd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CCD (Charge Code and Date) composite data type.
    
    Format: When to Charge Code^Date/Time
    Components:
    - CCD-1: When to Charge Code (ID) - Required, table 0100
    - CCD-2: Date/Time (DTM) - Optional
    
    Used in BLG segment field 1 (When to Charge).
    
    Examples:
    - "D" (valid - charge on discharge only)
    - "D^202401151430" (valid - charge on discharge with date/time)
    - "O^20240115" (valid - charge on order with date)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "CCD must be a string"
    
    components = value.split(component_separator)
    if len(components) > 2:
        return False, f"CCD has too many components (max 2, got {len(components)})"
    
    # Validate CCD-1: When to Charge Code (ID, table 0100)
    if components[0]:
        valid_codes = {"D", "O", "S", "T"}  # Standard codes: D=Discharge, O=Order, S=Service, T=Transaction
        if components[0] not in valid_codes:
            return False, f"CCD component 1 (When to Charge Code) must be one of {valid_codes}, got '{components[0]}'"
    
    # Validate CCD-2: Date/Time (DTM) if present
    if len(components) > 1 and components[1]:
        is_valid, error = validate_dtm(components[1])
        if not is_valid:
            return False, f"CCD component 2 (Date/Time) invalid: {error}"
    
    # Log completion timestamp at end of operation
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return True, None


def validate_cne(value: str, component_separator: str = "^", code_system_table: Optional[str] = None, valid_codes: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate CNE (Coded with No Exceptions) composite data type.
    
    Format: Identifier^Text^Name of Coding System^Alternate Identifier^Alternate Text^Name of Alternate Coding System^Coding System Version ID^Alternate Coding System Version ID^Original Text
    Components:
    - CNE-1: Identifier (ST) - Required
    - CNE-2: Text (ST)
    - CNE-3: Name of Coding System (ID)
    - CNE-4: Alternate Identifier (ST)
    - CNE-5: Alternate Text (ST)
    - CNE-6: Name of Alternate Coding System (ID)
    - CNE-7: Coding System Version ID (ST)
    - CNE-8: Alternate Coding System Version ID (ST)
    - CNE-9: Original Text (ST)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        code_system_table: Optional code system/table ID for validation
        valid_codes: Optional list of valid code identifiers for validation
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return False, "CNE requires at least an identifier (component 1)"
    
    if not isinstance(value, str):
        return False, "CNE must be a string"
    
    components = value.split(component_separator)
    if len(components) > 9:
        return False, f"CNE has too many components (max 9, got {len(components)})"
    
    # CNE-1 (Identifier) is required
    if not components[0] or not components[0].strip():
        return False, "CNE component 1 (Identifier) is required"
    
    # Validate code if code system validation is requested
    if valid_codes is not None:
        identifier = components[0].strip()
        if identifier not in valid_codes:
            table_info = f" for code system {code_system_table}" if code_system_table else ""
            return False, f"CNE identifier '{identifier}' is not a valid code{table_info}"
    
    return True, None


def validate_cq(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CQ (Composite Quantity with Units) composite data type.
    
    Format: Quantity^Units
    Components:
    - CQ-1: Quantity (NM)
    - CQ-2: Units (CE)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "CQ must be a string"
    
    components = value.split(component_separator)
    if len(components) > 2:
        return False, f"CQ has too many components (max 2, got {len(components)})"
    
    # Validate quantity component if present
    if len(components) > 0 and components[0]:
        is_valid, error = validate_nm(components[0])
        if not is_valid:
            return False, f"CQ quantity component invalid: {error}"
    
    # Validate units component if present
    if len(components) > 1 and components[1]:
        is_valid, error = validate_ce(components[1], component_separator=component_separator)
        if not is_valid:
            return False, f"CQ units component invalid: {error}"
    
    return True, None


def validate_csu(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate CSU (Channel Sensitivity/Units) composite data type.
    
    Format: Sensitivity^Unit of Measure Identifier^Unit of Measure Description^Unit of Measure Coding System^Alternate Unit of Measure Identifier^Alternate Unit of Measure Description^Alternate Unit of Measure Coding System
    Components:
    - CSU-1: Sensitivity (NM)
    - CSU-2: Unit of Measure Identifier (ST)
    - CSU-3: Unit of Measure Description (ST)
    - CSU-4: Unit of Measure Coding System (ID)
    - CSU-5: Alternate Unit of Measure Identifier (ST)
    - CSU-6: Alternate Unit of Measure Description (ST)
    - CSU-7: Alternate Unit of Measure Coding System (ID)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "CSU must be a string"
    
    components = value.split(component_separator)
    if len(components) > 7:
        return False, f"CSU has too many components (max 7, got {len(components)})"
    
    # Validate sensitivity component if present
    if len(components) > 0 and components[0]:
        is_valid, error = validate_nm(components[0])
        if not is_valid:
            return False, f"CSU sensitivity component invalid: {error}"
    
    return True, None


def validate_cwe(value: str, component_separator: str = "^", code_system_table: Optional[str] = None, valid_codes: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate CWE (Coded with Exceptions) composite data type.
    
    Format: Identifier^Text^Name of Coding System^Alternate Identifier^Alternate Text^Name of Alternate Coding System^Coding System Version ID^Alternate Coding System Version ID^Original Text
    Components:
    - CWE-1: Identifier (ST)
    - CWE-2: Text (ST)
    - CWE-3: Name of Coding System (ID)
    - CWE-4: Alternate Identifier (ST)
    - CWE-5: Alternate Text (ST)
    - CWE-6: Name of Alternate Coding System (ID)
    - CWE-7: Coding System Version ID (ST)
    - CWE-8: Alternate Coding System Version ID (ST)
    - CWE-9: Original Text (ST)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        code_system_table: Optional code system/table ID for validation
        valid_codes: Optional list of valid code identifiers for validation
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "CWE must be a string"
    
    components = value.split(component_separator)
    if len(components) > 9:
        return False, f"CWE has too many components (max 9, got {len(components)})"
    
    # Validate code if code system validation is requested
    if valid_codes is not None and len(components) > 0 and components[0]:
        identifier = components[0].strip()
        if identifier not in valid_codes:
            table_info = f" for code system {code_system_table}" if code_system_table else ""
            return False, f"CWE identifier '{identifier}' is not a valid code{table_info}"
    
    return True, None


def validate_dlt(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DLT (Delta) composite data type.
    
    Format: Normal Range^Numeric Threshold^Change Computation^Days Retained
    Components:
    - DLT-1: Normal Range (NR)
    - DLT-2: Numeric Threshold (NM)
    - DLT-3: Change Computation (ID)
    - DLT-4: Days Retained (NM)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "DLT must be a string"
    
    components = value.split(component_separator)
    if len(components) > 4:
        return False, f"DLT has too many components (max 4, got {len(components)})"
    
    # Validate numeric components if present
    for i, comp_idx in enumerate([1, 3], 1):  # Components 2 and 4 are numeric
        if len(components) > comp_idx and components[comp_idx]:
            is_valid, error = validate_nm(components[comp_idx])
            if not is_valid:
                return False, f"DLT component {comp_idx + 1} invalid: {error}"
    
    return True, None


def validate_dtm(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate DTM (Date/Time) composite data type.
    
    Format: Date/Time^Precision
    Components:
    - DTM-1: Date/Time (TS)
    - DTM-2: Precision (ID)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "DTM must be a string"
    
    components = value.split(component_separator)
    if len(components) > 2:
        return False, f"DTM has too many components (max 2, got {len(components)})"
    
    # Validate date/time component if present
    if len(components) > 0 and components[0]:
        is_valid, error = validate_ts(components[0])
        if not is_valid:
            return False, f"DTM date/time component invalid: {error}"
    
    return True, None


def validate_eip(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate EIP (Entity Identifier Pair) composite data type.
    
    Format: Placer Assigned Identifier^Filler Assigned Identifier
    Components:
    - EIP-1: Placer Assigned Identifier (EI)
    - EIP-2: Filler Assigned Identifier (EI)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "EIP must be a string"
    
    components = value.split(component_separator)
    if len(components) > 2:
        return False, f"EIP has too many components (max 2, got {len(components)})"
    
    # Validate EI components if present
    for i, comp in enumerate(components[:2], 1):
        if comp:
            is_valid, error = validate_ei(comp, component_separator=component_separator)
            if not is_valid:
                return False, f"EIP component {i} invalid: {error}"
    
    return True, None


def validate_erl(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate ERL (Error Location) composite data type.
    
    Format: Segment ID^Segment Sequence^Field Position^Field Repetition^Component Number^Sub-Component Number
    Components:
    - ERL-1: Segment ID (ST)
    - ERL-2: Segment Sequence (NM)
    - ERL-3: Field Position (NM)
    - ERL-4: Field Repetition (NM)
    - ERL-5: Component Number (NM)
    - ERL-6: Sub-Component Number (NM)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "ERL must be a string"
    
    components = value.split(component_separator)
    if len(components) > 6:
        return False, f"ERL has too many components (max 6, got {len(components)})"
    
    # Validate numeric components if present (components 2-6)
    for i, comp in enumerate(components[1:6], 2):
        if comp:
            is_valid, error = validate_nm(comp)
            if not is_valid:
                return False, f"ERL component {i} invalid: {error}"
    
    return True, None


def validate_gts(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate GTS (General Timing Specification) composite data type.
    
    Format: General Timing Specification (varies by version)
    This is a complex type that can represent various timing specifications.
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "GTS must be a string"
    
    # GTS is a complex type with variable structure
    # Basic validation: ensure it's a string
    # More detailed validation would depend on the specific GTS format used
    return True, None


def validate_ic(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate IC (Insurance Certification) composite data type.
    
    Format: Insurance Plan ID^Insurance Company ID^Insurance Company Name^Insurance Company Address^Insurance Co Contact Person^Insurance Co Phone Number^Group Number^Group Name^Insured's Group Emp Name^Insured's Group Emp Address^Insured's Group Emp Phone Number^Plan Effective Date^Plan Expiration Date^Authorization Information^Plan Type^Name Of Insured^Insured's Relationship To Patient^Insured's Date Of Birth^Insured's Address^Assignment Of Benefits^Coordination Of Benefits^Coord Of Ben Priority^Notice Of Admission Flag^Notice Of Admission Date^Report Of Eligibility Flag^Report Of Eligibility Date^Release Information Code^Pre-Admit Cert (PAC)^Verification Date/Time^Verification By^Type Of Agreement Code^Billing Status^Lifetime Reserve Days^Delay Before L.R. Day^Company Plan Code^Policy Number^Policy Deductible^Policy Limit - Amount^Policy Limit - Days^Room Rate - Semi-Private^Room Rate - Private^Insured's Employment Status^Insured's Sex^Insured's Employer Address^Verification Status^Prior Insurance Plan ID^Coverage's Insured's Plan Priority^Plan Type^Name Of Insured^Insured's Relationship To Patient^Insured's Date Of Birth^Insured's Address^Insured's Employee ID^Insured's Social Security Number^Employer Name^Employer Address^Employer Phone Number^Employer Contact Person^Employer Contact Phone Number^Plan Coverage Type^Plan Description^Name Of Insured^Insured's Relationship To Patient^Insured's Date Of Birth^Insured's Address^Insured's Employee ID^Insured's Social Security Number^Employer Name^Employer Address^Employer Phone Number^Employer Contact Person^Employer Contact Phone Number^Plan Coverage Type^Plan Description^Name Of Insured^Insured's Relationship To Patient^Insured's Date Of Birth^Insured's Address^Insured's Employee ID^Insured's Social Security Number^Employer Name^Employer Address^Employer Phone Number^Employer Contact Person^Employer Contact Phone Number^Plan Coverage Type^Plan Description
    
    Components (up to 200):
    - IC-1: Insurance Plan ID (CE) - Insurance plan identifier
    - IC-2: Insurance Company ID (CX) - Insurance company identifier
    - IC-3: Insurance Company Name (XON) - Insurance company name
    - IC-4: Insurance Company Address (XAD) - Insurance company address
    - IC-5: Insurance Co Contact Person (XPN) - Contact person at insurance company
    - IC-6: Insurance Co Phone Number (XTN) - Phone number for insurance company
    - IC-7: Group Number (ST) - Group number
    - IC-8: Group Name (XON) - Group name
    - IC-9 through IC-200: Additional insurance-related fields
    
    Note: IC is a very large composite type with up to 200 components covering
    all aspects of insurance certification and coverage information.
    
    Examples:
    - "PLAN123^COMP456^Blue Cross^123 Main St" (valid - basic insurance info)
    
    Args:
        value: String value to validate (components separated by component_separator)
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not value:
        return True, None  # Empty values are allowed in HL7
    
    if not isinstance(value, str):
        return False, "IC must be a string"
    
    # Split into components
    components = value.split(component_separator)
    
    # IC can have up to 200 components
    if len(components) > 200:
        return False, f"IC has too many components (max 200, got {len(components)})"
    
    # Basic validation: IC-1 (Insurance Plan ID) should be present if IC is not empty
    if components[0]:
        # IC-1 is CE (Coded Element), validate as CE
        is_valid, error = validate_ce(components[0], component_separator)
        if not is_valid:
            return False, f"IC-1 (Insurance Plan ID) validation failed: {error}"
    
    # Additional component validation can be added as needed
    # For now, we'll do basic structure validation
    
    return True, None


def validate_icd(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate ICD (Insurance Certification Definition) composite data type.
    
    Format: Certification Patient Type^Certification Required^Date/Time Certification Required^Date/Time Certification Expires
    Components:
    - ICD-1: Certification Patient Type (CE)
    - ICD-2: Certification Required (ID)
    - ICD-3: Date/Time Certification Required (TS)
    - ICD-4: Date/Time Certification Expires (TS)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "ICD must be a string"
    
    components = value.split(component_separator)
    if len(components) > 4:
        return False, f"ICD has too many components (max 4, got {len(components)})"
    
    # Validate date/time components if present (components 3 and 4)
    for i, comp_idx in enumerate([2, 3], 3):
        if len(components) > comp_idx and components[comp_idx]:
            is_valid, error = validate_ts(components[comp_idx])
            if not is_valid:
                return False, f"ICD component {comp_idx + 1} invalid: {error}"
    
    return True, None


def validate_la2(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate LA2 (Location with Address Variation 2) composite data type.
    
    Format: Point of Care^Room^Bed^Facility^Location Status^Person Location Type^Building^Floor^Location Description
    Components:
    - LA2-1: Point of Care (IS)
    - LA2-2: Room (IS)
    - LA2-3: Bed (IS)
    - LA2-4: Facility (HD)
    - LA2-5: Location Status (IS)
    - LA2-6: Person Location Type (IS)
    - LA2-7: Building (IS)
    - LA2-8: Floor (IS)
    - LA2-9: Location Description (ST)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "LA2 must be a string"
    
    components = value.split(component_separator)
    if len(components) > 9:
        return False, f"LA2 has too many components (max 9, got {len(components)})"
    
    # Validate facility component if present (component 4)
    if len(components) > 3 and components[3]:
        is_valid, error = validate_hd(components[3], component_separator=component_separator)
        if not is_valid:
            return False, f"LA2 facility component invalid: {error}"
    
    return True, None


def validate_pln(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate PLN (Practitioner License or Other ID Number) composite data type.
    
    Format: ID Number^Type of ID Number^State/Other Qualifying Information^Expiration Date
    Components:
    - PLN-1: ID Number (ST)
    - PLN-2: Type of ID Number (IS)
    - PLN-3: State/Other Qualifying Information (ST)
    - PLN-4: Expiration Date (DT)
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None
    
    if not isinstance(value, str):
        return False, "PLN must be a string"
    
    components = value.split(component_separator)
    if len(components) > 4:
        return False, f"PLN has too many components (max 4, got {len(components)})"
    
    # Validate expiration date component if present (component 4)
    if len(components) > 3 and components[3]:
        is_valid, error = validate_dt(components[3])
        if not is_valid:
            return False, f"PLN expiration date component invalid: {error}"
    
    return True, None


def validate_varies(value: str, component_separator: str = "^") -> Tuple[bool, Optional[str]]:
    """
    Validate VARIES (Variable Datatype) data type.
    
    VARIES indicates that the data type can vary and is determined at runtime.
    This is a placeholder type that accepts any value structure.
    
    Args:
        value: String value to validate
        component_separator: Component separator character (default: ^)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # VARIES accepts any value - it's a variable type
    return True, None


def validate_data_type(data_type: str, value: str, **kwargs) -> Tuple[bool, Optional[str]]:
    """
    Validate a value against an HL7 v2.x data type.
    
    Args:
        data_type: Data type code (DT, TM, TS, NM, ST, SI, TX, FT, ID, IS, etc.)
        value: Value to validate
        **kwargs: Additional parameters for specific data types
            - max_length: For ST, TX, FT types, maximum allowed length
            - table_id: For ID, IS types, table identifier
            - valid_codes: For ID, IS types, list of valid codes for table validation
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if value is valid, False otherwise
        - error_message: None if valid, error description if invalid
        
    Raises:
        ValueError: If data_type is not supported
    """
    data_type = data_type.upper()
    
    if data_type == "DT":
        return validate_dt(value)
    elif data_type == "TM":
        return validate_tm(value)
    elif data_type == "TS":
        return validate_ts(value)
    elif data_type == "NM":
        return validate_nm(value)
    elif data_type == "ST":
        max_length = kwargs.get("max_length")
        return validate_st(value, max_length=max_length)
    elif data_type == "SI":
        return validate_si(value)
    elif data_type == "TX":
        max_length = kwargs.get("max_length")
        return validate_tx(value, max_length=max_length)
    elif data_type == "FT":
        max_length = kwargs.get("max_length")
        return validate_ft(value, max_length=max_length)
    elif data_type == "ID":
        table_id = kwargs.get("table_id")
        valid_codes = kwargs.get("valid_codes")
        return validate_id(value, table_id=table_id, valid_codes=valid_codes)
    elif data_type == "IS":
        table_id = kwargs.get("table_id")
        valid_codes = kwargs.get("valid_codes")
        return validate_is(value, table_id=table_id, valid_codes=valid_codes)
    elif data_type == "AD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ad(value, component_separator=component_separator)
    elif data_type == "PN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pn(value, component_separator=component_separator)
    elif data_type == "PIP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pip(value, component_separator=component_separator)
    elif data_type == "PL":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pl(value, component_separator=component_separator)
    elif data_type == "PPN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ppn(value, component_separator=component_separator)
    elif data_type == "CE":
        component_separator = kwargs.get("component_separator", "^")
        code_system_table = kwargs.get("code_system_table")
        valid_codes = kwargs.get("valid_codes")
        return validate_ce(value, component_separator=component_separator, code_system_table=code_system_table, valid_codes=valid_codes)
    elif data_type == "CK":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ck(value, component_separator=component_separator)
    elif data_type == "CM":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cm(value, component_separator=component_separator)
    elif data_type == "TN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_tn(value, component_separator=component_separator)
    elif data_type == "DR":
        component_separator = kwargs.get("component_separator", "^")
        return validate_dr(value, component_separator=component_separator)
    elif data_type == "EI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ei(value, component_separator=component_separator)
    elif data_type == "HD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_hd(value, component_separator=component_separator)
    elif data_type == "MSG":
        component_separator = kwargs.get("component_separator", "^")
        return validate_msg(value, component_separator=component_separator)
    elif data_type == "FN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_fn(value, component_separator=component_separator)
    elif data_type == "CN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cn(value, component_separator=component_separator)
    elif data_type == "CP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cp(value, component_separator=component_separator)
    elif data_type == "XAD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_xad(value, component_separator=component_separator)
    elif data_type == "XCN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_xcn(value, component_separator=component_separator)
    elif data_type == "XON":
        component_separator = kwargs.get("component_separator", "^")
        return validate_xon(value, component_separator=component_separator)
    elif data_type == "XPN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_xpn(value, component_separator=component_separator)
    elif data_type == "XTN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_xtn(value, component_separator=component_separator)
    elif data_type == "MO":
        component_separator = kwargs.get("component_separator", "^")
        return validate_mo(value, component_separator=component_separator)
    elif data_type == "TQ":
        component_separator = kwargs.get("component_separator", "^")
        return validate_tq(value, component_separator=component_separator)
    elif data_type == "CX":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cx(value, component_separator=component_separator)
    elif data_type == "FC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_fc(value, component_separator=component_separator)
    elif data_type == "NA":
        component_separator = kwargs.get("component_separator", "^")
        return validate_na(value, component_separator=component_separator)
    elif data_type == "NDL":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ndl(value, component_separator=component_separator)
    elif data_type == "NR":
        component_separator = kwargs.get("component_separator", "^")
        return validate_nr(value, component_separator=component_separator)
    elif data_type == "CF":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cf(value, component_separator=component_separator)
    elif data_type == "JCC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_jcc(value, component_separator=component_separator)
    elif data_type == "OCD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ocd(value, component_separator=component_separator)
    elif data_type == "OSD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_osd(value, component_separator=component_separator)
    elif data_type == "OSP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_osp(value, component_separator=component_separator)
    elif data_type == "MOC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_moc(value, component_separator=component_separator)
    elif data_type == "MOP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_mop(value, component_separator=component_separator)
    elif data_type == "PRB":
        component_separator = kwargs.get("component_separator", "^")
        return validate_prb(value, component_separator=component_separator)
    elif data_type == "PRC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_prc(value, component_separator=component_separator)
    elif data_type == "PRL":
        component_separator = kwargs.get("component_separator", "^")
        return validate_prl(value, component_separator=component_separator)
    elif data_type == "PRD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_prd(value, component_separator=component_separator)
    elif data_type == "PT":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pt(value, component_separator=component_separator)
    elif data_type == "PTA":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pta(value, component_separator=component_separator)
    elif data_type == "PTH":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pth(value, component_separator=component_separator)
    elif data_type == "QAK":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qak(value, component_separator=component_separator)
    elif data_type == "QID":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qid(value, component_separator=component_separator)
    elif data_type == "QPD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qpd(value, component_separator=component_separator)
    elif data_type == "QRD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qrd(value, component_separator=component_separator)
    elif data_type == "QRF":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qrf(value, component_separator=component_separator)
    elif data_type == "QRI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qri(value, component_separator=component_separator)
    elif data_type == "RCP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rcp(value, component_separator=component_separator)
    elif data_type == "RCD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rcd(value, component_separator=component_separator)
    elif data_type == "RDF":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rdf(value, component_separator=component_separator)
    elif data_type == "RDT":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rdt(value, component_separator=component_separator)
    elif data_type == "RF1":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rf1(value, component_separator=component_separator)
    elif data_type == "RGS":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rgs(value, component_separator=component_separator)
    elif data_type == "RMI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rmi(value, component_separator=component_separator)
    elif data_type == "ROL":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rol(value, component_separator=component_separator)
    elif data_type == "RQ1":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rq1(value, component_separator=component_separator)
    elif data_type == "RQD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rqd(value, component_separator=component_separator)
    elif data_type == "SAC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sac(value, component_separator=component_separator)
    elif data_type == "SCD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_scd(value, component_separator=component_separator)
    elif data_type == "SCH":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sch(value, component_separator=component_separator)
    elif data_type == "SCP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_scp(value, component_separator=component_separator)
    elif data_type == "SDD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sdd(value, component_separator=component_separator)
    elif data_type == "SID":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sid(value, component_separator=component_separator)
    elif data_type == "SLT":
        component_separator = kwargs.get("component_separator", "^")
        return validate_slt(value, component_separator=component_separator)
    elif data_type == "SPM":
        component_separator = kwargs.get("component_separator", "^")
        return validate_spm(value, component_separator=component_separator)
    elif data_type == "SPR":
        component_separator = kwargs.get("component_separator", "^")
        return validate_spr(value, component_separator=component_separator)
    elif data_type == "STF":
        component_separator = kwargs.get("component_separator", "^")
        return validate_stf(value, component_separator=component_separator)
    elif data_type == "TCC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_tcc(value, component_separator=component_separator)
    elif data_type == "TCD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_tcd(value, component_separator=component_separator)
    elif data_type == "UAC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_uac(value, component_separator=component_separator)
    elif data_type == "VAR":
        component_separator = kwargs.get("component_separator", "^")
        return validate_var(value, component_separator=component_separator)
    elif data_type == "QIP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qip(value, component_separator=component_separator)
    elif data_type == "QSC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_qsc(value, component_separator=component_separator)
    elif data_type == "RI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ri(value, component_separator=component_separator)
    elif data_type == "RFR":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rfr(value, component_separator=component_separator)
    elif data_type == "RP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rp(value, component_separator=component_separator)
    elif data_type == "RPT":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rpt(value, component_separator=component_separator)
    elif data_type == "SAD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sad(value, component_separator=component_separator)
    elif data_type == "SCV":
        component_separator = kwargs.get("component_separator", "^")
        return validate_scv(value, component_separator=component_separator)
    elif data_type == "SN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sn(value, component_separator=component_separator)
    elif data_type == "SPD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_spd(value, component_separator=component_separator)
    elif data_type == "SPS":
        component_separator = kwargs.get("component_separator", "^")
        return validate_sps(value, component_separator=component_separator)
    elif data_type == "CNN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cnn(value, component_separator=component_separator)
    elif data_type == "DDI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ddi(value, component_separator=component_separator)
    elif data_type == "DIN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_din(value, component_separator=component_separator)
    elif data_type == "DLD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_dld(value, component_separator=component_separator)
    elif data_type == "ELD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_eld(value, component_separator=component_separator)
    elif data_type == "RMC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_rmc(value, component_separator=component_separator)
    elif data_type == "SRT":
        component_separator = kwargs.get("component_separator", "^")
        return validate_srt(value, component_separator=component_separator)
    elif data_type == "VID":
        component_separator = kwargs.get("component_separator", "^")
        return validate_vid(value, component_separator=component_separator)
    elif data_type == "VR":
        component_separator = kwargs.get("component_separator", "^")
        return validate_vr(value, component_separator=component_separator)
    elif data_type == "UVC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_uvc(value, component_separator=component_separator)
    elif data_type == "VH":
        component_separator = kwargs.get("component_separator", "^")
        return validate_vh(value, component_separator=component_separator)
    elif data_type == "WVI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_wvi(value, component_separator=component_separator)
    elif data_type == "WVS":
        component_separator = kwargs.get("component_separator", "^")
        return validate_wvs(value, component_separator=component_separator)
    elif data_type == "AUI":
        component_separator = kwargs.get("component_separator", "^")
        return validate_aui(value, component_separator=component_separator)
    elif data_type == "CCP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ccp(value, component_separator=component_separator)
    elif data_type == "CD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cd(value, component_separator=component_separator)
    elif data_type == "CNE":
        component_separator = kwargs.get("component_separator", "^")
        code_system_table = kwargs.get("code_system_table")
        valid_codes = kwargs.get("valid_codes")
        return validate_cne(value, component_separator=component_separator, code_system_table=code_system_table, valid_codes=valid_codes)
    elif data_type == "CQ":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cq(value, component_separator=component_separator)
    elif data_type == "CSU":
        component_separator = kwargs.get("component_separator", "^")
        return validate_csu(value, component_separator=component_separator)
    elif data_type == "CWE":
        component_separator = kwargs.get("component_separator", "^")
        code_system_table = kwargs.get("code_system_table")
        valid_codes = kwargs.get("valid_codes")
        return validate_cwe(value, component_separator=component_separator, code_system_table=code_system_table, valid_codes=valid_codes)
    elif data_type == "DLT":
        component_separator = kwargs.get("component_separator", "^")
        return validate_dlt(value, component_separator=component_separator)
    elif data_type == "DTM":
        component_separator = kwargs.get("component_separator", "^")
        return validate_dtm(value, component_separator=component_separator)
    elif data_type == "ED":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ed(value, component_separator=component_separator)
    elif data_type == "EIP":
        component_separator = kwargs.get("component_separator", "^")
        return validate_eip(value, component_separator=component_separator)
    elif data_type == "ERL":
        component_separator = kwargs.get("component_separator", "^")
        return validate_erl(value, component_separator=component_separator)
    elif data_type == "GTS":
        component_separator = kwargs.get("component_separator", "^")
        return validate_gts(value, component_separator=component_separator)
    elif data_type == "IC":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ic(value, component_separator=component_separator)
    elif data_type == "ICD":
        component_separator = kwargs.get("component_separator", "^")
        return validate_icd(value, component_separator=component_separator)
    elif data_type == "LA1":
        component_separator = kwargs.get("component_separator", "^")
        return validate_la1(value, component_separator=component_separator)
    elif data_type == "LA2":
        component_separator = kwargs.get("component_separator", "^")
        return validate_la2(value, component_separator=component_separator)
    elif data_type == "MA":
        component_separator = kwargs.get("component_separator", "^")
        return validate_ma(value, component_separator=component_separator)
    elif data_type == "PLN":
        component_separator = kwargs.get("component_separator", "^")
        return validate_pln(value, component_separator=component_separator)
    elif data_type == "VARIES":
        component_separator = kwargs.get("component_separator", "^")
        return validate_varies(value, component_separator=component_separator)
    elif data_type == "CNS":
        component_separator = kwargs.get("component_separator", "^")
        return validate_cns(value, component_separator=component_separator)
    elif data_type == "MS":
        return validate_ms(value)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

