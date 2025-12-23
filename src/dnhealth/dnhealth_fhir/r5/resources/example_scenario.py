# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 ExampleScenario resource.

A walkthrough of a workflow showing the interaction between systems and the instances shared, possibly including the evolution of instances over time.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Coding, ContactDetail, Extension, Identifier, Reference, UsageContext
from typing import Any, List, Optional

@dataclass
class ExampleScenarioActor:
    """
    ExampleScenarioActor nested class.
    """

    key: Optional[str] = None  # A unique string within the scenario that is used to reference the actor.
    type: Optional[str] = None  # The category of actor - person or system.
    title: Optional[str] = None  # The human-readable name for the actor used when rendering the scenario.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # An explanation of who/what the actor is and its role in the scenario.

@dataclass
class ExampleScenarioInstance:
    """
    ExampleScenarioInstance nested class.
    """

    key: Optional[str] = None  # A unique string within the scenario that is used to reference the instance.
    structureType: Optional[Coding] = None  # A code indicating the kind of data structure (FHIR resource or some other standard) this is an in...
    title: Optional[str] = None  # A short descriptive label the instance to be used in tables or diagrams.
    instanceReference: Optional[str] = None  # A reference to the key of an instance found within this one.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    structureVersion: Optional[str] = None  # Conveys the version of the data structure instantiated.  I.e. what release of FHIR, X12, OpenEHR,...
    structureProfile: Optional[Any] = None  # Refers to a profile, template or other ruleset the instance adheres to.
    description: Optional[str] = None  # An explanation of what the instance contains and what it's for.
    content: Optional[Reference] = None  # Points to an instance (typically an example) that shows the data that would corespond to this ins...
    version: Optional[List[BackboneElement]] = field(default_factory=list)  # Represents the instance as it was at a specific time-point.
    containedInstance: Optional[List[BackboneElement]] = field(default_factory=list)  # References to other instances that can be found within this instance (e.g. the observations conta...
    versionReference: Optional[str] = None  # A reference to the key of a specific version of an instance in this instance.

@dataclass
class ExampleScenarioInstanceVersion:
    """
    ExampleScenarioInstanceVersion nested class.
    """

    key: Optional[str] = None  # A unique string within the instance that is used to reference the version of the instance.
    title: Optional[str] = None  # A short descriptive label the version to be used in tables or diagrams.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # An explanation of what this specific version of the instance contains and represents.
    content: Optional[Reference] = None  # Points to an instance (typically an example) that shows the data that would flow at this point in...

@dataclass
class ExampleScenarioInstanceContainedInstance:
    """
    ExampleScenarioInstanceContainedInstance nested class.
    """

    instanceReference: Optional[str] = None  # A reference to the key of an instance found within this one.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    versionReference: Optional[str] = None  # A reference to the key of a specific version of an instance in this instance.

@dataclass
class ExampleScenarioProcess:
    """
    ExampleScenarioProcess nested class.
    """

    title: Optional[str] = None  # A short descriptive label the process to be used in tables or diagrams.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # An explanation of what the process represents and what it does.
    preConditions: Optional[str] = None  # Description of the initial state of the actors, environment and data before the process starts.
    postConditions: Optional[str] = None  # Description of the final state of the actors, environment and data after the process has been suc...
    step: Optional[List[BackboneElement]] = field(default_factory=list)  # A significant action that occurs as part of the process.
    number: Optional[str] = None  # The sequential number of the step, e.g. 1.2.5.
    process: Optional[Any] = None  # Indicates that the step is a complex sub-process with its own steps.
    workflow: Optional[str] = None  # Indicates that the step is defined by a seaparate scenario instance.
    operation: Optional[BackboneElement] = None  # The step represents a single operation invoked on receiver by sender.
    type: Optional[Coding] = None  # The standardized type of action (FHIR or otherwise).
    initiator: Optional[str] = None  # The system that invokes the action/transmits the data.
    receiver: Optional[str] = None  # The system on which the action is invoked/receives the data.
    initiatorActive: Optional[bool] = None  # If false, the initiator is deactivated right after the operation.
    receiverActive: Optional[bool] = None  # If false, the receiver is deactivated right after the operation.
    request: Optional[Any] = None  # A reference to the instance that is transmitted from requester to receiver as part of the invocat...
    response: Optional[Any] = None  # A reference to the instance that is transmitted from receiver to requester as part of the operati...
    alternative: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates an alternative step that can be taken instead of the sub-process, scenario or operation...
    pause: Optional[bool] = None  # If true, indicates that, following this step, there is a pause in the flow and the subsequent ste...

@dataclass
class ExampleScenarioProcessStep:
    """
    ExampleScenarioProcessStep nested class.
    """

    title: Optional[str] = None  # A short descriptive label the step to be used in tables or diagrams.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    number: Optional[str] = None  # The sequential number of the step, e.g. 1.2.5.
    process: Optional[Any] = None  # Indicates that the step is a complex sub-process with its own steps.
    workflow: Optional[str] = None  # Indicates that the step is defined by a seaparate scenario instance.
    operation: Optional[BackboneElement] = None  # The step represents a single operation invoked on receiver by sender.
    type: Optional[Coding] = None  # The standardized type of action (FHIR or otherwise).
    initiator: Optional[str] = None  # The system that invokes the action/transmits the data.
    receiver: Optional[str] = None  # The system on which the action is invoked/receives the data.
    description: Optional[str] = None  # An explanation of what the operation represents and what it does.
    initiatorActive: Optional[bool] = None  # If false, the initiator is deactivated right after the operation.
    receiverActive: Optional[bool] = None  # If false, the receiver is deactivated right after the operation.
    request: Optional[Any] = None  # A reference to the instance that is transmitted from requester to receiver as part of the invocat...
    response: Optional[Any] = None  # A reference to the instance that is transmitted from receiver to requester as part of the operati...
    alternative: Optional[List[BackboneElement]] = field(default_factory=list)  # Indicates an alternative step that can be taken instead of the sub-process, scenario or operation...
    step: Optional[List[Any]] = field(default_factory=list)  # Indicates the operation, sub-process or scenario that happens if the alternative option is selected.
    pause: Optional[bool] = None  # If true, indicates that, following this step, there is a pause in the flow and the subsequent ste...

@dataclass
class ExampleScenarioProcessStepOperation:
    """
    ExampleScenarioProcessStepOperation nested class.
    """

    title: Optional[str] = None  # A short descriptive label the step to be used in tables or diagrams.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    type: Optional[Coding] = None  # The standardized type of action (FHIR or otherwise).
    initiator: Optional[str] = None  # The system that invokes the action/transmits the data.
    receiver: Optional[str] = None  # The system on which the action is invoked/receives the data.
    description: Optional[str] = None  # An explanation of what the operation represents and what it does.
    initiatorActive: Optional[bool] = None  # If false, the initiator is deactivated right after the operation.
    receiverActive: Optional[bool] = None  # If false, the receiver is deactivated right after the operation.
    request: Optional[Any] = None  # A reference to the instance that is transmitted from requester to receiver as part of the invocat...
    response: Optional[Any] = None  # A reference to the instance that is transmitted from receiver to requester as part of the operati...

@dataclass
class ExampleScenarioProcessStepAlternative:
    """
    ExampleScenarioProcessStepAlternative nested class.
    """

    title: Optional[str] = None  # The label to display for the alternative that gives a sense of the circumstance in which the alte...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    description: Optional[str] = None  # A human-readable description of the alternative explaining when the alternative should occur rath...
    step: Optional[List[Any]] = field(default_factory=list)  # Indicates the operation, sub-process or scenario that happens if the alternative option is selected.


@dataclass
class ExampleScenario(FHIRResource):
    """
    A walkthrough of a workflow showing the interaction between systems and the instances shared, possibly including the evolution of instances over time.
    """

    status: Optional[str] = None  # The status of this example scenario. Enables tracking the life-cycle of the content.
    resourceType: str = "ExampleScenario"
    url: Optional[str] = None  # An absolute URI that is used to identify this example scenario when it is referenced in a specifi...
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this example scenario when it is represented in othe...
    version: Optional[str] = None  # The identifier that is used to identify this version of the example scenario when it is reference...
    versionAlgorithm: Optional[Any] = None  # Indicates the mechanism used to compare versions to determine which is more current.
    name: Optional[str] = None  # Temporarily retained for tooling purposes.
    title: Optional[str] = None  # A short, descriptive, user-friendly title for the ExampleScenario.
    experimental: Optional[bool] = None  # A Boolean value to indicate that this example scenario is authored for testing purposes (or educa...
    date: Optional[str] = None  # The date  (and optionally time) when the example scenario was last significantly changed. The dat...
    publisher: Optional[str] = None  # The name of the organization or individual responsible for the release and ongoing maintenance of...
    contact: Optional[List[ContactDetail]] = field(default_factory=list)  # Contact details to assist a user in finding and communicating with the publisher.
    description: Optional[str] = None  # A free text natural language description of the ExampleScenario from a consumer's perspective.
    useContext: Optional[List[UsageContext]] = field(default_factory=list)  # The content was developed with a focus and intent of supporting the contexts that are listed. The...
    jurisdiction: Optional[List[CodeableConcept]] = field(default_factory=list)  # A legal or geographic region in which the example scenario is intended to be used.
    purpose: Optional[str] = None  # What the example scenario resource is created for. This should not be used to show the business p...
    copyright: Optional[str] = None  # A copyright statement relating to the example scenario and/or its contents. Copyright statements ...
    copyrightLabel: Optional[str] = None  # A short string (<50 characters), suitable for inclusion in a page footer that identifies the copy...
    actor: Optional[List[BackboneElement]] = field(default_factory=list)  # A system or person who shares or receives an instance within the scenario.
    instance: Optional[List[BackboneElement]] = field(default_factory=list)  # A single data collection that is shared as part of the scenario.
    process: Optional[List[BackboneElement]] = field(default_factory=list)  # A group of operations that represents a significant step within a scenario.