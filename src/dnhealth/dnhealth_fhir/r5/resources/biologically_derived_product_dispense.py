# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 BiologicallyDerivedProductDispense resource.

A record of dispensation of a biologically derived product.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Quantity, Reference
from typing import List, Optional

@dataclass
class BiologicallyDerivedProductDispensePerformer:
    """
    BiologicallyDerivedProductDispensePerformer nested class.
    """

    actor: Optional[Reference] = None  # Identifies the person responsible for the action.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    function: Optional[CodeableConcept] = None  # Identifies the function of the performer during the dispense.


@dataclass
class BiologicallyDerivedProductDispense(FHIRResource):
    """
    A record of dispensation of a biologically derived product.
    """

    status: Optional[str] = None  # A code specifying the state of the dispense event.
    product: Optional[Reference] = None  # A link to a resource identifying the biologically derived product that is being dispensed.
    patient: Optional[Reference] = None  # A link to a resource representing the patient that the product is dispensed for.
    resourceType: str = "BiologicallyDerivedProductDispense"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Unique instance identifiers assigned to a biologically derived product dispense. Note: This is a ...
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # The order or request that the dispense is fulfilling. This is a reference to a ServiceRequest res...
    partOf: Optional[List[Reference]] = field(default_factory=list)  # A larger event of which this particular event is a component.
    originRelationshipType: Optional[CodeableConcept] = None  # Indicates the relationship between the donor of the biologically derived product and the intended...
    matchStatus: Optional[CodeableConcept] = None  # Indicates the type of matching associated with the dispense.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates who or what performed an action.
    location: Optional[Reference] = None  # The physical location where the dispense was performed.
    quantity: Optional[Quantity] = None  # The amount of product in the dispense. Quantity will depend on the product being dispensed. Examp...
    preparedDate: Optional[str] = None  # When the product was selected/ matched.
    whenHandedOver: Optional[str] = None  # When the product was dispatched for clinical use.
    destination: Optional[Reference] = None  # Link to a resource identifying the physical location that the product was dispatched to.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Additional notes.
    usageInstruction: Optional[str] = None  # Specific instructions for use.