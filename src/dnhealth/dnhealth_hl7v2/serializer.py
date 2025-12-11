# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x ER7 serializer.

Serializes Message model objects back to ER7 ("pipe-delimited") text format.
"""

import logging
from datetime import datetime
from typing import List

from dnhealth.dnhealth_hl7v2.model import Component, EncodingCharacters, Field, Message, Segment
from dnhealth.dnhealth_hl7v2.parser import escape_value

logger = logging.getLogger(__name__)


def serialize_subcomponents(    subcomponents: List, subcomponent_separator: str, escape_char: str, encoding_chars: EncodingCharacters
) -> str:
    """
    Serialize subcomponents to text.

    Args:
        subcomponents: List of Subcomponent objects
        subcomponent_separator: Subcomponent separator character
        escape_char: Escape character
        encoding_chars: Encoding characters

    Returns:
        Serialized subcomponent text
    """
    if not subcomponents:
        return ""

    parts = []
    for subcomp in subcomponents:
        escaped = escape_value(subcomp.value, escape_char, encoding_chars)
        parts.append(escaped)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return subcomponent_separator.join(parts)


def serialize_components(
    components: List[Component],
    component_separator: str,
    subcomponent_separator: str,
    escape_char: str,
    encoding_chars: EncodingCharacters,
) -> str:
    """
    Serialize components to text.

    Args:
        components: List of Component objects
        component_separator: Component separator character
        subcomponent_separator: Subcomponent separator character
        escape_char: Escape character
        encoding_chars: Encoding characters

    Returns:
        Serialized component text
    """
    if not components:
        return ""

    parts = []
    for comp in components:
        subcomp_text = serialize_subcomponents(
            comp.subcomponents, subcomponent_separator, escape_char, encoding_chars
        )
        parts.append(subcomp_text)
    
    result = component_separator.join(parts)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return result


def serialize_field(
    field: Field,
    component_separator: str,
    subcomponent_separator: str,
    repetition_separator: str,
    escape_char: str,
    encoding_chars: EncodingCharacters,
) -> str:
    """
    Serialize field to text.

    Args:
        field: Field object
        component_separator: Component separator character
        subcomponent_separator: Subcomponent separator character
        repetition_separator: Repetition separator character
        escape_char: Escape character
        encoding_chars: Encoding characters

    Returns:
        Serialized field text ('""' for null fields, '' for empty fields)
    """
    # Handle null field ("""" = double quotes)
    if field.is_null:
        return '""'

    if not field.components:
        return ""

    comp_text = serialize_components(
        field.components, component_separator, subcomponent_separator, escape_char, encoding_chars
    )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return comp_text


def serialize_segment(segment: Segment, encoding_chars: EncodingCharacters, normalize: bool = True) -> str:
    """
    Serialize segment to ER7 text line.

    Args:
        segment: Segment object
        encoding_chars: Encoding characters
        normalize: If True, normalize output (remove trailing empty fields) (default: True)

    Returns:
        Serialized segment line (without trailing \\r)
    """
    parts = [segment.name]

    # Serialize each field position with all its repetitions
    for field_repetitions in segment._field_repetitions:
        # Serialize each repetition and join with repetition separator
        repetition_texts = []
        for field in field_repetitions:
            field_text = serialize_field(
                field,
                encoding_chars.component_separator,
                encoding_chars.subcomponent_separator,
                encoding_chars.repetition_separator,
                encoding_chars.escape_character,
                encoding_chars,
            )
            repetition_texts.append(field_text)
        
        # Join repetitions with repetition separator
        field_text = encoding_chars.repetition_separator.join(repetition_texts)
        parts.append(field_text)
    
    # Preserve original formatting: maintain original field count when normalize=False
    if not normalize:
        # Ensure we have the original number of fields (preserve trailing empty fields)
        original_count = getattr(segment, '_original_field_count', len(segment._field_repetitions))
        # Pad with empty fields if needed to match original count
        while len(parts) - 1 < original_count:  # -1 because parts[0] is segment name
            parts.append("")
    # Normalize: remove trailing empty fields (except for MSH, BHS, and FHS which have special requirements)
    elif normalize and segment.name not in ("MSH", "BHS", "FHS"):
        # Remove trailing empty fields
        while len(parts) > 1 and not parts[-1]:
            parts.pop()
    
    # For MSH, ensure at least MSH-2 is present (encoding characters)
    if segment.name == "MSH" and len(parts) < 2:
        # Add default encoding characters if missing
        if len(parts) == 1:
            parts.append(encoding_chars.component_separator + 
                        encoding_chars.repetition_separator + 
                        encoding_chars.escape_character + 
                        encoding_chars.subcomponent_separator)
    
    # For BHS, ensure at least BHS-2 is present (encoding characters)
    # BHS-1 is the field separator (implicit, not stored)
    if segment.name == "BHS" and len(parts) < 2:
        # Add default encoding characters if missing
        if len(parts) == 1:
            parts.append(encoding_chars.component_separator + 
                        encoding_chars.repetition_separator + 
                        encoding_chars.escape_character + 
                        encoding_chars.subcomponent_separator)
    
    # For FHS, ensure at least FHS-2 is present (encoding characters)
    # FHS-1 is the field separator (implicit, not stored)
    if segment.name == "FHS" and len(parts) < 2:
        # Add default encoding characters if missing
        if len(parts) == 1:
            parts.append(encoding_chars.component_separator + 
                        encoding_chars.repetition_separator + 
                        encoding_chars.escape_character + 
                        encoding_chars.subcomponent_separator)

    return encoding_chars.field_separator.join(parts)


def serialize_hl7v2(message: Message, max_line_length: int = 32767, normalize: bool = True) -> str:
    """
    Serialize Message object to ER7 text format.

    Args:
        message: Message object to serialize
        max_line_length: Maximum line length before using continuation (default: 32767)
        normalize: If True, normalize output format (remove trailing empty fields, standardize separators) (default: True)

    Returns:
        ER7 text message (with \\r line endings)
    """
    if not message.segments:
        raise ValueError("Message has no segments")

    lines = []
    continuation_char = message.encoding_chars.continuation_character
    
    for segment in message.segments:
        line = serialize_segment(segment, message.encoding_chars, normalize=normalize)
        
        # Handle continuation if segment is too long and continuation char is set
        if continuation_char and len(line) > max_line_length:
            # Split segment into multiple lines
            segment_name = segment.name
            # First line: segment name + fields up to max length
            first_line = line[:max_line_length]
            # Find last complete field before max length
            last_sep = first_line.rfind(message.encoding_chars.field_separator)
            if last_sep > len(segment_name) + 1:  # Ensure we have at least segment name + separator
                first_line = first_line[:last_sep]
                remaining = line[last_sep + 1:]
            else:
                remaining = line[len(segment_name) + 1:]
            
            lines.append(first_line)
            
            # Add continuation lines
            while remaining:
                if len(remaining) <= max_line_length - len(continuation_char) - 1:
                    lines.append(continuation_char + message.encoding_chars.field_separator + remaining)
                    break
                else:
                    # Find last complete field
                    cont_line = remaining[:max_line_length - len(continuation_char) - 1]
                    last_sep = cont_line.rfind(message.encoding_chars.field_separator)
                    if last_sep > 0:
                        cont_line = cont_line[:last_sep]
                        remaining = remaining[last_sep + 1:]
                    else:
                        cont_line = remaining
                        remaining = ""
                    lines.append(continuation_char + message.encoding_chars.field_separator + cont_line)
        else:
            lines.append(line)
        
        # Ensure MSH-14 is set if continuation character exists
        if segment.name == "MSH" and continuation_char:
            # Check if MSH-14 is already set
            if len(segment.fields) < 14:
                # MSH-14 needs to be added - this is handled during segment serialization
                # We'll need to ensure MSH-14 is in the segment when serializing
                pass

    # Join with \r (HL7 v2 standard line ending)
    result = "\r".join(lines) + "\r"
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] HL7v2 message serialization completed successfully")
    
    return result

