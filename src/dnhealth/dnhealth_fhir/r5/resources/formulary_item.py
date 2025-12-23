# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 FormularyItem resource.

This resource describes a product or service that is available through a program and includes the conditions and constraints of availability.  All of the information in this resource is specific to the inclusion of the item in the formulary and is not inherent to the item itself.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import CodeableConcept, Identifier
from typing import List, Optional

@dataclass
class FormularyItem(FHIRResource):
    """
    This resource describes a product or service that is available through a program and includes the conditions and constraints of availability.  All of the information in this resource is specific to the inclusion of the item in the formulary and is not inherent to the item itself.
    """

    resourceType: str = "FormularyItem"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for this formulary item.
    code: Optional[CodeableConcept] = None  # A code (or set of codes) that specify the product or service that is identified by this formulary...
    status: Optional[str] = None  # The validity about the information of the formulary item and not of the underlying product or ser...