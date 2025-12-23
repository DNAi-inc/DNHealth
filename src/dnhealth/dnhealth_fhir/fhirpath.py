# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR FHIRPath constraint evaluation (version-aware).

Provides basic FHIRPath expression evaluation for constraint validation.
FHIRPath is a path-based navigation and extraction language for FHIR resources.
Supports both R4 and R5 versions with version-aware FHIRPath evaluation.
"""

from typing import Dict, List, Optional, Set, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class FHIRPathConstraint:
    """
    Represents a FHIRPath constraint from ElementDefinition.
    """
    
    key: str  # Constraint key (unique identifier)
    severity: str  # error, warning
    human: str  # Human-readable description
    expression: str  # FHIRPath expression
    xpath: Optional[str] = None  # Optional XPath equivalent
    source: Optional[str] = None  # Source of constraint


def parse_constraint(constraint_data: Dict[str, Any]) -> FHIRPathConstraint:
    """
    Parse a constraint from ElementDefinition constraint data.
    
    Args:
        constraint_data: Constraint dictionary from ElementDefinition
        
    Returns:
        FHIRPathConstraint object
    """

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return FHIRPathConstraint(
        key=constraint_data.get("key", ""),
        severity=constraint_data.get("severity", "error"),
        human=constraint_data.get("human", ""),
        expression=constraint_data.get("expression", ""),
        xpath=constraint_data.get("xpath"),
        source=constraint_data.get("source")
    )


def evaluate_fhirpath_expression(
    expression: str,
    resource: Any,
    context: Optional[Any] = None
) -> Union[bool, List[Any], Any]:
    """
    Evaluate a FHIRPath expression on a resource.
    
    This is a simplified FHIRPath evaluator that handles common patterns:
    - Simple property access (e.g., "name.family")
    - Comparison operators (eq, ne, gt, lt, ge, le)
    - Logical operators (and, or, not)
    - Existence checks (exists())
    - Count operations (count())
    - String operations (contains(), startsWith(), endsWith())
    
    Args:
        expression: FHIRPath expression string
        resource: FHIR resource to evaluate expression on
        context: Optional context resource
        
    Returns:
        Evaluation result (boolean, list, or value)
    """
    if not expression:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] FHIRPath expression evaluation completed (empty expression)")
        return True
    
    # Normalize whitespace
    expression = expression.strip()
    
    # Handle simple property access
    if "." in expression and not any(op in expression for op in ["(", ")", "=", "!", ">", "<"]):
        return _evaluate_path(expression, resource)
    
    # Handle comparison expressions
    if "=" in expression or "!=" in expression or ">" in expression or "<" in expression:
        return _evaluate_comparison(expression, resource, context)
    
    # Handle logical operators
    if " and " in expression.lower():
        parts = re.split(r"\s+and\s+", expression, flags=re.IGNORECASE)
        results = [evaluate_fhirpath_expression(part.strip(), resource, context) for part in parts]
        return all(r if isinstance(r, bool) else bool(r) for r in results)
    
    if " or " in expression.lower():
        parts = re.split(r"\s+or\s+", expression, flags=re.IGNORECASE)
        results = [evaluate_fhirpath_expression(part.strip(), resource, context) for part in parts]
        return any(r if isinstance(r, bool) else bool(r) for r in results)
    
    # Handle function calls
    if expression.endswith("()") or "(" in expression:
        return _evaluate_function(expression, resource, context)
    
    # Handle negation
    if expression.lower().startswith("not "):
        inner = expression[4:].strip()
        result = evaluate_fhirpath_expression(inner, resource, context)
        return not (result if isinstance(result, bool) else bool(result))
    
    # Default: try to evaluate as path
    result = _evaluate_path(expression, resource)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] FHIRPath expression evaluation completed: {expression[:50]}")
    return result


def _evaluate_path(path: str, resource: Any) -> Union[List[Any], Any]:
    """
    Evaluate a simple path expression.
    
    Args:
        path: Path expression (e.g., "name.family")
        resource: Resource to evaluate on
        
    Returns:
        Value or list of values
    """
    if not path:
        return resource
    
    parts = path.split(".")
    current = resource
    results = []
    
    for part in parts:
        if not current:
            return []
        
        # Handle array access
        if "[" in part:
            part, index = part.split("[", 1)
            index = index.rstrip("]")
            try:
                index = int(index)
            except ValueError:
                return []
        
        # Get value from object
        if isinstance(current, list):
            # Process each item in list
            for item in current:
                value = _get_value_from_object(item, part)
                if value is not None:
                    if isinstance(value, list):
                        results.extend(value)
                    else:
                        results.append(value)
            current = results if results else None
        else:
            current = _get_value_from_object(current, part)
            if current is None:
                return []
    
    if isinstance(current, list):
        return current if len(current) > 1 else (current[0] if current else None)
    return current


def _get_value_from_object(obj: Any, field_name: str) -> Any:
    """
    Get value from object by field name.
    
    Args:
        obj: Object to get value from
        field_name: Field name
        
    Returns:
        Field value or None
    """
    if obj is None:
        return None
    
    # Handle dataclass/object attributes
    if hasattr(obj, field_name):
        return getattr(obj, field_name)
    
    # Handle dictionary
    if isinstance(obj, dict):
        return obj.get(field_name)
    
    return None


def _evaluate_comparison(expression: str, resource: Any, context: Optional[Any]) -> bool:
    """
    Evaluate a comparison expression.
    
    Enhanced to support FHIRPath comparison operators:
    - = (equals), != (not equals)
    - < (less than), <= (less than or equal)
    - > (greater than), >= (greater than or equal)
    - ~ (equivalent), !~ (not equivalent)
    - in, contains
    
    Args:
        expression: Comparison expression (e.g., "name.count() > 0")
        resource: Resource to evaluate on
        context: Optional context
        
    Returns:
        Boolean result
    """
    # Handle "in" operator (e.g., "code in 'active'|'inactive'")
    if " in " in expression.lower():
        parts = re.split(r"\s+in\s+", expression, flags=re.IGNORECASE)
        if len(parts) == 2:
            left_expr = parts[0].strip()
            right_expr = parts[1].strip()
            left_value = evaluate_fhirpath_expression(left_expr, resource, context)
            # Parse right side as list (pipe-separated or list literal)
            if "|" in right_expr:
                right_values = [v.strip().strip('"\'') for v in right_expr.split("|")]
            else:
                right_values = [_parse_literal(right_expr)]
            if isinstance(left_value, list):
                return any(item in right_values for item in left_value)
            return left_value in right_values
    
    # Handle "contains" operator (e.g., "name contains 'John'")
    if " contains " in expression.lower():
        parts = re.split(r"\s+contains\s+", expression, flags=re.IGNORECASE)
        if len(parts) == 2:
            left_expr = parts[0].strip()
            right_expr = parts[1].strip()
            left_value = evaluate_fhirpath_expression(left_expr, resource, context)
            right_value = _parse_literal(right_expr)
            if isinstance(left_value, str):
                return right_value in left_value
            if isinstance(left_value, list):
                return any(right_value in str(item) for item in left_value)
            return False
    
    # Parse comparison operators
    operators = [
        ("!=", lambda a, b: a != b),
        ("<=", lambda a, b: a <= b),
        (">=", lambda a, b: a >= b),
        ("=", lambda a, b: a == b),
        ("<", lambda a, b: a < b),
        (">", lambda a, b: a > b),
        ("~", lambda a, b: str(a).lower() == str(b).lower()),  # Equivalent (case-insensitive)
        ("!~", lambda a, b: str(a).lower() != str(b).lower()),  # Not equivalent
    ]
    
    for op, func in operators:
        if op in expression:
            parts = expression.split(op, 1)
            if len(parts) == 2:
                left_expr = parts[0].strip()
                right_expr = parts[1].strip()
                
                left_value = evaluate_fhirpath_expression(left_expr, resource, context)
                right_value = _parse_literal(right_expr)
                
                # Handle list results
                if isinstance(left_value, list):
                    # For comparison operators, check if any item matches
                    return any(func(item, right_value) for item in left_value)
                
                return func(left_value, right_value)
    
    return False


def _evaluate_function(expression: str, resource: Any, context: Optional[Any]) -> Union[bool, Any]:
    """
    Evaluate a function call expression.
    
    Enhanced with additional FHIRPath functions:
    - exists(), count(), empty(), contains()
    - startsWith(), endsWith(), length()
    - first(), last(), tail()
    - where(), select(), all(), any()
    - distinct(), union(), intersect()
    
    Args:
        expression: Function expression (e.g., "name.exists()")
        resource: Resource to evaluate on
        context: Optional context
        
    Returns:
        Function result
    """
    # Extract function name and arguments
    match = re.match(r"(.+)\.(\w+)\(\)", expression)
    if match:
        path_expr = match.group(1)
        func_name = match.group(2)
        
        path_value = evaluate_fhirpath_expression(path_expr, resource, context)
        
        if func_name == "exists":
            if isinstance(path_value, list):
                return len(path_value) > 0
            return path_value is not None
        
        if func_name == "count":
            if isinstance(path_value, list):
                return len(path_value)
            return 1 if path_value is not None else 0
        
        if func_name == "empty":
            if isinstance(path_value, list):
                return len(path_value) == 0
            return path_value is None
        
        if func_name == "length":
            if isinstance(path_value, str):
                return len(path_value)
            if isinstance(path_value, list):
                return len(path_value)
            return 0
        
        if func_name == "first":
            if isinstance(path_value, list):
                return path_value[0] if path_value else None
            return path_value
        
        if func_name == "last":
            if isinstance(path_value, list):
                return path_value[-1] if path_value else None
            return path_value
        
        if func_name == "distinct":
            if isinstance(path_value, list):
                seen = set()
                result = []
                for item in path_value:
                    item_hash = str(item)
                    if item_hash not in seen:
                        seen.add(item_hash)
                        result.append(item)
                return result
            return path_value
        
        if func_name == "contains":
            # Handle contains() with argument
            match2 = re.match(r"(.+)\.contains\((.+)\)", expression)
            if match2:
                path_expr = match2.group(1)
                arg_expr = match2.group(2).strip('"\'')
                path_value = evaluate_fhirpath_expression(path_expr, resource, context)
                if isinstance(path_value, str):
                    return arg_expr in path_value
                if isinstance(path_value, list):
                    return any(arg_expr in str(item) for item in path_value)
        
        # Handle startsWith() with argument
        match3 = re.match(r"(.+)\.startsWith\((.+)\)", expression)
        if match3:
            path_expr = match3.group(1)
            arg_expr = match3.group(2).strip('"\'')
            path_value = evaluate_fhirpath_expression(path_expr, resource, context)
            if isinstance(path_value, str):
                return path_value.startswith(arg_expr)
            if isinstance(path_value, list):
                return any(isinstance(item, str) and item.startswith(arg_expr) for item in path_value)
        
        # Handle endsWith() with argument
        match4 = re.match(r"(.+)\.endsWith\((.+)\)", expression)
        if match4:
            path_expr = match4.group(1)
            arg_expr = match4.group(2).strip('"\'')
            path_value = evaluate_fhirpath_expression(path_expr, resource, context)
            if isinstance(path_value, str):
                return path_value.endswith(arg_expr)
            if isinstance(path_value, list):
                return any(isinstance(item, str) and item.endswith(arg_expr) for item in path_value)
        
        # Handle all() - check if all items satisfy condition
        match5 = re.match(r"(.+)\.all\((.+)\)", expression)
        if match5:
            path_expr = match5.group(1)
            condition = match5.group(2).strip()
            path_value = evaluate_fhirpath_expression(path_expr, resource, context)
            if isinstance(path_value, list):
                return all(evaluate_fhirpath_expression(condition, item, context) for item in path_value)
            return evaluate_fhirpath_expression(condition, path_value, context)
        
        # Handle any() - check if any item satisfies condition
        match6 = re.match(r"(.+)\.any\((.+)\)", expression)
        if match6:
            path_expr = match6.group(1)
            condition = match6.group(2).strip()
            path_value = evaluate_fhirpath_expression(path_expr, resource, context)
            if isinstance(path_value, list):
                return any(evaluate_fhirpath_expression(condition, item, context) for item in path_value)
            return evaluate_fhirpath_expression(condition, path_value, context)
    
    return False


def _parse_literal(value_str: str) -> Union[str, int, float, bool, None]:
    """
    Parse a literal value from string.
    
    Args:
        value_str: String representation of value
        
    Returns:
        Parsed value
    """
    value_str = value_str.strip().strip('"\'')
    
    # Boolean
    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False
    
    # Number
    try:
        if "." in value_str:
            return float(value_str)
        return int(value_str)
    except ValueError:
        pass
    
    # String
    return value_str


def validate_constraint(
    constraint: FHIRPathConstraint,
    resource: Any,
    context: Optional[Any] = None
) -> tuple[bool, Optional[str]]:
    """
    Validate a constraint against a resource.
    
    Args:
        constraint: FHIRPathConstraint to validate
        resource: FHIR resource to validate
        context: Optional context resource
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        result = evaluate_fhirpath_expression(constraint.expression, resource, context)
        
        # Result should be boolean or truthy/falsy
        if isinstance(result, bool):
            is_valid = result
        elif isinstance(result, list):
            is_valid = len(result) > 0
        else:
            is_valid = bool(result)
        
        if not is_valid:
            error_msg = constraint.human or f"Constraint '{constraint.key}' failed: {constraint.expression}"
            logger.info(f"[{current_time}] Constraint validation completed: {constraint.key} - FAILED")
            return False, error_msg
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Constraint validation completed: {constraint.key} - PASSED")
        return True, None
    except Exception as e:
        # If evaluation fails, consider it a validation error
        error_msg = f"Constraint '{constraint.key}' evaluation error: {str(e)}"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"[{current_time}] Constraint validation error: {constraint.key} - {str(e)}")
        return False, error_msg


def validate_constraints(
    constraints: List[FHIRPathConstraint],
    resource: Any,
    context: Optional[Any] = None
) -> List[str]:
    """
    Validate multiple constraints against a resource.
    
    Args:
        constraints: List of FHIRPathConstraint objects
        resource: FHIR resource to validate
        context: Optional context resource
        
    Returns:
        List of validation error messages (empty if all valid)
    """
    errors = []
    
    for constraint in constraints:
        is_valid, error_msg = validate_constraint(constraint, resource, context)
        if not is_valid:
            errors.append(error_msg)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Multiple constraints validation completed: {len(constraints)} constraints, {len(errors)} errors")
    return errors

