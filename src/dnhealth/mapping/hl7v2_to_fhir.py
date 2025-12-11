# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7v2 to FHIR R4 mapping utilities.

Provides functions to convert HL7v2 messages to FHIR R4 resources.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from time import time

from dnhealth.dnhealth_hl7v2.model import Message, Segment
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.servicerequest import ServiceRequest
from dnhealth.dnhealth_fhir.resources.documentreference import DocumentReference
from dnhealth.dnhealth_fhir.types import (
    Identifier,
    HumanName,
    ContactPoint,
    Address,
    Reference,
    CodeableConcept,
    Coding,
    Period,
    Quantity,
)

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def convert_adt_to_patient(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> Patient:
    """
    Convert HL7v2 ADT message to FHIR Patient resource.
    
    Maps PID segment fields to FHIR Patient resource fields:
    - PID-3 (Patient Identifier List) -> Patient.identifier
    - PID-5 (Patient Name) -> Patient.name
    - PID-7 (Date/Time of Birth) -> Patient.birthDate
    - PID-8 (Administrative Sex) -> Patient.gender
    - PID-11 (Patient Address) -> Patient.address
    - PID-13 (Phone Number - Home) -> Patient.telecom
    - PID-18 (Patient Account Number) -> Patient.identifier
    
    Args:
        message: HL7v2 ADT message (must contain PID segment)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        FHIR Patient resource
        
    Raises:
        ValueError: If message doesn't contain PID segment or conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT to Patient conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Find PID segment
    pid_segments = message.get_segments("PID")
    if not pid_segments:
        raise ValueError("ADT message must contain PID segment")
    
    pid = pid_segments[0]
    
    # Extract identifiers (PID-3: Patient Identifier List)
    identifiers: List[Identifier] = []
    pid3_field = pid.field(3)
    if pid3_field and pid3_field.value():
        # PID-3 format: ID^CheckDigit^CheckDigitScheme^AssigningAuthority^IDType^AssigningFacility
        for repetition in pid3_field.repetitions():
            if repetition and repetition.components:
                comp1 = repetition.component(1).value() if repetition.component(1) else None  # ID
                comp4 = repetition.component(4).value() if repetition.component(4) else None  # Assigning Authority
                comp5 = repetition.component(5).value() if repetition.component(5) else None  # ID Type
                
                if comp1:
                    identifier = Identifier(
                        use="usual" if comp5 == "MR" else "official",
                        system=comp4 if comp4 else None,
                        value=comp1,
                        type_=CodeableConcept(
                            coding=[Coding(
                                system="http://terminology.hl7.org/CodeSystem/v2-0203",
                                code=comp5 if comp5 else "MR",
                                display=comp5 if comp5 else "Medical Record Number"
                            )] if comp5 else []
                        ) if comp5 else None
                    )
                    identifiers.append(identifier)
    
    # Extract patient account number (PID-18)
    pid18_field = pid.field(18)
    if pid18_field and pid18_field.value():
        account_id = Identifier(
            use="usual",
            value=pid18_field.value(),
            type_=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="AN",
                    display="Account Number"
                )]
            )
        )
        identifiers.append(account_id)
    
    # Extract name (PID-5: Patient Name)
    names: List[HumanName] = []
    pid5_field = pid.field(5)
    if pid5_field and pid5_field.value():
        # PID-5 format: FamilyName^GivenName^MiddleName^Suffix^Prefix^Degree
        for repetition in pid5_field.repetitions():
            if repetition and repetition.components:
                comp1 = repetition.component(1).value() if repetition.component(1) else None  # Family
                comp2 = repetition.component(2).value() if repetition.component(2) else None  # Given
                comp3 = repetition.component(3).value() if repetition.component(3) else None  # Middle
                comp4 = repetition.component(4).value() if repetition.component(4) else None  # Suffix
                comp5 = repetition.component(5).value() if repetition.component(5) else None  # Prefix
                
                given_names = []
                if comp2:
                    given_names.append(comp2)
                if comp3:
                    given_names.append(comp3)
                
                name = HumanName(
                    use="official",
                    family=comp1 if comp1 else None,
                    given=given_names if given_names else None,
                    prefix=[comp5] if comp5 else None,
                    suffix=[comp4] if comp4 else None
                )
                names.append(name)
    
    # Extract birth date (PID-7: Date/Time of Birth)
    birth_date: Optional[str] = None
    pid7_field = pid.field(7)
    if pid7_field and pid7_field.value():
        # Convert HL7v2 date format (YYYYMMDD) to FHIR date format (YYYY-MM-DD)
        birth_date_str = pid7_field.value()
        if len(birth_date_str) >= 8:
            birth_date = f"{birth_date_str[0:4]}-{birth_date_str[4:6]}-{birth_date_str[6:8]}"
    
    # Extract gender (PID-8: Administrative Sex)
    gender: Optional[str] = None
    pid8_field = pid.field(8)
    if pid8_field and pid8_field.value():
        gender_code = pid8_field.value().upper()
        # Map HL7v2 gender codes to FHIR gender codes
        gender_map = {
            "M": "male",
            "F": "female",
            "O": "other",
            "U": "unknown",
            "A": "other",  # Ambiguous
        }
        gender = gender_map.get(gender_code, "unknown")
    
    # Extract address (PID-11: Patient Address)
    addresses: List[Address] = []
    pid11_field = pid.field(11)
    if pid11_field and pid11_field.value():
        # PID-11 format: Street^City^State^Zip^Country^Type^County^CensusTract
        for repetition in pid11_field.repetitions():
            if repetition and repetition.components:
                comp1 = repetition.component(1).value() if repetition.component(1) else None  # Street
                comp2 = repetition.component(2).value() if repetition.component(2) else None  # City
                comp3 = repetition.component(3).value() if repetition.component(3) else None  # State
                comp4 = repetition.component(4).value() if repetition.component(4) else None  # Zip
                comp5 = repetition.component(5).value() if repetition.component(5) else None  # Country
                comp6 = repetition.component(6).value() if repetition.component(6) else None  # Type
                
                address = Address(
                    use=comp6.lower() if comp6 else "home",
                    type_=None,
                    text=None,
                    line=[comp1] if comp1 else None,
                    city=comp2 if comp2 else None,
                    state=comp3 if comp3 else None,
                    postalCode=comp4 if comp4 else None,
                    country=comp5 if comp5 else None
                )
                addresses.append(address)
    
    # Extract telecom (PID-13: Phone Number - Home)
    telecom: List[ContactPoint] = []
    pid13_field = pid.field(13)
    if pid13_field and pid13_field.value():
        # PID-13 format: PhoneNumber^TelecommunicationUseCode^TelecommunicationEquipmentType^EmailAddress^CountryCode^AreaCode^PhoneNumber^Extension^AnyText
        for repetition in pid13_field.repetitions():
            if repetition and repetition.components:
                comp1 = repetition.component(1).value() if repetition.component(1) else None  # Phone Number
                comp2 = repetition.component(2).value() if repetition.component(2) else None  # Use Code
                comp4 = repetition.component(4).value() if repetition.component(4) else None  # Email
                
                if comp1:
                    contact = ContactPoint(
                        system="phone",
                        value=comp1,
                        use=comp2.lower() if comp2 else "home"
                    )
                    telecom.append(contact)
                
                if comp4:
                    contact = ContactPoint(
                        system="email",
                        value=comp4,
                        use="home"
                    )
                    telecom.append(contact)
    
    # Create Patient resource
    patient = Patient(
        resourceType="Patient",
        identifier=identifiers if identifiers else [],
        active=True,  # Default to active
        name=names if names else [],
        telecom=telecom if telecom else [],
        gender=gender,
        birthDate=birth_date,
        address=addresses if addresses else []
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] ADT to Patient conversion completed in {elapsed:.2f} seconds")
    logger.info(f"Current Time at End of Operations: {current_time_end}")
    
    return patient


def convert_adt_to_encounter(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> Encounter:
    """
    Convert HL7v2 ADT message to FHIR Encounter resource.
    
    Maps PV1 segment fields to FHIR Encounter resource fields:
    - PV1-2 (Patient Class) -> Encounter.class_
    - PV1-19 (Visit Number) -> Encounter.identifier
    - PV1-44 (Admit Date/Time) -> Encounter.period.start
    - PV1-45 (Discharge Date/Time) -> Encounter.period.end
    - PV1-10 (Hospital Service) -> Encounter.type
    - PV1-36 (Discharge Disposition) -> Encounter.hospitalization.dischargeDisposition
    - PV1-3 (Assigned Patient Location) -> Encounter.location
    
    Args:
        message: HL7v2 ADT message (must contain PV1 segment)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        FHIR Encounter resource
        
    Raises:
        ValueError: If message doesn't contain PV1 segment or conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ADT to Encounter conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Find PV1 segment
    pv1_segments = message.get_segments("PV1")
    if not pv1_segments:
        raise ValueError("ADT message must contain PV1 segment")
    
    pv1 = pv1_segments[0]
    
    # Extract encounter identifier (PV1-19: Visit Number)
    identifiers: List[Identifier] = []
    pv1_19_field = pv1.field(19)
    if pv1_19_field and pv1_19_field.value():
        visit_id = Identifier(
            use="usual",
            value=pv1_19_field.value(),
            type_=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="VN",
                    display="Visit Number"
                )]
            )
        )
        identifiers.append(visit_id)
    
    # Extract patient class (PV1-2: Patient Class)
    class_: Optional[CodeableConcept] = None
    pv1_2_field = pv1.field(2)
    if pv1_2_field and pv1_2_field.value():
        class_code = pv1_2_field.value()
        class_ = CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
                code=class_code,
                display=class_code
            )]
        )
    
    # Extract period (PV1-44: Admit Date/Time, PV1-45: Discharge Date/Time)
    period: Optional[Period] = None
    pv1_44_field = pv1.field(44)  # Admit Date/Time
    pv1_45_field = pv1.field(45)  # Discharge Date/Time
    
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    if pv1_44_field and pv1_44_field.value():
        # Convert HL7v2 datetime to FHIR datetime (ISO 8601)
        start_date = _convert_hl7v2_datetime_to_fhir(pv1_44_field.value())
    
    if pv1_45_field and pv1_45_field.value():
        end_date = _convert_hl7v2_datetime_to_fhir(pv1_45_field.value())
    
    if start_date or end_date:
        period = Period(
            start=start_date,
            end=end_date
        )
    
    # Extract encounter type (PV1-10: Hospital Service)
    encounter_types: List[CodeableConcept] = []
    pv1_10_field = pv1.field(10)
    if pv1_10_field and pv1_10_field.value():
        service_code = pv1_10_field.value()
        encounter_type = CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/v2-0069",
                code=service_code,
                display=service_code
            )]
        )
        encounter_types.append(encounter_type)
    
    # Extract subject reference (from PID segment)
    subject: Optional[Reference] = None
    pid_segments = message.get_segments("PID")
    if pid_segments:
        pid = pid_segments[0]
        pid3_field = pid.field(3)
        if pid3_field and pid3_field.value():
            patient_id = pid3_field.component(1).value() if pid3_field.component(1) else None
            if patient_id:
                subject = Reference(
                    reference=f"Patient/{patient_id}",
                    type_="Patient"
                )
    
    # Determine status from ADT message type
    status = "finished"  # Default
    msh_segment = message.get_segments("MSH")[0] if message.get_segments("MSH") else None
    if msh_segment:
        msh9_field = msh_segment.field(9)
        if msh9_field and msh9_field.value():
            message_type = msh9_field.value()
            if "A01" in message_type or "A04" in message_type or "A05" in message_type:
                status = "in-progress"
            elif "A03" in message_type or "A08" in message_type:
                status = "finished"
            elif "A02" in message_type:
                status = "in-progress"
    
    # Create Encounter resource
    encounter = Encounter(
        resourceType="Encounter",
        status=status,
        identifier=identifiers if identifiers else [],
        class_=class_,
        type_=encounter_types if encounter_types else [],
        subject=subject,
        period=period
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] ADT to Encounter conversion completed in {elapsed:.2f} seconds")
    
    return encounter


def convert_oru_to_observation(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> List[Observation]:
    """
    Convert HL7v2 ORU message to FHIR Observation resources.
    
    Maps OBX segments to FHIR Observation resources:
    - OBX-3 (Observation Identifier) -> Observation.code
    - OBX-5 (Observation Value) -> Observation.value[x]
    - OBX-6 (Units) -> Observation.valueQuantity.unit
    - OBX-7 (References Range) -> Observation.referenceRange
    - OBX-11 (Observation Result Status) -> Observation.status
    - OBX-14 (Date/Time of the Observation) -> Observation.effectiveDateTime
    
    Args:
        message: HL7v2 ORU message (must contain OBX segments)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        List of FHIR Observation resources (one per OBX segment)
        
    Raises:
        ValueError: If message doesn't contain OBX segments or conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ORU to Observation conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Find OBX segments
    obx_segments = message.get_segments("OBX")
    if not obx_segments:
        raise ValueError("ORU message must contain OBX segments")
    
    observations: List[Observation] = []
    
    for obx in obx_segments:
        # Extract observation code (OBX-3: Observation Identifier)
        code: Optional[CodeableConcept] = None
        obx3_field = obx.field(3)
        if obx3_field and obx3_field.value():
            # OBX-3 format: Identifier^Text^NameOfCodingSystem^AlternateIdentifier^AlternateText^AlternateNameOfCodingSystem
            comp1 = obx3_field.component(1).value() if obx3_field.component(1) else None  # Identifier
            comp2 = obx3_field.component(2).value() if obx3_field.component(2) else None  # Text
            comp3 = obx3_field.component(3).value() if obx3_field.component(3) else None  # Coding System
            
            code = CodeableConcept(
                coding=[Coding(
                    system=comp3 if comp3 else None,
                    code=comp1 if comp1 else None,
                    display=comp2 if comp2 else None
                )] if comp1 or comp2 else [],
                text=comp2 if comp2 else None
            )
        
        # Extract value type (OBX-2: Value Type) to determine how to parse OBX-5
        value_type: Optional[str] = None
        obx2_field = obx.field(2)
        if obx2_field and obx2_field.value():
            value_type = obx2_field.value().strip().upper()
        
        # Extract value (OBX-5: Observation Value) based on OBX-2 value type
        # OBX-2 indicates the data type of OBX-5 (ST, NM, TX, FT, DT, TM, TS, SN, CWE, etc.)
        value_string: Optional[str] = None
        value_quantity: Optional[Quantity] = None
        value_codeable_concept: Optional[CodeableConcept] = None
        value_integer: Optional[int] = None
        value_boolean: Optional[bool] = None
        value_datetime: Optional[str] = None
        
        obx5_field = obx.field(5)
        if obx5_field and obx5_field.value():
            obx5_value = obx5_field.value().strip()
            
            # Extract units (OBX-6: Units) for numeric values
            unit: Optional[str] = None
            obx6_field = obx.field(6)
            if obx6_field and obx6_field.value():
                unit = obx6_field.value().strip()
            
            # Map OBX-2 value type to appropriate FHIR value[x] field
            if value_type == "NM" or value_type == "SN":  # Numeric or Structured Numeric
                # Try to parse as float for Quantity
                try:
                    numeric_value = float(obx5_value)
                    value_quantity = Quantity(
                        value=numeric_value,
                        unit=unit if unit else None
                    )
                except (ValueError, TypeError):
                    # If parsing fails, fall back to string
                    value_string = obx5_value
            elif value_type == "CWE":  # Coded with Exceptions
                # OBX-5 format for CWE: Code^Text^NameOfCodingSystem^AlternateIdentifier^AlternateText^AlternateNameOfCodingSystem
                comp1 = obx5_field.component(1).value() if obx5_field.component(1) else None  # Code
                comp2 = obx5_field.component(2).value() if obx5_field.component(2) else None  # Text
                comp3 = obx5_field.component(3).value() if obx5_field.component(3) else None  # Coding System
                
                if comp1 or comp2:
                    value_codeable_concept = CodeableConcept(
                        coding=[Coding(
                            system=comp3 if comp3 else None,
                            code=comp1 if comp1 else None,
                            display=comp2 if comp2 else None
                        )] if comp1 or comp2 else [],
                        text=comp2 if comp2 else None
                    )
                else:
                    value_string = obx5_value
            elif value_type == "DT":  # Date
                # Convert HL7v2 date (YYYYMMDD) to FHIR date (YYYY-MM-DD)
                if len(obx5_value) >= 8:
                    fhir_date = f"{obx5_value[0:4]}-{obx5_value[4:6]}-{obx5_value[6:8]}"
                    value_string = fhir_date
                else:
                    value_string = obx5_value
            elif value_type == "TM":  # Time
                # Convert HL7v2 time (HHMMSS[.SSSS]) to FHIR time (HH:MM:SS[.SSS])
                if len(obx5_value) >= 4:
                    hour = obx5_value[0:2] if len(obx5_value) >= 2 else "00"
                    minute = obx5_value[2:4] if len(obx5_value) >= 4 else "00"
                    second = obx5_value[4:6] if len(obx5_value) >= 6 else "00"
                    fractional = obx5_value[6:] if len(obx5_value) > 6 else ""
                    if fractional and not fractional.startswith("."):
                        fractional = ""
                    fhir_time = f"{hour}:{minute}:{second}{fractional}"
                    value_string = fhir_time
                else:
                    value_string = obx5_value
            elif value_type == "TS":  # Time Stamp
                # Convert HL7v2 timestamp to FHIR datetime
                value_datetime = _convert_hl7v2_datetime_to_fhir(obx5_value)
                if not value_datetime:
                    value_string = obx5_value
            elif value_type in ["ID", "IS"]:  # Coded value or Coded value for user-defined tables
                # These are typically short codes, treat as string but could be CodeableConcept
                value_string = obx5_value
            elif value_type in ["ST", "TX", "FT"]:  # String, Text, Formatted Text
                value_string = obx5_value
            else:
                # Default: treat as string for unknown value types
                value_string = obx5_value
        
        # Extract status (OBX-11: Observation Result Status)
        status = "final"  # Default
        obx11_field = obx.field(11)
        if obx11_field and obx11_field.value():
            status_code = obx11_field.value().upper()
            # Map HL7v2 status codes to FHIR status codes
            status_map = {
                "P": "preliminary",
                "F": "final",
                "C": "corrected",
                "X": "cancelled",
                "I": "entered-in-error",
            }
            status = status_map.get(status_code, "final")
        
        # Extract effective date/time (OBX-14: Date/Time of the Observation)
        effective_datetime: Optional[str] = None
        obx14_field = obx.field(14)
        if obx14_field and obx14_field.value():
            effective_datetime = _convert_hl7v2_datetime_to_fhir(obx14_field.value())
        
        # Extract subject reference (from PID segment)
        subject: Optional[Reference] = None
        pid_segments = message.get_segments("PID")
        if pid_segments:
            pid = pid_segments[0]
            pid3_field = pid.field(3)
            if pid3_field and pid3_field.value():
                patient_id = pid3_field.component(1).value() if pid3_field.component(1) else None
                if patient_id:
                    subject = Reference(
                        reference=f"Patient/{patient_id}",
                        type_="Patient"
                    )
        
        # Create Observation resource with appropriate value[x] field
        observation = Observation(
            resourceType="Observation",
            status=status,
            code=code if code else CodeableConcept(),
            subject=subject,
            effectiveDateTime=effective_datetime,
            valueString=value_string,
            valueQuantity=value_quantity,
            valueCodeableConcept=value_codeable_concept,
            valueInteger=value_integer,
            valueBoolean=value_boolean,
            valueDateTime=value_datetime
        )
        
        observations.append(observation)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] ORU to Observation conversion completed in {elapsed:.2f} seconds: {len(observations)} observations")
    
    return observations


def convert_orm_to_servicerequest(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> List[ServiceRequest]:
    """
    Convert HL7v2 ORM message to FHIR ServiceRequest resources.
    
    Maps OBR segments to FHIR ServiceRequest resources:
    - OBR-2 (Placer Order Number) -> ServiceRequest.identifier
    - OBR-3 (Filler Order Number) -> ServiceRequest.identifier
    - OBR-4 (Universal Service Identifier) -> ServiceRequest.code
    - OBR-6 (Requested Date/Time) -> ServiceRequest.authoredOn
    - OBR-16 (Ordering Provider) -> ServiceRequest.requester
    - OBR-27 (Quantity/Timing) -> ServiceRequest.occurrenceTiming
    
    Args:
        message: HL7v2 ORM message (must contain OBR segments)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        List of FHIR ServiceRequest resources (one per OBR segment)
        
    Raises:
        ValueError: If message doesn't contain OBR segments or conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ORM to ServiceRequest conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Find OBR segments
    obr_segments = message.get_segments("OBR")
    if not obr_segments:
        raise ValueError("ORM message must contain OBR segments")
    
    service_requests: List[ServiceRequest] = []
    
    for obr in obr_segments:
        # Extract identifiers
        identifiers: List[Identifier] = []
        
        # OBR-2: Placer Order Number
        obr2_field = obr.field(2)
        if obr2_field and obr2_field.value():
            placer_id = Identifier(
                use="usual",
                value=obr2_field.value(),
                type_=CodeableConcept(
                    coding=[Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0203",
                        code="PLAC",
                        display="Placer"
                    )]
                )
            )
            identifiers.append(placer_id)
        
        # OBR-3: Filler Order Number
        obr3_field = obr.field(3)
        if obr3_field and obr3_field.value():
            filler_id = Identifier(
                use="usual",
                value=obr3_field.value(),
                type_=CodeableConcept(
                    coding=[Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0203",
                        code="FILL",
                        display="Filler"
                    )]
                )
            )
            identifiers.append(filler_id)
        
        # Extract code (OBR-4: Universal Service Identifier)
        code: Optional[CodeableConcept] = None
        obr4_field = obr.field(4)
        if obr4_field and obr4_field.value():
            # OBR-4 format: Identifier^Text^NameOfCodingSystem^AlternateIdentifier^AlternateText^AlternateNameOfCodingSystem
            comp1 = obr4_field.component(1).value() if obr4_field.component(1) else None
            comp2 = obr4_field.component(2).value() if obr4_field.component(2) else None
            comp3 = obr4_field.component(3).value() if obr4_field.component(3) else None
            
            code = CodeableConcept(
                coding=[Coding(
                    system=comp3 if comp3 else None,
                    code=comp1 if comp1 else None,
                    display=comp2 if comp2 else None
                )] if comp1 or comp2 else [],
                text=comp2 if comp2 else None
            )
        
        # Extract subject reference (from PID segment)
        subject: Optional[Reference] = None
        pid_segments = message.get_segments("PID")
        if pid_segments:
            pid = pid_segments[0]
            pid3_field = pid.field(3)
            if pid3_field and pid3_field.value():
                patient_id = pid3_field.component(1).value() if pid3_field.component(1) else None
                if patient_id:
                    subject = Reference(
                        reference=f"Patient/{patient_id}",
                        type_="Patient"
                    )
        
        # Extract authored date/time (OBR-6: Requested Date/Time)
        authored_on: Optional[str] = None
        obr6_field = obr.field(6)
        if obr6_field and obr6_field.value():
            authored_on = _convert_hl7v2_datetime_to_fhir(obr6_field.value())
        
        # Create ServiceRequest resource
        service_request = ServiceRequest(
            resourceType="ServiceRequest",
            status="active",  # Default status
            intent="order",  # Default intent
            code=code if code else CodeableConcept(),
            subject=subject,
            identifier=identifiers if identifiers else [],
            authoredOn=authored_on
        )
        
        service_requests.append(service_request)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] ORM to ServiceRequest conversion completed in {elapsed:.2f} seconds: {len(service_requests)} service requests")
    
    return service_requests


def convert_mdm_to_documentreference(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> DocumentReference:
    """
    Convert HL7v2 MDM message to FHIR DocumentReference resource.
    
    Maps TXA segment fields to FHIR DocumentReference resource fields:
    - TXA-2 (Document Type) -> DocumentReference.type
    - TXA-3 (Document Content Presentation) -> DocumentReference.content
    - TXA-4 (Activity Date/Time) -> DocumentReference.date
    - TXA-5 (Primary Activity Provider Code/Name) -> DocumentReference.author
    - TXA-12 (Unique Document Number) -> DocumentReference.identifier
    
    Args:
        message: HL7v2 MDM message (must contain TXA segment)
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        FHIR DocumentReference resource
        
    Raises:
        ValueError: If message doesn't contain TXA segment or conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MDM to DocumentReference conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Find TXA segment
    txa_segments = message.get_segments("TXA")
    if not txa_segments:
        raise ValueError("MDM message must contain TXA segment")
    
    txa = txa_segments[0]
    
    # Extract document type (TXA-2: Document Type)
    doc_type: Optional[CodeableConcept] = None
    txa2_field = txa.field(2)
    if txa2_field and txa2_field.value():
        # TXA-2 format: Identifier^Text^NameOfCodingSystem^AlternateIdentifier^AlternateText^AlternateNameOfCodingSystem
        comp1 = txa2_field.component(1).value() if txa2_field.component(1) else None
        comp2 = txa2_field.component(2).value() if txa2_field.component(2) else None
        comp3 = txa2_field.component(3).value() if txa2_field.component(3) else None
        
        doc_type = CodeableConcept(
            coding=[Coding(
                system=comp3 if comp3 else None,
                code=comp1 if comp1 else None,
                display=comp2 if comp2 else None
            )] if comp1 or comp2 else [],
            text=comp2 if comp2 else None
        )
    
    # Extract identifier (TXA-12: Unique Document Number)
    identifiers: List[Identifier] = []
    txa12_field = txa.field(12)
    if txa12_field and txa12_field.value():
        doc_id = Identifier(
            use="usual",
            value=txa12_field.value(),
            type_=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="UDN",
                    display="Unique Document Number"
                )]
            )
        )
        identifiers.append(doc_id)
    
    # Extract date (TXA-4: Activity Date/Time)
    date: Optional[str] = None
    txa4_field = txa.field(4)
    if txa4_field and txa4_field.value():
        date = _convert_hl7v2_datetime_to_fhir(txa4_field.value())
    
    # Extract subject reference (from PID segment)
    subject: Optional[Reference] = None
    pid_segments = message.get_segments("PID")
    if pid_segments:
        pid = pid_segments[0]
        pid3_field = pid.field(3)
        if pid3_field and pid3_field.value():
            patient_id = pid3_field.component(1).value() if pid3_field.component(1) else None
            if patient_id:
                subject = Reference(
                    reference=f"Patient/{patient_id}",
                    type_="Patient"
                )
    
    # Create DocumentReference resource
    document_reference = DocumentReference(
        resourceType="DocumentReference",
        status="current",  # Default status
        type_=doc_type if doc_type else CodeableConcept(),
        subject=subject,
        date=date,
        identifier=identifiers if identifiers else []
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] MDM to DocumentReference conversion completed in {elapsed:.2f} seconds")
    
    return document_reference


def _convert_hl7v2_datetime_to_fhir(datetime_str: str) -> str:
    """
    Convert HL7v2 datetime format to FHIR datetime format (ISO 8601).
    
    HL7v2 datetime format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
    FHIR datetime format: YYYY-MM-DDThh:mm:ss[.sss][+/-zz:zz] or YYYY-MM-DDThh:mm:ss[.sss]Z
    
    Args:
        datetime_str: HL7v2 datetime string
        
    Returns:
        FHIR datetime string (ISO 8601 format)
    """
    if not datetime_str:
        return None
    
    # Remove any whitespace
    datetime_str = datetime_str.strip()
    
    # Minimum length is 8 (YYYYMMDD)
    if len(datetime_str) < 8:
        return None
    
    # Extract date components
    year = datetime_str[0:4]
    month = datetime_str[4:6] if len(datetime_str) >= 6 else "01"
    day = datetime_str[6:8] if len(datetime_str) >= 8 else "01"
    
    # Extract time components if present
    hour = datetime_str[8:10] if len(datetime_str) >= 10 else "00"
    minute = datetime_str[10:12] if len(datetime_str) >= 12 else "00"
    second = datetime_str[12:14] if len(datetime_str) >= 14 else "00"
    
    # Extract fractional seconds if present
    fractional = ""
    if len(datetime_str) > 14 and datetime_str[14] == ".":
        # Find end of fractional seconds (before timezone or end of string)
        frac_end = len(datetime_str)
        for i in range(15, len(datetime_str)):
            if datetime_str[i] in ["+", "-", "Z"]:
                frac_end = i
                break
        fractional = datetime_str[14:frac_end]
    
    # Extract timezone if present
    timezone = ""
    tz_start = 14 + len(fractional)
    if tz_start < len(datetime_str):
        if datetime_str[tz_start] == "Z":
            timezone = "Z"
        elif datetime_str[tz_start] in ["+", "-"]:
            # HL7v2 timezone format: +/-HHMM
            if tz_start + 5 <= len(datetime_str):
                tz_sign = datetime_str[tz_start]
                tz_hh = datetime_str[tz_start + 1:tz_start + 3]
                tz_mm = datetime_str[tz_start + 3:tz_start + 5]
                timezone = f"{tz_sign}{tz_hh}:{tz_mm}"
    
    # Construct FHIR datetime
    fhir_datetime = f"{year}-{month}-{day}T{hour}:{minute}:{second}{fractional}{timezone}"
    
    return fhir_datetime
