# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Batch processing utilities for FHIR resources.
logger = logging.getLogger(__name__)

Provides utilities for processing multiple FHIR resources in batches,
including parsing, validation, and serialization operations.
Includes timestamp tracking for all operations.
"""

from datetime import datetime
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar, Union

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.parser_json import parse_fhir_json
from dnhealth.dnhealth_fhir.serializer_json import serialize_fhir_json
from dnhealth.util.logging import get_logger

T = TypeVar("T", bound=FHIRResource)

logger = get_logger(__name__)


def process_resources_batch(
    resources: List[Union[str, FHIRResource]],
    processor: Callable[[FHIRResource], Any],
    batch_size: int = 100,    fail_on_error: bool = False,
) -> List[Any]:
    """
    Process multiple FHIR resources in batches.

    Args:
        resources: List of resource JSON strings or parsed resource objects
        processor: Function to process each resource (takes resource, returns result)
        batch_size: Number of resources to process per batch (default: 100)
        fail_on_error: If True, raise exception on first error; if False, continue

    Returns:
        List of processor results

    Raises:
        Exception: If fail_on_error=True and processing fails
    """
    results = []
    total = len(resources)
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting batch processing of {total} resources (batch_size={batch_size})")

    for batch_idx in range(0, total, batch_size):
        batch = resources[batch_idx : batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processing batch {batch_num}/{total_batches} ({len(batch)} resources)")

        for idx, resource_input in enumerate(batch):
            try:
                # Parse if string, otherwise use as-is
                if isinstance(resource_input, str):
                    resource = parse_fhir_json(resource_input)
                else:
                    resource = resource_input

                # Process resource
                result = processor(resource)
                results.append(result)

            except Exception as e:
                logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error processing resource {batch_idx + idx + 1}/{total}: {e}")
                if fail_on_error:
                    raise
                results.append(None)

        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Completed batch {batch_num}/{total_batches}")

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Batch processing completed: {len(results)} results")

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return results


def parse_resources_batch(
    json_strings: List[str],
    resource_type: Optional[type] = None,
    batch_size: int = 100,
    fail_on_error: bool = False,
) -> List[Optional[FHIRResource]]:
    """
    Parse multiple FHIR JSON strings in batches.

    Args:
        json_strings: List of FHIR JSON strings
        resource_type: Optional resource type hint
        batch_size: Number of resources to parse per batch (default: 100)
        fail_on_error: If True, raise exception on first error; if False, continue

    Returns:
        List of parsed resources (None for failed parses if fail_on_error=False)

    Raises:
        Exception: If fail_on_error=True and parsing fails
    """
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting batch parsing of {len(json_strings)} JSON strings")

    def parse_resource(json_str: str) -> FHIRResource:
        return parse_fhir_json(json_str, resource_type=resource_type)

    results = []
    total = len(json_strings)

    for batch_idx in range(0, total, batch_size):
        batch = json_strings[batch_idx : batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size

        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Parsing batch {batch_num}/{total_batches} ({len(batch)} resources)")

        for idx, json_str in enumerate(batch):
            try:
                resource = parse_resource(json_str)
                results.append(resource)
            except Exception as e:
                logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error parsing resource {batch_idx + idx + 1}/{total}: {e}")
                if fail_on_error:
                    raise
                results.append(None)

        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Completed parsing batch {batch_num}/{total_batches}")

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Batch parsing completed: {len(results)} resources parsed")

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return results


def serialize_resources_batch(
    resources: List[FHIRResource],
    batch_size: int = 100,
    fail_on_error: bool = False,
) -> List[Optional[str]]:
    """
    Serialize multiple FHIR resources to JSON in batches.

    Args:
        resources: List of FHIR resource objects
        batch_size: Number of resources to serialize per batch (default: 100)
        fail_on_error: If True, raise exception on first error; if False, continue

    Returns:
        List of JSON strings (None for failed serializations if fail_on_error=False)

    Raises:
        Exception: If fail_on_error=True and serialization fails
    """
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting batch serialization of {len(resources)} resources")

    results = []
    total = len(resources)

    for batch_idx in range(0, total, batch_size):
        batch = resources[batch_idx : batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size

        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Serializing batch {batch_num}/{total_batches} ({len(batch)} resources)")

        for idx, resource in enumerate(batch):
            try:
                json_str = serialize_fhir_json(resource)
                results.append(json_str)
            except Exception as e:
                logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error serializing resource {batch_idx + idx + 1}/{total}: {e}")
                if fail_on_error:
                    raise
                results.append(None)

        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Completed serializing batch {batch_num}/{total_batches}")

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Batch serialization completed: {len(results)} JSON strings")

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return results


def create_bundle_from_resources(
    resources: List[FHIRResource],
    bundle_type: str = "collection",
    bundle_id: Optional[str] = None,
) -> Bundle:
    """
    Create a FHIR Bundle from a list of resources.

    Args:
        resources: List of FHIR resource objects
        bundle_type: Bundle type (default: "collection")
        bundle_id: Optional bundle ID

    Returns:
        Bundle resource containing all resources
    """
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Creating Bundle from {len(resources)} resources")

    from dnhealth.dnhealth_fhir.resources.bundle import BundleEntry

    entries = []
    for resource in resources:
        entry = BundleEntry(resource=resource)
        entries.append(entry)

    bundle = Bundle(
        resourceType="Bundle",
        type=bundle_type,
        entry=entries,
    )

    if bundle_id:
        bundle.id = bundle_id

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Created Bundle with {len(entries)} entries")

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return bundle


def extract_resources_from_bundle(bundle: Bundle) -> List[FHIRResource]:
    """
    Extract all resources from a FHIR Bundle.

    Args:
        bundle: Bundle resource

    Returns:
        List of resources from bundle entries
    """
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Extracting resources from Bundle")

    resources = []
    if bundle.entry:
        for entry in bundle.entry:
            if entry.resource:
                resources.append(entry.resource)

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Extracted {len(resources)} resources from Bundle")
    return resources


def batch_iterator(
    items: List[Any],
    batch_size: int = 100,
) -> Iterator[List[Any]]:
    """
    Iterator that yields items in batches.

    Args:
        items: List of items to batch
        batch_size: Size of each batch

    Yields:
        Lists of items in batches
    """
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]
