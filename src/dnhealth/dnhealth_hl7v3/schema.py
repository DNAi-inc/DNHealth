# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 XSD schema validation.

Provides programmatic API for validating HL7 v3 XML messages against XSD schemas.
Includes schema caching, enhanced error reporting, version detection, and support for schema imports/includes.
"""

from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib
import logging
from datetime import datetime

from dnhealth.errors import HL7v3ParseError

logger = logging.getLogger(__name__)


class SchemaValidationError(HL7v3ParseError):
    """Error raised when schema validation fails."""
    pass


# Schema cache for performance optimization
_schema_cache: Dict[str, Tuple[Any, Any]] = {}  # Maps schema_path -> (schema, schema_doc)


class SchemaValidator:
    """
    HL7 v3 XSD schema validator.
    
    Provides methods for loading XSD schemas and validating XML messages.
    Includes schema caching, enhanced error reporting, and version detection.
    """
    
    def __init__(self, schema_path: Optional[str] = None, use_cache: bool = True):
        """
        Initialize schema validator.
        
        Args:
            schema_path: Optional path to XSD schema file
            use_cache: Whether to use schema caching (default: True)
        """
        self.schema_path = schema_path
        self._schema = None
        self._schema_doc = None
        self.use_cache = use_cache
        self._schema_version = None
        
        if schema_path:
            self.load_schema(schema_path)
    
    def load_schema(self, schema_path: str) -> None:
        """
        Load an XSD schema file.
        
        Supports schema caching for performance and handles schema imports/includes.
        
        Args:
            schema_path: Path to XSD schema file
            
        Raises:
            SchemaValidationError: If schema cannot be loaded
        """
        self.schema_path = schema_path
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Loading schema from {schema_path}")
        
        # Check cache first if enabled
        if self.use_cache and schema_path in _schema_cache:
            logger.debug(f"[{current_time}] Using cached schema for {schema_path}")
            self._schema, self._schema_doc = _schema_cache[schema_path]
            self._schema_version = self._detect_schema_version()
            return
        
        # Try to use lxml for XSD validation if available
        try:
            from lxml import etree
            
            try:
                # Create parser with support for schema imports/includes
                parser = etree.XMLParser(load_dtd=False, no_network=False)
                self._schema_doc = etree.parse(schema_path, parser=parser)
                
                # Create XMLSchema with resolver for imports/includes
                # Note: lxml automatically resolves imports/includes when parsing
                self._schema = etree.XMLSchema(self._schema_doc)
                
                # Cache schema if caching is enabled
                if self.use_cache:
                    _schema_cache[schema_path] = (self._schema, self._schema_doc)
                    logger.debug(f"[{current_time}] Cached schema for {schema_path}")
                
                # Detect schema version
                self._schema_version = self._detect_schema_version()
                logger.info(f"[{current_time}] Schema loaded successfully (version: {self._schema_version})")
                
            except etree.XMLSyntaxError as e:
                raise SchemaValidationError(f"Error parsing schema file {schema_path}: {e}") from e
            except Exception as e:
                raise SchemaValidationError(f"Error loading schema file {schema_path}: {e}") from e
        except ImportError:
            # lxml not available - can only do basic XML well-formedness
            self._schema = None
            self._schema_doc = None
            raise SchemaValidationError(
                "lxml library required for XSD schema validation. "
                "Install with: pip install lxml"
            )
    
    def validate(self, xml_string: str) -> List[str]:
        """
        Validate an XML string against the loaded schema.
        
        Provides enhanced error reporting with detailed location information.
        
        Args:
            xml_string: XML string to validate
            
        Returns:
            List of validation error messages (empty if valid)
            
        Raises:
            SchemaValidationError: If validation fails and errors cannot be retrieved
        """
        errors = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting schema validation")
        
        # Basic XML well-formedness check first
        try:
            ET.fromstring(xml_string)
        except ET.ParseError as e:
            error_msg = f"XML parsing error: {str(e)}"
            if hasattr(e, 'lineno') and e.lineno:
                error_msg += f" at line {e.lineno}"
            if hasattr(e, 'offset') and e.offset:
                error_msg += f", column {e.offset}"
            errors.append(error_msg)
            logger.error(f"[{current_time}] XML parsing failed: {error_msg}")
            return errors
        
        # If no schema loaded, return basic check result
        if self._schema is None:
            if self.schema_path:
                errors.append("Schema not loaded. lxml library required for XSD validation.")
            return errors
        
        # Validate against XSD schema using lxml
        try:
            from lxml import etree
            
            try:
                xml_doc = etree.fromstring(xml_string.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                error_msg = f"XML syntax error: {str(e)}"
                if hasattr(e, 'lineno') and e.lineno:
                    error_msg += f" at line {e.lineno}"
                if hasattr(e, 'offset') and e.offset:
                    error_msg += f", column {e.offset}"
                errors.append(error_msg)
                logger.error(f"[{current_time}] XML syntax error: {error_msg}")
                return errors
            
            # Validate against schema
            if not self._schema.validate(xml_doc):
                # Collect validation errors with enhanced details
                for error in self._schema.error_log:
                    error_msg = f"Schema validation error: {error.message}"
                    
                    # Add line number if available
                    if error.line:
                        error_msg += f" (line {error.line})"
                    
                    # Add column number if available
                    if hasattr(error, 'column') and error.column:
                        error_msg += f", column {error.column}"
                    
                    # Add element path if available
                    if hasattr(error, 'path') and error.path:
                        error_msg += f" at path: {error.path}"
                    
                    # Add domain (element/attribute) if available
                    if hasattr(error, 'domain') and error.domain:
                        error_msg += f" [{error.domain}]"
                    
                    errors.append(error_msg)
                    logger.warning(f"[{current_time}] Schema validation error: {error_msg}")
        except ImportError:
            errors.append("lxml library required for XSD schema validation")
        except Exception as e:
            raise SchemaValidationError(f"Error during schema validation: {e}") from e
        
        if errors:
            logger.error(f"[{current_time}] Schema validation failed with {len(errors)} error(s)")
        else:
            logger.debug(f"[{current_time}] Schema validation passed")
        
        return errors
    
    def is_valid(self, xml_string: str) -> bool:
        """
        Check if XML string is valid against the schema.
        
        Args:
            xml_string: XML string to validate
            
        Returns:
            True if valid, False otherwise
        """
        errors = self.validate(xml_string)
        return len(errors) == 0
    
    def _detect_schema_version(self) -> Optional[str]:
        """
        Detect schema version from schema document.
        
        Returns:
            Schema version string or None
        """
        if self._schema_doc is None:
            return None
        
        try:
            from lxml import etree
            root = self._schema_doc.getroot()
            
            # Try to find version in schema attributes
            version = root.get("version")
            if version:
                return version
            
            # Try to find version in targetNamespace (common HL7 v3 pattern)
            target_ns = root.get("targetNamespace")
            if target_ns:
                # HL7 v3 namespaces often contain version info
                # e.g., "urn:hl7-org:v3" or "urn:hl7-org:v3:2015"
                if "v3" in target_ns:
                    # Extract version from namespace if present
                    parts = target_ns.split(":")
                    for part in parts:
                        if part.startswith("v3"):
                            return part
                    return "v3"  # Default to v3 if namespace contains v3
            
            # Try to find version in annotation/documentation
            annotations = root.findall(".//{http://www.w3.org/2001/XMLSchema}annotation")
            for annotation in annotations:
                docs = annotation.findall(".//{http://www.w3.org/2001/XMLSchema}documentation")
                for doc in docs:
                    text = doc.text
                    if text and "version" in text.lower():
                        # Try to extract version number
                        import re
                        match = re.search(r'version\s*[:\-]?\s*([0-9.]+)', text, re.IGNORECASE)
                        if match:
                            return match.group(1)
            
            return None
        except Exception as e:
            logger.warning(f"Error detecting schema version: {e}")
            return None
    
    def get_schema_version(self) -> Optional[str]:
        """
        Get the version of the loaded schema if available.
        
        Returns:
            Schema version string or None
        """
        return self._schema_version
    
    def clear_cache(self) -> None:
        """
        Clear the schema cache.
        
        Useful for freeing memory or forcing schema reload.
        """
        global _schema_cache
        _schema_cache.clear()
        logger.info("Schema cache cleared")
    
    @staticmethod
    def get_cache_size() -> int:
        """
        Get the number of schemas currently cached.
        
        Returns:
            Number of cached schemas
        """

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return len(_schema_cache)


def validate_against_schema(xml_string: str, schema_path: str) -> List[str]:
    """
    Validate an XML string against an XSD schema file.
    
    Convenience function for one-off validations.
    
    Args:
        xml_string: XML string to validate
        schema_path: Path to XSD schema file
        
    Returns:
        List of validation error messages (empty if valid)
        
    Raises:
        SchemaValidationError: If validation fails
    """
    validator = SchemaValidator(schema_path)
    return validator.validate(xml_string)


def is_valid_against_schema(xml_string: str, schema_path: str) -> bool:
    """
    Check if XML string is valid against an XSD schema file.
    
    Convenience function for one-off validations.
    
    Args:
        xml_string: XML string to validate
        schema_path: Path to XSD schema file
        
    Returns:
        True if valid, False otherwise
    """
    validator = SchemaValidator(schema_path)
    return validator.is_valid(xml_string)


def detect_schema_version_from_xml(xml_string: str) -> Optional[str]:
    """
    Detect HL7 v3 schema version from XML message.
    
    Attempts to detect version from namespace declarations or message attributes.
    
    Args:
        xml_string: XML string to analyze
        
    Returns:
        Schema version string (e.g., "v3", "2015") or None if not detectable
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Detecting schema version from XML")
    
    try:
        from lxml import etree
        root = etree.fromstring(xml_string.encode('utf-8'))
        
        # Check namespace declarations
        nsmap = root.nsmap
        for prefix, uri in nsmap.items():
            if uri and "hl7" in uri.lower() and "v3" in uri.lower():
                # Extract version from namespace URI
                # e.g., "urn:hl7-org:v3" or "urn:hl7-org:v3:2015"
                parts = uri.split(":")
                for part in parts:
                    if part.startswith("v3"):
                        version = part
                        # Check for year suffix
                        if len(parts) > parts.index(part) + 1:
                            year_part = parts[parts.index(part) + 1]
                            if year_part.isdigit():
                                version = f"{version}:{year_part}"
                        logger.info(f"[{current_time}] Detected schema version: {version}")
                        return version
        
        # Check root element attributes for version
        version_attr = root.get("version")
        if version_attr:
            logger.info(f"[{current_time}] Detected schema version from attribute: {version_attr}")
            return version_attr
        
        # Default to v3 if HL7 namespace detected
        if any("hl7" in uri.lower() for uri in nsmap.values() if uri):
            logger.info(f"[{current_time}] Defaulting to schema version: v3")
            return "v3"
        
        return None
    except Exception as e:
        logger.warning(f"[{current_time}] Error detecting schema version: {e}")
        return None


def select_schema_for_message(xml_string: str, schema_paths: Dict[str, str]) -> Optional[str]:
    """
    Select appropriate schema path based on message content.
    
    Detects message version and selects matching schema from provided paths.
    
    Args:
        xml_string: XML string to analyze
        schema_paths: Dictionary mapping version strings to schema paths
                     e.g., {"v3": "/path/to/v3.xsd", "2015": "/path/to/2015.xsd"}
        
    Returns:
        Selected schema path or None if no match found
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Selecting schema for message")
    
    detected_version = detect_schema_version_from_xml(xml_string)
    
    if detected_version:
        # Try exact match first
        if detected_version in schema_paths:
            selected = schema_paths[detected_version]
            logger.info(f"[{current_time}] Selected schema: {selected} (version: {detected_version})")
            return selected
        
        # Try partial match (e.g., "v3:2015" -> "2015")
        for version_key, schema_path in schema_paths.items():
            if version_key in detected_version or detected_version in version_key:
                logger.info(f"[{current_time}] Selected schema: {schema_path} (version match: {version_key})")
                return schema_path
    
    # Default to first schema if no version detected
    if schema_paths:
        default_path = list(schema_paths.values())[0]
        logger.warning(f"[{current_time}] No version detected, using default schema: {default_path}")
        return default_path
    
    return None
