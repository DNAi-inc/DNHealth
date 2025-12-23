# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 TestReport resource.

A summary of information based on the results of executing a TestScript.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, Extension, Identifier
from typing import Any, List, Optional

@dataclass
class TestReportParticipant:
    """
    TestReportParticipant nested class.
    """

    type: Optional[str] = None  # The type of participant.
    uri: Optional[str] = None  # The uri of the participant. An absolute URL is preferred.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    display: Optional[str] = None  # The display name of the participant.

@dataclass
class TestReportSetup:
    """
    TestReportSetup nested class.
    """

    action: List[BackboneElement] = field(default_factory=list)  # Action would contain either an operation or an assertion.
    result: Optional[str] = None  # The result of this operation.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    operation: Optional[BackboneElement] = None  # The operation performed.
    message: Optional[str] = None  # An explanatory message associated with the result.
    detail: Optional[str] = None  # A link to further details on the result.
    assert_: Optional[BackboneElement] = None  # The results of the assertion performed on the previous operations.
    requirement: Optional[List[BackboneElement]] = field(default_factory=list)  # Links or references providing traceability to the testing requirements for this assert.
    link: Optional[Any] = None  # Link or reference providing traceability to the testing requirement for this test.

@dataclass
class TestReportSetupAction:
    """
    TestReportSetupAction nested class.
    """

    result: Optional[str] = None  # The result of this operation.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    operation: Optional[BackboneElement] = None  # The operation performed.
    message: Optional[str] = None  # An explanatory message associated with the result.
    detail: Optional[str] = None  # A link to further details on the result.
    assert_: Optional[BackboneElement] = None  # The results of the assertion performed on the previous operations.
    requirement: Optional[List[BackboneElement]] = field(default_factory=list)  # Links or references providing traceability to the testing requirements for this assert.
    link: Optional[Any] = None  # Link or reference providing traceability to the testing requirement for this test.

@dataclass
class TestReportSetupActionOperation:
    """
    TestReportSetupActionOperation nested class.
    """

    result: Optional[str] = None  # The result of this operation.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    message: Optional[str] = None  # An explanatory message associated with the result.
    detail: Optional[str] = None  # A link to further details on the result.

@dataclass
class TestReportSetupActionAssert:
    """
    TestReportSetupActionAssert nested class.
    """

    result: Optional[str] = None  # The result of this assertion.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    message: Optional[str] = None  # An explanatory message associated with the result.
    detail: Optional[str] = None  # A link to further details on the result.
    requirement: Optional[List[BackboneElement]] = field(default_factory=list)  # Links or references providing traceability to the testing requirements for this assert.
    link: Optional[Any] = None  # Link or reference providing traceability to the testing requirement for this test.

@dataclass
class TestReportSetupActionAssertRequirement:
    """
    TestReportSetupActionAssertRequirement nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    link: Optional[Any] = None  # Link or reference providing traceability to the testing requirement for this test.

@dataclass
class TestReportTest:
    """
    TestReportTest nested class.
    """

    action: List[BackboneElement] = field(default_factory=list)  # Action would contain either an operation or an assertion.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    name: Optional[str] = None  # The name of this test used for tracking/logging purposes by test engines.
    description: Optional[str] = None  # A short description of the test used by test engines for tracking and reporting purposes.
    operation: Optional[Any] = None  # An operation would involve a REST request to a server.
    assert_: Optional[Any] = None  # The results of the assertion performed on the previous operations.

@dataclass
class TestReportTestAction:
    """
    TestReportTestAction nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    operation: Optional[Any] = None  # An operation would involve a REST request to a server.
    assert_: Optional[Any] = None  # The results of the assertion performed on the previous operations.

@dataclass
class TestReportTeardown:
    """
    TestReportTeardown nested class.
    """

    action: List[BackboneElement] = field(default_factory=list)  # The teardown action will only contain an operation.
    operation: Optional[Any] = None  # An operation would involve a REST request to a server.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...

@dataclass
class TestReportTeardownAction:
    """
    TestReportTeardownAction nested class.
    """

    operation: Optional[Any] = None  # An operation would involve a REST request to a server.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class TestReport(FHIRResource):
    """
    A summary of information based on the results of executing a TestScript.
    """

    status: Optional[str] = None  # The current state of this test report.
    testScript: Optional[str] = None  # Ideally this is an absolute URL that is used to identify the version-specific TestScript that was...
    result: Optional[str] = None  # The overall result from the execution of the TestScript.
    resourceType: str = "TestReport"
    identifier: Optional[Identifier] = None  # Identifier for the TestReport assigned for external purposes outside the context of FHIR.
    name: Optional[str] = None  # A free text natural language name identifying the executed TestReport.
    score: Optional[float] = None  # The final score (percentage of tests passed) resulting from the execution of the TestScript.
    tester: Optional[str] = None  # Name of the tester producing this report (Organization or individual).
    issued: Optional[str] = None  # When the TestScript was executed and this TestReport was generated.
    participant: Optional[List[BackboneElement]] = field(default_factory=list)  # A participant in the test execution, either the execution engine, a client, or a server.
    setup: Optional[BackboneElement] = None  # The results of the series of required setup operations before the tests were executed.
    test: Optional[List[BackboneElement]] = field(default_factory=list)  # A test executed from the test script.
    teardown: Optional[BackboneElement] = None  # The results of the series of operations required to clean up after all the tests were executed (s...