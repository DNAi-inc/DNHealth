# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 GenomicStudy resource.

A set of analyses performed to analyze and generate genomic data.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, BackboneElement, CodeableConcept, Extension, Identifier, Reference
from typing import Any, List, Optional

@dataclass
class GenomicStudyAnalysis:
    """
    GenomicStudyAnalysis nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers for the analysis event.
    methodType: Optional[List[CodeableConcept]] = field(default_factory=list)  # Type of the methods used in the analysis, e.g., Fluorescence in situ hybridization (FISH), Karyot...
    changeType: Optional[List[CodeableConcept]] = field(default_factory=list)  # Type of the genomic changes studied in the analysis, e.g., DNA, RNA, or amino acid change.
    genomeBuild: Optional[CodeableConcept] = None  # The reference genome build that is used in this analysis.
    instantiatesCanonical: Optional[str] = None  # The defined protocol that describes the analysis.
    instantiatesUri: Optional[str] = None  # The URL pointing to an externally maintained protocol that describes the analysis.
    title: Optional[str] = None  # Name of the analysis event (human friendly).
    focus: Optional[List[Reference]] = field(default_factory=list)  # The focus of a genomic analysis when it is not the patient of record representing something or so...
    specimen: Optional[List[Reference]] = field(default_factory=list)  # The specimen used in the analysis event.
    date: Optional[str] = None  # The date of the analysis event.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Any notes capture with the analysis event.
    protocolPerformed: Optional[Reference] = None  # The protocol that was performed for the analysis event.
    regionsStudied: Optional[List[Reference]] = field(default_factory=list)  # The genomic regions to be studied in the analysis (BED file).
    regionsCalled: Optional[List[Reference]] = field(default_factory=list)  # Genomic regions actually called in the analysis event (BED file).
    input: Optional[List[BackboneElement]] = field(default_factory=list)  # Inputs for the analysis event.
    file: Optional[Reference] = None  # File containing input data.
    type: Optional[CodeableConcept] = None  # Type of input data, e.g., BAM, CRAM, or FASTA.
    generatedBy: Optional[Any] = None  # The analysis event or other GenomicStudy that generated this input file.
    output: Optional[List[BackboneElement]] = field(default_factory=list)  # Outputs for the analysis event.
    performer: Optional[List[BackboneElement]] = field(default_factory=list)  # Performer for the analysis event.
    actor: Optional[Reference] = None  # The organization, healthcare professional, or others who participated in performing this analysis.
    role: Optional[CodeableConcept] = None  # Role of the actor for this analysis.
    device: Optional[List[BackboneElement]] = field(default_factory=list)  # Devices used for the analysis (e.g., instruments, software), with settings and parameters.
    function: Optional[CodeableConcept] = None  # Specific function for the device used for the analysis.

@dataclass
class GenomicStudyAnalysisInput:
    """
    GenomicStudyAnalysisInput nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    file: Optional[Reference] = None  # File containing input data.
    type: Optional[CodeableConcept] = None  # Type of input data, e.g., BAM, CRAM, or FASTA.
    generatedBy: Optional[Any] = None  # The analysis event or other GenomicStudy that generated this input file.

@dataclass
class GenomicStudyAnalysisOutput:
    """
    GenomicStudyAnalysisOutput nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    file: Optional[Reference] = None  # File containing output data.
    type: Optional[CodeableConcept] = None  # Type of output data, e.g., VCF, MAF, or BAM.

@dataclass
class GenomicStudyAnalysisPerformer:
    """
    GenomicStudyAnalysisPerformer nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    actor: Optional[Reference] = None  # The organization, healthcare professional, or others who participated in performing this analysis.
    role: Optional[CodeableConcept] = None  # Role of the actor for this analysis.

@dataclass
class GenomicStudyAnalysisDevice:
    """
    GenomicStudyAnalysisDevice nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    device: Optional[Reference] = None  # Device used for the analysis.
    function: Optional[CodeableConcept] = None  # Specific function for the device used for the analysis.


@dataclass
class GenomicStudy(FHIRResource):
    """
    A set of analyses performed to analyze and generate genomic data.
    """

    status: Optional[str] = None  # The status of the genomic study.
    subject: Optional[Reference] = None  # The primary subject of the genomic study.
    resourceType: str = "GenomicStudy"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers for this genomic study.
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The type of the study, e.g., Familial variant segregation, Functional variation detection, or Gen...
    encounter: Optional[Reference] = None  # The healthcare event with which this genomics study is associated.
    startDate: Optional[str] = None  # When the genomic study was started.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Event resources that the genomic study is based on.
    referrer: Optional[Reference] = None  # Healthcare professional who requested or referred the genomic study.
    interpreter: Optional[List[Reference]] = field(default_factory=list)  # Healthcare professionals who interpreted the genomic study.
    reason: Optional[List[Any]] = field(default_factory=list)  # Why the genomic study was performed.
    instantiatesCanonical: Optional[str] = None  # The defined protocol that describes the study.
    instantiatesUri: Optional[str] = None  # The URL pointing to an externally maintained protocol that describes the study.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments related to the genomic study.
    description: Optional[str] = None  # Description of the genomic study.
    analysis: Optional[List[BackboneElement]] = field(default_factory=list)  # The details about a specific analysis that was performed in this GenomicStudy.