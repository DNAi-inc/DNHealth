# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7v3 to FHIR R4 mapping utilities.

Provides functions to convert HL7v3 messages to FHIR R4 resources.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from time import time

from dnhealth.dnhealth_hl7v3.model import Message, ElementNode
from dnhealth.dnhealth_hl7v3.xpath import find_by_xpath
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.servicerequest import ServiceRequest
from dnhealth.dnhealth_fhir.resources.medicationrequest import MedicationRequest
from dnhealth.dnhealth_fhir.resources.medicationdispense import MedicationDispense
from dnhealth.dnhealth_fhir.types import (
    Identifier,
    HumanName,
    ContactPoint,
    Address,
    Reference,
    CodeableConcept,
    Coding,
    Period,
)

logger = logging.getLogger(__name__)

# Test timeout limit: 5 minutes (300 seconds)
TEST_TIMEOUT = 300


def convert_prpa_to_patient(
    message: Message,    timeout: int = TEST_TIMEOUT
) -> Patient:
    """
    Convert HL7v3 PRPA (Patient Registry) message to FHIR Patient resource.
    
    Maps PRPA message elements to FHIR Patient resource fields using XPath:
    - /PRPA_IN201301UV02/controlActProcess/subject/registrationEvent/subject1/patient/id -> Patient.identifier
    - /PRPA_IN201301UV02/controlActProcess/subject/registrationEvent/subject1/patient/name -> Patient.name
    - /PRPA_IN201301UV02/controlActProcess/subject/registrationEvent/subject1/patient/birthTime -> Patient.birthDate
    - /PRPA_IN201301UV02/controlActProcess/subject/registrationEvent/subject1/patient/administrativeGenderCode -> Patient.gender
    
    Args:
        message: HL7v3 PRPA message
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        FHIR Patient resource
        
    Raises:
        ValueError: If conversion exceeds timeout or required elements are missing
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PRPA to Patient conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root = message.root if hasattr(message, 'root') else message
    
    # Extract identifiers
    identifiers: List[Identifier] = []
    id_elements = find_by_xpath(root, "//patient/id")
    for id_elem in id_elements:
        if id_elem and id_elem.attributes:
            root_attr = id_elem.attributes.get("root", "")
            extension_attr = id_elem.attributes.get("extension", "")
            if root_attr or extension_attr:
                identifier = Identifier(
                    use="usual",
                    system=root_attr if root_attr else None,
                    value=extension_attr if extension_attr else root_attr,
                    type_=None
                )
                identifiers.append(identifier)
    
    # Extract names
    names: List[HumanName] = []
    name_elements = find_by_xpath(root, "//patient/name")
    for name_elem in name_elements:
        if name_elem:
            # Extract name parts
            given_parts = []
            family = None
            
            # Look for given name parts
            given_elems = find_by_xpath(name_elem, ".//given")
            for given_elem in given_elems:
                if given_elem and given_elem.text:
                    given_parts.append(given_elem.text)
            
            # Look for family name
            family_elems = find_by_xpath(name_elem, ".//family")
            if family_elems and family_elems[0] and family_elems[0].text:
                family = family_elems[0].text
            
            if family or given_parts:
                name = HumanName(
                    use="official",
                    family=family,
                    given=given_parts if given_parts else None
                )
                names.append(name)
    
    # Extract birth date
    birth_date: Optional[str] = None
    birth_elements = find_by_xpath(root, "//patient/birthTime")
    if birth_elements and birth_elements[0]:
        birth_elem = birth_elements[0]
        if birth_elem.attributes:
            value_attr = birth_elem.attributes.get("value", "")
            if value_attr:
                # Convert HL7v3 datetime to FHIR date format
                birth_date = _convert_hl7v3_datetime_to_fhir_date(value_attr)
    
    # Extract gender
    gender: Optional[str] = None
    gender_elements = find_by_xpath(root, "//patient/administrativeGenderCode")
    if gender_elements and gender_elements[0]:
        gender_elem = gender_elements[0]
        if gender_elem.attributes:
            code_attr = gender_elem.attributes.get("code", "")
            if code_attr:
                # Map HL7v3 gender codes to FHIR gender codes
                gender_map = {
                    "M": "male",
                    "F": "female",
                    "O": "other",
                    "U": "unknown",
                }
                gender = gender_map.get(code_attr.upper(), "unknown")
    
    # Create Patient resource
    patient = Patient(
        resourceType="Patient",
        identifier=identifiers if identifiers else [],
        active=True,
        name=names if names else [],
        gender=gender,
        birthDate=birth_date
    )
    
    elapsed = time() - start_time
    if elapsed > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] PRPA to Patient conversion completed in {elapsed:.2f} seconds")
    
    return patient


def convert_polb_to_observation(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> List[Observation]:
    """
    Convert HL7v3 POLB (Laboratory) message to FHIR Observation resources.
    
    Maps POLB message elements to FHIR Observation resources using XPath.
    
    Args:
        message: HL7v3 POLB message
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        List of FHIR Observation resources
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting POLB to Observation conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root = message.root if hasattr(message, 'root') else message
    observations: List[Observation] = []
    
    # Find observation elements
    observation_elements = find_by_xpath(root, "//observation")
    
    for obs_elem in observation_elements:
        # Extract code
        code: Optional[CodeableConcept] = None
        code_elements = find_by_xpath(obs_elem, ".//code")
        if code_elements and code_elements[0]:
            code_elem = code_elements[0]
            if code_elem.attributes:
                code_attr = code_elem.attributes.get("code", "")
                code_system = code_elem.attributes.get("codeSystem", "")
                display_name = code_elem.attributes.get("displayName", "")
                
                code = CodeableConcept(
                    coding=[Coding(
                        system=code_system if code_system else None,
                        code=code_attr if code_attr else None,
                        display=display_name if display_name else None
                    )] if code_attr or display_name else [],
                    text=display_name if display_name else None
                )
        
        # Extract value
        value_string: Optional[str] = None
        value_elements = find_by_xpath(obs_elem, ".//value")
        if value_elements and value_elements[0]:
            value_elem = value_elements[0]
            if value_elem.text:
                value_string = value_elem.text
            elif value_elem.attributes:
                value_string = value_elem.attributes.get("value", "")
        
        # Extract effective date/time
        effective_datetime: Optional[str] = None
        time_elements = find_by_xpath(obs_elem, ".//effectiveTime")
        if time_elements and time_elements[0]:
            time_elem = time_elements[0]
            if time_elem.attributes:
                time_value = time_elem.attributes.get("value", "")
                if time_value:
                    effective_datetime = _convert_hl7v3_datetime_to_fhir_datetime(time_value)
        
        # Create Observation resource
        observation = Observation(
            resourceType="Observation",
            status="final",
            code=code if code else CodeableConcept(),
            effectiveDateTime=effective_datetime,
            valueString=value_string
        )
        
        observations.append(observation)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] POLB to Observation conversion completed in {elapsed:.2f} seconds: {len(observations)} observations")
    
    return observations


def convert_polb_to_servicerequest(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> List[ServiceRequest]:
    """
    Convert HL7v3 POLB (Laboratory) message to FHIR ServiceRequest resources.
    
    Maps POLB message elements to FHIR ServiceRequest resources using XPath.
    
    Args:
        message: HL7v3 POLB message
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        List of FHIR ServiceRequest resources
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting POLB to ServiceRequest conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root = message.root if hasattr(message, 'root') else message
    service_requests: List[ServiceRequest] = []
    
    # Find service request elements
    request_elements = find_by_xpath(root, "//serviceRequest")
    
    for req_elem in request_elements:
        # Extract code
        code: Optional[CodeableConcept] = None
        code_elements = find_by_xpath(req_elem, ".//code")
        if code_elements and code_elements[0]:
            code_elem = code_elements[0]
            if code_elem.attributes:
                code_attr = code_elem.attributes.get("code", "")
                code_system = code_elem.attributes.get("codeSystem", "")
                display_name = code_elem.attributes.get("displayName", "")
                
                code = CodeableConcept(
                    coding=[Coding(
                        system=code_system if code_system else None,
                        code=code_attr if code_attr else None,
                        display=display_name if display_name else None
                    )] if code_attr or display_name else [],
                    text=display_name if display_name else None
                )
        
        # Create ServiceRequest resource
        service_request = ServiceRequest(
            resourceType="ServiceRequest",
            status="active",
            intent="order",
            code=code if code else CodeableConcept()
        )
        
        service_requests.append(service_request)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] POLB to ServiceRequest conversion completed in {elapsed:.2f} seconds: {len(service_requests)} service requests")
    
    return service_requests


def convert_porx_to_medicationrequest(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> List[MedicationRequest]:
    """
    Convert HL7v3 PORX (Pharmacy) message to FHIR MedicationRequest resources.
    
    Maps PORX message elements to FHIR MedicationRequest resources using XPath.
    
    Args:
        message: HL7v3 PORX message
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        List of FHIR MedicationRequest resources
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PORX to MedicationRequest conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root = message.root if hasattr(message, 'root') else message
    medication_requests: List[MedicationRequest] = []
    
    # Find medication request elements
    request_elements = find_by_xpath(root, "//medicationRequest")
    
    for req_elem in request_elements:
        # Extract medication code
        medication_code: Optional[CodeableConcept] = None
        medication_elements = find_by_xpath(req_elem, ".//medication/code")
        if medication_elements and medication_elements[0]:
            med_elem = medication_elements[0]
            if med_elem.attributes:
                code_attr = med_elem.attributes.get("code", "")
                code_system = med_elem.attributes.get("codeSystem", "")
                display_name = med_elem.attributes.get("displayName", "")
                
                medication_code = CodeableConcept(
                    coding=[Coding(
                        system=code_system if code_system else None,
                        code=code_attr if code_attr else None,
                        display=display_name if display_name else None
                    )] if code_attr or display_name else [],
                    text=display_name if display_name else None
                )
        
        # Create MedicationRequest resource
        medication_request = MedicationRequest(
            resourceType="MedicationRequest",
            status="active",
            intent="order",
            medicationCodeableConcept=medication_code if medication_code else CodeableConcept()
        )
        
        medication_requests.append(medication_request)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] PORX to MedicationRequest conversion completed in {elapsed:.2f} seconds: {len(medication_requests)} medication requests")
    
    return medication_requests


def convert_porx_to_medicationdispense(
    message: Message,
    timeout: int = TEST_TIMEOUT
) -> List[MedicationDispense]:
    """
    Convert HL7v3 PORX (Pharmacy) message to FHIR MedicationDispense resources.
    
    Maps PORX message elements to FHIR MedicationDispense resources using XPath.
    
    Args:
        message: HL7v3 PORX message
        timeout: Maximum time in seconds for conversion (default: 300)
        
    Returns:
        List of FHIR MedicationDispense resources
        
    Raises:
        ValueError: If conversion exceeds timeout
    """
    start_time = time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] Starting PORX to MedicationDispense conversion")
    
    # Check timeout
    if time() - start_time > timeout:
        raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")
    
    root = message.root if hasattr(message, 'root') else message
    medication_dispenses: List[MedicationDispense] = []
    
    # Find medication dispense elements
    dispense_elements = find_by_xpath(root, "//medicationDispense")
    
    for disp_elem in dispense_elements:
        # Extract medication code
        medication_code: Optional[CodeableConcept] = None
        medication_elements = find_by_xpath(disp_elem, ".//medication/code")
        if medication_elements and medication_elements[0]:
            med_elem = medication_elements[0]
            if med_elem.attributes:
                code_attr = med_elem.attributes.get("code", "")
                code_system = med_elem.attributes.get("codeSystem", "")
                display_name = med_elem.attributes.get("displayName", "")
                
                medication_code = CodeableConcept(
                    coding=[Coding(
                        system=code_system if code_system else None,
                        code=code_attr if code_attr else None,
                        display=display_name if display_name else None
                    )] if code_attr or display_name else [],
                    text=display_name if display_name else None
                )
        
        # Create MedicationDispense resource
        medication_dispense = MedicationDispense(
            resourceType="MedicationDispense",
            status="completed",
            medicationCodeableConcept=medication_code if medication_code else CodeableConcept()
        )
        
        medication_dispenses.append(medication_dispense)
        
        # Check timeout during loop
        if time() - start_time > timeout:
            raise ValueError(f"Conversion exceeded timeout of {timeout} seconds")

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    elapsed = time() - start_time
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time_end}] PORX to MedicationDispense conversion completed in {elapsed:.2f} seconds: {len(medication_dispenses)} medication dispenses")
    
    return medication_dispenses


def _convert_hl7v3_datetime_to_fhir_date(datetime_str: str) -> str:
    """
    Convert HL7v3 datetime format to FHIR date format.
    
    HL7v3 datetime format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
    FHIR date format: YYYY-MM-DD
    
    Args:
        datetime_str: HL7v3 datetime string
        
    Returns:
        FHIR date string
    """
    if not datetime_str:
        return None
    
    # Remove any whitespace
    datetime_str = datetime_str.strip()
    
    # Minimum length is 8 (YYYYMMDD)
    if len(datetime_str) < 8:
        return None

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    
    # Extract date components
    year = datetime_str[0:4]
    month = datetime_str[4:6] if len(datetime_str) >= 6 else "01"
    day = datetime_str[6:8] if len(datetime_str) >= 8 else "01"
    
    # Construct FHIR date
    fhir_date = f"{year}-{month}-{day}"
    
    return fhir_date


def _convert_hl7v3_datetime_to_fhir_datetime(datetime_str: str) -> str:
    """
    Convert HL7v3 datetime format to FHIR datetime format (ISO 8601).
    
    HL7v3 datetime format: YYYYMMDDHHMMSS[.SSSS][+/-ZZZZ]
    FHIR datetime format: YYYY-MM-DDThh:mm:ss[.sss][+/-zz:zz] or YYYY-MM-DDThh:mm:ss[.sss]Z
    
    Args:
        datetime_str: HL7v3 datetime string
        
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
            # HL7v3 timezone format: +/-HHMM
            if tz_start + 5 <= len(datetime_str):
                tz_sign = datetime_str[tz_start]
                tz_hh = datetime_str[tz_start + 1:tz_start + 3]
                tz_mm = datetime_str[tz_start + 3:tz_start + 5]
                timezone = f"{tz_sign}{tz_hh}:{tz_mm}"
    
    # Construct FHIR datetime
    fhir_datetime = f"{year}-{month}-{day}T{hour}:{minute}:{second}{fractional}{timezone}"
    
    return fhir_datetime
