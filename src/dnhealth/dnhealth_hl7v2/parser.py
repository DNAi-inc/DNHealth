# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x ER7 parser.

Parses ER7 ("pipe-delimited") text messages into Message model objects.
Handles escape sequences, encoding characters, and real-world quirks.
"""

import logging
import re
from datetime import datetime
from typing import List, Optional

from dnhealth.errors import HL7v2ParseError

logger = logging.getLogger(__name__)
from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)


def unescape_value(value: str, escape_char: str) -> str:
    """
    Unescape HL7 v2 escape sequences in a value.

    Escape sequences:
    - \\F\\ = field separator
    - \\S\\ = component separator
    - \\T\\ = subcomponent separator
    - \\R\\ = repetition separator
    - \\E\\ = escape character
    - \\.br\\ = line break
    - \\.ce\\ = center next line
    - \\.in\\ = indent next line
    - \\.sk\\ = skip next line
    - \\.ti\\ = tab indent
    - \\.fi\\ = end formatting

    Args:
        value: Value string potentially containing escape sequences
        escape_char: Escape character (typically \\)

    Returns:
        Unescaped value string
    """
    if not escape_char or not value:
        return value

    # Process escape sequences in order (longest first to avoid partial matches)
    # Formatting sequences first (they're longer)
    result = value
    result = result.replace(f"{escape_char}.br{escape_char}", "\n")
    result = result.replace(f"{escape_char}.ce{escape_char}", "\n")
    result = result.replace(f"{escape_char}.in{escape_char}", "\n")
    result = result.replace(f"{escape_char}.sk{escape_char}", "\n")
    result = result.replace(f"{escape_char}.ti{escape_char}", "\t")
    result = result.replace(f"{escape_char}.fi{escape_char}", "")
    
    # Then single-character escape sequences
    result = result.replace(f"{escape_char}F{escape_char}", "|")
    result = result.replace(f"{escape_char}S{escape_char}", "^")
    result = result.replace(f"{escape_char}T{escape_char}", "&")
    result = result.replace(f"{escape_char}R{escape_char}", "~")
    result = result.replace(f"{escape_char}E{escape_char}", escape_char)

    return result


def escape_value(value: str, escape_char: str, encoding_chars: EncodingCharacters) -> str:
    """
    Escape special characters in a value for HL7 v2 serialization.

    Args:
        value: Value string to escape
        escape_char: Escape character (typically \\)
        encoding_chars: Encoding characters

    Returns:
        Escaped value string
    """
    if not escape_char:
        return value

    result = value
    result = result.replace(escape_char, f"{escape_char}E{escape_char}")
    result = result.replace(encoding_chars.field_separator, f"{escape_char}F{escape_char}")
    result = result.replace(encoding_chars.component_separator, f"{escape_char}S{escape_char}")
    result = result.replace(encoding_chars.subcomponent_separator, f"{escape_char}T{escape_char}")
    result = result.replace(encoding_chars.repetition_separator, f"{escape_char}R{escape_char}")

    return result


def parse_subcomponents(    text: str, subcomponent_separator: str, escape_char: str
) -> List[Subcomponent]:
    """
    Parse subcomponents from text.

    Args:
        text: Text containing subcomponents
        subcomponent_separator: Subcomponent separator character
        escape_char: Escape character

    Returns:
        List of Subcomponent objects
    """
    if not text:
        return [Subcomponent()]

    # Split by subcomponent separator, handling escape sequences
    parts = []
    current = ""
    i = 0
    while i < len(text):
        if text[i : i + len(escape_char)] == escape_char:
            # Check for escape sequence
            if i + 1 < len(text) and text[i + 1] == escape_char[0] if escape_char else False:
                # Double escape - literal escape character
                current += escape_char
                i += len(escape_char) * 2
            else:
                # Look for escape sequence end
                end_idx = text.find(escape_char, i + 1)
                if end_idx != -1:
                    # Include entire escape sequence
                    current += text[i : end_idx + len(escape_char)]
                    i = end_idx + len(escape_char)
                else:
                    current += text[i]
                    i += 1
        elif text[i] == subcomponent_separator:
            parts.append(unescape_value(current, escape_char))
            current = ""
            i += 1
        else:
            current += text[i]
            i += 1

    parts.append(unescape_value(current, escape_char))


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return [Subcomponent(part) for part in parts]


def parse_components(
    text: str, component_separator: str, subcomponent_separator: str, escape_char: str
) -> List[Component]:
    """
    Parse components from text.

    Args:
        text: Text containing components
        component_separator: Component separator character
        subcomponent_separator: Subcomponent separator character
        escape_char: Escape character

    Returns:
        List of Component objects
    """
    if not text:
        return [Component()]

    # Split by component separator, handling escape sequences
    parts = []
    current = ""
    i = 0
    while i < len(text):
        if text[i : i + len(escape_char)] == escape_char:
            # Check for escape sequence
            end_idx = text.find(escape_char, i + 1)
            if end_idx != -1:
                current += text[i : end_idx + len(escape_char)]
                i = end_idx + len(escape_char)
            else:
                current += text[i]
                i += 1
        elif text[i] == component_separator:
            parts.append(current)
            current = ""
            i += 1
        else:
            current += text[i]
            i += 1

    parts.append(current)

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return [
        Component(parse_subcomponents(part, subcomponent_separator, escape_char))
        for part in parts
    ]


def parse_field(
    text: str,
    component_separator: str,
    subcomponent_separator: str,
    repetition_separator: str,
    escape_char: str,
) -> List[Field]:
    """
    Parse field repetitions from text.

    Args:
        text: Text containing field repetitions
        component_separator: Component separator character
        subcomponent_separator: Subcomponent separator character
        repetition_separator: Repetition separator character
        escape_char: Escape character

    Returns:
        List of Field objects (one per repetition)
    """
    if not text:
        return [Field()]

    # Check for null field ("""" = double quotes)
    is_null = text == '""'

    # Split by repetition separator, handling escape sequences
    parts = []
    current = ""
    i = 0
    while i < len(text):
        if text[i : i + len(escape_char)] == escape_char:
            # Check for escape sequence
            end_idx = text.find(escape_char, i + 1)
            if end_idx != -1:
                current += text[i : end_idx + len(escape_char)]
                i = end_idx + len(escape_char)
            else:
                current += text[i]
                i += 1
        elif text[i] == repetition_separator:
            parts.append(current)
            current = ""
            i += 1
        else:
            current += text[i]
            i += 1

    parts.append(current)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return [
        Field(
            parse_components(part, component_separator, subcomponent_separator, escape_char),
            is_null=part == '""' if part else False
        )
        for part in parts
    ]


def parse_segment(
    line: str,
    encoding_chars: EncodingCharacters,
    line_number: Optional[int] = None,
) -> Segment:
    """
    Parse a single segment line.

    Args:
        line: Segment line (without trailing \\r)
        encoding_chars: Encoding characters
        line_number: Optional line number for error reporting

    Returns:
        Segment object

    Raises:
        HL7v2ParseError: If segment cannot be parsed
    """
    if not line:
        raise HL7v2ParseError("Empty segment line", line_number=line_number)

    # Remove trailing whitespace
    line = line.rstrip()

    # Split by field separator
    parts = line.split(encoding_chars.field_separator)

    if not parts:
        raise HL7v2ParseError("Segment has no fields", line_number=line_number)

    # First part is segment name (3 characters)
    segment_name = parts[0]
    if len(segment_name) != 3:
        raise HL7v2ParseError(
            f"Invalid segment name: '{segment_name}' (must be 3 characters)",
            line_number=line_number,
            segment=segment_name,
        )
    
    # Allow custom Z-segments (Z followed by 2 alphanumeric characters)
    # Standard segments are 3 uppercase letters, Z-segments start with Z
    if not (segment_name.isalpha() and segment_name.isupper()) and not (
        segment_name.startswith("Z") and len(segment_name) == 3
    ):
        # In tolerant mode, allow non-standard segment names
        # Otherwise, only warn but don't fail
        pass  # Custom segments are allowed

    # Parse fields (skip first part which is segment name)
    field_repetitions_list = []
    for field_index, field_text in enumerate(parts[1:], start=1):
        try:
            field_repetitions = parse_field(
                field_text,
                encoding_chars.component_separator,
                encoding_chars.subcomponent_separator,
                encoding_chars.repetition_separator,
                encoding_chars.escape_character,
            )
            # Store all repetitions for this field position
            field_repetitions_list.append(field_repetitions if field_repetitions else [Field()])
        except Exception as e:
            # Wrap exception with field context
            raise HL7v2ParseError(
                f"Error parsing field {field_index} in segment {segment_name}: {e}",
                line_number=line_number,
                segment=segment_name,
            ) from e

    # Track original field count for preserving formatting
    original_field_count = len(field_repetitions_list)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return Segment(segment_name, field_repetitions=field_repetitions_list, original_field_count=original_field_count)


def parse_hl7v2(text: str, tolerant: bool = False) -> Message:
    """
    Parse HL7 v2.x ER7 text message into a Message object.

    Args:
        text: ER7 text message
        tolerant: If True, attempt to parse malformed messages (default: False)

    Returns:
        Message object

    Raises:
        HL7v2ParseError: If message cannot be parsed
    """
    if not text:
        raise HL7v2ParseError("Empty message")

    # Normalize line endings
    text = text.replace("\r\n", "\r").replace("\n", "\r")

    # Split into segments (segments are separated by \r)
    lines = text.split("\r")
    lines = [line for line in lines if line.strip()]  # Remove empty lines

    if not lines:
        raise HL7v2ParseError("No segments found in message")

    # First segment must be MSH
    if not lines[0].startswith("MSH"):
        if tolerant:
            # Try to find MSH segment
            msh_idx = None
            for i, line in enumerate(lines):
                if line.startswith("MSH"):
                    msh_idx = i
                    break
            if msh_idx is None:
                raise HL7v2ParseError("MSH segment not found")
            # Move MSH to front
            lines.insert(0, lines.pop(msh_idx))
        else:
            raise HL7v2ParseError("Message must start with MSH segment")

    # Parse MSH segment to extract encoding characters
    msh_line = lines[0]
    if len(msh_line) < 4:
        raise HL7v2ParseError("MSH segment too short", line_number=1, segment="MSH")

    # MSH-2 contains encoding characters (format: ^~\\&)
    # MSH format: MSH|^~\\&|...
    field_separator = msh_line[3] if len(msh_line) > 3 else "|"
    msh2_start = 4
    msh2_text = ""
    msh14_text = None
    
    if len(msh_line) > msh2_start:
        # Find end of MSH-2 (next field separator)
        for i in range(msh2_start, len(msh_line)):
            if msh_line[i] == field_separator:
                break
            msh2_text += msh_line[i]
    
    # Parse MSH to get MSH-14 (continuation character) if present
    msh_segment_temp = parse_segment(msh_line, EncodingCharacters(), line_number=1)
    if len(msh_segment_temp.fields) >= 14:
        msh14_field = msh_segment_temp.field(14)
        if msh14_field.value():
            msh14_text = msh14_field.value()
    
    encoding_chars = EncodingCharacters.from_msh2(msh2_text, msh14_text)
    encoding_chars.field_separator = field_separator

    # Parse all segments, handling continuation segments
    segments = []
    version = None
    continuation_char = encoding_chars.continuation_character
    i = 0
    
    while i < len(lines):
        line = lines[i]
        line_number = i + 1
        
        try:
            # Check if this is a continuation line
            if continuation_char and line.startswith(continuation_char):
                # This is a continuation of the previous segment
                if not segments:
                    raise HL7v2ParseError(
                        "Continuation line found without preceding segment",
                        line_number=line_number,
                    )
                # Get the last segment and append continuation fields
                last_segment = segments[-1]
                continuation_text = line[len(continuation_char):]
                # Remove field separator if present at start
                if continuation_text.startswith(encoding_chars.field_separator):
                    continuation_text = continuation_text[1:]
                
                # Parse continuation fields and append to last segment
                if continuation_text:
                    continuation_parts = continuation_text.split(encoding_chars.field_separator)
                    for field_text in continuation_parts:
                        field_repetitions = parse_field(
                            field_text,
                            encoding_chars.component_separator,
                            encoding_chars.subcomponent_separator,
                            encoding_chars.repetition_separator,
                            encoding_chars.escape_character,
                        )
                        last_segment._field_repetitions.append(field_repetitions if field_repetitions else [Field()])
                        last_segment.fields.append(field_repetitions[0] if field_repetitions else Field())
                
                i += 1
                continue
            
            # Parse normal segment
            segment = parse_segment(line, encoding_chars, line_number=line_number)
            segments.append(segment)
            
            # Extract version from MSH-12
            if segment.name == "MSH" and len(segment.fields) >= 12:
                version_field = segment.field(12)
                if version_field.components:
                    version = version_field.components[0].value()
            
            i += 1

        except HL7v2ParseError as e:
            if tolerant:
                # In tolerant mode, try to continue
                continue
            raise

    if not segments:
        raise HL7v2ParseError("No valid segments found")

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

    return Message(segments=segments, encoding_chars=encoding_chars, version=version)

