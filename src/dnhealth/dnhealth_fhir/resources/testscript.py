# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 TestScript resource.

TestScript defines a set of tests against a FHIR server implementation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dnhealth.dnhealth_fhir.resources.base import MetadataResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    ContactDetail,
    UsageContext,
    RelatedArtifact,
)


@dataclass
class TestScriptOrigin:
    """
    FHIR TestScript.origin complex type.
    
    An abstract server used in operations within this test script.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    index: int  # The index of the abstract origin server (required)
    profile: Any  # FHIR-Client | FHIR-SDC-FormFiller | FHIR-SDC-FormManager | FHIR-SDC-FormReceiver | FHIR-Server (Coding, required)


@dataclass
class TestScriptDestination:
    """
    FHIR TestScript.destination complex type.
    
    An abstract server used in operations within this test script.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    index: int  # The index of the abstract destination server (required)
    profile: Any  # FHIR-Client | FHIR-SDC-FormFiller | FHIR-SDC-FormManager | FHIR-SDC-FormReceiver | FHIR-Server (Coding, required)


@dataclass
class TestScriptMetadata:
    """
    FHIR TestScript.metadata complex type.
    
    The required capability that must exist and are required to execute the test script.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    link: List[Any] = field(default_factory=list)  # Links to the FHIR specification (TestScriptMetadataLink)
    capability: List[Any] = field(default_factory=list)  # Capabilities that must exist (TestScriptMetadataCapability, required)


@dataclass
class TestScriptFixture:
    """
    FHIR TestScript.fixture complex type.
    
    Fixture in the test script.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    autocreate: bool  # Whether or not to implicitly create the fixture during setup (required)
    autodelete: bool  # Whether or not to implicitly delete the fixture during teardown (required)
    resource: Optional[Reference] = None  # Reference to the resource


@dataclass
class TestScriptVariable:
    """
    FHIR TestScript.variable complex type.
    
    Variable is set based either on element value in response body or on header field value in the response headers.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    name: Optional[str] = None  # Descriptive name for this variable
    defaultValue: Optional[str] = None  # Default, hard-coded, or user-defined value for this variable
    description: Optional[str] = None  # Natural language description of the variable
    expression: Optional[str] = None  # The FHIRPath expression against the fixture body
    headerField: Optional[str] = None  # HTTP header field name for source
    hint: Optional[str] = None  # Hint help text for default value to enter
    path: Optional[str] = None  # XPath or JSONPath against the fixture body
    sourceId: Optional[str] = None  # Fixture Id of source expression or headerField within this variable


@dataclass
class TestScriptSetup:
    """
    FHIR TestScript.setup complex type.
    
    A series of required setup operations before tests are executed.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    action: List[Any] = field(default_factory=list)  # A setup operation or assert to perform (TestScriptSetupAction, required)


@dataclass
class TestScriptTest:
    """
    FHIR TestScript.test complex type.
    
    A test in this script.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    name: Optional[str] = None  # Tracking/logging name of this test
    description: Optional[str] = None  # Tracking/reporting short description of the test
    action: List[Any] = field(default_factory=list)  # A test operation or assert to perform (TestScriptTestAction, required)


@dataclass
class TestScriptTeardown:
    """
    FHIR TestScript.teardown complex type.
    
    A series of required clean up steps.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    action: List[Any] = field(default_factory=list)  # The teardown action to perform (TestScriptTeardownAction, required)


@dataclass
class TestScript(MetadataResource):
    """
    FHIR R4 TestScript resource.
    
    Defines a set of tests against a FHIR server implementation.
    Extends MetadataResource.
    """
    
    resourceType: str = "TestScript"
    # URL
    url: str  # Canonical URL (inherited from CanonicalResource, required)
    # Identifier
    identifier: Optional[Identifier] = None  # Additional identifier (inherited from CanonicalResource)
    # Version
    version: Optional[str] = None  # Business version (inherited from CanonicalResource)
    # Name
    name: str  # Name for this test script (inherited from CanonicalResource, required)
    # Title
    title: Optional[str] = None  # Title for this test script (inherited from CanonicalResource)
    # Status
    status: str  # draft | active | retired | unknown (inherited from CanonicalResource, required)
    # Experimental
    experimental: Optional[bool] = None  # For testing purposes (inherited from CanonicalResource)
    # Date
    date: Optional[str] = None  # Date last changed (inherited from CanonicalResource)
    # Publisher
    publisher: Optional[str] = None  # Name of publisher (inherited from CanonicalResource)
    # Contact
    contact: List[ContactDetail] = field(default_factory=list)  # Contact details (inherited from CanonicalResource)
    # Description
    description: Optional[str] = None  # Natural language description (inherited from CanonicalResource)
    # Use Context
    useContext: List[UsageContext] = field(default_factory=list)  # Context of use (inherited from CanonicalResource)
    # Jurisdiction
    jurisdiction: List[CodeableConcept] = field(default_factory=list)  # Intended jurisdiction (inherited from CanonicalResource)
    # Purpose
    purpose: Optional[str] = None  # Why this test script is defined (inherited from CanonicalResource)
    # Copyright
    copyright: Optional[str] = None  # Use and/or publishing restrictions (inherited from CanonicalResource)
    # Approval Date
    approvalDate: Optional[str] = None  # When the test script was approved by publisher (inherited from MetadataResource)
    # Last Review Date
    lastReviewDate: Optional[str] = None  # Date on which the resource content was last reviewed (inherited from MetadataResource)
    # Effective Period
    effectivePeriod: Optional[Period] = None  # When the test script is expected to be in use (inherited from MetadataResource)
    # Topic
    topic: List[CodeableConcept] = field(default_factory=list)  # The category of the test script (inherited from MetadataResource)
    # Author
    author: List[Reference] = field(default_factory=list)  # Who authored the content (inherited from MetadataResource)
    # Editor
    editor: List[Reference] = field(default_factory=list)  # Who edited the content (inherited from MetadataResource)
    # Reviewer
    reviewer: List[Reference] = field(default_factory=list)  # Who reviewed the content (inherited from MetadataResource)
    # Endorser
    endorser: List[Reference] = field(default_factory=list)  # Who endorsed the content (inherited from MetadataResource)
    # Related Artifact
    relatedArtifact: List[RelatedArtifact] = field(default_factory=list)  # Additional documentation, citations, etc. (inherited from MetadataResource)
    # Origin
    origin: List[TestScriptOrigin] = field(default_factory=list)  # An abstract server used in operations within this test script
    # Destination
    destination: List[TestScriptDestination] = field(default_factory=list)  # An abstract server used in operations within this test script
    # Metadata
    metadata: Optional[TestScriptMetadata] = None  # The required capability that must exist and are required to execute the test script
    # Fixture
    fixture: List[TestScriptFixture] = field(default_factory=list)  # Fixture in the test script
    # Profile
    profile: List[Reference] = field(default_factory=list)  # Reference of the validation profile
    # Variable
    variable: List[TestScriptVariable] = field(default_factory=list)  # Placeholder for evaluated elements
    # Setup
    setup: Optional[TestScriptSetup] = None  # A series of required setup operations before tests are executed
    # Test
    test: List[TestScriptTest] = field(default_factory=list)  # A test in this script
    # Teardown
    teardown: Optional[TestScriptTeardown] = None  # A series of required clean up steps


# Log completion timestamp at end of operations
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Current Time at End of Operations: {current_time}")
