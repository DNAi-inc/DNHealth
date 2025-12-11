# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 clinical reasoning engine.

Provides functionality to evaluate PlanDefinition against patient context,
execute Library logic (CQL, FHIRPath, etc.), and generate GuidanceResponse
according to the FHIR Clinical Reasoning specification.
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.plandefinition import PlanDefinition
from dnhealth.dnhealth_fhir.resources.library import Library
from dnhealth.dnhealth_fhir.resources.guidanceresponse import GuidanceResponse
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.fhirpath import evaluate_fhirpath_expression
from dnhealth.dnhealth_fhir.workflow import WorkflowEngine

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


class ClinicalReasoningEngine:
    """
    Evaluate PlanDefinition against patient context and generate guidance.
    
    This class provides functionality to:
    - Evaluate PlanDefinition against patient context
    - Execute Library logic (CQL, FHIRPath, etc.)
    - Generate GuidanceResponse with recommendations
    """

    def __init__(self, fhirpath_evaluator: Optional[Any] = None, cql_evaluator: Optional[Any] = None):
        """
        Initialize the clinical reasoning engine.
        
        Args:
            fhirpath_evaluator: Optional FHIRPath expression evaluator
            cql_evaluator: Optional CQL expression evaluator
        """
        self._fhirpath_evaluator = fhirpath_evaluator
        self._cql_evaluator = cql_evaluator
        self._libraries: Dict[str, Library] = {}
        self._workflow_engine = WorkflowEngine(fhirpath_evaluator=fhirpath_evaluator)
        self.start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] ClinicalReasoningEngine initialized")

    def load_library(self, library: Library) -> None:
        """
        Load a Library resource for use in clinical reasoning.
        
        Args:
            library: Library resource to load
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        library_id = library.id or library.url or library.name or "unknown"
        self._libraries[library_id] = library
        logger.info(f"[{current_time}] Loaded Library: {library_id}")

    def evaluate_guidance(
        self, plan_definition: PlanDefinition, context: Dict[str, Any]
    ) -> GuidanceResponse:
        """
        Evaluate PlanDefinition against context and generate guidance.
        
        Args:
            plan_definition: PlanDefinition to evaluate
            context: Evaluation context (patient, encounter, etc.)
            
        Returns:
            GuidanceResponse with recommendations
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Evaluating guidance for PlanDefinition: "
            f"{plan_definition.id or plan_definition.name}"
        )
        
        # Extract patient from context
        patient = context.get("patient")
        if not patient:
            # Try to get from subject reference
            if "subject" in context:
                subject = context["subject"]
                if isinstance(subject, Patient):
                    patient = subject
                elif hasattr(subject, "reference") and subject.reference:
                    # Would need to resolve reference in real implementation
                    pass
        
        # Evaluate PlanDefinition actions
        recommendations = []
        applicable_actions = []
        
        for action in plan_definition.action or []:
            # Evaluate conditions using workflow engine
            if self._workflow_engine.evaluate_conditions(action.condition or [], context):
                applicable_actions.append(action)
                # Create recommendation from action
                recommendation = {
                    "action": action,
                    "title": action.title or action.description or "Recommendation",
                    "priority": action.priority or "routine",
                }
                recommendations.append(recommendation)
        
        # Generate GuidanceResponse
        guidance_response = self.generate_guidance_response(
            plan_definition, recommendations, context
        )
        
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{completion_time}] Guidance evaluation "
            f"completed in {elapsed:.3f}s ({len(recommendations)} recommendations)"
        )
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {completion_time}")
        
        return guidance_response

    def apply_plan_definition(
        self,
        plan_definition: PlanDefinition,
        patient: Patient,
        context: Optional[Dict[str, Any]] = None,
    ) -> GuidanceResponse:
        """
        Apply PlanDefinition to a patient and generate guidance.
        
        Args:
            plan_definition: PlanDefinition to apply
            patient: Patient resource
            context: Additional context (encounter, etc.)
            
        Returns:
            GuidanceResponse with recommendations
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{current_time}] Applying PlanDefinition to patient: "
            f"{patient.id or 'unknown'}"
        )
        
        # Build context
        if context is None:
            context = {}
        context["patient"] = patient
        context["subject"] = patient
        
        # Evaluate guidance
        guidance_response = self.evaluate_guidance(plan_definition, context)
        
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{completion_time}] PlanDefinition application "
            f"completed in {elapsed:.3f}s"
        )
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {completion_time}")
        
        return guidance_response

    def evaluate_cql_expression(
        self, expression: str, context: Dict[str, Any]
    ) -> Any:
        """
        Evaluate a CQL expression.
        
        Args:
            expression: CQL expression string
            context: Evaluation context
            
        Returns:
            Evaluation result
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Evaluating CQL expression")
        
        if self._cql_evaluator:
            try:
                result = self._cql_evaluator.evaluate(expression, context)
                elapsed = time.time() - start_time
                completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"[{completion_time}] CQL evaluation "
                    f"completed in {elapsed:.3f}s"
                )
                # Log completion timestamp at end of operation
                logger.info(f"Current Time at End of Operations: {completion_time}")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(f"[{completion_time}] CQL evaluation error: {e}")
                logger.info(f"Current Time at End of Operations: {completion_time}")
                raise
        else:
            logger.warning(
                f"[{current_time}] No CQL evaluator available. "
                f"CQL evaluation requires external library."
            )
            # Fallback: try to evaluate as FHIRPath if possible
            if self._fhirpath_evaluator:
                try:
                    result = evaluate_fhirpath_expression(
                        expression, context.get("patient"), context
                    )
                    elapsed = time.time() - start_time
                    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(
                        f"[{completion_time}] CQL expression "
                        f"evaluated as FHIRPath in {elapsed:.3f}s"
                    )
                    # Log completion timestamp at end of operation
                    logger.info(f"Current Time at End of Operations: {completion_time}")
                    return result
                except Exception as e:
                    elapsed = time.time() - start_time
                    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.warning(
                        f"[{completion_time}] Failed to evaluate as FHIRPath: {e}"
                    )
                    logger.info(f"Current Time at End of Operations: {completion_time}")
            
            elapsed = time.time() - start_time
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {completion_time}")
            raise ValueError("No CQL evaluator available and FHIRPath fallback failed")

    def generate_guidance_response(
        self,
        plan_definition: PlanDefinition,
        recommendations: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> GuidanceResponse:
        """
        Generate GuidanceResponse from PlanDefinition and recommendations.
        
        Args:
            plan_definition: PlanDefinition that was evaluated
            recommendations: List of recommendation dictionaries
            context: Evaluation context
            
        Returns:
            GuidanceResponse resource
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Generating GuidanceResponse")
        
        # Determine status based on recommendations
        if recommendations:
            status = "success"
        else:
            status = "data-required"  # No recommendations might mean more data needed
        
        # Create GuidanceResponse
        guidance_response = GuidanceResponse(
            resourceType="GuidanceResponse",
            status=status,
            moduleCanonical=plan_definition.url,
            subject=context.get("subject"),
            encounter=context.get("encounter"),
            occurrenceDateTime=datetime.now().isoformat(),
        )
        
        # Add recommendations as output parameters or result
        # In a full implementation, this would create Parameters resource
        # with recommendations as output parameters
        
        elapsed = time.time() - start_time
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"[{completion_time}] GuidanceResponse generation "
            f"completed in {elapsed:.3f}s"
        )
        # Log completion timestamp at end of operation
        logger.info(f"Current Time at End of Operations: {completion_time}")
        
        return guidance_response


def evaluate_cql(cql_expression: str, context: Dict[str, Any]) -> Any:
    """
    Evaluate a CQL (Clinical Quality Language) expression.
    
    This function provides a standalone interface for CQL evaluation.
    For full CQL evaluation capabilities, an external library (e.g., cql-execution)
    is required. This implementation raises NotImplementedError to indicate that
    a CQL evaluator must be provided.
    
    To use CQL evaluation:
    1. Install a CQL execution library (e.g., cql-execution)
    2. Create a ClinicalReasoningEngine instance with a CQL evaluator:
       engine = ClinicalReasoningEngine(cql_evaluator=your_cql_evaluator)
    3. Use engine.evaluate_cql_expression() instead of this standalone function
    
    Args:
        cql_expression: CQL expression string to evaluate
        context: Evaluation context containing FHIR resources and variables
        
    Returns:
        Evaluation result (type depends on CQL expression)
        
    Raises:
        NotImplementedError: Always raised, as this function requires an external
            CQL execution library. Use ClinicalReasoningEngine with a CQL evaluator
            for actual CQL evaluation.
    """
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Evaluating CQL expression")
    
    # Full CQL evaluation requires an external library such as:
    # - cql-execution (Python CQL execution engine)
    # - cql-execution-java (Java-based CQL execution)
    # 
    # Example usage with external library:
    #     from cql_execution import evaluate
    #     return evaluate(cql_expression, context)
    #
    # For now, this function serves as a placeholder that demonstrates
    # the expected interface and provides clear error messaging.
    
    # Log completion timestamp at end of operation before raising error
    elapsed = time.time() - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.warning(
        f"[{completion_time}] CQL evaluation operation completed in {elapsed:.3f}s - "
        f"CQL evaluator not available (requires external library)"
    )
    logger.info(f"Current Time at End of Operations: {completion_time}")
    
    raise NotImplementedError(
        "CQL evaluation requires external library (e.g., cql-execution). "
        "Please install cql-execution or provide CQL evaluator to ClinicalReasoningEngine. "
        "Alternatively, use ClinicalReasoningEngine.evaluate_cql_expression() with a "
        "CQL evaluator instance."
    )
