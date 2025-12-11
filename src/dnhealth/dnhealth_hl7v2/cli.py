# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x command-line tool.

Provides commands for pretty-printing, JSON conversion, validation, and round-trip testing.
"""

import argparse
import sys
from pathlib import Path

from dnhealth.errors import HL7v2ParseError
from dnhealth.util.io import read_stdin, read_text_file, write_json_file, write_stdout
from dnhealth.dnhealth_hl7v2.jsoncodec import message_to_json
from dnhealth.dnhealth_hl7v2.parser import parse_hl7v2
from dnhealth.dnhealth_hl7v2.serializer import serialize_hl7v2
from dnhealth.dnhealth_hl7v2.ack import generate_ack
from dnhealth.dnhealth_hl7v2.diff import compare_messages, format_diff
from dnhealth.dnhealth_hl7v2.merge import merge_messages, merge_messages_by_segment_type
from dnhealth.dnhealth_hl7v2.convert import convert_message_simple, convert_message_version


def pretty_print(message, output_file=None):
    """
    Pretty-print an HL7 v2 message.

    Args:
        message: Message object
        output_file: Optional output file path (default: stdout)
    """
    output_lines = []
    output_lines.append(f"HL7 v2 Message (Version: {message.version or 'Unknown'})")
    output_lines.append("=" * 60)

    for segment in message.segments:
        output_lines.append(f"\nSegment: {segment.name}")
        for i, field in enumerate(segment.fields, start=1):
            field_value = field.value()
            if field_value:
                output_lines.append(f"  Field {i}: {field_value}")
            else:
                # Show components if field has multiple components
                if len(field.components) > 1:
                    comp_values = []
                    for comp in field.components:
                        comp_val = comp.value()
                        if comp_val:
                            comp_values.append(comp_val)
                    if comp_values:
                        output_lines.append(f"  Field {i}: {' ^ '.join(comp_values)}")

    output_text = "\n".join(output_lines) + "\n"

    if output_file:
        Path(output_file).write_text(output_text, encoding="utf-8")
    else:
        write_stdout(output_text)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_pretty(args):
    """Pretty-print command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)
        pretty_print(message, args.output)
    except HL7v2ParseError as e:
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
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)
        pretty = not args.compact if hasattr(args, 'compact') else True
        json_str = message_to_json(message, indent=args.indent, pretty=pretty)

        if args.output:
            Path(args.output).write_text(json_str, encoding="utf-8")
        else:
            write_stdout(json_str + "\n")
    except HL7v2ParseError as e:
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
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)

        # Basic validation checks
        errors = []
        warnings = []

        # Check for MSH segment
        msh_segments = message.get_segments("MSH")
        if not msh_segments:
            errors.append("Missing MSH segment")
        elif len(msh_segments) > 1:
            warnings.append(f"Multiple MSH segments found ({len(msh_segments)})")

        # Check MSH-12 (version)
        if msh_segments:
            msh = msh_segments[0]
            if len(msh.fields) < 12:
                warnings.append("MSH-12 (version) not found")
            elif not message.version:
                warnings.append("MSH-12 (version) is empty")

        # Check encoding characters
        if message.encoding_chars.field_separator != "|":
            warnings.append(f"Non-standard field separator: '{message.encoding_chars.field_separator}'")

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

        print(f"Segments: {len(message.segments)}")
        if message.version:
            print(f"Version: {message.version}")

    except HL7v2ParseError as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_roundtrip(args):
    """Round-trip test command."""
    try:
        if args.input == "-" or args.input is None:
            original_text = read_stdin()
        else:
            original_text = read_text_file(args.input)

        # Parse
        message = parse_hl7v2(original_text, tolerant=args.tolerant)

        # Serialize
        roundtripped_text = serialize_hl7v2(message)

        # Compare (normalize whitespace)
        original_normalized = original_text.replace("\r\n", "\r").replace("\n", "\r").rstrip()
        roundtripped_normalized = roundtripped_text.rstrip()

        if original_normalized == roundtripped_normalized:
            print("Round-trip test PASSED: Structure preserved", file=sys.stderr)
            if args.output:
                Path(args.output).write_text(roundtripped_text, encoding="utf-8")
            else:
                write_stdout(roundtripped_text)
        else:
            print("Round-trip test FAILED: Structure changed", file=sys.stderr)
            print("\nOriginal:", file=sys.stderr)
            print(original_normalized[:200] + ("..." if len(original_normalized) > 200 else ""), file=sys.stderr)
            print("\nRound-tripped:", file=sys.stderr)
            print(roundtripped_normalized[:200] + ("..." if len(roundtripped_normalized) > 200 else ""), file=sys.stderr)
            sys.exit(1)

    # Log completion timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_extract(args):
    """Extract specific segments or fields command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)
        
        # Extract segments
        extracted_segments = []
        if args.segments:
            segment_names = [s.strip().upper() for s in args.segments.split(",")]
            for seg_name in segment_names:
                segments = message.get_segments(seg_name)
                extracted_segments.extend(segments)
        else:
            # Extract all segments
            extracted_segments = message.segments
        
        # Filter by field if specified
        if args.fields:
            # Parse field specification (e.g., "PID.3,PID.5" or "3,5" for all segments)
            field_specs = [f.strip() for f in args.fields.split(",")]
            filtered_segments = []
            
            for segment in extracted_segments:
                # Create new segment with only specified fields
                field_indices = []
                for spec in field_specs:
                    if "." in spec:
                        # Format: SEGMENT.FIELD
                        seg_name, field_num = spec.split(".", 1)
                        if segment.name == seg_name.upper():
                            try:
                                field_indices.append(int(field_num))
                            except ValueError:
                                pass
                    else:
                        # Format: FIELD (apply to all segments)
                        try:
                            field_indices.append(int(spec))
                        except ValueError:
                            pass
                
                if field_indices:
                    # Extract specified fields
                    new_field_repetitions = []
                    for idx in field_indices:
                        if 1 <= idx <= len(segment._field_repetitions):
                            new_field_repetitions.append(segment._field_repetitions[idx - 1])
                    
                    from dnhealth.dnhealth_hl7v2.model import Segment
                    filtered_segments.append(Segment(segment.name, field_repetitions=new_field_repetitions))
                else:
                    filtered_segments.append(segment)
            
            extracted_segments = filtered_segments
        
        # Create new message with extracted segments
        from dnhealth.dnhealth_hl7v2.model import Message
        extracted_message = Message(
            segments=extracted_segments,
            encoding_chars=message.encoding_chars,
            version=message.version,
        )
        
        # Output
        output_text = serialize_hl7v2(extracted_message, normalize=args.normalize)
        
        if args.output:
            Path(args.output).write_text(output_text, encoding="utf-8")
        else:
            write_stdout(output_text)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_stats(args):
    """Display message statistics command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)
        
        # Collect statistics
        stats = {
            "version": message.version or "Unknown",
            "total_segments": len(message.segments),
            "segment_counts": {},
            "total_fields": 0,
            "total_repetitions": 0,
            "encoding_chars": {
                "field_separator": message.encoding_chars.field_separator,
                "component_separator": message.encoding_chars.component_separator,
                "repetition_separator": message.encoding_chars.repetition_separator,
                "escape_character": message.encoding_chars.escape_character,
                "subcomponent_separator": message.encoding_chars.subcomponent_separator,
            },
        }
        
        if message.encoding_chars.continuation_character:
            stats["encoding_chars"]["continuation_character"] = message.encoding_chars.continuation_character
        
        # Count segments by type
        for segment in message.segments:
            seg_name = segment.name
            stats["segment_counts"][seg_name] = stats["segment_counts"].get(seg_name, 0) + 1
            
            # Count fields and repetitions
            for field_repetitions in segment._field_repetitions:
                stats["total_fields"] += 1
                stats["total_repetitions"] += len(field_repetitions)
        
        # Format output
        output_lines = []
        output_lines.append("HL7 v2 Message Statistics")
        output_lines.append("=" * 60)
        output_lines.append(f"Version: {stats['version']}")
        output_lines.append(f"Total Segments: {stats['total_segments']}")
        output_lines.append(f"Total Fields: {stats['total_fields']}")
        output_lines.append(f"Total Field Repetitions: {stats['total_repetitions']}")
        output_lines.append("")
        output_lines.append("Segment Counts:")
        for seg_name, count in sorted(stats["segment_counts"].items()):
            output_lines.append(f"  {seg_name}: {count}")
        output_lines.append("")
        output_lines.append("Encoding Characters:")
        for char_name, char_value in stats["encoding_chars"].items():
            # Escape special characters for display
            display_value = repr(char_value) if char_value else "None"
            output_lines.append(f"  {char_name}: {display_value}")
        
        output_text = "\n".join(output_lines) + "\n"
        

            # Log completion timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        if args.output:
            Path(args.output).write_text(output_text, encoding="utf-8")
        else:
            write_stdout(output_text)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_ack(args):
    """Generate acknowledgment message command."""
    try:
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_text_file(args.input)

        original_message = parse_hl7v2(text, tolerant=args.tolerant)
        
        # Generate ACK message
        ack_message = generate_ack(
            original_message,
            acknowledgment_code=args.code,
            text_message=args.message,
            application_name=args.application,
            facility_name=args.facility,
        )
        
        # Serialize ACK message
        ack_text = serialize_hl7v2(ack_message, normalize=args.normalize)
        
        if args.output:
            Path(args.output).write_text(ack_text, encoding="utf-8")
        else:
            write_stdout(ack_text)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_diff(args):
    """Compare two messages command."""
    try:
        # Read first message
        if args.message1 == "-" or args.message1 is None:
            text1 = read_stdin()
        else:
            text1 = read_text_file(args.message1)

        message1 = parse_hl7v2(text1, tolerant=args.tolerant)

        # Read second message
        if args.message2:
            text2 = read_text_file(args.message2)
        else:
            # Read from stdin if message1 was from file
            text2 = read_stdin()

        message2 = parse_hl7v2(text2, tolerant=args.tolerant)

        # Compare messages
        diff = compare_messages(message1, message2)

        # Format output
        output_text = format_diff(diff, show_identical=args.show_identical)


        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        if args.output:
            Path(args.output).write_text(output_text, encoding="utf-8")
        else:
            write_stdout(output_text)
        
        # Exit with error code if messages differ
        if not diff.identical:
            sys.exit(1)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_merge(args):
    """Merge multiple messages command."""
    try:
        messages = []
        
        # Read messages from files
        if args.files:
            for file_path in args.files:
                text = read_text_file(file_path)
                msg = parse_hl7v2(text, tolerant=args.tolerant)
                messages.append(msg)
        
        # Read from stdin if no files specified
        if not args.files:
            text = read_stdin()
            msg = parse_hl7v2(text, tolerant=args.tolerant)
            messages.append(msg)
        
        if not messages:
            print("Error: No messages to merge", file=sys.stderr)
            sys.exit(1)
        
        # Determine merge strategy
        merge_strategy = args.strategy if args.strategy else "append"
        
        # Filter by segment types if specified
        segment_types = None
        if args.segments:
            segment_types = [s.strip().upper() for s in args.segments.split(",")]
        
        # Merge messages
        if segment_types:
            merged_message = merge_messages_by_segment_type(messages, segment_types)
        else:
            merged_message = merge_messages(
                messages,
                merge_strategy=merge_strategy,
                preserve_msh=args.preserve_msh,
            )
        
        # Serialize merged message
        merged_text = serialize_hl7v2(merged_message, normalize=args.normalize)
        
        if args.output:
            Path(args.output).write_text(merged_text, encoding="utf-8")
        else:
            write_stdout(merged_text)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def cmd_query(args):
    """Query/search command for finding values in HL7 v2 messages."""
    try:
        # Read input message
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)
        
        results = []
        search_term = args.search.lower() if args.search else None
        segment_filter = args.segment.upper() if args.segment else None
        field_filter = int(args.field) if args.field else None
        
        # Search through all segments
        for segment in message.segments:
            # Filter by segment name if specified
            if segment_filter and segment.name != segment_filter:
                continue
            
            # Search through fields
            for field_idx, field in enumerate(segment.fields, start=1):
                # Filter by field index if specified
                if field_filter and field_idx != field_filter:
                    continue
                
                field_value = field.value()
                if field_value:
                    # Search in field value
                    if search_term is None or search_term in field_value.lower():
                        results.append({
                            "segment": segment.name,
                            "field": field_idx,
                            "value": field_value,
                        })
                    
                    # Also search in components
                    if len(field.components) > 1:
                        for comp_idx, comp in enumerate(field.components, start=1):
                            comp_value = comp.value()
                            if comp_value:
                                if search_term is None or search_term in comp_value.lower():
                                    results.append({
                                        "segment": segment.name,
                                        "field": field_idx,
                                        "component": comp_idx,
                                        "value": comp_value,
                                    })
        
        # Output results
        if args.json:
            import json
            output = json.dumps(results, indent=2)
        else:
            output_lines = []
            if not results:
                output_lines.append("No matches found.")
            else:

        # Log completion timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
                output_lines.append(f"Found {len(results)} match(es):\n")
                for result in results:
                    seg_field = f"{result['segment']}-{result['field']}"
                    if 'component' in result:
                        seg_field += f".{result['component']}"
                    output_lines.append(f"{seg_field}: {result['value']}")
            output = "\n".join(output_lines) + "\n"
        
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            write_stdout(output)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_convert(args):
    """Convert message version command."""
    try:
        # Read input message
        if args.input == "-" or args.input is None:
            text = read_stdin()
        else:
            text = read_text_file(args.input)

        message = parse_hl7v2(text, tolerant=args.tolerant)
        
        # Validate target version
        valid_versions = ["2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"]
        if args.version not in valid_versions:
            print(f"Error: Invalid target version '{args.version}'. Valid versions: {', '.join(valid_versions)}", file=sys.stderr)
            sys.exit(1)
        
        # Convert message
        if args.full:
            converted_message = convert_message_version(
                message,
                target_version=args.version,
                preserve_unknown_segments=args.preserve_unknown,
            )
        else:
            converted_message = convert_message_simple(message, target_version=args.version)
        
        # Serialize converted message
        converted_text = serialize_hl7v2(converted_message, normalize=args.normalize)
        
        if args.output:
            Path(args.output).write_text(converted_text, encoding="utf-8")
        else:
            write_stdout(converted_text)
            
    except HL7v2ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
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
        description="HL7 v2.x message tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tolerant",
        action="store_true",
        help="Use tolerant parsing mode (attempt to parse malformed messages)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Pretty command
    pretty_parser = subparsers.add_parser("pretty", help="Pretty-print HL7 v2 message")
    pretty_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    pretty_parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    # JSON command
    json_parser = subparsers.add_parser("json", help="Convert HL7 v2 message to JSON")
    json_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    json_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    json_parser.add_argument("--indent", type=int, default=2, help="JSON indentation (default: 2)")
    json_parser.add_argument("--compact", action="store_true", help="Output compact JSON (no pretty-print)")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate HL7 v2 message")
    validate_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")

    # Round-trip command
    roundtrip_parser = subparsers.add_parser("roundtrip", help="Round-trip test (parse → serialize)")
    roundtrip_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    roundtrip_parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract specific segments or fields")
    extract_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    extract_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    extract_parser.add_argument("-s", "--segments", help="Comma-separated list of segment names to extract (e.g., 'MSH,PID,PV1')")
    extract_parser.add_argument("-f", "--fields", help="Comma-separated list of fields to extract (e.g., 'PID.3,PID.5' or '3,5' for all segments)")
    extract_parser.add_argument("--normalize", action="store_true", default=True, help="Normalize output format (default: True)")
    extract_parser.add_argument("--no-normalize", dest="normalize", action="store_false", help="Do not normalize output format")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Display message statistics")
    stats_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    stats_parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    # ACK command
    ack_parser = subparsers.add_parser("ack", help="Generate acknowledgment (ACK) message")
    ack_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    ack_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    ack_parser.add_argument(
        "-c", "--code",
        choices=["AA", "AE", "AR"],
        default="AA",
        help="Acknowledgment code: AA=Accept, AE=Error, AR=Reject (default: AA)"
    )
    ack_parser.add_argument("-m", "--message", help="Text message for MSA-3 (optional)")
    ack_parser.add_argument("-a", "--application", help="Application name for MSH-3 (optional)")
    ack_parser.add_argument("-f", "--facility", help="Facility name for MSH-4 (optional)")
    ack_parser.add_argument("--normalize", action="store_true", default=True, help="Normalize output format (default: True)")
    ack_parser.add_argument("--no-normalize", dest="normalize", action="store_false", help="Do not normalize output format")

    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Compare two HL7 v2 messages")
    diff_parser.add_argument("message1", nargs="?", help="First message file (use '-' for stdin)")
    diff_parser.add_argument("message2", nargs="?", help="Second message file (use '-' for stdin if message1 is file)")
    diff_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    diff_parser.add_argument("--show-identical", action="store_true", help="Show output even when messages are identical")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple HL7 v2 messages")
    merge_parser.add_argument("files", nargs="*", help="Message files to merge (use '-' for stdin if no files)")
    merge_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    merge_parser.add_argument(
        "-s", "--strategy",
        choices=["append", "unique", "replace"],
        default="append",
        help="Merge strategy: append=all segments, unique=no duplicates, replace=keep last (default: append)"
    )
    merge_parser.add_argument("--segments", help="Comma-separated list of segment types to keep (e.g., PID,PV1)")
    merge_parser.add_argument("--preserve-msh", action="store_true", default=True, help="Preserve MSH from first message (default: True)")
    merge_parser.add_argument("--no-preserve-msh", dest="preserve_msh", action="store_false", help="Do not preserve MSH from first message")
    merge_parser.add_argument("--normalize", action="store_true", default=True, help="Normalize output format (default: True)")
    merge_parser.add_argument("--no-normalize", dest="normalize", action="store_false", help="Do not normalize output format")

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert message to different HL7 v2 version")
    convert_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    convert_parser.add_argument("-v", "--version", required=True, help="Target version (e.g., 2.5, 2.6)")
    convert_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    convert_parser.add_argument("--full", action="store_true", help="Perform full conversion using profiles (default: simple conversion)")
    convert_parser.add_argument("--preserve-unknown", action="store_true", default=True, help="Preserve segments not in target version (default: True)")
    convert_parser.add_argument("--no-preserve-unknown", dest="preserve_unknown", action="store_false", help="Remove segments not in target version")
    convert_parser.add_argument("--normalize", action="store_true", default=True, help="Normalize output format (default: True)")
    convert_parser.add_argument("--no-normalize", dest="normalize", action="store_false", help="Do not normalize output format")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query/search for values in HL7 v2 message")
    query_parser.add_argument("input", nargs="?", help="Input file (use '-' or omit for stdin)")
    query_parser.add_argument("-s", "--search", help="Search term (case-insensitive substring match)")
    query_parser.add_argument("--segment", help="Filter by segment name (e.g., 'PID')")
    query_parser.add_argument("--field", help="Filter by field index (e.g., '3')")
    query_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    query_parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to command handler
    if args.command == "pretty":
        cmd_pretty(args)

                # Log completion timestamp
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
    elif args.command == "json":
        cmd_json(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "roundtrip":
        cmd_roundtrip(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "ack":
        cmd_ack(args)
    elif args.command == "diff":
        cmd_diff(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "query":
        cmd_query(args)
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
        print(f"[{completion_timestamp}] HL7v2 CLI operation completed in {duration:.3f} seconds", file=sys.stderr)

