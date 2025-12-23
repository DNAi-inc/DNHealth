# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Profile Parser for FHIR R5 StructureDefinition files.

Parses StructureDefinition JSON files to extract resource definitions,
element structures, data types, and constraints.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TypeDefinition:
    """
    FHIR type definition.
    
    Represents a type code and optionally a profile URL.
    """
    
    code: str  # Type code (e.g., "string", "Reference", "CodeableConcept")
    profile: Optional[str] = None  # Profile URL if specified
    targetProfile: Optional[List[str]] = None  # Target profiles for Reference types
    version: Optional[str] = None  # Version of the type


@dataclass
class ElementDefinition:
    """
    FHIR element definition.
    
    Represents a single element in a StructureDefinition.
    """
    
    id: str  # Element ID (e.g., "Task.id", "Task.status")
    path: str  # Element path (e.g., "Task.id", "Task.status")
    short: Optional[str] = None  # Short description
    definition: Optional[str] = None  # Full definition
    comment: Optional[str] = None  # Additional comments
    min: int = 0  # Minimum cardinality
    max: str = "*"  # Maximum cardinality ("*" for unbounded, or integer as string)
    base_min: Optional[int] = None  # Base minimum cardinality
    base_max: Optional[str] = None  # Base maximum cardinality
    types: List[TypeDefinition] = field(default_factory=list)  # Type definitions
    binding: Optional[Dict[str, Any]] = None  # Value set binding
    constraint: List[Dict[str, Any]] = field(default_factory=list)  # Constraints
    mustSupport: bool = False  # Must support flag
    isModifier: bool = False  # Is modifier flag
    isSummary: bool = False  # Is summary flag
    pattern: Optional[Any] = None  # Pattern value
    fixed: Optional[Any] = None  # Fixed value
    defaultValue: Optional[Any] = None  # Default value
    example: Optional[List[Any]] = None  # Example values
    slicing: Optional[Dict[str, Any]] = None  # Slicing information
    base: Optional[Dict[str, Any]] = None  # Base element information


@dataclass
class StructureDefinition:
    """
    FHIR StructureDefinition.
    
    Represents a complete StructureDefinition resource.
    """
    
    resourceType: str  # Should be "StructureDefinition"
    id: str  # Resource ID (e.g., "Task")
    url: str  # Canonical URL
    version: Optional[str] = None  # Version
    name: Optional[str] = None  # Name
    title: Optional[str] = None  # Title
    status: Optional[str] = None  # Status (draft, active, retired, unknown)
    kind: Optional[str] = None  # Kind (primitive-type, complex-type, resource, logical)
    type: Optional[str] = None  # Type (resource type name, e.g., "Task")
    baseDefinition: Optional[str] = None  # Base definition URL
    derivation: Optional[str] = None  # Derivation (specialization, constraint)
    description: Optional[str] = None  # Description
    elements: List[ElementDefinition] = field(default_factory=list)  # Element definitions
    differential_elements: List[ElementDefinition] = field(default_factory=list)  # Differential elements


def parse_profile(profile_path: Path) -> StructureDefinition:
    """
    Parse a StructureDefinition JSON file.
    
    Args:
        profile_path: Path to the profile JSON file
        
    Returns:
        Parsed StructureDefinition object
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is not a valid StructureDefinition
        json.JSONDecodeError: If the file is not valid JSON
    """
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile file not found: {profile_path}")
    
    with open(profile_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate it's a StructureDefinition
    if data.get('resourceType') != 'StructureDefinition':
        raise ValueError(f"File is not a StructureDefinition: {profile_path}")
    
    # Extract basic information
    struct_def = StructureDefinition(
        resourceType=data.get('resourceType', 'StructureDefinition'),
        id=data.get('id', ''),
        url=data.get('url', ''),
        version=data.get('version'),
        name=data.get('name'),
        title=data.get('title'),
        status=data.get('status'),
        kind=data.get('kind'),
        type=data.get('type'),
        baseDefinition=data.get('baseDefinition'),
        derivation=data.get('derivation'),
        description=data.get('description'),
    )
    
    # Parse snapshot elements
    snapshot = data.get('snapshot', {})
    if snapshot:
        elements_data = snapshot.get('element', [])
        struct_def.elements = [_parse_element(elem) for elem in elements_data]
    
    # Parse differential elements (if present)
    differential = data.get('differential', {})
    if differential:
        diff_elements_data = differential.get('element', [])
        struct_def.differential_elements = [_parse_element(elem) for elem in diff_elements_data]
    
    return struct_def


def _parse_element(elem_data: Dict[str, Any]) -> ElementDefinition:
    """
    Parse a single element definition from JSON data.
    
    Args:
        elem_data: Element definition dictionary from JSON
        
    Returns:
        Parsed ElementDefinition object
    """
    # Extract types
    types = []
    type_list = elem_data.get('type', [])
    if isinstance(type_list, list):
        for type_item in type_list:
            if isinstance(type_item, dict):
                type_def = TypeDefinition(
                    code=type_item.get('code', ''),
                    profile=type_item.get('profile'),
                    targetProfile=type_item.get('targetProfile'),
                    version=type_item.get('version'),
                )
                types.append(type_def)
            elif isinstance(type_item, str):
                # Simple string type code
                types.append(TypeDefinition(code=type_item))
    elif isinstance(type_list, str):
        # Single type as string
        types.append(TypeDefinition(code=type_list))
    
    # Extract base information
    base = elem_data.get('base', {})
    base_min = base.get('min') if isinstance(base, dict) else None
    base_max = base.get('max') if isinstance(base, dict) else None
    
    # Extract constraints
    constraints = elem_data.get('constraint', [])
    if not isinstance(constraints, list):
        constraints = []
    
    # Extract binding
    binding = elem_data.get('binding')
    
    # Extract slicing
    slicing = elem_data.get('slicing')
    
    return ElementDefinition(
        id=elem_data.get('id', ''),
        path=elem_data.get('path', ''),
        short=elem_data.get('short'),
        definition=elem_data.get('definition'),
        comment=elem_data.get('comment'),
        min=elem_data.get('min', 0),
        max=str(elem_data.get('max', '*')),
        base_min=base_min,
        base_max=str(base_max) if base_max is not None else None,
        types=types,
        binding=binding,
        constraint=constraints,
        mustSupport=elem_data.get('mustSupport', False),
        isModifier=elem_data.get('isModifier', False),
        isSummary=elem_data.get('isSummary', False),
        pattern=elem_data.get('pattern'),
        fixed=elem_data.get('fixed'),
        defaultValue=elem_data.get('defaultValue'),
        example=elem_data.get('example'),
        slicing=slicing,
        base=base if isinstance(base, dict) else None,
    )


def parse_all_profiles(profiles_dir: Path) -> Dict[str, StructureDefinition]:
    """
    Parse all profile JSON files in a directory.
    
    Args:
        profiles_dir: Directory containing profile JSON files
        
    Returns:
        Dictionary mapping resource IDs to StructureDefinition objects
    """
    profiles = {}
    
    if not profiles_dir.exists():
        return profiles
    
    # Find all .profile.json files
    profile_files = list(profiles_dir.glob("*.profile.json"))
    
    for profile_file in profile_files:
        try:
            struct_def = parse_profile(profile_file)
            profiles[struct_def.id] = struct_def
        except Exception as e:
            # Log error but continue with other files
            print(f"Warning: Failed to parse {profile_file.name}: {e}")
            continue
    
    return profiles


def filter_resource_profiles(profiles: Dict[str, StructureDefinition]) -> Dict[str, StructureDefinition]:
    """
    Filter profiles to only include resource profiles (kind == "resource").
    
    Args:
        profiles: Dictionary of all profiles
        
    Returns:
        Dictionary containing only resource profiles
    """
    return {
        resource_id: profile
        for resource_id, profile in profiles.items()
        if profile.kind == "resource"
    }
