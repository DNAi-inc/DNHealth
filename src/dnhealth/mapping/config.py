# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Mapping configuration utilities.

Provides functions to load, save, and create mapping configurations.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


def load_mapping_config(config_path: str) -> Dict[str, Any]:
    """
    Load mapping configuration from JSON file.
    
    Args:
        config_path: Path to configuration JSON file
        
    Returns:
        Mapping configuration dictionary
        
    Raises:
        FileNotFoundError: If configuration file does not exist
        ValueError: If configuration file is invalid
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Loading mapping configuration from {config_path}")
    
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logger.info(f"[{current_time}] Mapping configuration loaded successfully")
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {completion_time}")
        return config
    except json.JSONDecodeError as e:
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"Current Time at End of Operations: {completion_time}")
        raise ValueError(f"Invalid JSON in configuration file: {e}")
    except Exception as e:
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"Current Time at End of Operations: {completion_time}")
        raise ValueError(f"Error loading configuration file: {e}")


def save_mapping_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save mapping configuration to JSON file.
    
    Args:
        config: Mapping configuration dictionary
        config_path: Path to save configuration JSON file
        
    Raises:
        ValueError: If configuration is invalid
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Saving mapping configuration to {config_path}")
    
    try:
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[{current_time}] Mapping configuration saved successfully")
        # Log completion timestamp at end of operation
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {completion_time}")
    except Exception as e:
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"Current Time at End of Operations: {completion_time}")
        raise ValueError(f"Error saving configuration file: {e}")


def create_mapping_config(
    source_type: str,
    target_type: str,
    field_mappings: Dict[str, str],
    transformation_rules: Optional[Dict[str, Any]] = None,    custom_rules: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a mapping configuration.
    
    Args:
        source_type: Source message/resource type (e.g., "HL7v2_ADT", "FHIR_Patient")
        target_type: Target message/resource type (e.g., "FHIR_Patient", "HL7v2_ADT")
        field_mappings: Dictionary mapping source field paths to target field paths
        transformation_rules: Optional dictionary of transformation rules
        custom_rules: Optional list of custom mapping rules
        
    Returns:
        Mapping configuration dictionary
        
    Example:
        >>> config = create_mapping_config(
        ...     source_type="HL7v2_ADT",
        ...     target_type="FHIR_Patient",
        ...     field_mappings={
        ...         "PID.3.1": "identifier[0].value",
        ...         "PID.5.1": "name[0].family",
        ...         "PID.5.2": "name[0].given[0]",
        ...     }
        ... )
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Creating mapping configuration: {source_type} -> {target_type}")
    
    config = {
        "version": "1.0",
        "created": current_time,
        "source_type": source_type,
        "target_type": target_type,
        "field_mappings": field_mappings,
        "transformation_rules": transformation_rules or {},
        "custom_rules": custom_rules or []
    }
    
    logger.info(f"[{current_time}] Mapping configuration created successfully")
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {completion_time}")
    return config


def validate_mapping_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate mapping configuration.
    
    Args:
        config: Mapping configuration dictionary
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors: List[str] = []
    
    # Check required fields
    if "source_type" not in config:
        errors.append("Missing required field: source_type")
    
    if "target_type" not in config:
        errors.append("Missing required field: target_type")
    
    if "field_mappings" not in config:
        errors.append("Missing required field: field_mappings")
    
    # Validate field_mappings
    if "field_mappings" in config:
        if not isinstance(config["field_mappings"], dict):
            errors.append("field_mappings must be a dictionary")
    
    # Validate transformation_rules
    if "transformation_rules" in config:
        if not isinstance(config["transformation_rules"], dict):
            errors.append("transformation_rules must be a dictionary")
    
    # Validate custom_rules
    if "custom_rules" in config:
        if not isinstance(config["custom_rules"], list):
            errors.append("custom_rules must be a list")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"Current Time at End of Operations: {completion_time}")
    return errors
