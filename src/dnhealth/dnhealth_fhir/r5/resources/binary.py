# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Binary resource.

A resource that represents the data of a single raw artifact as digital content accessible in its native format.  A Binary resource can contain any content, whether text, image, pdf, zip archive, etc.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import Reference
from typing import List, Optional

@dataclass
class Binary(FHIRResource):
    """
    A resource that represents the data of a single raw artifact as digital content accessible in its native format.  A Binary resource can contain any content, whether text, image, pdf, zip archive, etc.
    """

    contentType: Optional[str] = None  # MimeType of the binary content represented as a standard MimeType (BCP 13).
    resourceType: str = "Binary"
    securityContext: Optional[Reference] = None  # This element identifies another resource that can be used as a proxy of the security sensitivity ...
    data: Optional[str] = None  # The actual content, base64 encoded.