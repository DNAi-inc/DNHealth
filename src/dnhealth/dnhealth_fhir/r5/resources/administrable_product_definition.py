# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 AdministrableProductDefinition resource.

A medicinal product in the final form which is suitable for administering to a patient (after any mixing of multiple components, dissolution etc. has been performed).
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Attachment, BackboneElement, CodeableConcept, Duration, Extension, Identifier, Quantity, Ratio, Reference
from typing import Any, List, Optional

@dataclass
class AdministrableProductDefinitionProperty:
    """
    AdministrableProductDefinitionProperty nested class.
    """

    type: Optional[CodeableConcept] = None  # A code expressing the type of characteristic.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    value: Optional[Any] = None  # A value for the characteristic.
    status: Optional[CodeableConcept] = None  # The status of characteristic e.g. assigned or pending.

@dataclass
class AdministrableProductDefinitionRouteOfAdministration:
    """
    AdministrableProductDefinitionRouteOfAdministration nested class.
    """

    code: Optional[CodeableConcept] = None  # Coded expression for the route.
    tissue: Optional[CodeableConcept] = None  # Coded expression for the type of tissue for which the withdrawal period applies, e.g. meat, milk.
    value: Optional[Quantity] = None  # A value for the time.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    firstDose: Optional[Quantity] = None  # The first dose (dose quantity) administered can be specified for the product, using a numerical v...
    maxSingleDose: Optional[Quantity] = None  # The maximum single dose that can be administered, specified using a numerical value and its unit ...
    maxDosePerDay: Optional[Quantity] = None  # The maximum dose per day (maximum dose quantity to be administered in any one 24-h period) that c...
    maxDosePerTreatmentPeriod: Optional[Ratio] = None  # The maximum dose per treatment period that can be administered.
    maxTreatmentPeriod: Optional[Duration] = None  # The maximum treatment period during which the product can be administered.
    targetSpecies: Optional[List[BackboneElement]] = field(default_factory=list)  # A species for which this route applies.
    withdrawalPeriod: Optional[List[BackboneElement]] = field(default_factory=list)  # A species specific time during which consumption of animal product is not appropriate.
    supportingInformation: Optional[str] = None  # Extra information about the withdrawal period.

@dataclass
class AdministrableProductDefinitionRouteOfAdministrationTargetSpecies:
    """
    AdministrableProductDefinitionRouteOfAdministrationTargetSpecies nested class.
    """

    code: Optional[CodeableConcept] = None  # Coded expression for the species.
    tissue: Optional[CodeableConcept] = None  # Coded expression for the type of tissue for which the withdrawal period applies, e.g. meat, milk.
    value: Optional[Quantity] = None  # A value for the time.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    withdrawalPeriod: Optional[List[BackboneElement]] = field(default_factory=list)  # A species specific time during which consumption of animal product is not appropriate.
    supportingInformation: Optional[str] = None  # Extra information about the withdrawal period.

@dataclass
class AdministrableProductDefinitionRouteOfAdministrationTargetSpeciesWithdrawalPeriod:
    """
    AdministrableProductDefinitionRouteOfAdministrationTargetSpeciesWithdrawalPeriod nested class.
    """

    tissue: Optional[CodeableConcept] = None  # Coded expression for the type of tissue for which the withdrawal period applies, e.g. meat, milk.
    value: Optional[Quantity] = None  # A value for the time.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    supportingInformation: Optional[str] = None  # Extra information about the withdrawal period.


@dataclass
class AdministrableProductDefinition(FHIRResource):
    """
    A medicinal product in the final form which is suitable for administering to a patient (after any mixing of multiple components, dissolution etc. has been performed).
    """

    status: Optional[str] = None  # The status of this administrable product. Enables tracking the life-cycle of the content.
    routeOfAdministration: List[BackboneElement] = field(default_factory=list)  # The path by which the product is taken into or makes contact with the body. In some regions this ...
    resourceType: str = "AdministrableProductDefinition"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # An identifier for the administrable product.
    formOf: Optional[List[Reference]] = field(default_factory=list)  # References a product from which one or more of the constituent parts of that product can be prepa...
    administrableDoseForm: Optional[CodeableConcept] = None  # The dose form of the final product after necessary reconstitution or processing. Contrasts to the...
    unitOfPresentation: Optional[CodeableConcept] = None  # The presentation type in which this item is given to a patient. e.g. for a spray - 'puff' (as in ...
    producedFrom: Optional[List[Reference]] = field(default_factory=list)  # Indicates the specific manufactured items that are part of the 'formOf' product that are used in ...
    ingredient: Optional[List[CodeableConcept]] = field(default_factory=list)  # The ingredients of this administrable medicinal product. This is only needed if the ingredients a...
    device: Optional[Reference] = None  # A device that is integral to the medicinal product, in effect being considered as an \"ingredient...
    description: Optional[str] = None  # A general description of the product, when in its final form, suitable for administration e.g. ef...
    property: Optional[List[BackboneElement]] = field(default_factory=list)  # Characteristics e.g. a product's onset of action.