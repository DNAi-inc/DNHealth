# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 Compartment definitions and compartment-based search.

Compartments are logical groupings of resources that share a common context.
"""

import logging
from datetime import datetime
from typing import Dict, Set, List, Optional
from dnhealth.dnhealth_fhir.resources.base import FHIRResource

logger = logging.getLogger(__name__)


# FHIR R4 standard compartments
COMPARTMENTS: Dict[str, Set[str]] = {
    "Patient": {
        "Patient", "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
        "DeviceUseStatement", "DiagnosticReport", "DocumentManifest", "DocumentReference",
        "Encounter", "EpisodeOfCare", "FamilyMemberHistory", "Flag", "Goal",
        "ImagingStudy", "Immunization", "MedicationRequest", "MedicationStatement",
        "Observation", "Procedure", "Provenance", "QuestionnaireResponse", "RiskAssessment"
    },
    "Encounter": {
        "Encounter", "Account", "AllergyIntolerance", "CarePlan", "Condition",
        "DeviceUseStatement", "DiagnosticReport", "DocumentReference", "Flag",
        "Goal", "ImagingStudy", "Immunization", "MedicationRequest", "MedicationStatement",
        "Observation", "Procedure", "Provenance", "QuestionnaireResponse", "RiskAssessment"
    },
    "RelatedPerson": {
        "RelatedPerson", "Account", "AllergyIntolerance", "CarePlan", "CareTeam",
        "Condition", "DeviceUseStatement", "DiagnosticReport", "DocumentReference",
        "Encounter", "FamilyMemberHistory", "Flag", "Goal", "ImagingStudy",
        "Immunization", "MedicationRequest", "MedicationStatement", "Observation",
        "Procedure", "Provenance", "QuestionnaireResponse", "RiskAssessment"
    },
    "Practitioner": {
        "Practitioner", "Account", "AllergyIntolerance", "Appointment", "AppointmentResponse",
        "CarePlan", "CareTeam", "Claim", "ClaimResponse", "ClinicalImpression", "Communication",
        "CommunicationRequest", "Composition", "Condition", "Consent", "Contract", "Coverage",
        "DeviceRequest", "DeviceUseStatement", "DiagnosticReport", "DocumentManifest",
        "DocumentReference", "Encounter", "EnrollmentRequest", "EpisodeOfCare", "ExplanationOfBenefit",
        "FamilyMemberHistory", "Flag", "Goal", "Group", "ImagingStudy", "Immunization",
        "ImmunizationRecommendation", "MedicationRequest", "MedicationStatement", "MessageHeader",
        "Observation", "Person", "Procedure", "ProcedureRequest", "Provenance",
        "QuestionnaireResponse", "ReferralRequest", "RelatedPerson", "RequestGroup",
        "ResearchSubject", "RiskAssessment", "Schedule", "Specimen", "SupplyDelivery",
        "SupplyRequest", "VisionPrescription"
    },
    "Device": {
        "Device", "DeviceComponent", "DeviceMetric", "DeviceRequest", "DeviceUseStatement",
        "DiagnosticReport", "DocumentReference", "Encounter", "ImagingStudy", "Observation",
        "Procedure", "Provenance", "SupplyDelivery", "SupplyRequest"
    }
}


def get_compartment_resources(compartment_name: str) -> Optional[Set[str]]:
    """
    Get the set of resource types in a compartment.
    
    Args:
        compartment_name: Compartment name (Patient, Encounter, RelatedPerson, Practitioner, Device)
        
    Returns:
        Set of resource type names, or None if compartment not found
    """
    return COMPARTMENTS.get(compartment_name)


def is_resource_in_compartment(resource_type: str, compartment_name: str) -> bool:
    """
    Check if a resource type belongs to a compartment.
    
    Args:
        resource_type: Resource type name (e.g., "Observation")
        compartment_name: Compartment name (e.g., "Patient")
        
    Returns:
        True if resource belongs to compartment, False otherwise
    """
    compartment_resources = get_compartment_resources(compartment_name)
    if compartment_resources is None:
        return False
    return resource_type in compartment_resources


def get_compartments_for_resource(resource_type: str) -> List[str]:
    """
    Get all compartments that contain a resource type.
    
    Args:
        resource_type: Resource type name (e.g., "Observation")
        
    Returns:
        List of compartment names
    """
    compartments = []
    for compartment_name, resources in COMPARTMENTS.items():
        if resource_type in resources:
            compartments.append(compartment_name)

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return compartments


def validate_compartment_search(
    compartment_name: str,
    resource_type: str,
    search_params: Optional[Dict[str, str]] = None
) -> List[str]:
    """
    Validate a compartment-based search.
    
    Args:
        compartment_name: Compartment name (Patient, Encounter, etc.)
        resource_type: Resource type being searched
        search_params: Optional search parameters
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Check if compartment exists
    if compartment_name not in COMPARTMENTS:
        errors.append(f"Unknown compartment: {compartment_name}")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Compartment validation completed with {len(errors)} error(s)")
        return errors
    
    # Check if resource type is in compartment
    if not is_resource_in_compartment(resource_type, compartment_name):
        errors.append(
            f"Resource type '{resource_type}' is not in compartment '{compartment_name}'"
        )
    
    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Compartment validation completed with {len(errors)} error(s)")
    
    return errors


def parse_compartment_url(url: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parse a compartment-based search URL.
    
    Format: /[compartment]/[id]/[resourceType]?parameters
    
    Args:
        url: Compartment search URL
        
    Returns:
        Tuple of (compartment_name, compartment_id, resource_type) or (None, None, None) if invalid
    """
    if not url:
        return None, None, None
    
    # Remove leading/trailing slashes and split
    parts = url.strip("/").split("/")
    
    if len(parts) < 2:
        return None, None, None
    
    compartment_name = parts[0]
    compartment_id = parts[1]
    
    # Resource type is optional (third part)
    resource_type = parts[2] if len(parts) > 2 else None
    
    # Validate compartment name
    if compartment_name not in COMPARTMENTS:
        return None, None, None
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    return compartment_name, compartment_id, resource_type


def format_compartment_url(
    compartment_name: str,
    compartment_id: str,
    resource_type: Optional[str] = None
) -> str:
    """
    Format a compartment-based search URL.
    
    Args:
        compartment_name: Compartment name (Patient, Encounter, etc.)
        compartment_id: Compartment resource ID
        resource_type: Optional resource type to search within compartment
        
    Returns:
        Formatted compartment URL
    """
    if resource_type:
        return f"/{compartment_name}/{compartment_id}/{resource_type}"
    return f"/{compartment_name}/{compartment_id}"

