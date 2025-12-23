# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 TestReport resource.

TestReport represents a summary of a test execution.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from datetime import datetime
import logging

from dnhealth.dnhealth_fhir.resources.base import DomainResource
from dnhealth.dnhealth_fhir.types import (
    Extension,
    Identifier,
    Reference,
    Period,
    Attachment,
)


logger = logging.getLogger(__name__)


@dataclass
class TestReportParticipant:
    """
    FHIR TestReport.participant complex type.
    
    A participant in the test execution.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: type is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce type is provided.
    type: Optional[str] = None  # test-engine | client | server (required)
    # Note: uri is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce uri is provided.
    uri: Optional[str] = None  # The uri of the participant (required)
    display: Optional[str] = None  # The display name of the participant


@dataclass
class TestReportSetup:
    """
    FHIR TestReport.setup complex type.
    
    The results of the setup operation.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    action: List["TestReportSetupAction"] = field(default_factory=list)  # A setup operation or assertion (required)


@dataclass
class TestReportSetupAction:
    """
    FHIR TestReport.setup.action complex type.
    
    The operation performed.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    operation: Optional["TestReportSetupActionOperation"] = None  # The operation performed
    assert_: Optional["TestReportSetupActionAssert"] = None  # The assertion performed


@dataclass
class TestReportSetupActionOperation:
    """
    FHIR TestReport.setup.action.operation complex type.
    
    The operation performed.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: result is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce result is provided.
    result: Optional[str] = None  # pass | skip | fail | warning | error (required)
    message: Optional[str] = None  # A message associated with the result
    detail: Optional[str] = None  # A link to further details on the result


@dataclass
class TestReportSetupActionAssert:
    """
    FHIR TestReport.setup.action.assert complex type.
    
    The assertion performed.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    # Note: result is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce result is provided.
    result: Optional[str] = None  # pass | skip | fail | warning | error (required)
    message: Optional[str] = None  # A message associated with the result
    detail: Optional[str] = None  # A link to further details on the result


@dataclass
class TestReportTest:
    """
    FHIR TestReport.test complex type.
    
    A test executed from the test script.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    name: Optional[str] = None  # Tracking/logging name of this test
    description: Optional[str] = None  # Tracking/reporting short description of the test
    action: List["TestReportTestAction"] = field(default_factory=list)  # A test operation or assertion (required)


@dataclass
class TestReportTestAction:
    """
    FHIR TestReport.test.action complex type.
    
    A test operation or assertion that was performed.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    operation: Optional[TestReportSetupActionOperation] = None  # The operation performed
    assert_: Optional[TestReportSetupActionAssert] = None  # The assertion performed


@dataclass
class TestReportTeardown:
    """
    FHIR TestReport.teardown complex type.
    
    The results of the teardown operation.
    """
    
    id: Optional[str] = None
    extension: List[Extension] = field(default_factory=list)
    modifierExtension: List[Extension] = field(default_factory=list)
    action: List[TestReportSetupAction] = field(default_factory=list)  # The teardown operation performed (required)


@dataclass
class TestReport(DomainResource):
    """
    FHIR R4 TestReport resource.
    
    Represents a summary of a test execution.
    Extends DomainResource.
    """
    
    resourceType: str = "TestReport"
    # Identifier
    identifier: Optional[Identifier] = None  # External identifier
    # Name
    name: Optional[str] = None  # Informal name of the executed TestScript
    # Status
    # Note: status is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce status is provided.
    status: Optional[str] = None  # completed | in-progress | waiting | stopped | entered-in-error (required)
    # Test Script
    # Note: testScript is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce testScript is provided.
    testScript: Optional[Reference] = None  # Reference to TestScript that was executed (required)
    # Result
    # Note: result is required in FHIR, but made Optional here for Python dataclass field ordering compatibility
    # Validation should enforce result is provided.
    result: Optional[str] = None  # pass | fail | pending (required)
    # Score
    score: Optional[float] = None  # The final score
    # Tester
    tester: Optional[str] = None  # Name of the tester producing this report
    # Issued
    issued: Optional[str] = None  # When the test execution was performed
    # Participant
    participant: List[TestReportParticipant] = field(default_factory=list)  # A participant in the test execution
    # Setup
    setup: Optional[TestReportSetup] = None  # The results of the setup operation
    # Test
    test: List[TestReportTest] = field(default_factory=list)  # A test executed from the test script
    # Teardown
    teardown: Optional[TestReportTeardown] = None  # The results of the teardown operation

def _log_module_initialization():
    """Log module initialization timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

# Log module initialization
_log_module_initialization()

