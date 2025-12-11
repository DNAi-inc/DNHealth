# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
HL7 v3 Reference Information Model (RIM) core classes.

Implements the six core RIM classes: Entity, Role, Act, Participation,
ActRelationship, and RoleLink, along with their relationships.

Includes validation and XML serialization/deserialization support.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# HL7 v3 namespace
HL7V3_NAMESPACE = "urn:hl7-org:v3"


@dataclass
class Entity:
    """
    RIM Entity class - represents a physical or conceptual thing.
    
    Entities are things that have identity and can have roles.
    Examples: Person, Organization, Place, Material, etc.
    """
    # Core attributes
    class_code: Optional[str] = None  # Classification of the entity
    determiner_code: Optional[str] = None  # Determines if entity is specific or generic
    id: Optional[str] = None  # Unique identifier
    code: Optional[str] = None  # Coded classification
    name: Optional[str] = None  # Name of the entity
    desc: Optional[str] = None  # Description
    
    # Status and validity
    status_code: Optional[str] = None  # Status of the entity
    effective_time: Optional[str] = None  # Time period when entity is valid
    
    # Additional commonly used attributes
    null_flavor: Optional[str] = None  # Null flavor (e.g., NI, UNK, NINF, PINF)
    negation_ind: Optional[bool] = None  # Negation indicator
    confidentiality_code: Optional[str] = None  # Confidentiality code
    
    # Relationships
    roles: List["Role"] = field(default_factory=list)  # Roles this entity plays
    
    def add_role(self, role: "Role") -> None:
        """
        Add a role to this entity.
        
        Args:
            role: Role instance to add
        """
        self.roles.append(role)
        role.entity = self
    
    def get_roles(self, class_code: Optional[str] = None) -> List["Role"]:
        """
        Get roles for this entity, optionally filtered by class code.
        
        Args:
            class_code: Optional role class code to filter by
            
        Returns:
            List of matching roles
        """
        if class_code is None:
            return self.roles
        return [role for role in self.roles if role.class_code == class_code]
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate Entity instance against HL7 v3 RIM constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # classCode is typically required in most contexts
        # (but not enforced here as it depends on context)
        
        # Validate effective_time format if present (should be TS format)
        if self.effective_time:
            # Basic TS format validation (YYYYMMDDHHmmss[.s[s[s[s]]]][+/-ZZzz])
            if not isinstance(self.effective_time, str):
                errors.append("Entity.effective_time must be a string")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Entity validation completed with {len(errors)} errors")
        
        return len(errors) == 0, errors
    
    def to_xml(self, element_name: str = "entity") -> ET.Element:
        """
        Serialize Entity to XML element.
        
        Args:
            element_name: XML element name (default: "entity")
            
        Returns:
            XML Element
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Entity XML serialization")
        
        element = ET.Element(element_name)
        element.set("xmlns", HL7V3_NAMESPACE)
        
        if self.class_code:
            element.set("classCode", self.class_code)
        if self.determiner_code:
            element.set("determinerCode", self.determiner_code)
        if self.id:
            id_elem = ET.SubElement(element, "id")
            id_elem.set("root", self.id)
        if self.code:
            code_elem = ET.SubElement(element, "code")
            code_elem.set("code", self.code)
        if self.name:
            name_elem = ET.SubElement(element, "name")
            name_elem.text = self.name
        if self.desc:
            desc_elem = ET.SubElement(element, "desc")
            desc_elem.text = self.desc
        if self.status_code:
            status_elem = ET.SubElement(element, "statusCode")
            status_elem.set("code", self.status_code)
        if self.effective_time:
            time_elem = ET.SubElement(element, "effectiveTime")
            time_elem.set("value", self.effective_time)
        
        # Serialize additional attributes
        if self.null_flavor:
            element.set("nullFlavor", self.null_flavor)
        if self.negation_ind is not None:
            element.set("negationInd", str(self.negation_ind).lower())
        if self.confidentiality_code:
            conf_elem = ET.SubElement(element, "confidentialityCode")
            conf_elem.set("code", self.confidentiality_code)
        
        # Serialize roles
        for role in self.roles:
            role_elem = role.to_xml("role")
            element.append(role_elem)
        
        logger.debug(f"[{current_time}] Entity XML serialization completed")
        return element
    
    @classmethod
    def from_xml(cls, element: ET.Element) -> "Entity":
        """
        Deserialize Entity from XML element.
        
        Args:
            element: XML Element
            
        Returns:
            Entity instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Entity XML deserialization")
        
        entity = cls()
        
        entity.class_code = element.get("classCode")
        entity.determiner_code = element.get("determinerCode")
        entity.null_flavor = element.get("nullFlavor")
        
        # Parse negationInd
        neg_ind = element.get("negationInd")
        if neg_ind:
            entity.negation_ind = neg_ind.lower() == "true"
        
        # Parse id
        id_elem = element.find(".//id")
        if id_elem is not None:
            entity.id = id_elem.get("root")
        
        # Parse code
        code_elem = element.find(".//code")
        if code_elem is not None:
            entity.code = code_elem.get("code")
        
        # Parse name
        name_elem = element.find(".//name")
        if name_elem is not None and name_elem.text:
            entity.name = name_elem.text
        
        # Parse desc
        desc_elem = element.find(".//desc")
        if desc_elem is not None and desc_elem.text:
            entity.desc = desc_elem.text
        
        # Parse statusCode
        status_elem = element.find(".//statusCode")
        if status_elem is not None:
            entity.status_code = status_elem.get("code")
        
        # Parse effectiveTime
        time_elem = element.find(".//effectiveTime")
        if time_elem is not None:
            entity.effective_time = time_elem.get("value")
        
        # Parse confidentialityCode
        conf_elem = element.find(".//confidentialityCode")
        if conf_elem is not None:
            entity.confidentiality_code = conf_elem.get("code")
        
        # Parse roles
        role_elems = element.findall(".//role")
        for role_elem in role_elems:
            role = Role.from_xml(role_elem)
            entity.add_role(role)
        
        logger.debug(f"[{current_time}] Entity XML deserialization completed")
        return entity


@dataclass
class Role:
    """
    RIM Role class - represents a function or capacity of an entity.
    
    Roles define how entities participate in acts.
    Examples: Patient, Provider, Author, Performer, etc.
    """
    # Core attributes
    class_code: Optional[str] = None  # Classification of the role
    id: Optional[str] = None  # Unique identifier
    code: Optional[str] = None  # Coded classification
    status_code: Optional[str] = None  # Status of the role
    effective_time: Optional[str] = None  # Time period when role is valid
    
    # Additional commonly used attributes
    null_flavor: Optional[str] = None  # Null flavor (e.g., NI, UNK, NINF, PINF)
    negation_ind: Optional[bool] = None  # Negation indicator
    
    # Relationships
    entity: Optional[Entity] = None  # Entity that plays this role
    role_links: List["RoleLink"] = field(default_factory=list)  # Links to other roles
    participations: List["Participation"] = field(default_factory=list)  # Participations in acts
    
    def add_role_link(self, role_link: "RoleLink") -> None:
        """
        Add a role link to another role.
        
        Args:
            role_link: RoleLink instance to add
        """
        self.role_links.append(role_link)
    
    def add_participation(self, participation: "Participation") -> None:
        """
        Add a participation in an act.
        
        Args:
            participation: Participation instance to add
        """
        self.participations.append(participation)
        participation.role = self
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate Role instance against HL7 v3 RIM constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate effective_time format if present
        if self.effective_time:
            if not isinstance(self.effective_time, str):
                errors.append("Role.effective_time must be a string")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Role validation completed with {len(errors)} errors")
        
        return len(errors) == 0, errors
    
    def to_xml(self, element_name: str = "role") -> ET.Element:
        """
        Serialize Role to XML element.
        
        Args:
            element_name: XML element name (default: "role")
            
        Returns:
            XML Element
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Role XML serialization")
        
        element = ET.Element(element_name)
        element.set("xmlns", HL7V3_NAMESPACE)
        
        if self.class_code:
            element.set("classCode", self.class_code)
        if self.null_flavor:
            element.set("nullFlavor", self.null_flavor)
        if self.negation_ind is not None:
            element.set("negationInd", str(self.negation_ind).lower())
        if self.id:
            id_elem = ET.SubElement(element, "id")
            id_elem.set("root", self.id)
        if self.code:
            code_elem = ET.SubElement(element, "code")
            code_elem.set("code", self.code)
        if self.status_code:
            status_elem = ET.SubElement(element, "statusCode")
            status_elem.set("code", self.status_code)
        if self.effective_time:
            time_elem = ET.SubElement(element, "effectiveTime")
            time_elem.set("value", self.effective_time)
        
        # Serialize role links
        for role_link in self.role_links:
            link_elem = role_link.to_xml("roleLink")
            element.append(link_elem)
        
        logger.debug(f"[{current_time}] Role XML serialization completed")
        return element
    
    @classmethod
    def from_xml(cls, element: ET.Element) -> "Role":
        """
        Deserialize Role from XML element.
        
        Args:
            element: XML Element
            
        Returns:
            Role instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Role XML deserialization")
        
        role = cls()
        
        role.class_code = element.get("classCode")
        role.null_flavor = element.get("nullFlavor")
        
        # Parse negationInd
        neg_ind = element.get("negationInd")
        if neg_ind:
            role.negation_ind = neg_ind.lower() == "true"
        
        # Parse id
        id_elem = element.find(".//id")
        if id_elem is not None:
            role.id = id_elem.get("root")
        
        # Parse code
        code_elem = element.find(".//code")
        if code_elem is not None:
            role.code = code_elem.get("code")
        
        # Parse statusCode
        status_elem = element.find(".//statusCode")
        if status_elem is not None:
            role.status_code = status_elem.get("code")
        
        # Parse effectiveTime
        time_elem = element.find(".//effectiveTime")
        if time_elem is not None:
            role.effective_time = time_elem.get("value")
        
        # Parse role links
        link_elems = element.findall(".//roleLink")
        for link_elem in link_elems:
            role_link = RoleLink.from_xml(link_elem)
            role.add_role_link(role_link)
        
        logger.debug(f"[{current_time}] Role XML deserialization completed")
        return role


@dataclass
class Act:
    """
    RIM Act class - represents an action or event.
    
    Acts are things that happen or are done.
    Examples: Observation, Procedure, Medication, Encounter, etc.
    """
    # Core attributes
    class_code: Optional[str] = None  # Classification of the act
    mood_code: Optional[str] = None  # Mood (e.g., INT, EVN, RQO, PRMS)
    id: Optional[str] = None  # Unique identifier
    code: Optional[str] = None  # Coded classification
    status_code: Optional[str] = None  # Status of the act
    effective_time: Optional[str] = None  # Time when act occurred/is valid
    text: Optional[str] = None  # Human-readable text
    
    # Additional commonly used attributes
    null_flavor: Optional[str] = None  # Null flavor (e.g., NI, UNK, NINF, PINF)
    negation_ind: Optional[bool] = None  # Negation indicator
    confidentiality_code: Optional[str] = None  # Confidentiality code
    
    # Relationships
    participations: List["Participation"] = field(default_factory=list)  # Entities participating
    act_relationships: List["ActRelationship"] = field(default_factory=list)  # Related acts
    
    def add_participation(self, participation: "Participation") -> None:
        """
        Add a participation to this act.
        
        Args:
            participation: Participation instance to add
        """
        self.participations.append(participation)
        participation.act = self
    
    def add_act_relationship(self, relationship: "ActRelationship") -> None:
        """
        Add a relationship to another act.
        
        Args:
            relationship: ActRelationship instance to add
        """
        self.act_relationships.append(relationship)
        relationship.source_act = self
    
    def get_participations(self, type_code: Optional[str] = None) -> List["Participation"]:
        """
        Get participations, optionally filtered by type code.
        
        Args:
            type_code: Optional participation type code to filter by
            
        Returns:
            List of matching participations
        """
        if type_code is None:
            return self.participations
        return [p for p in self.participations if p.type_code == type_code]
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate Act instance against HL7 v3 RIM constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # classCode is typically required
        # (but not enforced here as it depends on context)
        
        # Validate effective_time format if present
        if self.effective_time:
            if not isinstance(self.effective_time, str):
                errors.append("Act.effective_time must be a string")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Act validation completed with {len(errors)} errors")
        
        return len(errors) == 0, errors
    
    def to_xml(self, element_name: str = "act") -> ET.Element:
        """
        Serialize Act to XML element.
        
        Args:
            element_name: XML element name (default: "act")
            
        Returns:
            XML Element
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Act XML serialization")
        
        element = ET.Element(element_name)
        element.set("xmlns", HL7V3_NAMESPACE)
        
        if self.class_code:
            element.set("classCode", self.class_code)
        if self.mood_code:
            element.set("moodCode", self.mood_code)
        if self.null_flavor:
            element.set("nullFlavor", self.null_flavor)
        if self.negation_ind is not None:
            element.set("negationInd", str(self.negation_ind).lower())
        if self.id:
            id_elem = ET.SubElement(element, "id")
            id_elem.set("root", self.id)
        if self.code:
            code_elem = ET.SubElement(element, "code")
            code_elem.set("code", self.code)
        if self.status_code:
            status_elem = ET.SubElement(element, "statusCode")
            status_elem.set("code", self.status_code)
        if self.effective_time:
            time_elem = ET.SubElement(element, "effectiveTime")
            time_elem.set("value", self.effective_time)
        if self.text:
            text_elem = ET.SubElement(element, "text")
            text_elem.text = self.text
        if self.confidentiality_code:
            conf_elem = ET.SubElement(element, "confidentialityCode")
            conf_elem.set("code", self.confidentiality_code)
        
        # Serialize participations
        for participation in self.participations:
            part_elem = participation.to_xml("participation")
            element.append(part_elem)
        
        # Serialize act relationships
        for relationship in self.act_relationships:
            rel_elem = relationship.to_xml("actRelationship")
            element.append(rel_elem)
        
        logger.debug(f"[{current_time}] Act XML serialization completed")
        return element
    
    @classmethod
    def from_xml(cls, element: ET.Element) -> "Act":
        """
        Deserialize Act from XML element.
        
        Args:
            element: XML Element
            
        Returns:
            Act instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Act XML deserialization")
        
        act = cls()
        
        act.class_code = element.get("classCode")
        act.mood_code = element.get("moodCode")
        act.null_flavor = element.get("nullFlavor")
        
        # Parse negationInd
        neg_ind = element.get("negationInd")
        if neg_ind:
            act.negation_ind = neg_ind.lower() == "true"
        
        # Parse id
        id_elem = element.find(".//id")
        if id_elem is not None:
            act.id = id_elem.get("root")
        
        # Parse code
        code_elem = element.find(".//code")
        if code_elem is not None:
            act.code = code_elem.get("code")
        
        # Parse statusCode
        status_elem = element.find(".//statusCode")
        if status_elem is not None:
            act.status_code = status_elem.get("code")
        
        # Parse effectiveTime
        time_elem = element.find(".//effectiveTime")
        if time_elem is not None:
            act.effective_time = time_elem.get("value")
        
        # Parse text
        text_elem = element.find(".//text")
        if text_elem is not None and text_elem.text:
            act.text = text_elem.text
        
        # Parse confidentialityCode
        conf_elem = element.find(".//confidentialityCode")
        if conf_elem is not None:
            act.confidentiality_code = conf_elem.get("code")
        
        # Parse participations
        part_elems = element.findall(".//participation")
        for part_elem in part_elems:
            participation = Participation.from_xml(part_elem)
            act.add_participation(participation)
        
        # Parse act relationships
        rel_elems = element.findall(".//actRelationship")
        for rel_elem in rel_elems:
            relationship = ActRelationship.from_xml(rel_elem)
            act.add_act_relationship(relationship)
        
        logger.debug(f"[{current_time}] Act XML deserialization completed")
        return act


@dataclass
class Participation:
    """
    RIM Participation class - represents the involvement of an entity in an act.
    
    Participations link entities (via roles) to acts.
    Examples: Author, Performer, Subject, Location, etc.
    """
    # Core attributes
    type_code: Optional[str] = None  # Type of participation (e.g., AUT, PRF, SBJ)
    context_control_code: Optional[str] = None  # Context control (e.g., OP, AP)
    sequence_number: Optional[int] = None  # Ordering of participations
    
    # Relationships
    act: Optional[Act] = None  # Act being participated in
    role: Optional[Role] = None  # Role participating
    
    # Time and status
    time: Optional[str] = None  # Time of participation
    status_code: Optional[str] = None  # Status of participation
    
    def get_entity(self) -> Optional[Entity]:
        """
        Get the entity participating (via role).
        
        Returns:
            Entity instance or None
        """
        return self.role.entity if self.role else None
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate Participation instance against HL7 v3 RIM constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # typeCode is typically required
        if not self.type_code:
            errors.append("Participation.type_code is required")
        
        # Validate time format if present
        if self.time:
            if not isinstance(self.time, str):
                errors.append("Participation.time must be a string")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Participation validation completed with {len(errors)} errors")
        
        return len(errors) == 0, errors
    
    def to_xml(self, element_name: str = "participation") -> ET.Element:
        """
        Serialize Participation to XML element.
        
        Args:
            element_name: XML element name (default: "participation")
            
        Returns:
            XML Element
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Participation XML serialization")
        
        element = ET.Element(element_name)
        element.set("xmlns", HL7V3_NAMESPACE)
        
        if self.type_code:
            element.set("typeCode", self.type_code)
        if self.context_control_code:
            element.set("contextControlCode", self.context_control_code)
        if self.sequence_number is not None:
            element.set("sequenceNumber", str(self.sequence_number))
        if self.time:
            time_elem = ET.SubElement(element, "time")
            time_elem.set("value", self.time)
        if self.status_code:
            status_elem = ET.SubElement(element, "statusCode")
            status_elem.set("code", self.status_code)
        
        # Serialize role if present
        if self.role:
            role_elem = self.role.to_xml("role")
            element.append(role_elem)
        
        logger.debug(f"[{current_time}] Participation XML serialization completed")
        return element
    
    @classmethod
    def from_xml(cls, element: ET.Element) -> "Participation":
        """
        Deserialize Participation from XML element.
        
        Args:
            element: XML Element
            
        Returns:
            Participation instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting Participation XML deserialization")
        
        participation = cls()
        
        participation.type_code = element.get("typeCode")
        participation.context_control_code = element.get("contextControlCode")
        
        seq_num = element.get("sequenceNumber")
        if seq_num:
            try:
                participation.sequence_number = int(seq_num)
            except ValueError:
                pass
        
        # Parse time
        time_elem = element.find(".//time")
        if time_elem is not None:
            participation.time = time_elem.get("value")
        
        # Parse statusCode
        status_elem = element.find(".//statusCode")
        if status_elem is not None:
            participation.status_code = status_elem.get("code")
        
        # Parse role
        role_elem = element.find(".//role")
        if role_elem is not None:
            participation.role = Role.from_xml(role_elem)
        
        logger.debug(f"[{current_time}] Participation XML deserialization completed")
        return participation


@dataclass
class ActRelationship:
    """
    RIM ActRelationship class - represents relationships between acts.
    
    ActRelationships link acts to other acts.
    Examples: HasComponent, HasSupport, RefersTo, etc.
    """
    # Core attributes
    type_code: Optional[str] = None  # Type of relationship (e.g., COMP, REFR, SUBJ)
    context_control_code: Optional[str] = None  # Context control (e.g., OP, AP)
    sequence_number: Optional[int] = None  # Ordering of relationships
    
    # Relationships
    source_act: Optional[Act] = None  # Source act
    target_act: Optional[Act] = None  # Target act
    
    # Time and status
    effective_time: Optional[str] = None  # Time when relationship is valid
    status_code: Optional[str] = None  # Status of relationship
    
    def set_target_act(self, target: Act) -> None:
        """
        Set the target act for this relationship.
        
        Args:
            target: Target Act instance
        """
        self.target_act = target
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate ActRelationship instance against HL7 v3 RIM constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # typeCode is typically required
        if not self.type_code:
            errors.append("ActRelationship.type_code is required")
        
        # Validate effective_time format if present
        if self.effective_time:
            if not isinstance(self.effective_time, str):
                errors.append("ActRelationship.effective_time must be a string")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] ActRelationship validation completed with {len(errors)} errors")
        
        return len(errors) == 0, errors
    
    def to_xml(self, element_name: str = "actRelationship") -> ET.Element:
        """
        Serialize ActRelationship to XML element.
        
        Args:
            element_name: XML element name (default: "actRelationship")
            
        Returns:
            XML Element
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting ActRelationship XML serialization")
        
        element = ET.Element(element_name)
        element.set("xmlns", HL7V3_NAMESPACE)
        
        if self.type_code:
            element.set("typeCode", self.type_code)
        if self.context_control_code:
            element.set("contextControlCode", self.context_control_code)
        if self.sequence_number is not None:
            element.set("sequenceNumber", str(self.sequence_number))
        if self.effective_time:
            time_elem = ET.SubElement(element, "effectiveTime")
            time_elem.set("value", self.effective_time)
        if self.status_code:
            status_elem = ET.SubElement(element, "statusCode")
            status_elem.set("code", self.status_code)
        
        # Serialize target act if present
        if self.target_act:
            target_elem = self.target_act.to_xml("act")
            element.append(target_elem)
        
        logger.debug(f"[{current_time}] ActRelationship XML serialization completed")
        return element
    
    @classmethod
    def from_xml(cls, element: ET.Element) -> "ActRelationship":
        """
        Deserialize ActRelationship from XML element.
        
        Args:
            element: XML Element
            
        Returns:
            ActRelationship instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting ActRelationship XML deserialization")
        
        relationship = cls()
        
        relationship.type_code = element.get("typeCode")
        relationship.context_control_code = element.get("contextControlCode")
        
        seq_num = element.get("sequenceNumber")
        if seq_num:
            try:
                relationship.sequence_number = int(seq_num)
            except ValueError:
                pass
        
        # Parse effectiveTime
        time_elem = element.find(".//effectiveTime")
        if time_elem is not None:
            relationship.effective_time = time_elem.get("value")
        
        # Parse statusCode
        status_elem = element.find(".//statusCode")
        if status_elem is not None:
            relationship.status_code = status_elem.get("code")
        
        # Parse target act
        act_elem = element.find(".//act")
        if act_elem is not None:
            relationship.target_act = Act.from_xml(act_elem)
        
        logger.debug(f"[{current_time}] ActRelationship XML deserialization completed")
        return relationship


@dataclass
class RoleLink:
    """
    RIM RoleLink class - represents relationships between roles.
    
    RoleLinks connect roles to other roles.
    Examples: RelatedTo, Replaces, etc.
    """
    # Core attributes
    type_code: Optional[str] = None  # Type of link (e.g., REL, RPLC)
    
    # Relationships
    source_role: Optional[Role] = None  # Source role
    target_role: Optional[Role] = None  # Target role
    
    # Time and status
    effective_time: Optional[str] = None  # Time when link is valid
    status_code: Optional[str] = None  # Status of link
    
    def set_source_role(self, role: Role) -> None:
        """
        Set the source role for this link.
        
        Args:
            role: Source Role instance
        """
        self.source_role = role
        role.add_role_link(self)
    
    def set_target_role(self, role: Role) -> None:
        """
        Set the target role for this link.
        
        Args:
            role: Target Role instance
        """
        self.target_role = role
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate RoleLink instance against HL7 v3 RIM constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # typeCode is typically required
        if not self.type_code:
            errors.append("RoleLink.type_code is required")
        
        # Validate effective_time format if present
        if self.effective_time:
            if not isinstance(self.effective_time, str):
                errors.append("RoleLink.effective_time must be a string")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] RoleLink validation completed with {len(errors)} errors")
        
        return len(errors) == 0, errors
    
    def to_xml(self, element_name: str = "roleLink") -> ET.Element:
        """
        Serialize RoleLink to XML element.
        
        Args:
            element_name: XML element name (default: "roleLink")
            
        Returns:
            XML Element
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting RoleLink XML serialization")
        
        element = ET.Element(element_name)
        element.set("xmlns", HL7V3_NAMESPACE)
        
        if self.type_code:
            element.set("typeCode", self.type_code)
        if self.effective_time:
            time_elem = ET.SubElement(element, "effectiveTime")
            time_elem.set("value", self.effective_time)
        if self.status_code:
            status_elem = ET.SubElement(element, "statusCode")
            status_elem.set("code", self.status_code)
        
        # Serialize target role if present
        if self.target_role:
            target_elem = self.target_role.to_xml("role")
            element.append(target_elem)
        
        logger.debug(f"[{current_time}] RoleLink XML serialization completed")
        return element
    
    @classmethod
    def from_xml(cls, element: ET.Element) -> "RoleLink":
        """
        Deserialize RoleLink from XML element.
        
        Args:
            element: XML Element
            
        Returns:
            RoleLink instance
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Starting RoleLink XML deserialization")
        
        role_link = cls()
        
        role_link.type_code = element.get("typeCode")
        
        # Parse effectiveTime
        time_elem = element.find(".//effectiveTime")
        if time_elem is not None:
            role_link.effective_time = time_elem.get("value")
        
        # Parse statusCode
        status_elem = element.find(".//statusCode")
        if status_elem is not None:
            role_link.status_code = status_elem.get("code")
        
        # Parse target role
        role_elem = element.find(".//role")
        if role_elem is not None:
            role_link.target_role = Role.from_xml(role_elem)
        
        logger.debug(f"[{current_time}] RoleLink XML deserialization completed")
        return role_link


# RIM relationship helper functions


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")
def create_entity_role_relationship(entity: Entity, role: Role) -> None:
    """
    Create a relationship between an entity and a role.
    
    Args:
        entity: Entity instance
        role: Role instance

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    """
    entity.add_role(role)


def create_role_act_participation(role: Role, act: Act, type_code: str) -> Participation:
    """
    Create a participation linking a role to an act.
    
    Args:
        role: Role instance
        act: Act instance
        type_code: Participation type code
        
    Returns:

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        Created Participation instance
    """
    participation = Participation(type_code=type_code)
    act.add_participation(participation)
    role.add_participation(participation)
    return participation


def create_act_relationship(source: Act, target: Act, type_code: str) -> ActRelationship:
    """
    Create a relationship between two acts.
    
    Args:
        source: Source Act instance

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
        target: Target Act instance
        type_code: Relationship type code
        
    Returns:
        Created ActRelationship instance
    """
    relationship = ActRelationship(type_code=type_code)
    source.add_act_relationship(relationship)
    relationship.set_target_act(target)
    return relationship


def create_role_link(source: Role, target: Role, type_code: str) -> RoleLink:
    """
    Create a link between two roles.
    
    Args:
        source: Source Role instance
        target: Target Role instance
        type_code: Link type code
        
    Returns:
        Created RoleLink instance
    """
    role_link = RoleLink(type_code=type_code)
    role_link.set_source_role(source)
    role_link.set_target_role(target)
    return role_link
