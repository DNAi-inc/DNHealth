#!/usr/bin/env python3
# Copyright 2025 DNAi inc.
#
# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
CLI entry point for FHIR R5 resource generation.

This script provides a command-line interface to generate Python resource classes
from FHIR R5 StructureDefinition profile JSON files.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
_script_dir = Path(__file__).resolve().parent
# Navigate from: src/dnhealth/dnhealth_fhir/r5_generator/generate.py
# To: src/ (4 levels up: r5_generator -> dnhealth_fhir -> dnhealth -> src)
_src_dir = _script_dir.parent.parent.parent.parent
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

# Debug: print path if needed
# print(f"DEBUG: Added to path: {_src_dir}", file=sys.stderr)

from dnhealth.dnhealth_fhir.r5_generator.resource_generator import (
    generate_r5_resources_cli,
    generate_all_resources,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate FHIR R5 Python resource classes from profile JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all resources from default directories
  python -m dnhealth.dnhealth_fhir.r5_generator.generate

  # Generate first 10 resources
  python -m dnhealth.dnhealth_fhir.r5_generator.generate --max 10

  # Specify custom directories
  python -m dnhealth.dnhealth_fhir.r5_generator.generate \\
      --profiles-dir docs/FHIR_R5 \\
      --output-dir src/dnhealth/dnhealth_fhir/r5/resources

  # Dry run (validate profiles without generating)
  python -m dnhealth.dnhealth_fhir.r5_generator.generate --dry-run
        """,
    )
    
    parser.add_argument(
        "--profiles-dir",
        type=Path,
        default=None,
        help="Directory containing profile JSON files (default: docs/FHIR_R5)",
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write generated Python files (default: src/dnhealth/dnhealth_fhir/r5/resources)",
    )
    
    parser.add_argument(
        "--max",
        type=int,
        default=None,
        metavar="N",
        help="Maximum number of resources to generate (default: all)",
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate profiles without generating code",
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    
    args = parser.parse_args()
    
    # Set default directories if not provided
    if args.profiles_dir is None:
        # Try to find docs/FHIR_R5 relative to this file
        # From: src/dnhealth/dnhealth_fhir/r5_generator/generate.py
        # To: project root (5 levels up)
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent.parent.parent.parent.parent
        args.profiles_dir = project_root / "docs" / "FHIR_R5"
    
    if args.output_dir is None:
        # Default to r5/resources directory
        # From: src/dnhealth/dnhealth_fhir/r5_generator/generate.py
        # To: src/dnhealth/dnhealth_fhir/r5/resources (3 levels up, then into r5/resources)
        script_dir = Path(__file__).resolve().parent
        args.output_dir = script_dir.parent.parent / "r5" / "resources"
    
    # Validate directories
    if not args.profiles_dir.exists():
        print(f"❌ Profiles directory not found: {args.profiles_dir}", file=sys.stderr)
        print(f"   Please specify --profiles-dir or ensure the directory exists", file=sys.stderr)
        return 1
    
    if args.dry_run:
        print("=" * 80)
        print("FHIR R5 Profile Validation (Dry Run)")
        print("=" * 80)
        print(f"Profiles directory: {args.profiles_dir}")
        print()
        
        # Just validate profiles without generating
        from dnhealth.dnhealth_fhir.r5_generator.profile_parser import (
            parse_all_profiles,
            filter_resource_profiles,
        )
        
        try:
            all_profiles = parse_all_profiles(args.profiles_dir)
            resource_profiles = filter_resource_profiles(all_profiles)
            
            print(f"✅ Found {len(resource_profiles)} valid resource profiles")
            
            if args.verbose:
                print("\nResource profiles:")
                for resource_id, struct_def in list(resource_profiles.items())[:20]:
                    print(f"  - {struct_def.type or struct_def.id} ({struct_def.id})")
                if len(resource_profiles) > 20:
                    print(f"  ... and {len(resource_profiles) - 20} more")
            
            return 0
        except Exception as e:
            print(f"❌ Validation failed: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    # Generate resources
    print("=" * 80)
    print("FHIR R5 Resource Generator")
    print("=" * 80)
    print(f"Profiles directory: {args.profiles_dir}")
    print(f"Output directory: {args.output_dir}")
    if args.max:
        print(f"Maximum resources: {args.max}")
    print()
    
    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate resources
    try:
        results = generate_all_resources(
            args.profiles_dir,
            args.output_dir,
            max_resources=args.max,
        )
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        failed = total - successful
        
        print()
        print("=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"Total resources: {total}")
        print(f"✅ Successful: {successful}")
        if failed > 0:
            print(f"❌ Failed: {failed}")
            if args.verbose:
                print("\nFailed resources:")
                for resource_name, success in results.items():
                    if not success:
                        print(f"  - {resource_name}")
        
        if successful == total:
            print("\n✅ All resources generated successfully!")
            return 0
        elif successful > 0:
            print(f"\n⚠️  Generated {successful}/{total} resources successfully")
            return 0  # Partial success is still success
        else:
            print("\n❌ No resources generated successfully")
            return 1
            
    except Exception as e:
        print(f"❌ Generation failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
