# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 InventoryReport resource.

A report of inventory or stock items.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Period, Quantity, Reference
from typing import Any, List, Optional

@dataclass
class InventoryReportInventoryListing:
    """
    InventoryReportInventoryListing nested class.
    """

    quantity: Optional[Quantity] = None  # The quantity of the item or items being reported.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    location: Optional[Reference] = None  # Location of the inventory items.
    itemStatus: Optional[CodeableConcept] = None  # The status of the items.
    countingDateTime: Optional[str] = None  # The date and time when the items were counted.
    item: Optional[List[BackboneElement]] = field(default_factory=list)  # The item or items in this listing.
    category: Optional[CodeableConcept] = None  # The inventory category or classification of the items being reported. This is meant not for defin...

@dataclass
class InventoryReportInventoryListingItem:
    """
    InventoryReportInventoryListingItem nested class.
    """

    quantity: Optional[Quantity] = None  # The quantity of the item or items being reported.
    item: Optional[Any] = None  # The code or reference to the item type.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    category: Optional[CodeableConcept] = None  # The inventory category or classification of the items being reported. This is meant not for defin...


@dataclass
class InventoryReport(FHIRResource):
    """
    A report of inventory or stock items.
    """

    status: Optional[str] = None  # The status of the inventory check or notification - whether this is draft (e.g. the report is sti...
    countType: Optional[str] = None  # Whether the report is about the current inventory count (snapshot) or a differential change in in...
    reportedDateTime: Optional[str] = None  # When the report has been submitted.
    resourceType: str = "InventoryReport"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Business identifier for the InventoryReport.
    operationType: Optional[CodeableConcept] = None  # What type of operation is being performed - addition or subtraction.
    operationTypeReason: Optional[CodeableConcept] = None  # The reason for this count - regular count, ad-hoc count, new arrivals, etc.
    reporter: Optional[Reference] = None  # Who submits the report.
    reportingPeriod: Optional[Period] = None  # The period the report refers to.
    inventoryListing: Optional[List[BackboneElement]] = field(default_factory=list)  # An inventory listing section (grouped by any of the attributes).
    note: Optional[List[Annotation]] = field(default_factory=list)  # A note associated with the InventoryReport.