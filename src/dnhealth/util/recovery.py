# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Error recovery utilities for DNHealth library.

Provides recovery strategies for common parsing and validation errors,
allowing the library to attempt automatic recovery from recoverable errors.
All recovery operations include timestamps in logs for traceability.
"""

import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from enum import Enum

from dnhealth.errors import (
    DNHealthError,
    FHIRParseError,
    FHIRValidationError,
    HL7v2ParseError,
    HL7v3ParseError,
)
from dnhealth.util.logging import get_logger

logger = get_logger(__name__)


class RecoveryStrategy(Enum):
    """Types of recovery strategies."""

    FIX_MISSING_MSH = "fix_missing_msh"
    FIX_ENCODING_CHARS = "fix_encoding_chars"
    FIX_MALFORMED_SEGMENT = "fix_malformed_segment"
    FIX_ESCAPE_SEQUENCES = "fix_escape_sequences"
    FIX_LINE_ENDINGS = "fix_line_endings"
    FIX_XML_NAMESPACE = "fix_xml_namespace"
    FIX_XML_MALFORMED = "fix_xml_malformed"
    FIX_JSON_MALFORMED = "fix_json_malformed"
    FIX_MISSING_FIELDS = "fix_missing_fields"
    SKIP_INVALID_SEGMENT = "skip_invalid_segment"


class ErrorRecovery:
    """
    Error recovery handler for parsing and validation errors.

    Provides automatic recovery strategies for common errors encountered
    during parsing and validation operations. All recovery attempts are
    logged with timestamps for audit and debugging purposes.
    """

    def __init__(self, enabled_strategies: Optional[List[RecoveryStrategy]] = None):
        """
        Initialize error recovery handler.

        Args:
            enabled_strategies: List of recovery strategies to enable.
                              If None, all strategies are enabled.
        """
        self.enabled_strategies = enabled_strategies or list(RecoveryStrategy)
        self.recovery_attempts: List[Dict[str, Any]] = []
        self.successful_recoveries = 0
        self.failed_recoveries = 0

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ErrorRecovery initialized "
            f"with {len(self.enabled_strategies)} strategies"
        )

    def attempt_recovery(
        self,
        error: Exception,
        original_data: str,
        error_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Attempt to recover from a parsing or validation error.

        Args:
            error: The exception that was raised
            original_data: The original data that caused the error
            error_context: Optional context about the error (line number, etc.)

        Returns:
            Recovered data string if recovery successful, None otherwise
        """
        timestamp = datetime.now()
        error_type = type(error).__name__
        error_msg = str(error)

        logger.info(
            f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Attempting recovery from "
            f"{error_type}: {error_msg}"
        )

        recovery_attempt = {
            "timestamp": timestamp.isoformat(),
            "error_type": error_type,
            "error_message": error_msg,
            "strategy": None,
            "success": False,
            "recovered_data": None,
        }

        # Try recovery strategies based on error type
        if isinstance(error, HL7v2ParseError):
            recovered = self._recover_hl7v2_error(error, original_data, error_context)
        elif isinstance(error, HL7v3ParseError):
            recovered = self._recover_hl7v3_error(error, original_data, error_context)
        elif isinstance(error, FHIRParseError):
            recovered = self._recover_fhir_error(error, original_data, error_context)
        elif isinstance(error, FHIRValidationError):
            recovered = self._recover_fhir_validation_error(
                error, original_data, error_context
            )
        else:
            recovered = None

        if recovered is not None:
            recovery_attempt["success"] = True
            recovery_attempt["recovered_data"] = recovered
            self.successful_recoveries += 1
            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Recovery successful "
                f"using strategy: {recovery_attempt.get('strategy', 'unknown')}"
            )
        else:
            self.failed_recoveries += 1
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Recovery failed for "
                f"{error_type}"
            )

        self.recovery_attempts.append(recovery_attempt)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return recovered

    def _recover_hl7v2_error(
        self,
        error: HL7v2ParseError,
        original_data: str,
        error_context: Optional[Dict[str, Any]],
    ) -> Optional[str]:
        """Attempt to recover from HL7v2 parsing errors."""
        error_msg = str(error).lower()

        # Fix missing MSH segment
        if (
            RecoveryStrategy.FIX_MISSING_MSH in self.enabled_strategies
            and "msh" in error_msg
            and ("not found" in error_msg or "must start" in error_msg)
        ):
            return self._fix_missing_msh(original_data)

        # Fix encoding characters
        if (
            RecoveryStrategy.FIX_ENCODING_CHARS in self.enabled_strategies
            and ("encoding" in error_msg or "msh-2" in error_msg)
        ):
            return self._fix_encoding_chars(original_data)

        # Fix line endings
        if (
            RecoveryStrategy.FIX_LINE_ENDINGS in self.enabled_strategies
            and ("segment" in error_msg or "line" in error_msg)
        ):
            return self._fix_line_endings(original_data)

        # Fix malformed segment
        if (
            RecoveryStrategy.FIX_MALFORMED_SEGMENT in self.enabled_strategies
            and ("segment" in error_msg or "field" in error_msg)
        ):
            return self._fix_malformed_segment(original_data, error)

        # Skip invalid segment
        if (
            RecoveryStrategy.SKIP_INVALID_SEGMENT in self.enabled_strategies
            and error.segment
        ):
            return self._skip_invalid_segment(original_data, error)

        return None

    def _recover_hl7v3_error(
        self,
        error: HL7v3ParseError,
        original_data: str,
        error_context: Optional[Dict[str, Any]],
    ) -> Optional[str]:
        """Attempt to recover from HL7v3 parsing errors."""
        error_msg = str(error).lower()

        # Fix XML namespace issues
        if (
            RecoveryStrategy.FIX_XML_NAMESPACE in self.enabled_strategies
            and "namespace" in error_msg
        ):
            return self._fix_xml_namespace(original_data)

        # Fix malformed XML
        if (
            RecoveryStrategy.FIX_XML_MALFORMED in self.enabled_strategies
            and ("xml" in error_msg or "parse" in error_msg)
        ):
            return self._fix_xml_malformed(original_data)

        return None

    def _recover_fhir_error(
        self,
        error: FHIRParseError,
        original_data: str,
        error_context: Optional[Dict[str, Any]],
    ) -> Optional[str]:
        """Attempt to recover from FHIR parsing errors."""
        error_msg = str(error).lower()

        # Fix JSON malformed
        if (
            RecoveryStrategy.FIX_JSON_MALFORMED in self.enabled_strategies
            and ("json" in error_msg or "parse" in error_msg)
        ):
            return self._fix_json_malformed(original_data)

        # Fix XML malformed (FHIR XML)
        if (
            RecoveryStrategy.FIX_XML_MALFORMED in self.enabled_strategies
            and "xml" in error_msg
        ):
            return self._fix_xml_malformed(original_data)

        return None

    def _recover_fhir_validation_error(
        self,
        error: FHIRValidationError,
        original_data: str,
        error_context: Optional[Dict[str, Any]],
    ) -> Optional[str]:
        """Attempt to recover from FHIR validation errors."""
        # Validation errors typically can't be auto-recovered
        # but we can try to fix missing required fields
        if RecoveryStrategy.FIX_MISSING_FIELDS in self.enabled_strategies:
            error_msg = str(error).lower()
            if "required" in error_msg or "missing" in error_msg:
                return self._fix_missing_fields(original_data, error)

        return None

    def _fix_missing_msh(self, data: str) -> Optional[str]:
        """Fix missing MSH segment by finding and moving it to the front."""
        lines = data.replace("\r\n", "\r").replace("\n", "\r").split("\r")
        lines = [line.strip() for line in lines if line.strip()]

        # Find MSH segment
        msh_idx = None
        for i, line in enumerate(lines):
            if line.startswith("MSH"):
                msh_idx = i
                break

        if msh_idx is None or msh_idx == 0:
            return None

        # Move MSH to front
        msh_line = lines[msh_idx]
        lines.pop(msh_idx)
        lines.insert(0, msh_line)

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed missing MSH: "
            f"moved MSH segment from position {msh_idx} to front"
        )

        return "\r".join(lines)

    def _fix_encoding_chars(self, data: str) -> Optional[str]:
        """Fix encoding characters in MSH segment."""
        lines = data.replace("\r\n", "\r").replace("\n", "\r").split("\r")
        lines = [line.strip() for line in lines if line.strip()]

        if not lines or not lines[0].startswith("MSH"):
            return None

        msh_line = lines[0]
        if len(msh_line) < 4:
            return None

        # Check if MSH-2 is missing or malformed
        field_sep = msh_line[3] if len(msh_line) > 3 else "|"

        # If MSH-2 is missing, insert default encoding characters
        if len(msh_line) == 4 or (len(msh_line) > 4 and msh_line[4] == field_sep):
            # Insert default encoding: ^~\\&
            msh_line = msh_line[:4] + "^~\\&" + msh_line[4:]
            lines[0] = msh_line

            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed encoding chars: "
                f"inserted default encoding characters ^~\\&"
            )

            return "\r".join(lines)

        return None

    def _fix_line_endings(self, data: str) -> Optional[str]:
        """Normalize line endings."""
        # Try different line ending formats
        normalized = data.replace("\r\n", "\r").replace("\n", "\r")

        if normalized != data:
            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed line endings: "
                f"normalized to \\r"
            )
            return normalized

        return None

    def _fix_malformed_segment(
        self, data: str, error: HL7v2ParseError
    ) -> Optional[str]:
        """Attempt to fix malformed segment."""
        if not error.segment or not error.line_number:
            return None

        lines = data.replace("\r\n", "\r").replace("\n", "\r").split("\r")
        lines = [line.strip() for line in lines if line.strip()]

        line_idx = error.line_number - 1
        if line_idx < 0 or line_idx >= len(lines):
            return None

        # Try to fix common issues: missing field separators
        segment_line = lines[line_idx]
        if not segment_line.startswith(error.segment):
            return None

        # If segment name is correct but parsing failed, try adding missing separators
        # This is a simple heuristic - add separator if segment name followed by non-separator
        if len(segment_line) > 3:
            field_sep = segment_line[3] if len(segment_line) > 3 else "|"
            # Check if segment name is immediately followed by content without separator
            if segment_line[3] != field_sep:
                fixed_line = segment_line[:3] + field_sep + segment_line[3:]
                lines[line_idx] = fixed_line

                logger.info(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed malformed segment: "
                    f"added field separator after segment name"
                )

                return "\r".join(lines)

        return None

    def _skip_invalid_segment(
        self, data: str, error: HL7v2ParseError
    ) -> Optional[str]:
        """Skip invalid segment and continue parsing."""
        if not error.line_number:
            return None

        lines = data.replace("\r\n", "\r").replace("\n", "\r").split("\r")
        lines = [line.strip() for line in lines if line.strip()]

        line_idx = error.line_number - 1
        if line_idx < 0 or line_idx >= len(lines):
            return None

        # Don't skip MSH segment
        if lines[line_idx].startswith("MSH"):
            return None

        # Remove the problematic segment
        removed_segment = lines.pop(line_idx)

        logger.warning(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Skipped invalid segment: "
            f"{removed_segment[:20]}... (line {error.line_number})"
        )

        return "\r".join(lines)

    def _fix_xml_namespace(self, data: str) -> Optional[str]:
        """Fix XML namespace issues."""
        # Try to add default namespace if missing
        if 'xmlns=' not in data and 'xmlns:' not in data:
            # Try to find root element and add namespace
            match = re.search(r'<(\w+)', data)
            if match:
                root_tag = match.group(1)
                # Add default namespace (common HL7v3 namespace)
                fixed = data.replace(
                    f"<{root_tag}",
                    f'<{root_tag} xmlns="urn:hl7-org:v3"',
                    1,
                )

                logger.info(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed XML namespace: "
                    f"added default namespace to {root_tag}"
                )

                return fixed

        return None

    def _fix_xml_malformed(self, data: str) -> Optional[str]:
        """Attempt to fix malformed XML."""
        # Try to close unclosed tags (simple heuristic)
        open_tags = []
        fixed = data

        # Count open/close tags
        tag_pattern = r'<(/?)(\w+)[^>]*>'
        matches = list(re.finditer(tag_pattern, fixed))

        for match in matches:
            is_closing = match.group(1) == "/"
            tag_name = match.group(2)

            if is_closing:
                if open_tags and open_tags[-1] == tag_name:
                    open_tags.pop()
            else:
                # Check if self-closing
                tag_content = match.group(0)
                if not tag_content.endswith("/>"):
                    open_tags.append(tag_name)

        # Close remaining open tags
        if open_tags:
            closing_tags = "".join(f"</{tag}>" for tag in reversed(open_tags))
            fixed = fixed + closing_tags

            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed XML malformed: "
                f"closed {len(open_tags)} unclosed tags"
            )

            return fixed

        return None

    def _fix_json_malformed(self, data: str) -> Optional[str]:
        """Attempt to fix malformed JSON."""
        # Try to fix common JSON issues
        fixed = data.strip()

        # Fix trailing commas
        fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)

        # Fix unquoted keys (simple cases)
        fixed = re.sub(r'(\w+):', r'"\1":', fixed)

        # Try to ensure proper JSON structure
        if not fixed.startswith("{") and not fixed.startswith("["):
            # Try to wrap in object
            fixed = "{" + fixed + "}"

            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed JSON malformed: "
                f"wrapped in object structure"
            )

            return fixed

        if fixed != data:
            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fixed JSON malformed: "
                f"removed trailing commas and fixed quotes"
            )
            return fixed

        return None

    def _fix_missing_fields(
        self, data: str, error: FHIRValidationError
    ) -> Optional[str]:
        """Attempt to fix missing required fields in FHIR resources."""
        # This is a placeholder - actual implementation would need to know
        # the resource type and required fields
        # For now, we just log that we attempted recovery
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Attempted to fix missing fields "
            f"for resource type: {error.resource_type}"
        )
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get recovery statistics.

        Returns:
            Dictionary with recovery statistics
        """
        return {
            "total_attempts": len(self.recovery_attempts),
            "successful_recoveries": self.successful_recoveries,
            "failed_recoveries": self.failed_recoveries,
            "success_rate": (
                self.successful_recoveries / len(self.recovery_attempts)
                if self.recovery_attempts
                else 0.0
            ),
            "enabled_strategies": [s.value for s in self.enabled_strategies],
        }

    def clear_history(self) -> None:
        """Clear recovery attempt history."""
        self.recovery_attempts.clear()
        self.successful_recoveries = 0
        self.failed_recoveries = 0
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Recovery history cleared"
        )


def recover_from_error(
    error: Exception,
    original_data: str,
    error_context: Optional[Dict[str, Any]] = None,
    enabled_strategies: Optional[List[RecoveryStrategy]] = None,
) -> Optional[str]:
    """
    Convenience function to attempt error recovery.

    Args:
        error: The exception that was raised
        original_data: The original data that caused the error
        error_context: Optional context about the error
        enabled_strategies: Optional list of strategies to enable

    Returns:
        Recovered data string if recovery successful, None otherwise
    """
    recovery = ErrorRecovery(enabled_strategies=enabled_strategies)
    return recovery.attempt_recovery(error, original_data, error_context)
