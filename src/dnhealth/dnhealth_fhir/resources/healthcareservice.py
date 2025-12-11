# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 HealthcareService resource.

HealthcareService represents the details of a healthcare service available at a location.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation, ContactPoint


@dataclass
class HealthcareServiceEligibility:
    """
    FHIR HealthcareService.eligibility complex type.
    
    Specific eligibility requirements required to use the service.
    """
    
    code: Optional[CodeableConcept] = None  # Coded value for the eligibility
    comment: Optional[str] = None  # Describes the eligibility conditions for the service
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class HealthcareServiceAvailableTime:
    """
    FHIR HealthcareService.availableTime complex type.
    
    Times the Service Site is available.
    """
    
    daysOfWeek: List[str] = field(default_factory=list)  # mon | tue | wed | thu | fri | sat | sun
    allDay: Optional[bool] = None  # Always available? i.e. 24 hour service
    availableStartTime: Optional[str] = None  # Opening time of day (ignored if allDay = true)
    availableEndTime: Optional[str] = None  # Closing time of day (ignored if allDay = true)
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class HealthcareServiceNotAvailable:
    """
    FHIR HealthcareService.notAvailable complex type.
    
    Not available during this time due to provided reason.
    """
    
    description: str  # Reason presented to the user explaining why time not available (required)
    during: Optional[Period] = None  # Service not available from this date
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class HealthcareService(DomainResource):
    """
    FHIR R4 HealthcareService resource.
    
    Represents the details of a healthcare service available at a location.
    Extends DomainResource.
    """
    
    resourceType: str = "HealthcareService"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External identifiers for this item
    # Active
    active: Optional[bool] = None  # Whether this healthcare service record is in active use
    # Provided By
    providedBy: Optional[Reference] = None  # Organization that provides this service
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Broad category of service being performed or delivered
    # Type
    type: List[CodeableConcept] = field(default_factory=list)  # Type of service that may be delivered or performed
    # Specialty
    specialty: List[CodeableConcept] = field(default_factory=list)  # Specialties handled by the HealthcareService
    # Location
    location: List[Reference] = field(default_factory=list)  # Location(s) where service may be provided
    # Name
    name: Optional[str] = None  # Description of service as presented to a consumer while searching
    # Comment
    comment: Optional[str] = None  # Additional description and/or any specific issues not covered elsewhere
    # Extra Details
    extraDetails: Optional[str] = None  # Extra details about the service that can't be placed in the other fields
    # Photo
    photo: Optional[Any] = None  # Facilitates quick identification of the service
    # Telecom
    telecom: List[ContactPoint] = field(default_factory=list)  # Contacts related to the healthcare service
    # Coverage Area
    coverageArea: List[Reference] = field(default_factory=list)  # Location(s) service is intended for/available to
    # Service Provision Code
    serviceProvisionCode: List[CodeableConcept] = field(default_factory=list)  # Conditions under which service is available/offered
    # Eligibility
    eligibility: List[HealthcareServiceEligibility] = field(default_factory=list)  # Specific eligibility requirements required to use the service
    # Program
    program: List[CodeableConcept] = field(default_factory=list)  # Programs that this service is applicable to
    # Characteristic
    characteristic: List[CodeableConcept] = field(default_factory=list)  # Collection of characteristics (attributes)
    # Communication
    communication: List[CodeableConcept] = field(default_factory=list)  # The language that this service is offered in
    # Referral Method
    referralMethod: List[CodeableConcept] = field(default_factory=list)  # Ways that the service accepts referrals
    # Appointment Required
    appointmentRequired: Optional[bool] = None  # If an appointment is required for access to this service
    # Available Time
    availableTime: List[HealthcareServiceAvailableTime] = field(default_factory=list)  # Times the Service Site is available
    # Not Available
    notAvailable: List[HealthcareServiceNotAvailable] = field(default_factory=list)  # Not available during this time due to provided reason
    # Availability Exceptions
    availabilityExceptions: Optional[str] = None  # Description of availability exceptions
    # Endpoint
    endpoint: List[Reference] = field(default_factory=list)  # Technical endpoints providing access to services operated for the healthcare service

# Log completion timestamp at end of operations
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
