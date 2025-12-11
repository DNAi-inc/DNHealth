# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
HL7 v2.x version profiles and version-specific definitions.

Provides version-specific field definitions, segment definitions, and data type definitions
for different HL7 v2.x versions (2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9).
"""

from typing import Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class VersionProfile:
    """
    Profile for a specific HL7 v2.x version.
    
    Contains version-specific definitions for segments, fields, and data types.
    """

    def __init__(self, version: str):
        """
        Initialize version profile.

        Args:
            version: HL7 version string (e.g., "2.5")
        """
        self.version = version
        self.segment_definitions: Dict[str, Dict] = {}
        self.field_definitions: Dict[str, Dict[int, Dict]] = {}  # segment_name -> field_index -> definition
        self.data_type_definitions: Dict[str, Dict] = {}
        self.table_definitions: Dict[str, Dict[str, str]] = {}  # table_id -> code -> description

    def add_segment_definition(self, segment_name: str, definition: Dict):
        """
        Add segment definition for this version.

        Args:
            segment_name: Segment name (3 characters)
            definition: Segment definition dictionary
        """
        self.segment_definitions[segment_name] = definition

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def add_field_definition(self, segment_name: str, field_index: int, definition: Dict):
        """
        Add field definition for this version.

        Args:
            segment_name: Segment name
            field_index: Field index (1-based)
            definition: Field definition dictionary
        """
        if segment_name not in self.field_definitions:
            self.field_definitions[segment_name] = {}
        self.field_definitions[segment_name][field_index] = definition

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def get_segment_definition(self, segment_name: str) -> Optional[Dict]:
        """
        Get segment definition.

        Args:
            segment_name: Segment name

        Returns:
            Segment definition or None
        """
        return self.segment_definitions.get(segment_name)

    def get_field_definition(self, segment_name: str, field_index: int) -> Optional[Dict]:
        """
        Get field definition.

        Args:
            segment_name: Segment name
            field_index: Field index (1-based)

        Returns:
            Field definition or None
        """
        return self.field_definitions.get(segment_name, {}).get(field_index)

    def add_table_definition(self, table_id: str, code: str, description: str):
        """
        Add table value definition.

        Args:
            table_id: Table identifier
            code: Code value
            description: Code description
        """
        if table_id not in self.table_definitions:
            self.table_definitions[table_id] = {}
        self.table_definitions[table_id][code] = description

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def get_table_definition(self, table_id: str) -> Optional[Dict[str, str]]:
        """
        Get table definition for a specific table ID.

        Args:
            table_id: Table identifier (e.g., "0001", "0008")

        Returns:
            Dictionary mapping codes to descriptions, or None if table not found
        """
        return self.table_definitions.get(table_id)

    def get_table_value(self, table_id: str, code: str) -> Optional[str]:
        """
        Get description for a specific code in a table.

        Args:
            table_id: Table identifier (e.g., "0001", "0008")
            code: Code value to look up

        Returns:
            Description string if code exists, None otherwise
        """
        table = self.get_table_definition(table_id)
        if table is None:
            return None
        return table.get(code)
    
    def get_available_segments(self) -> List[str]:
        """
        Get list of all segment names available in this version profile.
        
        Returns:
            List of segment names (e.g., ["MSH", "PID", "OBR", ...])
        """
        return sorted(list(self.segment_definitions.keys()))
    
    def is_segment_available(self, segment_name: str) -> bool:
        """
        Check if a segment is available in this version profile.
        
        Args:
            segment_name: Segment name to check
            
        Returns:
            True if segment is available, False otherwise
        """
        return segment_name in self.segment_definitions

    def validate_table_value(self, table_id: str, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a code against a table definition.

        Args:
            table_id: Table identifier (e.g., "0001", "0008")
            code: Code value to validate

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if code is valid, False otherwise
            - error_message: None if valid, error description if invalid
        """
        table = self.get_table_definition(table_id)
        if table is None:
            return False, f"Table {table_id} not found in profile for version {self.version}"
        
        if code in table:
            return True, None
        
        return False, f"Code '{code}' is not valid for table {table_id}"

    def add_data_type_definition(self, data_type: str, definition: Dict):
        """
        Add data type definition for this version.

        Args:
            data_type: Data type name (e.g., "ST", "TS", "AD")
            definition: Data type definition dictionary containing:
                - name: Full name of the data type
                - description: Description of the data type
                - components: List of component definitions (for composite types)
                - max_length: Maximum length (for primitive types)
                - format: Format specification (for dates/times)
                - version_specific: Version-specific notes or changes
        """
        self.data_type_definitions[data_type] = definition

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")

    def get_data_type_definition(self, data_type: str) -> Optional[Dict]:
        """
        Get data type definition.

        Args:
            data_type: Data type name (e.g., "ST", "TS", "AD")

        Returns:
            Data type definition or None
        """

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        
        return self.data_type_definitions.get(data_type)


# Registry of version profiles
_version_profiles: Dict[str, VersionProfile] = {}


def _add_version_specific_segment_definition(
    profile: VersionProfile,
    segment_name: str,
    definition: Dict,
    min_version: Optional[str] = None,
    max_version: Optional[str] = None,
    versions: Optional[List[str]] = None,
) -> None:
    """
    Add version-specific segment definition with version constraints.
    
    This function ensures segment definitions are properly versioned and tracks
    which versions support which segments. It allows specifying version ranges
    or specific versions where a segment is available.
    
    Args:
        profile: VersionProfile to add segment definition to
        segment_name: Segment name (3 characters)
        definition: Segment definition dictionary with metadata
        min_version: Minimum version where segment is available (e.g., "2.5")
        max_version: Maximum version where segment is available (e.g., "2.9")
        versions: Specific list of versions where segment is available
                 (e.g., ["2.5", "2.6", "2.7"])
    
    Note:
        If versions is specified, min_version and max_version are ignored.
        Version comparison uses string comparison (e.g., "2.5" < "2.6").
    """
    import datetime
    from dnhealth.util.logging import get_logger
    
    logger = get_logger(__name__)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{current_time}] Adding version-specific segment definition for {segment_name}")
    
    version = profile.version
    
    # Determine if this version should have this segment
    should_add = False
    
    if versions is not None:
        # Specific versions list provided
        should_add = version in versions
    elif min_version is not None or max_version is not None:
        # Version range provided
        version_float = float(version)
        min_float = float(min_version) if min_version else 0.0
        max_float = float(max_version) if max_version else 999.0
        should_add = min_float <= version_float <= max_float
    else:
        # No version constraints - add to all versions
        should_add = True
    
    if should_add:
        # Add version metadata to definition
        enhanced_definition = definition.copy()
        enhanced_definition["version"] = version
        enhanced_definition["available_in_versions"] = versions if versions else (
            f"{min_version or 'all'}-{max_version or 'all'}"
        )
        
        profile.add_segment_definition(segment_name, enhanced_definition)
        logger.debug(f"[{current_time}] Added segment {segment_name} definition for version {version}")


def get_profile(version: str) -> VersionProfile:
    """
    Get version profile for a specific version.

    Args:
        version: HL7 version string (e.g., "2.5")

    Returns:
        VersionProfile instance
    """
    if version not in _version_profiles:
        _version_profiles[version] = VersionProfile(version)
        _initialize_default_profile(_version_profiles[version])
    return _version_profiles[version]


def _initialize_default_profile(profile: VersionProfile):
    """
    Initialize default profile with common segment definitions.

    Args:
        profile: VersionProfile to initialize
    """
    version = profile.version
    
    # MSH segment definition (common across all versions)
    _add_version_specific_segment_definition(
        profile,
        "MSH",
        {
            "name": "MSH",
            "description": "Message Header",
            "required": True,
            "max_repetitions": 1,
        }
    )
    
    # Common MSH fields (all versions)
    profile.add_field_definition("MSH", 1, {
        "name": "Field Separator",
        "data_type": "ST",
        "required": True,
        "max_length": 1,
    })
    profile.add_field_definition("MSH", 2, {
        "name": "Encoding Characters",
        "data_type": "ST",
        "required": True,
        "max_length": 4,
    })
    profile.add_field_definition("MSH", 3, {
        "name": "Sending Application",
        "data_type": "HD",
        "required": False,
    })
    profile.add_field_definition("MSH", 4, {
        "name": "Sending Facility",
        "data_type": "HD",
        "required": False,
    })
    profile.add_field_definition("MSH", 5, {
        "name": "Receiving Application",
        "data_type": "HD",
        "required": False,
    })
    profile.add_field_definition("MSH", 6, {
        "name": "Receiving Facility",
        "data_type": "HD",
        "required": False,
    })
    profile.add_field_definition("MSH", 7, {
        "name": "Date/Time of Message",
        "data_type": "TS",
        "required": False,
    })
    profile.add_field_definition("MSH", 8, {
        "name": "Security",
        "data_type": "ST",
        "required": False,
    })
    profile.add_field_definition("MSH", 9, {
        "name": "Message Type",
        "data_type": "MSG",
        "required": True,
    })
    profile.add_field_definition("MSH", 10, {
        "name": "Message Control ID",
        "data_type": "ST",
        "required": True,
    })
    profile.add_field_definition("MSH", 11, {
        "name": "Processing ID",
        "data_type": "PT",
        "required": False,
    })
    profile.add_field_definition("MSH", 12, {
        "name": "Version ID",
        "data_type": "VID",
        "required": False,
    })
    
    # Version-specific MSH fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # MSH-13: Sequence Number (added in 2.5+)
        profile.add_field_definition("MSH", 13, {
            "name": "Sequence Number",
            "data_type": "NM",
            "required": False,
        })
        # MSH-14: Continuation Pointer (added in 2.5+)
        profile.add_field_definition("MSH", 14, {
            "name": "Continuation Pointer",
            "data_type": "ST",
            "required": False,
        })
        # MSH-15: Accept Acknowledgment Type (added in 2.5+)
        profile.add_field_definition("MSH", 15, {
            "name": "Accept Acknowledgment Type",
            "data_type": "ID",
            "required": False,
        })
        # MSH-16: Application Acknowledgment Type (added in 2.5+)
        profile.add_field_definition("MSH", 16, {
            "name": "Application Acknowledgment Type",
            "data_type": "ID",
            "required": False,
        })
        # MSH-17: Country Code (added in 2.5+)
        profile.add_field_definition("MSH", 17, {
            "name": "Country Code",
            "data_type": "ID",
            "required": False,
        })
        # MSH-18: Character Set (added in 2.5+)
        profile.add_field_definition("MSH", 18, {
            "name": "Character Set",
            "data_type": "ID",
            "required": False,
        })
        # MSH-19: Principal Language of Message (added in 2.5+)
        profile.add_field_definition("MSH", 19, {
            "name": "Principal Language of Message",
            "data_type": "CE",
            "required": False,
        })
        # MSH-20: Alternate Character Set Handling Scheme (added in 2.5+)
        profile.add_field_definition("MSH", 20, {
            "name": "Alternate Character Set Handling Scheme",
            "data_type": "ID",
            "required": False,
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # MSH-21: Message Profile Identifier (added in 2.7+)
        profile.add_field_definition("MSH", 21, {
            "name": "Message Profile Identifier",
            "data_type": "EI",
            "required": False,
        })
    
    # MSA segment definition
    profile.add_segment_definition("MSA", {
        "name": "MSA",
        "description": "Message Acknowledgment",
        "required": False,
        "max_repetitions": 1,
    })
    
    profile.add_field_definition("MSA", 1, {
        "name": "Acknowledgment Code",
        "data_type": "ID",
        "required": True,
        "table": "0008",  # AA, AE, AR
    })
    profile.add_field_definition("MSA", 2, {
        "name": "Message Control ID",
        "data_type": "ST",
        "required": True,
    })
    # MSA-3: Text Message (optional, all versions)
    profile.add_field_definition("MSA", 3, {
        "name": "Text Message",
        "data_type": "ST",
        "required": False,
    })
    # MSA-4: Expected Sequence Number (optional, all versions)
    profile.add_field_definition("MSA", 4, {
        "name": "Expected Sequence Number",
        "data_type": "NM",
        "required": False,
    })
    
    # Version-specific MSA fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # MSA-5: Delayed Acknowledgment Type (added in 2.5+)
        profile.add_field_definition("MSA", 5, {
            "name": "Delayed Acknowledgment Type",
            "data_type": "ID",
            "required": False,
        })
        # MSA-6: Error Condition (added in 2.5+)
        profile.add_field_definition("MSA", 6, {
            "name": "Error Condition",
            "data_type": "CE",
            "required": False,
        })
    
    # NTE segment definition
    profile.add_segment_definition("NTE", {
        "name": "NTE",
        "description": "Notes and Comments",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # NTE-1: Set ID - NTE (optional, all versions)
    profile.add_field_definition("NTE", 1, {
        "name": "Set ID - NTE",
        "data_type": "SI",
        "required": False,
    })
    # NTE-2: Source of Comment (optional, all versions)
    profile.add_field_definition("NTE", 2, {
        "name": "Source of Comment",
        "data_type": "ID",
        "required": False,
        "table": "0105",  # Source of Comment table
    })
    # NTE-3: Comment (optional, all versions, unlimited repetitions)
    profile.add_field_definition("NTE", 3, {
        "name": "Comment",
        "data_type": "FT",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # Version-specific NTE fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # NTE-4: Comment Type (added in 2.5+)
        profile.add_field_definition("NTE", 4, {
            "name": "Comment Type",
            "data_type": "CE",
            "required": False,
        })
    
    # PID segment definition
    profile.add_segment_definition("PID", {
        "name": "PID",
        "description": "Patient Identification",
        "required": False,
        "max_repetitions": 1,
    })
    
    # PID-1: Set ID - PID (all versions)
    # Used when multiple PID segments exist in a message
    profile.add_field_definition("PID", 1, {
        "name": "Set ID - PID",
        "data_type": "SI",
        "required": False,
    })
    
    # PID-2: Patient ID (deprecated in 2.3+, replaced by PID-3)
    # This field exists in all versions but is deprecated in 2.3+
    profile.add_field_definition("PID", 2, {
        "name": "Patient ID",
        "data_type": "CX",
        "required": False,
        "deprecated": version not in ("2.1", "2.2"),  # Deprecated in 2.3+
    })
    
    profile.add_field_definition("PID", 3, {
        "name": "Patient Identifier List",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,  # Unlimited
    })
    
    # PID-4: Alternate Patient ID - PID (deprecated in 2.3+, replaced by PID-3)
    # This field exists in all versions but is deprecated in 2.3+
    profile.add_field_definition("PID", 4, {
        "name": "Alternate Patient ID - PID",
        "data_type": "CX",
        "required": False,
        "deprecated": version not in ("2.1", "2.2"),  # Deprecated in 2.3+
    })
    
    profile.add_field_definition("PID", 5, {
        "name": "Patient Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PID-6: Mother's Maiden Name (all versions)
    profile.add_field_definition("PID", 6, {
        "name": "Mother's Maiden Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    profile.add_field_definition("PID", 7, {
        "name": "Date/Time of Birth",
        "data_type": "TS",
        "required": False,
    })
    profile.add_field_definition("PID", 8, {
        "name": "Administrative Sex",
        "data_type": "IS",
        "required": False,
        "table": "0001",  # M, F, O, U
    })
    
    # Version-specific PID fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # PID-9: Patient Alias (added in 2.5+)
        profile.add_field_definition("PID", 9, {
            "name": "Patient Alias",
            "data_type": "XPN",
            "required": False,
            "max_repetitions": None,
        })
        # PID-10: Race (added in 2.5+)
        profile.add_field_definition("PID", 10, {
            "name": "Race",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PID-11: Patient Address (added in 2.5+)
        profile.add_field_definition("PID", 11, {
            "name": "Patient Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # PID-12: County Code (added in 2.5+)
        profile.add_field_definition("PID", 12, {
            "name": "County Code",
            "data_type": "IS",
            "required": False,
        })
        # PID-13: Phone Number - Home (added in 2.5+)
        profile.add_field_definition("PID", 13, {
            "name": "Phone Number - Home",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # PID-14: Phone Number - Business (added in 2.5+)
        profile.add_field_definition("PID", 14, {
            "name": "Phone Number - Business",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # PID-15: Primary Language (added in 2.5+)
        profile.add_field_definition("PID", 15, {
            "name": "Primary Language",
            "data_type": "CE",
            "required": False,
        })
        # PID-16: Marital Status (added in 2.5+)
        profile.add_field_definition("PID", 16, {
            "name": "Marital Status",
            "data_type": "CE",
            "required": False,
            "table": "0002",
        })
        # PID-17: Religion (added in 2.5+)
        profile.add_field_definition("PID", 17, {
            "name": "Religion",
            "data_type": "CE",
            "required": False,
        })
        # PID-18: Patient Account Number (added in 2.5+)
        profile.add_field_definition("PID", 18, {
            "name": "Patient Account Number",
            "data_type": "CX",
            "required": False,
        })
        # PID-19: SSN Number - Patient (added in 2.5+)
        profile.add_field_definition("PID", 19, {
            "name": "SSN Number - Patient",
            "data_type": "ST",
            "required": False,
        })
        # PID-20: Driver's License Number - Patient (added in 2.5+)
        profile.add_field_definition("PID", 20, {
            "name": "Driver's License Number - Patient",
            "data_type": "DLN",
            "required": False,
        })
        # PID-21: Mother's Identifier (added in 2.5+)
        profile.add_field_definition("PID", 21, {
            "name": "Mother's Identifier",
            "data_type": "CX",
            "required": False,
            "max_repetitions": None,
        })
        # PID-22: Ethnic Group (added in 2.5+)
        profile.add_field_definition("PID", 22, {
            "name": "Ethnic Group",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PID-23: Birth Place (added in 2.5+)
        profile.add_field_definition("PID", 23, {
            "name": "Birth Place",
            "data_type": "ST",
            "required": False,
        })
        # PID-24: Multiple Birth Indicator (added in 2.5+)
        profile.add_field_definition("PID", 24, {
            "name": "Multiple Birth Indicator",
            "data_type": "ID",
            "required": False,
        })
        # PID-25: Birth Order (added in 2.5+)
        profile.add_field_definition("PID", 25, {
            "name": "Birth Order",
            "data_type": "NM",
            "required": False,
        })
        # PID-26: Citizenship (added in 2.5+)
        profile.add_field_definition("PID", 26, {
            "name": "Citizenship",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PID-27: Veterans Military Status (added in 2.5+)
        profile.add_field_definition("PID", 27, {
            "name": "Veterans Military Status",
            "data_type": "CE",
            "required": False,
        })
        # PID-28: Nationality (added in 2.5+)
        profile.add_field_definition("PID", 28, {
            "name": "Nationality",
            "data_type": "CE",
            "required": False,
        })
        # PID-29: Patient Death Date and Time (added in 2.5+)
        profile.add_field_definition("PID", 29, {
            "name": "Patient Death Date and Time",
            "data_type": "TS",
            "required": False,
        })
        # PID-30: Patient Death Indicator (added in 2.5+)
        profile.add_field_definition("PID", 30, {
            "name": "Patient Death Indicator",
            "data_type": "ID",
            "required": False,
        })
    
    # PID fields added in version 2.7+
    if version in ("2.7", "2.8", "2.9"):
        # PID-31: Identity Unknown Indicator (added in 2.7+)
        profile.add_field_definition("PID", 31, {
            "name": "Identity Unknown Indicator",
            "data_type": "ID",
            "required": False,
        })
        # PID-32: Identity Reliability Code (added in 2.7+)
        profile.add_field_definition("PID", 32, {
            "name": "Identity Reliability Code",
            "data_type": "IS",
            "required": False,
        })
        # PID-33: Last Update Date/Time (added in 2.7+)
        profile.add_field_definition("PID", 33, {
            "name": "Last Update Date/Time",
            "data_type": "TS",
            "required": False,
        })
        # PID-34: Last Update Facility (added in 2.7+)
        profile.add_field_definition("PID", 34, {
            "name": "Last Update Facility",
            "data_type": "HD",
            "required": False,
        })
        # PID-35: Taxonomic Classification Code (added in 2.7+)
        profile.add_field_definition("PID", 35, {
            "name": "Taxonomic Classification Code",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PID-36: Breed Code (added in 2.7+)
        profile.add_field_definition("PID", 36, {
            "name": "Breed Code",
            "data_type": "CE",
            "required": False,
        })
        # PID-37: Strain (added in 2.7+)
        profile.add_field_definition("PID", 37, {
            "name": "Strain",
            "data_type": "ST",
            "required": False,
        })
        # PID-38: Production Class Code (added in 2.7+)
        profile.add_field_definition("PID", 38, {
            "name": "Production Class Code",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PID-39: Tribal Citizenship (added in 2.7+)
        profile.add_field_definition("PID", 39, {
            "name": "Tribal Citizenship",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
    
    # Common table definitions
    profile.add_table_definition("0001", "M", "Male")
    profile.add_table_definition("0001", "F", "Female")
    profile.add_table_definition("0001", "O", "Other")
    profile.add_table_definition("0001", "U", "Unknown")
    
    profile.add_table_definition("0008", "AA", "Application Accept")
    profile.add_table_definition("0008", "AE", "Application Error")
    profile.add_table_definition("0008", "AR", "Application Reject")
    
    # OBR segment definition (Observation Request)
    profile.add_segment_definition("OBR", {
        "name": "OBR",
        "description": "Observation Request",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-1: Set ID - OBR (all versions)
    profile.add_field_definition("OBR", 1, {
        "name": "Set ID - OBR",
        "data_type": "SI",
        "required": False,
    })
    
    # OBR-2: Placer Order Number (all versions)
    profile.add_field_definition("OBR", 2, {
        "name": "Placer Order Number",
        "data_type": "EI",
        "required": False,
    })
    
    # OBR-3: Filler Order Number (all versions)
    profile.add_field_definition("OBR", 3, {
        "name": "Filler Order Number",
        "data_type": "EI",
        "required": False,
    })
    
    # OBR-4: Universal Service Identifier (all versions)
    profile.add_field_definition("OBR", 4, {
        "name": "Universal Service Identifier",
        "data_type": "CE",
        "required": True,
    })
    
    # OBR-5: Priority - OBR (all versions)
    profile.add_field_definition("OBR", 5, {
        "name": "Priority - OBR",
        "data_type": "ID",
        "required": False,
        "table": "0027",
    })
    
    # OBR-6: Requested Date/Time (all versions)
    profile.add_field_definition("OBR", 6, {
        "name": "Requested Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # OBR-7: Observation Date/Time (all versions)
    profile.add_field_definition("OBR", 7, {
        "name": "Observation Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # OBR-8: Observation End Date/Time (all versions)
    profile.add_field_definition("OBR", 8, {
        "name": "Observation End Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # OBR-9: Collection Volume (all versions)
    profile.add_field_definition("OBR", 9, {
        "name": "Collection Volume",
        "data_type": "CQ",
        "required": False,
    })
    
    # OBR-10: Collector Identifier (all versions)
    profile.add_field_definition("OBR", 10, {
        "name": "Collector Identifier",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-11: Specimen Action Code (all versions)
    profile.add_field_definition("OBR", 11, {
        "name": "Specimen Action Code",
        "data_type": "ID",
        "required": False,
        "table": "0065",
    })
    
    # OBR-12: Danger Code (all versions)
    profile.add_field_definition("OBR", 12, {
        "name": "Danger Code",
        "data_type": "CE",
        "required": False,
    })
    
    # OBR-13: Relevant Clinical Information (all versions)
    profile.add_field_definition("OBR", 13, {
        "name": "Relevant Clinical Information",
        "data_type": "CE",
        "required": False,
    })
    
    # OBR-14: Specimen Received Date/Time (all versions)
    profile.add_field_definition("OBR", 14, {
        "name": "Specimen Received Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # OBR-15: Specimen Source (all versions)
    profile.add_field_definition("OBR", 15, {
        "name": "Specimen Source",
        "data_type": "SPS",
        "required": False,
    })
    
    # OBR-16: Ordering Provider (all versions)
    profile.add_field_definition("OBR", 16, {
        "name": "Ordering Provider",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-17: Order Callback Phone Number (all versions)
    profile.add_field_definition("OBR", 17, {
        "name": "Order Callback Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-18: Placer Field 1 (all versions)
    profile.add_field_definition("OBR", 18, {
        "name": "Placer Field 1",
        "data_type": "ST",
        "required": False,
    })
    
    # OBR-19: Placer Field 2 (all versions)
    profile.add_field_definition("OBR", 19, {
        "name": "Placer Field 2",
        "data_type": "ST",
        "required": False,
    })
    
    # OBR-20: Filler Field 1 (all versions)
    profile.add_field_definition("OBR", 20, {
        "name": "Filler Field 1",
        "data_type": "ST",
        "required": False,
    })
    
    # OBR-21: Filler Field 2 (all versions)
    profile.add_field_definition("OBR", 21, {
        "name": "Filler Field 2",
        "data_type": "ST",
        "required": False,
    })
    
    # OBR-22: Results Rpt/Status Chng - Date/Time (all versions)
    profile.add_field_definition("OBR", 22, {
        "name": "Results Rpt/Status Chng - Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # OBR-23: Charge to Practice (all versions)
    profile.add_field_definition("OBR", 23, {
        "name": "Charge to Practice",
        "data_type": "MOC",
        "required": False,
    })
    
    # OBR-24: Diagnostic Serv Sect ID (all versions)
    profile.add_field_definition("OBR", 24, {
        "name": "Diagnostic Serv Sect ID",
        "data_type": "ID",
        "required": False,
        "table": "0074",
    })
    
    # OBR-25: Result Status (all versions)
    profile.add_field_definition("OBR", 25, {
        "name": "Result Status",
        "data_type": "ID",
        "required": False,
        "table": "0123",
    })
    
    # OBR-26: Parent Result (all versions)
    profile.add_field_definition("OBR", 26, {
        "name": "Parent Result",
        "data_type": "CE",
        "required": False,
    })
    
    # OBR-27: Quantity/Timing (all versions)
    profile.add_field_definition("OBR", 27, {
        "name": "Quantity/Timing",
        "data_type": "TQ",
        "required": False,
    })
    
    # OBR-28: Result Copies To (all versions)
    profile.add_field_definition("OBR", 28, {
        "name": "Result Copies To",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-29: Parent (all versions)
    profile.add_field_definition("OBR", 29, {
        "name": "Parent",
        "data_type": "EIP",
        "required": False,
    })
    
    # OBR-30: Transportation Mode (all versions)
    profile.add_field_definition("OBR", 30, {
        "name": "Transportation Mode",
        "data_type": "ID",
        "required": False,
        "table": "0124",
    })
    
    # OBR-31: Reason for Study (all versions)
    profile.add_field_definition("OBR", 31, {
        "name": "Reason for Study",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-32: Principal Result Interpreter (all versions)
    profile.add_field_definition("OBR", 32, {
        "name": "Principal Result Interpreter",
        "data_type": "NDL",
        "required": False,
    })
    
    # OBR-33: Assistant Result Interpreter (all versions)
    profile.add_field_definition("OBR", 33, {
        "name": "Assistant Result Interpreter",
        "data_type": "NDL",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-34: Technician (all versions)
    profile.add_field_definition("OBR", 34, {
        "name": "Technician",
        "data_type": "NDL",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-35: Transcriptionist (all versions)
    profile.add_field_definition("OBR", 35, {
        "name": "Transcriptionist",
        "data_type": "NDL",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-36: Scheduled Date/Time (all versions)
    profile.add_field_definition("OBR", 36, {
        "name": "Scheduled Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # OBR-37: Number of Sample Containers (all versions)
    profile.add_field_definition("OBR", 37, {
        "name": "Number of Sample Containers",
        "data_type": "NM",
        "required": False,
    })
    
    # OBR-38: Transport Logistics of Collected Sample (all versions)
    profile.add_field_definition("OBR", 38, {
        "name": "Transport Logistics of Collected Sample",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-39: Collector's Comment (all versions)
    profile.add_field_definition("OBR", 39, {
        "name": "Collector's Comment",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBR-40: Transport Arrangement Responsibility (all versions)
    profile.add_field_definition("OBR", 40, {
        "name": "Transport Arrangement Responsibility",
        "data_type": "CE",
        "required": False,
    })
    
    # OBR-41: Transport Arranged (all versions)
    profile.add_field_definition("OBR", 41, {
        "name": "Transport Arranged",
        "data_type": "ID",
        "required": False,
        "table": "0224",
    })
    
    # OBR-42: Escort Required (all versions)
    profile.add_field_definition("OBR", 42, {
        "name": "Escort Required",
        "data_type": "ID",
        "required": False,
        "table": "0225",
    })
    
    # OBR-43: Planned Patient Transport Comment (all versions)
    profile.add_field_definition("OBR", 43, {
        "name": "Planned Patient Transport Comment",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific OBR fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # OBR-44: Procedure Code (added in 2.5+)
        profile.add_field_definition("OBR", 44, {
            "name": "Procedure Code",
            "data_type": "CE",
            "required": False,
        })
        # OBR-45: Procedure Code Modifier (added in 2.5+)
        profile.add_field_definition("OBR", 45, {
            "name": "Procedure Code Modifier",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # OBR-46: Placer Supplemental Service Information (added in 2.5+)
        profile.add_field_definition("OBR", 46, {
            "name": "Placer Supplemental Service Information",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # OBR-47: Filler Supplemental Service Information (added in 2.5+)
        profile.add_field_definition("OBR", 47, {
            "name": "Filler Supplemental Service Information",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # OBR-48: Medically Necessary Duplicate Procedure Reason (added in 2.5+)
        profile.add_field_definition("OBR", 48, {
            "name": "Medically Necessary Duplicate Procedure Reason",
            "data_type": "CWE",
            "required": False,
        })
        # OBR-49: Result Handling (added in 2.5+)
        profile.add_field_definition("OBR", 49, {
            "name": "Result Handling",
            "data_type": "IS",
            "required": False,
            "table": "0507",
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # OBR-50: Parent Universal Service Identifier (added in 2.7+)
        profile.add_field_definition("OBR", 50, {
            "name": "Parent Universal Service Identifier",
            "data_type": "CWE",
            "required": False,
        })
    
    # OBX segment definition (Observation/Result)
    profile.add_segment_definition("OBX", {
        "name": "OBX",
        "description": "Observation/Result",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBX-1: Set ID - OBX (all versions)
    profile.add_field_definition("OBX", 1, {
        "name": "Set ID - OBX",
        "data_type": "SI",
        "required": False,
    })
    
    # OBX-2: Value Type (all versions)
    profile.add_field_definition("OBX", 2, {
        "name": "Value Type",
        "data_type": "ID",
        "required": True,
        "table": "0125",
    })
    
    # OBX-3: Observation Identifier (all versions)
    profile.add_field_definition("OBX", 3, {
        "name": "Observation Identifier",
        "data_type": "CE",
        "required": True,
    })
    
    # OBX-4: Observation Sub-ID (all versions)
    profile.add_field_definition("OBX", 4, {
        "name": "Observation Sub-ID",
        "data_type": "ST",
        "required": False,
    })
    
    # OBX-5: Observation Value (all versions)
    profile.add_field_definition("OBX", 5, {
        "name": "Observation Value",
        "data_type": "Varies",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBX-6: Units (all versions)
    profile.add_field_definition("OBX", 6, {
        "name": "Units",
        "data_type": "CE",
        "required": False,
    })
    
    # OBX-7: References Range (all versions)
    profile.add_field_definition("OBX", 7, {
        "name": "References Range",
        "data_type": "ST",
        "required": False,
    })
    
    # OBX-8: Interpretation Codes (all versions)
    profile.add_field_definition("OBX", 8, {
        "name": "Interpretation Codes",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBX-9: Probability (all versions)
    profile.add_field_definition("OBX", 9, {
        "name": "Probability",
        "data_type": "NM",
        "required": False,
    })
    
    # OBX-10: Nature of Abnormal Test (all versions)
    profile.add_field_definition("OBX", 10, {
        "name": "Nature of Abnormal Test",
        "data_type": "ID",
        "required": False,
        "table": "0080",
    })
    
    # OBX-11: Observe Result Status (all versions)
    profile.add_field_definition("OBX", 11, {
        "name": "Observe Result Status",
        "data_type": "ID",
        "required": True,
        "table": "0085",
    })
    
    # OBX-12: Date/Time of the Observation (all versions)
    profile.add_field_definition("OBX", 12, {
        "name": "Date/Time of the Observation",
        "data_type": "TS",
        "required": False,
    })
    
    # OBX-13: Producer's ID (all versions)
    profile.add_field_definition("OBX", 13, {
        "name": "Producer's ID",
        "data_type": "CE",
        "required": False,
    })
    
    # OBX-14: Responsible Observer (all versions)
    profile.add_field_definition("OBX", 14, {
        "name": "Responsible Observer",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBX-15: Observation Method (all versions)
    profile.add_field_definition("OBX", 15, {
        "name": "Observation Method",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBX-16: Equipment Instance Identifier (all versions)
    profile.add_field_definition("OBX", 16, {
        "name": "Equipment Instance Identifier",
        "data_type": "EI",
        "required": False,
        "max_repetitions": None,
    })
    
    # OBX-17: Date/Time of the Analysis (all versions)
    profile.add_field_definition("OBX", 17, {
        "name": "Date/Time of the Analysis",
        "data_type": "TS",
        "required": False,
    })
    
    # Version-specific OBX fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # OBX-18: Observation Site (added in 2.5+)
        profile.add_field_definition("OBX", 18, {
            "name": "Observation Site",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # OBX-19: Observation Instance Identifier (added in 2.5+)
        profile.add_field_definition("OBX", 19, {
            "name": "Observation Instance Identifier",
            "data_type": "EI",
            "required": False,
        })
        # OBX-20: Mood Code (added in 2.5+)
        profile.add_field_definition("OBX", 20, {
            "name": "Mood Code",
            "data_type": "CE",
            "required": False,
        })
        # OBX-21: Performing Organization Name (added in 2.5+)
        profile.add_field_definition("OBX", 21, {
            "name": "Performing Organization Name",
            "data_type": "XON",
            "required": False,
        })
        # OBX-22: Performing Organization Address (added in 2.5+)
        profile.add_field_definition("OBX", 22, {
            "name": "Performing Organization Address",
            "data_type": "XAD",
            "required": False,
        })
        # OBX-23: Performing Organization Medical Director (added in 2.5+)
        profile.add_field_definition("OBX", 23, {
            "name": "Performing Organization Medical Director",
            "data_type": "XCN",
            "required": False,
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # OBX-24: Patient Results Release Category (added in 2.7+)
        profile.add_field_definition("OBX", 24, {
            "name": "Patient Results Release Category",
            "data_type": "ID",
            "required": False,
            "table": "0493",
        })
        # OBX-25: Root Cause (added in 2.7+)
        profile.add_field_definition("OBX", 25, {
            "name": "Root Cause",
            "data_type": "CE",
            "required": False,
        })
    
    if version in ("2.8", "2.9"):
        # OBX-26: Local Process Control (added in 2.8+)
        profile.add_field_definition("OBX", 26, {
            "name": "Local Process Control",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # OBX-27: Observation Type (added in 2.8+)
        profile.add_field_definition("OBX", 27, {
            "name": "Observation Type",
            "data_type": "ID",
            "required": False,
            "table": "0494",
        })
        # OBX-28: Observation Sub-type (added in 2.8+)
        profile.add_field_definition("OBX", 28, {
            "name": "Observation Sub-type",
            "data_type": "ID",
            "required": False,
            "table": "0495",
        })
    
    if version == "2.9":
        # OBX-29: Observation Value Type (added in 2.9)
        profile.add_field_definition("OBX", 29, {
            "name": "Observation Value Type",
            "data_type": "ID",
            "required": False,
            "table": "0125",
        })
    
    # EVN segment definition (Event Type)
    profile.add_segment_definition("EVN", {
        "name": "EVN",
        "description": "Event Type",
        "required": False,
        "max_repetitions": 1,
    })
    
    # EVN-1: Event Type Code (all versions)
    profile.add_field_definition("EVN", 1, {
        "name": "Event Type Code",
        "data_type": "ID",
        "required": False,
        "table": "0003",
    })
    
    # EVN-2: Recorded Date/Time (all versions)
    profile.add_field_definition("EVN", 2, {
        "name": "Recorded Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # EVN-3: Date/Time Planned Event (all versions)
    profile.add_field_definition("EVN", 3, {
        "name": "Date/Time Planned Event",
        "data_type": "TS",
        "required": False,
    })
    
    # EVN-4: Event Reason Code (all versions)
    profile.add_field_definition("EVN", 4, {
        "name": "Event Reason Code",
        "data_type": "ID",
        "required": False,
        "table": "0062",
    })
    
    # EVN-5: Operator ID (all versions)
    profile.add_field_definition("EVN", 5, {
        "name": "Operator ID",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific EVN fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # EVN-6: Event Occurred (added in 2.5+)
        profile.add_field_definition("EVN", 6, {
            "name": "Event Occurred",
            "data_type": "TS",
            "required": False,
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # EVN-7: Event Facility (added in 2.7+)
        profile.add_field_definition("EVN", 7, {
            "name": "Event Facility",
            "data_type": "HD",
            "required": False,
        })
    
    # PV1 segment definition (Patient Visit)
    profile.add_segment_definition("PV1", {
        "name": "PV1",
        "description": "Patient Visit",
        "required": False,
        "max_repetitions": 1,
    })
    
    # PV1-1: Set ID - PV1 (all versions)
    profile.add_field_definition("PV1", 1, {
        "name": "Set ID - PV1",
        "data_type": "SI",
        "required": False,
    })
    
    # PV1-2: Patient Class (all versions)
    profile.add_field_definition("PV1", 2, {
        "name": "Patient Class",
        "data_type": "IS",
        "required": True,
        "table": "0004",
    })
    
    # PV1-3: Assigned Patient Location (all versions)
    profile.add_field_definition("PV1", 3, {
        "name": "Assigned Patient Location",
        "data_type": "PL",
        "required": False,
    })
    
    # PV1-4: Admission Type (all versions)
    profile.add_field_definition("PV1", 4, {
        "name": "Admission Type",
        "data_type": "IS",
        "required": False,
        "table": "0007",
    })
    
    # PV1-5: Preadmit Number (all versions)
    profile.add_field_definition("PV1", 5, {
        "name": "Preadmit Number",
        "data_type": "CX",
        "required": False,
    })
    
    # PV1-6: Prior Patient Location (all versions)
    profile.add_field_definition("PV1", 6, {
        "name": "Prior Patient Location",
        "data_type": "PL",
        "required": False,
    })
    
    # PV1-7: Attending Doctor (all versions)
    profile.add_field_definition("PV1", 7, {
        "name": "Attending Doctor",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-8: Referring Doctor (all versions)
    profile.add_field_definition("PV1", 8, {
        "name": "Referring Doctor",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-9: Consulting Doctor (all versions)
    profile.add_field_definition("PV1", 9, {
        "name": "Consulting Doctor",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-10: Hospital Service (all versions)
    profile.add_field_definition("PV1", 10, {
        "name": "Hospital Service",
        "data_type": "IS",
        "required": False,
        "table": "0069",
    })
    
    # PV1-11: Temporary Location (all versions)
    profile.add_field_definition("PV1", 11, {
        "name": "Temporary Location",
        "data_type": "PL",
        "required": False,
    })
    
    # PV1-12: Preadmit Test Indicator (all versions)
    profile.add_field_definition("PV1", 12, {
        "name": "Preadmit Test Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0087",
    })
    
    # PV1-13: Re-admission Indicator (all versions)
    profile.add_field_definition("PV1", 13, {
        "name": "Re-admission Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0092",
    })
    
    # PV1-14: Admit Source (all versions)
    profile.add_field_definition("PV1", 14, {
        "name": "Admit Source",
        "data_type": "IS",
        "required": False,
        "table": "0023",
    })
    
    # PV1-15: Ambulatory Status (all versions)
    profile.add_field_definition("PV1", 15, {
        "name": "Ambulatory Status",
        "data_type": "IS",
        "required": False,
        "table": "0009",
    })
    
    # PV1-16: VIP Indicator (all versions)
    profile.add_field_definition("PV1", 16, {
        "name": "VIP Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0099",
    })
    
    # PV1-17: Admitting Doctor (all versions)
    profile.add_field_definition("PV1", 17, {
        "name": "Admitting Doctor",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-18: Patient Type (all versions)
    profile.add_field_definition("PV1", 18, {
        "name": "Patient Type",
        "data_type": "IS",
        "required": False,
        "table": "0018",
    })
    
    # PV1-19: Visit Number (all versions)
    profile.add_field_definition("PV1", 19, {
        "name": "Visit Number",
        "data_type": "CX",
        "required": False,
    })
    
    # PV1-20: Financial Class (all versions)
    profile.add_field_definition("PV1", 20, {
        "name": "Financial Class",
        "data_type": "FC",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-21: Charge Price Indicator (all versions)
    profile.add_field_definition("PV1", 21, {
        "name": "Charge Price Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0032",
    })
    
    # PV1-22: Courtesy Code (all versions)
    profile.add_field_definition("PV1", 22, {
        "name": "Courtesy Code",
        "data_type": "IS",
        "required": False,
        "table": "0045",
    })
    
    # PV1-23: Credit Rating (all versions)
    profile.add_field_definition("PV1", 23, {
        "name": "Credit Rating",
        "data_type": "IS",
        "required": False,
        "table": "0046",
    })
    
    # PV1-24: Contract Code (all versions)
    profile.add_field_definition("PV1", 24, {
        "name": "Contract Code",
        "data_type": "IS",
        "required": False,
        "table": "0044",
    })
    
    # PV1-25: Contract Effective Date (all versions)
    profile.add_field_definition("PV1", 25, {
        "name": "Contract Effective Date",
        "data_type": "DT",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-26: Contract Amount (all versions)
    profile.add_field_definition("PV1", 26, {
        "name": "Contract Amount",
        "data_type": "NM",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-27: Contract Period (all versions)
    profile.add_field_definition("PV1", 27, {
        "name": "Contract Period",
        "data_type": "NM",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV1-28: Interest Code (all versions)
    profile.add_field_definition("PV1", 28, {
        "name": "Interest Code",
        "data_type": "IS",
        "required": False,
        "table": "0073",
    })
    
    # PV1-29: Transfer to Bad Debt Code (all versions)
    profile.add_field_definition("PV1", 29, {
        "name": "Transfer to Bad Debt Code",
        "data_type": "IS",
        "required": False,
        "table": "0110",
    })
    
    # PV1-30: Transfer to Bad Debt Date (all versions)
    profile.add_field_definition("PV1", 30, {
        "name": "Transfer to Bad Debt Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV1-31: Bad Debt Agency Code (all versions)
    profile.add_field_definition("PV1", 31, {
        "name": "Bad Debt Agency Code",
        "data_type": "IS",
        "required": False,
        "table": "0021",
    })
    
    # PV1-32: Bad Debt Transfer Amount (all versions)
    profile.add_field_definition("PV1", 32, {
        "name": "Bad Debt Transfer Amount",
        "data_type": "NM",
        "required": False,
    })
    
    # PV1-33: Bad Debt Recovery Amount (all versions)
    profile.add_field_definition("PV1", 33, {
        "name": "Bad Debt Recovery Amount",
        "data_type": "NM",
        "required": False,
    })
    
    # PV1-34: Delete Account Indicator (all versions)
    profile.add_field_definition("PV1", 34, {
        "name": "Delete Account Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0111",
    })
    
    # PV1-35: Delete Account Date (all versions)
    profile.add_field_definition("PV1", 35, {
        "name": "Delete Account Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV1-36: Discharge Disposition (all versions)
    profile.add_field_definition("PV1", 36, {
        "name": "Discharge Disposition",
        "data_type": "IS",
        "required": False,
        "table": "0112",
    })
    
    # PV1-37: Discharged to Location (all versions)
    profile.add_field_definition("PV1", 37, {
        "name": "Discharged to Location",
        "data_type": "DLD",
        "required": False,
    })
    
    # PV1-38: Diet Type (all versions)
    profile.add_field_definition("PV1", 38, {
        "name": "Diet Type",
        "data_type": "CE",
        "required": False,
    })
    
    # PV1-39: Servicing Facility (all versions)
    profile.add_field_definition("PV1", 39, {
        "name": "Servicing Facility",
        "data_type": "IS",
        "required": False,
    })
    
    # PV1-40: Bed Status (all versions)
    profile.add_field_definition("PV1", 40, {
        "name": "Bed Status",
        "data_type": "IS",
        "required": False,
        "table": "0116",
    })
    
    # PV1-41: Account Status (all versions)
    profile.add_field_definition("PV1", 41, {
        "name": "Account Status",
        "data_type": "IS",
        "required": False,
        "table": "0117",
    })
    
    # PV1-42: Pending Location (all versions)
    profile.add_field_definition("PV1", 42, {
        "name": "Pending Location",
        "data_type": "PL",
        "required": False,
    })
    
    # PV1-43: Prior Temporary Location (all versions)
    profile.add_field_definition("PV1", 43, {
        "name": "Prior Temporary Location",
        "data_type": "PL",
        "required": False,
    })
    
    # PV1-44: Admit Date/Time (all versions)
    profile.add_field_definition("PV1", 44, {
        "name": "Admit Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # PV1-45: Discharge Date/Time (all versions)
    profile.add_field_definition("PV1", 45, {
        "name": "Discharge Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # PV1-46: Current Patient Balance (all versions)
    profile.add_field_definition("PV1", 46, {
        "name": "Current Patient Balance",
        "data_type": "NM",
        "required": False,
    })
    
    # PV1-47: Total Charges (all versions)
    profile.add_field_definition("PV1", 47, {
        "name": "Total Charges",
        "data_type": "NM",
        "required": False,
    })
    
    # PV1-48: Total Adjustments (all versions)
    profile.add_field_definition("PV1", 48, {
        "name": "Total Adjustments",
        "data_type": "NM",
        "required": False,
    })
    
    # PV1-49: Total Payments (all versions)
    profile.add_field_definition("PV1", 49, {
        "name": "Total Payments",
        "data_type": "NM",
        "required": False,
    })
    
    # PV1-50: Alternate Visit ID (all versions)
    profile.add_field_definition("PV1", 50, {
        "name": "Alternate Visit ID",
        "data_type": "CX",
        "required": False,
    })
    
    # Version-specific PV1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # PV1-51: Visit Indicator (added in 2.5+)
        profile.add_field_definition("PV1", 51, {
            "name": "Visit Indicator",
            "data_type": "IS",
            "required": False,
            "table": "0326",
        })
        # PV1-52: Other Healthcare Provider (added in 2.5+)
        profile.add_field_definition("PV1", 52, {
            "name": "Other Healthcare Provider",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
    
    # PV2 segment definition (Patient Visit - Additional Info)
    profile.add_segment_definition("PV2", {
        "name": "PV2",
        "description": "Patient Visit - Additional Info",
        "required": False,
        "max_repetitions": 1,
    })
    
    # PV2-1: Prior Pending Location (all versions)
    profile.add_field_definition("PV2", 1, {
        "name": "Prior Pending Location",
        "data_type": "PL",
        "required": False,
    })
    
    # PV2-2: Accommodation Code (all versions)
    profile.add_field_definition("PV2", 2, {
        "name": "Accommodation Code",
        "data_type": "CE",
        "required": False,
        "table": "0032",  # Accommodation Code table
    })
    
    # PV2-3: Admit Reason (all versions)
    profile.add_field_definition("PV2", 3, {
        "name": "Admit Reason",
        "data_type": "CE",
        "required": False,
    })
    
    # PV2-4: Transfer Reason (all versions)
    profile.add_field_definition("PV2", 4, {
        "name": "Transfer Reason",
        "data_type": "CE",
        "required": False,
    })
    
    # PV2-5: Patient Valuables (all versions)
    profile.add_field_definition("PV2", 5, {
        "name": "Patient Valuables",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV2-6: Patient Valuables Location (all versions)
    profile.add_field_definition("PV2", 6, {
        "name": "Patient Valuables Location",
        "data_type": "ST",
        "required": False,
    })
    
    # PV2-7: Visit User Code (all versions)
    profile.add_field_definition("PV2", 7, {
        "name": "Visit User Code",
        "data_type": "IS",
        "required": False,
        "table": "0130",  # Visit User Code table
    })
    
    # PV2-8: Expected Admit Date/Time (all versions)
    profile.add_field_definition("PV2", 8, {
        "name": "Expected Admit Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # PV2-9: Expected Discharge Date/Time (all versions)
    profile.add_field_definition("PV2", 9, {
        "name": "Expected Discharge Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # PV2-10: Estimated Length of Stay (all versions)
    profile.add_field_definition("PV2", 10, {
        "name": "Estimated Length of Stay",
        "data_type": "NM",
        "required": False,
    })
    
    # PV2-11: Actual Length of Stay (all versions)
    profile.add_field_definition("PV2", 11, {
        "name": "Actual Length of Stay",
        "data_type": "NM",
        "required": False,
    })
    
    # PV2-12: Visit Description (all versions)
    profile.add_field_definition("PV2", 12, {
        "name": "Visit Description",
        "data_type": "ST",
        "required": False,
    })
    
    # PV2-13: Referral Source Code (all versions)
    profile.add_field_definition("PV2", 13, {
        "name": "Referral Source Code",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV2-14: Previous Service Date (all versions)
    profile.add_field_definition("PV2", 14, {
        "name": "Previous Service Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV2-15: Employment Illness Related Indicator (all versions)
    profile.add_field_definition("PV2", 15, {
        "name": "Employment Illness Related Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-16: Purge Status Code (all versions)
    profile.add_field_definition("PV2", 16, {
        "name": "Purge Status Code",
        "data_type": "IS",
        "required": False,
        "table": "0213",  # Purge Status Code table
    })
    
    # PV2-17: Purge Status Date (all versions)
    profile.add_field_definition("PV2", 17, {
        "name": "Purge Status Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV2-18: Special Program Code (all versions)
    profile.add_field_definition("PV2", 18, {
        "name": "Special Program Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV2-19: Retention Indicator (all versions)
    profile.add_field_definition("PV2", 19, {
        "name": "Retention Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-20: Expected Number of Insurance Plans (all versions)
    profile.add_field_definition("PV2", 20, {
        "name": "Expected Number of Insurance Plans",
        "data_type": "NM",
        "required": False,
    })
    
    # PV2-21: Visit Publicity Code (all versions)
    profile.add_field_definition("PV2", 21, {
        "name": "Visit Publicity Code",
        "data_type": "CE",
        "required": False,
        "table": "0215",  # Visit Publicity Code table
    })
    
    # PV2-22: Visit Protection Indicator (all versions)
    profile.add_field_definition("PV2", 22, {
        "name": "Visit Protection Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-23: Clinic Organization Name (all versions)
    profile.add_field_definition("PV2", 23, {
        "name": "Clinic Organization Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV2-24: Patient Status Code (all versions)
    profile.add_field_definition("PV2", 24, {
        "name": "Patient Status Code",
        "data_type": "IS",
        "required": False,
        "table": "0216",  # Patient Status Code table
    })
    
    # PV2-25: Visit Priority Code (all versions)
    profile.add_field_definition("PV2", 25, {
        "name": "Visit Priority Code",
        "data_type": "IS",
        "required": False,
        "table": "0217",  # Visit Priority Code table
    })
    
    # PV2-26: Previous Treatment Date (all versions)
    profile.add_field_definition("PV2", 26, {
        "name": "Previous Treatment Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV2-27: Expected Discharge Disposition (all versions)
    profile.add_field_definition("PV2", 27, {
        "name": "Expected Discharge Disposition",
        "data_type": "IS",
        "required": False,
        "table": "0112",  # Discharge Disposition table
    })
    
    # PV2-28: Signature on File Date (all versions)
    profile.add_field_definition("PV2", 28, {
        "name": "Signature on File Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV2-29: First Similar Illness Date (all versions)
    profile.add_field_definition("PV2", 29, {
        "name": "First Similar Illness Date",
        "data_type": "DT",
        "required": False,
    })
    
    # PV2-30: Patient Charge Adjustment Code (all versions)
    profile.add_field_definition("PV2", 30, {
        "name": "Patient Charge Adjustment Code",
        "data_type": "CE",
        "required": False,
        "table": "0218",  # Patient Charge Adjustment Code table
    })
    
    # PV2-31: Recurring Service Code (all versions)
    profile.add_field_definition("PV2", 31, {
        "name": "Recurring Service Code",
        "data_type": "CE",
        "required": False,
        "table": "0014",  # Recurring Service Code table
    })
    
    # PV2-32: Billing Media Code (all versions)
    profile.add_field_definition("PV2", 32, {
        "name": "Billing Media Code",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table (used for billing media)
    })
    
    # PV2-33: Expected Surgery Date and Time (all versions)
    profile.add_field_definition("PV2", 33, {
        "name": "Expected Surgery Date and Time",
        "data_type": "TS",
        "required": False,
    })
    
    # PV2-34: Military Partnership Code (all versions)
    profile.add_field_definition("PV2", 34, {
        "name": "Military Partnership Code",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-35: Military Non-Availability Code (all versions)
    profile.add_field_definition("PV2", 35, {
        "name": "Military Non-Availability Code",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-36: Newborn Baby Indicator (all versions)
    profile.add_field_definition("PV2", 36, {
        "name": "Newborn Baby Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-37: Baby Detained Indicator (all versions)
    profile.add_field_definition("PV2", 37, {
        "name": "Baby Detained Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PV2-38: Mode of Arrival Code (all versions)
    profile.add_field_definition("PV2", 38, {
        "name": "Mode of Arrival Code",
        "data_type": "CE",
        "required": False,
        "table": "0430",  # Mode of Arrival Code table
    })
    
    # PV2-39: Recreational Drug Use Code (all versions)
    profile.add_field_definition("PV2", 39, {
        "name": "Recreational Drug Use Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # PV2-40: Admission Level of Care Code (all versions)
    profile.add_field_definition("PV2", 40, {
        "name": "Admission Level of Care Code",
        "data_type": "CE",
        "required": False,
        "table": "0432",  # Admission Level of Care Code table
    })
    
    # Version-specific PV2 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # PV2-41: Precaution Code (added in 2.5+)
        profile.add_field_definition("PV2", 41, {
            "name": "Precaution Code",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PV2-42: Patient Condition Code (added in 2.5+)
        profile.add_field_definition("PV2", 42, {
            "name": "Patient Condition Code",
            "data_type": "IS",
            "required": False,
            "table": "0433",  # Patient Condition Code table
        })
        # PV2-43: Living Will Code (added in 2.5+)
        profile.add_field_definition("PV2", 43, {
            "name": "Living Will Code",
            "data_type": "IS",
            "required": False,
            "table": "0315",  # Living Will Code table
        })
        # PV2-44: Organ Donor Code (added in 2.5+)
        profile.add_field_definition("PV2", 44, {
            "name": "Organ Donor Code",
            "data_type": "IS",
            "required": False,
            "table": "0316",  # Organ Donor Code table
        })
        # PV2-45: Advance Directive Code (added in 2.5+)
        profile.add_field_definition("PV2", 45, {
            "name": "Advance Directive Code",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        # PV2-46: Patient Status Effective Date (added in 2.5+)
        profile.add_field_definition("PV2", 46, {
            "name": "Patient Status Effective Date",
            "data_type": "DT",
            "required": False,
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # PV2-47: Expected LOA Return Date/Time (added in 2.7+)
        profile.add_field_definition("PV2", 47, {
            "name": "Expected LOA Return Date/Time",
            "data_type": "TS",
            "required": False,
        })
        # PV2-48: Expected Pre-admission Testing Date/Time (added in 2.7+)
        profile.add_field_definition("PV2", 48, {
            "name": "Expected Pre-admission Testing Date/Time",
            "data_type": "TS",
            "required": False,
        })
        # PV2-49: Notify Clergy Code (added in 2.7+)
        profile.add_field_definition("PV2", 49, {
            "name": "Notify Clergy Code",
            "data_type": "IS",
            "required": False,
            "table": "0532",  # Notify Clergy Code table
        })
        # PV2-50: Advance Directive Last Verified Date (added in 2.7+)
        profile.add_field_definition("PV2", 50, {
            "name": "Advance Directive Last Verified Date",
            "data_type": "DT",
            "required": False,
        })
    
    # AL1 segment definition (Patient Allergy Information)
    profile.add_segment_definition("AL1", {
        "name": "AL1",
        "description": "Patient Allergy Information",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # AL1-1: Set ID - AL1 (all versions)
    profile.add_field_definition("AL1", 1, {
        "name": "Set ID - AL1",
        "data_type": "SI",
        "required": False,
    })
    
    # AL1-2: Allergen Type Code (all versions)
    profile.add_field_definition("AL1", 2, {
        "name": "Allergen Type Code",
        "data_type": "CE",
        "required": False,
        "table": "0127",  # Allergen Type Code table
    })
    
    # AL1-3: Allergen Code/Mnemonic/Description (all versions)
    profile.add_field_definition("AL1", 3, {
        "name": "Allergen Code/Mnemonic/Description",
        "data_type": "CE",
        "required": False,
    })
    
    # AL1-4: Allergy Severity Code (all versions)
    profile.add_field_definition("AL1", 4, {
        "name": "Allergy Severity Code",
        "data_type": "CE",
        "required": False,
        "table": "0128",  # Allergy Severity Code table
    })
    
    # AL1-5: Allergy Reaction Code (all versions)
    profile.add_field_definition("AL1", 5, {
        "name": "Allergy Reaction Code",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,  # Can have multiple reactions
    })
    
    # AL1-6: Identification Date (all versions)
    profile.add_field_definition("AL1", 6, {
        "name": "Identification Date",
        "data_type": "DT",
        "required": False,
    })
    
    # DG1 segment definition (Diagnosis)
    profile.add_segment_definition("DG1", {
        "name": "DG1",
        "description": "Diagnosis",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # DG1-1: Set ID - DG1 (all versions)
    profile.add_field_definition("DG1", 1, {
        "name": "Set ID - DG1",
        "data_type": "SI",
        "required": False,
    })
    
    # DG1-2: Diagnosis Coding Method (all versions)
    profile.add_field_definition("DG1", 2, {
        "name": "Diagnosis Coding Method",
        "data_type": "ID",
        "required": False,
        "table": "0053",  # Diagnosis Coding Method table
    })
    
    # DG1-3: Diagnosis Code - DG1 (all versions)
    profile.add_field_definition("DG1", 3, {
        "name": "Diagnosis Code - DG1",
        "data_type": "CE",
        "required": False,
        "table": "0051",  # Diagnosis Type table
    })
    
    # DG1-4: Diagnosis Description (all versions)
    profile.add_field_definition("DG1", 4, {
        "name": "Diagnosis Description",
        "data_type": "ST",
        "required": False,
    })
    
    # DG1-5: Diagnosis Date/Time (all versions)
    profile.add_field_definition("DG1", 5, {
        "name": "Diagnosis Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # DG1-6: Diagnosis Type (all versions)
    profile.add_field_definition("DG1", 6, {
        "name": "Diagnosis Type",
        "data_type": "IS",
        "required": False,
        "table": "0052",  # Diagnosis Type table
    })
    
    # DG1-7: Major Diagnostic Category (all versions)
    profile.add_field_definition("DG1", 7, {
        "name": "Major Diagnostic Category",
        "data_type": "CE",
        "required": False,
        "table": "0118",  # Major Diagnostic Category table
    })
    
    # DG1-8: Diagnostic Related Group (all versions)
    profile.add_field_definition("DG1", 8, {
        "name": "Diagnostic Related Group",
        "data_type": "CE",
        "required": False,
        "table": "0119",  # Diagnostic Related Group table
    })
    
    # DG1-9: DRG Approval Indicator (all versions)
    profile.add_field_definition("DG1", 9, {
        "name": "DRG Approval Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # DG1-10: DRG Grouper Review Code (all versions)
    profile.add_field_definition("DG1", 10, {
        "name": "DRG Grouper Review Code",
        "data_type": "IS",
        "required": False,
        "table": "0055",  # DRG Grouper Review Code table
    })
    
    # DG1-11: Outlier Type (all versions)
    profile.add_field_definition("DG1", 11, {
        "name": "Outlier Type",
        "data_type": "CE",
        "required": False,
        "table": "0083",  # Outlier Type table
    })
    
    # DG1-12: Outlier Days (all versions)
    profile.add_field_definition("DG1", 12, {
        "name": "Outlier Days",
        "data_type": "NM",
        "required": False,
    })
    
    # DG1-13: Outlier Cost (all versions)
    profile.add_field_definition("DG1", 13, {
        "name": "Outlier Cost",
        "data_type": "CP",
        "required": False,
    })
    
    # DG1-14: Grouper Version And Type (all versions)
    profile.add_field_definition("DG1", 14, {
        "name": "Grouper Version And Type",
        "data_type": "ST",
        "required": False,
    })
    
    # Version-specific DG1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # DG1-15: Diagnosis Priority (added in 2.5+)
        profile.add_field_definition("DG1", 15, {
            "name": "Diagnosis Priority",
            "data_type": "ID",
            "required": False,
            "table": "0359",  # Diagnosis Priority table
        })
        # DG1-16: Diagnosing Clinician (added in 2.5+)
        profile.add_field_definition("DG1", 16, {
            "name": "Diagnosing Clinician",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
        # DG1-17: Diagnosis Classification (added in 2.5+)
        profile.add_field_definition("DG1", 17, {
            "name": "Diagnosis Classification",
            "data_type": "IS",
            "required": False,
            "table": "0228",  # Diagnosis Classification table
        })
        # DG1-18: Confidential Indicator (added in 2.5+)
        profile.add_field_definition("DG1", 18, {
            "name": "Confidential Indicator",
            "data_type": "ID",
            "required": False,
            "table": "0136",  # Yes/No Indicator table
        })
        # DG1-19: Attestation Date/Time (added in 2.5+)
        profile.add_field_definition("DG1", 19, {
            "name": "Attestation Date/Time",
            "data_type": "TS",
            "required": False,
        })
        # DG1-20: Diagnosis Identifier (added in 2.5+)
        profile.add_field_definition("DG1", 20, {
            "name": "Diagnosis Identifier",
            "data_type": "EI",
            "required": False,
        })
        # DG1-21: Diagnosis Action Code (added in 2.5+)
        profile.add_field_definition("DG1", 21, {
            "name": "Diagnosis Action Code",
            "data_type": "ID",
            "required": False,
            "table": "0206",  # Segment Action Code table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # DG1-22: Parent Diagnosis (added in 2.7+)
        profile.add_field_definition("DG1", 22, {
            "name": "Parent Diagnosis",
            "data_type": "EI",
            "required": False,
        })
        # DG1-23: DRG CCL Value Code (added in 2.7+)
        profile.add_field_definition("DG1", 23, {
            "name": "DRG CCL Value Code",
            "data_type": "CE",
            "required": False,
        })
        # DG1-24: DRG Grouping Usage (added in 2.7+)
        profile.add_field_definition("DG1", 24, {
            "name": "DRG Grouping Usage",
            "data_type": "ID",
            "required": False,
            "table": "0136",  # Yes/No Indicator table
        })
        # DG1-25: DRG Diagnosis Determination Status (added in 2.7+)
        profile.add_field_definition("DG1", 25, {
            "name": "DRG Diagnosis Determination Status",
            "data_type": "CE",
            "required": False,
        })
        # DG1-26: Present On Admission (POA) Indicator (added in 2.7+)
        profile.add_field_definition("DG1", 26, {
            "name": "Present On Admission (POA) Indicator",
            "data_type": "IS",
            "required": False,
            "table": "0895",  # Present On Admission (POA) Indicator table
        })
    
    # PR1 segment definition (Procedures)
    profile.add_segment_definition("PR1", {
        "name": "PR1",
        "description": "Procedures",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # PR1-1: Set ID - PR1 (all versions)
    profile.add_field_definition("PR1", 1, {
        "name": "Set ID - PR1",
        "data_type": "SI",
        "required": False,
    })
    
    # PR1-2: Procedure Coding Method (all versions)
    profile.add_field_definition("PR1", 2, {
        "name": "Procedure Coding Method",
        "data_type": "ID",
        "required": False,
        "table": "0089",  # Procedure Coding Method table
    })
    
    # PR1-3: Procedure Code (all versions)
    profile.add_field_definition("PR1", 3, {
        "name": "Procedure Code",
        "data_type": "CE",
        "required": False,
        "table": "0088",  # Procedure Code table
    })
    
    # PR1-4: Procedure Description (all versions)
    profile.add_field_definition("PR1", 4, {
        "name": "Procedure Description",
        "data_type": "ST",
        "required": False,
    })
    
    # PR1-5: Procedure Date/Time (all versions)
    profile.add_field_definition("PR1", 5, {
        "name": "Procedure Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # PR1-6: Procedure Functional Type (all versions)
    profile.add_field_definition("PR1", 6, {
        "name": "Procedure Functional Type",
        "data_type": "IS",
        "required": False,
        "table": "0230",  # Procedure Functional Type table
    })
    
    # PR1-7: Procedure Minutes (all versions)
    profile.add_field_definition("PR1", 7, {
        "name": "Procedure Minutes",
        "data_type": "NM",
        "required": False,
    })
    
    # PR1-8: Anesthesiologist (all versions)
    profile.add_field_definition("PR1", 8, {
        "name": "Anesthesiologist",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PR1-9: Anesthesia Code (all versions)
    profile.add_field_definition("PR1", 9, {
        "name": "Anesthesia Code",
        "data_type": "IS",
        "required": False,
        "table": "0019",  # Anesthesia Code table
    })
    
    # PR1-10: Anesthesia Minutes (all versions)
    profile.add_field_definition("PR1", 10, {
        "name": "Anesthesia Minutes",
        "data_type": "NM",
        "required": False,
    })
    
    # PR1-11: Surgeon (all versions)
    profile.add_field_definition("PR1", 11, {
        "name": "Surgeon",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PR1-12: Procedure Practitioner (all versions)
    profile.add_field_definition("PR1", 12, {
        "name": "Procedure Practitioner",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PR1-13: Consent Code (all versions)
    profile.add_field_definition("PR1", 13, {
        "name": "Consent Code",
        "data_type": "CE",
        "required": False,
        "table": "0059",  # Consent Code table
    })
    
    # PR1-14: Procedure Priority (all versions)
    profile.add_field_definition("PR1", 14, {
        "name": "Procedure Priority",
        "data_type": "NM",
        "required": False,
    })
    
    # PR1-15: Associated Diagnosis Code (all versions)
    profile.add_field_definition("PR1", 15, {
        "name": "Associated Diagnosis Code",
        "data_type": "CE",
        "required": False,
        "table": "0051",  # Diagnosis Type table
    })
    
    # Version-specific PR1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # PR1-16: Procedure Code Modifier (added in 2.5+)
        profile.add_field_definition("PR1", 16, {
            "name": "Procedure Code Modifier",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
            "table": "0340",  # Procedure Code Modifier table
        })
        # PR1-17: Procedure DRG Type (added in 2.5+)
        profile.add_field_definition("PR1", 17, {
            "name": "Procedure DRG Type",
            "data_type": "CE",
            "required": False,
            "table": "0416",  # Procedure DRG Type table
        })
        # PR1-18: Tissue Type Code (added in 2.5+)
        profile.add_field_definition("PR1", 18, {
            "name": "Tissue Type Code",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
            "table": "0417",  # Tissue Type Code table
        })
        # PR1-19: Procedure Identifier (added in 2.5+)
        profile.add_field_definition("PR1", 19, {
            "name": "Procedure Identifier",
            "data_type": "EI",
            "required": False,
        })
        # PR1-20: Procedure Action Code (added in 2.5+)
        profile.add_field_definition("PR1", 20, {
            "name": "Procedure Action Code",
            "data_type": "ID",
            "required": False,
            "table": "0206",  # Segment Action Code table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # PR1-21: DRG Procedure Determination Status (added in 2.7+)
        profile.add_field_definition("PR1", 21, {
            "name": "DRG Procedure Determination Status",
            "data_type": "CE",
            "required": False,
        })
        # PR1-22: DRG Procedure Relevance (added in 2.7+)
        profile.add_field_definition("PR1", 22, {
            "name": "DRG Procedure Relevance",
            "data_type": "ID",
            "required": False,
            "table": "0136",  # Yes/No Indicator table
        })
    
    # NK1 segment definition (Next of Kin / Associated Parties)
    profile.add_segment_definition("NK1", {
        "name": "NK1",
        "description": "Next of Kin / Associated Parties",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # NK1-1: Set ID - NK1 (all versions)
    profile.add_field_definition("NK1", 1, {
        "name": "Set ID - NK1",
        "data_type": "SI",
        "required": False,
    })
    
    # NK1-2: Name (all versions)
    profile.add_field_definition("NK1", 2, {
        "name": "Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-3: Relationship (all versions)
    profile.add_field_definition("NK1", 3, {
        "name": "Relationship",
        "data_type": "CE",
        "required": False,
        "table": "0063",  # Relationship table
    })
    
    # NK1-4: Address (all versions)
    profile.add_field_definition("NK1", 4, {
        "name": "Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-5: Phone Number (all versions)
    profile.add_field_definition("NK1", 5, {
        "name": "Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-6: Business Phone Number (all versions)
    profile.add_field_definition("NK1", 6, {
        "name": "Business Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-7: Contact Role (all versions)
    profile.add_field_definition("NK1", 7, {
        "name": "Contact Role",
        "data_type": "CE",
        "required": False,
        "table": "0131",  # Contact Role table
    })
    
    # NK1-8: Start Date (all versions)
    profile.add_field_definition("NK1", 8, {
        "name": "Start Date",
        "data_type": "DT",
        "required": False,
    })
    
    # NK1-9: End Date (all versions)
    profile.add_field_definition("NK1", 9, {
        "name": "End Date",
        "data_type": "DT",
        "required": False,
    })
    
    # NK1-10: Next of Kin / Associated Parties Job Title (all versions)
    profile.add_field_definition("NK1", 10, {
        "name": "Next of Kin / Associated Parties Job Title",
        "data_type": "ST",
        "required": False,
    })
    
    # NK1-11: Next of Kin / Associated Parties Job Code/Class (all versions)
    profile.add_field_definition("NK1", 11, {
        "name": "Next of Kin / Associated Parties Job Code/Class",
        "data_type": "JCC",
        "required": False,
    })
    
    # NK1-12: Next of Kin / Associated Parties Employee Number (all versions)
    profile.add_field_definition("NK1", 12, {
        "name": "Next of Kin / Associated Parties Employee Number",
        "data_type": "CX",
        "required": False,
    })
    
    # NK1-13: Organization Name - NK1 (all versions)
    profile.add_field_definition("NK1", 13, {
        "name": "Organization Name - NK1",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-14: Marital Status (all versions)
    profile.add_field_definition("NK1", 14, {
        "name": "Marital Status",
        "data_type": "CE",
        "required": False,
        "table": "0002",  # Marital Status table
    })
    
    # NK1-15: Administrative Sex (all versions)
    profile.add_field_definition("NK1", 15, {
        "name": "Administrative Sex",
        "data_type": "IS",
        "required": False,
        "table": "0001",  # Administrative Sex table
    })
    
    # NK1-16: Date/Time of Birth (all versions)
    profile.add_field_definition("NK1", 16, {
        "name": "Date/Time of Birth",
        "data_type": "TS",
        "required": False,
    })
    
    # NK1-17: Living Dependency (all versions)
    profile.add_field_definition("NK1", 17, {
        "name": "Living Dependency",
        "data_type": "IS",
        "required": False,
        "max_repetitions": None,
        "table": "0223",  # Living Dependency table
    })
    
    # NK1-18: Ambulatory Status (all versions)
    profile.add_field_definition("NK1", 18, {
        "name": "Ambulatory Status",
        "data_type": "IS",
        "required": False,
        "max_repetitions": None,
        "table": "0009",  # Ambulatory Status table
    })
    
    # NK1-19: Citizenship (all versions)
    profile.add_field_definition("NK1", 19, {
        "name": "Citizenship",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
        "table": "0171",  # Citizenship table
    })
    
    # NK1-20: Primary Language (all versions)
    profile.add_field_definition("NK1", 20, {
        "name": "Primary Language",
        "data_type": "CE",
        "required": False,
        "table": "0296",  # Primary Language table
    })
    
    # NK1-21: Living Arrangement (all versions)
    profile.add_field_definition("NK1", 21, {
        "name": "Living Arrangement",
        "data_type": "IS",
        "required": False,
        "table": "0220",  # Living Arrangement table
    })
    
    # NK1-22: Publicity Code (all versions)
    profile.add_field_definition("NK1", 22, {
        "name": "Publicity Code",
        "data_type": "CE",
        "required": False,
        "table": "0215",  # Publicity Code table
    })
    
    # NK1-23: Protection Indicator (all versions)
    profile.add_field_definition("NK1", 23, {
        "name": "Protection Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # NK1-24: Student Indicator (all versions)
    profile.add_field_definition("NK1", 24, {
        "name": "Student Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0231",  # Student Indicator table
    })
    
    # NK1-25: Religion (all versions)
    profile.add_field_definition("NK1", 25, {
        "name": "Religion",
        "data_type": "CE",
        "required": False,
        "table": "0006",  # Religion table
    })
    
    # NK1-26: Mother's Maiden Name (all versions)
    profile.add_field_definition("NK1", 26, {
        "name": "Mother's Maiden Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-27: Nationality (all versions)
    profile.add_field_definition("NK1", 27, {
        "name": "Nationality",
        "data_type": "CE",
        "required": False,
        "table": "0212",  # Nationality table
    })
    
    # NK1-28: Ethnic Group (all versions)
    profile.add_field_definition("NK1", 28, {
        "name": "Ethnic Group",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
        "table": "0189",  # Ethnic Group table
    })
    
    # NK1-29: Contact Reason (all versions)
    profile.add_field_definition("NK1", 29, {
        "name": "Contact Reason",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
        "table": "0022",  # Contact Reason table
    })
    
    # NK1-30: Contact Person's Name (all versions)
    profile.add_field_definition("NK1", 30, {
        "name": "Contact Person's Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-31: Contact Person's Telephone Number (all versions)
    profile.add_field_definition("NK1", 31, {
        "name": "Contact Person's Telephone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # NK1-32: Contact Person's Address (all versions)
    profile.add_field_definition("NK1", 32, {
        "name": "Contact Person's Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific NK1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # NK1-33: Next of Kin/Associated Party's Identifiers (added in 2.5+)
        profile.add_field_definition("NK1", 33, {
            "name": "Next of Kin/Associated Party's Identifiers",
            "data_type": "CX",
            "required": False,
            "max_repetitions": None,
        })
        # NK1-34: Job Status (added in 2.5+)
        profile.add_field_definition("NK1", 34, {
            "name": "Job Status",
            "data_type": "IS",
            "required": False,
            "table": "0311",  # Job Status table
        })
        # NK1-35: Race (added in 2.5+)
        profile.add_field_definition("NK1", 35, {
            "name": "Race",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
            "table": "0005",  # Race table
        })
        # NK1-36: Handicap (added in 2.5+)
        profile.add_field_definition("NK1", 36, {
            "name": "Handicap",
            "data_type": "IS",
            "required": False,
            "table": "0295",  # Handicap table
        })
        # NK1-37: Contact Person Social Security Number (added in 2.5+)
        profile.add_field_definition("NK1", 37, {
            "name": "Contact Person Social Security Number",
            "data_type": "ST",
            "required": False,
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # NK1-38: Next of Kin Birth Place (added in 2.7+)
        profile.add_field_definition("NK1", 38, {
            "name": "Next of Kin Birth Place",
            "data_type": "ST",
            "required": False,
        })
        # NK1-39: VIP Indicator (added in 2.7+)
        profile.add_field_definition("NK1", 39, {
            "name": "VIP Indicator",
            "data_type": "IS",
            "required": False,
            "table": "0099",  # VIP Indicator table
        })
    
    # ORC segment definition (Common Order)
    profile.add_segment_definition("ORC", {
        "name": "ORC",
        "description": "Common Order",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # ORC-1: Order Control (all versions)
    profile.add_field_definition("ORC", 1, {
        "name": "Order Control",
        "data_type": "ID",
        "required": True,
        "table": "0119",  # Order Control table
    })
    
    # ORC-2: Placer Order Number (all versions)
    profile.add_field_definition("ORC", 2, {
        "name": "Placer Order Number",
        "data_type": "EI",
        "required": False,
    })
    
    # ORC-3: Filler Order Number (all versions)
    profile.add_field_definition("ORC", 3, {
        "name": "Filler Order Number",
        "data_type": "EI",
        "required": False,
    })
    
    # ORC-4: Placer Group Number (all versions)
    profile.add_field_definition("ORC", 4, {
        "name": "Placer Group Number",
        "data_type": "EI",
        "required": False,
    })
    
    # ORC-5: Order Status (all versions)
    profile.add_field_definition("ORC", 5, {
        "name": "Order Status",
        "data_type": "ID",
        "required": False,
        "table": "0038",  # Order Status table
    })
    
    # ORC-6: Response Flag (all versions)
    profile.add_field_definition("ORC", 6, {
        "name": "Response Flag",
        "data_type": "ID",
        "required": False,
        "table": "0121",  # Response Flag table
    })
    
    # ORC-7: Quantity/Timing (all versions)
    profile.add_field_definition("ORC", 7, {
        "name": "Quantity/Timing",
        "data_type": "TQ",
        "required": False,
        "max_repetitions": None,
    })
    
    # ORC-8: Parent (all versions)
    profile.add_field_definition("ORC", 8, {
        "name": "Parent",
        "data_type": "EIP",
        "required": False,
    })
    
    # ORC-9: Date/Time of Transaction (all versions)
    profile.add_field_definition("ORC", 9, {
        "name": "Date/Time of Transaction",
        "data_type": "TS",
        "required": False,
    })
    
    # ORC-10: Entered By (all versions)
    profile.add_field_definition("ORC", 10, {
        "name": "Entered By",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ORC-11: Verified By (all versions)
    profile.add_field_definition("ORC", 11, {
        "name": "Verified By",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ORC-12: Ordering Provider (all versions)
    profile.add_field_definition("ORC", 12, {
        "name": "Ordering Provider",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ORC-13: Enterer's Location (all versions)
    profile.add_field_definition("ORC", 13, {
        "name": "Enterer's Location",
        "data_type": "PL",
        "required": False,
    })
    
    # ORC-14: Call Back Phone Number (all versions)
    profile.add_field_definition("ORC", 14, {
        "name": "Call Back Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ORC-15: Order Effective Date/Time (all versions)
    profile.add_field_definition("ORC", 15, {
        "name": "Order Effective Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # ORC-16: Order Control Code Reason (all versions)
    profile.add_field_definition("ORC", 16, {
        "name": "Order Control Code Reason",
        "data_type": "CE",
        "required": False,
    })
    
    # ORC-17: Entering Organization (all versions)
    profile.add_field_definition("ORC", 17, {
        "name": "Entering Organization",
        "data_type": "CE",
        "required": False,
    })
    
    # ORC-18: Entering Device (all versions)
    profile.add_field_definition("ORC", 18, {
        "name": "Entering Device",
        "data_type": "CE",
        "required": False,
    })
    
    # ORC-19: Action By (all versions)
    profile.add_field_definition("ORC", 19, {
        "name": "Action By",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ORC-20: Advanced Beneficiary Notice Code (all versions)
    profile.add_field_definition("ORC", 20, {
        "name": "Advanced Beneficiary Notice Code",
        "data_type": "CE",
        "required": False,
    })
    
    # Version-specific ORC fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # ORC-21: Ordering Facility Name (added in 2.5+)
        profile.add_field_definition("ORC", 21, {
            "name": "Ordering Facility Name",
            "data_type": "XON",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-22: Ordering Facility Address (added in 2.5+)
        profile.add_field_definition("ORC", 22, {
            "name": "Ordering Facility Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-23: Ordering Facility Phone Number (added in 2.5+)
        profile.add_field_definition("ORC", 23, {
            "name": "Ordering Facility Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-24: Ordering Provider Address (added in 2.5+)
        profile.add_field_definition("ORC", 24, {
            "name": "Ordering Provider Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-25: Order Status Modifier (added in 2.5+)
        profile.add_field_definition("ORC", 25, {
            "name": "Order Status Modifier",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-26: Advanced Beneficiary Notice Override Reason (added in 2.5+)
        profile.add_field_definition("ORC", 26, {
            "name": "Advanced Beneficiary Notice Override Reason",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-27: Filler's Expected Availability Date/Time (added in 2.5+)
        profile.add_field_definition("ORC", 27, {
            "name": "Filler's Expected Availability Date/Time",
            "data_type": "TS",
            "required": False,
        })
        # ORC-28: Confidentiality Code (added in 2.5+)
        profile.add_field_definition("ORC", 28, {
            "name": "Confidentiality Code",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-29: Order Type (added in 2.5+)
        profile.add_field_definition("ORC", 29, {
            "name": "Order Type",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-30: Enterer Authorization Mode (added in 2.5+)
        profile.add_field_definition("ORC", 30, {
            "name": "Enterer Authorization Mode",
            "data_type": "CNE",
            "required": False,
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # ORC-31: Parent Universal Service Identifier (added in 2.7+)
        profile.add_field_definition("ORC", 31, {
            "name": "Parent Universal Service Identifier",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-32: Advanced Beneficiary Notice Code (added in 2.7+, replaces ORC-20 in some contexts)
        profile.add_field_definition("ORC", 32, {
            "name": "Advanced Beneficiary Notice Code",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-33: Ordering Facility Phone Number (added in 2.7+, replaces ORC-23 in some contexts)
        profile.add_field_definition("ORC", 33, {
            "name": "Ordering Facility Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-34: Ordering Provider Phone Number (added in 2.7+)
        profile.add_field_definition("ORC", 34, {
            "name": "Ordering Provider Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-35: Ordering Provider Address (added in 2.7+, replaces ORC-24 in some contexts)
        profile.add_field_definition("ORC", 35, {
            "name": "Ordering Provider Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-36: Order Status Modifier (added in 2.7+, replaces ORC-25 in some contexts)
        profile.add_field_definition("ORC", 36, {
            "name": "Order Status Modifier",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-37: Advanced Beneficiary Notice Override Reason (added in 2.7+, replaces ORC-26 in some contexts)
        profile.add_field_definition("ORC", 37, {
            "name": "Advanced Beneficiary Notice Override Reason",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
        })
        # ORC-38: Filler's Expected Availability Date/Time (added in 2.7+, replaces ORC-27 in some contexts)
        profile.add_field_definition("ORC", 38, {
            "name": "Filler's Expected Availability Date/Time",
            "data_type": "TS",
            "required": False,
        })
        # ORC-39: Confidentiality Code (added in 2.7+, replaces ORC-28 in some contexts)
        profile.add_field_definition("ORC", 39, {
            "name": "Confidentiality Code",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-40: Order Type (added in 2.7+, replaces ORC-29 in some contexts)
        profile.add_field_definition("ORC", 40, {
            "name": "Order Type",
            "data_type": "CWE",
            "required": False,
        })
        # ORC-41: Enterer Authorization Mode (added in 2.7+, replaces ORC-30 in some contexts)
        profile.add_field_definition("ORC", 41, {
            "name": "Enterer Authorization Mode",
            "data_type": "CNE",
            "required": False,
        })
    
    # IN1 segment definition (Insurance)
    profile.add_segment_definition("IN1", {
        "name": "IN1",
        "description": "Insurance",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # IN1-1: Set ID - IN1 (all versions)
    profile.add_field_definition("IN1", 1, {
        "name": "Set ID - IN1",
        "data_type": "SI",
        "required": False,
    })
    
    # IN1-2: Insurance Plan ID (all versions)
    profile.add_field_definition("IN1", 2, {
        "name": "Insurance Plan ID",
        "data_type": "CE",
        "required": False,
        "table": "0072",  # Insurance Plan ID table
    })
    
    # IN1-3: Insurance Company ID (all versions)
    profile.add_field_definition("IN1", 3, {
        "name": "Insurance Company ID",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-4: Insurance Company Name (all versions)
    profile.add_field_definition("IN1", 4, {
        "name": "Insurance Company Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-5: Insurance Company Address (all versions)
    profile.add_field_definition("IN1", 5, {
        "name": "Insurance Company Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-6: Insurance Co Contact Person (all versions)
    profile.add_field_definition("IN1", 6, {
        "name": "Insurance Co Contact Person",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-7: Insurance Co Phone Number (all versions)
    profile.add_field_definition("IN1", 7, {
        "name": "Insurance Co Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-8: Group Number (all versions)
    profile.add_field_definition("IN1", 8, {
        "name": "Group Number",
        "data_type": "ST",
        "required": False,
    })
    
    # IN1-9: Group Name (all versions)
    profile.add_field_definition("IN1", 9, {
        "name": "Group Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-10: Insured's Group Emp ID (all versions)
    profile.add_field_definition("IN1", 10, {
        "name": "Insured's Group Emp ID",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-11: Insured's Group Emp Name (all versions)
    profile.add_field_definition("IN1", 11, {
        "name": "Insured's Group Emp Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-12: Plan Effective Date (all versions)
    profile.add_field_definition("IN1", 12, {
        "name": "Plan Effective Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN1-13: Plan Expiration Date (all versions)
    profile.add_field_definition("IN1", 13, {
        "name": "Plan Expiration Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN1-14: Authorization Information (all versions)
    profile.add_field_definition("IN1", 14, {
        "name": "Authorization Information",
        "data_type": "AUI",
        "required": False,
    })
    
    # IN1-15: Plan Type (all versions)
    profile.add_field_definition("IN1", 15, {
        "name": "Plan Type",
        "data_type": "IS",
        "required": False,
        "table": "0086",  # Plan Type table
    })
    
    # IN1-16: Name Of Insured (all versions)
    profile.add_field_definition("IN1", 16, {
        "name": "Name Of Insured",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-17: Insured's Relationship To Patient (all versions)
    profile.add_field_definition("IN1", 17, {
        "name": "Insured's Relationship To Patient",
        "data_type": "CE",
        "required": False,
        "table": "0063",  # Relationship table
    })
    
    # IN1-18: Insured's Date Of Birth (all versions)
    profile.add_field_definition("IN1", 18, {
        "name": "Insured's Date Of Birth",
        "data_type": "TS",
        "required": False,
    })
    
    # IN1-19: Insured's Address (all versions)
    profile.add_field_definition("IN1", 19, {
        "name": "Insured's Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-20: Assignment Of Benefits (all versions)
    profile.add_field_definition("IN1", 20, {
        "name": "Assignment Of Benefits",
        "data_type": "IS",
        "required": False,
        "table": "0231",  # Assignment Of Benefits table
    })
    
    # IN1-21: Coordination Of Benefits (all versions)
    profile.add_field_definition("IN1", 21, {
        "name": "Coordination Of Benefits",
        "data_type": "IS",
        "required": False,
        "table": "0230",  # Coordination Of Benefits table
    })
    
    # IN1-22: Coord Of Ben. Priority (all versions)
    profile.add_field_definition("IN1", 22, {
        "name": "Coord Of Ben. Priority",
        "data_type": "ST",
        "required": False,
    })
    
    # IN1-23: Notice Of Admission Flag (all versions)
    profile.add_field_definition("IN1", 23, {
        "name": "Notice Of Admission Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN1-24: Notice Of Admission Date (all versions)
    profile.add_field_definition("IN1", 24, {
        "name": "Notice Of Admission Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN1-25: Report Of Eligibility Flag (all versions)
    profile.add_field_definition("IN1", 25, {
        "name": "Report Of Eligibility Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN1-26: Report Of Eligibility Date (all versions)
    profile.add_field_definition("IN1", 26, {
        "name": "Report Of Eligibility Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN1-27: Release Information Code (all versions)
    profile.add_field_definition("IN1", 27, {
        "name": "Release Information Code",
        "data_type": "IS",
        "required": False,
        "table": "0093",  # Release Information Code table
    })
    
    # IN1-28: Pre-Admit Cert (PAC) (all versions)
    profile.add_field_definition("IN1", 28, {
        "name": "Pre-Admit Cert (PAC)",
        "data_type": "ST",
        "required": False,
    })
    
    # IN1-29: Verification Date/Time (all versions)
    profile.add_field_definition("IN1", 29, {
        "name": "Verification Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # IN1-30: Verification By (all versions)
    profile.add_field_definition("IN1", 30, {
        "name": "Verification By",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-31: Type Of Agreement Code (all versions)
    profile.add_field_definition("IN1", 31, {
        "name": "Type Of Agreement Code",
        "data_type": "IS",
        "required": False,
        "table": "0098",  # Type Of Agreement Code table
    })
    
    # IN1-32: Billing Status (all versions)
    profile.add_field_definition("IN1", 32, {
        "name": "Billing Status",
        "data_type": "IS",
        "required": False,
        "table": "0022",  # Billing Status table
    })
    
    # IN1-33: Lifetime Reserve Days (all versions)
    profile.add_field_definition("IN1", 33, {
        "name": "Lifetime Reserve Days",
        "data_type": "NM",
        "required": False,
    })
    
    # IN1-34: Delay Before L.R. Day (all versions)
    profile.add_field_definition("IN1", 34, {
        "name": "Delay Before L.R. Day",
        "data_type": "NM",
        "required": False,
    })
    
    # IN1-35: Company Plan Code (all versions)
    profile.add_field_definition("IN1", 35, {
        "name": "Company Plan Code",
        "data_type": "IS",
        "required": False,
        "table": "0042",  # Company Plan Code table
    })
    
    # IN1-36: Policy Number (all versions)
    profile.add_field_definition("IN1", 36, {
        "name": "Policy Number",
        "data_type": "ST",
        "required": False,
    })
    
    # IN1-37: Policy Deductible (all versions)
    profile.add_field_definition("IN1", 37, {
        "name": "Policy Deductible",
        "data_type": "CP",
        "required": False,
    })
    
    # IN1-38: Policy Limit - Amount (all versions)
    profile.add_field_definition("IN1", 38, {
        "name": "Policy Limit - Amount",
        "data_type": "CP",
        "required": False,
    })
    
    # IN1-39: Policy Limit - Days (all versions)
    profile.add_field_definition("IN1", 39, {
        "name": "Policy Limit - Days",
        "data_type": "NM",
        "required": False,
    })
    
    # IN1-40: Room Rate - Semi-Private (all versions)
    profile.add_field_definition("IN1", 40, {
        "name": "Room Rate - Semi-Private",
        "data_type": "CP",
        "required": False,
    })
    
    # IN1-41: Room Rate - Private (all versions)
    profile.add_field_definition("IN1", 41, {
        "name": "Room Rate - Private",
        "data_type": "CP",
        "required": False,
    })
    
    # IN1-42: Insured's Employment Status (all versions)
    profile.add_field_definition("IN1", 42, {
        "name": "Insured's Employment Status",
        "data_type": "CE",
        "required": False,
        "table": "0066",  # Employment Status table
    })
    
    # IN1-43: Insured's Administrative Sex (all versions)
    profile.add_field_definition("IN1", 43, {
        "name": "Insured's Administrative Sex",
        "data_type": "IS",
        "required": False,
        "table": "0001",  # Administrative Sex table
    })
    
    # IN1-44: Insured's Employer's Address (all versions)
    profile.add_field_definition("IN1", 44, {
        "name": "Insured's Employer's Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN1-45: Verification Status (all versions)
    profile.add_field_definition("IN1", 45, {
        "name": "Verification Status",
        "data_type": "ST",
        "required": False,
    })
    
    # IN1-46: Prior Insurance Plan ID (all versions)
    profile.add_field_definition("IN1", 46, {
        "name": "Prior Insurance Plan ID",
        "data_type": "IS",
        "required": False,
        "table": "0072",  # Insurance Plan ID table
    })
    
    # IN1-47: Coverage Type (all versions)
    profile.add_field_definition("IN1", 47, {
        "name": "Coverage Type",
        "data_type": "IS",
        "required": False,
        "table": "0309",  # Coverage Type table
    })
    
    # IN1-48: Handicap (all versions)
    profile.add_field_definition("IN1", 48, {
        "name": "Handicap",
        "data_type": "IS",
        "required": False,
        "table": "0295",  # Handicap table
    })
    
    # IN1-49: Insured's ID Number (all versions)
    profile.add_field_definition("IN1", 49, {
        "name": "Insured's ID Number",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific IN1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # IN1-50: Signature Code (added in 2.5+)
        profile.add_field_definition("IN1", 50, {
            "name": "Signature Code",
            "data_type": "IS",
            "required": False,
            "table": "0535",  # Signature Code table
        })
        # IN1-51: Signature Code Date (added in 2.5+)
        profile.add_field_definition("IN1", 51, {
            "name": "Signature Code Date",
            "data_type": "DT",
            "required": False,
        })
        # IN1-52: Insured's Birth Place (added in 2.5+)
        profile.add_field_definition("IN1", 52, {
            "name": "Insured's Birth Place",
            "data_type": "ST",
            "required": False,
        })
        # IN1-53: VIP Indicator (added in 2.5+)
        profile.add_field_definition("IN1", 53, {
            "name": "VIP Indicator",
            "data_type": "IS",
            "required": False,
            "table": "0099",  # VIP Indicator table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # IN1-54: External Health Plan Identifiers (added in 2.7+)
        profile.add_field_definition("IN1", 54, {
            "name": "External Health Plan Identifiers",
            "data_type": "CX",
            "required": False,
            "max_repetitions": None,
        })
        # IN1-55: Insurance Action Code (added in 2.7+)
        profile.add_field_definition("IN1", 55, {
            "name": "Insurance Action Code",
            "data_type": "IS",
            "required": False,
            "table": "0206",  # Segment Action Code table
        })
    
    # IN2 segment definition (Insurance Additional Information)
    profile.add_segment_definition("IN2", {
        "name": "IN2",
        "description": "Insurance Additional Information",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # IN2-1: Set ID - IN2 (all versions)
    profile.add_field_definition("IN2", 1, {
        "name": "Set ID - IN2",
        "data_type": "SI",
        "required": False,
    })
    
    # IN2-2: Insured's Employee ID (all versions)
    profile.add_field_definition("IN2", 2, {
        "name": "Insured's Employee ID",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-3: Insured's Social Security Number (all versions)
    profile.add_field_definition("IN2", 3, {
        "name": "Insured's Social Security Number",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-4: Insured's Employer's Name and ID (all versions)
    profile.add_field_definition("IN2", 4, {
        "name": "Insured's Employer's Name and ID",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-5: Employer Information Data (all versions)
    profile.add_field_definition("IN2", 5, {
        "name": "Employer Information Data",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-6: Mail Claim Party (all versions)
    profile.add_field_definition("IN2", 6, {
        "name": "Mail Claim Party",
        "data_type": "IS",
        "required": False,
        "table": "0137",  # Mail Claim Party table
    })
    
    # IN2-7: Medicare Health Ins Card Number (all versions)
    profile.add_field_definition("IN2", 7, {
        "name": "Medicare Health Ins Card Number",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-8: Medicaid Case Name (all versions)
    profile.add_field_definition("IN2", 8, {
        "name": "Medicaid Case Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-9: Medicaid Case Number (all versions)
    profile.add_field_definition("IN2", 9, {
        "name": "Medicaid Case Number",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-10: Military Sponsor Name (all versions)
    profile.add_field_definition("IN2", 10, {
        "name": "Military Sponsor Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-11: Military ID Number (all versions)
    profile.add_field_definition("IN2", 11, {
        "name": "Military ID Number",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-12: Dependent Of Military Recipient (all versions)
    profile.add_field_definition("IN2", 12, {
        "name": "Dependent Of Military Recipient",
        "data_type": "CE",
        "required": False,
        "table": "0342",  # Military Recipient table
    })
    
    # IN2-13: Military Organization (all versions)
    profile.add_field_definition("IN2", 13, {
        "name": "Military Organization",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-14: Military Station (all versions)
    profile.add_field_definition("IN2", 14, {
        "name": "Military Station",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-15: Military Service (all versions)
    profile.add_field_definition("IN2", 15, {
        "name": "Military Service",
        "data_type": "IS",
        "required": False,
        "table": "0140",  # Military Service table
    })
    
    # IN2-16: Military Rank/Grade (all versions)
    profile.add_field_definition("IN2", 16, {
        "name": "Military Rank/Grade",
        "data_type": "IS",
        "required": False,
        "table": "0141",  # Military Rank/Grade table
    })
    
    # IN2-17: Military Status (all versions)
    profile.add_field_definition("IN2", 17, {
        "name": "Military Status",
        "data_type": "IS",
        "required": False,
        "table": "0142",  # Military Status table
    })
    
    # IN2-18: Military Retire Date (all versions)
    profile.add_field_definition("IN2", 18, {
        "name": "Military Retire Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN2-19: Military Non-Avail Cert On File (all versions)
    profile.add_field_definition("IN2", 19, {
        "name": "Military Non-Avail Cert On File",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-20: Baby Coverage (all versions)
    profile.add_field_definition("IN2", 20, {
        "name": "Baby Coverage",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-21: Combine Baby Bill (all versions)
    profile.add_field_definition("IN2", 21, {
        "name": "Combine Baby Bill",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-22: Blood Deductible (all versions)
    profile.add_field_definition("IN2", 22, {
        "name": "Blood Deductible",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-23: Special Coverage Approval Name (all versions)
    profile.add_field_definition("IN2", 23, {
        "name": "Special Coverage Approval Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-24: Special Coverage Approval Title (all versions)
    profile.add_field_definition("IN2", 24, {
        "name": "Special Coverage Approval Title",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-25: Non-Covered Insurance Code (all versions)
    profile.add_field_definition("IN2", 25, {
        "name": "Non-Covered Insurance Code",
        "data_type": "IS",
        "required": False,
        "table": "0143",  # Non-Covered Insurance Code table
    })
    
    # IN2-26: Payor ID (all versions)
    profile.add_field_definition("IN2", 26, {
        "name": "Payor ID",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-27: Payor Subscriber ID (all versions)
    profile.add_field_definition("IN2", 27, {
        "name": "Payor Subscriber ID",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-28: Eligibility Source (all versions)
    profile.add_field_definition("IN2", 28, {
        "name": "Eligibility Source",
        "data_type": "IS",
        "required": False,
        "table": "0144",  # Eligibility Source table
    })
    
    # IN2-29: Room Coverage Type/Amount (all versions)
    profile.add_field_definition("IN2", 29, {
        "name": "Room Coverage Type/Amount",
        "data_type": "RMC",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-30: Policy Type/Amount (all versions)
    profile.add_field_definition("IN2", 30, {
        "name": "Policy Type/Amount",
        "data_type": "PTA",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-31: Daily Deductible (all versions)
    profile.add_field_definition("IN2", 31, {
        "name": "Daily Deductible",
        "data_type": "DDI",
        "required": False,
    })
    
    # IN2-32: Living Dependency (all versions)
    profile.add_field_definition("IN2", 32, {
        "name": "Living Dependency",
        "data_type": "IS",
        "required": False,
        "table": "0223",  # Living Dependency table
    })
    
    # IN2-33: Ambulatory Status (all versions)
    profile.add_field_definition("IN2", 33, {
        "name": "Ambulatory Status",
        "data_type": "IS",
        "required": False,
        "table": "0009",  # Ambulatory Status table
    })
    
    # IN2-34: Citizenship (all versions)
    profile.add_field_definition("IN2", 34, {
        "name": "Citizenship",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-35: Primary Language (all versions)
    profile.add_field_definition("IN2", 35, {
        "name": "Primary Language",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-36: Living Arrangement (all versions)
    profile.add_field_definition("IN2", 36, {
        "name": "Living Arrangement",
        "data_type": "IS",
        "required": False,
        "table": "0220",  # Living Arrangement table
    })
    
    # IN2-37: Patient's Primary Facility (all versions)
    profile.add_field_definition("IN2", 37, {
        "name": "Patient's Primary Facility",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-38: Patient's Primary Care Provider Name/ID No (all versions)
    profile.add_field_definition("IN2", 38, {
        "name": "Patient's Primary Care Provider Name/ID No",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-39: Student Status (all versions)
    profile.add_field_definition("IN2", 39, {
        "name": "Student Status",
        "data_type": "IS",
        "required": False,
        "table": "0231",  # Student Status table
    })
    
    # IN2-40: Handicap (all versions)
    profile.add_field_definition("IN2", 40, {
        "name": "Handicap",
        "data_type": "IS",
        "required": False,
        "table": "0295",  # Handicap table
    })
    
    # IN2-41: Patient's Primary Facility Name (all versions)
    profile.add_field_definition("IN2", 41, {
        "name": "Patient's Primary Facility Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-42: Patient's Primary Care Provider Name (all versions)
    profile.add_field_definition("IN2", 42, {
        "name": "Patient's Primary Care Provider Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-43: Patient's Primary Care Provider Address (all versions)
    profile.add_field_definition("IN2", 43, {
        "name": "Patient's Primary Care Provider Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-44: Patient's Primary Care Provider Phone Number (all versions)
    profile.add_field_definition("IN2", 44, {
        "name": "Patient's Primary Care Provider Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-45: Patient's Primary Care Provider ID Number (all versions)
    profile.add_field_definition("IN2", 45, {
        "name": "Patient's Primary Care Provider ID Number",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-46: Champus Service (all versions)
    profile.add_field_definition("IN2", 46, {
        "name": "Champus Service",
        "data_type": "IS",
        "required": False,
        "table": "0140",  # Military Service table
    })
    
    # IN2-47: Champus Rank/Grade (all versions)
    profile.add_field_definition("IN2", 47, {
        "name": "Champus Rank/Grade",
        "data_type": "IS",
        "required": False,
        "table": "0141",  # Military Rank/Grade table
    })
    
    # IN2-48: Champus Status (all versions)
    profile.add_field_definition("IN2", 48, {
        "name": "Champus Status",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-49: Champus Retire Date (all versions)
    profile.add_field_definition("IN2", 49, {
        "name": "Champus Retire Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN2-50: Champus Non-Avail Cert On File (all versions)
    profile.add_field_definition("IN2", 50, {
        "name": "Champus Non-Avail Cert On File",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-51: Champus Organization (all versions)
    profile.add_field_definition("IN2", 51, {
        "name": "Champus Organization",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-52: Champus Station (all versions)
    profile.add_field_definition("IN2", 52, {
        "name": "Champus Station",
        "data_type": "ST",
        "required": False,
    })
    
    # IN2-53: Room Coverage Type/Amount - Second (all versions)
    profile.add_field_definition("IN2", 53, {
        "name": "Room Coverage Type/Amount - Second",
        "data_type": "RMC",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-54: Policy Type/Amount - Second (all versions)
    profile.add_field_definition("IN2", 54, {
        "name": "Policy Type/Amount - Second",
        "data_type": "PTA",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-55: Daily Deductible - Second (all versions)
    profile.add_field_definition("IN2", 55, {
        "name": "Daily Deductible - Second",
        "data_type": "DDI",
        "required": False,
    })
    
    # IN2-56: Living Dependency - Second (all versions)
    profile.add_field_definition("IN2", 56, {
        "name": "Living Dependency - Second",
        "data_type": "IS",
        "required": False,
        "table": "0223",  # Living Dependency table
    })
    
    # IN2-57: Ambulatory Status - Second (all versions)
    profile.add_field_definition("IN2", 57, {
        "name": "Ambulatory Status - Second",
        "data_type": "IS",
        "required": False,
        "table": "0009",  # Ambulatory Status table
    })
    
    # IN2-58: Citizenship - Second (all versions)
    profile.add_field_definition("IN2", 58, {
        "name": "Citizenship - Second",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-59: Primary Language - Second (all versions)
    profile.add_field_definition("IN2", 59, {
        "name": "Primary Language - Second",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-60: Living Arrangement - Second (all versions)
    profile.add_field_definition("IN2", 60, {
        "name": "Living Arrangement - Second",
        "data_type": "IS",
        "required": False,
        "table": "0220",  # Living Arrangement table
    })
    
    # IN2-61: Patient's Primary Facility - Second (all versions)
    profile.add_field_definition("IN2", 61, {
        "name": "Patient's Primary Facility - Second",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-62: Patient's Primary Care Provider Name/ID No - Second (all versions)
    profile.add_field_definition("IN2", 62, {
        "name": "Patient's Primary Care Provider Name/ID No - Second",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-63: Student Status - Second (all versions)
    profile.add_field_definition("IN2", 63, {
        "name": "Student Status - Second",
        "data_type": "IS",
        "required": False,
        "table": "0231",  # Student Status table
    })
    
    # IN2-64: Handicap - Second (all versions)
    profile.add_field_definition("IN2", 64, {
        "name": "Handicap - Second",
        "data_type": "IS",
        "required": False,
        "table": "0295",  # Handicap table
    })
    
    # IN2-65: Patient's Primary Facility Name - Second (all versions)
    profile.add_field_definition("IN2", 65, {
        "name": "Patient's Primary Facility Name - Second",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-66: Patient's Primary Care Provider Name - Second (all versions)
    profile.add_field_definition("IN2", 66, {
        "name": "Patient's Primary Care Provider Name - Second",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-67: Patient's Primary Care Provider Address - Second (all versions)
    profile.add_field_definition("IN2", 67, {
        "name": "Patient's Primary Care Provider Address - Second",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-68: Patient's Primary Care Provider Phone Number - Second (all versions)
    profile.add_field_definition("IN2", 68, {
        "name": "Patient's Primary Care Provider Phone Number - Second",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-69: Patient's Primary Care Provider ID Number - Second (all versions)
    profile.add_field_definition("IN2", 69, {
        "name": "Patient's Primary Care Provider ID Number - Second",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-70: Insured's Contact Person's Name (all versions)
    profile.add_field_definition("IN2", 70, {
        "name": "Insured's Contact Person's Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-71: Insured's Contact Person Phone Number (all versions)
    profile.add_field_definition("IN2", 71, {
        "name": "Insured's Contact Person Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-72: Insured's Contact Person Reason (all versions)
    profile.add_field_definition("IN2", 72, {
        "name": "Insured's Contact Person Reason",
        "data_type": "IS",
        "required": False,
        "table": "0222",  # Contact Reason table
    })
    
    # IN2-73: Relationship To The Patient Start Date (all versions)
    profile.add_field_definition("IN2", 73, {
        "name": "Relationship To The Patient Start Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN2-74: Relationship To The Patient Stop Date (all versions)
    profile.add_field_definition("IN2", 74, {
        "name": "Relationship To The Patient Stop Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN2-75: Insurance Co Contact Reason (all versions)
    profile.add_field_definition("IN2", 75, {
        "name": "Insurance Co Contact Reason",
        "data_type": "IS",
        "required": False,
        "table": "0232",  # Insurance Co Contact Reason table
    })
    
    # IN2-76: Insurance Co Contact Phone Number (all versions)
    profile.add_field_definition("IN2", 76, {
        "name": "Insurance Co Contact Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-77: Policy Scope (all versions)
    profile.add_field_definition("IN2", 77, {
        "name": "Policy Scope",
        "data_type": "IS",
        "required": False,
        "table": "0312",  # Policy Scope table
    })
    
    # IN2-78: Policy Source (all versions)
    profile.add_field_definition("IN2", 78, {
        "name": "Policy Source",
        "data_type": "IS",
        "required": False,
        "table": "0313",  # Policy Source table
    })
    
    # IN2-79: Patient Member Number (all versions)
    profile.add_field_definition("IN2", 79, {
        "name": "Patient Member Number",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-80: Guarantor's Relationship To Insured (all versions)
    profile.add_field_definition("IN2", 80, {
        "name": "Guarantor's Relationship To Insured",
        "data_type": "CE",
        "required": False,
        "table": "0063",  # Relationship table
    })
    
    # IN2-81: Insured's Phone Number - Home (all versions)
    profile.add_field_definition("IN2", 81, {
        "name": "Insured's Phone Number - Home",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-82: Insured's Employer Phone Number (all versions)
    profile.add_field_definition("IN2", 82, {
        "name": "Insured's Employer Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-83: Military Handicapped Program (all versions)
    profile.add_field_definition("IN2", 83, {
        "name": "Military Handicapped Program",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-84: Suspend Flag (all versions)
    profile.add_field_definition("IN2", 84, {
        "name": "Suspend Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-85: Copay Limit Flag (all versions)
    profile.add_field_definition("IN2", 85, {
        "name": "Copay Limit Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-86: Stoploss Limit Flag (all versions)
    profile.add_field_definition("IN2", 86, {
        "name": "Stoploss Limit Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN2-87: Insured Organization Name And ID (all versions)
    profile.add_field_definition("IN2", 87, {
        "name": "Insured Organization Name And ID",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-88: Insured Employer Organization Name And ID (all versions)
    profile.add_field_definition("IN2", 88, {
        "name": "Insured Employer Organization Name And ID",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN2-89: Race (all versions)
    profile.add_field_definition("IN2", 89, {
        "name": "Race",
        "data_type": "CE",
        "required": False,
    })
    
    # IN2-90: Patient's Relationship To Insured (all versions)
    profile.add_field_definition("IN2", 90, {
        "name": "Patient's Relationship To Insured",
        "data_type": "CE",
        "required": False,
        "table": "0063",  # Relationship table
    })
    
    # Version-specific IN2 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # IN2-91: Patient's Citizenship (added in 2.5+)
        profile.add_field_definition("IN2", 91, {
            "name": "Patient's Citizenship",
            "data_type": "CE",
            "required": False,
        })
        # IN2-92: Patient's Veterans Military Status (added in 2.5+)
        profile.add_field_definition("IN2", 92, {
            "name": "Patient's Veterans Military Status",
            "data_type": "CE",
            "required": False,
        })
        # IN2-93: Patient's Nationality (added in 2.5+)
        profile.add_field_definition("IN2", 93, {
            "name": "Patient's Nationality",
            "data_type": "CE",
            "required": False,
        })
        # IN2-94: Patient's Marital Status (added in 2.5+)
        profile.add_field_definition("IN2", 94, {
            "name": "Patient's Marital Status",
            "data_type": "CE",
            "required": False,
            "table": "0002",  # Marital Status table
        })
        # IN2-95: Insured's Marital Status (added in 2.5+)
        profile.add_field_definition("IN2", 95, {
            "name": "Insured's Marital Status",
            "data_type": "CE",
            "required": False,
            "table": "0002",  # Marital Status table
        })
        # IN2-96: Insured's Employment Status (added in 2.5+)
        profile.add_field_definition("IN2", 96, {
            "name": "Insured's Employment Status",
            "data_type": "CE",
            "required": False,
            "table": "0066",  # Employment Status table
        })
        # IN2-97: Insured's Sex (added in 2.5+)
        profile.add_field_definition("IN2", 97, {
            "name": "Insured's Sex",
            "data_type": "IS",
            "required": False,
            "table": "0001",  # Administrative Sex table
        })
        # IN2-98: Insured's Employer Address (added in 2.5+)
        profile.add_field_definition("IN2", 98, {
            "name": "Insured's Employer Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-99: Insured's Employer City/State (added in 2.5+)
        profile.add_field_definition("IN2", 99, {
            "name": "Insured's Employer City/State",
            "data_type": "ST",
            "required": False,
        })
        # IN2-100: Insured's Employer Country/Postal Code (added in 2.5+)
        profile.add_field_definition("IN2", 100, {
            "name": "Insured's Employer Country/Postal Code",
            "data_type": "ST",
            "required": False,
        })
        # IN2-101: Insured's Employer Phone Number (added in 2.5+)
        profile.add_field_definition("IN2", 101, {
            "name": "Insured's Employer Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-102: Insured's Employer Organization Name and ID (added in 2.5+)
        profile.add_field_definition("IN2", 102, {
            "name": "Insured's Employer Organization Name and ID",
            "data_type": "XON",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-103: Insured's Employer Contact Person Name (added in 2.5+)
        profile.add_field_definition("IN2", 103, {
            "name": "Insured's Employer Contact Person Name",
            "data_type": "XPN",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-104: Insured's Employer Contact Person Phone Number (added in 2.5+)
        profile.add_field_definition("IN2", 104, {
            "name": "Insured's Employer Contact Person Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-105: Insured's Employer Contact Reason (added in 2.5+)
        profile.add_field_definition("IN2", 105, {
            "name": "Insured's Employer Contact Reason",
            "data_type": "IS",
            "required": False,
            "table": "0222",  # Contact Reason table
        })
        # IN2-106: Insured's Employer Contact Address (added in 2.5+)
        profile.add_field_definition("IN2", 106, {
            "name": "Insured's Employer Contact Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-107: Insured's Employer Organization Name and ID (added in 2.5+)
        profile.add_field_definition("IN2", 107, {
            "name": "Insured's Employer Organization Name and ID",
            "data_type": "XON",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-108: Insured's Employer Organization Address (added in 2.5+)
        profile.add_field_definition("IN2", 108, {
            "name": "Insured's Employer Organization Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-109: Insured's Employer Organization Phone Number (added in 2.5+)
        profile.add_field_definition("IN2", 109, {
            "name": "Insured's Employer Organization Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-110: Insured's Employer Organization Contact Person Name (added in 2.5+)
        profile.add_field_definition("IN2", 110, {
            "name": "Insured's Employer Organization Contact Person Name",
            "data_type": "XPN",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-111: Insured's Employer Organization Contact Person Phone Number (added in 2.5+)
        profile.add_field_definition("IN2", 111, {
            "name": "Insured's Employer Organization Contact Person Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        # IN2-112: Insured's Employer Organization Contact Reason (added in 2.5+)
        profile.add_field_definition("IN2", 112, {
            "name": "Insured's Employer Organization Contact Reason",
            "data_type": "IS",
            "required": False,
            "table": "0222",  # Contact Reason table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # IN2-113: Insured's Birth Place (added in 2.7+)
        profile.add_field_definition("IN2", 113, {
            "name": "Insured's Birth Place",
            "data_type": "ST",
            "required": False,
        })
        # IN2-114: VIP Indicator (added in 2.7+)
        profile.add_field_definition("IN2", 114, {
            "name": "VIP Indicator",
            "data_type": "IS",
            "required": False,
            "table": "0099",  # VIP Indicator table
        })
    
    # IN3 segment definition (Insurance Additional Information - Certification)
    profile.add_segment_definition("IN3", {
        "name": "IN3",
        "description": "Insurance Additional Information - Certification",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # IN3-1: Set ID - IN3 (all versions)
    profile.add_field_definition("IN3", 1, {
        "name": "Set ID - IN3",
        "data_type": "SI",
        "required": False,
    })
    
    # IN3-2: Certification Number (all versions)
    profile.add_field_definition("IN3", 2, {
        "name": "Certification Number",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN3-3: Certified By (all versions)
    profile.add_field_definition("IN3", 3, {
        "name": "Certified By",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN3-4: Certification Required (all versions)
    profile.add_field_definition("IN3", 4, {
        "name": "Certification Required",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # IN3-5: Penalty (all versions)
    profile.add_field_definition("IN3", 5, {
        "name": "Penalty",
        "data_type": "MOP",
        "required": False,
    })
    
    # IN3-6: Certification Date/Time (all versions)
    profile.add_field_definition("IN3", 6, {
        "name": "Certification Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # IN3-7: Certification Modify Date/Time (all versions)
    profile.add_field_definition("IN3", 7, {
        "name": "Certification Modify Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # IN3-8: Operator (all versions)
    profile.add_field_definition("IN3", 8, {
        "name": "Operator",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN3-9: Certification Begin Date (all versions)
    profile.add_field_definition("IN3", 9, {
        "name": "Certification Begin Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN3-10: Certification End Date (all versions)
    profile.add_field_definition("IN3", 10, {
        "name": "Certification End Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN3-11: Days (all versions)
    profile.add_field_definition("IN3", 11, {
        "name": "Days",
        "data_type": "DTN",
        "required": False,
    })
    
    # IN3-12: Non-Concur Code/Description (all versions)
    profile.add_field_definition("IN3", 12, {
        "name": "Non-Concur Code/Description",
        "data_type": "CE",
        "required": False,
    })
    
    # IN3-13: Non-Concur Effective Date/Time (all versions)
    profile.add_field_definition("IN3", 13, {
        "name": "Non-Concur Effective Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # IN3-14: Physician Reviewer (all versions)
    profile.add_field_definition("IN3", 14, {
        "name": "Physician Reviewer",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN3-15: Certification Contact (all versions)
    profile.add_field_definition("IN3", 15, {
        "name": "Certification Contact",
        "data_type": "ST",
        "required": False,
    })
    
    # IN3-16: Certification Contact Phone Number (all versions)
    profile.add_field_definition("IN3", 16, {
        "name": "Certification Contact Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN3-17: Appeal Reason (all versions)
    profile.add_field_definition("IN3", 17, {
        "name": "Appeal Reason",
        "data_type": "CE",
        "required": False,
    })
    
    # IN3-18: Certification Agency (all versions)
    profile.add_field_definition("IN3", 18, {
        "name": "Certification Agency",
        "data_type": "CE",
        "required": False,
    })
    
    # IN3-19: Certification Agency Phone Number (all versions)
    profile.add_field_definition("IN3", 19, {
        "name": "Certification Agency Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # IN3-20: Pre-Certification Requirement/Window (all versions)
    profile.add_field_definition("IN3", 20, {
        "name": "Pre-Certification Requirement/Window",
        "data_type": "PIP",
        "required": False,
    })
    
    # IN3-21: Case Manager (all versions)
    profile.add_field_definition("IN3", 21, {
        "name": "Case Manager",
        "data_type": "ST",
        "required": False,
    })
    
    # IN3-22: Second Opinion Date (all versions)
    profile.add_field_definition("IN3", 22, {
        "name": "Second Opinion Date",
        "data_type": "DT",
        "required": False,
    })
    
    # IN3-23: Second Opinion Status (all versions)
    profile.add_field_definition("IN3", 23, {
        "name": "Second Opinion Status",
        "data_type": "IS",
        "required": False,
        "table": "0151",  # Second Opinion Status table
    })
    
    # IN3-24: Second Opinion Documentation Received (all versions)
    profile.add_field_definition("IN3", 24, {
        "name": "Second Opinion Documentation Received",
        "data_type": "IS",
        "required": False,
        "table": "0152",  # Second Opinion Documentation Received table
    })
    
    # IN3-25: Second Opinion Physician (all versions)
    profile.add_field_definition("IN3", 25, {
        "name": "Second Opinion Physician",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific IN3 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # IN3-26: Certification Type (added in 2.5+)
        profile.add_field_definition("IN3", 26, {
            "name": "Certification Type",
            "data_type": "CE",
            "required": False,
        })
        # IN3-27: Certification Category (added in 2.5+)
        profile.add_field_definition("IN3", 27, {
            "name": "Certification Category",
            "data_type": "CE",
            "required": False,
        })
        # IN3-28: Certification Value/Amount (added in 2.5+)
        profile.add_field_definition("IN3", 28, {
            "name": "Certification Value/Amount",
            "data_type": "CP",
            "required": False,
        })
        # IN3-29: Certification Value/Amount - Second (added in 2.5+)
        profile.add_field_definition("IN3", 29, {
            "name": "Certification Value/Amount - Second",
            "data_type": "CP",
            "required": False,
        })
        # IN3-30: Certification Value/Amount - Third (added in 2.5+)
        profile.add_field_definition("IN3", 30, {
            "name": "Certification Value/Amount - Third",
            "data_type": "CP",
            "required": False,
        })
        # IN3-31: Certification Value/Amount - Fourth (added in 2.5+)
        profile.add_field_definition("IN3", 31, {
            "name": "Certification Value/Amount - Fourth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-32: Certification Value/Amount - Fifth (added in 2.5+)
        profile.add_field_definition("IN3", 32, {
            "name": "Certification Value/Amount - Fifth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-33: Certification Value/Amount - Sixth (added in 2.5+)
        profile.add_field_definition("IN3", 33, {
            "name": "Certification Value/Amount - Sixth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-34: Certification Value/Amount - Seventh (added in 2.5+)
        profile.add_field_definition("IN3", 34, {
            "name": "Certification Value/Amount - Seventh",
            "data_type": "CP",
            "required": False,
        })
        # IN3-35: Certification Value/Amount - Eighth (added in 2.5+)
        profile.add_field_definition("IN3", 35, {
            "name": "Certification Value/Amount - Eighth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-36: Certification Value/Amount - Ninth (added in 2.5+)
        profile.add_field_definition("IN3", 36, {
            "name": "Certification Value/Amount - Ninth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-37: Certification Value/Amount - Tenth (added in 2.5+)
        profile.add_field_definition("IN3", 37, {
            "name": "Certification Value/Amount - Tenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-38: Certification Value/Amount - Eleventh (added in 2.5+)
        profile.add_field_definition("IN3", 38, {
            "name": "Certification Value/Amount - Eleventh",
            "data_type": "CP",
            "required": False,
        })
        # IN3-39: Certification Value/Amount - Twelfth (added in 2.5+)
        profile.add_field_definition("IN3", 39, {
            "name": "Certification Value/Amount - Twelfth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-40: Certification Value/Amount - Thirteenth (added in 2.5+)
        profile.add_field_definition("IN3", 40, {
            "name": "Certification Value/Amount - Thirteenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-41: Certification Value/Amount - Fourteenth (added in 2.5+)
        profile.add_field_definition("IN3", 41, {
            "name": "Certification Value/Amount - Fourteenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-42: Certification Value/Amount - Fifteenth (added in 2.5+)
        profile.add_field_definition("IN3", 42, {
            "name": "Certification Value/Amount - Fifteenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-43: Certification Value/Amount - Sixteenth (added in 2.5+)
        profile.add_field_definition("IN3", 43, {
            "name": "Certification Value/Amount - Sixteenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-44: Certification Value/Amount - Seventeenth (added in 2.5+)
        profile.add_field_definition("IN3", 44, {
            "name": "Certification Value/Amount - Seventeenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-45: Certification Value/Amount - Eighteenth (added in 2.5+)
        profile.add_field_definition("IN3", 45, {
            "name": "Certification Value/Amount - Eighteenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-46: Certification Value/Amount - Nineteenth (added in 2.5+)
        profile.add_field_definition("IN3", 46, {
            "name": "Certification Value/Amount - Nineteenth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-47: Certification Value/Amount - Twentieth (added in 2.5+)
        profile.add_field_definition("IN3", 47, {
            "name": "Certification Value/Amount - Twentieth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-48: Certification Value/Amount - Twenty-First (added in 2.5+)
        profile.add_field_definition("IN3", 48, {
            "name": "Certification Value/Amount - Twenty-First",
            "data_type": "CP",
            "required": False,
        })
        # IN3-49: Certification Value/Amount - Twenty-Second (added in 2.5+)
        profile.add_field_definition("IN3", 49, {
            "name": "Certification Value/Amount - Twenty-Second",
            "data_type": "CP",
            "required": False,
        })
        # IN3-50: Certification Value/Amount - Twenty-Third (added in 2.5+)
        profile.add_field_definition("IN3", 50, {
            "name": "Certification Value/Amount - Twenty-Third",
            "data_type": "CP",
            "required": False,
        })
        # IN3-51: Certification Value/Amount - Twenty-Fourth (added in 2.5+)
        profile.add_field_definition("IN3", 51, {
            "name": "Certification Value/Amount - Twenty-Fourth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-52: Certification Value/Amount - Twenty-Fifth (added in 2.5+)
        profile.add_field_definition("IN3", 52, {
            "name": "Certification Value/Amount - Twenty-Fifth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-53: Certification Value/Amount - Twenty-Sixth (added in 2.5+)
        profile.add_field_definition("IN3", 53, {
            "name": "Certification Value/Amount - Twenty-Sixth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-54: Certification Value/Amount - Twenty-Seventh (added in 2.5+)
        profile.add_field_definition("IN3", 54, {
            "name": "Certification Value/Amount - Twenty-Seventh",
            "data_type": "CP",
            "required": False,
        })
        # IN3-55: Certification Value/Amount - Twenty-Eighth (added in 2.5+)
        profile.add_field_definition("IN3", 55, {
            "name": "Certification Value/Amount - Twenty-Eighth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-56: Certification Value/Amount - Twenty-Ninth (added in 2.5+)
        profile.add_field_definition("IN3", 56, {
            "name": "Certification Value/Amount - Twenty-Ninth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-57: Certification Value/Amount - Thirtieth (added in 2.5+)
        profile.add_field_definition("IN3", 57, {
            "name": "Certification Value/Amount - Thirtieth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-58: Certification Value/Amount - Thirty-First (added in 2.5+)
        profile.add_field_definition("IN3", 58, {
            "name": "Certification Value/Amount - Thirty-First",
            "data_type": "CP",
            "required": False,
        })
        # IN3-59: Certification Value/Amount - Thirty-Second (added in 2.5+)
        profile.add_field_definition("IN3", 59, {
            "name": "Certification Value/Amount - Thirty-Second",
            "data_type": "CP",
            "required": False,
        })
        # IN3-60: Certification Value/Amount - Thirty-Third (added in 2.5+)
        profile.add_field_definition("IN3", 60, {
            "name": "Certification Value/Amount - Thirty-Third",
            "data_type": "CP",
            "required": False,
        })
        # IN3-61: Certification Value/Amount - Thirty-Fourth (added in 2.5+)
        profile.add_field_definition("IN3", 61, {
            "name": "Certification Value/Amount - Thirty-Fourth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-62: Certification Value/Amount - Thirty-Fifth (added in 2.5+)
        profile.add_field_definition("IN3", 62, {
            "name": "Certification Value/Amount - Thirty-Fifth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-63: Certification Value/Amount - Thirty-Sixth (added in 2.5+)
        profile.add_field_definition("IN3", 63, {
            "name": "Certification Value/Amount - Thirty-Sixth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-64: Certification Value/Amount - Thirty-Seventh (added in 2.5+)
        profile.add_field_definition("IN3", 64, {
            "name": "Certification Value/Amount - Thirty-Seventh",
            "data_type": "CP",
            "required": False,
        })
        # IN3-65: Certification Value/Amount - Thirty-Eighth (added in 2.5+)
        profile.add_field_definition("IN3", 65, {
            "name": "Certification Value/Amount - Thirty-Eighth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-66: Certification Value/Amount - Thirty-Ninth (added in 2.5+)
        profile.add_field_definition("IN3", 66, {
            "name": "Certification Value/Amount - Thirty-Ninth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-67: Certification Value/Amount - Fortieth (added in 2.5+)
        profile.add_field_definition("IN3", 67, {
            "name": "Certification Value/Amount - Fortieth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-68: Certification Value/Amount - Forty-First (added in 2.5+)
        profile.add_field_definition("IN3", 68, {
            "name": "Certification Value/Amount - Forty-First",
            "data_type": "CP",
            "required": False,
        })
        # IN3-69: Certification Value/Amount - Forty-Second (added in 2.5+)
        profile.add_field_definition("IN3", 69, {
            "name": "Certification Value/Amount - Forty-Second",
            "data_type": "CP",
            "required": False,
        })
        # IN3-70: Certification Value/Amount - Forty-Third (added in 2.5+)
        profile.add_field_definition("IN3", 70, {
            "name": "Certification Value/Amount - Forty-Third",
            "data_type": "CP",
            "required": False,
        })
        # IN3-71: Certification Value/Amount - Forty-Fourth (added in 2.5+)
        profile.add_field_definition("IN3", 71, {
            "name": "Certification Value/Amount - Forty-Fourth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-72: Certification Value/Amount - Forty-Fifth (added in 2.5+)
        profile.add_field_definition("IN3", 72, {
            "name": "Certification Value/Amount - Forty-Fifth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-73: Certification Value/Amount - Forty-Sixth (added in 2.5+)
        profile.add_field_definition("IN3", 73, {
            "name": "Certification Value/Amount - Forty-Sixth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-74: Certification Value/Amount - Forty-Seventh (added in 2.5+)
        profile.add_field_definition("IN3", 74, {
            "name": "Certification Value/Amount - Forty-Seventh",
            "data_type": "CP",
            "required": False,
        })
        # IN3-75: Certification Value/Amount - Forty-Eighth (added in 2.5+)
        profile.add_field_definition("IN3", 75, {
            "name": "Certification Value/Amount - Forty-Eighth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-76: Certification Value/Amount - Forty-Ninth (added in 2.5+)
        profile.add_field_definition("IN3", 76, {
            "name": "Certification Value/Amount - Forty-Ninth",
            "data_type": "CP",
            "required": False,
        })
        # IN3-77: Certification Value/Amount - Fiftieth (added in 2.5+)
        profile.add_field_definition("IN3", 77, {
            "name": "Certification Value/Amount - Fiftieth",
            "data_type": "CP",
            "required": False,
        })
    
    # GT1 segment definition (Guarantor)
    profile.add_segment_definition("GT1", {
        "name": "GT1",
        "description": "Guarantor",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # GT1-1: Set ID - GT1 (all versions)
    profile.add_field_definition("GT1", 1, {
        "name": "Set ID - GT1",
        "data_type": "SI",
        "required": False,
    })
    
    # GT1-2: Guarantor Number (all versions)
    profile.add_field_definition("GT1", 2, {
        "name": "Guarantor Number",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-3: Guarantor Name (all versions)
    profile.add_field_definition("GT1", 3, {
        "name": "Guarantor Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-4: Guarantor Spouse Name (all versions)
    profile.add_field_definition("GT1", 4, {
        "name": "Guarantor Spouse Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-5: Guarantor Address (all versions)
    profile.add_field_definition("GT1", 5, {
        "name": "Guarantor Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-6: Guarantor Ph Num - Home (all versions)
    profile.add_field_definition("GT1", 6, {
        "name": "Guarantor Ph Num - Home",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-7: Guarantor Ph Num - Business (all versions)
    profile.add_field_definition("GT1", 7, {
        "name": "Guarantor Ph Num - Business",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-8: Guarantor Date/Time Of Birth (all versions)
    profile.add_field_definition("GT1", 8, {
        "name": "Guarantor Date/Time Of Birth",
        "data_type": "TS",
        "required": False,
    })
    
    # GT1-9: Guarantor Administrative Sex (all versions)
    profile.add_field_definition("GT1", 9, {
        "name": "Guarantor Administrative Sex",
        "data_type": "IS",
        "required": False,
        "table": "0001",  # Administrative Sex table
    })
    
    # GT1-10: Guarantor Type (all versions)
    profile.add_field_definition("GT1", 10, {
        "name": "Guarantor Type",
        "data_type": "IS",
        "required": False,
        "table": "0068",  # Guarantor Type table
    })
    
    # GT1-11: Guarantor Relationship (all versions)
    profile.add_field_definition("GT1", 11, {
        "name": "Guarantor Relationship",
        "data_type": "CE",
        "required": False,
        "table": "0063",  # Relationship table
    })
    
    # GT1-12: Guarantor SSN (all versions)
    profile.add_field_definition("GT1", 12, {
        "name": "Guarantor SSN",
        "data_type": "ST",
        "required": False,
    })
    
    # GT1-13: Guarantor Date - Begin (all versions)
    profile.add_field_definition("GT1", 13, {
        "name": "Guarantor Date - Begin",
        "data_type": "DT",
        "required": False,
    })
    
    # GT1-14: Guarantor Date - End (all versions)
    profile.add_field_definition("GT1", 14, {
        "name": "Guarantor Date - End",
        "data_type": "DT",
        "required": False,
    })
    
    # GT1-15: Guarantor Priority (all versions)
    profile.add_field_definition("GT1", 15, {
        "name": "Guarantor Priority",
        "data_type": "NM",
        "required": False,
    })
    
    # GT1-16: Guarantor Employer Name (all versions)
    profile.add_field_definition("GT1", 16, {
        "name": "Guarantor Employer Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-17: Guarantor Employer Address (all versions)
    profile.add_field_definition("GT1", 17, {
        "name": "Guarantor Employer Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-18: Guarantor Employer Phone Number (all versions)
    profile.add_field_definition("GT1", 18, {
        "name": "Guarantor Employer Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-19: Guarantor Employee ID Number (all versions)
    profile.add_field_definition("GT1", 19, {
        "name": "Guarantor Employee ID Number",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-20: Guarantor Employment Status (all versions)
    profile.add_field_definition("GT1", 20, {
        "name": "Guarantor Employment Status",
        "data_type": "CE",
        "required": False,
        "table": "0066",  # Employment Status table
    })
    
    # GT1-21: Guarantor Organization Name (all versions)
    profile.add_field_definition("GT1", 21, {
        "name": "Guarantor Organization Name",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-22: Guarantor Billing Hold Flag (all versions)
    profile.add_field_definition("GT1", 22, {
        "name": "Guarantor Billing Hold Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # GT1-23: Guarantor Credit Rating Code (all versions)
    profile.add_field_definition("GT1", 23, {
        "name": "Guarantor Credit Rating Code",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-24: Guarantor Death Date And Time (all versions)
    profile.add_field_definition("GT1", 24, {
        "name": "Guarantor Death Date And Time",
        "data_type": "TS",
        "required": False,
    })
    
    # GT1-25: Guarantor Death Flag (all versions)
    profile.add_field_definition("GT1", 25, {
        "name": "Guarantor Death Flag",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # GT1-26: Guarantor Charge Adjustment Code (all versions)
    profile.add_field_definition("GT1", 26, {
        "name": "Guarantor Charge Adjustment Code",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-27: Guarantor Household Annual Income (all versions)
    profile.add_field_definition("GT1", 27, {
        "name": "Guarantor Household Annual Income",
        "data_type": "CP",
        "required": False,
    })
    
    # GT1-28: Guarantor Household Size (all versions)
    profile.add_field_definition("GT1", 28, {
        "name": "Guarantor Household Size",
        "data_type": "NM",
        "required": False,
    })
    
    # GT1-29: Guarantor Employer ID Number (all versions)
    profile.add_field_definition("GT1", 29, {
        "name": "Guarantor Employer ID Number",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-30: Guarantor Marital Status Code (all versions)
    profile.add_field_definition("GT1", 30, {
        "name": "Guarantor Marital Status Code",
        "data_type": "CE",
        "required": False,
        "table": "0002",  # Marital Status table
    })
    
    # GT1-31: Guarantor Hire Effective Date (all versions)
    profile.add_field_definition("GT1", 31, {
        "name": "Guarantor Hire Effective Date",
        "data_type": "DT",
        "required": False,
    })
    
    # GT1-32: Employment Stop Date (all versions)
    profile.add_field_definition("GT1", 32, {
        "name": "Employment Stop Date",
        "data_type": "DT",
        "required": False,
    })
    
    # GT1-33: Living Dependency (all versions)
    profile.add_field_definition("GT1", 33, {
        "name": "Living Dependency",
        "data_type": "IS",
        "required": False,
        "table": "0223",  # Living Dependency table
    })
    
    # GT1-34: Ambulatory Status (all versions)
    profile.add_field_definition("GT1", 34, {
        "name": "Ambulatory Status",
        "data_type": "IS",
        "required": False,
        "table": "0009",  # Ambulatory Status table
    })
    
    # GT1-35: Citizenship (all versions)
    profile.add_field_definition("GT1", 35, {
        "name": "Citizenship",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-36: Primary Language (all versions)
    profile.add_field_definition("GT1", 36, {
        "name": "Primary Language",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-37: Living Arrangement (all versions)
    profile.add_field_definition("GT1", 37, {
        "name": "Living Arrangement",
        "data_type": "IS",
        "required": False,
        "table": "0220",  # Living Arrangement table
    })
    
    # GT1-38: Publicity Code (all versions)
    profile.add_field_definition("GT1", 38, {
        "name": "Publicity Code",
        "data_type": "CE",
        "required": False,
        "table": "0215",  # Publicity Code table
    })
    
    # GT1-39: Protection Indicator (all versions)
    profile.add_field_definition("GT1", 39, {
        "name": "Protection Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # GT1-40: Student Indicator (all versions)
    profile.add_field_definition("GT1", 40, {
        "name": "Student Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0231",  # Student Indicator table (reusing 0231)
    })
    
    # GT1-41: Religion (all versions)
    profile.add_field_definition("GT1", 41, {
        "name": "Religion",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-42: Mother's Maiden Name (all versions)
    profile.add_field_definition("GT1", 42, {
        "name": "Mother's Maiden Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-43: Nationality (all versions)
    profile.add_field_definition("GT1", 43, {
        "name": "Nationality",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-44: Guarantor Ethnic Group (all versions)
    profile.add_field_definition("GT1", 44, {
        "name": "Guarantor Ethnic Group",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-45: Contact Person's Name (all versions)
    profile.add_field_definition("GT1", 45, {
        "name": "Contact Person's Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-46: Contact Person's Phone Number (all versions)
    profile.add_field_definition("GT1", 46, {
        "name": "Contact Person's Phone Number",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-47: Contact Person's Address (all versions)
    profile.add_field_definition("GT1", 47, {
        "name": "Contact Person's Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-48: Contact Person's Relationship (all versions)
    profile.add_field_definition("GT1", 48, {
        "name": "Contact Person's Relationship",
        "data_type": "CE",
        "required": False,
        "table": "0063",  # Relationship table
    })
    
    # GT1-49: Contact Person's SSN (all versions)
    profile.add_field_definition("GT1", 49, {
        "name": "Contact Person's SSN",
        "data_type": "ST",
        "required": False,
    })
    
    # GT1-50: Next Of Kin / Associated Party's Identifiers (all versions)
    profile.add_field_definition("GT1", 50, {
        "name": "Next Of Kin / Associated Party's Identifiers",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # GT1-51: Job Status (all versions)
    profile.add_field_definition("GT1", 51, {
        "name": "Job Status",
        "data_type": "IS",
        "required": False,
        "table": "0311",  # Job Status table
    })
    
    # GT1-52: Race (all versions)
    profile.add_field_definition("GT1", 52, {
        "name": "Race",
        "data_type": "CE",
        "required": False,
    })
    
    # GT1-53: Contact Person's Race (all versions)
    profile.add_field_definition("GT1", 53, {
        "name": "Contact Person's Race",
        "data_type": "CE",
        "required": False,
    })
    
    # Version-specific GT1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # GT1-54: Contact Person's Birth Place (added in 2.5+)
        profile.add_field_definition("GT1", 54, {
            "name": "Contact Person's Birth Place",
            "data_type": "ST",
            "required": False,
        })
    
    # ROL segment definition (Role)
    profile.add_segment_definition("ROL", {
        "name": "ROL",
        "description": "Role",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # ROL-1: Role Instance ID (all versions)
    profile.add_field_definition("ROL", 1, {
        "name": "Role Instance ID",
        "data_type": "EI",
        "required": False,
    })
    
    # ROL-2: Action Code (all versions)
    profile.add_field_definition("ROL", 2, {
        "name": "Action Code",
        "data_type": "ID",
        "required": False,
        "table": "0287",  # Action Code table
    })
    
    # ROL-3: Role-ROL (all versions)
    profile.add_field_definition("ROL", 3, {
        "name": "Role-ROL",
        "data_type": "CE",
        "required": False,
        "table": "0443",  # Role table
    })
    
    # ROL-4: Role Person (all versions)
    profile.add_field_definition("ROL", 4, {
        "name": "Role Person",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ROL-5: Role Begin Date/Time (all versions)
    profile.add_field_definition("ROL", 5, {
        "name": "Role Begin Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # ROL-6: Role End Date/Time (all versions)
    profile.add_field_definition("ROL", 6, {
        "name": "Role End Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # ROL-7: Role Duration (all versions)
    profile.add_field_definition("ROL", 7, {
        "name": "Role Duration",
        "data_type": "CE",
        "required": False,
    })
    
    # ROL-8: Role Action Reason (all versions)
    profile.add_field_definition("ROL", 8, {
        "name": "Role Action Reason",
        "data_type": "CE",
        "required": False,
    })
    
    # ROL-9: Provider Type (all versions)
    profile.add_field_definition("ROL", 9, {
        "name": "Provider Type",
        "data_type": "CE",
        "required": False,
        "table": "0286",  # Provider Type table
    })
    
    # ROL-10: Organization Unit Type (all versions)
    profile.add_field_definition("ROL", 10, {
        "name": "Organization Unit Type",
        "data_type": "CE",
        "required": False,
        "table": "0405",  # Organization Unit Type table
    })
    
    # ROL-11: Office/Home Address/Birthplace (all versions)
    profile.add_field_definition("ROL", 11, {
        "name": "Office/Home Address/Birthplace",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # ROL-12: Phone (all versions)
    profile.add_field_definition("ROL", 12, {
        "name": "Phone",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ROL-13: Person Location (all versions)
    profile.add_field_definition("ROL", 13, {
        "name": "Person Location",
        "data_type": "PL",
        "required": False,
    })
    
    # ROL-14: Status (all versions)
    profile.add_field_definition("ROL", 14, {
        "name": "Status",
        "data_type": "IS",
        "required": False,
        "table": "0444",  # Status table
    })
    
    # CTD segment definition (Contact Data)
    profile.add_segment_definition("CTD", {
        "name": "CTD",
        "description": "Contact Data",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # CTD-1: Contact Role (all versions)
    profile.add_field_definition("CTD", 1, {
        "name": "Contact Role",
        "data_type": "CE",
        "required": False,
        "table": "0131",  # Contact Role table
    })
    
    # CTD-2: Contact Name (all versions)
    profile.add_field_definition("CTD", 2, {
        "name": "Contact Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # CTD-3: Contact Address (all versions)
    profile.add_field_definition("CTD", 3, {
        "name": "Contact Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # CTD-4: Contact Location (all versions)
    profile.add_field_definition("CTD", 4, {
        "name": "Contact Location",
        "data_type": "PL",
        "required": False,
    })
    
    # CTD-5: Contact Communication Information (all versions)
    profile.add_field_definition("CTD", 5, {
        "name": "Contact Communication Information",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # CTD-6: Preferred Method of Contact (all versions)
    profile.add_field_definition("CTD", 6, {
        "name": "Preferred Method of Contact",
        "data_type": "CE",
        "required": False,
        "table": "0185",  # Preferred Method of Contact table
    })
    
    # CTD-7: Contact Identifiers (all versions)
    profile.add_field_definition("CTD", 7, {
        "name": "Contact Identifiers",
        "data_type": "PLN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PD1 segment definition (Patient Additional Demographic)
    profile.add_segment_definition("PD1", {
        "name": "PD1",
        "description": "Patient Additional Demographic",
        "required": False,
        "max_repetitions": 1,
    })
    
    # PD1-1: Living Dependency (all versions)
    profile.add_field_definition("PD1", 1, {
        "name": "Living Dependency",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
        "table": "0223",  # Living Dependency table
    })
    
    # PD1-2: Living Arrangement (all versions)
    profile.add_field_definition("PD1", 2, {
        "name": "Living Arrangement",
        "data_type": "IS",
        "required": False,
        "table": "0220",  # Living Arrangement table
    })
    
    # PD1-3: Patient Primary Facility (all versions)
    profile.add_field_definition("PD1", 3, {
        "name": "Patient Primary Facility",
        "data_type": "XON",
        "required": False,
        "max_repetitions": None,
    })
    
    # PD1-4: Patient Primary Care Provider Name & ID No. (all versions)
    profile.add_field_definition("PD1", 4, {
        "name": "Patient Primary Care Provider Name & ID No.",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # PD1-5: Student Indicator (all versions)
    profile.add_field_definition("PD1", 5, {
        "name": "Student Indicator",
        "data_type": "IS",
        "required": False,
        "table": "0231",  # Student Status table
    })
    
    # PD1-6: Handicap (all versions)
    profile.add_field_definition("PD1", 6, {
        "name": "Handicap",
        "data_type": "IS",
        "required": False,
        "table": "0295",  # Handicap table
    })
    
    # PD1-7: Living Will Code (all versions)
    profile.add_field_definition("PD1", 7, {
        "name": "Living Will Code",
        "data_type": "IS",
        "required": False,
        "table": "0315",  # Living Will Code table
    })
    
    # PD1-8: Organ Donor Code (all versions)
    profile.add_field_definition("PD1", 8, {
        "name": "Organ Donor Code",
        "data_type": "IS",
        "required": False,
        "table": "0316",  # Organ Donor Code table
    })
    
    # PD1-9: Separate Bill (all versions)
    profile.add_field_definition("PD1", 9, {
        "name": "Separate Bill",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # PD1-10: Duplicate Patient (all versions)
    profile.add_field_definition("PD1", 10, {
        "name": "Duplicate Patient",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # PD1-11: Publicity Code (all versions)
    profile.add_field_definition("PD1", 11, {
        "name": "Publicity Code",
        "data_type": "CE",
        "required": False,
        "table": "0215",  # Publicity Code table
    })
    
    # PD1-12: Protection Indicator (all versions)
    profile.add_field_definition("PD1", 12, {
        "name": "Protection Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # Version-specific PD1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # PD1-13: Protection Indicator Effective Date (added in 2.5+)
        profile.add_field_definition("PD1", 13, {
            "name": "Protection Indicator Effective Date",
            "data_type": "DT",
            "required": False,
        })
        # PD1-14: Place of Worship (added in 2.5+)
        profile.add_field_definition("PD1", 14, {
            "name": "Place of Worship",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        # PD1-15: Advance Directive Code (added in 2.5+)
        profile.add_field_definition("PD1", 15, {
            "name": "Advance Directive Code",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
            "table": "0435",  # Advance Directive Code table
        })
        # PD1-16: Immunization Registry Status (added in 2.5+)
        profile.add_field_definition("PD1", 16, {
            "name": "Immunization Registry Status",
            "data_type": "CE",
            "required": False,
            "table": "0443",  # Immunization Registry Status table
        })
        # PD1-17: Immunization Registry Status Effective Date (added in 2.5+)
        profile.add_field_definition("PD1", 17, {
            "name": "Immunization Registry Status Effective Date",
            "data_type": "DT",
            "required": False,
        })
        # PD1-18: Publicity Code Effective Date (added in 2.5+)
        profile.add_field_definition("PD1", 18, {
            "name": "Publicity Code Effective Date",
            "data_type": "DT",
            "required": False,
        })
        # PD1-19: Military Branch (added in 2.5+)
        profile.add_field_definition("PD1", 19, {
            "name": "Military Branch",
            "data_type": "CE",
            "required": False,
            "table": "0140",  # Military Branch table
        })
        # PD1-20: Military Rank/Grade (added in 2.5+)
        profile.add_field_definition("PD1", 20, {
            "name": "Military Rank/Grade",
            "data_type": "CE",
            "required": False,
            "table": "0141",  # Military Rank/Grade table
        })
        # PD1-21: Military Status (added in 2.5+)
        profile.add_field_definition("PD1", 21, {
            "name": "Military Status",
            "data_type": "CE",
            "required": False,
            "table": "0142",  # Military Status table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # PD1-22: Advance Directive Last Verified Date (added in 2.7+)
        profile.add_field_definition("PD1", 22, {
            "name": "Advance Directive Last Verified Date",
            "data_type": "DT",
            "required": False,
        })
    
    # FT1 segment definition (Financial Transaction)
    profile.add_segment_definition("FT1", {
        "name": "FT1",
        "description": "Financial Transaction",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # FT1-1: Set ID - FT1 (all versions)
    profile.add_field_definition("FT1", 1, {
        "name": "Set ID - FT1",
        "data_type": "SI",
        "required": False,
    })
    
    # FT1-2: Transaction ID (all versions)
    profile.add_field_definition("FT1", 2, {
        "name": "Transaction ID",
        "data_type": "ST",
        "required": False,
    })
    
    # FT1-3: Transaction Batch ID (all versions)
    profile.add_field_definition("FT1", 3, {
        "name": "Transaction Batch ID",
        "data_type": "ST",
        "required": False,
    })
    
    # FT1-4: Transaction Date (all versions)
    profile.add_field_definition("FT1", 4, {
        "name": "Transaction Date",
        "data_type": "DR",
        "required": False,
    })
    
    # FT1-5: Transaction Posting Date (all versions)
    profile.add_field_definition("FT1", 5, {
        "name": "Transaction Posting Date",
        "data_type": "TS",
        "required": False,
    })
    
    # FT1-6: Transaction Type (all versions)
    profile.add_field_definition("FT1", 6, {
        "name": "Transaction Type",
        "data_type": "IS",
        "required": False,
        "table": "0017",  # Transaction Type table
    })
    
    # FT1-7: Transaction Code (all versions)
    profile.add_field_definition("FT1", 7, {
        "name": "Transaction Code",
        "data_type": "CE",
        "required": True,
        "table": "0132",  # Transaction Code table
    })
    
    # FT1-8: Transaction Description (all versions)
    profile.add_field_definition("FT1", 8, {
        "name": "Transaction Description",
        "data_type": "ST",
        "required": False,
    })
    
    # FT1-9: Transaction Description - Alt (all versions)
    profile.add_field_definition("FT1", 9, {
        "name": "Transaction Description - Alt",
        "data_type": "ST",
        "required": False,
    })
    
    # FT1-10: Transaction Quantity (all versions)
    profile.add_field_definition("FT1", 10, {
        "name": "Transaction Quantity",
        "data_type": "NM",
        "required": False,
    })
    
    # FT1-11: Transaction Amount - Extended (all versions)
    profile.add_field_definition("FT1", 11, {
        "name": "Transaction Amount - Extended",
        "data_type": "CP",
        "required": False,
    })
    
    # FT1-12: Transaction Quantity Units (all versions)
    profile.add_field_definition("FT1", 12, {
        "name": "Transaction Quantity Units",
        "data_type": "CE",
        "required": False,
    })
    
    # FT1-13: Department Code (all versions)
    profile.add_field_definition("FT1", 13, {
        "name": "Department Code",
        "data_type": "CE",
        "required": False,
        "table": "0049",  # Department Code table
    })
    
    # FT1-14: Insurance Plan ID (all versions)
    profile.add_field_definition("FT1", 14, {
        "name": "Insurance Plan ID",
        "data_type": "CE",
        "required": False,
        "table": "0072",  # Insurance Plan ID table
    })
    
    # FT1-15: Insurance Amount (all versions)
    profile.add_field_definition("FT1", 15, {
        "name": "Insurance Amount",
        "data_type": "CP",
        "required": False,
    })
    
    # FT1-16: Assigned Patient Location (all versions)
    profile.add_field_definition("FT1", 16, {
        "name": "Assigned Patient Location",
        "data_type": "PL",
        "required": False,
    })
    
    # FT1-17: Fee Schedule (all versions)
    profile.add_field_definition("FT1", 17, {
        "name": "Fee Schedule",
        "data_type": "IS",
        "required": False,
        "table": "0024",  # Fee Schedule table
    })
    
    # FT1-18: Patient Type (all versions)
    profile.add_field_definition("FT1", 18, {
        "name": "Patient Type",
        "data_type": "CE",
        "required": False,
        "table": "0018",  # Patient Type table
    })
    
    # FT1-19: Diagnosis Code - FT1 (all versions)
    profile.add_field_definition("FT1", 19, {
        "name": "Diagnosis Code - FT1",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
        "table": "0051",  # Diagnosis Code table
    })
    
    # FT1-20: Performed By Code (all versions)
    profile.add_field_definition("FT1", 20, {
        "name": "Performed By Code",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific FT1 fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # FT1-21: Ordered By Code (added in 2.5+)
        profile.add_field_definition("FT1", 21, {
            "name": "Ordered By Code",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
        # FT1-22: Unit Cost (added in 2.5+)
        profile.add_field_definition("FT1", 22, {
            "name": "Unit Cost",
            "data_type": "CP",
            "required": False,
        })
        # FT1-23: Filler Order Number (added in 2.5+)
        profile.add_field_definition("FT1", 23, {
            "name": "Filler Order Number",
            "data_type": "EI",
            "required": False,
        })
        # FT1-24: Entered By Code (added in 2.5+)
        profile.add_field_definition("FT1", 24, {
            "name": "Entered By Code",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
        # FT1-25: Procedure Code (added in 2.5+)
        profile.add_field_definition("FT1", 25, {
            "name": "Procedure Code",
            "data_type": "CE",
            "required": False,
            "table": "0088",  # Procedure Code table
        })
        # FT1-26: Procedure Code Modifier (added in 2.5+)
        profile.add_field_definition("FT1", 26, {
            "name": "Procedure Code Modifier",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
            "table": "0340",  # Procedure Code Modifier table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # FT1-27: Advanced Beneficiary Notice Code (added in 2.7+)
        profile.add_field_definition("FT1", 27, {
            "name": "Advanced Beneficiary Notice Code",
            "data_type": "CE",
            "required": False,
            "table": "0339",  # Advanced Beneficiary Notice Code table
        })
        # FT1-28: Medically Necessary Duplicate Procedure Reason (added in 2.7+)
        profile.add_field_definition("FT1", 28, {
            "name": "Medically Necessary Duplicate Procedure Reason",
            "data_type": "CWE",
            "required": False,
            "table": "0476",  # Medically Necessary Duplicate Procedure Reason table
        })
        # FT1-29: NDC Code (added in 2.7+)
        profile.add_field_definition("FT1", 29, {
            "name": "NDC Code",
            "data_type": "CWE",
            "required": False,
        })
        # FT1-30: Payment Reference ID (added in 2.7+)
        profile.add_field_definition("FT1", 30, {
            "name": "Payment Reference ID",
            "data_type": "CX",
            "required": False,
            "max_repetitions": None,
        })
    
    # SFT segment definition (Software - added in 2.5+)
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        _add_version_specific_segment_definition(
            profile,
            "SFT",
            {
                "name": "SFT",
                "description": "Software Segment",
                "required": False,
                "max_repetitions": None,  # Unlimited repetitions
            },
            versions=["2.5", "2.6", "2.7", "2.8", "2.9"]
        )
        
        # SFT-1: Software Vendor Organization (all versions 2.5+)
        profile.add_field_definition("SFT", 1, {
            "name": "Software Vendor Organization",
            "data_type": "XON",
            "required": False,
        })
        
        # SFT-2: Software Certified Version or Release Number (all versions 2.5+)
        profile.add_field_definition("SFT", 2, {
            "name": "Software Certified Version or Release Number",
            "data_type": "ST",
            "required": False,
        })
        
        # SFT-3: Software Product Name (all versions 2.5+)
        profile.add_field_definition("SFT", 3, {
            "name": "Software Product Name",
            "data_type": "ST",
            "required": False,
        })
        
        # SFT-4: Software Binary ID (all versions 2.5+)
        profile.add_field_definition("SFT", 4, {
            "name": "Software Binary ID",
            "data_type": "ST",
            "required": False,
        })
        
        # SFT-5: Software Product Information (all versions 2.5+)
        profile.add_field_definition("SFT", 5, {
            "name": "Software Product Information",
            "data_type": "TX",
            "required": False,
        })
        
        # SFT-6: Software Install Date (all versions 2.5+)
        profile.add_field_definition("SFT", 6, {
            "name": "Software Install Date",
            "data_type": "TS",
            "required": False,
        })
    
    # SPM segment definition (Specimen - added in 2.5+)
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        _add_version_specific_segment_definition(
            profile,
            "SPM",
            {
                "name": "SPM",
                "description": "Specimen",
                "required": False,
                "max_repetitions": None,
            },
            versions=["2.5", "2.6", "2.7", "2.8", "2.9"]
        )
        
        # SPM-1: Set ID (all versions 2.5+)
        profile.add_field_definition("SPM", 1, {
            "name": "Set ID",
            "data_type": "SI",
            "required": False,
        })
        
        # SPM-2: Specimen ID (all versions 2.5+)
        profile.add_field_definition("SPM", 2, {
            "name": "Specimen ID",
            "data_type": "EIP",
            "required": False,
            "max_repetitions": None,
        })
        
        # SPM-3: Specimen Parent IDs (all versions 2.5+)
        profile.add_field_definition("SPM", 3, {
            "name": "Specimen Parent IDs",
            "data_type": "EIP",
            "required": False,
            "max_repetitions": None,
        })
        
        # SPM-4: Specimen Type (all versions 2.5+)
        profile.add_field_definition("SPM", 4, {
            "name": "Specimen Type",
            "data_type": "CWE",
            "required": True,
            "table": "0487",  # Specimen Type table
        })
        
        # SPM-5: Specimen Type Modifier (all versions 2.5+)
        profile.add_field_definition("SPM", 5, {
            "name": "Specimen Type Modifier",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0541",  # Specimen Type Modifier table
        })
        
        # SPM-6: Specimen Additives (all versions 2.5+)
        profile.add_field_definition("SPM", 6, {
            "name": "Specimen Additives",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0371",  # Additive/Preservative table
        })
        
        # SPM-7: Specimen Collection Method (all versions 2.5+)
        profile.add_field_definition("SPM", 7, {
            "name": "Specimen Collection Method",
            "data_type": "CWE",
            "required": False,
            "table": "0488",  # Specimen Collection Method table
        })
        
        # SPM-8: Specimen Source Site (all versions 2.5+)
        profile.add_field_definition("SPM", 8, {
            "name": "Specimen Source Site",
            "data_type": "CWE",
            "required": False,
            "table": "0542",  # Source of Specimen table
        })
        
        # SPM-9: Specimen Source Site Modifier (all versions 2.5+)
        profile.add_field_definition("SPM", 9, {
            "name": "Specimen Source Site Modifier",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0543",  # Specimen Source Site Modifier table
        })
        
        # SPM-10: Specimen Collection Site (all versions 2.5+)
        profile.add_field_definition("SPM", 10, {
            "name": "Specimen Collection Site",
            "data_type": "CWE",
            "required": False,
            "table": "0544",  # Collection Method Modifier Code table
        })
        
        # SPM-11: Specimen Role (all versions 2.5+)
        profile.add_field_definition("SPM", 11, {
            "name": "Specimen Role",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0369",  # Specimen Role table
        })
        
        # SPM-12: Specimen Collection Amount (all versions 2.5+)
        profile.add_field_definition("SPM", 12, {
            "name": "Specimen Collection Amount",
            "data_type": "CQ",
            "required": False,
        })
        
        # SPM-13: Grouped Specimen Count (all versions 2.5+)
        profile.add_field_definition("SPM", 13, {
            "name": "Grouped Specimen Count",
            "data_type": "NM",
            "required": False,
        })
        
        # SPM-14: Specimen Description (all versions 2.5+)
        profile.add_field_definition("SPM", 14, {
            "name": "Specimen Description",
            "data_type": "ST",
            "required": False,
            "max_repetitions": None,
        })
        
        # SPM-15: Specimen Handling Code (all versions 2.5+)
        profile.add_field_definition("SPM", 15, {
            "name": "Specimen Handling Code",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0376",  # Specimen Handling Code table
        })
        
        # SPM-16: Specimen Risk Code (all versions 2.5+)
        profile.add_field_definition("SPM", 16, {
            "name": "Specimen Risk Code",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0489",  # Specimen Risk Code table
        })
        
        # SPM-17: Specimen Collection Date/Time (all versions 2.5+)
        profile.add_field_definition("SPM", 17, {
            "name": "Specimen Collection Date/Time",
            "data_type": "DR",
            "required": False,
        })
        
        # SPM-18: Specimen Received Date/Time (all versions 2.5+)
        profile.add_field_definition("SPM", 18, {
            "name": "Specimen Received Date/Time",
            "data_type": "TS",
            "required": False,
        })
        
        # SPM-19: Specimen Expiration Date/Time (all versions 2.5+)
        profile.add_field_definition("SPM", 19, {
            "name": "Specimen Expiration Date/Time",
            "data_type": "TS",
            "required": False,
        })
        
        # SPM-20: Specimen Availability (all versions 2.5+)
        profile.add_field_definition("SPM", 20, {
            "name": "Specimen Availability",
            "data_type": "ID",
            "required": False,
            "table": "0136",  # Yes/No Indicator table
        })
        
        # SPM-21: Specimen Reject Reason (all versions 2.5+)
        profile.add_field_definition("SPM", 21, {
            "name": "Specimen Reject Reason",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0490",  # Specimen Reject Reason table
        })
        
        # SPM-22: Specimen Quality (all versions 2.5+)
        profile.add_field_definition("SPM", 22, {
            "name": "Specimen Quality",
            "data_type": "CWE",
            "required": False,
            "table": "0491",  # Specimen Quality table
        })
        
        # SPM-23: Specimen Appropriateness (all versions 2.5+)
        profile.add_field_definition("SPM", 23, {
            "name": "Specimen Appropriateness",
            "data_type": "CWE",
            "required": False,
            "table": "0492",  # Specimen Appropriateness table
        })
        
        # SPM-24: Specimen Condition (all versions 2.5+)
        profile.add_field_definition("SPM", 24, {
            "name": "Specimen Condition",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0493",  # Specimen Condition table
        })
        
        # SPM-25: Specimen Current Quantity (all versions 2.5+)
        profile.add_field_definition("SPM", 25, {
            "name": "Specimen Current Quantity",
            "data_type": "CQ",
            "required": False,
        })
        
        # SPM-26: Number of Specimen Containers (all versions 2.5+)
        profile.add_field_definition("SPM", 26, {
            "name": "Number of Specimen Containers",
            "data_type": "NM",
            "required": False,
        })
        
        # SPM-27: Container Type (all versions 2.5+)
        profile.add_field_definition("SPM", 27, {
            "name": "Container Type",
            "data_type": "CWE",
            "required": False,
            "table": "0374",  # Container Type table
        })
        
        # SPM-28: Container Condition (all versions 2.5+)
        profile.add_field_definition("SPM", 28, {
            "name": "Container Condition",
            "data_type": "CWE",
            "required": False,
            "table": "0545",  # Container Condition table
        })
        
        # SPM-29: Specimen Child Role (all versions 2.5+)
        profile.add_field_definition("SPM", 29, {
            "name": "Specimen Child Role",
            "data_type": "CWE",
            "required": False,
            "table": "0369",  # Specimen Role table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # SPM-30: Accession ID (added in 2.7+)
        profile.add_field_definition("SPM", 30, {
            "name": "Accession ID",
            "data_type": "CX",
            "required": False,
            "max_repetitions": None,
        })
        
        # SPM-31: Other Specimen ID (added in 2.7+)
        profile.add_field_definition("SPM", 31, {
            "name": "Other Specimen ID",
            "data_type": "CX",
            "required": False,
            "max_repetitions": None,
        })
        
        # SPM-32: Shipment ID (added in 2.7+)
        profile.add_field_definition("SPM", 32, {
            "name": "Shipment ID",
            "data_type": "EI",
            "required": False,
        })
    
    # MRG segment definition (Merge Patient Information)
    profile.add_segment_definition("MRG", {
        "name": "MRG",
        "description": "Merge Patient Information",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # MRG-1: Prior Patient Identifier List (all versions)
    profile.add_field_definition("MRG", 1, {
        "name": "Prior Patient Identifier List",
        "data_type": "CX",
        "required": True,
        "max_repetitions": None,
    })
    
    # MRG-2: Prior Alternate Patient ID (all versions, deprecated in 2.3+)
    profile.add_field_definition("MRG", 2, {
        "name": "Prior Alternate Patient ID",
        "data_type": "CX",
        "required": False,
        "max_repetitions": None,
    })
    
    # MRG-3: Prior Patient Account Number (all versions)
    profile.add_field_definition("MRG", 3, {
        "name": "Prior Patient Account Number",
        "data_type": "CX",
        "required": False,
    })
    
    # MRG-4: Prior Patient ID (all versions, deprecated in 2.3+)
    profile.add_field_definition("MRG", 4, {
        "name": "Prior Patient ID",
        "data_type": "CX",
        "required": False,
    })
    
    # MRG-5: Prior Visit Number (all versions)
    profile.add_field_definition("MRG", 5, {
        "name": "Prior Visit Number",
        "data_type": "CX",
        "required": False,
    })
    
    # MRG-6: Prior Alternate Visit ID (all versions)
    profile.add_field_definition("MRG", 6, {
        "name": "Prior Alternate Visit ID",
        "data_type": "CX",
        "required": False,
    })
    
    # MRG-7: Prior Patient Name (all versions)
    profile.add_field_definition("MRG", 7, {
        "name": "Prior Patient Name",
        "data_type": "XPN",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific MRG fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # MRG-8: Prior Patient Alias (added in 2.5+)
        profile.add_field_definition("MRG", 8, {
            "name": "Prior Patient Alias",
            "data_type": "XPN",
            "required": False,
            "max_repetitions": None,
        })
        # MRG-9: Prior Patient Social Security Number (added in 2.5+)
        profile.add_field_definition("MRG", 9, {
            "name": "Prior Patient Social Security Number",
            "data_type": "ST",
            "required": False,
        })
        # MRG-10: Prior Patient Mother's Maiden Name (added in 2.5+)
        profile.add_field_definition("MRG", 10, {
            "name": "Prior Patient Mother's Maiden Name",
            "data_type": "XPN",
            "required": False,
            "max_repetitions": None,
        })
        # MRG-11: Prior Patient Race (added in 2.5+)
        profile.add_field_definition("MRG", 11, {
            "name": "Prior Patient Race",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
            "table": "0005",  # Race table
        })
        # MRG-12: Prior Patient Address (added in 2.5+)
        profile.add_field_definition("MRG", 12, {
            "name": "Prior Patient Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
    
    # ERR segment definition (Error)
    profile.add_segment_definition("ERR", {
        "name": "ERR",
        "description": "Error",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # ERR-1: Error Code and Location (all versions)
    profile.add_field_definition("ERR", 1, {
        "name": "Error Code and Location",
        "data_type": "ELD",
        "required": False,
        "max_repetitions": None,
    })
    
    # ERR-2: Error Location (versions 2.3-2.4 only, deprecated in 2.5+)
    if version in ("2.3", "2.4"):
        profile.add_field_definition("ERR", 2, {
            "name": "Error Location",
            "data_type": "ERL",
            "required": False,
            "max_repetitions": None,
        })
    
    # ERR-3: HL7 Error Code (all versions)
    profile.add_field_definition("ERR", 3, {
        "name": "HL7 Error Code",
        "data_type": "CWE",
        "required": False,
        "table": "0357",  # HL7 Error Code table
    })
    
    # ERR-4: Severity (all versions)
    profile.add_field_definition("ERR", 4, {
        "name": "Severity",
        "data_type": "ID",
        "required": False,
        "table": "0516",  # Error Severity table
    })
    
    # ERR-5: Application Error Code (all versions)
    profile.add_field_definition("ERR", 5, {
        "name": "Application Error Code",
        "data_type": "CWE",
        "required": False,
    })
    
    # ERR-6: Application Error Parameter (all versions)
    profile.add_field_definition("ERR", 6, {
        "name": "Application Error Parameter",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # ERR-7: Diagnostic Information (all versions)
    profile.add_field_definition("ERR", 7, {
        "name": "Diagnostic Information",
        "data_type": "TX",
        "required": False,
    })
    
    # ERR-8: User Message (all versions)
    profile.add_field_definition("ERR", 8, {
        "name": "User Message",
        "data_type": "TX",
        "required": False,
    })
    
    # ERR-9: Inform Person Indicator (all versions)
    profile.add_field_definition("ERR", 9, {
        "name": "Inform Person Indicator",
        "data_type": "CWE",
        "required": False,
        "table": "0517",  # Inform Person Code table
    })
    
    # ERR-10: Override Type (all versions)
    profile.add_field_definition("ERR", 10, {
        "name": "Override Type",
        "data_type": "CWE",
        "required": False,
        "table": "0518",  # Override Type table
    })
    
    # ERR-11: Override Reason Code (all versions)
    profile.add_field_definition("ERR", 11, {
        "name": "Override Reason Code",
        "data_type": "CWE",
        "required": False,
        "max_repetitions": None,
    })
    
    # ERR-12: Help Desk Contact Point (all versions)
    profile.add_field_definition("ERR", 12, {
        "name": "Help Desk Contact Point",
        "data_type": "XTN",
        "required": False,
        "max_repetitions": None,
    })
    
    # TQ1 segment definition (Timing/Quantity)
    profile.add_segment_definition("TQ1", {
        "name": "TQ1",
        "description": "Timing/Quantity",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # TQ1-1: Set ID (all versions)
    profile.add_field_definition("TQ1", 1, {
        "name": "Set ID",
        "data_type": "SI",
        "required": False,
    })
    
    # TQ1-2: Quantity (all versions)
    profile.add_field_definition("TQ1", 2, {
        "name": "Quantity",
        "data_type": "CQ",
        "required": False,
    })
    
    # TQ1-3: Repeat Pattern (all versions)
    profile.add_field_definition("TQ1", 3, {
        "name": "Repeat Pattern",
        "data_type": "RPT",
        "required": False,
        "max_repetitions": None,
    })
    
    # TQ1-4: Explicit Time (all versions)
    profile.add_field_definition("TQ1", 4, {
        "name": "Explicit Time",
        "data_type": "TM",
        "required": False,
        "max_repetitions": None,
    })
    
    # TQ1-5: Relative Time and Units (all versions)
    profile.add_field_definition("TQ1", 5, {
        "name": "Relative Time and Units",
        "data_type": "CQ",
        "required": False,
        "max_repetitions": None,
    })
    
    # TQ1-6: Service Duration (all versions)
    profile.add_field_definition("TQ1", 6, {
        "name": "Service Duration",
        "data_type": "CQ",
        "required": False,
    })
    
    # TQ1-7: Start Date/Time (all versions)
    profile.add_field_definition("TQ1", 7, {
        "name": "Start Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # TQ1-8: End Date/Time (all versions)
    profile.add_field_definition("TQ1", 8, {
        "name": "End Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # TQ1-9: Priority (all versions)
    profile.add_field_definition("TQ1", 9, {
        "name": "Priority",
        "data_type": "CWE",
        "required": False,
        "table": "0485",  # Priority table
    })
    
    # TQ1-10: Condition Text (all versions)
    profile.add_field_definition("TQ1", 10, {
        "name": "Condition Text",
        "data_type": "TX",
        "required": False,
    })
    
    # TQ1-11: Text Instruction (all versions)
    profile.add_field_definition("TQ1", 11, {
        "name": "Text Instruction",
        "data_type": "TX",
        "required": False,
    })
    
    # TQ1-12: Conjunction (all versions)
    profile.add_field_definition("TQ1", 12, {
        "name": "Conjunction",
        "data_type": "ID",
        "required": False,
        "table": "0472",  # Conjunction table
    })
    
    # TQ1-13: Occurrence Duration (all versions)
    profile.add_field_definition("TQ1", 13, {
        "name": "Occurrence Duration",
        "data_type": "CQ",
        "required": False,
    })
    
    # TQ1-14: Total Occurrences (all versions)
    profile.add_field_definition("TQ1", 14, {
        "name": "Total Occurrences",
        "data_type": "NM",
        "required": False,
    })
    
    # TQ2 segment definition (Timing/Quantity Relationship - added in 2.3+)
    if version in ("2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"):
        profile.add_segment_definition("TQ2", {
            "name": "TQ2",
            "description": "Timing/Quantity Relationship",
            "required": False,
            "max_repetitions": None,  # Unlimited repetitions
        })
        
        # TQ2-1: Set ID (all versions 2.3+)
        profile.add_field_definition("TQ2", 1, {
            "name": "Set ID",
            "data_type": "SI",
            "required": False,
        })
        
        # TQ2-2: Sequence/Results Flag (all versions 2.3+)
        profile.add_field_definition("TQ2", 2, {
            "name": "Sequence/Results Flag",
            "data_type": "ID",
            "required": False,
            "table": "0503",  # Sequence/Results Flag table
        })
        
        # TQ2-3: Related Placer Number (all versions 2.3+)
        profile.add_field_definition("TQ2", 3, {
            "name": "Related Placer Number",
            "data_type": "EI",
            "required": False,
            "max_repetitions": None,
        })
        
        # TQ2-4: Related Filler Number (all versions 2.3+)
        profile.add_field_definition("TQ2", 4, {
            "name": "Related Filler Number",
            "data_type": "EI",
            "required": False,
            "max_repetitions": None,
        })
        
        # TQ2-5: Related Quantity (all versions 2.3+)
        profile.add_field_definition("TQ2", 5, {
            "name": "Related Quantity",
            "data_type": "CQ",
            "required": False,
            "max_repetitions": None,
        })
        
        # TQ2-6: Related Interval (all versions 2.3+)
        profile.add_field_definition("TQ2", 6, {
            "name": "Related Interval",
            "data_type": "RI",
            "required": False,
            "max_repetitions": None,
        })
        
        # TQ2-7: Related Duration (all versions 2.3+)
        profile.add_field_definition("TQ2", 7, {
            "name": "Related Duration",
            "data_type": "ST",
            "required": False,
        })
        
        # TQ2-8: Related Start Date/Time (all versions 2.3+)
        profile.add_field_definition("TQ2", 8, {
            "name": "Related Start Date/Time",
            "data_type": "TS",
            "required": False,
        })
        
        # TQ2-9: Related End Date/Time (all versions 2.3+)
        profile.add_field_definition("TQ2", 9, {
            "name": "Related End Date/Time",
            "data_type": "TS",
            "required": False,
        })
        
        # TQ2-10: Related Priority (all versions 2.3+)
        profile.add_field_definition("TQ2", 10, {
            "name": "Related Priority",
            "data_type": "CWE",
            "required": False,
            "max_repetitions": None,
            "table": "0485",  # Priority table
        })
        
        # TQ2-11: Related Condition (all versions 2.3+)
        profile.add_field_definition("TQ2", 11, {
            "name": "Related Condition",
            "data_type": "ID",
            "required": False,
            "table": "0504",  # Related Condition table
        })
        
        # TQ2-12: Related Text (all versions 2.3+)
        profile.add_field_definition("TQ2", 12, {
            "name": "Related Text",
            "data_type": "TX",
            "required": False,
        })
        
        # TQ2-13: Related Text Instruction (all versions 2.3+)
        profile.add_field_definition("TQ2", 13, {
            "name": "Related Text Instruction",
            "data_type": "TX",
            "required": False,
        })
        
        # TQ2-14: Related Timing/Quantity Relationship (all versions 2.3+)
        profile.add_field_definition("TQ2", 14, {
            "name": "Related Timing/Quantity Relationship",
            "data_type": "ID",
            "required": False,
            "table": "0505",  # Timing/Quantity Relationship table
        })
        
        # TQ2-15: Related Date/Time Selection Criteria (all versions 2.3+)
        profile.add_field_definition("TQ2", 15, {
            "name": "Related Date/Time Selection Criteria",
            "data_type": "SCV",
            "required": False,
            "max_repetitions": None,
        })
        
        # TQ2-16: Related Duration (all versions 2.3+) - Note: This field appears twice in some versions
        # Keeping as defined in HL7 specification
        profile.add_field_definition("TQ2", 16, {
            "name": "Related Duration",
            "data_type": "CQ",
            "required": False,
        })
        
        # TQ2-17: Related Start Date/Time Offset (all versions 2.3+)
        profile.add_field_definition("TQ2", 17, {
            "name": "Related Start Date/Time Offset",
            "data_type": "NM",
            "required": False,
        })
        
        # TQ2-18: Related Start Date/Time Offset Units (all versions 2.3+)
        profile.add_field_definition("TQ2", 18, {
            "name": "Related Start Date/Time Offset Units",
            "data_type": "CE",
            "required": False,
        })
        
        # TQ2-19: Related Duration Range (all versions 2.3+)
        profile.add_field_definition("TQ2", 19, {
            "name": "Related Duration Range",
            "data_type": "CQ",
            "required": False,
            "max_repetitions": None,
        })
        
        # TQ2-20: Related Duration Range Units (all versions 2.3+)
        profile.add_field_definition("TQ2", 20, {
            "name": "Related Duration Range Units",
            "data_type": "CE",
            "required": False,
        })
        
        # TQ2-21: Related Priority (all versions 2.3+) - Note: This field appears twice in some versions
        profile.add_field_definition("TQ2", 21, {
            "name": "Related Priority",
            "data_type": "CWE",
            "required": False,
            "table": "0485",  # Priority table
        })
    
    # RXE segment definition (Pharmacy/Treatment Encoded Order)
    profile.add_segment_definition("RXE", {
        "name": "RXE",
        "description": "Pharmacy/Treatment Encoded Order",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # RXE-1: Quantity/Timing (all versions)
    profile.add_field_definition("RXE", 1, {
        "name": "Quantity/Timing",
        "data_type": "TQ",
        "required": False,
    })
    
    # RXE-2: Give Code (all versions)
    profile.add_field_definition("RXE", 2, {
        "name": "Give Code",
        "data_type": "CE",
        "required": True,
    })
    
    # RXE-3: Give Amount - Minimum (all versions)
    profile.add_field_definition("RXE", 3, {
        "name": "Give Amount - Minimum",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-4: Give Amount - Maximum (all versions)
    profile.add_field_definition("RXE", 4, {
        "name": "Give Amount - Maximum",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-5: Give Units (all versions)
    profile.add_field_definition("RXE", 5, {
        "name": "Give Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXE-6: Give Dosage Form (all versions)
    profile.add_field_definition("RXE", 6, {
        "name": "Give Dosage Form",
        "data_type": "CE",
        "required": False,
    })
    
    # RXE-7: Provider's Administration Instructions (all versions)
    profile.add_field_definition("RXE", 7, {
        "name": "Provider's Administration Instructions",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXE-8: Deliver-to Location (all versions)
    profile.add_field_definition("RXE", 8, {
        "name": "Deliver-to Location",
        "data_type": "LA1",
        "required": False,
    })
    
    # RXE-9: Substitution Status (all versions)
    profile.add_field_definition("RXE", 9, {
        "name": "Substitution Status",
        "data_type": "ID",
        "required": False,
        "table": "0167",  # Substitution Status table
    })
    
    # RXE-10: Dispense Amount (all versions)
    profile.add_field_definition("RXE", 10, {
        "name": "Dispense Amount",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-11: Dispense Units (all versions)
    profile.add_field_definition("RXE", 11, {
        "name": "Dispense Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXE-12: Number Of Refills (all versions)
    profile.add_field_definition("RXE", 12, {
        "name": "Number Of Refills",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-13: Ordering Provider's DEA Number (all versions)
    profile.add_field_definition("RXE", 13, {
        "name": "Ordering Provider's DEA Number",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXE-14: Pharmacist/Treatment Supplier's Verifier ID (all versions)
    profile.add_field_definition("RXE", 14, {
        "name": "Pharmacist/Treatment Supplier's Verifier ID",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXE-15: Prescription Number (all versions)
    profile.add_field_definition("RXE", 15, {
        "name": "Prescription Number",
        "data_type": "ST",
        "required": False,
    })
    
    # RXE-16: Number of Refills Remaining (all versions)
    profile.add_field_definition("RXE", 16, {
        "name": "Number of Refills Remaining",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-17: Number of Refills/Doses Dispensed (all versions)
    profile.add_field_definition("RXE", 17, {
        "name": "Number of Refills/Doses Dispensed",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-18: D/T of Most Recent Refill or Dose Dispensed (all versions)
    profile.add_field_definition("RXE", 18, {
        "name": "D/T of Most Recent Refill or Dose Dispensed",
        "data_type": "TS",
        "required": False,
    })
    
    # RXE-19: Total Daily Dose (all versions)
    profile.add_field_definition("RXE", 19, {
        "name": "Total Daily Dose",
        "data_type": "CQ",
        "required": False,
    })
    
    # RXE-20: Needs Human Review (all versions)
    profile.add_field_definition("RXE", 20, {
        "name": "Needs Human Review",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # RXE-21: Pharmacy/Treatment Supplier's Special Dispensing Instructions (all versions)
    profile.add_field_definition("RXE", 21, {
        "name": "Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXE-22: Give Per (Time Unit) (all versions)
    profile.add_field_definition("RXE", 22, {
        "name": "Give Per (Time Unit)",
        "data_type": "ST",
        "required": False,
    })
    
    # RXE-23: Give Rate Amount (all versions)
    profile.add_field_definition("RXE", 23, {
        "name": "Give Rate Amount",
        "data_type": "ST",
        "required": False,
    })
    
    # RXE-24: Give Rate Units (all versions)
    profile.add_field_definition("RXE", 24, {
        "name": "Give Rate Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXE-25: Give Strength (all versions)
    profile.add_field_definition("RXE", 25, {
        "name": "Give Strength",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-26: Give Strength Units (all versions)
    profile.add_field_definition("RXE", 26, {
        "name": "Give Strength Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXE-27: Give Indication (all versions)
    profile.add_field_definition("RXE", 27, {
        "name": "Give Indication",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXE-28: Dispense Package Size (all versions)
    profile.add_field_definition("RXE", 28, {
        "name": "Dispense Package Size",
        "data_type": "NM",
        "required": False,
    })
    
    # RXE-29: Dispense Package Size Unit (all versions)
    profile.add_field_definition("RXE", 29, {
        "name": "Dispense Package Size Unit",
        "data_type": "CE",
        "required": False,
    })
    
    # RXE-30: Dispense Package Method (all versions)
    profile.add_field_definition("RXE", 30, {
        "name": "Dispense Package Method",
        "data_type": "ID",
        "required": False,
        "table": "0321",  # Dispense Package Method table
    })
    
    # RXE-31: Supplementary Code (all versions)
    profile.add_field_definition("RXE", 31, {
        "name": "Supplementary Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific RXE fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # RXE-32: Original Order Date/Time (added in 2.5+)
        profile.add_field_definition("RXE", 32, {
            "name": "Original Order Date/Time",
            "data_type": "TS",
            "required": False,
        })
        
        # RXE-33: Give Drug Strength Volume (added in 2.5+)
        profile.add_field_definition("RXE", 33, {
            "name": "Give Drug Strength Volume",
            "data_type": "NM",
            "required": False,
        })
        
        # RXE-34: Give Drug Strength Volume Units (added in 2.5+)
        profile.add_field_definition("RXE", 34, {
            "name": "Give Drug Strength Volume Units",
            "data_type": "CE",
            "required": False,
        })
        
        # RXE-35: Controlled Substance Schedule (added in 2.5+)
        profile.add_field_definition("RXE", 35, {
            "name": "Controlled Substance Schedule",
            "data_type": "CE",
            "required": False,
            "table": "0477",  # Controlled Substance Schedule table
        })
        
        # RXE-36: Formulary Status (added in 2.5+)
        profile.add_field_definition("RXE", 36, {
            "name": "Formulary Status",
            "data_type": "ID",
            "required": False,
            "table": "0478",  # Formulary Status table
        })
        
        # RXE-37: Pharmaceutical Substance Alternative (added in 2.5+)
        profile.add_field_definition("RXE", 37, {
            "name": "Pharmaceutical Substance Alternative",
            "data_type": "CE",
            "required": False,
            "max_repetitions": None,
        })
        
        # RXE-38: Pharmacy of Most Recent Fill (added in 2.5+)
        profile.add_field_definition("RXE", 38, {
            "name": "Pharmacy of Most Recent Fill",
            "data_type": "CE",
            "required": False,
        })
        
        # RXE-39: Initial Dispense Amount (added in 2.5+)
        profile.add_field_definition("RXE", 39, {
            "name": "Initial Dispense Amount",
            "data_type": "NM",
            "required": False,
        })
        
        # RXE-40: Dispensing Pharmacy (added in 2.5+)
        profile.add_field_definition("RXE", 40, {
            "name": "Dispensing Pharmacy",
            "data_type": "CE",
            "required": False,
        })
        
        # RXE-41: Dispensing Pharmacy Address (added in 2.5+)
        profile.add_field_definition("RXE", 41, {
            "name": "Dispensing Pharmacy Address",
            "data_type": "XAD",
            "required": False,
        })
        
        # RXE-42: Deliver-to Patient Location (added in 2.5+)
        profile.add_field_definition("RXE", 42, {
            "name": "Deliver-to Patient Location",
            "data_type": "PL",
            "required": False,
        })
        
        # RXE-43: Deliver-to Address (added in 2.5+)
        profile.add_field_definition("RXE", 43, {
            "name": "Deliver-to Address",
            "data_type": "XAD",
            "required": False,
        })
        
        # RXE-44: Pharmacy Order Type (added in 2.5+)
        profile.add_field_definition("RXE", 44, {
            "name": "Pharmacy Order Type",
            "data_type": "ID",
            "required": False,
            "table": "0480",  # Pharmacy Order Type table
        })
    
    if version in ("2.7", "2.8", "2.9"):
        # RXE-45: Dispense to Pharmacy (added in 2.7+)
        profile.add_field_definition("RXE", 45, {
            "name": "Dispense to Pharmacy",
            "data_type": "CE",
            "required": False,
        })
        
        # RXE-46: Dispense to Pharmacy Address (added in 2.7+)
        profile.add_field_definition("RXE", 46, {
            "name": "Dispense to Pharmacy Address",
            "data_type": "XAD",
            "required": False,
        })
        
        # RXE-47: Pharmacy Phone Number (added in 2.7+)
        profile.add_field_definition("RXE", 47, {
            "name": "Pharmacy Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
    
    if version in ("2.8", "2.9"):
        # RXE-48: Prescription Origin (added in 2.8+)
        profile.add_field_definition("RXE", 48, {
            "name": "Prescription Origin",
            "data_type": "ID",
            "required": False,
            "table": "0481",  # Prescription Origin table
        })
        
        # RXE-49: Substitution Status (added in 2.8+)
        profile.add_field_definition("RXE", 49, {
            "name": "Substitution Status",
            "data_type": "CE",
            "required": False,
            "table": "0167",  # Substitution Status table
        })
        
        # RXE-50: Therapeutic Substitution Evaluation (added in 2.8+)
        profile.add_field_definition("RXE", 50, {
            "name": "Therapeutic Substitution Evaluation",
            "data_type": "ID",
            "required": False,
            "table": "0136",  # Yes/No Indicator table
        })
    
    # RXA segment definition (Pharmacy/Treatment Administration)
    profile.add_segment_definition("RXA", {
        "name": "RXA",
        "description": "Pharmacy/Treatment Administration",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # RXA-1: Give Sub-ID Counter (all versions)
    profile.add_field_definition("RXA", 1, {
        "name": "Give Sub-ID Counter",
        "data_type": "NM",
        "required": True,
    })
    
    # RXA-2: Administration Sub-ID Counter (all versions)
    profile.add_field_definition("RXA", 2, {
        "name": "Administration Sub-ID Counter",
        "data_type": "NM",
        "required": True,
    })
    
    # RXA-3: Date/Time Start of Administration (all versions)
    profile.add_field_definition("RXA", 3, {
        "name": "Date/Time Start of Administration",
        "data_type": "TS",
        "required": True,
    })
    
    # RXA-4: Date/Time End of Administration (all versions)
    profile.add_field_definition("RXA", 4, {
        "name": "Date/Time End of Administration",
        "data_type": "TS",
        "required": False,
    })
    
    # RXA-5: Administered Code (all versions)
    profile.add_field_definition("RXA", 5, {
        "name": "Administered Code",
        "data_type": "CE",
        "required": True,
    })
    
    # RXA-6: Administered Amount (all versions)
    profile.add_field_definition("RXA", 6, {
        "name": "Administered Amount",
        "data_type": "NM",
        "required": True,
    })
    
    # RXA-7: Administered Units (all versions)
    profile.add_field_definition("RXA", 7, {
        "name": "Administered Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXA-8: Administered Dosage Form (all versions)
    profile.add_field_definition("RXA", 8, {
        "name": "Administered Dosage Form",
        "data_type": "CE",
        "required": False,
    })
    
    # RXA-9: Administration Notes (all versions)
    profile.add_field_definition("RXA", 9, {
        "name": "Administration Notes",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-10: Administering Provider (all versions)
    profile.add_field_definition("RXA", 10, {
        "name": "Administering Provider",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-11: Administered-at Location (all versions)
    profile.add_field_definition("RXA", 11, {
        "name": "Administered-at Location",
        "data_type": "LA1",
        "required": False,
    })
    
    # RXA-12: Administered Per (Time Unit) (all versions)
    profile.add_field_definition("RXA", 12, {
        "name": "Administered Per (Time Unit)",
        "data_type": "ST",
        "required": False,
    })
    
    # RXA-13: Administered Strength (all versions)
    profile.add_field_definition("RXA", 13, {
        "name": "Administered Strength",
        "data_type": "NM",
        "required": False,
    })
    
    # RXA-14: Administered Strength Units (all versions)
    profile.add_field_definition("RXA", 14, {
        "name": "Administered Strength Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXA-15: Substance Lot Number (all versions)
    profile.add_field_definition("RXA", 15, {
        "name": "Substance Lot Number",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-16: Substance Expiration Date (all versions)
    profile.add_field_definition("RXA", 16, {
        "name": "Substance Expiration Date",
        "data_type": "TS",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-17: Substance Manufacturer Name (all versions)
    profile.add_field_definition("RXA", 17, {
        "name": "Substance Manufacturer Name",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-18: Substance/Treatment Refusal Reason (all versions)
    profile.add_field_definition("RXA", 18, {
        "name": "Substance/Treatment Refusal Reason",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-19: Indication (all versions)
    profile.add_field_definition("RXA", 19, {
        "name": "Indication",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXA-20: Completion Status (all versions)
    profile.add_field_definition("RXA", 20, {
        "name": "Completion Status",
        "data_type": "ID",
        "required": False,
        "table": "0322",  # Completion Status table
    })
    
    # RXA-21: Action Code - RXA (all versions)
    profile.add_field_definition("RXA", 21, {
        "name": "Action Code - RXA",
        "data_type": "ID",
        "required": False,
        "table": "0323",  # Action Code table
    })
    
    # RXA-22: System Entry Date/Time (all versions)
    profile.add_field_definition("RXA", 22, {
        "name": "System Entry Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # RXA-23: Administered Drug Strength Volume (all versions)
    profile.add_field_definition("RXA", 23, {
        "name": "Administered Drug Strength Volume",
        "data_type": "NM",
        "required": False,
    })
    
    # RXA-24: Administered Drug Strength Volume Units (all versions)
    profile.add_field_definition("RXA", 24, {
        "name": "Administered Drug Strength Volume Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXA-25: Administered Barcode Identifier (all versions)
    profile.add_field_definition("RXA", 25, {
        "name": "Administered Barcode Identifier",
        "data_type": "CE",
        "required": False,
    })
    
    # RXA-26: Pharmacy Order Type (all versions)
    profile.add_field_definition("RXA", 26, {
        "name": "Pharmacy Order Type",
        "data_type": "ID",
        "required": False,
        "table": "0480",  # Pharmacy Order Type table
    })
    
    # Version-specific RXA fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # RXA-27: Administer-at (the facility where the drug was administered) (added in 2.5+)
        profile.add_field_definition("RXA", 27, {
            "name": "Administer-at (the facility where the drug was administered)",
            "data_type": "CE",
            "required": False,
        })
        
        # RXA-28: Administered-at Address (added in 2.5+)
        profile.add_field_definition("RXA", 28, {
            "name": "Administered-at Address",
            "data_type": "XAD",
            "required": False,
        })
    
    # RXC segment definition (Pharmacy/Treatment Component Order)
    profile.add_segment_definition("RXC", {
        "name": "RXC",
        "description": "Pharmacy/Treatment Component Order",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # RXC-1: RX Component Type (all versions)
    profile.add_field_definition("RXC", 1, {
        "name": "RX Component Type",
        "data_type": "ID",
        "required": True,
        "table": "0166",  # RX Component Type table
    })
    
    # RXC-2: Component Code (all versions)
    profile.add_field_definition("RXC", 2, {
        "name": "Component Code",
        "data_type": "CE",
        "required": True,
    })
    
    # RXC-3: Component Amount (all versions)
    profile.add_field_definition("RXC", 3, {
        "name": "Component Amount",
        "data_type": "NM",
        "required": True,
    })
    
    # RXC-4: Component Units (all versions)
    profile.add_field_definition("RXC", 4, {
        "name": "Component Units",
        "data_type": "CE",
        "required": True,
    })
    
    # RXC-5: Component Strength (all versions)
    profile.add_field_definition("RXC", 5, {
        "name": "Component Strength",
        "data_type": "NM",
        "required": False,
    })
    
    # RXC-6: Component Strength Units (all versions)
    profile.add_field_definition("RXC", 6, {
        "name": "Component Strength Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXC-7: Supplementary Code (all versions)
    profile.add_field_definition("RXC", 7, {
        "name": "Supplementary Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # Version-specific RXC fields
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # RXC-8: Component Drug Strength Volume (added in 2.5+)
        profile.add_field_definition("RXC", 8, {
            "name": "Component Drug Strength Volume",
            "data_type": "NM",
            "required": False,
        })
        
        # RXC-9: Component Drug Strength Volume Units (added in 2.5+)
        profile.add_field_definition("RXC", 9, {
            "name": "Component Drug Strength Volume Units",
            "data_type": "CE",
            "required": False,
        })
    
    # SCH segment definition (Schedule - added in 2.3+)
    if version in ("2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"):
        profile.add_segment_definition("SCH", {
            "name": "SCH",
            "description": "Schedule",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-1: Placer Appointment ID (all versions 2.3+)
        profile.add_field_definition("SCH", 1, {
            "name": "Placer Appointment ID",
            "data_type": "EI",
            "required": False,
        })
        
        # SCH-2: Filler Appointment ID (all versions 2.3+)
        profile.add_field_definition("SCH", 2, {
            "name": "Filler Appointment ID",
            "data_type": "EI",
            "required": False,
        })
        
        # SCH-3: Occurrence Number (all versions 2.3+)
        profile.add_field_definition("SCH", 3, {
            "name": "Occurrence Number",
            "data_type": "NM",
            "required": False,
        })
        
        # SCH-4: Placer Group Number (all versions 2.3+)
        profile.add_field_definition("SCH", 4, {
            "name": "Placer Group Number",
            "data_type": "EI",
            "required": False,
        })
        
        # SCH-5: Schedule ID (all versions 2.3+)
        profile.add_field_definition("SCH", 5, {
            "name": "Schedule ID",
            "data_type": "CE",
            "required": False,
            "table": "0274",  # Appointment Type table
        })
        
        # SCH-6: Event Reason (all versions 2.3+)
        profile.add_field_definition("SCH", 6, {
            "name": "Event Reason",
            "data_type": "CE",
            "required": False,
            "table": "0626",  # Event Reason table
        })
        
        # SCH-7: Appointment Reason (all versions 2.3+)
        profile.add_field_definition("SCH", 7, {
            "name": "Appointment Reason",
            "data_type": "CE",
            "required": False,
            "table": "0276",  # Appointment Reason Codes table
        })
        
        # SCH-8: Appointment Type (all versions 2.3+)
        profile.add_field_definition("SCH", 8, {
            "name": "Appointment Type",
            "data_type": "CE",
            "required": False,
            "table": "0277",  # Appointment Type Codes table
        })
        
        # SCH-9: Appointment Duration (all versions 2.3+)
        profile.add_field_definition("SCH", 9, {
            "name": "Appointment Duration",
            "data_type": "NM",
            "required": False,
        })
        
        # SCH-10: Appointment Duration Units (all versions 2.3+)
        profile.add_field_definition("SCH", 10, {
            "name": "Appointment Duration Units",
            "data_type": "CE",
            "required": False,
            "table": "0278",  # Appointment Duration Units table
        })
        
        # SCH-11: Appointment Timing Quantity (all versions 2.3+)
        profile.add_field_definition("SCH", 11, {
            "name": "Appointment Timing Quantity",
            "data_type": "TQ",
            "required": False,
        })
        
        # SCH-12: Placer Contact Person (all versions 2.3+)
        profile.add_field_definition("SCH", 12, {
            "name": "Placer Contact Person",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-13: Placer Contact Phone (all versions 2.3+)
        profile.add_field_definition("SCH", 13, {
            "name": "Placer Contact Phone",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-14: Placer Contact Address (all versions 2.3+)
        profile.add_field_definition("SCH", 14, {
            "name": "Placer Contact Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-15: Placer Contact Location (all versions 2.3+)
        profile.add_field_definition("SCH", 15, {
            "name": "Placer Contact Location",
            "data_type": "PL",
            "required": False,
        })
        
        # SCH-16: Filler Contact Person (all versions 2.3+)
        profile.add_field_definition("SCH", 16, {
            "name": "Filler Contact Person",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-17: Filler Contact Phone (all versions 2.3+)
        profile.add_field_definition("SCH", 17, {
            "name": "Filler Contact Phone",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-18: Filler Contact Address (all versions 2.3+)
        profile.add_field_definition("SCH", 18, {
            "name": "Filler Contact Address",
            "data_type": "XAD",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-19: Filler Contact Location (all versions 2.3+)
        profile.add_field_definition("SCH", 19, {
            "name": "Filler Contact Location",
            "data_type": "PL",
            "required": False,
        })
        
        # SCH-20: Entered By Person (all versions 2.3+)
        profile.add_field_definition("SCH", 20, {
            "name": "Entered By Person",
            "data_type": "XCN",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-21: Entered By Phone Number (all versions 2.3+)
        profile.add_field_definition("SCH", 21, {
            "name": "Entered By Phone Number",
            "data_type": "XTN",
            "required": False,
            "max_repetitions": None,
        })
        
        # SCH-22: Entered By Location (all versions 2.3+)
        profile.add_field_definition("SCH", 22, {
            "name": "Entered By Location",
            "data_type": "PL",
            "required": False,
        })
        
        # SCH-23: Parent Placer Appointment ID (all versions 2.3+)
        profile.add_field_definition("SCH", 23, {
            "name": "Parent Placer Appointment ID",
            "data_type": "EI",
            "required": False,
        })
        
        # SCH-24: Parent Filler Appointment ID (all versions 2.3+)
        profile.add_field_definition("SCH", 24, {
            "name": "Parent Filler Appointment ID",
            "data_type": "EI",
            "required": False,
        })
        
        # SCH-25: Filler Status Code (all versions 2.3+)
        profile.add_field_definition("SCH", 25, {
            "name": "Filler Status Code",
            "data_type": "CE",
            "required": False,
            "table": "0273",  # Appointment Status Codes table
        })
    
    # RGS segment definition (Resource Group - added in 2.3+)
    if version in ("2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"):
        profile.add_segment_definition("RGS", {
            "name": "RGS",
            "description": "Resource Group",
            "required": False,
            "max_repetitions": None,  # Unlimited repetitions
        })
        
        # RGS-1: Set ID (all versions 2.3+)
        profile.add_field_definition("RGS", 1, {
            "name": "Set ID",
            "data_type": "SI",
            "required": True,
        })
        
        # RGS-2: Segment Action Code (all versions 2.3+)
        profile.add_field_definition("RGS", 2, {
            "name": "Segment Action Code",
            "data_type": "ID",
            "required": False,
            "table": "0206",  # Segment Action Code table
        })
        
        # RGS-3: Resource Group ID (all versions 2.3+)
        profile.add_field_definition("RGS", 3, {
            "name": "Resource Group ID",
            "data_type": "CE",
            "required": False,
        })
    
    # ACC segment definition (Accident - all versions)
    profile.add_segment_definition("ACC", {
        "name": "ACC",
        "description": "Accident",
        "required": False,
        "max_repetitions": None,  # Unlimited repetitions
    })
    
    # ACC-1: Accident Date/Time (all versions)
    profile.add_field_definition("ACC", 1, {
        "name": "Accident Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # ACC-2: Accident Code (all versions)
    profile.add_field_definition("ACC", 2, {
        "name": "Accident Code",
        "data_type": "CE",
        "required": False,
        "table": "0055",  # Accident Code table
    })
    
    # ACC-3: Accident Location (all versions)
    profile.add_field_definition("ACC", 3, {
        "name": "Accident Location",
        "data_type": "ST",
        "required": False,
    })
    
    # ACC-4: Auto Accident State (all versions)
    profile.add_field_definition("ACC", 4, {
        "name": "Auto Accident State",
        "data_type": "CE",
        "required": False,
    })
    
    # ACC-5: Accident Job Related Indicator (all versions)
    profile.add_field_definition("ACC", 5, {
        "name": "Accident Job Related Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # ACC-6: Accident Death Indicator (all versions)
    profile.add_field_definition("ACC", 6, {
        "name": "Accident Death Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # ACC-7: Entered By (all versions)
    profile.add_field_definition("ACC", 7, {
        "name": "Entered By",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # ACC-8: Accident Description (all versions)
    profile.add_field_definition("ACC", 8, {
        "name": "Accident Description",
        "data_type": "ST",
        "required": False,
    })
    
    # ACC-9: Brought In By (all versions)
    profile.add_field_definition("ACC", 9, {
        "name": "Brought In By",
        "data_type": "ST",
        "required": False,
    })
    
    # ACC-10: Police Notified Indicator (all versions)
    profile.add_field_definition("ACC", 10, {
        "name": "Police Notified Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # ACC-11: Accident Address (all versions)
    profile.add_field_definition("ACC", 11, {
        "name": "Accident Address",
        "data_type": "XAD",
        "required": False,
        "max_repetitions": None,
    })
    
    # BLG segment definition (Billing - all versions)
    profile.add_segment_definition("BLG", {
        "name": "BLG",
        "description": "Billing",
        "required": False,
        "max_repetitions": None,
    })
    
    # BLG-1: When to Charge (all versions)
    profile.add_field_definition("BLG", 1, {
        "name": "When to Charge",
        "data_type": "CCD",
        "required": False,
    })
    
    # BLG-2: Charge Type (all versions)
    profile.add_field_definition("BLG", 2, {
        "name": "Charge Type",
        "data_type": "ID",
        "required": False,
        "table": "0122",  # Charge Type table
    })
    
    # BLG-3: Account ID (all versions)
    profile.add_field_definition("BLG", 3, {
        "name": "Account ID",
        "data_type": "CX",
        "required": False,
    })
    
    # BLG-4: Charge Type Reason (all versions)
    profile.add_field_definition("BLG", 4, {
        "name": "Charge Type Reason",
        "data_type": "CWE",
        "required": False,
    })
    
    # MFI segment definition (Master File Identification - all versions)
    profile.add_segment_definition("MFI", {
        "name": "MFI",
        "description": "Master File Identification",
        "required": True,
        "max_repetitions": 1,
    })
    
    # MFI-1: Master File Identifier (all versions)
    profile.add_field_definition("MFI", 1, {
        "name": "Master File Identifier",
        "data_type": "CE",
        "required": True,
        "table": "0175",  # Master File Identifier Code table
    })
    
    # MFI-2: Master File Application Identifier (all versions)
    profile.add_field_definition("MFI", 2, {
        "name": "Master File Application Identifier",
        "data_type": "HD",
        "required": False,
    })
    
    # MFI-3: File-Level Event Code (all versions)
    profile.add_field_definition("MFI", 3, {
        "name": "File-Level Event Code",
        "data_type": "ID",
        "required": True,
        "table": "0178",  # File-Level Event Code table
    })
    
    # MFI-4: Entered Date/Time (all versions)
    profile.add_field_definition("MFI", 4, {
        "name": "Entered Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # MFI-5: Effective Date/Time (all versions)
    profile.add_field_definition("MFI", 5, {
        "name": "Effective Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # MFI-6: Response Level Code (all versions)
    profile.add_field_definition("MFI", 6, {
        "name": "Response Level Code",
        "data_type": "ID",
        "required": True,
        "table": "0179",  # Response Level table
    })
    
    # MFE segment definition (Master File Entry - all versions)
    profile.add_segment_definition("MFE", {
        "name": "MFE",
        "description": "Master File Entry",
        "required": False,
        "max_repetitions": None,
    })
    
    # MFE-1: Record-Level Event Code (all versions)
    profile.add_field_definition("MFE", 1, {
        "name": "Record-Level Event Code",
        "data_type": "ID",
        "required": True,
        "table": "0180",  # Record-Level Event Code table
    })
    
    # MFE-2: MFN Control ID (all versions)
    profile.add_field_definition("MFE", 2, {
        "name": "MFN Control ID",
        "data_type": "ST",
        "required": False,
    })
    
    # MFE-3: Effective Date/Time (all versions)
    profile.add_field_definition("MFE", 3, {
        "name": "Effective Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # MFE-4: Primary Key Value - MFE (all versions)
    profile.add_field_definition("MFE", 4, {
        "name": "Primary Key Value - MFE",
        "data_type": "CE",
        "required": True,
    })
    
    # MFE-5: Primary Key Value Type - MFE (all versions)
    profile.add_field_definition("MFE", 5, {
        "name": "Primary Key Value Type - MFE",
        "data_type": "ID",
        "required": True,
        "table": "0355",  # Primary Key Value Type table
    })
    
    # RXD segment definition (Pharmacy/Treatment Dispense - all versions)
    profile.add_segment_definition("RXD", {
        "name": "RXD",
        "description": "Pharmacy/Treatment Dispense",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-1: Dispense Sub-ID Counter (all versions)
    profile.add_field_definition("RXD", 1, {
        "name": "Dispense Sub-ID Counter",
        "data_type": "NM",
        "required": True,
    })
    
    # RXD-2: Dispense/Give Code (all versions)
    profile.add_field_definition("RXD", 2, {
        "name": "Dispense/Give Code",
        "data_type": "CE",
        "required": True,
    })
    
    # RXD-3: Date/Time Dispensed (all versions)
    profile.add_field_definition("RXD", 3, {
        "name": "Date/Time Dispensed",
        "data_type": "TS",
        "required": False,
    })
    
    # RXD-4: Actual Dispense Amount (all versions)
    profile.add_field_definition("RXD", 4, {
        "name": "Actual Dispense Amount",
        "data_type": "NM",
        "required": False,
    })
    
    # RXD-5: Actual Dispense Units (all versions)
    profile.add_field_definition("RXD", 5, {
        "name": "Actual Dispense Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXD-6: Actual Dosage Form (all versions)
    profile.add_field_definition("RXD", 6, {
        "name": "Actual Dosage Form",
        "data_type": "CE",
        "required": False,
    })
    
    # RXD-7: Prescription Number (all versions)
    profile.add_field_definition("RXD", 7, {
        "name": "Prescription Number",
        "data_type": "ST",
        "required": False,
    })
    
    # RXD-8: Number of Refills Remaining (all versions)
    profile.add_field_definition("RXD", 8, {
        "name": "Number of Refills Remaining",
        "data_type": "NM",
        "required": False,
    })
    
    # RXD-9: Dispense Notes (all versions)
    profile.add_field_definition("RXD", 9, {
        "name": "Dispense Notes",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-10: Dispensing Provider (all versions)
    profile.add_field_definition("RXD", 10, {
        "name": "Dispensing Provider",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-11: Substitution Status (all versions)
    profile.add_field_definition("RXD", 11, {
        "name": "Substitution Status",
        "data_type": "ID",
        "required": False,
        "table": "0167",  # Substitution Status table
    })
    
    # RXD-12: Total Daily Dose (all versions)
    profile.add_field_definition("RXD", 12, {
        "name": "Total Daily Dose",
        "data_type": "CQ",
        "required": False,
    })
    
    # RXD-13: Dispense-to Location (all versions)
    profile.add_field_definition("RXD", 13, {
        "name": "Dispense-to Location",
        "data_type": "LA2",
        "required": False,
    })
    
    # RXD-14: Needs Human Review (all versions)
    profile.add_field_definition("RXD", 14, {
        "name": "Needs Human Review",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # RXD-15: Pharmacy/Treatment Supplier's Special Dispensing Instructions (all versions)
    profile.add_field_definition("RXD", 15, {
        "name": "Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-16: Actual Strength (all versions)
    profile.add_field_definition("RXD", 16, {
        "name": "Actual Strength",
        "data_type": "NM",
        "required": False,
    })
    
    # RXD-17: Actual Strength Unit (all versions)
    profile.add_field_definition("RXD", 17, {
        "name": "Actual Strength Unit",
        "data_type": "CE",
        "required": False,
    })
    
    # RXD-18: Substance Lot Number (all versions)
    profile.add_field_definition("RXD", 18, {
        "name": "Substance Lot Number",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-19: Substance Expiration Date (all versions)
    profile.add_field_definition("RXD", 19, {
        "name": "Substance Expiration Date",
        "data_type": "TS",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-20: Substance Manufacturer Name (all versions)
    profile.add_field_definition("RXD", 20, {
        "name": "Substance Manufacturer Name",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-21: Indication (all versions)
    profile.add_field_definition("RXD", 21, {
        "name": "Indication",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXD-22: Dispense Package Size (all versions)
    profile.add_field_definition("RXD", 22, {
        "name": "Dispense Package Size",
        "data_type": "NM",
        "required": False,
    })
    
    # RXD-23: Dispense Package Size Unit (all versions)
    profile.add_field_definition("RXD", 23, {
        "name": "Dispense Package Size Unit",
        "data_type": "CE",
        "required": False,
    })
    
    # RXD-24: Dispense Package Method (all versions)
    profile.add_field_definition("RXD", 24, {
        "name": "Dispense Package Method",
        "data_type": "ID",
        "required": False,
        "table": "0321",  # Dispense Method table
    })
    
    # RXD-25: Supplementary Code (all versions)
    profile.add_field_definition("RXD", 25, {
        "name": "Supplementary Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG segment definition (Pharmacy/Treatment Give - all versions)
    profile.add_segment_definition("RXG", {
        "name": "RXG",
        "description": "Pharmacy/Treatment Give",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-1: Give Sub-ID Counter (all versions)
    profile.add_field_definition("RXG", 1, {
        "name": "Give Sub-ID Counter",
        "data_type": "NM",
        "required": True,
    })
    
    # RXG-2: Dispense/Give Code (all versions)
    profile.add_field_definition("RXG", 2, {
        "name": "Dispense/Give Code",
        "data_type": "CE",
        "required": True,
    })
    
    # RXG-3: Give Amount - Minimum (all versions)
    profile.add_field_definition("RXG", 3, {
        "name": "Give Amount - Minimum",
        "data_type": "NM",
        "required": False,
    })
    
    # RXG-4: Give Amount - Maximum (all versions)
    profile.add_field_definition("RXG", 4, {
        "name": "Give Amount - Maximum",
        "data_type": "NM",
        "required": False,
    })
    
    # RXG-5: Give Units (all versions)
    profile.add_field_definition("RXG", 5, {
        "name": "Give Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXG-6: Give Dosage Form (all versions)
    profile.add_field_definition("RXG", 6, {
        "name": "Give Dosage Form",
        "data_type": "CE",
        "required": False,
    })
    
    # RXG-7: Administration Notes (all versions)
    profile.add_field_definition("RXG", 7, {
        "name": "Administration Notes",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-8: Substitution Status (all versions)
    profile.add_field_definition("RXG", 8, {
        "name": "Substitution Status",
        "data_type": "ID",
        "required": False,
        "table": "0167",  # Substitution Status table
    })
    
    # RXG-9: Dispense-to Location (all versions)
    profile.add_field_definition("RXG", 9, {
        "name": "Dispense-to Location",
        "data_type": "LA2",
        "required": False,
    })
    
    # RXG-10: Needs Human Review (all versions)
    profile.add_field_definition("RXG", 10, {
        "name": "Needs Human Review",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # RXG-11: Pharmacy/Treatment Supplier's Special Administration Instructions (all versions)
    profile.add_field_definition("RXG", 11, {
        "name": "Pharmacy/Treatment Supplier's Special Administration Instructions",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-12: Give Per (Time Unit) (all versions)
    profile.add_field_definition("RXG", 12, {
        "name": "Give Per (Time Unit)",
        "data_type": "ST",
        "required": False,
    })
    
    # RXG-13: Give Rate Amount (all versions)
    profile.add_field_definition("RXG", 13, {
        "name": "Give Rate Amount",
        "data_type": "ST",
        "required": False,
    })
    
    # RXG-14: Give Rate Units (all versions)
    profile.add_field_definition("RXG", 14, {
        "name": "Give Rate Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXG-15: Give Strength (all versions)
    profile.add_field_definition("RXG", 15, {
        "name": "Give Strength",
        "data_type": "NM",
        "required": False,
    })
    
    # RXG-16: Give Strength Units (all versions)
    profile.add_field_definition("RXG", 16, {
        "name": "Give Strength Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXG-17: Substance Lot Number (all versions)
    profile.add_field_definition("RXG", 17, {
        "name": "Substance Lot Number",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-18: Substance Expiration Date (all versions)
    profile.add_field_definition("RXG", 18, {
        "name": "Substance Expiration Date",
        "data_type": "TS",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-19: Substance Manufacturer Name (all versions)
    profile.add_field_definition("RXG", 19, {
        "name": "Substance Manufacturer Name",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-20: Indication (all versions)
    profile.add_field_definition("RXG", 20, {
        "name": "Indication",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXG-21: Give Drug Strength Volume (all versions)
    profile.add_field_definition("RXG", 21, {
        "name": "Give Drug Strength Volume",
        "data_type": "NM",
        "required": False,
    })
    
    # RXG-22: Give Drug Strength Volume Units (all versions)
    profile.add_field_definition("RXG", 22, {
        "name": "Give Drug Strength Volume Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXG-23: Give Barcode Identifier (all versions)
    profile.add_field_definition("RXG", 23, {
        "name": "Give Barcode Identifier",
        "data_type": "CWE",
        "required": False,
    })
    
    # RXG-24: Pharmacy Order Type (all versions)
    profile.add_field_definition("RXG", 24, {
        "name": "Pharmacy Order Type",
        "data_type": "ID",
        "required": False,
        "table": "0480",  # Pharmacy Order Types table
    })
    
    # RXO segment definition (Pharmacy/Treatment Order - all versions)
    profile.add_segment_definition("RXO", {
        "name": "RXO",
        "description": "Pharmacy/Treatment Order",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-1: Requested Give Code (all versions)
    profile.add_field_definition("RXO", 1, {
        "name": "Requested Give Code",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-2: Requested Give Amount - Minimum (all versions)
    profile.add_field_definition("RXO", 2, {
        "name": "Requested Give Amount - Minimum",
        "data_type": "NM",
        "required": False,
    })
    
    # RXO-3: Requested Give Amount - Maximum (all versions)
    profile.add_field_definition("RXO", 3, {
        "name": "Requested Give Amount - Maximum",
        "data_type": "NM",
        "required": False,
    })
    
    # RXO-4: Requested Give Units (all versions)
    profile.add_field_definition("RXO", 4, {
        "name": "Requested Give Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-5: Requested Dosage Form (all versions)
    profile.add_field_definition("RXO", 5, {
        "name": "Requested Dosage Form",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-6: Provider's Pharmacy/Treatment Instructions (all versions)
    profile.add_field_definition("RXO", 6, {
        "name": "Provider's Pharmacy/Treatment Instructions",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-7: Provider's Administration Instructions (all versions)
    profile.add_field_definition("RXO", 7, {
        "name": "Provider's Administration Instructions",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-8: Deliver-to Location (all versions)
    profile.add_field_definition("RXO", 8, {
        "name": "Deliver-to Location",
        "data_type": "LA1",
        "required": False,
    })
    
    # RXO-9: Allow Substitutions (all versions)
    profile.add_field_definition("RXO", 9, {
        "name": "Allow Substitutions",
        "data_type": "ID",
        "required": False,
        "table": "0161",  # Allow Substitution table
    })
    
    # RXO-10: Requested Dispense Code (all versions)
    profile.add_field_definition("RXO", 10, {
        "name": "Requested Dispense Code",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-11: Requested Dispense Amount (all versions)
    profile.add_field_definition("RXO", 11, {
        "name": "Requested Dispense Amount",
        "data_type": "NM",
        "required": False,
    })
    
    # RXO-12: Requested Dispense Units (all versions)
    profile.add_field_definition("RXO", 12, {
        "name": "Requested Dispense Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-13: Number of Refills (all versions)
    profile.add_field_definition("RXO", 13, {
        "name": "Number of Refills",
        "data_type": "NM",
        "required": False,
    })
    
    # RXO-14: Ordering Provider's DEA Number (all versions)
    profile.add_field_definition("RXO", 14, {
        "name": "Ordering Provider's DEA Number",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-15: Pharmacist/Treatment Supplier's Verifier ID (all versions)
    profile.add_field_definition("RXO", 15, {
        "name": "Pharmacist/Treatment Supplier's Verifier ID",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-16: Needs Human Review (all versions)
    profile.add_field_definition("RXO", 16, {
        "name": "Needs Human Review",
        "data_type": "ID",
        "required": False,
        "table": "0136",  # Yes/No Indicator table
    })
    
    # RXO-17: Requested Give Per (Time Unit) (all versions)
    profile.add_field_definition("RXO", 17, {
        "name": "Requested Give Per (Time Unit)",
        "data_type": "ST",
        "required": False,
    })
    
    # RXO-18: Requested Give Strength (all versions)
    profile.add_field_definition("RXO", 18, {
        "name": "Requested Give Strength",
        "data_type": "NM",
        "required": False,
    })
    
    # RXO-19: Requested Give Strength Units (all versions)
    profile.add_field_definition("RXO", 19, {
        "name": "Requested Give Strength Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-20: Indication (all versions)
    profile.add_field_definition("RXO", 20, {
        "name": "Indication",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-21: Requested Give Rate Amount (all versions)
    profile.add_field_definition("RXO", 21, {
        "name": "Requested Give Rate Amount",
        "data_type": "ST",
        "required": False,
    })
    
    # RXO-22: Requested Give Rate Units (all versions)
    profile.add_field_definition("RXO", 22, {
        "name": "Requested Give Rate Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-23: Total Daily Dose (all versions)
    profile.add_field_definition("RXO", 23, {
        "name": "Total Daily Dose",
        "data_type": "CQ",
        "required": False,
    })
    
    # RXO-24: Supplementary Code (all versions)
    profile.add_field_definition("RXO", 24, {
        "name": "Supplementary Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXO-25: Requested Drug Strength Volume (all versions)
    profile.add_field_definition("RXO", 25, {
        "name": "Requested Drug Strength Volume",
        "data_type": "NM",
        "required": False,
    })
    
    # RXO-26: Requested Drug Strength Volume Units (all versions)
    profile.add_field_definition("RXO", 26, {
        "name": "Requested Drug Strength Volume Units",
        "data_type": "CE",
        "required": False,
    })
    
    # RXO-27: Pharmacy Order Type (all versions)
    profile.add_field_definition("RXO", 27, {
        "name": "Pharmacy Order Type",
        "data_type": "ID",
        "required": False,
        "table": "0480",  # Pharmacy Order Types table
    })
    
    # RXO-28: Dispensing Interval (all versions)
    profile.add_field_definition("RXO", 28, {
        "name": "Dispensing Interval",
        "data_type": "NM",
        "required": False,
    })
    
    # RXR segment definition (Pharmacy/Treatment Route - all versions)
    profile.add_segment_definition("RXR", {
        "name": "RXR",
        "description": "Pharmacy/Treatment Route",
        "required": False,
        "max_repetitions": None,
    })
    
    # RXR-1: Route (all versions)
    profile.add_field_definition("RXR", 1, {
        "name": "Route",
        "data_type": "CE",
        "required": True,
        "table": "0162",  # Route of Administration table
    })
    
    # RXR-2: Administration Site (all versions)
    profile.add_field_definition("RXR", 2, {
        "name": "Administration Site",
        "data_type": "CWE",
        "required": False,
        "table": "0163",  # Administration Site table
    })
    
    # RXR-3: Administration Device (all versions)
    profile.add_field_definition("RXR", 3, {
        "name": "Administration Device",
        "data_type": "CWE",
        "required": False,
        "table": "0164",  # Administration Device table
    })
    
    # RXR-4: Administration Method (all versions)
    profile.add_field_definition("RXR", 4, {
        "name": "Administration Method",
        "data_type": "CWE",
        "required": False,
        "table": "0165",  # Administration Method table
    })
    
    # RXR-5: Routing Instruction (all versions)
    profile.add_field_definition("RXR", 5, {
        "name": "Routing Instruction",
        "data_type": "CE",
        "required": False,
    })
    
    # RXR-6: Administration Site Modifier (all versions)
    profile.add_field_definition("RXR", 6, {
        "name": "Administration Site Modifier",
        "data_type": "CWE",
        "required": False,
        "table": "0495",  # Administration Site Modifier table
    })
    
    # DSC segment definition (Continuation Pointer)
    profile.add_segment_definition("DSC", {
        "name": "DSC",
        "description": "Continuation Pointer",
        "required": False,
        "max_repetitions": None,
    })
    
    # DSC-1: Continuation Pointer (all versions)
    profile.add_field_definition("DSC", 1, {
        "name": "Continuation Pointer",
        "data_type": "ST",
        "required": False,
    })
    
    # DSC-2: Continuation Style (all versions)
    profile.add_field_definition("DSC", 2, {
        "name": "Continuation Style",
        "data_type": "ID",
        "required": False,
        "table": "0398",  # Continuation Style table
    })
    
    # QRD segment definition (Original-Style Query Definition)
    profile.add_segment_definition("QRD", {
        "name": "QRD",
        "description": "Original-Style Query Definition",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRD-1: Query Date/Time (all versions)
    profile.add_field_definition("QRD", 1, {
        "name": "Query Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # QRD-2: Query Format Code (all versions)
    profile.add_field_definition("QRD", 2, {
        "name": "Query Format Code",
        "data_type": "ID",
        "required": False,
        "table": "0106",  # Query Format Code table
    })
    
    # QRD-3: Query Priority (all versions)
    profile.add_field_definition("QRD", 3, {
        "name": "Query Priority",
        "data_type": "ID",
        "required": False,
        "table": "0091",  # Query Priority table
    })
    
    # QRD-4: Query ID (all versions)
    profile.add_field_definition("QRD", 4, {
        "name": "Query ID",
        "data_type": "ST",
        "required": False,
    })
    
    # QRD-5: Deferred Response Type (all versions)
    profile.add_field_definition("QRD", 5, {
        "name": "Deferred Response Type",
        "data_type": "ID",
        "required": False,
        "table": "0107",  # Deferred Response Type table
    })
    
    # QRD-6: Deferred Response Date/Time (all versions)
    profile.add_field_definition("QRD", 6, {
        "name": "Deferred Response Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # QRD-7: Quantity Limited Request (all versions)
    profile.add_field_definition("QRD", 7, {
        "name": "Quantity Limited Request",
        "data_type": "CQ",
        "required": False,
    })
    
    # QRD-8: Who Subject Filter (all versions)
    profile.add_field_definition("QRD", 8, {
        "name": "Who Subject Filter",
        "data_type": "XCN",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRD-9: What Subject Filter (all versions)
    profile.add_field_definition("QRD", 9, {
        "name": "What Subject Filter",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRD-10: What Department Data Code (all versions)
    profile.add_field_definition("QRD", 10, {
        "name": "What Department Data Code",
        "data_type": "CE",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRD-11: What Data Code Value Qual (all versions)
    profile.add_field_definition("QRD", 11, {
        "name": "What Data Code Value Qual",
        "data_type": "VR",
        "required": False,
    })
    
    # QRD-12: Query Results Level (all versions)
    profile.add_field_definition("QRD", 12, {
        "name": "Query Results Level",
        "data_type": "ID",
        "required": False,
        "table": "0108",  # Query Results Level table
    })
    
    # QRD-13: Where Subject Filter (all versions)
    profile.add_field_definition("QRD", 13, {
        "name": "Where Subject Filter",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRD-14: When Data Start Date/Time (all versions)
    profile.add_field_definition("QRD", 14, {
        "name": "When Data Start Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # QRD-15: When Data End Date/Time (all versions)
    profile.add_field_definition("QRD", 15, {
        "name": "When Data End Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # QRD-16: What User Qualifier (all versions)
    profile.add_field_definition("QRD", 16, {
        "name": "What User Qualifier",
        "data_type": "ST",
        "required": False,
    })
    
    # QRD-17: Other QRY Subject Filter (all versions)
    profile.add_field_definition("QRD", 17, {
        "name": "Other QRY Subject Filter",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRD-18: Which Date/Time Qualifier (all versions)
    profile.add_field_definition("QRD", 18, {
        "name": "Which Date/Time Qualifier",
        "data_type": "ID",
        "required": False,
        "table": "0156",  # Which Date/Time Qualifier table
    })
    
    # QRD-19: Which Date/Time Status Qualifier (all versions)
    profile.add_field_definition("QRD", 19, {
        "name": "Which Date/Time Status Qualifier",
        "data_type": "ID",
        "required": False,
        "table": "0157",  # Which Date/Time Status Qualifier table
    })
    
    # QRD-20: Date/Time Selection Qualifier (all versions)
    profile.add_field_definition("QRD", 20, {
        "name": "Date/Time Selection Qualifier",
        "data_type": "ID",
        "required": False,
        "table": "0158",  # Date/Time Selection Qualifier table
    })
    
    # QRF segment definition (Original Style Query Filter)
    profile.add_segment_definition("QRF", {
        "name": "QRF",
        "description": "Original Style Query Filter",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRF-1: Where Subject Filter (all versions)
    profile.add_field_definition("QRF", 1, {
        "name": "Where Subject Filter",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRF-2: When Data Start Date/Time (all versions)
    profile.add_field_definition("QRF", 2, {
        "name": "When Data Start Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # QRF-3: When Data End Date/Time (all versions)
    profile.add_field_definition("QRF", 3, {
        "name": "When Data End Date/Time",
        "data_type": "TS",
        "required": False,
    })
    
    # QRF-4: What User Qualifier (all versions)
    profile.add_field_definition("QRF", 4, {
        "name": "What User Qualifier",
        "data_type": "ST",
        "required": False,
    })
    
    # QRF-5: Other QRY Subject Filter (all versions)
    profile.add_field_definition("QRF", 5, {
        "name": "Other QRY Subject Filter",
        "data_type": "ST",
        "required": False,
        "max_repetitions": None,
    })
    
    # QRF-6: Which Date/Time Qualifier (all versions)
    profile.add_field_definition("QRF", 6, {
        "name": "Which Date/Time Qualifier",
        "data_type": "ID",
        "required": False,
        "table": "0156",  # Which Date/Time Qualifier table
    })
    
    # QRF-7: Which Date/Time Status Qualifier (all versions)
    profile.add_field_definition("QRF", 7, {
        "name": "Which Date/Time Status Qualifier",
        "data_type": "ID",
        "required": False,
        "table": "0157",  # Which Date/Time Status Qualifier table
    })
    
    # QRF-8: Date/Time Selection Qualifier (all versions)
    profile.add_field_definition("QRF", 8, {
        "name": "Date/Time Selection Qualifier",
        "data_type": "ID",
        "required": False,
        "table": "0158",  # Date/Time Selection Qualifier table
    })
    
    # QAK segment definition (Query Acknowledgment)
    profile.add_segment_definition("QAK", {
        "name": "QAK",
        "description": "Query Acknowledgment",
        "required": False,
        "max_repetitions": None,
    })
    
    # QAK-1: Query Tag (all versions)
    profile.add_field_definition("QAK", 1, {
        "name": "Query Tag",
        "data_type": "ST",
        "required": False,
    })
    
    # QAK-2: Query Response Status (all versions)
    profile.add_field_definition("QAK", 2, {
        "name": "Query Response Status",
        "data_type": "ID",
        "required": False,
        "table": "0208",  # Query Response Status table
    })
    
    # QAK-3: Message Query Name (all versions)
    profile.add_field_definition("QAK", 3, {
        "name": "Message Query Name",
        "data_type": "CE",
        "required": False,
    })
    
    # QAK-4: Hit Count Total (all versions)
    profile.add_field_definition("QAK", 4, {
        "name": "Hit Count Total",
        "data_type": "NM",
        "required": False,
    })
    
    # QAK-5: This payload (all versions)
    profile.add_field_definition("QAK", 5, {
        "name": "This payload",
        "data_type": "NM",
        "required": False,
    })
    
    # QAK-6: Hits remaining (all versions)
    profile.add_field_definition("QAK", 6, {
        "name": "Hits remaining",
        "data_type": "NM",
        "required": False,
    })
    
    # QPD segment definition (Query Parameter Definition)
    profile.add_segment_definition("QPD", {
        "name": "QPD",
        "description": "Query Parameter Definition",
        "required": False,
        "max_repetitions": None,
    })
    
    # QPD-1: Message Query Name (all versions)
    profile.add_field_definition("QPD", 1, {
        "name": "Message Query Name",
        "data_type": "CE",
        "required": True,  # Required for QPD
    })
    
    # QPD-2: Query Tag (all versions)
    profile.add_field_definition("QPD", 2, {
        "name": "Query Tag",
        "data_type": "ST",
        "required": False,
    })
    
    # QPD-3: Stored Procedure Name (all versions)
    profile.add_field_definition("QPD", 3, {
        "name": "Stored Procedure Name",
        "data_type": "CE",
        "required": False,
    })
    
    # QPD-4: Input Parameter List (all versions)
    profile.add_field_definition("QPD", 4, {
        "name": "Input Parameter List",
        "data_type": "QIP",
        "required": False,
        "max_repetitions": None,
    })
    
    # QPD-5: Output Parameter List (all versions)
    profile.add_field_definition("QPD", 5, {
        "name": "Output Parameter List",
        "data_type": "QSC",
        "required": False,
        "max_repetitions": None,
    })
    
    # RCP segment definition (Response Control Parameter)
    profile.add_segment_definition("RCP", {
        "name": "RCP",
        "description": "Response Control Parameter",
        "required": False,
        "max_repetitions": None,
    })
    
    # RCP-1: Query Priority (all versions)
    profile.add_field_definition("RCP", 1, {
        "name": "Query Priority",
        "data_type": "ID",
        "required": False,
        "table": "0091",  # Query Priority table
    })
    
    # RCP-2: Quantity Limited Request (all versions)
    profile.add_field_definition("RCP", 2, {
        "name": "Quantity Limited Request",
        "data_type": "CQ",
        "required": False,
    })
    
    # RCP-3: Response Modality (all versions)
    profile.add_field_definition("RCP", 3, {
        "name": "Response Modality",
        "data_type": "CE",
        "required": False,
    })
    
    # RCP-4: Execution and Delivery Time (all versions)
    profile.add_field_definition("RCP", 4, {
        "name": "Execution and Delivery Time",
        "data_type": "TS",
        "required": False,
    })
    
    # RCP-5: Modify Indicator (all versions)
    profile.add_field_definition("RCP", 5, {
        "name": "Modify Indicator",
        "data_type": "ID",
        "required": False,
        "table": "0393",  # Modify Indicator table
    })
    
    # RCP-6: Sort-by Field (all versions)
    profile.add_field_definition("RCP", 6, {
        "name": "Sort-by Field",
        "data_type": "SRT",
        "required": False,
        "max_repetitions": None,
    })
    
    # RCP-7: Segment group inclusion (all versions)
    profile.add_field_definition("RCP", 7, {
        "name": "Segment group inclusion",
        "data_type": "ID",
        "required": False,
        "max_repetitions": None,
    })
    
    # Initialize data type definitions per version
    _initialize_data_type_definitions(profile)
    
    # Initialize table definitions from standard tables
    _initialize_table_definitions(profile)


def _initialize_data_type_definitions(profile: VersionProfile):
    """
    Initialize version-specific data type definitions.
    
    Args:
        profile: VersionProfile to initialize with data type definitions
    """
    version = profile.version
    
    # Primitive Data Types - Common across all versions
    profile.add_data_type_definition("ST", {
        "name": "String",
        "description": "Character string data",
        "max_length": 199,  # Standard max length for ST
        "version_specific": {}
    })
    
    profile.add_data_type_definition("TX", {
        "name": "Text Data",
        "description": "Free-form text data",
        "max_length": 65536,  # Large text field
        "version_specific": {}
    })
    
    profile.add_data_type_definition("FT", {
        "name": "Formatted Text",
        "description": "Formatted text with formatting escape sequences",
        "max_length": 65536,
        "version_specific": {}
    })
    
    profile.add_data_type_definition("ID", {
        "name": "Coded Value for HL7 Tables",
        "description": "Coded value from HL7-defined tables",
        "max_length": None,  # Variable length
        "version_specific": {}
    })
    
    profile.add_data_type_definition("IS", {
        "name": "Coded Value for User-Defined Tables",
        "description": "Coded value from user-defined tables",
        "max_length": None,  # Variable length
        "version_specific": {}
    })
    
    profile.add_data_type_definition("SI", {
        "name": "Sequence ID",
        "description": "Sequence identifier",
        "max_length": None,
        "version_specific": {}
    })
    
    profile.add_data_type_definition("NM", {
        "name": "Numeric",
        "description": "Numeric data",
        "max_length": None,
        "version_specific": {}
    })
    
    # Date/Time types - version-specific formats
    dt_format = "YYYY[MM[DD]]"  # Standard format
    tm_format = "HH[MM[SS[.S[S[S[S]]]]]][+/-ZZZZ]"  # Standard format
    ts_format = "YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]][+/-ZZZZ]"  # Standard format
    
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        # Enhanced precision in later versions
        ts_format = "YYYY[MM[DD[HH[MM[SS[.S[S[S[S[S]]]]]]]]]][+/-ZZZZ]"
    
    profile.add_data_type_definition("DT", {
        "name": "Date",
        "description": "Date value",
        "format": dt_format,
        "version_specific": {
            "2.3": "YYYY[MM[DD]]",
            "2.4": "YYYY[MM[DD]]",
            "2.5+": "YYYY[MM[DD]]"
        }
    })
    
    profile.add_data_type_definition("TM", {
        "name": "Time",
        "description": "Time value",
        "format": tm_format,
        "version_specific": {
            "2.3": "HH[MM[SS[.S[S[S[S]]]]]][+/-ZZZZ]",
            "2.4": "HH[MM[SS[.S[S[S[S]]]]]][+/-ZZZZ]",
            "2.5+": "HH[MM[SS[.S[S[S[S[S]]]]]]]][+/-ZZZZ]"
        }
    })
    
    profile.add_data_type_definition("TS", {
        "name": "Time Stamp",
        "description": "Date and time value",
        "format": ts_format,
        "version_specific": {
            "2.3": "YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]][+/-ZZZZ]",
            "2.4": "YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]][+/-ZZZZ]",
            "2.5+": "YYYY[MM[DD[HH[MM[SS[.S[S[S[S[S]]]]]]]]]][+/-ZZZZ]"
        }
    })
    
    # Composite Data Types - Common components
    profile.add_data_type_definition("AD", {
        "name": "Address",
        "description": "Street or mailing address",
        "components": [
            {"name": "Street Address", "data_type": "ST", "required": False},
            {"name": "Other Designation", "data_type": "ST", "required": False},
            {"name": "City", "data_type": "ST", "required": False},
            {"name": "State or Province", "data_type": "ST", "required": False},
            {"name": "Zip or Postal Code", "data_type": "ST", "required": False},
            {"name": "Country", "data_type": "ID", "required": False},
            {"name": "Address Type", "data_type": "ID", "required": False},
            {"name": "Other Geographic Designation", "data_type": "ST", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("CE", {
        "name": "Coded Element",
        "description": "Coded element with optional text",
        "components": [
            {"name": "Identifier", "data_type": "ST", "required": False},
            {"name": "Text", "data_type": "ST", "required": False},
            {"name": "Name of Coding System", "data_type": "ID", "required": False},
            {"name": "Alternate Identifier", "data_type": "ST", "required": False},
            {"name": "Alternate Text", "data_type": "ST", "required": False},
            {"name": "Name of Alternate Coding System", "data_type": "ID", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("PN", {
        "name": "Person Name",
        "description": "Person name",
        "components": [
            {"name": "Family Name", "data_type": "FN", "required": False},
            {"name": "Given Name", "data_type": "ST", "required": False},
            {"name": "Middle Name or Initial", "data_type": "ST", "required": False},
            {"name": "Suffix", "data_type": "ST", "required": False},
            {"name": "Prefix", "data_type": "ST", "required": False},
            {"name": "Degree", "data_type": "IS", "required": False},
            {"name": "Name Type Code", "data_type": "ID", "required": False},
            {"name": "Name Representation Code", "data_type": "ID", "required": False},
            {"name": "Name Context", "data_type": "CE", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("HD", {
        "name": "Hierarchic Designator",
        "description": "Hierarchic designator",
        "components": [
            {"name": "Namespace ID", "data_type": "IS", "required": False},
            {"name": "Universal ID", "data_type": "ST", "required": False},
            {"name": "Universal ID Type", "data_type": "ID", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("EI", {
        "name": "Entity Identifier",
        "description": "Entity identifier",
        "components": [
            {"name": "Entity ID", "data_type": "ST", "required": False},
            {"name": "Namespace ID", "data_type": "IS", "required": False},
            {"name": "Universal ID", "data_type": "ST", "required": False},
            {"name": "Universal ID Type", "data_type": "ID", "required": False},
        ],
        "version_specific": {}
    })
    
    # Extended composite types (added in later versions)
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        profile.add_data_type_definition("XCN", {
            "name": "Extended Composite ID Number and Name",
            "description": "Extended composite ID and name",
            "components": [
                {"name": "ID Number", "data_type": "ST", "required": False},
                {"name": "Family Name", "data_type": "FN", "required": False},
                {"name": "Given Name", "data_type": "ST", "required": False},
                {"name": "Middle Initial or Name", "data_type": "ST", "required": False},
                {"name": "Suffix", "data_type": "ST", "required": False},
                {"name": "Prefix", "data_type": "ST", "required": False},
                {"name": "Degree", "data_type": "IS", "required": False},
                {"name": "Source Table", "data_type": "ID", "required": False},
                {"name": "Assigning Authority", "data_type": "HD", "required": False},
                {"name": "Name Type Code", "data_type": "ID", "required": False},
                {"name": "Identifier Check Digit", "data_type": "ST", "required": False},
                {"name": "Check Digit Scheme", "data_type": "ID", "required": False},
                {"name": "Identifier Type Code", "data_type": "ID", "required": False},
                {"name": "Assigning Facility", "data_type": "HD", "required": False},
                {"name": "Name Representation Code", "data_type": "ID", "required": False},
                {"name": "Name Context", "data_type": "CE", "required": False},
                {"name": "Name Validity Range", "data_type": "DR", "required": False},
                {"name": "Name Assembly Order", "data_type": "ID", "required": False},
                {"name": "Effective Date", "data_type": "TS", "required": False},
                {"name": "Expiration Date", "data_type": "TS", "required": False},
                {"name": "Professional Suffix", "data_type": "ST", "required": False},
                {"name": "Assigning Jurisdiction", "data_type": "CWE", "required": False},
                {"name": "Assigning Agency or Department", "data_type": "CWE", "required": False},
            ],
            "version_specific": {
                "2.5": "Extended to 23 components",
                "2.6+": "Extended to 23 components"
            }
        })
        
        profile.add_data_type_definition("XPN", {
            "name": "Extended Person Name",
            "description": "Extended person name",
            "components": [
                {"name": "Family Name", "data_type": "FN", "required": False},
                {"name": "Given Name", "data_type": "ST", "required": False},
                {"name": "Middle Initial or Name", "data_type": "ST", "required": False},
                {"name": "Suffix", "data_type": "ST", "required": False},
                {"name": "Prefix", "data_type": "ST", "required": False},
                {"name": "Degree", "data_type": "IS", "required": False},
                {"name": "Name Type Code", "data_type": "ID", "required": False},
                {"name": "Name Representation Code", "data_type": "ID", "required": False},
                {"name": "Name Context", "data_type": "CE", "required": False},
                {"name": "Name Validity Range", "data_type": "DR", "required": False},
                {"name": "Name Assembly Order", "data_type": "ID", "required": False},
                {"name": "Effective Date", "data_type": "TS", "required": False},
                {"name": "Expiration Date", "data_type": "TS", "required": False},
                {"name": "Professional Suffix", "data_type": "ST", "required": False},
            ],
            "version_specific": {
                "2.5": "Extended to 14 components",
                "2.6+": "Extended to 14 components"
            }
        })
        
        profile.add_data_type_definition("XAD", {
            "name": "Extended Address",
            "description": "Extended address",
            "components": [
                {"name": "Street Address", "data_type": "SAD", "required": False},
                {"name": "Other Designation", "data_type": "ST", "required": False},
                {"name": "City", "data_type": "ST", "required": False},
                {"name": "State or Province", "data_type": "ST", "required": False},
                {"name": "Zip or Postal Code", "data_type": "ST", "required": False},
                {"name": "Country", "data_type": "ID", "required": False},
                {"name": "Address Type", "data_type": "ID", "required": False},
                {"name": "Other Geographic Designation", "data_type": "ST", "required": False},
                {"name": "County/Parish Code", "data_type": "IS", "required": False},
                {"name": "Census Tract", "data_type": "IS", "required": False},
                {"name": "Address Representation Code", "data_type": "ID", "required": False},
                {"name": "Address Validity Range", "data_type": "DR", "required": False},
                {"name": "Effective Date", "data_type": "TS", "required": False},
                {"name": "Expiration Date", "data_type": "TS", "required": False},
            ],
            "version_specific": {
                "2.5": "Extended to 14 components",
                "2.6+": "Extended to 14 components"
            }
        })
    
    # Additional composite types
    profile.add_data_type_definition("PL", {
        "name": "Person Location",
        "description": "Person location",
        "components": [
            {"name": "Point of Care", "data_type": "IS", "required": False},
            {"name": "Room", "data_type": "IS", "required": False},
            {"name": "Bed", "data_type": "IS", "required": False},
            {"name": "Facility", "data_type": "HD", "required": False},
            {"name": "Location Status", "data_type": "IS", "required": False},
            {"name": "Person Location Type", "data_type": "IS", "required": False},
            {"name": "Building", "data_type": "IS", "required": False},
            {"name": "Floor", "data_type": "IS", "required": False},
            {"name": "Location Description", "data_type": "ST", "required": False},
            {"name": "Comprehensive Location Identifier", "data_type": "EI", "required": False},
            {"name": "Assigning Authority for Location", "data_type": "HD", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("MSG", {
        "name": "Message Type",
        "description": "Message type",
        "components": [
            {"name": "Message Code", "data_type": "ID", "required": True},
            {"name": "Trigger Event", "data_type": "ID", "required": True},
            {"name": "Message Structure", "data_type": "ID", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("PT", {
        "name": "Processing Type",
        "description": "Processing type",
        "components": [
            {"name": "Processing ID", "data_type": "ID", "required": False},
            {"name": "Processing Mode", "data_type": "ID", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("DR", {
        "name": "Date/Time Range",
        "description": "Date/time range",
        "components": [
            {"name": "Range Start Date/Time", "data_type": "TS", "required": False},
            {"name": "Range End Date/Time", "data_type": "TS", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("FN", {
        "name": "Family Name",
        "description": "Family name",
        "components": [
            {"name": "Surname", "data_type": "ST", "required": False},
            {"name": "Own Surname Prefix", "data_type": "ST", "required": False},
            {"name": "Own Surname", "data_type": "ST", "required": False},
            {"name": "Surname Prefix from Partner/Spouse", "data_type": "ST", "required": False},
            {"name": "Surname from Partner/Spouse", "data_type": "ST", "required": False},
        ],
        "version_specific": {}
    })
    
    profile.add_data_type_definition("SAD", {
        "name": "Street Address",
        "description": "Street address",
        "components": [
            {"name": "Street or Mailing Address", "data_type": "ST", "required": False},
            {"name": "Street Name", "data_type": "ST", "required": False},
            {"name": "Dwelling Number", "data_type": "ST", "required": False},
        ],
        "version_specific": {}
    })
    
    # Additional composite types - Common across versions
    profile.add_data_type_definition("CX", {
        "name": "Extended Composite ID with Check Digit",
        "description": "Extended composite ID with check digit",
        "components": [
            {"name": "ID Number", "data_type": "ST", "required": False},
            {"name": "Check Digit", "data_type": "ST", "required": False},
            {"name": "Check Digit Scheme", "data_type": "ID", "required": False},
            {"name": "Assigning Authority", "data_type": "HD", "required": False},
            {"name": "Identifier Type Code", "data_type": "ID", "required": False},
            {"name": "Assigning Facility", "data_type": "HD", "required": False},
        ],
        "version_specific": {}
    })
    
    # Additional types for 2.5+
    if version in ("2.5", "2.6", "2.7", "2.8", "2.9"):
        profile.add_data_type_definition("XON", {
            "name": "Extended Organization Name",
            "description": "Extended organization name",
            "components": [
                {"name": "Organization Name", "data_type": "ST", "required": False},
                {"name": "Organization Name Type Code", "data_type": "IS", "required": False},
                {"name": "ID Number", "data_type": "NM", "required": False},
                {"name": "Check Digit", "data_type": "ST", "required": False},
                {"name": "Check Digit Scheme", "data_type": "ID", "required": False},
                {"name": "Assigning Authority", "data_type": "HD", "required": False},
                {"name": "Identifier Type Code", "data_type": "ID", "required": False},
                {"name": "Assigning Facility ID", "data_type": "HD", "required": False},
                {"name": "Name Representation Code", "data_type": "ID", "required": False},
                {"name": "Organization Identifier", "data_type": "ST", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("XTN", {
            "name": "Extended Telecommunication Number",
            "description": "Extended telecommunication number",
            "components": [
                {"name": "Telephone Number", "data_type": "ST", "required": False},
                {"name": "Telecommunication Use Code", "data_type": "ID", "required": False},
                {"name": "Telecommunication Equipment Type", "data_type": "ID", "required": False},
                {"name": "Email Address", "data_type": "ST", "required": False},
                {"name": "Country Code", "data_type": "NM", "required": False},
                {"name": "Area/City Code", "data_type": "NM", "required": False},
                {"name": "Phone Number", "data_type": "NM", "required": False},
                {"name": "Extension", "data_type": "NM", "required": False},
                {"name": "Any Text", "data_type": "ST", "required": False},
                {"name": "Extension Prefix", "data_type": "ST", "required": False},
                {"name": "Speed Dial Code", "data_type": "ST", "required": False},
                {"name": "Unformatted Telephone Number", "data_type": "ST", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("CQ", {
            "name": "Composite Quantity with Units",
            "description": "Composite quantity with units",
            "components": [
                {"name": "Quantity", "data_type": "NM", "required": False},
                {"name": "Units", "data_type": "CE", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("GTS", {
            "name": "General Timing Specification",
            "description": "General timing specification",
            "components": [
                {"name": "Timing Specification", "data_type": "ST", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("RPT", {
            "name": "Repeat Pattern",
            "description": "Repeat pattern",
            "components": [
                {"name": "Repeat Pattern Code", "data_type": "ID", "required": False},
                {"name": "Calendar Alignment", "data_type": "ID", "required": False},
                {"name": "Frequency Range", "data_type": "ID", "required": False},
                {"name": "Period", "data_type": "NM", "required": False},
                {"name": "Period Units", "data_type": "CE", "required": False},
                {"name": "Institution Specified Time", "data_type": "ST", "required": False},
                {"name": "Event", "data_type": "ID", "required": False},
                {"name": "Event Offset Quantity", "data_type": "NM", "required": False},
                {"name": "Event Offset Units", "data_type": "CE", "required": False},
                {"name": "General Timing Specification", "data_type": "GTS", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("ELD", {
            "name": "Error Location and Description",
            "description": "Error location and description",
            "components": [
                {"name": "Segment ID", "data_type": "ST", "required": False},
                {"name": "Segment Sequence", "data_type": "NM", "required": False},
                {"name": "Field Position", "data_type": "NM", "required": False},
                {"name": "Code Identifying Error", "data_type": "CWE", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("ERL", {
            "name": "Error Location",
            "description": "Error location (deprecated in 2.5+)",
            "components": [
                {"name": "Segment ID", "data_type": "ST", "required": False},
                {"name": "Segment Sequence", "data_type": "NM", "required": False},
                {"name": "Field Position", "data_type": "NM", "required": False},
                {"name": "Field Repetition", "data_type": "NM", "required": False},
                {"name": "Component Number", "data_type": "NM", "required": False},
                {"name": "Sub-Component Number", "data_type": "NM", "required": False},
            ],
            "version_specific": {
                "2.3": "Used in versions 2.3-2.4",
                "2.4": "Deprecated in 2.5+"
            }
        })
        
        profile.add_data_type_definition("EIP", {
            "name": "Entity Identifier Pair",
            "description": "Entity identifier pair",
            "components": [
                {"name": "Placer Assigned Identifier", "data_type": "EI", "required": False},
                {"name": "Filler Assigned Identifier", "data_type": "EI", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("PLN", {
            "name": "Practitioner License or other ID Number",
            "description": "Practitioner license or other ID number",
            "components": [
                {"name": "ID Number", "data_type": "ST", "required": False},
                {"name": "Type of ID Number", "data_type": "IS", "required": False},
                {"name": "State/other Qualifying Information", "data_type": "ST", "required": False},
                {"name": "Expiration Date", "data_type": "DT", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })
        
        profile.add_data_type_definition("CWE", {
            "name": "Coded With Exceptions",
            "description": "Coded element with exceptions",
            "components": [
                {"name": "Identifier", "data_type": "ST", "required": False},
                {"name": "Text", "data_type": "ST", "required": False},
                {"name": "Name of Coding System", "data_type": "ID", "required": False},
                {"name": "Alternate Identifier", "data_type": "ST", "required": False},
                {"name": "Alternate Text", "data_type": "ST", "required": False},
                {"name": "Name of Alternate Coding System", "data_type": "ID", "required": False},
                {"name": "Coding System Version ID", "data_type": "ST", "required": False},
                {"name": "Alternate Coding System Version ID", "data_type": "ST", "required": False},
                {"name": "Original Text", "data_type": "ST", "required": False},
            ],
            "version_specific": {
                "2.5": "Added in version 2.5",
                "2.6+": "Extended in later versions"
            }
        })


def _initialize_table_definitions(profile: VersionProfile):
    """
    Initialize table definitions from standard tables module.
    
    Populates the profile with all standard HL7 v2.x table definitions
    from the tables module. This ensures that table value validation
    can be performed using profile methods.
    
    Args:
        profile: VersionProfile to initialize with table definitions
    """
    try:
        from dnhealth.dnhealth_hl7v2.tables import STANDARD_TABLES
        
        # Populate all standard tables into the profile
        for table_id, table_dict in STANDARD_TABLES.items():
            for code, description in table_dict.items():
                profile.add_table_definition(table_id, code, description)
    except ImportError:
        # If tables module is not available, skip initialization
        # This allows the profile to work without table definitions
        pass


def validate_message_against_profile(message, profile: Optional[VersionProfile] = None) -> List[str]:
    """
    Validate message against version profile.

    Args:
        message: Message object to validate
        profile: Optional VersionProfile (default: use message version)

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if profile is None:
        if not message.version:
            errors.append("Message version not specified")
            return errors
        profile = get_profile(message.version)
    
    # Validate MSH segment exists
    msh_segments = message.get_segments("MSH")
    if not msh_segments:
        errors.append("MSH segment is required")
        return errors
    
    msh = msh_segments[0]
    msh_def = profile.get_segment_definition("MSH")
    
    if msh_def:
        # Validate required MSH fields
        # Note: MSH-1 (Field Separator) is implicit and not stored as a field in the parsed structure
        # MSH fields are stored starting from MSH-2 (field index 1 in 1-based indexing)
        required_fields = [2, 9, 10]  # Skip MSH-1 as it's the field separator
        for field_idx in required_fields:
            field_def = profile.get_field_definition("MSH", field_idx)
            if field_def and field_def.get("required"):
                # MSH.field() uses 1-based indexing, but MSH-1 is not stored
                # So MSH-2 is accessed as field(2), MSH-9 as field(9), etc.
                field = msh.field(field_idx)
                if not field.value():
                    errors.append(f"MSH-{field_idx} ({field_def.get('name', 'Unknown')}) is required")
    
    # Validate other segments against profile
    for segment in message.segments:
        if segment.name == "MSH":
            continue
        
        seg_def = profile.get_segment_definition(segment.name)
        if seg_def:
            # Check max repetitions
            max_reps = seg_def.get("max_repetitions")
            if max_reps is not None:
                segments_with_same_name = message.get_segments(segment.name)
                if len(segments_with_same_name) > max_reps:
                    errors.append(
                        f"Segment {segment.name} exceeds max repetitions ({max_reps})"
                    )
        
        # Validate fields
        for field_idx in range(1, len(segment.fields) + 1):
            field_def = profile.get_field_definition(segment.name, field_idx)
            if field_def:
                field = segment.field(field_idx)
                
                # Check required fields
                if field_def.get("required") and not field.value():
                    errors.append(
                        f"{segment.name}-{field_idx} ({field_def.get('name', 'Unknown')}) is required"
                    )
                
                # Check max length
                max_length = field_def.get("max_length")
                if max_length and len(field.value()) > max_length:
                    errors.append(
                        f"{segment.name}-{field_idx} exceeds max length ({max_length})"
                    )
    
    return errors


def validate_message_with_profile_and_ig(
    message,
    profile: Optional[VersionProfile] = None,
    implementation_guide: Optional["ImplementationGuide"] = None,
) -> Tuple[bool, List[str]]:
    """
    Validate message against version profile and implementation guide constraints.
    
    This function combines profile-based validation (version-specific rules) with
    implementation guide constraints (custom validation rules).
    
    Args:
        message: Message object to validate
        profile: Optional VersionProfile (default: use message version)
        implementation_guide: Optional ImplementationGuide with custom constraints
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    from datetime import datetime
    from dnhealth.util.logging import get_logger
    
    logger = get_logger(__name__)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{current_time}] Starting profile and implementation guide validation")
    
    errors = []
    
    # Step 1: Validate against version profile
    if profile is None:
        if not message.version:
            errors.append("Message version not specified")
            logger.error(f"[{current_time}] Validation failed: message version not specified")
            return False, errors
        profile = get_profile(message.version)
        logger.debug(f"[{current_time}] Using profile for version {message.version}")
    
    profile_errors = validate_message_against_profile(message, profile)
    errors.extend(profile_errors)
    
    # Step 2: Validate against implementation guide constraints
    if implementation_guide:
        logger.debug(
            f"[{current_time}] Validating against implementation guide: "
            f"{implementation_guide.name} v{implementation_guide.version}"
        )
        ig_valid, ig_errors = implementation_guide.validate_constraints(message)
        if not ig_valid:
            errors.extend(ig_errors)
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"[{current_time}] Message validation passed all profile and IG checks")
    else:
        logger.warning(
            f"[{current_time}] Message validation failed with {len(errors)} errors"
        )
    
    return is_valid, errors


def apply_profile_to_message(
    message,
    profile: Optional[VersionProfile] = None,
) -> Tuple[bool, List[str]]:
    """
    Apply profile definitions to message (validate and enrich with profile metadata).
    
    This function validates a message against a profile and can also enrich
    the message with profile-specific metadata if needed.
    
    Args:
        message: Message object to validate
        profile: Optional VersionProfile (default: use message version)
        
    Returns:
        Tuple of (is_valid, list_of_warnings)
    """
    from datetime import datetime
    from dnhealth.util.logging import get_logger
    
    logger = get_logger(__name__)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{current_time}] Applying profile to message")
    
    warnings = []
    
    if profile is None:
        if not message.version:
            warnings.append("Message version not specified, cannot apply profile")
            return False, warnings
        profile = get_profile(message.version)
    
    # Validate message structure against profile
    errors = validate_message_against_profile(message, profile)
    if errors:
        warnings.extend([f"Profile validation error: {e}" for e in errors])
    
    # Check for segments not in profile
    for segment in message.segments:
        if segment.name == "MSH":
            continue
        
        if not profile.is_segment_available(segment.name):
            warnings.append(
                f"Segment {segment.name} is not defined in profile for version {profile.version}"
            )
    
    is_valid = len(errors) == 0
    logger.info(
        f"[{current_time}] Profile application completed: "
        f"{'valid' if is_valid else 'invalid'} ({len(warnings)} warnings)"
    )
    
    return is_valid, warnings

