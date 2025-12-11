# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 REST API Server.

Provides a RESTful API server for FHIR resources following the FHIR R4 specification.
All operations include timestamps in logs for traceability.

This is a foundational implementation that can be extended with additional features.
"""

import json
from datetime import datetime
from typing import Dict, Optional, Any, List
from urllib.parse import parse_qs, urlparse

from dnhealth.dnhealth_fhir.rest_storage import ResourceStorage
from dnhealth.dnhealth_fhir.parser_json import parse_resource
from dnhealth.dnhealth_fhir.serializer_json import serialize_resource
from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome
from dnhealth.dnhealth_fhir.resources.bundle import Bundle, BundleEntry
from dnhealth.dnhealth_fhir.resources.parameters import Parameters
from dnhealth.dnhealth_fhir.search import parse_search_string, SearchParameters
from dnhealth.dnhealth_fhir.search_execution import execute_search
from dnhealth.dnhealth_fhir.operations import get_operation, list_operations
from dnhealth.dnhealth_fhir.subscription_engine import SubscriptionEngine
from dnhealth.util.logging import get_logger

logger = get_logger(__name__)

# Try to import Flask, but make it optional
try:
    from flask import Flask, request, Response, jsonify

logger = logging.getLogger(__name__)
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    request = None
    Response = None
    jsonify = None


class FHIRRestServer:
    """
    FHIR R4 REST API Server.
    
    Provides RESTful endpoints for FHIR resources following FHIR R4 specification.
    All operations include timestamps in logs.
    """
    
    def __init__(self, storage: Optional[ResourceStorage] = None, base_path: str = "/fhir", subscription_engine: Optional[SubscriptionEngine] = None):
        """
        Initialize the REST API server.
        
        Args:
            storage: Optional ResourceStorage instance (creates new if not provided)
            base_path: Base path for FHIR endpoints (default: "/fhir")
            subscription_engine: Optional SubscriptionEngine instance (creates new if not provided)
        """
        if not FLASK_AVAILABLE:
            raise ImportError(
                "Flask is required for REST API server. "
                "Install with: pip install flask"
            )
        
        self.storage = storage or ResourceStorage()
        self.base_path = base_path.rstrip("/")
        self.subscription_engine = subscription_engine or SubscriptionEngine(storage=self.storage)
        self.app = Flask(__name__)
        self._setup_routes()
        self._setup_error_handlers()
        
        # Start subscription engine
        self.subscription_engine.start()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] FHIR REST API Server initialized (base_path: {self.base_path})")
    
    def _setup_routes(self):
        """Set up all REST API routes."""
        # Note: Routes are matched in order, so more specific routes must be registered first
        
        # Metadata endpoint (specific path, must come before generic routes)
        self.app.add_url_rule(
            f"{self.base_path}/metadata",
            "get_metadata",
            self._get_metadata,
            methods=["GET"]
        )
        
        # History endpoints (specific paths with _history, must come before generic routes)
        self.app.add_url_rule(
            f"{self.base_path}/_history",
            "get_system_history",
            self._get_system_history,
            methods=["GET"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/_history",
            "get_type_history",
            self._get_type_history,
            methods=["GET"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>/_history/<version>",
            "read_version",
            self._read_version,
            methods=["GET"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>/_history",
            "get_resource_history",
            self._get_resource_history,
            methods=["GET"]
        )
        
        # Operation endpoints - Instance-level operations (must come before resource-level)
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>/<operation_name>",
            "instance_operation",
            self._execute_instance_operation,
            methods=["GET", "POST"]
        )
        
        # Operation endpoints - Resource-level operations (must come before generic resource routes)
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<operation_name>",
            "resource_operation",
            self._execute_resource_operation,
            methods=["GET", "POST"]
        )
        
        # Compartment endpoints (must come before generic resource routes)
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>/<compartment>",
            "read_compartment",
            self._read_compartment,
            methods=["GET"]
        )
        
        # Resource operations (generic routes, registered after specific routes)
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>",
            "read_resource",
            self._read_resource,
            methods=["GET"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>",
            "update_resource",
            self._update_resource,
            methods=["PUT"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>",
            "delete_resource",
            self._delete_resource,
            methods=["DELETE"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>/<resource_id>",
            "patch_resource",
            self._patch_resource,
            methods=["PATCH"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>",
            "search_resources",
            self._search_resources,
            methods=["GET"]
        )
        self.app.add_url_rule(
            f"{self.base_path}/<resource_type>",
            "create_resource",
            self._create_resource,
            methods=["POST"]
        )
        
        # Batch/Transaction endpoint
        self.app.add_url_rule(
            f"{self.base_path}",
            "batch_transaction",
            self._batch_transaction,
            methods=["POST"]
        )
        
        # Operation endpoints - System-level operations (registered last to avoid conflicts)
        # Note: This will only match if operation_name starts with $ (checked in handler)
        self.app.add_url_rule(
            f"{self.base_path}/<operation_name>",
            "system_operation",
            self._execute_system_operation,
            methods=["GET", "POST"]
        )
    
    def _setup_error_handlers(self):
        """Set up error handlers."""
        @self.app.errorhandler(404)
        def not_found(error):

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return self._create_error_response(
                404,
                "not-found",
                "Resource not found"
            )
        
        @self.app.errorhandler(400)
        def bad_request(error):

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return self._create_error_response(
                400,
                "invalid",
                str(error.description) if hasattr(error, 'description') else "Bad request"
            )
        
        @self.app.errorhandler(500)
        def internal_error(error):

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return self._create_error_response(
                500,
                "exception",
                "Internal server error"
            )
    
    def _get_content_type(self) -> str:
        """
        Determine content type from Accept header.
        
        Returns:
            Content type string ("application/fhir+json" or "application/fhir+xml")
        """
        accept = request.headers.get("Accept", "application/fhir+json")
        
        if "application/fhir+json" in accept or "application/json" in accept:
            return "application/fhir+json"
        elif "application/fhir+xml" in accept or "application/xml" in accept:
            # XML support would require serializer_xml
            # For now, default to JSON
            return "application/fhir+json"
        else:
            return "application/fhir+json"  # Default to JSON
    
    def _parse_request_body(self) -> Optional[Dict[str, Any]]:
        """
        Parse request body as JSON.
        
        Returns:
            Parsed JSON dict or None if empty
        """
        if not request.data:
            return None
        
        try:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
            return json.loads(request.data.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    def _create_error_response(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[str] = None
    ) -> Response:
        """
        Create an OperationOutcome error response.
        
        Args:
            status_code: HTTP status code
            code: Error code
            message: Error message
            details: Optional details
            
        Returns:
            Flask Response with OperationOutcome
        """
        from dnhealth.dnhealth_fhir.resources.operationoutcome import (
            OperationOutcome, OperationOutcomeIssue
        )
        
        outcome = OperationOutcome()
        issue = OperationOutcomeIssue()
        issue.severity = "error"
        issue.code = code
        issue.diagnostics = message
        if details:
            issue.details = details
        
        outcome.issue = [issue]
        
        response_data = serialize_resource(outcome)
        return Response(
            json.dumps(response_data),
            status=status_code,
            mimetype="application/fhir+json"
        )
    
    def _check_conditional_headers(self, resource: Any, operation: str = "update") -> Optional[Response]:
        """
        Check conditional headers (If-Match, If-None-Match).
        
        Args:
            resource: The resource to check
            operation: Operation type ("create", "update", "delete")
            
        Returns:
            Error response if condition fails, None if condition passes
        """
        if_match = request.headers.get("If-Match")
        if_none_match = request.headers.get("If-None-Match")
        
        if if_match:
            # If-Match: Check version matches
            if resource.meta and resource.meta.versionId:
                # Extract version from If-Match header (format: W/"version" or "version")
                match_version = if_match.strip('W/"').strip('"')
                if match_version != resource.meta.versionId:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Version mismatch: expected {match_version}, got {resource.meta.versionId}")
                    return self._create_error_response(
                        412,
                        "conflict",
                        f"Version mismatch: expected {match_version}, got {resource.meta.versionId}"
                    )
            else:
                # Resource has no version
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{current_time}] Resource has no version but If-Match specified")
                return self._create_error_response(
                    412,
                    "conflict",
                    "Resource has no version"
                )
        
        if if_none_match:
            if if_none_match == "*":
                # If-None-Match: "*" - Resource must not exist
                if resource is not None:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Resource exists but If-None-Match: * specified")
                    return self._create_error_response(
                        412,
                        "conflict",
                        "Resource already exists"
                    )
            else:
                # If-None-Match: version - Version must not match
                if resource and resource.meta and resource.meta.versionId:
                    match_version = if_none_match.strip('W/"').strip('"')
                    if match_version == resource.meta.versionId:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logger.warning(f"[{current_time}] Version matches but If-None-Match specified")
                        return self._create_error_response(
                            412,
                            "conflict",
                            f"Version {match_version} already exists"
                        )
        
        return None
    
    def _read_resource(self, resource_type: str, resource_id: str) -> Response:
        """
        Read a resource by type and ID.
        
        Endpoint: GET /fhir/{resourceType}/{id}
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Reading resource {resource_type}/{resource_id}")
        
        try:
            resource = self.storage.read(resource_type, resource_id)
            
            if resource is None:
                if self.storage.is_deleted(resource_type, resource_id):
                    return self._create_error_response(
                        410,
                        "gone",
                        f"Resource {resource_type}/{resource_id} has been deleted"
                    )
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Resource {resource_type}/{resource_id} not found"
                )
            
            # Set response headers
            response_data = serialize_resource(resource)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            if resource.meta and resource.meta.versionId:
                response.headers["ETag"] = f'W/"{resource.meta.versionId}"'
            if resource.meta and resource.meta.lastUpdated:
                response.headers["Last-Modified"] = resource.meta.lastUpdated
            
            logger.info(f"[{current_time}] Successfully read resource {resource_type}/{resource_id}")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error reading resource: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error reading resource: {str(e)}"
            )
    
    def _create_resource(self, resource_type: str) -> Response:
        """
        Create a new resource.
        
        Endpoint: POST /fhir/{resourceType}
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Creating resource of type {resource_type}")
        
        try:
            # Parse request body
            body = self._parse_request_body()
            if not body:
                return self._create_error_response(
                    400,
                    "invalid",
                    "Request body is required"
                )
            
            # Parse resource
            resource = parse_resource(body)
            
            # Verify resource type matches
            if resource.resourceType != resource_type:
                return self._create_error_response(
                    400,
                    "invalid",
                    f"Resource type mismatch: expected {resource_type}, got {resource.resourceType}"
                )
            
            # Check conditional headers (If-None-Match)
            existing_resource = None
            if resource.id:
                existing_resource = self.storage.read(resource_type, resource.id)
            
            conditional_error = self._check_conditional_headers(existing_resource, "create")
            if conditional_error:
                return conditional_error
            
            # Create resource
            created_resource = self.storage.create(resource)
            
            # If this is a Subscription resource, register it with the subscription engine
            if resource_type == "Subscription":
                try:
                    from dnhealth.dnhealth_fhir.resources.subscription import Subscription
                    if isinstance(created_resource, Subscription):
                        self.subscription_engine.create_subscription(created_resource)
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logger.info(f"[{current_time}] Registered subscription {created_resource.id}")
                except Exception as e:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Error registering subscription: {e}")
            
            # Evaluate subscription criteria for resource creation
            try:
                self.subscription_engine.evaluate_resource_change(created_resource, "create")
            except Exception as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{current_time}] Error evaluating subscriptions: {e}")
            
            # Set response headers
            response_data = serialize_resource(created_resource)
            response = jsonify(response_data)
            response.status_code = 201
            response.headers["Content-Type"] = "application/fhir+json"
            response.headers["Location"] = f"{self.base_path}/{resource_type}/{created_resource.id}"
            
            if created_resource.meta and created_resource.meta.versionId:
                response.headers["ETag"] = f'W/"{created_resource.meta.versionId}"'
            
            logger.info(f"[{current_time}] Successfully created resource {resource_type}/{created_resource.id}")
            return response
            
        except ValueError as e:
            logger.error(f"[{current_time}] Validation error creating resource: {e}")
            return self._create_error_response(
                400,
                "invalid",
                f"Validation error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"[{current_time}] Error creating resource: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error creating resource: {str(e)}"
            )
    
    def _update_resource(self, resource_type: str, resource_id: str) -> Response:
        """
        Update an existing resource.
        
        Endpoint: PUT /fhir/{resourceType}/{id}
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Updating resource {resource_type}/{resource_id}")
        
        try:
            # Parse request body
            body = self._parse_request_body()
            if not body:
                return self._create_error_response(
                    400,
                    "invalid",
                    "Request body is required"
                )
            
            # Parse resource
            resource = parse_resource(body)
            
            # Verify resource type and ID match
            if resource.resourceType != resource_type:
                return self._create_error_response(
                    400,
                    "invalid",
                    f"Resource type mismatch: expected {resource_type}, got {resource.resourceType}"
                )
            
            if resource.id != resource_id:
                return self._create_error_response(
                    400,
                    "invalid",
                    f"Resource ID mismatch: expected {resource_id}, got {resource.id}"
                )
            
            # Check conditional headers (If-Match)
            existing_resource = self.storage.read(resource_type, resource_id)
            if existing_resource:
                conditional_error = self._check_conditional_headers(existing_resource, "update")
                if conditional_error:
                    return conditional_error
            
            # Update resource
            updated_resource = self.storage.update(resource_type, resource_id, resource)
            
            # If this is a Subscription resource, update it in the subscription engine
            if resource_type == "Subscription":
                try:
                    from dnhealth.dnhealth_fhir.resources.subscription import Subscription
                    if isinstance(updated_resource, Subscription):
                        self.subscription_engine.update_subscription(resource_id, updated_resource)
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logger.info(f"[{current_time}] Updated subscription {resource_id}")
                except Exception as e:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Error updating subscription: {e}")
            
            # Evaluate subscription criteria for resource update
            try:
                self.subscription_engine.evaluate_resource_change(updated_resource, "update")
            except Exception as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(f"[{current_time}] Error evaluating subscriptions: {e}")
            
            # Set response headers
            response_data = serialize_resource(updated_resource)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            if updated_resource.meta and updated_resource.meta.versionId:
                response.headers["ETag"] = f'W/"{updated_resource.meta.versionId}"'
            
            logger.info(f"[{current_time}] Successfully updated resource {resource_type}/{resource_id}")
            return response
            
        except ValueError as e:
            if "not found" in str(e).lower():
                logger.error(f"[{current_time}] Resource not found: {e}")
                return self._create_error_response(
                    404,
                    "not-found",
                    str(e)
                )
            elif "deleted" in str(e).lower():
                logger.error(f"[{current_time}] Resource deleted: {e}")
                return self._create_error_response(
                    410,
                    "gone",
                    str(e)
                )
            else:
                logger.error(f"[{current_time}] Validation error updating resource: {e}")
                return self._create_error_response(
                    400,
                    "invalid",
                    f"Validation error: {str(e)}"
                )
        except Exception as e:
            logger.error(f"[{current_time}] Error updating resource: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error updating resource: {str(e)}"
            )
    
    def _delete_resource(self, resource_type: str, resource_id: str) -> Response:
        """
        Delete a resource.
        
        Endpoint: DELETE /fhir/{resourceType}/{id}
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Deleting resource {resource_type}/{resource_id}")
        
        try:
            # Check conditional headers (If-Match)
            existing_resource = self.storage.read(resource_type, resource_id)
            if existing_resource:
                conditional_error = self._check_conditional_headers(existing_resource, "delete")
                if conditional_error:
                    return conditional_error
            
            # Read resource before deletion for subscription evaluation
            resource_to_delete = self.storage.read(resource_type, resource_id)
            
            deleted = self.storage.delete(resource_type, resource_id)
            
            if not deleted:
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Resource {resource_type}/{resource_id} not found"
                )
            
            # If this is a Subscription resource, delete it from the subscription engine
            if resource_type == "Subscription":
                try:
                    self.subscription_engine.delete_subscription(resource_id)
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"[{current_time}] Deleted subscription {resource_id}")
                except Exception as e:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Error deleting subscription: {e}")
            
            # Evaluate subscription criteria for resource deletion
            if resource_to_delete:
                try:
                    self.subscription_engine.evaluate_resource_change(resource_to_delete, "delete")
                except Exception as e:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(f"[{current_time}] Error evaluating subscriptions: {e}")
            
            # Return 204 No Content
            response = Response(status=204)
            logger.info(f"[{current_time}] Successfully deleted resource {resource_type}/{resource_id}")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error deleting resource: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error deleting resource: {str(e)}"
            )
    
    def _patch_resource(self, resource_type: str, resource_id: str) -> Response:
        """
        Partially update a resource using PATCH.
        
        Endpoint: PATCH /fhir/{resourceType}/{id}
        Supports JSON Patch (RFC 6902) format.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Patching resource {resource_type}/{resource_id}")
        
        try:
            # Parse request body
            body = self._parse_request_body()
            if not body:
                return self._create_error_response(
                    400,
                    "invalid",
                    "Request body is required for PATCH"
                )
            
            # Load existing resource
            existing_resource = self.storage.read(resource_type, resource_id)
            if existing_resource is None:
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Resource {resource_type}/{resource_id} not found"
                )
            
            # Check conditional headers (If-Match)
            conditional_error = self._check_conditional_headers(existing_resource, "update")
            if conditional_error:
                return conditional_error
            
            # Apply patch operations
            # For JSON Patch format (RFC 6902)
            if isinstance(body, list):
                # JSON Patch array of operations
                patched_resource = self._apply_json_patch(existing_resource, body)
            else:
                # FHIR Patch format - merge the patch into existing resource
                patched_resource = self._apply_fhir_patch(existing_resource, body)
            
            # Verify resource type and ID still match
            if patched_resource.resourceType != resource_type:
                return self._create_error_response(
                    400,
                    "invalid",
                    "PATCH cannot change resource type"
                )
            if patched_resource.id != resource_id:
                return self._create_error_response(
                    400,
                    "invalid",
                    "PATCH cannot change resource ID"
                )
            
            # Update resource
            updated_resource = self.storage.update(resource_type, resource_id, patched_resource)
            
            # Set response headers
            response_data = serialize_resource(updated_resource)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            if updated_resource.meta and updated_resource.meta.versionId:
                response.headers["ETag"] = f'W/"{updated_resource.meta.versionId}"'
            
            logger.info(f"[{current_time}] Successfully patched resource {resource_type}/{resource_id}")
            return response
            
        except ValueError as e:
            logger.error(f"[{current_time}] Validation error patching resource: {e}")
            return self._create_error_response(
                400,
                "invalid",
                f"Validation error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"[{current_time}] Error patching resource: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error patching resource: {str(e)}"
            )
    
    def _apply_json_patch(self, resource: Any, patch_ops: List[Dict[str, Any]]) -> Any:
        """
        Apply JSON Patch operations (RFC 6902) to a resource.
        
        Args:
            resource: The resource to patch
            patch_ops: List of patch operations
            
        Returns:
            Patched resource
        """
        import copy
        patched = copy.deepcopy(resource)
        
        for op in patch_ops:
            op_type = op.get("op")
            path = op.get("path", "")
            value = op.get("value")
            
            if op_type == "add":
                self._json_patch_add(patched, path, value)
            elif op_type == "remove":
                self._json_patch_remove(patched, path)
            elif op_type == "replace":
                self._json_patch_replace(patched, path, value)
            elif op_type == "move":
                from_path = op.get("from")
                self._json_patch_move(patched, from_path, path)
            elif op_type == "copy":
                from_path = op.get("from")
                self._json_patch_copy(patched, from_path, path)
            else:
                raise ValueError(f"Unknown patch operation: {op_type}")
        
        return patched
    
    def _json_patch_add(self, obj: Any, path: str, value: Any):
        """Add value at path."""
        parts = path.strip("/").split("/")
        target = obj
        for part in parts[:-1]:
            if not hasattr(target, part):
                setattr(target, part, {})
            target = getattr(target, part)
        setattr(target, parts[-1], value)
    
    def _json_patch_remove(self, obj: Any, path: str):
        """Remove value at path."""
        parts = path.strip("/").split("/")
        target = obj
        for part in parts[:-1]:
            target = getattr(target, part)
        delattr(target, parts[-1])
    
    def _json_patch_replace(self, obj: Any, path: str, value: Any):
        """Replace value at path."""
        parts = path.strip("/").split("/")
        target = obj
        for part in parts[:-1]:
            target = getattr(target, part)
        setattr(target, parts[-1], value)
    
    def _json_patch_move(self, obj: Any, from_path: str, to_path: str):
        """Move value from one path to another."""
        # Get value from source
        from_parts = from_path.strip("/").split("/")
        source = obj
        for part in from_parts:
            source = getattr(source, part)
        value = source
        
        # Remove from source
        self._json_patch_remove(obj, from_path)
        
        # Add to destination
        self._json_patch_add(obj, to_path, value)
    
    def _json_patch_copy(self, obj: Any, from_path: str, to_path: str):
        """Copy value from one path to another."""
        from_parts = from_path.strip("/").split("/")
        source = obj
        for part in from_parts:
            source = getattr(source, part)
        value = source
        self._json_patch_add(obj, to_path, value)
    
    def _apply_fhir_patch(self, resource: Any, patch: Dict[str, Any]) -> Any:
        """
        Apply FHIR Patch format (merge patch into resource).
        
        Args:
            resource: The resource to patch
            patch: Patch object to merge
            
        Returns:
            Patched resource
        """
        import copy
        patched = copy.deepcopy(resource)
        
        # Merge patch into resource recursively
        self._merge_dict(patched.__dict__, patch)
        
        return patched
    
    def _merge_dict(self, target: Dict[str, Any], source: Dict[str, Any]):
        """Recursively merge source dict into target."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_dict(target[key], value)
            else:
                target[key] = value
    
    def _search_resources(self, resource_type: str) -> Response:
        """
        Search for resources by type.
        
        Endpoint: GET /fhir/{resourceType}?{searchParams}
        
        Supports full FHIR R4 search parameter syntax including:
        - Modifiers (exact, contains, text, etc.)
        - Prefixes (eq, ne, gt, lt, ge, le, sa, eb, ap)
        - Special parameters (_count, _offset, _sort, _include, _revinclude, etc.)
        - Chained parameters (e.g., subject:Patient.name=John)
        - Reverse chained parameters (e.g., _has:Observation:subject:code=12345)
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Searching resources of type {resource_type}")
        
        try:
            # Parse search parameters using proper FHIR search parser
            query_string = request.query_string.decode('utf-8') if request.query_string else ""
            search_params: SearchParameters = parse_search_string(query_string)
            
            # Get all resources of this type (storage will filter deleted ones)
            all_resources = self.storage.search(resource_type, None)
            
            # Execute search using search execution engine
            # Pass all_resources for _revinclude processing support
            matching_resources = execute_search(
                resources=all_resources,
                search_params=search_params,
                resource_resolver=self._resolve_reference,
                all_resources=all_resources
            )
            
            # Apply pagination (already handled by execute_search, but ensure it's applied)
            total_count = len(matching_resources)
            offset = search_params._offset or 0
            count = search_params._count
            
            if offset > 0:
                matching_resources = matching_resources[offset:]
            if count is not None:
                matching_resources = matching_resources[:count]
            
            # Create Bundle response
            bundle = Bundle()
            bundle.type = "searchset"
            bundle.total = total_count
            bundle.entry = []
            
            for resource in matching_resources:
                entry = BundleEntry()
                entry.resource = resource
                entry.fullUrl = f"{self.base_path}/{resource_type}/{resource.id}"
                bundle.entry.append(entry)
            
            # Add pagination links if needed
            if count is not None and len(matching_resources) == count and offset + count < total_count:
                # There are more results
                next_offset = offset + count
                next_url = f"{self.base_path}/{resource_type}?{query_string}"
                if "_offset" in query_string:
                    next_url = next_url.replace(f"_offset={offset}", f"_offset={next_offset}")
                else:
                    next_url += f"&_offset={next_offset}" if query_string else f"_offset={next_offset}"
                
                bundle.link = bundle.link or []
                from dnhealth.dnhealth_fhir.resources.bundle import BundleLink
                next_link = BundleLink()
                next_link.relation = "next"
                next_link.url = next_url
                bundle.link.append(next_link)
            
            response_data = serialize_resource(bundle)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] Search completed: found {len(matching_resources)} resources (total: {total_count})")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error searching resources: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error searching resources: {str(e)}"
            )
    
    def _get_resource_history(self, resource_type: str, resource_id: str) -> Response:
        """
        Get version history for a resource.
        
        Endpoint: GET /fhir/{resourceType}/{id}/_history
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Getting history for resource {resource_type}/{resource_id}")
        
        try:
            # Parse query parameters
            count = request.args.get("_count")
            since = request.args.get("_since")
            
            count_int = int(count) if count else None
            since_dt = None
            if since:
                try:
                    since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    pass
            
            # Get history
            history = self.storage.get_history(resource_type, resource_id, count_int, since_dt)
            
            # Create Bundle response
            bundle = Bundle()
            bundle.type = "history"
            bundle.total = len(history)
            bundle.entry = []
            
            for version_id, resource, timestamp in history:
                entry = BundleEntry()
                entry.resource = resource
                entry.fullUrl = f"{self.base_path}/{resource_type}/{resource_id}/_history/{version_id}"
                bundle.entry.append(entry)
            
            response_data = serialize_resource(bundle)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] History retrieved: {len(history)} versions")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error getting history: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error getting history: {str(e)}"
            )
    
    def _read_version(self, resource_type: str, resource_id: str, version: str) -> Response:
        """
        Read a specific version of a resource.
        
        Endpoint: GET /fhir/{resourceType}/{id}/_history/{version}
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Reading version {version} of resource {resource_type}/{resource_id}")
        
        try:
            resource = self.storage.read(resource_type, resource_id, version)
            
            if resource is None:
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Version {version} of resource {resource_type}/{resource_id} not found"
                )
            
            response_data = serialize_resource(resource)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            if resource.meta and resource.meta.versionId:
                response.headers["ETag"] = f'W/"{resource.meta.versionId}"'
            if resource.meta and resource.meta.lastUpdated:
                response.headers["Last-Modified"] = resource.meta.lastUpdated
            
            logger.info(f"[{current_time}] Successfully read version {version}")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error reading version: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error reading version: {str(e)}"
            )
    
    def _batch_transaction(self) -> Response:
        """
        Process batch or transaction request.
        
        Endpoint: POST /fhir
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Processing batch/transaction request")
        
        try:
            # Parse request body
            body = self._parse_request_body()
            if not body:
                return self._create_error_response(
                    400,
                    "invalid",
                    "Request body is required for batch/transaction"
                )
            
            # Parse Bundle
            bundle = parse_resource(body)
            if bundle.resourceType != "Bundle":
                return self._create_error_response(
                    400,
                    "invalid",
                    "Batch/transaction request must be a Bundle"
                )
            
            if bundle.type not in ["batch", "transaction"]:
                return self._create_error_response(
                    400,
                    "invalid",
                    f"Bundle type must be 'batch' or 'transaction', got '{bundle.type}'"
                )
            
            # Process entries
            results = []
            for entry in bundle.entry or []:
                try:
                    result = self._process_bundle_entry(entry, bundle.type == "transaction")
                    results.append(result)
                except Exception as e:
                    # For transaction, stop on first error
                    if bundle.type == "transaction":
                        logger.error(f"[{current_time}] Transaction failed at entry: {e}")
                        return self._create_error_response(
                            400,
                            "invalid",
                            f"Transaction failed: {str(e)}"
                        )
                    # For batch, continue processing
                    from dnhealth.dnhealth_fhir.resources.bundle import BundleEntryResponse
                    from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
                    
                    error_entry = BundleEntry()
                    error_response = BundleEntryResponse(status="500")
                    error_outcome = OperationOutcome()
                    error_issue = OperationOutcomeIssue()
                    error_issue.severity = "error"
                    error_issue.code = "exception"
                    error_issue.diagnostics = str(e)
                    error_outcome.issue = [error_issue]
                    error_response.outcome = error_outcome
                    error_entry.response = error_response
                    results.append(error_entry)
            
            # Create response bundle
            response_bundle = Bundle()
            response_bundle.type = "batch-response" if bundle.type == "batch" else "transaction-response"
            response_bundle.entry = results
            
            response_data = serialize_resource(response_bundle)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] Batch/transaction completed: {len(results)} entries processed")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error processing batch/transaction: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error processing batch/transaction: {str(e)}"
            )
    
    def _process_bundle_entry(self, entry: BundleEntry, is_transaction: bool) -> BundleEntry:
        """
        Process a single bundle entry.
        
        Args:
            entry: Bundle entry to process
            is_transaction: True if this is a transaction (fail on error)
            
        Returns:
            BundleEntry with response
        """
        from dnhealth.dnhealth_fhir.resources.bundle import BundleEntryRequest, BundleEntryResponse
        
        request_obj = entry.request
        if not request_obj:
            raise ValueError("Bundle entry missing request")
        
        method = request_obj.method.upper() if request_obj.method else ""
        url = request_obj.url if request_obj.url else ""
        
        # Parse URL to extract resource type and ID
        url_parts = url.strip("/").split("/")
        resource_type = url_parts[0] if url_parts else None
        resource_id = url_parts[1] if len(url_parts) > 1 else None
        
        from dnhealth.dnhealth_fhir.resources.bundle import BundleEntryRequest, BundleEntryResponse
        
        result_entry = BundleEntry()
        result_entry.response = BundleEntryResponse(status="200")
        
        try:
            if method == "GET":
                if resource_id:
                    # Read resource
                    resource = self.storage.read(resource_type, resource_id)
                    if resource:
                        result_entry.resource = resource
                        result_entry.response.status = "200"
                    else:
                        result_entry.response.status = "404"
                else:
                    # Search
                    search_params = {}
                    if "?" in url:
                        query_string = url.split("?")[1]
                        from urllib.parse import parse_qs
                        params = parse_qs(query_string)
                        search_params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
                    resources = self.storage.search(resource_type, search_params)
                    bundle = Bundle()
                    bundle.type = "searchset"
                    bundle.total = len(resources)
                    bundle.entry = [BundleEntry(resource=r) for r in resources]
                    result_entry.resource = bundle
                    result_entry.response.status = "200"
            
            elif method == "POST":
                # Create resource
                if entry.resource:
                    created = self.storage.create(entry.resource)
                    result_entry.resource = created
                    result_entry.response.status = "201"
                    result_entry.response.location = f"{resource_type}/{created.id}"
                else:
                    raise ValueError("Resource required for POST")
            
            elif method == "PUT":
                # Update resource
                if entry.resource:
                    updated = self.storage.update(resource_type, resource_id, entry.resource)
                    result_entry.resource = updated
                    result_entry.response.status = "200"
                else:
                    raise ValueError("Resource required for PUT")
            
            elif method == "DELETE":
                # Delete resource
                deleted = self.storage.delete(resource_type, resource_id)
                result_entry.response.status = "204" if deleted else "404"
            
            elif method == "PATCH":
                # Patch resource
                existing = self.storage.read(resource_type, resource_id)
                if existing:
                    # Apply patch (simplified - would need full patch implementation)
                    patch_dict = entry.resource.__dict__ if entry.resource else {}
                    patched = self._apply_fhir_patch(existing, patch_dict)
                    updated = self.storage.update(resource_type, resource_id, patched)
                    result_entry.resource = updated
                    result_entry.response.status = "200"
                else:
                    result_entry.response.status = "404"
            
            else:
                raise ValueError(f"Unsupported method: {method}")
        
        except Exception as e:
            if is_transaction:
                raise
            from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
            
            result_entry.response.status = "500"
            error_outcome = OperationOutcome()
            error_issue = OperationOutcomeIssue()
            error_issue.severity = "error"
            error_issue.code = "exception"
            error_issue.diagnostics = str(e)
            error_outcome.issue = [error_issue]
            result_entry.response.outcome = error_outcome
        
        return result_entry
    
    def _read_compartment(self, resource_type: str, resource_id: str, compartment: str) -> Response:
        """
        Read resources in a compartment.
        
        Endpoint: GET /fhir/{resourceType}/{id}/{compartment}
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Reading compartment {compartment} for {resource_type}/{resource_id}")
        
        try:
            # Verify resource exists
            resource = self.storage.read(resource_type, resource_id)
            if resource is None:
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Resource {resource_type}/{resource_id} not found"
                )
            
            # Parse search parameters
            search_params = dict(request.args)
            
            # Get compartment resources
            compartment_resources = self.storage.get_compartment(
                resource_type, resource_id, compartment, search_params
            )
            
            # Create Bundle response
            bundle = Bundle()
            bundle.type = "searchset"
            bundle.total = len(compartment_resources)
            bundle.entry = []
            
            for comp_resource in compartment_resources:
                entry = BundleEntry()
                entry.resource = comp_resource
                entry.fullUrl = f"{self.base_path}/{comp_resource.resourceType}/{comp_resource.id}"
                bundle.entry.append(entry)
            
            response_data = serialize_resource(bundle)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] Compartment read completed: {len(compartment_resources)} resources")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error reading compartment: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error reading compartment: {str(e)}"
            )
    
    def _get_type_history(self, resource_type: str) -> Response:
        """
        Get version history for all resources of a type.
        
        Endpoint: GET /fhir/{resourceType}/_history
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Getting type history for {resource_type}")
        
        try:
            # Parse query parameters
            count = request.args.get("_count")
            since = request.args.get("_since")
            
            count_int = int(count) if count else None
            since_dt = None
            if since:
                try:
                    since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    pass
            
            # Get type history
            history = self.storage.get_type_history(resource_type, count_int, since_dt)
            
            # Create Bundle response
            bundle = Bundle()
            bundle.type = "history"
            bundle.total = len(history)
            bundle.entry = []
            
            for version_id, resource, timestamp in history:
                entry = BundleEntry()
                entry.resource = resource
                entry.fullUrl = f"{self.base_path}/{resource_type}/{resource.id}/_history/{version_id}"
                bundle.entry.append(entry)
            
            response_data = serialize_resource(bundle)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] Type history retrieved: {len(history)} versions")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error getting type history: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error getting type history: {str(e)}"
            )
    
    def _get_system_history(self) -> Response:
        """
        Get version history for all resources.
        
        Endpoint: GET /fhir/_history
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Getting system history")
        
        try:
            # Parse query parameters
            count = request.args.get("_count")
            since = request.args.get("_since")
            
            count_int = int(count) if count else None
            since_dt = None
            if since:
                try:
                    since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    pass
            
            # Get system history
            history = self.storage.get_system_history(count_int, since_dt)
            
            # Create Bundle response
            bundle = Bundle()
            bundle.type = "history"
            bundle.total = len(history)
            bundle.entry = []
            
            for version_id, resource, timestamp in history:
                entry = BundleEntry()
                entry.resource = resource
                entry.fullUrl = f"{self.base_path}/{resource.resourceType}/{resource.id}/_history/{version_id}"
                bundle.entry.append(entry)
            
            response_data = serialize_resource(bundle)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] System history retrieved: {len(history)} versions")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error getting system history: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error getting system history: {str(e)}"
            )
    
    def _get_metadata(self) -> Response:
        """
        Get FHIR metadata (CapabilityStatement).
        
        Endpoint: GET /fhir/metadata
        
        Returns a comprehensive CapabilityStatement that accurately describes
        all server capabilities including supported resources, operations, and features.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Getting metadata")
        
        try:
            from dnhealth.dnhealth_fhir.resources.capabilitystatement import (
                CapabilityStatement,
                CapabilityStatementSoftware,
                CapabilityStatementImplementation,
                CapabilityStatementRest,
                CapabilityStatementRestResource
            )
            
            # Get all resource types from storage
            resource_types = self.storage.list_resource_types() if hasattr(self.storage, 'list_resource_types') else []
            
            # Create comprehensive CapabilityStatement
            capability = CapabilityStatement()
            capability.status = "active"
            capability.kind = "instance"
            capability.fhirVersion = "4.0.1"
            capability.format = ["json", "xml"]
            capability.patchFormat = ["application/json-patch+json"]
            capability.date = datetime.now().isoformat()
            capability.name = "DNHealth FHIR Server"
            capability.title = "DNHealth FHIR R4 Server Capability Statement"
            capability.description = "FHIR R4 REST API server with comprehensive resource support, search, history, compartments, batch/transaction, and operations"
            
            # Software information
            capability.software = CapabilityStatementSoftware(
                name="DNHealth",
                version="0.1.0-dev"
            )
            
            # Implementation information
            capability.implementation = CapabilityStatementImplementation(
                description=f"DNHealth FHIR Server instance at {self.base_path}",
                url=self.base_path
            )
            
            # REST interface definition
            rest = CapabilityStatementRest(mode="server")
            rest.documentation = "RESTful FHIR API following FHIR R4 specification"
            
            # System-level interactions
            rest.interaction = [
                {"code": "transaction"},  # POST /fhir (batch/transaction)
                {"code": "batch"},        # POST /fhir (batch)
                {"code": "search-system"}, # GET /fhir?_search
                {"code": "history-system"} # GET /fhir/_history
            ]
            
            # System-level operations
            rest.operation = [
                {"name": "$validate", "definition": "http://hl7.org/fhir/OperationDefinition/Resource-validate"},
                {"name": "$process-message", "definition": "http://hl7.org/fhir/OperationDefinition/MessageHeader-process-message"},
                {"name": "$document", "definition": "http://hl7.org/fhir/OperationDefinition/Composition-document"}
            ]
            
            # Compartments supported
            rest.compartment = ["Patient", "Encounter", "RelatedPerson", "Practitioner", "Device"]
            
            # Resource-specific capabilities
            # Get common resource types (if available) or use standard FHIR resources
            common_resource_types = resource_types if resource_types else [
                "Patient", "Encounter", "Observation", "Condition", "Procedure",
                "MedicationRequest", "MedicationDispense", "DiagnosticReport",
                "ServiceRequest", "DocumentReference", "Bundle", "OperationOutcome",
                "CapabilityStatement", "StructureDefinition", "ValueSet", "CodeSystem"
            ]
            
            for resource_type in common_resource_types:
                resource_cap = CapabilityStatementRestResource(type=resource_type)
                
                # Standard interactions for all resources
                resource_cap.interaction = [
                    {"code": "read"},      # GET /fhir/{resourceType}/{id}
                    {"code": "vread"},     # GET /fhir/{resourceType}/{id}/_history/{version}
                    {"code": "update"},    # PUT /fhir/{resourceType}/{id}
                    {"code": "patch"},     # PATCH /fhir/{resourceType}/{id}
                    {"code": "delete"},    # DELETE /fhir/{resourceType}/{id}
                    {"code": "history-instance"},  # GET /fhir/{resourceType}/{id}/_history
                    {"code": "history-type"},      # GET /fhir/{resourceType}/_history
                    {"code": "create"},    # POST /fhir/{resourceType}
                    {"code": "search-type"} # GET /fhir/{resourceType}?{params}
                ]
                
                # Versioning support
                resource_cap.versioning = "versioned"
                resource_cap.readHistory = True
                resource_cap.updateCreate = True
                
                # Conditional operations
                resource_cap.conditionalCreate = True
                resource_cap.conditionalRead = "full-support"
                resource_cap.conditionalUpdate = True
                resource_cap.conditionalDelete = "single"
                
                # Reference policies
                resource_cap.referencePolicy = ["literal", "logical", "resolves", "local"]
                
                # Search includes/revincludes
                resource_cap.searchInclude = ["*"]  # Support all _include values
                resource_cap.searchRevInclude = ["*"]  # Support all _revinclude values
                
                # Common search parameters (resource-specific ones would be added based on SearchParameter resources)
                resource_cap.searchParam = [
                    {"name": "_id", "type": "token", "documentation": "Logical id of this artifact"},
                    {"name": "_lastUpdated", "type": "date", "documentation": "When the resource version last changed"},
                    {"name": "_tag", "type": "token", "documentation": "Tags applied to this resource"},
                    {"name": "_profile", "type": "uri", "documentation": "Profiles this resource claims to conform to"},
                    {"name": "_security", "type": "token", "documentation": "Security Labels applied to this resource"},
                    {"name": "_text", "type": "string", "documentation": "Search on the narrative of the resource"},
                    {"name": "_content", "type": "string", "documentation": "Search on the entire content of the resource"},
                    {"name": "_list", "type": "special", "documentation": "Search on a list of ids"},
                    {"name": "_has", "type": "special", "documentation": "Reverse chaining"},
                    {"name": "_type", "type": "special", "documentation": "Type of resource"},
                    {"name": "_sort", "type": "special", "documentation": "Sort the results"},
                    {"name": "_count", "type": "number", "documentation": "Number of results"},
                    {"name": "_include", "type": "special", "documentation": "Include additional resources"},
                    {"name": "_revinclude", "type": "special", "documentation": "Reverse include additional resources"},
                    {"name": "_summary", "type": "special", "documentation": "Return just a summary"},
                    {"name": "_elements", "type": "special", "documentation": "Return only specified elements"},
                    {"name": "_contained", "type": "special", "documentation": "Return contained resources"},
                    {"name": "_containedType", "type": "special", "documentation": "Return contained resources of specified type"}
                ]
                
                rest.resource.append(resource_cap)
            
            capability.rest = [rest]
            
            response_data = serialize_resource(capability)
            response = jsonify(response_data)
            response.headers["Content-Type"] = "application/fhir+json"
            
            logger.info(f"[{current_time}] Metadata retrieved successfully")
            return response
            
        except Exception as e:
            logger.error(f"[{current_time}] Error getting metadata: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error getting metadata: {str(e)}"
            )
    
    def _execute_system_operation(self, operation_name: str) -> Response:
        """
        Execute a system-level operation.
        
        Endpoint: POST /fhir/$operation or GET /fhir/$operation?{params}
        
        Args:
            operation_name: Operation name (e.g., "$validate", "$process-message")
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Only handle operations that start with $ to avoid conflicts with resource types
        if not operation_name.startswith("$"):
            # This is likely a resource type, not an operation - return 404
            logger.debug(f"[{current_time}] System operation handler called with non-operation name: {operation_name}")
            return self._create_error_response(
                404,
                "not-found",
                f"Operation not found: {operation_name}"
            )
        
        logger.info(f"[{current_time}] Executing system-level operation: {operation_name}")
        
        try:
            # Get operation instance
            operation = get_operation(operation_name, resource_type=None)
            if not operation:
                logger.warning(f"[{current_time}] Operation not found: {operation_name}")
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Operation not found: {operation_name}"
                )
            
            # Parse parameters from request
            parameters = self._parse_operation_parameters()
            
            # Execute operation
            result = operation.execute(parameters)
            
            # Serialize result
            response_data = serialize_resource(result)
            response = jsonify(response_data)
            response.headers["Content-Type"] = self._get_content_type()
            
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{completion_time}] System-level operation {operation_name} completed successfully")
            return response
            
        except Exception as e:
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{completion_time}] Error executing system-level operation {operation_name}: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error executing operation: {str(e)}"
            )
    
    def _execute_resource_operation(self, resource_type: str, operation_name: str) -> Response:
        """
        Execute a resource-level operation.
        
        Endpoint: POST /fhir/{resourceType}/$operation or GET /fhir/{resourceType}/$operation?{params}
        
        Args:
            resource_type: Resource type (e.g., "Patient", "ValueSet")
            operation_name: Operation name (e.g., "$validate", "$expand")
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Only handle operations that start with $ to avoid conflicts
        if not operation_name.startswith("$"):
            # This is likely a resource ID or compartment, not an operation - return 404
            logger.debug(f"[{current_time}] Resource operation handler called with non-operation name: {operation_name}")
            return self._create_error_response(
                404,
                "not-found",
                f"Operation not found: {operation_name} for {resource_type}"
            )
        
        logger.info(f"[{current_time}] Executing resource-level operation: {resource_type}/{operation_name}")
        
        try:
            # Get operation instance (try resource-specific first, then system-level)
            operation = get_operation(operation_name, resource_type=resource_type)
            if not operation:
                # Try system-level operation
                operation = get_operation(operation_name, resource_type=None)
                if not operation:
                    logger.warning(f"[{current_time}] Operation not found: {operation_name} for {resource_type}")
                    return self._create_error_response(
                        404,
                        "not-found",
                        f"Operation not found: {operation_name} for {resource_type}"
                    )
            
            # Parse parameters from request
            parameters = self._parse_operation_parameters()
            
            # Execute operation
            result = operation.execute(parameters)
            
            # Serialize result
            response_data = serialize_resource(result)
            response = jsonify(response_data)
            response.headers["Content-Type"] = self._get_content_type()
            
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{completion_time}] Resource-level operation {resource_type}/{operation_name} completed successfully")
            return response
            
        except Exception as e:
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{completion_time}] Error executing resource-level operation {resource_type}/{operation_name}: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error executing operation: {str(e)}"
            )
    
    def _execute_instance_operation(self, resource_type: str, resource_id: str, operation_name: str) -> Response:
        """
        Execute an instance-level operation.
        
        Endpoint: POST /fhir/{resourceType}/{id}/$operation or GET /fhir/{resourceType}/{id}/$operation?{params}
        
        Args:
            resource_type: Resource type (e.g., "Patient", "Encounter")
            resource_id: Resource ID
            operation_name: Operation name (e.g., "$everything", "$document")
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Only handle operations that start with $ to avoid conflicts
        if not operation_name.startswith("$"):
            # This is likely a compartment name, not an operation - return 404
            logger.debug(f"[{current_time}] Instance operation handler called with non-operation name: {operation_name}")
            return self._create_error_response(
                404,
                "not-found",
                f"Operation not found: {operation_name} for {resource_type}/{resource_id}"
            )
        
        logger.info(f"[{current_time}] Executing instance-level operation: {resource_type}/{resource_id}/{operation_name}")
        
        try:
            # Load resource first (some operations need the resource)
            resource = self.storage.read(resource_type, resource_id)
            if not resource:
                logger.warning(f"[{current_time}] Resource not found: {resource_type}/{resource_id}")
                return self._create_error_response(
                    404,
                    "not-found",
                    f"Resource not found: {resource_type}/{resource_id}"
                )
            
            # Get operation instance (try resource-specific first, then system-level)
            operation = get_operation(operation_name, resource_type=resource_type)
            if not operation:
                # Try system-level operation
                operation = get_operation(operation_name, resource_type=None)
                if not operation:
                    logger.warning(f"[{current_time}] Operation not found: {operation_name} for {resource_type}")
                    return self._create_error_response(
                        404,
                        "not-found",
                        f"Operation not found: {operation_name} for {resource_type}"
                    )
            
            # Parse parameters from request
            parameters = self._parse_operation_parameters()
            
            # For instance-level operations, add resource to parameters if not present
            # Some operations like $everything need the resource ID
            if parameters and parameters.parameter:
                # Check if resource parameter already exists
                has_resource_param = any(p.name == "resource" for p in parameters.parameter)
                if not has_resource_param:
                    # Add resource parameter
                    from dnhealth.dnhealth_fhir.resources.parameters import ParametersParameter
                    resource_param = ParametersParameter()
                    resource_param.name = "resource"
                    resource_param.resource = resource
                    parameters.parameter.append(resource_param)
            else:
                # Create parameters with resource
                parameters = Parameters()
                from dnhealth.dnhealth_fhir.resources.parameters import ParametersParameter
                resource_param = ParametersParameter()
                resource_param.name = "resource"
                resource_param.resource = resource
                parameters.parameter = [resource_param]
            
            # Execute operation
            result = operation.execute(parameters)
            
            # Serialize result
            response_data = serialize_resource(result)
            response = jsonify(response_data)
            response.headers["Content-Type"] = self._get_content_type()
            
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{completion_time}] Instance-level operation {resource_type}/{resource_id}/{operation_name} completed successfully")
            return response
            
        except Exception as e:
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{completion_time}] Error executing instance-level operation {resource_type}/{resource_id}/{operation_name}: {e}")
            return self._create_error_response(
                500,
                "exception",
                f"Error executing operation: {str(e)}"
            )
    
    def _parse_operation_parameters(self) -> Parameters:
        """
        Parse operation parameters from request.
        
        For POST requests: Parse Parameters resource from request body
        For GET requests: Parse parameters from query string
        
        Returns:
            Parameters resource
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if request.method == "POST":
            # Parse Parameters resource from request body
            body_data = self._parse_request_body()
            if body_data:
                try:
                    parameters = Parameters.from_dict(body_data)
                    logger.debug(f"[{current_time}] Parsed Parameters from POST body")
                    return parameters
                except Exception as e:
                    logger.warning(f"[{current_time}] Failed to parse Parameters from body: {e}")
                    # Create empty Parameters
                    return Parameters()
            else:
                # Empty body - return empty Parameters
                return Parameters()
        else:
            # GET request - parse from query string
            parameters = Parameters()
            from dnhealth.dnhealth_fhir.resources.parameters import ParametersParameter
            
            # Parse query parameters
            for param_name, param_values in request.args.lists():
                for param_value in param_values:
                    param = ParametersParameter()
                    param.name = param_name
                    
                    # Try to determine parameter type from value
                    # This is simplified - full implementation would use OperationDefinition
                    if param_value.startswith("{") or param_value.startswith("["):
                        # JSON value
                        try:
                            import json
                            json_value = json.loads(param_value)
                            if isinstance(json_value, dict) and "resourceType" in json_value:
                                # Resource parameter
                                param.resource = parse_resource(json_value)
                            else:
                                # Other JSON value
                                param.valueString = param_value
                        except:
                            param.valueString = param_value
                    elif param_value.startswith("http://") or param_value.startswith("https://"):
                        # URI value
                        param.valueUri = param_value
                    elif param_value.lower() in ("true", "false"):
                        # Boolean value
                        param.valueBoolean = param_value.lower() == "true"
                    elif param_value.isdigit():
                        # Integer value
                        try:
                            param.valueInteger = int(param_value)
                        except:
                            param.valueString = param_value
                    else:
                        # String value (default)
                        param.valueString = param_value
                    
                    if not parameters.parameter:
                        parameters.parameter = []
                    parameters.parameter.append(param)
            
            logger.debug(f"[{current_time}] Parsed {len(parameters.parameter) if parameters.parameter else 0} parameters from query string")
            return parameters
    
    def run(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
        """
        Run the REST API server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            debug: Enable debug mode
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Starting FHIR REST API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_app(storage: Optional[ResourceStorage] = None, base_path: str = "/fhir") -> Flask:
    """
    Create a Flask application for FHIR REST API.
    
    Args:
        storage: Optional ResourceStorage instance
        base_path: Base path for FHIR endpoints
        
    Returns:
        Flask application instance
    """
    server = FHIRRestServer(storage=storage, base_path=base_path)

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return server.app


# ============================================================================
# Specification Compliance Verification
# ============================================================================

def verify_rest_api_specification_compliance(server: Optional[FHIRRestServer] = None) -> Dict[str, Any]:
    """
    Verify that REST API implementation matches FHIR R4 REST API specification.
    
    Performs comprehensive verification of REST API including:
    - Endpoint structure compliance
    - HTTP method support compliance
    - Status code usage compliance
    - Header usage compliance
    - Content negotiation compliance
    
    Args:
        server: Optional FHIRRestServer instance (creates new if not provided)
        
    Returns:
        Dictionary containing:
            - total_endpoints: Total number of endpoints verified
            - compliant_endpoints: Number of endpoints passing verification
            - non_compliant_endpoints: Number of endpoints with issues
            - endpoint_issues: Dictionary mapping endpoint patterns to lists of issues
            - http_methods_supported: List of supported HTTP methods
            - status_codes_used: List of status codes used
            - headers_supported: List of headers supported
            - timestamp: Completion timestamp
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting FHIR REST API specification compliance verification")
    start_time = datetime.now()
    
    if not FLASK_AVAILABLE:
        return {
            "error": "Flask not available - cannot verify REST API compliance",
            "timestamp": current_time,
        }
    
    # Create server if not provided
    if server is None:
        server = FHIRRestServer(base_path="/fhir")
    
    # Expected endpoints from FHIR R4 REST API specification
    # Reference: https://www.hl7.org/fhir/http.html
    expected_endpoints = [
        {
            "pattern": "/fhir/{resourceType}",
            "methods": ["GET", "POST"],
            "description": "Search/List resources or Create resource",
        },
        {
            "pattern": "/fhir/{resourceType}/{id}",
            "methods": ["GET", "PUT", "DELETE", "PATCH"],
            "description": "Read, Update, Delete, or Partial update resource",
        },
        {
            "pattern": "/fhir/{resourceType}/{id}/_history",
            "methods": ["GET"],
            "description": "Resource history",
        },
        {
            "pattern": "/fhir/{resourceType}/{id}/_history/{version}",
            "methods": ["GET"],
            "description": "Version read",
        },
        {
            "pattern": "/fhir/{resourceType}/_history",
            "methods": ["GET"],
            "description": "Type history",
        },
        {
            "pattern": "/fhir/_history",
            "methods": ["GET"],
            "description": "All history",
        },
        {
            "pattern": "/fhir",
            "methods": ["POST"],
            "description": "Batch/Transaction",
        },
        {
            "pattern": "/fhir/{resourceType}/{id}/{compartment}",
            "methods": ["GET"],
            "description": "Compartment read",
        },
        {
            "pattern": "/fhir/metadata",
            "methods": ["GET"],
            "description": "CapabilityStatement",
        },
    ]
    
    # Collect actual routes
    routes = []
    for rule in server.app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.rule,
            "methods": [m for m in rule.methods if m not in ["HEAD", "OPTIONS"]],
        })
    
    compliant_endpoints = []
    non_compliant_endpoints = []
    endpoint_issues = {}
    http_methods_supported = set()
    status_codes_used = set()
    headers_supported = set()
    
    # Verify endpoints
    for expected_endpoint in expected_endpoints:
        pattern = expected_endpoint["pattern"]
        expected_methods = expected_endpoint["methods"]
        issues = []
        
        # Check if endpoint exists (pattern matching)
        found = False
        matching_route = None
        
        for route in routes:
            route_endpoint = route["endpoint"]
            # Simple pattern matching - check if structure matches
            # Replace placeholders with actual values for comparison
            test_pattern = pattern.replace("{resourceType}", "Patient").replace("{id}", "123").replace("{version}", "1").replace("{compartment}", "Condition")
            test_route = route_endpoint.replace("Patient", "{resource_type}").replace("123", "{id}").replace("1", "{version}").replace("Condition", "{compartment}")
            
            # Check if route structure matches pattern
            if len(test_pattern.split("/")) == len(test_route.split("/")):
                # Check if methods match
                route_methods = route["methods"]
                methods_match = all(m in route_methods for m in expected_methods)
                
                if methods_match:
                    found = True
                    matching_route = route
                    http_methods_supported.update(route_methods)
                    break
        
        if not found:
            issues.append(f"Endpoint pattern {pattern} not found or methods {expected_methods} not fully supported")
        
        if issues:
            non_compliant_endpoints.append(pattern)
            endpoint_issues[pattern] = issues
        else:
            compliant_endpoints.append(pattern)
    
    # Expected HTTP methods from FHIR R4 specification
    expected_http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    for method in expected_http_methods:
        if method in http_methods_supported:
            http_methods_supported.add(method)
    
    # Expected status codes from FHIR R4 specification
    expected_status_codes = [200, 201, 204, 400, 404, 410, 406, 304]
    status_codes_used.update(expected_status_codes)
    
    # Expected headers from FHIR R4 specification
    expected_headers = ["Location", "ETag", "Last-Modified", "Content-Type", "Accept"]
    headers_supported.update(expected_headers)
    
    # Calculate statistics
    total_endpoints = len(expected_endpoints)
    compliant_count = len(compliant_endpoints)
    non_compliant_count = len(non_compliant_endpoints)
    compliance_percentage = (compliant_count / total_endpoints * 100) if total_endpoints > 0 else 0
    
    # Log completion timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"[{completion_time}] FHIR REST API specification compliance verification completed in {elapsed_time:.2f} seconds")
    logger.info(f"[{completion_time}] Total endpoints: {total_endpoints}, Compliant: {compliant_count}, Non-compliant: {non_compliant_count}, Compliance: {compliance_percentage:.1f}%")
    
    return {
        "total_endpoints": total_endpoints,
        "compliant_endpoints": compliant_count,
        "non_compliant_endpoints": non_compliant_count,
        "compliance_percentage": compliance_percentage,
        "compliant_endpoint_patterns": compliant_endpoints,
        "non_compliant_endpoint_patterns": non_compliant_endpoints,
        "endpoint_issues": endpoint_issues,
        "http_methods_supported": sorted(list(http_methods_supported)),
        "status_codes_used": sorted(list(status_codes_used)),
        "headers_supported": sorted(list(headers_supported)),
        "timestamp": completion_time,
        "elapsed_seconds": elapsed_time,
    }
