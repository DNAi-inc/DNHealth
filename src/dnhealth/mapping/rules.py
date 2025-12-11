# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Mapping rules utilities.

Provides functions to create and apply custom mapping rules.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from time import time

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class MappingRule:
    """
    Represents a custom mapping rule.
    
    A mapping rule defines how to transform data from source to target format.
    """
    
    def __init__(
        self,
        name: str,
        source_path: str,
        target_path: str,
        transformation: Optional[Callable[[Any], Any]] = None,
        condition: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None
    ):
        """
        Initialize mapping rule.
        
        Args:
            name: Rule name
            source_path: Source field path (e.g., "PID.5.1" for HL7v2, "name[0].family" for FHIR)
            target_path: Target field path
            transformation: Optional transformation function to apply to source value
            condition: Optional condition function to check if rule should be applied
            description: Optional rule description
        """
        self.name = name
        self.source_path = source_path
        self.target_path = target_path
        self.transformation = transformation
        self.condition = condition
        self.description = description
    
    def apply(self, source_data: Any, target_data: Any) -> Any:
        """
        Apply mapping rule to transform data.
        
        Args:
            source_data: Source data object
            target_data: Target data object
            
        Returns:
            Transformed target data object
        """
        # Check condition if provided
        if self.condition and not self.condition(source_data):
            return target_data
        
        # Get source value
        source_value = self._get_value_by_path(source_data, self.source_path)
        
        if source_value is None:
            return target_data
        
        # Apply transformation if provided
        if self.transformation:
            try:
                source_value = self.transformation(source_value)
            except Exception as e:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Transformation failed for rule {self.name}: {e}"
                )
                return target_data
        
        # Set target value
        self._set_value_by_path(target_data, self.target_path, source_value)
        
        return target_data
    
    def _get_value_by_path(self, data: Any, path: str) -> Any:
        """Get value from data object by path."""
        # Simplified implementation - would need to handle different data structures
        # (HL7v2 Message, HL7v3 Message, FHIR Resource, etc.)
        parts = path.split(".")
        value = data
        
        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            elif isinstance(value, (list, dict)):
                # Handle list/dict access
                if isinstance(value, list) and part.isdigit():
                    idx = int(part)
                    if 0 <= idx < len(value):
                        value = value[idx]
                    else:
                        return None
                elif isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            else:
                return None
        

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return value
    
    def _set_value_by_path(self, data: Any, path: str, value: Any) -> None:
        """Set value in data object by path."""
        # Simplified implementation - would need to handle different data structures
        parts = path.split(".")
        current = data
        
        # Navigate to parent
        for part in parts[:-1]:
            if hasattr(current, part):
                current = getattr(current, part)
            elif isinstance(current, (list, dict)):
                if isinstance(current, list) and part.isdigit():
                    idx = int(part)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return
                elif isinstance(current, dict):
                    current = current.get(part)
                else:
                    return
            else:
                return
        
        # Set value
        final_part = parts[-1]
        if hasattr(current, final_part):
            setattr(current, final_part, value)
        elif isinstance(current, dict):
            current[final_part] = value


def apply_mapping_rules(
    source_data: Any,
    target_data: Any,
    rules: List[MappingRule],
    timeout: int = TEST_TIMEOUT
) -> Any:
    """
    Apply list of mapping rules to transform data.
    
    Args:
        source_data: Source data object
        target_data: Target data object
        rules: List of MappingRule objects to apply
        timeout: Maximum time in seconds for rule application (default: 300)
        
    Returns:
        Transformed target data object
        
    Raises:
        ValueError: If rule application exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Applying {len(rules)} mapping rules")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Rule application exceeded timeout of {timeout} seconds")
    
    result = target_data
    
    for rule in rules:
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Rule application exceeded timeout of {timeout} seconds")
        
        try:
            result = rule.apply(source_data, result)
        except Exception as e:
            logger.warning(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Rule {rule.name} failed: {e}"
            )
            continue
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] Mapping rules applied in {elapsed:.2f} seconds")
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return result


def create_custom_rule(
    name: str,
    source_path: str,
    target_path: str,
    transformation: Optional[Callable[[Any], Any]] = None,
    condition: Optional[Callable[[Any], bool]] = None,
    description: Optional[str] = None
) -> MappingRule:
    """
    Create a custom mapping rule.
    
    Args:
        name: Rule name
        source_path: Source field path
        target_path: Target field path
        transformation: Optional transformation function
        condition: Optional condition function
        description: Optional rule description
        
    Returns:
        MappingRule object
        
    Example:
        >>> def uppercase_transform(value):
        ...     return value.upper() if isinstance(value, str) else value
        ...
        >>> rule = create_custom_rule(
        ...     name="uppercase_name",
        ...     source_path="PID.5.1",
        ...     target_path="name[0].family",
        ...     transformation=uppercase_transform,
        ...     description="Convert family name to uppercase"
        ... )
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Creating custom mapping rule: {name}")
    
    rule = MappingRule(
        name=name,
        source_path=source_path,
        target_path=target_path,
        transformation=transformation,
        condition=condition,
        description=description
    )
    
    logger.debug(f"[{current_time}] Custom mapping rule created: {name}")
    return rule
