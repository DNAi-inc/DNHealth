# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Configuration management utilities for DNHealth library.

Provides configuration loading from files, environment variables, and defaults.
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Config:
    """
    Configuration manager for DNHealth library.

    Supports loading configuration from:
    - Environment variables (DNHEALTH_* prefix)
    - JSON configuration files
    - Default values
    """

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_file: Optional path to JSON configuration file
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Initializing configuration")
        
        self._config: Dict[str, Any] = {}
        self._load_defaults()
        if config_file and config_file.exists():
            self._load_file(config_file)
        self._load_environment()
        
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Configuration initialization completed")

    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self._config = {
            "hl7v2": {
                "tolerant_parsing": False,
                "preserve_formatting": False,
                "validate_version": True,
            },
            "hl7v3": {
                "validate_schema": False,
                "preserve_namespaces": True,
            },
            "fhir": {
                "validate_profiles": False,
                "strict_validation": False,
                "preserve_unknown_fields": True,
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "network": {
                "timeout": 30,
                "retries": 3,
                "retry_delay": 1.0,
            },
        }

    def _load_file(self, config_file: Path) -> None:
        """Load configuration from JSON file."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Loading configuration from file: {config_file}")
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                self._config.update(file_config)
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{completion_time}] Configuration file loaded successfully")
        except (IOError, json.JSONDecodeError) as e:
            # Silently fail - use defaults
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"[{completion_time}] Configuration file load failed, using defaults")
            pass

    def _load_environment(self) -> None:
        """Load configuration from environment variables."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Loading configuration from environment variables")
        
        env_count = 0
        for key, value in os.environ.items():
            if key.startswith("DNHEALTH_"):
                env_count += 1
                # Convert DNHEALTH_SECTION_KEY to section.key
                parts = key[9:].lower().split("_", 1)
                if len(parts) == 2:
                    section, option = parts
                    if section not in self._config:
                        self._config[section] = {}
                    # Try to convert to appropriate type
                    self._config[section][option] = self._parse_value(value)
                else:
                    # Single part key
                    self._config[parts[0].lower()] = self._parse_value(value)
        
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{completion_time}] Environment configuration loading completed ({env_count} variables processed)")

    def _parse_value(self, value: str) -> Any:
        """
        Parse environment variable value to appropriate type.

        Args:
            value: String value from environment

        Returns:
            Parsed value (bool, int, float, or str)
        """
        # Try boolean
        if value.lower() in ("true", "1", "yes", "on"):
            return True
        if value.lower() in ("false", "0", "no", "off"):
            return False

        # Try integer
        try:
            return int(value)
        except ValueError:
            pass

        # Try float
        try:
            return float(value)
        except ValueError:
            pass

        # Return as string
        return value

    def get(self, section: str, option: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            section: Configuration section (e.g., "hl7v2")
            option: Configuration option (e.g., "tolerant_parsing")
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self._config.get(section, {}).get(option, default)

    def set(self, section: str, option: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            section: Configuration section
            option: Configuration option
            value: Value to set
        """
        if section not in self._config:
            self._config[section] = {}
        self._config[section][option] = value

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.

        Args:
            section: Configuration section name

        Returns:
            Dictionary of section options
        """

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self._config.get(section, {})



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
# Global configuration instance
_default_config: Optional[Config] = None


def get_config(config_file: Optional[Path] = None) -> Config:
    """
    Get global configuration instance.

    Args:
        config_file: Optional path to configuration file

    Returns:
        Config instance
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Getting global configuration instance")
    
    global _default_config
    if _default_config is None:
        _default_config = Config(config_file)
    
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Global configuration instance retrieved")
    
    return _default_config


def reset_config() -> None:
    """Reset global configuration (useful for testing)."""
    global _default_config
    _default_config = None

