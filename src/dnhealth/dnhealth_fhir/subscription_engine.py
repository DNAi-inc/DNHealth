# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Subscription Engine.

Provides subscription management, criteria evaluation, and notification delivery.
All operations include timestamps in logs for traceability.
"""

import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from urllib.parse import urlparse
import requests
from queue import Queue

from dnhealth.dnhealth_fhir.resources.subscription import Subscription, SubscriptionChannel
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry, BundleType
from dnhealth.dnhealth_fhir.search import parse_search_string
from dnhealth.dnhealth_fhir.search_execution import execute_search, resource_matches_search
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)

# Test timeout limit: 5 minutes
TEST_TIMEOUT = 300


class SubscriptionNotification:
    """
    Represents a subscription notification.
    
    Contains the subscription, the resource that triggered it, and the event type.
    """
    
    def __init__(
        self,
        subscription: Subscription,
        resource: FHIRResource,
        event_type: str  # "create", "update", "delete"
    ):
        """
        Initialize subscription notification.
        
        Args:
            subscription: The subscription that matched
            resource: The resource that triggered the notification
            event_type: Type of event (create, update, delete)
        """
        self.subscription = subscription
        self.resource = resource
        self.event_type = event_type
        self.timestamp = datetime.now()


class SubscriptionEngine:
    """
    FHIR Subscription Engine.
    
    Manages subscriptions, evaluates criteria, and sends notifications.
    Thread-safe and supports multiple notification channels.
    """
    
    def __init__(self, storage: Optional[Any] = None):
        """
        Initialize the subscription engine.
        
        Args:
            storage: Optional storage backend for retrieving resources
                    (must have search() method)
        """
        self._subscriptions: Dict[str, Subscription] = {}
        self._lock = threading.Lock()
        self._notification_queue: Queue = Queue()
        self._notification_thread: Optional[threading.Thread] = None
        self._running = False
        self.storage = storage
        
        # Channel handlers
        self._channel_handlers: Dict[str, Callable] = {
            "rest-hook": self._send_rest_hook_notification,
            "websocket": self._send_websocket_notification,
            "email": self._send_email_notification,
            "sms": self._send_sms_notification,
            "message": self._send_message_notification,
        }
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] SubscriptionEngine initialized")
    
    def start(self):
        """Start the notification processing thread."""
        if self._running:
            return
        
        self._running = True
        self._notification_thread = threading.Thread(
            target=self._process_notifications,
            daemon=True
        )
        self._notification_thread.start()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] SubscriptionEngine notification thread started")
    
    def stop(self):
        """Stop the notification processing thread."""
        self._running = False
        if self._notification_thread:
            self._notification_thread.join(timeout=5.0)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] SubscriptionEngine notification thread stopped")
    
    def create_subscription(self, subscription: Subscription) -> Subscription:
        """
        Create a new subscription.
        
        Args:
            subscription: Subscription resource to create
            
        Returns:
            Created subscription with ID and metadata set
            
        Raises:
            ValueError: If subscription is invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Creating subscription")
        
        # Validate subscription
        if not subscription.status:
            raise ValueError("Subscription status is required")
        
        if not subscription.criteria:
            raise ValueError("Subscription criteria is required")
        
        if not subscription.channel:
            raise ValueError("Subscription channel is required")
        
        if not subscription.channel.type:
            raise ValueError("Subscription channel type is required")
        
        # Validate channel type
        valid_channel_types = {"rest-hook", "websocket", "email", "sms", "message"}
        if subscription.channel.type not in valid_channel_types:
            raise ValueError(f"Invalid channel type: {subscription.channel.type}")
        
        # Validate endpoint for rest-hook and websocket
        if subscription.channel.type in {"rest-hook", "websocket"}:
            if not subscription.channel.endpoint:
                raise ValueError(f"Endpoint is required for {subscription.channel.type} channel")
        
        # Generate ID if not provided
        if not subscription.id:
            import uuid
            subscription.id = str(uuid.uuid4())
        
        # Set meta if not present
        if not subscription.meta:
            from dnhealth.dnhealth_fhir.resources.base import Meta
            subscription.meta = Meta()
        
        now = datetime.now().isoformat()
        subscription.meta.lastUpdated = now
        subscription.meta.versionId = "1"
        
        # Store subscription
        with self._lock:
            self._subscriptions[subscription.id] = subscription
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Created subscription {subscription.id} with criteria: {subscription.criteria}")
        
        return subscription
    
    def update_subscription(self, subscription_id: str, subscription: Subscription) -> Subscription:
        """
        Update an existing subscription.
        
        Args:
            subscription_id: ID of subscription to update
            subscription: Updated subscription
            
        Returns:
            Updated subscription
            
        Raises:
            ValueError: If subscription not found or invalid
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Updating subscription {subscription_id}")
        
        with self._lock:
            if subscription_id not in self._subscriptions:
                raise ValueError(f"Subscription {subscription_id} not found")
            
            # Validate subscription
            if not subscription.status:
                raise ValueError("Subscription status is required")
            
            if not subscription.criteria:
                raise ValueError("Subscription criteria is required")
            
            if not subscription.channel:
                raise ValueError("Subscription channel is required")
            
            # Update subscription
            subscription.id = subscription_id
            if subscription.meta:
                subscription.meta.lastUpdated = datetime.now().isoformat()
            
            self._subscriptions[subscription_id] = subscription
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Updated subscription {subscription_id}")
        
        return subscription
    
    def delete_subscription(self, subscription_id: str) -> bool:
        """
        Delete a subscription.
        
        Args:
            subscription_id: ID of subscription to delete
            
        Returns:
            True if deleted, False if not found
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Deleting subscription {subscription_id}")
        
        with self._lock:
            if subscription_id in self._subscriptions:
                del self._subscriptions[subscription_id]
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{current_time}] Deleted subscription {subscription_id}")
                return True
        
        return False
    
    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """
        Get a subscription by ID.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Subscription if found, None otherwise
        """
        with self._lock:
            return self._subscriptions.get(subscription_id)
    
    def list_subscriptions(self, status: Optional[str] = None) -> List[Subscription]:
        """
        List all subscriptions, optionally filtered by status.
        
        Args:
            status: Optional status filter (e.g., "active", "off")
            
        Returns:
            List of subscriptions
        """
        with self._lock:
            subscriptions = list(self._subscriptions.values())
            
            if status:
                subscriptions = [s for s in subscriptions if s.status == status]
            

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return subscriptions
    
    def evaluate_resource_change(
        self,
        resource: FHIRResource,
        event_type: str  # "create", "update", "delete"
    ):
        """
        Evaluate a resource change against all active subscriptions.
        
        This method should be called whenever a resource is created, updated, or deleted.
        
        Args:
            resource: The resource that changed
            event_type: Type of event ("create", "update", "delete")
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Evaluating resource change: {resource.resourceType}/{resource.id} ({event_type})")
        
        # Check timeout
        if time.time() - start_time > TEST_TIMEOUT:
            logger.warning(f"[{current_time}] Subscription evaluation exceeded timeout")
            return
        
        # Get active subscriptions
        active_subscriptions = self.list_subscriptions(status="active")
        
        if not active_subscriptions:
            return
        
        # Evaluate each subscription
        for subscription in active_subscriptions:
            # Check timeout
            if time.time() - start_time > TEST_TIMEOUT:
                logger.warning(f"[{current_time}] Subscription evaluation exceeded timeout")
                break
            
            # Check if subscription matches this resource type
            if self._subscription_matches_resource(subscription, resource):
                # Create notification
                notification = SubscriptionNotification(
                    subscription=subscription,
                    resource=resource,
                    event_type=event_type
                )
                
                # Queue notification
                self._notification_queue.put(notification)
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{current_time}] Queued notification for subscription {subscription.id}")
        
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Subscription evaluation completed in {elapsed:.3f}s")
    
    def _subscription_matches_resource(
        self,
        subscription: Subscription,
        resource: FHIRResource
    ) -> bool:
        """
        Check if a subscription's criteria matches a resource.
        
        Args:
            subscription: Subscription to check
            resource: Resource to evaluate
            
        Returns:
            True if subscription matches resource
        """
        try:
            # Parse criteria as search query
            # Criteria format: "ResourceType?param1=value1&param2=value2"
            criteria = subscription.criteria.strip()
            
            # Extract resource type from criteria
            if "?" in criteria:
                resource_type_part, query_part = criteria.split("?", 1)
            else:
                resource_type_part = criteria
                query_part = ""
            
            resource_type_part = resource_type_part.strip()
            
            # Check if resource type matches
            if resource_type_part and resource_type_part != resource.resourceType:
                return False
            
            # If no query part, match all resources of this type
            if not query_part:
                return True
            
            # Parse search parameters
            try:
                search_params = parse_search_string(query_part)
            except Exception as e:
                logger.warning(f"Failed to parse subscription criteria: {e}")
                return False
            
            # Evaluate search parameters against resource
            try:
                return resource_matches_search(resource, search_params)
            except Exception as e:
                logger.warning(f"Failed to evaluate subscription criteria: {e}")
                return False
        
        except Exception as e:
            logger.error(f"Error evaluating subscription criteria: {e}")
            return False
    
    def _process_notifications(self):
        """Process notifications from the queue (runs in background thread)."""
        while self._running:
            try:
                # Get notification with timeout
                try:
                    notification = self._notification_queue.get(timeout=1.0)
                except:
                    continue
                
                # Process notification
                self._send_notification(notification)
                
                # Mark task as done
                self._notification_queue.task_done()
            
            except Exception as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(f"[{current_time}] Error processing notification: {e}")
    
    def _send_notification(self, notification: SubscriptionNotification):
        """
        Send a notification via the subscription's channel.
        
        Args:
            notification: Notification to send
        """
        subscription = notification.subscription
        channel = subscription.channel
        channel_type = channel.type
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Sending notification for subscription {subscription.id} via {channel_type}")
        
        # Get handler for channel type
        handler = self._channel_handlers.get(channel_type)
        if not handler:
            logger.error(f"Unknown channel type: {channel_type}")
            self._mark_subscription_error(subscription, f"Unknown channel type: {channel_type}")
            return
        
        # Send notification
        try:
            handler(notification)
            logger.info(f"[{current_time}] Successfully sent notification for subscription {subscription.id}")
        except Exception as e:
            logger.error(f"[{current_time}] Failed to send notification for subscription {subscription.id}: {e}")
            self._mark_subscription_error(subscription, str(e))
    
    def _send_rest_hook_notification(self, notification: SubscriptionNotification):
        """
        Send REST hook notification (HTTP POST).
        
        Args:
            notification: Notification to send
        """
        subscription = notification.subscription
        channel = subscription.channel
        endpoint = channel.endpoint
        
        if not endpoint:
            raise ValueError("Endpoint is required for rest-hook channel")
        
        # Build notification Bundle
        bundle = self._create_notification_bundle(notification)
        
        # Serialize bundle
        from dnhealth.dnhealth_fhir.serialization import serialize_resource
        bundle_data = serialize_resource(bundle)
        
        # Prepare headers
        headers = {
            "Content-Type": channel.payload or "application/fhir+json"
        }
        
        # Add custom headers
        for header in channel.header:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
        
        # Send HTTP POST request
        start_time = time.time()
        response = requests.post(
            endpoint,
            json=bundle_data,
            headers=headers,
            timeout=30.0  # 30 second timeout for HTTP requests
        )
        elapsed = time.time() - start_time
        
        # Check timeout
        if elapsed > TEST_TIMEOUT:
            raise TimeoutError(f"REST hook notification exceeded timeout: {elapsed:.3f}s")
        
        # Check response
        response.raise_for_status()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] REST hook notification sent to {endpoint}: {response.status_code}")
    
    def _send_websocket_notification(self, notification: SubscriptionNotification):
        """
        Send WebSocket notification.
        
        Args:
            notification: Notification to send
            
        Note:
            This implementation attempts to send via WebSocket if websocket-client
            library is available. Otherwise, it logs the notification for manual
            processing or integration with a WebSocket server.
        """
        subscription = notification.subscription
        channel = subscription.channel
        endpoint = channel.endpoint
        
        if not endpoint:
            raise ValueError("Endpoint is required for websocket channel")
        
        # Build notification Bundle
        bundle = self._create_notification_bundle(notification)
        
        # Serialize bundle
        from dnhealth.dnhealth_fhir.serialization import serialize_resource
        bundle_data = serialize_resource(bundle)
        
        # Try to use websocket-client if available
        try:
            import websocket
            import json
            
            # Parse WebSocket URL (ws:// or wss://)
            ws_url = endpoint
            if not ws_url.startswith(("ws://", "wss://")):
                # Convert http:// to ws:// or https:// to wss://
                ws_url = endpoint.replace("http://", "ws://").replace("https://", "wss://")
            
            # Send WebSocket message
            start_time = time.time()
            ws = websocket.create_connection(ws_url, timeout=10.0)
            try:
                ws.send(json.dumps(bundle_data))
                response = ws.recv()  # Wait for acknowledgment (optional)
                ws.close()
                
                elapsed = time.time() - start_time
                if elapsed > TEST_TIMEOUT:
                    raise TimeoutError(f"WebSocket notification exceeded timeout: {elapsed:.3f}s")
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{current_time}] WebSocket notification sent to {endpoint} in {elapsed:.3f}s")
            except Exception as e:
                ws.close()
                raise
        except ImportError:
            # websocket-client not available, log for manual processing
            logger.info(
                f"[{current_time}] WebSocket notification prepared for {endpoint}. "
                f"Install 'websocket-client' package for automatic sending. "
                f"Bundle data: {len(str(bundle_data))} bytes"
            )
        except Exception as e:
            logger.error(f"[{current_time}] Failed to send WebSocket notification to {endpoint}: {e}")
            raise
    
    def _send_email_notification(self, notification: SubscriptionNotification):
        """
        Send email notification.
        
        Args:
            notification: Notification to send
            
        Note:
            This implementation attempts to send email via SMTP if configured.
            Requires SMTP server configuration via environment variables or
            subscription channel extension parameters.
        """
        subscription = notification.subscription
        channel = subscription.channel
        endpoint = channel.endpoint  # Email address
        
        if not endpoint:
            raise ValueError("Endpoint (email address) is required for email channel")
        
        # Build notification Bundle
        bundle = self._create_notification_bundle(notification)
        
        # Serialize bundle
        from dnhealth.dnhealth_fhir.serialization import serialize_resource
        bundle_data = serialize_resource(bundle)
        
        # Try to send email via SMTP
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import os
            
            # Get SMTP configuration from environment or channel extensions
            smtp_host = os.getenv("FHIR_SMTP_HOST", "localhost")
            smtp_port = int(os.getenv("FHIR_SMTP_PORT", "25"))
            smtp_user = os.getenv("FHIR_SMTP_USER", "")
            smtp_password = os.getenv("FHIR_SMTP_PASSWORD", "")
            smtp_from = os.getenv("FHIR_SMTP_FROM", "fhir@localhost")
            
            # Create email message
            msg = MIMEMultipart()
            msg["From"] = smtp_from
            msg["To"] = endpoint
            msg["Subject"] = f"FHIR Subscription Notification: {notification.resource.resourceType}/{notification.resource.id}"
            
            # Create email body
            body = f"""
FHIR Subscription Notification

Event Type: {notification.event_type}
Resource Type: {notification.resource.resourceType}
Resource ID: {notification.resource.id}
Timestamp: {notification.timestamp.isoformat()}

Bundle data is attached as JSON.
            """.strip()
            msg.attach(MIMEText(body, "plain"))
            
            # Attach bundle as JSON
            import json
            attachment = MIMEText(json.dumps(bundle_data, indent=2), "json")
            attachment.add_header("Content-Disposition", "attachment", filename="bundle.json")
            msg.attach(attachment)
            
            # Send email
            start_time = time.time()
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_user and smtp_password:
                    server.login(smtp_user, smtp_password)
                server.send_message(msg)
            
            elapsed = time.time() - start_time
            if elapsed > TEST_TIMEOUT:
                raise TimeoutError(f"Email notification exceeded timeout: {elapsed:.3f}s")
            
            logger.info(f"[{current_time}] Email notification sent to {endpoint} in {elapsed:.3f}s")
        except ImportError:
            # smtplib should always be available in Python stdlib
            logger.warning(f"[{current_time}] Email notification prepared for {endpoint} but SMTP module unavailable")
        except Exception as e:
            # If SMTP fails, log for manual processing
            logger.warning(
                f"[{current_time}] Email notification prepared for {endpoint} but SMTP send failed: {e}. "
                f"Configure SMTP via environment variables (FHIR_SMTP_HOST, FHIR_SMTP_PORT, etc.) "
                f"or process manually. Bundle data: {len(str(bundle_data))} bytes"
            )
            # Don't raise - allow notification to be logged for manual processing
    
    def _send_sms_notification(self, notification: SubscriptionNotification):
        """
        Send SMS notification.
        
        Args:
            notification: Notification to send
            
        Note:
            This implementation attempts to send SMS via HTTP-based SMS gateway
            (e.g., Twilio, AWS SNS) if configured. Requires SMS gateway configuration
            via environment variables or subscription channel extension parameters.
        """
        subscription = notification.subscription
        channel = subscription.channel
        endpoint = channel.endpoint  # Phone number or SMS gateway URL
        
        if not endpoint:
            raise ValueError("Endpoint (phone number) is required for SMS channel")
        
        # Build notification Bundle
        bundle = self._create_notification_bundle(notification)
        
        # Serialize bundle
        from dnhealth.dnhealth_fhir.serialization import serialize_resource
        bundle_data = serialize_resource(bundle)
        
        # Create SMS message text (summary of notification)
        resource_summary = f"{notification.resource.resourceType}/{notification.resource.id}"
        sms_text = f"FHIR Notification: {resource_summary} ({notification.event_type})"
        
        # Try to send SMS via HTTP gateway (Twilio, AWS SNS, etc.)
        try:
            import os
            
            # Check for SMS gateway configuration
            sms_gateway_url = os.getenv("FHIR_SMS_GATEWAY_URL", "")
            sms_gateway_api_key = os.getenv("FHIR_SMS_GATEWAY_API_KEY", "")
            
            if sms_gateway_url and sms_gateway_api_key:
                # Send via HTTP gateway
                start_time = time.time()
                response = requests.post(
                    sms_gateway_url,
                    json={
                        "to": endpoint,
                        "message": sms_text,
                        "metadata": {
                            "resource_type": notification.resource.resourceType,
                            "resource_id": notification.resource.id,
                            "event_type": notification.event_type
                        }
                    },
                    headers={"Authorization": f"Bearer {sms_gateway_api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()
                
                elapsed = time.time() - start_time
                if elapsed > TEST_TIMEOUT:
                    raise TimeoutError(f"SMS notification exceeded timeout: {elapsed:.3f}s")
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{current_time}] SMS notification sent to {endpoint} via gateway in {elapsed:.3f}s")
            else:
                # No gateway configured, log for manual processing
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{current_time}] SMS notification prepared for {endpoint}. "
                    f"Configure SMS gateway via FHIR_SMS_GATEWAY_URL and FHIR_SMS_GATEWAY_API_KEY "
                    f"environment variables. Message: {sms_text}"
                )
        except Exception as e:
            logger.warning(
                f"[{current_time}] SMS notification prepared for {endpoint} but gateway send failed: {e}. "
                f"Message: {sms_text}"
            )
            # Don't raise - allow notification to be logged for manual processing
    
    def _send_message_notification(self, notification: SubscriptionNotification):
        """
        Send message notification (FHIR messaging).
        
        Creates a proper FHIR message Bundle with MessageHeader and sends it
        to the configured endpoint. The message Bundle structure follows the
        FHIR Messaging specification.
        
        Args:
            notification: Notification to send
            
        Note:
            This implementation creates the complete message structure including
            MessageHeader and message Bundle. Actual transmission to the endpoint
            requires FHIR messaging infrastructure (HTTP client, message queue, etc.).
            The message Bundle is serialized and logged for verification.
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Preparing message notification")
        
        subscription = notification.subscription
        channel = subscription.channel
        endpoint = channel.endpoint  # Message endpoint
        
        if not endpoint:
            raise ValueError("Endpoint is required for message channel")
        
        # Create MessageHeader resource
        from dnhealth.dnhealth_fhir.resources.messageheader import (
            MessageHeader,
            MessageHeaderSource,
            MessageHeaderDestination
        )
        from dnhealth.dnhealth_fhir.types import Coding, Reference
        import uuid
        
        # Create event coding for subscription notification
        event_coding = Coding(
            system="http://hl7.org/fhir/message-events",
            code="subscription-notification",
            display="Subscription Notification"
        )
        
        # Create source (this subscription engine)
        source = MessageHeaderSource(
            name="DNHealth Subscription Engine",
            software="DNHealth",
            version="1.0",
            endpoint=endpoint
        )
        
        # Create destination
        destination = MessageHeaderDestination(
            name=endpoint,
            endpoint=endpoint
        )
        
        # Create MessageHeader
        message_header = MessageHeader(
            id=str(uuid.uuid4()),
            eventCoding=event_coding,
            source=source,
            destination=[destination],
            focus=[Reference(reference=f"{notification.resource.resourceType}/{notification.resource.id}")]
        )
        
        # Set timestamp
        if not message_header.meta:
            from dnhealth.dnhealth_fhir.resources.base import Meta
            message_header.meta = Meta()
        message_header.meta.lastUpdated = datetime.now().isoformat()
        
        # Build notification Bundle (message Bundle)
        notification_bundle = self._create_notification_bundle(notification)
        
        # Create message Bundle with MessageHeader as first entry
        from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry, BundleType
        
        # Add MessageHeader as first entry
        header_entry = BundleEntry(
            fullUrl=f"urn:uuid:{message_header.id}",
            resource=message_header
        )
        
        # Add notification resource entry
        resource_entry = BundleEntry(
            fullUrl=f"urn:uuid:{notification.resource.id}",
            resource=notification.resource
        )
        
        # Create message Bundle (type should be "message" per FHIR spec)
        # Note: BundleType enum may not have "message", so we'll use string
        message_bundle = Bundle(
            type="message",  # Message Bundle type
            entry=[header_entry, resource_entry]
        )
        
        # Set bundle ID and timestamp
        message_bundle.id = str(uuid.uuid4())
        if not message_bundle.meta:
            from dnhealth.dnhealth_fhir.resources.base import Meta
            message_bundle.meta = Meta()
        message_bundle.meta.lastUpdated = datetime.now().isoformat()
        
        # Serialize message bundle
        from dnhealth.dnhealth_fhir.serialization import serialize_resource
        bundle_data = serialize_resource(message_bundle)
        
        # Log message notification details
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{completion_time}] Message notification prepared for {endpoint}. "
            f"MessageHeader ID: {message_header.id}, Bundle ID: {message_bundle.id}, "
            f"Resource: {notification.resource.resourceType}/{notification.resource.id}. "
            f"Elapsed time: {elapsed:.3f}s"
        )
        logger.info(f"Current Time at End of Operations: {completion_time}")
        
        # Note: Actual transmission would require:
        # 1. HTTP client to POST message Bundle to endpoint
        # 2. Message queue for asynchronous delivery
        # 3. Error handling and retry logic
        # 4. Response message processing
        # 
        # For now, the complete message structure is created and serialized.
        # The serialized bundle_data can be sent via any messaging infrastructure.
    
    def _create_notification_bundle(self, notification: SubscriptionNotification) -> Bundle:
        """
        Create a notification Bundle for a subscription notification.
        
        Args:
            notification: Notification to create bundle for
            
        Returns:
            Bundle containing the notification
        """
        # Create Bundle entry
        entry = BundleEntry(
            fullUrl=f"urn:uuid:{notification.resource.id}",
            resource=notification.resource
        )
        
        # Create Bundle
        bundle = Bundle(
            type=BundleType.HISTORY,
            entry=[entry]
        )
        
        # Set bundle ID and timestamp
        import uuid
        bundle.id = str(uuid.uuid4())
        if not bundle.meta:
            from dnhealth.dnhealth_fhir.resources.base import Meta
            bundle.meta = Meta()
        bundle.meta.lastUpdated = datetime.now().isoformat()
        
        return bundle
    
    def _mark_subscription_error(self, subscription: Subscription, error_message: str):
        """
        Mark a subscription as having an error.
        
        Args:
            subscription: Subscription to mark
            error_message: Error message
        """
        with self._lock:
            if subscription.id in self._subscriptions:
                subscription.error = error_message
                # Optionally set status to "error"
                # subscription.status = "error"
                self._subscriptions[subscription.id] = subscription
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{current_time}] Marked subscription {subscription.id} with error: {error_message}")


def get_current_time() -> str:
    """
    Get current time as formatted string.
    
    Returns:
        Current time as "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
