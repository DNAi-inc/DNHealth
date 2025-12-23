# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Endpoint resource.

The technical details of an endpoint that can be used for electronic services, such as for web services providing XDS.b, a REST endpoint for another FHIR server, or a s/Mime email address. This may include any security context information.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, ContactPoint, Extension, Identifier, Period, Reference
from typing import List, Optional

@dataclass
class EndpointPayload:
    """
    EndpointPayload nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The payload type describes the acceptable content that can be communicated on the endpoint.
    mimeType: Optional[List[str]] = field(default_factory=list)  # The mime type to send the payload in - e.g. application/fhir+xml, application/fhir+json. If the m...


@dataclass
class Endpoint(FHIRResource):
    """
    The technical details of an endpoint that can be used for electronic services, such as for web services providing XDS.b, a REST endpoint for another FHIR server, or a s/Mime email address. This may include any security context information.
    """

    status: Optional[str] = None  # The endpoint status represents the general expected availability of an endpoint.
    connectionType: List[CodeableConcept] = field(default_factory=list)  # A coded value that represents the technical details of the usage of this endpoint, such as what
    address: Optional[str] = None  # The uri that describes the actual end-point to connect to.
    resourceType: str = "Endpoint"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # Identifier for the organization that is used to identify the endpoint across multiple disparate s...
    name: Optional[str] = None  # A friendly name that this endpoint can be referred to with.
    description: Optional[str] = None  # The description of the endpoint and what it is for (typically used as supplemental information in...
    environmentType: Optional[List[CodeableConcept]] = field(default_factory=list)  # The type of environment(s) exposed at this endpoint (dev, prod, test, etc.).
    managingOrganization: Optional[Reference] = None  # The organization that manages this endpoint (even if technically another organization is hosting ...
    contact: Optional[List[ContactPoint]] = field(default_factory=list)  # Contact details for a human to contact about the endpoint. The primary use of this for system adm...
    period: Optional[Period] = None  # The interval during which the endpoint is expected to be operational.
    payload: Optional[List[BackboneElement]] = field(default_factory=list)  # The set of payloads that are provided/available at this endpoint.
    header: Optional[List[str]] = field(default_factory=list)  # Additional headers / information to send as part of the notification.