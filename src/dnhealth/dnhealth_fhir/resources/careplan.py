# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 CarePlan resource.

CarePlan describes the intention of how one or more practitioners intend to deliver care for a particular patient.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period, Annotation
import logging
from datetime import datetime



logger = logging.getLogger(__name__)
@dataclass
class CarePlanActivity:
    """
    FHIR CarePlan.activity complex type.
    
    Identifies a planned action to occur as part of the plan.
    """
    
    outcomeCodeableConcept: List[CodeableConcept] = field(default_factory=list)  # Results of the activity
    outcomeReference: List[Reference] = field(default_factory=list)  # Appointment, Encounter, Procedure, etc.
    progress: List[Annotation] = field(default_factory=list)  # Comments about the activity status/progress
    reference: Optional[Reference] = None  # Activity details defined in specific resource
    detail: Optional[Dict[str, Any]] = None  # In-line definition of activity
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class CarePlan(DomainResource):
    """
    FHIR R4 CarePlan resource.
    
    Describes the intention of how one or more practitioners intend to deliver care for a particular patient.
    Extends DomainResource.
    """
    
    resourceType: str = "CarePlan"
    # Required fields (using Optional to satisfy dataclass field ordering, validated in __post_init__)
    # Status
    status: Optional[str] = None  # draft | active | on-hold | revoked | completed | entered-in-error | unknown (required)
    # Intent
    intent: Optional[str] = None  # proposal | plan | order | option (required)
    # Subject
    subject: Optional[Reference] = None  # Who the care plan is for (required)
    # Optional fields
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # External Ids for this plan
    # Instantiates Canonical
    instantiatesCanonical: List[str] = field(default_factory=list)  # Instantiates FHIR protocol or definition
    # Instantiates URI
    instantiatesUri: List[str] = field(default_factory=list)  # Instantiates external protocol or definition
    # Based On
    basedOn: List[Reference] = field(default_factory=list)  # Fulfills CarePlan
    # Replaces
    replaces: List[Reference] = field(default_factory=list)  # CarePlan replaced by this CarePlan
    # Part Of
    partOf: List[Reference] = field(default_factory=list)  # Part of referenced CarePlan
    # Category
    category: List[CodeableConcept] = field(default_factory=list)  # Type of plan
    # Title
    title: Optional[str] = None  # Human-friendly name for the care plan
    # Description
    description: Optional[str] = None  # Summary of nature/purpose
    # Encounter
    encounter: Optional[Reference] = None  # Encounter created as part of
    # Period
    period: Optional[Period] = None  # Time period plan covers
    # Created
    created: Optional[str] = None  # Date record was first recorded
    # Author
    author: Optional[Reference] = None  # Who is the designated responsible party
    # Contributor
    contributor: List[Reference] = field(default_factory=list)  # Who provided the content of the care plan
    # Care Team
    careTeam: List[Reference] = field(default_factory=list)  # Who's involved in plan execution
    # Addresses
    addresses: List[Reference] = field(default_factory=list)  # Health issues this plan addresses
    # Supporting Info
    supportingInfo: List[Reference] = field(default_factory=list)  # Information considered as part of plan
    # Goal
    goal: List[Reference] = field(default_factory=list)  # Desired outcome of plan
    # Activity
    activity: List[CarePlanActivity] = field(default_factory=list)  # Action to occur as part of plan
    # Note
    note: List[Annotation] = field(default_factory=list)  # Comments about the plan
    
    def __post_init__(self):
        """Validate required fields after initialization."""
        super().__post_init__()
        if self.status is None:
            raise ValueError("status is required for CarePlan")
        if self.intent is None:
            raise ValueError("intent is required for CarePlan")
        if self.subject is None:
            raise ValueError("subject is required for CarePlan")
        
        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
