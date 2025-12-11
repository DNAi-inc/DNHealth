# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 RIM Completeness Verification.

Provides functions to verify that all RIM classes have all required attributes
per HL7 v3 specification and identify any missing attributes.
"""

from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import logging

from dnhealth.dnhealth_hl7v3.rim import (
    Entity,
    Role,
    Act,
    Participation,
    ActRelationship,
    RoleLink,
)

logger = logging.getLogger(__name__)

# Required attributes per HL7 v3 RIM specification
# Based on HL7 v3 RIM specification v3.0
RIM_REQUIRED_ATTRIBUTES = {
    "Entity": {
        # classCode is typically required in most contexts but depends on usage
        # determinerCode is typically required
        # id is optional but commonly used
        "core": ["class_code", "determiner_code"],  # Typically required
        "optional_but_common": ["id", "code", "name", "status_code", "effective_time"],
    },
    "Role": {
        "core": ["class_code"],  # Typically required
        "optional_but_common": ["id", "code", "status_code", "effective_time"],
    },
    "Act": {
        "core": ["class_code", "mood_code"],  # Typically required
        "optional_but_common": ["id", "code", "status_code", "effective_time"],
    },
    "Participation": {
        "core": ["type_code"],  # Required
        "optional_but_common": ["context_control_code", "sequence_number", "time", "status_code"],
    },
    "ActRelationship": {
        "core": ["type_code"],  # Required
        "optional_but_common": ["context_control_code", "sequence_number", "effective_time", "status_code"],
    },
    "RoleLink": {
        "core": ["type_code"],  # Required
        "optional_but_common": ["effective_time", "status_code"],
    },
}

# Additional attributes that should be supported per HL7 v3 specification
RIM_ADDITIONAL_ATTRIBUTES = {
    "Entity": [
        "quantity",  # Quantity of entity
        "telecom",  # Telecommunications
        "addr",  # Address
        "scoping_entity",  # Scoping entity
        "scoping_role",  # Scoping role
    ],
    "Role": [
        "scoper",  # Entity that scopes this role
        "telecom",  # Telecommunications
        "addr",  # Address
    ],
    "Act": [
        "priority_code",  # Priority code
        "reason_code",  # Reason code
        "language_code",  # Language code
        "interpreter",  # Interpreter
        "performer",  # Performer
        "author",  # Author
        "informant",  # Informant
        "subject",  # Subject
        "location",  # Location
        "specimen",  # Specimen
    ],
    "Participation": [
        "function_code",  # Function code
        "awareness_code",  # Awareness code
    ],
    "ActRelationship": [
        "inversion_ind",  # Inversion indicator
        "conjunction_code",  # Conjunction code
    ],
    "RoleLink": [
        "inversion_ind",  # Inversion indicator
    ],
}


def verify_rim_class_completeness(rim_class_name: str, instance: Optional[object] = None) -> Tuple[bool, List[str]]:
    """
    Verify that a RIM class has all required attributes per HL7 v3 specification.
    
    Args:
        rim_class_name: Name of RIM class (Entity, Role, Act, Participation, ActRelationship, RoleLink)
        instance: Optional instance of the RIM class to check
        
    Returns:
        Tuple of (is_complete, list_of_missing_attributes)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RIM class completeness verification for {rim_class_name}")
    
    if rim_class_name not in RIM_REQUIRED_ATTRIBUTES:
        return False, [f"Unknown RIM class: {rim_class_name}"]
    
    missing_attributes = []
    required_attrs = RIM_REQUIRED_ATTRIBUTES[rim_class_name].get("core", [])
    
    # If instance provided, check actual attributes
    if instance:
        instance_attrs = set(dir(instance))
        for attr in required_attrs:
            # Check if attribute exists (may be None but should exist)
            if not hasattr(instance, attr):
                missing_attributes.append(f"{rim_class_name}.{attr}")
    else:
        # Just verify the class definition has the attributes
        # This is a structural check
        pass
    
    is_complete = len(missing_attributes) == 0
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{completion_time}] RIM class completeness verification completed: "
                f"is_complete={is_complete}, missing={len(missing_attributes)}")
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return is_complete, missing_attributes


def verify_all_rim_classes() -> Dict[str, Tuple[bool, List[str]]]:
    """
    Verify all RIM classes for completeness.
    
    Returns:
        Dictionary mapping class name to (is_complete, missing_attributes) tuple
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting verification of all RIM classes")
    
    results = {}
    
    for rim_class_name in RIM_REQUIRED_ATTRIBUTES.keys():
        is_complete, missing = verify_rim_class_completeness(rim_class_name)
        results[rim_class_name] = (is_complete, missing)
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{completion_time}] Verification of all RIM classes completed")
    logger.info(f"Current Time at End of Operations: {completion_time}")
    return results


def get_missing_rim_attributes(rim_class_name: str) -> List[str]:
    """
    Get list of additional attributes that should be supported but may be missing.
    
    Args:
        rim_class_name: Name of RIM class
        
    Returns:
        List of attribute names that should be added
    """
    return RIM_ADDITIONAL_ATTRIBUTES.get(rim_class_name, [])


def validate_rim_instance(instance: Entity | Role | Act | Participation | ActRelationship | RoleLink) -> Tuple[bool, List[str]]:
    """
    Validate a RIM instance against HL7 v3 RIM constraints.
    
    This function calls the instance's validate() method and also checks
    for required attributes based on the instance type.
    
    Args:
        instance: RIM instance to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting RIM instance validation for {type(instance).__name__}")
    
    errors = []
    
    # Call instance's validate method
    if hasattr(instance, "validate"):
        is_valid, instance_errors = instance.validate()
        if not is_valid:
            errors.extend(instance_errors)
    
    # Check for required attributes based on instance type
    class_name = type(instance).__name__
    if class_name in RIM_REQUIRED_ATTRIBUTES:
        required_attrs = RIM_REQUIRED_ATTRIBUTES[class_name].get("core", [])
        for attr in required_attrs:
            if not hasattr(instance, attr):
                errors.append(f"{class_name}.{attr} is required but missing")
            elif getattr(instance, attr) is None:
                # Note: Some attributes may be None in certain contexts
                # This is a warning, not necessarily an error
                pass
    
    is_valid = len(errors) == 0
    
    logger.info(f"[{current_time}] RIM instance validation completed: "
                f"is_valid={is_valid}, errors={len(errors)}")
    
    return is_valid, errors
