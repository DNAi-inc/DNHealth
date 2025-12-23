# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 DiagnosticReport resource.

The findings and interpretation of diagnostic tests performed on patients, groups of patients, products, substances, devices, and locations, and/or specimens derived from these. The report includes clinical context such as requesting provider information, and some mix of atomic results, images, textual and coded interpretations, and formatted representation of diagnostic reports. The report also includes non-clinical context such as batch analysis and stability reporting of products and substances.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Annotation, Attachment, BackboneElement, CodeableConcept, Extension, Identifier, Period, Reference
from typing import Any, List, Optional

@dataclass
class DiagnosticReportSupportingInfo:
    """
    DiagnosticReportSupportingInfo nested class.
    """

    type: Optional[CodeableConcept] = None  # The code value for the role of the supporting information in the diagnostic report.
    reference: Optional[Reference] = None  # The reference for the supporting information in the diagnostic report.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class DiagnosticReportMedia:
    """
    DiagnosticReportMedia nested class.
    """

    link: Optional[Reference] = None  # Reference to the image or data source.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    comment: Optional[str] = None  # A comment about the image or data. Typically, this is used to provide an explanation for why the ...


@dataclass
class DiagnosticReport(FHIRResource):
    """
    The findings and interpretation of diagnostic tests performed on patients, groups of patients, products, substances, devices, and locations, and/or specimens derived from these. The report includes clinical context such as requesting provider information, and some mix of atomic results, images, textual and coded interpretations, and formatted representation of diagnostic reports. The report also includes non-clinical context such as batch analysis and stability reporting of products and substances.
    """

    status: Optional[str] = None  # The status of the diagnostic report.
    code: Optional[CodeableConcept] = None  # A code or name that describes this diagnostic report.
    resourceType: str = "DiagnosticReport"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifiers assigned to this report by the performer or other systems.
    basedOn: Optional[List[Reference]] = field(default_factory=list)  # Details concerning a service requested.
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # A code that classifies the clinical discipline, department or diagnostic service that created the...
    subject: Optional[Reference] = None  # The subject of the report. Usually, but not always, this is a patient. However, diagnostic servic...
    encounter: Optional[Reference] = None  # The healthcare event  (e.g. a patient and healthcare provider interaction) which this DiagnosticR...
    effective: Optional[Any] = None  # The time or time-period the observed values are related to. When the subject of the report is a p...
    issued: Optional[str] = None  # The date and time that this version of the report was made available to providers, typically afte...
    performer: Optional[List[Reference]] = field(default_factory=list)  # The diagnostic service that is responsible for issuing the report.
    resultsInterpreter: Optional[List[Reference]] = field(default_factory=list)  # The practitioner or organization that is responsible for the report's conclusions and interpretat...
    specimen: Optional[List[Reference]] = field(default_factory=list)  # Details about the specimens on which this diagnostic report is based.
    result: Optional[List[Reference]] = field(default_factory=list)  # [Observations](observation.html)  that are part of this diagnostic report.
    note: Optional[List[Annotation]] = field(default_factory=list)  # Comments about the diagnostic report.
    study: Optional[List[Reference]] = field(default_factory=list)  # One or more links to full details of any study performed during the diagnostic investigation. An ...
    supportingInfo: Optional[List[BackboneElement]] = field(default_factory=list)  # This backbone element contains supporting information that was used in the creation of the report...
    media: Optional[List[BackboneElement]] = field(default_factory=list)  # A list of key images or data associated with this report. The images or data are generally create...
    composition: Optional[Reference] = None  # Reference to a Composition resource instance that provides structure for organizing the contents ...
    conclusion: Optional[str] = None  # Concise and clinically contextualized summary conclusion (interpretation/impression) of the diagn...
    conclusionCode: Optional[List[CodeableConcept]] = field(default_factory=list)  # One or more codes that represent the summary conclusion (interpretation/impression) of the diagno...
    presentedForm: Optional[List[Attachment]] = field(default_factory=list)  # Rich text representation of the entire result as issued by the diagnostic service. Multiple forma...