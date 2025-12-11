# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v2.x Segment Field Definitions.

Provides complete field definitions for HL7 v2.x segments including:
- Field data types
- Field lengths
- Required/optional status
- Table bindings
- Version-specific differences
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class FieldDefinition:
    """
    Definition of a segment field.
    
    Contains all metadata about a field including type, length, cardinality, etc.
    """
    field_index: int  # 1-based field index
    field_name: str
    data_type: str  # ST, FT, TS, ID, IS, etc.
    length: Optional[int] = None  # Maximum length
    min_length: Optional[int] = None  # Minimum length
    required: bool = False  # Required field
    optional: bool = True  # Optional field
    repeating: bool = False  # Can repeat
    table_binding: Optional[str] = None  # Table ID (e.g., "0001")
    description: Optional[str] = None
    version_specific: Dict[str, Dict] = field(default_factory=dict)  # Version-specific overrides


# ============================================================================
# MSH Segment - Message Header
# ============================================================================

MSH_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Field Separator",
        data_type="ST",
        length=1,
        required=True,
        description="Separator character (usually |)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Encoding Characters",
        data_type="ST",
        length=4,
        required=True,
        description="Encoding characters (^~\\&)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Sending Application",
        data_type="HD",
        length=227,
        description="Sending application identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Sending Facility",
        data_type="HD",
        length=227,
        description="Sending facility identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Receiving Application",
        data_type="HD",
        length=227,
        description="Receiving application identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Receiving Facility",
        data_type="HD",
        length=227,
        description="Receiving facility identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Date/Time of Message",
        data_type="TS",
        length=26,
        description="Message timestamp"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Security",
        data_type="ST",
        length=40,
        description="Security field"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Message Type",
        data_type="MSG",
        length=15,
        required=True,
        description="Message type (e.g., ADT^A01^ADT_A01)"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Message Control ID",
        data_type="ST",
        length=20,
        required=True,
        description="Unique message identifier"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Processing ID",
        data_type="PT",
        length=3,
        required=True,
        description="Processing mode (P=Production, T=Test, D=Debug)"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Version ID",
        data_type="VID",
        length=60,
        required=True,
        description="HL7 version (e.g., 2.5)"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Sequence Number",
        data_type="NM",
        length=15,
        description="Sequence number"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Continuation Pointer",
        data_type="ST",
        length=180,
        description="Continuation pointer for long messages"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Accept Acknowledgment Type",
        data_type="ID",
        length=2,
        table_binding="0155",
        description="AA=Always, NE=Never, ER=Error, SU=Success"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Application Acknowledgment Type",
        data_type="ID",
        length=2,
        table_binding="0155",
        description="AA=Always, NE=Never, ER=Error, SU=Success"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Country Code",
        data_type="ID",
        length=3,
        table_binding="0399",
        description="ISO 3166 country code"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Character Set",
        data_type="ID",
        length=16,
        table_binding="0211",
        description="Character set (e.g., ASCII, ISO IR14)"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Principal Language of Message",
        data_type="CE",
        length=250,
        description="Language code"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Alternate Character Set Handling Scheme",
        data_type="ID",
        length=20,
        table_binding="0356",
        description="Character set handling"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Message Profile Identifier",
        data_type="EI",
        length=427,
        description="Message profile identifier"
    ),
}


# ============================================================================
# PID Segment - Patient Identification
# ============================================================================

PID_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - PID",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Patient ID (External ID)",
        data_type="CX",
        length=250,
        description="External patient identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient ID (Internal ID)",
        data_type="CX",
        length=250,
        repeating=True,
        description="Internal patient identifier(s)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Alternate Patient ID - PID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Alternate patient identifiers"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Patient Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Patient name"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Mother's maiden name"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Date/Time of Birth",
        data_type="TS",
        length=26,
        description="Patient date of birth"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administrative Sex",
        data_type="IS",
        length=1,
        table_binding="0001",
        description="M=Male, F=Female, O=Other, U=Unknown"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Patient Alias",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Patient alias(es)"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Race",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0005",
        description="Patient race"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Patient Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Patient address"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="County Code",
        data_type="IS",
        length=4,
        description="County code"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Phone Number - Home",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Home phone number"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Phone Number - Business",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Business phone number"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Primary Language",
        data_type="CE",
        length=250,
        description="Primary language"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Marital Status",
        data_type="CE",
        length=250,
        table_binding="0002",
        description="Marital status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Religion",
        data_type="CE",
        length=250,
        table_binding="0006",
        description="Religion"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Patient Account Number",
        data_type="CX",
        length=250,
        description="Patient account number"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="SSN Number - Patient",
        data_type="ST",
        length=16,
        description="Social Security Number"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Driver's License Number - Patient",
        data_type="DLN",
        length=25,
        description="Driver's license number"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Mother's Identifier",
        data_type="CX",
        length=250,
        repeating=True,
        description="Mother's identifier"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Ethnic Group",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0189",
        description="Ethnic group"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Birth Place",
        data_type="ST",
        length=250,
        description="Birth place"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Multiple Birth Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Y=Yes, N=No"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Birth Order",
        data_type="NM",
        length=2,
        description="Birth order"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Citizenship",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0171",
        description="Citizenship"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Veterans Military Status",
        data_type="CE",
        length=250,
        description="Veterans military status"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Nationality",
        data_type="CE",
        length=250,
        description="Nationality"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Patient Death Date and Time",
        data_type="TS",
        length=26,
        description="Date and time of death"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Patient Death Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Y=Yes, N=No"
    ),
}


# ============================================================================
# Helper Functions
# ============================================================================

def get_field_definition(segment_name: str, field_index: int, version: Optional[str] = None) -> Optional[FieldDefinition]:
    """
    Get field definition for a segment field.
    
    Args:
        segment_name: Segment name (e.g., "MSH", "PID", "Z01")
        field_index: Field index (1-based)
        version: Optional HL7 version (e.g., "2.5")
        
    Returns:
        FieldDefinition or None if not found
    """
    # Check for Z-segment first
    if is_z_segment(segment_name):
        z_segment_defs = get_z_segment_fields(segment_name)
        if z_segment_defs:
            return z_segment_defs.get(field_index)
    
    segment_defs = {
        "MSH": MSH_FIELD_DEFINITIONS,
        "PID": PID_FIELD_DEFINITIONS,
        "EVN": EVN_FIELD_DEFINITIONS,
        "PV1": PV1_FIELD_DEFINITIONS,
        "OBR": OBR_FIELD_DEFINITIONS,
        "OBX": OBX_FIELD_DEFINITIONS,
        "NTE": NTE_FIELD_DEFINITIONS,
        "AL1": AL1_FIELD_DEFINITIONS,
        "DG1": DG1_FIELD_DEFINITIONS,
        "PR1": PR1_FIELD_DEFINITIONS,
        "ORC": ORC_FIELD_DEFINITIONS,
        "IN1": IN1_FIELD_DEFINITIONS,
        "IN2": IN2_FIELD_DEFINITIONS,
        "IN3": IN3_FIELD_DEFINITIONS,
        "NK1": NK1_FIELD_DEFINITIONS,
        "PD1": PD1_FIELD_DEFINITIONS,
        "PV2": PV2_FIELD_DEFINITIONS,
        "GT1": GT1_FIELD_DEFINITIONS,
        "MSA": MSA_FIELD_DEFINITIONS,
        "ERR": ERR_FIELD_DEFINITIONS,
        "QRD": QRD_FIELD_DEFINITIONS,
        "QRF": QRF_FIELD_DEFINITIONS,
        "QAK": QAK_FIELD_DEFINITIONS,
        "QPD": QPD_FIELD_DEFINITIONS,
        "QRA": QRA_FIELD_DEFINITIONS,
        "RGS": RGS_FIELD_DEFINITIONS,
        "SPM": SPM_FIELD_DEFINITIONS,
        "SN": SN_FIELD_DEFINITIONS,
        "SPS": SPS_FIELD_DEFINITIONS,
        "TQ1": TQ1_FIELD_DEFINITIONS,
        "TQ2": TQ2_FIELD_DEFINITIONS,
        "RXR": RXR_FIELD_DEFINITIONS,
        "RXC": RXC_FIELD_DEFINITIONS,
        "RXA": RXA_FIELD_DEFINITIONS,
        "DSC": DSC_FIELD_DEFINITIONS,
        "UB1": UB1_FIELD_DEFINITIONS,
        "UB2": UB2_FIELD_DEFINITIONS,
        "ROL": ROL_FIELD_DEFINITIONS,
        "CTD": CTD_FIELD_DEFINITIONS,
        "ACC": ACC_FIELD_DEFINITIONS,
        "BHS": BHS_FIELD_DEFINITIONS,
        "BTS": BTS_FIELD_DEFINITIONS,
        "SCH": SCH_FIELD_DEFINITIONS,
        "TXA": TXA_FIELD_DEFINITIONS,
        "RCP": RCP_FIELD_DEFINITIONS,
        "RF1": RF1_FIELD_DEFINITIONS,
        "RMI": RMI_FIELD_DEFINITIONS,
        "AIS": AIS_FIELD_DEFINITIONS,
        "AIG": AIG_FIELD_DEFINITIONS,
        "AIL": AIL_FIELD_DEFINITIONS,
        "AIP": AIP_FIELD_DEFINITIONS,
        "DB1": DB1_FIELD_DEFINITIONS,
        "FAC": FAC_FIELD_DEFINITIONS,
        "STF": STF_FIELD_DEFINITIONS,
        "FHS": FHS_FIELD_DEFINITIONS,
        "FTS": FTS_FIELD_DEFINITIONS,
        "RXD": RXD_FIELD_DEFINITIONS,
        "RXE": RXE_FIELD_DEFINITIONS,
        "RXG": RXG_FIELD_DEFINITIONS,
        "RXO": RXO_FIELD_DEFINITIONS,
        "RXP": RXP_FIELD_DEFINITIONS,
        "CDM": CDM_FIELD_DEFINITIONS,
        "DRG": DRG_FIELD_DEFINITIONS,
        "MRG": MRG_FIELD_DEFINITIONS,
        "QID": QID_FIELD_DEFINITIONS,
        "QRI": QRI_FIELD_DEFINITIONS,
        "QSC": QSC_FIELD_DEFINITIONS,
        "RCD": RCD_FIELD_DEFINITIONS,
        "RDF": RDF_FIELD_DEFINITIONS,
        "RDT": RDT_FIELD_DEFINITIONS,
        "RQ1": RQ1_FIELD_DEFINITIONS,
        "RQD": RQD_FIELD_DEFINITIONS,
        "RPT": RPT_FIELD_DEFINITIONS,
        "SAC": SAC_FIELD_DEFINITIONS,
        "SCD": SCD_FIELD_DEFINITIONS,
        "SCP": SCP_FIELD_DEFINITIONS,
        "SDD": SDD_FIELD_DEFINITIONS,
        "SID": SID_FIELD_DEFINITIONS,
        "SLT": SLT_FIELD_DEFINITIONS,
        "SPR": SPR_FIELD_DEFINITIONS,
        "TCC": TCC_FIELD_DEFINITIONS,
        "TCD": TCD_FIELD_DEFINITIONS,
        "UAC": UAC_FIELD_DEFINITIONS,
        "VAR": VAR_FIELD_DEFINITIONS,
        "PDA": PDA_FIELD_DEFINITIONS,
        "FT1": FT1_FIELD_DEFINITIONS,
        "VXA": VXA_FIELD_DEFINITIONS,
        "VXU": VXU_FIELD_DEFINITIONS,
        "VXR": VXR_FIELD_DEFINITIONS,
        "VXQ": VXQ_FIELD_DEFINITIONS,
        "VXX": VXX_FIELD_DEFINITIONS,
        "SFT": SFT_FIELD_DEFINITIONS,
        "SAD": SAD_FIELD_DEFINITIONS,
        "SCV": SCV_FIELD_DEFINITIONS,
        "SPD": SPD_FIELD_DEFINITIONS,
        "SRT": SRT_FIELD_DEFINITIONS,
        "ABS": ABS_FIELD_DEFINITIONS,
        "BLC": BLC_FIELD_DEFINITIONS,
        "CM0": CM0_FIELD_DEFINITIONS,
        "CM1": CM1_FIELD_DEFINITIONS,
        "CM2": CM2_FIELD_DEFINITIONS,
        "CNS": CNS_FIELD_DEFINITIONS,
        "CSP": CSP_FIELD_DEFINITIONS,
        "ED": ED_FIELD_DEFINITIONS,
        "ADJ": ADJ_FIELD_DEFINITIONS,
        "AFF": AFF_FIELD_DEFINITIONS,
        "BTX": BTX_FIELD_DEFINITIONS,
        "DMI": DMI_FIELD_DEFINITIONS,
        "DON": DON_FIELD_DEFINITIONS,
        "PMT": PMT_FIELD_DEFINITIONS,
        "RBC": RBC_FIELD_DEFINITIONS,
        "REL": REL_FIELD_DEFINITIONS,
        "RRO": RRO_FIELD_DEFINITIONS,
        "RXX": RXX_FIELD_DEFINITIONS,
        "ILT": ILT_FIELD_DEFINITIONS,
        "OM7": OM7_FIELD_DEFINITIONS,
        "PDC": PDC_FIELD_DEFINITIONS,
        "PKG": PKG_FIELD_DEFINITIONS,
        "PRA": PRA_FIELD_DEFINITIONS,
        "RXV": RXV_FIELD_DEFINITIONS,
        "RXI": RXI_FIELD_DEFINITIONS,
        "URD": URD_FIELD_DEFINITIONS,
        "URS": URS_FIELD_DEFINITIONS,
        "VTQ": VTQ_FIELD_DEFINITIONS,
        "CSR": CSR_FIELD_DEFINITIONS,
        "CSS": CSS_FIELD_DEFINITIONS,
        "CTI": CTI_FIELD_DEFINITIONS,
        "DSP": DSP_FIELD_DEFINITIONS,
        "ECD": ECD_FIELD_DEFINITIONS,
        "ECR": ECR_FIELD_DEFINITIONS,
        "EDU": EDU_FIELD_DEFINITIONS,
        "EQL": EQL_FIELD_DEFINITIONS,
        "EQP": EQP_FIELD_DEFINITIONS,
        "EQU": EQU_FIELD_DEFINITIONS,
        "ERQ": ERQ_FIELD_DEFINITIONS,
        "ARV": ARV_FIELD_DEFINITIONS,
        "AUT": AUT_FIELD_DEFINITIONS,
        "BPO": BPO_FIELD_DEFINITIONS,
        "BPX": BPX_FIELD_DEFINITIONS,
        "BUI": BUI_FIELD_DEFINITIONS,
        "IAM": IAM_FIELD_DEFINITIONS,
        "IAR": IAR_FIELD_DEFINITIONS,
        "MFI": MFI_FIELD_DEFINITIONS,
        "MFE": MFE_FIELD_DEFINITIONS,
        "MFA": MFA_FIELD_DEFINITIONS,
        "OM1": OM1_FIELD_DEFINITIONS,
        "OM2": OM2_FIELD_DEFINITIONS,
        "OM3": OM3_FIELD_DEFINITIONS,
        "OM4": OM4_FIELD_DEFINITIONS,
        "OM5": OM5_FIELD_DEFINITIONS,
        "OM6": OM6_FIELD_DEFINITIONS,
        "PRB": PRB_FIELD_DEFINITIONS,
        "PRC": PRC_FIELD_DEFINITIONS,
        "PRD": PRD_FIELD_DEFINITIONS,
        "PSH": PSH_FIELD_DEFINITIONS,
        "PTH": PTH_FIELD_DEFINITIONS,
        "ODS": ODS_FIELD_DEFINITIONS,
        "ODT": ODT_FIELD_DEFINITIONS,
        "OMS": OMS_FIELD_DEFINITIONS,
        "ORG": ORG_FIELD_DEFINITIONS,
        "ORO": ORO_FIELD_DEFINITIONS,
        "OVR": OVR_FIELD_DEFINITIONS,
        "PCR": PCR_FIELD_DEFINITIONS,
        "PEO": PEO_FIELD_DEFINITIONS,
        "PE1": PE1_FIELD_DEFINITIONS,
        "PE2": PE2_FIELD_DEFINITIONS,
        "PES": PES_FIELD_DEFINITIONS,
        "IVT": IVT_FIELD_DEFINITIONS,
        "IVC": IVC_FIELD_DEFINITIONS,
        "IPR": IPR_FIELD_DEFINITIONS,
        "IVP": IVP_FIELD_DEFINITIONS,
        "ITM": ITM_FIELD_DEFINITIONS,
        "LDP": LDP_FIELD_DEFINITIONS,
        "LCC": LCC_FIELD_DEFINITIONS,
        "LCH": LCH_FIELD_DEFINITIONS,
        "LRL": LRL_FIELD_DEFINITIONS,
        "BLG": BLG_FIELD_DEFINITIONS,
        "LOC": LOC_FIELD_DEFINITIONS,
        "PCE": PCE_FIELD_DEFINITIONS,
        "PRT": PRT_FIELD_DEFINITIONS,
        "MDM": MDM_FIELD_DEFINITIONS,
        "SIU": SIU_FIELD_DEFINITIONS,
        "BAR": BAR_FIELD_DEFINITIONS,
        "RDE": RDE_FIELD_DEFINITIONS,
        "RDS": RDS_FIELD_DEFINITIONS,
        "RGV": RGV_FIELD_DEFINITIONS,
        "RAS": RAS_FIELD_DEFINITIONS,
        "RAR": RAR_FIELD_DEFINITIONS,
        "RER": RER_FIELD_DEFINITIONS,
        "RGR": RGR_FIELD_DEFINITIONS,
        "APR": APR_FIELD_DEFINITIONS,
        "ARQ": ARQ_FIELD_DEFINITIONS,
        "RRA": RRA_FIELD_DEFINITIONS,
        "RRD": RRD_FIELD_DEFINITIONS,
        "RRG": RRG_FIELD_DEFINITIONS,
        "RRE": RRE_FIELD_DEFINITIONS,
        "RRF": RRF_FIELD_DEFINITIONS,
        "RCL": RCL_FIELD_DEFINITIONS,
        "ROR": ROR_FIELD_DEFINITIONS,
        "CON": CON_FIELD_DEFINITIONS,
        "GP1": GP1_FIELD_DEFINITIONS,
        "GP2": GP2_FIELD_DEFINITIONS,
        "LAN": LAN_FIELD_DEFINITIONS,
        "QBP": QBP_FIELD_DEFINITIONS,
        "QRY": QRY_FIELD_DEFINITIONS,
        "RSP": RSP_FIELD_DEFINITIONS,
        "RTB": RTB_FIELD_DEFINITIONS,
        "QCN": QCN_FIELD_DEFINITIONS,
        "PV3": PV3_FIELD_DEFINITIONS,
        "ADD": ADD_FIELD_DEFINITIONS,
        "CER": CER_FIELD_DEFINITIONS,
        "NCK": NCK_FIELD_DEFINITIONS,
        "NDS": NDS_FIELD_DEFINITIONS,
        "NPU": NPU_FIELD_DEFINITIONS,
        "NSC": NSC_FIELD_DEFINITIONS,
        "NST": NST_FIELD_DEFINITIONS,
        "GOL": GOL_FIELD_DEFINITIONS,
        "IIM": IIM_FIELD_DEFINITIONS,
        "INV": INV_FIELD_DEFINITIONS,
        "IPC": IPC_FIELD_DEFINITIONS,
        "ISD": ISD_FIELD_DEFINITIONS,
        "OMD": OMD_FIELD_DEFINITIONS,
        "OMG": OMG_FIELD_DEFINITIONS,
        "OML": OML_FIELD_DEFINITIONS,
        "OMN": OMN_FIELD_DEFINITIONS,
        "OMP": OMP_FIELD_DEFINITIONS,
        "ORD": ORD_FIELD_DEFINITIONS,
        "ORF": ORF_FIELD_DEFINITIONS,
        "ORI": ORI_FIELD_DEFINITIONS,
        "ORL": ORL_FIELD_DEFINITIONS,
        "ORM": ORM_FIELD_DEFINITIONS,
        "ORN": ORN_FIELD_DEFINITIONS,
        "ORP": ORP_FIELD_DEFINITIONS,
        "ORR": ORR_FIELD_DEFINITIONS,
        "ORS": ORS_FIELD_DEFINITIONS,
        "ORU": ORU_FIELD_DEFINITIONS,
        "OSD": OSD_FIELD_DEFINITIONS,
        "OSP": OSP_FIELD_DEFINITIONS,
        "PEX": PEX_FIELD_DEFINITIONS,
        "PGL": PGL_FIELD_DEFINITIONS,
        "PIN": PIN_FIELD_DEFINITIONS,
        "STZ": STZ_FIELD_DEFINITIONS,
        "PMU": PMU_FIELD_DEFINITIONS,
        "PPG": PPG_FIELD_DEFINITIONS,
        "PPT": PPT_FIELD_DEFINITIONS,
        "PPV": PPV_FIELD_DEFINITIONS,
        "PTR": PTR_FIELD_DEFINITIONS,
        "QCK": QCK_FIELD_DEFINITIONS,
        "RCI": RCI_FIELD_DEFINITIONS,
        "RDR": RDR_FIELD_DEFINITIONS,
        "RDY": RDY_FIELD_DEFINITIONS,
        "REF": REF_FIELD_DEFINITIONS,
        "RPA": RPA_FIELD_DEFINITIONS,
        "RPI": RPI_FIELD_DEFINITIONS,
        "RPL": RPL_FIELD_DEFINITIONS,
        "RPR": RPR_FIELD_DEFINITIONS,
        "RQA": RQA_FIELD_DEFINITIONS,
        "RQC": RQC_FIELD_DEFINITIONS,
        "RQI": RQI_FIELD_DEFINITIONS,
        "RQP": RQP_FIELD_DEFINITIONS,
        "RQQ": RQQ_FIELD_DEFINITIONS,
        "RRI": RRI_FIELD_DEFINITIONS,
        "SQM": SQM_FIELD_DEFINITIONS,
        "SQR": SQR_FIELD_DEFINITIONS,
        "SRM": SRM_FIELD_DEFINITIONS,
        "SRR": SRR_FIELD_DEFINITIONS,
        "SSR": SSR_FIELD_DEFINITIONS,
        "SSU": SSU_FIELD_DEFINITIONS,
        "STC": STC_FIELD_DEFINITIONS,
        "TCU": TCU_FIELD_DEFINITIONS,
        "UDM": UDM_FIELD_DEFINITIONS,
    }
    
    if segment_name not in segment_defs:
        return None
    
    field_def = segment_defs[segment_name].get(field_index)
    if field_def is None:
        return None
    
    # Apply version-specific overrides if available
    if version and version in field_def.version_specific:
        override = field_def.version_specific[version]
        # Create a copy with overrides applied
        from copy import deepcopy
        result = deepcopy(field_def)
        for key, value in override.items():
            setattr(result, key, value)
        logger.debug(f"get_field_definition completed at {datetime.now().isoformat()}")
        return result
    
    logger.debug(f"get_field_definition completed at {datetime.now().isoformat()}")
    return field_def


def validate_field_value(segment_name: str, field_index: int, value: str, version: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate a field value against its definition.
    
    Args:
        segment_name: Segment name
        field_index: Field index (1-based)
        value: Field value to validate
        version: Optional HL7 version
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    field_def = get_field_definition(segment_name, field_index, version)
    if field_def is None:
        return True, None  # No definition = no validation
    
    # Check required
    if field_def.required and (not value or value.strip() == ""):
        return False, f"Field {segment_name}-{field_index} ({field_def.field_name}) is required"
    
    # Check length
    if field_def.length and len(value) > field_def.length:
        return False, f"Field {segment_name}-{field_index} ({field_def.field_name}) exceeds maximum length {field_def.length}"
    
    if field_def.min_length and len(value) < field_def.min_length:
        return False, f"Field {segment_name}-{field_index} ({field_def.field_name}) is below minimum length {field_def.min_length}"
    
    logger.debug(f"validate_field_value completed at {datetime.now().isoformat()}")

    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
    return True, None


# ============================================================================
# EVN Segment - Event Type
# ============================================================================

EVN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Event Type Code",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0003",
        description="Event type code",
        version_specific={
            "2.1": {"required": False, "optional": True},  # Optional in 2.1
            "2.2": {"required": False, "optional": True},  # Optional in 2.2
            "2.3": {"required": True, "optional": False},  # Required in 2.3+
            "2.4": {"required": True, "optional": False},
            "2.5": {"required": True, "optional": False},
            "2.6": {"required": True, "optional": False},
            "2.7": {"required": True, "optional": False},
            "2.8": {"required": True, "optional": False},
            "2.9": {"required": True, "optional": False},
        }
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Recorded Date/Time",
        data_type="TS",
        length=26,
        description="Date/time event was recorded"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date/Time Planned Event",
        data_type="TS",
        length=26,
        description="Date/time event is planned"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Reason Code",
        data_type="ID",
        length=3,
        table_binding="0062",
        description="Reason code for event"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Operator ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Operator identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Event Occurred",
        data_type="TS",
        length=26,
        description="Date/time event occurred (v2.5+)",
        version_specific={
            # Field 6 only available in 2.5+
            "2.1": {"description": "Field not available in v2.1"},
            "2.2": {"description": "Field not available in v2.2"},
            "2.3": {"description": "Field not available in v2.3"},
            "2.4": {"description": "Field not available in v2.4"},
        }
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Event Facility",
        data_type="HD",
        length=227,
        description="Facility where event occurred (v2.7+)",
        version_specific={
            # Field 7 only available in 2.7+
            "2.1": {"description": "Field not available in v2.1"},
            "2.2": {"description": "Field not available in v2.2"},
            "2.3": {"description": "Field not available in v2.3"},
            "2.4": {"description": "Field not available in v2.4"},
            "2.5": {"description": "Field not available in v2.5"},
            "2.6": {"description": "Field not available in v2.6"},
        }
    ),
}


# ============================================================================
# PV1 Segment - Patient Visit
# ============================================================================

PV1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - PV1",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Patient Class",
        data_type="IS",
        length=1,
        required=True,
        table_binding="0004",
        description="Patient class (I=Inpatient, O=Outpatient, E=Emergency, etc.)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Assigned Patient Location",
        data_type="PL",
        length=80,
        description="Assigned patient location"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Admission Type",
        data_type="IS",
        length=2,
        table_binding="0007",
        description="Type of admission"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Preadmit Number",
        data_type="CX",
        length=250,
        description="Preadmit number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Prior Patient Location",
        data_type="PL",
        length=80,
        description="Prior patient location"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Attending Doctor",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Attending doctor"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Referring Doctor",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Referring doctor"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Consulting Doctor",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Consulting doctor"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Hospital Service",
        data_type="IS",
        length=3,
        table_binding="0069",
        description="Hospital service"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Temporary Location",
        data_type="PL",
        length=80,
        description="Temporary location"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Preadmit Test Indicator",
        data_type="IS",
        length=1,
        table_binding="0087",
        description="Preadmit test indicator"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Re-admission Indicator",
        data_type="IS",
        length=2,
        table_binding="0092",
        description="Re-admission indicator"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Admit Source",
        data_type="IS",
        length=3,
        table_binding="0023",
        description="Admit source"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Ambulatory Status",
        data_type="IS",
        length=2,
        repeating=True,
        table_binding="0009",
        description="Ambulatory status"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="VIP Indicator",
        data_type="IS",
        length=2,
        table_binding="0099",
        description="VIP indicator"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Admitting Doctor",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Admitting doctor"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Patient Type",
        data_type="IS",
        length=2,
        table_binding="0018",
        description="Patient type"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Visit Number",
        data_type="CX",
        length=250,
        description="Visit number"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Financial Class",
        data_type="FC",
        length=50,
        repeating=True,
        description="Financial class"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Charge Price Indicator",
        data_type="IS",
        length=2,
        table_binding="0032",
        description="Charge price indicator"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Courtesy Code",
        data_type="IS",
        length=2,
        table_binding="0045",
        description="Courtesy code"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Credit Rating",
        data_type="IS",
        length=2,
        table_binding="0046",
        description="Credit rating"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Contract Code",
        data_type="IS",
        length=2,
        repeating=True,
        table_binding="0044",
        description="Contract code"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Contract Effective Date",
        data_type="DT",
        length=8,
        repeating=True,
        description="Contract effective date"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Contract Amount",
        data_type="NM",
        length=12,
        repeating=True,
        description="Contract amount"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Contract Period",
        data_type="NM",
        length=3,
        repeating=True,
        description="Contract period"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Interest Code",
        data_type="IS",
        length=2,
        table_binding="0073",
        description="Interest code"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Transfer to Bad Debt Code",
        data_type="IS",
        length=1,
        table_binding="0110",
        description="Transfer to bad debt code"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Transfer to Bad Debt Date",
        data_type="DT",
        length=8,
        description="Transfer to bad debt date"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Bad Debt Agency Code",
        data_type="IS",
        length=10,
        table_binding="0021",
        description="Bad debt agency code"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Bad Debt Transfer Amount",
        data_type="NM",
        length=12,
        description="Bad debt transfer amount"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Bad Debt Recovery Amount",
        data_type="NM",
        length=12,
        description="Bad debt recovery amount"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Delete Account Indicator",
        data_type="IS",
        length=1,
        table_binding="0111",
        description="Delete account indicator"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Delete Account Date",
        data_type="DT",
        length=8,
        description="Delete account date"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Discharge Disposition",
        data_type="IS",
        length=3,
        table_binding="0112",
        description="Discharge disposition"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Discharged to Location",
        data_type="DLD",
        length=47,
        description="Discharged to location"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Diet Type",
        data_type="CE",
        length=250,
        table_binding="0114",
        description="Diet type"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Servicing Facility",
        data_type="IS",
        length=2,
        table_binding="0115",
        description="Servicing facility"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Bed Status",
        data_type="IS",
        length=1,
        table_binding="0116",
        description="Bed status"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Account Status",
        data_type="IS",
        length=2,
        table_binding="0117",
        description="Account status"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Pending Location",
        data_type="PL",
        length=80,
        description="Pending location"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Prior Temporary Location",
        data_type="PL",
        length=80,
        description="Prior temporary location"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Admit Date/Time",
        data_type="TS",
        length=26,
        description="Admit date/time"
    ),
    45: FieldDefinition(
        field_index=45,
        field_name="Discharge Date/Time",
        data_type="TS",
        length=26,
        description="Discharge date/time"
    ),
    46: FieldDefinition(
        field_index=46,
        field_name="Current Patient Balance",
        data_type="NM",
        length=12,
        description="Current patient balance"
    ),
    47: FieldDefinition(
        field_index=47,
        field_name="Total Charges",
        data_type="NM",
        length=12,
        description="Total charges"
    ),
    48: FieldDefinition(
        field_index=48,
        field_name="Total Adjustments",
        data_type="NM",
        length=12,
        description="Total adjustments"
    ),
    49: FieldDefinition(
        field_index=49,
        field_name="Total Payments",
        data_type="NM",
        length=12,
        description="Total payments"
    ),
    50: FieldDefinition(
        field_index=50,
        field_name="Alternate Visit ID",
        data_type="CX",
        length=250,
        description="Alternate visit ID"
    ),
    51: FieldDefinition(
        field_index=51,
        field_name="Visit Indicator",
        data_type="IS",
        length=1,
        table_binding="0326",
        description="Visit indicator"
    ),
    52: FieldDefinition(
        field_index=52,
        field_name="Other Healthcare Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Other healthcare provider"
    ),
}


# ============================================================================
# OBR Segment - Observation Request
# ============================================================================

OBR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - OBR",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Placer Order Number",
        data_type="EI",
        length=427,
        description="Placer order number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Filler Order Number",
        data_type="EI",
        length=427,
        description="Filler order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Universal Service Identifier",
        data_type="CWE",
        length=250,
        required=True,
        description="Universal service identifier (required)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Priority - OBR",
        data_type="ID",
        length=2,
        table_binding="0027",
        description="Priority"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Requested Date/Time",
        data_type="TS",
        length=26,
        description="Requested date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Observation Date/Time",
        data_type="TS",
        length=26,
        description="Observation date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Observation End Date/Time",
        data_type="TS",
        length=26,
        description="Observation end date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Collection Volume",
        data_type="CQ",
        length=20,
        description="Collection volume"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Collector Identifier",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Collector identifier"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Specimen Action Code",
        data_type="ID",
        length=1,
        table_binding="0065",
        description="Specimen action code"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Danger Code",
        data_type="CE",
        length=250,
        description="Danger code"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Relevant Clinical Information",
        data_type="ST",
        length=300,
        description="Relevant clinical information"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Specimen Received Date/Time",
        data_type="TS",
        length=26,
        description="Specimen received date/time"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Specimen Source",
        data_type="SPS",
        length=300,
        description="Specimen source"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Ordering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Ordering provider"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Order Callback Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Order callback phone number"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Placer Field 1",
        data_type="ST",
        length=60,
        description="Placer field 1"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Placer Field 2",
        data_type="ST",
        length=60,
        description="Placer field 2"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Filler Field 1",
        data_type="ST",
        length=60,
        description="Filler field 1"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Filler Field 2",
        data_type="ST",
        length=60,
        description="Filler field 2"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Results Rpt/Status Chng - Date/Time",
        data_type="TS",
        length=26,
        description="Results report/status change date/time"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Charge to Practice",
        data_type="MOC",
        length=40,
        description="Charge to practice"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Diagnostic Serv Sect ID",
        data_type="ID",
        length=10,
        table_binding="0074",
        description="Diagnostic service section ID"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Result Status",
        data_type="ID",
        length=1,
        table_binding="0123",
        description="Result status"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Parent Result",
        data_type="PRL",
        length=200,
        description="Parent result"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        repeating=True,
        description="Quantity/timing"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Result Copies To",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Result copies to"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Parent",
        data_type="EIP",
        length=200,
        description="Parent"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Transportation Mode",
        data_type="ID",
        length=4,
        table_binding="0124",
        description="Transportation mode"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Reason for Study",
        data_type="CE",
        length=250,
        repeating=True,
        description="Reason for study"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Principal Result Interpreter",
        data_type="NDL",
        length=200,
        description="Principal result interpreter"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Assistant Result Interpreter",
        data_type="NDL",
        length=200,
        repeating=True,
        description="Assistant result interpreter"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Technician",
        data_type="NDL",
        length=200,
        repeating=True,
        description="Technician"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Transcriptionist",
        data_type="NDL",
        length=200,
        repeating=True,
        description="Transcriptionist"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Scheduled Date/Time",
        data_type="TS",
        length=26,
        description="Scheduled date/time"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Number of Sample Containers",
        data_type="NM",
        length=4,
        description="Number of sample containers"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Transport Logistics of Collected Sample",
        data_type="CE",
        length=250,
        repeating=True,
        description="Transport logistics of collected sample"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Collector's Comment",
        data_type="CE",
        length=250,
        repeating=True,
        description="Collector's comment"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Transport Arrangement Responsibility",
        data_type="CE",
        length=250,
        description="Transport arrangement responsibility"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Transport Arranged",
        data_type="ID",
        length=30,
        table_binding="0224",
        description="Transport arranged"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Escort Required",
        data_type="ID",
        length=1,
        table_binding="0225",
        description="Escort required"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Planned Patient Transport Comment",
        data_type="CE",
        length=250,
        repeating=True,
        description="Planned patient transport comment"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Procedure Code",
        data_type="CE",
        length=250,
        description="Procedure code"
    ),
    45: FieldDefinition(
        field_index=45,
        field_name="Procedure Code Modifier",
        data_type="CE",
        length=250,
        repeating=True,
        description="Procedure code modifier"
    ),
    46: FieldDefinition(
        field_index=46,
        field_name="Placer Supplemental Service Information",
        data_type="CE",
        length=250,
        repeating=True,
        description="Placer supplemental service information"
    ),
    47: FieldDefinition(
        field_index=47,
        field_name="Filler Supplemental Service Information",
        data_type="CE",
        length=250,
        repeating=True,
        description="Filler supplemental service information"
    ),
    48: FieldDefinition(
        field_index=48,
        field_name="Medically Necessary Duplicate Procedure Reason",
        data_type="CWE",
        length=250,
        description="Medically necessary duplicate procedure reason"
    ),
    49: FieldDefinition(
        field_index=49,
        field_name="Result Handling",
        data_type="IS",
        length=2,
        table_binding="0507",
        description="Result handling"
    ),
    50: FieldDefinition(
        field_index=50,
        field_name="Parent Universal Service Identifier",
        data_type="CWE",
        length=250,
        description="Parent universal service identifier"
    ),
}


# ============================================================================
# OBX Segment - Observation/Result
# ============================================================================

OBX_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - OBX",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Value Type",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0125",
        description="Value type (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Observation Identifier",
        data_type="CWE",
        length=250,
        required=True,
        description="Observation identifier (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Observation Sub-ID",
        data_type="ST",
        length=20,
        description="Observation sub-ID"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Observation Value",
        data_type="Varies",
        length=99999,
        repeating=True,
        description="Observation value (varies by value type)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Units",
        data_type="CWE",
        length=250,
        description="Units"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="References Range",
        data_type="ST",
        length=60,
        description="References range"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Interpretation Codes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Interpretation codes"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Probability",
        data_type="NM",
        length=5,
        description="Probability"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Nature of Abnormal Test",
        data_type="ID",
        length=5,
        repeating=True,
        table_binding="0080",
        description="Nature of abnormal test"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Observe Result Status",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0085",
        description="Observe result status (required)"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Date/Time of the Observation",
        data_type="TS",
        length=26,
        description="Date/time of the observation"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Producer's ID",
        data_type="CWE",
        length=250,
        description="Producer's ID"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Responsible Observer",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Responsible observer"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Observation Method",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Observation method"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Equipment Instance Identifier",
        data_type="EI",
        length=427,
        repeating=True,
        description="Equipment instance identifier"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Date/Time of the Analysis",
        data_type="TS",
        length=26,
        description="Date/time of the analysis"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Observation Site",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Observation site"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Observation Instance Identifier",
        data_type="EI",
        length=427,
        description="Observation instance identifier"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Mood Code",
        data_type="CNE",
        length=250,
        description="Mood code"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Performing Organization Name",
        data_type="XON",
        length=250,
        description="Performing organization name"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Performing Organization Address",
        data_type="XAD",
        length=250,
        description="Performing organization address"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Performing Organization Medical Director",
        data_type="XCN",
        length=250,
        description="Performing organization medical director"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Patient Results Release Category",
        data_type="ID",
        length=1,
        table_binding="0490",
        description="Patient results release category"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Root Cause",
        data_type="CWE",
        length=250,
        description="Root cause"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Local Process Control",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Local process control"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Observation Type",
        data_type="CWE",
        length=250,
        description="Observation type"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Performed Start Date/Time",
        data_type="TS",
        length=26,
        description="Performed start date/time"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Performed End Date/Time",
        data_type="TS",
        length=26,
        description="Performed end date/time"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Performed Date/Time",
        data_type="TS",
        length=26,
        description="Performed date/time"
    ),
}


# ============================================================================
# NTE Segment - Notes and Comments
# ============================================================================

NTE_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - NTE",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Source of Comment",
        data_type="ID",
        length=8,
        table_binding="0105",
        description="Source of comment"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Comment",
        data_type="FT",
        length=65536,
        repeating=True,
        description="Comment text"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Comment Type",
        data_type="CWE",
        length=250,
        description="Comment type"
    ),
}


# ============================================================================
# AL1 Segment - Patient Allergy Information
# ============================================================================

AL1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - AL1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Allergen Type Code",
        data_type="CWE",
        length=250,
        table_binding="0127",
        description="Allergen type code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Allergen Code/Mnemonic/Description",
        data_type="CWE",
        length=250,
        required=True,
        description="Allergen code/mnemonic/description (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Allergy Severity Code",
        data_type="CWE",
        length=250,
        table_binding="0128",
        description="Allergy severity code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Allergy Reaction Code",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Allergy reaction code"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Identification Date",
        data_type="DT",
        length=8,
        description="Identification date"
    ),
}


# ============================================================================
# DG1 Segment - Diagnosis
# ============================================================================

DG1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - DG1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Diagnosis Coding Method",
        data_type="ID",
        length=1,
        table_binding="0053",
        description="Diagnosis coding method"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Diagnosis Code - DG1",
        data_type="CWE",
        length=250,
        required=True,
        description="Diagnosis code (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Diagnosis Description",
        data_type="ST",
        length=250,
        description="Diagnosis description"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Diagnosis Date/Time",
        data_type="TS",
        length=26,
        description="Diagnosis date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Diagnosis Type",
        data_type="CWE",
        length=250,
        table_binding="0052",
        description="Diagnosis type"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Major Diagnostic Category",
        data_type="CWE",
        length=250,
        table_binding="0118",
        description="Major diagnostic category"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Diagnostic Related Group",
        data_type="CWE",
        length=250,
        table_binding="0055",
        description="Diagnostic related group"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="DRG Approval Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="DRG approval indicator"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="DRG Grouper Review Code",
        data_type="IS",
        length=2,
        table_binding="0056",
        description="DRG grouper review code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Outlier Type",
        data_type="CWE",
        length=250,
        table_binding="0083",
        description="Outlier type"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Outlier Days",
        data_type="NM",
        length=3,
        description="Outlier days"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Outlier Cost",
        data_type="CP",
        length=12,
        description="Outlier cost"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Grouper Version And Type",
        data_type="ST",
        length=4,
        description="Grouper version and type"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Diagnosis Priority",
        data_type="ID",
        length=2,
        table_binding="0359",
        description="Diagnosis priority"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Diagnosing Clinician",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Diagnosing clinician"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Diagnosis Classification",
        data_type="CWE",
        length=250,
        table_binding="0228",
        description="Diagnosis classification"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Confidential Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Confidential indicator"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Attestation Date/Time",
        data_type="TS",
        length=26,
        description="Attestation date/time"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Diagnosis Identifier",
        data_type="EI",
        length=427,
        description="Diagnosis identifier"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Diagnosis Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Diagnosis action code"
    ),
}


# ============================================================================
# PR1 Segment - Procedures
# ============================================================================

PR1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - PR1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Procedure Coding Method",
        data_type="IS",
        length=3,
        table_binding="0089",
        description="Procedure coding method"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Procedure Code",
        data_type="CWE",
        length=250,
        required=True,
        description="Procedure code (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Procedure Description",
        data_type="ST",
        length=250,
        description="Procedure description"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Procedure Date/Time",
        data_type="TS",
        length=26,
        description="Procedure date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Procedure Functional Type",
        data_type="CWE",
        length=250,
        table_binding="0230",
        description="Procedure functional type"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Procedure Minutes",
        data_type="NM",
        length=4,
        description="Procedure minutes"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Anesthesiologist",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Anesthesiologist"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Anesthesia Code",
        data_type="CWE",
        length=250,
        table_binding="0019",
        description="Anesthesia code"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Anesthesia Minutes",
        data_type="NM",
        length=4,
        description="Anesthesia minutes"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Surgeon",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Surgeon"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Procedure Practitioner",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Procedure practitioner"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Consent Code",
        data_type="CWE",
        length=250,
        table_binding="0059",
        description="Consent code"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Procedure Priority",
        data_type="NM",
        length=2,
        description="Procedure priority"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Associated Diagnosis Code",
        data_type="CWE",
        length=250,
        description="Associated diagnosis code"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Procedure Code Modifier",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Procedure code modifier"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Procedure DRG Type",
        data_type="CWE",
        length=250,
        description="Procedure DRG type"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Tissue Type Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0417",
        description="Tissue type code"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Procedure Identifier",
        data_type="EI",
        length=427,
        description="Procedure identifier"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Procedure Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Procedure action code"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="DRG Procedure Determination Status",
        data_type="CWE",
        length=250,
        table_binding="0761",
        description="DRG procedure determination status"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="DRG Procedure Relevance",
        data_type="CWE",
        length=250,
        table_binding="0762",
        description="DRG procedure relevance"
    ),
}


# ============================================================================
# ORC Segment - Common Order
# ============================================================================

ORC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Placer Order Number",
        data_type="EI",
        length=427,
        description="Placer order number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Filler Order Number",
        data_type="EI",
        length=427,
        description="Filler order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Placer Group Number",
        data_type="EI",
        length=427,
        description="Placer group number"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Order Status",
        data_type="ID",
        length=2,
        table_binding="0038",
        description="Order status"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Response Flag",
        data_type="ID",
        length=1,
        table_binding="0121",
        description="Response flag"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        repeating=True,
        description="Quantity/timing"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Parent",
        data_type="EIP",
        length=200,
        description="Parent"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Date/Time of Transaction",
        data_type="TS",
        length=26,
        description="Date/time of transaction"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Entered By",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Entered by"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Verified By",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Verified by"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Ordering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Ordering provider"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Enterer's Location",
        data_type="PL",
        length=80,
        description="Enterer's location"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Call Back Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Call back phone number"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Order Effective Date/Time",
        data_type="TS",
        length=26,
        description="Order effective date/time"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Order Control Code Reason",
        data_type="CWE",
        length=250,
        description="Order control code reason"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Entering Organization",
        data_type="CWE",
        length=250,
        description="Entering organization"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Entering Device",
        data_type="CWE",
        length=250,
        description="Entering device"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Action By",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Action by"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Advanced Beneficiary Notice Code",
        data_type="CWE",
        length=250,
        table_binding="0339",
        description="Advanced beneficiary notice code"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Ordering Facility Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Ordering facility name"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Ordering Facility Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Ordering facility address"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Ordering Facility Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Ordering facility phone number"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Ordering Provider Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Ordering provider address"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Order Status Modifier",
        data_type="CWE",
        length=250,
        description="Order status modifier"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Advanced Beneficiary Notice Override Reason",
        data_type="CWE",
        length=250,
        table_binding="0552",
        description="Advanced beneficiary notice override reason"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Filler's Expected Availability Date/Time",
        data_type="TS",
        length=26,
        description="Filler's expected availability date/time"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Confidentiality Code",
        data_type="CWE",
        length=250,
        table_binding="0177",
        description="Confidentiality code"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Order Type",
        data_type="CWE",
        length=250,
        table_binding="0482",
        description="Order type"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Enterer Authorization Mode",
        data_type="CNE",
        length=250,
        table_binding="0483",
        description="Enterer authorization mode"
    ),
}


# ============================================================================
# IN1 Segment - Insurance
# ============================================================================

IN1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - IN1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Insurance Plan ID",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0072",
        description="Insurance plan ID (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Insurance Company ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Insurance company ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Insurance Company Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Insurance company name"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Insurance Company Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Insurance company address"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Insurance Co Contact Person",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Insurance company contact person"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Insurance Co Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Insurance company phone number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Group Number",
        data_type="ST",
        length=12,
        description="Group number"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Group Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Group name"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Insured's Group Emp ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Insured's group employee ID"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Insured's Group Emp Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Insured's group employee name"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Plan Effective Date",
        data_type="DT",
        length=8,
        description="Plan effective date"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Plan Expiration Date",
        data_type="DT",
        length=8,
        description="Plan expiration date"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Authorization Information",
        data_type="AUI",
        length=55,
        description="Authorization information"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Plan Type",
        data_type="IS",
        length=3,
        table_binding="0086",
        description="Plan type"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Name Of Insured",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Name of insured"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Insured's Relationship To Patient",
        data_type="CWE",
        length=250,
        table_binding="0063",
        description="Insured's relationship to patient"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Insured's Date/Time Of Birth",
        data_type="TS",
        length=26,
        description="Insured's date/time of birth"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Insured's Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Insured's address"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Assignment Of Benefits",
        data_type="IS",
        length=2,
        table_binding="0135",
        description="Assignment of benefits"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Coordination Of Benefits",
        data_type="IS",
        length=2,
        table_binding="0173",
        description="Coordination of benefits"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Coord Of Ben. Priority",
        data_type="ST",
        length=2,
        description="Coordination of benefits priority"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Notice Of Admission Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Notice of admission flag"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Notice Of Admission Date",
        data_type="DT",
        length=8,
        description="Notice of admission date"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Report Of Eligibility Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Report of eligibility flag"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Report Of Eligibility Date",
        data_type="DT",
        length=8,
        description="Report of eligibility date"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Release Information Code",
        data_type="IS",
        length=2,
        table_binding="0093",
        description="Release information code"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Pre-Admit Cert (PAC)",
        data_type="ST",
        length=15,
        description="Pre-admit certificate"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Verification Date/Time",
        data_type="TS",
        length=26,
        description="Verification date/time"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Verification By",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Verification by"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Type Of Agreement Code",
        data_type="IS",
        length=2,
        table_binding="0098",
        description="Type of agreement code"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Billing Status",
        data_type="IS",
        length=2,
        table_binding="0022",
        description="Billing status"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Lifetime Reserve Days",
        data_type="NM",
        length=4,
        description="Lifetime reserve days"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Delay Before L.R. Day",
        data_type="NM",
        length=4,
        description="Delay before lifetime reserve day"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Company Plan Code",
        data_type="IS",
        length=8,
        table_binding="0042",
        description="Company plan code"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Policy Number",
        data_type="ST",
        length=15,
        description="Policy number"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Policy Deductible",
        data_type="CP",
        length=12,
        description="Policy deductible"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Policy Limit - Amount",
        data_type="CP",
        length=12,
        description="Policy limit amount"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Policy Limit - Days",
        data_type="NM",
        length=4,
        description="Policy limit days"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Room Rate - Semi-Private",
        data_type="CP",
        length=12,
        description="Room rate semi-private"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Room Rate - Private",
        data_type="CP",
        length=12,
        description="Room rate private"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Insured's Employment Status",
        data_type="CWE",
        length=250,
        table_binding="0066",
        description="Insured's employment status"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Insured's Administrative Sex",
        data_type="CWE",
        length=250,
        table_binding="0001",
        description="Insured's administrative sex"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Insured's Employer Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Insured's employer address"
    ),
    45: FieldDefinition(
        field_index=45,
        field_name="Verification Status",
        data_type="ST",
        length=2,
        description="Verification status"
    ),
    46: FieldDefinition(
        field_index=46,
        field_name="Prior Insurance Plan ID",
        data_type="IS",
        length=8,
        table_binding="0072",
        description="Prior insurance plan ID"
    ),
    47: FieldDefinition(
        field_index=47,
        field_name="Coverage Type",
        data_type="IS",
        length=3,
        table_binding="0309",
        description="Coverage type"
    ),
    48: FieldDefinition(
        field_index=48,
        field_name="Handicap",
        data_type="IS",
        length=2,
        table_binding="0295",
        description="Handicap"
    ),
    49: FieldDefinition(
        field_index=49,
        field_name="Insured's ID Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Insured's ID number"
    ),
    50: FieldDefinition(
        field_index=50,
        field_name="Signature Code",
        data_type="IS",
        length=1,
        table_binding="0535",
        description="Signature code"
    ),
    51: FieldDefinition(
        field_index=51,
        field_name="Signature Code Date",
        data_type="DT",
        length=8,
        description="Signature code date"
    ),
    52: FieldDefinition(
        field_index=52,
        field_name="Insured's Birth Place",
        data_type="ST",
        length=250,
        description="Insured's birth place"
    ),
    53: FieldDefinition(
        field_index=53,
        field_name="VIP Indicator",
        data_type="IS",
        length=2,
        table_binding="0099",
        description="VIP indicator"
    ),
}


# ============================================================================
# IN2 Segment - Insurance Additional Information
# ============================================================================

IN2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Insured's Employee ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Insured's employee ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Insured's Social Security Number",
        data_type="ST",
        length=11,
        description="Insured's social security number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Insured's Employer's Name and ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Insured's employer's name and ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Employer Information Data",
        data_type="IS",
        length=1,
        table_binding="0139",
        description="Employer information data"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Mail Claim Party",
        data_type="IS",
        length=1,
        table_binding="0137",
        description="Mail claim party"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Medicare Health Ins Card Number",
        data_type="ST",
        length=15,
        description="Medicare health insurance card number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Medicaid Case Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Medicaid case name"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Medicaid Case Number",
        data_type="ST",
        length=15,
        description="Medicaid case number"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Military Sponsor Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Military sponsor name"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Military ID Number",
        data_type="ST",
        length=20,
        description="Military ID number"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Dependent Of Military Personnel",
        data_type="CE",
        length=250,
        table_binding="0342",
        description="Dependent of military personnel"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Military Organization",
        data_type="ST",
        length=25,
        description="Military organization"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Military Station",
        data_type="ST",
        length=25,
        description="Military station"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Military Service",
        data_type="IS",
        length=14,
        table_binding="0140",
        description="Military service"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Military Rank/Grade",
        data_type="IS",
        length=2,
        table_binding="0141",
        description="Military rank/grade"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Military Status",
        data_type="IS",
        length=3,
        table_binding="0142",
        description="Military status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Retirement Date",
        data_type="DT",
        length=8,
        description="Retirement date"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Death Date",
        data_type="DT",
        length=8,
        description="Death date"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Military Non-Availability Statement On File",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Military non-availability statement on file"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Baby Coverage",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Baby coverage"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Combine Baby Bill",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Combine baby bill"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Blood Deductible",
        data_type="ST",
        length=1,
        description="Blood deductible"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Special Coverage Approval Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Special coverage approval name"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Special Coverage Approval Title",
        data_type="ST",
        length=30,
        description="Special coverage approval title"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Non-Covered Insurance Code",
        data_type="IS",
        length=8,
        table_binding="0143",
        description="Non-covered insurance code"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Payor ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Payor ID"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Payor Subscriber ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Payor subscriber ID"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Eligibility Source",
        data_type="IS",
        length=1,
        table_binding="0144",
        description="Eligibility source"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Room Coverage Type/Amount",
        data_type="RMC",
        length=25,
        repeating=True,
        description="Room coverage type/amount"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Policy Type/Amount",
        data_type="PTA",
        length=25,
        repeating=True,
        description="Policy type/amount"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Daily Deductible",
        data_type="DDI",
        length=25,
        description="Daily deductible"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Living Dependency",
        data_type="IS",
        length=2,
        table_binding="0223",
        description="Living dependency"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Ambulatory Status",
        data_type="IS",
        length=2,
        table_binding="0009",
        description="Ambulatory status"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Citizenship",
        data_type="CE",
        length=250,
        table_binding="0171",
        description="Citizenship"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Primary Language",
        data_type="CE",
        length=250,
        table_binding="0296",
        description="Primary language"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Living Arrangement",
        data_type="IS",
        length=2,
        table_binding="0220",
        description="Living arrangement"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Publicity Code",
        data_type="CE",
        length=250,
        table_binding="0215",
        description="Publicity code"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Protection Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Protection indicator"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Student Indicator",
        data_type="IS",
        length=2,
        table_binding="0231",
        description="Student indicator"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Religion",
        data_type="CE",
        length=250,
        table_binding="0006",
        description="Religion"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Mother's maiden name"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Nationality",
        data_type="CE",
        length=250,
        table_binding="0212",
        description="Nationality"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Ethnic Group",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0189",
        description="Ethnic group"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Marital Status",
        data_type="CE",
        length=250,
        table_binding="0002",
        description="Marital status"
    ),
    45: FieldDefinition(
        field_index=45,
        field_name="Insured's Employment Start Date",
        data_type="DT",
        length=8,
        description="Insured's employment start date"
    ),
    46: FieldDefinition(
        field_index=46,
        field_name="Employment Stop Date",
        data_type="DT",
        length=8,
        description="Employment stop date"
    ),
    47: FieldDefinition(
        field_index=47,
        field_name="Job Title",
        data_type="ST",
        length=20,
        description="Job title"
    ),
    48: FieldDefinition(
        field_index=48,
        field_name="Job Code/Class",
        data_type="JCC",
        length=20,
        description="Job code/class"
    ),
    49: FieldDefinition(
        field_index=49,
        field_name="Job Status",
        data_type="IS",
        length=2,
        table_binding="0311",
        description="Job status"
    ),
    50: FieldDefinition(
        field_index=50,
        field_name="Employer Contact Person Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Employer contact person name"
    ),
    51: FieldDefinition(
        field_index=51,
        field_name="Employer Contact Person Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Employer contact person phone number"
    ),
    52: FieldDefinition(
        field_index=52,
        field_name="Employer Contact Reason",
        data_type="IS",
        length=2,
        table_binding="0222",
        description="Employer contact reason"
    ),
    53: FieldDefinition(
        field_index=53,
        field_name="Insured's Contact Person's Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Insured's contact person's name"
    ),
    54: FieldDefinition(
        field_index=54,
        field_name="Insured's Contact Person Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Insured's contact person phone number"
    ),
    55: FieldDefinition(
        field_index=55,
        field_name="Insured's Contact Person Reason",
        data_type="IS",
        length=2,
        table_binding="0222",
        description="Insured's contact person reason"
    ),
    56: FieldDefinition(
        field_index=56,
        field_name="Relationship To The Patient Start Date",
        data_type="DT",
        length=8,
        description="Relationship to the patient start date"
    ),
    57: FieldDefinition(
        field_index=57,
        field_name="Relationship To The Patient Stop Date",
        data_type="DT",
        length=8,
        description="Relationship to the patient stop date"
    ),
    58: FieldDefinition(
        field_index=58,
        field_name="Insurance Co Contact Reason",
        data_type="IS",
        length=2,
        table_binding="0232",
        description="Insurance co contact reason"
    ),
    59: FieldDefinition(
        field_index=59,
        field_name="Insurance Co Contact Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Insurance co contact phone number"
    ),
    60: FieldDefinition(
        field_index=60,
        field_name="Policy Scope",
        data_type="IS",
        length=2,
        table_binding="0443",
        description="Policy scope"
    ),
    61: FieldDefinition(
        field_index=61,
        field_name="Policy Source",
        data_type="IS",
        length=2,
        table_binding="0444",
        description="Policy source"
    ),
    62: FieldDefinition(
        field_index=62,
        field_name="Patient Member Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Patient member number"
    ),
    63: FieldDefinition(
        field_index=63,
        field_name="Guarantor's Relationship To Insured",
        data_type="CE",
        length=250,
        table_binding="0063",
        description="Guarantor's relationship to insured"
    ),
    64: FieldDefinition(
        field_index=64,
        field_name="Insured's Phone Number - Home",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Insured's phone number - home"
    ),
    65: FieldDefinition(
        field_index=65,
        field_name="Insured's Employer Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Insured's employer phone number"
    ),
    66: FieldDefinition(
        field_index=66,
        field_name="Military Handicapped Program",
        data_type="CE",
        length=250,
        table_binding="0343",
        description="Military handicapped program"
    ),
    67: FieldDefinition(
        field_index=67,
        field_name="Suspend Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Suspend flag"
    ),
    68: FieldDefinition(
        field_index=68,
        field_name="Copay Limit Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Copay limit flag"
    ),
    69: FieldDefinition(
        field_index=69,
        field_name="Stoploss Limit Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Stoploss limit flag"
    ),
    70: FieldDefinition(
        field_index=70,
        field_name="Insured Organization Name And ID",
        data_type="XON",
        length=250,
        repeating=True,
        description="Insured organization name and ID"
    ),
    71: FieldDefinition(
        field_index=71,
        field_name="Insured Employer Organization Name And ID",
        data_type="XON",
        length=250,
        repeating=True,
        description="Insured employer organization name and ID"
    ),
    72: FieldDefinition(
        field_index=72,
        field_name="Race",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0005",
        description="Race"
    ),
    73: FieldDefinition(
        field_index=73,
        field_name="Patient's Relationship To Insured",
        data_type="CE",
        length=250,
        table_binding="0063",
        description="Patient's relationship to insured"
    ),
    74: FieldDefinition(
        field_index=74,
        field_name="Patient's Relationship To Insured Start Date",
        data_type="DT",
        length=8,
        description="Patient's relationship to insured start date"
    ),
    75: FieldDefinition(
        field_index=75,
        field_name="Patient's Relationship To Insured Stop Date",
        data_type="DT",
        length=8,
        description="Patient's relationship to insured stop date"
    ),
    76: FieldDefinition(
        field_index=76,
        field_name="Insured's Contact Person's Social Security Number",
        data_type="ST",
        length=11,
        description="Insured's contact person's social security number"
    ),
    77: FieldDefinition(
        field_index=77,
        field_name="Insured's Contact Person Relationship To Insured",
        data_type="CE",
        length=250,
        table_binding="0063",
        description="Insured's contact person relationship to insured"
    ),
    78: FieldDefinition(
        field_index=78,
        field_name="Patient Birth Place",
        data_type="ST",
        length=250,
        description="Patient birth place"
    ),
    79: FieldDefinition(
        field_index=79,
        field_name="VIP Indicator",
        data_type="IS",
        length=2,
        table_binding="0099",
        description="VIP indicator"
    ),
    80: FieldDefinition(
        field_index=80,
        field_name="Insured's ID Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Insured's ID number"
    ),
    81: FieldDefinition(
        field_index=81,
        field_name="Insurance Plan Type",
        data_type="CE",
        length=250,
        table_binding="0203",
        description="Insurance plan type"
    ),
    82: FieldDefinition(
        field_index=82,
        field_name="Coverage Type",
        data_type="IS",
        length=3,
        table_binding="0309",
        description="Coverage type"
    ),
    83: FieldDefinition(
        field_index=83,
        field_name="Handicap",
        data_type="CE",
        length=250,
        table_binding="0295",
        description="Handicap"
    ),
    84: FieldDefinition(
        field_index=84,
        field_name="Insured's Secondary Medicare ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Insured's secondary Medicare ID"
    ),
    85: FieldDefinition(
        field_index=85,
        field_name="Supplemental Insurance Eligibility",
        data_type="CE",
        length=250,
        table_binding="0384",
        description="Supplemental insurance eligibility"
    ),
    86: FieldDefinition(
        field_index=86,
        field_name="Resource Link",
        data_type="EI",
        length=60,
        repeating=True,
        description="Resource link"
    ),
    87: FieldDefinition(
        field_index=87,
        field_name="Other Insured's Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Other insured's name"
    ),
    88: FieldDefinition(
        field_index=88,
        field_name="Other Insured's Policy Number",
        data_type="ST",
        length=50,
        description="Other insured's policy number"
    ),
    89: FieldDefinition(
        field_index=89,
        field_name="Other Insured's Date Of Birth",
        data_type="TS",
        length=26,
        description="Other insured's date of birth"
    ),
    90: FieldDefinition(
        field_index=90,
        field_name="Other Insured's Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Other insured's address"
    ),
}


# ============================================================================
# IN3 Segment - Insurance Additional Information - Certification
# ============================================================================

IN3_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - IN3",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Certification Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Certification number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Certified By",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Certified by"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Certification Required",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Certification required"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Penalty",
        data_type="MOP",
        length=10,
        description="Penalty"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Certification Date/Time",
        data_type="TS",
        length=26,
        description="Certification date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Certification Modify Date/Time",
        data_type="TS",
        length=26,
        description="Certification modify date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Operator",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Operator"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Certification Begin Date",
        data_type="DT",
        length=8,
        description="Certification begin date"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Certification End Date",
        data_type="DT",
        length=8,
        description="Certification end date"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Days",
        data_type="DTN",
        length=5,
        description="Days"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Non-Concur Code/Description",
        data_type="CE",
        length=250,
        table_binding="0233",
        description="Non-concur code/description"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Non-Concur Effective Date/Time",
        data_type="TS",
        length=26,
        description="Non-concur effective date/time"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Physician Reviewer",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Physician reviewer"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Certification Contact",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Certification contact"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Certification Contact Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Certification contact phone number"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Appeal Reason",
        data_type="CE",
        length=250,
        table_binding="0344",
        description="Appeal reason"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Certification Agency",
        data_type="CE",
        length=250,
        table_binding="0345",
        description="Certification agency"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Certification Agency Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Certification agency phone number"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Pre-Certification Requirement",
        data_type="ICD",
        length=40,
        repeating=True,
        description="Pre-certification requirement"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Case Manager",
        data_type="ST",
        length=15,
        description="Case manager"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Second Opinion Date",
        data_type="DT",
        length=8,
        description="Second opinion date"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Second Opinion Status",
        data_type="IS",
        length=1,
        table_binding="0151",
        description="Second opinion status"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Second Opinion Documentation Received",
        data_type="IS",
        length=1,
        table_binding="0152",
        description="Second opinion documentation received"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Second Opinion Physician",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Second opinion physician"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Certification Type",
        data_type="CE",
        length=250,
        table_binding="0346",
        description="Certification type"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Certification Category",
        data_type="CE",
        length=250,
        table_binding="0347",
        description="Certification category"
    ),
}


# ============================================================================
# NK1 Segment - Next of Kin / Associated Parties
# ============================================================================

NK1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - NK1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Name"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Relationship",
        data_type="CWE",
        length=250,
        table_binding="0063",
        description="Relationship"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Address"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Business Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Business phone number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Contact Role",
        data_type="CWE",
        length=250,
        table_binding="0131",
        description="Contact role"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Start Date",
        data_type="DT",
        length=8,
        description="Start date"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="End Date",
        data_type="DT",
        length=8,
        description="End date"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Next of Kin / Associated Parties Job Title",
        data_type="ST",
        length=60,
        description="Job title"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Next of Kin / Associated Parties Job Code/Class",
        data_type="JCC",
        length=20,
        description="Job code/class"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Next of Kin / Associated Parties Employee Number",
        data_type="CX",
        length=250,
        description="Employee number"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Organization Name - NK1",
        data_type="XON",
        length=250,
        repeating=True,
        description="Organization name"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Marital Status",
        data_type="CWE",
        length=250,
        table_binding="0002",
        description="Marital status"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Administrative Sex",
        data_type="CWE",
        length=250,
        table_binding="0001",
        description="Administrative sex"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Date/Time of Birth",
        data_type="TS",
        length=26,
        description="Date/time of birth"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Living Dependency",
        data_type="CWE",
        length=250,
        table_binding="0223",
        description="Living dependency"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Ambulatory Status",
        data_type="CWE",
        length=250,
        table_binding="0009",
        repeating=True,
        description="Ambulatory status"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Citizenship",
        data_type="CWE",
        length=250,
        table_binding="0171",
        repeating=True,
        description="Citizenship"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Primary Language",
        data_type="CWE",
        length=250,
        description="Primary language"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Living Arrangement",
        data_type="CWE",
        length=250,
        table_binding="0220",
        description="Living arrangement"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Publicity Code",
        data_type="CWE",
        length=250,
        table_binding="0215",
        description="Publicity code"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Protection Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Protection indicator"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Student Indicator",
        data_type="CWE",
        length=250,
        table_binding="0231",
        description="Student indicator"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Religion",
        data_type="CWE",
        length=250,
        table_binding="0006",
        description="Religion"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Mother's maiden name"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Nationality",
        data_type="CWE",
        length=250,
        table_binding="0212",
        description="Nationality"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Ethnic Group",
        data_type="CWE",
        length=250,
        table_binding="0189",
        repeating=True,
        description="Ethnic group"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Contact Reason",
        data_type="CWE",
        length=250,
        table_binding="0022",
        description="Contact reason"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Contact Person's Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Contact person's name"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Contact Person's Telephone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Contact person's telephone number"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Contact Person's Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Contact person's address"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Next of Kin/Associated Party's Identifiers",
        data_type="CX",
        length=250,
        repeating=True,
        description="Identifiers"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Job Status",
        data_type="CWE",
        length=250,
        table_binding="0311",
        description="Job status"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Race",
        data_type="CWE",
        length=250,
        table_binding="0005",
        repeating=True,
        description="Race"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Handicap",
        data_type="CWE",
        length=250,
        table_binding="0295",
        description="Handicap"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Contact Person Social Security Number",
        data_type="ST",
        length=11,
        description="Contact person social security number"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Next of Kin Birth Place",
        data_type="ST",
        length=250,
        description="Birth place"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="VIP Indicator",
        data_type="CWE",
        length=250,
        table_binding="0099",
        description="VIP indicator"
    ),
}


# ============================================================================
# PD1 Segment - Patient Additional Demographic
# ============================================================================

PD1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Living Dependency",
        data_type="CWE",
        length=250,
        table_binding="0223",
        description="Living dependency"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Living Arrangement",
        data_type="CWE",
        length=250,
        table_binding="0220",
        description="Living arrangement"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient Primary Facility",
        data_type="XON",
        length=250,
        repeating=True,
        description="Patient primary facility"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Patient Primary Care Provider Name & ID No.",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Patient primary care provider name and ID number"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Student Indicator",
        data_type="CWE",
        length=250,
        table_binding="0231",
        description="Student indicator"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Handicap",
        data_type="CWE",
        length=250,
        table_binding="0295",
        description="Handicap"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Living Will Code",
        data_type="CWE",
        length=250,
        table_binding="0315",
        description="Living will code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Organ Donor Code",
        data_type="CWE",
        length=250,
        table_binding="0316",
        description="Organ donor code"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Separate Bill",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Separate bill"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Duplicate Patient",
        data_type="CX",
        length=250,
        repeating=True,
        description="Duplicate patient"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Publicity Code",
        data_type="CWE",
        length=250,
        table_binding="0215",
        description="Publicity code"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Protection Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Protection indicator"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Protection Indicator Effective Date",
        data_type="DT",
        length=8,
        description="Protection indicator effective date"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Place of Worship",
        data_type="XON",
        length=250,
        repeating=True,
        description="Place of worship"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Advance Directive Code",
        data_type="CWE",
        length=250,
        table_binding="0435",
        repeating=True,
        description="Advance directive code"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Immunization Registry Status",
        data_type="CWE",
        length=250,
        table_binding="0441",
        description="Immunization registry status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Immunization Registry Status Effective Date",
        data_type="DT",
        length=8,
        description="Immunization registry status effective date"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Publicity Code Effective Date",
        data_type="DT",
        length=8,
        description="Publicity code effective date"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Military Branch",
        data_type="CWE",
        length=250,
        table_binding="0140",
        description="Military branch"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Military Rank/Grade",
        data_type="CWE",
        length=250,
        table_binding="0141",
        description="Military rank/grade"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Military Status",
        data_type="CWE",
        length=250,
        table_binding="0142",
        description="Military status"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Advance Directive Last Verified Date",
        data_type="DT",
        length=8,
        description="Advance directive last verified date"
    ),
}


# ============================================================================
# PV2 Segment - Patient Visit - Additional Information
# ============================================================================

PV2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Prior Pending Location",
        data_type="PL",
        length=80,
        description="Prior pending location"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Accommodation Code",
        data_type="CWE",
        length=250,
        table_binding="0013",
        description="Accommodation code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Admit Reason",
        data_type="CWE",
        length=250,
        description="Admit reason"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Transfer Reason",
        data_type="CWE",
        length=250,
        description="Transfer reason"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Patient Valuables",
        data_type="ST",
        length=25,
        repeating=True,
        description="Patient valuables"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Patient Valuables Location",
        data_type="ST",
        length=25,
        description="Patient valuables location"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Visit User Code",
        data_type="IS",
        length=3,
        table_binding="0130",
        description="Visit user code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Expected Admit Date/Time",
        data_type="TS",
        length=26,
        description="Expected admit date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Expected Discharge Date/Time",
        data_type="TS",
        length=26,
        description="Expected discharge date/time"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Estimated Length Of Stay (In Days)",
        data_type="NM",
        length=3,
        description="Estimated length of stay in days"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Actual Length Of Stay (In Days)",
        data_type="NM",
        length=3,
        description="Actual length of stay in days"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Visit Description",
        data_type="ST",
        length=50,
        description="Visit description"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Referral Source Code",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Referral source code"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Previous Service Date",
        data_type="DT",
        length=8,
        description="Previous service date"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Employment Illness Related Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Employment illness related indicator"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Purge Status Code",
        data_type="IS",
        length=1,
        table_binding="0213",
        description="Purge status code"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Purge Status Date",
        data_type="DT",
        length=8,
        description="Purge status date"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Special Program Code",
        data_type="IS",
        length=2,
        table_binding="0214",
        description="Special program code"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Retention Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Retention indicator"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Expected Number of Insurance Plans",
        data_type="NM",
        length=1,
        description="Expected number of insurance plans"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Visit Publicity Code",
        data_type="IS",
        length=1,
        table_binding="0215",
        description="Visit publicity code"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Visit Protection Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Visit protection indicator"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Clinic Organization Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Clinic organization name"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Patient Status Code",
        data_type="IS",
        length=2,
        table_binding="0216",
        description="Patient status code"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Visit Priority Code",
        data_type="IS",
        length=1,
        table_binding="0217",
        description="Visit priority code"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Previous Treatment Date",
        data_type="DT",
        length=8,
        description="Previous treatment date"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Expected Discharge Disposition",
        data_type="CWE",
        length=250,
        table_binding="0112",
        description="Expected discharge disposition"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Signature on File Date",
        data_type="DT",
        length=8,
        description="Signature on file date"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="First Similar Illness Date",
        data_type="DT",
        length=8,
        description="First similar illness date"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Patient Charge Adjustment Code",
        data_type="CWE",
        length=250,
        table_binding="0218",
        description="Patient charge adjustment code"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Recurring Service Code",
        data_type="IS",
        length=2,
        table_binding="0219",
        description="Recurring service code"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Billing Media Code",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Billing media code"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Expected Surgery Date & Time",
        data_type="TS",
        length=26,
        description="Expected surgery date and time"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Military Partnership Code",
        data_type="ID",
        length=1,
        table_binding="0268",
        description="Military partnership code"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Military Non-Availability Code",
        data_type="ID",
        length=1,
        table_binding="0269",
        description="Military non-availability code"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Newborn Baby Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Newborn baby indicator"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Baby Detained Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Baby detained indicator"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Mode Of Arrival Code",
        data_type="CWE",
        length=250,
        table_binding="0430",
        description="Mode of arrival code"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Recreational Drug Use Code",
        data_type="CWE",
        length=250,
        table_binding="0431",
        repeating=True,
        description="Recreational drug use code"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Admission Level Of Care Code",
        data_type="CWE",
        length=250,
        table_binding="0432",
        description="Admission level of care code"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Precaution Code",
        data_type="CWE",
        length=250,
        table_binding="0433",
        repeating=True,
        description="Precaution code"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Patient Condition Code",
        data_type="CWE",
        length=250,
        table_binding="0434",
        description="Patient condition code"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Living Will Code",
        data_type="IS",
        length=2,
        table_binding="0315",
        description="Living will code"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Organ Donor Code",
        data_type="IS",
        length=2,
        table_binding="0316",
        description="Organ donor code"
    ),
    45: FieldDefinition(
        field_index=45,
        field_name="Advance Directive Code",
        data_type="CWE",
        length=250,
        table_binding="0435",
        repeating=True,
        description="Advance directive code"
    ),
    46: FieldDefinition(
        field_index=46,
        field_name="Patient Status Effective Date",
        data_type="DT",
        length=8,
        description="Patient status effective date"
    ),
    47: FieldDefinition(
        field_index=47,
        field_name="Expected LOA Return Date/Time",
        data_type="TS",
        length=26,
        description="Expected leave of absence return date/time"
    ),
    48: FieldDefinition(
        field_index=48,
        field_name="Expected Pre-Admission Testing Date/Time",
        data_type="TS",
        length=26,
        description="Expected pre-admission testing date/time"
    ),
    49: FieldDefinition(
        field_index=49,
        field_name="Notify Clergy Code",
        data_type="IS",
        length=20,
        table_binding="0534",
        description="Notify clergy code"
    ),
    50: FieldDefinition(
        field_index=50,
        field_name="Advance Directive Last Verified Date",
        data_type="DT",
        length=8,
        description="Advance directive last verified date"
    ),
}


# ============================================================================
# GT1 Segment - Guarantor
# ============================================================================

GT1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - GT1",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Guarantor Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Guarantor identifier(s)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Guarantor Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Guarantor name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Guarantor Spouse Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Guarantor spouse name"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Guarantor Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Guarantor address"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Guarantor Phone Number - Home",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Guarantor home phone number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Guarantor Phone Number - Business",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Guarantor business phone number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Guarantor Date/Time of Birth",
        data_type="TS",
        length=26,
        description="Guarantor date/time of birth"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Guarantor Administrative Sex",
        data_type="IS",
        length=1,
        table_binding="0001",
        description="Guarantor sex (M=Male, F=Female, O=Other, U=Unknown)"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Guarantor Type",
        data_type="IS",
        length=2,
        table_binding="0068",
        description="Guarantor type"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Guarantor Relationship",
        data_type="CE",
        length=250,
        table_binding="0063",
        description="Guarantor relationship to patient"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Guarantor SSN",
        data_type="ST",
        length=11,
        description="Guarantor Social Security Number"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Guarantor Date - Begin",
        data_type="DT",
        length=8,
        description="Guarantor coverage begin date"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Guarantor Date - End",
        data_type="DT",
        length=8,
        description="Guarantor coverage end date"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Guarantor Priority",
        data_type="NM",
        length=2,
        description="Guarantor priority (1=Primary, 2=Secondary, etc.)"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Guarantor Employer Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Guarantor employer name"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Guarantor Employer Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Guarantor employer address"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Guarantor Employer Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Guarantor employer phone number"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Guarantor Employee ID Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Guarantor employee ID number"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Guarantor Employment Status",
        data_type="IS",
        length=2,
        table_binding="0066",
        description="Guarantor employment status"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Guarantor Organization Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Guarantor organization name"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Guarantor Billing Hold Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Billing hold flag (Y=Yes, N=No)"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Guarantor Credit Rating Code",
        data_type="CE",
        length=250,
        description="Guarantor credit rating code"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Guarantor Death Date and Time",
        data_type="TS",
        length=26,
        description="Guarantor death date and time"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Guarantor Death Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Death flag (Y=Yes, N=No)"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Guarantor Charge Adjustment Code",
        data_type="CE",
        length=250,
        description="Charge adjustment code"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Guarantor Household Annual Income",
        data_type="CP",
        length=12,
        description="Household annual income"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Guarantor Household Size",
        data_type="NM",
        length=3,
        description="Household size"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Guarantor Employer ID Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Guarantor employer ID number"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Guarantor Marital Status Code",
        data_type="CE",
        length=250,
        table_binding="0002",
        description="Marital status code"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Guarantor Hire Effective Date",
        data_type="DT",
        length=8,
        description="Hire effective date"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Employment Stop Date",
        data_type="DT",
        length=8,
        description="Employment stop date"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Living Dependency",
        data_type="IS",
        length=2,
        table_binding="0223",
        description="Living dependency code"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Ambulatory Status",
        data_type="IS",
        length=2,
        table_binding="0009",
        description="Ambulatory status code"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Citizenship",
        data_type="CE",
        length=250,
        table_binding="0171",
        repeating=True,
        description="Citizenship code"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Primary Language",
        data_type="CE",
        length=250,
        table_binding="0296",
        description="Primary language code"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Living Arrangement",
        data_type="IS",
        length=1,
        table_binding="0220",
        description="Living arrangement code"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Publicity Code",
        data_type="CE",
        length=250,
        table_binding="0215",
        description="Publicity code"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Protection Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Protection indicator (Y=Yes, N=No)"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Student Indicator",
        data_type="IS",
        length=1,
        table_binding="0231",
        description="Student indicator"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Religion",
        data_type="CE",
        length=250,
        table_binding="0006",
        description="Religion code"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Mother's maiden name"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Nationality",
        data_type="CE",
        length=250,
        table_binding="0212",
        description="Nationality code"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Ethnic Group",
        data_type="CE",
        length=250,
        table_binding="0189",
        repeating=True,
        description="Ethnic group code"
    ),
    45: FieldDefinition(
        field_index=45,
        field_name="Contact Person's Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Contact person's name"
    ),
    46: FieldDefinition(
        field_index=46,
        field_name="Contact Person's Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Contact person's phone number"
    ),
    47: FieldDefinition(
        field_index=47,
        field_name="Contact Reason",
        data_type="CE",
        length=250,
        table_binding="0222",
        description="Contact reason code"
    ),
    48: FieldDefinition(
        field_index=48,
        field_name="Contact Relationship",
        data_type="IS",
        length=2,
        table_binding="0063",
        description="Contact relationship code"
    ),
    49: FieldDefinition(
        field_index=49,
        field_name="Job Title",
        data_type="ST",
        length=20,
        description="Job title"
    ),
    50: FieldDefinition(
        field_index=50,
        field_name="Job Code/Class",
        data_type="JCC",
        length=20,
        description="Job code/class"
    ),
    51: FieldDefinition(
        field_index=51,
        field_name="Guarantor Employer's Organization Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Guarantor employer's organization name"
    ),
    52: FieldDefinition(
        field_index=52,
        field_name="Handicap",
        data_type="IS",
        length=2,
        table_binding="0295",
        description="Handicap code"
    ),
    53: FieldDefinition(
        field_index=53,
        field_name="Job Status",
        data_type="IS",
        length=2,
        table_binding="0311",
        description="Job status code"
    ),
    54: FieldDefinition(
        field_index=54,
        field_name="Guarantor Financial Class",
        data_type="FC",
        length=50,
        repeating=True,
        description="Guarantor financial class"
    ),
    55: FieldDefinition(
        field_index=55,
        field_name="Guarantor Race",
        data_type="CE",
        length=250,
        table_binding="0005",
        repeating=True,
        description="Guarantor race code"
    ),
    56: FieldDefinition(
        field_index=56,
        field_name="Guarantor Birth Place",
        data_type="ST",
        length=25,
        description="Guarantor birth place"
    ),
    57: FieldDefinition(
        field_index=57,
        field_name="VIP Indicator",
        data_type="IS",
        length=2,
        table_binding="0099",
        description="VIP indicator code"
    ),
}


# ============================================================================
# MSA Segment - Message Acknowledgment
# ============================================================================

MSA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Acknowledgment Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0008",
        description="Acknowledgment code (AA=Application Accept, AE=Application Error, AR=Application Reject)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Message Control ID",
        data_type="ST",
        length=20,
        required=True,
        description="Message control ID from original message (MSH-10)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Text Message",
        data_type="ST",
        length=80,
        description="Text message (optional error/status message)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Expected Sequence Number",
        data_type="NM",
        length=15,
        description="Expected sequence number"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Delayed Acknowledgment Type",
        data_type="ID",
        length=1,
        table_binding="0102",
        description="Delayed acknowledgment type"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Error Condition",
        data_type="CE",
        length=250,
        description="Error condition code"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Message Waiting Number",
        data_type="NM",
        length=20,
        description="Message waiting number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Message Waiting Priority",
        data_type="ID",
        length=1,
        table_binding="0000",
        description="Message waiting priority"
    ),
}


# ============================================================================
# ERR Segment - Error
# ============================================================================

ERR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Error Code and Location",
        data_type="ELD",
        length=493,
        repeating=True,
        description="Error code and location (repeating field)"
    ),
}


# ============================================================================
# QRD Segment - Query Definition (Original-Style)
# ============================================================================

QRD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Query date/time (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Format Code",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0106",
        description="Query format code (R=Record, D=Display, T=Tabular) (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Query Priority",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0091",
        description="Query priority (I=Immediate, D=Deferred) (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Query ID",
        data_type="ST",
        length=10,
        required=True,
        description="Query ID (required)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Deferred Response Type",
        data_type="ID",
        length=1,
        table_binding="0107",
        description="Deferred response type"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Deferred Response Date/Time",
        data_type="TS",
        length=26,
        description="Deferred response date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Quantity Limited Request",
        data_type="CQ",
        length=10,
        description="Quantity limited request"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Who Subject Filter",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Who subject filter"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="What Subject Filter",
        data_type="CE",
        length=250,
        repeating=True,
        description="What subject filter"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="What Department Data Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="What department data code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="What Data Code Value Qual",
        data_type="VR",
        length=20,
        repeating=True,
        description="What data code value qualifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Query Results Level",
        data_type="ID",
        length=1,
        table_binding="0108",
        description="Query results level"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Where Subject Filter",
        data_type="ST",
        length=20,
        repeating=True,
        description="Where subject filter"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="When Data Start Date/Time",
        data_type="TS",
        length=26,
        description="When data start date/time"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="When Data End Date/Time",
        data_type="TS",
        length=26,
        description="When data end date/time"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="What User Qualifier",
        data_type="ST",
        length=20,
        repeating=True,
        description="What user qualifier"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Other QRY Subject Filter",
        data_type="ST",
        length=20,
        repeating=True,
        description="Other query subject filter"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Which Date/Time Qualifier",
        data_type="ID",
        length=2,
        table_binding="0156",
        description="Which date/time qualifier"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Which Date/Time Status Qualifier",
        data_type="ID",
        length=2,
        table_binding="0157",
        description="Which date/time status qualifier"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Date/Time Selection Qualifier",
        data_type="ID",
        length=2,
        table_binding="0158",
        description="Date/time selection qualifier"
    ),
}


# ============================================================================
# QRF Segment - Query Filter
# ============================================================================

QRF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Where Subject Filter",
        data_type="ST",
        length=20,
        repeating=True,
        description="Where subject filter"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="When Data Start Date/Time",
        data_type="TS",
        length=26,
        description="When data start date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="When Data End Date/Time",
        data_type="TS",
        length=26,
        description="When data end date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="What User Qualifier",
        data_type="ST",
        length=20,
        repeating=True,
        description="What user qualifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Other QRY Subject Filter",
        data_type="ST",
        length=20,
        repeating=True,
        description="Other query subject filter"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Which Date/Time Qualifier",
        data_type="ID",
        length=2,
        table_binding="0156",
        description="Which date/time qualifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Which Date/Time Status Qualifier",
        data_type="ID",
        length=2,
        table_binding="0157",
        description="Which date/time status qualifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Date/Time Selection Qualifier",
        data_type="ID",
        length=2,
        table_binding="0158",
        description="Date/time selection qualifier"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="When Quantity/Timing Qualifier",
        data_type="TQ",
        length=200,
        description="When quantity/timing qualifier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Search Confidence Threshold",
        data_type="NM",
        length=5,
        description="Search confidence threshold"
    ),
}


# ============================================================================
# QAK Segment - Query Acknowledgment
# ============================================================================

QAK_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag (echoes QPD-2 or QRD-4)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Response Status",
        data_type="ID",
        length=2,
        table_binding="0208",
        description="Query response status (OK=Data found, NF=No data found, AE=Application error, AR=Application reject)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        description="Message query name (echoes QPD-1)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Hit Count Total",
        data_type="NM",
        length=10,
        description="Hit count total (total number of matches)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="This payload",
        data_type="NM",
        length=10,
        description="This payload (number of records in this response)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Hits remaining",
        data_type="NM",
        length=10,
        description="Hits remaining (number of records remaining to be sent)"
    ),
}


# ============================================================================
# QPD Segment - Query Parameter Definition (Enhanced)
# ============================================================================

QPD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        required=True,
        description="Message query name (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag (unique identifier for this query)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Stored Procedure Name",
        data_type="CE",
        length=250,
        description="Stored procedure name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Input Parameter List",
        data_type="QIP",
        length=256,
        repeating=True,
        description="Input parameter list (repeating field)"
    ),
}


# ============================================================================
# RGS Segment - Resource Group
# ============================================================================

RGS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - RGS",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Resource Group ID",
        data_type="CE",
        length=250,
        description="Resource group ID"
    ),
}


# ============================================================================
# SPM Segment - Specimen
# ============================================================================

SPM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - SPM",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Specimen ID",
        data_type="EIP",
        length=427,
        repeating=True,
        description="Specimen identifier(s)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Specimen Parent IDs",
        data_type="EIP",
        length=427,
        repeating=True,
        description="Specimen parent identifier(s)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Specimen Type",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0487",
        description="Specimen type (required)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Specimen Type Modifier",
        data_type="CWE",
        length=250,
        table_binding="0541",
        repeating=True,
        description="Specimen type modifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Specimen Additives",
        data_type="CWE",
        length=250,
        table_binding="0371",
        repeating=True,
        description="Specimen additives"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Specimen Collection Method",
        data_type="CWE",
        length=250,
        table_binding="0488",
        description="Specimen collection method"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Specimen Source Site",
        data_type="CWE",
        length=250,
        table_binding="0542",
        description="Specimen source site"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Specimen Source Site Modifier",
        data_type="CWE",
        length=250,
        table_binding="0543",
        repeating=True,
        description="Specimen source site modifier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Specimen Collection Site",
        data_type="CWE",
        length=250,
        table_binding="0544",
        description="Specimen collection site"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Specimen Role",
        data_type="CWE",
        length=250,
        table_binding="0369",
        repeating=True,
        description="Specimen role"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Specimen Collection Amount",
        data_type="CQ",
        length=20,
        description="Specimen collection amount"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Grouped Specimen Count",
        data_type="NM",
        length=4,
        description="Grouped specimen count"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Specimen Description",
        data_type="ST",
        length=200,
        repeating=True,
        description="Specimen description"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Specimen Handling Code",
        data_type="CWE",
        length=250,
        table_binding="0376",
        repeating=True,
        description="Specimen handling code"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Specimen Risk Code",
        data_type="CWE",
        length=250,
        table_binding="0489",
        description="Specimen risk code"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Specimen Collection Date/Time",
        data_type="DR",
        length=53,
        description="Specimen collection date/time"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Specimen Received Date/Time",
        data_type="TS",
        length=26,
        description="Specimen received date/time"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Specimen Expiration Date/Time",
        data_type="TS",
        length=26,
        description="Specimen expiration date/time"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Specimen Availability",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Specimen availability (Y=Yes, N=No)"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Specimen Reject Reason",
        data_type="CWE",
        length=250,
        table_binding="0490",
        repeating=True,
        description="Specimen reject reason"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Specimen Quality",
        data_type="CWE",
        length=250,
        table_binding="0491",
        description="Specimen quality"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Specimen Appropriateness",
        data_type="CWE",
        length=250,
        table_binding="0492",
        description="Specimen appropriateness"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Specimen Condition",
        data_type="CWE",
        length=250,
        table_binding="0493",
        repeating=True,
        description="Specimen condition"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Specimen Current Quantity",
        data_type="CQ",
        length=20,
        description="Specimen current quantity"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Number of Specimen Containers",
        data_type="NM",
        length=4,
        description="Number of specimen containers"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Container Type",
        data_type="CWE",
        length=250,
        table_binding="0322",
        description="Container type"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Container Condition",
        data_type="CWE",
        length=250,
        table_binding="0544",
        description="Container condition"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Specimen Child Role",
        data_type="CWE",
        length=250,
        table_binding="0494",
        description="Specimen child role"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Accession ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Accession identifier(s)"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Other Specimen ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Other specimen identifier(s)"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Shipment ID",
        data_type="EI",
        length=427,
        description="Shipment identifier"
    ),
}


# ============================================================================
# TQ1 Segment - Timing/Quantity
# ============================================================================

TQ1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - TQ1",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Quantity",
        data_type="CQ",
        length=20,
        repeating=True,
        description="Quantity"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Repeat Pattern",
        data_type="RPT",
        length=540,
        repeating=True,
        description="Repeat pattern"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Explicit Time",
        data_type="TM",
        length=16,
        repeating=True,
        description="Explicit time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Relative Time and Units",
        data_type="CQ",
        length=20,
        repeating=True,
        description="Relative time and units"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Service Duration",
        data_type="CQ",
        length=20,
        description="Service duration"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="End Date/Time",
        data_type="TS",
        length=26,
        description="End date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Priority",
        data_type="CWE",
        length=250,
        table_binding="0485",
        description="Priority"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Condition Text",
        data_type="ST",
        length=250,
        description="Condition text"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Text Instruction",
        data_type="ST",
        length=250,
        description="Text instruction"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Conjunction",
        data_type="ID",
        length=1,
        table_binding="0472",
        description="Conjunction (A=And, O=Or)"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Occurrence Duration",
        data_type="CQ",
        length=20,
        description="Occurrence duration"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Total Occurrences",
        data_type="NM",
        length=5,
        description="Total occurrences"
    ),
}


# ============================================================================
# TQ2 Segment - Timing/Quantity Relationship
# ============================================================================

TQ2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - TQ2",
        data_type="SI",
        length=4,
        description="Sequence number",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequence/Results Flag",
        data_type="ID",
        length=1,
        table_binding="0503",
        description="Sequence/Results Flag",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Related Placer Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Related placer number",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Related Filler Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Related filler number",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Related Quantity",
        data_type="CQ",
        length=20,
        repeating=True,
        description="Related quantity",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Related Interval",
        data_type="RI",
        length=200,
        repeating=True,
        description="Related interval",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Related Duration",
        data_type="ST",
        length=20,
        description="Related duration",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Related Start Date/Time",
        data_type="TS",
        length=26,
        description="Related start date/time",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Related End Date/Time",
        data_type="TS",
        length=26,
        description="Related end date/time",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Related Priority",
        data_type="CWE",
        length=250,
        table_binding="0485",
        repeating=True,
        description="Related priority",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Related Condition",
        data_type="ID",
        length=1,
        table_binding="0504",
        description="Related condition",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Related Text",
        data_type="TX",
        length=65536,
        description="Related text",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
        }
    ),
}


# ============================================================================
# RXR Segment - Pharmacy/Treatment Route
# ============================================================================

RXR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Route",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0162",
        description="Route (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administration Site",
        data_type="CWE",
        length=250,
        table_binding="0163",
        description="Administration site"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Administration Device",
        data_type="CWE",
        length=250,
        table_binding="0164",
        description="Administration device"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Administration Method",
        data_type="CWE",
        length=250,
        table_binding="0165",
        description="Administration method"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Routing Instruction",
        data_type="CWE",
        length=250,
        description="Routing instruction"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administration Site Modifier",
        data_type="CWE",
        length=250,
        table_binding="0495",
        description="Administration site modifier"
    ),
}


# ============================================================================
# RXC Segment - Pharmacy/Treatment Component
# ============================================================================

RXC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="RX Component Type",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0166",
        description="RX component type (B=Base, A=Additive) (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Component Code",
        data_type="CWE",
        length=250,
        required=True,
        description="Component code (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Component Amount",
        data_type="NM",
        length=20,
        description="Component amount"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Component Units",
        data_type="CWE",
        length=250,
        description="Component units"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Component Strength",
        data_type="NM",
        length=20,
        description="Component strength"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Component Strength Units",
        data_type="CWE",
        length=250,
        description="Component strength units"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Supplementary Code",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Component Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Component drug strength volume"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Component Drug Strength Volume Units",
        data_type="CWE",
        length=250,
        description="Component drug strength volume units"
    ),
}


# ============================================================================
# RXA Segment - Pharmacy/Treatment Administration
# ============================================================================

RXA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Give Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Give sub-ID counter (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administration Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Administration sub-ID counter (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date/Time Start of Administration",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time start of administration (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Date/Time End of Administration",
        data_type="TS",
        length=26,
        description="Date/time end of administration"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administered Code",
        data_type="CWE",
        length=250,
        required=True,
        description="Administered code (required)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administered Amount",
        data_type="NM",
        length=20,
        required=True,
        description="Administered amount (required)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Administered units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administered Dosage Form",
        data_type="CWE",
        length=250,
        description="Administered dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administration Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Administration notes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Administering provider"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administered-at Location",
        data_type="LA2",
        length=200,
        description="Administered-at location"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Administered per (time unit)"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Administered Strength",
        data_type="NM",
        length=20,
        description="Administered strength"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Administered strength units"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Substance Manufacturer Name",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0227",
        description="Substance manufacturer name"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Substance/Treatment Refusal Reason",
        data_type="CWE",
        length=250,
        table_binding="0496",
        repeating=True,
        description="Substance/treatment refusal reason"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Indication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Completion Status",
        data_type="ID",
        length=2,
        table_binding="0322",
        description="Completion status"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Action Code - RXA",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="System Entry Date/Time",
        data_type="TS",
        length=26,
        description="System entry date/time"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Administered Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Administered drug strength volume"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Administered Drug Strength Volume Units",
        data_type="CWE",
        length=250,
        description="Administered drug strength volume units"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Administered Barcode Identifier",
        data_type="CWE",
        length=250,
        description="Administered barcode identifier"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# DSC Segment - Continuation Pointer
# ============================================================================

DSC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Continuation Pointer",
        data_type="ST",
        length=180,
        description="Continuation pointer for query continuation"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Continuation Style",
        data_type="ID",
        length=1,
        table_binding="0398",
        description="Continuation style (I=Interactive, R=Refresh, A=Asynchronous)"
    ),
}


# ============================================================================
# UB1 Segment - UB82 Data
# ============================================================================

UB1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - UB1",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Blood Deductible",
        data_type="NM",
        length=12,
        description="Blood deductible"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Blood Furnished-Pints",
        data_type="NM",
        length=2,
        description="Blood furnished - pints"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Blood Replaced-Pints",
        data_type="NM",
        length=2,
        description="Blood replaced - pints"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Blood Not Replaced-Pints",
        data_type="NM",
        length=2,
        description="Blood not replaced - pints"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Co-Insurance Days",
        data_type="NM",
        length=2,
        description="Co-insurance days"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Condition Code",
        data_type="IS",
        length=2,
        table_binding="0043",
        repeating=True,
        description="Condition code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Covered Days",
        data_type="NM",
        length=2,
        description="Covered days"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Non-Covered Days",
        data_type="NM",
        length=2,
        description="Non-covered days"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Value Amount & Code",
        data_type="UVC",
        length=12,
        repeating=True,
        description="Value amount and code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Number Of Grace Days",
        data_type="NM",
        length=2,
        description="Number of grace days"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Special Program Indicator",
        data_type="CE",
        length=250,
        table_binding="0348",
        description="Special program indicator"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="PSRO/UR Approval Indicator",
        data_type="CE",
        length=250,
        table_binding="0349",
        description="PSRO/UR approval indicator"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="PSRO/UR Approved Stay-Fm",
        data_type="DT",
        length=8,
        description="PSRO/UR approved stay - from"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="PSRO/UR Approved Stay-To",
        data_type="DT",
        length=8,
        description="PSRO/UR approved stay - to"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Occurrence",
        data_type="CE",
        length=250,
        table_binding="0350",
        repeating=True,
        description="Occurrence"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Occurrence Span",
        data_type="CE",
        length=250,
        table_binding="0351",
        description="Occurrence span"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Occur Span Start Date",
        data_type="DT",
        length=8,
        description="Occurrence span start date"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Occur Span End Date",
        data_type="DT",
        length=8,
        description="Occurrence span end date"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="UB82 Locator 2",
        data_type="ST",
        length=30,
        description="UB82 locator 2"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="UB82 Locator 9",
        data_type="ST",
        length=30,
        description="UB82 locator 9"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="UB82 Locator 27",
        data_type="ST",
        length=30,
        description="UB82 locator 27"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="UB82 Locator 45",
        data_type="ST",
        length=30,
        description="UB82 locator 45"
    ),
}


# ============================================================================
# UB2 Segment - UB92 Data
# ============================================================================

UB2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - UB2",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Co-Insurance Days (9)",
        data_type="ST",
        length=3,
        description="Co-insurance days (9)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Condition Code (24-30)",
        data_type="IS",
        length=2,
        table_binding="0043",
        repeating=True,
        description="Condition code (24-30)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Covered Days (23)",
        data_type="ST",
        length=3,
        description="Covered days (23)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Non-Covered Days (24)",
        data_type="ST",
        length=3,
        description="Non-covered days (24)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Value Amount & Code (25-31)",
        data_type="UVC",
        length=12,
        repeating=True,
        description="Value amount and code (25-31)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Occurrence Code & Date (32-35)",
        data_type="OCD",
        length=11,
        repeating=True,
        description="Occurrence code and date (32-35)"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Occurrence Span Code/Dates (36)",
        data_type="OSP",
        length=11,
        description="Occurrence span code/dates (36)"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="UB92 Locator 2 (State)",
        data_type="ST",
        length=29,
        description="UB92 locator 2 (state)"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="UB92 Locator 11 (State)",
        data_type="ST",
        length=12,
        description="UB92 locator 11 (state)"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="UB92 Locator 31 (National)",
        data_type="ST",
        length=5,
        description="UB92 locator 31 (national)"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Document Control Number (37)",
        data_type="ST",
        length=23,
        description="Document control number (37)"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="UB92 Locator 49 (National)",
        data_type="ST",
        length=4,
        description="UB92 locator 49 (national)"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="UB92 Locator 56 (State)",
        data_type="ST",
        length=14,
        description="UB92 locator 56 (state)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="UB92 Locator 57 (National)",
        data_type="ST",
        length=27,
        description="UB92 locator 57 (national)"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="UB92 Locator 78 (State)",
        data_type="ST",
        length=2,
        description="UB92 locator 78 (state)"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Special Visit Count",
        data_type="NM",
        length=3,
        description="Special visit count"
    ),
}


# ============================================================================
# ROL Segment - Role
# ============================================================================

ROL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Role Instance ID",
        data_type="EI",
        length=427,
        description="Role instance ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Code",
        data_type="ID",
        length=2,
        table_binding="0287",
        description="Action code (AD=Add, UP=Update, DE=Delete)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Role-ROL",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0443",
        description="Role (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Role Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Role person"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Role Begin Date/Time",
        data_type="TS",
        length=26,
        description="Role begin date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Role End Date/Time",
        data_type="TS",
        length=26,
        description="Role end date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Role Duration",
        data_type="CE",
        length=250,
        description="Role duration"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Role Action Reason",
        data_type="CE",
        length=250,
        description="Role action reason"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider Type",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0186",
        description="Provider type"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Organization Unit Type",
        data_type="CE",
        length=250,
        table_binding="0406",
        description="Organization unit type"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Office/Home Address/Birthplace",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Office/home address/birthplace"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone"
    ),
}


# ============================================================================
# CTD Segment - Contact Data
# ============================================================================

CTD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Contact Role",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0131",
        description="Contact role"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Contact Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Contact name"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Contact Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Contact address"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Contact Location",
        data_type="PL",
        length=250,
        description="Contact location"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Contact Communication Information",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Contact communication information"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Preferred Method of Contact",
        data_type="CE",
        length=250,
        table_binding="0185",
        description="Preferred method of contact"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Contact Identifiers",
        data_type="PLN",
        length=250,
        repeating=True,
        description="Contact identifiers"
    ),
}


# ============================================================================
# ACC Segment - Accident
# ============================================================================

ACC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Accident Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of accident"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Accident Code",
        data_type="CE",
        length=250,
        table_binding="0050",
        description="Type of accident"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Accident Location",
        data_type="ST",
        length=25,
        description="Location of accident"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Auto Accident State",
        data_type="CE",
        length=250,
        description="State where auto accident occurred"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Accident Job Related Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Y=Yes, N=No"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Accident Death Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Y=Yes, N=No"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Entered By",
        data_type="XCN",
        length=250,
        description="Person who entered accident information"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Accident Description",
        data_type="ST",
        length=25,
        description="Description of accident"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Brought In By",
        data_type="ST",
        length=25,
        description="How patient was brought in"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Police Notified Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Y=Yes, N=No"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Accident Address",
        data_type="XAD",
        length=250,
        description="Address where accident occurred"
    ),
}


# ============================================================================
# BHS Segment - Batch Header Segment
# ============================================================================

BHS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Batch Field Separator",
        data_type="ST",
        length=1,
        required=True,
        description="Field separator character"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Batch Encoding Characters",
        data_type="ST",
        length=4,
        required=True,
        description="Encoding characters"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Batch Sending Application",
        data_type="HD",
        length=227,
        description="Sending application"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Batch Sending Facility",
        data_type="HD",
        length=227,
        description="Sending facility"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Batch Receiving Application",
        data_type="HD",
        length=227,
        description="Receiving application"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Batch Receiving Facility",
        data_type="HD",
        length=227,
        description="Receiving facility"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Batch Creation Date/Time",
        data_type="TS",
        length=26,
        description="Batch creation timestamp"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Batch Security",
        data_type="ST",
        length=40,
        description="Security information"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Batch Name/ID/Type",
        data_type="ST",
        length=20,
        description="Batch identifier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Batch Comment",
        data_type="ST",
        length=80,
        description="Batch comment"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Batch Control ID",
        data_type="ST",
        length=20,
        description="Batch control identifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Reference Batch Control ID",
        data_type="ST",
        length=20,
        description="Reference to previous batch"
    ),
}


# ============================================================================
# BTS Segment - Batch Trailer Segment
# ============================================================================

BTS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Batch Message Count",
        data_type="ST",
        length=10,
        description="Number of messages in batch"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Batch Comment",
        data_type="ST",
        length=80,
        description="Batch comment"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Batch Totals",
        data_type="NM",
        length=10,
        repeating=True,
        description="Batch totals"
    ),
}


# ============================================================================
# BLG Segment - Billing
# ============================================================================

BLG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="When to Charge",
        data_type="CCD",
        length=20,
        description="When to charge"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Charge Type",
        data_type="ID",
        length=50,
        table_binding="0122",
        description="Charge type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Account ID",
        data_type="CX",
        length=250,
        description="Account identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Charge Type Reason",
        data_type="CE",
        length=250,
        description="Reason for charge type"
    ),
}


# ============================================================================
# SCH Segment - Scheduling Information
# ============================================================================

SCH_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Appointment ID",
        data_type="EI",
        length=427,
        description="Placer appointment identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Appointment ID",
        data_type="EI",
        length=427,
        description="Filler appointment identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Occurrence Number",
        data_type="NM",
        length=5,
        description="Occurrence number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Placer Group Number",
        data_type="EI",
        length=427,
        description="Placer group number"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Schedule ID",
        data_type="CE",
        length=250,
        table_binding="0274",
        description="Schedule identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Event Reason",
        data_type="CE",
        length=250,
        description="Reason for event"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Appointment Reason",
        data_type="CE",
        length=250,
        table_binding="0276",
        description="Reason for appointment"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Appointment Type",
        data_type="CE",
        length=250,
        table_binding="0277",
        description="Type of appointment"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Appointment Duration",
        data_type="NM",
        length=20,
        description="Duration of appointment"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Appointment Duration Units",
        data_type="CE",
        length=250,
        description="Units for duration"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Appointment Timing Quantity",
        data_type="TQ",
        length=200,
        repeating=True,
        description="Timing quantity"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Placer Contact Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Placer contact person"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Placer Contact Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Placer contact phone"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Placer Contact Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Placer contact address"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Placer Contact Location",
        data_type="PL",
        length=250,
        description="Placer contact location"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Filler Contact Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Filler contact person"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Filler Contact Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Filler contact phone"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Filler Contact Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Filler contact address"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Filler Contact Location",
        data_type="PL",
        length=250,
        description="Filler contact location"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Entered By Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who entered appointment"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Entered By Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone number of person who entered"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Entered By Location",
        data_type="PL",
        length=250,
        description="Location of person who entered"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Parent Placer Appointment ID",
        data_type="EI",
        length=427,
        description="Parent placer appointment identifier"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Parent Filler Appointment ID",
        data_type="EI",
        length=427,
        description="Parent filler appointment identifier"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Filler Status Code",
        data_type="CE",
        length=250,
        table_binding="0278",
        description="Filler status code"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Placer Order Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Placer order number"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Filler Order Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Filler order number"
    ),
}


# ============================================================================
# TXA Segment - Transcription Document Header
# ============================================================================

TXA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - TXA",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Document Type",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0270",
        description="Type of document"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Document Content Presentation",
        data_type="ID",
        length=2,
        table_binding="0191",
        description="Content presentation format"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Activity Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time of activity"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Primary Activity Provider Code Name",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Primary provider"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Origination Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of origination"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Transcription Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of transcription"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Edit Date/Time",
        data_type="TS",
        length=26,
        repeating=True,
        description="Date/time of edits"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Originator Code Name",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Originator code name"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Assigned Document Authenticator",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Assigned authenticator"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Transcriptionist Code Name",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Transcriptionist code name"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Unique Document Number",
        data_type="EI",
        length=427,
        required=True,
        description="Unique document identifier"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Parent Document Number",
        data_type="EI",
        length=427,
        description="Parent document identifier"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Placer Order Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Placer order number"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Filler Order Number",
        data_type="EI",
        length=427,
        description="Filler order number"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Unique Document File Name",
        data_type="ST",
        length=30,
        description="Unique document file name"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Document Completion Status",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0271",
        description="Completion status"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Document Confidentiality Status",
        data_type="ID",
        length=2,
        table_binding="0272",
        description="Confidentiality status"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Document Availability Status",
        data_type="ID",
        length=2,
        table_binding="0273",
        description="Availability status"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Document Storage Status",
        data_type="ID",
        length=2,
        table_binding="0275",
        description="Storage status"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Document Change Reason",
        data_type="ST",
        length=30,
        description="Reason for document change"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Authentication Person, Time Stamp",
        data_type="PPN",
        length=250,
        repeating=True,
        description="Authentication person and timestamp"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Distributed Copies Code and Name of Recipients",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Distributed copies recipients"
    ),
}


# ============================================================================
# RCP Segment - Response Control Parameter
# ============================================================================

RCP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Priority",
        data_type="ID",
        length=1,
        table_binding="0091",
        description="Priority of query"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Quantity Limited Request",
        data_type="CQ",
        length=267,
        description="Quantity limited request"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Response Modality",
        data_type="CE",
        length=250,
        table_binding="0394",
        description="Response modality"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Execution and Delivery Time",
        data_type="TS",
        length=26,
        description="Execution and delivery time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Modify Indicator",
        data_type="ID",
        length=1,
        table_binding="0395",
        description="Modify indicator"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Sort-by Field",
        data_type="SRT",
        length=200,
        repeating=True,
        description="Sort-by field"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Segment Group Inclusion",
        data_type="ID",
        length=256,
        repeating=True,
        table_binding="0396",
        description="Segment group inclusion"
    ),
}


# ============================================================================
# RF1 Segment - Referral Information
# ============================================================================

RF1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Referral Status",
        data_type="CE",
        length=250,
        table_binding="0283",
        description="Referral status"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Referral Priority",
        data_type="CE",
        length=250,
        table_binding="0280",
        description="Referral priority"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Referral Type",
        data_type="CE",
        length=250,
        table_binding="0281",
        description="Referral type"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Referral Disposition",
        data_type="CE",
        length=250,
        table_binding="0282",
        repeating=True,
        description="Referral disposition"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Referral Category",
        data_type="CE",
        length=250,
        table_binding="0284",
        description="Referral category"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Originating Referral Identifier",
        data_type="EI",
        length=427,
        description="Originating referral identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Effective Date",
        data_type="TS",
        length=26,
        description="Effective date"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Expiration Date",
        data_type="TS",
        length=26,
        description="Expiration date"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Process Date",
        data_type="TS",
        length=26,
        description="Process date"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Referral Reason",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0336",
        description="Referral reason"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="External Referral Identifier",
        data_type="EI",
        length=427,
        repeating=True,
        description="External referral identifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Referral Documentation Completion Status",
        data_type="CE",
        length=250,
        table_binding="0851",
        description="Documentation completion status"
    ),
}


# ============================================================================
# RMI Segment - Risk Management Incident
# ============================================================================

RMI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Risk Management Incident Code",
        data_type="CE",
        length=250,
        table_binding="0427",
        description="Risk management incident code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="DateTime Incident",
        data_type="TS",
        length=26,
        description="Date/time of incident"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Incident Type Code",
        data_type="CE",
        length=250,
        table_binding="0428",
        description="Incident type code"
    ),
}

# ============================================================================
# AIS Segment - Appointment Information - Service
# ============================================================================

AIS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - AIS",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code (I=Insert, U=Update, D=Delete)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Universal Service Identifier",
        data_type="CE",
        length=250,
        description="Service identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Start Date/Time",
        data_type="TS",
        length=26,
        description="Appointment start date/time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Start Date/Time Offset",
        data_type="NM",
        length=5,
        description="Offset in minutes from start date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Start Date/Time Offset Units",
        data_type="CE",
        length=250,
        description="Units for offset (e.g., minutes, hours)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Duration",
        data_type="NM",
        length=20,
        description="Duration of appointment"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Duration Units",
        data_type="CE",
        length=250,
        description="Units for duration"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Allow Substitution Code",
        data_type="IS",
        length=10,
        table_binding="0279",
        description="Allow substitution indicator"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Filler Status Code",
        data_type="CE",
        length=250,
        table_binding="0278",
        description="Filler status code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Placer Supplemental Service Information",
        data_type="CE",
        length=250,
        description="Additional service information from placer"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Filler Supplemental Service Information",
        data_type="CE",
        length=250,
        description="Additional service information from filler"
    ),
}

# ============================================================================
# AIG Segment - Appointment Information - General Resource
# ============================================================================

AIG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - AIG",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Resource ID",
        data_type="CE",
        length=250,
        description="Resource identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Resource Type",
        data_type="CE",
        length=250,
        table_binding="0182",
        description="Type of resource"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Resource Group",
        data_type="CE",
        length=250,
        description="Resource group identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Resource Quantity",
        data_type="NM",
        length=5,
        description="Quantity of resource"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Resource Quantity Units",
        data_type="CE",
        length=250,
        description="Units for resource quantity"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Start Date/Time",
        data_type="TS",
        length=26,
        description="Resource start date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Start Date/Time Offset",
        data_type="NM",
        length=5,
        description="Offset in minutes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Start Date/Time Offset Units",
        data_type="CE",
        length=250,
        description="Offset units"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Duration",
        data_type="NM",
        length=20,
        description="Duration"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Duration Units",
        data_type="CE",
        length=250,
        description="Duration units"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Allow Substitution Code",
        data_type="IS",
        length=10,
        table_binding="0279",
        description="Allow substitution"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Filler Status Code",
        data_type="CE",
        length=250,
        table_binding="0278",
        description="Filler status"
    ),
}

# ============================================================================
# AIL Segment - Appointment Information - Location Resource
# ============================================================================

AIL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - AIL",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Location Resource ID",
        data_type="PL",
        length=200,
        description="Location resource identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Location Type - AIL",
        data_type="CE",
        length=250,
        table_binding="0305",
        description="Location type"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Location Group",
        data_type="CE",
        length=250,
        description="Location group identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Start Date/Time Offset",
        data_type="NM",
        length=5,
        description="Offset in minutes"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Start Date/Time Offset Units",
        data_type="CE",
        length=250,
        description="Offset units"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Duration",
        data_type="NM",
        length=20,
        description="Duration"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Duration Units",
        data_type="CE",
        length=250,
        description="Duration units"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Allow Substitution Code",
        data_type="IS",
        length=10,
        table_binding="0279",
        description="Allow substitution"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Filler Status Code",
        data_type="CE",
        length=250,
        table_binding="0278",
        description="Filler status"
    ),
}

# ============================================================================
# AIP Segment - Appointment Information - Personnel Resource
# ============================================================================

AIP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - AIP",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Personnel Resource ID",
        data_type="XCN",
        length=250,
        description="Personnel resource identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Resource Type",
        data_type="CE",
        length=250,
        table_binding="0182",
        description="Resource type"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Resource Group",
        data_type="CE",
        length=250,
        description="Resource group"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Start Date/Time Offset",
        data_type="NM",
        length=5,
        description="Offset in minutes"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Start Date/Time Offset Units",
        data_type="CE",
        length=250,
        description="Offset units"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Duration",
        data_type="NM",
        length=20,
        description="Duration"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Duration Units",
        data_type="CE",
        length=250,
        description="Duration units"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Allow Substitution Code",
        data_type="IS",
        length=10,
        table_binding="0279",
        description="Allow substitution"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Filler Status Code",
        data_type="CE",
        length=250,
        table_binding="0278",
        description="Filler status"
    ),
}

# ============================================================================
# DB1 Segment - Disability
# ============================================================================

DB1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - DB1",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Disabled Person Code",
        data_type="IS",
        length=2,
        table_binding="0334",
        description="Disabled person code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Disabled Person Identifier",
        data_type="CX",
        length=250,
        description="Disabled person identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Disability Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Disability indicator"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Disability Start Date",
        data_type="DT",
        length=8,
        description="Disability start date"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Disability End Date",
        data_type="DT",
        length=8,
        description="Disability end date"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Disability Return to Work Date",
        data_type="DT",
        length=8,
        description="Return to work date"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Disability Unable to Work Date",
        data_type="DT",
        length=8,
        description="Unable to work date"
    ),
}

# ============================================================================
# FAC Segment - Facility
# ============================================================================

FAC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Facility ID - FAC",
        data_type="EI",
        length=427,
        description="Facility identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Facility Type",
        data_type="ID",
        length=1,
        table_binding="0331",
        description="Facility type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Facility Address",
        data_type="XAD",
        length=250,
        description="Facility address"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Facility Telecommunication",
        data_type="XTN",
        length=250,
        description="Facility telecommunication"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Contact Person",
        data_type="XCN",
        length=250,
        description="Contact person"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Contact Title",
        data_type="ST",
        length=60,
        description="Contact title"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Contact Address",
        data_type="XAD",
        length=250,
        description="Contact address"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Contact Telecommunication",
        data_type="XTN",
        length=250,
        description="Contact telecommunication"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Signature Authority",
        data_type="XCN",
        length=250,
        description="Signature authority"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Signature Authority Title",
        data_type="ST",
        length=60,
        description="Signature authority title"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Signature Authority Address",
        data_type="XAD",
        length=250,
        description="Signature authority address"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Signature Authority Telecommunication",
        data_type="XTN",
        length=250,
        description="Signature authority telecommunication"
    ),
}

# ============================================================================
# STF Segment - Staff Identification
# ============================================================================

STF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - STF",
        data_type="CE",
        length=250,
        description="Primary key value"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Staff Identifier List",
        data_type="CX",
        length=250,
        repeating=True,
        description="Staff identifier list"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Staff Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Staff name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Staff Type",
        data_type="IS",
        length=2,
        table_binding="0182",
        repeating=True,
        description="Staff type"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administrative Sex",
        data_type="IS",
        length=1,
        table_binding="0001",
        description="Administrative sex"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Date/Time of Birth",
        data_type="TS",
        length=26,
        description="Date/time of birth"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Active/Inactive Flag",
        data_type="ID",
        length=1,
        table_binding="0183",
        description="Active/inactive flag"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Department",
        data_type="CE",
        length=250,
        repeating=True,
        description="Department"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Hospital Service - STF",
        data_type="CE",
        length=250,
        repeating=True,
        description="Hospital service"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone number"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Office/Home Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Office/home address"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Institution Activation Date",
        data_type="DIN",
        length=26,
        repeating=True,
        description="Institution activation date"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Institution Inactivation Date",
        data_type="DIN",
        length=26,
        repeating=True,
        description="Institution inactivation date"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Backup Person ID",
        data_type="CE",
        length=250,
        repeating=True,
        description="Backup person identifier"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="E-Mail Address",
        data_type="ST",
        length=199,
        repeating=True,
        description="E-mail address"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Preferred Method of Contact",
        data_type="CE",
        length=250,
        description="Preferred method of contact"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Marital Status",
        data_type="IS",
        length=1,
        table_binding="0002",
        description="Marital status"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Job Title",
        data_type="ST",
        length=60,
        description="Job title"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Job Code/Class",
        data_type="JCC",
        length=20,
        description="Job code/class"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Employment Status Code",
        data_type="IS",
        length=2,
        table_binding="0066",
        description="Employment status code"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Additional Insured on Auto",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Additional insured on auto"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Driver's License Number - Staff",
        data_type="DLN",
        length=25,
        description="Driver's license number"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Copy Auto Ins",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Copy auto insurance"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Auto Ins Expires",
        data_type="DT",
        length=8,
        description="Auto insurance expiration date"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Date Last DMV Review",
        data_type="DT",
        length=8,
        description="Date last DMV review"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Date Next DMV Review",
        data_type="DT",
        length=8,
        description="Date next DMV review"
    ),
}


# ============================================================================
# MRG Segment - Merge Patient Information
# ============================================================================

MRG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Prior Patient Identifier List",
        data_type="CX",
        length=None,
        required=True,
        description="Prior patient identifier list - contains identifiers to be merged"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Prior Alternate Patient ID",
        data_type="CX",
        length=None,
        description="Prior alternate patient identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Prior Patient Account Number",
        data_type="CX",
        length=None,
        description="Prior patient account number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Prior Patient ID",
        data_type="CX",
        length=None,
        description="Prior patient ID"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Prior Visit Number",
        data_type="CX",
        length=None,
        description="Prior visit number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Prior Alternate Visit ID",
        data_type="CX",
        length=None,
        description="Prior alternate visit identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Prior Patient Name",
        data_type="XPN",
        length=None,
        description="Prior patient name"
    ),
}


# ============================================================================
# FHS Segment - File Header Segment
# ============================================================================

FHS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Field Separator",
        data_type="ST",
        length=1,
        required=True,
        description="Field separator character (usually |)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Encoding Characters",
        data_type="ST",
        length=4,
        required=True,
        description="Encoding characters (^~\\&)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="File Sending Application",
        data_type="HD",
        length=227,
        description="File sending application identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="File Sending Facility",
        data_type="HD",
        length=227,
        description="File sending facility identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="File Receiving Application",
        data_type="HD",
        length=227,
        description="File receiving application identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="File Receiving Facility",
        data_type="HD",
        length=227,
        description="File receiving facility identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="File Creation Date/Time",
        data_type="TS",
        length=26,
        description="File creation date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="File Security",
        data_type="ST",
        length=40,
        description="File security field"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="File ID/Name/Type",
        data_type="ST",
        length=199,
        description="File identifier, name, or type"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="File Comment",
        data_type="ST",
        length=80,
        description="File comment"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="File Control ID",
        data_type="ST",
        length=199,
        description="File control identifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Reference File Control ID",
        data_type="ST",
        length=199,
        description="Reference file control identifier"
    ),
}


# ============================================================================
# FTS Segment - File Trailer Segment
# ============================================================================

FTS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="File Batch Count",
        data_type="NM",
        length=10,
        description="Number of batches in file"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="File Comment",
        data_type="ST",
        length=80,
        description="File comment"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="File Totals",
        data_type="ST",
        length=80,
        repeating=True,
        description="File totals (optional, multiple values)"
    ),
}


# ============================================================================
# RXD Segment - Pharmacy/Treatment Dispense
# ============================================================================

RXD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Dispense sub-identifier counter"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense/Give Code",
        data_type="CE",
        length=250,
        required=True,
        description="Dispense/give code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="DateTime Dispensed",
        data_type="TS",
        length=26,
        description="Date/time dispensed"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Actual Dispense Amount",
        data_type="NM",
        length=20,
        description="Actual dispense amount"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Actual Dispense Units",
        data_type="CE",
        length=250,
        description="Actual dispense units"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Actual Dosage Form",
        data_type="CE",
        length=250,
        description="Actual dosage form"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Prescription Number",
        data_type="ST",
        length=20,
        description="Prescription number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Number of Refills Remaining",
        data_type="NM",
        length=20,
        description="Number of refills remaining"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Dispense Notes",
        data_type="ST",
        length=200,
        repeating=True,
        description="Dispense notes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Dispensing Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Dispensing provider"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=10,
        description="Total daily dose"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Dispense-to Location",
        data_type="LA2",
        length=200,
        description="Dispense-to location"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review (Y/N)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Actual Strength",
        data_type="NM",
        length=20,
        description="Actual strength"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Actual Strength Unit",
        data_type="CE",
        length=250,
        description="Actual strength unit"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Substance Manufacturer Name",
        data_type="CE",
        length=250,
        repeating=True,
        description="Substance manufacturer name"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Dispense Package Size Unit",
        data_type="CE",
        length=250,
        description="Dispense package size unit"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Supplementary Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Initiating Location",
        data_type="LA2",
        length=200,
        description="Initiating location"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Packaging/Assembly Location",
        data_type="LA2",
        length=200,
        description="Packaging/assembly location"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Actual Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Actual drug strength volume"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Actual Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Actual drug strength volume units"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Dispense to Patient Location",
        data_type="PL",
        length=80,
        description="Dispense to patient location"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Dispense to Patient Address",
        data_type="XAD",
        length=250,
        description="Dispense to patient address"
    ),
}


# ============================================================================
# RXE Segment - Pharmacy/Treatment Encoded Order
# ============================================================================

RXE_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity/timing"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Give Code",
        data_type="CE",
        length=250,
        required=True,
        description="Give code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Units",
        data_type="CE",
        length=250,
        required=True,
        description="Give units"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Dosage Form",
        data_type="CE",
        length=250,
        description="Give dosage form"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Provider's Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Deliver-to Location",
        data_type="LA2",
        length=200,
        description="Deliver-to location"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Dispense Amount",
        data_type="NM",
        length=20,
        description="Dispense amount"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Dispense Units",
        data_type="CE",
        length=250,
        description="Dispense units"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Number of Refills",
        data_type="NM",
        length=20,
        description="Number of refills"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Ordering Provider's DEA Number",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Ordering provider's DEA number"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Pharmacist/Treatment Supplier's Verifier ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Pharmacist/treatment supplier's verifier ID"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Prescription Number",
        data_type="ST",
        length=20,
        description="Prescription number"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Number of Refills Remaining",
        data_type="NM",
        length=20,
        description="Number of refills remaining"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Number of Refills/Doses Total",
        data_type="NM",
        length=20,
        description="Number of refills/doses total"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Give Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Give per (time unit)"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Give Rate Amount",
        data_type="ST",
        length=6,
        description="Give rate amount"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Give Rate Units",
        data_type="CE",
        length=250,
        description="Give rate units"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Give Strength",
        data_type="NM",
        length=20,
        description="Give strength"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Give Strength Units",
        data_type="CE",
        length=250,
        description="Give strength units"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Give Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Give indication"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Dispense Package Size Unit",
        data_type="CE",
        length=250,
        description="Dispense package size unit"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Supplementary Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Original Order Date/Time",
        data_type="TS",
        length=26,
        description="Original order date/time"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Give Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Give drug strength volume"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Give Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Give drug strength volume units"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Controlled Substance Schedule",
        data_type="ID",
        length=1,
        table_binding="0477",
        description="Controlled substance schedule"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Formulary Status",
        data_type="ID",
        length=1,
        table_binding="0478",
        description="Formulary status"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Pharmaceutical Substance Alternative",
        data_type="CE",
        length=250,
        repeating=True,
        description="Pharmaceutical substance alternative"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Pharmacy of Most Recent Fill",
        data_type="CE",
        length=250,
        description="Pharmacy of most recent fill"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Initial Dispense Amount",
        data_type="NM",
        length=20,
        description="Initial dispense amount"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Dispensing Pharmacy",
        data_type="CE",
        length=250,
        description="Dispensing pharmacy"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Dispensing Pharmacy Address",
        data_type="XAD",
        length=250,
        description="Dispensing pharmacy address"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Deliver-to Patient Location",
        data_type="PL",
        length=80,
        description="Deliver-to patient location"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Deliver-to Address",
        data_type="XAD",
        length=250,
        description="Deliver-to address"
    ),
}


# ============================================================================
# RXG Segment - Pharmacy/Treatment Give
# ============================================================================

RXG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Give Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Give sub-identifier counter"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Dispense sub-identifier counter"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity/timing"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CE",
        length=250,
        required=True,
        description="Give code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CE",
        length=250,
        required=True,
        description="Give units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administration Notes",
        data_type="CE",
        length=250,
        repeating=True,
        description="Administration notes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Dispense-to Location",
        data_type="LA2",
        length=200,
        description="Dispense-to location"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review (Y/N)"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Pharmacy/Treatment Supplier's Special Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special administration instructions"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Give Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Give per (time unit)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Give Rate Amount",
        data_type="ST",
        length=6,
        description="Give rate amount"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Give Rate Units",
        data_type="CE",
        length=250,
        description="Give rate units"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Give Strength",
        data_type="NM",
        length=20,
        description="Give strength"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Give Strength Units",
        data_type="CE",
        length=250,
        description="Give strength units"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Give Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Give indication"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Dispense Package Size Unit",
        data_type="CE",
        length=250,
        description="Dispense package size unit"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Supplementary Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Pharmacy/Treatment Supplier's Verifier ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Pharmacy/treatment supplier's verifier ID"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Give Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Give drug strength volume"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Give Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Give drug strength volume units"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Controlled Substance Schedule",
        data_type="ID",
        length=1,
        table_binding="0477",
        description="Controlled substance schedule"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Formulary Status",
        data_type="ID",
        length=1,
        table_binding="0478",
        description="Formulary status"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Pharmaceutical Substance Alternative",
        data_type="CE",
        length=250,
        repeating=True,
        description="Pharmaceutical substance alternative"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Pharmacy of Most Recent Fill",
        data_type="CE",
        length=250,
        description="Pharmacy of most recent fill"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Initial Dispense Amount",
        data_type="NM",
        length=20,
        description="Initial dispense amount"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Dispensing Pharmacy",
        data_type="CE",
        length=250,
        description="Dispensing pharmacy"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Dispensing Pharmacy Address",
        data_type="XAD",
        length=250,
        description="Dispensing pharmacy address"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Deliver-to Patient Location",
        data_type="PL",
        length=80,
        description="Deliver-to patient location"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Deliver-to Address",
        data_type="XAD",
        length=250,
        description="Deliver-to address"
    ),
}


# ============================================================================
# RXO Segment - Pharmacy/Treatment Order
# ============================================================================

RXO_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Requested Give Code",
        data_type="CE",
        length=250,
        required=True,
        description="Requested give code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Requested Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Requested give amount - minimum"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Requested Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Requested give amount - maximum"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Requested Give Units",
        data_type="CE",
        length=250,
        required=True,
        description="Requested give units"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Requested Dosage Form",
        data_type="CE",
        length=250,
        description="Requested dosage form"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Provider's Pharmacy/Treatment Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Provider's pharmacy/treatment instructions"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Provider's Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Deliver-to Location",
        data_type="LA2",
        length=200,
        description="Deliver-to location"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Allow Substitutions",
        data_type="ID",
        length=1,
        table_binding="0161",
        description="Allow substitutions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Requested Dispense Code",
        data_type="CE",
        length=250,
        description="Requested dispense code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Requested Dispense Amount",
        data_type="NM",
        length=20,
        description="Requested dispense amount"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Requested Dispense Units",
        data_type="CE",
        length=250,
        description="Requested dispense units"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Number of Refills",
        data_type="NM",
        length=20,
        description="Number of refills"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Ordering Provider's DEA Number",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Ordering provider's DEA number"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Pharmacist/Treatment Supplier's Verifier ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Pharmacist/treatment supplier's verifier ID"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review (Y/N)"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Requested Give Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Requested give per (time unit)"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Requested Give Strength",
        data_type="NM",
        length=20,
        description="Requested give strength"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Requested Give Strength Units",
        data_type="CE",
        length=250,
        description="Requested give strength units"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Requested Give Rate Amount",
        data_type="ST",
        length=6,
        description="Requested give rate amount"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Requested Give Rate Units",
        data_type="CE",
        length=250,
        description="Requested give rate units"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=10,
        description="Total daily dose"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Supplementary Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Requested Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Requested drug strength volume"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Requested Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Requested drug strength volume units"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Requested Give Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Requested give substitution status"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Requested Dispense Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Requested dispense substitution status"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Requested Quantity",
        data_type="CQ",
        length=10,
        description="Requested quantity"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Requested Number of Refills",
        data_type="NM",
        length=20,
        description="Requested number of refills"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Requested Give Start Date/Time",
        data_type="TS",
        length=26,
        description="Requested give start date/time"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Requested Give End Date/Time",
        data_type="TS",
        length=26,
        description="Requested give end date/time"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Requested Give Units of Measure",
        data_type="CE",
        length=250,
        description="Requested give units of measure"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Requested Give Strength Volume",
        data_type="NM",
        length=20,
        description="Requested give strength volume"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Requested Give Strength Volume Units",
        data_type="CE",
        length=250,
        description="Requested give strength volume units"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Indication for Give",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication for give"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Requested Give Rate Type",
        data_type="ID",
        length=1,
        table_binding="0479",
        description="Requested give rate type"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Requested Give Rate Amount/Volume",
        data_type="CE",
        length=250,
        description="Requested give rate amount/volume"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Requested Give Strength",
        data_type="NM",
        length=20,
        description="Requested give strength"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Requested Give Strength Units",
        data_type="CE",
        length=250,
        description="Requested give strength units"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Requested Give Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Requested give indication"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Requested Give Rate",
        data_type="ST",
        length=6,
        description="Requested give rate"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Requested Give Rate Units",
        data_type="CE",
        length=250,
        description="Requested give rate units"
    ),
}


# ============================================================================
# RXP Segment - Pharmacy/Treatment Component
# ============================================================================

RXP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Route",
        data_type="CE",
        length=250,
        required=True,
        description="Route"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administration Site",
        data_type="CE",
        length=250,
        description="Administration site"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Administration Device",
        data_type="CE",
        length=250,
        description="Administration device"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Administration Method",
        data_type="CE",
        length=250,
        description="Administration method"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Routing Instruction",
        data_type="CE",
        length=250,
        description="Routing instruction"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administration Site Modifier",
        data_type="CE",
        length=250,
        description="Administration site modifier"
    ),
}


# ============================================================================
# CDM Segment - Charge Description Master
# ============================================================================

CDM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - CDM",
        data_type="CE",
        length=250,
        required=True,
        description="Primary key value - CDM"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Charge Code Alias",
        data_type="CE",
        length=250,
        repeating=True,
        description="Charge code alias"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Charge Description Short",
        data_type="ST",
        length=20,
        description="Charge description short"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Charge Description Long",
        data_type="ST",
        length=250,
        description="Charge description long"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Description Override Indicator",
        data_type="IS",
        length=1,
        table_binding="0268",
        description="Description override indicator"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Exploding Charges",
        data_type="CE",
        length=250,
        repeating=True,
        description="Exploding charges"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Procedure Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Procedure code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Active/Inactive Flag",
        data_type="ID",
        length=1,
        table_binding="0183",
        description="Active/inactive flag"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Inventory Number",
        data_type="CE",
        length=250,
        repeating=True,
        description="Inventory number"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Resource Load",
        data_type="NM",
        length=12,
        description="Resource load"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Contract Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Contract number"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Contract Organization",
        data_type="XON",
        length=250,
        repeating=True,
        description="Contract organization"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Room Fee Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Room fee indicator (Y/N)"
    ),
}


# ============================================================================
# DRG Segment - Diagnosis Related Group
# ============================================================================

DRG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Diagnostic Related Group",
        data_type="CE",
        length=250,
        description="Diagnostic related group"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="DRG Assigned Date/Time",
        data_type="TS",
        length=26,
        description="DRG assigned date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="DRG Approval Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="DRG approval indicator (Y/N)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="DRG Grouper Review Code",
        data_type="IS",
        length=2,
        table_binding="0076",
        description="DRG grouper review code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Outlier Type",
        data_type="CE",
        length=250,
        description="Outlier type"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Outlier Days",
        data_type="NM",
        length=3,
        description="Outlier days"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Outlier Cost",
        data_type="CP",
        length=12,
        description="Outlier cost"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="DRG Payor",
        data_type="IS",
        length=1,
        table_binding="0229",
        description="DRG payor"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Outlier Reimbursement",
        data_type="CP",
        length=12,
        description="Outlier reimbursement"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Confidential Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Confidential indicator (Y/N)"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="DRG Transfer Type",
        data_type="IS",
        length=3,
        table_binding="0415",
        description="DRG transfer type"
    ),
}


# ============================================================================
# QRA Segment - Query Response Authorization
# ============================================================================

QRA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag from QPD segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Response Status",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0208",
        description="Query response status (OK=Data found, NF=No data found, AE=Application error)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        required=True,
        description="Message query name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Hit Count Total",
        data_type="NM",
        length=10,
        description="Total number of hits"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="This Payload",
        data_type="NM",
        length=10,
        description="Number of records in this payload"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Hits Remaining",
        data_type="NM",
        length=10,
        description="Number of hits remaining"
    ),
}


# ============================================================================
# QID Segment - Query Identification
# ============================================================================

QID_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Unique identifier for the query"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        required=True,
        description="Name of the query message"
    ),
}


# ============================================================================
# QRI Segment - Query Response Instance
# ============================================================================

QRI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Candidate Confidence",
        data_type="NM",
        length=5,
        description="Confidence level of the candidate match"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Match Reason Code",
        data_type="IS",
        length=2,
        table_binding="0392",
        description="Reason code for the match"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Algorithm Descriptor",
        data_type="CE",
        length=250,
        description="Algorithm used for matching"
    ),
}


# ============================================================================
# QSC Segment - Query Selection Criteria
# ============================================================================

QSC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Field Name",
        data_type="ST",
        length=40,
        required=True,
        description="Name of the field being queried"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Relational Operator",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0209",
        description="Relational operator (EQ, NE, GT, LT, GE, LE, etc.)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Value",
        data_type="ST",
        length=256,
        description="Value to compare against"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Relational Conjunction",
        data_type="ID",
        length=2,
        table_binding="0210",
        description="Conjunction operator (AND, OR)"
    ),
}


# ============================================================================
# RCD Segment - Row Column Definition
# ============================================================================

RCD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Field Name",
        data_type="ST",
        length=40,
        description="Name of the field"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="HCFA-1500 Claim Form Locator",
        data_type="ST",
        length=15,
        description="HCFA-1500 claim form locator number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Column Value",
        data_type="ST",
        length=40,
        description="Column value"
    ),
}


# ============================================================================
# RDF Segment - Table Row Definition
# ============================================================================

RDF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Number of Columns per Row",
        data_type="NM",
        length=3,
        required=True,
        description="Number of columns in the row"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Column Description",
        data_type="RCD",
        length=40,
        repeating=True,
        description="Description of each column"
    ),
}


# ============================================================================
# RDT Segment - Table Row Data
# ============================================================================

RDT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Column Value",
        data_type="ST",
        length=65536,
        repeating=True,
        description="Value for each column in the row"
    ),
}


# ============================================================================
# RQ1 Segment - Requisition Detail-1
# ============================================================================

RQ1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Anticipated Price",
        data_type="MO",
        length=20,
        description="Anticipated price for the item"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Manufactured ID",
        data_type="CE",
        length=250,
        description="Manufacturer identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Manufacturer's Catalog",
        data_type="ST",
        length=16,
        description="Manufacturer's catalog number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Vendor ID",
        data_type="CE",
        length=250,
        description="Vendor identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Vendor Catalog",
        data_type="ST",
        length=16,
        description="Vendor catalog number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Taxable",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Taxable indicator (Y/N)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Substitute Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Substitute allowed indicator (Y/N)"
    ),
}


# ============================================================================
# RQD Segment - Requisition Detail
# ============================================================================

RQD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Requisition Line Number",
        data_type="SI",
        length=4,
        description="Line number of the requisition"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Item Code - Internal",
        data_type="CE",
        length=250,
        description="Internal item code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Item Code - External",
        data_type="CE",
        length=250,
        description="External item code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Hospital Item Code",
        data_type="CE",
        length=250,
        description="Hospital item code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Requisition Quantity",
        data_type="NM",
        length=6,
        description="Quantity requested"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Requisition Unit of Measure",
        data_type="CE",
        length=250,
        description="Unit of measure"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Dept. Cost Center",
        data_type="IS",
        length=30,
        table_binding="0319",
        description="Department cost center"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Item Natural Account Code",
        data_type="IS",
        length=30,
        table_binding="0320",
        description="Natural account code"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Deliver To ID",
        data_type="CE",
        length=250,
        description="Delivery location identifier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Date Needed",
        data_type="DT",
        length=8,
        description="Date item is needed"
    ),
}


# ============================================================================
# RPT Segment - Report Type
# ============================================================================

RPT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Report Type",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0148",
        description="Type of report"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Report Subtype",
        data_type="ST",
        length=60,
        description="Subtype of the report"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Report Catalog",
        data_type="ST",
        length=60,
        description="Report catalog identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Report Description",
        data_type="TX",
        length=200,
        description="Description of the report"
    ),
}


# ============================================================================
# SAC Segment - Specimen Container Detail
# ============================================================================

SAC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="External Accession ID",
        data_type="EI",
        length=80,
        description="External accession identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Accession ID",
        data_type="EI",
        length=80,
        description="Accession identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Container Identifier",
        data_type="EI",
        length=80,
        description="Container identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Primary (Parent) Container Identifier",
        data_type="EI",
        length=80,
        description="Parent container identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Equipment Container Identifier",
        data_type="EI",
        length=80,
        description="Equipment container identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Specimen Source",
        data_type="SPS",
        length=300,
        description="Source of the specimen"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Registration Date/Time",
        data_type="DTM",
        length=24,
        description="Registration date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Container Status",
        data_type="CWE",
        length=250,
        table_binding="0370",
        description="Status of the container"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Carrier Type",
        data_type="CWE",
        length=250,
        table_binding="0371",
        description="Type of carrier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Carrier Identifier",
        data_type="EI",
        length=80,
        description="Carrier identifier"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Position in Carrier",
        data_type="NA",
        length=20,
        description="Position within carrier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Tray Type - SAC",
        data_type="CWE",
        length=250,
        table_binding="0372",
        description="Type of tray"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Tray Identifier",
        data_type="EI",
        length=80,
        description="Tray identifier"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Position in Tray",
        data_type="NA",
        length=20,
        description="Position within tray"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Location",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Location information"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Container Height",
        data_type="NM",
        length=5,
        description="Height of container"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Container Diameter",
        data_type="NM",
        length=5,
        description="Diameter of container"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Barrier Delta Height",
        data_type="NM",
        length=5,
        description="Barrier delta height"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Bottom Delta",
        data_type="NM",
        length=5,
        description="Bottom delta"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Container Height/Diameter/Delta Units",
        data_type="CWE",
        length=250,
        table_binding="0373",
        description="Units for height/diameter/delta"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Container Volume",
        data_type="NM",
        length=5,
        description="Volume of container"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Available Specimen Volume",
        data_type="NM",
        length=5,
        description="Available specimen volume"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Initial Specimen Volume",
        data_type="NM",
        length=5,
        description="Initial specimen volume"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Volume Units",
        data_type="CWE",
        length=250,
        table_binding="0374",
        description="Units for volume"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Separator Type",
        data_type="CWE",
        length=250,
        table_binding="0375",
        description="Type of separator"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Cap Type",
        data_type="CWE",
        length=250,
        table_binding="0376",
        description="Type of cap"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Additive",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0371",
        description="Additive information"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Specimen Component",
        data_type="CWE",
        length=250,
        table_binding="0377",
        description="Component of specimen"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Dilution Factor",
        data_type="SN",
        length=20,
        description="Dilution factor"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Treatment",
        data_type="CWE",
        length=250,
        table_binding="0378",
        description="Treatment information"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Temperature",
        data_type="CWE",
        length=250,
        table_binding="0379",
        description="Temperature information"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Hemolysis Index",
        data_type="NM",
        length=5,
        description="Hemolysis index"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Hemolysis Index Units",
        data_type="CWE",
        length=250,
        description="Units for hemolysis index"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Lipemia Index",
        data_type="NM",
        length=5,
        description="Lipemia index"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Lipemia Index Units",
        data_type="CWE",
        length=250,
        description="Units for lipemia index"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Icterus Index",
        data_type="NM",
        length=5,
        description="Icterus index"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Icterus Index Units",
        data_type="CWE",
        length=250,
        description="Units for icterus index"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Fibrin Index",
        data_type="NM",
        length=5,
        description="Fibrin index"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Fibrin Index Units",
        data_type="CWE",
        length=250,
        description="Units for fibrin index"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="System Induced Contaminants",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0378",
        description="System induced contaminants"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Drug Interference",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0382",
        description="Drug interference information"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Artificial Blood",
        data_type="CWE",
        length=250,
        table_binding="0375",
        description="Artificial blood information"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Special Handling Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0376",
        description="Special handling codes"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Other Environmental Factors",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0383",
        description="Other environmental factors"
    ),
}


# ============================================================================
# SCD Segment - Anti-Microbial Cycle Data
# ============================================================================

SCD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Cycle Start Time",
        data_type="TM",
        length=8,
        description="Start time of the cycle"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Cycle Count",
        data_type="NM",
        length=4,
        description="Number of cycles"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Temp Max",
        data_type="CQ",
        length=20,
        description="Maximum temperature"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Temp Min",
        data_type="CQ",
        length=20,
        description="Minimum temperature"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Load Number",
        data_type="NM",
        length=4,
        description="Load number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Condition Time",
        data_type="CQ",
        length=20,
        description="Conditioning time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Sterilization Time",
        data_type="CQ",
        length=20,
        description="Sterilization time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Aeration Time",
        data_type="CQ",
        length=20,
        description="Aeration time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Aeration Temperature",
        data_type="CQ",
        length=20,
        description="Aeration temperature"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Aeration Pressure",
        data_type="CQ",
        length=20,
        description="Aeration pressure"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Humidity",
        data_type="CQ",
        length=20,
        description="Humidity level"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Humidity Rate",
        data_type="CQ",
        length=20,
        description="Humidity rate"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Flow Rate",
        data_type="CQ",
        length=20,
        description="Flow rate"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Pressure",
        data_type="CQ",
        length=20,
        description="Pressure"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Preconditioning",
        data_type="CE",
        length=250,
        description="Preconditioning information"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Monitored Parameter",
        data_type="CE",
        length=250,
        repeating=True,
        description="Monitored parameters"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Procedure Identifier",
        data_type="CE",
        length=250,
        description="Procedure identifier"
    ),
}


# ============================================================================
# SCP Segment - Anti-Microbial Cycle Data - Phase
# ============================================================================

SCP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Number of Cycles (Trays)",
        data_type="NM",
        length=4,
        description="Number of cycles or trays"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Number of Probes",
        data_type="NM",
        length=4,
        description="Number of probes"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Set Temperature - Degrees",
        data_type="NM",
        length=5,
        description="Set temperature in degrees"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Set Temperature - Units",
        data_type="CE",
        length=250,
        description="Temperature units"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Set Duration - Seconds",
        data_type="NM",
        length=6,
        description="Set duration in seconds"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Set Duration - Units",
        data_type="CE",
        length=250,
        description="Duration units"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Set Pressure - Units",
        data_type="CE",
        length=250,
        description="Pressure units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Set Flow Rate - Units",
        data_type="CE",
        length=250,
        description="Flow rate units"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Cycle Start Time",
        data_type="TM",
        length=8,
        description="Start time of the cycle"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Cycle End Time",
        data_type="TM",
        length=8,
        description="End time of the cycle"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Set Change Parameter",
        data_type="CE",
        length=250,
        description="Set change parameter"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Cycle Machine Status",
        data_type="CE",
        length=250,
        table_binding="0380",
        description="Machine status during cycle"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Set Chamber Temperature - Degrees",
        data_type="NM",
        length=5,
        description="Set chamber temperature in degrees"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Set Chamber Temperature - Units",
        data_type="CE",
        length=250,
        description="Chamber temperature units"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Set Chamber Pressure - Units",
        data_type="CE",
        length=250,
        description="Chamber pressure units"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Set Chamber Humidity - Units",
        data_type="CE",
        length=250,
        description="Chamber humidity units"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Actual Cycle Time",
        data_type="TM",
        length=8,
        description="Actual cycle time"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Actual Temperature - Degrees",
        data_type="NM",
        length=5,
        description="Actual temperature in degrees"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Actual Temperature - Units",
        data_type="CE",
        length=250,
        description="Actual temperature units"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Actual Duration - Seconds",
        data_type="NM",
        length=6,
        description="Actual duration in seconds"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Actual Duration - Units",
        data_type="CE",
        length=250,
        description="Actual duration units"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Actual Pressure - Units",
        data_type="CE",
        length=250,
        description="Actual pressure units"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Actual Flow Rate - Units",
        data_type="CE",
        length=250,
        description="Actual flow rate units"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Actual Chamber Temperature - Degrees",
        data_type="NM",
        length=5,
        description="Actual chamber temperature in degrees"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Actual Chamber Temperature - Units",
        data_type="CE",
        length=250,
        description="Actual chamber temperature units"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Actual Chamber Pressure - Units",
        data_type="CE",
        length=250,
        description="Actual chamber pressure units"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Actual Chamber Humidity - Units",
        data_type="CE",
        length=250,
        description="Actual chamber humidity units"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Exit Temperature - Degrees",
        data_type="NM",
        length=5,
        description="Exit temperature in degrees"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Exit Temperature - Units",
        data_type="CE",
        length=250,
        description="Exit temperature units"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Exit Pressure - Units",
        data_type="CE",
        length=250,
        description="Exit pressure units"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Exit Humidity - Units",
        data_type="CE",
        length=250,
        description="Exit humidity units"
    ),
}


# ============================================================================
# SDD Segment - Sterilization Device Data
# ============================================================================

SDD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Lot Number",
        data_type="ST",
        length=20,
        description="Lot number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Device Number",
        data_type="EI",
        length=80,
        description="Device identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Device Name",
        data_type="ST",
        length=20,
        description="Name of the device"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Device Data State",
        data_type="CE",
        length=250,
        table_binding="0381",
        description="State of device data"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Load Status",
        data_type="CE",
        length=250,
        table_binding="0382",
        description="Status of the load"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Control Code",
        data_type="CE",
        length=250,
        table_binding="0383",
        description="Control code"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Operator Name",
        data_type="XCN",
        length=250,
        description="Name of operator"
    ),
}


# ============================================================================
# SID Segment - Substance Identifier
# ============================================================================

SID_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Application/Method Identifier",
        data_type="CE",
        length=250,
        description="Application or method identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Substance Lot Number",
        data_type="ST",
        length=20,
        description="Lot number of substance"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Substance Container Identifier",
        data_type="EI",
        length=80,
        description="Container identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Substance Manufacturer Identifier",
        data_type="CE",
        length=250,
        description="Manufacturer identifier"
    ),
}


# ============================================================================
# SLT Segment - Sterilization Lot
# ============================================================================

SLT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Device Number",
        data_type="EI",
        length=80,
        description="Device identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Device Name",
        data_type="ST",
        length=20,
        description="Name of the device"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Lot Number",
        data_type="EI",
        length=80,
        description="Lot identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Item Identifier",
        data_type="EI",
        length=80,
        description="Item identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Bar Code",
        data_type="ST",
        length=20,
        description="Bar code"
    ),
}


# ============================================================================
# SPR Segment - Stored Procedure Request Definition
# ============================================================================

SPR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Name",
        data_type="ST",
        length=20,
        required=True,
        description="Name of the query"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Input Parameter List",
        data_type="QIP",
        length=256,
        repeating=True,
        description="Input parameters for the query"
    ),
}


# ============================================================================
# TCC Segment - Test Code Configuration
# ============================================================================

TCC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Universal Service Identifier",
        data_type="CE",
        length=250,
        required=True,
        description="Universal service identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Equipment Test Application Identifier",
        data_type="IS",
        length=20,
        table_binding="0367",
        description="Equipment test application identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Specimen Source",
        data_type="SPS",
        length=300,
        description="Source of specimen"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Auto-Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Default auto-dilution factor"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Rerun Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Default rerun dilution factor"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Pre-Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Default pre-dilution factor"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Endogenous Content of Pre-Dilution Diluent",
        data_type="SN",
        length=20,
        description="Endogenous content of pre-dilution diluent"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Inventory Limits Warning Level",
        data_type="NM",
        length=5,
        description="Warning level for inventory limits"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Automatic Rerun Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Automatic rerun allowed indicator (Y/N)"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Automatic Repeat Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Automatic repeat allowed indicator (Y/N)"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Automatic Reflex Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Automatic reflex allowed indicator (Y/N)"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Equipment Dynamic Range",
        data_type="SN",
        length=20,
        description="Dynamic range of equipment"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Units",
        data_type="CE",
        length=250,
        description="Units of measurement"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Processing Type",
        data_type="ID",
        length=1,
        table_binding="0388",
        description="Type of processing"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Test Criticality",
        data_type="ID",
        length=1,
        table_binding="0389",
        description="Criticality of the test"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="QC Test Required",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="QC test required indicator (Y/N)"
    ),
}


# ============================================================================
# TCD Segment - Test Code Detail
# ============================================================================

TCD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Universal Service Identifier",
        data_type="CE",
        length=250,
        required=True,
        description="Universal service identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Auto-Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Default auto-dilution factor"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Rerun Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Default rerun dilution factor"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Pre-Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Default pre-dilution factor"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Endogenous Content of Pre-Dilution Diluent",
        data_type="SN",
        length=20,
        description="Endogenous content of pre-dilution diluent"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Automatic Rerun Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Automatic rerun allowed indicator (Y/N)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Automatic Repeat Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Automatic repeat allowed indicator (Y/N)"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Automatic Reflex Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Automatic reflex allowed indicator (Y/N)"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Equipment Dynamic Range",
        data_type="SN",
        length=20,
        description="Dynamic range of equipment"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Units",
        data_type="CE",
        length=250,
        description="Units of measurement"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Processing Type",
        data_type="ID",
        length=1,
        table_binding="0388",
        description="Type of processing"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Test Criticality",
        data_type="ID",
        length=1,
        table_binding="0389",
        description="Criticality of the test"
    ),
}


# ============================================================================
# UAC Segment - User Authentication Credential
# ============================================================================

UAC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="User Authentication Credential Type Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0485",
        description="Type of authentication credential"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="User Authentication Credential",
        data_type="ED",
        length=65536,
        required=True,
        description="Authentication credential data"
    ),
}


# ============================================================================
# VAR Segment - Variance
# ============================================================================

VAR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Variance Instance ID",
        data_type="EI",
        length=80,
        required=True,
        description="Instance identifier for the variance"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Documented Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time when variance was documented"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Stated Variance Date/Time",
        data_type="DTM",
        length=24,
        description="Stated date/time of variance"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Variance Originator",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who originated the variance"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Variance Classification",
        data_type="CWE",
        length=250,
        table_binding="0384",
        description="Classification of the variance"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Variance Description",
        data_type="ST",
        length=512,
        repeating=True,
        description="Description of the variance"
    ),
}


# ============================================================================
# FT1 (Financial Transaction) Segment Field Definitions
# ============================================================================

FT1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - FT1",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Transaction ID",
        data_type="ST",
        length=12,
        description="Unique transaction identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Transaction Batch ID",
        data_type="ST",
        length=10,
        description="Batch identifier for grouping transactions"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Transaction Date",
        data_type="DR",
        length=53,
        description="Date range for transaction"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Transaction Posting Date",
        data_type="TS",
        length=26,
        description="Date/time transaction was posted"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Transaction Type",
        data_type="IS",
        length=8,
        table_binding="0017",
        description="Type of transaction"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Transaction Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0132",
        description="Code identifying the transaction"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Transaction Description",
        data_type="ST",
        length=40,
        description="Description of transaction"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Transaction Description - Alt",
        data_type="ST",
        length=40,
        description="Alternate description"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Transaction Quantity",
        data_type="NM",
        length=16,
        description="Quantity for transaction"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Transaction Amount - Extended",
        data_type="CP",
        length=12,
        description="Extended transaction amount"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Transaction Quantity Units",
        data_type="CE",
        length=250,
        description="Units for transaction quantity"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Department Code",
        data_type="CE",
        length=250,
        table_binding="0049",
        description="Department code"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Insurance Plan ID",
        data_type="CE",
        length=250,
        table_binding="0072",
        description="Insurance plan identifier"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Insurance Amount",
        data_type="CP",
        length=12,
        description="Insurance payment amount"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Assigned Patient Location",
        data_type="PL",
        length=80,
        description="Patient location"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Fee Schedule",
        data_type="IS",
        length=1,
        table_binding="0024",
        description="Fee schedule code"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Patient Type",
        data_type="CE",
        length=250,
        table_binding="0018",
        description="Type of patient"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Diagnosis Code - FT1",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0051",
        description="Diagnosis code"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Performed By Code",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who performed service"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Ordered By Code",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who ordered service",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
        }
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Unit Cost",
        data_type="CP",
        length=12,
        description="Cost per unit",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
        }
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Filler Order Number",
        data_type="EI",
        length=75,
        description="Filler order number",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
        }
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Entered By Code",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who entered transaction",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
        }
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Procedure Code",
        data_type="CE",
        length=250,
        table_binding="0088",
        description="Procedure code",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
        }
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Procedure Code Modifier",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0340",
        description="Procedure code modifier",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
        }
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Advanced Beneficiary Notice Code",
        data_type="CE",
        length=250,
        table_binding="0339",
        description="Advanced beneficiary notice code",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
            "2.5": {"required": False},
            "2.6": {"required": False},
        }
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Medically Necessary Duplicate Procedure Reason",
        data_type="CWE",
        length=250,
        table_binding="0476",
        description="Reason for duplicate procedure",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
            "2.5": {"required": False},
            "2.6": {"required": False},
        }
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="NDC Code",
        data_type="CWE",
        length=250,
        description="National Drug Code",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
            "2.5": {"required": False},
            "2.6": {"required": False},
        }
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Payment Reference ID",
        data_type="CX",
        length=250,
        repeating=True,
        description="Payment reference identifier",
        version_specific={
            "2.1": {"required": False},
            "2.2": {"required": False},
            "2.3": {"required": False},
            "2.4": {"required": False},
            "2.5": {"required": False},
            "2.6": {"required": False},
        }
    ),
}


# ============================================================================
# SFT (Software) Segment Field Definitions
# ============================================================================

SFT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Software Vendor Organization",
        data_type="XON",
        length=250,
        description="Organization that developed the software"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Software Certified Version or Release Number",
        data_type="ST",
        length=20,
        description="Certified version or release number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Software Product Name",
        data_type="ST",
        length=20,
        description="Name of software product"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Software Binary ID",
        data_type="ST",
        length=20,
        description="Binary identifier for software"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Software Product Information",
        data_type="TX",
        length=65536,
        description="Additional product information"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Software Install Date",
        data_type="TS",
        length=26,
        description="Date/time software was installed"
    ),
}


# ============================================================================
# PDA Segment - Patient Death and Autopsy
# ============================================================================

PDA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Death Cause Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0385",
        description="Code indicating cause of death"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Death Location",
        data_type="PL",
        length=200,
        description="Location where death occurred"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Death Certified Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Death certified indicator (Y/N)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Death Certificate Signed Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time death certificate was signed"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Death Certified By",
        data_type="XCN",
        length=250,
        description="Person who certified death"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Autopsy Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Autopsy indicator (Y/N)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Autopsy Start Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time autopsy started"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Autopsy End Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time autopsy ended"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Autopsy Performed By",
        data_type="XCN",
        length=250,
        description="Person who performed autopsy"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Coroner Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Coroner indicator (Y/N)"
    ),
}


# ============================================================================
# CSR Segment - Clinical Study Registration
# ============================================================================

CSR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sponsor Study ID",
        data_type="EI",
        length=60,
        required=True,
        description="Sponsor's unique identifier for the study"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Alternate Study ID",
        data_type="EI",
        length=60,
        description="Alternate identifier for the study"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Institution Registering the Patient",
        data_type="CE",
        length=250,
        description="Institution where patient is registered"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Sponsor Patient ID",
        data_type="CX",
        length=250,
        required=True,
        description="Sponsor's unique identifier for the patient"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Alternate Patient ID - CSR",
        data_type="CX",
        length=250,
        description="Alternate patient identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Date/Time of Patient Study Registration",
        data_type="TS",
        length=26,
        description="Date/time patient was registered in study"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Person Performing Study Registration",
        data_type="XCN",
        length=250,
        description="Person who registered patient in study"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Study Authorizing Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Provider who authorized patient participation"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Date/Time Patient Study Consent Signed",
        data_type="TS",
        length=26,
        description="Date/time consent was signed"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Patient Study Eligibility Status",
        data_type="CE",
        length=250,
        table_binding="0716",
        description="Eligibility status for study"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Study Randomization Date/Time",
        data_type="TS",
        length=26,
        description="Date/time patient was randomized"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Randomized Study Arm",
        data_type="CE",
        length=250,
        repeating=True,
        description="Study arm to which patient was randomized"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Stratum for Study Randomization",
        data_type="CE",
        length=250,
        repeating=True,
        description="Stratum used for randomization"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Patient Evaluability Status",
        data_type="CE",
        length=250,
        table_binding="0717",
        description="Evaluability status"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Date/Time Ended Study",
        data_type="TS",
        length=26,
        description="Date/time patient ended participation"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Reason Ended Study",
        data_type="CE",
        length=250,
        table_binding="0718",
        description="Reason patient ended participation"
    ),
}


# ============================================================================
# CSS Segment - Clinical Study Data Schedule Segment
# ============================================================================

CSS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Study Scheduled Time Point",
        data_type="CE",
        length=250,
        required=True,
        description="Scheduled time point identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Study Scheduled Patient Time Point",
        data_type="ST",
        length=26,
        description="Patient-specific time point"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Study Quality Control Codes",
        data_type="CE",
        length=250,
        repeating=True,
        description="Quality control codes"
    ),
}


# ============================================================================
# CTI Segment - Clinical Trial Identification
# ============================================================================

CTI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sponsor Study ID",
        data_type="EI",
        length=60,
        required=True,
        description="Sponsor's unique identifier for the study"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Study Phase Identifier",
        data_type="CE",
        length=250,
        description="Phase of the clinical trial"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Study Scheduled Time Point",
        data_type="CE",
        length=250,
        description="Scheduled time point in study"
    ),
}


# ============================================================================
# DSP Segment - Display Data
# ============================================================================

DSP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - DSP",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Display Level",
        data_type="SI",
        length=4,
        description="Display level for hierarchical display"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Data Line",
        data_type="TX",
        length=300,
        required=True,
        description="Line of data to display"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Logical Break Point",
        data_type="ST",
        length=2,
        description="Logical break point indicator"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Segment Result ID",
        data_type="ST",
        length=20,
        description="Result identifier"
    ),
}


# ============================================================================
# ECD Segment - Equipment Command
# ============================================================================

ECD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Reference Command Number",
        data_type="NM",
        length=20,
        required=True,
        description="Reference number for command"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Remote Control Command",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0368",
        description="Command to be executed"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Response Required",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Response required indicator (Y/N)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Requested Completion Time",
        data_type="TQ",
        length=200,
        description="Requested completion time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Parameters",
        data_type="TX",
        length=65536,
        description="Command parameters"
    ),
}


# ============================================================================
# ECR Segment - Equipment Command Response
# ============================================================================

ECR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Command Response",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0387",
        description="Response to command"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Date/Time Completed",
        data_type="TS",
        length=26,
        description="Date/time command completed"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Response Data",
        data_type="TX",
        length=65536,
        description="Response data"
    ),
}


# ============================================================================
# EDU Segment - Educational Detail
# ============================================================================

EDU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - EDU",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Academic Degree",
        data_type="IS",
        length=10,
        table_binding="0360",
        description="Academic degree"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Academic Degree Program Date Range",
        data_type="DR",
        length=52,
        description="Date range of degree program"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Academic Degree Program Participation Date Range",
        data_type="DR",
        length=52,
        description="Participation date range"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Academic Degree Granted Date",
        data_type="DT",
        length=8,
        description="Date degree was granted"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="School",
        data_type="XON",
        length=250,
        description="School name"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="School Type Code",
        data_type="CE",
        length=250,
        table_binding="0402",
        description="Type of school"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="School Address",
        data_type="XAD",
        length=250,
        description="School address"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Major Field of Study",
        data_type="CE",
        length=250,
        repeating=True,
        description="Major field of study"
    ),
}


# ============================================================================
# EQL Segment - Embedded Query Language
# ============================================================================

EQL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query/Response Format Code",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0106",
        description="Format code for query/response"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="EQL Query Statement",
        data_type="ST",
        length=4096,
        required=True,
        description="Embedded query language statement"
    ),
}


# ============================================================================
# EQP Segment - Equipment/Log Service
# ============================================================================

EQP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Event Type",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0450",
        description="Type of equipment/log event"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="File Name",
        data_type="ST",
        length=20,
        description="Name of log file"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time of log"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="End Date/Time",
        data_type="TS",
        length=26,
        description="End date/time of log"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Transaction Data",
        data_type="FT",
        length=65536,
        description="Transaction data"
    ),
}


# ============================================================================
# EQU Segment - Equipment Detail
# ============================================================================

EQU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Equipment Instance Identifier",
        data_type="EI",
        length=60,
        required=True,
        description="Unique identifier for equipment instance"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Event Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of event"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Equipment State",
        data_type="CE",
        length=250,
        table_binding="0365",
        description="Current state of equipment"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Local/Remote Control State",
        data_type="CE",
        length=250,
        table_binding="0366",
        description="Local or remote control state"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Alert Level",
        data_type="CE",
        length=250,
        table_binding="0367",
        description="Alert level"
    ),
}


# ============================================================================
# ERQ Segment - Equipment/Log Service Request
# ============================================================================

ERQ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Event Type",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0450",
        description="Type of equipment/log event"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Name of Log File",
        data_type="ST",
        length=20,
        description="Name of log file to retrieve"
    ),
}


# ============================================================================
# ARV Segment - Access Restriction
# ============================================================================

ARV_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - ARV",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Access Restriction Action Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0718",
        description="Action code for access restriction"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Access Restriction Value",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0719",
        description="Value of access restriction"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Access Restriction Reason",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0720",
        description="Reason for access restriction"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Special Access Restriction Instructions",
        data_type="ST",
        length=80,
        repeating=True,
        description="Special instructions for access restriction"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Access Restriction Date Range",
        data_type="DR",
        length=53,
        description="Date range for access restriction"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Security Classification Tag",
        data_type="CE",
        length=250,
        table_binding="0717",
        description="Security classification"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Security Handling Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0716",
        description="Security handling instructions"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Access Restriction Message Location",
        data_type="ST",
        length=80,
        repeating=True,
        description="Location of access restriction message"
    ),
}


# ============================================================================
# AUT Segment - Authorization Information
# ============================================================================

AUT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Authorizing Payor, Plan ID",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0072",
        description="Authorizing payor plan identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Authorizing Payor, Company ID",
        data_type="CE",
        length=250,
        table_binding="0285",
        description="Authorizing payor company identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Authorizing Payor, Company Name",
        data_type="ST",
        length=45,
        description="Authorizing payor company name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Authorization Effective Date",
        data_type="TS",
        length=26,
        description="Date authorization becomes effective"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Authorization Expiration Date",
        data_type="TS",
        length=26,
        description="Date authorization expires"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Authorization Identifier",
        data_type="EI",
        length=30,
        description="Authorization identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Reimbursement Limit",
        data_type="CP",
        length=25,
        description="Reimbursement limit amount"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Requested Number of Treatments",
        data_type="NM",
        length=2,
        description="Number of treatments requested"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Authorized Number of Treatments",
        data_type="NM",
        length=2,
        description="Number of treatments authorized"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Process Date",
        data_type="TS",
        length=26,
        description="Date authorization was processed"
    ),
}


# ============================================================================
# BPO Segment - Blood Product Order
# ============================================================================

BPO_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - BPO",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="BP Universal Service ID",
        data_type="CE",
        length=250,
        required=True,
        description="Blood product universal service identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="BP Processing Requirements",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0508",
        description="Blood product processing requirements"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="BP Quantity",
        data_type="NM",
        length=5,
        required=True,
        description="Quantity of blood product"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="BP Amount",
        data_type="NM",
        length=10,
        description="Amount of blood product"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="BP Units",
        data_type="CE",
        length=250,
        description="Units for blood product"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="BP Intended Use Date/Time",
        data_type="TS",
        length=26,
        description="Date/time blood product intended for use"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="BP Intended Dispense From Location",
        data_type="PL",
        length=80,
        description="Location to dispense blood product from"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="BP Intended Dispense From Address",
        data_type="XAD",
        length=250,
        description="Address to dispense blood product from"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="BP Requested Dispense Date/Time",
        data_type="TS",
        length=26,
        description="Date/time blood product requested for dispense"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="BP Requested Quantity",
        data_type="NM",
        length=5,
        description="Requested quantity of blood product"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="BP Requested Amount",
        data_type="NM",
        length=10,
        description="Requested amount of blood product"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="BP Requested Units",
        data_type="CE",
        length=250,
        description="Requested units for blood product"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="BP Intended Use Code",
        data_type="CE",
        length=250,
        table_binding="0509",
        description="Intended use code for blood product"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="BP Intended Dispense To Location",
        data_type="PL",
        length=80,
        description="Location to dispense blood product to"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="BP Requested Dispense To Address",
        data_type="XAD",
        length=250,
        description="Address to dispense blood product to"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="BP Blood Type",
        data_type="CE",
        length=250,
        table_binding="0501",
        description="Blood type required"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="BP Special Testing Requirements",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0510",
        description="Special testing requirements"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="BP Special Processing Requirements",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0511",
        description="Special processing requirements"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="BP Special Delivery Requirements",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0512",
        description="Special delivery requirements"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="BP Order Date/Time",
        data_type="TS",
        length=26,
        description="Date/time blood product order was placed"
    ),
}


# ============================================================================
# BPX Segment - Blood Product Dispense Status
# ============================================================================

BPX_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - BPX",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="BP Dispense Status",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0513",
        description="Blood product dispense status"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="BP Status Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of status change"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="BC Donation ID",
        data_type="EI",
        length=22,
        description="Blood component donation identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="BC Component",
        data_type="CE",
        length=250,
        table_binding="0514",
        description="Blood component type"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="BC Donation Type / Intended Use",
        data_type="CE",
        length=250,
        table_binding="0515",
        description="Donation type or intended use"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="CP Commercial Product",
        data_type="CE",
        length=250,
        table_binding="0516",
        description="Commercial product code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="CP Manufacturer",
        data_type="XON",
        length=250,
        description="Commercial product manufacturer"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="CP Lot Number",
        data_type="EI",
        length=22,
        description="Commercial product lot number"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="BP Blood Group",
        data_type="CE",
        length=250,
        table_binding="0517",
        description="Blood group"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="BC Special Testing",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0518",
        description="Special testing performed"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="BP Expiration Date/Time",
        data_type="TS",
        length=26,
        description="Blood product expiration date/time"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="BP Quantity",
        data_type="NM",
        length=5,
        required=True,
        description="Quantity of blood product"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="BP Amount",
        data_type="NM",
        length=10,
        description="Amount of blood product"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="BP Units",
        data_type="CE",
        length=250,
        description="Units for blood product"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="BP Unique ID",
        data_type="EI",
        length=22,
        description="Unique identifier for blood product"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="BP Actual Dispensed To Location",
        data_type="PL",
        length=80,
        description="Location blood product was dispensed to"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="BP Actual Dispensed To Address",
        data_type="XAD",
        length=250,
        description="Address blood product was dispensed to"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="BP Dispensed To Receiver",
        data_type="XCN",
        length=250,
        description="Person who received blood product"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="BP Dispensing Individual",
        data_type="XCN",
        length=250,
        description="Person who dispensed blood product"
    ),
}


# ============================================================================
# BUI Segment - Blood Product Usage Information
# ============================================================================

BUI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - BUI",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Blood Product Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0519",
        description="Blood product code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Blood Amount",
        data_type="CQ",
        length=267,
        required=True,
        description="Amount of blood product used"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Transfusion Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of transfusion"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administrative Duration",
        data_type="CQ",
        length=267,
        description="Duration of administration"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Blood Start Date/Time",
        data_type="TS",
        length=26,
        description="Date/time blood product administration started"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Blood End Date/Time",
        data_type="TS",
        length=26,
        description="Date/time blood product administration ended"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administered Amount of Blood Product",
        data_type="CQ",
        length=267,
        description="Amount of blood product actually administered"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administered Blood Product Units",
        data_type="CE",
        length=250,
        description="Units for administered blood product"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administered Blood Product Volume",
        data_type="NM",
        length=10,
        description="Volume of blood product administered"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Wasted Amount of Blood Product",
        data_type="CQ",
        length=267,
        description="Amount of blood product wasted"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Wasted Blood Product Units",
        data_type="CE",
        length=250,
        description="Units for wasted blood product"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Wasted Blood Product Volume",
        data_type="NM",
        length=10,
        description="Volume of wasted blood product"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="BP Reaction",
        data_type="CE",
        length=250,
        table_binding="0520",
        description="Blood product reaction code"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="BP Transfusion Disposition Status",
        data_type="ID",
        length=1,
        table_binding="0513",
        description="Transfusion disposition status"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="BP Unique ID",
        data_type="EI",
        length=22,
        description="Unique identifier for blood product"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="BP Actual Dispensed To Location",
        data_type="PL",
        length=80,
        description="Location blood product was dispensed to"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="BP Actual Dispensed To Address",
        data_type="XAD",
        length=250,
        description="Address blood product was dispensed to"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="BP Dispensed To Receiver",
        data_type="XCN",
        length=250,
        description="Person who received blood product"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="BP Dispensing Individual",
        data_type="XCN",
        length=250,
        description="Person who dispensed blood product"
    ),
}

# ============================================================================
# IAM Segment - Patient Adverse Reaction Information
# ============================================================================

IAM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - IAM",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Allergen Type Code",
        data_type="CE",
        length=250,
        table_binding="0127",
        description="Type of allergen"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Allergen Code/Mnemonic/Description",
        data_type="CE",
        length=250,
        required=True,
        description="Allergen identification"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Allergy Severity Code",
        data_type="CE",
        length=250,
        table_binding="0128",
        description="Severity of allergy"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Allergy Reaction Code",
        data_type="ST",
        length=15,
        description="Reaction description"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Identification Date",
        data_type="DT",
        length=8,
        description="Date allergy was identified"
    ),
}

# ============================================================================
# IAR Segment - Allergy Reaction
# ============================================================================

IAR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Allergy Reaction Code",
        data_type="CE",
        length=250,
        required=True,
        description="Reaction code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Allergy Severity Code",
        data_type="CE",
        length=250,
        table_binding="0128",
        description="Severity of reaction"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Sensitivity to Causative Agent Code",
        data_type="CE",
        length=250,
        description="Sensitivity information"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Management",
        data_type="ST",
        length=60,
        description="Management instructions"
    ),
}

# ============================================================================
# MFI Segment - Master File Identification
# ============================================================================

MFI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Master File Identifier",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0175",
        description="Type of master file"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Master File Application Identifier",
        data_type="HD",
        length=227,
        description="Application that owns master file"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="File-Level Event Code",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0178",
        description="Event type (REP=Replace, UPD=Update, etc.)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Entered Date/Time",
        data_type="TS",
        length=26,
        description="Date/time entered"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Effective Date/Time",
        data_type="TS",
        length=26,
        description="Effective date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Response Level Code",
        data_type="ID",
        length=1,
        table_binding="0179",
        description="Response level"
    ),
}

# ============================================================================
# MFE Segment - Master File Entry
# ============================================================================

MFE_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Record-Level Event Code",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0180",
        description="Event type (MAD=Add, MUP=Update, MDL=Delete, etc.)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="MFN Control ID",
        data_type="ST",
        length=20,
        description="Control ID for master file notification"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Effective Date/Time",
        data_type="TS",
        length=26,
        description="Effective date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Primary Key Value - MFE",
        data_type="CE",
        length=250,
        required=True,
        description="Primary key for master file entry"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Primary Key Value Type",
        data_type="ID",
        length=3,
        table_binding="0355",
        description="Type of primary key"
    ),
}

# ============================================================================
# MFA Segment - Master File Acknowledgment
# ============================================================================

MFA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Record-Level Event Code",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0180",
        description="Event type"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="MFN Control ID",
        data_type="ST",
        length=20,
        description="Control ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Completion Date/Time",
        data_type="TS",
        length=26,
        description="Completion date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="MFN Record Level Error Return",
        data_type="CE",
        length=250,
        table_binding="0181",
        description="Error code if processing failed"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Primary Key Value - MFA",
        data_type="CE",
        length=250,
        required=True,
        description="Primary key value"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Primary Key Value Type - MFA",
        data_type="ID",
        length=3,
        table_binding="0355",
        description="Primary key type"
    ),
}

# ============================================================================
# OM1 Segment - General Segment
# ============================================================================

OM1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Universal Service Identifier",
        data_type="CE",
        length=250,
        required=True,
        description="Service/test identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Primary Key Value - OM1",
        data_type="CE",
        length=250,
        required=True,
        description="Primary key"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Producer's Service/Test/Observation ID",
        data_type="CE",
        length=250,
        description="Producer's identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Permitted Data Types",
        data_type="ID",
        length=12,
        repeating=True,
        description="Allowed data types"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Specimen Required",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Specimen required indicator"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Producer ID",
        data_type="CE",
        length=250,
        description="Producer identifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Observation Description",
        data_type="TX",
        length=200,
        description="Description of observation"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Other Service/Test/Observation IDs for the Observation",
        data_type="CE",
        length=250,
        repeating=True,
        description="Alternative identifiers"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Other Names",
        data_type="ST",
        length=200,
        repeating=True,
        description="Other names for observation"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Preferred Report Name for the Observation",
        data_type="ST",
        length=30,
        description="Preferred report name"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Preferred Short Name or Mnemonic for Observation",
        data_type="ST",
        length=8,
        description="Short name/mnemonic"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Preferred Long Name for the Observation",
        data_type="ST",
        length=200,
        description="Long name"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Orderability",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Orderable indicator"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Identity of Instrument Used to Perform this Study",
        data_type="CE",
        length=250,
        repeating=True,
        description="Instrument identifiers"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Coded Representation of Method",
        data_type="CE",
        length=250,
        repeating=True,
        description="Method codes"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Portable Device Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Portable device indicator"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Observation Producing Department/Section",
        data_type="CE",
        length=250,
        repeating=True,
        description="Department codes"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Telephone Number of Section",
        data_type="XTN",
        length=250,
        description="Phone number"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Nature of Service/Test/Observation",
        data_type="ID",
        length=1,
        table_binding="0174",
        description="Nature of service"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Report Subheader",
        data_type="CE",
        length=250,
        description="Report subheader"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Report Display Order",
        data_type="ST",
        length=20,
        description="Display order"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Date/Time Stamp for Any Change in Definition for the Observation",
        data_type="TS",
        length=26,
        description="Last change timestamp"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Effective Date/Time of Change",
        data_type="TS",
        length=26,
        description="Effective change date/time"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Typical Turn-Around Time",
        data_type="NM",
        length=5,
        description="Turnaround time"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Typical Number of Days for Results",
        data_type="NM",
        length=3,
        description="Days for results"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Number of Produced Results",
        data_type="NM",
        length=3,
        description="Number of results"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Observations Used to Calculate the Patient Result or Estimate",
        data_type="CE",
        length=250,
        repeating=True,
        description="Input observations"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Comment",
        data_type="TX",
        length=65536,
        description="Comments"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Location Value 1",
        data_type="CE",
        length=250,
        description="Location value"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Location Value 2",
        data_type="CE",
        length=250,
        description="Location value"
    ),
}

# ============================================================================
# OM2 Segment - Numeric Observation
# ============================================================================

OM2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Units of Measure",
        data_type="CE",
        length=250,
        description="Units"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Range of Decimal Precision",
        data_type="NM",
        length=10,
        description="Decimal precision"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Corresponding SI Units of Measure",
        data_type="CE",
        length=250,
        description="SI units"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="SI Conversion Factor",
        data_type="TX",
        length=60,
        description="Conversion factor"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Reference (Normal) Range - Ordinal and Continuous Observations",
        data_type="CM",
        length=250,
        repeating=True,
        description="Normal range"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Critical Range for Ordinal and Continuous Observations",
        data_type="CM",
        length=250,
        repeating=True,
        description="Critical range"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Absolute Range for Ordinal and Continuous Observations",
        data_type="CM",
        length=250,
        repeating=True,
        description="Absolute range"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Delta Check Criteria",
        data_type="CM",
        length=200,
        repeating=True,
        description="Delta check criteria"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Minimum Meaningful Increments",
        data_type="NM",
        length=20,
        description="Minimum increment"
    ),
}

# ============================================================================
# OM3 Segment - Categorical Service/Test/Observation
# ============================================================================

OM3_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Preferred Coding System",
        data_type="CE",
        length=250,
        description="Preferred coding system"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Valid Coded Answers",
        data_type="CE",
        length=250,
        repeating=True,
        description="Valid coded answers"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Normal Text/Codes for Categorical Observations",
        data_type="CE",
        length=250,
        repeating=True,
        description="Normal codes"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Abnormal Text/Codes for Categorical Observations",
        data_type="CE",
        length=250,
        repeating=True,
        description="Abnormal codes"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Critical Text/Codes for Categorical Observations",
        data_type="CE",
        length=250,
        repeating=True,
        description="Critical codes"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Value Type",
        data_type="ID",
        length=2,
        table_binding="0125",
        description="Value type"
    ),
}

# ============================================================================
# OM4 Segment - Observations that Require Specimens
# ============================================================================

OM4_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Derived Specimen",
        data_type="ID",
        length=1,
        table_binding="0170",
        description="Derived specimen indicator"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Container Description",
        data_type="TX",
        length=60,
        description="Container description"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Container Volume",
        data_type="CE",
        length=250,
        description="Container volume"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Container Units",
        data_type="CE",
        length=250,
        description="Container units"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Specimen",
        data_type="CE",
        length=250,
        description="Specimen type"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Additive",
        data_type="CE",
        length=250,
        description="Additive"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Preparation",
        data_type="TX",
        length=10240,
        description="Preparation instructions"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Special Handling Requirements",
        data_type="TX",
        length=10240,
        description="Special handling"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Normal Collection Volume",
        data_type="CQ",
        length=20,
        description="Normal volume"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Minimum Collection Volume",
        data_type="CQ",
        length=20,
        description="Minimum volume"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Specimen Requirements",
        data_type="TX",
        length=10240,
        description="Specimen requirements"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Specimen Priorities",
        data_type="ID",
        length=1,
        repeating=True,
        table_binding="0027",
        description="Priority codes"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Specimen Retention Time",
        data_type="CQ",
        length=20,
        description="Retention time"
    ),
}

# ============================================================================
# OM5 Segment - Observation Batteries (Sets)
# ============================================================================

OM5_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Test/Observations Included Within an Ordered Test Battery",
        data_type="CE",
        length=250,
        repeating=True,
        required=True,
        description="Included tests"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Observation ID Suffixes",
        data_type="ST",
        length=250,
        description="ID suffixes"
    ),
}

# ============================================================================
# OM6 Segment - Observations that are Calculated from Other Observations
# ============================================================================

OM6_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Derivation Rule",
        data_type="TX",
        length=10240,
        required=True,
        description="Derivation rule"
    ),
}

# ============================================================================
# PRB Segment - Problem Detail
# ============================================================================

PRB_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Action date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Problem ID",
        data_type="CE",
        length=250,
        required=True,
        description="Problem identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Problem Instance ID",
        data_type="EI",
        length=60,
        required=True,
        description="Problem instance identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Episode of Care ID",
        data_type="EI",
        length=60,
        description="Episode identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Problem List Priority",
        data_type="NM",
        length=60,
        description="Priority"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Problem Established Date/Time",
        data_type="TS",
        length=26,
        description="Established date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Anticipated Problem Resolution Date/Time",
        data_type="TS",
        length=26,
        description="Expected resolution date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Actual Problem Resolution Date/Time",
        data_type="TS",
        length=26,
        description="Actual resolution date/time"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Problem Classification",
        data_type="CE",
        length=250,
        description="Classification"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Problem Management Discipline",
        data_type="CE",
        length=250,
        repeating=True,
        description="Management discipline"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Problem Persistence",
        data_type="CE",
        length=250,
        description="Persistence"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Problem Confirmation Status",
        data_type="CE",
        length=250,
        description="Confirmation status"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Problem Life Cycle Status",
        data_type="CE",
        length=250,
        description="Life cycle status"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Problem Life Cycle Status Date/Time",
        data_type="TS",
        length=26,
        description="Status date/time"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Problem Date of Onset",
        data_type="TS",
        length=26,
        description="Onset date/time"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Problem Onset Text",
        data_type="ST",
        length=80,
        description="Onset text"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Problem Ranking",
        data_type="CE",
        length=250,
        description="Ranking"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Certainty of Problem",
        data_type="CE",
        length=250,
        description="Certainty"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Probability of Problem (0-1)",
        data_type="NM",
        length=5,
        description="Probability"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Individual Awareness of Problem",
        data_type="CE",
        length=250,
        description="Awareness"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Problem Prognosis",
        data_type="CE",
        length=250,
        description="Prognosis"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Individual Awareness of Prognosis",
        data_type="CE",
        length=250,
        description="Awareness of prognosis"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Family/Significant Other Awareness of Problem/Prognosis",
        data_type="ST",
        length=200,
        description="Family awareness"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Security/Sensitivity",
        data_type="CE",
        length=250,
        description="Security classification"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Problem Severity",
        data_type="CE",
        length=250,
        description="Severity"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Problem Persistence",
        data_type="CE",
        length=250,
        description="Persistence"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Problem Exacerbation Date/Time",
        data_type="TS",
        length=26,
        description="Exacerbation date/time"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Problem Stabilized Date/Time",
        data_type="TS",
        length=26,
        description="Stabilized date/time"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Problem Improved Date/Time",
        data_type="TS",
        length=26,
        description="Improved date/time"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Subjective Data for Observation",
        data_type="TX",
        length=65536,
        description="Subjective data"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Objective Data for Observation",
        data_type="TX",
        length=65536,
        description="Objective data"
    ),
}

# ============================================================================
# PRC Segment - Pricing
# ============================================================================

PRC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - PRC",
        data_type="CE",
        length=250,
        required=True,
        description="Primary key"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Facility ID - PRC",
        data_type="CE",
        length=250,
        repeating=True,
        description="Facility identifiers"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Department",
        data_type="CE",
        length=250,
        repeating=True,
        description="Department codes"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Valid Patient Classes",
        data_type="IS",
        length=1,
        repeating=True,
        table_binding="0004",
        description="Valid patient classes"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Price",
        data_type="CP",
        length=12,
        description="Price"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Formula",
        data_type="ST",
        length=200,
        description="Pricing formula"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Minimum Quantity",
        data_type="NM",
        length=4,
        description="Minimum quantity"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Maximum Quantity",
        data_type="NM",
        length=4,
        description="Maximum quantity"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Minimum Price",
        data_type="MO",
        length=20,
        description="Minimum price"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Maximum Price",
        data_type="MO",
        length=20,
        description="Maximum price"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Effective Date/Time",
        data_type="TS",
        length=26,
        description="Effective date/time"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Expiration Date/Time",
        data_type="TS",
        length=26,
        description="Expiration date/time"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Price Override Flag",
        data_type="IS",
        length=1,
        table_binding="0268",
        description="Override flag"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Billing Category",
        data_type="CE",
        length=250,
        repeating=True,
        description="Billing categories"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Chargeable Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Chargeable indicator"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Active/Inactive Flag",
        data_type="ID",
        length=1,
        table_binding="0183",
        description="Active status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Cost",
        data_type="MO",
        length=20,
        description="Cost"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Charge on Indicator",
        data_type="CE",
        length=250,
        repeating=True,
        description="Charge indicators"
    ),
}

# ============================================================================
# PRD Segment - Provider Data
# ============================================================================

PRD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Provider Role",
        data_type="CE",
        length=250,
        repeating=True,
        description="Provider roles"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Provider Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Provider names"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Provider Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Provider addresses"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Provider Location",
        data_type="PL",
        length=80,
        description="Provider location"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Provider Communication Information",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Communication info"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Preferred Method of Contact",
        data_type="CE",
        length=250,
        description="Preferred contact method"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Provider Identifiers",
        data_type="PLN",
        length=100,
        repeating=True,
        description="Provider identifiers"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Effective Start Date of Provider Role",
        data_type="TS",
        length=26,
        description="Start date"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Effective End Date of Provider Role",
        data_type="TS",
        length=26,
        description="End date"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Provider Organization Name and Identifier",
        data_type="XON",
        length=250,
        description="Organization info"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Provider Organization Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Organization addresses"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Provider Organization Location Information",
        data_type="PL",
        length=80,
        repeating=True,
        description="Organization locations"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Provider Organization Communication Information",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Organization communication"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Provider Organization Method of Contact",
        data_type="CE",
        length=250,
        description="Organization contact method"
    ),
}

# ============================================================================
# PSH Segment - Product Summary Header
# ============================================================================

PSH_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Report Type",
        data_type="ST",
        length=60,
        required=True,
        description="Report type"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Report Form Identifier",
        data_type="ST",
        length=60,
        description="Form identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Report Date",
        data_type="TS",
        length=26,
        required=True,
        description="Report date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Report Interval Start Date",
        data_type="TS",
        length=26,
        description="Interval start"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Report Interval End Date",
        data_type="TS",
        length=26,
        description="Interval end"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Quantity Manufactured",
        data_type="CQ",
        length=20,
        description="Quantity manufactured"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Quantity Distributed",
        data_type="CQ",
        length=20,
        description="Quantity distributed"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Quantity Distributed Method",
        data_type="ID",
        length=1,
        table_binding="0329",
        description="Distribution method"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Quantity Distributed Comment",
        data_type="FT",
        length=600,
        description="Distribution comment"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Quantity in Use",
        data_type="CQ",
        length=20,
        description="Quantity in use"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Quantity in Use Method",
        data_type="ID",
        length=1,
        table_binding="0329",
        description="Use method"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Quantity in Use Comment",
        data_type="FT",
        length=600,
        description="Use comment"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Number of Product Experience Reports Filed by Facility",
        data_type="NM",
        length=4,
        description="Number of reports"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Number of Product Experience Reports Filed by Distributor",
        data_type="NM",
        length=4,
        description="Number of distributor reports"
    ),
}

# ============================================================================
# PTH Segment - Pathway
# ============================================================================

PTH_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Pathway ID",
        data_type="CE",
        length=250,
        required=True,
        description="Pathway identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Pathway Instance ID",
        data_type="EI",
        length=60,
        required=True,
        description="Pathway instance identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Pathway Established Date/Time",
        data_type="TS",
        length=26,
        description="Established date/time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Pathway Life Cycle Status",
        data_type="CE",
        length=250,
        description="Life cycle status"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Change Pathway Life Cycle Status Date/Time",
        data_type="TS",
        length=26,
        description="Status change date/time"
    ),
}

# ============================================================================
# ODS Segment - Dietary Orders, Supplements, and Preferences
# ============================================================================

ODS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Type",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0159",
        description="Type (D=Diet, S=Supplement, P=Preference)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Service Period",
        data_type="CE",
        length=250,
        repeating=True,
        description="Service periods"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Diet, Supplement, or Preference Code",
        data_type="CE",
        length=250,
        repeating=True,
        required=True,
        description="Diet/supplement codes"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Text Instruction",
        data_type="ST",
        length=80,
        repeating=True,
        description="Text instructions"
    ),
}

# ============================================================================
# ODT Segment - Diet Tray Instructions
# ============================================================================

ODT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Tray Type",
        data_type="CE",
        length=250,
        required=True,
        description="Tray type"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Service Period",
        data_type="CE",
        length=250,
        repeating=True,
        description="Service periods"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Text Instruction",
        data_type="ST",
        length=80,
        repeating=True,
        description="Text instructions"
    ),
}

# ============================================================================
# OMS Segment - Specialty Type
# ============================================================================

OMS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        description="Segment type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Sequence/Test/Observation Master File",
        data_type="CE",
        length=250,
        repeating=True,
        description="Test/observation identifiers"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Derived Specialty Type",
        data_type="CE",
        length=250,
        description="Derived specialty"
    ),
}

# ============================================================================
# ORG Segment - Practitioner Organization Unit
# ============================================================================

ORG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - ORG",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Organization Unit Code",
        data_type="CE",
        length=250,
        description="Organization unit code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Organization Unit Type Code",
        data_type="CE",
        length=250,
        description="Unit type code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Primary Org Unit Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Primary indicator"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Practitioner Org Unit Identifier",
        data_type="CX",
        length=250,
        description="Practitioner identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Health Care Provider Type Code",
        data_type="CE",
        length=250,
        description="Provider type"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Health Care Provider Classification Code",
        data_type="CE",
        length=250,
        description="Classification code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Health Care Provider Area of Specialization Code",
        data_type="CE",
        length=250,
        description="Specialization code"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Effective Date Range",
        data_type="DR",
        length=52,
        description="Effective date range"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Employment Status Code",
        data_type="CE",
        length=250,
        table_binding="0066",
        description="Employment status"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Board Approval Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Board approval"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Primary Care Physician Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Primary care indicator"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Cost Center Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Cost center codes"
    ),
}

# ============================================================================
# ORO Segment - Common Order
# ============================================================================

ORO_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Order Item ID",
        data_type="CE",
        length=250,
        required=True,
        description="Order item identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Supplemental Service Information",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplemental services"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Result Status",
        data_type="ID",
        length=1,
        table_binding="0123",
        description="Result status"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        description="Quantity and timing"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Parent Order",
        data_type="EIP",
        length=200,
        description="Parent order"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Transport Mode",
        data_type="ID",
        length=20,
        table_binding="0124",
        description="Transport mode"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Reason for Study",
        data_type="CE",
        length=250,
        repeating=True,
        description="Reason codes"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Principal Result Interpreter",
        data_type="NDL",
        length=200,
        description="Principal interpreter"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Assistant Result Interpreter",
        data_type="NDL",
        length=200,
        repeating=True,
        description="Assistant interpreters"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Technician",
        data_type="NDL",
        length=200,
        repeating=True,
        description="Technicians"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Transcriptionist",
        data_type="NDL",
        length=200,
        repeating=True,
        description="Transcriptionists"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Scheduled Date/Time",
        data_type="TS",
        length=26,
        description="Scheduled date/time"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Number of Sample Containers",
        data_type="NM",
        length=4,
        description="Number of containers"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Transport Logistics of Collected Sample",
        data_type="CE",
        length=250,
        repeating=True,
        description="Transport logistics"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Collector's Comment",
        data_type="CE",
        length=250,
        repeating=True,
        description="Collector comments"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Transport Arrangement Responsibility",
        data_type="CE",
        length=250,
        description="Transport responsibility"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Transport Arranged",
        data_type="ID",
        length=30,
        table_binding="0224",
        description="Transport arranged indicator"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Escort Required",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Escort required"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Planned Patient Transport Comment",
        data_type="CE",
        length=250,
        repeating=True,
        description="Transport comments"
    ),
}

# ============================================================================
# OVR Segment - Override Segment
# ============================================================================

OVR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Business Rule Override Type",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0518",
        description="Override type"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Business Rule Override Code",
        data_type="CWE",
        length=250,
        required=True,
        description="Override code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Override Comments",
        data_type="ST",
        length=200,
        description="Override comments"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Override Entered By",
        data_type="XCN",
        length=250,
        description="Person who entered override"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Override Authorized By",
        data_type="XCN",
        length=250,
        description="Person who authorized override"
    ),
}

# ============================================================================
# PCR Segment - Possible Causal Relationship
# ============================================================================

PCR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Implicated Product",
        data_type="CE",
        length=250,
        required=True,
        description="Implicated product"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Generic Product",
        data_type="IS",
        length=1,
        table_binding="0249",
        description="Generic product indicator"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Product Class",
        data_type="CE",
        length=250,
        description="Product class"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Total Duration of Therapy",
        data_type="CQ",
        length=20,
        description="Total duration"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Product Manufacture Date",
        data_type="TS",
        length=26,
        description="Manufacture date"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Product Expiration Date",
        data_type="TS",
        length=26,
        description="Expiration date"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Product Implantation Date",
        data_type="TS",
        length=26,
        description="Implantation date"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Product Explantation Date",
        data_type="TS",
        length=26,
        description="Explantation date"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Single Use Device",
        data_type="IS",
        length=1,
        table_binding="0244",
        description="Single use indicator"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Indication for Product Use",
        data_type="CE",
        length=250,
        description="Indication"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Product Problem",
        data_type="CE",
        length=250,
        description="Product problem"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Product Serial/Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Serial/lot numbers"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Product Available for Inspection",
        data_type="IS",
        length=1,
        table_binding="0244",
        description="Available for inspection"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Product Evaluation Performed",
        data_type="CE",
        length=250,
        description="Evaluation performed"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Product Evaluation Status",
        data_type="CE",
        length=250,
        description="Evaluation status"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Product Evaluation Results",
        data_type="CE",
        length=250,
        description="Evaluation results"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Evaluated Product Source",
        data_type="ID",
        length=8,
        table_binding="0245",
        description="Evaluation source"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Date Product Returned to Manufacturer",
        data_type="TS",
        length=26,
        description="Return date"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Device Operator Qualifications",
        data_type="ID",
        length=1,
        table_binding="0242",
        description="Operator qualifications"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Relatedness Assessment",
        data_type="ID",
        length=1,
        table_binding="0250",
        description="Relatedness assessment"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Action Taken in Response to the Event",
        data_type="ID",
        length=2,
        repeating=True,
        table_binding="0251",
        description="Actions taken"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Event Causality Observations",
        data_type="ID",
        length=10,
        repeating=True,
        table_binding="0252",
        description="Causality observations"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Indirect Exposure Mechanism",
        data_type="ID",
        length=1,
        repeating=True,
        table_binding="0253",
        description="Exposure mechanism"
    ),
}

# ============================================================================
# PEO Segment - Product Experience Observation
# ============================================================================

PEO_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Event Identifiers Used",
        data_type="CE",
        length=250,
        repeating=True,
        description="Event identifiers"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Event Symptom/Diagnosis Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Symptom/diagnosis codes"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Onset Date/Time",
        data_type="TS",
        length=26,
        description="Onset date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Exacerbation Date/Time",
        data_type="TS",
        length=26,
        description="Exacerbation date/time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Event Improved Date/Time",
        data_type="TS",
        length=26,
        description="Improved date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Event Ended Date/Time",
        data_type="TS",
        length=26,
        description="Ended date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Event Location Occurred",
        data_type="PL",
        length=80,
        description="Location"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Event Qualification",
        data_type="ID",
        length=1,
        repeating=True,
        table_binding="0237",
        description="Event qualifications"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Event Serious",
        data_type="ID",
        length=1,
        table_binding="0238",
        description="Serious indicator"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Event Expected",
        data_type="ID",
        length=1,
        table_binding="0239",
        description="Expected indicator"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Event Outcome",
        data_type="ID",
        length=1,
        repeating=True,
        table_binding="0240",
        description="Outcome codes"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Patient Outcome",
        data_type="ID",
        length=1,
        table_binding="0241",
        description="Patient outcome"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Event Description from Others",
        data_type="FT",
        length=600,
        repeating=True,
        description="Description from others"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Event Description from Original Reporter",
        data_type="FT",
        length=600,
        repeating=True,
        description="Original description"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Event Description from Patient",
        data_type="FT",
        length=600,
        repeating=True,
        description="Patient description"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Event Description from Practitioner",
        data_type="FT",
        length=600,
        repeating=True,
        description="Practitioner description"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Event Description from Autopsy",
        data_type="FT",
        length=600,
        repeating=True,
        description="Autopsy description"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Cause of Death",
        data_type="CE",
        length=250,
        repeating=True,
        description="Cause of death codes"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Primary Observer Name",
        data_type="XPN",
        length=250,
        description="Primary observer"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Primary Observer Address",
        data_type="XAD",
        length=250,
        description="Observer address"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Primary Observer Telephone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Observer telephone"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Primary Observer's Qualification",
        data_type="ID",
        length=1,
        table_binding="0242",
        description="Observer qualification"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Confirmation Provided By",
        data_type="ID",
        length=1,
        table_binding="0242",
        description="Confirmation provider"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Primary Observer Aware of Event",
        data_type="ID",
        length=1,
        table_binding="0243",
        description="Aware indicator"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Report Transmitted To",
        data_type="ID",
        length=1,
        table_binding="0244",
        description="Transmission indicator"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Event Report Date",
        data_type="TS",
        length=26,
        description="Report date"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Event Report Timing/Type",
        data_type="ID",
        length=2,
        repeating=True,
        table_binding="0234",
        description="Report timing/type"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Event Report Source",
        data_type="ID",
        length=1,
        table_binding="0235",
        description="Report source"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Event Reported To",
        data_type="ID",
        length=1,
        table_binding="0236",
        description="Reported to"
    ),
}

# ============================================================================
# PES Segment - Product Experience Sender
# ============================================================================

PES_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sender Organization Name",
        data_type="XON",
        length=250,
        repeating=True,
        description="Organization names"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sender Individual Name",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Individual names"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Sender Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Addresses"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Sender Telephone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Telephone numbers"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Sender Event Identifier",
        data_type="EI",
        length=60,
        description="Event identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Sender Sequence Number",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Sender Event Description",
        data_type="FT",
        length=600,
        repeating=True,
        description="Event descriptions"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Sender Comment",
        data_type="FT",
        length=600,
        description="Comments"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Sender Aware Date/Time",
        data_type="TS",
        length=26,
        description="Aware date/time"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Event Report Date",
        data_type="TS",
        length=26,
        description="Report date"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Event Report Timing/Type",
        data_type="ID",
        length=2,
        repeating=True,
        table_binding="0234",
        description="Report timing/type"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Event Report Source",
        data_type="ID",
        length=1,
        table_binding="0235",
        description="Report source"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Event Reported To",
        data_type="ID",
        length=1,
        table_binding="0236",
        description="Reported to"
    ),
}

# ============================================================================
# IVT Segment - Inventory
# ============================================================================

IVT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - IVT",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Inventory Location Identifier",
        data_type="EI",
        length=60,
        description="Inventory location identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Inventory Location Name",
        data_type="ST",
        length=200,
        description="Location name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Source Location Identifier",
        data_type="EI",
        length=60,
        description="Source location identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Source Location Name",
        data_type="ST",
        length=200,
        description="Source location name"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Item Status",
        data_type="CWE",
        length=250,
        table_binding="0625",
        description="Item status code"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Bin Location Identifier",
        data_type="EI",
        length=60,
        repeating=True,
        description="Bin location identifiers"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Order Packaging",
        data_type="CWE",
        length=250,
        table_binding="0626",
        description="Order packaging code"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Issue Packaging",
        data_type="CWE",
        length=250,
        table_binding="0626",
        description="Issue packaging code"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Default Inventory Asset Account",
        data_type="EI",
        length=60,
        description="Default asset account"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Patient Chargeable Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Chargeable indicator"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Transaction Code",
        data_type="CWE",
        length=250,
        table_binding="0132",
        description="Transaction code"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Transaction Amount - Unit",
        data_type="CP",
        length=20,
        description="Unit transaction amount"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Item Importance Code",
        data_type="CWE",
        length=250,
        table_binding="0627",
        description="Item importance code"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Stocked Item Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Stocked item indicator"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Consignment Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Consignment indicator"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Reusable Item Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Reusable item indicator"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Reusable Cost",
        data_type="CP",
        length=20,
        description="Reusable cost"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Substitute Item Identifier",
        data_type="EI",
        length=60,
        repeating=True,
        description="Substitute item identifiers"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Latex-Free Substitute Item Identifier",
        data_type="EI",
        length=60,
        repeating=True,
        description="Latex-free substitute identifiers"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Recommended Reorder Theory",
        data_type="CWE",
        length=250,
        table_binding="0628",
        description="Reorder theory code"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Recommended Safety Stock Days",
        data_type="NM",
        length=5,
        description="Safety stock days"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Recommended Maximum Days Inventory",
        data_type="NM",
        length=5,
        description="Maximum days inventory"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Recommended Order Point",
        data_type="NM",
        length=10,
        description="Order point quantity"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Recommended Order Amount",
        data_type="NM",
        length=10,
        description="Order amount"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Operating Room Par Level Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="OR par level indicator"
    ),
}

# ============================================================================
# IVC Segment - Inventory Certificate
# ============================================================================

IVC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Provider Certification Number",
        data_type="CE",
        length=250,
        required=True,
        description="Certification number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Certification Begin Date",
        data_type="DT",
        length=8,
        description="Begin date"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Certification End Date",
        data_type="DT",
        length=8,
        description="End date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Days",
        data_type="NM",
        length=3,
        description="Number of days"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Non-Concur Code/Description",
        data_type="CE",
        length=250,
        description="Non-concur code"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Non-Concur Effective Date/Time",
        data_type="TS",
        length=26,
        description="Non-concur effective date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Physician Reviewer ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Reviewer identifiers"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Certification Contact",
        data_type="ST",
        length=48,
        description="Contact name"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Certification Contact Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Contact phone numbers"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Appeal Reason",
        data_type="CE",
        length=250,
        description="Appeal reason code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Certification Agency",
        data_type="CE",
        length=250,
        description="Certification agency"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Certification Agency Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Agency phone numbers"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Pre-Certification Required/Window",
        data_type="CM",
        length=40,
        description="Pre-certification requirements"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Case Manager",
        data_type="ST",
        length=48,
        description="Case manager name"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Second Opinion Date",
        data_type="DT",
        length=8,
        description="Second opinion date"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Second Opinion Status",
        data_type="IS",
        length=1,
        table_binding="0151",
        description="Second opinion status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Second Opinion Documentation Received",
        data_type="IS",
        length=1,
        table_binding="0152",
        description="Documentation received indicator"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Second Opinion Physician",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Second opinion physician identifiers"
    ),
}
# ============================================================================
# IPR Segment - Interaction Profile Detail
# ============================================================================

IPR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="IPR Identifier",
        data_type="EI",
        length=60,
        required=True,
        description="Interaction profile identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="IPR Value",
        data_type="ST",
        length=200,
        required=True,
        description="Interaction profile value"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="IPR Type",
        data_type="CWE",
        length=250,
        description="Type of interaction profile"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="IPR Description",
        data_type="ST",
        length=200,
        description="Description of interaction profile"
    ),
}

# ============================================================================
# IVP Segment - IV Pump
# ============================================================================

IVP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - IVP",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="IV Pump Status",
        data_type="CWE",
        length=250,
        table_binding="0625",
        description="IV pump status code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="IV Pump Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="IV Pump End Date/Time",
        data_type="TS",
        length=26,
        description="End date/time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="IV Pump Type",
        data_type="CWE",
        length=250,
        description="Type of IV pump"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="IV Pump Identifier",
        data_type="EI",
        length=60,
        description="IV pump identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="IV Pump Description",
        data_type="ST",
        length=200,
        description="IV pump description"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="IV Pump Flow Rate",
        data_type="NM",
        length=20,
        description="Flow rate"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="IV Pump Volume",
        data_type="NM",
        length=20,
        description="Volume"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="IV Pump Volume Units",
        data_type="CWE",
        length=250,
        description="Volume units"
    ),
}

# ============================================================================
# ITM Segment - Material Item
# ============================================================================

ITM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Item Identifier",
        data_type="EI",
        length=60,
        required=True,
        description="Material item identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Item Description",
        data_type="ST",
        length=200,
        description="Item description"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Item Status",
        data_type="CWE",
        length=250,
        table_binding="0625",
        description="Item status code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Item Type",
        data_type="CWE",
        length=250,
        table_binding="0629",
        description="Item type code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Item Category",
        data_type="CWE",
        length=250,
        table_binding="0630",
        description="Item category code"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Item Catalog Number",
        data_type="ST",
        length=60,
        description="Catalog number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Item Lot Number",
        data_type="ST",
        length=60,
        description="Lot number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Item Expiration Date",
        data_type="TS",
        length=26,
        description="Expiration date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Item Manufacturer Identifier",
        data_type="CWE",
        length=250,
        description="Manufacturer identifier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Item Manufacturer Name",
        data_type="ST",
        length=200,
        description="Manufacturer name"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Item Vendor Identifier",
        data_type="CWE",
        length=250,
        description="Vendor identifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Item Vendor Name",
        data_type="ST",
        length=200,
        description="Vendor name"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Item Unit Cost",
        data_type="CP",
        length=20,
        description="Unit cost"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Item Unit of Measure",
        data_type="CWE",
        length=250,
        description="Unit of measure"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Item Stocking Unit of Measure",
        data_type="CWE",
        length=250,
        description="Stocking unit of measure"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Item Reorder Point",
        data_type="NM",
        length=10,
        description="Reorder point quantity"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Item Reorder Quantity",
        data_type="NM",
        length=10,
        description="Reorder quantity"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Item Safety Stock",
        data_type="NM",
        length=10,
        description="Safety stock quantity"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Item Maximum Stock",
        data_type="NM",
        length=10,
        description="Maximum stock quantity"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Item Reorder Classification",
        data_type="CWE",
        length=250,
        table_binding="0628",
        description="Reorder classification code"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Item ABC Code",
        data_type="ID",
        length=1,
        description="ABC classification code"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Item Active/Inactive",
        data_type="ID",
        length=1,
        table_binding="0183",
        description="Active/inactive status"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Item Critical",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Critical item indicator"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Item Substitution Allowed",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Substitution allowed indicator"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Item Latex Free",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Latex free indicator"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Item User Defined Field 1",
        data_type="ST",
        length=200,
        description="User defined field 1"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Item User Defined Field 2",
        data_type="ST",
        length=200,
        description="User defined field 2"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Item User Defined Field 3",
        data_type="ST",
        length=200,
        description="User defined field 3"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Item User Defined Field 4",
        data_type="ST",
        length=200,
        description="User defined field 4"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Item User Defined Field 5",
        data_type="ST",
        length=200,
        description="User defined field 5"
    ),
}



# ============================================================================
# LDP Segment - Location Department
# ============================================================================

LDP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - LDP",
        data_type="PL",
        length=200,
        required=True,
        description="Primary key value"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Location Department",
        data_type="IS",
        length=10,
        required=True,
        table_binding="0264",
        description="Department code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Location Service",
        data_type="IS",
        length=3,
        table_binding="0069",
        description="Service code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Specialty Type",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0265",
        description="Specialty type codes"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Valid Patient Classes",
        data_type="IS",
        length=1,
        repeating=True,
        table_binding="0004",
        description="Valid patient class codes"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Active/Inactive Flag",
        data_type="ID",
        length=1,
        table_binding="0183",
        description="Active/inactive flag"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Activation Date - LDP",
        data_type="TS",
        length=26,
        description="Activation date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Inactivation Date - LDP",
        data_type="TS",
        length=26,
        description="Inactivation date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Inactivated Reason",
        data_type="ST",
        length=80,
        description="Inactivation reason"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Visiting Hours",
        data_type="VH",
        length=80,
        repeating=True,
        description="Visiting hours"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Contact Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Contact phone numbers"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Location Cost Center",
        data_type="IS",
        length=10,
        table_binding="0462",
        description="Cost center code"
    ),
}

# ============================================================================
# LCC Segment - Location Charge Code
# ============================================================================

LCC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - LCC",
        data_type="PL",
        length=200,
        required=True,
        description="Primary key value"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Location Department",
        data_type="IS",
        length=10,
        required=True,
        table_binding="0264",
        description="Department code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Accommodation Type",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0012",
        description="Accommodation type codes"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Charge Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0132",
        description="Charge code"
    ),
}

# ============================================================================
# LCH Segment - Location Characteristic
# ============================================================================

LCH_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - LCH",
        data_type="PL",
        length=200,
        required=True,
        description="Primary key value"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Segment Unique Key",
        data_type="EI",
        length=60,
        description="Unique key"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Location Characteristic ID",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0324",
        description="Characteristic identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Location Characteristic Value - LCH",
        data_type="CWE",
        length=250,
        required=True,
        description="Characteristic value"
    ),
}

# ============================================================================
# LRL Segment - Location Relationship
# ============================================================================

LRL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - LRL",
        data_type="PL",
        length=200,
        required=True,
        description="Primary key value"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Segment Unique Key",
        data_type="EI",
        length=60,
        description="Unique key"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Location Relationship ID",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0325",
        description="Relationship identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Organizational Location Relationship Value",
        data_type="XON",
        length=250,
        repeating=True,
        description="Related organization location values"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Patient Location Relationship Value",
        data_type="PL",
        length=200,
        description="Related patient location value"
    ),
}

# ============================================================================
# BLG Segment - Billing
# ============================================================================

BLG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="When to Charge",
        data_type="CCD",
        length=20,
        description="When to charge"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Charge Type",
        data_type="ID",
        length=50,
        table_binding="0122",
        description="Charge type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Account ID",
        data_type="CX",
        length=250,
        description="Account identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Charge Type Reason",
        data_type="CWE",
        length=250,
        description="Charge type reason"
    ),
}


# ============================================================================
# LOC Segment - Location Identification
# ============================================================================

LOC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - LOC",
        data_type="PL",
        length=200,
        required=True,
        description="Location identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Location Description",
        data_type="ST",
        length=48,
        description="Location description"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Location Type",
        data_type="CWE",
        length=250,
        table_binding="0260",
        description="Location type (e.g., D=Department, H=Home, O=Office, P=Permanent, T=Temporary)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Organization Name - LOC",
        data_type="XON",
        length=250,
        repeating=True,
        description="Organization name"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Location Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Location address"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Location Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Location phone number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="License Number",
        data_type="CE",
        length=250,
        repeating=True,
        description="License number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Location Equipment",
        data_type="IS",
        length=3,
        table_binding="0261",
        repeating=True,
        description="Location equipment"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Location Service Code",
        data_type="IS",
        length=3,
        table_binding="0442",
        description="Location service code"
    ),
}


# ============================================================================
# LCH Segment - Location Characteristic
# ============================================================================
# Note: LCH already exists, this is for reference


# ============================================================================
# PCE Segment - Patient Charge Cost Center Exceptions
# ============================================================================

PCE_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - PCE",
        data_type="SI",
        length=4,
        description="Sequence ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Cost Center Account Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Cost center account number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Transaction Code",
        data_type="CE",
        length=250,
        description="Transaction code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Transaction Amount - Unit",
        data_type="CP",
        length=25,
        description="Transaction amount per unit"
    ),
}

# ============================================================================
# MDM Segment - Medical Document Management
# ============================================================================

MDM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - MDM",
        data_type="SI",
        length=4,
        description="Sequence ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Document Control ID",
        data_type="EI",
        length=427,
        required=True,
        description="Document control identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time of document event"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Document Type",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0270",
        description="Type of document"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Document ID",
        data_type="EI",
        length=427,
        description="Document identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Document Status",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0271",
        description="Document status (e.g., AU=Authenticated, DI=Dictated, DO=Documented, IN=Incomplete, IP=In Progress, PA=Pre-authenticated)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Document Availability Status",
        data_type="ID",
        length=1,
        table_binding="0272",
        description="Document availability status"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Document Storage Status",
        data_type="ID",
        length=1,
        table_binding="0273",
        description="Document storage status"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Document Change Reason",
        data_type="ST",
        length=30,
        description="Reason for document change"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Authentication Person, Time Stamp",
        data_type="PPN",
        length=250,
        repeating=True,
        description="Person who authenticated and timestamp"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Distributed Copies (Code and Name of Recipients)",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Recipients of distributed copies"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Folder Assignment",
        data_type="EI",
        length=427,
        repeating=True,
        description="Folder assignment identifier"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Document Title",
        data_type="ST",
        length=250,
        description="Title of document"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Agreed Due Date/Time",
        data_type="TS",
        length=26,
        description="Agreed due date/time"
    ),
}


# ============================================================================
# SIU Segment - Scheduling Information Unsolicited
# ============================================================================

SIU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Appointment ID",
        data_type="EI",
        length=427,
        description="Placer appointment identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Appointment ID",
        data_type="EI",
        length=427,
        description="Filler appointment identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Occurrence Number",
        data_type="NM",
        length=5,
        description="Occurrence number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Placer Group Number",
        data_type="EI",
        length=427,
        description="Placer group number"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Schedule ID",
        data_type="CE",
        length=250,
        table_binding="0274",
        description="Schedule identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Event Reason",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0626",
        description="Reason for event"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Appointment Reason",
        data_type="CE",
        length=250,
        table_binding="0276",
        description="Reason for appointment"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Appointment Type",
        data_type="CE",
        length=250,
        table_binding="0277",
        description="Type of appointment"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Appointment Duration",
        data_type="NM",
        length=20,
        description="Duration of appointment in minutes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Appointment Duration Units",
        data_type="CE",
        length=250,
        description="Units for appointment duration"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Appointment Timing Quantity",
        data_type="TQ",
        length=200,
        repeating=True,
        description="Timing quantity for appointment"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Placer Contact Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Placer contact person"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Placer Contact Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Placer contact phone number"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Placer Contact Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Placer contact address"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Placer Contact Location",
        data_type="PL",
        length=80,
        description="Placer contact location"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Filler Contact Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Filler contact person"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Filler Contact Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Filler contact phone number"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Filler Contact Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Filler contact address"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Filler Contact Location",
        data_type="PL",
        length=80,
        description="Filler contact location"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Entered By Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who entered the appointment"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Entered By Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone number of person who entered"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Entered By Location",
        data_type="PL",
        length=80,
        description="Location of person who entered"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Parent Placer Appointment ID",
        data_type="EI",
        length=427,
        description="Parent placer appointment identifier"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Parent Filler Appointment ID",
        data_type="EI",
        length=427,
        description="Parent filler appointment identifier"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Filler Status Code",
        data_type="CE",
        length=250,
        table_binding="0278",
        description="Filler status code"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Placer Order Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Placer order number"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Filler Order Number",
        data_type="EI",
        length=427,
        repeating=True,
        description="Filler order number"
    ),
}


# ============================================================================
# BAR Segment - Billing Account Record
# ============================================================================

BAR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - BAR",
        data_type="SI",
        length=4,
        description="Sequence ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Billing Account Number",
        data_type="CX",
        length=250,
        required=True,
        description="Billing account number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Filler Account Number",
        data_type="CX",
        length=250,
        description="Filler account number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Account Type",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0018",
        description="Account type (e.g., P=Patient, A=Account)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Account Status",
        data_type="ID",
        length=1,
        table_binding="0117",
        description="Account status (e.g., A=Active, I=Inactive)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Account Start Date/Time",
        data_type="TS",
        length=26,
        description="Account start date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Account End Date/Time",
        data_type="TS",
        length=26,
        description="Account end date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Account Expiration Date/Time",
        data_type="TS",
        length=26,
        description="Account expiration date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Account Balance",
        data_type="CP",
        length=25,
        description="Account balance"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Account Balance Currency Code",
        data_type="IS",
        length=3,
        table_binding="0421",
        description="Currency code for account balance"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Billing Cycle Start Date",
        data_type="DT",
        length=8,
        description="Billing cycle start date"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Billing Cycle End Date",
        data_type="DT",
        length=8,
        description="Billing cycle end date"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Account Balance Amount",
        data_type="NM",
        length=12,
        description="Account balance amount"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Account Balance Check Date",
        data_type="DT",
        length=8,
        description="Date account balance was checked"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Account Balance Expiration Date",
        data_type="DT",
        length=8,
        description="Account balance expiration date"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Account Balance Type",
        data_type="IS",
        length=2,
        table_binding="0140",
        description="Account balance type"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Account Balance ID",
        data_type="CX",
        length=250,
        description="Account balance identifier"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Account Balance Credit Limit",
        data_type="CP",
        length=25,
        description="Account balance credit limit"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Account Balance Credit Limit Currency Code",
        data_type="IS",
        length=3,
        table_binding="0421",
        description="Currency code for credit limit"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Account Balance Credit Limit Date",
        data_type="DT",
        length=8,
        description="Credit limit date"
    ),
}


# ============================================================================
# PRT Segment - Participation Information
# ============================================================================

PRT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Participation Instance ID",
        data_type="EI",
        length=427,
        description="Participation instance identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Code",
        data_type="ID",
        length=2,
        table_binding="0287",
        description="Action code (e.g., AD, UP, DE)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Action Reason",
        data_type="CWE",
        length=250,
        description="Reason for action"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Participation",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0912",
        description="Type of participation"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Participation Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person participating"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Participation Person Provider Type",
        data_type="CWE",
        length=250,
        description="Provider type of participating person"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Participant Organization Unit Type",
        data_type="CWE",
        length=250,
        description="Organization unit type"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Participation Organization",
        data_type="XON",
        length=250,
        repeating=True,
        description="Organization participating"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Participant Location",
        data_type="PL",
        length=80,
        description="Location of participant"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Participation Device",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Device participating"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Participation Begin Date/Time",
        data_type="TS",
        length=26,
        description="Begin date/time of participation"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Participation End Date/Time",
        data_type="TS",
        length=26,
        description="End date/time of participation"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Participation Qualitative Duration",
        data_type="CWE",
        length=250,
        description="Qualitative duration of participation"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Participation Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Address of participant"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Participant Telecommunication Address",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Telecommunication address of participant"
    ),
}


# ============================================================================
# RDE Segment - Pharmacy/Treatment Encoded Order
# ============================================================================

RDE_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity and timing of medication"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Give Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0292",
        description="Code identifying medication to give"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Minimum amount to give"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Maximum amount to give"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Units",
        data_type="CE",
        length=250,
        description="Units for give amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Dosage Form",
        data_type="CE",
        length=250,
        description="Dosage form"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Provider's Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Administration instructions"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Deliver-To Location",
        data_type="LA1",
        length=200,
        description="Location to deliver medication"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Dispense Amount",
        data_type="NM",
        length=20,
        description="Amount to dispense"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Dispense Units",
        data_type="CE",
        length=250,
        description="Units for dispense amount"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Number Of Refills",
        data_type="NM",
        length=3,
        description="Number of refills"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Ordering Provider's DEA Number",
        data_type="XCN",
        length=250,
        repeating=True,
        description="DEA number of ordering provider"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Pharmacist/Treatment Supplier's Verifier ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Verifier identifier"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Prescription Number",
        data_type="ST",
        length=20,
        description="Prescription number"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Number Of Refills Remaining",
        data_type="NM",
        length=3,
        description="Number of refills remaining"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Number Of Refills/Doses Dispensed",
        data_type="NM",
        length=3,
        description="Number of refills/doses dispensed"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="D/T Of Most Recent Refill Or Dose Dispensed",
        data_type="TS",
        length=26,
        description="Date/time of most recent refill"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=10,
        description="Total daily dose"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review indicator"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Give Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Give per time unit"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Give Rate Amount",
        data_type="ST",
        length=6,
        description="Give rate amount"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Give Rate Units",
        data_type="CE",
        length=250,
        description="Give rate units"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Give Strength",
        data_type="NM",
        length=20,
        description="Give strength"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Give Strength Units",
        data_type="CE",
        length=250,
        description="Give strength units"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Give Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication for giving medication"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Dispense Package Size Unit",
        data_type="CE",
        length=250,
        description="Dispense package size unit"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Supplementary Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Original Order Date/Time",
        data_type="TS",
        length=26,
        description="Original order date/time"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Give Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Give drug strength volume"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Give Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Give drug strength volume units"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Controlled Substance Schedule",
        data_type="CE",
        length=250,
        table_binding="0477",
        description="Controlled substance schedule"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Formulary Status",
        data_type="ID",
        length=1,
        table_binding="0478",
        description="Formulary status"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Pharmaceutical Substance Alternative",
        data_type="CE",
        length=250,
        repeating=True,
        description="Pharmaceutical substance alternative"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Pharmacy Of Most Recent Fill",
        data_type="CE",
        length=250,
        description="Pharmacy of most recent fill"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Initial Dispense Amount",
        data_type="NM",
        length=20,
        description="Initial dispense amount"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Dispensing Pharmacy",
        data_type="CE",
        length=250,
        description="Dispensing pharmacy"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Dispensing Pharmacy Address",
        data_type="XAD",
        length=250,
        description="Dispensing pharmacy address"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Deliver-To Patient Location",
        data_type="PL",
        length=80,
        description="Deliver to patient location"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Deliver-To Address",
        data_type="XAD",
        length=250,
        description="Deliver to address"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RDS Segment - Pharmacy/Treatment Dispense
# ============================================================================

RDS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Dispense sub-identifier counter"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense/Give Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0292",
        description="Code for dispense/give"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date/Time Dispensed",
        data_type="TS",
        length=26,
        description="Date/time dispensed"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Actual Dispense Amount",
        data_type="NM",
        length=20,
        description="Actual dispense amount"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Actual Dispense Units",
        data_type="CE",
        length=250,
        description="Actual dispense units"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Actual Dosage Form",
        data_type="CE",
        length=250,
        description="Actual dosage form"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Prescription Number",
        data_type="ST",
        length=20,
        description="Prescription number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Number Of Refills Remaining",
        data_type="NM",
        length=3,
        description="Number of refills remaining"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Dispense Notes",
        data_type="ST",
        length=200,
        repeating=True,
        description="Dispense notes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Dispensing Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Dispensing provider"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=10,
        description="Total daily dose"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Dispense-To Location",
        data_type="LA1",
        length=200,
        description="Dispense to location"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review indicator"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Actual Strength",
        data_type="NM",
        length=20,
        description="Actual strength"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Actual Strength Unit",
        data_type="CE",
        length=250,
        description="Actual strength unit"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Substance Manufacturer Name",
        data_type="CE",
        length=250,
        repeating=True,
        description="Substance manufacturer name"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Dispense Package Size Unit",
        data_type="CE",
        length=250,
        description="Dispense package size unit"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Supplementary Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Initiating Location",
        data_type="CE",
        length=250,
        description="Initiating location"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Packaging/Assembly Location",
        data_type="CE",
        length=250,
        description="Packaging/assembly location"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Actual Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Actual drug strength volume"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Actual Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Actual drug strength volume units"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Dispense To Pharmacy",
        data_type="CE",
        length=250,
        description="Dispense to pharmacy"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Dispense To Pharmacy Address",
        data_type="XAD",
        length=250,
        description="Dispense to pharmacy address"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RGV Segment - Pharmacy/Treatment Give
# ============================================================================

RGV_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Give Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Give sub-identifier counter"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Dispense sub-identifier counter"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity and timing"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0292",
        description="Code identifying medication to give"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Minimum amount to give"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Maximum amount to give"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CE",
        length=250,
        description="Units for give amount"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CE",
        length=250,
        description="Dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-To Location",
        data_type="LA1",
        length=200,
        description="Location to deliver"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CE",
        length=250,
        description="Identification modifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Administered Code",
        data_type="CE",
        length=250,
        table_binding="0292",
        description="Code for administered medication"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Administered Amount",
        data_type="NM",
        length=20,
        description="Administered amount"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Administered Units",
        data_type="CE",
        length=250,
        description="Administered units"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Administered Dosage Form",
        data_type="CE",
        length=250,
        description="Administered dosage form"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Administration Notes",
        data_type="CE",
        length=250,
        repeating=True,
        description="Administration notes"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Administering provider"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Administered-At Location",
        data_type="LA1",
        length=200,
        description="Location where administered"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Administered per time unit"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Administered Strength",
        data_type="NM",
        length=20,
        description="Administered strength"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Administered Strength Units",
        data_type="CE",
        length=250,
        description="Administered strength units"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Substance Manufacturer Name",
        data_type="CE",
        length=250,
        repeating=True,
        description="Substance manufacturer name"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Substance Refusal Reason",
        data_type="CE",
        length=250,
        repeating=True,
        description="Substance refusal reason"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Completion Status",
        data_type="ID",
        length=2,
        table_binding="0322",
        description="Completion status"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Action Code - RGV",
        data_type="ID",
        length=2,
        table_binding="0206",
        description="Action code"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="System Entry Date/Time",
        data_type="TS",
        length=26,
        description="System entry date/time"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Administered Drug Strength Volume",
        data_type="NM",
        length=20,
        description="Administered drug strength volume"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Administered Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Administered drug strength volume units"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Administered Barcode Identifier",
        data_type="CWE",
        length=250,
        description="Administered barcode identifier"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RAS Segment - Pharmacy/Treatment Administration (Response)
# ============================================================================

RAS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Give Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Give sub-ID counter (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administration Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Administration sub-ID counter (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date/Time Start of Administration",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time start of administration (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Date/Time End of Administration",
        data_type="TS",
        length=26,
        description="Date/time end of administration"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administered Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0292",
        description="Administered code (required)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administered Amount",
        data_type="NM",
        length=20,
        required=True,
        description="Administered amount (required)"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Administered units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administered Dosage Form",
        data_type="CWE",
        length=250,
        description="Administered dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administration Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Administration notes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Administering provider"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administered-at Location",
        data_type="LA2",
        length=200,
        description="Administered-at location"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Administered per time unit"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Administered Strength",
        data_type="NM",
        length=20,
        description="Administered strength"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Administered strength units"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Substance Manufacturer Name",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0227",
        description="Substance manufacturer name"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Substance/Treatment Refusal Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Substance/treatment refusal reason"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Indication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Completion Status",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0322",
        description="Completion status (required)"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Action Code - RXA",
        data_type="ID",
        length=2,
        table_binding="0206",
        description="Action code"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="System Entry Date/Time",
        data_type="TS",
        length=26,
        description="System entry date/time"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Administered Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Administered drug strength volume"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Administered Drug Strength Volume Units",
        data_type="CWE",
        length=250,
        description="Administered drug strength volume units"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Administered Barcode Identifier",
        data_type="CWE",
        length=250,
        description="Administered barcode identifier"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RAR Segment - Pharmacy/Treatment Administration Acknowledgement
# ============================================================================

RAR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Application ID",
        data_type="EI",
        length=427,
        description="Placer application identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Application ID",
        data_type="EI",
        length=427,
        description="Filler application identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        description="Quantity/timing"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CWE",
        length=250,
        table_binding="0292",
        description="Give code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CWE",
        length=250,
        description="Give units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CWE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-to Location",
        data_type="LA1",
        length=200,
        description="Deliver-to location"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CWE",
        length=250,
        description="Identification modifier"
    ),
}


# ============================================================================
# RER Segment - Pharmacy/Treatment Encoded Order Information Response
# ============================================================================

RER_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Event Type",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0003",
        description="Event type (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="DateTime Event Occurred",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time event occurred (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="DateTime Event Placed",
        data_type="TS",
        length=26,
        description="Date/time event placed"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Facility",
        data_type="HD",
        length=227,
        description="Event facility"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Event Location",
        data_type="PL",
        length=80,
        description="Event location"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Event Operator",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Event operator"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Event Type Code",
        data_type="ID",
        length=3,
        table_binding="0003",
        description="Event type code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Event Occurred",
        data_type="TS",
        length=26,
        description="Event occurred"
    ),
}


# ============================================================================
# RGR Segment - Pharmacy/Treatment Give Response
# ============================================================================

RGR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Give Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Give sub-ID counter"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Dispense sub-ID counter"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity/timing (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0292",
        description="Give code (required)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CWE",
        length=250,
        description="Give units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CWE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-to Location",
        data_type="LA1",
        length=200,
        description="Deliver-to location"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CWE",
        length=250,
        description="Identification modifier"
    ),
}


# ============================================================================
# APR Segment - Appointment Preferences
# ============================================================================

APR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Time Selection Criteria",
        data_type="SCV",
        length=80,
        repeating=True,
        description="Time selection criteria for appointment preferences"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Resource Selection Criteria",
        data_type="SCV",
        length=80,
        repeating=True,
        description="Resource selection criteria for appointment preferences"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Location Selection Criteria",
        data_type="SCV",
        length=80,
        repeating=True,
        description="Location selection criteria for appointment preferences"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Slot Spacing Criteria",
        data_type="NM",
        length=5,
        description="Slot spacing criteria in minutes"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Filler Override Criteria",
        data_type="SCV",
        length=80,
        repeating=True,
        description="Filler override criteria for appointment preferences"
    ),
}


# ============================================================================
# ARQ Segment - Appointment Request
# ============================================================================

ARQ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Appointment ID",
        data_type="EI",
        length=75,
        required=True,
        description="Placer appointment identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Appointment ID",
        data_type="EI",
        length=75,
        description="Filler appointment identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Occurrence Number",
        data_type="NM",
        length=5,
        description="Occurrence number for recurring appointments"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Placer Group Number",
        data_type="EI",
        length=75,
        description="Placer group number"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Schedule ID",
        data_type="CE",
        length=250,
        table_binding="0274",
        description="Schedule identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Request Event Reason",
        data_type="CE",
        length=250,
        table_binding="0276",
        description="Reason for appointment request"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Appointment Reason",
        data_type="CE",
        length=250,
        table_binding="0277",
        description="Reason for appointment"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Appointment Type",
        data_type="CE",
        length=250,
        table_binding="0275",
        description="Type of appointment"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Appointment Duration",
        data_type="NM",
        length=20,
        description="Duration of appointment in minutes"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Appointment Duration Units",
        data_type="CE",
        length=250,
        description="Units for appointment duration"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Requested Start Date/Time Range",
        data_type="DR",
        length=53,
        repeating=True,
        description="Requested start date/time range"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Priority - ARQ",
        data_type="ST",
        length=5,
        description="Priority of appointment request"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Repeating Interval",
        data_type="RI",
        length=100,
        description="Repeating interval for recurring appointments"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Repeating Interval Duration",
        data_type="ST",
        length=5,
        description="Duration of repeating interval"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Placer Contact Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Contact person for placer"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Placer Contact Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Contact phone for placer"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Placer Contact Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Contact address for placer"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Placer Contact Location",
        data_type="PL",
        length=80,
        description="Contact location for placer"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Entered By Person",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Person who entered the appointment request"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Entered By Phone Number",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone number of person who entered request"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Entered By Location",
        data_type="PL",
        length=80,
        description="Location of person who entered request"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Parent Placer Appointment ID",
        data_type="EI",
        length=75,
        description="Parent placer appointment identifier"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Parent Filler Appointment ID",
        data_type="EI",
        length=75,
        description="Parent filler appointment identifier"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Placer Order Number",
        data_type="EI",
        length=75,
        repeating=True,
        description="Placer order number"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Filler Order Number",
        data_type="EI",
        length=75,
        repeating=True,
        description="Filler order number"
    ),
}


# ============================================================================
# RRA Segment - Pharmacy/Treatment Administration Acknowledgment
# ============================================================================

RRA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Application ID",
        data_type="EI",
        length=427,
        description="Placer application identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Application ID",
        data_type="EI",
        length=427,
        description="Filler application identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        description="Quantity and timing"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CWE",
        length=250,
        table_binding="0292",
        description="Give code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CWE",
        length=250,
        description="Give units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CWE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-to Location",
        data_type="LA1",
        length=200,
        description="Deliver-to location"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CWE",
        length=250,
        description="Identification modifier"
    ),
}


# ============================================================================
# RRD Segment - Pharmacy/Treatment Dispense Acknowledgment
# ============================================================================

RRD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Dispense sub-ID counter (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Transaction Type",
        data_type="ID",
        length=1,
        table_binding="0162",
        description="Transaction type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Transaction Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Transaction date/time (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Dispense Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Dispense date/time (required)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Actual Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Actual drug strength volume"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Actual Drug Strength Volume Units",
        data_type="CWE",
        length=250,
        description="Actual drug strength volume units"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Actual Dispense Amount",
        data_type="NM",
        length=20,
        description="Actual dispense amount"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Actual Dispense Units",
        data_type="CWE",
        length=250,
        description="Actual dispense units"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Actual Dosage Form",
        data_type="CWE",
        length=250,
        description="Actual dosage form"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Prescription Number",
        data_type="ST",
        length=20,
        required=True,
        description="Prescription number (required)"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Number of Refills Remaining",
        data_type="NM",
        length=3,
        description="Number of refills remaining"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Dispense Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Dispense notes"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Dispensing Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Dispensing provider"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=10,
        description="Total daily dose"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Dispense-to Location",
        data_type="LA2",
        length=200,
        description="Dispense-to location"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Actual Strength",
        data_type="NM",
        length=20,
        description="Actual strength"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Actual Strength Units",
        data_type="CWE",
        length=250,
        description="Actual strength units"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Substance Manufacturer Name",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0227",
        description="Substance manufacturer name"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Indication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Dispense Package Size Unit",
        data_type="CWE",
        length=250,
        description="Dispense package size unit"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Supplementary Code",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Initiating Location",
        data_type="CWE",
        length=250,
        description="Initiating location"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Packaging/Assembly Location",
        data_type="CWE",
        length=250,
        description="Packaging/assembly location"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Actual Drug Strength",
        data_type="NM",
        length=20,
        description="Actual drug strength"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Actual Drug Strength Units",
        data_type="CWE",
        length=250,
        description="Actual drug strength units"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Dispense-to Patient",
        data_type="XCN",
        length=250,
        description="Dispense-to patient"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Dispense-to Patient Address",
        data_type="XAD",
        length=250,
        description="Dispense-to patient address"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RRG Segment - Pharmacy/Treatment Give Acknowledgment
# ============================================================================

RRG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Give Sub-ID Counter",
        data_type="NM",
        length=4,
        required=True,
        description="Give sub-ID counter (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Dispense sub-ID counter"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity and timing (required)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0292",
        description="Give code (required)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        required=True,
        description="Give amount - minimum (required)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CWE",
        length=250,
        required=True,
        description="Give units (required)"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CWE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-to Location",
        data_type="LA1",
        length=200,
        description="Deliver-to location"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CWE",
        length=250,
        description="Identification modifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Administered Code",
        data_type="CWE",
        length=250,
        table_binding="0292",
        description="Administered code"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Administered Amount",
        data_type="NM",
        length=20,
        description="Administered amount"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Administered units"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Administered Dosage Form",
        data_type="CWE",
        length=250,
        description="Administered dosage form"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Administration Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Administration notes"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Administering provider"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Administered-at Location",
        data_type="LA2",
        length=200,
        description="Administered-at location"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Administered per time unit"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Administered Strength",
        data_type="NM",
        length=20,
        description="Administered strength"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Administered strength units"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Substance lot number"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Substance Manufacturer Name",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0227",
        description="Substance manufacturer name"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Substance/Treatment Refusal Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Substance/treatment refusal reason"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Indication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Completion Status",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0322",
        description="Completion status (required)"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Action Code - RXG",
        data_type="ID",
        length=2,
        table_binding="0206",
        description="Action code"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="System Entry Date/Time",
        data_type="TS",
        length=26,
        description="System entry date/time"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Administered Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Administered drug strength volume"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Administered Drug Strength Volume Units",
        data_type="CWE",
        length=250,
        description="Administered drug strength volume units"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Administered Barcode Identifier",
        data_type="CWE",
        length=250,
        description="Administered barcode identifier"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RRE Segment - Pharmacy/Treatment Encoded Order Acknowledgment
# ============================================================================

RRE_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        required=True,
        description="Quantity and timing (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Give Code",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0292",
        description="Code identifying medication to give (required)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Minimum amount to give"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Maximum amount to give"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Units",
        data_type="CE",
        length=250,
        description="Units for give amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Dosage Form",
        data_type="CE",
        length=250,
        description="Dosage form"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Provider's Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Administration instructions"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Deliver-To Location",
        data_type="LA1",
        length=200,
        description="Location to deliver medication"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Dispense Amount",
        data_type="NM",
        length=20,
        description="Amount to dispense"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Dispense Units",
        data_type="CE",
        length=250,
        description="Units for dispense amount"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Number Of Refills",
        data_type="NM",
        length=3,
        description="Number of refills"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Ordering Provider's DEA Number",
        data_type="XCN",
        length=250,
        repeating=True,
        description="DEA number of ordering provider"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Pharmacist/Treatment Supplier's Verifier ID",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Verifier identifier"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Prescription Number",
        data_type="ST",
        length=20,
        required=True,
        description="Prescription number (required)"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Number of Refills Remaining",
        data_type="NM",
        length=3,
        description="Number of refills remaining"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Number of Refills/Doses Dispensed",
        data_type="NM",
        length=3,
        description="Number of refills/doses dispensed"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="D/T of Most Recent Refill or Dose Dispensed",
        data_type="TS",
        length=26,
        description="Date/time of most recent refill or dose dispensed"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=10,
        description="Total daily dose"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Pharmacy/Treatment Supplier's Special Dispensing Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Special dispensing instructions"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Give Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Give per time unit"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Give Rate Amount",
        data_type="ST",
        length=6,
        description="Give rate amount"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Give Rate Units",
        data_type="CE",
        length=250,
        description="Give rate units"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Give Strength",
        data_type="NM",
        length=20,
        description="Give strength"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Give Strength Units",
        data_type="CE",
        length=250,
        description="Give strength units"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Give Indication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Give indication"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Dispense Package Size",
        data_type="NM",
        length=20,
        description="Dispense package size"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Dispense Package Size Unit",
        data_type="CWE",
        length=250,
        description="Dispense package size unit"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Dispense Package Method",
        data_type="ID",
        length=2,
        table_binding="0321",
        description="Dispense package method"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Supplementary Code",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Supplementary code"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Original Order Date/Time",
        data_type="TS",
        length=26,
        description="Original order date/time"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Give Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Give drug strength volume"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Give Drug Strength Volume Units",
        data_type="CWE",
        length=250,
        description="Give drug strength volume units"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Controlled Substance Schedule",
        data_type="CWE",
        length=250,
        table_binding="0477",
        description="Controlled substance schedule"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Formulary Status",
        data_type="ID",
        length=1,
        table_binding="0478",
        description="Formulary status"
    ),
    37: FieldDefinition(
        field_index=37,
        field_name="Pharmaceutical Substance Alternative",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Pharmaceutical substance alternative"
    ),
    38: FieldDefinition(
        field_index=38,
        field_name="Pharmacy of Most Recent Fill",
        data_type="CWE",
        length=250,
        description="Pharmacy of most recent fill"
    ),
    39: FieldDefinition(
        field_index=39,
        field_name="Initial Dispense Amount",
        data_type="NM",
        length=20,
        description="Initial dispense amount"
    ),
    40: FieldDefinition(
        field_index=40,
        field_name="Dispensing Pharmacy",
        data_type="CWE",
        length=250,
        description="Dispensing pharmacy"
    ),
    41: FieldDefinition(
        field_index=41,
        field_name="Dispensing Pharmacy Address",
        data_type="XAD",
        length=250,
        description="Dispensing pharmacy address"
    ),
    42: FieldDefinition(
        field_index=42,
        field_name="Deliver-to Patient Location",
        data_type="PL",
        length=80,
        description="Deliver-to patient location"
    ),
    43: FieldDefinition(
        field_index=43,
        field_name="Deliver-to Address",
        data_type="XAD",
        length=250,
        description="Deliver-to address"
    ),
    44: FieldDefinition(
        field_index=44,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# RRF Segment - Pharmacy/Treatment Order Response
# ============================================================================

RRF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Application ID",
        data_type="EI",
        length=427,
        description="Placer application identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Application ID",
        data_type="EI",
        length=427,
        description="Filler application identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        description="Quantity and timing"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CWE",
        length=250,
        table_binding="0292",
        description="Give code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CWE",
        length=250,
        description="Give units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CWE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-to Location",
        data_type="LA1",
        length=200,
        description="Deliver-to location"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CWE",
        length=250,
        description="Identification modifier"
    ),
}


# ============================================================================
# RCL Segment - Pharmacy Clinical
# ============================================================================

RCL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Substance Identifier",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0451",
        description="Substance identifier (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Substance Status",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0383",
        description="Substance status"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Substance Type",
        data_type="CWE",
        length=250,
        table_binding="0384",
        description="Substance type"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Custom Classification",
        data_type="CWE",
        length=250,
        description="Custom classification"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Clinic Identifier",
        data_type="CWE",
        length=250,
        description="Clinic identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Substance Name",
        data_type="ST",
        length=250,
        description="Substance name"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Substance Name Modifier",
        data_type="ST",
        length=250,
        description="Substance name modifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Substance Class",
        data_type="CWE",
        length=250,
        table_binding="0452",
        description="Substance class"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Substance Form",
        data_type="CWE",
        length=250,
        table_binding="0453",
        description="Substance form"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Substance Route",
        data_type="CWE",
        length=250,
        table_binding="0162",
        description="Substance route"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administration Site",
        data_type="CWE",
        length=250,
        table_binding="0163",
        description="Administration site"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Administration Device",
        data_type="CWE",
        length=250,
        table_binding="0164",
        description="Administration device"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Administration Method",
        data_type="CWE",
        length=250,
        table_binding="0165",
        description="Administration method"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Routing Instruction",
        data_type="CWE",
        length=250,
        description="Routing instruction"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Administration Site Modifier",
        data_type="CWE",
        length=250,
        table_binding="0495",
        description="Administration site modifier"
    ),
}


# ============================================================================
# ROR Segment - Pharmacy Prescription Order
# ============================================================================

ROR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Placer Application ID",
        data_type="EI",
        length=427,
        description="Placer application identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Filler Application ID",
        data_type="EI",
        length=427,
        description="Filler application identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Quantity/Timing",
        data_type="TQ",
        length=200,
        description="Quantity and timing"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Code",
        data_type="CWE",
        length=250,
        table_binding="0292",
        description="Give code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Give Units",
        data_type="CWE",
        length=250,
        description="Give units"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Give Dosage Form",
        data_type="CWE",
        length=250,
        description="Give dosage form"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Provider's Administration Instructions",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Provider's administration instructions"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Deliver-to Location",
        data_type="LA1",
        length=200,
        description="Deliver-to location"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Identification Modifier",
        data_type="CWE",
        length=250,
        description="Identification modifier"
    ),
}


# ============================================================================
# GP1 Segment - Grouping/Reimbursement - Visit
# ============================================================================

GP1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Type of Bill Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0450",
        description="Code identifying the type of bill"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Revenue Code",
        data_type="CWE",
        length=250,
        table_binding="0451",
        description="Revenue code for this visit"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Overall Claim Disposition Code",
        data_type="CWE",
        length=250,
        table_binding="0452",
        description="Code indicating overall claim disposition"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="OCE Edits per Visit Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0453",
        description="OCE (Outpatient Code Editor) edits for this visit"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Outlier Cost",
        data_type="CP",
        length=12,
        description="Outlier cost amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Outlier Days",
        data_type="NM",
        length=3,
        description="Number of outlier days"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="GP1 Grouping/Reimbursement - Visit",
        data_type="CWE",
        length=250,
        table_binding="0454",
        description="Grouping/reimbursement code for visit"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="GP1 Value Amount",
        data_type="CP",
        length=12,
        description="Value amount for GP1 grouping"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="GP1 Non-Covered Amount",
        data_type="CP",
        length=12,
        description="Non-covered amount for GP1 grouping"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="GP1 Outlier Amount",
        data_type="CP",
        length=12,
        description="Outlier amount for GP1 grouping"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="GP1 Outlier Days",
        data_type="NM",
        length=3,
        description="Outlier days for GP1 grouping"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="GP1 Grouping/Reimbursement - Visit",
        data_type="CWE",
        length=250,
        table_binding="0455",
        description="Additional grouping/reimbursement code"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="GP1 Value Amount",
        data_type="CP",
        length=12,
        description="Additional value amount"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="GP1 Non-Covered Amount",
        data_type="CP",
        length=12,
        description="Additional non-covered amount"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="GP1 Outlier Amount",
        data_type="CP",
        length=12,
        description="Additional outlier amount"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="GP1 Outlier Days",
        data_type="NM",
        length=3,
        description="Additional outlier days"
    ),
}


# ============================================================================
# GP2 Segment - Grouping/Reimbursement - Procedure Line Item
# ============================================================================

GP2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Revenue Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0451",
        description="Revenue code for this procedure line item"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Number of Service Units",
        data_type="NM",
        length=7,
        description="Number of service units"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Charge",
        data_type="CP",
        length=12,
        description="Charge amount for this line item"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Reimbursement Action Code",
        data_type="CWE",
        length=250,
        table_binding="0456",
        description="Code indicating reimbursement action"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Denial or Rejection Code",
        data_type="CWE",
        length=250,
        table_binding="0457",
        description="Code indicating denial or rejection reason"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="OCE Edit Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0458",
        description="OCE (Outpatient Code Editor) edit codes"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Ambulatory Payment Classification Code",
        data_type="CWE",
        length=250,
        table_binding="0459",
        description="APC (Ambulatory Payment Classification) code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Modifier Edit Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0460",
        description="Modifier edit codes"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Payment Adjustment Code",
        data_type="CWE",
        length=250,
        table_binding="0461",
        description="Payment adjustment code"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Packaging Status Code",
        data_type="CWE",
        length=250,
        table_binding="0462",
        description="Packaging status code"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Expected CMS Payment Amount",
        data_type="CP",
        length=12,
        description="Expected CMS (Centers for Medicare & Medicaid Services) payment amount"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Reimbursement Type Code",
        data_type="CWE",
        length=250,
        table_binding="0463",
        description="Reimbursement type code"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Co-Pay Amount",
        data_type="CP",
        length=12,
        description="Co-pay amount"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Pay Rate per Service Unit",
        data_type="NM",
        length=7,
        description="Pay rate per service unit"
    ),
}


# ============================================================================
# LAN Segment - Language Detail
# ============================================================================

LAN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - LAN",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this language segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Language Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0296",
        description="Code identifying the language"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Language Ability Code",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0403",
        description="Code indicating language ability (Read, Write, Speak, Understand)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Language Proficiency Code",
        data_type="CWE",
        length=250,
        table_binding="0404",
        description="Code indicating language proficiency level"
    ),
}


# ============================================================================
# QBP Segment - Query by Parameter
# ============================================================================

QBP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Message Query Name",
        data_type="CWE",
        length=250,
        required=True,
        description="Name of the query message"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Unique identifier for this query"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Message Response Type",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0091",
        description="Type of response requested"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Hit Count Total",
        data_type="NM",
        length=10,
        description="Total number of hits expected"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="QBP Input Parameter List",
        data_type="QIP",
        length=256,
        repeating=True,
        description="Input parameters for the query"
    ),
}


# ============================================================================
# QRY Segment - Query
# ============================================================================

QRY_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Unique identifier for this query"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Format Code",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0106",
        description="Format code for the query"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Query Priority",
        data_type="ID",
        length=1,
        table_binding="0091",
        description="Priority of the query"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Query ID",
        data_type="ST",
        length=10,
        description="Query identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Deferred Response Type",
        data_type="ID",
        length=1,
        table_binding="0107",
        description="Type of deferred response"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Deferred Response Date/Time",
        data_type="TS",
        length=26,
        description="Date/time for deferred response"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Quantity Limited Request",
        data_type="CQ",
        length=10,
        description="Quantity limit for the request"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Who Subject Filter",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Subject filter for the query"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="What Subject Filter",
        data_type="CE",
        length=250,
        repeating=True,
        description="What subject filter for the query"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="What Department Data Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Department data code filter"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="What Data Code Value Qual.",
        data_type="VR",
        length=20,
        repeating=True,
        description="Data code value qualifier"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Query Results Level",
        data_type="ID",
        length=1,
        table_binding="0108",
        description="Level of detail for query results"
    ),
}


# ============================================================================
# CON Segment - Consent
# ============================================================================

CON_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - CON",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this consent segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Consent Type",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0495",
        description="Type of consent (e.g., Release of Information, Research)"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Subject-Specific Consent",
        data_type="CWE",
        length=250,
        table_binding="0496",
        description="Subject-specific consent code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Consent Mode",
        data_type="CNE",
        length=250,
        table_binding="0497",
        description="Mode of consent (e.g., Verbal, Written, Electronic)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Consent Status",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0498",
        description="Status of consent (e.g., Active, Inactive, Pending)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Consent Discussion Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time consent was discussed with patient"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Consent Decision Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time consent decision was made"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Consent Effective Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time consent becomes effective"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Consent End Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time consent expires or ends"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Subject Competence Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Indicator of subject's competence (Y/N)"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Translator Assistance Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Indicator if translator assistance was used (Y/N)"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Language Translated To",
        data_type="CWE",
        length=250,
        table_binding="0296",
        description="Language consent was translated to"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Informational Material Supplied Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Indicator if informational material was supplied (Y/N)"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Consent Bypass Reason",
        data_type="CWE",
        length=250,
        table_binding="0499",
        description="Reason consent was bypassed (if applicable)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Consent Disclosure Level",
        data_type="ID",
        length=1,
        table_binding="0500",
        description="Level of disclosure (F=Full, P=Partial, N=None)"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Non-Disclosure Reason",
        data_type="CWE",
        length=250,
        description="Reason for non-disclosure (if applicable)"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Non-Disclosure Reason Text",
        data_type="FT",
        length=65536,
        description="Free text reason for non-disclosure"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Non-Subject Consenter Reason",
        data_type="CWE",
        length=250,
        table_binding="0501",
        description="Reason non-subject consenter was used"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Consenter ID",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Identifier of person who gave consent"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Relationship to Subject",
        data_type="CWE",
        length=250,
        table_binding="0063",
        description="Relationship of consenter to subject"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Consenter Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Name of person who gave consent"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Consenter Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Address of consenter"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Consenter Phone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Phone number of consenter"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Consenter's Organization",
        data_type="XON",
        length=250,
        repeating=True,
        description="Organization of consenter"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Subject's Rights",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Indicator if subject's rights were explained (Y/N)"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Consent to Disclose Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Flag indicating consent to disclose (Y/N)"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Subject Non-Disclosure Flag",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Flag indicating subject requested non-disclosure (Y/N)"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Consent Non-Disclosure Reason",
        data_type="CWE",
        length=250,
        description="Reason for consent non-disclosure"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Non-Subject Consenter",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Indicator if non-subject consenter was used (Y/N)"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Consent Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time consent was obtained"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Consent Revocation Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time consent was revoked"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Consent Revocation Reason Code",
        data_type="CWE",
        length=250,
        description="Reason code for consent revocation"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Consent Revocation Reason Text",
        data_type="FT",
        length=65536,
        description="Free text reason for consent revocation"
    ),
}


# ============================================================================
# VXA Segment - Vaccination Administered
# ============================================================================

VXA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - VXA",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this vaccination administered segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administration Date/Time",
        data_type="DTM",
        length=24,
        required=True,
        description="Date/time vaccination was administered"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Administered Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0292",
        description="Vaccine code administered (CVX code)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Administered Amount",
        data_type="NM",
        length=5,
        description="Amount of vaccine administered"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Units for administered amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administered Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Notes about administration"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Provider who administered the vaccination"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administered-at Location",
        data_type="LA2",
        length=250,
        description="Location where vaccination was administered"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Time unit for administration rate"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administered Strength",
        data_type="NM",
        length=5,
        description="Strength of vaccine administered"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Units for administered strength"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Substance Refusal Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0491",
        description="Reason for refusal if vaccination was refused"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Completion Status",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0322",
        description="Completion status (CP=Complete, RE=Refused, NA=Not Administered)"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Action Code - RXA",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0323",
        description="Action code (A=Add, D=Delete, U=Update)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="System Entry Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time record was entered into system"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Administered Drug Manufacturer Code",
        data_type="CWE",
        length=250,
        description="Manufacturer of administered vaccine"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Administered Mass/Vaccine Code",
        data_type="CWE",
        length=250,
        description="Mass/vaccine code"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Administered Given By",
        data_type="CWE",
        length=250,
        description="Person who gave the vaccination"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Administered How",
        data_type="ST",
        length=20,
        description="Method of administration"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Administered Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0336",
        description="Reason for administration"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Administered Site/Route",
        data_type="CWE",
        length=250,
        description="Site and route of administration"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Administered Site",
        data_type="CWE",
        length=250,
        table_binding="0163",
        description="Anatomical site of administration"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Administered Route",
        data_type="CWE",
        length=250,
        table_binding="0162",
        description="Route of administration"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Administered Dose",
        data_type="CQ",
        length=20,
        description="Dose administered"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Units for administered dose"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Time unit for administration rate"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Administered Strength",
        data_type="NM",
        length=5,
        description="Strength of vaccine administered"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Units for administered strength"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Substance Lot Number",
        data_type="ST",
        length=200,
        repeating=True,
        description="Lot number of vaccine substance"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Substance Expiration Date",
        data_type="DTM",
        length=24,
        repeating=True,
        description="Expiration date of vaccine substance"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Substance Manufacturer Name",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Manufacturer name of vaccine substance"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Substance/Treatment Refusal Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0491",
        description="Reason for refusal if vaccination was refused"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Indication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Indication for vaccination"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Completion Status",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0322",
        description="Completion status (CP=Complete, RE=Refused, NA=Not Administered)"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Action Code - RXA",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0323",
        description="Action code (A=Add, D=Delete, U=Update)"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="System Entry Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time record was entered into system"
    ),
}


# ============================================================================
# VXU Segment - Vaccination Update
# ============================================================================

VXU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - VXU",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this vaccination update segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administered Date/Time",
        data_type="DTM",
        length=24,
        required=True,
        description="Date/time vaccination was administered"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Administered Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0292",
        description="Vaccine code administered (CVX code)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Administered Amount",
        data_type="NM",
        length=5,
        description="Amount of vaccine administered"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Units for administered amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administered Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Notes about administration"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Provider who administered the vaccination"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administered-at Location",
        data_type="LA2",
        length=250,
        description="Location where vaccination was administered"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Time unit for administration rate"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administered Strength",
        data_type="NM",
        length=5,
        description="Strength of vaccine administered"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Units for administered strength"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Substance Refusal Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0491",
        description="Reason for refusal if vaccination was refused"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Completion Status",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0322",
        description="Completion status (CP=Complete, RE=Refused, NA=Not Administered)"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Action Code - RXA",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0323",
        description="Action code (A=Add, D=Delete, U=Update)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="System Entry Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time record was entered into system"
    ),
}


# ============================================================================
# VXR Segment - Vaccination Record Response
# ============================================================================

VXR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - VXR",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this vaccination record response segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administered Date/Time",
        data_type="DTM",
        length=24,
        required=True,
        description="Date/time vaccination was administered"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Administered Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0292",
        description="Vaccine code administered (CVX code)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Administered Amount",
        data_type="NM",
        length=5,
        description="Amount of vaccine administered"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Administered Units",
        data_type="CWE",
        length=250,
        description="Units for administered amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Administered Notes",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Notes about administration"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Administering Provider",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Provider who administered the vaccination"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Administered-at Location",
        data_type="LA2",
        length=250,
        description="Location where vaccination was administered"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Administered Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Time unit for administration rate"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administered Strength",
        data_type="NM",
        length=5,
        description="Strength of vaccine administered"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administered Strength Units",
        data_type="CWE",
        length=250,
        description="Units for administered strength"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Substance Refusal Reason",
        data_type="CWE",
        length=250,
        repeating=True,
        table_binding="0491",
        description="Reason for refusal if vaccination was refused"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Completion Status",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0322",
        description="Completion status (CP=Complete, RE=Refused, NA=Not Administered)"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Action Code - RXA",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0323",
        description="Action code (A=Add, D=Delete, U=Update)"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="System Entry Date/Time",
        data_type="DTM",
        length=24,
        description="Date/time record was entered into system"
    ),
}


# ============================================================================
# VXQ Segment - Vaccination Query
# ============================================================================

VXQ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - VXQ",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this vaccination query segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time of query"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Query Format Code",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0106",
        description="Query format code (R=Record, D=Display, T=Tabular)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Query Priority",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0091",
        description="Query priority (I=Immediate, D=Deferred)"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Query ID",
        data_type="ST",
        length=10,
        required=True,
        description="Unique query identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Who Subject Filter",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Patient identifier filter"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="What Subject Filter",
        data_type="CE",
        length=250,
        repeating=True,
        description="Vaccine code filter"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="What Department Data Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Department data code filter"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="What Data Code Value Qual.",
        data_type="VR",
        length=20,
        repeating=True,
        description="Data code value qualifier"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Query Results Level",
        data_type="ID",
        length=1,
        table_binding="0108",
        description="Level of detail for query results"
    ),
}


# ============================================================================
# VXX Segment - Vaccination Response
# ============================================================================

VXX_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - VXX",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number for this vaccination response segment"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Response Date/Time",
        data_type="DTM",
        length=24,
        required=True,
        description="Date/time of response"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Response Code",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0208",
        description="Response code (OK=Success, NF=Not Found, AE=Application Error)"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Response Message",
        data_type="ST",
        length=200,
        description="Response message text"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Hit Count Total",
        data_type="NM",
        length=10,
        description="Total number of vaccination records found"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="This Payload",
        data_type="NM",
        length=10,
        description="Number of records in this payload"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Hits Remaining",
        data_type="NM",
        length=10,
        description="Number of records remaining to be sent"
    ),
}


# ============================================================================
# RSP Segment - Response
# ============================================================================

RSP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Unique identifier for the query"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        required=True,
        description="Name of the query message"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Hit Count Total",
        data_type="NM",
        length=10,
        description="Total number of hits found"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="This Payload",
        data_type="NM",
        length=10,
        description="Number of records in this payload"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Hits Remaining",
        data_type="NM",
        length=10,
        description="Number of records remaining to be sent"
    ),
}


# ============================================================================
# RTB Segment - Tabular Response
# ============================================================================

RTB_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Unique identifier for the query"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        required=True,
        description="Name of the query message"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Column Description",
        data_type="RCD",
        length=40,
        repeating=True,
        description="Column descriptions for tabular data"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Row Data",
        data_type="RDT",
        length=65536,
        repeating=True,
        description="Row data for tabular response"
    ),
}


# ============================================================================
# QCN Segment - Cancel Query
# ============================================================================

QCN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        required=True,
        description="Unique identifier for the query to cancel (required)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Message Query Name",
        data_type="CE",
        length=250,
        description="Name of the query message to cancel"
    ),
}


# ============================================================================
# PV3 Segment - Patient Visit - Additional Information (v2.7+)
# ============================================================================

PV3_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - PV3",
        data_type="SI",
        length=4,
        description="Sequence number",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Patient Point of Care",
        data_type="PL",
        length=80,
        description="Patient point of care location",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient Room",
        data_type="PL",
        length=80,
        description="Patient room location",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Patient Bed",
        data_type="PL",
        length=80,
        description="Patient bed location",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Patient Location Status",
        data_type="IS",
        length=1,
        table_binding="0326",
        description="Patient location status",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Patient Location Type",
        data_type="IS",
        length=2,
        table_binding="0305",
        description="Patient location type",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Bed Status",
        data_type="IS",
        length=1,
        table_binding="0116",
        description="Bed status",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Room Type",
        data_type="IS",
        length=2,
        table_binding="0145",
        description="Room type",
        version_specific={
            "2.1": {},  # Not available in 2.1
            "2.2": {},  # Not available in 2.2
            "2.3": {},  # Not available in 2.3
            "2.4": {},  # Not available in 2.4
            "2.5": {},  # Not available in 2.5
            "2.6": {},  # Not available in 2.6
        }
    ),
}


# ============================================================================
# ADD Segment - Addendum
# ============================================================================

ADD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Addendum Continuation Pointer",
        data_type="ST",
        length=65536,
        description="Continuation pointer for addendum data"
    ),
}


# ============================================================================
# CER Segment - Certificate Detail
# ============================================================================

CER_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - CER",
        data_type="SI",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Serial Number",
        data_type="ST",
        length=80,
        description="Certificate serial number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Version",
        data_type="ST",
        length=80,
        description="Certificate version"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Granting Authority",
        data_type="XON",
        length=250,
        description="Authority that granted the certificate"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Issuing Authority",
        data_type="XON",
        length=250,
        description="Authority that issued the certificate"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Signature Algorithm",
        data_type="ST",
        length=80,
        description="Algorithm used for signature"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Certificate Type",
        data_type="CE",
        length=250,
        table_binding="0384",
        description="Type of certificate"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Certificate Server ID",
        data_type="ST",
        length=80,
        description="Server identifier for certificate"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Signature",
        data_type="ED",
        length=65536,
        description="Digital signature"
    ),
}


# ============================================================================
# NCK Segment - System Clock
# ============================================================================

NCK_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="System Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="System date and time"
    ),
}


# ============================================================================
# NDS Segment - Notification Detail
# ============================================================================

NDS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Notification Reference Number",
        data_type="NM",
        length=20,
        required=True,
        description="Reference number for notification"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Notification Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Date and time of notification"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Notification Alert Severity",
        data_type="CE",
        length=250,
        table_binding="0367",
        required=True,
        description="Severity level of notification alert"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Notification Code",
        data_type="CE",
        length=250,
        table_binding="0366",
        required=True,
        description="Code identifying the notification"
    ),
}


# ============================================================================
# NPU Segment - Bed Status Update
# ============================================================================

NPU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Bed Location",
        data_type="PL",
        length=80,
        required=True,
        description="Location of the bed"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Bed Status",
        data_type="IS",
        length=1,
        table_binding="0116",
        description="Status of the bed"
    ),
}


# ============================================================================
# NSC Segment - Application Status Change
# ============================================================================

NSC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Application Change Type",
        data_type="ID",
        length=1,
        table_binding="0409",
        required=True,
        description="Type of application change"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Current CPU",
        data_type="ST",
        length=30,
        description="Current CPU identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Current Fileserver",
        data_type="ST",
        length=30,
        description="Current fileserver identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Current Application",
        data_type="HD",
        length=30,
        description="Current application identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Current Facility",
        data_type="HD",
        length=30,
        description="Current facility identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="New CPU",
        data_type="ST",
        length=30,
        description="New CPU identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="New Fileserver",
        data_type="ST",
        length=30,
        description="New fileserver identifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="New Application",
        data_type="HD",
        length=30,
        description="New application identifier"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="New Facility",
        data_type="HD",
        length=30,
        description="New facility identifier"
    ),
}


# ============================================================================
# NST Segment - Application Control Level Statistics
# ============================================================================

NST_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Statistics Available",
        data_type="ID",
        length=1,
        table_binding="0136",
        required=True,
        description="Indicates if statistics are available"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Source Identifier",
        data_type="ST",
        length=30,
        description="Source of statistics"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Source Type",
        data_type="ID",
        length=3,
        table_binding="0332",
        description="Type of source"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Statistics Start",
        data_type="TS",
        length=26,
        description="Start time for statistics"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Statistics End",
        data_type="TS",
        length=26,
        description="End time for statistics"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Receive Character Count",
        data_type="NM",
        length=10,
        description="Number of characters received"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Send Character Count",
        data_type="NM",
        length=10,
        description="Number of characters sent"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Characters Received",
        data_type="ST",
        length=65536,
        description="Characters received (for debugging)"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Characters Sent",
        data_type="ST",
        length=65536,
        description="Characters sent (for debugging)"
    ),
}


# ============================================================================
# GOL Segment - Goal Detail
# ============================================================================

GOL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code (AD=Add, DE=Delete, UP=Update)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="Date/time of action"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Goal ID",
        data_type="EI",
        length=60,
        required=True,
        description="Unique identifier for the goal"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Goal Instance ID",
        data_type="EI",
        length=60,
        required=True,
        description="Instance identifier for this goal"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Episode of Care ID",
        data_type="EI",
        length=60,
        description="Episode of care identifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Goal List Priority",
        data_type="NM",
        length=60,
        description="Priority of goal in list"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Goal Established Date/Time",
        data_type="TS",
        length=26,
        description="Date/time goal was established"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Expected Goal Achieve Date/Time",
        data_type="TS",
        length=26,
        description="Expected date/time to achieve goal"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Goal Classification",
        data_type="CWE",
        length=250,
        description="Classification of the goal"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Goal Management Discipline",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Discipline managing the goal"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Current Goal Review Status",
        data_type="CWE",
        length=250,
        description="Current review status of goal"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Current Goal Review Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of current review"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Next Goal Review Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of next scheduled review"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Previous Goal Review Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of previous review"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Goal Review Interval",
        data_type="TQ",
        length=200,
        description="Interval between goal reviews"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Goal Evaluation",
        data_type="CWE",
        length=250,
        description="Evaluation of goal achievement"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Goal Evaluation Comment",
        data_type="ST",
        length=65536,
        repeating=True,
        description="Comments on goal evaluation"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Goal Life Cycle Status",
        data_type="CWE",
        length=250,
        description="Life cycle status of goal"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Goal Life Cycle Status Date/Time",
        data_type="TS",
        length=26,
        description="Date/time of life cycle status change"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Goal Target Type",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Type of target for goal"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Goal Target Name",
        data_type="XPN",
        length=250,
        repeating=True,
        description="Name of goal target"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Goal Target Address",
        data_type="XAD",
        length=250,
        repeating=True,
        description="Address of goal target"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Goal Target Organization",
        data_type="XON",
        length=250,
        repeating=True,
        description="Organization of goal target"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Goal Target Job Code/Class",
        data_type="JCC",
        length=20,
        repeating=True,
        description="Job code/class of goal target"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Goal Target Job Employee Number",
        data_type="CX",
        length=250,
        repeating=True,
        description="Employee number of goal target"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Goal Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time for goal"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Goal Stop Date/Time",
        data_type="TS",
        length=26,
        description="Stop date/time for goal"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Goal Description",
        data_type="ST",
        length=65536,
        required=True,
        description="Description of the goal"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Goal on Set Date/Time",
        data_type="TS",
        length=26,
        description="Date/time goal was set"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Goal Rank",
        data_type="NM",
        length=5,
        description="Rank/priority of goal"
    ),
    31: FieldDefinition(
        field_index=31,
        field_name="Goal Achievement Status",
        data_type="CWE",
        length=250,
        description="Status of goal achievement"
    ),
    32: FieldDefinition(
        field_index=32,
        field_name="Goal Achieve Date/Time",
        data_type="TS",
        length=26,
        description="Date/time goal was achieved"
    ),
    33: FieldDefinition(
        field_index=33,
        field_name="Goal Evaluation Cycle",
        data_type="ST",
        length=32,
        description="Evaluation cycle for goal"
    ),
    34: FieldDefinition(
        field_index=34,
        field_name="Evaluation Date/Time",
        data_type="TS",
        length=26,
        repeating=True,
        description="Date/time of evaluation"
    ),
    35: FieldDefinition(
        field_index=35,
        field_name="Goal Delete Reason Code",
        data_type="CWE",
        length=250,
        description="Reason code for goal deletion"
    ),
    36: FieldDefinition(
        field_index=36,
        field_name="Goal Delete Date/Time",
        data_type="TS",
        length=26,
        description="Date/time goal was deleted"
    ),
}


# ============================================================================
# IIM Segment - Inventory Item Master
# ============================================================================

IIM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - IIM",
        data_type="CWE",
        length=250,
        required=True,
        description="Primary key identifier for inventory item"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Service Item Code",
        data_type="CWE",
        length=250,
        description="Service item code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Inventory Lot Number",
        data_type="ST",
        length=20,
        description="Lot number for inventory item"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Inventory Expiration Date",
        data_type="TS",
        length=26,
        description="Expiration date for inventory item"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Inventory Manufacturer Name",
        data_type="CWE",
        length=250,
        description="Manufacturer name"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Inventory Location",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Location of inventory item"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Inventory Received Date",
        data_type="TS",
        length=26,
        description="Date inventory was received"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Inventory Received Quantity",
        data_type="NM",
        length=10,
        description="Quantity received"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Inventory Received Quantity Unit",
        data_type="CWE",
        length=250,
        description="Unit for received quantity"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Inventory Received Average Cost",
        data_type="MO",
        length=20,
        description="Average cost of received inventory"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Inventory On Hand Date",
        data_type="TS",
        length=26,
        description="Date of on-hand inventory count"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Inventory On Hand Quantity",
        data_type="NM",
        length=10,
        description="Quantity on hand"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Inventory On Hand Quantity Unit",
        data_type="CWE",
        length=250,
        description="Unit for on-hand quantity"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Procedure Code",
        data_type="CNE",
        length=250,
        repeating=True,
        description="Procedure code associated with inventory item"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Procedure Code Modifier",
        data_type="CNE",
        length=250,
        repeating=True,
        description="Modifier for procedure code"
    ),
}


# ============================================================================
# INV Segment - Inventory Detail
# ============================================================================

INV_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Substance Identifier",
        data_type="CWE",
        length=250,
        required=True,
        description="Identifier for the substance/inventory item"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Substance Status",
        data_type="CWE",
        length=250,
        repeating=True,
        required=True,
        table_binding="0373",
        description="Status of the substance"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Substance Type",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0387",
        description="Type of substance"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Inventory Container Identifier",
        data_type="CWE",
        length=250,
        description="Container identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Container Carrier Identifier",
        data_type="CWE",
        length=250,
        description="Carrier identifier for container"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Position on Carrier",
        data_type="CWE",
        length=250,
        description="Position of container on carrier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Initial Quantity",
        data_type="NM",
        length=10,
        description="Initial quantity"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Current Quantity",
        data_type="NM",
        length=10,
        description="Current quantity"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Available Quantity",
        data_type="NM",
        length=10,
        description="Available quantity"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Consumption Quantity",
        data_type="NM",
        length=10,
        description="Consumption quantity"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Quantity Units",
        data_type="CWE",
        length=250,
        description="Units for quantity"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Expiration Date/Time",
        data_type="TS",
        length=26,
        description="Expiration date/time"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="First Used Date/Time",
        data_type="TS",
        length=26,
        description="First used date/time"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="On Board Stability Duration",
        data_type="TQ",
        length=200,
        description="Stability duration on board"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Test/Fluid Identifier(s)",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Test or fluid identifiers"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Manufacturer Lot Number",
        data_type="ST",
        length=20,
        description="Manufacturer lot number"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Manufacturer Identifier",
        data_type="CWE",
        length=250,
        description="Manufacturer identifier"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Supplier Identifier",
        data_type="CWE",
        length=250,
        description="Supplier identifier"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="On Board Stability Time",
        data_type="CQ",
        length=20,
        description="Stability time on board"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Target Value",
        data_type="CQ",
        length=20,
        description="Target value for substance"
    ),
}


# ============================================================================
# IPC Segment - Imaging Procedure Control Segment
# ============================================================================

IPC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Accession Number",
        data_type="EI",
        length=60,
        required=True,
        description="Accession number for imaging procedure"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Requested Procedure ID",
        data_type="EI",
        length=60,
        required=True,
        description="Requested procedure identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Study Instance UID",
        data_type="EI",
        length=60,
        description="Study instance unique identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Scheduled Procedure Step ID",
        data_type="EI",
        length=60,
        description="Scheduled procedure step identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Modality",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Imaging modality (CT, MR, US, etc.)"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Protocol Code",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Protocol code for procedure"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Protocol Name",
        data_type="ST",
        length=250,
        description="Name of protocol"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Scheduled Station Name",
        data_type="CWE",
        length=250,
        description="Scheduled station name"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Scheduled Procedure Step Location",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Location for scheduled procedure step"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Scheduled Station AE Title",
        data_type="ST",
        length=16,
        description="Scheduled station AE title"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Scheduled Procedure Step Start Date/Time",
        data_type="TS",
        length=26,
        description="Start date/time for scheduled procedure step"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Scheduled Procedure Step Start Date/Time Offset",
        data_type="NM",
        length=20,
        description="Offset for start date/time"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Scheduled Procedure Step Duration",
        data_type="NM",
        length=20,
        description="Duration of scheduled procedure step"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Scheduled Procedure Step Priority",
        data_type="ST",
        length=4,
        description="Priority of scheduled procedure step"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Scheduled Workitem Code",
        data_type="CWE",
        length=250,
        description="Workitem code for scheduled procedure"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Scheduled Station Name",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Scheduled station names"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Scheduled Procedure Step Description",
        data_type="ST",
        length=250,
        repeating=True,
        description="Description of scheduled procedure step"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Scheduled Performing Physician's Name",
        data_type="XCN",
        length=250,
        repeating=True,
        description="Performing physician name"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Scheduled Procedure Step Location",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Location for scheduled procedure step"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Pre-Medication",
        data_type="CWE",
        length=250,
        repeating=True,
        description="Pre-medication information"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Scheduled Procedure Step Status",
        data_type="CWE",
        length=250,
        table_binding="0277",
        description="Status of scheduled procedure step"
    ),
}


# ============================================================================
# ISD Segment - Interaction Status Detail
# ============================================================================

ISD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Reference Interaction Number",
        data_type="NM",
        length=20,
        required=True,
        description="Reference number for interaction"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Interaction Type ID",
        data_type="CWE",
        length=250,
        required=True,
        description="Type identifier for interaction"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Interaction Active State",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0387",
        description="Active state of interaction"
    ),
}


# ============================================================================
# SAD Segment - Specimen Additive
# ============================================================================

SAD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Additive or Preservative",
        data_type="CWE",
        length=250,
        required=False,
        description="Additive or preservative used with specimen"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Additive/Preservative Description",
        data_type="ST",
        length=200,
        required=False,
        description="Description of additive or preservative"
    ),
}


# ============================================================================
# SCV Segment - Scheduling Class Value Pair
# ============================================================================

SCV_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Parameter Class",
        data_type="CWE",
        length=250,
        required=False,
        table_binding="0294",
        description="Parameter class code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Parameter Value",
        data_type="ST",
        length=250,
        required=False,
        description="Parameter value"
    ),
}


# ============================================================================
# SPD Segment - Specimen Disposition
# ============================================================================

SPD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Specimen Disposition",
        data_type="CWE",
        length=250,
        required=False,
        table_binding="0491",
        description="Disposition of specimen"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Specimen Disposition Description",
        data_type="ST",
        length=200,
        required=False,
        description="Description of specimen disposition"
    ),
}


# ============================================================================
# SRT Segment - Sort Order
# ============================================================================

SRT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sort-by Field",
        data_type="ST",
        length=20,
        required=False,
        description="Field to sort by"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequencing",
        data_type="ID",
        length=1,
        required=False,
        table_binding="0397",
        description="Sort order (ASC or DESC)"
    ),
}


# ============================================================================
# OMD Segment - Dietary Order
# ============================================================================

OMD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OMD"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Tray Type",
        data_type="CE",
        length=250,
        description="Type of tray"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Service Period",
        data_type="CE",
        length=250,
        description="Service period"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Text Instruction",
        data_type="ST",
        length=200,
        description="Text instruction"
    ),
}


# ============================================================================
# OMG Segment - General Clinical Order
# ============================================================================

OMG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OMG"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# OML Segment - Laboratory Order
# ============================================================================

OML_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OML"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# OMN Segment - Non-stock Supply Order
# ============================================================================

OMN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OMN"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Requested Give Code",
        data_type="CE",
        length=250,
        description="Requested give code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Requested Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Requested give amount minimum"
    ),
}


# ============================================================================
# OMP Segment - Pharmacy/Treatment Order
# ============================================================================

OMP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OMP"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Requested Give Code",
        data_type="CE",
        length=250,
        description="Requested give code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Requested Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Requested give amount minimum"
    ),
}


# ============================================================================
# ORD Segment - Dietary Order Acknowledgment
# ============================================================================

ORD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORD"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORF Segment - Observations Result
# ============================================================================

ORF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORF"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORI Segment - Imaging Order
# ============================================================================

ORI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORI"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORL Segment - Laboratory Acknowledgment
# ============================================================================

ORL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORL"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Laboratory Allergen Type Code",
        data_type="CE",
        length=250,
        description="Laboratory allergen type code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Allergen Code/Mnemonic/Description",
        data_type="CE",
        length=250,
        description="Allergen code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Allergen Severity Code",
        data_type="CE",
        length=250,
        description="Allergen severity code"
    ),
}


# ============================================================================
# ORM Segment - Pharmacy/Treatment Order Message
# ============================================================================

ORM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORM"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORN Segment - Non-stock Supply Acknowledgment
# ============================================================================

ORN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORN"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORP Segment - Pharmacy/Treatment Order Acknowledgment
# ============================================================================

ORP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORP"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORR Segment - General Order Response
# ============================================================================

ORR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORS Segment - Stock Supply Acknowledgment
# ============================================================================

ORS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORS"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Order Control",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0119",
        description="Order control code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# ORU Segment - Unsolicited Transmission of an Observation Message
# ============================================================================

ORU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="ORU"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - ORU",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number",
        data_type="EI",
        length=22,
        description="Placer order number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Order Number",
        data_type="EI",
        length=22,
        description="Filler order number"
    ),
}


# ============================================================================
# OSD Segment - Observation Selection
# ============================================================================

OSD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OSD"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sequence/Results Flag",
        data_type="ID",
        length=1,
        description="Sequence/results flag"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Order Number: Entity Identifier",
        data_type="ST",
        length=22,
        description="Placer order number entity identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Placer Order Number: Namespace ID",
        data_type="IS",
        length=227,
        description="Placer order number namespace ID"
    ),
}


# ============================================================================
# OSP Segment - Observation Specimen
# ============================================================================

OSP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="OSP"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Sequence",
        data_type="NM",
        length=4,
        description="Segment sequence"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Specimen Source",
        data_type="SPS",
        length=300,
        description="Specimen source"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Specimen Collection Date/Time",
        data_type="TS",
        length=26,
        description="Specimen collection date/time"
    ),
}


# ============================================================================
# PEX Segment - Product Experience
# ============================================================================

PEX_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PEX"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Event Identifiers Used",
        data_type="CE",
        length=250,
        description="Event identifiers used"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Symptom/Diagnosis Code",
        data_type="CE",
        length=250,
        description="Event symptom/diagnosis code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Onset Date/Time",
        data_type="TS",
        length=26,
        description="Event onset date/time"
    ),
}


# ============================================================================
# PE1 Segment - Product Experience Header
# ============================================================================

PE1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PE1"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - PE1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Product Identifier",
        data_type="CE",
        length=250,
        required=True,
        description="Product identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Product Name",
        data_type="ST",
        length=250,
        description="Product name"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Product Lot Number",
        data_type="ST",
        length=250,
        description="Product lot number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Product Expiration Date",
        data_type="TS",
        length=26,
        description="Product expiration date"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Product Manufacturer Identifier",
        data_type="CE",
        length=250,
        description="Manufacturer identifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Product Manufacturer Name",
        data_type="ST",
        length=250,
        description="Manufacturer name"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Product Recall Status",
        data_type="CE",
        length=250,
        table_binding="0238",
        description="Recall status"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Product Recall Date/Time",
        data_type="TS",
        length=26,
        description="Recall date/time"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Product Recall Reason",
        data_type="CE",
        length=250,
        description="Recall reason"
    ),
}


# ============================================================================
# PE2 Segment - Product Experience Data
# ============================================================================

PE2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PE2"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - PE2",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Identifiers Used",
        data_type="CE",
        length=250,
        repeating=True,
        description="Event identifiers"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Symptom/Diagnosis Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="Symptom/diagnosis codes"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Event Onset Date/Time",
        data_type="TS",
        length=26,
        description="Event onset date/time"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Event Exacerbation Date/Time",
        data_type="TS",
        length=26,
        description="Exacerbation date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Event Improved Date/Time",
        data_type="TS",
        length=26,
        description="Improved date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Event Ended Date/Time",
        data_type="TS",
        length=26,
        description="Ended date/time"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Event Location Occurred",
        data_type="PL",
        length=80,
        description="Location where event occurred"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Event Qualification",
        data_type="ID",
        length=1,
        repeating=True,
        table_binding="0237",
        description="Event qualifications"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Event Serious",
        data_type="ID",
        length=1,
        table_binding="0239",
        description="Event seriousness indicator"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Event Expected",
        data_type="ID",
        length=1,
        table_binding="0240",
        description="Event expected indicator"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Event Outcome",
        data_type="ID",
        length=1,
        repeating=True,
        table_binding="0241",
        description="Event outcome"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Patient Outcome",
        data_type="ID",
        length=1,
        table_binding="0242",
        description="Patient outcome"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Event Description from Others",
        data_type="FT",
        length=600,
        description="Event description"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Event Description from Original Reporter",
        data_type="FT",
        length=600,
        description="Original reporter description"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Event Description from Patient",
        data_type="FT",
        length=600,
        description="Patient description"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Event Description from Practitioner",
        data_type="FT",
        length=600,
        description="Practitioner description"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Event Description from Autopsy",
        data_type="FT",
        length=600,
        description="Autopsy description"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Cause Of Death",
        data_type="CE",
        length=250,
        repeating=True,
        description="Cause of death codes"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Primary Observer Name",
        data_type="XPN",
        length=250,
        description="Primary observer name"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Primary Observer Address",
        data_type="XAD",
        length=250,
        description="Primary observer address"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Primary Observer Telephone",
        data_type="XTN",
        length=250,
        repeating=True,
        description="Primary observer telephone"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Primary Observer's Qualification",
        data_type="ID",
        length=1,
        table_binding="0243",
        description="Observer qualification"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Confirmation Provided By",
        data_type="ID",
        length=1,
        table_binding="0244",
        description="Confirmation provider"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Primary Observer Aware Of Diagnosis",
        data_type="ID",
        length=1,
        table_binding="0245",
        description="Observer aware of diagnosis"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Primary Observer's Identity May Be Divulged",
        data_type="ID",
        length=1,
        table_binding="0246",
        description="Identity disclosure permission"
    ),
}


# ============================================================================
# STZ Segment - Sterilization
# ============================================================================

STZ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="STZ"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - STZ",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Sterilization Type",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0247",
        description="Type of sterilization"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Sterilization Cycle",
        data_type="CE",
        length=250,
        description="Sterilization cycle identifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Sterilization Cycle Time",
        data_type="NM",
        length=4,
        description="Cycle time in minutes"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Sterilization Date/Time",
        data_type="TS",
        length=26,
        description="Sterilization date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Sterilization Expiration Date/Time",
        data_type="TS",
        length=26,
        description="Expiration date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Sterilization Lot Number",
        data_type="ST",
        length=250,
        description="Lot number"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Sterilization Operator Name",
        data_type="XCN",
        length=250,
        description="Operator name"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Sterilization Indicator",
        data_type="ID",
        length=1,
        table_binding="0248",
        description="Sterilization indicator"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Sterilization Chemical Type",
        data_type="CE",
        length=250,
        description="Chemical type used"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Sterilization Chemical Concentration",
        data_type="NM",
        length=4,
        description="Chemical concentration"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Sterilization Temperature",
        data_type="NM",
        length=4,
        description="Temperature in degrees"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Sterilization Pressure",
        data_type="NM",
        length=4,
        description="Pressure value"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Sterilization Duration",
        data_type="NM",
        length=4,
        description="Duration in minutes"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Sterilization Quality Control Indicator",
        data_type="ID",
        length=1,
        table_binding="0249",
        description="Quality control indicator"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Sterilization Quality Control Date/Time",
        data_type="TS",
        length=26,
        description="Quality control date/time"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Sterilization Quality Control Results",
        data_type="ST",
        length=250,
        description="Quality control results"
    ),
}


# ============================================================================
# PGL Segment - Patient Goal
# ============================================================================

PGL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PGL"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Goal ID",
        data_type="EI",
        length=22,
        description="Goal ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Goal Instance ID",
        data_type="EI",
        length=22,
        description="Goal instance ID"
    ),
}


# ============================================================================
# PIN Segment - Patient Insurance Information
# ============================================================================

PIN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PIN"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - PIN",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Insurance Company ID",
        data_type="CX",
        length=250,
        description="Insurance company ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Insurance Company Name",
        data_type="XON",
        length=250,
        description="Insurance company name"
    ),
}


# ============================================================================
# PMU Segment - Add Personnel Record
# ============================================================================

PMU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PMU"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Event Reason",
        data_type="CE",
        length=250,
        required=True,
        description="Event reason"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Date/Time",
        data_type="TS",
        length=26,
        description="Event date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Operator ID",
        data_type="XCN",
        length=250,
        description="Event operator ID"
    ),
}


# ============================================================================
# PPG Segment - Patient Pathway Goal
# ============================================================================

PPG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PPG"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Goal ID",
        data_type="EI",
        length=22,
        description="Goal ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Goal Instance ID",
        data_type="EI",
        length=22,
        description="Goal instance ID"
    ),
}


# ============================================================================
# PPT Segment - Patient Pathway Problem
# ============================================================================

PPT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PPT"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Pathway Problem ID",
        data_type="EI",
        length=22,
        description="Pathway problem ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Pathway Problem Instance ID",
        data_type="EI",
        length=22,
        description="Pathway problem instance ID"
    ),
}


# ============================================================================
# PPV Segment - Patient Pathway Variance
# ============================================================================

PPV_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PPV"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Variance Instance ID",
        data_type="EI",
        length=22,
        description="Variance instance ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Documented Date/Time",
        data_type="TS",
        length=26,
        description="Documented date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Stated Variance Date/Time",
        data_type="TS",
        length=26,
        description="Stated variance date/time"
    ),
}


# ============================================================================
# PTR Segment - Patient Pathway Problem Relationship
# ============================================================================

PTR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="PTR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Action Code",
        data_type="ID",
        length=2,
        required=True,
        table_binding="0287",
        description="Action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Pathway Problem ID",
        data_type="EI",
        length=22,
        description="Pathway problem ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Pathway Problem Instance ID",
        data_type="EI",
        length=22,
        description="Pathway problem instance ID"
    ),
}


# ============================================================================
# QCK Segment - Query Selection
# ============================================================================

QCK_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="QCK"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Select Field",
        data_type="ST",
        length=20,
        description="Select field"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Relational Operator",
        data_type="ID",
        length=2,
        table_binding="0209",
        description="Relational operator"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Value",
        data_type="ST",
        length=20,
        description="Value"
    ),
}


# ============================================================================
# RCI Segment - Resource Identification
# ============================================================================

RCI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RCI"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Resource Identifier",
        data_type="EI",
        length=22,
        description="Resource identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Resource Type",
        data_type="CE",
        length=250,
        description="Resource type"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Resource Group",
        data_type="CE",
        length=250,
        description="Resource group"
    ),
}


# ============================================================================
# RDR Segment - Pharmacy/Treatment Dispense Information
# ============================================================================

RDR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RDR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Dispense Sub-ID Counter",
        data_type="NM",
        length=4,
        description="Dispense sub-ID counter"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Actual Dispense Date/Time",
        data_type="TS",
        length=26,
        description="Actual dispense date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Actual Dispense Amount",
        data_type="NM",
        length=20,
        description="Actual dispense amount"
    ),
}


# ============================================================================
# RDY Segment - Display Data
# ============================================================================

RDY_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RDY"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Section",
        data_type="CE",
        length=250,
        description="Section"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Line Number",
        data_type="NM",
        length=4,
        description="Line number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Display Level",
        data_type="NM",
        length=4,
        description="Display level"
    ),
}


# ============================================================================
# REF Segment - Professional Referral
# ============================================================================

REF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="REF"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Referral Status",
        data_type="CE",
        length=250,
        description="Referral status"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Referral Priority",
        data_type="CE",
        length=250,
        description="Referral priority"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Referral Type",
        data_type="CE",
        length=250,
        description="Referral type"
    ),
}


# ============================================================================
# RPA Segment - Return Patient Authorization
# ============================================================================

RPA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RPA"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Authorization Number",
        data_type="EI",
        length=22,
        description="Authorization number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date",
        data_type="TS",
        length=26,
        description="Date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Source",
        data_type="ST",
        length=20,
        description="Source"
    ),
}


# ============================================================================
# RPI Segment - Return Patient Information
# ============================================================================

RPI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RPI"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Return Patient Identifier",
        data_type="CX",
        length=250,
        description="Return patient identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient Name",
        data_type="XPN",
        length=250,
        description="Patient name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        description="Mother's maiden name"
    ),
}


# ============================================================================
# RPL Segment - Return Patient List
# ============================================================================

RPL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RPL"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Return Patient Identifier",
        data_type="CX",
        length=250,
        description="Return patient identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient Name",
        data_type="XPN",
        length=250,
        description="Patient name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        description="Mother's maiden name"
    ),
}


# ============================================================================
# RPR Segment - Return Patient Display
# ============================================================================

RPR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RPR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Return Patient Identifier",
        data_type="CX",
        length=250,
        description="Return patient identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient Name",
        data_type="XPN",
        length=250,
        description="Patient name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Mother's Maiden Name",
        data_type="XPN",
        length=250,
        description="Mother's maiden name"
    ),
}


# ============================================================================
# RQA Segment - Request Patient Authorization
# ============================================================================

RQA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RQA"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Authorization Number",
        data_type="EI",
        length=22,
        description="Authorization number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date",
        data_type="TS",
        length=26,
        description="Date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Source",
        data_type="ST",
        length=20,
        description="Source"
    ),
}


# ============================================================================
# RQC Segment - Request Clinical Information
# ============================================================================

RQC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RQC"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Date/Time",
        data_type="TS",
        length=26,
        description="Query date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Query Format Code",
        data_type="ID",
        length=1,
        table_binding="0106",
        description="Query format code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Query Priority",
        data_type="ID",
        length=1,
        table_binding="0091",
        description="Query priority"
    ),
}


# ============================================================================
# RQI Segment - Request Patient Information
# ============================================================================

RQI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RQI"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Request Date",
        data_type="TS",
        length=26,
        description="Request date"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Response Due Date",
        data_type="TS",
        length=26,
        description="Response due date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Patient Consent",
        data_type="ID",
        length=1,
        table_binding="0139",
        description="Patient consent"
    ),
}


# ============================================================================
# RQP Segment - Request Patient Demographics
# ============================================================================

RQP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RQP"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Segment Action Code",
        data_type="ID",
        length=1,
        table_binding="0206",
        description="Segment action code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Patient Last Name",
        data_type="FN",
        length=194,
        description="Patient last name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Patient First Name",
        data_type="ST",
        length=30,
        description="Patient first name"
    ),
}


# ============================================================================
# RQQ Segment - Event Query
# ============================================================================

RQQ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RQQ"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Event Identifier",
        data_type="CE",
        length=250,
        description="Event identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Event Completion Date/Time",
        data_type="TS",
        length=26,
        description="Event completion date/time"
    ),
}


# ============================================================================
# RRI Segment - Return Referral Information
# ============================================================================

RRI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="RRI"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Referral Status",
        data_type="CE",
        length=250,
        description="Referral status"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Referral Priority",
        data_type="CE",
        length=250,
        description="Referral priority"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Referral Type",
        data_type="CE",
        length=250,
        description="Referral type"
    ),
}


# ============================================================================
# SQM Segment - Schedule Query Message
# ============================================================================

SQM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="SQM"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Query Response Format Code",
        data_type="ID",
        length=1,
        table_binding="0106",
        description="Query response format code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Stored Procedure Name",
        data_type="CE",
        length=250,
        description="Stored procedure name"
    ),
}


# ============================================================================
# SQR Segment - Schedule Query Response
# ============================================================================

SQR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="SQR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - SQR",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Placer Appointment ID",
        data_type="EI",
        length=22,
        description="Placer appointment ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Filler Appointment ID",
        data_type="EI",
        length=22,
        description="Filler appointment ID"
    ),
}


# ============================================================================
# SRM Segment - Schedule Request Message
# ============================================================================

SRM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="SRM"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Appointment Placer",
        data_type="EI",
        length=22,
        description="Appointment placer"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Appointment Filler",
        data_type="EI",
        length=22,
        description="Appointment filler"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Occurrence Number",
        data_type="NM",
        length=4,
        description="Occurrence number"
    ),
}


# ============================================================================
# SRR Segment - Scheduled Request Response
# ============================================================================

SRR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="SRR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Placer Appointment ID",
        data_type="EI",
        length=22,
        description="Placer appointment ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Filler Appointment ID",
        data_type="EI",
        length=22,
        description="Filler appointment ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Placer Group Number",
        data_type="EI",
        length=22,
        description="Placer group number"
    ),
}


# ============================================================================
# SSR Segment - Specimen Status Request
# ============================================================================

SSR_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="SSR"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Specimen ID",
        data_type="EI",
        length=22,
        description="Specimen ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Specimen Status",
        data_type="CE",
        length=250,
        description="Specimen status"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Specimen Status Date/Time",
        data_type="TS",
        length=26,
        description="Specimen status date/time"
    ),
}


# ============================================================================
# SSU Segment - Specimen Status Update
# ============================================================================

SSU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="SSU"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Specimen ID",
        data_type="EI",
        length=22,
        description="Specimen ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Specimen Status",
        data_type="CE",
        length=250,
        description="Specimen status"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Specimen Status Date/Time",
        data_type="TS",
        length=26,
        description="Specimen status date/time"
    ),
}


# ============================================================================
# STC Segment - System Clock
# ============================================================================

STC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="STC"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="System Date/Time",
        data_type="TS",
        length=26,
        required=True,
        description="System date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="System Time Zone",
        data_type="ST",
        length=5,
        description="System time zone"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Daylight Saving Time Indicator",
        data_type="ID",
        length=1,
        table_binding="0243",
        description="Daylight saving time indicator"
    ),
}


# ============================================================================
# TCU Segment - Test Code Configuration
# ============================================================================

TCU_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="TCU"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Set ID - TCU",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Universal Service Identifier",
        data_type="CE",
        length=250,
        required=True,
        description="Universal service identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Auto-Dilution Factor Default",
        data_type="SN",
        length=20,
        description="Auto-dilution factor default"
    ),
}


# ============================================================================
# UDM Segment - User Authentication Credential
# ============================================================================

UDM_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Segment Type ID",
        data_type="ST",
        length=3,
        required=True,
        description="UDM"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="User Authentication Credential Type Code",
        data_type="CWE",
        length=250,
        required=True,
        table_binding="0615",
        description="User authentication credential type code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="User Authentication Credential",
        data_type="ED",
        length=65536,
        required=True,
        description="User authentication credential"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="User Authentication Credential Expiration Date/Time",
        data_type="TS",
        length=26,
        description="User authentication credential expiration date/time"
    ),
}


# ============================================================================
# ABS Segment - Abstract
# ============================================================================

ABS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Discharge Care Provider",
        data_type="XCN",
        length=250,
        description="Discharge care provider"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Transfer Medical Service Code",
        data_type="CE",
        length=250,
        description="Transfer medical service code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Severity of Illness Code",
        data_type="CE",
        length=250,
        table_binding="0421",
        description="Severity of illness code"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Date/Time of Attestation",
        data_type="TS",
        length=26,
        description="Date/time of attestation"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Attested By",
        data_type="XCN",
        length=250,
        description="Attested by"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Triage Code",
        data_type="CE",
        length=250,
        table_binding="0422",
        description="Triage code"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Abstract Completion Date/Time",
        data_type="TS",
        length=26,
        description="Abstract completion date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Abstracted By",
        data_type="XCN",
        length=250,
        description="Abstracted by"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Case Category Code",
        data_type="CE",
        length=250,
        table_binding="0423",
        description="Case category code"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Caesarian Section Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Caesarian section indicator"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Gestation Category Code",
        data_type="CE",
        length=250,
        table_binding="0424",
        description="Gestation category code"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Gestation Period - Weeks",
        data_type="NM",
        length=3,
        description="Gestation period in weeks"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Newborn Code",
        data_type="CE",
        length=250,
        table_binding="0425",
        description="Newborn code"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Stillborn Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Stillborn indicator"
    ),
}


# ============================================================================
# BLC Segment - Blood Code
# ============================================================================

BLC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Blood Product Code",
        data_type="CE",
        length=250,
        table_binding="0426",
        description="Blood product code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Blood Amount",
        data_type="CQ",
        length=20,
        description="Blood amount"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Blood Type",
        data_type="CE",
        length=250,
        table_binding="0427",
        description="Blood type"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Blood Irradiated",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Blood irradiated indicator"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Blood Special Processing",
        data_type="CE",
        length=250,
        table_binding="0428",
        description="Blood special processing"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Blood Product Dispensed Status",
        data_type="CE",
        length=250,
        table_binding="0429",
        description="Blood product dispensed status"
    ),
}


# ============================================================================
# CM0 Segment - Clinical Study Master
# ============================================================================

CM0_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - CM0",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Sponsor Study ID",
        data_type="EI",
        length=22,
        required=True,
        description="Sponsor study ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Alternate Study ID",
        data_type="EI",
        length=22,
        description="Alternate study ID"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Title of Study",
        data_type="ST",
        length=300,
        required=True,
        description="Title of study"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Chairman of Study",
        data_type="XCN",
        length=250,
        description="Chairman of study"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Last IRB Approval Date",
        data_type="DT",
        length=8,
        description="Last IRB approval date"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Total Accrual to Date",
        data_type="NM",
        length=8,
        description="Total accrual to date"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Last Accrual Date",
        data_type="DT",
        length=8,
        description="Last accrual date"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Contact for Study",
        data_type="XCN",
        length=250,
        description="Contact for study"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Contact's Telephone Number",
        data_type="XTN",
        length=250,
        description="Contact's telephone number"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Contact's Address",
        data_type="XAD",
        length=250,
        description="Contact's address"
    ),
}


# ============================================================================
# CM1 Segment - Clinical Study Phase Master
# ============================================================================

CM1_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - CM1",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Study Phase Identifier",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0137",
        description="Study phase identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Description of Study Phase",
        data_type="ST",
        length=300,
        description="Description of study phase"
    ),
}


# ============================================================================
# CM2 Segment - Clinical Study Schedule Master
# ============================================================================

CM2_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - CM2",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Scheduled Time Point",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0138",
        description="Scheduled time point"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Description of Time Point",
        data_type="ST",
        length=300,
        description="Description of time point"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Events Scheduled This Time Point",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0139",
        description="Events scheduled this time point"
    ),
}


# ============================================================================
# CNS Segment - Clear Notification
# ============================================================================

CNS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Starting Notification Reference Number",
        data_type="NM",
        length=20,
        description="Starting notification reference number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Ending Notification Reference Number",
        data_type="NM",
        length=20,
        description="Ending notification reference number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Starting Notification Date/Time",
        data_type="TS",
        length=26,
        description="Starting notification date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Ending Notification Date/Time",
        data_type="TS",
        length=26,
        description="Ending notification date/time"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Starting Notification Code",
        data_type="CE",
        length=250,
        table_binding="0430",
        description="Starting notification code"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Ending Notification Code",
        data_type="CE",
        length=250,
        table_binding="0430",
        description="Ending notification code"
    ),
}


# ============================================================================
# CSP Segment - Clinical Study Phase
# ============================================================================

CSP_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Study Phase Identifier",
        data_type="CE",
        length=250,
        table_binding="0137",
        description="Study phase identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Date/time Study Phase Began",
        data_type="TS",
        length=26,
        description="Date/time study phase began"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Date/time Study Phase Ended",
        data_type="TS",
        length=26,
        description="Date/time study phase ended"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Study Phase Evaluability",
        data_type="CE",
        length=250,
        table_binding="0140",
        description="Study phase evaluability"
    ),
}


# ============================================================================
# ED Segment - Encapsulated Data
# ============================================================================

ED_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Source Application",
        data_type="HD",
        length=227,
        description="Source application"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Type of Data",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0191",
        description="Type of data"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Data Subtype",
        data_type="ID",
        length=3,
        table_binding="0291",
        description="Data subtype"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Encoding",
        data_type="ID",
        length=3,
        required=True,
        table_binding="0299",
        description="Encoding"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Data",
        data_type="TX",
        length=65536,
        required=True,
        description="Data"
    ),
}


# ============================================================================
# ILT Segment - Material Lot
# ============================================================================

ILT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - ILT",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Inventory Lot Number",
        data_type="ST",
        length=20,
        required=True,
        description="Inventory lot number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Inventory Expiration Date",
        data_type="TS",
        length=26,
        description="Inventory expiration date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Inventory Received Date",
        data_type="TS",
        length=26,
        description="Inventory received date"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Inventory Received Quantity",
        data_type="NM",
        length=10,
        description="Inventory received quantity"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Inventory Received Quantity Unit",
        data_type="CE",
        length=250,
        description="Inventory received quantity unit"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Inventory Received Item Cost",
        data_type="MO",
        length=20,
        description="Inventory received item cost"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Inventory On Hand Date",
        data_type="TS",
        length=26,
        description="Inventory on hand date"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Inventory On Hand Quantity",
        data_type="NM",
        length=10,
        description="Inventory on hand quantity"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Inventory On Hand Quantity Unit",
        data_type="CE",
        length=250,
        description="Inventory on hand quantity unit"
    ),
}


# ============================================================================
# OM7 Segment - Additional Basic Attributes
# ============================================================================

OM7_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Sequence Number - Test/Observation Master File",
        data_type="NM",
        length=4,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Universal Service Identifier",
        data_type="CE",
        length=250,
        required=True,
        description="Universal service identifier"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Category Identifier",
        data_type="CE",
        length=250,
        description="Category identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Category Description",
        data_type="TX",
        length=200,
        description="Category description"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Category Synonym",
        data_type="ST",
        length=200,
        repeating=True,
        description="Category synonym"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Effective Test/Service Start Date/Time",
        data_type="TS",
        length=26,
        description="Effective test/service start date/time"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Effective Test/Service End Date/Time",
        data_type="TS",
        length=26,
        description="Effective test/service end date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Test/Service Default Duration Quantity",
        data_type="NM",
        length=5,
        description="Test/service default duration quantity"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Test/Service Default Duration Units",
        data_type="CE",
        length=250,
        description="Test/service default duration units"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Test/Service Default Frequency",
        data_type="CE",
        length=250,
        description="Test/service default frequency"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Consent Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Consent indicator"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Consent Identifier",
        data_type="CE",
        length=250,
        table_binding="0141",
        description="Consent identifier"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Consent Effective Start Date/Time",
        data_type="TS",
        length=26,
        description="Consent effective start date/time"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Consent Effective End Date/Time",
        data_type="TS",
        length=26,
        description="Consent effective end date/time"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Consent Interval Quantity",
        data_type="NM",
        length=5,
        description="Consent interval quantity"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Consent Interval Units",
        data_type="CE",
        length=250,
        description="Consent interval units"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Consent Waiting Period Quantity",
        data_type="NM",
        length=5,
        description="Consent waiting period quantity"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Consent Waiting Period Units",
        data_type="CE",
        length=250,
        description="Consent waiting period units"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Effective Date/Time of Change",
        data_type="TS",
        length=26,
        description="Effective date/time of change"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Entered By",
        data_type="XCN",
        length=250,
        description="Entered by"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Orderable-at Location",
        data_type="PL",
        length=200,
        repeating=True,
        description="Orderable-at location"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Formulary Status",
        data_type="CE",
        length=250,
        table_binding="0473",
        description="Formulary status"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Special Order Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Special order indicator"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Primary Key Value - CDM",
        data_type="CE",
        length=250,
        description="Primary key value - CDM"
    ),
}


# ============================================================================
# PDC Segment - Product Detail Country
# ============================================================================

PDC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Manufacturer/Distributor",
        data_type="XON",
        length=250,
        required=True,
        description="Manufacturer/distributor"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Country",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0224",
        description="Country"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Brand Name",
        data_type="ST",
        length=60,
        description="Brand name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Device Family Name",
        data_type="ST",
        length=60,
        description="Device family name"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Generic Name",
        data_type="CE",
        length=250,
        description="Generic name"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Model Identifier",
        data_type="ST",
        length=60,
        description="Model identifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Catalogue Identifier",
        data_type="ST",
        length=60,
        description="Catalogue identifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Other Identifier",
        data_type="ST",
        length=60,
        repeating=True,
        description="Other identifier"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Product Code",
        data_type="CE",
        length=250,
        description="Product code"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Marketing Basis",
        data_type="ID",
        length=4,
        table_binding="0330",
        description="Marketing basis"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Marketing Approval ID",
        data_type="ST",
        length=60,
        description="Marketing approval ID"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Labeled Shelf Life",
        data_type="CQ",
        length=20,
        description="Labeled shelf life"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Expected Shelf Life",
        data_type="CQ",
        length=20,
        description="Expected shelf life"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Date First Marketed",
        data_type="TS",
        length=26,
        description="Date first marketed"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Date Last Marketed",
        data_type="TS",
        length=26,
        description="Date last marketed"
    ),
}


# ============================================================================
# PKG Segment - Packaging
# ============================================================================

PKG_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - PKG",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Packaging Units",
        data_type="CE",
        length=250,
        required=True,
        table_binding="0431",
        description="Packaging units"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Default Order Unit Of Measure Indicator",
        data_type="CE",
        length=250,
        table_binding="0432",
        description="Default order unit of measure indicator"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Package Quantity",
        data_type="NM",
        length=5,
        description="Package quantity"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Price",
        data_type="MO",
        length=20,
        description="Price"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Future Item Price",
        data_type="MO",
        length=20,
        description="Future item price"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Future Item Price Effective Date",
        data_type="TS",
        length=26,
        description="Future item price effective date"
    ),
}


# ============================================================================
# PRA Segment - Practitioner Detail
# ============================================================================

PRA_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Primary Key Value - PRA",
        data_type="CE",
        length=250,
        required=True,
        description="Primary key value - PRA"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Practitioner Group",
        data_type="CE",
        length=250,
        description="Practitioner group"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Practitioner Category",
        data_type="IS",
        length=3,
        repeating=True,
        table_binding="0186",
        description="Practitioner category"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Provider Billing",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Provider billing indicator"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Specialty",
        data_type="SPD",
        length=112,
        repeating=True,
        description="Specialty"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Practitioner ID Numbers",
        data_type="PLN",
        length=100,
        repeating=True,
        description="Practitioner ID numbers"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Privileges",
        data_type="PIP",
        length=770,
        repeating=True,
        description="Privileges"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Date Entered Practice",
        data_type="DT",
        length=8,
        description="Date entered practice"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Institution",
        data_type="CE",
        length=250,
        description="Institution"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Date Left Practice",
        data_type="DT",
        length=8,
        description="Date left practice"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Government Reimbursement Billing Eligibility",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0401",
        description="Government reimbursement billing eligibility"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Set ID - PRA",
        data_type="SI",
        length=4,
        description="Set ID - PRA"
    ),
}


# ============================================================================
# RXV Segment - Pharmacy/Treatment Give
# ============================================================================

RXV_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - RXV",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Bolus Type",
        data_type="CE",
        length=250,
        table_binding="0166",
        description="Bolus type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Bolus Dose Amount",
        data_type="CQ",
        length=20,
        description="Bolus dose amount"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Bolus Dose Amount Units",
        data_type="CE",
        length=250,
        description="Bolus dose amount units"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Bolus Dose Volume",
        data_type="CQ",
        length=20,
        description="Bolus dose volume"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Bolus Dose Volume Units",
        data_type="CE",
        length=250,
        description="Bolus dose volume units"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="VTBI - Volume To Be Infused",
        data_type="CQ",
        length=20,
        description="VTBI - volume to be infused"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="VTBI Units",
        data_type="CE",
        length=250,
        description="VTBI units"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Route",
        data_type="CE",
        length=250,
        table_binding="0162",
        description="Route"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Administration Site",
        data_type="CE",
        length=250,
        table_binding="0163",
        description="Administration site"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Administration Method",
        data_type="CE",
        length=250,
        table_binding="0164",
        description="Administration method"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Administration Rate",
        data_type="CQ",
        length=20,
        description="Administration rate"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Administration Rate Units",
        data_type="CE",
        length=250,
        description="Administration rate units"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="Administration Equipment",
        data_type="CE",
        length=250,
        table_binding="0165",
        description="Administration equipment"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Administration Notes",
        data_type="CE",
        length=250,
        repeating=True,
        description="Administration notes"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Substance Status",
        data_type="CE",
        length=250,
        table_binding="0167",
        description="Substance status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Substance Status Reason",
        data_type="CE",
        length=250,
        table_binding="0433",
        description="Substance status reason"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Substance Lot Number",
        data_type="ST",
        length=20,
        repeating=True,
        description="Substance lot number"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Substance Manufacturer Name",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0227",
        description="Substance manufacturer name"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Substance/Treatment Refusal Reason",
        data_type="CE",
        length=250,
        repeating=True,
        description="Substance/treatment refusal reason"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Component Drug Instances",
        data_type="NM",
        length=4,
        description="Component drug instances"
    ),
}


# ============================================================================
# RXI Segment - Pharmacy/Treatment Component
# ============================================================================

RXI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - RXI",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Give Code",
        data_type="CE",
        length=250,
        required=True,
        description="Give code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Give Amount - Minimum",
        data_type="NM",
        length=20,
        description="Give amount - minimum"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Give Amount - Maximum",
        data_type="NM",
        length=20,
        description="Give amount - maximum"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Give Units",
        data_type="CE",
        length=250,
        description="Give units"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Give Dosage Form",
        data_type="CE",
        length=250,
        description="Give dosage form"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Providers Administration Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Providers administration instructions"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Deliver-to Location",
        data_type="CE",
        length=250,
        description="Deliver-to location"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Substitution Status",
        data_type="ID",
        length=1,
        table_binding="0167",
        description="Substitution status"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Dispense Amount",
        data_type="NM",
        length=20,
        description="Dispense amount"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Dispense Units",
        data_type="CE",
        length=250,
        description="Dispense units"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Number Of Refills Remaining",
        data_type="NM",
        length=3,
        description="Number of refills remaining"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="Number Of Refills/Doses Dispensed",
        data_type="NM",
        length=3,
        description="Number of refills/doses dispensed"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="D/T Of Most Recent Refill Or Dose Dispensed",
        data_type="TS",
        length=26,
        description="D/T of most recent refill or dose dispensed"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="Total Daily Dose",
        data_type="CQ",
        length=20,
        description="Total daily dose"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="Needs Human Review",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Needs human review"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="Pharmacy/Treatment Suppliers Special Dispensing Instructions",
        data_type="CE",
        length=250,
        repeating=True,
        description="Pharmacy/treatment suppliers special dispensing instructions"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="Give Per (Time Unit)",
        data_type="ST",
        length=20,
        description="Give per (time unit)"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="Give Rate Amount",
        data_type="ST",
        length=6,
        description="Give rate amount"
    ),
    20: FieldDefinition(
        field_index=20,
        field_name="Give Rate Units",
        data_type="CE",
        length=250,
        description="Give rate units"
    ),
    21: FieldDefinition(
        field_index=21,
        field_name="Give Strength",
        data_type="NM",
        length=20,
        description="Give strength"
    ),
    22: FieldDefinition(
        field_index=22,
        field_name="Give Strength Units",
        data_type="CE",
        length=250,
        description="Give strength units"
    ),
    23: FieldDefinition(
        field_index=23,
        field_name="Substance Lot Number",
        data_type="ST",
        length=20,
        repeating=True,
        description="Substance lot number"
    ),
    24: FieldDefinition(
        field_index=24,
        field_name="Substance Expiration Date",
        data_type="TS",
        length=26,
        repeating=True,
        description="Substance expiration date"
    ),
    25: FieldDefinition(
        field_index=25,
        field_name="Substance Manufacturer Name",
        data_type="CE",
        length=250,
        repeating=True,
        table_binding="0227",
        description="Substance manufacturer name"
    ),
    26: FieldDefinition(
        field_index=26,
        field_name="Indication",
        data_type="CE",
        length=250,
        repeating=True,
        description="Indication"
    ),
    27: FieldDefinition(
        field_index=27,
        field_name="Give Drug Strength Volume",
        data_type="NM",
        length=5,
        description="Give drug strength volume"
    ),
    28: FieldDefinition(
        field_index=28,
        field_name="Give Drug Strength Volume Units",
        data_type="CE",
        length=250,
        description="Give drug strength volume units"
    ),
    29: FieldDefinition(
        field_index=29,
        field_name="Give Barcode Identifier",
        data_type="CE",
        length=250,
        description="Give barcode identifier"
    ),
    30: FieldDefinition(
        field_index=30,
        field_name="Pharmacy Order Type",
        data_type="ID",
        length=1,
        table_binding="0480",
        description="Pharmacy order type"
    ),
}


# ============================================================================
# URD Segment - Results/Update Definition
# ============================================================================

URD_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="R/U Date/Time",
        data_type="TS",
        length=26,
        description="R/U date/time"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Report Priority",
        data_type="ID",
        length=1,
        table_binding="0109",
        description="Report priority"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="R/U Who Subject Definition",
        data_type="ST",
        length=20,
        repeating=True,
        description="R/U who subject definition"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="R/U What Subject Definition",
        data_type="ID",
        length=3,
        repeating=True,
        table_binding="0048",
        description="R/U what subject definition"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="R/U What Department Code",
        data_type="CE",
        length=250,
        repeating=True,
        description="R/U what department code"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="R/U Display/Print Locations",
        data_type="ST",
        length=20,
        repeating=True,
        description="R/U display/print locations"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="R/U Results Level",
        data_type="ID",
        length=1,
        table_binding="0108",
        description="R/U results level"
    ),
}


# ============================================================================
# URS Segment - Unsolicited Selection
# ============================================================================

URS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="R/U Where Subject Definition",
        data_type="ST",
        length=20,
        repeating=True,
        description="R/U where subject definition"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="R/U When Data Start Date/Time",
        data_type="TS",
        length=26,
        description="R/U when data start date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="R/U When Data End Date/Time",
        data_type="TS",
        length=26,
        description="R/U when data end date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="R/U What User Qualifier",
        data_type="ST",
        length=20,
        repeating=True,
        description="R/U what user qualifier"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="R/U Other Results Subject Definition",
        data_type="ST",
        length=20,
        repeating=True,
        description="R/U other results subject definition"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="R/U Which Date/Time Status Qualifier",
        data_type="ID",
        length=12,
        repeating=True,
        table_binding="0142",
        description="R/U which date/time status qualifier"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="R/U Which Date/Time Selection Qualifier",
        data_type="ID",
        length=12,
        repeating=True,
        table_binding="0143",
        description="R/U which date/time selection qualifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="R/U When Date/Time Selection Qualifier",
        data_type="CQ",
        length=20,
        repeating=True,
        description="R/U when date/time selection qualifier"
    ),
}


# ============================================================================
# VTQ Segment - Virtual Table Query Request
# ============================================================================

VTQ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Query Tag",
        data_type="ST",
        length=32,
        description="Query tag"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Query/Response Format Code",
        data_type="ID",
        length=1,
        required=True,
        table_binding="0106",
        description="Query/response format code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="VT Query Name",
        data_type="CE",
        length=250,
        required=True,
        description="VT query name"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Virtual Table Name",
        data_type="CE",
        length=250,
        required=True,
        description="Virtual table name"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Selection Criteria",
        data_type="QSC",
        length=256,
        repeating=True,
        description="Selection criteria"
    ),
}


# ============================================================================
# Z-Segment (Custom Segment) Support Framework
# ============================================================================

# Registry for custom Z-segment definitions
# Z-segments are implementation-specific custom segments
_Z_SEGMENT_REGISTRY: Dict[str, Dict[int, FieldDefinition]] = {}


def register_z_segment(segment_name: str, field_definitions: Dict[int, FieldDefinition]) -> None:
    """
    Register a custom Z-segment definition.
    
    Z-segments are implementation-specific custom segments that start with 'Z'
    followed by two alphanumeric characters (e.g., Z01, ZAB, Z99).
    
    Args:
        segment_name: Z-segment name (must start with 'Z' and be 3 characters)
        field_definitions: Dictionary mapping field index to FieldDefinition
        
    Raises:
        ValueError: If segment_name is not a valid Z-segment name
    """
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Registering Z-segment: {segment_name}")
    
    if not segment_name or len(segment_name) != 3:
        raise ValueError(f"Z-segment name must be exactly 3 characters, got: {segment_name}")
    
    if not segment_name.startswith('Z'):
        raise ValueError(f"Z-segment name must start with 'Z', got: {segment_name}")
    
    if not segment_name[1:].isalnum():
        raise ValueError(f"Z-segment name characters 2-3 must be alphanumeric, got: {segment_name}")
    
    _Z_SEGMENT_REGISTRY[segment_name] = field_definitions
    logger.info(f"[{current_time}] Z-segment {segment_name} registered with {len(field_definitions)} fields")


def get_z_segment_fields(segment_name: str) -> Optional[Dict[int, FieldDefinition]]:
    """
    Get field definitions for a registered Z-segment.
    
    Args:
        segment_name: Z-segment name
        
    Returns:
        Dictionary mapping field index to FieldDefinition, or None if not registered
    """
    return _Z_SEGMENT_REGISTRY.get(segment_name)


def is_z_segment(segment_name: str) -> bool:
    """
    Check if a segment name is a Z-segment (custom segment).
    
    Args:
        segment_name: Segment name to check
        
    Returns:
        True if segment name is a Z-segment, False otherwise
    """
    if not segment_name or len(segment_name) != 3:
        return False
    
    return segment_name.startswith('Z') and segment_name[1:].isalnum()


def list_registered_z_segments() -> List[str]:
    """
    List all registered Z-segment names.
    
    Returns:
        List of registered Z-segment names
    """
    return list(_Z_SEGMENT_REGISTRY.keys())


def get_segment_fields(segment_name: str, version: Optional[str] = None) -> Dict[int, FieldDefinition]:
    """
    Get all field definitions for a segment.
    
    Args:
        segment_name: Segment name
        version: Optional HL7 version
        
    Returns:
        Dictionary mapping field index to FieldDefinition
    """
    # Check for Z-segment first
    if is_z_segment(segment_name):
        z_segment_defs = get_z_segment_fields(segment_name)
        if z_segment_defs:
            return z_segment_defs
    
    segment_defs = {
        "MSH": MSH_FIELD_DEFINITIONS,
        "PID": PID_FIELD_DEFINITIONS,
        "EVN": EVN_FIELD_DEFINITIONS,
        "PV1": PV1_FIELD_DEFINITIONS,
        "OBR": OBR_FIELD_DEFINITIONS,
        "OBX": OBX_FIELD_DEFINITIONS,
        "NTE": NTE_FIELD_DEFINITIONS,
        "AL1": AL1_FIELD_DEFINITIONS,
        "DG1": DG1_FIELD_DEFINITIONS,
        "PR1": PR1_FIELD_DEFINITIONS,
        "ORC": ORC_FIELD_DEFINITIONS,
        "IN1": IN1_FIELD_DEFINITIONS,
        "IN2": IN2_FIELD_DEFINITIONS,
        "IN3": IN3_FIELD_DEFINITIONS,
        "NK1": NK1_FIELD_DEFINITIONS,
        "PD1": PD1_FIELD_DEFINITIONS,
        "PV2": PV2_FIELD_DEFINITIONS,
        "GT1": GT1_FIELD_DEFINITIONS,
        "MSA": MSA_FIELD_DEFINITIONS,
        "ERR": ERR_FIELD_DEFINITIONS,
        "QRD": QRD_FIELD_DEFINITIONS,
        "QRF": QRF_FIELD_DEFINITIONS,
        "QAK": QAK_FIELD_DEFINITIONS,
        "QPD": QPD_FIELD_DEFINITIONS,
        "QRA": QRA_FIELD_DEFINITIONS,
        "RGS": RGS_FIELD_DEFINITIONS,
        "SPM": SPM_FIELD_DEFINITIONS,
        "SN": SN_FIELD_DEFINITIONS,
        "SPS": SPS_FIELD_DEFINITIONS,
        "TQ1": TQ1_FIELD_DEFINITIONS,
        "TQ2": TQ2_FIELD_DEFINITIONS,
        "RXR": RXR_FIELD_DEFINITIONS,
        "RXC": RXC_FIELD_DEFINITIONS,
        "RXA": RXA_FIELD_DEFINITIONS,
        "DSC": DSC_FIELD_DEFINITIONS,
        "UB1": UB1_FIELD_DEFINITIONS,
        "UB2": UB2_FIELD_DEFINITIONS,
        "ROL": ROL_FIELD_DEFINITIONS,
        "CTD": CTD_FIELD_DEFINITIONS,
        "ACC": ACC_FIELD_DEFINITIONS,
        "BHS": BHS_FIELD_DEFINITIONS,
        "BTS": BTS_FIELD_DEFINITIONS,
        "SCH": SCH_FIELD_DEFINITIONS,
        "TXA": TXA_FIELD_DEFINITIONS,
        "RCP": RCP_FIELD_DEFINITIONS,
        "RF1": RF1_FIELD_DEFINITIONS,
        "RMI": RMI_FIELD_DEFINITIONS,
        "AIS": AIS_FIELD_DEFINITIONS,
        "AIG": AIG_FIELD_DEFINITIONS,
        "AIL": AIL_FIELD_DEFINITIONS,
        "AIP": AIP_FIELD_DEFINITIONS,
        "DB1": DB1_FIELD_DEFINITIONS,
        "FAC": FAC_FIELD_DEFINITIONS,
        "STF": STF_FIELD_DEFINITIONS,
        "FHS": FHS_FIELD_DEFINITIONS,
        "FTS": FTS_FIELD_DEFINITIONS,
        "RXD": RXD_FIELD_DEFINITIONS,
        "RXE": RXE_FIELD_DEFINITIONS,
        "RXG": RXG_FIELD_DEFINITIONS,
        "RXO": RXO_FIELD_DEFINITIONS,
        "RXP": RXP_FIELD_DEFINITIONS,
        "CDM": CDM_FIELD_DEFINITIONS,
        "DRG": DRG_FIELD_DEFINITIONS,
        "MRG": MRG_FIELD_DEFINITIONS,
        "QID": QID_FIELD_DEFINITIONS,
        "QRI": QRI_FIELD_DEFINITIONS,
        "QSC": QSC_FIELD_DEFINITIONS,
        "RCD": RCD_FIELD_DEFINITIONS,
        "RDF": RDF_FIELD_DEFINITIONS,
        "RDT": RDT_FIELD_DEFINITIONS,
        "RQ1": RQ1_FIELD_DEFINITIONS,
        "RQD": RQD_FIELD_DEFINITIONS,
        "RPT": RPT_FIELD_DEFINITIONS,
        "SAC": SAC_FIELD_DEFINITIONS,
        "SCD": SCD_FIELD_DEFINITIONS,
        "SCP": SCP_FIELD_DEFINITIONS,
        "SDD": SDD_FIELD_DEFINITIONS,
        "SID": SID_FIELD_DEFINITIONS,
        "SLT": SLT_FIELD_DEFINITIONS,
        "SPR": SPR_FIELD_DEFINITIONS,
        "TCC": TCC_FIELD_DEFINITIONS,
        "TCD": TCD_FIELD_DEFINITIONS,
        "UAC": UAC_FIELD_DEFINITIONS,
        "VAR": VAR_FIELD_DEFINITIONS,
        "PDA": PDA_FIELD_DEFINITIONS,
        "FT1": FT1_FIELD_DEFINITIONS,
        "VXA": VXA_FIELD_DEFINITIONS,
        "VXU": VXU_FIELD_DEFINITIONS,
        "VXR": VXR_FIELD_DEFINITIONS,
        "VXQ": VXQ_FIELD_DEFINITIONS,
        "VXX": VXX_FIELD_DEFINITIONS,
        "SFT": SFT_FIELD_DEFINITIONS,
        "SAD": SAD_FIELD_DEFINITIONS,
        "SCV": SCV_FIELD_DEFINITIONS,
        "SPD": SPD_FIELD_DEFINITIONS,
        "SRT": SRT_FIELD_DEFINITIONS,
        "ABS": ABS_FIELD_DEFINITIONS,
        "BLC": BLC_FIELD_DEFINITIONS,
        "CM0": CM0_FIELD_DEFINITIONS,
        "CM1": CM1_FIELD_DEFINITIONS,
        "CM2": CM2_FIELD_DEFINITIONS,
        "CNS": CNS_FIELD_DEFINITIONS,
        "CSP": CSP_FIELD_DEFINITIONS,
        "ED": ED_FIELD_DEFINITIONS,
        "ADJ": ADJ_FIELD_DEFINITIONS,
        "AFF": AFF_FIELD_DEFINITIONS,
        "BTX": BTX_FIELD_DEFINITIONS,
        "DMI": DMI_FIELD_DEFINITIONS,
        "DON": DON_FIELD_DEFINITIONS,
        "PMT": PMT_FIELD_DEFINITIONS,
        "RBC": RBC_FIELD_DEFINITIONS,
        "REL": REL_FIELD_DEFINITIONS,
        "RRO": RRO_FIELD_DEFINITIONS,
        "RXX": RXX_FIELD_DEFINITIONS,
        "ILT": ILT_FIELD_DEFINITIONS,
        "OM7": OM7_FIELD_DEFINITIONS,
        "PDC": PDC_FIELD_DEFINITIONS,
        "PKG": PKG_FIELD_DEFINITIONS,
        "PRA": PRA_FIELD_DEFINITIONS,
        "RXV": RXV_FIELD_DEFINITIONS,
        "RXI": RXI_FIELD_DEFINITIONS,
        "URD": URD_FIELD_DEFINITIONS,
        "URS": URS_FIELD_DEFINITIONS,
        "VTQ": VTQ_FIELD_DEFINITIONS,
        "CSR": CSR_FIELD_DEFINITIONS,
        "CSS": CSS_FIELD_DEFINITIONS,
        "CTI": CTI_FIELD_DEFINITIONS,
        "DSP": DSP_FIELD_DEFINITIONS,
        "ECD": ECD_FIELD_DEFINITIONS,
        "ECR": ECR_FIELD_DEFINITIONS,
        "EDU": EDU_FIELD_DEFINITIONS,
        "EQL": EQL_FIELD_DEFINITIONS,
        "EQP": EQP_FIELD_DEFINITIONS,
        "EQU": EQU_FIELD_DEFINITIONS,
        "ERQ": ERQ_FIELD_DEFINITIONS,
        "ARV": ARV_FIELD_DEFINITIONS,
        "AUT": AUT_FIELD_DEFINITIONS,
        "BPO": BPO_FIELD_DEFINITIONS,
        "BPX": BPX_FIELD_DEFINITIONS,
        "BUI": BUI_FIELD_DEFINITIONS,
        "IAM": IAM_FIELD_DEFINITIONS,
        "IAR": IAR_FIELD_DEFINITIONS,
        "MFI": MFI_FIELD_DEFINITIONS,
        "MFE": MFE_FIELD_DEFINITIONS,
        "MFA": MFA_FIELD_DEFINITIONS,
        "OM1": OM1_FIELD_DEFINITIONS,
        "OM2": OM2_FIELD_DEFINITIONS,
        "OM3": OM3_FIELD_DEFINITIONS,
        "OM4": OM4_FIELD_DEFINITIONS,
        "OM5": OM5_FIELD_DEFINITIONS,
        "OM6": OM6_FIELD_DEFINITIONS,
        "PRB": PRB_FIELD_DEFINITIONS,
        "PRC": PRC_FIELD_DEFINITIONS,
        "PRD": PRD_FIELD_DEFINITIONS,
        "PSH": PSH_FIELD_DEFINITIONS,
        "PTH": PTH_FIELD_DEFINITIONS,
        "ODS": ODS_FIELD_DEFINITIONS,
        "ODT": ODT_FIELD_DEFINITIONS,
        "OMS": OMS_FIELD_DEFINITIONS,
        "ORG": ORG_FIELD_DEFINITIONS,
        "ORO": ORO_FIELD_DEFINITIONS,
        "OVR": OVR_FIELD_DEFINITIONS,
        "PCR": PCR_FIELD_DEFINITIONS,
        "PEO": PEO_FIELD_DEFINITIONS,
        "PE1": PE1_FIELD_DEFINITIONS,
        "PE2": PE2_FIELD_DEFINITIONS,
        "PES": PES_FIELD_DEFINITIONS,
        "IVT": IVT_FIELD_DEFINITIONS,
        "IVC": IVC_FIELD_DEFINITIONS,
        "IPR": IPR_FIELD_DEFINITIONS,
        "IVP": IVP_FIELD_DEFINITIONS,
        "ITM": ITM_FIELD_DEFINITIONS,
        "LDP": LDP_FIELD_DEFINITIONS,
        "LCC": LCC_FIELD_DEFINITIONS,
        "LCH": LCH_FIELD_DEFINITIONS,
        "LRL": LRL_FIELD_DEFINITIONS,
        "BLG": BLG_FIELD_DEFINITIONS,
        "LOC": LOC_FIELD_DEFINITIONS,
        "PCE": PCE_FIELD_DEFINITIONS,
        "PRT": PRT_FIELD_DEFINITIONS,
        "MDM": MDM_FIELD_DEFINITIONS,
        "SIU": SIU_FIELD_DEFINITIONS,
        "BAR": BAR_FIELD_DEFINITIONS,
        "RDE": RDE_FIELD_DEFINITIONS,
        "RDS": RDS_FIELD_DEFINITIONS,
        "RGV": RGV_FIELD_DEFINITIONS,
        "RAS": RAS_FIELD_DEFINITIONS,
        "RAR": RAR_FIELD_DEFINITIONS,
        "RER": RER_FIELD_DEFINITIONS,
        "RGR": RGR_FIELD_DEFINITIONS,
        "APR": APR_FIELD_DEFINITIONS,
        "ARQ": ARQ_FIELD_DEFINITIONS,
        "RRA": RRA_FIELD_DEFINITIONS,
        "RRD": RRD_FIELD_DEFINITIONS,
        "RRG": RRG_FIELD_DEFINITIONS,
        "RRE": RRE_FIELD_DEFINITIONS,
        "RRF": RRF_FIELD_DEFINITIONS,
        "RCL": RCL_FIELD_DEFINITIONS,
        "ROR": ROR_FIELD_DEFINITIONS,
        "CON": CON_FIELD_DEFINITIONS,
        "GP1": GP1_FIELD_DEFINITIONS,
        "GP2": GP2_FIELD_DEFINITIONS,
        "LAN": LAN_FIELD_DEFINITIONS,
        "QBP": QBP_FIELD_DEFINITIONS,
        "QRY": QRY_FIELD_DEFINITIONS,
        "RSP": RSP_FIELD_DEFINITIONS,
        "RTB": RTB_FIELD_DEFINITIONS,
        "QCN": QCN_FIELD_DEFINITIONS,
        "PV3": PV3_FIELD_DEFINITIONS,
        "ADD": ADD_FIELD_DEFINITIONS,
        "CER": CER_FIELD_DEFINITIONS,
        "NCK": NCK_FIELD_DEFINITIONS,
        "NDS": NDS_FIELD_DEFINITIONS,
        "NPU": NPU_FIELD_DEFINITIONS,
        "NSC": NSC_FIELD_DEFINITIONS,
        "NST": NST_FIELD_DEFINITIONS,
        "GOL": GOL_FIELD_DEFINITIONS,
        "IIM": IIM_FIELD_DEFINITIONS,
        "INV": INV_FIELD_DEFINITIONS,
        "IPC": IPC_FIELD_DEFINITIONS,
        "ISD": ISD_FIELD_DEFINITIONS,
        "OMD": OMD_FIELD_DEFINITIONS,
        "OMG": OMG_FIELD_DEFINITIONS,
        "OML": OML_FIELD_DEFINITIONS,
        "OMN": OMN_FIELD_DEFINITIONS,
        "OMP": OMP_FIELD_DEFINITIONS,
        "ORD": ORD_FIELD_DEFINITIONS,
        "ORF": ORF_FIELD_DEFINITIONS,
        "ORI": ORI_FIELD_DEFINITIONS,
        "ORL": ORL_FIELD_DEFINITIONS,
        "ORM": ORM_FIELD_DEFINITIONS,
        "ORN": ORN_FIELD_DEFINITIONS,
        "ORP": ORP_FIELD_DEFINITIONS,
        "ORR": ORR_FIELD_DEFINITIONS,
        "ORS": ORS_FIELD_DEFINITIONS,
        "ORU": ORU_FIELD_DEFINITIONS,
        "OSD": OSD_FIELD_DEFINITIONS,
        "OSP": OSP_FIELD_DEFINITIONS,
        "PEX": PEX_FIELD_DEFINITIONS,
        "PGL": PGL_FIELD_DEFINITIONS,
        "PIN": PIN_FIELD_DEFINITIONS,
        "STZ": STZ_FIELD_DEFINITIONS,
        "PMU": PMU_FIELD_DEFINITIONS,
        "PPG": PPG_FIELD_DEFINITIONS,
        "PPT": PPT_FIELD_DEFINITIONS,
        "PPV": PPV_FIELD_DEFINITIONS,
        "PTR": PTR_FIELD_DEFINITIONS,
        "QCK": QCK_FIELD_DEFINITIONS,
        "RCI": RCI_FIELD_DEFINITIONS,
        "RDR": RDR_FIELD_DEFINITIONS,
        "RDY": RDY_FIELD_DEFINITIONS,
        "REF": REF_FIELD_DEFINITIONS,
        "RPA": RPA_FIELD_DEFINITIONS,
        "RPI": RPI_FIELD_DEFINITIONS,
        "RPL": RPL_FIELD_DEFINITIONS,
        "RPR": RPR_FIELD_DEFINITIONS,
        "RQA": RQA_FIELD_DEFINITIONS,
        "RQC": RQC_FIELD_DEFINITIONS,
        "RQI": RQI_FIELD_DEFINITIONS,
        "RQP": RQP_FIELD_DEFINITIONS,
        "RQQ": RQQ_FIELD_DEFINITIONS,
        "RRI": RRI_FIELD_DEFINITIONS,
        "SQM": SQM_FIELD_DEFINITIONS,
        "SQR": SQR_FIELD_DEFINITIONS,
        "SRM": SRM_FIELD_DEFINITIONS,
        "SRR": SRR_FIELD_DEFINITIONS,
        "SSR": SSR_FIELD_DEFINITIONS,
        "SSU": SSU_FIELD_DEFINITIONS,
        "STC": STC_FIELD_DEFINITIONS,
        "TCU": TCU_FIELD_DEFINITIONS,
        "UDM": UDM_FIELD_DEFINITIONS,
    }
    
    if segment_name not in segment_defs:
        return {}
    
    fields = segment_defs[segment_name]
    
    # Apply version-specific overrides if needed
    if version:
        result = {}
        for field_index, field_def in fields.items():
            if version in field_def.version_specific:
                from copy import deepcopy
                result[field_index] = deepcopy(field_def)
                for key, value in field_def.version_specific[version].items():
                    setattr(result[field_index], key, value)
            else:
                result[field_index] = field_def
        logger.debug(f"get_segment_fields completed at {datetime.now().isoformat()}")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return result
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    logger.debug(f"get_segment_fields completed at {datetime.now().isoformat()}")
    return fields


# ============================================================================
# Verification and Completeness Utilities
# ============================================================================

def verify_segment_completeness(segment_name: str, expected_field_count: Optional[int] = None) -> Tuple[bool, List[str]]:
    """
    Verify completeness of a segment's field definitions.
    
    Checks if all expected fields are present and validates field definitions.
    
    Args:
        segment_name: Segment name to verify
        expected_field_count: Optional expected number of fields
        
    Returns:
        Tuple of (is_complete, list_of_issues)
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Verifying segment completeness: {segment_name}")
    
    issues = []
    fields = get_segment_fields(segment_name)
    
    if not fields:
        issues.append(f"Segment {segment_name} has no field definitions")
        logger.warning(f"[{current_time}] Segment {segment_name} verification failed: no fields")
        return False, issues
    
    # Check expected field count if provided
    if expected_field_count is not None:
        actual_count = len(fields)
        if actual_count != expected_field_count:
            issues.append(
                f"Field count mismatch: expected {expected_field_count}, found {actual_count}"
            )
    
    # Verify field definitions are valid
    for field_index, field_def in fields.items():
        if not isinstance(field_def, FieldDefinition):
            issues.append(f"Field {field_index} is not a FieldDefinition instance")
            continue
        
        # Check required attributes
        if field_def.field_index != field_index:
            issues.append(
                f"Field {field_index} has incorrect field_index: {field_def.field_index}"
            )
        
        if not field_def.field_name:
            issues.append(f"Field {field_index} missing field_name")
        

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        if not field_def.data_type:
            issues.append(f"Field {field_index} missing data_type")
    
    is_complete = len(issues) == 0
    if is_complete:
        logger.info(f"[{current_time}] Segment {segment_name} verification passed")
    else:
        logger.warning(f"[{current_time}] Segment {segment_name} verification found {len(issues)} issues")
    
    return is_complete, issues


def get_all_implemented_segments() -> List[str]:
    """
    Get list of all segments with field definitions implemented.
    
    Returns:
        List of segment names
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{current_time}] Retrieving list of implemented segments")
    
    # Get segments from get_field_definition function's segment_defs dict
    # We need to extract from the function's internal dict
    # Get all segments from get_segment_fields function's segment_defs dictionary
    # This ensures we include all segments that are actually implemented
    segment_defs = {
        "MSH", "PID", "EVN", "PV1", "OBR", "OBX", "NTE", "AL1", "DG1", "PR1",
        "ORC", "IN1", "IN2", "IN3", "NK1", "PD1", "PV2", "GT1", "MSA", "ERR",
        "QRD", "QRF", "QAK", "QPD", "RGS", "SPM", "TQ1", "TQ2", "RXR", "RXC",
        "RXA", "DSC", "UB1", "UB2", "ROL", "CTD", "ACC", "BHS", "BTS", "SCH",
        "TXA", "RCP", "RF1", "RMI", "AIS", "AIG", "AIL", "AIP", "DB1", "FAC",
        "STF", "FHS", "FTS", "RXD", "RXE", "RXG", "RXO", "RXP", "CDM", "DRG",
        "MRG", "QID", "QRI", "QSC", "RCD", "RDF", "RDT", "RQ1", "RQD", "RPT",
        "SAC", "SCD", "SCP", "SDD", "SID", "SLT", "SPR", "TCC", "TCD", "UAC",
        "VAR", "PDA", "FT1", "VXA", "VXU", "VXR", "VXQ", "VXX", "SFT", "CSR",
        "CSS", "CTI", "DSP", "ECD", "ECR", "EDU", "EQL", "EQP", "EQU", "ERQ",
        "ARV", "AUT", "BPO", "BPX", "BUI", "IAM", "IAR", "MFI", "MFE", "MFA",
        "OM1", "OM2", "OM3", "OM4", "OM5", "OM6", "OM7", "PRB", "PRC", "PRD", "PSH",
        "PTH", "ODS", "ODT", "OMS", "ORG", "ORO", "OVR", "PCR", "PEO", "PES",
        "IVT", "IVC", "IPR", "IVP", "ITM", "LDP", "LCC", "LCH", "LRL", "BLG", "LOC", "PCE", "PRT",
        "MDM", "SIU", "BAR", "RDE", "RDS", "RGV", "RAS", "RAR", "RER", "RGR",
        "APR", "ARQ", "RRA", "RRD", "RRG", "RRE", "RRF", "RCL", "ROR", "CON",
        "GP1", "GP2", "LAN", "QBP", "QRY", "RSP", "RTB", "QCN", "PV3",
        "ADD", "CER", "NCK", "NDS", "NPU", "NSC", "NST", "GOL", "IIM",
        "INV", "IPC", "ISD", "SAD", "SCV", "SPD", "SRT", "CM0", "CM1", "CM2",
        "ED", "RXV", "SN", "SPS", "IPR", "IVP",
        # Additional segments from HL7v2.9.1 standard
        "BLC", "CNS", "CSP", "PDC", "PE1", "PE2", "PEX", "STZ", "URD", "URS", "VTQ"
    }
    
    # Filter to only segments that actually have definitions
    implemented = []
    for seg in segment_defs:
        fields = get_segment_fields(seg)
        if fields:
            implemented.append(seg)
    
    # Add registered Z-segments
    implemented.extend(list_registered_z_segments())
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"[{completion_time}] Found {len(implemented)} implemented segments")
    logger.info(f"Current Time at End of Operations: {completion_time}")
    return sorted(implemented)


def get_segment_implementation_statistics() -> Dict[str, Any]:
    """
    Get statistics about segment field definition implementation.
    
    Returns:
        Dictionary with statistics including:
        - total_segments: Total number of segments with definitions
        - total_fields: Total number of fields across all segments
        - average_fields_per_segment: Average fields per segment
        - segments_by_field_count: Distribution of segments by field count
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Generating segment implementation statistics")
    
    segments = get_all_implemented_segments()
    total_fields = 0
    field_counts = []
    
    for seg in segments:
        fields = get_segment_fields(seg)
        field_count = len(fields)
        field_counts.append(field_count)
        total_fields += field_count
    
    # Calculate distribution
    from collections import Counter
    distribution = Counter(field_counts)
    
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log completion timestamp at end of operation
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    stats = {
        "total_segments": len(segments),
        "total_fields": total_fields,
        "average_fields_per_segment": total_fields / len(segments) if segments else 0,
        "segments_by_field_count": dict(distribution),
        "start_time": current_time,
        "completion_time": completion_time,
        "timestamp": completion_time
    }
    
    logger.info(f"[{completion_time}] Statistics generated: {stats['total_segments']} segments, {stats['total_fields']} total fields")
    logger.info(f"Current Time at End of Operations: {completion_time}")
    return stats


def verify_all_segments_completeness(timeout_seconds: int = 300) -> Dict[str, Any]:
    """
    Verify completeness of all implemented segments.
    
    Performs comprehensive verification of all segments with field definitions,
    checking for completeness, consistency, and proper structure.
    
    Args:
        timeout_seconds: Maximum time allowed for verification (default: 300 seconds = 5 minutes)
    
    Returns:
        Dictionary containing:
            - total_segments: Total number of segments verified
            - complete_segments: Number of segments passing verification
            - incomplete_segments: Number of segments with issues
            - segment_issues: Dictionary mapping segment names to lists of issues
            - timestamp: Completion timestamp
            - timeout_exceeded: Boolean indicating if timeout was exceeded
    
    Raises:
        TimeoutError: If verification exceeds timeout_seconds
    """
    import time as time_module
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting comprehensive segment completeness verification (timeout: {timeout_seconds}s)")
    start_time = time_module.time()
    start_datetime = datetime.now()
    
    segments = get_all_implemented_segments()
    complete_segments = []
    incomplete_segments = []
    segment_issues = {}
    timeout_exceeded = False
    
    for seg in segments:
        # Check timeout before processing each segment
        elapsed = time_module.time() - start_time
        if elapsed > timeout_seconds:
            timeout_exceeded = True
            logger.warning(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verification timeout exceeded after {elapsed:.2f}s")
            break
        
        is_complete, issues = verify_segment_completeness(seg)
        if is_complete:
            complete_segments.append(seg)
        else:
            incomplete_segments.append(seg)
            segment_issues[seg] = issues
    
    end_time = time_module.time()
    elapsed = end_time - start_time
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = {
        "total_segments": len(segments),
        "complete_segments": len(complete_segments),
        "incomplete_segments": len(incomplete_segments),
        "completeness_percentage": (len(complete_segments) / len(segments) * 100) if segments else 0,
        "segment_issues": segment_issues,
        "start_time": current_time,
        "completion_time": completion_time,
        "elapsed_seconds": elapsed,
        "timestamp": completion_time,
        "timeout_exceeded": timeout_exceeded,
        "segments_processed": len(complete_segments) + len(incomplete_segments)
    }
    
    if timeout_exceeded:
        logger.warning(f"[{completion_time}] Comprehensive segment verification timed out: "
                      f"{len(complete_segments) + len(incomplete_segments)}/{len(segments)} segments processed "
                      f"in {elapsed:.2f}s")
    else:
        logger.info(f"[{completion_time}] Comprehensive segment verification completed: "
                    f"{len(complete_segments)}/{len(segments)} segments complete "
                    f"({result['completeness_percentage']:.1f}%) in {elapsed:.2f}s")
    
    return result


# ============================================================================
# Common Z-Segment Definitions (Placeholder Registration)
# ============================================================================
# Z-segments are implementation-specific custom segments.
# These are placeholder definitions for common Z-segments (Z01-Z20).
# Actual implementations should register their own Z-segment definitions with
# specific field definitions as needed.

def _create_default_z_segment_fields() -> Dict[int, FieldDefinition]:
    """Create default field definitions for a generic Z-segment."""
    return {
        1: FieldDefinition(
            field_index=1,
            field_name="Custom Field 1",
            data_type="ST",
            length=250,
            description="Custom field 1 (implementation-specific)"
        ),
        2: FieldDefinition(
            field_index=2,
            field_name="Custom Field 2",
            data_type="ST",
            length=250,
            description="Custom field 2 (implementation-specific)"
        ),
    }


# ============================================================================
# SN Segment - Structured Numeric (HL7v2.9.1)
# ============================================================================

SN_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Comparator",
        data_type="ST",
        length=2,
        description="Comparator (<, <=, =, >=, >)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Num1",
        data_type="NM",
        length=16,
        description="First number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Separator/Suffix",
        data_type="ST",
        length=2,
        description="Separator/suffix"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Num2",
        data_type="NM",
        length=16,
        description="Second number"
    ),
}


# ============================================================================
# SPS Segment - Specimen Source (HL7v2.9.1)
# ============================================================================

SPS_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Specimen Source Name or Code",
        data_type="CE",
        length=250,
        description="Specimen source name or code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Additives",
        data_type="CE",
        length=250,
        description="Additives"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Freetext",
        data_type="ST",
        length=200,
        description="Freetext description"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Body Site",
        data_type="CE",
        length=250,
        description="Body site"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Site Modifier",
        data_type="CE",
        length=250,
        description="Site modifier"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Collection Method Modifier Code",
        data_type="CE",
        length=250,
        description="Collection method modifier code"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Specimen Role",
        data_type="CE",
        length=250,
        description="Specimen role"
    ),
}


# ============================================================================
# ADJ Segment - Adjustment (HL7v2.9.1)
# ============================================================================

ADJ_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Provider Adjustment Number",
        data_type="EI",
        length=30,
        description="Provider adjustment number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Payer Adjustment Number",
        data_type="EI",
        length=30,
        description="Payer adjustment number"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Adjustment Sequence Number",
        data_type="NM",
        length=4,
        required=True,
        description="Adjustment sequence number"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Adjustment Category",
        data_type="CE",
        length=250,
        table_binding="0456",
        required=True,
        description="Adjustment category"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Adjustment Amount",
        data_type="CP",
        length=12,
        description="Adjustment amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Adjustment Quantity",
        data_type="NM",
        length=6,
        description="Adjustment quantity"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Adjustment Reason Code",
        data_type="CE",
        length=250,
        table_binding="0457",
        description="Adjustment reason code"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Adjustment Description",
        data_type="ST",
        length=60,
        description="Adjustment description"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Original Value",
        data_type="CP",
        length=12,
        description="Original value"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Substitute Value",
        data_type="CP",
        length=12,
        description="Substitute value"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Adjustment Calculation Method",
        data_type="ST",
        length=10,
        description="Adjustment calculation method"
    ),
}


# ============================================================================
# AFF Segment - Professional Affiliation (HL7v2.9.1)
# ============================================================================

AFF_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - AFF",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Professional Organization",
        data_type="XON",
        length=250,
        required=True,
        description="Professional organization"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Professional Organization Address",
        data_type="XAD",
        length=250,
        description="Professional organization address"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Professional Organization Contact Person",
        data_type="XPN",
        length=250,
        description="Professional organization contact person"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Professional Organization Contact Phone",
        data_type="XTN",
        length=250,
        description="Professional organization contact phone"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Affiliated Organization",
        data_type="XON",
        length=250,
        description="Affiliated organization"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Affiliated Organization Address",
        data_type="XAD",
        length=250,
        description="Affiliated organization address"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Affiliated Organization Contact Person",
        data_type="XPN",
        length=250,
        description="Affiliated organization contact person"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Affiliated Organization Contact Phone",
        data_type="XTN",
        length=250,
        description="Affiliated organization contact phone"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Professional Organization Affiliation Date Range",
        data_type="DR",
        length=52,
        description="Professional organization affiliation date range"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Professional Affiliation Additional Information",
        data_type="ST",
        length=200,
        description="Professional affiliation additional information"
    ),
}


# ============================================================================
# BTX Segment - Blood Product Transfusion/Disposition (HL7v2.9.1)
# ============================================================================

BTX_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - BTX",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="BC Donation ID",
        data_type="EI",
        length=22,
        description="BC donation ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="BC Component",
        data_type="CNE",
        length=250,
        table_binding="0429",
        description="BC component"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="BC Blood Group",
        data_type="CNE",
        length=250,
        description="BC blood group"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="CP Commercial Product",
        data_type="CWE",
        length=250,
        table_binding="0426",
        description="CP commercial product"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="CP Manufacturer",
        data_type="XON",
        length=250,
        description="CP manufacturer"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="CP Lot Number",
        data_type="EI",
        length=22,
        description="CP lot number"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="BP Quantity",
        data_type="NM",
        length=10,
        description="BP quantity"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="BP Amount",
        data_type="NM",
        length=10,
        description="BP amount"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="BP Units",
        data_type="CE",
        length=250,
        description="BP units"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="BP Transfusion/Disposition Status",
        data_type="CWE",
        length=250,
        table_binding="0513",
        required=True,
        description="BP transfusion/disposition status"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="BP Message Status",
        data_type="ID",
        length=1,
        table_binding="0514",
        description="BP message status"
    ),
    13: FieldDefinition(
        field_index=13,
        field_name="BP Date/Time of Status",
        data_type="DTM",
        length=24,
        description="BP date/time of status"
    ),
    14: FieldDefinition(
        field_index=14,
        field_name="BP Transfusion Administrator",
        data_type="XCN",
        length=250,
        description="BP transfusion administrator"
    ),
    15: FieldDefinition(
        field_index=15,
        field_name="BP Transfusion Verifier",
        data_type="XCN",
        length=250,
        description="BP transfusion verifier"
    ),
    16: FieldDefinition(
        field_index=16,
        field_name="BP Transfusion Start Date/Time of Status",
        data_type="DTM",
        length=24,
        description="BP transfusion start date/time of status"
    ),
    17: FieldDefinition(
        field_index=17,
        field_name="BP Transfusion End Date/Time of Status",
        data_type="DTM",
        length=24,
        description="BP transfusion end date/time of status"
    ),
    18: FieldDefinition(
        field_index=18,
        field_name="BP Adverse Reaction Type",
        data_type="CWE",
        length=250,
        table_binding="0515",
        description="BP adverse reaction type"
    ),
    19: FieldDefinition(
        field_index=19,
        field_name="BP Transfusion Interrupted Reason",
        data_type="CWE",
        length=250,
        table_binding="0516",
        description="BP transfusion interrupted reason"
    ),
}


# ============================================================================
# DMI Segment - DRG Master File Information (HL7v2.9.1)
# ============================================================================

DMI_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Diagnostic Related Group (DRG)",
        data_type="CWE",
        length=250,
        table_binding="0229",
        required=True,
        description="Diagnostic related group (DRG)"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="DRG Assigned Date/Time",
        data_type="DTM",
        length=24,
        description="DRG assigned date/time"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="DRG Approval Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="DRG approval indicator"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="DRG Grouper Review Code",
        data_type="CWE",
        length=250,
        table_binding="0428",
        description="DRG grouper review code"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Outlier Type",
        data_type="CWE",
        length=250,
        table_binding="0083",
        description="Outlier type"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Outlier Days",
        data_type="NM",
        length=3,
        description="Outlier days"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Outlier Cost",
        data_type="CP",
        length=12,
        description="Outlier cost"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="DRG Payor",
        data_type="CWE",
        length=250,
        table_binding="0229",
        description="DRG payor"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Outlier Reimbursement",
        data_type="CP",
        length=12,
        description="Outlier reimbursement"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Confidential Indicator",
        data_type="ID",
        length=1,
        table_binding="0136",
        description="Confidential indicator"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="DRG Transfer Type",
        data_type="CWE",
        length=250,
        table_binding="0415",
        description="DRG transfer type"
    ),
}


# ============================================================================
# DON Segment - Donation (HL7v2.9.1)
# ============================================================================

DON_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Donation ID",
        data_type="EI",
        length=22,
        required=True,
        description="Donation ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Donation Type",
        data_type="CWE",
        length=250,
        table_binding="0425",
        description="Donation type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Donation Date/Time",
        data_type="DTM",
        length=24,
        description="Donation date/time"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Expiration Date",
        data_type="DTM",
        length=24,
        description="Expiration date"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Donation Quantity",
        data_type="NM",
        length=10,
        description="Donation quantity"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Donation Quantity Units",
        data_type="CE",
        length=250,
        description="Donation quantity units"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Donation Intended Use Date/Time",
        data_type="DTM",
        length=24,
        description="Donation intended use date/time"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Donation Intended Use",
        data_type="CWE",
        length=250,
        table_binding="0426",
        description="Donation intended use"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Donation Intended Use Text",
        data_type="ST",
        length=200,
        description="Donation intended use text"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Donation Processing Status",
        data_type="CWE",
        length=250,
        table_binding="0427",
        description="Donation processing status"
    ),
}


# ============================================================================
# PMT Segment - Payment Information (HL7v2.9.1)
# ============================================================================

PMT_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Payment/Remit Advice Unique Identifier",
        data_type="EI",
        length=30,
        required=True,
        description="Payment/remit advice unique identifier"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Payment/Remit Advice Effective Date",
        data_type="DTM",
        length=24,
        required=True,
        description="Payment/remit advice effective date"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Payment/Remit Advice Expiration Date",
        data_type="DTM",
        length=24,
        description="Payment/remit advice expiration date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Payment Method",
        data_type="CWE",
        length=250,
        table_binding="0170",
        required=True,
        description="Payment method"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Payment/Remit Advice Amount",
        data_type="CP",
        length=12,
        required=True,
        description="Payment/remit advice amount"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Check Number",
        data_type="ST",
        length=30,
        description="Check number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Payee Payee Organization Name",
        data_type="XON",
        length=250,
        description="Payee payee organization name"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Payee Payee Organization Address",
        data_type="XAD",
        length=250,
        description="Payee payee organization address"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Payee Payee Organization Contact Person",
        data_type="XCN",
        length=250,
        description="Payee payee organization contact person"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Payee Payee Organization Contact Phone",
        data_type="XTN",
        length=250,
        description="Payee payee organization contact phone"
    ),
}


# ============================================================================
# RBC Segment - Result Blood Component (HL7v2.9.1)
# ============================================================================

RBC_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Donation ID",
        data_type="EI",
        length=22,
        required=True,
        description="Donation ID"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Product Code",
        data_type="CWE",
        length=250,
        table_binding="0426",
        required=True,
        description="Product code"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Product Expiration Date",
        data_type="DTM",
        length=24,
        description="Product expiration date"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Product Status",
        data_type="CWE",
        length=250,
        table_binding="0512",
        description="Product status"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Product Lot Number",
        data_type="EI",
        length=22,
        description="Product lot number"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Blood Product Group",
        data_type="CWE",
        length=250,
        description="Blood product group"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Blood Product Rh",
        data_type="CWE",
        length=250,
        description="Blood product Rh"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Blood Product ABO",
        data_type="CWE",
        length=250,
        description="Blood product ABO"
    ),
}


# ============================================================================
# REL Segment - Clinical Relationship (HL7v2.9.1)
# ============================================================================

REL_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Set ID - REL",
        data_type="SI",
        length=4,
        required=True,
        description="Sequence number"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Relationship Type",
        data_type="CWE",
        length=250,
        table_binding="0503",
        required=True,
        description="Relationship type"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="This Person Identifier",
        data_type="XPN",
        length=250,
        required=True,
        description="This person identifier"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="This Person Relationship Role",
        data_type="CWE",
        length=250,
        table_binding="0504",
        description="This person relationship role"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="This Person Relationship Begin Date",
        data_type="DT",
        length=8,
        description="This person relationship begin date"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="This Person Relationship End Date",
        data_type="DT",
        length=8,
        description="This person relationship end date"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Related Person Identifier",
        data_type="XPN",
        length=250,
        description="Related person identifier"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Related Person Relationship Role",
        data_type="CWE",
        length=250,
        table_binding="0504",
        description="Related person relationship role"
    ),
    9: FieldDefinition(
        field_index=9,
        field_name="Related Person Relationship Begin Date",
        data_type="DT",
        length=8,
        description="Related person relationship begin date"
    ),
    10: FieldDefinition(
        field_index=10,
        field_name="Related Person Relationship End Date",
        data_type="DT",
        length=8,
        description="Related person relationship end date"
    ),
    11: FieldDefinition(
        field_index=11,
        field_name="Relationship Priority",
        data_type="ID",
        length=1,
        table_binding="0517",
        description="Relationship priority"
    ),
    12: FieldDefinition(
        field_index=12,
        field_name="Relationship Status",
        data_type="CWE",
        length=250,
        table_binding="0505",
        description="Relationship status"
    ),
}


# ============================================================================
# RRO Segment - Request/Response Information (HL7v2.9.1)
# ============================================================================

RRO_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Anticipated Price",
        data_type="MO",
        length=20,
        description="Anticipated price"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Manufactured ID",
        data_type="CWE",
        length=250,
        description="Manufactured ID"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Manufacturer's Catalog",
        data_type="ST",
        length=60,
        description="Manufacturer's catalog"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Vendor ID",
        data_type="CWE",
        length=250,
        description="Vendor ID"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Vendor Catalog",
        data_type="ST",
        length=60,
        description="Vendor catalog"
    ),
    6: FieldDefinition(
        field_index=6,
        field_name="Vendor Order Number",
        data_type="ST",
        length=60,
        description="Vendor order number"
    ),
    7: FieldDefinition(
        field_index=7,
        field_name="Vendor Order Status",
        data_type="CWE",
        length=250,
        table_binding="0518",
        description="Vendor order status"
    ),
    8: FieldDefinition(
        field_index=8,
        field_name="Shipping Date/Time",
        data_type="DTM",
        length=24,
        description="Shipping date/time"
    ),
}


# ============================================================================
# RXX Segment - Pharmacy/Treatment Route Segment (HL7v2.9.1)
# ============================================================================

RXX_FIELD_DEFINITIONS: Dict[int, FieldDefinition] = {
    1: FieldDefinition(
        field_index=1,
        field_name="Route Code",
        data_type="CWE",
        length=250,
        table_binding="0162",
        required=True,
        description="Route code"
    ),
    2: FieldDefinition(
        field_index=2,
        field_name="Administration Site",
        data_type="CWE",
        length=250,
        table_binding="0163",
        description="Administration site"
    ),
    3: FieldDefinition(
        field_index=3,
        field_name="Administration Device",
        data_type="CWE",
        length=250,
        table_binding="0164",
        description="Administration device"
    ),
    4: FieldDefinition(
        field_index=4,
        field_name="Administration Method",
        data_type="CWE",
        length=250,
        table_binding="0165",
        description="Administration method"
    ),
    5: FieldDefinition(
        field_index=5,
        field_name="Routing Instruction",
        data_type="CWE",
        length=250,
        description="Routing instruction"
    ),
}


# Register common Z-segments (Z01-Z30) with default definitions at module load
# These are placeholders - actual implementations should override with specific definitions
# Log completion timestamp at end of operation
_current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"[{_current_time}] Registering common Z-segments (Z01-Z30) with default definitions")
for z_num in range(1, 31):
    z_seg_name = f"Z{z_num:02d}"
    try:
        register_z_segment(z_seg_name, _create_default_z_segment_fields())
    except Exception as e:
        # Segment may already be registered, which is fine
        logger.debug(f"Z-segment {z_seg_name} registration: {e}")

logger.info(f"[{_current_time}] Z-segment registration completed. Current Time at End of Operations: {_current_time}")
