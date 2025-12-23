# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Flag resource.

Prospective warnings of potential issues when providing care to the patient.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier, Period, Reference
from typing import List, Optional

@dataclass
class Flag(FHIRResource):
    """
    Prospective warnings of potential issues when providing care to the patient.
    """

    status: Optional[str] = None  # Supports basic workflow.
    code: Optional[CodeableConcept] = None  # The coded value or textual component of the flag to display to the user.
    subject: Optional[Reference] = None  # The patient, related person, location, group, organization, or practitioner etc. this is about re...
    resourceType: str = "Flag"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifiers assigned to this flag by the performer or other systems which remain constan...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # Allows a flag to be divided into different categories like clinical, administrative etc. Intended...
    period: Optional[Period] = None  # The period of time from the activation of the flag to inactivation of the flag. If the flag is ac...
    encounter: Optional[Reference] = None  # This alert is only relevant during the encounter.
    author: Optional[Reference] = None  # The person, organization or device that created the flag.