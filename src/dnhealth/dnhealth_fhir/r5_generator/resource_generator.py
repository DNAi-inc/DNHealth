# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Resource Generator for FHIR R5 resources.

Orchestrates the generation of Python resource classes from
StructureDefinition profile JSON files.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from dnhealth.dnhealth_fhir.r5_generator.profile_parser import (
    parse_profile,
    parse_all_profiles,
    filter_resource_profiles,
    StructureDefinition,
)
from dnhealth.dnhealth_fhir.r5_generator.element_analyzer import analyze_elements
from dnhealth.dnhealth_fhir.r5_generator.code_generator import generate_resource_code


def generate_resource_from_profile(
    profile_path: Path,
    output_dir: Path,
    base_class: str = "FHIRResource"
) -> bool:
    """
    Generate a single resource class from a profile JSON file.
    
    Args:
        profile_path: Path to the profile JSON file
        output_dir: Directory to write the generated Python file
        base_class: Base class to inherit from
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Parse the profile
        struct_def = parse_profile(profile_path)
        
        # Only generate resources (not data types or extensions)
        if struct_def.kind != "resource":
            print(f"Skipping {struct_def.id}: not a resource (kind={struct_def.kind})")
            return False
        
        resource_name = struct_def.type or struct_def.id
        
        # Analyze elements
        top_level_metadata, nested_metadata = analyze_elements(struct_def, resource_name)
        
        # Generate code
        code = generate_resource_code(
            struct_def,
            top_level_metadata,
            nested_metadata,
            base_class=base_class
        )
        
        # Write to file
        output_file = output_dir / f"{_resource_name_to_filename(resource_name)}.py"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"✅ Generated: {output_file.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {profile_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_all_resources(
    profiles_dir: Path,
    output_dir: Path,
    base_class: str = "FHIRResource",
    max_resources: Optional[int] = None
) -> Dict[str, bool]:
    """
    Generate all resource classes from profile JSON files.
    
    Args:
        profiles_dir: Directory containing profile JSON files
        output_dir: Directory to write generated Python files
        base_class: Base class to inherit from
        max_resources: Maximum number of resources to generate (None for all)
        
    Returns:
        Dictionary mapping resource names to success status
    """
    results = {}
    
    # Parse all profiles
    print(f"Parsing profiles from {profiles_dir}...")
    all_profiles = parse_all_profiles(profiles_dir)
    
    # Filter to only resource profiles
    resource_profiles = filter_resource_profiles(all_profiles)
    
    print(f"Found {len(resource_profiles)} resource profiles")
    
    if max_resources:
        resource_profiles = dict(list(resource_profiles.items())[:max_resources])
        print(f"Generating first {max_resources} resources...")
    
    # Generate each resource
    for resource_id, struct_def in resource_profiles.items():
        resource_name = struct_def.type or struct_def.id
        
        # Find the profile file
        profile_file = profiles_dir / f"{resource_id.lower()}.profile.json"
        if not profile_file.exists():
            # Try alternative naming
            profile_file = profiles_dir / f"{resource_id}.profile.json"
        
        if profile_file.exists():
            success = generate_resource_from_profile(
                profile_file,
                output_dir,
                base_class=base_class
            )
            results[resource_name] = success
        else:
            print(f"⚠️  Profile file not found for {resource_id}")
            results[resource_name] = False
    
    # Generate summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    print(f"\n✅ Generated {successful}/{total} resources successfully")
    
    return results


def _resource_name_to_filename(resource_name: str) -> str:
    """
    Convert resource name to Python filename.
    
    Args:
        resource_name: Resource name (e.g., "Task", "Patient")
        
    Returns:
        Filename (e.g., "task", "patient")
    """
    # Convert PascalCase to snake_case
    import re
    # Insert underscore before uppercase letters (except the first one)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', resource_name)
    # Insert underscore before uppercase letters that follow lowercase
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def generate_r5_resources_cli(
    profiles_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    max_resources: Optional[int] = None
) -> int:
    """
    CLI entry point for resource generation.
    
    Args:
        profiles_dir: Directory containing profile JSON files (default: docs/FHIR_R5)
        output_dir: Directory to write generated files (default: src/dnhealth/dnhealth_fhir/r5/resources)
        max_resources: Maximum number of resources to generate
        
    Returns:
        Exit code (0 for success)
    """
    if profiles_dir is None:
        profiles_dir = Path(__file__).parent.parent.parent.parent.parent / "docs" / "FHIR_R5"
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "r5" / "resources"
    
    if not profiles_dir.exists():
        print(f"❌ Profiles directory not found: {profiles_dir}")
        return 1
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("FHIR R5 Resource Generator")
    print("=" * 80)
    print(f"Profiles directory: {profiles_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    results = generate_all_resources(
        profiles_dir,
        output_dir,
        max_resources=max_resources
    )
    
    if all(results.values()):
        return 0
    else:
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(generate_r5_resources_cli())
