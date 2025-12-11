# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Exception hierarchy for DNHealth library.

All exceptions inherit from DNHealthError for easy catching.
"""

from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DNHealthError(Exception):
    """
    Base exception for all DNHealth errors.
    
    Provides common error handling functionality including:
    - Error codes for standardized error identification
    - JSONPath/XPath error locations
    - Detailed error messages
    - Timestamp tracking
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        jsonpath: Optional[str] = None,
        xpath: Optional[str] = None,
        details: Optional[str] = None
    ):
        """
        Initialize DNHealthError.
        
        Args:
            message: Error message
            error_code: Optional standardized error code
            jsonpath: Optional JSONPath expression indicating error location
            xpath: Optional XPath expression indicating error location
            details: Optional additional error details
        """
        super().__init__(message)
        self.error_code = error_code
        self.jsonpath = jsonpath
        self.xpath = xpath
        self.details = details
        self.timestamp = datetime.now().isoformat()
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    def __str__(self) -> str:
        """Format error message with context."""
        parts = [super().__str__()]
        
        if self.error_code:
            parts.append(f"Code: {self.error_code}")
        
        if self.jsonpath:
            parts.append(f"JSONPath: {self.jsonpath}")
        
        if self.xpath:
            parts.append(f"XPath: {self.xpath}")
        
        if self.details:
            parts.append(f"Details: {self.details}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """
        Convert error to dictionary representation.
        
        Returns:
            Dictionary with error details
        """
        result = {
            "message": str(super().__str__()),
            "timestamp": self.timestamp
        }
        
        if self.error_code:
            result["error_code"] = self.error_code
        
        if self.jsonpath:
            result["jsonpath"] = self.jsonpath
        
        if self.xpath:
            result["xpath"] = self.xpath
        
        if self.details:
            result["details"] = self.details
        
        return result


class HL7v2ParseError(DNHealthError):
    """
    Raised when HL7 v2 message parsing fails.
    
    Error codes:
    - PARSE_001: Invalid message format
    - PARSE_002: Missing required segment
    - PARSE_003: Invalid segment structure
    - PARSE_004: Field parsing error
    - PARSE_005: Encoding character error
    """

    def __init__(
        self,
        message: str,
        line_number: Optional[int] = None,
        segment: Optional[str] = None,
        field_number: Optional[int] = None,
        error_code: Optional[str] = None,
        details: Optional[str] = None
    ):
        """
        Initialize HL7v2ParseError.

        Args:
            message: Error message
            line_number: Optional line number where error occurred
            segment: Optional segment name where error occurred
            field_number: Optional field number where error occurred
            error_code: Optional standardized error code
            details: Optional additional error details
        """
        # Generate error code if not provided
        if not error_code:
            if segment and field_number is not None:
                error_code = "PARSE_004"  # Field parsing error
            elif segment:
                error_code = "PARSE_003"  # Invalid segment structure
            elif line_number is not None:
                error_code = "PARSE_001"  # Invalid message format
            else:
                error_code = "PARSE_001"  # Default
        
        super().__init__(message, error_code=error_code, details=details)
        self.line_number = line_number
        self.segment = segment
        self.field_number = field_number

    def __str__(self) -> str:
        """Format error message with context."""
        parts = [super().__str__()]
        if self.line_number is not None:
            parts.append(f"Line: {self.line_number}")
        if self.segment:
            parts.append(f"Segment: {self.segment}")
        if self.field_number is not None:
            parts.append(f"Field: {self.field_number}")
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary representation."""
        result = super().to_dict()
        if self.line_number is not None:
            result["line_number"] = self.line_number
        if self.segment:
            result["segment"] = self.segment
        if self.field_number is not None:
            result["field_number"] = self.field_number
        return result


class HL7v3ParseError(DNHealthError):
    """
    Raised when HL7 v3 XML message parsing fails.
    
    Error codes:
    - PARSE_101: XML syntax error
    - PARSE_102: Schema validation error
    - PARSE_103: Missing required element
    - PARSE_104: Invalid element structure
    - PARSE_105: Namespace error
    """

    def __init__(
        self,
        message: str,
        element: Optional[str] = None,
        line_number: Optional[int] = None,
        xpath: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[str] = None
    ):
        """
        Initialize HL7v3ParseError.

        Args:
            message: Error message
            element: Optional element name where error occurred
            line_number: Optional line number where error occurred
            xpath: Optional XPath expression indicating error location
            error_code: Optional standardized error code
            details: Optional additional error details
        """
        # Generate error code if not provided
        if not error_code:
            if "XML syntax" in message.lower() or "parse" in message.lower():
                error_code = "PARSE_101"  # XML syntax error
            elif "schema" in message.lower() or "validation" in message.lower():
                error_code = "PARSE_102"  # Schema validation error
            elif element:
                error_code = "PARSE_104"  # Invalid element structure
            else:
                error_code = "PARSE_101"  # Default
        
        super().__init__(message, error_code=error_code, xpath=xpath, details=details)
        self.element = element
        self.line_number = line_number

    def __str__(self) -> str:
        """Format error message with context."""
        parts = [super().__str__()]
        if self.element:
            parts.append(f"Element: {self.element}")
        if self.line_number is not None:
            parts.append(f"Line: {self.line_number}")
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary representation."""
        result = super().to_dict()
        if self.element:
            result["element"] = self.element
        if self.line_number is not None:
            result["line_number"] = self.line_number
        return result


class FHIRParseError(DNHealthError):
    """
    Raised when FHIR resource parsing fails.
    
    Error codes:
    - PARSE_201: JSON parsing error
    - PARSE_202: XML parsing error
    - PARSE_203: Invalid resource structure
    - PARSE_204: Missing required field
    - PARSE_205: Invalid data type
    """

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        field: Optional[str] = None,
        jsonpath: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[str] = None
    ):
        """
        Initialize FHIRParseError.

        Args:
            message: Error message
            resource_type: Optional resource type where error occurred
            field: Optional field name where error occurred
            jsonpath: Optional JSONPath expression indicating error location
            error_code: Optional standardized error code
            details: Optional additional error details
        """
        # Generate error code if not provided
        if not error_code:
            if "JSON" in message or "json" in message.lower():
                error_code = "PARSE_201"  # JSON parsing error
            elif "XML" in message or "xml" in message.lower():
                error_code = "PARSE_202"  # XML parsing error
            elif field:
                error_code = "PARSE_204"  # Missing required field
            else:
                error_code = "PARSE_203"  # Invalid resource structure
        
        super().__init__(message, error_code=error_code, jsonpath=jsonpath, details=details)
        self.resource_type = resource_type
        self.field = field

    def __str__(self) -> str:
        """Format error message with context."""
        parts = [super().__str__()]
        if self.resource_type:
            parts.append(f"ResourceType: {self.resource_type}")
        if self.field:
            parts.append(f"Field: {self.field}")
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary representation."""
        result = super().to_dict()
        if self.resource_type:
            result["resource_type"] = self.resource_type
        if self.field:
            result["field"] = self.field
        return result


class FHIRValidationError(DNHealthError):
    """
    Raised when FHIR resource validation fails.
    
    Error codes:
    - VALID_201: Constraint violation
    - VALID_202: Cardinality violation
    - VALID_203: Data type violation
    - VALID_204: Value set violation
    - VALID_205: Profile conformance violation
    """

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        field: Optional[str] = None,
        jsonpath: Optional[str] = None,
        fhirpath: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[str] = None
    ):
        """
        Initialize FHIRValidationError.

        Args:
            message: Error message
            resource_type: Optional resource type where error occurred
            field: Optional field name where error occurred
            jsonpath: Optional JSONPath expression indicating error location
            fhirpath: Optional FHIRPath expression indicating error location
            error_code: Optional standardized error code
            details: Optional additional error details
        """
        # Generate error code if not provided
        if not error_code:
            if "cardinality" in message.lower() or "required" in message.lower():
                error_code = "VALID_202"  # Cardinality violation
            elif "type" in message.lower() or "datatype" in message.lower():
                error_code = "VALID_203"  # Data type violation
            elif "valueset" in message.lower() or "code" in message.lower():
                error_code = "VALID_204"  # Value set violation
            elif "profile" in message.lower() or "constraint" in message.lower():
                error_code = "VALID_205"  # Profile conformance violation
            else:
                error_code = "VALID_201"  # Constraint violation
        
        super().__init__(message, error_code=error_code, jsonpath=jsonpath, details=details)
        self.resource_type = resource_type
        self.field = field
        self.fhirpath = fhirpath

    def __str__(self) -> str:
        """Format error message with context."""
        parts = [super().__str__()]
        if self.resource_type:
            parts.append(f"ResourceType: {self.resource_type}")
        if self.field:
            parts.append(f"Field: {self.field}")
        if self.fhirpath:
            parts.append(f"FHIRPath: {self.fhirpath}")
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary representation."""
        result = super().to_dict()
        if self.resource_type:
            result["resource_type"] = self.resource_type
        if self.field:
            result["field"] = self.field
        if self.fhirpath:
            result["fhirpath"] = self.fhirpath
        return result

