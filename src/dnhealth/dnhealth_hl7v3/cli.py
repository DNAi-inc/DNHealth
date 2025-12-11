# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 command-line tool.

Provides commands for pretty-printing, JSON conversion, and validation.
"""

import argparse
import json
import sys
from pathlib import Path

from dnhealth.errors import HL7v3ParseError
from dnhealth.util.io import read_stdin, read_text_file, read_xml_file, write_stdout
from dnhealth.dnhealth_hl7v3.parser import parse_hl7v3
from dnhealth.dnhealth_hl7v3.serializer import serialize_hl7v3
from dnhealth.dnhealth_hl7v3.xpath import find_by_xpath
import xml.etree.ElementTree as ET


def _node_to_dict(node):
    """Convert ElementNode to dictionary for JSON serialization."""
    result = {
        "name": node.name,
    }
    if node.namespace:
        result["namespace"] = node.namespace
    if node.attributes:
        result["attributes"] = node.attributes
    if node.text:
        result["text"] = node.text
    if node.children:
        result["children"] = [_node_to_dict(child) for child in node.children]
    return result


def pretty_print(message, output_file=None):
    """
    Pretty-print an HL7 v3 message.

    Args:
        message: Message object
        output_file: Optional output file path (default: stdout)
    """
    output_lines = []
    output_lines.append(f"HL7 v3 Message (Root: {message.root_name})")
    output_lines.append("=" * 60)

    def _print_node(node, indent=0):
        """Recursively print node structure."""
        prefix = "  " * indent
        ns_str = f" xmlns='{node.namespace}'" if node.namespace else ""
        attrs_str = " ".join(f"{k}='{v}'" for k, v in node.attributes.items())
        attrs_str = f" {attrs_str}" if attrs_str else ""
        output_lines.append(f"{prefix}<{node.name}{ns_str}{attrs_str}>")
        if node.text:
            output_lines.append(f"{prefix}  {node.text}")
        for child in node.children:
            _print_node(child, indent + 1)
        output_lines.append(f"{prefix}</{node.name}>")

    _print_node(message.root)

    output_text = "\n".join(output_lines) + "\n"

    if output_file:
        Path(output_file).write_text(output_text, encoding="utf-8")
    else:
        write_stdout(output_text)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
# Log completion timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_pretty(args):
    """Pretty-print command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_xml_file(args.input)

        message = parse_hl7v3(text)
        pretty_print(message, args.output)
    except HL7v3ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_json(args):
    """JSON conversion command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_xml_file(args.input)

        message = parse_hl7v3(text)
        data = {"root": _node_to_dict(message.root)}
        json_str = json.dumps(data, indent=args.indent, ensure_ascii=False)

        if args.output:
            Path(args.output).write_text(json_str, encoding="utf-8")
        else:
            write_stdout(json_str + "\n")
    except HL7v3ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_validate(args):
    """Validation command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_xml_file(args.input)

        message = parse_hl7v3(text)

        # Basic validation checks
        errors = []
        warnings = []

        # Check for root element
        if not message.root:
            errors.append("Missing root element")
        else:
            # Check for common HL7 v3 elements
            if not message.root.name:
                errors.append("Root element has no name")

        # Report results
        if errors:
            print("Validation FAILED:", file=sys.stderr)
            for error in errors:
                print(f"  ERROR: {error}", file=sys.stderr)
            sys.exit(1)

        if warnings:
            print("Validation passed with warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"  WARNING: {warning}", file=sys.stderr)
        else:
            print("Validation passed", file=sys.stderr)

        print(f"Root element: {message.root_name}")
        if message.root.namespace:
            print(f"Namespace: {message.root.namespace}")

    except HL7v3ParseError as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_extract(args):
    """Extract elements by XPath command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_xml_file(args.input)

        message = parse_hl7v3(text)
        
        # Extract elements by XPath
        results = []
        for xpath in args.xpath:
            nodes = find_by_xpath(message.root, xpath)
            if nodes:
                for node in nodes:
                    # Convert node to dict for JSON output
                    if args.format == "json":
                        node_dict = _node_to_dict(node)
                        results.append({"xpath": xpath, "result": node_dict})
                    else:
                        # XML output - serialize the node
                        from dnhealth.dnhealth_hl7v3.model import Message
                        temp_message = Message(root=node, root_name=node.name)
                        xml_str = serialize_hl7v3(temp_message)
                        results.append({"xpath": xpath, "result": xml_str})
            else:
                # No matches found
                results.append({"xpath": xpath, "result": None, "error": "No elements found"})
        
        # Output results
        if args.format == "json":
            output = json.dumps(results, indent=args.indent, ensure_ascii=False)
        else:
            # XML output - combine all results
            output_lines = []
            for result in results:
                output_lines.append(f"<!-- XPath: {result['xpath']} -->")
                if result.get("result"):
                    output_lines.append(result["result"])
                else:
                    output_lines.append(f"<!-- {result.get('error', 'No result')} -->")
            output = "\n".join(output_lines)
        
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            write_stdout(output + "\n")

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
            
    except HL7v3ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_schema(args):
    """Schema validation command."""
    try:
        # Read XML message
        if args.input == "-" or args.input is None:
            xml_text = read_stdin()
        else:
            xml_text = read_xml_file(args.input)
        
        # Read schema file if provided
        schema_file = args.schema
        if not schema_file:
            # Basic XML well-formedness check if no schema provided
            try:
                ET.fromstring(xml_text)
                print("XML is well-formed", file=sys.stderr)
                print("Note: No schema file provided. Use --schema to validate against XSD.", file=sys.stderr)
                return
            except ET.ParseError as e:
                print(f"XML parsing error: {e}", file=sys.stderr)
                sys.exit(1)
        
        # Try to use lxml for XSD validation if available
        try:
            from lxml import etree
            
            # Parse schema
            try:
                schema_doc = etree.parse(schema_file)
                schema = etree.XMLSchema(schema_doc)
            except Exception as e:
                print(f"Error parsing schema file: {e}", file=sys.stderr)
                sys.exit(1)
            
            # Parse XML
            try:
                xml_doc = etree.fromstring(xml_text.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                print(f"XML syntax error: {e}", file=sys.stderr)
                sys.exit(1)
            
            # Validate against schema
            if schema.validate(xml_doc):
                print("Schema validation passed", file=sys.stderr)
                print(f"Schema: {schema_file}", file=sys.stderr)
            else:
                print("Schema validation FAILED:", file=sys.stderr)
                for error in schema.error_log:
                    print(f"  ERROR: {error.message} (line {error.line})", file=sys.stderr)
                sys.exit(1)
                
        except ImportError:
            # lxml not available - fall back to basic validation
            print("Warning: lxml not available. Performing basic XML well-formedness check only.", file=sys.stderr)
            print("Install lxml for full XSD schema validation: pip install lxml", file=sys.stderr)
            
            try:
                ET.fromstring(xml_text)
                print("XML is well-formed", file=sys.stderr)
                print("Note: Full schema validation requires lxml library.", file=sys.stderr)
            except ET.ParseError as e:
                print(f"XML parsing error: {e}", file=sys.stderr)
                sys.exit(1)
                
    except HL7v3ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_transform(args):
    """XSLT transformation command."""
    try:
        # Read XML message
        if args.input == "-" or args.input is None:
            xml_text = read_stdin()
        else:
            xml_text = read_xml_file(args.input)
        
        # Read XSLT stylesheet
        if not args.stylesheet:
            print("Error: XSLT stylesheet file required. Use --stylesheet option.", file=sys.stderr)
            sys.exit(1)
        
        stylesheet_path = Path(args.stylesheet)
        if not stylesheet_path.exists():
            print(f"Error: Stylesheet file not found: {args.stylesheet}", file=sys.stderr)
            sys.exit(1)
        
        # Try to use lxml for XSLT transformation
        try:
            from lxml import etree
            
            # Parse XML
            try:
                xml_doc = etree.fromstring(xml_text.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                print(f"XML syntax error: {e}", file=sys.stderr)
                sys.exit(1)
            
            # Parse and compile XSLT stylesheet
            try:
                xslt_doc = etree.parse(str(stylesheet_path))
                transform = etree.XSLT(xslt_doc)
            except etree.XSLTParseError as e:
                print(f"XSLT parsing error: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error parsing stylesheet: {e}", file=sys.stderr)
                sys.exit(1)
            
            # Apply transformation
            try:
                result_tree = transform(xml_doc)
                result_xml = str(result_tree)
            except etree.XSLTApplyError as e:
                print(f"XSLT transformation error: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error applying transformation: {e}", file=sys.stderr)
                sys.exit(1)
            
            # Output result
            if args.output:
                Path(args.output).write_text(result_xml, encoding="utf-8")
            else:
                write_stdout(result_xml)
                
        except ImportError:

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
            # lxml not available
            print("Error: lxml library required for XSLT transformation.", file=sys.stderr)
            print("Install lxml: pip install lxml", file=sys.stderr)
            sys.exit(1)
                
    except HL7v3ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="HL7 v3 XML message tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Pretty command
    pretty_parser = subparsers.add_parser("pretty", help="Pretty-print HL7 v3 XML message")
    pretty_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    pretty_parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    # JSON command
    json_parser = subparsers.add_parser("json", help="Convert HL7 v3 XML message to JSON")
    json_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    json_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    json_parser.add_argument("--indent", type=int, default=2, help="JSON indentation (default: 2)")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate HL7 v3 XML message")
    validate_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract elements by XPath")
    extract_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    extract_parser.add_argument("xpath", nargs="+", help="XPath expression(s) to extract (can specify multiple)")
    extract_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    extract_parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format (default: json)")
    extract_parser.add_argument("--indent", type=int, default=2, help="JSON indentation (default: 2)")

    # Schema command
    schema_parser = subparsers.add_parser("schema", help="Validate XML against XSD schema")
    schema_parser.add_argument("input", nargs="?", help="Input XML file (use '-' or omit for stdin)")
    schema_parser.add_argument("-s", "--schema", help="XSD schema file (optional - performs well-formedness check if not provided)")

    # Transform command
    transform_parser = subparsers.add_parser("transform", help="Transform XML using XSLT stylesheet")
    transform_parser.add_argument("input", nargs="?", help="Input XML file (use '-' or omit for stdin)")
    transform_parser.add_argument("-s", "--stylesheet", required=True, help="XSLT stylesheet file (required)")
    transform_parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to command handler
    if args.command == "pretty":
        cmd_pretty(args)
    elif args.command == "json":
        cmd_json(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "schema":
        cmd_schema(args)
    elif args.command == "transform":
        cmd_transform(args)
    else:
        parser.print_help()
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

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
        print(f"[{completion_timestamp}] HL7v3 CLI operation completed in {duration:.3f} seconds", file=sys.stderr)

