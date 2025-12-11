# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x message model classes.

Represents the complete structure of an HL7 v2.x message:
Message -> Segment -> Field -> Component -> Subcomponent
"""

from typing import Dict, List, Optional
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
class EncodingCharacters:
    """
    Encoding characters extracted from MSH-2.

    HL7 v2 uses special characters to separate different parts of a message:
    - Field separator (default: |)
    - Component separator (default: ^)
    - Repetition separator (default: ~)
    - Escape character (default: \\)
    - Subcomponent separator (default: &)
    - Continuation character (from MSH-14, default: None)
    """

    def __init__(
        self,
        field_separator: str = "|",
        component_separator: str = "^",
        repetition_separator: str = "~",
        escape_character: str = "\\",
        subcomponent_separator: str = "&",
        continuation_character: Optional[str] = None,
    ):
        """
        Initialize encoding characters.

        Args:
            field_separator: Character separating fields (default: |)
            component_separator: Character separating components (default: ^)
            repetition_separator: Character separating repetitions (default: ~)
            escape_character: Escape character (default: \\)
            subcomponent_separator: Character separating subcomponents (default: &)
            continuation_character: Character indicating segment continuation (from MSH-14, default: None)
        """
        self.field_separator = field_separator
        self.component_separator = component_separator
        self.repetition_separator = repetition_separator
        self.escape_character = escape_character
        self.subcomponent_separator = subcomponent_separator
        self.continuation_character = continuation_character

    @classmethod
    def from_msh2(cls, msh2: str, msh14: Optional[str] = None) -> "EncodingCharacters":
        """
        Create EncodingCharacters from MSH-2 and MSH-14 field values.

        MSH-2 format: ^~\\& (component, repetition, escape, subcomponent)
        MSH-14 format: continuation character (optional)
        Field separator is always | and not included in MSH-2.

        Args:
            msh2: MSH-2 field value (e.g., "^~\\&")
            msh14: MSH-14 field value (continuation character, optional)

        Returns:
            EncodingCharacters instance
        """
        continuation_char = None
        if msh14:
            continuation_char = msh14.strip()
        
        if len(msh2) < 4:
            # Default encoding characters
            result = cls(continuation_character=continuation_char)
        else:
            result = cls(
                component_separator=msh2[0] if len(msh2) > 0 else "^",
                repetition_separator=msh2[1] if len(msh2) > 1 else "~",
                escape_character=msh2[2] if len(msh2) > 2 else "\\",
                subcomponent_separator=msh2[3] if len(msh2) > 3 else "&",
                continuation_character=continuation_char,
            )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"EncodingCharacters(field='{self.field_separator}', "
            f"component='{self.component_separator}', "
            f"repetition='{self.repetition_separator}', "
            f"escape='{self.escape_character}', "
            f"subcomponent='{self.subcomponent_separator}')"
        )


class Subcomponent:
    """Represents a subcomponent (lowest level of HL7 v2 structure)."""

    def __init__(self, value: str = ""):
        """
        Initialize subcomponent.

        Args:
            value: Subcomponent value (empty string if not present)
        """
        self.value = value

    def __repr__(self) -> str:
        """String representation."""
        return f"Subcomponent(value='{self.value}')"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Subcomponent):
            return False
        return self.value == other.value


class Component:
    """Represents a component (contains subcomponents)."""

    def __init__(self, subcomponents: Optional[List[Subcomponent]] = None):
        """
        Initialize component.

        Args:
            subcomponents: List of subcomponents (default: single empty subcomponent)
        """
        if subcomponents is None:
            subcomponents = [Subcomponent()]
        self.subcomponents = subcomponents

    def value(self) -> str:
        """
        Get the value of the first subcomponent (convenience method).


        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        Returns:
            Value of first subcomponent
        """
        return self.subcomponents[0].value if self.subcomponents else ""

    def __repr__(self) -> str:
        """String representation."""
        if len(self.subcomponents) == 1:
            return f"Component(value='{self.subcomponents[0].value}')"
        return f"Component(subcomponents={len(self.subcomponents)})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Component):
            return False

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self.subcomponents == other.subcomponents

    def component(self, index: int) -> Subcomponent:
        """
        Get subcomponent by index (1-based).

        Args:
            index: 1-based subcomponent index

        Returns:
            Subcomponent at index

        Raises:
            IndexError: If index is out of range
        """
        if index < 1 or index > len(self.subcomponents):
            raise IndexError(f"Subcomponent index {index} out of range (1-{len(self.subcomponents)})")
        return self.subcomponents[index - 1]


class Field:
    """
    Represents a field (contains components, supports repetition).
    
    A field can be empty (no value) or null (explicitly null).
    """

    def __init__(self, components: Optional[List[Component]] = None, is_null: bool = False):
        """
        Initialize field.

        Args:
            components: List of components (default: single empty component)
            is_null: True if field is explicitly null (double quotes '""' in HL7v2)
        """
        if components is None:
            components = [Component()]
        self.components = components
        self.is_null = is_null  # True if field is '""' (double quotes = null in HL7v2)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def value(self) -> str:
        """
        Get the value of the first component's first subcomponent (convenience method).

        Returns:
            Value string
        """
        return self.components[0].value() if self.components else ""

    def component(self, index: int) -> Component:
        """
        Get component by index (1-based).

        Args:
            index: 1-based component index

        Returns:
            Component at index

        Raises:
            IndexError: If index is out of range
        """
        if index < 1 or index > len(self.components):
            raise IndexError(f"Component index {index} out of range (1-{len(self.components)})")
        return self.components[index - 1]

    def __repr__(self) -> str:
        """String representation."""
        if len(self.components) == 1:
            return f"Field(value='{self.components[0].value()}')"
        return f"Field(components={len(self.components)})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Field):
            return False
        return self.components == other.components


class Segment:
    """
    Represents an HL7 v2 segment (3-character name + ordered fields).
    
    Fields can have repetitions, which are stored as lists of Field objects.
    """

    def __init__(self, name: str, fields: Optional[List[Field]] = None, field_repetitions: Optional[List[List[Field]]] = None, original_field_count: Optional[int] = None):
        """
        Initialize segment.

        Args:
            name: Segment name (3 characters, e.g., "MSH", "PID")
            fields: List of fields (1-based indexing) - first repetition of each field
            field_repetitions: List of field repetition lists - all repetitions for each field position
                              If provided, takes precedence over fields parameter
            original_field_count: Original number of fields from parsed message (for preserving formatting)
        """
        if len(name) != 3:
            raise ValueError(f"Segment name must be 3 characters, got: {name}")
        self.name = name
        
        if field_repetitions is not None:
            # Store all repetitions for each field position
            self._field_repetitions = field_repetitions
            # For backward compatibility, fields contains first repetition of each field
            self.fields = [reps[0] if reps else Field() for reps in field_repetitions]
        else:
            # Legacy mode: single repetition per field
            self.fields = fields if fields is not None else []
            self._field_repetitions = [[field] for field in self.fields] if self.fields else []
        
        # Track original field count for preserving formatting
        self._original_field_count = original_field_count if original_field_count is not None else len(self._field_repetitions)

    def field(self, index: int, repetition: int = 1) -> Field:
        """
        Get field by index (1-based) and optional repetition (1-based).

        Args:
            index: 1-based field index
            repetition: 1-based repetition index (default: 1)

        Returns:
            Field at index and repetition

        Raises:
            IndexError: If index or repetition is out of range

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        """
        if index < 1:
            raise IndexError(f"Field index must be >= 1, got: {index}")
        if repetition < 1:
            raise IndexError(f"Repetition index must be >= 1, got: {repetition}")
        
        if index > len(self._field_repetitions):
            # Return empty field if index is beyond available fields
            return Field()
        
        repetitions = self._field_repetitions[index - 1]
        if repetition > len(repetitions):
            # Return empty field if repetition is beyond available repetitions
            return Field()
        
        return repetitions[repetition - 1]

    def get_field_repetitions(self, index: int) -> List[Field]:
        """
        Get all repetitions of a field by index (1-based).

        Args:
            index: 1-based field index

        Returns:
            List of Field objects (all repetitions)
        """
        if index < 1 or index > len(self._field_repetitions):
            return []
        return self._field_repetitions[index - 1]

    def __repr__(self) -> str:
        """String representation."""
        return f"Segment(name='{self.name}', fields={len(self.fields)})"

    def __eq__(self, other: object) -> bool:
        """String representation."""
        return f"Segment(name='{self.name}', fields={len(self.fields)})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Segment):
            return False

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self.name == other.name and self._field_repetitions == other._field_repetitions


class SegmentGroup:
    """
    Represents a group of segments in HL7 v2.x.
    
    Segment groups are used to organize related segments together,
    especially for repeating groups (e.g., OBR + OBX groups in ORU messages).
    """

    def __init__(self, segments: Optional[List[Segment]] = None, group_id: Optional[str] = None):
        """
        Initialize segment group.
        
        Args:
            segments: List of segments in this group
            group_id: Optional identifier for the group (e.g., "PATIENT_RESULT")
        """
        self.segments = segments if segments is not None else []
        self.group_id = group_id
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def get_segments(self, name: str) -> List[Segment]:
        """
        Get all segments with the given name from this group.
        
        Args:
            name: Segment name (3 characters)
            
        Returns:
            List of matching segments
        """
        return [seg for seg in self.segments if seg.name == name]

    def add_segment(self, segment: Segment):
        """
        Add a segment to this group.
        
        Args:
            segment: Segment to add
        """
        self.segments.append(segment)

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def __repr__(self) -> str:
        """String representation."""
        group_info = f", group_id='{self.group_id}'" if self.group_id else ""
        return f"SegmentGroup(segments={len(self.segments)}{group_info})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, SegmentGroup):
            return False
        return self.segments == other.segments and self.group_id == other.group_id


class Message:
    """
    Represents a complete HL7 v2.x message.

    Contains ordered segments and metadata (encoding characters, version).
    Supports both flat segment lists and segment groups.
    """

    def __init__(
        self,
        segments: Optional[List[Segment]] = None,
        encoding_chars: Optional[EncodingCharacters] = None,
        version: Optional[str] = None,
        groups: Optional[List[SegmentGroup]] = None,
    ):
        """

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
        Initialize message.

        Args:
            segments: Ordered list of segments (flat structure)
            encoding_chars: Encoding characters (default: standard)
            version: HL7 version (e.g., "2.5") extracted from MSH-12
            groups: Optional list of segment groups (for hierarchical structure)
        """
        self.segments = segments if segments is not None else []
        self.encoding_chars = encoding_chars or EncodingCharacters()
        self.version = version
        self.groups = groups if groups is not None else []

    def get_segments(self, name: str) -> List[Segment]:
        """
        Get all segments with the given name (from flat structure).

        Args:
            name: Segment name (3 characters)

        Returns:
            List of matching segments
        """
        result = [seg for seg in self.segments if seg.name == name]
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result

    def get_segments_from_groups(self, name: str) -> List[Segment]:
        """
        Get all segments with the given name from all groups.

        Args:
            name: Segment name (3 characters)


            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        Returns:
            List of matching segments from all groups
        """
        result = []
        for group in self.groups:
            result.extend(group.get_segments(name))

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result

    def get_all_segments(self, name: str) -> List[Segment]:
        """
        Get all segments with the given name from both flat structure and groups.

        Args:
            name: Segment name (3 characters)

        Returns:
            List of matching segments from both flat structure and groups
        """
        result = self.get_segments(name)
        result.extend(self.get_segments_from_groups(name))
        return result

    def add_group(self, group: SegmentGroup):
        """
        Add a segment group to the message.

        Args:
            group: Segment group to add
        """
        self.groups.append(group)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def flatten_segments(self) -> List[Segment]:
        """
        Get all segments in order (flat structure).
        
        Combines segments from flat structure and groups.
        Groups are flattened in order.
        
        Returns:
            List of all segments in order
        """
        result = list(self.segments)
        for group in self.groups:
            result.extend(group.segments)
        return result

    def __getitem__(self, name: str) -> List[Segment]:
        """
        Get segments by name (convenience method).
        Uses get_all_segments to include both flat and grouped segments.

        Args:
            name: Segment name

        Returns:
            List of matching segments
        """
        return self.get_all_segments(name)

    def __repr__(self) -> str:
        """String representation."""
        groups_info = f", groups={len(self.groups)}" if self.groups else ""
        return f"Message(segments={len(self.segments)}{groups_info}, version={self.version})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Message):
            return False
        return (
            self.segments == other.segments
            and self.encoding_chars == other.encoding_chars
            and self.version == other.version
            and self.groups == other.groups
        )

