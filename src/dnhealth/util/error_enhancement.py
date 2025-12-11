# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Error message enhancement utilities for DNHealth library.

Provides utilities to automatically generate JSONPath/XPath expressions,
standardize error codes, and create detailed error messages.
"""

import time
from datetime import datetime
from typing import Optional, Dict, Any, List, Union, Tuple
from dnhealth.errors import DNHealthError, FHIRParseError, FHIRValidationError, HL7v2ParseError, HL7v3ParseError

logger = logging.getLogger(__name__)


# Standardized error code registry
ERROR_CODES = {
    # HL7v2 Parse Errors
    "PARSE_001": "Invalid message format",
    "PARSE_002": "Missing required segment",
    "PARSE_003": "Invalid segment structure",
    "PARSE_004": "Field parsing error",
    "PARSE_005": "Encoding character error",
    "PARSE_006": "Invalid field separator",
    "PARSE_007": "Invalid component separator",
    "PARSE_008": "Invalid repetition separator",
    "PARSE_009": "Invalid escape character",
    "PARSE_010": "Invalid subcomponent separator",
    
    # HL7v3 Parse Errors
    "PARSE_101": "XML syntax error",
    "PARSE_102": "Schema validation error",
    "PARSE_103": "Missing required element",
    "PARSE_104": "Invalid element structure",
    "PARSE_105": "Namespace error",
    "PARSE_106": "Invalid attribute value",
    "PARSE_107": "Missing required attribute",
    "PARSE_108": "Invalid XML structure",
    
    # FHIR Parse Errors
    "PARSE_201": "JSON parsing error",
    "PARSE_202": "XML parsing error",
    "PARSE_203": "Invalid resource structure",
    "PARSE_204": "Missing required field",
    "PARSE_205": "Invalid data type",
    "PARSE_206": "Invalid resource type",
    "PARSE_207": "Invalid JSON structure",
    "PARSE_208": "Invalid XML structure",
    
    # HL7v2 Validation Errors
    "VALID_001": "Constraint violation",
    "VALID_002": "Cardinality violation",
    "VALID_003": "Data type violation",
    "VALID_004": "Value set violation",
    "VALID_005": "Table binding violation",
    "VALID_006": "Length constraint violation",
    "VALID_007": "Required field missing",
    "VALID_008": "Invalid field value",
    
    # HL7v3 Validation Errors
    "VALID_101": "Constraint violation",
    "VALID_102": "Cardinality violation",
    "VALID_103": "Data type violation",
    "VALID_104": "Value set violation",
    "VALID_105": "Schema constraint violation",
    "VALID_106": "RIM constraint violation",
    
    # FHIR Validation Errors
    "VALID_201": "Constraint violation",
    "VALID_202": "Cardinality violation",
    "VALID_203": "Data type violation",
    "VALID_204": "Value set violation",
    "VALID_205": "Profile conformance violation",
    "VALID_206": "Reference integrity violation",
    "VALID_207": "Narrative validation error",
    "VALID_208": "Extension validation error",
    
    # Client/Server Errors
    "CLIENT_001": "HTTP request error",
    "CLIENT_002": "Network error",
    "CLIENT_003": "Timeout error",
    "CLIENT_004": "Authentication error",
    "SERVER_001": "Internal server error",
    "SERVER_002": "Resource not found",
    "SERVER_003": "Method not allowed",
    "SERVER_004": "Conflict error",
}


def get_error_code_description(error_code: str) -> Optional[str]:
    """
    Get description for an error code.
    
    Args:
        error_code: Error code string
        
    Returns:
        Error code description or None if not found
    """

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return ERROR_CODES.get(error_code)


def generate_jsonpath_for_fhir_field(
    resource_type: Optional[str] = None,
    field_path: Optional[str] = None,
    field_index: Optional[int] = None,
    array_index: Optional[int] = None
) -> str:
    """
    Generate JSONPath expression for a FHIR field.
    
    Args:
        resource_type: Resource type (e.g., "Patient")
        field_path: Field path (e.g., "name.family" or "name[0].family")
        field_index: Optional field index for array fields
        array_index: Optional array index
        
    Returns:
        JSONPath expression (e.g., "$.Patient.name[0].family")
    """
    jsonpath_parts = ["$"]
    
    if resource_type:
        jsonpath_parts.append(resource_type)
    
    if field_path:
        parts = field_path.split(".")
        for part in parts:
            if "[" in part:
                # Already has array index
                jsonpath_parts.append(part)
            elif array_index is not None and part == parts[-1]:
                # Add array index to last part
                jsonpath_parts.append(f"{part}[{array_index}]")
            else:
                jsonpath_parts.append(part)
    elif field_index is not None:
        jsonpath_parts.append(f"[{field_index}]")
    

                    # Log completion timestamp at end of operation
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Current Time at End of Operations: {current_time}")
    return ".".join(jsonpath_parts)


def generate_xpath_for_hl7v3_element(
    element_name: Optional[str] = None,
    parent_path: Optional[str] = None,
    element_index: Optional[int] = None,
    attribute_name: Optional[str] = None
) -> str:
    """
    Generate XPath expression for an HL7v3 element.
    
    Args:
        element_name: Element name
        parent_path: Optional parent XPath
        element_index: Optional element index (1-based)
        attribute_name: Optional attribute name
        
    Returns:
        XPath expression (e.g., "/root/parent/child[1]/@attribute")
    """
    if parent_path:
        xpath = parent_path
    else:
        xpath = ""
    
    if element_name:
        if xpath:
            xpath += f"/{element_name}"
        else:
            xpath = f"/{element_name}"
        
        if element_index is not None:
            xpath += f"[{element_index}]"
    

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
    if attribute_name:
        xpath += f"/@{attribute_name}"
    
    return xpath


def generate_hl7v2_path(
    segment: Optional[str] = None,
    field_number: Optional[int] = None,
    component_number: Optional[int] = None,
    subcomponent_number: Optional[int] = None,
    repetition_number: Optional[int] = None
) -> str:
    """
    Generate HL7v2 field path expression.
    
    Args:
        segment: Segment name (e.g., "PID")
        field_number: Field number (1-based)
        component_number: Component number (1-based)
        subcomponent_number: Subcomponent number (1-based)
        repetition_number: Repetition number (1-based)
        
    Returns:
        HL7v2 path expression (e.g., "PID.5.1.2")
    """
    parts = []
    
    if segment:
        parts.append(segment)
    
    if field_number is not None:
        parts.append(str(field_number))
    
    if component_number is not None:
        parts.append(str(component_number))
    
    if subcomponent_number is not None:
        parts.append(str(subcomponent_number))
    
    if repetition_number is not None:
        # Repetition is typically indicated before component
        # Format: SEGMENT.FIELD[REPETITION].COMPONENT
        if len(parts) >= 2:
            parts.insert(1, f"[{repetition_number}]")
        else:
            parts.append(f"[{repetition_number}]")
    
    return ".".join(parts)


def enhance_error_message(
    error: Exception,
    resource_type: Optional[str] = None,
    field_path: Optional[str] = None,
    jsonpath: Optional[str] = None,
    xpath: Optional[str] = None,
    hl7v2_path: Optional[str] = None,
    additional_context: Optional[Dict[str, Any]] = None
) -> str:
    """
    Enhance error message with detailed context.
    
    Args:
        error: Exception object
        resource_type: Resource type (for FHIR)
        field_path: Field path
        jsonpath: JSONPath expression
        xpath: XPath expression
        hl7v2_path: HL7v2 path expression
        additional_context: Additional context dictionary
        
    Returns:
        Enhanced error message string
    """
    parts = [str(error)]
    
    if resource_type:
        parts.append(f"ResourceType: {resource_type}")
    
    if field_path:
        parts.append(f"Field: {field_path}")
    
    if jsonpath:
        parts.append(f"JSONPath: {jsonpath}")
    
    if xpath:
        parts.append(f"XPath: {xpath}")
    
    if hl7v2_path:
        parts.append(f"HL7v2Path: {hl7v2_path}")
    
    if additional_context:
        for key, value in additional_context.items():
            parts.append(f"{key}: {value}")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Add timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts.append(f"Timestamp: {current_time}")
    
    return " | ".join(parts)


def create_enhanced_fhir_error(
    message: str,
    resource_type: Optional[str] = None,
    field: Optional[str] = None,
    field_path: Optional[str] = None,
    error_code: Optional[str] = None,
    details: Optional[str] = None,
    is_validation: bool = False
) -> Union[FHIRParseError, FHIRValidationError]:
    """
    Create enhanced FHIR error with automatic JSONPath generation.
    
    Args:
        message: Error message
        resource_type: Resource type
        field: Field name
        field_path: Full field path (e.g., "name.family")
        error_code: Optional error code
        details: Optional additional details
        is_validation: Whether this is a validation error (default: False for parse error)
        
    Returns:
        FHIRParseError or FHIRValidationError with enhanced context
    """
    # Generate JSONPath if not provided
    jsonpath = None
    if field_path:
        jsonpath = generate_jsonpath_for_fhir_field(
            resource_type=resource_type,
            field_path=field_path
        )
    elif field and resource_type:
        jsonpath = generate_jsonpath_for_fhir_field(
            resource_type=resource_type,
            field_path=field
        )
    
    # Generate error code if not provided
    if not error_code:
        if is_validation:
            if "cardinality" in message.lower() or "required" in message.lower():
                error_code = "VALID_202"
            elif "type" in message.lower() or "datatype" in message.lower():
                error_code = "VALID_203"
            elif "valueset" in message.lower() or "code" in message.lower():
                error_code = "VALID_204"
            elif "profile" in message.lower() or "constraint" in message.lower():
                error_code = "VALID_205"
            else:
                error_code = "VALID_201"
        else:
            if "JSON" in message or "json" in message.lower():
                error_code = "PARSE_201"
            elif "XML" in message or "xml" in message.lower():
                error_code = "PARSE_202"
            elif field:
                error_code = "PARSE_204"
            else:
                error_code = "PARSE_203"
    
    # Create enhanced error message
    enhanced_message = enhance_error_message(
        Exception(message),
        resource_type=resource_type,
        field_path=field_path or field,
        jsonpath=jsonpath
    )
    
    if is_validation:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        return FHIRValidationError(
            message=enhanced_message,
            resource_type=resource_type,
            field=field,
            jsonpath=jsonpath,
            error_code=error_code,
            details=details
        )
    else:
        return FHIRParseError(
            message=enhanced_message,
            resource_type=resource_type,
            field=field,
            jsonpath=jsonpath,
            error_code=error_code,
            details=details
        )


def create_enhanced_hl7v3_error(
    message: str,
    element: Optional[str] = None,
    parent_path: Optional[str] = None,
    element_index: Optional[int] = None,
    line_number: Optional[int] = None,
    error_code: Optional[str] = None,
    details: Optional[str] = None
) -> HL7v3ParseError:
    """
    Create enhanced HL7v3 error with automatic XPath generation.
    
    Args:
        message: Error message
        element: Element name
        parent_path: Optional parent XPath
        element_index: Optional element index
        line_number: Optional line number
        error_code: Optional error code
        details: Optional additional details
        
    Returns:
        HL7v3ParseError with enhanced context
    """
    # Generate XPath if not provided
    xpath = None
    if element:
        xpath = generate_xpath_for_hl7v3_element(
            element_name=element,
            parent_path=parent_path,
            element_index=element_index
        )
    
    # Generate error code if not provided
    if not error_code:
        if "XML syntax" in message.lower() or "parse" in message.lower():
            error_code = "PARSE_101"
        elif "schema" in message.lower() or "validation" in message.lower():
            error_code = "PARSE_102"
        elif element:
            error_code = "PARSE_104"
        else:
            error_code = "PARSE_101"
    
    # Create enhanced error message

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
    enhanced_message = enhance_error_message(
        Exception(message),
        xpath=xpath,
        additional_context={"line_number": line_number} if line_number else None
    )
    
    return HL7v3ParseError(
        message=enhanced_message,
        element=element,
        line_number=line_number,
        xpath=xpath,
        error_code=error_code,
        details=details
    )


def create_enhanced_hl7v2_error(
    message: str,
    segment: Optional[str] = None,
    field_number: Optional[int] = None,
    component_number: Optional[int] = None,
    line_number: Optional[int] = None,
    error_code: Optional[str] = None,
    details: Optional[str] = None
) -> HL7v2ParseError:
    """
    Create enhanced HL7v2 error with automatic path generation.
    
    Args:
        message: Error message
        segment: Segment name
        field_number: Field number (1-based)
        component_number: Component number (1-based)
        line_number: Optional line number
        error_code: Optional error code
        details: Optional additional details
        
    Returns:
        HL7v2ParseError with enhanced context
    """
    # Generate HL7v2 path
    hl7v2_path = None
    if segment:
        hl7v2_path = generate_hl7v2_path(
            segment=segment,
            field_number=field_number,
            component_number=component_number
        )
    
    # Generate error code if not provided
    if not error_code:
        if segment and field_number is not None:
            error_code = "PARSE_004"
        elif segment:
            error_code = "PARSE_003"
        elif line_number is not None:
            error_code = "PARSE_001"
        else:
            error_code = "PARSE_001"
    
    # Create enhanced error message
    enhanced_message = enhance_error_message(
        Exception(message),
        hl7v2_path=hl7v2_path,
        additional_context={"line_number": line_number} if line_number else None
    )
    
    return HL7v2ParseError(
        message=enhanced_message,
        line_number=line_number,
        segment=segment,
        field_number=field_number,
        error_code=error_code,
        details=details
    )


def format_error_summary(error: DNHealthError) -> Dict[str, Any]:
    """
    Format error as a structured summary dictionary.
    
    Args:
        error: DNHealthError instance
        
    Returns:
        Dictionary with error summary
    """
    summary = {
        "message": str(error),
        "error_code": error.error_code,
        "timestamp": error.timestamp,
        "type": type(error).__name__
    }
    
    # Add location information
    if hasattr(error, "jsonpath") and error.jsonpath:
        summary["jsonpath"] = error.jsonpath
    
    if hasattr(error, "xpath") and error.xpath:
        summary["xpath"] = error.xpath
    
    if hasattr(error, "resource_type") and error.resource_type:
        summary["resource_type"] = error.resource_type
    
    if hasattr(error, "field") and error.field:
        summary["field"] = error.field
    
    if hasattr(error, "segment") and error.segment:
        summary["segment"] = error.segment
    
    if hasattr(error, "field_number") and error.field_number is not None:
        summary["field_number"] = error.field_number
    
    if hasattr(error, "element") and error.element:
        summary["element"] = error.element
    
    if hasattr(error, "line_number") and error.line_number is not None:
        summary["line_number"] = error.line_number
    
    # Add error code description
    if error.error_code:
        summary["error_description"] = get_error_code_description(error.error_code)
    
    # Add details if present
    if error.details:
        summary["details"] = error.details
    
    return summary
