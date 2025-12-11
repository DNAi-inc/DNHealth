# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Cross-standard mapping utilities.

Provides functions to convert between HL7v2, HL7v3, and FHIR R4 formats.
"""

from dnhealth.mapping.hl7v2_to_fhir import (
    convert_adt_to_patient,
    convert_adt_to_encounter,
    convert_oru_to_observation,
    convert_orm_to_servicerequest,
    convert_mdm_to_documentreference,
)
from dnhealth.mapping.hl7v3_to_fhir import (
    convert_prpa_to_patient,
    convert_polb_to_observation,
    convert_polb_to_servicerequest,
    convert_porx_to_medicationrequest,
    convert_porx_to_medicationdispense,
)
from dnhealth.mapping.fhir_to_hl7v2 import (
    convert_patient_to_adt,
    convert_encounter_to_adt,
    convert_observation_to_oru,
    convert_servicerequest_to_orm,
    convert_documentreference_to_mdm,
)
from dnhealth.mapping.fhir_to_hl7v3 import (
    convert_patient_to_prpa,
    convert_observation_to_polb,
    convert_servicerequest_to_polb,
    convert_medicationrequest_to_porx,
    convert_medicationdispense_to_porx,
)
from dnhealth.mapping.config import (
    load_mapping_config,
    save_mapping_config,
    create_mapping_config,
)
from dnhealth.mapping.rules import (
    MappingRule,
    apply_mapping_rules,
    create_custom_rule,
)

__all__ = [
    # HL7v2 to FHIR
    "convert_adt_to_patient",
    "convert_adt_to_encounter",
    "convert_oru_to_observation",
    "convert_orm_to_servicerequest",
    "convert_mdm_to_documentreference",
    # HL7v3 to FHIR
    "convert_prpa_to_patient",
    "convert_polb_to_observation",
    "convert_polb_to_servicerequest",
    "convert_porx_to_medicationrequest",
    "convert_porx_to_medicationdispense",
    # FHIR to HL7v2
    "convert_patient_to_adt",
    "convert_encounter_to_adt",
    "convert_observation_to_oru",
    "convert_servicerequest_to_orm",
    "convert_documentreference_to_mdm",
    # FHIR to HL7v3
    "convert_patient_to_prpa",
    "convert_observation_to_polb",
    "convert_servicerequest_to_polb",
    "convert_medicationrequest_to_porx",
    "convert_medicationdispense_to_porx",
    # Configuration
    "load_mapping_config",
    "save_mapping_config",
    "create_mapping_config",
    # Rules
    "MappingRule",
    "apply_mapping_rules",
    "create_custom_rule",
]
