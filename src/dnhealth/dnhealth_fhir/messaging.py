# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 messaging workflow processing.

Provides functionality to process FHIR message Bundles according to the FHIR Messaging specification,
including message validation, routing, and response generation.
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry
from dnhealth.dnhealth_fhir.resources.messageheader import MessageHeader
from dnhealth.dnhealth_fhir.resources.messagedefinition import MessageDefinition, MessageDefinitionFocus

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class MessageProcessor:
    """
    Process FHIR message Bundles according to FHIR Messaging specification.
    
    This class provides functionality to:
    - Process incoming message Bundles
    - Validate message structure against MessageDefinition
    - Route messages to appropriate handlers
    - Generate response messages
    """

    def __init__(self):
        """Initialize the message processor."""
        self._message_definitions: Dict[str, MessageDefinition] = {}
        self._handlers: Dict[str, Any] = {}
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] MessageProcessor initialized")

    def register_message_definition(
        self, event_code: str, message_definition: MessageDefinition
    ) -> None:
        """
        Register a MessageDefinition for an event code.
        
        Args:
            event_code: Event code (e.g., "patient-notify")
            message_definition: MessageDefinition resource
        """
        self._message_definitions[event_code] = message_definition
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Registered MessageDefinition for event code: {event_code}"
        )

    def register_handler(self, event_code: str, handler: Any) -> None:
        """
        Register a handler function for an event code.
        
        Args:
            event_code: Event code
            handler: Handler function that takes (message_header, focus_resources) and returns response resources
        """
        self._handlers[event_code] = handler
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Registered handler for event code: {event_code}")

    def process_message(self, bundle: Bundle) -> Bundle:
        """
        Process an incoming message Bundle.
        
        Args:
            bundle: The message Bundle to process
            
        Returns:
            Response Bundle (if response required) or processed Bundle
            
        Raises:
            ValueError: If message Bundle is invalid
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Processing message Bundle")
        
        # Validate message structure
        validation_errors = self.validate_message_bundle(bundle)
        if validation_errors:
            error_msg = "; ".join(validation_errors)
            logger.error(f"[{current_time}] Message validation failed: {error_msg}")
            raise ValueError(f"Invalid message Bundle: {error_msg}")
        
        # Extract MessageHeader
        message_header = self.extract_message_header(bundle)
        if not message_header:
            raise ValueError("Message Bundle missing MessageHeader")
        
        # Get event code
        event_code = self._get_event_code(message_header)
        if not event_code:
            raise ValueError("MessageHeader missing event code")
        
        # Load MessageDefinition
        message_definition = self.load_message_definition(event_code)
        if not message_definition:
            logger.warning(
                f"[{current_time}] No MessageDefinition found for event code: {event_code}"
            )
        else:
            # Validate against MessageDefinition
            definition_errors = self.validate_message_structure(bundle, message_definition)
            if definition_errors:
                error_msg = "; ".join(definition_errors)
                logger.warning(
                    f"[{current_time}] Message structure validation warnings: {error_msg}"
                )
        
        # Extract focus resources
        focus_resources = self._extract_focus_resources(bundle, message_header)
        
        # Route to handler if registered
        if event_code in self._handlers:
            handler = self._handlers[event_code]
            response_resources = handler(message_header, focus_resources)
            
            # Generate response message
            if response_resources:
                response_bundle = self.generate_response_message(
                    bundle, response_resources
                )
                elapsed = time.time() - start_time
                logger.info(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message processing "
                    f"completed in {elapsed:.3f}s (response generated)"
                )
                return response_bundle
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message processing "
            f"completed in {elapsed:.3f}s"
        )
        
        return bundle

    def validate_message_structure(        self, bundle: Bundle, message_definition: MessageDefinition
    ) -> List[str]:
        """
        Validate message structure against MessageDefinition.
        
        Args:
            bundle: The message Bundle
            message_definition: MessageDefinition to validate against
            
        Returns:
            List of validation errors (empty if valid)
        """
        start_time = time.time()
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract MessageHeader
        message_header = self.extract_message_header(bundle)
        if not message_header:
            errors.append("Message Bundle missing MessageHeader")
            return errors
        
        # Validate focus resources
        focus_resources = self._extract_focus_resources(bundle, message_header)
        
        # Check each focus definition
        for focus_def in message_definition.focus:
            resource_type = focus_def.code
            min_count = focus_def.min
            max_count = focus_def.max if focus_def.max else "*"
            
            # Count resources of this type
            count = sum(
                1
                for entry in bundle.entry
                if entry.resource
                and entry.resource.resourceType == resource_type
            )
            
            # Check minimum
            if count < min_count:
                errors.append(
                    f"Focus resource {resource_type}: minimum {min_count} required, "
                    f"found {count}"
                )
            
            # Check maximum
            if max_count != "*":
                try:
                    max_int = int(max_count)
                    if count > max_int:
                        errors.append(
                            f"Focus resource {resource_type}: maximum {max_int} allowed, "
                            f"found {count}"
                        )
                except ValueError:
                    pass  # Invalid max format
        
        elapsed = time.time() - start_time
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message structure validation "
            f"completed in {elapsed:.3f}s (errors: {len(errors)})"
        )
        
        return errors

    def extract_message_header(self, bundle: Bundle) -> Optional[MessageHeader]:
        """
        Extract MessageHeader from message Bundle.
        
        Args:
            bundle: The message Bundle
            
        Returns:
            MessageHeader if found, None otherwise
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Extracting MessageHeader from Bundle")
        
        if bundle.type != "message":
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MessageHeader extraction "
                f"completed in {elapsed:.3f}s (not a message Bundle)"
            )
            return None
        
        if not bundle.entry:
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MessageHeader extraction "
                f"completed in {elapsed:.3f}s (no entries)"
            )
            return None
        
        first_entry = bundle.entry[0]
        if not first_entry.resource:
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MessageHeader extraction "
                f"completed in {elapsed:.3f}s (no resource in first entry)"
            )
            return None
        
        if isinstance(first_entry.resource, MessageHeader):
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MessageHeader extraction "
                f"completed in {elapsed:.3f}s"
            )
            return first_entry.resource
        
        elapsed = time.time() - start_time
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MessageHeader extraction "
            f"completed in {elapsed:.3f}s (not a MessageHeader)"
        )
        return None

    def load_message_definition(self, event_code: str) -> Optional[MessageDefinition]:
        """
        Load MessageDefinition for an event code.
        
        Args:
            event_code: Event code
            
        Returns:
            MessageDefinition if found, None otherwise
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Loading MessageDefinition for event code: {event_code}")
        
        result = self._message_definitions.get(event_code)
        
        elapsed = time.time() - start_time
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MessageDefinition loading "
            f"completed in {elapsed:.3f}s ({'found' if result else 'not found'})"
        )

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result

    def generate_response_message(
        self, original_message: Bundle, response_resources: List[FHIRResource]
    ) -> Bundle:
        """
        Generate response message Bundle.
        
        Args:
            original_message: Original message Bundle
            response_resources: List of response resources
            
        Returns:
            Response Bundle
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Generating response message")
        
        # Extract original MessageHeader
        original_header = self.extract_message_header(original_message)
        if not original_header:
            raise ValueError("Original message missing MessageHeader")
        
        # Create response MessageHeader
        response_header = MessageHeader(
            resourceType="MessageHeader",
            source=original_header.source,
            eventCoding=original_header.eventCoding,
            focus=[],  # Will be populated from response_resources
        )
        
        # Set response reference if original had response
        if original_header.response:
            # Create response reference
            from dnhealth.dnhealth_fhir.resources.messageheader import MessageHeaderResponse
            response_header.response = MessageHeaderResponse(
                identifier=original_header.response.identifier,
                code="ok",  # or appropriate response code
            )
        
        # Create response Bundle entries
        entries = [BundleEntry(resource=response_header)]
        for resource in response_resources:
            entries.append(BundleEntry(resource=resource))
        
        # Create response Bundle
        response_bundle = Bundle(
            resourceType="Bundle",
            type="message",
            entry=entries,
        )
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response message generation "
            f"completed in {elapsed:.3f}s"
        )
        
        return response_bundle

    def _get_event_code(self, message_header: MessageHeader) -> Optional[str]:
        """Extract event code from MessageHeader."""
        if message_header.eventCoding:
            # Return system|code format
            if hasattr(message_header.eventCoding, "system") and hasattr(
                message_header.eventCoding, "code"
            ):

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
                system = message_header.eventCoding.system or ""
                code = message_header.eventCoding.code or ""
                return f"{system}|{code}" if system else code
        if message_header.eventUri:
            return message_header.eventUri
        return None

    def _extract_focus_resources(
        self, bundle: Bundle, message_header: MessageHeader
    ) -> List[FHIRResource]:
        """Extract focus resources from Bundle."""
        focus_resources = []
        
        # Get focus references from MessageHeader
        focus_refs = message_header.focus if message_header.focus else []
        
        # Extract resources referenced by focus
        for entry in bundle.entry:
            if entry.resource and entry.resource not in focus_resources:
                # Check if resource is in focus
                resource_id = entry.resource.id if hasattr(entry.resource, "id") else None
                if resource_id:
                    for focus_ref in focus_refs:
                        if focus_ref.reference and resource_id in focus_ref.reference:
                            focus_resources.append(entry.resource)
                            break
                else:
                    # If no focus specified, include all non-MessageHeader resources
                    if not isinstance(entry.resource, MessageHeader):
                        focus_resources.append(entry.resource)
        
        return focus_resources


def validate_message_bundle(bundle: Bundle) -> List[str]:
    """
    Validate message Bundle structure.
    
    Args:
        bundle: The message Bundle to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    start_time = time.time()
    errors = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check Bundle type
    if bundle.type != "message":
        errors.append(f"Bundle.type must be 'message', got '{bundle.type}'")
    
    # Check Bundle has entries
    if not bundle.entry:
        errors.append("Message Bundle must have at least one entry")
    
    # Check first entry is MessageHeader
    if bundle.entry:
        first_entry = bundle.entry[0]
        if not first_entry.resource:
            errors.append("First Bundle entry must have a resource")
        elif not isinstance(first_entry.resource, MessageHeader):
            errors.append(
                f"First Bundle entry must be MessageHeader, got {type(first_entry.resource).__name__}"
            )
        else:
            # Validate MessageHeader has event
            message_header = first_entry.resource
            if not message_header.eventCoding and not message_header.eventUri:
                errors.append("MessageHeader must have eventCoding or eventUri")
    
    elapsed = time.time() - start_time
    logger.debug(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message Bundle validation "
        f"completed in {elapsed:.3f}s (errors: {len(errors)})"
    )
    
    return errors


def route_message(
    message_header: MessageHeader, message_definition: Optional[MessageDefinition] = None
) -> str:
    """
    Determine message destination from MessageHeader.
    
    Args:
        message_header: MessageHeader from message
        message_definition: Optional MessageDefinition
        
    Returns:
        Destination identifier
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get destination from MessageHeader
    if message_header.destination:
        # Use first destination
        first_dest = message_header.destination[0]
        if first_dest.endpoint:
            destination = first_dest.endpoint
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message routing "
                f"completed in {elapsed:.3f}s (destination: {destination})"
            )
            return destination
        elif first_dest.name:
            destination = first_dest.name
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message routing "
                f"completed in {elapsed:.3f}s (destination: {destination})"
            )
            return destination
    
    # Default destination
    destination = "default"
    elapsed = time.time() - start_time
    logger.debug(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message routing "
        f"completed in {elapsed:.3f}s (destination: {destination})"
    )
    return destination
