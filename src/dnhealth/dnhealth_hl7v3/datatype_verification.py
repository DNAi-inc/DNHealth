# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Data Type Completeness Verification.

Provides functions to verify that all data types have all required attributes
per HL7 v3 specification and identify any missing attributes.
"""

from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import logging

from dnhealth.dnhealth_hl7v3.datatypes import (
    ANY, BL, BN, BAG, LIST, SET,
    CD, CE, CS, CV, ED, EIVL, EN, ENXP, GTS, II, INT, IVL, MO, ON, PIVL,
    PN, PQ, QTY, REAL, RTO, SC, ST, TEL, TS, URL, UVP, AD, ADXP, CO, CR, HXIT,
)

logger = logging.getLogger(__name__)

# Required attributes per HL7 v3 data type specification
# Based on HL7 v3 Data Types specification v3.0
DATATYPE_REQUIRED_ATTRIBUTES = {
    "CD": {
        "core": [],  # CD has optional attributes
        "optional_but_common": ["code", "code_system", "display_name"],
    },
    "CE": {
        "core": [],  # CE has optional attributes
        "optional_but_common": ["code", "code_system", "display_name"],
    },
    "CS": {
        "core": [],  # CS has optional attributes
        "optional_but_common": ["code"],
    },
    "CV": {
        "core": [],  # CV has optional attributes
        "optional_but_common": ["code", "code_system", "display_name"],
    },
    "ED": {
        "core": [],  # ED has optional attributes
        "optional_but_common": ["media_type", "data"],
    },
    "II": {
        "core": ["root"],  # root is typically required
        "optional_but_common": ["extension"],
    },
    "TS": {
        "core": ["value"],  # value is typically required
        "optional_but_common": [],
    },
    "PN": {
        "core": [],  # PN has optional attributes
        "optional_but_common": ["part"],
    },
    "PQ": {
        "core": ["value"],  # value is typically required
        "optional_but_common": ["unit"],
    },
    "MO": {
        "core": ["value"],  # value is typically required
        "optional_but_common": ["currency"],
    },
}

# Additional attributes that should be supported per HL7 v3 specification
DATATYPE_ADDITIONAL_ATTRIBUTES = {
    "CD": [
        "value_set",  # Value set OID
        "value_set_version",  # Value set version
    ],
    "CE": [
        "value_set",  # Value set OID
        "value_set_version",  # Value set version
    ],
    "ED": [
        "thumbnail",  # Thumbnail image
        "representation",  # Representation code
    ],
    "II": [
        "scope",  # Scope of identifier
    ],
    "TS": [
        "inclusive",  # Inclusive indicator
    ],
    "PN": [
        "delimiter",  # Delimiter
    ],
    "PQ": [
        "translation",  # Translation
    ],
}



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def verify_datatype_completeness(datatype_name: str, instance: Optional[object] = None) -> Tuple[bool, List[str]]:
    """
    Verify that a data type has all required attributes per HL7 v3 specification.
    
    Args:
        datatype_name: Name of data type (CD, CE, CS, II, TS, etc.)
        instance: Optional instance of the data type to check
        
    Returns:
        Tuple of (is_complete, list_of_missing_attributes)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting data type completeness verification for {datatype_name}")
    
    if datatype_name not in DATATYPE_REQUIRED_ATTRIBUTES:
        # Primitive types (ANY, BL, BN, etc.) don't have required attributes
        return True, []
    
    missing_attributes = []
    required_attrs = DATATYPE_REQUIRED_ATTRIBUTES[datatype_name].get("core", [])
    
    # If instance provided, check actual attributes
    if instance:
        for attr in required_attrs:
            if not hasattr(instance, attr):
                missing_attributes.append(f"{datatype_name}.{attr}")
            elif getattr(instance, attr) is None:
                # Check if None is allowed (depends on context)
                pass
    
    is_complete = len(missing_attributes) == 0
    
    logger.info(f"[{current_time}] Data type completeness verification completed: "
                f"is_complete={is_complete}, missing={len(missing_attributes)}")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    return is_complete, missing_attributes


def verify_all_datatypes() -> Dict[str, Tuple[bool, List[str]]]:
    """
    Verify all data types for completeness.
    
    Returns:
        Dictionary mapping data type name to (is_complete, missing_attributes) tuple
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting verification of all data types")
    
    results = {}
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    for datatype_name in DATATYPE_REQUIRED_ATTRIBUTES.keys():
        is_complete, missing = verify_datatype_completeness(datatype_name)
        results[datatype_name] = (is_complete, missing)
    
    logger.info(f"[{current_time}] Verification of all data types completed")
    return results


def get_missing_datatype_attributes(datatype_name: str) -> List[str]:

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    """
    Get list of additional attributes that should be supported but may be missing.
    
    Args:
        datatype_name: Name of data type
        
    Returns:
        List of attribute names that should be added
    """
    return DATATYPE_ADDITIONAL_ATTRIBUTES.get(datatype_name, [])


def validate_datatype_instance(instance: object) -> Tuple[bool, List[str]]:
    """
    Validate a data type instance against HL7 v3 data type constraints.
    
    Args:
        instance: Data type instance to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting data type instance validation for {type(instance).__name__}")
    
    errors = []
    
    # Check for required attributes based on instance type
    class_name = type(instance).__name__
    if class_name in DATATYPE_REQUIRED_ATTRIBUTES:
        required_attrs = DATATYPE_REQUIRED_ATTRIBUTES[class_name].get("core", [])
        for attr in required_attrs:
            if not hasattr(instance, attr):
                errors.append(f"{class_name}.{attr} is required but missing")
            elif getattr(instance, attr) is None:
                errors.append(f"{class_name}.{attr} is required but is None")
    
    is_valid = len(errors) == 0
    
    logger.info(f"[{current_time}] Data type instance validation completed: "
                f"is_valid={is_valid}, errors={len(errors)}")
    
    return is_valid, errors
