# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 workflow execution engine.

Provides functionality to execute FHIR workflow resources including PlanDefinition,
ActivityDefinition, and RequestGroup according to the FHIR Workflow specification.
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.activitydefinition import ActivityDefinition
from dnhealth.dnhealth_fhir.resources.plandefinition import (
    PlanDefinition,
    PlanDefinitionAction,
    PlanDefinitionActionCondition,
)
from dnhealth.dnhealth_fhir.resources.requestgroup import (
    RequestGroup,
    RequestGroupAction,
    RequestGroupActionCondition,
)
from dnhealth.dnhealth_fhir.resources.task import Task
from dnhealth.dnhealth_fhir.resources.servicerequest import ServiceRequest
from dnhealth.dnhealth_fhir.resources.medicationrequest import MedicationRequest
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.types import Reference, CodeableConcept

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class WorkflowEngine:
    """
    Execute FHIR workflow resources.
    
    This class provides functionality to:
    - Execute PlanDefinition to generate RequestGroup
    - Execute ActivityDefinition to generate Task
    - Execute RequestGroup to generate Tasks
    - Evaluate conditions using FHIRPath
    - Manage workflow state
    """

    def __init__(self, fhirpath_evaluator: Optional[Any] = None):
        """
        Initialize the workflow engine.
        
        Args:
            fhirpath_evaluator: Optional FHIRPath expression evaluator
        """
        self._fhirpath_evaluator = fhirpath_evaluator
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] WorkflowEngine initialized")

    def execute_plan_definition(        self, plan_definition: PlanDefinition, context: Dict[str, Any]
    ) -> RequestGroup:
        """
        Execute PlanDefinition to generate RequestGroup.
        
        Args:
            plan_definition: PlanDefinition to execute
            context: Execution context (patient, encounter, etc.)
            
        Returns:
            RequestGroup with actions from PlanDefinition
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Executing PlanDefinition: {plan_definition.id or plan_definition.name}"
        )
        
        # Create RequestGroup actions from PlanDefinition actions
        actions = []
        for plan_action in plan_definition.action or []:
            # Evaluate conditions
            if not self.evaluate_conditions(plan_action.condition or [], context):
                continue  # Skip action if conditions not met
            
            # Convert PlanDefinitionAction to RequestGroupAction
            request_action = self._convert_plan_action_to_request_action(plan_action, context)
            if request_action:
                actions.append(request_action)
        
        # Create RequestGroup
        request_group = RequestGroup(
            resourceType="RequestGroup",
            status="draft",
            intent="order",
            priority="routine",
            action=actions,
        )
        
        # Set subject from context if available
        if "subject" in context:
            request_group.subject = context["subject"]
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] PlanDefinition execution "
            f"completed in {elapsed:.3f}s (generated {len(actions)} actions)"
        )

            # Log completion timestamp at end of operation
        
        return request_group

    def execute_activity_definition(
        self, activity_definition: ActivityDefinition, context: Dict[str, Any]
    ) -> Task:
        """
        Execute ActivityDefinition to generate Task.
        
        Args:
            activity_definition: ActivityDefinition to execute
            context: Execution context
            
        Returns:
            Task resource
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Executing ActivityDefinition: "
            f"{activity_definition.id or activity_definition.name}"
        )
        
        # Create Task from ActivityDefinition
        task = Task(
            resourceType="Task",
            status="ready",
            intent="order",
            priority=activity_definition.priority or "routine",
        )
        
        # Set code from ActivityDefinition
        if activity_definition.code:
            # Task doesn't have code field directly, but we can set it in description
            task.description = (
                activity_definition.description
                or activity_definition.title
                or "Task from ActivityDefinition"
            )
        
        # Set subject from context or ActivityDefinition
        if "subject" in context:
            task.for_fhir = context["subject"]
        elif activity_definition.subjectReference:
            task.for_fhir = activity_definition.subjectReference
        
        elapsed = time.time() - start_time
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ActivityDefinition execution "
            f"completed in {elapsed:.3f}s"
        )
        
        return task

    def execute_request_group(self, request_group: RequestGroup) -> List[Task]:
        """
        Execute RequestGroup to generate Tasks.
        
        Args:
            request_group: RequestGroup to execute
            
        Returns:
            List of Task resources
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Executing RequestGroup: {request_group.id or 'unnamed'}"
        )
        
        tasks = []
        context = {
            "subject": request_group.subject,
            "encounter": request_group.encounter,
        }
        
        # Process each action
        for action in request_group.action or []:
            # Evaluate conditions
            if not self.evaluate_conditions(action.condition or [], context):
                continue  # Skip action if conditions not met
            
            # Create Task from action
            task = self._create_task_from_action(action, request_group)
            if task:
                tasks.append(task)
        
        elapsed = time.time() - start_time

            # Log completion timestamp at end of operation
        logger.info(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] RequestGroup execution "
            f"completed in {elapsed:.3f}s (generated {len(tasks)} tasks)"
        )
        
        return tasks

    def evaluate_conditions(
        self, conditions: List[Any], context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate conditions using FHIRPath.
        
        Args:
            conditions: List of condition objects (PlanDefinitionActionCondition or RequestGroupActionCondition)
            context: Execution context
            
        Returns:
            True if all conditions are met, False otherwise
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Evaluating {len(conditions)} conditions")
        
        if not conditions:
            elapsed = time.time() - start_time
            logger.debug(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Condition evaluation "
                f"completed in {elapsed:.3f}s (no conditions, returning True)"
            )
            return True  # No conditions means always applicable
        
        for condition in conditions:
            if not self.evaluate_condition(condition, context):
                elapsed = time.time() - start_time
                logger.debug(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Condition evaluation "
                    f"completed in {elapsed:.3f}s (condition not met, returning False)"
                )
                return False
        
        elapsed = time.time() - start_time
        logger.debug(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Condition evaluation "
            f"completed in {elapsed:.3f}s (all conditions met, returning True)"
        )
        return True

    def evaluate_condition(self, condition: Any, context: Dict[str, Any]) -> bool:
        """
        Evaluate a single condition.
        
        Args:
            condition: Condition object (PlanDefinitionActionCondition or RequestGroupActionCondition)
            context: Execution context
            
        Returns:
            True if condition is met, False otherwise
        """
        # Check condition kind
        if hasattr(condition, "kind"):
            kind = condition.kind
        else:
            return True  # No kind means always applicable
        
        # Evaluate expression if available
        if hasattr(condition, "expression") and condition.expression:
            if self._fhirpath_evaluator:
                try:
                    result = self._fhirpath_evaluator.evaluate(
                        condition.expression, context
                    )
                    # Convert result to boolean
                    if isinstance(result, bool):
                        return result
                    elif isinstance(result, list) and len(result) > 0:
                        # If list, check if any element is truthy
                        return any(result)
                    else:
                        return bool(result)
                except Exception as e:
                    logger.warning(
                        f"Error evaluating condition expression: {e}. "
                        f"Assuming condition is not met."
                    )

                        # Log completion timestamp at end of operation
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logger.info(f"Current Time at End of Operations: {current_time}")
                    return False
            else:
                # No FHIRPath evaluator, assume condition is met if expression exists
                logger.warning(
                    "No FHIRPath evaluator available. Cannot evaluate condition expression."
                )
                return True
        
        # No expression means condition is always applicable
        return True

    def _convert_plan_action_to_request_action(
        self, plan_action: PlanDefinitionAction, context: Dict[str, Any]
    ) -> Optional[RequestGroupAction]:
        """Convert PlanDefinitionAction to RequestGroupAction."""
        from dnhealth.dnhealth_fhir.resources.requestgroup import RequestGroupAction

            # Log completion timestamp at end of operation
        
        return RequestGroupAction(
            id=plan_action.id,
            prefix=plan_action.prefix,
            title=plan_action.title,
            description=plan_action.description,
            textEquivalent=plan_action.textEquivalent,
            priority=plan_action.priority,
            code=plan_action.code,
            timingDateTime=plan_action.timingDateTime,
            timingPeriod=plan_action.timingPeriod,
            timingDuration=plan_action.timingDuration,
            timingRange=plan_action.timingRange,
        )

    def _create_task_from_action(
        self, action: RequestGroupAction, request_group: RequestGroup
    ) -> Optional[Task]:
        """Create Task from RequestGroupAction."""

            # Log completion timestamp at end of operation
        task = Task(
            resourceType="Task",
            status="ready",
            intent="order",
            priority=action.priority or request_group.priority or "routine",
            description=action.description or action.title or "Task from RequestGroup",
        )
        
        # Set subject from RequestGroup
        if request_group.subject:
            task.for_fhir = request_group.subject
        
        # Set resource reference if action has resource
        if action.resource:
            task.focus = action.resource
        
        return task


def execute_action(
    action: PlanDefinitionAction, context: Dict[str, Any]
) -> Optional[FHIRResource]:
    """
    Execute a PlanDefinitionAction.
    
    Args:
        action: PlanDefinitionAction to execute
        context: Execution context
        
    Returns:
        Created resource if action executed, None otherwise
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Executing action: {action.id or action.title}")
    
    # Evaluate conditions
    engine = WorkflowEngine()
    if not engine.evaluate_conditions(action.condition or [], context):
        logger.info(f"[{current_time}] Action conditions not met, skipping")
        return None
    
    # Create appropriate resource based on action type and definition
    created_resource = None
    
    # Get action type from code
    action_type = None
    if action.code:
        for code_concept in action.code:
            if code_concept.coding:
                for coding in code_concept.coding:
                    if coding.code:
                        action_type = coding.code
                        break
                if action_type:
                    break
    
    # Get subject from context
    subject = context.get("subject")
    if not subject and "patient" in context:
        subject = context["patient"]
    
    # Create resource based on action type or definition
    if action.definition:
        # If definition is a reference, try to determine resource type from it
        definition_str = str(action.definition)
        if "ActivityDefinition" in definition_str or "activity-definition" in definition_str.lower():
            # Create ServiceRequest for activity definitions
            created_resource = ServiceRequest(
                resourceType="ServiceRequest",
                status="draft",
                intent="order",
                subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
                code=action.code[0] if action.code else None,
            )
        elif "Medication" in definition_str or "medication" in definition_str.lower():
            # Create MedicationRequest
            created_resource = MedicationRequest(
                resourceType="MedicationRequest",
                status="draft",
                intent="order",
                subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
                medicationCodeableConcept=action.code[0] if action.code else None,
            )
        elif "Observation" in definition_str or "observation" in definition_str.lower():
            # Create Observation
            created_resource = Observation(
                resourceType="Observation",
                status="preliminary",
                subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
                code=action.code[0] if action.code else None,
            )
    elif action_type:
        # Create resource based on action type code
        action_type_lower = action_type.lower()
        if "service" in action_type_lower or "procedure" in action_type_lower:
            created_resource = ServiceRequest(
                resourceType="ServiceRequest",
                status="draft",
                intent="order",
                subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
                code=action.code[0] if action.code else None,
            )
        elif "medication" in action_type_lower or "drug" in action_type_lower:
            created_resource = MedicationRequest(
                resourceType="MedicationRequest",
                status="draft",
                intent="order",
                subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
                medicationCodeableConcept=action.code[0] if action.code else None,
            )
        elif "observation" in action_type_lower or "measurement" in action_type_lower:
            created_resource = Observation(
                resourceType="Observation",
                status="preliminary",
                subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
                code=action.code[0] if action.code else None,
            )
    
    # If no specific resource type determined, create a generic ServiceRequest
    if not created_resource:
        created_resource = ServiceRequest(
            resourceType="ServiceRequest",
            status="draft",
            intent="order",
            subject=subject if isinstance(subject, Reference) else Reference(reference=str(subject)) if subject else None,
            code=action.code[0] if action.code else None,
        )
    
    # Set priority if specified
    if action.priority and hasattr(created_resource, 'priority'):
        created_resource.priority = action.priority
    
    # Set timing if specified
    if action.timingDateTime and hasattr(created_resource, 'occurrenceDateTime'):
        created_resource.occurrenceDateTime = action.timingDateTime
    elif action.timingPeriod and hasattr(created_resource, 'occurrencePeriod'):
        created_resource.occurrencePeriod = action.timingPeriod
    
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        f"[{completion_time}] Action execution "
        f"completed in {elapsed:.3f}s (created {created_resource.resourceType})"
    )
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    return created_resource
