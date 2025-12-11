# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Parallel Processing Support.

Provides parallel processing capabilities for parsing multiple HL7v2 messages
concurrently using Python's concurrent.futures module.

This is useful for:
- Batch processing multiple messages
- High-throughput message parsing
- Processing messages from multiple sources concurrently
"""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Optional, Callable, Iterator, Dict, Any, Union
from datetime import datetime
import logging

from dnhealth.errors import HL7v2ParseError
from dnhealth.dnhealth_hl7v2.parser import parse_hl7v2
from dnhealth.dnhealth_hl7v2.model import Message

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def _parse_message_wrapper(message_text: str, tolerant: bool = False) -> Message:
    """
    Wrapper function for parsing a single message.
    
    This function is used by ProcessPoolExecutor which requires
    a picklable function at module level.
    
    Args:
        message_text: HL7v2 message text to parse
        tolerant: If True, attempt to parse malformed messages
        
    Returns:
        Parsed Message object
        
    Raises:
        HL7v2ParseError: If message cannot be parsed
    """

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return parse_hl7v2(message_text, tolerant=tolerant)


def parse_messages_parallel(
    messages: List[str],
    max_workers: Optional[int] = None,
    use_processes: bool = False,
    tolerant: bool = False,
    timeout: int = TEST_TIMEOUT,
    callback: Optional[Callable[[Message, int], None]] = None
) -> List[Union[Message, Exception]]:
    """
    Parse multiple HL7v2 messages in parallel.
    
    Uses ThreadPoolExecutor (default) or ProcessPoolExecutor for parallel
    processing. ThreadPoolExecutor is generally faster for I/O-bound tasks
    like parsing, while ProcessPoolExecutor can be better for CPU-bound tasks.
    
    Args:
        messages: List of HL7v2 message strings to parse
        max_workers: Maximum number of worker threads/processes (default: None = auto)
        use_processes: If True, use ProcessPoolExecutor instead of ThreadPoolExecutor
        tolerant: If True, attempt to parse malformed messages (default: False)
        timeout: Maximum time in seconds for parsing all messages (default: 300)
        callback: Optional callback function called for each parsed message
                  Signature: callback(message: Message, index: int) -> None
                  
    Returns:
        List of parsed Message objects or Exception objects if parsing failed.
        Results are in the same order as input messages.
        
    Raises:
        TimeoutError: If parsing exceeds timeout limit
        
    Example:
        >>> messages = ["MSH|^~\\&|...", "MSH|^~\\&|..."]
        >>> results = parse_messages_parallel(messages, max_workers=4)
        >>> for result in results:
        ...     if isinstance(result, Message):
        ...         print(f"Parsed: {result.message_type()}")
        ...     else:
        ...         print(f"Error: {result}")
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting parallel parsing of {len(messages)} messages")
    
    if not messages:
        return []
    
    # Check timeout before starting
    elapsed = time.time() - start_time
    if elapsed > timeout:
        raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
    
    # Determine executor type
    executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    
    # Results dictionary to maintain order
    results: Dict[int, Union[Message, Exception]] = {}
    
    try:
        with executor_class(max_workers=max_workers) as executor:
            # Submit all parsing tasks
            future_to_index = {}
            for index, message_text in enumerate(messages):
                # Check timeout before submitting
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
                
                if use_processes:
                    # ProcessPoolExecutor requires picklable function
                    future = executor.submit(_parse_message_wrapper, message_text, tolerant)
                else:
                    # ThreadPoolExecutor can use lambda
                    future = executor.submit(parse_hl7v2, message_text, tolerant)
                
                future_to_index[future] = index
            
            # Collect results as they complete
            for future in as_completed(future_to_index, timeout=timeout - elapsed):
                index = future_to_index[future]
                
                # Check timeout during processing
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    # Cancel remaining futures
                    for f in future_to_index:
                        if not f.done():
                            f.cancel()
                    raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
                
                try:
                    message = future.result(timeout=1.0)  # Individual task timeout
                    results[index] = message
                    
                    # Call callback if provided
                    if callback:
                        try:
                            callback(message, index)
                        except Exception as e:
                            logger.warning(f"Callback failed for message {index}: {e}")
                            
                except Exception as e:
                    logger.error(f"Failed to parse message {index}: {e}")
                    results[index] = e
            
            # Build ordered results list
            ordered_results = [results[i] for i in range(len(messages))]
            
    except TimeoutError:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Parallel parsing exceeded timeout of {timeout} seconds (elapsed: {elapsed:.2f}s)")
        raise
    except Exception as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Parallel parsing failed: {e} (elapsed: {elapsed:.2f}s)")
        raise
    
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Parallel parsing completed: {len(messages)} messages in {elapsed:.2f}s")
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return ordered_results


def parse_messages_streaming_parallel(
    message_stream: Iterator[str],
    max_workers: Optional[int] = None,
    use_processes: bool = False,
    tolerant: bool = False,
    timeout: int = TEST_TIMEOUT,
    batch_size: int = 100,
    callback: Optional[Callable[[Message, int], None]] = None
) -> Iterator[Union[Message, Exception]]:
    """
    Parse HL7v2 messages from a stream in parallel batches.
    
    Processes messages in batches for efficient parallel processing.
    Useful for processing large streams of messages.
    
    Args:
        message_stream: Iterator yielding HL7v2 message strings
        max_workers: Maximum number of worker threads/processes (default: None = auto)
        use_processes: If True, use ProcessPoolExecutor instead of ThreadPoolExecutor
        tolerant: If True, attempt to parse malformed messages (default: False)
        timeout: Maximum time in seconds for parsing all messages (default: 300)
        batch_size: Number of messages to process in each batch (default: 100)
        callback: Optional callback function called for each parsed message
                  Signature: callback(message: Message, index: int) -> None
                  
    Yields:
        Parsed Message objects or Exception objects if parsing failed.
        Results are yielded as they become available (not necessarily in order).
        
    Raises:
        TimeoutError: If parsing exceeds timeout limit
        
    Example:
        >>> def message_generator():
        ...     yield "MSH|^~\\&|..."
        ...     yield "MSH|^~\\&|..."
        ...
        >>> for result in parse_messages_streaming_parallel(message_generator()):
        ...     if isinstance(result, Message):
        ...         print(f"Parsed: {result.message_type()}")
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting streaming parallel parsing")
    
    batch = []
    batch_index = 0
    
    try:
        for message_text in message_stream:
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
            
            batch.append(message_text)
            
            # Process batch when it reaches batch_size
            if len(batch) >= batch_size:
                batch_start_time = time.time()
                results = parse_messages_parallel(
                    batch,
                    max_workers=max_workers,
                    use_processes=use_processes,
                    tolerant=tolerant,
                    timeout=timeout - elapsed,
                    callback=callback
                )
                
                # Yield results
                for result in results:
                    yield result
                
                batch_elapsed = time.time() - batch_start_time
                logger.debug(f"Processed batch {batch_index} ({len(batch)} messages) in {batch_elapsed:.2f}s")
                
                batch = []
                batch_index += 1
        
        # Process remaining messages in final batch
        if batch:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
            
            results = parse_messages_parallel(
                batch,
                max_workers=max_workers,
                use_processes=use_processes,
                tolerant=tolerant,
                timeout=timeout - elapsed,
                callback=callback
            )
            
            for result in results:
                yield result
        
    except TimeoutError:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Streaming parallel parsing exceeded timeout of {timeout} seconds (elapsed: {elapsed:.2f}s)")
        raise
    except Exception as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Streaming parallel parsing failed: {e} (elapsed: {elapsed:.2f}s)")
        raise
    
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Streaming parallel parsing completed in {elapsed:.2f}s")


def validate_messages_parallel(
    messages: List[Message],
    max_workers: Optional[int] = None,
    use_processes: bool = False,
    timeout: int = TEST_TIMEOUT,
    validation_callback: Optional[Callable[[Message, List[str]], None]] = None
) -> List[Dict[str, Any]]:
    """
    Validate multiple HL7v2 messages in parallel.
    
    Args:
        messages: List of Message objects to validate
        max_workers: Maximum number of worker threads/processes (default: None = auto)
        use_processes: If True, use ProcessPoolExecutor instead of ThreadPoolExecutor
        timeout: Maximum time in seconds for validation (default: 300)
        validation_callback: Optional callback function called for each validation result
                            Signature: callback(message: Message, errors: List[str]) -> None
                            
    Returns:
        List of validation result dictionaries, each containing:
        - 'message': Message object
        - 'is_valid': bool
        - 'errors': List[str]
        - 'warnings': List[str]
        
    Raises:
        TimeoutError: If validation exceeds timeout limit
    """
    from dnhealth.dnhealth_hl7v2.message_validation import validate_message
    
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting parallel validation of {len(messages)} messages")
    
    if not messages:
        return []
    
    def _validate_wrapper(message: Message) -> Dict[str, Any]:
        """Wrapper function for validation."""
        is_valid, errors, warnings = validate_message(message)
        return {
            'message': message,
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings
        }
    
    executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    results: Dict[int, Dict[str, Any]] = {}
    
    try:
        with executor_class(max_workers=max_workers) as executor:
            future_to_index = {}
            for index, message in enumerate(messages):
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
                
                future = executor.submit(_validate_wrapper, message)
                future_to_index[future] = index
            
            for future in as_completed(future_to_index, timeout=timeout - elapsed):
                index = future_to_index[future]
                
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    for f in future_to_index:
                        if not f.done():
                            f.cancel()
                    raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
                
                try:
                    result = future.result(timeout=1.0)
                    results[index] = result
                    
                    if validation_callback:
                        try:
                            validation_callback(result['message'], result['errors'])
                        except Exception as e:
                            logger.warning(f"Validation callback failed for message {index}: {e}")
                            
                except Exception as e:
                    logger.error(f"Failed to validate message {index}: {e}")
                    results[index] = {
                        'message': messages[index],
                        'is_valid': False,
                        'errors': [str(e)],
                        'warnings': []
                    }
            
            ordered_results = [results[i] for i in range(len(messages))]
            
    except TimeoutError:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Parallel validation exceeded timeout of {timeout} seconds (elapsed: {elapsed:.2f}s)")
        raise
    except Exception as e:
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Parallel validation failed: {e} (elapsed: {elapsed:.2f}s)")
        raise
    
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Parallel validation completed: {len(messages)} messages in {elapsed:.2f}s")
    
    return ordered_results
