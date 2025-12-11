# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Streaming Parser.

Provides streaming parser for large HL7v2 messages that processes segments
incrementally without loading the entire message into memory.

This is useful for:
- Large messages that don't fit in memory
- Processing messages from files or network streams
- Memory-efficient message processing
"""

import re
from typing import Iterator, Optional, Callable, List
from datetime import datetime
import logging

from dnhealth.errors import HL7v2ParseError
from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)
from dnhealth.dnhealth_hl7v2.parser import (
    parse_segment,
    unescape_value,
)

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class StreamingParser:
    """
    Streaming parser for HL7 v2.x messages.
    
    Processes messages segment by segment without loading the entire message
    into memory. Useful for large messages or streaming data sources.
    """
    
    def __init__(
        self,
        segment_callback: Optional[Callable[[Segment], None]] = None,
        message_callback: Optional[Callable[[Message], None]] = None,
        tolerant: bool = False,
        timeout: int = TEST_TIMEOUT
    ):
        """
        Initialize streaming parser.
        
        Args:
            segment_callback: Optional callback function called for each parsed segment
            message_callback: Optional callback function called when a complete message is parsed
            tolerant: If True, attempt to parse malformed messages (default: False)
            timeout: Maximum time in seconds for parsing operations (default: 300)
        """
        self.segment_callback = segment_callback
        self.message_callback = message_callback
        self.tolerant = tolerant
        self.timeout = timeout
        self.start_time: Optional[float] = None
        self.encoding_chars: Optional[EncodingCharacters] = None
        self.version: Optional[str] = None
        self.segments: List[Segment] = []
        self.current_message_segments: List[Segment] = []
        self.buffer = ""
        
    def _check_timeout(self):
        """Check if parsing has exceeded timeout limit."""
        if self.start_time is None:
            return
        
        from time import time
        elapsed = time() - self.start_time
        if elapsed > self.timeout:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Streaming parser exceeded timeout of {self.timeout} seconds")
            raise HL7v2ParseError(f"Parsing exceeded timeout limit of {self.timeout} seconds")
    
    def _parse_msh_segment(self, msh_text: str) -> Segment:
        """
        Parse MSH segment and extract encoding characters.
        
        Args:
            msh_text: MSH segment text
            
        Returns:
            Parsed MSH segment
            
        Raises:
            HL7v2ParseError: If MSH segment cannot be parsed
        """
        if len(msh_text) < 4:
            raise HL7v2ParseError("MSH segment too short", line_number=1, segment="MSH")
        
        # Extract field separator (character after "MSH")
        field_separator = msh_text[3] if len(msh_text) > 3 else "|"
        
        # Parse MSH-2 (encoding characters)
        msh2_start = 4
        msh2_text = ""
        
        if len(msh_text) > msh2_start:
            # Find end of MSH-2 (next field separator)
            for i in range(msh2_start, len(msh_text)):
                if msh_text[i] == field_separator:
                    break
                msh2_text += msh_text[i]
        
        # Default encoding characters if MSH-2 is empty
        if len(msh2_text) < 4:
            msh2_text = "^~\\&"
        
        # Extract encoding characters
        component_separator = msh2_text[0] if len(msh2_text) > 0 else "^"
        repetition_separator = msh2_text[1] if len(msh2_text) > 1 else "~"
        escape_char = msh2_text[2] if len(msh2_text) > 2 else "\\"
        subcomponent_separator = msh2_text[3] if len(msh2_text) > 3 else "&"
        
        # Create encoding characters object
        self.encoding_chars = EncodingCharacters(
            field_separator=field_separator,
            component_separator=component_separator,
            repetition_separator=repetition_separator,
            escape_char=escape_char,
            subcomponent_separator=subcomponent_separator,
        )
        
        # Parse MSH segment using standard parser
        segment = parse_segment(msh_text, self.encoding_chars, tolerant=self.tolerant)
        
        # Extract version from MSH-12
        if len(segment.fields) >= 12:
            version_field = segment.field(12)
            if version_field.components:
                self.version = version_field.components[0].value()
        
        return segment
    
    def feed(self, data: str) -> Iterator[Segment]:
        """
        Feed data to the parser and yield parsed segments.
        
        Args:
            data: String data to parse (can be partial)
            
        Yields:
            Parsed Segment objects as they are completed
            
        Raises:
            HL7v2ParseError: If parsing fails
        """
        if self.start_time is None:
            from time import time
            self.start_time = time()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{current_time}] Starting streaming parser")
        
        # Add data to buffer
        self.buffer += data
        
        # Normalize line endings
        self.buffer = self.buffer.replace("\r\n", "\r").replace("\n", "\r")
        
        # Process complete segments (segments end with \r)
        while "\r" in self.buffer:
            # Check timeout
            self._check_timeout()
            
            # Extract segment (up to first \r)
            segment_end = self.buffer.find("\r")
            segment_text = self.buffer[:segment_end]
            self.buffer = self.buffer[segment_end + 1:]
            
            # Skip empty segments
            if not segment_text.strip():
                continue
            
            # Parse segment
            try:
                if segment_text.startswith("MSH"):
                    # MSH segment - extract encoding characters
                    segment = self._parse_msh_segment(segment_text)
                else:
                    # Other segments - use standard parser
                    if self.encoding_chars is None:
                        if self.tolerant:
                            # Try to use default encoding characters
                            self.encoding_chars = EncodingCharacters()
                        else:
                            raise HL7v2ParseError("MSH segment must be parsed first")
                    
                    segment = parse_segment(segment_text, self.encoding_chars, tolerant=self.tolerant)
                
                # Add to current message segments
                self.current_message_segments.append(segment)
                self.segments.append(segment)
                
                # Call segment callback if provided
                if self.segment_callback:
                    self.segment_callback(segment)
                
                # Yield segment
                yield segment
                
            except HL7v2ParseError as e:
                if self.tolerant:
                    # In tolerant mode, log error and continue
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Failed to parse segment (tolerant mode): {e}")
                    continue
                raise
        
        # Check timeout at end
        self._check_timeout()
    
    def finish(self) -> Optional[Message]:
        """
        Finish parsing and return complete message if available.
        
        Returns:
            Complete Message object if message is complete, None otherwise
            
        Raises:
            HL7v2ParseError: If message is incomplete or invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Process any remaining data in buffer
        if self.buffer.strip():
            # Try to parse remaining buffer as final segment
            try:
                if self.buffer.startswith("MSH"):
                    segment = self._parse_msh_segment(self.buffer)
                else:
                    if self.encoding_chars is None:
                        if self.tolerant:
                            self.encoding_chars = EncodingCharacters()
                        else:
                            raise HL7v2ParseError("MSH segment must be parsed first")
                    
                    segment = parse_segment(self.buffer, self.encoding_chars, tolerant=self.tolerant)
                
                self.current_message_segments.append(segment)
                self.segments.append(segment)
                
                if self.segment_callback:
                    self.segment_callback(segment)
                    
            except HL7v2ParseError as e:
                if not self.tolerant:
                    raise
                logger.warning(f"[{current_time}] Failed to parse final segment (tolerant mode): {e}")
        
        # Check if we have a complete message
        if not self.current_message_segments:
            logger.debug(f"[{current_time}] No segments parsed")
            return None
        
        # Verify MSH segment exists
        msh_segments = [s for s in self.current_message_segments if s.name == "MSH"]
        if not msh_segments:
            if self.tolerant:
                logger.warning(f"[{current_time}] No MSH segment found (tolerant mode)")
                return None
            raise HL7v2ParseError("Message must contain MSH segment")
        
        # Create message object
        message = Message(
            segments=self.current_message_segments.copy(),
            encoding_chars=self.encoding_chars or EncodingCharacters(),
            version=self.version
        )
        
        # Call message callback if provided
        if self.message_callback:
            self.message_callback(message)
        
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{elapsed_time}] Streaming parser finished: {len(self.current_message_segments)} segments parsed")
        
        return message
    
    def reset(self):
        """Reset parser state for parsing a new message."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Resetting streaming parser")
        
        self.start_time = None
        self.encoding_chars = None
        self.version = None
        self.segments = []
        self.current_message_segments = []
        self.buffer = ""


def parse_streaming(
    stream: Iterator[str],
    segment_callback: Optional[Callable[[Segment], None]] = None,
    message_callback: Optional[Callable[[Message], None]] = None,
    tolerant: bool = False,    timeout: int = TEST_TIMEOUT
) -> Iterator[Segment]:
    """
    Parse HL7v2 message from a stream of strings.
    
    Args:
        stream: Iterator yielding string chunks
        segment_callback: Optional callback function called for each parsed segment
        message_callback: Optional callback function called when a complete message is parsed
        tolerant: If True, attempt to parse malformed messages (default: False)
        timeout: Maximum time in seconds for parsing operations (default: 300)
        
    Yields:
        Parsed Segment objects as they are completed
        
    Raises:
        HL7v2ParseError: If parsing fails
        
    Example:
        >>> def process_segment(segment):
        ...     print(f"Parsed segment: {segment.name}")
        ...
        >>> with open("message.hl7", "r") as f:
        ...     chunks = iter(lambda: f.read(1024), "")
        ...     for segment in parse_streaming(chunks, segment_callback=process_segment):
        ...         # Process segment
        ...         pass
    """
    parser = StreamingParser(
        segment_callback=segment_callback,
        message_callback=message_callback,
        tolerant=tolerant,
        timeout=timeout
    )
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting stream parsing")
    
    try:
        for chunk in stream:
            for segment in parser.feed(chunk):
                yield segment
        
        # Finish parsing
        message = parser.finish()
        if message and message_callback:
            message_callback(message)
            
    finally:
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{elapsed_time}] Stream parsing completed")


def parse_file_streaming(
    file_path: str,
    chunk_size: int = 8192,
    segment_callback: Optional[Callable[[Segment], None]] = None,
    message_callback: Optional[Callable[[Message], None]] = None,
    tolerant: bool = False,
    timeout: int = TEST_TIMEOUT
) -> Iterator[Segment]:
    """
    Parse HL7v2 message from a file using streaming parser.
    
    Args:
        file_path: Path to HL7v2 message file
        chunk_size: Size of chunks to read from file (default: 8192 bytes)
        segment_callback: Optional callback function called for each parsed segment
        message_callback: Optional callback function called when a complete message is parsed
        tolerant: If True, attempt to parse malformed messages (default: False)
        timeout: Maximum time in seconds for parsing operations (default: 300)
        
    Yields:
        Parsed Segment objects as they are completed
        
    Raises:
        HL7v2ParseError: If parsing fails
        FileNotFoundError: If file does not exist
        
    Example:
        >>> for segment in parse_file_streaming("large_message.hl7"):
        ...     print(f"Parsed segment: {segment.name}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Starting file streaming parse: {file_path}")
    
    def read_chunks():
        """Generator function to read file in chunks."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    for segment in parse_streaming(
        read_chunks(),
        segment_callback=segment_callback,
        message_callback=message_callback,
        tolerant=tolerant,
        timeout=timeout
    ):
        yield segment
    
    elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{elapsed_time}] File streaming parse completed: {file_path}")
