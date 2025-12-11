# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

import logging
"""
FHIR R4 GraphQL Support.

Provides GraphQL schema generation, query parsing, and query execution for FHIR resources.
All operations include timestamps in logs for traceability.

This implementation follows the FHIR GraphQL specification:
https://www.hl7.org/fhir/graphql.html
"""

import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.resources.observation import Observation
from dnhealth.dnhealth_fhir.resources.encounter import Encounter
from dnhealth.dnhealth_fhir.resources.bundle import Bundle
from dnhealth.dnhealth_fhir.resources.condition import Condition
from dnhealth.dnhealth_fhir.parser_json import parse_resource
from dnhealth.dnhealth_fhir.serializer_json import serialize_resource
from dnhealth.util.logging import get_logger

logger = logging.getLogger(__name__)

logger = get_logger(__name__)

# Test timeout limit: 5 minutes
TEST_TIMEOUT = 300

# Resource type mapping for GraphQL schema generation
RESOURCE_TYPE_MAP = {
    "Patient": Patient,
    "Observation": Observation,
    "Encounter": Encounter,
    "Bundle": Bundle,
    "Condition": Condition,
    # Add more resource types as needed
}


@dataclass
class GraphQLField:
    """
    Represents a GraphQL field definition.
    
    Attributes:
        name: Field name
        type: Field type (String, Int, Boolean, ResourceType, [Type], etc.)
        description: Field description
        arguments: Field arguments (for queries)
        is_list: Whether field is a list
        is_required: Whether field is required
    """
    name: str
    type: str
    description: Optional[str] = None
    arguments: Dict[str, str] = field(default_factory=dict)  # arg_name -> arg_type
    is_list: bool = False
    is_required: bool = False


@dataclass
class GraphQLType:
    """
    Represents a GraphQL type definition.
    
    Attributes:
        name: Type name
        fields: List of fields in this type
        description: Type description
    """
    name: str
    fields: List[GraphQLField] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class GraphQLQueryNode:
    """
    Represents a node in a GraphQL query AST.
    
    Attributes:
        field_name: Name of the field being queried
        alias: Optional alias for the field
        arguments: Query arguments
        selections: Nested field selections
    """
    field_name: str
    alias: Optional[str] = None
    arguments: Dict[str, Any] = field(default_factory=dict)
    selections: List["GraphQLQueryNode"] = field(default_factory=list)


class GraphQLSchemaGenerator:
    """
    Generates GraphQL schema from FHIR resource definitions.
    
    Follows FHIR GraphQL specification for schema generation.
    """
    
    def __init__(self):
        """Initialize the schema generator."""
        self.types: Dict[str, GraphQLType] = {}
        self.query_type: Optional[GraphQLType] = None
        self.mutation_type: Optional[GraphQLType] = None
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Initialize base GraphQL schema."""
        # Create Query type
        query_fields = []
        
        # Add resource query fields (e.g., Patient, Observation, etc.)
        for resource_type in RESOURCE_TYPE_MAP.keys():
            query_fields.append(GraphQLField(
                name=resource_type.lower(),
                type=resource_type,
                description=f"Query {resource_type} resources",
                arguments={
                    "id": "ID",
                    "_id": "String",
                    "_lastUpdated": "String",
                    "_tag": "String",
                    "_profile": "String",
                    "_security": "String",
                    "_source": "String",
                    "_content": "String",
                    "_text": "String",
                    "_list": "String",
                    "_has": "String",
                    "_type": "String",
                    "_count": "Int",
                    "_offset": "Int",
                    "_sort": "String",
                    "_summary": "String",
                    "_elements": "String",
                    "_include": "String",
                    "_revInclude": "String",
                }
            ))
        
        self.query_type = GraphQLType(
            name="Query",
            fields=query_fields,
            description="Root query type for FHIR resources"
        )
        
        # Create Mutation type
        mutation_fields = []
        for resource_type in RESOURCE_TYPE_MAP.keys():
            mutation_fields.append(GraphQLField(
                name=f"create{resource_type}",
                type=resource_type,
                description=f"Create a {resource_type} resource",
                arguments={
                    "resource": resource_type
                }
            ))
            mutation_fields.append(GraphQLField(
                name=f"update{resource_type}",
                type=resource_type,
                description=f"Update a {resource_type} resource",
                arguments={
                    "id": "ID!",
                    "resource": resource_type
                }
            ))
            mutation_fields.append(GraphQLField(
                name=f"delete{resource_type}",
                type="Boolean",
                description=f"Delete a {resource_type} resource",
                arguments={
                    "id": "ID!"
                }
            ))
        
        self.mutation_type = GraphQLType(
            name="Mutation",
            fields=mutation_fields,
            description="Root mutation type for FHIR resources"
        )
        
        # Generate types for each resource
        for resource_type, resource_class in RESOURCE_TYPE_MAP.items():
            self._generate_resource_type(resource_type, resource_class)
    
    def _generate_resource_type(self, resource_type: str, resource_class: type):
        """
        Generate GraphQL type definition for a FHIR resource.
        
        Args:
            resource_type: Resource type name
            resource_class: Resource class
        """
        fields = []
        
        # Get all fields from resource class
        if hasattr(resource_class, "__dataclass_fields__"):
            for field_name, field_info in resource_class.__dataclass_fields__.items():
                if field_name.startswith("_"):
                    continue  # Skip internal fields
                
                # Determine GraphQL type
                graphql_type = self._get_graphql_type(field_info.type, field_name)
                
                # Check if field is a list
                is_list = self._is_list_type(field_info.type)
                
                # Check if field is required
                is_required = field_info.default == field_info.default_factory == None
                
                fields.append(GraphQLField(
                    name=field_name,
                    type=graphql_type,
                    description=f"{resource_type}.{field_name}",
                    is_list=is_list,
                    is_required=is_required
                ))
        
        self.types[resource_type] = GraphQLType(
            name=resource_type,
            fields=fields,
            description=f"FHIR {resource_type} resource"
        )
    
    def _get_graphql_type(self, python_type: type, field_name: str) -> str:
        """
        Convert Python type to GraphQL type.
        
        Args:
            python_type: Python type annotation
            field_name: Field name (for context)
            
        Returns:
            GraphQL type string
        """
        # Handle Optional types
        if hasattr(python_type, "__origin__"):
            origin = python_type.__origin__
            if origin is Union:
                # Get non-None type
                args = python_type.__args__
                non_none_types = [t for t in args if t is not type(None)]
                if non_none_types:
                    return self._get_graphql_type(non_none_types[0], field_name)
        
        # Map Python types to GraphQL types
        type_mapping = {
            str: "String",
            int: "Int",
            float: "Float",
            bool: "Boolean",
        }
        
        if python_type in type_mapping:
            return type_mapping[python_type]
        
        # Check if it's a list
        if self._is_list_type(python_type):
            return "String"  # Default to String for lists
        
        # Check if it's a FHIR resource type
        if hasattr(python_type, "__name__"):
            type_name = python_type.__name__
            if type_name in RESOURCE_TYPE_MAP:
                return type_name
        
        # Default to String for unknown types
        return "String"
    
    def _is_list_type(self, python_type: type) -> bool:
        """Check if a Python type is a list."""
        if hasattr(python_type, "__origin__"):
            origin = python_type.__origin__
            if origin is list:
                return True
            elif origin is Union:
                # Check if any union member is a list
                args = python_type.__args__
                return any(self._is_list_type(t) for t in args)
        return False
    
    def generate_schema_string(self) -> str:
        """
        Generate GraphQL schema as SDL (Schema Definition Language) string.
        
        Returns:
            GraphQL schema string
        """
        lines = []
        
        # Add Query type
        if self.query_type:
            lines.append(f"type {self.query_type.name} {{")
            for field in self.query_type.fields:
                field_str = f"  {field.name}"
                if field.arguments:
                    args_str = ", ".join([f"{name}: {type_}" for name, type_ in field.arguments.items()])
                    field_str += f"({args_str})"
                field_type = f"[{field.type}]" if field.is_list else field.type
                field_type += "!" if field.is_required else ""
                field_str += f": {field_type}"
                if field.description:
                    field_str += f" # {field.description}"
                lines.append(field_str)
            lines.append("}")
            lines.append("")
        
        # Add Mutation type
        if self.mutation_type:
            lines.append(f"type {self.mutation_type.name} {{")
            for field in self.mutation_type.fields:
                field_str = f"  {field.name}"
                if field.arguments:
                    args_str = ", ".join([f"{name}: {type_}" for name, type_ in field.arguments.items()])
                    field_str += f"({args_str})"
                field_type = f"[{field.type}]" if field.is_list else field.type
                field_type += "!" if field.is_required else ""
                field_str += f": {field_type}"
                if field.description:
                    field_str += f" # {field.description}"
                lines.append(field_str)
            lines.append("")
            lines.append("")
        
        # Add resource types
        for type_name, graphql_type in sorted(self.types.items()):
            lines.append(f"type {type_name} {{")
            for field in graphql_type.fields:
                field_type = f"[{field.type}]" if field.is_list else field.type
                field_type += "!" if field.is_required else ""
                field_str = f"  {field.name}: {field_type}"
                if field.description:
                    field_str += f" # {field.description}"
                lines.append(field_str)
            lines.append("}")
            lines.append("")
        

                # Log completion timestamp at end of operation
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Current Time at End of Operations: {current_time}")
        return "\n".join(lines)
    
    def get_type(self, type_name: str) -> Optional[GraphQLType]:
        """
        Get a GraphQL type by name.
        
        Args:
            type_name: Type name
            
        Returns:
            GraphQLType if found, None otherwise
        """

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
        return self.types.get(type_name)


class GraphQLQueryParser:
    """
    Parses GraphQL query strings into AST (Abstract Syntax Tree).
    
    Supports basic GraphQL query syntax.
    """
    
    def __init__(self):
        """Initialize the query parser."""
        pass
    
    def parse(self, query: str) -> GraphQLQueryNode:
        """
        Parse a GraphQL query string.
        
        Args:
            query: GraphQL query string
            
        Returns:
            Root GraphQLQueryNode
            
        Raises:
            ValueError: If query is invalid
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] Parsing GraphQL query")
        
        # Remove comments and normalize whitespace
        query = self._clean_query(query)
        
        # Check timeout
        if time.time() - start_time > TEST_TIMEOUT:
            raise TimeoutError(f"Query parsing exceeded timeout of {TEST_TIMEOUT} seconds")
        
        # Parse query
        try:
            root_node = self._parse_query(query)
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Failed to parse GraphQL query: {e}")
            raise ValueError(f"Invalid GraphQL query: {e}") from e
        
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[{current_time}] GraphQL query parsed in {elapsed:.3f}s")
        
        return root_node
    
    def _clean_query(self, query: str) -> str:
        """
        Clean and normalize GraphQL query string.
        
        Args:
            query: Raw query string
            
        Returns:
            Cleaned query string
        """
        # Remove comments (# ... or /* ... */)
        query = re.sub(r'#.*?$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        
        # Normalize whitespace
        query = re.sub(r'\s+', ' ', query)
        query = query.strip()
        
        return query
    
    def _parse_query(self, query: str) -> GraphQLQueryNode:
        """
        Parse GraphQL query into AST.
        
        Args:
            query: Cleaned query string
            
        Returns:
            Root GraphQLQueryNode
        """
        # Simple parser for basic GraphQL queries
        # This is a simplified implementation - full parser would use a proper parser library
        
        # Remove "query" keyword if present
        query = re.sub(r'^\s*query\s+', '', query, flags=re.IGNORECASE)
        query = query.strip()
        
        # Find root field (first field in query)
        # Format: fieldName(args) { selections }
        match = re.match(r'(\w+)(?:\s*:\s*(\w+))?(?:\s*\(([^)]*)\))?\s*(\{.*\})?', query)
        if not match:
            raise ValueError("Invalid query format")
        
        field_name = match.group(1)
        alias = match.group(2)
        args_str = match.group(3) or ""
        selections_str = match.group(4) or ""
        
        # Parse arguments
        arguments = self._parse_arguments(args_str)
        
        # Parse selections
        selections = []
        if selections_str:
            selections = self._parse_selections(selections_str)
        
        return GraphQLQueryNode(
            field_name=field_name,
            alias=alias,
            arguments=arguments,
            selections=selections
        )
    
    def _parse_arguments(self, args_str: str) -> Dict[str, Any]:
        """
        Parse GraphQL arguments string.
        
        Args:
            args_str: Arguments string (e.g., "id: \"123\", name: \"John\"")
            
        Returns:
            Dictionary of argument name -> value
        """
        arguments = {}
        
        if not args_str.strip():
            return arguments
        
        # Simple argument parser
        # Format: name: value, name: value
        pattern = r'(\w+)\s*:\s*([^,]+)'
        matches = re.findall(pattern, args_str)
        
        for name, value in matches:
            value = value.strip()
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Try to parse as number or boolean
            elif value.isdigit():
                value = int(value)
            elif value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            
            arguments[name] = value
        
        return arguments
    
    def _parse_selections(self, selections_str: str) -> List[GraphQLQueryNode]:
        """
        Parse GraphQL field selections.
        
        Args:
            selections_str: Selections string (e.g., "{ id name address { city } }")
            
        Returns:
            List of GraphQLQueryNode objects
        """
        selections = []
        
        # Remove outer braces
        selections_str = selections_str.strip()
        if selections_str.startswith('{'):
            selections_str = selections_str[1:]
        if selections_str.endswith('}'):
            selections_str = selections_str[:-1]
        selections_str = selections_str.strip()
        
        if not selections_str:
            return selections
        
        # Simple selection parser
        # Split by fields (handling nested selections)
        depth = 0
        current_field = ""
        for char in selections_str:
            if char == '{':
                depth += 1
                current_field += char
            elif char == '}':
                depth -= 1
                current_field += char
            elif char == ' ' and depth == 0:
                if current_field.strip():
                    # Parse field
                    field_node = self._parse_field_selection(current_field.strip())
                    if field_node:
                        selections.append(field_node)
                    current_field = ""
                continue
            else:
                current_field += char
        
        # Parse last field
        if current_field.strip():
            field_node = self._parse_field_selection(current_field.strip())
            if field_node:
                selections.append(field_node)
        
        return selections
    
    def _parse_field_selection(self, field_str: str) -> Optional[GraphQLQueryNode]:
        """
        Parse a single field selection.
        
        Args:
            field_str: Field string (e.g., "id" or "address { city }")
            
        Returns:
            GraphQLQueryNode or None
        """
        # Check for nested selections
        if '{' in field_str:
            # Has nested selections
            match = re.match(r'(\w+)(?:\s*:\s*(\w+))?(?:\s*\(([^)]*)\))?\s*(\{.*\})', field_str)
            if match:
                field_name = match.group(1)
                alias = match.group(2)
                args_str = match.group(3) or ""
                selections_str = match.group(4) or ""
                
                arguments = self._parse_arguments(args_str)
                selections = self._parse_selections(selections_str)
                

            # Log completion timestamp at end of operation
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Current Time at End of Operations: {current_time}")
                return GraphQLQueryNode(
                    field_name=field_name,
                    alias=alias,
                    arguments=arguments,
                    selections=selections
                )
        else:
            # Simple field
            match = re.match(r'(\w+)(?:\s*:\s*(\w+))?', field_str)
            if match:
                field_name = match.group(1)
                alias = match.group(2)
                
                return GraphQLQueryNode(
                    field_name=field_name,
                    alias=alias,
                    arguments={},
                    selections=[]
                )
        
        return None


class GraphQLExecutor:
    """
    Executes GraphQL queries against FHIR resources.
    
    Supports query execution with resource filtering and field selection.
    """
    
    def __init__(self, storage: Optional[Any] = None):
        """
        Initialize the GraphQL executor.
        
        Args:
            storage: Optional storage backend for retrieving resources
                    (must have search() and get() methods)
        """
        self.storage = storage
        self.schema_generator = GraphQLSchemaGenerator()
        self.query_parser = GraphQLQueryParser()
    
    def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query.
        
        Args:
            query: GraphQL query string
            variables: Optional query variables
            
        Returns:
            Query result as dictionary
            
        Raises:
            ValueError: If query is invalid
            TimeoutError: If execution exceeds timeout
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Executing GraphQL query")
        
        # Check timeout
        if time.time() - start_time > TEST_TIMEOUT:
            raise TimeoutError(f"Query execution exceeded timeout of {TEST_TIMEOUT} seconds")
        
        # Parse query
        try:
            query_node = self.query_parser.parse(query)
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Failed to parse GraphQL query: {e}")
            raise ValueError(f"Invalid GraphQL query: {e}") from e
        
        # Execute query
        try:
            result = self._execute_query_node(query_node, variables or {})
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Failed to execute GraphQL query: {e}")
            raise ValueError(f"Query execution failed: {e}") from e
        
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] GraphQL query executed in {elapsed:.3f}s")
        
        return result
    
    def _execute_query_node(self, node: GraphQLQueryNode, variables: Dict[str, Any]) -> Any:
        """
        Execute a GraphQL query node.
        
        Args:
            node: GraphQLQueryNode to execute
            variables: Query variables
            
        Returns:
            Query result
        """
        # Check timeout
        if time.time() > TEST_TIMEOUT:
            raise TimeoutError(f"Query execution exceeded timeout of {TEST_TIMEOUT} seconds")
        
        field_name = node.field_name
        
        # Check if it's a resource query (e.g., "patient", "observation")
        resource_type = self._get_resource_type_from_field(field_name)
        
        if resource_type:
            # Execute resource query
            return self._execute_resource_query(resource_type, node, variables)
        else:
            # Field selection (for nested queries)
            return self._execute_field_selection(node, variables)
    
    def _get_resource_type_from_field(self, field_name: str) -> Optional[str]:
        """
        Get resource type from GraphQL field name.
        
        Args:
            field_name: GraphQL field name (e.g., "patient" -> "Patient")
            
        Returns:
            Resource type name or None
        """
        # Capitalize first letter
        resource_type = field_name.capitalize()
        
        if resource_type in RESOURCE_TYPE_MAP:
            return resource_type
        
        return None
    
    def _execute_resource_query(self, resource_type: str, node: GraphQLQueryNode, variables: Dict[str, Any]) -> Any:
        """
        Execute a resource query.
        
        Args:
            resource_type: FHIR resource type
            node: GraphQL query node
            variables: Query variables
            
        Returns:
            Query result (resource or list of resources)
        """
        # Get resources from storage
        if not self.storage:
            # No storage - return empty result
            return []
        
        # Extract query arguments
        args = node.arguments.copy()
        
        # Handle ID query
        if "id" in args:
            resource_id = args["id"]
            resource = self.storage.get(resource_type, resource_id)
            if resource:
                return self._select_fields(resource, node.selections)
            return None
        
        # Handle search query
        # Convert GraphQL arguments to search parameters
        search_params = {}
        for key, value in args.items():
            if key.startswith("_"):
                search_params[key] = value
        
        # Execute search
        resources = self.storage.search(resource_type, search_params)
        
        # Select fields
        if node.selections:
            return [self._select_fields(resource, node.selections) for resource in resources]
        else:
            return resources
    
    def _execute_field_selection(self, node: GraphQLQueryNode, variables: Dict[str, Any]) -> Any:
        """
        Execute a field selection (nested query).
        
        Args:
            node: GraphQL query node
            variables: Query variables
            
        Returns:
            Field value
        """
        # This would be called for nested field selections
        # For now, return the field name as placeholder
        return node.field_name
    
    def _select_fields(self, resource: FHIRResource, selections: List[GraphQLQueryNode]) -> Dict[str, Any]:
        """
        Select fields from a resource based on GraphQL selections.
        
        Args:
            resource: FHIR resource
            selections: List of field selections
            
        Returns:
            Dictionary with selected fields
        """
        result = {}
        
        if not selections:
            # No selections - return all fields
            return serialize_resource(resource)
        
        for selection in selections:
            field_name = selection.field_name
            alias = selection.alias or field_name
            
            # Get field value from resource
            if hasattr(resource, field_name):
                value = getattr(resource, field_name)
                
                # Handle nested selections
                if selection.selections:
                    if isinstance(value, list):
                        value = [self._select_fields(item, selection.selections) for item in value if hasattr(item, "__dict__")]
                    elif hasattr(value, "__dict__"):
                        value = self._select_fields(value, selection.selections)
                
                result[alias] = value
        
        return result
    
    def execute_mutation(self, mutation: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL mutation.
        
        Args:
            mutation: GraphQL mutation string
            variables: Optional mutation variables
            
        Returns:
            Mutation result
            
        Raises:
            ValueError: If mutation is invalid
            TimeoutError: If execution exceeds timeout
        """
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Executing GraphQL mutation")
        
        # Check timeout
        if time.time() - start_time > TEST_TIMEOUT:
            raise TimeoutError(f"Mutation execution exceeded timeout of {TEST_TIMEOUT} seconds")
        
        # Parse mutation
        try:
            mutation_node = self.query_parser.parse(mutation)
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Failed to parse GraphQL mutation: {e}")
            raise ValueError(f"Invalid GraphQL mutation: {e}") from e
        
        # Execute mutation
        try:
            result = self._execute_mutation_node(mutation_node, variables or {})
        except Exception as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"[{current_time}] Failed to execute GraphQL mutation: {e}")
            raise ValueError(f"Mutation execution failed: {e}") from e
        
        elapsed = time.time() - start_time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] GraphQL mutation executed in {elapsed:.3f}s")
        
        return result
    
    def _execute_mutation_node(self, node: GraphQLQueryNode, variables: Dict[str, Any]) -> Any:
        """
        Execute a GraphQL mutation node.
        
        Args:
            node: GraphQL mutation node
            variables: Mutation variables
            
        Returns:
            Mutation result
        """
        # Check timeout
        if time.time() > TEST_TIMEOUT:
            raise TimeoutError(f"Mutation execution exceeded timeout of {TEST_TIMEOUT} seconds")
        
        field_name = node.field_name
        
        # Parse mutation name (e.g., "createPatient", "updatePatient", "deletePatient")
        if field_name.startswith("create"):
            resource_type = field_name[6:]  # Remove "create" prefix
            return self._execute_create_mutation(resource_type, node, variables)
        elif field_name.startswith("update"):
            resource_type = field_name[6:]  # Remove "update" prefix
            return self._execute_update_mutation(resource_type, node, variables)
        elif field_name.startswith("delete"):
            resource_type = field_name[6:]  # Remove "delete" prefix
            return self._execute_delete_mutation(resource_type, node, variables)
        else:
            raise ValueError(f"Unknown mutation: {field_name}")
    
    def _execute_create_mutation(self, resource_type: str, node: GraphQLQueryNode, variables: Dict[str, Any]) -> Any:
        """
        Execute a create mutation.
        
        Args:
            resource_type: Resource type
            node: Mutation node
            variables: Mutation variables
            
        Returns:
            Created resource
        """
        if not self.storage:
            raise ValueError("Storage backend required for mutations")
        
        # Get resource from arguments
        if "resource" not in node.arguments:
            raise ValueError("resource argument required for create mutation")
        
        resource_data = node.arguments["resource"]
        
        # Parse resource
        if isinstance(resource_data, dict):
            resource_data["resourceType"] = resource_type
            resource = parse_resource(resource_data)
        else:
            raise ValueError("Invalid resource data")
        
        # Create resource
        created_resource = self.storage.create(resource_type, resource)
        
        return serialize_resource(created_resource)
    
    def _execute_update_mutation(self, resource_type: str, node: GraphQLQueryNode, variables: Dict[str, Any]) -> Any:
        """
        Execute an update mutation.
        
        Args:
            resource_type: Resource type
            node: Mutation node
            variables: Mutation variables
            
        Returns:
            Updated resource
        """
        if not self.storage:
            raise ValueError("Storage backend required for mutations")
        
        # Get ID and resource from arguments
        if "id" not in node.arguments:
            raise ValueError("id argument required for update mutation")
        
        resource_id = node.arguments["id"]
        
        if "resource" not in node.arguments:
            raise ValueError("resource argument required for update mutation")
        
        resource_data = node.arguments["resource"]
        
        # Parse resource
        if isinstance(resource_data, dict):
            resource_data["resourceType"] = resource_type
            resource_data["id"] = resource_id
            resource = parse_resource(resource_data)
        else:
            raise ValueError("Invalid resource data")
        
        # Update resource
        updated_resource = self.storage.update(resource_type, resource_id, resource)
        
        return serialize_resource(updated_resource)
    
    def _execute_delete_mutation(self, resource_type: str, node: GraphQLQueryNode, variables: Dict[str, Any]) -> bool:
        """
        Execute a delete mutation.
        
        Args:
            resource_type: Resource type
            node: Mutation node
            variables: Mutation variables
            
        Returns:
            True if deleted successfully
        """
        if not self.storage:
            raise ValueError("Storage backend required for mutations")
        
        # Get ID from arguments
        if "id" not in node.arguments:
            raise ValueError("id argument required for delete mutation")
        
        resource_id = node.arguments["id"]
        
        # Delete resource
        return self.storage.delete(resource_type, resource_id)


def get_current_time() -> str:
    """
    Get current time as formatted string.
    
    Returns:
        Current time as "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
