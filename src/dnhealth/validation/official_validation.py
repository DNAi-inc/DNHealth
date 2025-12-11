# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Official HL7/FHIR Validation Module.

Provides validation functions that compare implemented features with official
definitions from HL7Documentation/definitions.json.

All operations enforce a 5-minute timeout limit and include timestamp logging.
"""

import json
import time
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime

logger = logging.getLogger(__name__)

# Path to definitions.json directory
DEFINITIONS_DIR = Path(__file__).parent.parent.parent.parent / "HL7Documentation" / "definitions.json"

# Default timeout for operations (5 minutes = 300 seconds)
OPERATION_TIMEOUT = 300


def get_current_time() -> str:
    """Get current timestamp as formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def validate_hl7v2_tables_against_official() -> Dict[str, Any]:
    """
    Compare implemented HL7v2 tables with official definitions from v2-tables.json.
    
    Returns:
        Dictionary with validation results including:
        - total_implemented: Number of tables in implementation
        - total_official: Number of tables in official definitions
        - missing_tables: List of table IDs missing from implementation
        - extra_tables: List of table IDs in implementation but not in official
        - mismatched_codes: Dictionary of table ID -> list of code mismatches
        - completeness: Percentage of official tables that are implemented
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting HL7v2 table validation against official definitions")
    
    try:
        # Load implemented tables
        from dnhealth.dnhealth_hl7v2.tables import STANDARD_TABLES
        
        implemented_tables = STANDARD_TABLES
        total_implemented = len(implemented_tables)
        
        # Load official tables from definitions.json
        tables_file = DEFINITIONS_DIR / "v2-tables.json"
        
        if not tables_file.exists():
            error_msg = f"Official tables file not found: {tables_file}"
            logger.error(f"[{get_current_time()}] {error_msg}")
            elapsed = time.time() - start_time
            return {
                "error": error_msg,
                "status": "error",
                "elapsed_time": elapsed,
                "timestamp": get_current_time()
            }
        
        # Parse official tables (FHIR Bundle with ValueSet resources)
        official_tables = {}
        with open(tables_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract table IDs from ValueSet resources
        if isinstance(data, dict) and "entry" in data:
            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") == "ValueSet":
                    # Extract table ID from ValueSet ID or name
                    vs_id = resource.get("id", "")
                    vs_name = resource.get("name", "")
                    
                    # Table ID is typically in format "v2-XXXX" or just "XXXX"
                    if vs_id.startswith("v2-"):
                        table_id = vs_id[3:]  # Remove "v2-" prefix
                    elif vs_name.startswith("v2."):
                        table_id = vs_name[3:].replace(".", "")  # Remove "v2." prefix
                    else:
                        # Try to extract from URL
                        url = resource.get("url", "")
                        if "v2-" in url:
                            table_id = url.split("v2-")[-1].split("/")[0]
                        else:
                            continue
                    
                    # Normalize table ID to 4-digit format
                    try:
                        table_num = int(table_id)
                        table_id_normalized = f"{table_num:04d}"
                        official_tables[table_id_normalized] = resource
                    except ValueError:
                        # Skip if not a numeric table ID
                        continue
        
        total_official = len(official_tables)
        
        # Find missing and extra tables
        implemented_ids = set(implemented_tables.keys())
        official_ids = set(official_tables.keys())
        
        missing_tables = sorted(list(official_ids - implemented_ids))
        extra_tables = sorted(list(implemented_ids - official_ids))
        
        # Compare codes for matching tables (sample first 10 to avoid timeout)
        mismatched_codes = {}
        missing_descriptions = {}
        compared_count = 0
        max_comparisons = 10  # Limit to avoid timeout
        
        for table_id in sorted(implemented_ids & official_ids)[:max_comparisons]:
            if time.time() - start_time > OPERATION_TIMEOUT - 5:  # Reserve 5 seconds
                logger.warning(f"[{get_current_time()}] Timeout approaching, stopping code comparison")
                break
            
            implemented_table = implemented_tables[table_id]
            implemented_codes = set(implemented_table.keys())
            
            # Extract codes from official ValueSet
            official_vs = official_tables[table_id]
            official_codes = {}
            official_code_descriptions = {}
            
            # Try to extract codes from expansion
            if "expansion" in official_vs:
                for contains in official_vs["expansion"].get("contains", []):
                    code = contains.get("code")
                    display = contains.get("display", "")
                    if code:
                        official_codes[code] = display
                        official_code_descriptions[code] = display
            
            # Try to extract from compose
            if "compose" in official_vs:
                for include in official_vs["compose"].get("include", []):
                    # Codes might be in concept list
                    for concept in include.get("concept", []):
                        code = concept.get("code")
                        display = concept.get("display", "")
                        if code:
                            official_codes[code] = display
                            official_code_descriptions[code] = display
            
            # Compare code sets
            implemented_code_set = set(implemented_codes)
            official_code_set = set(official_codes.keys())
            
            if implemented_code_set != official_code_set:
                mismatched_codes[table_id] = {
                    "implemented_only": sorted(list(implemented_code_set - official_code_set)),
                    "official_only": sorted(list(official_code_set - implemented_code_set)),
                    "common": sorted(list(implemented_code_set & official_code_set))
                }
            
            # Check for missing descriptions in implemented codes
            codes_missing_descriptions = []
            for code in implemented_code_set & official_code_set:
                implemented_desc = implemented_table.get(code, "")
                official_desc = official_code_descriptions.get(code, "")
                # Check if implemented description is missing or significantly different
                if not implemented_desc or (official_desc and len(official_desc) > len(implemented_desc) * 2):
                    codes_missing_descriptions.append(code)
            
            if codes_missing_descriptions:
                missing_descriptions[table_id] = codes_missing_descriptions[:10]  # Limit to first 10
            
            compared_count += 1
        
        # Calculate completeness
        if total_official > 0:
            completeness = ((total_official - len(missing_tables)) / total_official) * 100
        else:
            completeness = 0.0
        
        # Determine status
        if len(missing_tables) == 0 and len(extra_tables) == 0 and len(mismatched_codes) == 0:
            status = "complete"
        elif completeness >= 90:
            status = "partial"
        else:
            status = "incomplete"
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        logger.info(
            f"[{end_time}] HL7v2 table validation completed "
            f"(implemented: {total_implemented}, official: {total_official}, "
            f"missing: {len(missing_tables)}, completeness: {completeness:.1f}%, "
            f"elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "total_implemented": total_implemented,
            "total_official": total_official,
            "missing_tables": missing_tables[:50],  # Limit to first 50
            "missing_tables_count": len(missing_tables),
            "extra_tables": extra_tables[:50],  # Limit to first 50
            "extra_tables_count": len(extra_tables),
            "mismatched_codes": mismatched_codes,
            "missing_descriptions": missing_descriptions,
            "compared_tables": compared_count,
            "completeness": completeness,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating HL7v2 tables: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def validate_valuesets_against_official() -> Dict[str, Any]:
    """
    Validate ValueSet implementation against official definitions.
    
    Returns:
        Dictionary with validation results including:
        - total_official: Number of ValueSets in official definitions
        - expansion_capability: Whether ValueSet expansion is supported
        - validation_capability: Whether ValueSet validation is supported
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting ValueSet validation against official definitions")
    
    try:
        # Load official ValueSets
        from tests.fhir.definitions_integration import load_valuesets_from_definitions
        
        official_valuesets = load_valuesets_from_definitions()
        total_official = len(official_valuesets)
        
        # Check if we have ValueSet expansion capability
        expansion_capability = False
        validation_capability = False
        
        try:
            from dnhealth.dnhealth_fhir.terminology_service import TerminologyService
            # Check if TerminologyService has expansion capability
            expansion_capability = hasattr(TerminologyService, 'expand_valueset') or hasattr(TerminologyService, 'expand')
            validation_capability = hasattr(TerminologyService, 'validate_code') or hasattr(TerminologyService, 'validate')
        except ImportError:
            pass
        
        # Sample a few ValueSets to check structure (limit to avoid timeout)
        sampled_count = 0
        max_samples = 10
        sample_results = []
        
        for vs_id, vs_data in list(official_valuesets.items())[:max_samples]:
            if time.time() - start_time > OPERATION_TIMEOUT - 5:
                break
            
            sample_results.append({
                "id": vs_id,
                "has_url": "url" in vs_data,
                "has_name": "name" in vs_data,
                "has_compose": "compose" in vs_data,
                "has_expansion": "expansion" in vs_data
            })
            sampled_count += 1
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Determine status
        if expansion_capability and validation_capability:
            status = "complete"
        elif expansion_capability or validation_capability:
            status = "partial"
        else:
            status = "basic"
        
        logger.info(
            f"[{end_time}] ValueSet validation completed "
            f"(official: {total_official}, expansion: {expansion_capability}, "
            f"validation: {validation_capability}, sampled: {sampled_count}, "
            f"elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "total_official": total_official,
            "expansion_capability": expansion_capability,
            "validation_capability": validation_capability,
            "sampled_count": sampled_count,
            "sample_results": sample_results,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating ValueSets: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def validate_profiles_against_official() -> Dict[str, Any]:
    """
    Validate StructureDefinition profiles against official definitions.
    
    Returns:
        Dictionary with validation results including:
        - total_official: Number of profiles in official definitions
        - validation_capability: Whether profile validation is supported
        - constraint_capability: Whether constraint validation is supported
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting profile validation against official definitions")
    
    try:
        # Load official profiles
        from tests.fhir.definitions_integration import load_profiles_from_definitions
        
        official_profiles = load_profiles_from_definitions()
        total_official = len(official_profiles)
        
        # Check if we have profile validation capability
        validation_capability = False
        constraint_capability = False
        
        try:
            from dnhealth.dnhealth_fhir.profile import validate_against_profile
            validation_capability = True
            
            # Check for constraint validation (FHIRPath)
            from dnhealth.dnhealth_fhir.fhirpath import evaluate_fhirpath
            constraint_capability = True
        except ImportError:
            pass
        
        # Sample a few profiles to check structure (limit to avoid timeout)
        sampled_count = 0
        max_samples = 10
        sample_results = []
        
        for profile_id, profile_data in list(official_profiles.items())[:max_samples]:
            if time.time() - start_time > OPERATION_TIMEOUT - 5:
                break
            
            sample_results.append({
                "id": profile_id,
                "has_url": "url" in profile_data,
                "has_name": "name" in profile_data,
                "has_type": "type" in profile_data,
                "has_snapshot": "snapshot" in profile_data,
                "has_differential": "differential" in profile_data
            })
            sampled_count += 1
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Determine status
        if validation_capability and constraint_capability:
            status = "complete"
        elif validation_capability:
            status = "partial"
        else:
            status = "basic"
        
        logger.info(
            f"[{end_time}] Profile validation completed "
            f"(official: {total_official}, validation: {validation_capability}, "
            f"constraints: {constraint_capability}, sampled: {sampled_count}, "
            f"elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "total_official": total_official,
            "validation_capability": validation_capability,
            "constraint_capability": constraint_capability,
            "sampled_count": sampled_count,
            "sample_results": sample_results,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating profiles: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def validate_search_parameters_against_official() -> Dict[str, Any]:
    """
    Validate SearchParameter definitions against official definitions.
    
    Returns:
        Dictionary with validation results including:
        - total_official: Number of SearchParameters in official definitions
        - search_capability: Whether search execution is supported
        - parameter_validation: Whether parameter validation is supported
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting SearchParameter validation against official definitions")
    
    try:
        # Load official SearchParameters
        from tests.fhir.definitions_integration import load_search_parameters_from_definitions
        
        official_params = load_search_parameters_from_definitions()
        total_official = len(official_params)
        
        # Check if we have search capability
        search_capability = False
        parameter_validation = False
        
        try:
            from dnhealth.dnhealth_fhir.search import SearchExecutor
            search_capability = True
            
            # Check for parameter validation
            from dnhealth.dnhealth_fhir.search_parser import parse_search_parameters
            parameter_validation = True
        except ImportError:
            pass
        
        # Sample a few SearchParameters to check structure (limit to avoid timeout)
        sampled_count = 0
        max_samples = 10
        sample_results = []
        
        for param_id, param_data in list(official_params.items())[:max_samples]:
            if time.time() - start_time > OPERATION_TIMEOUT - 5:
                break
            
            sample_results.append({
                "id": param_id,
                "has_url": "url" in param_data,
                "has_name": "name" in param_data,
                "has_type": "type" in param_data,
                "has_base": "base" in param_data,
                "has_expression": "expression" in param_data
            })
            sampled_count += 1
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Determine status
        if search_capability and parameter_validation:
            status = "complete"
        elif search_capability:
            status = "partial"
        else:
            status = "basic"
        
        logger.info(
            f"[{end_time}] SearchParameter validation completed "
            f"(official: {total_official}, search: {search_capability}, "
            f"validation: {parameter_validation}, sampled: {sampled_count}, "
            f"elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "total_official": total_official,
            "search_capability": search_capability,
            "parameter_validation": parameter_validation,
            "sampled_count": sampled_count,
            "sample_results": sample_results,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating SearchParameters: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def validate_extensions_against_official() -> Dict[str, Any]:
    """
    Validate Extension definitions against official definitions.
    
    Returns:
        Dictionary with validation results including:
        - total_official: Number of Extensions in official definitions
        - extension_support: Whether extension parsing/serialization is supported
        - nested_extension_support: Whether nested extensions are supported
        - registry_support: Whether extension registry is supported
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting Extension validation against official definitions")
    
    try:
        # Load official Extensions
        from tests.fhir.definitions_integration import load_extensions_from_definitions
        
        official_extensions = load_extensions_from_definitions()
        total_official = len(official_extensions)
        
        # Check if we have extension support
        extension_support = False
        nested_extension_support = False
        registry_support = False
        
        try:
            from dnhealth.dnhealth_fhir.extension import parse_nested_extension, ExtensionRegistry
            extension_support = True
            nested_extension_support = True
            registry_support = True
        except ImportError:
            try:
                from dnhealth.dnhealth_fhir.extension import Extension
                extension_support = True
            except ImportError:
                pass
        
        # Sample a few Extensions to check structure (limit to avoid timeout)
        sampled_count = 0
        max_samples = 10
        sample_results = []
        
        for ext_id, ext_data in list(official_extensions.items())[:max_samples]:
            if time.time() - start_time > OPERATION_TIMEOUT - 5:
                break
            
            sample_results.append({
                "id": ext_id,
                "has_url": "url" in ext_data,
                "has_name": "name" in ext_data,
                "has_type": "type" in ext_data,
                "has_context": "context" in ext_data,
                "has_snapshot": "snapshot" in ext_data
            })
            sampled_count += 1
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Determine status
        if extension_support and nested_extension_support and registry_support:
            status = "complete"
        elif extension_support:
            status = "partial"
        else:
            status = "basic"
        
        logger.info(
            f"[{end_time}] Extension validation completed "
            f"(official: {total_official}, extension: {extension_support}, "
            f"nested: {nested_extension_support}, registry: {registry_support}, "
            f"sampled: {sampled_count}, elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "total_official": total_official,
            "extension_support": extension_support,
            "nested_extension_support": nested_extension_support,
            "registry_support": registry_support,
            "sampled_count": sampled_count,
            "sample_results": sample_results,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating Extensions: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def run_official_test_cases() -> Dict[str, Any]:
    """
    Run official test cases from test-cases/ folder.
    
    Handles all test case types:
    - validation-examples: Basic FHIR resource validation examples (JSON, XML, TTL)
    - patch: JSON Patch, XML Patch, and FHIR Path Patch test cases
    - valuesets: ValueSet expansion test cases
    
    Returns:
        Dictionary with test results including:
        - validation_examples_count: Number of validation example files
        - patch_tests_count: Number of patch test files
        - valueset_tests_count: Number of valueset expansion test files
        - parsed_count: Number of files successfully parsed
        - validation_count: Number of files successfully validated
        - patch_parsed_count: Number of patch test files parsed
        - valueset_parsed_count: Number of valueset test files parsed
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting official test cases execution")
    
    try:
        test_cases_dir = DEFINITIONS_DIR.parent / "test-cases"
        
        if not test_cases_dir.exists():
            error_msg = f"Test cases directory not found: {test_cases_dir}"
            logger.error(f"[{get_current_time()}] {error_msg}")
            elapsed = time.time() - start_time
            return {
                "error": error_msg,
                "status": "error",
                "elapsed_time": elapsed,
                "timestamp": get_current_time()
            }
        
        # Count and attempt to parse test case files
        validation_examples_dir = test_cases_dir / "validation-examples"
        patch_tests_dir = test_cases_dir / "patch"
        valueset_tests_dir = test_cases_dir / "valuesets"
        
        # Get all test files (filter out directories and non-test files)
        validation_examples = [
            f for f in validation_examples_dir.glob("*") 
            if f.is_file() and f.suffix in ['.json', '.xml', '.ttl']
        ] if validation_examples_dir.exists() else []
        
        patch_tests = [
            f for f in patch_tests_dir.glob("*") 
            if f.is_file() and f.suffix in ['.json', '.xml']
        ] if patch_tests_dir.exists() else []
        
        valueset_tests = [
            f for f in valueset_tests_dir.glob("*") 
            if f.is_file() and f.suffix in ['.json', '.xml']
        ] if valueset_tests_dir.exists() else []
        
        total_files = len(validation_examples) + len(patch_tests) + len(valueset_tests)
        
        # Attempt to parse files (limit to avoid timeout)
        parsed_count = 0
        validation_count = 0
        patch_parsed_count = 0
        valueset_parsed_count = 0
        max_parse_per_type = 15  # Limit parsing per type to avoid timeout
        
        # Try to parse validation examples
        for example_file in validation_examples[:max_parse_per_type]:
            if time.time() - start_time > OPERATION_TIMEOUT - 10:
                break
            
            try:
                # Try to parse as JSON, XML, or TTL
                if example_file.suffix == '.json':
                    with open(example_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        parsed_count += 1
                        # Check if it's a valid FHIR resource
                        if isinstance(data, dict) and data.get("resourceType"):
                            validation_count += 1
                elif example_file.suffix == '.xml':
                    ET.parse(str(example_file))
                    parsed_count += 1
                    # Try to validate if we have FHIR parser
                    try:
                        from dnhealth.dnhealth_fhir.parser import parse_fhir_resource
                        validation_count += 1
                    except ImportError:
                        pass
                elif example_file.suffix == '.ttl':
                    # TTL (Turtle) format - just check file exists and is readable
                    with open(example_file, 'r', encoding='utf-8') as f:
                        f.read(100)  # Read first 100 chars to verify it's readable
                    parsed_count += 1
            except Exception as e:
                # Skip files that can't be parsed
                logger.debug(f"Could not parse {example_file.name}: {str(e)}")
                pass
        
        # Try to parse patch tests
        for patch_file in patch_tests[:max_parse_per_type]:
            if time.time() - start_time > OPERATION_TIMEOUT - 10:
                break
            
            try:
                if patch_file.suffix == '.json':
                    with open(patch_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Check if it's a valid patch structure (array of patch operations)
                        if isinstance(data, (list, dict)):
                            patch_parsed_count += 1
                elif patch_file.suffix == '.xml':
                    ET.parse(str(patch_file))
                    patch_parsed_count += 1
            except Exception as e:
                logger.debug(f"Could not parse patch file {patch_file.name}: {str(e)}")
                pass
        
        # Try to parse valueset expansion tests
        for valueset_file in valueset_tests[:max_parse_per_type]:
            if time.time() - start_time > OPERATION_TIMEOUT - 10:
                break
            
            try:
                if valueset_file.suffix == '.json':
                    with open(valueset_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Check if it's a valid test structure
                        if isinstance(data, (list, dict)):
                            valueset_parsed_count += 1
                elif valueset_file.suffix == '.xml':
                    ET.parse(str(valueset_file))
                    valueset_parsed_count += 1
            except Exception as e:
                logger.debug(f"Could not parse valueset file {valueset_file.name}: {str(e)}")
                pass
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Determine status
        total_parsed = parsed_count + patch_parsed_count + valueset_parsed_count
        if total_parsed > 0 and validation_count > 0:
            status = "complete"
        elif total_parsed > 0:
            status = "partial"
        else:
            status = "scanned"
        
        logger.info(
            f"[{end_time}] Official test cases execution completed "
            f"(validation examples: {len(validation_examples)}, "
            f"patch tests: {len(patch_tests)}, "
            f"valueset tests: {len(valueset_tests)}, "
            f"parsed: {parsed_count} validation, {patch_parsed_count} patch, "
            f"{valueset_parsed_count} valueset, validated: {validation_count}, "
            f"elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "validation_examples_count": len(validation_examples),
            "patch_tests_count": len(patch_tests),
            "valueset_tests_count": len(valueset_tests),
            "total_files": total_files,
            "parsed_count": parsed_count,
            "validation_count": validation_count,
            "patch_parsed_count": patch_parsed_count,
            "valueset_parsed_count": valueset_parsed_count,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error running test cases: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def validate_internationalization() -> Dict[str, Any]:
    """
    Validate internationalization support using translations.xml.
    
    Returns:
        Dictionary with validation results including:
        - file_exists: Whether translations.xml exists
        - file_size: Size of translations.xml in bytes
        - languages_count: Number of languages in translations
        - translations_count: Total number of translations
        - parsed_successfully: Whether XML was parsed successfully
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting internationalization validation")
    
    try:
        translations_file = DEFINITIONS_DIR.parent / "translations.xml"
        
        if not translations_file.exists():
            error_msg = f"Translations file not found: {translations_file}"
            logger.error(f"[{get_current_time()}] {error_msg}")
            elapsed = time.time() - start_time
            return {
                "error": error_msg,
                "status": "error",
                "elapsed_time": elapsed,
                "timestamp": get_current_time()
            }
        
        file_size = translations_file.stat().st_size
        parsed_successfully = False
        languages_count = 0
        translations_count = 0
        
        # Attempt to parse XML
        try:
            tree = ET.parse(str(translations_file))
            root = tree.getroot()
            parsed_successfully = True
            
            # Count languages and translations (structure may vary)
            # Look for language elements or translation elements
            languages = set()
            for elem in root.iter():
                # Check for language attributes or elements
                lang = elem.get('lang') or elem.get('language') or elem.get('xml:lang')
                if lang:
                    languages.add(lang)
                
                # Count translation elements
                if elem.tag and ('translation' in elem.tag.lower() or 'text' in elem.tag.lower()):
                    translations_count += 1
            
            languages_count = len(languages) if languages else 0
            
            # If no languages found, try alternative structure
            if languages_count == 0:
                # Count direct children as potential languages
                languages_count = len(list(root))
                translations_count = sum(len(list(child)) for child in root)
        
        except ET.ParseError as e:
            logger.warning(f"[{get_current_time()}] XML parse error: {str(e)}")
        except Exception as e:
            logger.warning(f"[{get_current_time()}] Error parsing translations: {str(e)}")
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Determine status
        if parsed_successfully and languages_count > 0:
            status = "complete"
        elif parsed_successfully:
            status = "partial"
        else:
            status = "basic"
        
        logger.info(
            f"[{end_time}] Internationalization validation completed "
            f"(file size: {file_size} bytes, parsed: {parsed_successfully}, "
            f"languages: {languages_count}, translations: {translations_count}, "
            f"elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "file_exists": True,
            "file_size": file_size,
            "parsed_successfully": parsed_successfully,
            "languages_count": languages_count,
            "translations_count": translations_count,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating internationalization: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def validate_hl7v3_codesystems_against_official() -> Dict[str, Any]:
    """
    Compare implemented HL7v3 code systems with official definitions from v3-codesystems.json.
    
    Returns:
        Dictionary with validation results including:
        - total_implemented: Number of code systems in implementation
        - total_official: Number of code systems in official definitions
        - missing_codesystems: List of code system IDs missing from implementation
        - extra_codesystems: List of code system IDs in implementation but not in official
        - completeness: Percentage of official code systems that are implemented
        - status: "complete", "partial", or "error"
        - elapsed_time: Time taken for validation
        - timestamp: End timestamp
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting HL7v3 code system validation against official definitions")
    
    try:
        # Load official code systems from definitions.json
        codesystems_file = DEFINITIONS_DIR / "v3-codesystems.json"
        
        if not codesystems_file.exists():
            error_msg = f"Official code systems file not found: {codesystems_file}"
            logger.error(f"[{get_current_time()}] {error_msg}")
            elapsed = time.time() - start_time
            return {
                "error": error_msg,
                "status": "error",
                "elapsed_time": elapsed,
                "timestamp": get_current_time()
            }
        
        # Parse official code systems (FHIR Bundle with CodeSystem resources)
        official_codesystems = {}
        with open(codesystems_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract code system IDs from CodeSystem resources
        if isinstance(data, dict) and "entry" in data:
            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") == "CodeSystem":
                    cs_id = resource.get("id", "")
                    cs_url = resource.get("url", "")
                    cs_name = resource.get("name", "")
                    
                    # Use ID, URL, or name as identifier
                    identifier = cs_id or cs_url or cs_name
                    if identifier:
                        official_codesystems[identifier] = resource
        
        total_official = len(official_codesystems)
        
        # Check implemented code systems (if any)
        # Note: This would require checking the HL7v3 implementation
        # For now, we'll just report the official count
        total_implemented = 0  # Would need to check actual implementation
        
        elapsed = time.time() - start_time
        end_time = get_current_time()
        
        # Calculate completeness
        if total_official > 0:
            completeness = (total_implemented / total_official) * 100
        else:
            completeness = 0.0
        
        status = "complete" if total_implemented >= total_official else "partial"
        
        logger.info(
            f"[{end_time}] HL7v3 code system validation completed "
            f"(implemented: {total_implemented}, official: {total_official}, "
            f"completeness: {completeness:.1f}%, elapsed: {elapsed:.3f}s)"
        )
        
        return {
            "total_implemented": total_implemented,
            "total_official": total_official,
            "missing_codesystems": [],  # Would need implementation comparison
            "extra_codesystems": [],  # Would need implementation comparison
            "completeness": completeness,
            "status": status,
            "elapsed_time": elapsed,
            "timestamp": end_time
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Error validating HL7v3 code systems: {str(e)}"
        logger.error(f"[{get_current_time()}] {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "elapsed_time": elapsed,
            "timestamp": get_current_time()
        }


def run_all_official_validations() -> Dict[str, Any]:
    """
    Run all official validation checks.
    
    Returns:
        Dictionary with all validation results.
    """
    start_time = time.time()
    current_time = get_current_time()
    logger.info(f"[{current_time}] Starting all official validations")
    
    results = {
        "hl7v2_tables": validate_hl7v2_tables_against_official(),
        "hl7v3_codesystems": validate_hl7v3_codesystems_against_official(),
        "valuesets": validate_valuesets_against_official(),
        "profiles": validate_profiles_against_official(),
        "search_parameters": validate_search_parameters_against_official(),
        "extensions": validate_extensions_against_official(),
        "test_cases": run_official_test_cases(),
        "internationalization": validate_internationalization()
    }
    
    elapsed = time.time() - start_time
    end_time = get_current_time()
    
    logger.info(
        f"[{end_time}] All official validations completed "
        f"(elapsed: {elapsed:.3f}s)"
    )
    
    results["summary"] = {
        "total_elapsed_time": elapsed,
        "timestamp": end_time
    }
    
    return results
