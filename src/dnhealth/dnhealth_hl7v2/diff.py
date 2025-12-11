# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message comparison and diff utilities.

Provides functions to compare two HL7v2 messages and identify differences.
"""

from typing import Dict, List, Optional, Tuple

from dnhealth.dnhealth_hl7v2.model import Message, Segment
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
class MessageDiff:
    """
    Represents differences between two HL7v2 messages.
    """

    def __init__(self):
        """Initialize diff result."""
        self.segment_differences: List[Dict] = []
        self.field_differences: List[Dict] = []
        self.structural_differences: List[str] = []
        self.identical = True

    def add_segment_difference(self, segment_name: str, position: int, message1_value: str, message2_value: str):
        """Add a segment difference."""
        self.identical = False
        self.segment_differences.append({
            "segment": segment_name,
            "position": position,
            "message1": message1_value,
            "message2": message2_value,
        })


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

    def add_field_difference(        self, segment_name: str, field_index: int, message1_value: str, message2_value: str
    ):
        """Add a field difference."""
        self.identical = False
        self.field_differences.append({
            "segment": segment_name,
            "field": field_index,
            "message1": message1_value,
            "message2": message2_value,
        })

    def add_structural_difference(self, description: str):
        """Add a structural difference."""
        self.identical = False
        self.structural_differences.append(description)


def compare_messages(message1: Message, message2: Message) -> MessageDiff:
    """
    Compare two HL7v2 messages and return differences.

    Args:
        message1: First message to compare
        message2: Second message to compare

    Returns:
        MessageDiff object containing all differences
    """
    diff = MessageDiff()

    # Compare versions
    if message1.version != message2.version:
        diff.add_structural_difference(
            f"Version mismatch: {message1.version} vs {message2.version}"
        )

    # Compare encoding characters
    if message1.encoding_chars.field_separator != message2.encoding_chars.field_separator:
        diff.add_structural_difference(
            f"Field separator mismatch: '{message1.encoding_chars.field_separator}' vs '{message2.encoding_chars.field_separator}'"
        )

    # Compare segment counts
    if len(message1.segments) != len(message2.segments):
        diff.add_structural_difference(
            f"Segment count mismatch: {len(message1.segments)} vs {len(message2.segments)}"
        )

    # Compare segments
    max_segments = max(len(message1.segments), len(message2.segments))
    for i in range(max_segments):
        if i >= len(message1.segments):
            diff.add_segment_difference(
                message2.segments[i].name, i, "<missing>", message2.segments[i].name
            )
            continue
        if i >= len(message2.segments):
            diff.add_segment_difference(
                message1.segments[i].name, i, message1.segments[i].name, "<missing>"
            )
            continue

        seg1 = message1.segments[i]
        seg2 = message2.segments[i]

        # Compare segment names
        if seg1.name != seg2.name:
            diff.add_segment_difference(seg1.name, i, seg1.name, seg2.name)
            continue

        # Compare fields in segment
        max_fields = max(len(seg1.fields), len(seg2.fields))
        for j in range(max_fields):
            field_idx = j + 1  # 1-based indexing

            if j >= len(seg1.fields):
                diff.add_field_difference(seg1.name, field_idx, "<missing>", seg2.fields[j].value())
                continue
            if j >= len(seg2.fields):
                diff.add_field_difference(seg1.name, field_idx, seg1.fields[j].value(), "<missing>")
                continue

            field1_value = seg1.fields[j].value()
            field2_value = seg2.fields[j].value()

            if field1_value != field2_value:
                diff.add_field_difference(seg1.name, field_idx, field1_value, field2_value)

    return diff


def format_diff(diff: MessageDiff, show_identical: bool = False) -> str:
    """
    Format MessageDiff as human-readable text.

    Args:
        diff: MessageDiff object
        show_identical: If True, show message even when messages are identical

    Returns:
        Formatted diff text
    """
    lines = []
    lines.append("HL7 v2 Message Comparison")
    lines.append("=" * 60)

    if diff.identical:
        lines.append("Messages are IDENTICAL")
        if not show_identical:
            return "\n".join(lines) + "\n"
    else:
        lines.append("Messages are DIFFERENT")
        lines.append("")

    # Structural differences
    if diff.structural_differences:
        lines.append("Structural Differences:")
        for diff_desc in diff.structural_differences:
            lines.append(f"  - {diff_desc}")
        lines.append("")

    # Segment differences
    if diff.segment_differences:
        lines.append("Segment Differences:")
        for seg_diff in diff.segment_differences:
            lines.append(
                f"  Position {seg_diff['position']}: {seg_diff['segment']}"
            )
            lines.append(f"    Message 1: {seg_diff['message1']}")
            lines.append(f"    Message 2: {seg_diff['message2']}")
        lines.append("")

    # Field differences
    if diff.field_differences:
        lines.append("Field Differences:")
        for field_diff in diff.field_differences:
            lines.append(
                f"  {field_diff['segment']}-{field_diff['field']}:"
            )
            lines.append(f"    Message 1: {field_diff['message1']}")
            lines.append(f"    Message 2: {field_diff['message2']}")
        lines.append("")

    # Summary
    lines.append("Summary:")
    lines.append(f"  Structural differences: {len(diff.structural_differences)}")
    lines.append(f"  Segment differences: {len(diff.segment_differences)}")
    lines.append(f"  Field differences: {len(diff.field_differences)}")

    return "\n".join(lines) + "\n"

