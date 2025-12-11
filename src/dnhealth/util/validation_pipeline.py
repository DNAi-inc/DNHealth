# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
Message validation pipeline utilities for DNHealth library.
logger = logging.getLogger(__name__)

Provides configurable validation pipelines for HL7v2, HL7v3, and FHIR messages.
Supports multiple validation rules, custom validators, and validation result aggregation.
All validation operations include timestamps in logs for traceability.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass

from dnhealth.util.logging import get_logger

logger = get_logger(__name__)


class ValidationSeverity(Enum):
    """Validation severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Result of a validation check."""

    rule_name: str
    severity: ValidationSeverity
    message: str
    field_path: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class ValidationRule:
    """
    Defines a validation rule for messages.

    Validates messages based on matching conditions and validation functions.
    """

    def __init__(
        self,
        name: str,
        condition: Callable[[Any], bool],
        validate_func: Callable[[Any], List[ValidationResult]],
        severity: ValidationSeverity = ValidationSeverity.ERROR,
        priority: int = 0,
        description: Optional[str] = None,
        stop_on_error: bool = False,
    ):
        """
        Initialize validation rule.

        Args:
            name: Unique name for the rule
            condition: Function that takes a message and returns True if rule applies
            validate_func: Function that validates the message and returns list of results
            severity: Default severity for validation failures
            priority: Rule priority (higher priority rules are evaluated first)
            description: Optional description of the rule
            stop_on_error: If True, stop pipeline execution on error
        """
        self.name = name
        self.condition = condition
        self.validate_func = validate_func
        self.severity = severity
        self.priority = priority
        self.description = description
        self.stop_on_error = stop_on_error

    def applies_to(self, message: Any) -> bool:
        """
        Check if validation rule applies to message.

        Args:
            message: Message to check

        Returns:
            True if rule applies, False otherwise
        """
        try:
            return self.condition(message)
        except Exception as e:
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error evaluating "
                f"validation rule '{self.name}': {str(e)}"
            )
            return False

    def validate(self, message: Any) -> List[ValidationResult]:
        """
        Validate message.

        Args:
            message: Message to validate

        Returns:
            List of validation results
        """
        try:
            results = self.validate_func(message)
            # Ensure all results have the rule name and severity
            for result in results:
                if result.rule_name != self.name:
                    result.rule_name = self.name
                if result.severity is None:
                    result.severity = self.severity
            return results
        except Exception as e:
            logger.error(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error validating "
                f"with rule '{self.name}': {str(e)}"
            )

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return [
            ValidationResult(
                rule_name=self.name,
                severity=ValidationSeverity.ERROR,
                message=f"Validation error: {str(e)}",
            )
        ]


class ValidationPipeline:
    """
    Validation pipeline for validating HL7v2, HL7v3, and FHIR messages.

    Supports multiple validation rules, custom validators, and validation result
    aggregation. All validations are logged with timestamps.
    """

    def __init__(self, stop_on_error: bool = False):
        """
        Initialize validation pipeline.

        Args:
            stop_on_error: If True, stop validation on first error
        """
        self.rules: List[ValidationRule] = []
        self.stop_on_error = stop_on_error
        self.validation_history: List[Dict[str, Any]] = []
        self.validated_count = 0
        self.failed_count = 0

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValidationPipeline initialized"
        )

    def add_rule(
        self,
        name: str,
        condition: Callable[[Any], bool],
        validate_func: Callable[[Any], List[ValidationResult]],
        severity: ValidationSeverity = ValidationSeverity.ERROR,
        priority: int = 0,
        description: Optional[str] = None,
        stop_on_error: Optional[bool] = None,
    ) -> None:
        """
        Add a validation rule.

        Args:
            name: Unique name for the rule
            condition: Function that takes a message and returns True if rule applies
            validate_func: Function that validates the message and returns list of results
            severity: Default severity for validation failures
            priority: Rule priority (higher priority rules are evaluated first)
            description: Optional description of the rule
            stop_on_error: If True, stop pipeline execution on error (overrides pipeline default)
        """
        if stop_on_error is None:
            stop_on_error = self.stop_on_error

        rule = ValidationRule(
            name=name,
            condition=condition,
            validate_func=validate_func,
            severity=severity,
            priority=priority,
            description=description,
            stop_on_error=stop_on_error,
        )
        self.rules.append(rule)
        # Sort rules by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Added validation rule "
            f"'{name}' with priority {priority}"
        )

    def remove_rule(self, name: str) -> bool:
        """
        Remove a validation rule by name.

        Args:
            name: Name of the rule to remove

        Returns:
            True if rule was removed, False if not found
        """
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r.name != name]
        removed = len(self.rules) < initial_count

        if removed:
            logger.info(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Removed validation rule '{name}'"
            )
        else:
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validation rule '{name}' not found"
            )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return removed

    def validate(
        self, message: Any, stop_on_error: Optional[bool] = None
    ) -> Tuple[bool, List[ValidationResult]]:
        """
        Validate a message using applicable rules.

        Args:
            message: Message to validate (HL7v2 Message, HL7v3 Message, FHIR Resource, etc.)
            stop_on_error: Override pipeline stop_on_error setting

        Returns:
            Tuple of (is_valid, list_of_validation_results)
        """
        timestamp = datetime.now()
        results: List[ValidationResult] = []
        applied_rules = []

        if stop_on_error is None:
            stop_on_error = self.stop_on_error

        # Validate using rules in priority order
        for rule in self.rules:
            if rule.applies_to(message):
                try:
                    rule_results = rule.validate(message)
                    results.extend(rule_results)
                    applied_rules.append(rule.name)

                    # Check if we should stop on error
                    if stop_on_error or rule.stop_on_error:
                        errors = [
                            r
                            for r in rule_results
                            if r.severity == ValidationSeverity.ERROR
                        ]
                        if errors:
                            logger.warning(
                                f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Validation stopped "
                                f"on error from rule '{rule.name}'"
                            )
                            break

                except Exception as e:
                    logger.error(
                        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Error validating "
                        f"with rule '{rule.name}': {str(e)}"
                    )
                    results.append(
                        ValidationResult(
                            rule_name=rule.name,
                            severity=ValidationSeverity.ERROR,
                            message=f"Validation error: {str(e)}",
                        )
                    )
                    if stop_on_error or rule.stop_on_error:
                        break

        # Determine if validation passed
        errors = [r for r in results if r.severity == ValidationSeverity.ERROR]
        is_valid = len(errors) == 0

        # Update statistics
        if is_valid:
            self.validated_count += 1
        else:
            self.failed_count += 1

        # Record in history
        self.validation_history.append(
            {
                "timestamp": timestamp.isoformat(),
                "is_valid": is_valid,
                "applied_rules": applied_rules,
                "error_count": len(errors),
                "warning_count": len(
                    [r for r in results if r.severity == ValidationSeverity.WARNING]
                ),
                "message_type": self._detect_message_type(message),
            }
        )

        logger.info(
            f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Validation completed: "
            f"{'PASSED' if is_valid else 'FAILED'} ({len(errors)} errors, "
            f"{len([r for r in results if r.severity == ValidationSeverity.WARNING])} warnings)"
        )


        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return is_valid, results

    def add_required_field_validation(
        self,
        name: str,
        field_paths: List[str],
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a required field validation rule.

        Args:
            name: Unique name for the rule
            field_paths: List of field paths that must be present
            condition: Optional condition function
            priority: Rule priority
        """
        def validate_func(msg: Any) -> List[ValidationResult]:
            """Validate required fields."""
            results = []
            msg_type = self._detect_message_type(msg)

            for field_path in field_paths:
                value = self._get_field_value(msg, field_path, msg_type)
                if value is None or (isinstance(value, str) and not value.strip()):
                    results.append(
                        ValidationResult(
                            rule_name=name,
                            severity=ValidationSeverity.ERROR,
                            message=f"Required field '{field_path}' is missing or empty",
                            field_path=field_path,
                        )
                    )


            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return results

        if condition is None:
            condition = lambda m: True

        self.add_rule(
            name=name,
            condition=condition,
            validate_func=validate_func,
            severity=ValidationSeverity.ERROR,
            priority=priority,
            description=f"Required field validation: {len(field_paths)} fields",
        )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def add_data_type_validation(
        self,
        name: str,
        field_type_mapping: Dict[str, str],
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a data type validation rule.

        Args:
            name: Unique name for the rule
            field_type_mapping: Dictionary mapping field paths to expected data types
            condition: Optional condition function
            priority: Rule priority
        """
        def validate_func(msg: Any) -> List[ValidationResult]:
            """Validate data types."""
            results = []
            msg_type = self._detect_message_type(msg)

            for field_path, expected_type in field_type_mapping.items():
                value = self._get_field_value(msg, field_path, msg_type)
                if value is not None:
                    if not self._check_data_type(value, expected_type, msg_type):
                        results.append(
                            ValidationResult(
                                rule_name=name,
                                severity=ValidationSeverity.ERROR,
                                message=(
                                    f"Field '{field_path}' has incorrect data type. "
                                    f"Expected {expected_type}, got {type(value).__name__}"
                                ),
                                field_path=field_path,
                            )
                        )


            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return results

        if condition is None:
            condition = lambda m: True

        self.add_rule(
            name=name,
            condition=condition,
            validate_func=validate_func,
            severity=ValidationSeverity.ERROR,
            priority=priority,
            description=f"Data type validation: {len(field_type_mapping)} fields",
        )
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def add_value_set_validation(
        self,
        name: str,
        field_value_sets: Dict[str, List[str]],
        condition: Optional[Callable[[Any], bool]] = None,
        priority: int = 0,
    ) -> None:
        """
        Add a value set validation rule.

        Args:
            name: Unique name for the rule
            field_value_sets: Dictionary mapping field paths to allowed values
            condition: Optional condition function
            priority: Rule priority
        """
        def validate_func(msg: Any) -> List[ValidationResult]:
            """Validate value sets."""
            results = []
            msg_type = self._detect_message_type(msg)

            for field_path, allowed_values in field_value_sets.items():
                value = self._get_field_value(msg, field_path, msg_type)
                if value is not None:
                    if str(value) not in allowed_values:
                        results.append(
                            ValidationResult(
                                rule_name=name,
                                severity=ValidationSeverity.ERROR,
                                message=(
                                    f"Field '{field_path}' has invalid value '{value}'. "
                                    f"Allowed values: {', '.join(allowed_values)}"
                                ),
                                field_path=field_path,
                            )
                        )


            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            return results

        if condition is None:
            condition = lambda m: True

        self.add_rule(
            name=name,
            condition=condition,
            validate_func=validate_func,
            severity=ValidationSeverity.ERROR,
            priority=priority,
            description=f"Value set validation: {len(field_value_sets)} fields",
        )

    def _get_field_value(self, message: Any, field_path: str, msg_type: str) -> Any:
        """Get field value from message."""
        if msg_type == "hl7v2":
            # Parse path like "PID.5.1"
            parts = field_path.split(".")
            segment = parts[0]
            field_idx = int(parts[1]) - 1 if len(parts) > 1 else 0
            comp_idx = int(parts[2]) - 1 if len(parts) > 2 else None

            segments = message.get_segments(segment)
            if segments:
                seg = segments[0]
                if len(seg.fields) > field_idx:
                    field_obj = seg.field(field_idx + 1)
                    if comp_idx is not None:
                        if len(field_obj.components) > comp_idx:
                            return field_obj.component(comp_idx + 1).value()
                    else:
                        return field_obj.value()
        elif msg_type == "fhir":
            # Use dot notation for FHIR paths
            parts = field_path.split(".")
            value = message
            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                elif isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            return value
        elif msg_type == "hl7v3":
            # HL7v3 uses XPath - simplified implementation
            logger.warning(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - HL7v3 field access "
                f"not yet fully implemented"
            )

        return None

    def _check_data_type(self, value: Any, expected_type: str, msg_type: str) -> bool:
        """Check if value matches expected data type."""
        type_mapping = {
            "string": str,
            "int": int,
            "integer": int,
            "float": float,
            "number": (int, float),
            "bool": bool,
            "boolean": bool,
            "list": list,
            "dict": dict,
            "date": str,  # Dates are often strings in HL7/FHIR
            "datetime": str,
        }

        python_type = type_mapping.get(expected_type.lower())
        if python_type:
            if isinstance(python_type, tuple):
                return isinstance(value, python_type)
            return isinstance(value, python_type)

        # For HL7v2 specific types, use validation functions
        if msg_type == "hl7v2":
            from dnhealth.dnhealth_hl7v2.datatypes import validate_data_type

            is_valid, _ = validate_data_type(expected_type, str(value))
            return is_valid

        return True  # Default to True if type not recognized

    def _detect_message_type(self, message: Any) -> str:
        """
        Detect message type.

        Args:
            message: Message to detect type for

        Returns:
            Message type string: "hl7v2", "hl7v3", or "fhir"
        """
        # Check for HL7v2 Message
        if hasattr(message, "segments") and hasattr(message, "encoding_chars"):
            return "hl7v2"

        # Check for HL7v3 Message
        if hasattr(message, "interaction_id") or (
            isinstance(message, dict) and "interactionId" in message
        ):
            return "hl7v3"

        # Check for FHIR Resource
        if hasattr(message, "resourceType") or (
            isinstance(message, dict) and "resourceType" in message
        ):
            return "fhir"

        # Default to unknown
        return "unknown"

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get validation statistics.

        Returns:
            Dictionary with validation statistics
        """
        stats = {
            "total_rules": len(self.rules),
            "validated_count": self.validated_count,
            "failed_count": self.failed_count,
            "success_rate": (
                self.validated_count / (self.validated_count + self.failed_count)
                if (self.validated_count + self.failed_count) > 0
                else 0.0
            ),
            "history_size": len(self.validation_history),
        }
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return stats

    def clear_history(self) -> None:
        """Clear validation history."""
        self.validation_history.clear()
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validation history cleared"
        )

    def get_errors(self, results: List[ValidationResult]) -> List[ValidationResult]:
        """
        Filter validation results to get only errors.

        Args:
            results: List of validation results

        Returns:
            List of error results
        """
        return [r for r in results if r.severity == ValidationSeverity.ERROR]

    def get_warnings(self, results: List[ValidationResult]) -> List[ValidationResult]:
        """
        Filter validation results to get only warnings.

        Args:
            results: List of validation results

        Returns:
            List of warning results
        """
        return [r for r in results if r.severity == ValidationSeverity.WARNING]

    def get_info(self, results: List[ValidationResult]) -> List[ValidationResult]:
        """
        Filter validation results to get only info messages.

        Args:
            results: List of validation results

        Returns:
            List of info results
        """
        return [r for r in results if r.severity == ValidationSeverity.INFO]
