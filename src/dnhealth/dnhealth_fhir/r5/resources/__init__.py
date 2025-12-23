# Copyright 2025 DNAi inc.
#
# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""FHIR R5 resource definitions."""

# Auto-generated exports for R5 resources

from dnhealth.dnhealth_fhir.r5.resources.account import Account
from dnhealth.dnhealth_fhir.r5.resources.activity_definition import ActivityDefinition
from dnhealth.dnhealth_fhir.r5.resources.actor_definition import ActorDefinition
from dnhealth.dnhealth_fhir.r5.resources.administrable_product_definition import AdministrableProductDefinition
from dnhealth.dnhealth_fhir.r5.resources.adverse_event import AdverseEvent
from dnhealth.dnhealth_fhir.r5.resources.allergy_intolerance import AllergyIntolerance
from dnhealth.dnhealth_fhir.r5.resources.appointment import Appointment
from dnhealth.dnhealth_fhir.r5.resources.appointment_response import AppointmentResponse
from dnhealth.dnhealth_fhir.r5.resources.artifact_assessment import ArtifactAssessment
from dnhealth.dnhealth_fhir.r5.resources.audit_event import AuditEvent
from dnhealth.dnhealth_fhir.r5.resources.basic import Basic
from dnhealth.dnhealth_fhir.r5.resources.binary import Binary
from dnhealth.dnhealth_fhir.r5.resources.biologically_derived_product import BiologicallyDerivedProduct
from dnhealth.dnhealth_fhir.r5.resources.biologically_derived_product_dispense import BiologicallyDerivedProductDispense
from dnhealth.dnhealth_fhir.r5.resources.body_structure import BodyStructure
from dnhealth.dnhealth_fhir.r5.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.r5.resources.canonical_resource import CanonicalResource
from dnhealth.dnhealth_fhir.r5.resources.capability_statement import CapabilityStatement
from dnhealth.dnhealth_fhir.r5.resources.care_plan import CarePlan
from dnhealth.dnhealth_fhir.r5.resources.care_team import CareTeam
from dnhealth.dnhealth_fhir.r5.resources.charge_item import ChargeItem
from dnhealth.dnhealth_fhir.r5.resources.charge_item_definition import ChargeItemDefinition
from dnhealth.dnhealth_fhir.r5.resources.citation import Citation
from dnhealth.dnhealth_fhir.r5.resources.claim import Claim
from dnhealth.dnhealth_fhir.r5.resources.claim_response import ClaimResponse
from dnhealth.dnhealth_fhir.r5.resources.clinical_impression import ClinicalImpression
from dnhealth.dnhealth_fhir.r5.resources.clinical_use_definition import ClinicalUseDefinition
from dnhealth.dnhealth_fhir.r5.resources.code_system import CodeSystem
from dnhealth.dnhealth_fhir.r5.resources.communication import Communication
from dnhealth.dnhealth_fhir.r5.resources.communication_request import CommunicationRequest
from dnhealth.dnhealth_fhir.r5.resources.compartment_definition import CompartmentDefinition
from dnhealth.dnhealth_fhir.r5.resources.composition import Composition
from dnhealth.dnhealth_fhir.r5.resources.concept_map import ConceptMap
from dnhealth.dnhealth_fhir.r5.resources.condition import Condition
from dnhealth.dnhealth_fhir.r5.resources.condition_definition import ConditionDefinition
from dnhealth.dnhealth_fhir.r5.resources.consent import Consent
from dnhealth.dnhealth_fhir.r5.resources.contract import Contract
from dnhealth.dnhealth_fhir.r5.resources.coverage import Coverage
from dnhealth.dnhealth_fhir.r5.resources.coverage_eligibility_request import CoverageEligibilityRequest
from dnhealth.dnhealth_fhir.r5.resources.coverage_eligibility_response import CoverageEligibilityResponse
from dnhealth.dnhealth_fhir.r5.resources.detected_issue import DetectedIssue
from dnhealth.dnhealth_fhir.r5.resources.device import Device
from dnhealth.dnhealth_fhir.r5.resources.device_association import DeviceAssociation
from dnhealth.dnhealth_fhir.r5.resources.device_definition import DeviceDefinition
from dnhealth.dnhealth_fhir.r5.resources.device_dispense import DeviceDispense
from dnhealth.dnhealth_fhir.r5.resources.device_metric import DeviceMetric
from dnhealth.dnhealth_fhir.r5.resources.device_request import DeviceRequest
from dnhealth.dnhealth_fhir.r5.resources.device_usage import DeviceUsage
from dnhealth.dnhealth_fhir.r5.resources.diagnostic_report import DiagnosticReport
from dnhealth.dnhealth_fhir.r5.resources.document_reference import DocumentReference
from dnhealth.dnhealth_fhir.r5.resources.domain_resource import DomainResource
from dnhealth.dnhealth_fhir.r5.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.r5.resources.encounter_history import EncounterHistory
from dnhealth.dnhealth_fhir.r5.resources.endpoint import Endpoint
from dnhealth.dnhealth_fhir.r5.resources.enrollment_request import EnrollmentRequest
from dnhealth.dnhealth_fhir.r5.resources.enrollment_response import EnrollmentResponse
from dnhealth.dnhealth_fhir.r5.resources.episode_of_care import EpisodeOfCare
from dnhealth.dnhealth_fhir.r5.resources.event_definition import EventDefinition
from dnhealth.dnhealth_fhir.r5.resources.evidence import Evidence
from dnhealth.dnhealth_fhir.r5.resources.evidence_report import EvidenceReport
from dnhealth.dnhealth_fhir.r5.resources.evidence_variable import EvidenceVariable
from dnhealth.dnhealth_fhir.r5.resources.example_scenario import ExampleScenario
from dnhealth.dnhealth_fhir.r5.resources.explanation_of_benefit import ExplanationOfBenefit
from dnhealth.dnhealth_fhir.r5.resources.family_member_history import FamilyMemberHistory
from dnhealth.dnhealth_fhir.r5.resources.flag import Flag
from dnhealth.dnhealth_fhir.r5.resources.formulary_item import FormularyItem
from dnhealth.dnhealth_fhir.r5.resources.genomic_study import GenomicStudy
from dnhealth.dnhealth_fhir.r5.resources.goal import Goal
from dnhealth.dnhealth_fhir.r5.resources.graph_definition import GraphDefinition
from dnhealth.dnhealth_fhir.r5.resources.group import Group
from dnhealth.dnhealth_fhir.r5.resources.guidance_response import GuidanceResponse
from dnhealth.dnhealth_fhir.r5.resources.healthcare_service import HealthcareService
from dnhealth.dnhealth_fhir.r5.resources.imaging_selection import ImagingSelection
from dnhealth.dnhealth_fhir.r5.resources.imaging_study import ImagingStudy
from dnhealth.dnhealth_fhir.r5.resources.immunization import Immunization
from dnhealth.dnhealth_fhir.r5.resources.immunization_evaluation import ImmunizationEvaluation
from dnhealth.dnhealth_fhir.r5.resources.immunization_recommendation import ImmunizationRecommendation
from dnhealth.dnhealth_fhir.r5.resources.implementation_guide import ImplementationGuide
from dnhealth.dnhealth_fhir.r5.resources.ingredient import Ingredient
from dnhealth.dnhealth_fhir.r5.resources.insurance_plan import InsurancePlan
from dnhealth.dnhealth_fhir.r5.resources.inventory_item import InventoryItem
from dnhealth.dnhealth_fhir.r5.resources.inventory_report import InventoryReport
from dnhealth.dnhealth_fhir.r5.resources.invoice import Invoice
from dnhealth.dnhealth_fhir.r5.resources.library import Library
from dnhealth.dnhealth_fhir.r5.resources.linkage import Linkage
from dnhealth.dnhealth_fhir.r5.resources.list import List
from dnhealth.dnhealth_fhir.r5.resources.location import Location
from dnhealth.dnhealth_fhir.r5.resources.manufactured_item_definition import ManufacturedItemDefinition
from dnhealth.dnhealth_fhir.r5.resources.measure import Measure
from dnhealth.dnhealth_fhir.r5.resources.measure_report import MeasureReport
from dnhealth.dnhealth_fhir.r5.resources.medication import Medication
from dnhealth.dnhealth_fhir.r5.resources.medication_administration import MedicationAdministration
from dnhealth.dnhealth_fhir.r5.resources.medication_dispense import MedicationDispense
from dnhealth.dnhealth_fhir.r5.resources.medication_knowledge import MedicationKnowledge
from dnhealth.dnhealth_fhir.r5.resources.medication_request import MedicationRequest
from dnhealth.dnhealth_fhir.r5.resources.medication_statement import MedicationStatement
from dnhealth.dnhealth_fhir.r5.resources.medicinal_product_definition import MedicinalProductDefinition
from dnhealth.dnhealth_fhir.r5.resources.message_definition import MessageDefinition
from dnhealth.dnhealth_fhir.r5.resources.message_header import MessageHeader
from dnhealth.dnhealth_fhir.r5.resources.metadata_resource import MetadataResource
from dnhealth.dnhealth_fhir.r5.resources.molecular_sequence import MolecularSequence
from dnhealth.dnhealth_fhir.r5.resources.naming_system import NamingSystem
from dnhealth.dnhealth_fhir.r5.resources.nutrition_intake import NutritionIntake
from dnhealth.dnhealth_fhir.r5.resources.nutrition_order import NutritionOrder
from dnhealth.dnhealth_fhir.r5.resources.nutrition_product import NutritionProduct
from dnhealth.dnhealth_fhir.r5.resources.observation import Observation
from dnhealth.dnhealth_fhir.r5.resources.observation_definition import ObservationDefinition
from dnhealth.dnhealth_fhir.r5.resources.operation_definition import OperationDefinition
from dnhealth.dnhealth_fhir.r5.resources.operation_outcome import OperationOutcome
from dnhealth.dnhealth_fhir.r5.resources.organization import Organization
from dnhealth.dnhealth_fhir.r5.resources.organization_affiliation import OrganizationAffiliation
from dnhealth.dnhealth_fhir.r5.resources.packaged_product_definition import PackagedProductDefinition
from dnhealth.dnhealth_fhir.r5.resources.parameters import Parameters
from dnhealth.dnhealth_fhir.r5.resources.patient import Patient
from dnhealth.dnhealth_fhir.r5.resources.payment_notice import PaymentNotice
from dnhealth.dnhealth_fhir.r5.resources.payment_reconciliation import PaymentReconciliation
from dnhealth.dnhealth_fhir.r5.resources.permission import Permission
from dnhealth.dnhealth_fhir.r5.resources.person import Person
from dnhealth.dnhealth_fhir.r5.resources.plan_definition import PlanDefinition
from dnhealth.dnhealth_fhir.r5.resources.practitioner import Practitioner
from dnhealth.dnhealth_fhir.r5.resources.practitioner_role import PractitionerRole
from dnhealth.dnhealth_fhir.r5.resources.procedure import Procedure
from dnhealth.dnhealth_fhir.r5.resources.provenance import Provenance
from dnhealth.dnhealth_fhir.r5.resources.questionnaire import Questionnaire
from dnhealth.dnhealth_fhir.r5.resources.questionnaire_response import QuestionnaireResponse
from dnhealth.dnhealth_fhir.r5.resources.regulated_authorization import RegulatedAuthorization
from dnhealth.dnhealth_fhir.r5.resources.related_person import RelatedPerson
from dnhealth.dnhealth_fhir.r5.resources.request_orchestration import RequestOrchestration
from dnhealth.dnhealth_fhir.r5.resources.requirements import Requirements
from dnhealth.dnhealth_fhir.r5.resources.research_study import ResearchStudy
from dnhealth.dnhealth_fhir.r5.resources.research_subject import ResearchSubject
from dnhealth.dnhealth_fhir.r5.resources.resource import Resource
from dnhealth.dnhealth_fhir.r5.resources.risk_assessment import RiskAssessment
from dnhealth.dnhealth_fhir.r5.resources.schedule import Schedule
from dnhealth.dnhealth_fhir.r5.resources.search_parameter import SearchParameter
from dnhealth.dnhealth_fhir.r5.resources.service_request import ServiceRequest
from dnhealth.dnhealth_fhir.r5.resources.slot import Slot
from dnhealth.dnhealth_fhir.r5.resources.specimen import Specimen
from dnhealth.dnhealth_fhir.r5.resources.specimen_definition import SpecimenDefinition
from dnhealth.dnhealth_fhir.r5.resources.structure_definition import StructureDefinition
from dnhealth.dnhealth_fhir.r5.resources.structure_map import StructureMap
from dnhealth.dnhealth_fhir.r5.resources.subscription import Subscription
from dnhealth.dnhealth_fhir.r5.resources.subscription_status import SubscriptionStatus
from dnhealth.dnhealth_fhir.r5.resources.subscription_topic import SubscriptionTopic
from dnhealth.dnhealth_fhir.r5.resources.substance import Substance
from dnhealth.dnhealth_fhir.r5.resources.substance_definition import SubstanceDefinition
from dnhealth.dnhealth_fhir.r5.resources.substance_nucleic_acid import SubstanceNucleicAcid
from dnhealth.dnhealth_fhir.r5.resources.substance_polymer import SubstancePolymer
from dnhealth.dnhealth_fhir.r5.resources.substance_protein import SubstanceProtein
from dnhealth.dnhealth_fhir.r5.resources.substance_reference_information import SubstanceReferenceInformation
from dnhealth.dnhealth_fhir.r5.resources.substance_source_material import SubstanceSourceMaterial
from dnhealth.dnhealth_fhir.r5.resources.supply_delivery import SupplyDelivery
from dnhealth.dnhealth_fhir.r5.resources.supply_request import SupplyRequest
from dnhealth.dnhealth_fhir.r5.resources.task import Task
from dnhealth.dnhealth_fhir.r5.resources.terminology_capabilities import TerminologyCapabilities
from dnhealth.dnhealth_fhir.r5.resources.test_plan import TestPlan
from dnhealth.dnhealth_fhir.r5.resources.test_report import TestReport
from dnhealth.dnhealth_fhir.r5.resources.test_script import TestScript
from dnhealth.dnhealth_fhir.r5.resources.transport import Transport
from dnhealth.dnhealth_fhir.r5.resources.value_set import ValueSet
from dnhealth.dnhealth_fhir.r5.resources.verification_result import VerificationResult
from dnhealth.dnhealth_fhir.r5.resources.vision_prescription import VisionPrescription

__all__ = [
    "Account",
    "ActivityDefinition",
    "ActorDefinition",
    "AdministrableProductDefinition",
    "AdverseEvent",
    "AllergyIntolerance",
    "Appointment",
    "AppointmentResponse",
    "ArtifactAssessment",
    "AuditEvent",
    "Basic",
    "Binary",
    "BiologicallyDerivedProduct",
    "BiologicallyDerivedProductDispense",
    "BodyStructure",
    "Bundle",
    "CanonicalResource",
    "CapabilityStatement",
    "CarePlan",
    "CareTeam",
    "ChargeItem",
    "ChargeItemDefinition",
    "Citation",
    "Claim",
    "ClaimResponse",
    "ClinicalImpression",
    "ClinicalUseDefinition",
    "CodeSystem",
    "Communication",
    "CommunicationRequest",
    "CompartmentDefinition",
    "Composition",
    "ConceptMap",
    "Condition",
    "ConditionDefinition",
    "Consent",
    "Contract",
    "Coverage",
    "CoverageEligibilityRequest",
    "CoverageEligibilityResponse",
    "DetectedIssue",
    "Device",
    "DeviceAssociation",
    "DeviceDefinition",
    "DeviceDispense",
    "DeviceMetric",
    "DeviceRequest",
    "DeviceUsage",
    "DiagnosticReport",
    "DocumentReference",
    "DomainResource",
    "Encounter",
    "EncounterHistory",
    "Endpoint",
    "EnrollmentRequest",
    "EnrollmentResponse",
    "EpisodeOfCare",
    "EventDefinition",
    "Evidence",
    "EvidenceReport",
    "EvidenceVariable",
    "ExampleScenario",
    "ExplanationOfBenefit",
    "FamilyMemberHistory",
    "Flag",
    "FormularyItem",
    "GenomicStudy",
    "Goal",
    "GraphDefinition",
    "Group",
    "GuidanceResponse",
    "HealthcareService",
    "ImagingSelection",
    "ImagingStudy",
    "Immunization",
    "ImmunizationEvaluation",
    "ImmunizationRecommendation",
    "ImplementationGuide",
    "Ingredient",
    "InsurancePlan",
    "InventoryItem",
    "InventoryReport",
    "Invoice",
    "Library",
    "Linkage",
    "List",
    "Location",
    "ManufacturedItemDefinition",
    "Measure",
    "MeasureReport",
    "Medication",
    "MedicationAdministration",
    "MedicationDispense",
    "MedicationKnowledge",
    "MedicationRequest",
    "MedicationStatement",
    "MedicinalProductDefinition",
    "MessageDefinition",
    "MessageHeader",
    "MetadataResource",
    "MolecularSequence",
    "NamingSystem",
    "NutritionIntake",
    "NutritionOrder",
    "NutritionProduct",
    "Observation",
    "ObservationDefinition",
    "OperationDefinition",
    "OperationOutcome",
    "Organization",
    "OrganizationAffiliation",
    "PackagedProductDefinition",
    "Parameters",
    "Patient",
    "PaymentNotice",
    "PaymentReconciliation",
    "Permission",
    "Person",
    "PlanDefinition",
    "Practitioner",
    "PractitionerRole",
    "Procedure",
    "Provenance",
    "Questionnaire",
    "QuestionnaireResponse",
    "RegulatedAuthorization",
    "RelatedPerson",
    "RequestOrchestration",
    "Requirements",
    "ResearchStudy",
    "ResearchSubject",
    "Resource",
    "RiskAssessment",
    "Schedule",
    "SearchParameter",
    "ServiceRequest",
    "Slot",
    "Specimen",
    "SpecimenDefinition",
    "StructureDefinition",
    "StructureMap",
    "Subscription",
    "SubscriptionStatus",
    "SubscriptionTopic",
    "Substance",
    "SubstanceDefinition",
    "SubstanceNucleicAcid",
    "SubstancePolymer",
    "SubstanceProtein",
    "SubstanceReferenceInformation",
    "SubstanceSourceMaterial",
    "SupplyDelivery",
    "SupplyRequest",
    "Task",
    "TerminologyCapabilities",
    "TestPlan",
    "TestReport",
    "TestScript",
    "Transport",
    "ValueSet",
    "VerificationResult",
    "VisionPrescription",
]
