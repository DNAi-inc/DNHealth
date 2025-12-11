# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Specification Compliance Verification.

Provides utilities to verify data type implementations against HL7 v3 specification.
This module helps ensure that data types match the official specification.

Note: This module provides programmatic verification utilities. For full compliance
verification, official HL7 v3 specification documents should be consulted.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime
import time
import inspect

from . import datatypes

logger = logging.getLogger(__name__)

# Test timeout: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


@dataclass
class SpecificationDataTypeDefinition:
    """
    Expected data type definition from HL7 v3 specification.
    
    This can be populated from official specification documents or
    from known reference implementations.
    """
    type_name: str
    base_type: Optional[str] = None
    required_attributes: List[str] = None
    optional_attributes: List[str] = None
    xml_element_name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class DataTypeComplianceIssue:
    """Represents a compliance issue found during verification."""
    type_name: str
    issue_type: str = ""  # missing_type, missing_attribute, missing_method, etc.
    message: str = ""
    severity: str = "warning"  # error, warning, info


def verify_data_type_specification_compliance(
    type_name: str,
    specification_definition: Optional[SpecificationDataTypeDefinition] = None,
    timeout: int = TEST_TIMEOUT
) -> Dict[str, Any]:
    """
    Verify data type implementation against specification.
    
    Compares implemented data type with expected specification definition.
    If specification_definition is not provided, performs internal consistency checks.
    
    Args:
        type_name: Data type name to verify
        specification_definition: Optional expected data type definition from specification
        timeout: Maximum time in seconds for verification (default: 300)
        
    Returns:
        Dictionary containing:
            - is_compliant: Boolean indicating overall compliance
            - issues: List of DataTypeComplianceIssue objects
            - has_xml_serialization: Boolean indicating XML serialization support
            - has_xml_deserialization: Boolean indicating XML deserialization support
            - attributes_found: List of attributes found in implementation
            - methods_found: List of methods found in implementation
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting specification compliance verification for data type: {type_name}")
    
    issues: List[DataTypeComplianceIssue] = []
    attributes_found: List[str] = []
    methods_found: List[str] = []
    has_xml_serialization = False
    has_xml_deserialization = False
    
    # Try to get the data type class
    try:
        data_type_class = getattr(datatypes, type_name, None)
        
        if data_type_class is None:
            issue = DataTypeComplianceIssue(
                type_name=type_name,
                issue_type="missing_type",
                message=f"Data type {type_name} is not implemented",
                severity="error"
            )
            issues.append(issue)
            
            elapsed = time.time() - start_time
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.warning(f"[{completion_time}] Specification compliance verification failed for {type_name}: type not found")
            
            return {
                "is_compliant": False,
                "issues": [issue.__dict__ for issue in issues],
                "has_xml_serialization": False,
                "has_xml_deserialization": False,
                "attributes_found": [],
                "methods_found": [],
                "verification_time": elapsed,
                "completion_time": completion_time,
            }
        
        # Inspect the class
        if inspect.isclass(data_type_class):
            # Get attributes
            for name, value in inspect.getmembers(data_type_class):
                if not name.startswith("_") and not inspect.ismethod(value) and not inspect.isfunction(value):
                    attributes_found.append(name)
            
            # Get methods
            for name, value in inspect.getmembers(data_type_class):
                if inspect.ismethod(value) or inspect.isfunction(value):
                    methods_found.append(name)
            
            # Check for XML serialization
            if hasattr(data_type_class, "to_xml") or hasattr(data_type_class, "to_xml_element"):
                has_xml_serialization = True
            else:
                issue = DataTypeComplianceIssue(
                    type_name=type_name,
                    issue_type="missing_xml_serialization",
                    message=f"Data type {type_name} missing XML serialization method",
                    severity="warning"
                )
                issues.append(issue)
            
            # Check for XML deserialization
            if hasattr(data_type_class, "from_xml") or hasattr(data_type_class, "from_xml_element"):
                has_xml_deserialization = True
            else:
                issue = DataTypeComplianceIssue(
                    type_name=type_name,
                    issue_type="missing_xml_deserialization",
                    message=f"Data type {type_name} missing XML deserialization method",
                    severity="warning"
                )
                issues.append(issue)
        
        # If specification provided, compare against it
        if specification_definition:
            # Check required attributes
            if specification_definition.required_attributes:
                for req_attr in specification_definition.required_attributes:
                    if req_attr not in attributes_found:
                        issue = DataTypeComplianceIssue(
                            type_name=type_name,
                            issue_type="missing_required_attribute",
                            message=f"Data type {type_name} missing required attribute: {req_attr}",
                            severity="error"
                        )
                        issues.append(issue)
            
            # Check required methods
            required_methods = ["to_xml", "from_xml"]
            for req_method in required_methods:
                if req_method not in methods_found:
                    issue = DataTypeComplianceIssue(
                        type_name=type_name,
                        issue_type="missing_required_method",
                        message=f"Data type {type_name} missing required method: {req_method}",
                        severity="error"
                    )
                    issues.append(issue)
    
    except Exception as e:
        issue = DataTypeComplianceIssue(
            type_name=type_name,
            issue_type="verification_error",
            message=f"Error during verification: {str(e)}",
            severity="error"
        )
        issues.append(issue)
        logger.error(f"Error verifying {type_name}: {e}")
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine overall compliance
    error_issues = [issue for issue in issues if issue.severity == "error"]
    is_compliant = len(error_issues) == 0
    
    if is_compliant:
        logger.info(f"[{completion_time}] Specification compliance verification passed for {type_name} ({len(issues)} warnings/info)")
    else:
        logger.warning(f"[{completion_time}] Specification compliance verification found {len(error_issues)} errors for {type_name}")
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return {
        "is_compliant": is_compliant,
        "issues": [issue.__dict__ for issue in issues],
        "error_count": len(error_issues),
        "warning_count": len([issue for issue in issues if issue.severity == "warning"]),
        "info_count": len([issue for issue in issues if issue.severity == "info"]),
        "has_xml_serialization": has_xml_serialization,
        "has_xml_deserialization": has_xml_deserialization,
        "attributes_found": attributes_found,
        "methods_found": methods_found,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }


def get_all_implemented_data_types() -> List[str]:
    """
    Get list of all implemented HL7 v3 data types.
    
    Returns:
        List of data type names
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Retrieving list of implemented data types")
    
    # Known HL7 v3 data types - check what's actually in the datatypes module
    known_types = [
        # Primitive types
        "ANY", "BL", "BN", "BAG", "LIST", "SET", "BIN",
        # Complex types
        "CD", "CE", "CS", "CV", "ED", "EIVL", "EN", "ENXP", "GTS", "II", "INT",
        "IVL", "MO", "ON", "PIVL", "PN", "PQ", "QTY", "REAL", "RTO", "SC", "ST",
        "TEL", "TN", "TS", "URL", "UVP", "AD", "ADXP", "CO", "CR", "HXIT",
        # Interval types
        "IVL_PQ", "IVL_TS", "PIVL_TS", "UVN_TS", "QTY_PQ", "QTY_TS",
        # List types
        "LIST_CE", "LIST_II", "LIST_MO", "LIST_PQ", "LIST_TS", "LIST_INT",
        # Ratio types
        "RTO_MO_PQ", "RTO_PQ_PQ",
        # Sequence list types
        "SLIST", "SLIST_PQ", "SLIST_TS",
        # Set expression types
        "SXCM", "SXCM_TS", "SXPR", "SXPR_TS",
        # Probability distribution types
        "NPPD", "PPD", "PPD_CD", "PPD_PQ", "PPD_TS", "PRPA",
        # Query types
        "QSC", "QSI", "QSS", "QSU",
        # Other types
        "PQR", "UUID", "ANYNonNull", "URG", "UVC", "UVP_TS",
    ]
    
    # Filter to only types that actually exist in the datatypes module
    implemented = []
    for type_name in known_types:
        try:
            if hasattr(datatypes, type_name):
                implemented.append(type_name)
            # Also check if it's a class or alias
            elif type_name in dir(datatypes):
                implemented.append(type_name)
        except:
            pass
    
    logger.debug(f"[{current_time}] Found {len(implemented)} implemented data types")
    return sorted(implemented)


def verify_all_data_types_specification_compliance(
    specification_data: Optional[Dict[str, SpecificationDataTypeDefinition]] = None,
    timeout: int = TEST_TIMEOUT
) -> Dict[str, Any]:
    """
    Verify all implemented data types against specification.
    
    Args:
        specification_data: Optional dictionary mapping type names to their specification definitions
        timeout: Maximum time in seconds for verification (default: 300)
        
    Returns:
        Dictionary containing:
            - total_types: Total number of types verified
            - compliant_types: Number of compliant types
            - non_compliant_types: Number of non-compliant types
            - type_results: Dictionary mapping type names to their verification results
            - overall_compliance: Overall compliance status
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting specification compliance verification for all data types")
    
    types = get_all_implemented_data_types()
    type_results: Dict[str, Dict[str, Any]] = {}
    compliant_count = 0
    non_compliant_count = 0
    
    for type_name in types:
        if time.time() - start_time > timeout:
            logger.warning(f"Verification timeout exceeded after {timeout} seconds")
            break
        
        spec_def = None
        if specification_data and type_name in specification_data:
            spec_def = specification_data[type_name]
        
        result = verify_data_type_specification_compliance(
            type_name=type_name,
            specification_definition=spec_def,
            timeout=timeout - (time.time() - start_time)
        )
        
        type_results[type_name] = result
        
        if result["is_compliant"]:
            compliant_count += 1
        else:
            non_compliant_count += 1
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    overall_compliance = non_compliant_count == 0
    
    logger.info(
        f"[{completion_time}] Specification compliance verification completed: "
        f"{compliant_count} compliant, {non_compliant_count} non-compliant out of {len(types)} types"
    )
    
    return {
        "total_types": len(types),
        "compliant_types": compliant_count,
        "non_compliant_types": non_compliant_count,
        "type_results": type_results,
        "overall_compliance": overall_compliance,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }


def generate_data_type_compliance_report(
    verification_results: Dict[str, Any],
    output_file: Optional[str] = None
) -> str:
    """
    Generate a human-readable compliance report from verification results.
    
    Args:
        verification_results: Results from verify_all_data_types_specification_compliance()
        output_file: Optional file path to write report to
        
    Returns:
        Report string
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "=" * 80,
        "HL7 v3 Data Type Specification Compliance Report",
        "=" * 80,
        f"Generated: {current_time}",
        "",
        f"Total Types: {verification_results['total_types']}",
        f"Compliant Types: {verification_results['compliant_types']}",
        f"Non-Compliant Types: {verification_results['non_compliant_types']}",
        f"Overall Compliance: {'COMPLIANT' if verification_results['overall_compliance'] else 'NON-COMPLIANT'}",
        f"Verification Time: {verification_results['verification_time']:.2f} seconds",
        "",
        "=" * 80,
        "Type Details",
        "=" * 80,
        ""
    ]
    
    # Add type details
    for type_name, result in verification_results["type_results"].items():
        status = "COMPLIANT" if result["is_compliant"] else "NON-COMPLIANT"
        report_lines.append(f"Type: {type_name} - {status}")
        report_lines.append(f"  XML Serialization: {'Yes' if result['has_xml_serialization'] else 'No'}")
        report_lines.append(f"  XML Deserialization: {'Yes' if result['has_xml_deserialization'] else 'No'}")
        report_lines.append(f"  Errors: {result['error_count']}")
        report_lines.append(f"  Warnings: {result['warning_count']}")
        report_lines.append(f"  Info: {result['info_count']}")
        
        # Add issue details
        if result["issues"]:
            report_lines.append("  Issues:")
            for issue in result["issues"][:10]:  # Limit to first 10 issues
                report_lines.append(f"    [{issue['severity'].upper()}] {issue['message']}")
            if len(result["issues"]) > 10:
                report_lines.append(f"    ... and {len(result['issues']) - 10} more issues")
        
        report_lines.append("")
    
    report_lines.append("=" * 80)
    report_lines.append(f"Report completed at: {current_time}")
    report_lines.append("=" * 80)
    
    report = "\n".join(report_lines)
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Compliance report written to: {output_file}")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    return report


def verify_message_id_format(message_id) -> Dict[str, Any]:
    """
    Verify message ID format matches specification (II data type).
    
    Verifies that a message ID follows HL7 v3 II (Instance Identifier) specification:
    - Uses II data type
    - Root is valid OID format (dotted decimal notation)
    - Extension is valid UUID format (preferred) or other valid format
    
    Args:
        message_id: II data type instance to verify
        
    Returns:
        Dictionary containing:
            - is_compliant: Boolean indicating format compliance
            - issues: List of format issues found
            - oid_format_valid: Boolean indicating OID format validity
            - uuid_format_valid: Boolean indicating UUID format validity
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Verifying message ID format compliance")
    
    issues: List[str] = []
    oid_format_valid = False
    uuid_format_valid = False
    
    # Import II data type
    from .datatypes import II
    import re
    
    # Verify II data type
    if not isinstance(message_id, II):
        issues.append(f"Message ID should be II data type, got {type(message_id).__name__}")
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.warning(f"[{completion_time}] Message ID format verification failed: not II data type")
        return {
            "is_compliant": False,
            "issues": issues,
            "oid_format_valid": False,
            "uuid_format_valid": False,
            "verification_time": elapsed,
            "completion_time": completion_time,
        }
    
    # Verify root is valid OID format (dotted decimal notation: digits.digits.digits...)
    oid_pattern = r'^(\d+\.)+\d+$'
    if re.match(oid_pattern, message_id.root):
        oid_format_valid = True
    else:
        issues.append(f"Message ID root should be valid OID format (dotted decimal), got: {message_id.root}")
    
    # Verify extension is valid UUID format (8-4-4-4-12 hex digits)
    if message_id.extension:
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if re.match(uuid_pattern, message_id.extension, re.IGNORECASE):
            uuid_format_valid = True
        else:
            issues.append(f"Message ID extension should be valid UUID format (8-4-4-4-12 hex), got: {message_id.extension}")
    else:
        issues.append("Message ID extension is missing")
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    is_compliant = len(issues) == 0
    
    if is_compliant:
        logger.info(f"[{completion_time}] Message ID format verification passed")
    else:
        logger.warning(f"[{completion_time}] Message ID format verification found {len(issues)} issues")
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return {
        "is_compliant": is_compliant,
        "issues": issues,
        "oid_format_valid": oid_format_valid,
        "uuid_format_valid": uuid_format_valid,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }


def verify_timestamp_format(timestamp) -> Dict[str, Any]:
    """
    Verify timestamp format matches specification (TS data type, ISO 8601).
    
    Verifies that a timestamp follows HL7 v3 TS (Time Stamp) specification:
    - Uses TS data type
    - Value is valid ISO 8601 format
    - Format: YYYYMMDDHHmmss[.s[s[s[s]]]][+/-ZZzz] or YYYY-MM-DDTHH:mm:ss[.s[s[s[s]]]][+/-ZZzz]
    
    Args:
        timestamp: TS data type instance to verify
        
    Returns:
        Dictionary containing:
            - is_compliant: Boolean indicating format compliance
            - issues: List of format issues found
            - iso8601_format_valid: Boolean indicating ISO 8601 format validity
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Verifying timestamp format compliance")
    
    issues: List[str] = []
    iso8601_format_valid = False
    
    # Import TS data type
    from .datatypes import TS
    import re
    
    # Verify TS data type
    if not isinstance(timestamp, TS):
        issues.append(f"Timestamp should be TS data type, got {type(timestamp).__name__}")
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.warning(f"[{completion_time}] Timestamp format verification failed: not TS data type")
        return {
            "is_compliant": False,
            "issues": issues,
            "iso8601_format_valid": False,
            "verification_time": elapsed,
            "completion_time": completion_time,
        }
    
    # Verify timestamp value format
    if not timestamp.value:
        issues.append("Timestamp value is missing")
    else:
        # HL7 v3 TS format patterns:
        # YYYYMMDDHHmmss[.s[s[s[s]]]][+/-ZZzz] (compact format)
        # YYYY-MM-DDTHH:mm:ss[.s[s[s[s]]]][+/-ZZzz] (ISO 8601 extended format)
        
        # Pattern for compact format: YYYYMMDDHHmmss with optional fractional seconds and timezone
        compact_pattern = r'^\d{8}\d{6}(\.\d{1,4})?([+-]\d{4}|Z)?$'
        
        # Pattern for extended format: YYYY-MM-DDTHH:mm:ss with optional fractional seconds and timezone
        extended_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,4})?([+-]\d{2}:\d{2}|Z)?$'
        
        # Remove any whitespace
        value_clean = timestamp.value.strip()
        
        # Check against both patterns
        if re.match(compact_pattern, value_clean) or re.match(extended_pattern, value_clean):
            iso8601_format_valid = True
        else:
            issues.append(f"Timestamp value should be valid ISO 8601 format, got: {timestamp.value}")
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    is_compliant = len(issues) == 0
    
    if is_compliant:
        logger.info(f"[{completion_time}] Timestamp format verification passed")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    else:
        logger.warning(f"[{completion_time}] Timestamp format verification found {len(issues)} issues")
    
    return {
        "is_compliant": is_compliant,
        "issues": issues,
        "iso8601_format_valid": iso8601_format_valid,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }


def verify_xml_structure(xml_string: str, expected_namespace: Optional[str] = None) -> Dict[str, Any]:
    """
    Verify XML structure matches HL7 v3 specification.
    
    Verifies that XML is well-formed and follows HL7 v3 structure requirements:
    - XML is well-formed
    - Root element structure is valid
    - Namespace usage is correct (default: urn:hl7-org:v3)
    
    Args:
        xml_string: XML string to verify
        expected_namespace: Expected namespace URI (default: urn:hl7-org:v3)
        
    Returns:
        Dictionary containing:
            - is_compliant: Boolean indicating structure compliance
            - issues: List of structure issues found
            - is_well_formed: Boolean indicating XML well-formedness
            - namespace_valid: Boolean indicating namespace validity
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Verifying XML structure compliance")
    
    issues: List[str] = []
    is_well_formed = False
    namespace_valid = False
    
    if expected_namespace is None:
        expected_namespace = "urn:hl7-org:v3"
    
    import xml.etree.ElementTree as ET
    import re
    
    # Verify XML is well-formed
    try:
        root = ET.fromstring(xml_string)
        is_well_formed = True
    except ET.ParseError as e:
        issues.append(f"XML is not well-formed: {str(e)}")
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.warning(f"[{completion_time}] XML structure verification failed: not well-formed")
        return {
            "is_compliant": False,
            "issues": issues,
            "is_well_formed": False,
            "namespace_valid": False,
            "verification_time": elapsed,
            "completion_time": completion_time,
        }
    
    # Verify namespace usage
    namespace_match = re.search(r'xmlns="([^"]+)"', xml_string)
    if namespace_match:
        namespace = namespace_match.group(1)
        if namespace == expected_namespace:
            namespace_valid = True
        else:
            issues.append(f"XML namespace should be '{expected_namespace}', got: '{namespace}'")
    else:
        # Check for default namespace in root element
        if root.tag.startswith(f"{{{expected_namespace}}}"):
            namespace_valid = True
        else:
            issues.append(f"XML namespace not found or does not match expected '{expected_namespace}'")
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    is_compliant = len(issues) == 0
    
    if is_compliant:
        logger.info(f"[{completion_time}] XML structure verification passed")
    else:
        logger.warning(f"[{completion_time}] XML structure verification found {len(issues)} issues")
    
    return {
        "is_compliant": is_compliant,
        "issues": issues,
        "is_well_formed": is_well_formed,
        "namespace_valid": namespace_valid,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }
