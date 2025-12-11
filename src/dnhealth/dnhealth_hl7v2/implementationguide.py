# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
HL7 v2.x Implementation Guide support.
logger = logging.getLogger(__name__)

Provides functionality for parsing and applying implementation guide definitions,
including custom segment definitions, field definitions, table definitions, and
constraint validation.

All operations include timestamps in logs for traceability.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from dnhealth.util.logging import get_logger

logger = get_logger(__name__)


class Constraint:
    """
    Represents a validation constraint for a field or segment.
    
    Constraints define rules that must be satisfied for a message to be valid
    according to an implementation guide.
    """
    
    def __init__(
        self,
        constraint_type: str,
        field_path: str,
        rule: str,
        error_message: Optional[str] = None,
    ):
        """
        Initialize constraint.
        
        Args:
            constraint_type: Type of constraint (e.g., "required", "pattern", "range", "custom")
            field_path: Path to field (e.g., "MSH-9", "PID-3")
            rule: Constraint rule (pattern, range, etc.)
            error_message: Custom error message if constraint fails
        """
        self.constraint_type = constraint_type
        self.field_path = field_path
        self.rule = rule
        self.error_message = error_message or f"Constraint violation: {constraint_type} on {field_path}"
        self.created_at = datetime.now()
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Created constraint: {constraint_type} on {field_path}"
        )
    
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a value against this constraint.
        
        Args:
            value: Value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.constraint_type == "required":
            is_valid = value is not None and str(value).strip() != ""
            return is_valid, None if is_valid else self.error_message
        
        elif self.constraint_type == "pattern":
            import re
            try:
                is_valid = bool(re.match(self.rule, str(value)))
                return is_valid, None if is_valid else self.error_message
            except Exception as e:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Pattern validation error: {e}"
                )
                return False, f"Pattern validation error: {e}"
        
        elif self.constraint_type == "range":
            # Rule format: "min:max" or "min:" or ":max"
            try:
                parts = self.rule.split(":")
                min_val = float(parts[0]) if parts[0] else None
                max_val = float(parts[1]) if len(parts) > 1 and parts[1] else None
                val = float(value)
                
                if min_val is not None and val < min_val:
                    return False, self.error_message
                if max_val is not None and val > max_val:
                    return False, self.error_message
                return True, None
            except Exception as e:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Range validation error: {e}"
                )
                return False, f"Range validation error: {e}"
        
        elif self.constraint_type == "length":
            # Rule format: "min:max" or "min:" or ":max"
            try:
                parts = self.rule.split(":")
                min_len = int(parts[0]) if parts[0] else None
                max_len = int(parts[1]) if len(parts) > 1 and parts[1] else None
                val_str = str(value)
                
                if min_len is not None and len(val_str) < min_len:
                    return False, self.error_message
                if max_len is not None and len(val_str) > max_len:
                    return False, self.error_message
                return True, None
            except Exception as e:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Length validation error: {e}"
                )
                return False, f"Length validation error: {e}"
        
        elif self.constraint_type == "enum":
            # Rule format: comma-separated list of allowed values
            allowed_values = [v.strip() for v in self.rule.split(",")]
            is_valid = str(value) in allowed_values
            return is_valid, None if is_valid else self.error_message
        
        elif self.constraint_type == "table":
            # Rule format: table ID (e.g., "0001", "0003")
            # Validate that value exists in the specified table
            try:
                from dnhealth.dnhealth_hl7v2.tables import get_table_value
                table_id = self.rule.strip()
                table_value = get_table_value(table_id, str(value))
                is_valid = table_value is not None
                return is_valid, None if is_valid else self.error_message
            except Exception as e:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Table validation error for table {self.rule}: {e}"
                )
                return False, f"Table validation error: {e}"
        
        elif self.constraint_type == "date_format":
            # Rule format: date format pattern (e.g., "YYYYMMDD", "YYYYMMDDHHMMSS")
            # Validate that value matches the date format
            try:
                from datetime import datetime
                value_str = str(value).strip()
                
                if self.rule == "YYYYMMDD":
                    if len(value_str) == 8:
                        datetime.strptime(value_str, "%Y%m%d")
                        return True, None
                    return False, self.error_message
                elif self.rule == "YYYYMMDDHHMMSS":
                    if len(value_str) == 14:
                        datetime.strptime(value_str, "%Y%m%d%H%M%S")
                        return True, None
                    return False, self.error_message
                elif self.rule == "YYYYMMDDHHMM":
                    if len(value_str) == 12:
                        datetime.strptime(value_str, "%Y%m%d%H%M")
                        return True, None
                    return False, self.error_message
                else:
                    # Try to parse as ISO format
                    datetime.fromisoformat(value_str.replace("Z", "+00:00"))
                    return True, None
            except Exception as e:
                logger.debug(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Date format validation error: {e}"
                )
                return False, self.error_message
        
        elif self.constraint_type == "not_empty":
            # Value must not be empty (whitespace-only is considered empty)
            is_valid = value is not None and str(value).strip() != ""
            return is_valid, None if is_valid else self.error_message
        
        elif self.constraint_type == "custom":
            # Custom constraint - rule should be a Python expression or function name
            # Supports safe evaluation of Python expressions with restricted context
            try:
                # Create a safe evaluation context with only safe built-ins
                safe_builtins = {
                    'abs': abs, 'all': all, 'any': any, 'bool': bool, 'dict': dict,
                    'float': float, 'int': int, 'len': len, 'list': list, 'max': max,
                    'min': min, 'str': str, 'sum': sum, 'tuple': tuple, 'type': type,
                    'isinstance': isinstance, 'hasattr': hasattr, 'getattr': getattr,
                }
                
                # Create evaluation context with value and safe operations
                eval_context = {
                    '__builtins__': safe_builtins,
                    'value': value,
                    'val': value,  # Alias for convenience
                }
                
                # Evaluate the custom rule expression
                # The rule can be a simple expression like: "len(value) > 5" or "value.startswith('ABC')"
                result = eval(self.rule, eval_context)
                
                # Result should be boolean-like
                is_valid = bool(result)
                
                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.debug(
                    f"[{current_time}] Custom constraint evaluated: {self.rule} = {result}"
                )
                
                return is_valid, None if is_valid else self.error_message
                
            except SyntaxError as e:
                # Invalid expression syntax
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(
                    f"[{current_time}] Custom constraint syntax error: {e}. Rule: {self.rule}"
                )
                return False, f"Custom constraint syntax error: {e}"
            except Exception as e:
                # Other evaluation errors (e.g., NameError, TypeError)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning(
                    f"[{current_time}] Custom constraint evaluation error: {e}. Rule: {self.rule}"
                )
                return False, f"Custom constraint evaluation error: {e}"
        
        else:
            logger.warning(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Unknown constraint type: {self.constraint_type}"
            )

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return True, None  # Don't fail on unknown constraint types


class ImplementationGuide:
    """
    Represents an HL7 v2.x Implementation Guide.
    
    Implementation guides define customizations to the base HL7 standard,
    including custom segments, fields, tables, and validation constraints.
    """
    
    def __init__(
        self,
        name: str,
        version: str,
        hl7_version: str,
        description: Optional[str] = None,
    ):
        """
        Initialize implementation guide.
        
        Args:
            name: Name of the implementation guide
            version: Version of the implementation guide
            hl7_version: Base HL7 version (e.g., "2.5")
            description: Description of the implementation guide
        """
        self.name = name
        self.version = version
        self.hl7_version = hl7_version
        self.description = description
        self.created_at = datetime.now()
        
        # Custom definitions
        self.custom_segments: Dict[str, Dict] = {}
        self.custom_fields: Dict[str, Dict[int, Dict]] = {}  # segment_name -> field_index -> definition
        self.custom_tables: Dict[str, Dict[str, str]] = {}  # table_id -> code -> description
        
        # Constraints
        self.constraints: List[Constraint] = []
        
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Created Implementation Guide: {name} v{version} for HL7 {hl7_version}"
        )
    
    def add_custom_segment(self, segment_name: str, definition: Dict):
        """
        Add custom segment definition.
        
        Args:
            segment_name: Segment name (3 characters)
            definition: Segment definition dictionary
        """
        self.custom_segments[segment_name] = definition
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Added custom segment: {segment_name}"
        )
    
    def add_custom_field(
        self,
        segment_name: str,
        field_index: int,
        definition: Dict,
    ):
        """
        Add custom field definition.
        
        Args:
            segment_name: Segment name
            field_index: Field index (1-based)
            definition: Field definition dictionary
        """
        if segment_name not in self.custom_fields:
            self.custom_fields[segment_name] = {}
        self.custom_fields[segment_name][field_index] = definition
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Added custom field: {segment_name}-{field_index}"
        )
    
    def add_custom_table(self, table_id: str, code: str, description: str):
        """
        Add custom table value definition.
        
        Args:
            table_id: Table identifier
            code: Code value
            description: Code description
        """
        if table_id not in self.custom_tables:
            self.custom_tables[table_id] = {}
        self.custom_tables[table_id][code] = description
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Added custom table value: {table_id}[{code}]"
        )
    
    def add_constraint(
        self,
        constraint_type: str,
        field_path: str,
        rule: str,
        error_message: Optional[str] = None,
    ):
        """
        Add validation constraint.
        
        Args:
            constraint_type: Type of constraint
            field_path: Path to field (e.g., "MSH-9", "PID-3")
            rule: Constraint rule
            error_message: Custom error message
        """
        constraint = Constraint(constraint_type, field_path, rule, error_message)
        self.constraints.append(constraint)
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Added constraint: {constraint_type} on {field_path}"
        )
    
    def get_custom_segment(self, segment_name: str) -> Optional[Dict]:
        """
        Get custom segment definition.
        
        Args:
            segment_name: Segment name
            
        Returns:
            Segment definition or None
        """
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return self.custom_segments.get(segment_name)
    
    def get_custom_field(
        self,
        segment_name: str,
        field_index: int,
    ) -> Optional[Dict]:
        """
        Get custom field definition.
        
        Args:
            segment_name: Segment name
            field_index: Field index
            
        Returns:
            Field definition or None
        """
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return self.custom_fields.get(segment_name, {}).get(field_index)
    
    def get_custom_table(self, table_id: str) -> Optional[Dict[str, str]]:
        """
        Get custom table definition.
        
        Args:
            table_id: Table identifier
            
        Returns:
            Dictionary mapping codes to descriptions, or None
        """
        return self.custom_tables.get(table_id)
    
    def validate_constraints(
        self,
        message: Any,  # Message object from model.py
    ) -> Tuple[bool, List[str]]:
        """
        Validate message against all constraints.
        
        Args:
            message: HL7 message object
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors: List[str] = []
        
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Validating message against {len(self.constraints)} constraints"
        )
        
        for constraint in self.constraints:
            # Parse field path (e.g., "MSH-9" -> segment "MSH", field 9)
            # Also handle component paths like "MSH-9-2" -> segment "MSH", field 9, component 2
            try:
                parts = constraint.field_path.split("-")
                segment_name = parts[0]
                field_index = int(parts[1])
                component_index = int(parts[2]) if len(parts) > 2 else None
                
                # Get segments from message (returns list)
                segments = message.get_all_segments(segment_name)
                if not segments:
                    if constraint.constraint_type == "required":
                        errors.append(
                            f"Missing required segment: {segment_name} "
                            f"(constraint: {constraint.field_path})"
                        )
                    continue
                
                # Use first segment if multiple exist
                segment = segments[0]
                
                # Get field value
                field = segment.field(field_index)
                if field is None or (hasattr(field, "is_empty") and field.is_empty()):
                    if constraint.constraint_type == "required":
                        errors.append(
                            f"Missing required field: {constraint.field_path}"
                        )
                    continue
                
                # Get field value
                if component_index is not None:
                    # Get component value
                    if hasattr(field, "get_component"):
                        component = field.get_component(component_index)
                        field_value = str(component) if component else ""
                    else:
                        # Try to parse component from field value
                        field_str = str(field)
                        if "^" in field_str:
                            components = field_str.split("^")
                            if component_index <= len(components):
                                field_value = components[component_index - 1]
                            else:
                                field_value = ""
                        else:
                            field_value = field_str if component_index == 1 else ""
                else:
                    # Get full field value
                    field_value = str(field)
                
                # Validate constraint
                is_valid, error_msg = constraint.validate(field_value)
                if not is_valid:
                    errors.append(
                        error_msg or f"Constraint violation: {constraint.field_path}"
                    )
            
            except Exception as e:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Error validating constraint {constraint.field_path}: {e}"
                )
                errors.append(f"Error validating constraint {constraint.field_path}: {e}")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Message validation passed all constraints"
            )
        else:
            logger.warning(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Message validation failed with {len(errors)} errors"
            )
        

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return is_valid, errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert implementation guide to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "version": self.version,
            "hl7_version": self.hl7_version,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "custom_segments": self.custom_segments,
            "custom_fields": {
                seg: {
                    str(field_idx): field_def
                    for field_idx, field_def in fields.items()
                }
                for seg, fields in self.custom_fields.items()
            },
            "custom_tables": self.custom_tables,
            "constraints": [
                {
                    "constraint_type": c.constraint_type,
                    "field_path": c.field_path,
                    "rule": c.rule,
                    "error_message": c.error_message,
                }
                for c in self.constraints
            ],
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImplementationGuide":
        """
        Create implementation guide from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            ImplementationGuide instance
        """
        ig = cls(
            name=data["name"],
            version=data["version"],
            hl7_version=data["hl7_version"],
            description=data.get("description"),
        )
        
        # Load custom segments
        for seg_name, seg_def in data.get("custom_segments", {}).items():
            ig.add_custom_segment(seg_name, seg_def)
        
        # Load custom fields
        for seg_name, fields in data.get("custom_fields", {}).items():
            for field_idx_str, field_def in fields.items():
                ig.add_custom_field(seg_name, int(field_idx_str), field_def)
        
        # Load custom tables
        for table_id, table_data in data.get("custom_tables", {}).items():
            if isinstance(table_data, dict):
                for code, description in table_data.items():
                    ig.add_custom_table(table_id, code, description)
        
        # Load constraints
        for constraint_data in data.get("constraints", []):
            ig.add_constraint(
                constraint_type=constraint_data["constraint_type"],
                field_path=constraint_data["field_path"],
                rule=constraint_data["rule"],
                error_message=constraint_data.get("error_message"),
            )
        
        return ig
    
    @classmethod
    def from_json(cls, json_str: str) -> "ImplementationGuide":
        """
        Create implementation guide from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            ImplementationGuide instance
        """
        data = json.loads(json_str)
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Parsing Implementation Guide from JSON: {data.get('name', 'Unknown')}"
        )
        
        result = cls.from_dict(data)
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert implementation guide to JSON string.
        
        Args:
            indent: JSON indentation
            
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)


def load_implementation_guide(file_path: str) -> ImplementationGuide:
    """
    Load implementation guide from JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        ImplementationGuide instance
    """
    logger.info(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Loading Implementation Guide from file: {file_path}"
    )
    
    with open(file_path, "r", encoding="utf-8") as f:
        json_str = f.read()
    
    result = ImplementationGuide.from_json(json_str)
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return result


def save_implementation_guide(ig: ImplementationGuide, file_path: str):
    """
    Save implementation guide to JSON file.
    
    Args:
        ig: ImplementationGuide instance
        file_path: Path to output JSON file
    """
    logger.info(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Saving Implementation Guide to file: {file_path}"
    )
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ig.to_json(indent=2))
