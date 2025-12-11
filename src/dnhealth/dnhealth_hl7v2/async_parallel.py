# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Async/Await Parallel Processing Support.

Provides async/await support for parallel processing of HL7v2 messages
using Python's asyncio module.

This is useful for:
- Async/await-based applications
- High-throughput message processing
- Integration with async web frameworks
- Non-blocking I/O operations
"""

import asyncio
import time
from typing import List, Optional, Callable, Iterator, Dict, Any, Union, AsyncIterator
from datetime import datetime
import logging

from dnhealth.errors import HL7v2ParseError
from dnhealth.dnhealth_hl7v2.parser import parse_hl7v2
from dnhealth.dnhealth_hl7v2.model import Message

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


async def parse_message_async(
    message_text: str,    tolerant: bool = False
) -> Message:
    """
    Parse a single HL7v2 message asynchronously.
    
    Args:
        message_text: HL7v2 message text to parse
        tolerant: If True, attempt to parse malformed messages
        
    Returns:
        Parsed Message object
        
    Raises:
        HL7v2ParseError: If message cannot be parsed
        
    Example:
        >>> async def main():
        ...     message = await parse_message_async("MSH|^~\\&|...")
        ...     print(message.message_type())
    """
    # Run parsing in executor to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: parse_hl7v2(message_text, tolerant=tolerant)
    )


async def parse_messages_async(    messages: List[str],
    max_concurrent: Optional[int] = None,
    tolerant: bool = False,
    timeout: int = TEST_TIMEOUT,
    callback: Optional[Callable[[Message, int], None]] = None
) -> List[Union[Message, Exception]]:
    """
    Parse multiple HL7v2 messages concurrently using async/await.
    
    Args:
        messages: List of HL7v2 message strings to parse
        max_concurrent: Maximum number of concurrent parsing tasks (default: None = unlimited)
        tolerant: If True, attempt to parse malformed messages (default: False)
        timeout: Maximum time in seconds for parsing all messages (default: 300)
        callback: Optional async callback function called for each parsed message
                  Signature: callback(message: Message, index: int) -> None
                  
    Returns:
        List of parsed Message objects or Exception objects if parsing failed.
        Results are in the same order as input messages.
        
    Raises:
        TimeoutError: If parsing exceeds timeout limit
        asyncio.TimeoutError: If individual tasks exceed timeout
        
    Example:
        >>> async def main():
        ...     messages = ["MSH|^~\\&|...", "MSH|^~\\&|..."]
        ...     results = await parse_messages_async(messages, max_concurrent=4)
        ...     for result in results:
        ...         if isinstance(result, Message):
        ...             print(f"Parsed: {result.message_type()}")
        ...         else:
        ...             print(f"Error: {result}")
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting async parsing of {len(messages)} messages")
    
    if not messages:
        return []
    
    # Check timeout before starting
    elapsed = time.time() - start_time
    if elapsed > timeout:
        raise TimeoutError(f"Operation exceeded timeout of {timeout} seconds")
    
    # Create semaphore to limit concurrency if specified
    semaphore = asyncio.Semaphore(max_concurrent) if max_concurrent else None

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    async def parse_with_semaphore(index: int, message_text: str) -> tuple[int, Union[Message, Exception]]:
        """Parse a single message with semaphore control."""
        if semaphore:
            async with semaphore:
                return await _parse_single_async(index, message_text, tolerant, callback)
        else:
            return await _parse_single_async(index, message_text, tolerant, callback)
    
    # Create tasks for all messages
    tasks = [
        parse_with_semaphore(i, msg)
        for i, msg in enumerate(messages)
    ]
    
    # Wait for all tasks with timeout
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        elapsed = time.time() - start_time
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{elapsed_time}] Async parsing exceeded timeout of {timeout} seconds after {elapsed:.3f}s")
        raise TimeoutError(f"Async parsing exceeded timeout of {timeout} seconds")
    
    # Sort results by index to maintain order
    sorted_results = sorted(results, key=lambda x: x[0] if isinstance(x, tuple) else -1)
    parsed_results = [result[1] if isinstance(result, tuple) else result for result in sorted_results]

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    elapsed = time.time() - start_time
    elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{elapsed_time}] Async parsing completed: {len(messages)} messages in {elapsed:.3f}s")
    
    return parsed_results


async def _parse_single_async(
    index: int,
    message_text: str,
    tolerant: bool,
    callback: Optional[Callable[[Message, int], None]]
) -> tuple[int, Union[Message, Exception]]:
    """Parse a single message and handle callback."""
    try:
        message = await parse_message_async(message_text, tolerant)
        
        if callback:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(message, index)

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
                else:
                    callback(message, index)
            except Exception as e:
                logger.warning(f"Callback failed for message {index}: {e}")
        
        return (index, message)
    except Exception as e:
        logger.error(f"Failed to parse message {index}: {e}")
        return (index, e)


async def parse_messages_async_stream(
    message_stream: AsyncIterator[str],
    max_concurrent: Optional[int] = None,
    tolerant: bool = False,
    timeout: int = TEST_TIMEOUT,
    callback: Optional[Callable[[Message, int], None]] = None
) -> AsyncIterator[Union[Message, Exception]]:
    """
    Parse a stream of HL7v2 messages concurrently using async/await.
    
    Args:
        message_stream: AsyncIterator yielding HL7v2 message strings
        max_concurrent: Maximum number of concurrent parsing tasks (default: None = unlimited)
        tolerant: If True, attempt to parse malformed messages (default: False)
        timeout: Maximum time in seconds for parsing (default: 300)
        callback: Optional async callback function called for each parsed message
                  Signature: callback(message: Message, index: int) -> None
                  
    Yields:
        Parsed Message objects or Exception objects as they are completed
        
    Example:
        >>> async def message_generator():
        ...     yield "MSH|^~\\&|..."
        ...     yield "MSH|^~\\&|..."
        ...
        >>> async def main():
        ...     async for result in parse_messages_async_stream(message_generator()):
        ...         if isinstance(result, Message):
        ...             print(f"Parsed: {result.message_type()}")
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting async stream parsing")
    
    semaphore = asyncio.Semaphore(max_concurrent) if max_concurrent else None
    index = 0
    pending_tasks: Dict[asyncio.Task, int] = {}
    
    try:
        async for message_text in message_stream:
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > timeout:
                elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{elapsed_time}] Async stream parsing exceeded timeout of {timeout} seconds")
                raise TimeoutError(f"Async stream parsing exceeded timeout of {timeout} seconds")
            
            current_index = index
            index += 1
            
            async def parse_task(msg: str, idx: int):
                """Parse task with semaphore control."""
                if semaphore:
                    async with semaphore:
                        return await _parse_single_async(idx, msg, tolerant, callback)
                else:
                    return await _parse_single_async(idx, msg, tolerant, callback)
            
            task = asyncio.create_task(parse_task(message_text, current_index))
            pending_tasks[task] = current_index
            
            # Yield completed tasks
            while pending_tasks:
                done, pending = await asyncio.wait(
                    pending_tasks.keys(),
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=0.1
                )
                
                for task in done:
                    idx = pending_tasks.pop(task)
                    try:
                        result = await task
                        if isinstance(result, tuple):
                            yield result[1]
                        else:
                            yield result
                    except Exception as e:
                        logger.error(f"Error processing task {idx}: {e}")
                        yield e
                
                if not done:
                    break
        
        # Wait for remaining tasks
        if pending_tasks:
            for task in asyncio.as_completed(pending_tasks.keys()):
                try:
                    result = await task
                    if isinstance(result, tuple):
                        yield result[1]
                    else:

                        # Log completion timestamp at end of operation
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logger.info(f"Current Time at End of Operations: {current_time}")
                        yield result
                except Exception as e:
                    idx = pending_tasks.get(task, -1)
                    logger.error(f"Error processing remaining task {idx}: {e}")
                    yield e
        
        elapsed = time.time() - start_time
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{elapsed_time}] Async stream parsing completed in {elapsed:.3f}s")
        
    except Exception as e:
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{elapsed_time}] Error in async stream parsing: {e}")
        raise


async def validate_messages_async(
    messages: List[Message],
    max_concurrent: Optional[int] = None,
    timeout: int = TEST_TIMEOUT,
    validation_callback: Optional[Callable[[Message, List[str]], None]] = None
) -> List[Dict[str, Any]]:
    """
    Validate multiple HL7v2 messages concurrently using async/await.
    
    Args:
        messages: List of Message objects to validate
        max_concurrent: Maximum number of concurrent validation tasks (default: None = unlimited)
        timeout: Maximum time in seconds for validation (default: 300)
        validation_callback: Optional async callback function called for each validation result
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
    logger.info(f"[{current_time}] Starting async validation of {len(messages)} messages")
    
    if not messages:
        return []
    
    async def validate_single(message: Message, index: int) -> tuple[int, Dict[str, Any]]:
        """Validate a single message."""
        loop = asyncio.get_event_loop()
        is_valid, errors, warnings = await loop.run_in_executor(
            None,
            lambda: validate_message(message)
        )
        
        result = {
            'message': message,
            'is_valid': is_valid,

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
            'errors': errors,
            'warnings': warnings
        }
        
        if validation_callback:
            try:
                if asyncio.iscoroutinefunction(validation_callback):
                    await validation_callback(message, errors)
                else:
                    validation_callback(message, errors)
            except Exception as e:
                logger.warning(f"Validation callback failed for message {index}: {e}")
        
        return (index, result)
    
    semaphore = asyncio.Semaphore(max_concurrent) if max_concurrent else None
    
    async def validate_with_semaphore(msg: Message, idx: int) -> tuple[int, Dict[str, Any]]:
        """Validate with semaphore control."""
        if semaphore:
            async with semaphore:
                return await validate_single(msg, idx)
        else:
            return await validate_single(msg, idx)
    
    tasks = [
        validate_with_semaphore(msg, i)
        for i, msg in enumerate(messages)
    ]
    
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        elapsed = time.time() - start_time
        elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{elapsed_time}] Async validation exceeded timeout of {timeout} seconds after {elapsed:.3f}s")
        raise TimeoutError(f"Async validation exceeded timeout of {timeout} seconds")
    
    # Sort results by index to maintain order
    sorted_results = sorted(results, key=lambda x: x[0] if isinstance(x, tuple) else -1)
    validation_results = [
        result[1] if isinstance(result, tuple) and isinstance(result[1], dict) else {
            'message': messages[i] if i < len(messages) else None,
            'is_valid': False,
            'errors': [str(result)] if not isinstance(result, tuple) else [],
            'warnings': []
        }
        for i, result in enumerate(sorted_results)
    ]
    
    elapsed = time.time() - start_time
    elapsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{elapsed_time}] Async validation completed: {len(messages)} messages in {elapsed:.3f}s")
    
    return validation_results
