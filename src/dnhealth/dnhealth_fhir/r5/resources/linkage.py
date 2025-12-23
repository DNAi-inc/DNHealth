# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Linkage resource.

Identifies two or more records (resource instances) that refer to the same real-world "occurrence".
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, Extension, Reference
from typing import List, Optional

@dataclass
class LinkageItem:
    """
    LinkageItem nested class.
    """

    type: Optional[str] = None  # Distinguishes which item is \"source of truth\" (if any) and which items are no longer considered...
    resource: Optional[Reference] = None  # The resource instance being linked as part of the group.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Linkage(FHIRResource):
    """
    Identifies two or more records (resource instances) that refer to the same real-world "occurrence".
    """

    item: List[BackboneElement] = field(default_factory=list)  # Identifies which record considered as the reference to the same real-world occurrence as well as ...
    resourceType: str = "Linkage"
    active: Optional[bool] = None  # Indicates whether the asserted set of linkages are considered to be \"in effect\".
    author: Optional[Reference] = None  # Identifies the user or organization responsible for asserting the linkages as well as the user or...