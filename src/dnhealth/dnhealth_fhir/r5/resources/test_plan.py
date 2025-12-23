# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 TestPlan resource.

A plan for executing testing on an artifact or specifications
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Reference, UsageContext
from typing import Any, List, Optional

@dataclass
class TestPlanDependency:
    """
    TestPlanDependency nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # A textual description of the criterium - what is needed for the dependency to be considered met.
    predecessor: Optional[Reference] = None  # Predecessor test plans - those that are expected to be successfully performed as a dependency for...

@dataclass
class TestPlanTestCase:
    """
    TestPlanTestCase nested class.
    """

    type: Optional[Coding] = None  # The type of test data description, e.g. 'synthea'.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    sequence: Optional[int] = None  # Sequence of test case - an ordinal number that indicates the order for the present test case in t...
    scope: Optional[List[Reference]] = field(default_factory=list)  # The scope or artifact covered by the case, when the individual test case is associated with a tes...
    dependency: Optional[List[BackboneElement]] = field(default_factory=list)  # The required criteria to execute the test case - e.g. preconditions, previous tests.
    description: Optional[str] = None  # Description of the criteria.
    predecessor: Optional[Reference] = None  # Link to predecessor test plans.
    testRun: Optional[List[BackboneElement]] = field(default_factory=list)  # The actual test to be executed.
    narrative: Optional[str] = None  # The narrative description of the tests.
    script: Optional[BackboneElement] = None  # The test cases in a structured language e.g. gherkin, Postman, or FHIR TestScript.
    language: Optional[CodeableConcept] = None  # The language for the test cases e.g. 'gherkin', 'testscript'.
    source: Optional[Any] = None  # The actual content of the cases - references to TestScripts or externally defined content.
    testData: Optional[List[BackboneElement]] = field(default_factory=list)  # The test data used in the test case.
    content: Optional[Reference] = None  # The actual test resources when they exist.
    assertion: Optional[List[BackboneElement]] = field(default_factory=list)  # The test assertions - the expectations of test results from the execution of the test case.
    object: Optional[List[Any]] = field(default_factory=list)  # The focus or object of the assertion i.e. a resource.
    result: Optional[List[Any]] = field(default_factory=list)  # The test assertion - the expected outcome from the test case execution.

@dataclass
class TestPlanTestCaseDependency:
    """
    TestPlanTestCaseDependency nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # Description of the criteria.
    predecessor: Optional[Reference] = None  # Link to predecessor test plans.

@dataclass
class TestPlanTestCaseTestRun:
    """
    TestPlanTestCaseTestRun nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    narrative: Optional[str] = None  # The narrative description of the tests.
    script: Optional[BackboneElement] = None  # The test cases in a structured language e.g. gherkin, Postman, or FHIR TestScript.
    language: Optional[CodeableConcept] = None  # The language for the test cases e.g. 'gherkin', 'testscript'.
    source: Optional[Any] = None  # The actual content of the cases - references to TestScripts or externally defined content.

@dataclass
class TestPlanTestCaseTestRunScript:
    """
    TestPlanTestCaseTestRunScript nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    language: Optional[CodeableConcept] = None  # The language for the test cases e.g. 'gherkin', 'testscript'.
    source: Optional[Any] = None  # The actual content of the cases - references to TestScripts or externally defined content.

@dataclass
class TestPlanTestCaseTestData:
    """
    TestPlanTestCaseTestData nested class.
    """

    type: Optional[Coding] = None  # The type of test data description, e.g. 'synthea'.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    content: Optional[Reference] = None  # The actual test resources when they exist.
    source: Optional[Any] = None  # Pointer to a definition of test resources - narrative or structured e.g. synthetic data generatio...

@dataclass
class TestPlanTestCaseAssertion:
    """
    TestPlanTestCaseAssertion nested class.
    """

    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[List[CodeableConcept]] = field(default_factory=list)  # The test assertion type - this can be used to group assertions as 'required' or 'optional', or ca...
    object: Optional[List[Any]] = field(default_factory=list)  # The focus or object of the assertion i.e. a resource.
    result: Optional[List[Any]] = field(default_factory=list)  # The test assertion - the expected outcome from the test case execution.


@dataclass
class TestPlan(FHIRResource):
    """
    A plan for executing testing on an artifact or specifications
    """

    status: Optional[str] = None  # The status of this test plan. Enables tracking the life-cycle of the content.
    resourceType: str = "TestPlan"
    url: Optional[str] = None  # An absolute URI that is used to identify this test plan when it is referenced in a specification,...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this test plan when it is represented in other forma...
    version: Optional[str] = None  # The identifier that is used to identify this version of the test plan when it is referenced in a ...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # A natural language name identifying the test plan. This name should be usable as an identifier fo...
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the test plan.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this test plan is authored for testing purposes (or education/ev...
    date: Optional[str] = None  # The date (and optionally time) when the test plan was last significantly changed. The date must c...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the test plan from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the test plan is intended to be used.
    purpose: Optional[str] = None  # Explanation of why this test plan is needed and why it has been designed as it has.
    copyright: Optional[str] = None  # A copyright statement relating to the test plan and/or its contents. Copyright statements are gen...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    category: Optional[List[CodeableConcept]] = field(default_factory=list)  # The category of the Test Plan - can be acceptance, unit, performance, etc.
    scope: Optional[List[Reference]] = field(default_factory=list)  # What is being tested with this Test Plan - a conformance resource, or narrative criteria, or an e...
    testTools: Optional[str] = None  # A description of test tools to be used in the test plan.
    dependency: Optional[List[BackboneElement]] = field(default_factory=list)  # The required criteria to execute the test plan - e.g. preconditions, previous tests...
    exitCriteria: Optional[str] = None  # The threshold or criteria for the test plan to be considered successfully executed - narrative.
    testCase: Optional[List[BackboneElement]] = field(default_factory=list)  # The individual test cases that are part of this plan, when they they are made explicit.