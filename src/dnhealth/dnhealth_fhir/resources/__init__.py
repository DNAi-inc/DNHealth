# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""FHIR R4 resource definitions."""

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.binary import Binary
from dnhealth.dnhealth_fhir.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.resources.capabilitystatement import (
    CapabilityStatement,
    CapabilityStatementSoftware,
    CapabilityStatementImplementation,
    CapabilityStatementRest,
    CapabilityStatementRestResource
)
from dnhealth.dnhealth_fhir.resources.codesystem import (
    CodeSystem,
    CodeSystemConcept,
    CodeSystemConceptDesignation,
    CodeSystemConceptProperty,
    CodeSystemFilter,
    CodeSystemProperty,
    get_codes_from_codesystem,
)
from dnhealth.dnhealth_fhir.resources.conceptmap import (
    ConceptMap,
    ConceptMapGroup,
    ConceptMapGroupElement,
    ConceptMapGroupElementTarget,
    ConceptMapGroupElementTargetDependsOn,
    ConceptMapGroupUnmapped,
    translate_code,
)
from dnhealth.dnhealth_fhir.resources.condition import Condition
from dnhealth.dnhealth_fhir.resources.graphdefinition import (
    GraphDefinition,
    GraphDefinitionLink,
    GraphDefinitionLinkTarget
)
from dnhealth.dnhealth_fhir.resources.implementationguide import (
    ImplementationGuide,
    ImplementationGuideDependsOn,
    ImplementationGuideGlobal,
    ImplementationGuideDefinition,
    ImplementationGuideManifest
)
from dnhealth.dnhealth_fhir.resources.messagedefinition import (
    MessageDefinition,
    MessageDefinitionFocus,
    MessageDefinitionAllowedResponse
)
from dnhealth.dnhealth_fhir.resources.operationdefinition import (
    OperationDefinition,
    OperationDefinitionParameter,
    OperationDefinitionOverload
)
from dnhealth.dnhealth_fhir.resources.searchparameter import (
    SearchParameter as SearchParameterResource,
    SearchParameterComponent
)
from dnhealth.dnhealth_fhir.resources.structuredefinition import (
    StructureDefinition,
    StructureDefinitionSnapshot,
    StructureDefinitionDifferential,
    StructureDefinitionMapping,
    StructureDefinitionContext,
    ElementDefinition,
)
from dnhealth.dnhealth_fhir.resources.structuremap import (
    StructureMap,
    StructureMapStructure,
    StructureMapGroup
)
from dnhealth.dnhealth_fhir.resources.terminologycapabilities import (
    TerminologyCapabilities,
    TerminologyCapabilitiesSoftware,
    TerminologyCapabilitiesImplementation,
    TerminologyCapabilitiesCodeSystem,
    TerminologyCapabilitiesExpansion,
    TerminologyCapabilitiesValidateCode,
    TerminologyCapabilitiesTranslation,
    TerminologyCapabilitiesClosure
)
from dnhealth.dnhealth_fhir.resources.account import (
    Account,
    AccountCoverage,
    AccountGuarantor
)
from dnhealth.dnhealth_fhir.resources.activitydefinition import (
    ActivityDefinition,
    ActivityDefinitionParticipant,
    ActivityDefinitionDynamicValue
)
from dnhealth.dnhealth_fhir.resources.adverseevent import (
    AdverseEvent,
    AdverseEventSuspectEntity
)
from dnhealth.dnhealth_fhir.resources.allergyintolerance import (
    AllergyIntolerance,
    AllergyIntoleranceReaction
)
from dnhealth.dnhealth_fhir.resources.basic import Basic
from dnhealth.dnhealth_fhir.resources.biologicallyderivedproduct import (
    BiologicallyDerivedProduct,
    BiologicallyDerivedProductCollection,
    BiologicallyDerivedProductProcessing,
    BiologicallyDerivedProductManipulation,
    BiologicallyDerivedProductStorage
)
from dnhealth.dnhealth_fhir.resources.bodystructure import BodyStructure
from dnhealth.dnhealth_fhir.resources.careplan import (
    CarePlan,
    CarePlanActivity
)
from dnhealth.dnhealth_fhir.resources.careteam import (
    CareTeam,
    CareTeamParticipant
)
from dnhealth.dnhealth_fhir.resources.catalogentry import (
    CatalogEntry,
    CatalogEntryRelatedEntry
)
from dnhealth.dnhealth_fhir.resources.chargeitem import (
    ChargeItem,
    ChargeItemPerformer
)
from dnhealth.dnhealth_fhir.resources.chargeitemdefinition import (
    ChargeItemDefinition,
    ChargeItemDefinitionApplicability,
    ChargeItemDefinitionPropertyGroup
)
from dnhealth.dnhealth_fhir.resources.claim import (
    Claim,
    ClaimRelated,
    ClaimPayee,
    ClaimCareTeam,
    ClaimSupportingInfo,
    ClaimDiagnosis,
    ClaimProcedure,
    ClaimInsurance,
    ClaimAccident,
    ClaimItem,
    ClaimItemDetail,
    ClaimItemDetailSubDetail
)
from dnhealth.dnhealth_fhir.resources.claimresponse import (
    ClaimResponse,
    ClaimResponseItemAdjudication,
    ClaimResponseItem,
    ClaimResponseItemDetail,
    ClaimResponseItemDetailSubDetail,
    ClaimResponseAddItem,
    ClaimResponseAddItemDetail,
    ClaimResponseAddItemDetailSubDetail,
    ClaimResponseTotal,
    ClaimResponsePayment,
    ClaimResponseProcessNote,
    ClaimResponseInsurance,
    ClaimResponseError
)
from dnhealth.dnhealth_fhir.resources.clinicalimpression import (
    ClinicalImpression,
    ClinicalImpressionInvestigation,
    ClinicalImpressionFinding
)
from dnhealth.dnhealth_fhir.resources.communication import (
    Communication,
    CommunicationPayload
)
from dnhealth.dnhealth_fhir.resources.communicationrequest import (
    CommunicationRequest,
    CommunicationRequestPayload
)
from dnhealth.dnhealth_fhir.resources.compartmentdefinition import (
    CompartmentDefinition,
    CompartmentDefinitionResource
)
from dnhealth.dnhealth_fhir.resources.composition import (
    Composition,
    CompositionAttester,
    CompositionRelatesTo,
    CompositionEvent,
    CompositionSection
)
from dnhealth.dnhealth_fhir.resources.consent import (
    Consent,
    ConsentPolicy,
    ConsentVerification,
    ConsentProvisionActor,
    ConsentProvisionData,
    ConsentProvision
)
from dnhealth.dnhealth_fhir.resources.contract import (
    Contract,
    ContractContentDefinition,
    ContractTermAssetContext,
    ContractTermAssetValuedItem,
    ContractTermAsset,
    ContractTermActionSubject,
    ContractTermAction,
    ContractTerm,
    ContractSigner,
    ContractFriendly,
    ContractLegal
)
from dnhealth.dnhealth_fhir.resources.coverage import (
    Coverage,
    CoverageCostToBeneficiaryException,
    CoverageCostToBeneficiary,
    CoverageClass
)
from dnhealth.dnhealth_fhir.resources.coverageeligibilityrequest import (
    CoverageEligibilityRequest,
    CoverageEligibilityRequestSupportingInfo,
    CoverageEligibilityRequestInsurance,
    CoverageEligibilityRequestItemDiagnosis,
    CoverageEligibilityRequestItem
)
from dnhealth.dnhealth_fhir.resources.coverageeligibilityresponse import (
    CoverageEligibilityResponse,
    CoverageEligibilityResponseInsuranceItemBenefit,
    CoverageEligibilityResponseInsuranceItem,
    CoverageEligibilityResponseInsurance,
    CoverageEligibilityResponseError
)
from dnhealth.dnhealth_fhir.resources.detectedissue import (
    DetectedIssue,
    DetectedIssueMitigation
)
from dnhealth.dnhealth_fhir.resources.device import (
    Device,
    DeviceUdiCarrier,
    DeviceDeviceName,
    DeviceSpecialization,
    DeviceVersion,
    DeviceProperty
)
from dnhealth.dnhealth_fhir.resources.devicedefinition import (
    DeviceDefinition,
    DeviceDefinitionUdiDeviceIdentifier,
    DeviceDefinitionDeviceName,
    DeviceDefinitionSpecialization,
    DeviceDefinitionCapability,
    DeviceDefinitionProperty,
    DeviceDefinitionMaterial
)
from dnhealth.dnhealth_fhir.resources.devicemetric import (
    DeviceMetric,
    DeviceMetricCalibration
)
from dnhealth.dnhealth_fhir.resources.devicerequest import (
    DeviceRequest,
    DeviceRequestParameter
)
from dnhealth.dnhealth_fhir.resources.deviceusestatement import DeviceUseStatement
from dnhealth.dnhealth_fhir.resources.diagnosticreport import (
    DiagnosticReport,
    DiagnosticReportMedia
)
from dnhealth.dnhealth_fhir.resources.documentmanifest import (
    DocumentManifest,
    DocumentManifestRelated
)
from dnhealth.dnhealth_fhir.resources.documentreference import (
    DocumentReference,
    DocumentReferenceRelatesTo,
    DocumentReferenceContent,
    DocumentReferenceContext
)
from dnhealth.dnhealth_fhir.resources.effectevidencesynthesis import (
    EffectEvidenceSynthesis,
    EffectEvidenceSynthesisSampleSize,
    EffectEvidenceSynthesisResultsByExposure,
    EffectEvidenceSynthesisEffectEstimate,
    EffectEvidenceSynthesisEffectEstimatePrecisionEstimate,
    EffectEvidenceSynthesisCertainty,
    EffectEvidenceSynthesisCertaintyCertaintySubcomponent
)
from dnhealth.dnhealth_fhir.resources.appointment import (
    Appointment,
    AppointmentParticipant
)
from dnhealth.dnhealth_fhir.resources.appointmentresponse import AppointmentResponse
from dnhealth.dnhealth_fhir.resources.auditevent import (
    AuditEvent,
    AuditEventAgent,
    AuditEventAgentNetwork,
    AuditEventSource,
    AuditEventEntity,
    AuditEventEntityDetail
)
from dnhealth.dnhealth_fhir.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.resources.endpoint import Endpoint
from dnhealth.dnhealth_fhir.resources.enrollmentrequest import EnrollmentRequest
from dnhealth.dnhealth_fhir.resources.enrollmentresponse import EnrollmentResponse
from dnhealth.dnhealth_fhir.resources.episodeofcare import (
    EpisodeOfCare,
    EpisodeOfCareStatusHistory,
    EpisodeOfCareDiagnosis
)
from dnhealth.dnhealth_fhir.resources.eventdefinition import EventDefinition
from dnhealth.dnhealth_fhir.resources.evidence import Evidence
from dnhealth.dnhealth_fhir.resources.evidencevariable import (
    EvidenceVariable,
    EvidenceVariableCharacteristic
)
from dnhealth.dnhealth_fhir.resources.examplescenario import (
    ExampleScenario,
    ExampleScenarioActor,
    ExampleScenarioInstance,
    ExampleScenarioInstanceVersion,
    ExampleScenarioInstanceContainedInstance,
    ExampleScenarioProcess,
    ExampleScenarioProcessStep,
    ExampleScenarioProcessStepOperation,
    ExampleScenarioProcessStepAlternative
)
from dnhealth.dnhealth_fhir.resources.explanationofbenefit import (
    ExplanationOfBenefit,
    ExplanationOfBenefitRelated,
    ExplanationOfBenefitPayee,
    ExplanationOfBenefitCareTeam,
    ExplanationOfBenefitSupportingInfo,
    ExplanationOfBenefitDiagnosis,
    ExplanationOfBenefitProcedure
)
from dnhealth.dnhealth_fhir.resources.familymemberhistory import (
    FamilyMemberHistory,
    FamilyMemberHistoryCondition
)
from dnhealth.dnhealth_fhir.resources.flag import Flag
from dnhealth.dnhealth_fhir.resources.goal import Goal, GoalTarget
from dnhealth.dnhealth_fhir.resources.group import (
    Group,
    GroupCharacteristic,
    GroupMember
)
from dnhealth.dnhealth_fhir.resources.guidanceresponse import GuidanceResponse
from dnhealth.dnhealth_fhir.resources.healthcareservice import (
    HealthcareService,
    HealthcareServiceEligibility,
    HealthcareServiceAvailableTime,
    HealthcareServiceNotAvailable
)
from dnhealth.dnhealth_fhir.resources.imagingstudy import (
    ImagingStudy,
    ImagingStudySeries,
    ImagingStudySeriesPerformer,
    ImagingStudySeriesInstance
)
from dnhealth.dnhealth_fhir.resources.immunization import (
    Immunization,
    ImmunizationPerformer,
    ImmunizationEducation,
    ImmunizationReaction,
    ImmunizationProtocolApplied
)
from dnhealth.dnhealth_fhir.resources.immunizationevaluation import ImmunizationEvaluation
from dnhealth.dnhealth_fhir.resources.immunizationrecommendation import (
    ImmunizationRecommendation,
    ImmunizationRecommendationRecommendation
)
from dnhealth.dnhealth_fhir.resources.insuranceplan import (
    InsurancePlan,
    InsurancePlanContact,
    InsurancePlanCoverage,
    InsurancePlanCoverageBenefit,
    InsurancePlanCoverageBenefitLimit,
    InsurancePlanPlan,
    InsurancePlanPlanGeneralCost,
    InsurancePlanPlanSpecificCost,
    InsurancePlanPlanSpecificCostBenefit,
    InsurancePlanPlanSpecificCostBenefitCost
)
from dnhealth.dnhealth_fhir.resources.invoice import (
    Invoice,
    InvoiceParticipant,
    InvoiceLineItem,
    InvoiceLineItemPriceComponent
)
from dnhealth.dnhealth_fhir.resources.library import Library
from dnhealth.dnhealth_fhir.resources.linkage import (
    Linkage,
    LinkageItem
)
from dnhealth.dnhealth_fhir.resources.location import (
    Location,
    LocationPosition,
    LocationHoursOfOperation
)
from dnhealth.dnhealth_fhir.resources.list import (
    ListResource,
    ListEntry
)
# Alias for compatibility
List = ListResource
from dnhealth.dnhealth_fhir.resources.media import Media
from dnhealth.dnhealth_fhir.resources.medication import (
    Medication,
    MedicationIngredient,
    MedicationBatch
)
from dnhealth.dnhealth_fhir.resources.medicationadministration import (
    MedicationAdministration,
    MedicationAdministrationPerformer,
    MedicationAdministrationDosage
)
from dnhealth.dnhealth_fhir.resources.medicationdispense import (
    MedicationDispense,
    MedicationDispensePerformer,
    MedicationDispenseSubstitution
)
from dnhealth.dnhealth_fhir.resources.medicationknowledge import (
    MedicationKnowledge,
    MedicationKnowledgeRelatedMedicationKnowledge,
    MedicationKnowledgeMonograph,
    MedicationKnowledgeIngredient,
    MedicationKnowledgeCost,
    MedicationKnowledgeMonitoringProgram,
    MedicationKnowledgeAdministrationGuidelines,
    MedicationKnowledgeMedicineClassification,
    MedicationKnowledgePackaging,
    MedicationKnowledgeDrugCharacteristic,
    MedicationKnowledgeRegulatory,
    MedicationKnowledgeKinetics
)
from dnhealth.dnhealth_fhir.resources.medicationrequest import (
    MedicationRequest,
    MedicationRequestDispenseRequest,
    MedicationRequestDispenseRequestInitialFill,
    MedicationRequestSubstitution
)
from dnhealth.dnhealth_fhir.resources.medicationstatement import MedicationStatement
from dnhealth.dnhealth_fhir.resources.messageheader import (
    MessageHeader,
    MessageHeaderSource,
    MessageHeaderDestination,
    MessageHeaderResponse
)
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
from dnhealth.dnhealth_fhir.resources.organization import (
    Organization,
    OrganizationContact
)
from dnhealth.dnhealth_fhir.resources.organizationaffiliation import OrganizationAffiliation
from dnhealth.dnhealth_fhir.resources.parameters import Parameters, ParametersParameter
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.person import (
    Person,
    PersonLink
)
from dnhealth.dnhealth_fhir.resources.practitioner import (
    Practitioner,
    PractitionerQualification
)
from dnhealth.dnhealth_fhir.resources.practitionerrole import (
    PractitionerRole,
    PractitionerRoleAvailableTime,
    PractitionerRoleNotAvailable
)
from dnhealth.dnhealth_fhir.resources.procedure import (
    Procedure,
    ProcedurePerformer,
    ProcedureFocalDevice
)
from dnhealth.dnhealth_fhir.resources.provenance import (
    Provenance,
    ProvenanceAgent,
    ProvenanceEntity
)
from dnhealth.dnhealth_fhir.resources.questionnaire import (
    Questionnaire,
    QuestionnaireItem
)
from dnhealth.dnhealth_fhir.resources.questionnaireresponse import (
    QuestionnaireResponse,
    QuestionnaireResponseItem,
    QuestionnaireResponseItemAnswer
)
from dnhealth.dnhealth_fhir.resources.relatedperson import (
    RelatedPerson,
    RelatedPersonCommunication
)
from dnhealth.dnhealth_fhir.resources.schedule import Schedule
from dnhealth.dnhealth_fhir.resources.servicerequest import ServiceRequest
from dnhealth.dnhealth_fhir.resources.slot import Slot
from dnhealth.dnhealth_fhir.resources.specimen import (
    Specimen,
    SpecimenCollection,
    SpecimenProcessing,
    SpecimenContainer,
    SpecimenCondition
)
from dnhealth.dnhealth_fhir.resources.specimendefinition import (
    SpecimenDefinition,
    SpecimenDefinitionTypeTested,
    SpecimenDefinitionTypeTestedContainer,
    SpecimenDefinitionTypeTestedContainerAdditive,
    SpecimenDefinitionTypeTestedHandling,
    SpecimenDefinitionCollection
)
from dnhealth.dnhealth_fhir.resources.task import (
    Task,
    TaskInput,
    TaskOutput,
    TaskRestriction
)
from dnhealth.dnhealth_fhir.resources.measure import (
    Measure,
    MeasureGroup,
    MeasureGroupPopulation,
    MeasureGroupStratifier,
    MeasureGroupStratifierComponent,
    MeasureSupplementalData,
    MeasureTerm
)
from dnhealth.dnhealth_fhir.resources.measurereport import (
    MeasureReport,
    MeasureReportGroup,
    MeasureReportGroupPopulation,
    MeasureReportGroupStratifier,
    MeasureReportGroupStratifierStratum,
    MeasureReportGroupStratifierStratumComponent
)
from dnhealth.dnhealth_fhir.resources.nutritionorder import (
    NutritionOrder,
    NutritionOrderOralDiet,
    NutritionOrderOralDietNutrient,
    NutritionOrderOralDietTexture,
    NutritionOrderSupplement,
    NutritionOrderEnteralFormula,
    NutritionOrderEnteralFormulaAdministration
)
from dnhealth.dnhealth_fhir.resources.observationdefinition import (
    ObservationDefinition,
    ObservationDefinitionQuantitativeDetails,
    ObservationDefinitionQualifiedInterval
)
from dnhealth.dnhealth_fhir.resources.paymentnotice import PaymentNotice
from dnhealth.dnhealth_fhir.resources.paymentreconciliation import (
    PaymentReconciliation,
    PaymentReconciliationDetail,
    PaymentReconciliationProcessNote
)
from dnhealth.dnhealth_fhir.resources.plandefinition import (
    PlanDefinition,
    PlanDefinitionGoal,
    PlanDefinitionGoalTarget,
    PlanDefinitionAction,
    PlanDefinitionActionCondition,
    PlanDefinitionActionInput,
    PlanDefinitionActionOutput,
    PlanDefinitionActionRelatedAction,
    PlanDefinitionActionParticipant,
    PlanDefinitionActionDynamicValue
)
from dnhealth.dnhealth_fhir.resources.requestgroup import (
    RequestGroup,
    RequestGroupAction,
    RequestGroupActionCondition,
    RequestGroupActionRelatedAction
)
from dnhealth.dnhealth_fhir.resources.researchdefinition import ResearchDefinition
from dnhealth.dnhealth_fhir.resources.researchelementdefinition import (
    ResearchElementDefinition,
    ResearchElementDefinitionCharacteristic
)
from dnhealth.dnhealth_fhir.resources.researchstudy import (
    ResearchStudy,
    ResearchStudyArm,
    ResearchStudyObjective
)
from dnhealth.dnhealth_fhir.resources.researchsubject import ResearchSubject
from dnhealth.dnhealth_fhir.resources.riskassessment import (
    RiskAssessment,
    RiskAssessmentPrediction
)
from dnhealth.dnhealth_fhir.resources.riskevidencesynthesis import (
    RiskEvidenceSynthesis,
    RiskEvidenceSynthesisSampleSize,
    RiskEvidenceSynthesisRiskEstimate,
    RiskEvidenceSynthesisRiskEstimatePrecisionEstimate,
    RiskEvidenceSynthesisCertainty,
    RiskEvidenceSynthesisCertaintyCertaintySubcomponent
)
from dnhealth.dnhealth_fhir.resources.subscription import (
    Subscription,
    SubscriptionChannel
)
from dnhealth.dnhealth_fhir.resources.supplydelivery import (
    SupplyDelivery,
    SupplyDeliverySuppliedItem
)
from dnhealth.dnhealth_fhir.resources.supplyrequest import (
    SupplyRequest,
    SupplyRequestParameter
)
from dnhealth.dnhealth_fhir.resources.testreport import (
    TestReport,
    TestReportParticipant,
    TestReportSetup,
    TestReportSetupAction,
    TestReportSetupActionOperation,
    TestReportSetupActionAssert,
    TestReportTest,
    TestReportTestAction,
    TestReportTeardown
)
from dnhealth.dnhealth_fhir.resources.testscript import (
    TestScript,
    TestScriptOrigin,
    TestScriptDestination,
    TestScriptMetadata,
    TestScriptFixture,
    TestScriptVariable,
    TestScriptSetup,
    TestScriptTest,
    TestScriptTeardown
)
from dnhealth.dnhealth_fhir.resources.verificationresult import (
    VerificationResult,
    VerificationResultAttestation,
    VerificationResultValidator,
    VerificationResultPrimarySource
)
from dnhealth.dnhealth_fhir.resources.valueset import (
    ValueSet,
    ValueSetCompose,
    ValueSetComposeInclude,
    ValueSetComposeIncludeConcept,
    ValueSetComposeIncludeFilter,
    ValueSetExpansion,
    ValueSetExpansionContains,
    ValueSetExpansionParameter,
    get_codes_from_valueset,
)
from dnhealth.dnhealth_fhir.resources.visionprescription import (
    VisionPrescription,
    VisionPrescriptionLensSpecification,
    VisionPrescriptionLensSpecificationPrism
)
from dnhealth.dnhealth_fhir.resources.medicinalproduct import (
    MedicinalProduct,
    MedicinalProductName,
    MedicinalProductNamePart,
    MedicinalProductCountryLanguage,
    MedicinalProductManufacturingBusinessOperation,
    MedicinalProductSpecialDesignation,
    MarketingStatus
)
from dnhealth.dnhealth_fhir.resources.medicinalproductauthorization import (
    MedicinalProductAuthorization,
    MedicinalProductAuthorizationJurisdictionalAuthorization,
    MedicinalProductAuthorizationProcedure
)
from dnhealth.dnhealth_fhir.resources.medicinalproductcontraindication import (
    MedicinalProductContraindication,
    MedicinalProductContraindicationOtherTherapy
)
from dnhealth.dnhealth_fhir.resources.medicinalproductindication import (
    MedicinalProductIndication,
    MedicinalProductIndicationOtherTherapy
)
from dnhealth.dnhealth_fhir.resources.medicinalproductingredient import (
    MedicinalProductIngredient,
    MedicinalProductIngredientSpecifiedSubstance,
    MedicinalProductIngredientSpecifiedSubstanceStrength,
    MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength,
    MedicinalProductIngredientSubstance
)
from dnhealth.dnhealth_fhir.resources.medicinalproductinteraction import (
    MedicinalProductInteraction,
    MedicinalProductInteractionInteractant
)
from dnhealth.dnhealth_fhir.resources.medicinalproductmanufactured import (
    MedicinalProductManufactured,
    MedicinalProductManufacturedPhysicalCharacteristics
)
from dnhealth.dnhealth_fhir.resources.medicinalproductpackaged import (
    MedicinalProductPackaged,
    MedicinalProductPackagedBatchIdentifier,
    MedicinalProductPackagedPackageItem,
    MedicinalProductPackagedPhysicalCharacteristics,
    MedicinalProductPackagedShelfLifeStorage
)
from dnhealth.dnhealth_fhir.resources.medicinalproductpharmaceutical import (
    MedicinalProductPharmaceutical,
    MedicinalProductPharmaceuticalCharacteristics,
    MedicinalProductPharmaceuticalRouteOfAdministration,
    MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies,
    MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod
)
from dnhealth.dnhealth_fhir.resources.medicinalproductundesirableeffect import (
    MedicinalProductUndesirableEffect,
    Population
)
from dnhealth.dnhealth_fhir.resources.molecularsequence import (
    MolecularSequence,
    MolecularSequenceReferenceSeq,
    MolecularSequenceVariant,
    MolecularSequenceQuality,
    MolecularSequenceRepository,
    MolecularSequenceStructureVariant,
    MolecularSequenceStructureVariantOuter,
    MolecularSequenceStructureVariantInner
)
from dnhealth.dnhealth_fhir.resources.namingsystem import (
    NamingSystem,
    NamingSystemUniqueId
)
from dnhealth.dnhealth_fhir.resources.substance import (
    Substance,
    SubstanceInstance,
    SubstanceIngredient
)
from dnhealth.dnhealth_fhir.resources.substancenucleicacid import (
    SubstanceNucleicAcid,
    SubstanceNucleicAcidSubunit,
    SubstanceNucleicAcidSubunitLinkage,
    SubstanceNucleicAcidSubunitSugar
)
from dnhealth.dnhealth_fhir.resources.substancepolymer import (
    SubstancePolymer,
    SubstancePolymerMonomerSet,
    SubstancePolymerMonomerSetStartingMaterial,
    SubstancePolymerRepeat,
    SubstancePolymerRepeatRepeatUnit,
    SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation,
    SubstancePolymerRepeatRepeatUnitStructuralRepresentation
)
from dnhealth.dnhealth_fhir.resources.substanceprotein import (
    SubstanceProtein,
    SubstanceProteinSubunit
)
from dnhealth.dnhealth_fhir.resources.substancereferenceinformation import (
    SubstanceReferenceInformation,
    SubstanceReferenceInformationGene,
    SubstanceReferenceInformationGeneElement,
    SubstanceReferenceInformationClassification,
    SubstanceReferenceInformationTarget
)
from dnhealth.dnhealth_fhir.resources.substancesourcematerial import (
    SubstanceSourceMaterial,
    SubstanceSourceMaterialFractionDescription,
    SubstanceSourceMaterialOrganism,
    SubstanceSourceMaterialOrganismAuthor,
    SubstanceSourceMaterialOrganismHybrid,
    SubstanceSourceMaterialOrganismOrganismGeneral,
    SubstanceSourceMaterialPartDescription
)
from dnhealth.dnhealth_fhir.resources.substancespecification import (
    SubstanceSpecification,
    SubstanceSpecificationMoiety,
    SubstanceSpecificationProperty,
    SubstanceSpecificationStructure,
    SubstanceSpecificationStructureIsotope,
    SubstanceSpecificationStructureMolecularWeight,
    SubstanceSpecificationStructureRepresentation,
    SubstanceSpecificationCode,
    SubstanceSpecificationName,
    SubstanceSpecificationNameOfficial,
    SubstanceSpecificationRelationship
)

__all__ = [
    "FHIRResource",
    "Binary",
    "Bundle",
    "CapabilityStatement",
    "CapabilityStatementSoftware",
    "CapabilityStatementImplementation",
    "CapabilityStatementRest",
    "CapabilityStatementRestResource",
    "Condition",
    "GraphDefinition",
    "GraphDefinitionLink",
    "GraphDefinitionLinkTarget",
    "ImplementationGuide",
    "ImplementationGuideDependsOn",
    "ImplementationGuideGlobal",
    "ImplementationGuideDefinition",
    "ImplementationGuideManifest",
    "MessageDefinition",
    "MessageDefinitionFocus",
    "MessageDefinitionAllowedResponse",
    "OperationDefinition",
    "OperationDefinitionParameter",
    "OperationDefinitionOverload",
    "SearchParameterResource",
    "SearchParameter",  # Alias for SearchParameterResource
    "SearchParameterComponent",
    "StructureDefinition",
    "StructureDefinitionSnapshot",
    "StructureDefinitionDifferential",
    "StructureDefinitionMapping",
    "StructureDefinitionContext",
    "ElementDefinition",
    "StructureMap",
    "StructureMapStructure",
    "StructureMapGroup",
    "TerminologyCapabilities",
    "TerminologyCapabilitiesSoftware",
    "TerminologyCapabilitiesImplementation",
    "TerminologyCapabilitiesCodeSystem",
    "TerminologyCapabilitiesExpansion",
    "TerminologyCapabilitiesValidateCode",
    "TerminologyCapabilitiesTranslation",
    "TerminologyCapabilitiesClosure",
    "Account",
    "AccountCoverage",
    "AccountGuarantor",
    "ActivityDefinition",
    "ActivityDefinitionParticipant",
    "ActivityDefinitionDynamicValue",
    "AdverseEvent",
    "AdverseEventSuspectEntity",
    "AllergyIntolerance",
    "AllergyIntoleranceReaction",
    "Basic",
    "BiologicallyDerivedProduct",
    "BiologicallyDerivedProductCollection",
    "BiologicallyDerivedProductProcessing",
    "BiologicallyDerivedProductManipulation",
    "BiologicallyDerivedProductStorage",
    "BodyStructure",
    "CarePlan",
    "CarePlanActivity",
    "CareTeam",
    "CareTeamParticipant",
    "CatalogEntry",
    "CatalogEntryRelatedEntry",
    "ChargeItem",
    "ChargeItemPerformer",
    "ChargeItemDefinition",
    "ChargeItemDefinitionApplicability",
    "ChargeItemDefinitionPropertyGroup",
    "Claim",
    "ClaimRelated",
    "ClaimPayee",
    "ClaimCareTeam",
    "ClaimSupportingInfo",
    "ClaimDiagnosis",
    "ClaimProcedure",
    "ClaimInsurance",
    "ClaimAccident",
    "ClaimItem",
    "ClaimItemDetail",
    "ClaimItemDetailSubDetail",
    "ClaimResponse",
    "ClaimResponseItemAdjudication",
    "ClaimResponseItem",
    "ClaimResponseItemDetail",
    "ClaimResponseItemDetailSubDetail",
    "ClaimResponseAddItem",
    "ClaimResponseAddItemDetail",
    "ClaimResponseAddItemDetailSubDetail",
    "ClaimResponseTotal",
    "ClaimResponsePayment",
    "ClaimResponseProcessNote",
    "ClaimResponseInsurance",
    "ClaimResponseError",
    "ClinicalImpression",
    "CodeSystem",
    "CodeSystemConcept",
    "CodeSystemConceptDesignation",
    "CodeSystemConceptProperty",
    "CodeSystemFilter",
    "CodeSystemProperty",
    "ConceptMap",
    "ConceptMapGroup",
    "ConceptMapGroupElement",
    "ConceptMapGroupElementTarget",
    "ConceptMapGroupElementTargetDependsOn",
    "ConceptMapGroupUnmapped",
    "ClinicalImpressionInvestigation",
    "ClinicalImpressionFinding",
    "Communication",
    "CommunicationPayload",
    "CommunicationRequest",
    "CommunicationRequestPayload",
    "CompartmentDefinition",
    "CompartmentDefinitionResource",
    "Composition",
    "CompositionAttester",
    "CompositionRelatesTo",
    "CompositionEvent",
    "CompositionSection",
    "Consent",
    "ConsentPolicy",
    "ConsentVerification",
    "ConsentProvisionActor",
    "ConsentProvisionData",
    "ConsentProvision",
    "Contract",
    "ContractContentDefinition",
    "ContractTermAssetContext",
    "ContractTermAssetValuedItem",
    "ContractTermAsset",
    "ContractTermActionSubject",
    "ContractTermAction",
    "ContractTerm",
    "ContractSigner",
    "ContractFriendly",
    "ContractLegal",
    "Coverage",
    "CoverageCostToBeneficiaryException",
    "CoverageCostToBeneficiary",
    "CoverageClass",
    "CoverageEligibilityRequest",
    "CoverageEligibilityRequestSupportingInfo",
    "CoverageEligibilityRequestInsurance",
    "CoverageEligibilityRequestItemDiagnosis",
    "CoverageEligibilityRequestItem",
    "CoverageEligibilityResponse",
    "CoverageEligibilityResponseInsuranceItemBenefit",
    "CoverageEligibilityResponseInsuranceItem",
    "CoverageEligibilityResponseInsurance",
    "CoverageEligibilityResponseError",
    "DetectedIssue",
    "DetectedIssueMitigation",
    "Device",
    "DeviceUdiCarrier",
    "DeviceDeviceName",
    "DeviceSpecialization",
    "DeviceVersion",
    "DeviceProperty",
    "DeviceDefinition",
    "DeviceDefinitionUdiDeviceIdentifier",
    "DeviceDefinitionDeviceName",
    "DeviceDefinitionSpecialization",
    "DeviceDefinitionCapability",
    "DeviceDefinitionProperty",
    "DeviceDefinitionMaterial",
    "DeviceMetric",
    "DeviceMetricCalibration",
    "DeviceRequest",
    "DeviceRequestParameter",
    "DeviceUseStatement",
    "DiagnosticReport",
    "DiagnosticReportMedia",
    "DocumentManifest",
    "DocumentManifestRelated",
    "DocumentReference",
    "DocumentReferenceRelatesTo",
    "DocumentReferenceContent",
    "DocumentReferenceContext",
    "EffectEvidenceSynthesis",
    "EffectEvidenceSynthesisSampleSize",
    "EffectEvidenceSynthesisResultsByExposure",
    "EffectEvidenceSynthesisEffectEstimate",
    "EffectEvidenceSynthesisEffectEstimatePrecisionEstimate",
    "EffectEvidenceSynthesisCertainty",
    "EffectEvidenceSynthesisCertaintyCertaintySubcomponent",
    "Encounter",
    "Endpoint",
    "EnrollmentRequest",
    "EnrollmentResponse",
    "EpisodeOfCare",
    "EpisodeOfCareStatusHistory",
    "EpisodeOfCareDiagnosis",
    "EventDefinition",
    "Evidence",
    "EvidenceVariable",
    "EvidenceVariableCharacteristic",
    "ExampleScenario",
    "ExampleScenarioActor",
    "ExampleScenarioInstance",
    "ExampleScenarioInstanceVersion",
    "ExampleScenarioInstanceContainedInstance",
    "ExampleScenarioProcess",
    "ExampleScenarioProcessStep",
    "ExampleScenarioProcessStepOperation",
    "ExampleScenarioProcessStepAlternative",
    "ExplanationOfBenefit",
    "ExplanationOfBenefitRelated",
    "ExplanationOfBenefitPayee",
    "ExplanationOfBenefitCareTeam",
    "ExplanationOfBenefitSupportingInfo",
    "ExplanationOfBenefitDiagnosis",
    "ExplanationOfBenefitProcedure",
    "FamilyMemberHistory",
    "FamilyMemberHistoryCondition",
    "Flag",
    "Goal",
    "GoalTarget",
    "Group",
    "GroupCharacteristic",
    "GroupMember",
    "GuidanceResponse",
    "HealthcareService",
    "HealthcareServiceEligibility",
    "HealthcareServiceAvailableTime",
    "HealthcareServiceNotAvailable",
    "ImagingStudy",
    "ImagingStudySeries",
    "ImagingStudySeriesPerformer",
    "ImagingStudySeriesInstance",
    "Immunization",
    "ImmunizationPerformer",
    "ImmunizationEducation",
    "ImmunizationReaction",
    "ImmunizationProtocolApplied",
    "ImmunizationEvaluation",
    "ImmunizationRecommendation",
    "ImmunizationRecommendationRecommendation",
    "InsurancePlan",
    "InsurancePlanContact",
    "InsurancePlanCoverage",
    "InsurancePlanCoverageBenefit",
    "InsurancePlanCoverageBenefitLimit",
    "InsurancePlanPlan",
    "InsurancePlanPlanGeneralCost",
    "InsurancePlanPlanSpecificCost",
    "InsurancePlanPlanSpecificCostBenefit",
    "InsurancePlanPlanSpecificCostBenefitCost",
    "Invoice",
    "InvoiceParticipant",
    "InvoiceLineItem",
    "InvoiceLineItemPriceComponent",
    "Library",
    "Linkage",
    "LinkageItem",
    "ListResource",
    "List",  # Alias for ListResource
    "ListEntry",
    "Observation",
    "OperationOutcome",
    "OperationOutcomeIssue",
    "Parameters",
    "ParametersParameter",
    "Patient",
    "Appointment",
    "AppointmentParticipant",
    "AppointmentResponse",
    "AuditEvent",
    "AuditEventAgent",
    "AuditEventAgentNetwork",
    "AuditEventSource",
    "AuditEventEntity",
    "AuditEventEntityDetail",
    "Location",
    "LocationPosition",
    "LocationHoursOfOperation",
    "Media",
    "Medication",
    "MedicationIngredient",
    "MedicationBatch",
    "MedicationAdministration",
    "MedicationAdministrationPerformer",
    "MedicationAdministrationDosage",
    "MedicationDispense",
    "MedicationDispensePerformer",
    "MedicationDispenseSubstitution",
    "MedicationKnowledge",
    "MedicationKnowledgeRelatedMedicationKnowledge",
    "MedicationKnowledgeMonograph",
    "MedicationKnowledgeIngredient",
    "MedicationKnowledgeCost",
    "MedicationKnowledgeMonitoringProgram",
    "MedicationKnowledgeAdministrationGuidelines",
    "MedicationKnowledgeMedicineClassification",
    "MedicationKnowledgePackaging",
    "MedicationKnowledgeDrugCharacteristic",
    "MedicationKnowledgeRegulatory",
    "MedicationKnowledgeKinetics",
    "MedicationRequest",
    "MedicationRequestDispenseRequest",
    "MedicationRequestDispenseRequestInitialFill",
    "MedicationRequestSubstitution",
    "MedicationStatement",
    "MessageHeader",
    "MessageHeaderSource",
    "MessageHeaderDestination",
    "MessageHeaderResponse",
    "Organization",
    "OrganizationContact",
    "OrganizationAffiliation",
    "Person",
    "PersonLink",
    "Practitioner",
    "PractitionerQualification",
    "PractitionerRole",
    "PractitionerRoleAvailableTime",
    "PractitionerRoleNotAvailable",
    "Procedure",
    "ProcedurePerformer",
    "ProcedureFocalDevice",
    "Provenance",
    "ProvenanceAgent",
    "ProvenanceEntity",
    "Questionnaire",
    "QuestionnaireItem",
    "QuestionnaireResponse",
    "QuestionnaireResponseItem",
    "QuestionnaireResponseItemAnswer",
    "RelatedPerson",
    "RelatedPersonCommunication",
    "Schedule",
    "ServiceRequest",
    "Slot",
    "Specimen",
    "SpecimenCollection",
    "SpecimenProcessing",
    "SpecimenContainer",
    "SpecimenCondition",
    "SpecimenDefinition",
    "SpecimenDefinitionTypeTested",
    "SpecimenDefinitionTypeTestedContainer",
    "SpecimenDefinitionTypeTestedContainerAdditive",
    "SpecimenDefinitionTypeTestedHandling",
    "SpecimenDefinitionCollection",
    "Task",
    "TaskInput",
    "TaskOutput",
    "TaskRestriction",
    "Measure",
    "MeasureGroup",
    "MeasureGroupPopulation",
    "MeasureGroupStratifier",
    "MeasureGroupStratifierComponent",
    "MeasureSupplementalData",
    "MeasureTerm",
    "MeasureReport",
    "MeasureReportGroup",
    "MeasureReportGroupPopulation",
    "MeasureReportGroupStratifier",
    "MeasureReportGroupStratifierStratum",
    "MeasureReportGroupStratifierStratumComponent",
    "NutritionOrder",
    "NutritionOrderOralDiet",
    "NutritionOrderOralDietNutrient",
    "NutritionOrderOralDietTexture",
    "NutritionOrderSupplement",
    "NutritionOrderEnteralFormula",
    "NutritionOrderEnteralFormulaAdministration",
    "ObservationDefinition",
    "ObservationDefinitionQuantitativeDetails",
    "ObservationDefinitionQualifiedInterval",
    "PaymentNotice",
    "PaymentReconciliation",
    "PaymentReconciliationDetail",
    "PaymentReconciliationProcessNote",
    "PlanDefinition",
    "PlanDefinitionGoal",
    "PlanDefinitionGoalTarget",
    "PlanDefinitionAction",
    "PlanDefinitionActionCondition",
    "PlanDefinitionActionInput",
    "PlanDefinitionActionOutput",
    "PlanDefinitionActionRelatedAction",
    "PlanDefinitionActionParticipant",
    "PlanDefinitionActionDynamicValue",
    "RequestGroup",
    "RequestGroupAction",
    "RequestGroupActionCondition",
    "RequestGroupActionRelatedAction",
    "ResearchDefinition",
    "ResearchElementDefinition",
    "ResearchElementDefinitionCharacteristic",
    "ResearchStudy",
    "ResearchStudyArm",
    "ResearchStudyObjective",
    "ResearchSubject",
    "RiskAssessment",
    "RiskAssessmentPrediction",
    "RiskEvidenceSynthesis",
    "RiskEvidenceSynthesisSampleSize",
    "RiskEvidenceSynthesisRiskEstimate",
    "RiskEvidenceSynthesisRiskEstimatePrecisionEstimate",
    "RiskEvidenceSynthesisCertainty",
    "RiskEvidenceSynthesisCertaintyCertaintySubcomponent",
    "Subscription",
    "SubscriptionChannel",
    "SupplyDelivery",
    "SupplyDeliverySuppliedItem",
    "SupplyRequest",
    "SupplyRequestParameter",
    "TestReport",
    "TestReportParticipant",
    "TestReportSetup",
    "TestReportSetupAction",
    "TestReportSetupActionOperation",
    "TestReportSetupActionAssert",
    "TestReportTest",
    "TestReportTestAction",
    "TestReportTeardown",
    "TestScript",
    "TestScriptOrigin",
    "TestScriptDestination",
    "TestScriptMetadata",
    "TestScriptFixture",
    "TestScriptVariable",
    "TestScriptSetup",
    "TestScriptTest",
    "TestScriptTeardown",
    "VerificationResult",
    "VerificationResultAttestation",
    "VerificationResultValidator",
    "VerificationResultPrimarySource",
    "ValueSet",
    "ValueSetCompose",
    "ValueSetComposeInclude",
    "ValueSetComposeIncludeConcept",
    "ValueSetComposeIncludeFilter",
    "ValueSetExpansion",
    "ValueSetExpansionContains",
    "ValueSetExpansionParameter",
    "get_codes_from_valueset",
    "get_codes_from_codesystem",
    "translate_code",
    "VisionPrescription",
    "VisionPrescriptionLensSpecification",
    "VisionPrescriptionLensSpecificationPrism",
    # MedicinalProduct series
    "MedicinalProduct",
    "MedicinalProductName",
    "MedicinalProductNamePart",
    "MedicinalProductCountryLanguage",
    "MedicinalProductManufacturingBusinessOperation",
    "MedicinalProductSpecialDesignation",
    "MarketingStatus",
    "MedicinalProductAuthorization",
    "MedicinalProductAuthorizationJurisdictionalAuthorization",
    "MedicinalProductAuthorizationProcedure",
    "MedicinalProductContraindication",
    "MedicinalProductContraindicationOtherTherapy",
    "MedicinalProductIndication",
    "MedicinalProductIndicationOtherTherapy",
    "MedicinalProductIngredient",
    "MedicinalProductIngredientSpecifiedSubstance",
    "MedicinalProductIngredientSpecifiedSubstanceStrength",
    "MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength",
    "MedicinalProductIngredientSubstance",
    "MedicinalProductInteraction",
    "MedicinalProductInteractionInteractant",
    "MedicinalProductManufactured",
    "MedicinalProductManufacturedPhysicalCharacteristics",
    "MedicinalProductPackaged",
    "MedicinalProductPackagedBatchIdentifier",
    "MedicinalProductPackagedPackageItem",
    "MedicinalProductPackagedPhysicalCharacteristics",
    "MedicinalProductPackagedShelfLifeStorage",
    "MedicinalProductPharmaceutical",
    "MedicinalProductPharmaceuticalCharacteristics",
    "MedicinalProductPharmaceuticalRouteOfAdministration",
    "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies",
    "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod",
    "MedicinalProductUndesirableEffect",
    "Population",
    # MolecularSequence
    "MolecularSequence",
    "MolecularSequenceReferenceSeq",
    "MolecularSequenceVariant",
    "MolecularSequenceQuality",
    "MolecularSequenceRepository",
    "MolecularSequenceStructureVariant",
    "MolecularSequenceStructureVariantOuter",
    "MolecularSequenceStructureVariantInner",
    # NamingSystem
    "NamingSystem",
    "NamingSystemUniqueId",
    # Substance series
    "Substance",
    "SubstanceInstance",
    "SubstanceIngredient",
    "SubstanceNucleicAcid",
    "SubstanceNucleicAcidSubunit",
    "SubstanceNucleicAcidSubunitLinkage",
    "SubstanceNucleicAcidSubunitSugar",
    "SubstancePolymer",
    "SubstancePolymerMonomerSet",
    "SubstancePolymerMonomerSetStartingMaterial",
    "SubstancePolymerRepeat",
    "SubstancePolymerRepeatRepeatUnit",
    "SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation",
    "SubstancePolymerRepeatRepeatUnitStructuralRepresentation",
    "SubstanceProtein",
    "SubstanceProteinSubunit",
    "SubstanceReferenceInformation",
    "SubstanceReferenceInformationGene",
    "SubstanceReferenceInformationGeneElement",
    "SubstanceReferenceInformationClassification",
    "SubstanceReferenceInformationTarget",
    "SubstanceSourceMaterial",
    "SubstanceSourceMaterialFractionDescription",
    "SubstanceSourceMaterialOrganism",
    "SubstanceSourceMaterialOrganismAuthor",
    "SubstanceSourceMaterialOrganismHybrid",
    "SubstanceSourceMaterialOrganismOrganismGeneral",
    "SubstanceSourceMaterialPartDescription",
    "SubstanceSpecification",
    "SubstanceSpecificationMoiety",
    "SubstanceSpecificationProperty",
    "SubstanceSpecificationStructure",
    "SubstanceSpecificationStructureIsotope",
    "SubstanceSpecificationStructureMolecularWeight",
    "SubstanceSpecificationStructureRepresentation",
    "SubstanceSpecificationCode",
    "SubstanceSpecificationName",
    "SubstanceSpecificationNameOfficial",
    "SubstanceSpecificationRelationship",
]


