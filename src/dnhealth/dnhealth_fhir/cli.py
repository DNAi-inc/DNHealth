# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 command-line tool.

Provides commands for pretty-printing, validation, and format conversion.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Any

from dnhealth.errors import FHIRParseError, FHIRValidationError
from dnhealth.util.io import read_stdin, read_json_file, read_xml_file, write_stdout
from dnhealth.dnhealth_fhir.parser_json import parse_fhir_json
from dnhealth.dnhealth_fhir.parser_xml import parse_fhir_xml
from dnhealth.dnhealth_fhir.serializer_json import serialize_fhir_json
from dnhealth.dnhealth_fhir.serializer_xml import serialize_fhir_xml
from dnhealth.dnhealth_fhir.validation import validate_and_raise
from dnhealth.dnhealth_fhir.search import parse_search_string, SearchParameters
from dnhealth.dnhealth_fhir.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.profile import check_profile_conformance, validate_against_profile
from dnhealth.dnhealth_fhir.structuredefinition import StructureDefinition, parse_structure_definition_json
from dnhealth.dnhealth_fhir.resources.bundle import BundleEntry
from dnhealth.dnhealth_fhir.diff import compare_resources, format_diff
from dnhealth.dnhealth_fhir.merge import merge_resources, merge_resources_into_bundle
from dnhealth.dnhealth_fhir.transform import transform_resource, apply_field_mapping
from datetime import datetime


def cmd_pretty(args):
    """Pretty-print command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            if args.input.endswith(".json"):
                text = read_json_file(args.input)
            else:
                text = read_xml_file(args.input)

        # Try JSON first, then XML
        try:
            resource = parse_fhir_json(text)
        except FHIRParseError:
            resource = parse_fhir_xml(text)

        # Pretty-print as JSON
        json_str = serialize_fhir_json(resource, indent=2)
        if args.output:
            Path(args.output).write_text(json_str, encoding="utf-8")
        else:
            write_stdout(json_str + "\n")

    except (FHIRParseError, FHIRValidationError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
# Log completion timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_validate(args):
    """Validation command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            if args.input.endswith(".json"):
                text = read_json_file(args.input)
            else:
                text = read_xml_file(args.input)

        # Parse
        try:
            resource = parse_fhir_json(text)
        except FHIRParseError:
            resource = parse_fhir_xml(text)

        # Validate
        validate_and_raise(resource)

        print("Validation passed", file=sys.stderr)
        print(f"ResourceType: {resource.resourceType}")
        if resource.id:
            print(f"ID: {resource.id}")

    except FHIRParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except FHIRValidationError as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_to_xml(args):
    """Convert JSON to XML command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_json_file(args.input)

        resource = parse_fhir_json(text)
        xml_str = serialize_fhir_xml(resource)

        if args.output:
            Path(args.output).write_text(xml_str, encoding="utf-8")
        else:
            write_stdout(xml_str)

    except FHIRParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_to_json(args):
    """Convert XML to JSON command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_xml_file(args.input)

        resource = parse_fhir_xml(text)
        json_str = serialize_fhir_json(resource, indent=args.indent)

        if args.output:
            Path(args.output).write_text(json_str, encoding="utf-8")
        else:
            write_stdout(json_str + "\n")

    except FHIRParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def _matches_search(resource: FHIRResource, search_params: SearchParameters) -> bool:
    """
    Check if a resource matches search parameters.
    
    Uses the comprehensive search execution engine.
    
    Args:
        resource: FHIR resource to check
        search_params: Search parameters
    
    Returns:
        True if resource matches, False otherwise
    """
    from dnhealth.dnhealth_fhir.search_execution import resource_matches_search

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return resource_matches_search(resource, search_params)


def cmd_search(args):
    """Search command."""
    try:
        # Parse input
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            if args.input.endswith(".json"):
                text = read_json_file(args.input)
            else:
                text = read_xml_file(args.input)

        # Parse resource
        try:
            resource = parse_fhir_json(text)
        except FHIRParseError:
            resource = parse_fhir_xml(text)

        # Parse search parameters
        query_string = args.query if args.query else ""
        search_params = parse_search_string(query_string)

        # Get resources to search
        resources_to_search: List[FHIRResource] = []
        if isinstance(resource, Bundle):
            # Extract resources from Bundle
            for entry in resource.entry:
                if entry.resource:
                    resources_to_search.append(entry.resource)
        else:
            # Single resource
            resources_to_search = [resource]

        # Execute search using comprehensive search execution engine
        from dnhealth.dnhealth_fhir.search_execution import execute_search
        # Pass resources_to_search as all_resources for _revinclude support
        matching_resources = execute_search(
            resources=resources_to_search,
            search_params=search_params,
            all_resources=resources_to_search  # Pass for _revinclude support
        )

        # Output results
        if args.output:
            # Output as Bundle
            from dnhealth.dnhealth_fhir.resources.bundle import BundleEntry
            bundle = Bundle(
                resourceType="Bundle",
                type="searchset",
                total=len(matching_resources)
            )
            for res in matching_resources:
                entry = BundleEntry(resource=res)
                bundle.entry.append(entry)
            
            if args.format == "json":
                output = serialize_fhir_json(bundle, indent=2)
            else:
                output = serialize_fhir_xml(bundle)
            
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            # Output to stdout
            if args.format == "json":
                for res in matching_resources:
                    json_str = serialize_fhir_json(res, indent=2)
                    write_stdout(json_str + "\n")
            else:
                for res in matching_resources:
                    xml_str = serialize_fhir_xml(res)
                    write_stdout(xml_str + "\n")

        # Print summary to stderr
        print(f"Found {len(matching_resources)} matching resource(s)", file=sys.stderr)

    except FHIRParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_profile(args):
    """Profile validation command."""
    try:
        # Parse resource
        if args.resource == "-" or args.resource is None:
            resource_text = read_stdin()
        else:
            if args.resource.endswith(".json"):
                resource_text = read_json_file(args.resource)
            else:
                resource_text = read_xml_file(args.resource)

        try:
            resource = parse_fhir_json(resource_text)
        except FHIRParseError:
            resource = parse_fhir_xml(resource_text)

        # Parse profile
        if args.profile.endswith(".json"):
            profile_text = read_json_file(args.profile)
            try:
                if isinstance(profile_text, str):
                    profile_data = json.loads(profile_text)
                else:
                    profile_data = profile_text
                profile = parse_structure_definition_json(profile_data)
            except Exception as e:
                print(f"Error parsing profile JSON: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            profile_text = read_xml_file(args.profile)
            try:
                profile = parse_fhir_xml(profile_text)
                if not isinstance(profile, StructureDefinition):
                    print(f"Error: Profile file must be a StructureDefinition resource", file=sys.stderr)
                    sys.exit(1)
            except Exception as e:
                print(f"Error parsing profile XML: {e}", file=sys.stderr)
                sys.exit(1)

        # Validate resource against profile
        errors = check_profile_conformance(resource, profile, strict=args.strict)

        # Output results
        if errors:
            print("Profile validation FAILED:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            
            if args.output:
                # Write errors to file
                error_output = "\n".join(errors)
                Path(args.output).write_text(error_output, encoding="utf-8")
            
            sys.exit(1)
        else:
            print("Profile validation PASSED", file=sys.stderr)
            print(f"ResourceType: {resource.resourceType}", file=sys.stderr)
            if resource.id:
                print(f"ID: {resource.id}", file=sys.stderr)
            print(f"Profile: {profile.url or profile.name or 'Unknown'}", file=sys.stderr)
            
            if args.output:

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
                # Write success message to file
                Path(args.output).write_text("Profile validation PASSED\n", encoding="utf-8")

    except FHIRParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def cmd_diff(args):
    """Diff command."""
    try:
        # Parse first resource
        if args.resource1 == "-" or args.resource1 is None:
            text1 = read_stdin()
        else:
            if args.resource1.endswith(".json"):
                text1 = read_json_file(args.resource1)
            else:
                text1 = read_xml_file(args.resource1)
        
        try:
            resource1 = parse_fhir_json(text1)
        except FHIRParseError:
            resource1 = parse_fhir_xml(text1)
        
        # Parse second resource
        if args.resource2:
            if args.resource2.endswith(".json"):
                text2 = read_json_file(args.resource2)
            else:
                text2 = read_xml_file(args.resource2)
        else:
            # Read from stdin if resource1 was from file
            text2 = read_stdin()
        
        try:
            resource2 = parse_fhir_json(text2)
        except FHIRParseError:
            resource2 = parse_fhir_xml(text2)
        
        # Compare resources
        diff = compare_resources(resource1, resource2)
        
        # Format output
        output_text = format_diff(diff, show_identical=args.show_identical)
        
        if args.output:
            Path(args.output).write_text(output_text, encoding="utf-8")
        else:
            write_stdout(output_text)
        
        # Exit with error code if resources differ
        if not diff.identical:
            sys.exit(1)
    
    except FHIRParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def _extract_value(value: Any) -> Any:
    """
    Extract and serialize a value for output.
    
    Args:
        value: Value to extract
        
    Returns:
        Serializable value (dict, list, or primitive)
    """
    if value is None:
        return None
    
    # If it's a FHIR resource or complex type, convert to dict
    if hasattr(value, "__dict__"):
        result = {}
        for key, val in value.__dict__.items():
            if not key.startswith("_"):
                result[key] = _extract_value(val)
        return result
    
    # If it's a list, process each item
    if isinstance(value, list):
        return [_extract_value(item) for item in value]
    
    # Primitive value

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return value


def cmd_extract(args):
    """Extract command."""
    try:
        # Parse input
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            if args.input.endswith(".json"):
                text = read_json_file(args.input)
            else:
                text = read_xml_file(args.input)

        # Parse resource
        try:
            resource = parse_fhir_json(text)
        except FHIRParseError:
            resource = parse_fhir_xml(text)

        # Parse paths
        paths = []
        if args.path:
            # Support comma-separated paths or multiple --path arguments
            for path_arg in args.path:
                paths.extend([p.strip() for p in path_arg.split(",")])
        else:
            print("Error: At least one path must be specified", file=sys.stderr)
            sys.exit(1)

        # Extract values
        extracted = {}
        for path in paths:
            value = _get_field_value(resource, path)
            if value is not None:
                extracted[path] = _extract_value(value)
            else:
                extracted[path] = None

        # Output results
        if args.format == "json":
            output = json.dumps(extracted, indent=2, ensure_ascii=False)
        else:
            # For XML, create a simple structure
            import xml.etree.ElementTree as ET
            root = ET.Element("extracted")
            for path, value in extracted.items():
                elem = ET.SubElement(root, "element")
                elem.set("path", path)
                if value is not None:
                    elem.text = json.dumps(value)
            output = ET.tostring(root, encoding="unicode")

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            write_stdout(output + "\n")

    except FHIRParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FHIR R4 resource tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Pretty command
    pretty_parser = subparsers.add_parser("pretty", help="Pretty-print FHIR resource")
    pretty_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    pretty_parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate FHIR resource")
    validate_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")

    # To-XML command
    to_xml_parser = subparsers.add_parser("to-xml", help="Convert JSON to XML")
    to_xml_parser.add_argument("input", nargs="?", help="Input JSON file (use '-' or omit for stdin)")
    to_xml_parser.add_argument("-o", "--output", help="Output XML file (default: stdout)")

    # To-JSON command
    to_json_parser = subparsers.add_parser("to-json", help="Convert XML to JSON")
    to_json_parser.add_argument("input", nargs="?", help="Input XML file (use '-' or omit for stdin)")
    to_json_parser.add_argument("-o", "--output", help="Output JSON file (default: stdout)")
    to_json_parser.add_argument("--indent", type=int, default=2, help="JSON indentation (default: 2)")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search resources")
    search_parser.add_argument("input", nargs="?", help="Input file (Bundle or resource, use '-' or omit for stdin)")
    search_parser.add_argument("query", nargs="?", help="Search query string (e.g., 'status=active&name=John')")
    search_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    search_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")

    # Profile command
    profile_parser = subparsers.add_parser("profile", help="Validate resource against profile")
    profile_parser.add_argument("resource", nargs="?", help="Resource file (use '-' or omit for stdin)")
    profile_parser.add_argument("profile", help="Profile file (StructureDefinition)")
    profile_parser.add_argument("-o", "--output", help="Output file for validation results (default: stderr)")
    profile_parser.add_argument("--strict", action="store_true", help="Strict mode (enforce fixed values)")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract specific elements from resource")
    extract_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    extract_parser.add_argument("-p", "--path", action="append", help="Path to extract (e.g., 'status' or 'name.family', can be specified multiple times)")
    extract_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    extract_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")

    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Compare two resources")
    diff_parser.add_argument("resource1", nargs="?", help="First resource file (use '-' or omit for stdin)")
    diff_parser.add_argument("resource2", nargs="?", help="Second resource file (use '-' or omit for stdin)")
    diff_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    diff_parser.add_argument("--show-identical", action="store_true", help="Show message even when resources are identical")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple resources")
    merge_parser.add_argument("resources", nargs="+", help="Resource files to merge")
    merge_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    merge_parser.add_argument("--mode", choices=["resource", "bundle"], default="resource", help="Merge mode: resource=merge fields, bundle=create bundle (default: resource)")
    merge_parser.add_argument("--strategy", choices=["replace", "keep-first"], default="replace", help="Merge strategy for fields (default: replace)")
    merge_parser.add_argument("--merge-lists", choices=["append", "replace", "unique"], default="append", help="Strategy for merging list fields (default: append)")
    merge_parser.add_argument("--bundle-type", default="collection", help="Bundle type when using bundle mode (default: collection)")
    merge_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")

    # Transform command
    transform_parser = subparsers.add_parser("transform", help="Transform resource using field mappings")
    transform_parser.add_argument("input", nargs="?", help="Input resource file (use '-' or omit for stdin)")
    transform_parser.add_argument("-m", "--mapping", help="Mapping file (JSON with source->target field mappings)")
    transform_parser.add_argument("-f", "--field", action="append", help="Field mapping (format: 'source:target' or 'source=target', can be specified multiple times)")
    transform_parser.add_argument("-t", "--target-type", help="Target resource type (if different from source)")
    transform_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    transform_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")

    # Bundle command
    bundle_parser = subparsers.add_parser("bundle", help="Create and manipulate bundles")
    bundle_subparsers = bundle_parser.add_subparsers(dest="action", help="Bundle action")
    
    # Create subcommand
    create_parser = bundle_subparsers.add_parser("create", help="Create a new bundle from resources")
    create_parser.add_argument("resources", nargs="+", help="Resource files to include in bundle")
    create_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    create_parser.add_argument("--type", dest="bundle_type", default="collection", help="Bundle type (default: collection)")
    create_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")
    
    # Add subcommand
    add_parser = bundle_subparsers.add_parser("add", help="Add resources to existing bundle")
    add_parser.add_argument("bundle", help="Bundle file")
    add_parser.add_argument("resources", nargs="+", help="Resource files to add")
    add_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    add_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")
    
    # List subcommand
    list_parser = bundle_subparsers.add_parser("list", help="List bundle contents")
    list_parser.add_argument("bundle", help="Bundle file")
    
    # Extract subcommand
    extract_bundle_parser = bundle_subparsers.add_parser("extract", help="Extract resources from bundle")
    extract_bundle_parser.add_argument("bundle", help="Bundle file")
    extract_bundle_parser.add_argument("-o", "--output", help="Output file (default: stdout, creates numbered files for multiple resources)")
    extract_bundle_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to command handler
    if args.command == "pretty":
        cmd_pretty(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "to-xml":
        cmd_to_xml(args)

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
    elif args.command == "to-json":
        cmd_to_json(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "profile":
        cmd_profile(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "bundle":
        cmd_bundle(args)
    elif args.command == "diff":
        cmd_diff(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == "transform":
        cmd_transform(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    from datetime import datetime
import logging

logger = logging.getLogger(__name__)
    start_time = datetime.now()
    try:
        main()
    finally:
        # Always log completion timestamp at end of operations
        end_time = datetime.now()
        completion_timestamp = end_time.strftime("%Y-%m-%d %H:%M:%S")
        duration = (end_time - start_time).total_seconds()
        print(f"[{completion_timestamp}] FHIR CLI operation completed in {duration:.3f} seconds", file=sys.stderr)

