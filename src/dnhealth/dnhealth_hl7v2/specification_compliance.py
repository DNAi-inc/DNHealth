# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Specification Compliance Verification.

Provides utilities to verify segment field definitions against HL7 v2.x specification.
This module helps ensure that field definitions match the official specification.

Note: This module provides programmatic verification utilities. For full compliance
verification, official HL7 v2.x specification documents should be consulted.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
from datetime import datetime
import time

from .segment_definitions import (
    get_field_definition,
    get_segment_fields,
    FieldDefinition,
    get_all_implemented_segments,
)

logger = logging.getLogger(__name__)

# Test timeout: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


@dataclass
class SpecificationFieldDefinition:
    """
    Expected field definition from HL7 v2.x specification.
    
    This can be populated from official specification documents or
    from known reference implementations.
    """
    field_index: int
    field_name: str
    data_type: str
    length: Optional[int] = None
    min_length: Optional[int] = None
    required: bool = False
    optional: bool = True
    repeating: bool = False
    table_binding: Optional[str] = None
    description: Optional[str] = None
    version_specific: Dict[str, Dict] = None


@dataclass
class ComplianceIssue:
    """Represents a compliance issue found during verification."""
    segment_name: str
    field_index: Optional[int] = None
    issue_type: str = ""  # missing_field, extra_field, data_type_mismatch, length_mismatch, etc.
    message: str = ""
    severity: str = "warning"  # error, warning, info


def verify_segment_field_specification_compliance(
    segment_name: str,
    specification_fields: Optional[Dict[int, SpecificationFieldDefinition]] = None,
    version: Optional[str] = None,    timeout: int = TEST_TIMEOUT
) -> Dict[str, Any]:
    """
    Verify segment field definitions against specification.
    
    Compares implemented field definitions with expected specification definitions.
    If specification_fields is not provided, performs internal consistency checks.
    
    Args:
        segment_name: Segment name to verify
        specification_fields: Optional dictionary of expected field definitions from specification
        version: Optional HL7 version (2.1-2.9)
        timeout: Maximum time in seconds for verification (default: 300)
        
    Returns:
        Dictionary containing:
            - is_compliant: Boolean indicating overall compliance
            - issues: List of ComplianceIssue objects
            - field_count: Number of fields verified
            - missing_fields: List of missing field indices
            - extra_fields: List of extra field indices
            - data_type_mismatches: List of data type mismatches
            - length_mismatches: List of length mismatches
            - required_status_mismatches: List of required/optional mismatches
            - table_binding_mismatches: List of table binding mismatches
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting specification compliance verification for segment: {segment_name}")
    
    issues: List[ComplianceIssue] = []
    missing_fields: List[int] = []
    extra_fields: List[int] = []
    data_type_mismatches: List[Dict[str, Any]] = []
    length_mismatches: List[Dict[str, Any]] = []
    required_status_mismatches: List[Dict[str, Any]] = []
    table_binding_mismatches: List[Dict[str, Any]] = []
    
    # Get implemented field definitions
    implemented_fields = get_segment_fields(segment_name, version=version)
    
    if not implemented_fields:
        issue = ComplianceIssue(
            segment_name=segment_name,
            issue_type="no_fields",
            message=f"Segment {segment_name} has no field definitions",
            severity="error"
        )
        issues.append(issue)
        
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.warning(f"[{completion_time}] Specification compliance verification failed for {segment_name}: no fields")
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return {
        "is_compliant": False,
        "issues": [issue.__dict__ for issue in issues],
        "field_count": 0,
        "missing_fields": missing_fields,
        "extra_fields": extra_fields,
        "data_type_mismatches": data_type_mismatches,
        "length_mismatches": length_mismatches,
        "required_status_mismatches": required_status_mismatches,
        "table_binding_mismatches": table_binding_mismatches,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }
    
    # If specification fields provided, compare against them
    if specification_fields:
        # Check for missing fields
        for spec_field_index, spec_field in specification_fields.items():
            if time.time() - start_time > timeout:
                logger.warning(f"Verification timeout exceeded for segment {segment_name}")
                break
                
            if spec_field_index not in implemented_fields:
                missing_fields.append(spec_field_index)
                issue = ComplianceIssue(
                    segment_name=segment_name,
                    field_index=spec_field_index,
                    issue_type="missing_field",
                    message=f"Field {spec_field_index} ({spec_field.field_name}) is missing from implementation",
                    severity="error"
                )
                issues.append(issue)
            else:
                # Compare field definitions
                impl_field = implemented_fields[spec_field_index]
                
                # Check data type
                if impl_field.data_type != spec_field.data_type:
                    data_type_mismatches.append({
                        "field_index": spec_field_index,
                        "expected": spec_field.data_type,
                        "actual": impl_field.data_type
                    })
                    issue = ComplianceIssue(
                        segment_name=segment_name,
                        field_index=spec_field_index,
                        issue_type="data_type_mismatch",
                        message=f"Field {spec_field_index} data type mismatch: expected {spec_field.data_type}, found {impl_field.data_type}",
                        severity="error"
                    )
                    issues.append(issue)
                
                # Check length (if specified)
                if spec_field.length is not None:
                    if impl_field.length != spec_field.length:
                        length_mismatches.append({
                            "field_index": spec_field_index,
                            "expected": spec_field.length,
                            "actual": impl_field.length
                        })
                        issue = ComplianceIssue(
                            segment_name=segment_name,
                            field_index=spec_field_index,
                            issue_type="length_mismatch",
                            message=f"Field {spec_field_index} length mismatch: expected {spec_field.length}, found {impl_field.length}",
                            severity="warning"
                        )
                        issues.append(issue)
                
                # Check required/optional status
                if impl_field.required != spec_field.required:
                    required_status_mismatches.append({
                        "field_index": spec_field_index,
                        "expected": spec_field.required,
                        "actual": impl_field.required
                    })
                    issue = ComplianceIssue(
                        segment_name=segment_name,
                        field_index=spec_field_index,
                        issue_type="required_status_mismatch",
                        message=f"Field {spec_field_index} required status mismatch: expected {spec_field.required}, found {impl_field.required}",
                        severity="warning"
                    )
                    issues.append(issue)
                
                # Check table binding
                if spec_field.table_binding is not None:
                    if impl_field.table_binding != spec_field.table_binding:
                        table_binding_mismatches.append({
                            "field_index": spec_field_index,
                            "expected": spec_field.table_binding,
                            "actual": impl_field.table_binding
                        })
                        issue = ComplianceIssue(
                            segment_name=segment_name,
                            field_index=spec_field_index,
                            issue_type="table_binding_mismatch",
                            message=f"Field {spec_field_index} table binding mismatch: expected {spec_field.table_binding}, found {impl_field.table_binding}",
                            severity="warning"
                        )
                        issues.append(issue)
        
        # Check for extra fields (fields in implementation but not in specification)
        for impl_field_index in implemented_fields:
            if time.time() - start_time > timeout:
                break
            if impl_field_index not in specification_fields:
                extra_fields.append(impl_field_index)
                issue = ComplianceIssue(
                    segment_name=segment_name,
                    field_index=impl_field_index,
                    issue_type="extra_field",
                    message=f"Field {impl_field_index} is in implementation but not in specification",
                    severity="info"
                )
                issues.append(issue)
    else:
        # No specification provided - perform internal consistency checks
        for field_index, field_def in implemented_fields.items():
            if time.time() - start_time > timeout:
                break
            # Check field definition consistency
            if not isinstance(field_def, FieldDefinition):
                issue = ComplianceIssue(
                    segment_name=segment_name,
                    field_index=field_index,
                    issue_type="invalid_field_definition",
                    message=f"Field {field_index} is not a valid FieldDefinition instance",
                    severity="error"
                )
                issues.append(issue)
            else:
                # Check required attributes
                if not field_def.field_name:
                    issue = ComplianceIssue(
                        segment_name=segment_name,
                        field_index=field_index,
                        issue_type="missing_field_name",
                        message=f"Field {field_index} missing field_name",
                        severity="error"
                    )
                    issues.append(issue)
                
                if not field_def.data_type:
                    issue = ComplianceIssue(
                        segment_name=segment_name,
                        field_index=field_index,
                        issue_type="missing_data_type",
                        message=f"Field {field_index} missing data_type",
                        severity="error"
                    )
                    issues.append(issue)
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine overall compliance
    error_issues = [issue for issue in issues if issue.severity == "error"]
    is_compliant = len(error_issues) == 0
    
    if is_compliant:
        logger.info(f"[{completion_time}] Specification compliance verification passed for {segment_name} ({len(issues)} warnings/info)")
    else:
        logger.warning(f"[{completion_time}] Specification compliance verification found {len(error_issues)} errors for {segment_name}")
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return {
        "is_compliant": is_compliant,
        "issues": [issue.__dict__ for issue in issues],
        "error_count": len(error_issues),
        "warning_count": len([issue for issue in issues if issue.severity == "warning"]),
        "info_count": len([issue for issue in issues if issue.severity == "info"]),
        "field_count": len(implemented_fields),
        "missing_fields": missing_fields,
        "extra_fields": extra_fields,
        "data_type_mismatches": data_type_mismatches,
        "length_mismatches": length_mismatches,
        "required_status_mismatches": required_status_mismatches,
        "table_binding_mismatches": table_binding_mismatches,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }


def verify_all_segments_specification_compliance(
    specification_data: Optional[Dict[str, Dict[int, SpecificationFieldDefinition]]] = None,
    timeout: int = TEST_TIMEOUT
) -> Dict[str, Any]:
    """
    Verify all implemented segments against specification.
    
    Args:
        specification_data: Optional dictionary mapping segment names to their specification field definitions
        timeout: Maximum time in seconds for verification (default: 300)
        
    Returns:
        Dictionary containing:
            - total_segments: Total number of segments verified
            - compliant_segments: Number of compliant segments
            - non_compliant_segments: Number of non-compliant segments
            - segment_results: Dictionary mapping segment names to their verification results
            - overall_compliance: Overall compliance status
            - verification_time: Time taken for verification
            - completion_time: Completion timestamp
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting specification compliance verification for all segments")
    
    segments = get_all_implemented_segments()
    segment_results: Dict[str, Dict[str, Any]] = {}
    compliant_count = 0
    non_compliant_count = 0
    
    for segment_name in segments:
        if time.time() - start_time > timeout:
            logger.warning(f"Verification timeout exceeded after {timeout} seconds")
            break
        
        spec_fields = None
        if specification_data and segment_name in specification_data:
            spec_fields = specification_data[segment_name]
        
        result = verify_segment_field_specification_compliance(
            segment_name=segment_name,
            specification_fields=spec_fields,
            timeout=timeout - (time.time() - start_time)
        )
        
        segment_results[segment_name] = result
        
        if result["is_compliant"]:
            compliant_count += 1
        else:
            non_compliant_count += 1
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    overall_compliance = non_compliant_count == 0
    
    logger.info(
        f"[{completion_time}] Specification compliance verification completed: "
        f"{compliant_count} compliant, {non_compliant_count} non-compliant out of {len(segments)} segments"
    )
    
    # Log completion timestamp at end of operation
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return {
        "total_segments": len(segments),
        "compliant_segments": compliant_count,
        "non_compliant_segments": non_compliant_count,
        "segment_results": segment_results,
        "overall_compliance": overall_compliance,
        "verification_time": elapsed,
        "completion_time": completion_time,
    }


def generate_specification_compliance_report(
    verification_results: Dict[str, Any],
    output_file: Optional[str] = None
) -> str:
    """
    Generate a human-readable compliance report from verification results.
    
    Args:
        verification_results: Results from verify_all_segments_specification_compliance()
        output_file: Optional file path to write report to
        
    Returns:
        Report string
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "=" * 80,
        "HL7 v2.x Segment Field Definition Specification Compliance Report",
        "=" * 80,
        f"Generated: {current_time}",
        "",
        f"Total Segments: {verification_results['total_segments']}",
        f"Compliant Segments: {verification_results['compliant_segments']}",
        f"Non-Compliant Segments: {verification_results['non_compliant_segments']}",
        f"Overall Compliance: {'COMPLIANT' if verification_results['overall_compliance'] else 'NON-COMPLIANT'}",
        f"Verification Time: {verification_results['verification_time']:.2f} seconds",
        "",
        "=" * 80,
        "Segment Details",
        "=" * 80,
        ""
    ]
    
    # Add segment details
    for segment_name, result in verification_results["segment_results"].items():
        status = "COMPLIANT" if result["is_compliant"] else "NON-COMPLIANT"
        report_lines.append(f"Segment: {segment_name} - {status}")
        report_lines.append(f"  Field Count: {result['field_count']}")
        report_lines.append(f"  Errors: {result['error_count']}")
        report_lines.append(f"  Warnings: {result['warning_count']}")
        report_lines.append(f"  Info: {result['info_count']}")
        
        if result["missing_fields"]:
            report_lines.append(f"  Missing Fields: {result['missing_fields']}")
        if result["extra_fields"]:
            report_lines.append(f"  Extra Fields: {result['extra_fields']}")
        if result["data_type_mismatches"]:
            report_lines.append(f"  Data Type Mismatches: {len(result['data_type_mismatches'])}")
        if result["length_mismatches"]:
            report_lines.append(f"  Length Mismatches: {len(result['length_mismatches'])}")
        
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
    logger.info(f"Current Time at End of Operations: {current_time}")
    
    return report
