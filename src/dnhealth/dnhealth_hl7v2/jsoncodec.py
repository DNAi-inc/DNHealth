# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x JSON codec.

Converts Message objects to/from JSON/dict format.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from dnhealth.dnhealth_hl7v2.model import (
    Component,
    EncodingCharacters,
    Field,
    Message,
    Segment,
    Subcomponent,
)


def message_to_dict(message: Message) -> Dict[str, Any]:
    """
    Convert Message object to dictionary.

    Args:
        message: Message object

    Returns:
        Dictionary representation
    """
    segments_data = []
    for segment in message.segments:
        segment_dict = {
            "name": segment.name,
            "fields": [],
        }
        # Serialize all field repetitions
        for field_repetitions in segment._field_repetitions:
            repetitions_list = []
            for field in field_repetitions:
                field_dict = {"components": []}
                for component in field.components:
                    component_dict = {
                        "subcomponents": [subcomp.value for subcomp in component.subcomponents]
                    }
                    field_dict["components"].append(component_dict)
                repetitions_list.append(field_dict)
            segment_dict["fields"].append({"repetitions": repetitions_list})
        segments_data.append(segment_dict)

    result = {
        "segments": segments_data,
        "encoding_chars": {
            "field_separator": message.encoding_chars.field_separator,
            "component_separator": message.encoding_chars.component_separator,
            "repetition_separator": message.encoding_chars.repetition_separator,
            "escape_character": message.encoding_chars.escape_character,
            "subcomponent_separator": message.encoding_chars.subcomponent_separator,
        },
    }
    if message.version:
        result["version"] = message.version

    return result


def dict_to_message(data: Dict[str, Any]) -> Message:
    """
    Convert dictionary to Message object.

    Args:
        data: Dictionary representation

    Returns:
        Message object
    """
    encoding_chars_data = data.get("encoding_chars", {})
    encoding_chars = EncodingCharacters(
        field_separator=encoding_chars_data.get("field_separator", "|"),
        component_separator=encoding_chars_data.get("component_separator", "^"),
        repetition_separator=encoding_chars_data.get("repetition_separator", "~"),
        escape_character=encoding_chars_data.get("escape_character", "\\"),
        subcomponent_separator=encoding_chars_data.get("subcomponent_separator", "&"),
    )

    segments = []
    for seg_data in data.get("segments", []):
        name = seg_data["name"]
        field_repetitions_list = []
        for field_data in seg_data.get("fields", []):
            # Handle both old format (single repetition) and new format (repetitions list)
            if "repetitions" in field_data:
                repetitions = []
                for rep_data in field_data["repetitions"]:
                    components = []
                    for comp_data in rep_data.get("components", []):
                        subcomponents = [
                            Subcomponent(subcomp_value)
                            for subcomp_value in comp_data.get("subcomponents", [""])
                        ]
                        components.append(Component(subcomponents))
                    repetitions.append(Field(components))
                field_repetitions_list.append(repetitions)
            else:
                # Legacy format: single repetition
                components = []
                for comp_data in field_data.get("components", []):
                    subcomponents = [
                        Subcomponent(subcomp_value)
                        for subcomp_value in comp_data.get("subcomponents", [""])
                    ]
                    components.append(Component(subcomponents))
                field_repetitions_list.append([Field(components)])
        segments.append(Segment(name, field_repetitions=field_repetitions_list))

    version = data.get("version")
    return Message(segments=segments, encoding_chars=encoding_chars, version=version)


def message_to_json(message: Message, indent: int = 2, pretty: bool = True) -> str:
    """
    Convert Message object to JSON string.

    Args:
        message: Message object
        indent: JSON indentation level (used if pretty=True)
        pretty: If True, format JSON with indentation (default: True)

    Returns:
        JSON string
    """
    data = message_to_dict(message)
    if pretty:
        result = json.dumps(data, indent=indent, ensure_ascii=False)
    else:
        result = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Message to JSON conversion completed")
    
    return result


def json_to_message(json_str: str) -> Message:
    """
    Convert JSON string to Message object.

    Args:
        json_str: JSON string

    Returns:
        Message object
    """
    data = json.loads(json_str)
    result = dict_to_message(data)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] JSON to message conversion completed")
    
    return result


def create_custom_json_schema(
    require_version: bool = False,
    require_segment_name_pattern: Optional[str] = None,
    max_segments: Optional[int] = None,
    max_fields_per_segment: Optional[int] = None,    additional_properties: bool = False,
) -> Dict[str, Any]:
    """
    Create a custom JSON schema for HL7 v2.x message JSON format.
    
    Args:
        require_version: If True, version field is required
        require_segment_name_pattern: Optional regex pattern for segment names (default: ^[A-Z0-9]{3}$)
        max_segments: Optional maximum number of segments
        max_fields_per_segment: Optional maximum number of fields per segment
        additional_properties: If True, allow additional properties not in schema
        
    Returns:
        Custom JSON schema dictionary
    """
    base_schema = get_default_json_schema()
    
    # Modify segments array schema
    segments_schema = base_schema["properties"]["segments"]
    
    if max_segments is not None:
        segments_schema["maxItems"] = max_segments
    
    # Modify segment name pattern if specified
    if require_segment_name_pattern is not None:
        segment_item_schema = segments_schema["items"]
        segment_item_schema["properties"]["name"]["pattern"] = require_segment_name_pattern
    
    # Modify fields schema if max_fields_per_segment specified
    if max_fields_per_segment is not None:
        segment_item_schema = segments_schema["items"]
        segment_item_schema["properties"]["fields"]["maxItems"] = max_fields_per_segment
    
    # Modify version requirement
    if require_version:
        if "version" not in base_schema["required"]:
            base_schema["required"].append("version")
    
    # Set additionalProperties
    base_schema["additionalProperties"] = additional_properties
    
    return base_schema


def get_default_json_schema() -> Dict[str, Any]:
    """
    Get default JSON schema for HL7 v2.x message JSON format.
    
    Returns:
        JSON schema dictionary
    """
    result = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["segments", "encoding_chars"],
        "properties": {
            "segments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "fields"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "pattern": "^[A-Z0-9]{3}$"
                        },
                        "fields": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["repetitions"],
                                "properties": {
                                    "repetitions": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["components"],
                                            "properties": {
                                                "components": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "required": ["subcomponents"],
                                                        "properties": {
                                                            "subcomponents": {
                                                                "type": "array",
                                                                "items": {"type": "string"}
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "encoding_chars": {
                "type": "object",
                "required": [
                    "field_separator",
                    "component_separator",
                    "repetition_separator",
                    "escape_character",
                    "subcomponent_separator"
                ],
                "properties": {
                    "field_separator": {"type": "string"},
                    "component_separator": {"type": "string"},
                    "repetition_separator": {"type": "string"},
                    "escape_character": {"type": "string"},
                    "subcomponent_separator": {"type": "string"}
                }
            },
            "version": {
                "type": "string",
                "pattern": "^2\\.[0-9]+$"
            }
        }
    }
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return result


def validate_json_schema(
    data: Dict[str, Any],
    schema: Optional[Dict[str, Any]] = None
) -> Tuple[bool, Optional[str], Optional[List[str]]]:
    """
    Validate JSON data against a JSON schema.
    
    Args:
        data: JSON data dictionary to validate
        schema: Optional JSON schema (default: use default HL7 v2.x schema)
        
    Returns:
        Tuple of (is_valid, error_message, validation_errors)
        - is_valid: True if data is valid, False otherwise
        - error_message: None if valid, summary error message if invalid
        - validation_errors: List of detailed validation errors (if jsonschema available)
    """
    if schema is None:
        schema = get_default_json_schema()
    
    if not JSONSCHEMA_AVAILABLE:
        # Basic validation without jsonschema library
        return _basic_json_validation(data, schema)
    
    # Use jsonschema library for full validation
    try:
        validator = jsonschema.Draft7Validator(schema)
        errors = list(validator.iter_errors(data))
        
        if errors:
            error_messages = [str(error) for error in errors]
            return False, f"JSON schema validation failed: {len(errors)} error(s)", error_messages
        return True, None, None
    except jsonschema.SchemaError as e:
        return False, f"Invalid JSON schema: {e}", None
    except Exception as e:
        return False, f"Validation error: {e}", None


def _basic_json_validation(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[List[str]]]:
    """
    Basic JSON validation without jsonschema library.
    
    Args:
        data: JSON data dictionary to validate
        schema: JSON schema dictionary
        
    Returns:
        Tuple of (is_valid, error_message, validation_errors)
    """
    errors = []
    
    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check segments structure
    if "segments" in data:
        if not isinstance(data["segments"], list):
            errors.append("'segments' must be an array")
        else:
            for i, seg in enumerate(data["segments"]):
                if not isinstance(seg, dict):
                    errors.append(f"Segment {i} must be an object")
                    continue
                if "name" not in seg:
                    errors.append(f"Segment {i} missing 'name' field")
                if "fields" not in seg:
                    errors.append(f"Segment {i} missing 'fields' field")
    
    # Check encoding_chars structure
    if "encoding_chars" in data:
        if not isinstance(data["encoding_chars"], dict):
            errors.append("'encoding_chars' must be an object")
        else:
            required_chars = schema.get("properties", {}).get("encoding_chars", {}).get("required", [])
            for char in required_chars:
                if char not in data["encoding_chars"]:
                    errors.append(f"Missing required encoding character: {char}")
    
    if errors:
        return False, f"JSON validation failed: {len(errors)} error(s)", errors
    return True, None, None


def validate_message_json(json_str: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str], Optional[List[str]]]:
    """
    Validate JSON string against a JSON schema.
    
    Args:
        json_str: JSON string to validate
        schema: Optional JSON schema (default: use default HL7 v2.x schema)
        
    Returns:
        Tuple of (is_valid, error_message, validation_errors)
    """
    try:
        data = json.loads(json_str)
        result = validate_json_schema(data, schema)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_valid = result[0]
        logger.debug(f"[{current_time}] Message JSON validation completed (valid={is_valid})")
        
        return result
    except json.JSONDecodeError as e:
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Message JSON validation completed (invalid JSON)")
        return False, f"Invalid JSON: {e}", None

