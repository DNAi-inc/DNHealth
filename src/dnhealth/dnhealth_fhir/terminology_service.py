# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR Terminology Service integration (version-aware, supports R4 and R5).

Provides a unified interface for terminology operations including validation, expansion, and translation.
Version-aware: supports both FHIR R4 and R5 terminology resources.
"""

from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime, timedelta
from functools import lru_cache
from dnhealth.dnhealth_fhir.valueset_resource import ValueSet, get_value_set_by_url
from dnhealth.dnhealth_fhir.codesystem_resource import (
    CodeSystem,
    get_code_system_by_url,
    get_concept_by_code,
    CodeSystemConcept
)
from dnhealth.dnhealth_fhir.conceptmap_resource import (
    ConceptMap,
    translate_code,
    get_concept_map_by_url,
    ConceptMapGroup,
    ConceptMapGroupElement
)
from dnhealth.dnhealth_fhir.code_validation import (
    validate_code_against_valueset,
    validate_coding_against_valueset,
    validate_codeable_concept_against_valueset,
    validate_code_against_codesystem,
    validate_coding_against_codesystem,
    validate_codeable_concept_against_codesystem
)

# Binding strength values in FHIR
BINDING_STRENGTH_REQUIRED = "required"
BINDING_STRENGTH_EXTENSIBLE = "extensible"
BINDING_STRENGTH_PREFERRED = "preferred"
BINDING_STRENGTH_EXAMPLE = "example"

VALID_BINDING_STRENGTHS = {
    BINDING_STRENGTH_REQUIRED,
    BINDING_STRENGTH_EXTENSIBLE,
    BINDING_STRENGTH_PREFERRED,
    BINDING_STRENGTH_EXAMPLE
}
from dnhealth.dnhealth_fhir.code_expansion import expand_valueset, get_expanded_codes
from dnhealth.dnhealth_fhir.types import Coding, CodeableConcept
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)


class TerminologyService:
    """
    Terminology Service for FHIR terminology operations.
    
    Provides a unified interface for:
    - Code validation against ValueSets and CodeSystems
    - ValueSet expansion
    - Code translation using ConceptMaps
    - CodeSystem lookup
    - CodeSystem subsumption checking
    - Reverse translation
    - ConceptMap validation
    """
    
    def __init__(
        self,
        valuesets: Optional[List[ValueSet]] = None,
        codesystems: Optional[List[CodeSystem]] = None,
        conceptmaps: Optional[List[ConceptMap]] = None,
        cache_ttl: Optional[int] = 3600
    ):
        """
        Initialize Terminology Service.
        
        Args:
            valuesets: Optional list of ValueSet resources
            codesystems: Optional list of CodeSystem resources
            conceptmaps: Optional list of ConceptMap resources
            cache_ttl: Cache time-to-live in seconds (default: 3600 = 1 hour)
        """
        self._valuesets: Dict[str, ValueSet] = {}
        self._codesystems: Dict[str, CodeSystem] = {}
        self._conceptmaps: Dict[str, ConceptMap] = {}
        
        # Cache for expanded valuesets and validation results
        self._expansion_cache: Dict[str, Tuple[Any, datetime]] = {}  # URL -> (expansion, timestamp)
        self._validation_cache: Dict[str, Tuple[bool, Optional[str], datetime]] = {}  # key -> (is_valid, error, timestamp)
        self._cache_ttl = cache_ttl if cache_ttl else 3600
        
        # Index resources by URL
        if valuesets:
            for vs in valuesets:
                if vs.url:
                    self._valuesets[vs.url] = vs
        
        if codesystems:
            for cs in codesystems:
                if cs.url:
                    self._codesystems[cs.url] = cs
        
        if conceptmaps:
            for cm in conceptmaps:
                if cm.url:
                    self._conceptmaps[cm.url] = cm
    
    def add_valueset(self, valueset: ValueSet) -> None:
        """Add a ValueSet to the service."""
        if valueset.url:
            self._valuesets[valueset.url] = valueset
            # Clear cache for this valueset
            if valueset.url in self._expansion_cache:
                del self._expansion_cache[valueset.url]
    
    def add_codesystem(self, codesystem: CodeSystem) -> None:
        """Add a CodeSystem to the service."""
        if codesystem.url:
            self._codesystems[codesystem.url] = codesystem
    
    def add_conceptmap(self, conceptmap: ConceptMap) -> None:
        """Add a ConceptMap to the service."""
        if conceptmap.url:
            self._conceptmaps[conceptmap.url] = conceptmap
    
    def clear_cache(self) -> None:
        """Clear all caches."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Clearing terminology service cache")
        self._expansion_cache.clear()
        self._validation_cache.clear()
    
    def _get_cached_expansion(self, url: str) -> Optional[Any]:
        """Get cached expansion if still valid."""
        if url in self._expansion_cache:
            expansion, timestamp = self._expansion_cache[url]
            if datetime.now() - timestamp < timedelta(seconds=self._cache_ttl):
                return expansion
            else:
                # Cache expired, remove it
                del self._expansion_cache[url]
        return None
    
    def _cache_expansion(self, url: str, expansion: Any) -> None:
        """Cache expansion result."""
        self._expansion_cache[url] = (expansion, datetime.now())
    
    def _get_cached_validation(self, cache_key: str) -> Optional[Tuple[bool, Optional[str]]]:
        """Get cached validation result if still valid."""
        if cache_key in self._validation_cache:
            is_valid, error, timestamp = self._validation_cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self._cache_ttl):
                return (is_valid, error)
            else:
                # Cache expired, remove it
                del self._validation_cache[cache_key]
        return None
    
    def _cache_validation(self, cache_key: str, is_valid: bool, error: Optional[str]) -> None:
        """Cache validation result."""
        self._validation_cache[cache_key] = (is_valid, error, datetime.now())
    
    def get_valueset(self, url: str) -> Optional[ValueSet]:
        """Get a ValueSet by URL."""
        return self._valuesets.get(url)
    
    def get_codesystem(self, url: str) -> Optional[CodeSystem]:
        """Get a CodeSystem by URL."""
        return self._codesystems.get(url)
    
    def get_conceptmap(self, url: str) -> Optional[ConceptMap]:
        """Get a ConceptMap by URL."""

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self._conceptmaps.get(url)
    
    def validate_code(
        self,
        code: str,
        valueset_url: Optional[str] = None,
        codesystem_url: Optional[str] = None,
        system: Optional[str] = None,
        expand_valueset: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a code against a ValueSet and/or CodeSystem.
        
        Args:
            code: Code to validate
            valueset_url: Optional ValueSet URL
            codesystem_url: Optional CodeSystem URL
            system: Optional code system URL for filtering
            expand_valueset: Whether to expand ValueSet before validation (default: True)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating code '{code}' against ValueSet '{valueset_url}' and CodeSystem '{codesystem_url}'")
        
        if valueset_url:
            valueset = self.get_valueset(valueset_url)
            if valueset:
                # If ValueSet needs expansion and expand_valueset is True, expand it first
                if expand_valueset and valueset.compose and not valueset.expansion:
                    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Expanding ValueSet '{valueset_url}' for validation")
                    expansion = self.expand_valueset(valueset_url, include_designations=False)
                    if expansion:
                        # Use expanded codes for validation
                        expanded_codes = self.get_expanded_codes(valueset_url)
                        if expanded_codes:
                            if code in expanded_codes:
                                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' is valid in expanded ValueSet '{valueset_url}'")
                                return True, None
                            else:
                                error_msg = f"Code '{code}' is not in expanded ValueSet '{valueset_url}'"
                                logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                                return False, error_msg
                
                is_valid, error = validate_code_against_valueset(code, valueset, system=system)
                if not is_valid:
                    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet validation failed: {error}")
                    return False, error
                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' is valid in ValueSet '{valueset_url}'")
        
        if codesystem_url:
            codesystem = self.get_codesystem(codesystem_url)
            if codesystem:
                is_valid, error = validate_code_against_codesystem(code, codesystem, system=system)
                if not is_valid:
                    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem validation failed: {error}")
                    return False, error
                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' is valid in CodeSystem '{codesystem_url}'")
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' validation successful")
        return True, None
    
    def validate_coding(
        self,
        coding: Coding,
        valueset_url: Optional[str] = None,
        codesystem_url: Optional[str] = None,
        expand_valueset: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a Coding against a ValueSet and/or CodeSystem.
        
        Args:
            coding: Coding to validate
            valueset_url: Optional ValueSet URL
            codesystem_url: Optional CodeSystem URL
            expand_valueset: Whether to expand ValueSet before validation (default: True)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating Coding '{coding.code}' (system: {coding.system}) against ValueSet '{valueset_url}' and CodeSystem '{codesystem_url}'")
        
        if valueset_url:
            valueset = self.get_valueset(valueset_url)
            if valueset:
                # If ValueSet needs expansion and expand_valueset is True, expand it first
                if expand_valueset and valueset.compose and not valueset.expansion:
                    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Expanding ValueSet '{valueset_url}' for validation")
                    expansion = self.expand_valueset(valueset_url, include_designations=False)
                    if expansion:
                        # Use expanded codes for validation
                        expanded_codes = self.get_expanded_codes(valueset_url)
                        if expanded_codes:
                            if coding.code and coding.code in expanded_codes:
                                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coding '{coding.code}' is valid in expanded ValueSet '{valueset_url}'")
                                return True, None
                            else:
                                error_msg = f"Coding '{coding.code}' is not in expanded ValueSet '{valueset_url}'"
                                logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                                return False, error_msg
                
                is_valid, error = validate_coding_against_valueset(coding, valueset)
                if not is_valid:
                    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet validation failed: {error}")
                    return False, error
                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coding '{coding.code}' is valid in ValueSet '{valueset_url}'")
        
        if codesystem_url:
            codesystem = self.get_codesystem(codesystem_url)
            if codesystem:
                is_valid, error = validate_coding_against_codesystem(coding, codesystem)
                if not is_valid:
                    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem validation failed: {error}")
                    return False, error
                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coding '{coding.code}' is valid in CodeSystem '{codesystem_url}'")
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coding '{coding.code}' validation successful")
        return True, None
    
    def validate_codeable_concept(
        self,
        concept: CodeableConcept,
        valueset_url: Optional[str] = None,
        codesystem_url: Optional[str] = None,
        expand_valueset: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a CodeableConcept against a ValueSet and/or CodeSystem.
        
        Args:
            concept: CodeableConcept to validate
            valueset_url: Optional ValueSet URL
            codesystem_url: Optional CodeSystem URL
            expand_valueset: Whether to expand ValueSet before validation (default: True)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        codes_str = ", ".join([c.code or "" for c in (concept.coding or [])])
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating CodeableConcept with codings [{codes_str}] against ValueSet '{valueset_url}' and CodeSystem '{codesystem_url}'")
        
        if valueset_url:
            valueset = self.get_valueset(valueset_url)
            if valueset:
                # If ValueSet needs expansion and expand_valueset is True, expand it first
                if expand_valueset and valueset.compose and not valueset.expansion:
                    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Expanding ValueSet '{valueset_url}' for validation")
                    expansion = self.expand_valueset(valueset_url, include_designations=False)
                
                is_valid, error = validate_codeable_concept_against_valueset(concept, valueset)
                if not is_valid:
                    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet validation failed: {error}")
                    return False, error
                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeableConcept is valid in ValueSet '{valueset_url}'")
        
        if codesystem_url:
            codesystem = self.get_codesystem(codesystem_url)
            if codesystem:
                is_valid, error = validate_codeable_concept_against_codesystem(concept, codesystem)
                if not is_valid:
                    logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem validation failed: {error}")
                    return False, error
                logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeableConcept is valid in CodeSystem '{codesystem_url}'")
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeableConcept validation successful")
        return True, None
    
    def expand_valueset(
        self,
        valueset_url: str,
        include_designations: bool = False,
        use_cache: bool = True
    ) -> Optional[Any]:
        """
        Expand a ValueSet.
        
        Uses caching to improve performance for repeated expansions.
        
        Args:
            valueset_url: ValueSet URL
            include_designations: Whether to include designations in expansion
            use_cache: Whether to use cache (default: True)
            
        Returns:
            ValueSetExpansion object or None if ValueSet not found
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache_key = f"{valueset_url}:{include_designations}"
        
        # Check cache first
        if use_cache:
            cached_expansion = self._get_cached_expansion(cache_key)
            if cached_expansion:
                logger.debug(f"[{current_time}] Using cached expansion for ValueSet '{valueset_url}'")
                return cached_expansion
        
        logger.info(f"[{current_time}] Expanding ValueSet '{valueset_url}'")
        
        valueset = self.get_valueset(valueset_url)
        if not valueset:
            logger.warning(f"[{current_time}] ValueSet '{valueset_url}' not found")
            return None
        
        try:
            codesystems_dict = self._codesystems
            valuesets_dict = {url: vs for url, vs in self._valuesets.items()}
            
            expansion = expand_valueset(
                valueset,
                codesystems=codesystems_dict,
                nested_valuesets=valuesets_dict,
                include_designations=include_designations
            )
            
            # Cache the expansion
            if use_cache and expansion:
                self._cache_expansion(cache_key, expansion)
            
            logger.info(f"[{current_time}] Successfully expanded ValueSet '{valueset_url}' with {expansion.total if expansion else 0} codes")
            return expansion
        except Exception as e:
            error_msg = f"Error expanding ValueSet '{valueset_url}': {str(e)}"
            logger.error(f"[{current_time}] {error_msg}")
            raise
    
    def translate_code(
        self,
        conceptmap_url: str,
        source_code: str,
        source_system: Optional[str] = None,
        target_system: Optional[str] = None
    ) -> Optional[List[Tuple[str, str, str]]]:
        """
        Translate a code using a ConceptMap.
        
        Args:
            conceptmap_url: ConceptMap URL
            source_code: Source code to translate
            source_system: Optional source code system URL
            target_system: Optional target code system URL
            
        Returns:
            List of translations (target_code, target_system, equivalence) or None if ConceptMap not found
        """
        conceptmap = self.get_conceptmap(conceptmap_url)
        if not conceptmap:
            return None
        
        return translate_code(
            conceptmap,
            source_code,
            source_system=source_system,
            target_system=target_system
        )
    
    def get_expanded_codes(self, valueset_url: str) -> Optional[Set[str]]:
        """
        Get expanded codes from a ValueSet.
        
        Args:
            valueset_url: ValueSet URL
            
        Returns:
            Set of code strings or None if ValueSet not found
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Getting expanded codes from ValueSet '{valueset_url}'")
        
        valueset = self.get_valueset(valueset_url)
        if not valueset:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet '{valueset_url}' not found")
            return None
        
        codesystems_dict = self._codesystems
        valuesets_dict = {url: vs for url, vs in self._valuesets.items()}
        
        codes = get_expanded_codes(
            valueset,
            codesystems=codesystems_dict,
            nested_valuesets=valuesets_dict
        )
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Retrieved {len(codes) if codes else 0} expanded codes from ValueSet '{valueset_url}'")
        return codes
    
    def lookup_code(
        self,
        codesystem_url: str,
        code: str,
        version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Look up a code in a CodeSystem.
        
        Returns information about the code including display name, definition,
        designations, and properties.
        
        Args:
            codesystem_url: CodeSystem URL
            code: Code to look up
            version: Optional version of the CodeSystem
            
        Returns:
            Dictionary with code information or None if code not found.
            Dictionary contains: code, display, definition, designations, properties
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Looking up code '{code}' in CodeSystem '{codesystem_url}'")
        
        codesystem = self.get_codesystem(codesystem_url)
        if not codesystem:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem '{codesystem_url}' not found")
            return None
        
        # Check version if specified
        if version and codesystem.version != version:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem version mismatch: expected '{version}', got '{codesystem.version}'")
            return None
        
        # Find the concept
        concept = get_concept_by_code(codesystem, code)
        if not concept:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' not found in CodeSystem '{codesystem_url}'")
            return None
        
        # Build result dictionary
        result = {
            "code": concept.code,
            "display": concept.display,
            "definition": concept.definition,
            "designations": [],
            "properties": []
        }
        
        # Add designations
        for designation in concept.designation:
            result["designations"].append({
                "language": designation.language,
                "use": designation.use,
                "value": designation.value
            })
        
        # Add properties
        for prop in concept.property:
            prop_dict = {"code": prop.code}
            if prop.valueCode:
                prop_dict["valueCode"] = prop.valueCode
            elif prop.valueCoding:
                prop_dict["valueCoding"] = prop.valueCoding
            elif prop.valueString:
                prop_dict["valueString"] = prop.valueString
            elif prop.valueInteger is not None:
                prop_dict["valueInteger"] = prop.valueInteger
            elif prop.valueBoolean is not None:
                prop_dict["valueBoolean"] = prop.valueBoolean
            elif prop.valueDateTime:
                prop_dict["valueDateTime"] = prop.valueDateTime
            elif prop.valueDecimal is not None:
                prop_dict["valueDecimal"] = prop.valueDecimal
            result["properties"].append(prop_dict)
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Successfully looked up code '{code}' in CodeSystem '{codesystem_url}'")
        return result
    
    def subsumes(
        self,
        codesystem_url: str,
        code_a: str,
        code_b: str,
        version: Optional[str] = None
    ) -> Optional[str]:
        """
        Check if one code subsumes another in a CodeSystem.
        
        This checks the hierarchical relationship between two codes.
        Returns:
            - "subsumes" if code_a subsumes code_b (code_b is a child of code_a)
            - "subsumed-by" if code_a is subsumed by code_b (code_a is a child of code_b)
            - "equivalent" if code_a and code_b are equivalent
            - "not-subsumed" if there is no subsumption relationship
            - None if codesystem or codes not found
        
        Args:
            codesystem_url: CodeSystem URL
            code_a: First code
            code_b: Second code
            version: Optional version of the CodeSystem
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking subsumption: '{code_a}' vs '{code_b}' in CodeSystem '{codesystem_url}'")
        
        codesystem = self.get_codesystem(codesystem_url)
        if not codesystem:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem '{codesystem_url}' not found")
            return None
        
        # Check version if specified
        if version and codesystem.version != version:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem version mismatch: expected '{version}', got '{codesystem.version}'")
            return None
        
        # Find both concepts
        concept_a = get_concept_by_code(codesystem, code_a)
        concept_b = get_concept_by_code(codesystem, code_b)
        
        if not concept_a or not concept_b:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - One or both codes not found in CodeSystem")
            return None
        
        # If codes are the same, they're equivalent
        if code_a == code_b:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Codes are equivalent")
            return "equivalent"
        
        # Check hierarchy meaning - only "is-a" supports subsumption
        if codesystem.hierarchyMeaning != "is-a":
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CodeSystem hierarchy meaning is '{codesystem.hierarchyMeaning}', subsumption only supported for 'is-a'")
            return "not-subsumed"
        
        # Check if code_b is a descendant of code_a
        if _is_descendant(concept_a, code_b, codesystem):
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code_a}' subsumes '{code_b}'")
            return "subsumes"
        
        # Check if code_a is a descendant of code_b
        if _is_descendant(concept_b, code_a, codesystem):
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code_a}' is subsumed by '{code_b}'")
            return "subsumed-by"
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No subsumption relationship found")
        return "not-subsumed"
    
    def reverse_translate_code(
        self,
        conceptmap_url: str,
        target_code: str,
        target_system: Optional[str] = None,
        source_system: Optional[str] = None
    ) -> Optional[List[Tuple[str, str, str]]]:
        """
        Reverse translate a code using a ConceptMap.
        
        Finds all source codes that map to the given target code.
        
        Args:
            conceptmap_url: ConceptMap URL
            target_code: Target code to reverse translate
            target_system: Optional target code system URL
            source_system: Optional source code system URL to filter results
            
        Returns:
            List of reverse translations (source_code, source_system, equivalence) or None if ConceptMap not found
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Reverse translating code '{target_code}' using ConceptMap '{conceptmap_url}'")
        
        conceptmap = self.get_conceptmap(conceptmap_url)
        if not conceptmap:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ConceptMap '{conceptmap_url}' not found")
            return None
        
        reverse_translations = []
        
        # Iterate through all groups
        for group in conceptmap.group:
            # Check if target system matches (if specified)
            if target_system and group.target != target_system:
                continue
            
            # Check if source system matches (if specified)
            if source_system and group.source != source_system:
                continue
            
            # Iterate through all elements in the group
            for element in group.element:
                # Check if any target matches the target_code
                for target in element.target:
                    if target.code == target_code:
                        # Found a match - add reverse translation
                        reverse_translations.append((
                            element.code or "",
                            group.source or "",
                            target.equivalence or "related-to"
                        ))
        
        if reverse_translations:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Found {len(reverse_translations)} reverse translation(s) for code '{target_code}'")
        else:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No reverse translations found for code '{target_code}'")
        
        return reverse_translations if reverse_translations else None
    
    def validate_valueset(
        self,
        valueset_url: str
    ) -> Tuple[bool, List[str]]:
        """
        Validate a ValueSet resource structure.
        
        Checks for common issues such as:
        - Missing required fields (url, status)
        - Invalid status values
        - Compose structure (include/exclude)
        - Expansion structure
        - Filter operators
        - Concept codes
        - ValueSet references
        
        Args:
            valueset_url: ValueSet URL
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating ValueSet '{valueset_url}'")
        
        valueset = self.get_valueset(valueset_url)
        if not valueset:
            error_msg = f"ValueSet '{valueset_url}' not found"
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            return False, [error_msg]
        
        errors = []
        
        # Check required fields
        if not valueset.url:
            errors.append("ValueSet missing required field: url")
        
        if not valueset.status:
            errors.append("ValueSet missing required field: status")
        elif valueset.status not in ["draft", "active", "retired", "unknown"]:
            errors.append(f"ValueSet has invalid status: '{valueset.status}'")
        
        # Validate compose structure
        if valueset.compose:
            if not valueset.compose.include:
                errors.append("ValueSet.compose has no includes defined")
            else:
                valid_filter_ops = {
                    "=", "is-a", "descendent-of", "is-not-a",
                    "regex", "in", "not-in", "generalizes", "exists"
                }
                
                for i, include in enumerate(valueset.compose.include):
                    # Check if include has system, valueSet, or concept
                    has_system = bool(include.system)
                    has_valueset = bool(include.valueSet)
                    has_concept = bool(include.concept)
                    
                    if not has_system and not has_valueset:
                        errors.append(f"Compose.include[{i}] missing both system and valueSet")
                    
                    # Validate filters
                    for j, filter_obj in enumerate(include.filter):
                        if not filter_obj.property:
                            errors.append(f"Compose.include[{i}].filter[{j}] missing property")
                        
                        if not filter_obj.op:
                            errors.append(f"Compose.include[{i}].filter[{j}] missing operator")
                        elif filter_obj.op not in valid_filter_ops:
                            errors.append(
                                f"Compose.include[{i}].filter[{j}] has invalid operator: '{filter_obj.op}'"
                            )
                        
                        if filter_obj.op != "exists" and not filter_obj.value:
                            errors.append(
                                f"Compose.include[{i}].filter[{j}] missing value (required for operator '{filter_obj.op}')"
                            )
                    
                    # Validate concepts
                    for j, concept in enumerate(include.concept):
                        if not concept.code:
                            errors.append(f"Compose.include[{i}].concept[{j}] missing code")
        
        # Validate expansion structure
        if valueset.expansion:
            if valueset.expansion.total is not None and valueset.expansion.total < 0:
                errors.append("ValueSet.expansion.total cannot be negative")
            
            if valueset.expansion.offset is not None and valueset.expansion.offset < 0:
                errors.append("ValueSet.expansion.offset cannot be negative")
            
            # Validate contains recursively
            _validate_expansion_contains(valueset.expansion.contains, errors, "expansion.contains")
        
        # Check that ValueSet has either compose or expansion
        if not valueset.compose and not valueset.expansion:
            errors.append("ValueSet must have either compose or expansion")
        
        # Validate referenced ValueSets exist
        if valueset.compose:
            for include in valueset.compose.include:
                for vs_url in include.valueSet:
                    if vs_url not in self._valuesets:
                        errors.append(
                            f"ValueSet references non-existent ValueSet: '{vs_url}'"
                        )
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet '{valueset_url}' validation passed")
        else:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ValueSet '{valueset_url}' validation failed with {len(errors)} error(s)")
        
        return is_valid, errors
    
    def validate_conceptmap(
        self,
        conceptmap_url: str
    ) -> Tuple[bool, List[str]]:
        """
        Validate a ConceptMap resource.
        
        Checks for common issues such as:
        - Missing required fields
        - Invalid group structures
        - Missing source/target systems
        - Invalid equivalence values
        
        Args:
            conceptmap_url: ConceptMap URL
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating ConceptMap '{conceptmap_url}'")
        
        conceptmap = self.get_conceptmap(conceptmap_url)
        if not conceptmap:
            error_msg = f"ConceptMap '{conceptmap_url}' not found"
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            return False, [error_msg]
        
        errors = []
        
        # Check required fields
        if not conceptmap.url:
            errors.append("ConceptMap missing required field: url")
        
        if not conceptmap.status:
            errors.append("ConceptMap missing required field: status")
        elif conceptmap.status not in ["draft", "active", "retired", "unknown"]:
            errors.append(f"ConceptMap has invalid status: '{conceptmap.status}'")
        
        # Validate groups
        if not conceptmap.group:
            errors.append("ConceptMap has no groups defined")
        else:
            valid_equivalences = {
                "related-to", "equivalent", "wider", "narrower",
                "specializes", "generalizes", "inexact", "unmatched", "disjoint"
            }
            
            for i, group in enumerate(conceptmap.group):
                # Check group structure
                if not group.source and not group.target:
                    errors.append(f"Group {i} missing both source and target systems")
                
                if not group.element:
                    errors.append(f"Group {i} has no elements defined")
                else:
                    # Validate elements
                    for j, element in enumerate(group.element):
                        if not element.code:
                            errors.append(f"Group {i}, element {j} missing code")
                        
                        # Validate targets
                        for k, target in enumerate(element.target):
                            if not target.code:
                                errors.append(f"Group {i}, element {j}, target {k} missing code")
                            
                            if target.equivalence and target.equivalence not in valid_equivalences:
                                errors.append(
                                    f"Group {i}, element {j}, target {k} has invalid equivalence: '{target.equivalence}'"
                                )
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ConceptMap '{conceptmap_url}' validation passed")
        else:
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ConceptMap '{conceptmap_url}' validation failed with {len(errors)} error(s)")
        
        return is_valid, errors
    
    def validate_code_with_binding_strength(
        self,
        code: str,
        valueset_url: str,
        binding_strength: str,
        system: Optional[str] = None,
        expand_valueset: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a code against a ValueSet with binding strength consideration.
        
        Binding strength determines how strictly the validation is enforced:
        - required: Code MUST be in ValueSet (strict validation)
        - extensible: Code MUST be in ValueSet, but additional codes allowed (strict validation)
        - preferred: Code SHOULD be in ValueSet (warning if not found)
        - example: Code is an example only (no validation)
        
        Args:
            code: Code to validate
            valueset_url: ValueSet URL
            binding_strength: Binding strength (required, extensible, preferred, example)
            system: Optional code system URL for filtering
            expand_valueset: Whether to expand ValueSet before validation (default: True)
            
        Returns:
            Tuple of (is_valid, error_message)
            For 'required' and 'extensible': returns False if code not in ValueSet
            For 'preferred': returns True but logs warning if code not in ValueSet
            For 'example': always returns True
        """
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating code '{code}' against ValueSet '{valueset_url}' "
            f"with binding strength '{binding_strength}'"
        )
        
        # Validate binding strength
        if binding_strength not in VALID_BINDING_STRENGTHS:
            error_msg = f"Invalid binding strength: '{binding_strength}'. Must be one of: {', '.join(VALID_BINDING_STRENGTHS)}"
            logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            return False, error_msg
        
        # Example binding strength doesn't require validation
        if binding_strength == BINDING_STRENGTH_EXAMPLE:
            logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Binding strength is 'example', skipping validation")
            return True, None
        
        # Validate code against ValueSet
        is_valid, error = self.validate_code(
            code=code,
            valueset_url=valueset_url,
            system=system,
            expand_valueset=expand_valueset
        )
        
        if not is_valid:
            if binding_strength in [BINDING_STRENGTH_REQUIRED, BINDING_STRENGTH_EXTENSIBLE]:
                # Required and extensible are strict - return error
                error_msg = f"Code '{code}' not in ValueSet '{valueset_url}' (binding strength: {binding_strength})"
                logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                return False, error_msg
            elif binding_strength == BINDING_STRENGTH_PREFERRED:
                # Preferred is a warning - code is valid but not recommended
                warning_msg = f"Code '{code}' not in preferred ValueSet '{valueset_url}' (binding strength: preferred)"
                logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {warning_msg}")
                return True, None  # Code is valid but not preferred
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Code '{code}' validation successful with binding strength '{binding_strength}'")
        return True, None
    
    def validate_binding_strength(
        self,
        binding_strength: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that a binding strength value is valid.
        
        Args:
            binding_strength: Binding strength value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Validating binding strength '{binding_strength}'")
        
        if binding_strength not in VALID_BINDING_STRENGTHS:
            error_msg = (
                f"Invalid binding strength: '{binding_strength}'. "
                f"Must be one of: {', '.join(sorted(VALID_BINDING_STRENGTHS))}"
            )
            logger.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            return False, error_msg
        
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Binding strength '{binding_strength}' is valid")
        return True, None


def _is_descendant(parent_concept: CodeSystemConcept, target_code: str, codesystem: CodeSystem) -> bool:
    """
    Check if target_code is a descendant of parent_concept in the CodeSystem hierarchy.
    
    Args:
        parent_concept: Parent concept to search from
        target_code: Code to find as descendant
        codesystem: CodeSystem containing the concepts
        
    Returns:
        True if target_code is a descendant of parent_concept, False otherwise
    """
    # Check nested concepts recursively
    for nested_concept in parent_concept.concept:
        if nested_concept.code == target_code:
            return True
        # Recursively check descendants
        if _is_descendant(nested_concept, target_code, codesystem):

            # Log completion timestamp at end of operation
            return True
    
    return False


def _validate_expansion_contains(
    contains_list: List[Any],
    errors: List[str],
    path: str
) -> None:
    """
    Recursively validate ValueSet expansion contains structure.
    
    Args:
        contains_list: List of ValueSetExpansionContains objects
        errors: List to append errors to
        path: Path prefix for error messages
    """
    if not contains_list:
        return
    
    for i, contains in enumerate(contains_list):
        current_path = f"{path}[{i}]"
        
        # Check that contains has either code or nested contains
        if not hasattr(contains, 'code') or (not contains.code and (not hasattr(contains, 'contains') or not contains.contains)):
            errors.append(f"{current_path} missing both code and nested contains")
        
        # Validate nested contains recursively
        if hasattr(contains, 'contains') and contains.contains:
            _validate_expansion_contains(contains.contains, errors, f"{current_path}.contains")

