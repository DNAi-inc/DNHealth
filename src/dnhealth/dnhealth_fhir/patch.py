# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Patch Support.

Provides comprehensive patch operations for FHIR resources including:
- JSON Patch (RFC 6902) support
- FHIR Patch format support
- Patch validation
- Patch application with proper error handling

All operations include timestamps in logs for traceability.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from copy import deepcopy
import json
import logging
from datetime import datetime

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
from dnhealth.dnhealth_fhir.resources.parameters import Parameters

logger = logging.getLogger(__name__)


class PatchError(Exception):
    """Exception raised for patch operation errors."""
    
    def __init__(self, message: str, operation: Optional[Dict[str, Any]] = None):
        """
        Initialize patch error.
        
        Args:
            message: Error message
            operation: Optional patch operation that caused the error
        """
        super().__init__(message)
        self.message = message
        self.operation = operation
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def apply_json_patch(
    resource: Union[FHIRResource, Dict[str, Any]],
    patch_operations: List[Dict[str, Any]],    validate: bool = True
) -> Tuple[Union[FHIRResource, Dict[str, Any]], List[str]]:
    """
    Apply JSON Patch operations (RFC 6902) to a FHIR resource.
    
    Args:
        resource: FHIR resource (as object or dict) to patch
        patch_operations: List of JSON Patch operations
                         Format: [{"op": "add", "path": "/field", "value": value}, ...]
        validate: Whether to validate patch operations before applying
        
    Returns:
        Tuple of (patched_resource, list_of_errors)
        
    Raises:
        PatchError: If patch operation fails
        
    Example:
        patch_ops = [
            {"op": "replace", "path": "/status", "value": "active"},
            {"op": "add", "path": "/name/0/given", "value": ["John"]}
        ]
        patched, errors = apply_json_patch(patient, patch_ops)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Applying JSON Patch with {len(patch_operations)} operations")
    
    errors = []
    
    # Validate patch operations if requested
    if validate:
        validation_errors = validate_json_patch_operations(patch_operations)
        if validation_errors:
            errors.extend(validation_errors)
            if errors:
                logger.warning(f"[{current_time}] Patch validation failed: {errors}")
                return resource, errors
    
    # Convert resource to dict if needed
    if isinstance(resource, FHIRResource):
        resource_dict = resource.to_dict() if hasattr(resource, 'to_dict') else resource.__dict__
    else:
        resource_dict = deepcopy(resource)
    
    # Apply each patch operation
    patched_dict = deepcopy(resource_dict)
    
    for i, op in enumerate(patch_operations):
        try:
            op_type = op.get("op")
            path = op.get("path", "")
            
            if op_type == "add":
                _json_patch_add(patched_dict, path, op.get("value"))
            elif op_type == "remove":
                _json_patch_remove(patched_dict, path)
            elif op_type == "replace":
                _json_patch_replace(patched_dict, path, op.get("value"))
            elif op_type == "move":
                from_path = op.get("from")
                if not from_path:
                    errors.append(f"Operation {i}: 'move' requires 'from' field")
                    continue
                _json_patch_move(patched_dict, from_path, path)
            elif op_type == "copy":
                from_path = op.get("from")
                if not from_path:
                    errors.append(f"Operation {i}: 'copy' requires 'from' field")
                    continue
                _json_patch_copy(patched_dict, from_path, path)
            elif op_type == "test":
                test_value = op.get("value")
                if not _json_patch_test(patched_dict, path, test_value):
                    errors.append(f"Operation {i}: 'test' failed at path '{path}'")
                    continue
            else:
                errors.append(f"Operation {i}: Unknown operation type '{op_type}'")
                continue
                
        except Exception as e:
            error_msg = f"Operation {i} failed: {str(e)}"
            errors.append(error_msg)
            logger.warning(f"[{current_time}] {error_msg}")
            continue
    
    # Convert back to resource object if original was a resource
    if isinstance(resource, FHIRResource):
        # Try to reconstruct resource from dict
        try:
            resource_type = patched_dict.get("resourceType") or resource.resourceType
            from dnhealth.dnhealth_fhir.parser_json import parse_resource
            patched_resource = parse_resource(json.dumps(patched_dict))
        except Exception as e:
            logger.error(f"[{current_time}] Failed to reconstruct resource: {e}")
            errors.append(f"Failed to reconstruct resource: {str(e)}")
            patched_resource = resource
    else:
        patched_resource = patched_dict
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if errors:
        logger.warning(f"[{current_time}] Patch completed with {len(errors)} errors")
    else:
        logger.debug(f"[{current_time}] Patch completed successfully")
    

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return patched_resource, errors


def apply_fhir_patch(
    resource: Union[FHIRResource, Dict[str, Any]],
    patch_parameters: Union[Parameters, Dict[str, Any]],
    validate: bool = True
) -> Tuple[Union[FHIRResource, Dict[str, Any]], List[str]]:
    """
    Apply FHIR Patch operations to a FHIR resource.
    
    FHIR Patch uses Parameters resource with operation definitions.
    
    Args:
        resource: FHIR resource (as object or dict) to patch
        patch_parameters: Parameters resource containing patch operations
                         Format: Parameters with parameter entries containing operation details
        validate: Whether to validate patch operations before applying
        
    Returns:
        Tuple of (patched_resource, list_of_errors)
        
    Example:
        parameters = Parameters(
            parameter=[
                {
                    "name": "operation",
                    "part": [
                        {"name": "type", "valueString": "replace"},
                        {"name": "path", "valueString": "Patient.status"},
                        {"name": "value", "valueString": "active"}
                    ]
                }
            ]
        )
        patched, errors = apply_fhir_patch(patient, parameters)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Applying FHIR Patch")
    
    # Convert Parameters to dict if needed
    if isinstance(patch_parameters, Parameters):
        params_dict = patch_parameters.to_dict() if hasattr(patch_parameters, 'to_dict') else patch_parameters.__dict__
    else:
        params_dict = patch_parameters
    
    # Extract operations from Parameters
    operations = []
    parameters = params_dict.get("parameter", [])
    
    for param in parameters:
        if param.get("name") == "operation":
            parts = param.get("part", [])
            operation = {}
            for part in parts:
                part_name = part.get("name")
                # Extract value from various value types
                value = None
                for key in part:
                    if key.startswith("value"):
                        value = part[key]
                        break
                
                if part_name == "type":
                    operation["op"] = value
                elif part_name == "path":
                    operation["path"] = value
                elif part_name == "value":
                    operation["value"] = value
                elif part_name == "from":
                    operation["from"] = value
            
            if operation.get("op") and operation.get("path"):
                operations.append(operation)
    
    # Convert FHIR paths to JSON Patch paths
    json_patch_ops = []
    for op in operations:
        json_op = {
            "op": op.get("op"),
            "path": _fhir_path_to_json_path(op.get("path", ""))
        }
        if "value" in op:
            json_op["value"] = op["value"]
        if "from" in op:
            json_op["from"] = _fhir_path_to_json_path(op["from"])
        json_patch_ops.append(json_op)
    
    # Apply as JSON Patch
    return apply_json_patch(resource, json_patch_ops, validate)


def validate_json_patch_operations(patch_operations: List[Dict[str, Any]]) -> List[str]:
    """
    Validate JSON Patch operations.
    
    Args:
        patch_operations: List of patch operations
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    valid_ops = {"add", "remove", "replace", "move", "copy", "test"}
    
    for i, op in enumerate(patch_operations):
        if not isinstance(op, dict):
            errors.append(f"Operation {i}: Must be a dictionary")
            continue
        
        op_type = op.get("op")
        if not op_type:
            errors.append(f"Operation {i}: Missing 'op' field")
            continue
        
        if op_type not in valid_ops:
            errors.append(f"Operation {i}: Invalid operation type '{op_type}'")
            continue
        
        path = op.get("path")
        if not path:
            errors.append(f"Operation {i}: Missing 'path' field")
            continue
        
        # Validate path format
        if not path.startswith("/"):
            errors.append(f"Operation {i}: Path must start with '/'")
        
        # Validate required fields based on operation type
        if op_type in {"add", "replace"}:
            if "value" not in op:
                errors.append(f"Operation {i}: '{op_type}' requires 'value' field")
        
        if op_type in {"move", "copy"}:
            if "from" not in op:
                errors.append(f"Operation {i}: '{op_type}' requires 'from' field")
        
        if op_type == "test":
            if "value" not in op:
                errors.append(f"Operation {i}: 'test' requires 'value' field")
    
    return errors


def _json_patch_add(obj: Any, path: str, value: Any) -> None:
    """Add value at path."""
    parts = _parse_json_path(path)
    target = obj
    
    # Navigate to parent
    for part in parts[:-1]:
        target = _get_path_component(target, part, create=True)
    
    # Set value
    final_key = parts[-1]
    if isinstance(target, dict):
        target[final_key] = value
    elif isinstance(target, list):
        if final_key == "-":
            # Append to end
            target.append(value)
        else:
            idx = int(final_key)
            if idx == len(target):
                target.append(value)
            else:
                target.insert(idx, value)
    else:
        setattr(target, final_key, value)


def _json_patch_remove(obj: Any, path: str) -> None:
    """Remove value at path."""
    parts = _parse_json_path(path)
    target = obj
    
    # Navigate to parent
    for part in parts[:-1]:
        target = _get_path_component(target, part, create=False)
        if target is None:
            raise ValueError(f"Path not found: {path}")
    
    # Remove value
    final_key = parts[-1]
    if isinstance(target, dict):
        if final_key not in target:
            raise ValueError(f"Key not found: {final_key}")
        del target[final_key]
    elif isinstance(target, list):
        idx = int(final_key)
        if idx >= len(target):
            raise ValueError(f"Index out of range: {idx}")
        del target[idx]
    else:
        if not hasattr(target, final_key):
            raise ValueError(f"Attribute not found: {final_key}")
        delattr(target, final_key)


def _json_patch_replace(obj: Any, path: str, value: Any) -> None:
    """Replace value at path."""
    parts = _parse_json_path(path)
    target = obj
    
    # Navigate to target
    for part in parts[:-1]:
        target = _get_path_component(target, part, create=False)
        if target is None:
            raise ValueError(f"Path not found: {path}")
    
    # Replace value
    final_key = parts[-1]
    if isinstance(target, dict):
        if final_key not in target:
            raise ValueError(f"Key not found: {final_key}")
        target[final_key] = value
    elif isinstance(target, list):
        idx = int(final_key)
        if idx >= len(target):
            raise ValueError(f"Index out of range: {idx}")
        target[idx] = value
    else:
        if not hasattr(target, final_key):
            raise ValueError(f"Attribute not found: {final_key}")
        setattr(target, final_key, value)


def _json_patch_move(obj: Any, from_path: str, to_path: str) -> None:
    """Move value from one path to another."""
    # Get value from source
    parts_from = _parse_json_path(from_path)
    source = obj
    for part in parts_from[:-1]:
        source = _get_path_component(source, part, create=False)
        if source is None:
            raise ValueError(f"Source path not found: {from_path}")
    
    final_key_from = parts_from[-1]
    if isinstance(source, dict):
        value = source.get(final_key_from)
        if value is None:
            raise ValueError(f"Source key not found: {final_key_from}")
        del source[final_key_from]
    elif isinstance(source, list):
        idx = int(final_key_from)
        if idx >= len(source):
            raise ValueError(f"Source index out of range: {idx}")
        value = source[idx]
        del source[idx]
    else:
        if not hasattr(source, final_key_from):
            raise ValueError(f"Source attribute not found: {final_key_from}")
        value = getattr(source, final_key_from)
        delattr(source, final_key_from)
    
    # Add value to destination
    _json_patch_add(obj, to_path, value)


def _json_patch_copy(obj: Any, from_path: str, to_path: str) -> None:
    """Copy value from one path to another."""
    # Get value from source
    parts_from = _parse_json_path(from_path)
    source = obj
    for part in parts_from[:-1]:
        source = _get_path_component(source, part, create=False)
        if source is None:
            raise ValueError(f"Source path not found: {from_path}")
    
    final_key_from = parts_from[-1]
    if isinstance(source, dict):
        value = deepcopy(source.get(final_key_from))
        if value is None:
            raise ValueError(f"Source key not found: {final_key_from}")
    elif isinstance(source, list):
        idx = int(final_key_from)
        if idx >= len(source):
            raise ValueError(f"Source index out of range: {idx}")
        value = deepcopy(source[idx])
    else:
        if not hasattr(source, final_key_from):
            raise ValueError(f"Source attribute not found: {final_key_from}")
        value = deepcopy(getattr(source, final_key_from))
    
    # Add value to destination
    _json_patch_add(obj, to_path, value)


def _json_patch_test(obj: Any, path: str, value: Any) -> bool:
    """Test if value at path matches expected value."""
    parts = _parse_json_path(path)
    target = obj
    
    # Navigate to target
    for part in parts:
        target = _get_path_component(target, part, create=False)
        if target is None:
            return False
    
    # Compare values
    return target == value


def _parse_json_path(path: str) -> List[str]:
    """Parse JSON Patch path into components."""
    if not path.startswith("/"):
        raise ValueError(f"Path must start with '/': {path}")
    
    # Remove leading slash and split
    parts = path[1:].split("/")
    return [p for p in parts if p]


def _fhir_path_to_json_path(fhir_path: str) -> str:
    """
    Convert FHIR path to JSON Patch path.
    
    Examples:
        "Patient.status" -> "/status"
        "Patient.name[0].given" -> "/name/0/given"
        "Patient.name[0].given[0]" -> "/name/0/given/0"
    """
    if not fhir_path:
        return "/"
    
    # Remove resource type prefix if present
    parts = fhir_path.split(".")
    if len(parts) > 1 and parts[0][0].isupper():
        # First part is resource type, remove it
        parts = parts[1:]
    
    # Convert to JSON Patch format
    json_parts = []
    for part in parts:
        if "[" in part:
            # Handle array notation: field[0] -> field/0
            field_name, index = part.split("[")
            index = index.rstrip("]")
            json_parts.append(field_name)
            json_parts.append(index)
        else:
            json_parts.append(part)
    
    return "/" + "/".join(json_parts)


def _get_path_component(obj: Any, key: str, create: bool = False) -> Any:
    """
    Get component from object by key.
    
    Args:
        obj: Object (dict, list, or object)
        key: Key/index to access
        create: Whether to create missing components
        
    Returns:
        Component value or None
    """
    if isinstance(obj, dict):
        if key not in obj:
            if create:
                obj[key] = {}
            else:
                return None
        return obj[key]
    elif isinstance(obj, list):
        try:
            idx = int(key)
            if idx >= len(obj):
                if create:
                    # Extend list if needed
                    while len(obj) <= idx:
                        obj.append({})
                else:
                    return None
            return obj[idx]
        except ValueError:
            return None
    else:
        # Object attribute
        if hasattr(obj, key):
            return getattr(obj, key)
        elif create:
            setattr(obj, key, {})

            # Log completion timestamp at end of operation
            return getattr(obj, key)
        else:
            return None


def create_patch_operation(
    operation_type: str,
    path: str,
    value: Optional[Any] = None,
    from_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a JSON Patch operation.
    
    Args:
        operation_type: Operation type ("add", "remove", "replace", "move", "copy", "test")
        path: JSON Patch path (e.g., "/status" or "/name/0/given")
        value: Value for add/replace/test operations
        from_path: Source path for move/copy operations
        
    Returns:
        Patch operation dictionary
        
    Example:
        op = create_patch_operation("replace", "/status", "active")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Creating patch operation: {operation_type} at {path}")
    
    op = {
        "op": operation_type,

            # Log completion timestamp at end of operation
        "path": path
    }
    
    if value is not None:
        op["value"] = value
    
    if from_path is not None:
        op["from"] = from_path
    
    return op


def create_fhir_patch_parameters(operations: List[Dict[str, Any]]) -> Parameters:
    """
    Create FHIR Parameters resource from patch operations.
    
    Args:
        operations: List of patch operations (can be JSON Patch format)
        
    Returns:
        Parameters resource
        
    Example:
        ops = [
            {"op": "replace", "path": "/status", "value": "active"}
        ]
        params = create_fhir_patch_parameters(ops)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Creating FHIR Patch Parameters from {len(operations)} operations")
    
    parameter_list = []
    
    for op in operations:
        op_type = op.get("op")
        path = op.get("path", "")
        
        # Convert JSON Patch path to FHIR path if needed
        fhir_path = _json_path_to_fhir_path(path)
        
        parts = [
            {"name": "type", "valueString": op_type},
            {"name": "path", "valueString": fhir_path}
        ]
        
        if "value" in op:
            # Determine value type and add appropriate part
            value = op["value"]
            if isinstance(value, str):
                parts.append({"name": "value", "valueString": value})
            elif isinstance(value, bool):
                parts.append({"name": "value", "valueBoolean": value})
            elif isinstance(value, int):
                parts.append({"name": "value", "valueInteger": value})
            elif isinstance(value, float):
                parts.append({"name": "value", "valueDecimal": value})
            else:
                # Complex value - serialize as JSON string
                parts.append({"name": "value", "valueString": json.dumps(value)})
        
        if "from" in op:
            from_fhir_path = _json_path_to_fhir_path(op["from"])
            parts.append({"name": "from", "valueString": from_fhir_path})
        
        parameter_list.append({
            "name": "operation",
            "part": parts
        })
    
    return Parameters(parameter=parameter_list)


def _json_path_to_fhir_path(json_path: str) -> str:
    """
    Convert JSON Patch path to FHIR path.
    
    Examples:
        "/status" -> "status"
        "/name/0/given" -> "name[0].given"
        "/name/0/given/0" -> "name[0].given[0]"
    """
    if not json_path or json_path == "/":
        return ""
    
    parts = _parse_json_path(json_path)
    fhir_parts = []
    i = 0
    
    while i < len(parts):
        part = parts[i]
        # Check if next part is a number (array index)
        if i + 1 < len(parts) and parts[i + 1].isdigit():
            fhir_parts.append(f"{part}[{parts[i + 1]}]")
            i += 2
        else:
            fhir_parts.append(part)
            i += 1
    
    return ".".join(fhir_parts)
