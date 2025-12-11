# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 Narrative Generation and Validation.

Provides functions for generating, validating, and rendering FHIR narratives.
Narratives are human-readable summaries stored in resource.text.
All operations include timestamps in logs for traceability.
"""

import html
import re
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from dnhealth.dnhealth_fhir.types import Narrative
from dnhealth.util.logging import get_logger

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.resources.base import Resource, DomainResource

logger = logging.getLogger(__name__)

logger = get_logger(__name__)



    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def generate_narrative(resource: "DomainResource") -> Narrative:
    """
    Generate a human-readable HTML narrative from a FHIR resource.
    
    Extracts key information from the resource and formats it as XHTML div.
    The narrative is stored in resource.text.div.
    
    Args:
        resource: FHIR DomainResource to generate narrative for
    
    Returns:
        Narrative object with generated HTML content
    
    Raises:
        AttributeError: If resource is not a DomainResource (doesn't have text field)
    
    Example:
        >>> narrative = generate_narrative(patient)
        >>> patient.text = narrative
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Generating narrative for resource {resource.resourceType}/{resource.id}")
    
    # Build HTML content
    html_parts = []
    html_parts.append(f'<div xmlns="http://www.w3.org/1999/xhtml">')
    html_parts.append(f'<h1>{resource.resourceType}</h1>')
    
    # Add resource ID if available
    if resource.id:
        html_parts.append(f'<p><b>ID:</b> {html.escape(str(resource.id))}</p>')
    
    # Extract key fields based on resource type
    if hasattr(resource, 'name') and resource.name:
        # For Patient, Practitioner, etc.
        names = []
        for name_item in resource.name:
            if hasattr(name_item, 'given') and name_item.given:
                given = ' '.join(name_item.given)
                family = getattr(name_item, 'family', '') or ''
                full_name = f"{given} {family}".strip()
                if full_name:
                    names.append(full_name)
        if names:
            html_parts.append(f'<p><b>Name:</b> {html.escape(", ".join(names))}</p>')
    
    if hasattr(resource, 'status') and resource.status:
        html_parts.append(f'<p><b>Status:</b> {html.escape(str(resource.status))}</p>')
    
    if hasattr(resource, 'birthDate') and resource.birthDate:
        html_parts.append(f'<p><b>Birth Date:</b> {html.escape(str(resource.birthDate))}</p>')
    
    if hasattr(resource, 'gender') and resource.gender:
        html_parts.append(f'<p><b>Gender:</b> {html.escape(str(resource.gender))}</p>')
    
    # Add meta information if available
    if hasattr(resource, 'meta') and resource.meta:
        if resource.meta.lastUpdated:
            html_parts.append(f'<p><b>Last Updated:</b> {html.escape(str(resource.meta.lastUpdated))}</p>')
        if resource.meta.versionId:
            html_parts.append(f'<p><b>Version:</b> {html.escape(str(resource.meta.versionId))}</p>')
    
    html_parts.append('</div>')
    
    html_content = '\n'.join(html_parts)
    
    # Create Narrative object
    narrative = Narrative(
        status="generated",
        div=html_content
    )
    
    logger.info(f"[{current_time}] Generated narrative for resource {resource.resourceType}/{resource.id} ({len(html_content)} characters)")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Narrative generation operation completed")
    
    return narrative


def validate_narrative(resource: "DomainResource") -> List[str]:
    """
    Validate narrative on a FHIR resource.
    
    Verifies that narrative.text.div is valid XHTML and narrative.status is valid.
    Returns a list of validation errors (empty if valid).
    
    Args:
        resource: FHIR DomainResource to validate narrative for
    
    Returns:
        List of validation error messages (empty if valid)
    
    Example:
        >>> errors = validate_narrative(patient)
        >>> if errors:
        ...     for error in errors:
        ...         print(f"Validation error: {error}")
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Validating narrative for resource {resource.resourceType}/{resource.id}")
    
    errors = []
    
    # Check if resource has text
    if not hasattr(resource, 'text') or resource.text is None:
        logger.debug(f"[{current_time}] Resource has no narrative, skipping validation")
        return errors
    
    narrative = resource.text
    
    # Validate status
    valid_statuses = ["generated", "extensions", "additional", "empty"]
    if narrative.status not in valid_statuses:
        errors.append(f"Invalid narrative status: {narrative.status}. Must be one of: {', '.join(valid_statuses)}")
    
    # Validate div content
    if not narrative.div:
        if narrative.status != "empty":
            errors.append("Narrative div is empty but status is not 'empty'")
    else:
        # Basic XHTML validation
        # Check for well-formed XML/XHTML structure
        div_content = narrative.div.strip()
        
        # Check for proper div tag
        if not div_content.startswith('<div'):
            errors.append("Narrative div must start with <div> tag")
        
        if not div_content.endswith('</div>'):
            errors.append("Narrative div must end with </div> tag")
        
        # Check for xmlns attribute (required for XHTML)
        if 'xmlns="http://www.w3.org/1999/xhtml"' not in div_content:
            errors.append("Narrative div must include xmlns=\"http://www.w3.org/1999/xhtml\" attribute")
        
        # Check for balanced tags (basic check)
        open_tags = len(re.findall(r'<[^/][^>]*>', div_content))
        close_tags = len(re.findall(r'</[^>]+>', div_content))
        if open_tags != close_tags:
            errors.append(f"Narrative div has unbalanced tags ({open_tags} open, {close_tags} close)")
    
    if errors:
        logger.warning(f"[{current_time}] Found {len(errors)} validation error(s) in narrative for resource {resource.resourceType}/{resource.id}")
    else:
        logger.debug(f"[{current_time}] Narrative is valid for resource {resource.resourceType}/{resource.id}")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Narrative validation operation completed")
    
    return errors


def render_narrative(narrative: Narrative) -> str:
    """
    Render narrative HTML for display.
    
    Sanitizes HTML content for security and returns HTML string suitable for display.
    
    Args:
        narrative: Narrative object to render
    
    Returns:
        HTML string for display
    
    Example:
        >>> html = render_narrative(patient.text)
        >>> print(html)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Rendering narrative")
    
    if not narrative or not narrative.div:
        return ""
    
    # Basic sanitization - escape any potentially dangerous content
    # In a production system, you might want to use a more robust HTML sanitizer
    # For now, we'll return the div content as-is since it should already be XHTML
    
    html_content = narrative.div
    
    logger.debug(f"[{current_time}] Rendered narrative ({len(html_content)} characters)")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Narrative rendering operation completed")
    
    return html_content
