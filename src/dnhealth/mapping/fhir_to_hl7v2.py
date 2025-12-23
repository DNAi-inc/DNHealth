# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 to HL7v2 mapping utilities.

Provides functions to convert FHIR R4 resources to HL7v2 messages.
"""

import logging
from datetime import datetime
from typing import List, Optional
from time import time

from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.servicerequest import ServiceRequest
from dnhealth.dnhealth_fhir.resources.documentreference import DocumentReference
from dnhealth.dnhealth_hl7v2.model import Message, Segment, Field, Component, Subcomponent, EncodingCharacters

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def convert_patient_to_adt(
    patient: Patient,
    message_type: str = "A08",    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR Patient resource to HL7v2 ADT message.
    
    Maps FHIR Patient fields to HL7v2 ADT message segments:
    - Patient.identifier -> PID-3 (Patient Identifier List)
    - Patient.name -> PID-5 (Patient Name)
    - Patient.birthDate -> PID-7 (Date/Time of Birth)
    - Patient.gender -> PID-8 (Administrative Sex)
    - Patient.address -> PID-11 (Patient Address)
    - Patient.telecom -> PID-13 (Phone Number - Home)
    
    Args:
        patient: FHIR Patient resource
        message_type: ADT message type (default: A08 - Update patient information)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v2 ADT message
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting Patient to ADT conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    encoding_chars = EncodingCharacters()
    segments: List[Segment] = []
    
    # Create MSH segment
    msh = _create_msh_segment(message_type, encoding_chars)
    segments.append(msh)
    
    # Create EVN segment
    evn = _create_evn_segment(encoding_chars)
    segments.append(evn)
    
    # Create PID segment
    pid = _create_pid_segment_from_patient(patient, encoding_chars)
    segments.append(pid)
    
    # Create message
    message = Message(
        segments=segments,
        encoding_chars=encoding_chars,
        version="2.5"  # Default version
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] Patient to ADT conversion completed in {elapsed:.2f} seconds")
    
    return message


def convert_encounter_to_adt(
    encounter: Encounter,
    message_type: str = "A02",
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR Encounter resource to HL7v2 ADT message.
    
    Maps FHIR Encounter fields to HL7v2 ADT message segments:
    - Encounter.identifier -> PV1-19 (Visit Number)
    - Encounter.class_ -> PV1-2 (Patient Class)
    - Encounter.period -> PV1-44 (Admit Date/Time), PV1-45 (Discharge Date/Time)
    - Encounter.type -> PV1-10 (Hospital Service)
    
    Args:
        encounter: FHIR Encounter resource
        message_type: ADT message type (default: A02 - Transfer a patient)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v2 ADT message
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting Encounter to ADT conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    encoding_chars = EncodingCharacters()
    segments: List[Segment] = []
    
    # Create MSH segment
    msh = _create_msh_segment(message_type, encoding_chars)
    segments.append(msh)
    
    # Create EVN segment
    evn = _create_evn_segment(encoding_chars)
    segments.append(evn)
    
    # Create PV1 segment
    pv1 = _create_pv1_segment_from_encounter(encounter, encoding_chars)
    segments.append(pv1)
    
    # Create message
    message = Message(
        segments=segments,
        encoding_chars=encoding_chars,
        version="2.5"  # Default version
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] Encounter to ADT conversion completed in {elapsed:.2f} seconds")
    
    return message


def convert_observation_to_oru(
    observations: List[Observation],
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR Observation resources to HL7v2 ORU message.
    
    Maps FHIR Observation fields to HL7v2 ORU message segments:
    - Observation.code -> OBX-3 (Observation Identifier)
    - Observation.value[x] -> OBX-5 (Observation Value)
    - Observation.status -> OBX-11 (Observation Result Status)
    - Observation.effectiveDateTime -> OBX-14 (Date/Time of the Observation)
    
    Args:
        observations: List of FHIR Observation resources
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v2 ORU message
        
    Raises:
        ValueError: If conversion exceeds timeout or no observations provided
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting Observation to ORU conversion")
    
    if not observations:
        raise ValueError("At least one Observation resource is required")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    encoding_chars = EncodingCharacters()
    segments: List[Segment] = []
    
    # Create MSH segment
    msh = _create_msh_segment("R01", encoding_chars)  # ORU message type
    segments.append(msh)
    
    # Create PID segment (from first observation's subject if available)
    if observations and observations[0].subject:
        # Simplified - would need to fetch patient data
        pid = _create_pid_segment_minimal(encoding_chars)
        segments.append(pid)
    
    # Create OBR segment (simplified)
    obr = _create_obr_segment_minimal(encoding_chars)
    segments.append(obr)
    
    # Create OBX segments for each observation
    for obs in observations:
        obx = _create_obx_segment_from_observation(obs, encoding_chars)
        segments.append(obx)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create message
    message = Message(
        segments=segments,
        encoding_chars=encoding_chars,
        version="2.5"  # Default version
    )
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] Observation to ORU conversion completed in {elapsed:.2f} seconds: {len(observations)} observations")
    
    return message


def convert_servicerequest_to_orm(
    service_requests: List[ServiceRequest],
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR ServiceRequest resources to HL7v2 ORM message.
    
    Maps FHIR ServiceRequest fields to HL7v2 ORM message segments:
    - ServiceRequest.identifier -> OBR-2 (Placer Order Number), OBR-3 (Filler Order Number)
    - ServiceRequest.code -> OBR-4 (Universal Service Identifier)
    - ServiceRequest.authoredOn -> OBR-6 (Requested Date/Time)
    
    Args:
        service_requests: List of FHIR ServiceRequest resources
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v2 ORM message
        
    Raises:
        ValueError: If conversion exceeds timeout or no service requests provided
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ServiceRequest to ORM conversion")
    
    if not service_requests:
        raise ValueError("At least one ServiceRequest resource is required")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    encoding_chars = EncodingCharacters()
    segments: List[Segment] = []
    
    # Create MSH segment
    msh = _create_msh_segment("O01", encoding_chars)  # ORM message type
    segments.append(msh)
    
    # Create PID segment (from first service request's subject if available)
    if service_requests and service_requests[0].subject:
        pid = _create_pid_segment_minimal(encoding_chars)
        segments.append(pid)
    
    # Create OBR segments for each service request
    for sr in service_requests:
        obr = _create_obr_segment_from_servicerequest(sr, encoding_chars)
        segments.append(obr)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create message
    message = Message(
        segments=segments,
        encoding_chars=encoding_chars,
        version="2.5"  # Default version
    )
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] ServiceRequest to ORM conversion completed in {elapsed:.2f} seconds: {len(service_requests)} service requests")
    
    return message


def convert_documentreference_to_mdm(
    document_reference: DocumentReference,
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR DocumentReference resource to HL7v2 MDM message.
    
    Maps FHIR DocumentReference fields to HL7v2 MDM message segments:
    - DocumentReference.type -> TXA-2 (Document Type)
    - DocumentReference.date -> TXA-4 (Activity Date/Time)
    - DocumentReference.identifier -> TXA-12 (Unique Document Number)
    
    Args:
        document_reference: FHIR DocumentReference resource
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v2 MDM message
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting DocumentReference to MDM conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    encoding_chars = EncodingCharacters()
    segments: List[Segment] = []
    
    # Create MSH segment
    msh = _create_msh_segment("T02", encoding_chars)  # MDM message type
    segments.append(msh)
    
    # Create TXA segment
    txa = _create_txa_segment_from_documentreference(document_reference, encoding_chars)
    segments.append(txa)
    
    # Create message
    message = Message(
        segments=segments,
        encoding_chars=encoding_chars,
        version="2.5"  # Default version
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] DocumentReference to MDM conversion completed in {elapsed:.2f} seconds")
    
    return message


# Helper functions for creating segments

def _create_msh_segment(message_type: str, encoding_chars: EncodingCharacters) -> Segment:
    """Create MSH segment."""
    from datetime import datetime
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    
    fields = [
        [Field([Component([Subcomponent("MSH")])])],  # MSH-1: Field Separator (implicit)
        [Field([Component([Subcomponent(encoding_chars.component_separator + encoding_chars.repetition_separator + encoding_chars.escape_character + encoding_chars.subcomponent_separator)])])],  # MSH-2: Encoding Characters
        [Field([Component([Subcomponent("SendingApp")])])],  # MSH-3: Sending Application
        [Field([Component([Subcomponent("SendingFacility")])])],  # MSH-4: Sending Facility
        [Field([Component([Subcomponent("ReceivingApp")])])],  # MSH-5: Receiving Application
        [Field([Component([Subcomponent("ReceivingFacility")])])],  # MSH-6: Receiving Facility
        [Field([Component([Subcomponent(timestamp)])])],  # MSH-7: Date/Time of Message
        [Field()],  # MSH-8: Security
        [Field([Component([Subcomponent(message_type)])])],  # MSH-9: Message Type
        [Field([Component([Subcomponent("1")])])],  # MSH-10: Message Control ID
        [Field([Component([Subcomponent("P")])])],  # MSH-11: Processing ID
        [Field([Component([Subcomponent("2.5")])])],  # MSH-12: Version ID
    ]
    
    return Segment("MSH", field_repetitions=fields)


def _create_evn_segment(encoding_chars: EncodingCharacters) -> Segment:
    """Create EVN segment."""
    from datetime import datetime
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    
    fields = [
        [Field([Component([Subcomponent("A08")])])],  # EVN-1: Event Type Code
        [Field([Component([Subcomponent(timestamp)])])],  # EVN-2: Recorded Date/Time
    ]
    
    return Segment("EVN", field_repetitions=fields)


def _create_pid_segment_from_patient(patient: Patient, encoding_chars: EncodingCharacters) -> Segment:
    """Create PID segment from Patient resource."""
    fields = []
    
    # PID-3: Patient Identifier List
    if patient.identifier:
        id_fields = []
        for identifier in patient.identifier:
            comp = Component([
                Subcomponent(identifier.value if identifier.value else ""),
                Subcomponent(""),  # Check Digit
                Subcomponent(""),  # Check Digit Scheme
                Subcomponent(identifier.system if identifier.system else ""),  # Assigning Authority
                Subcomponent("MR"),  # ID Type
            ])
            id_fields.append(Field([comp]))
        fields.append(id_fields)
    else:
        fields.append([Field()])
    
    # PID-5: Patient Name
    if patient.name:
        name_fields = []
        for name in patient.name:
            comp = Component([
                Subcomponent(name.family if name.family else ""),
                Subcomponent(name.given[0] if name.given and len(name.given) > 0 else ""),
                Subcomponent(name.given[1] if name.given and len(name.given) > 1 else ""),
                Subcomponent(name.suffix[0] if name.suffix and len(name.suffix) > 0 else ""),
                Subcomponent(name.prefix[0] if name.prefix and len(name.prefix) > 0 else ""),
            ])
            name_fields.append(Field([comp]))
        fields.append(name_fields)
    else:
        fields.append([Field()])
    
    # PID-7: Date/Time of Birth
    if patient.birthDate:
        # Convert FHIR date (YYYY-MM-DD) to HL7v2 date (YYYYMMDD)
        birth_date = patient.birthDate.replace("-", "")
        fields.append([Field([Component([Subcomponent(birth_date)])])])
    else:
        fields.append([Field()])
    
    # PID-8: Administrative Sex
    if patient.gender:
        # Map FHIR gender to HL7v2 gender codes
        gender_map = {
            "male": "M",
            "female": "F",
            "other": "O",
            "unknown": "U",
        }
        gender_code = gender_map.get(patient.gender.lower(), "U")
        fields.append([Field([Component([Subcomponent(gender_code)])])])
    else:
        fields.append([Field()])
    
    # Add empty fields for remaining PID fields (simplified)
    while len(fields) < 18:
        fields.append([Field()])
    
    return Segment("PID", field_repetitions=fields)


def _create_pid_segment_minimal(encoding_chars: EncodingCharacters) -> Segment:
    """Create minimal PID segment."""
    fields = [[Field()] for _ in range(18)]
    return Segment("PID", field_repetitions=fields)


def _create_pv1_segment_from_encounter(encounter: Encounter, encoding_chars: EncodingCharacters) -> Segment:
    """Create PV1 segment from Encounter resource."""
    fields = []
    
    # PV1-2: Patient Class
    if encounter.class_ and encounter.class_.coding:
        class_code = encounter.class_.coding[0].code if encounter.class_.coding[0].code else ""
        fields.append([Field([Component([Subcomponent(class_code)])])])
    else:
        fields.append([Field()])
    
    # Add empty fields for remaining PV1 fields (simplified)
    while len(fields) < 45:
        fields.append([Field()])
    
    # PV1-19: Visit Number
    if encounter.identifier:
        visit_id = encounter.identifier[0].value if encounter.identifier[0].value else ""
        if len(fields) >= 19:
            fields[18] = [Field([Component([Subcomponent(visit_id)])])]
    
    # PV1-44: Admit Date/Time
    if encounter.period and encounter.period.start:
        admit_dt = _convert_fhir_datetime_to_hl7v2(encounter.period.start)
        if len(fields) >= 44:
            fields[43] = [Field([Component([Subcomponent(admit_dt)])])]
    
    # PV1-45: Discharge Date/Time
    if encounter.period and encounter.period.end:
        discharge_dt = _convert_fhir_datetime_to_hl7v2(encounter.period.end)
        if len(fields) >= 45:
            fields[44] = [Field([Component([Subcomponent(discharge_dt)])])]
    
    return Segment("PV1", field_repetitions=fields)


def _create_obr_segment_minimal(encoding_chars: EncodingCharacters) -> Segment:
    """Create minimal OBR segment."""
    fields = [[Field()] for _ in range(50)]
    return Segment("OBR", field_repetitions=fields)


def _create_obr_segment_from_servicerequest(sr: ServiceRequest, encoding_chars: EncodingCharacters) -> Segment:
    """Create OBR segment from ServiceRequest resource."""
    fields = []
    
    # OBR-2: Placer Order Number
    if sr.identifier:
        placer_id = sr.identifier[0].value if sr.identifier[0].value else ""
        fields.append([Field([Component([Subcomponent(placer_id)])])])
    else:
        fields.append([Field()])
    
    # OBR-4: Universal Service Identifier
    if sr.code and sr.code.coding:
        code = sr.code.coding[0].code if sr.code.coding[0].code else ""
        display = sr.code.coding[0].display if sr.code.coding[0].display else ""
        system = sr.code.coding[0].system if sr.code.coding[0].system else ""
        comp = Component([
            Subcomponent(code),
            Subcomponent(display),
            Subcomponent(system),
        ])
        fields.append([Field()])  # OBR-3
        fields.append([Field([comp])])
    else:
        fields.append([Field()])  # OBR-3
        fields.append([Field()])
    
    # OBR-6: Requested Date/Time
    if sr.authoredOn:
        authored_dt = _convert_fhir_datetime_to_hl7v2(sr.authoredOn)
        while len(fields) < 6:
            fields.append([Field()])
        fields[5] = [Field([Component([Subcomponent(authored_dt)])])]
    
    # Add empty fields for remaining OBR fields (simplified)
    while len(fields) < 50:
        fields.append([Field()])
    
    return Segment("OBR", field_repetitions=fields)


def _create_obx_segment_from_observation(obs: Observation, encoding_chars: EncodingCharacters) -> Segment:
    """Create OBX segment from Observation resource."""
    fields = []
    
    # OBX-3: Observation Identifier
    if obs.code and obs.code.coding:
        code = obs.code.coding[0].code if obs.code.coding[0].code else ""
        display = obs.code.coding[0].display if obs.code.coding[0].display else ""
        system = obs.code.coding[0].system if obs.code.coding[0].system else ""
        comp = Component([
            Subcomponent(code),
            Subcomponent(display),
            Subcomponent(system),
        ])
        fields.append([Field()])  # OBX-1
        fields.append([Field()])  # OBX-2
        fields.append([Field([comp])])
    else:
        fields.append([Field()])  # OBX-1
        fields.append([Field()])  # OBX-2
        fields.append([Field()])
    
    # OBX-5: Observation Value
    if obs.valueString:
        fields.append([Field()])  # OBX-4
        fields.append([Field([Component([Subcomponent(obs.valueString)])])])
    else:
        fields.append([Field()])  # OBX-4
        fields.append([Field()])
    
    # OBX-11: Observation Result Status
    status_map = {
        "registered": "P",
        "preliminary": "P",
        "final": "F",
        "amended": "C",
        "corrected": "C",
        "cancelled": "X",
        "entered-in-error": "I",
        "unknown": "P",
    }
    status_code = status_map.get(obs.status.lower(), "F")
    while len(fields) < 11:
        fields.append([Field()])
    fields[10] = [Field([Component([Subcomponent(status_code)])])]
    
    # OBX-14: Date/Time of the Observation
    if obs.effectiveDateTime:
        effective_dt = _convert_fhir_datetime_to_hl7v2(obs.effectiveDateTime)
        while len(fields) < 14:
            fields.append([Field()])
        fields[13] = [Field([Component([Subcomponent(effective_dt)])])]
    
    # Add empty fields for remaining OBX fields (simplified)
    while len(fields) < 20:
        fields.append([Field()])
    
    return Segment("OBX", field_repetitions=fields)


def _create_txa_segment_from_documentreference(dr: DocumentReference, encoding_chars: EncodingCharacters) -> Segment:
    """Create TXA segment from DocumentReference resource."""
    fields = []
    
    # TXA-2: Document Type
    if dr.type_ and dr.type_.coding:
        code = dr.type_.coding[0].code if dr.type_.coding[0].code else ""
        display = dr.type_.coding[0].display if dr.type_.coding[0].display else ""
        system = dr.type_.coding[0].system if dr.type_.coding[0].system else ""
        comp = Component([
            Subcomponent(code),
            Subcomponent(display),
            Subcomponent(system),
        ])
        fields.append([Field()])  # TXA-1
        fields.append([Field([comp])])
    else:
        fields.append([Field()])  # TXA-1
        fields.append([Field()])
    
    # TXA-4: Activity Date/Time
    if dr.date:
        activity_dt = _convert_fhir_datetime_to_hl7v2(dr.date)
        while len(fields) < 4:
            fields.append([Field()])
        fields[3] = [Field([Component([Subcomponent(activity_dt)])])]
    
    # TXA-12: Unique Document Number
    if dr.identifier:
        doc_id = dr.identifier[0].value if dr.identifier[0].value else ""
        while len(fields) < 12:
            fields.append([Field()])
        fields[11] = [Field([Component([Subcomponent(doc_id)])])]
    
    # Add empty fields for remaining TXA fields (simplified)
    while len(fields) < 20:
        fields.append([Field()])
    
    return Segment("TXA", field_repetitions=fields)


def _convert_fhir_datetime_to_hl7v2(datetime_str: str) -> str:
    """
    Convert FHIR datetime format to HL7v2 datetime format.
    
    FHIR datetime format: YYYY-MM-DDThh:mm:ss[.sss][+/-zz:zz] or YYYY-MM-DDThh:mm:ss[.sss]Z
    HL7v2 datetime format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
    
    Args:
        datetime_str: FHIR datetime string
        
    Returns:
        HL7v2 datetime string
    """
    if not datetime_str:
        return ""
    
    # Remove any whitespace
    datetime_str = datetime_str.strip()
    
    # Remove 'T' separator
    datetime_str = datetime_str.replace("T", "")
    
    # Remove '-' from date part
    datetime_str = datetime_str.replace("-", "")
    
    # Remove ':' from time part
    datetime_str = datetime_str.replace(":", "")
    
    # Handle timezone
    if datetime_str.endswith("Z"):
        datetime_str = datetime_str[:-1] + "+0000"
    elif "+" in datetime_str or "-" in datetime_str:
        # Find timezone position
        tz_pos = max(datetime_str.rfind("+"), datetime_str.rfind("-"))
        if tz_pos > 0:
            # Remove ':' from timezone if present
            tz_part = datetime_str[tz_pos:]
            datetime_str = datetime_str[:tz_pos] + tz_part.replace(":", "")
    
    return datetime_str
