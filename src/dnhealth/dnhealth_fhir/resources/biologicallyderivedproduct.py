# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 BiologicallyDerivedProduct resource.

BiologicallyDerivedProduct describes a material substance originating from a biological entity.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import Extension, Identifier, CodeableConcept, Reference, Period


@dataclass
class BiologicallyDerivedProductCollection:
    """
    FHIR BiologicallyDerivedProduct.collection complex type.
    
    How this product was collected.
    """
    
    collector: Optional[Reference] = None  # Who collected this product
    source: Optional[Reference] = None  # Patient or group from which the product was collected
    collectedDateTime: Optional[str] = None  # Time of product collection
    collectedPeriod: Optional[Period] = None  # Time of product collection
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class BiologicallyDerivedProductProcessing:
    """
    FHIR BiologicallyDerivedProduct.processing complex type.
    
    Any processing of the product during collection.
    """
    
    description: Optional[str] = None  # Description of processing
    procedure: Optional[CodeableConcept] = None  # Procesing code
    additive: Optional[Reference] = None  # Substance added during processing
    timeDateTime: Optional[str] = None  # Time of processing
    timePeriod: Optional[Period] = None  # Time of processing
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class BiologicallyDerivedProductManipulation:
    """
    FHIR BiologicallyDerivedProduct.manipulation complex type.
    
    Any manipulation of product post-collection.
    """
    
    description: Optional[str] = None  # Description of manipulation
    timeDateTime: Optional[str] = None  # Time of manipulation
    timePeriod: Optional[Period] = None  # Time of manipulation
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class BiologicallyDerivedProductStorage:
    """
    FHIR BiologicallyDerivedProduct.storage complex type.
    
    Product storage.
    """
    
    description: Optional[str] = None  # Description of storage
    temperature: Optional[float] = None  # Storage temperature
    scale: Optional[str] = None  # farenheit | celsius | kelvin
    duration: Optional[Period] = None  # Storage timeperiod
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)


@dataclass
class BiologicallyDerivedProduct(DomainResource):
    """
    FHIR R4 BiologicallyDerivedProduct resource.
    
    Describes a material substance originating from a biological entity.
    Extends DomainResource.
    """
    
    resourceType: str = "BiologicallyDerivedProduct"
    # Identifier
    identifier: List[Identifier] = field(default_factory=list)  # Business identifier of this biologically-derived product
    # Product Category
    productCategory: Optional[str] = None  # organ | tissue | fluid | cells | biologicalAgent
    # Product Code
    productCode: Optional[CodeableConcept] = None  # What this biologically-derived product is
    # Status
    status: Optional[str] = None  # available | unavailable
    # Request
    request: List[Reference] = field(default_factory=list)  # Request to obtain and/or distribute this biologically-derived product
    # Quantity
    quantity: Optional[int] = None  # Number of discrete units within this product
    # Parent
    parent: List[Reference] = field(default_factory=list)  # Parent product
    # Collection
    collection: Optional[BiologicallyDerivedProductCollection] = None  # How this product was collected
    # Processing
    processing: List[BiologicallyDerivedProductProcessing] = field(default_factory=list)  # Any processing of the product during collection
    # Manipulation
    manipulation: Optional[BiologicallyDerivedProductManipulation] = None  # Any manipulation of product post-collection
    # Storage
    storage: List[BiologicallyDerivedProductStorage] = field(default_factory=list)  # Product storage

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()


