# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 to HL7v3 mapping utilities.

Provides functions to convert FHIR R4 resources to HL7v3 messages.
"""

import logging
from datetime import datetime
from typing import List, Optional
from time import time

from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.servicerequest import ServiceRequest
from dnhealth.dnhealth_fhir.resources.medicationrequest import MedicationRequest
from dnhealth.dnhealth_fhir.resources.medicationdispense import MedicationDispense
from dnhealth.dnhealth_hl7v3.model import Message, ElementNode

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def convert_patient_to_prpa(
    patient: Patient,    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR Patient resource to HL7v3 PRPA message.
    
    Maps FHIR Patient fields to HL7v3 PRPA message elements using XPath structure.
    
    Args:
        patient: FHIR Patient resource
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v3 PRPA message
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting Patient to PRPA conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create root element
    root = ElementNode(
        name="PRPA_IN201301UV02",
        namespace="urn:hl7-org:v3",
        attributes={
            "xmlns": "urn:hl7-org:v3",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    )
    
    # Create control act process
    control_act = ElementNode(
        name="controlActProcess",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Create subject element
    subject = ElementNode(
        name="subject",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Create registration event
    reg_event = ElementNode(
        name="registrationEvent",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Create subject1 element
    subject1 = ElementNode(
        name="subject1",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Create patient element
    patient_elem = ElementNode(
        name="patient",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Add identifiers
    if patient.identifier:
        for identifier in patient.identifier:
            id_elem = ElementNode(
                name="id",
                namespace="urn:hl7-org:v3",
                attributes={
                    "root": identifier.system if identifier.system else "",
                    "extension": identifier.value if identifier.value else ""
                }
            )
            patient_elem.children.append(id_elem)
    
    # Add names
    if patient.name:
        for name in patient.name:
            name_elem = ElementNode(
                name="name",
                namespace="urn:hl7-org:v3",
                children=[]
            )
            
            # Add family name
            if name.family:
                family_elem = ElementNode(
                    name="family",
                    namespace="urn:hl7-org:v3",
                    text=name.family
                )
                name_elem.children.append(family_elem)
            
            # Add given names
            if name.given:
                for given_name in name.given:
                    given_elem = ElementNode(
                        name="given",
                        namespace="urn:hl7-org:v3",
                        text=given_name
                    )
                    name_elem.children.append(given_elem)
            
            patient_elem.children.append(name_elem)
    
    # Add birth date
    if patient.birthDate:
        birth_elem = ElementNode(
            name="birthTime",
            namespace="urn:hl7-org:v3",
            attributes={
                "value": _convert_fhir_date_to_hl7v3(patient.birthDate)
            }
        )
        patient_elem.children.append(birth_elem)
    
    # Add gender
    if patient.gender:
        gender_map = {
            "male": "M",
            "female": "F",
            "other": "O",
            "unknown": "U",
        }
        gender_code = gender_map.get(patient.gender.lower(), "U")
        gender_elem = ElementNode(
            name="administrativeGenderCode",
            namespace="urn:hl7-org:v3",
            attributes={
                "code": gender_code
            }
        )
        patient_elem.children.append(gender_elem)
    
    # Build hierarchy
    subject1.children.append(patient_elem)
    reg_event.children.append(subject1)
    subject.children.append(reg_event)
    control_act.children.append(subject)
    root.children.append(control_act)
    
    # Create message
    message = Message(root=root)
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] Patient to PRPA conversion completed in {elapsed:.2f} seconds")
    
    return message


def convert_observation_to_polb(
    observations: List[Observation],
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR Observation resources to HL7v3 POLB message.
    
    Maps FHIR Observation fields to HL7v3 POLB message elements.
    
    Args:
        observations: List of FHIR Observation resources
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v3 POLB message
        
    Raises:
        ValueError: If conversion exceeds timeout or no observations provided
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting Observation to POLB conversion")
    
    if not observations:
        raise ValueError("At least one Observation resource is required")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create root element
    root = ElementNode(
        name="POLB_IN224200UV01",
        namespace="urn:hl7-org:v3",
        attributes={
            "xmlns": "urn:hl7-org:v3",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    )
    
    # Create control act process
    control_act = ElementNode(
        name="controlActProcess",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Add observation elements
    for obs in observations:
        obs_elem = ElementNode(
            name="observation",
            namespace="urn:hl7-org:v3",
            children=[]
        )
        
        # Add code
        if obs.code and obs.code.coding:
            code_elem = ElementNode(
                name="code",
                namespace="urn:hl7-org:v3",
                attributes={
                    "code": obs.code.coding[0].code if obs.code.coding[0].code else "",
                    "codeSystem": obs.code.coding[0].system if obs.code.coding[0].system else "",
                    "displayName": obs.code.coding[0].display if obs.code.coding[0].display else ""
                }
            )
            obs_elem.children.append(code_elem)
        
        # Add value
        if obs.valueString:
            value_elem = ElementNode(
                name="value",
                namespace="urn:hl7-org:v3",
                text=obs.valueString
            )
            obs_elem.children.append(value_elem)
        
        # Add effective time
        if obs.effectiveDateTime:
            time_elem = ElementNode(
                name="effectiveTime",
                namespace="urn:hl7-org:v3",
                attributes={
                    "value": _convert_fhir_datetime_to_hl7v3(obs.effectiveDateTime)
                }
            )
            obs_elem.children.append(time_elem)
        
        control_act.children.append(obs_elem)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root.children.append(control_act)
    
    # Create message
    message = Message(root=root)
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] Observation to POLB conversion completed in {elapsed:.2f} seconds: {len(observations)} observations")
    
    return message


def convert_servicerequest_to_polb(
    service_requests: List[ServiceRequest],
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR ServiceRequest resources to HL7v3 POLB message.
    
    Maps FHIR ServiceRequest fields to HL7v3 POLB message elements.
    
    Args:
        service_requests: List of FHIR ServiceRequest resources
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v3 POLB message
        
    Raises:
        ValueError: If conversion exceeds timeout or no service requests provided
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting ServiceRequest to POLB conversion")
    
    if not service_requests:
        raise ValueError("At least one ServiceRequest resource is required")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create root element
    root = ElementNode(
        name="POLB_IN224200UV01",
        namespace="urn:hl7-org:v3",
        attributes={
            "xmlns": "urn:hl7-org:v3",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    )
    
    # Create control act process
    control_act = ElementNode(
        name="controlActProcess",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Add service request elements
    for sr in service_requests:
        req_elem = ElementNode(
            name="serviceRequest",
            namespace="urn:hl7-org:v3",
            children=[]
        )
        
        # Add code
        if sr.code and sr.code.coding:
            code_elem = ElementNode(
                name="code",
                namespace="urn:hl7-org:v3",
                attributes={
                    "code": sr.code.coding[0].code if sr.code.coding[0].code else "",
                    "codeSystem": sr.code.coding[0].system if sr.code.coding[0].system else "",
                    "displayName": sr.code.coding[0].display if sr.code.coding[0].display else ""
                }
            )
            req_elem.children.append(code_elem)
        
        control_act.children.append(req_elem)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root.children.append(control_act)
    
    # Create message
    message = Message(root=root)
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] ServiceRequest to POLB conversion completed in {elapsed:.2f} seconds: {len(service_requests)} service requests")
    
    return message


def convert_medicationrequest_to_porx(
    medication_requests: List[MedicationRequest],
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR MedicationRequest resources to HL7v3 PORX message.
    
    Maps FHIR MedicationRequest fields to HL7v3 PORX message elements.
    
    Args:
        medication_requests: List of FHIR MedicationRequest resources
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v3 PORX message
        
    Raises:
        ValueError: If conversion exceeds timeout or no medication requests provided
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MedicationRequest to PORX conversion")
    
    if not medication_requests:
        raise ValueError("At least one MedicationRequest resource is required")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create root element
    root = ElementNode(
        name="PORX_IN020101UV01",
        namespace="urn:hl7-org:v3",
        attributes={
            "xmlns": "urn:hl7-org:v3",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    )
    
    # Create control act process
    control_act = ElementNode(
        name="controlActProcess",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Add medication request elements
    for mr in medication_requests:
        req_elem = ElementNode(
            name="medicationRequest",
            namespace="urn:hl7-org:v3",
            children=[]
        )
        
        # Add medication
        medication_elem = ElementNode(
            name="medication",
            namespace="urn:hl7-org:v3",
            children=[]
        )
        
        # Add medication code
        if mr.medicationCodeableConcept and mr.medicationCodeableConcept.coding:
            code_elem = ElementNode(
                name="code",
                namespace="urn:hl7-org:v3",
                attributes={
                    "code": mr.medicationCodeableConcept.coding[0].code if mr.medicationCodeableConcept.coding[0].code else "",
                    "codeSystem": mr.medicationCodeableConcept.coding[0].system if mr.medicationCodeableConcept.coding[0].system else "",
                    "displayName": mr.medicationCodeableConcept.coding[0].display if mr.medicationCodeableConcept.coding[0].display else ""
                }
            )
            medication_elem.children.append(code_elem)
        
        req_elem.children.append(medication_elem)
        control_act.children.append(req_elem)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root.children.append(control_act)
    
    # Create message
    message = Message(root=root)
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] MedicationRequest to PORX conversion completed in {elapsed:.2f} seconds: {len(medication_requests)} medication requests")
    
    return message


def convert_medicationdispense_to_porx(
    medication_dispenses: List[MedicationDispense],
    timeout: int = TEST_TIMEOUT
) -> Message:
    """
    Convert FHIR MedicationDispense resources to HL7v3 PORX message.
    
    Maps FHIR MedicationDispense fields to HL7v3 PORX message elements.
    
    Args:
        medication_dispenses: List of FHIR MedicationDispense resources
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        HL7v3 PORX message
        
    Raises:
        ValueError: If conversion exceeds timeout or no medication dispenses provided
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting MedicationDispense to PORX conversion")
    
    if not medication_dispenses:
        raise ValueError("At least one MedicationDispense resource is required")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    # Create root element
    root = ElementNode(
        name="PORX_IN020201UV01",
        namespace="urn:hl7-org:v3",
        attributes={
            "xmlns": "urn:hl7-org:v3",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    )
    
    # Create control act process
    control_act = ElementNode(
        name="controlActProcess",
        namespace="urn:hl7-org:v3",
        children=[]
    )
    
    # Add medication dispense elements
    for md in medication_dispenses:
        disp_elem = ElementNode(
            name="medicationDispense",
            namespace="urn:hl7-org:v3",
            children=[]
        )
        
        # Add medication
        medication_elem = ElementNode(
            name="medication",
            namespace="urn:hl7-org:v3",
            children=[]
        )
        
        # Add medication code
        if md.medicationCodeableConcept and md.medicationCodeableConcept.coding:
            code_elem = ElementNode(
                name="code",
                namespace="urn:hl7-org:v3",
                attributes={
                    "code": md.medicationCodeableConcept.coding[0].code if md.medicationCodeableConcept.coding[0].code else "",
                    "codeSystem": md.medicationCodeableConcept.coding[0].system if md.medicationCodeableConcept.coding[0].system else "",
                    "displayName": md.medicationCodeableConcept.coding[0].display if md.medicationCodeableConcept.coding[0].display else ""
                }
            )
            medication_elem.children.append(code_elem)
        
        disp_elem.children.append(medication_elem)
        control_act.children.append(disp_elem)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root.children.append(control_act)
    
    # Create message
    message = Message(root=root)
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] MedicationDispense to PORX conversion completed in {elapsed:.2f} seconds: {len(medication_dispenses)} medication dispenses")
    
    return message


def _convert_fhir_date_to_hl7v3(date_str: str) -> str:
    """
    Convert FHIR date format to HL7v3 datetime format.
    
    FHIR date format: YYYY-MM-DD
    HL7v3 datetime format: YYYYMMDDHHMMSS
    
    Args:
        date_str: FHIR date string
        
    Returns:
        HL7v3 datetime string
    """
    if not date_str:
        return ""
    
    # Remove any whitespace
    date_str = date_str.strip()
    
    # Remove '-' from date
    date_str = date_str.replace("-", "")
    
    # Add default time if not present
    if len(date_str) == 8:
        date_str += "000000"  # Add HHMMSS
    
    return date_str


def _convert_fhir_datetime_to_hl7v3(datetime_str: str) -> str:
    """
    Convert FHIR datetime format to HL7v3 datetime format.
    
    FHIR datetime format: YYYY-MM-DDThh:mm:ss[.sss][+/-zz:zz] or YYYY-MM-DDThh:mm:ss[.sss]Z
    HL7v3 datetime format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
    
    Args:
        datetime_str: FHIR datetime string
        
    Returns:
        HL7v3 datetime string
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
