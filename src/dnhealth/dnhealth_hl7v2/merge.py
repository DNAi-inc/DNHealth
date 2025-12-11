# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message merging utilities.

Provides functions to merge multiple HL7v2 messages into a single message.
"""

from typing import List, Optional

from dnhealth.dnhealth_hl7v2.model import Message, Segment
import logging
from datetime import datetime



logger = logging.getLogger(__name__)


def merge_messages(
    messages: List[Message],
    merge_strategy: str = "append",
    preserve_msh: bool = True,
) -> Message:
    """
    Merge multiple HL7v2 messages into a single message.

    Args:
        messages: List of Message objects to merge
        merge_strategy: Strategy for merging segments:
            - "append": Append all segments from all messages
            - "unique": Only append segments not already present (by name)
            - "replace": Replace segments with same name (keep last)
        preserve_msh: If True, use MSH from first message; if False, create new MSH

    Returns:
        Merged Message object

    Raises:
        ValueError: If messages list is empty or merge_strategy is invalid
    """
    if not messages:
        raise ValueError("Cannot merge empty list of messages")

    valid_strategies = {"append", "unique", "replace"}
    if merge_strategy not in valid_strategies:
        raise ValueError(f"Invalid merge_strategy: {merge_strategy}. Must be one of {valid_strategies}")

    # Use first message as base
    base_message = messages[0]
    
    # Determine MSH segment
    if preserve_msh:
        msh_segment = base_message.get_segments("MSH")[0] if base_message.get_segments("MSH") else None
    else:
        # Create a new MSH from first message but update timestamp
        msh_segment = base_message.get_segments("MSH")[0] if base_message.get_segments("MSH") else None
    
    # Collect all segments
    all_segments: List[Segment] = []
    seen_segment_names: set = set()
    
    # Process each message
    for msg_idx, msg in enumerate(messages):
        # Skip MSH segments (we'll add it separately)
        for segment in msg.segments:
            if segment.name == "MSH":
                continue
            
            if merge_strategy == "append":
                # Always append
                all_segments.append(segment)
            elif merge_strategy == "unique":
                # Only append if segment name not seen before
                if segment.name not in seen_segment_names:
                    all_segments.append(segment)
                    seen_segment_names.add(segment.name)
            elif merge_strategy == "replace":
                # Remove existing segments with same name, then append
                all_segments = [s for s in all_segments if s.name != segment.name]
                all_segments.append(segment)
                seen_segment_names.add(segment.name)
    
    # Prepend MSH segment if we have one
    if msh_segment:
        all_segments.insert(0, msh_segment)
    
    # Create merged message
    merged_message = Message(
        segments=all_segments,
        encoding_chars=base_message.encoding_chars,
        version=base_message.version,
    )
    

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return merged_message


def merge_messages_by_segment_type(
    messages: List[Message],
    segment_types: Optional[List[str]] = None,
) -> Message:
    """
    Merge messages, keeping only specified segment types.

    Args:
        messages: List of Message objects to merge
        segment_types: List of segment type names to keep (e.g., ["PID", "PV1"]).
                      If None, keeps all segments except MSH (uses first message's MSH).

    Returns:
        Merged Message object with filtered segments
    """
    if not messages:
        raise ValueError("Cannot merge empty list of messages")

    base_message = messages[0]
    msh_segment = base_message.get_segments("MSH")[0] if base_message.get_segments("MSH") else None
    
    # Collect segments
    all_segments: List[Segment] = []
    
    if segment_types is None:
        # Keep all segments except MSH
        segment_types_set = None
    else:
        segment_types_set = set(segment_types)
    
    for msg in messages:
        for segment in msg.segments:
            if segment.name == "MSH":
                continue
            
            if segment_types_set is None or segment.name in segment_types_set:
                all_segments.append(segment)
    
    # Prepend MSH
    if msh_segment:
        all_segments.insert(0, msh_segment)
    
    merged_message = Message(
        segments=all_segments,
        encoding_chars=base_message.encoding_chars,
        version=base_message.version,
    )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return merged_message

