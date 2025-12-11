<!--
Copyright 2025 DNAi inc.

Dual-licensed under the DNAi Free License v1.1 and the
DNAi Commercial License v1.1.
See the LICENSE files in the project root for details.
-->


# DNHealth

A pure-Python library suite for healthcare integration standards: **HL7 v2.x**, **HL7 v3**, and **FHIR R4**.

## Overview

DNHealth provides complete read/write support for the three major healthcare messaging standards:

- **HL7 v2.x**: Parse and serialize ER7 ("pipe-delimited") messages with full support for segments, fields, components, subcomponents, repetitions, and escape sequences.
- **HL7 v3**: Parse and serialize HL7 v3 XML messages with namespace support and full structural preservation.
- **FHIR R4**: Parse and serialize FHIR resources in both JSON and XML formats, with support for primitive types, complex types, and full resource structures.

## Features

### Core Capabilities
- **Pure Python**: Minimal dependencies (standard library + optional `lxml` for XML)
- **Complete Coverage**: Full structural representation of all message elements
- **Round-trip Guarantee**: Parse → serialize preserves structure (or fails clearly)
- **Type Hints**: Full type coverage throughout the codebase
- **CLI Tools**: Command-line utilities for each standard (`hl7v2tool`, `hl7v3tool`, `fhirtool`)
- **Robust Error Handling**: Clear exception hierarchy with actionable error messages
- **Tolerant Parsing**: Handles real-world quirks while maintaining spec correctness

### HL7 v2.x Advanced Features
- **Complete ER7 Parsing**: Full support for segments, fields, components, subcomponents, repetitions, and escape sequences
- **Version Support**: Multiple HL7 v2.x versions (2.3 through 2.9.1)
- **500+ Table Definitions**: Comprehensive code table support with official HL7 definitions
- **Message Validation**: Structural validation against segment definitions and table codes
- **Batch Processing**: Support for batch messages (BHS/BTS segments)
- **ACK Processing**: Automatic acknowledgment generation and processing
- **Streaming Parser**: Memory-efficient parsing for large message streams
- **JSON Codec**: Convert HL7v2 messages to/from JSON format
- **Message Correlation**: Track and correlate related messages
- **Query Support**: HL7 query message handling
- **FTP Integration**: Built-in FTP client for HL7 message exchange
- **Parallel Processing**: Multi-threaded message processing
- **Message Diffing**: Compare and identify differences between messages
- **Message Merging**: Merge multiple messages intelligently
- **Implementation Guides**: Support for HL7 Implementation Guides
- **Profiles**: Custom profile support for specialized use cases
- **Specification Compliance**: Official validation against HL7 specifications

### HL7 v3 Advanced Features
- **XML Parsing & Serialization**: Complete namespace support and structural preservation
- **RIM Classes**: Reference Information Model (RIM) class support
- **30+ Data Types**: Comprehensive HL7v3 data type implementation
- **54+ Interactions**: Support for standard HL7v3 interaction patterns
- **Message Control**: Control act wrapper and envelope handling
- **XPath Support**: Navigate and query HL7v3 XML structures
- **Schema Validation**: XML schema validation against HL7v3 schemas
- **Infrastructure Classes**: Complete infrastructure layer support
- **Transmission Wrapper**: MCCI message transmission wrapper support
- **Specification Compliance**: Official validation against HL7v3 specifications

### FHIR R4 Comprehensive Features
- **145+ Resources**: Complete FHIR R4 resource coverage including:
  - Clinical resources (Patient, Observation, Encounter, Condition, Procedure, etc.)
  - Administrative resources (Organization, Practitioner, Location, Schedule, etc.)
  - Financial resources (Claim, ClaimResponse, Coverage, ExplanationOfBenefit, etc.)
  - Medication resources (Medication, MedicationRequest, MedicationDispense, etc.)
  - Diagnostic resources (DiagnosticReport, ImagingStudy, Specimen, etc.)
  - Workflow resources (Task, Appointment, AppointmentResponse, etc.)
  - Terminology resources (CodeSystem, ValueSet, ConceptMap, etc.)
  - Conformance resources (StructureDefinition, CapabilityStatement, OperationDefinition, etc.)
  - And many more...
- **Dual Format Support**: Full JSON and XML parsing/serialization
- **FHIR Operations**: Complete support for standard FHIR operations:
  - `$validate` - Resource validation
  - `$validate-code` - Code validation against value sets
  - `$expand` - ValueSet expansion
  - `$lookup` - Code system lookup
  - `$translate` - Concept map translation
  - `$subsumes` - Code subsumption testing
  - `$closure` - Closure table management
  - `$everything` - Patient/Encounter everything operation
  - `$document` - Document generation
  - `$process-message` - Message processing
  - `$stats` - Resource statistics
  - `$meta` operations - Meta management
- **REST API Server**: Full FHIR REST API implementation with:
  - CRUD operations (Create, Read, Update, Delete)
  - Search with comprehensive parameter support
  - History and versioning support
  - Compartment-based access
  - Batch and transaction processing
  - Operation endpoints (system, resource, and instance level)
  - Subscription support
- **FHIRPath**: Complete FHIRPath expression evaluation
- **Profile Validation**: Validate resources against StructureDefinition profiles
- **Terminology Services**: Code validation, value set expansion, concept mapping
- **Extensions**: Full support for FHIR extensions and custom extensions
- **Contained Resources**: Support for contained resource references
- **Reference Validation**: Validate and resolve FHIR references
- **Polymorphic Types**: Support for choice types and polymorphic elements
- **Narrative Generation**: Automatic narrative generation for resources
- **Document Generation**: Generate FHIR Documents from resources
- **Messaging**: FHIR messaging support with Bundle processing
- **GraphQL**: FHIR GraphQL query support
- **Search Parameters**: Comprehensive search parameter support
- **Compartments**: Compartment-based resource organization
- **Conditional Operations**: Conditional create, update, and delete
- **Lazy Loading**: Efficient resource loading for large datasets
- **Diff & Merge**: Resource comparison and merging capabilities
- **Canonical URLs**: Support for canonical resource references
- **Clinical Reasoning**: Support for clinical reasoning resources
- **Specification Compliance**: Official validation against FHIR R4 specifications

### Cross-Standard Mapping
- **HL7v2 ↔ FHIR**: Bidirectional conversion between HL7v2 and FHIR
  - ADT messages ↔ Patient/Encounter resources
  - ORU messages ↔ Observation resources
  - ORM messages ↔ ServiceRequest resources
  - MDM messages ↔ DocumentReference resources
- **HL7v3 ↔ FHIR**: Bidirectional conversion between HL7v3 and FHIR
  - PRPA messages ↔ Patient resources
  - POLB messages ↔ Observation/ServiceRequest resources
  - PORX messages ↔ MedicationRequest/MedicationDispense resources
- **Configurable Mapping**: Custom mapping rules and configuration support

### Utilities & Infrastructure
- **Validation Pipeline**: Configurable multi-stage validation pipeline
- **Error Enhancement**: Enhanced error messages with context
- **Logging**: Comprehensive logging infrastructure
- **Profiling**: Performance profiling and optimization tools
- **Memory Optimization**: Efficient memory usage for large datasets
- **Retry Logic**: Automatic retry with exponential backoff
- **Recovery**: Error recovery and data consistency mechanisms
- **Audit Trail**: Complete audit logging support
- **Database Integration**: Database utilities for persistence
- **Queue Management**: Message queue handling
- **Routing**: Intelligent message routing
- **Transformation**: Data transformation utilities
- **IO Utilities**: Enhanced I/O operations
- **Network Utilities**: Network communication helpers
- **Configuration Management**: Flexible configuration system

## Installation

```bash
pip install dnhealth
```

For XML support (recommended for HL7v3 and FHIR XML):

```bash
pip install dnhealth[xml]
```

## Quick Start

### HL7 v2.x

```python
from dnhealth.dnhealth_hl7v2.parser import parse_hl7v2
from dnhealth.dnhealth_hl7v2.serializer import serialize_hl7v2

# Parse an HL7 v2 message
text = "MSH|^~\\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|20240101120000||ADT^A01|12345|P|2.5\rPID|||123456^^^MRN||DOE^JOHN||19800101|M"
msg = parse_hl7v2(text)

# Access message elements
pid = msg.segments["PID"][0]
patient_id = pid.field(3).component(1).value
patient_name = pid.field(5).component(1).value
print(f"Patient: {patient_name}, ID: {patient_id}")

# Serialize back to ER7
serialized = serialize_hl7v2(msg)
```

### HL7 v3

```python
from dnhealth.dnhealth_hl7v3.parser import parse_hl7v3
from dnhealth.dnhealth_hl7v3.serializer import serialize_hl7v3

# Parse an HL7 v3 XML message
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<PRPA_IN201305UV02 xmlns="urn:hl7-org:v3">
    <id root="1.2.3.4.5"/>
    <controlActProcess>
        <subject>
            <registrationEvent>
                <id root="1.2.3.4.5.6"/>
            </registrationEvent>
        </subject>
    </controlActProcess>
</PRPA_IN201305UV02>"""

msg = parse_hl7v3(xml_string)

# Access elements
root_id = msg.root.get_attribute("root")
print(f"Root ID: {root_id}")

# Serialize back to XML
serialized = serialize_hl7v3(msg)
```

### FHIR R4

```python
from dnhealth.dnhealth_fhir.resources.patient import Patient
from dnhealth.dnhealth_fhir.parser_json import parse_fhir_json
from dnhealth.dnhealth_fhir.serializer_json import serialize_fhir_json

# Parse a FHIR Patient resource
json_string = """{
    "resourceType": "Patient",
    "id": "example",
    "name": [{
        "family": "Doe",
        "given": ["John"]
    }],
    "birthDate": "1980-01-01",
    "gender": "male"
}"""

patient = parse_fhir_json(json_string, Patient)
assert patient.name[0].family == "Doe"
assert patient.name[0].given[0] == "John"

# Serialize back to JSON
serialized = serialize_fhir_json(patient)
```

## CLI Tools

### hl7v2tool

```bash
# Pretty-print an HL7 v2 message
hl7v2tool pretty message.hl7

# Convert to JSON
hl7v2tool json message.hl7

# Validate structure
hl7v2tool validate message.hl7

# Round-trip test
hl7v2tool roundtrip message.hl7
```

### hl7v3tool

```bash
# Pretty-print HL7 v3 XML
hl7v3tool pretty message.xml

# Convert to JSON representation
hl7v3tool json message.xml

# Validate structure
hl7v3tool validate message.xml
```

### fhirtool

```bash
# Pretty-print FHIR JSON
fhirtool pretty patient.json

# Validate FHIR resource
fhirtool validate patient.json

# Convert JSON to XML
fhirtool to-xml patient.json

# Convert XML to JSON
fhirtool to-json patient.xml
```


## Use Cases

DNHealth is suitable for a wide range of healthcare integration scenarios:

- **Healthcare Information Systems**: Integrate HL7v2, HL7v3, and FHIR messaging in EHR systems
- **Interoperability Solutions**: Build bridges between different healthcare standards
- **Data Transformation**: Convert between HL7v2, HL7v3, and FHIR formats
- **API Development**: Create FHIR REST APIs for healthcare applications
- **Message Processing**: Parse, validate, and process healthcare messages at scale
- **Clinical Data Exchange**: Exchange patient data, observations, and clinical documents
- **Terminology Services**: Validate codes, expand value sets, and translate concepts
- **Compliance Testing**: Validate implementations against official HL7/FHIR specifications
- **Research & Analytics**: Process healthcare data for research and analytics purposes
- **Integration Testing**: Test healthcare integrations with realistic message data

## Testing

The test suite includes comprehensive coverage:

- **Unit Tests**: Embedded examples and test cases for all features
- **Integration Tests**: Tests against official HL7/FHIR test data
- **Specification Compliance**: Validation against official HL7/FHIR specifications
- **Cross-Standard Tests**: Round-trip conversion tests between standards

```bash
pytest tests/
```

For official specification compliance validation:

```python
from dnhealth.validation import run_all_official_validations

results = run_all_official_validations()
```

## Advanced Usage Examples

### FHIR Operations

```python
from dnhealth.dnhealth_fhir.operations import execute_operation
from dnhealth.dnhealth_fhir.resources.parameters import Parameters, ParametersParameter

# Validate a resource
result = execute_operation("$validate", Parameters(parameter=[
    ParametersParameter(name="resource", resource=patient_resource)
]))

# Expand a ValueSet
result = execute_operation("$expand", Parameters(parameter=[
    ParametersParameter(name="url", valueString="http://hl7.org/fhir/ValueSet/administrative-gender")
]))

# Validate a code
result = execute_operation("$validate-code", Parameters(parameter=[
    ParametersParameter(name="url", valueString="http://hl7.org/fhir/ValueSet/administrative-gender"),
    ParametersParameter(name="code", valueString="male")
]))
```

### FHIR REST API Server

```python
from dnhealth.dnhealth_fhir.rest_server import FHIRRestServer

# Create and start FHIR REST API server
server = FHIRRestServer(base_path="/fhir")
server.run(host="0.0.0.0", port=8080)

# Access via standard FHIR REST endpoints:
# GET /fhir/Patient/123
# POST /fhir/Patient
# GET /fhir/Patient?name=Smith
# GET /fhir/Patient/123/$everything
```

### Cross-Standard Mapping

```python
from dnhealth.mapping import convert_adt_to_patient, convert_patient_to_adt

# Convert HL7v2 ADT message to FHIR Patient
hl7v2_message = parse_hl7v2(adt_text)
patient = convert_adt_to_patient(hl7v2_message)

# Convert FHIR Patient to HL7v2 ADT message
adt_message = convert_patient_to_adt(patient, message_type="A08")
```

### HL7v2 Advanced Features

```python
from dnhealth.dnhealth_hl7v2.batch import parse_batch_message
from dnhealth.dnhealth_hl7v2.ack import generate_ack
from dnhealth.dnhealth_hl7v2.streaming_parser import StreamingParser

# Process batch messages
batch = parse_batch_message(batch_text)
for message in batch.messages:
    process_message(message)

# Generate acknowledgment
ack = generate_ack(original_message, ack_code="AA")

# Stream processing for large files
parser = StreamingParser()
for message in parser.parse_file("large_messages.hl7"):
    process_message(message)
```

### FHIRPath Expressions

```python
from dnhealth.dnhealth_fhir.fhirpath import evaluate_fhirpath

# Evaluate FHIRPath expression
result = evaluate_fhirpath(patient, "name.given.first()")
result = evaluate_fhirpath(observation, "valueQuantity.value > 100")
```

## Current Coverage

### HL7 v2.x (~95% Complete)
- ✅ Complete ER7 parsing and serialization
- ✅ All structural elements (segments, fields, components, subcomponents, repetitions)
- ✅ Escape sequence handling
- ✅ Multiple version support (2.3 through 2.9.1)
- ✅ 500+ table definitions with official HL7 codes
- ✅ 181+ segment field definitions
- ✅ Message validation and structural checking
- ✅ Batch message processing
- ✅ ACK generation and processing
- ✅ JSON codec
- ✅ Streaming parser for large files
- ✅ Message correlation and tracking
- ✅ Query message support
- ✅ FTP integration
- ✅ Parallel processing
- ✅ Message diffing and merging
- ✅ Implementation guide support
- ✅ Profile support
- ✅ Official specification compliance validation

### HL7 v3 (~90% Complete)
- ✅ XML parsing and serialization
- ✅ Namespace support
- ✅ Full structural preservation
- ✅ RIM (Reference Information Model) classes
- ✅ 30+ data types
- ✅ 54+ interaction patterns
- ✅ Message control wrappers
- ✅ XPath navigation
- ✅ Schema validation
- ✅ Infrastructure classes
- ✅ Transmission wrappers
- ✅ Official specification compliance validation

### FHIR R4 (~98% Complete)
- ✅ **145+ Resources**: Complete FHIR R4 resource coverage
- ✅ JSON and XML parsing/serialization
- ✅ All primitive and complex types
- ✅ Comprehensive validation framework
- ✅ FHIR operations (11+ standard operations)
- ✅ REST API server implementation
- ✅ FHIRPath expression evaluation
- ✅ Profile validation
- ✅ Terminology services (CodeSystem, ValueSet, ConceptMap)
- ✅ Extensions and custom extensions
- ✅ Contained resources
- ✅ Reference validation
- ✅ Polymorphic types
- ✅ Narrative generation
- ✅ Document generation
- ✅ Messaging support
- ✅ GraphQL support
- ✅ Search parameters
- ✅ Compartments
- ✅ Conditional operations
- ✅ Lazy loading
- ✅ Official specification compliance validation

### Cross-Standard Mapping
- ✅ HL7v2 ↔ FHIR bidirectional conversion
- ✅ HL7v3 ↔ FHIR bidirectional conversion
- ✅ Configurable mapping rules

## Architecture

DNHealth is built with a modular architecture:

```
dnhealth/
├── dnhealth_hl7v2/      # HL7 v2.x support
│   ├── parser.py        # ER7 parsing
│   ├── serializer.py    # ER7 serialization
│   ├── model.py         # Message models
│   ├── validation.py    # Message validation
│   ├── tables.py        # Code tables
│   ├── batch.py         # Batch processing
│   ├── ack.py           # Acknowledgments
│   └── ...
├── dnhealth_hl7v3/      # HL7 v3 support
│   ├── parser.py        # XML parsing
│   ├── serializer.py    # XML serialization
│   ├── rim.py           # RIM classes
│   ├── datatypes.py     # Data types
│   ├── interactions.py  # Interaction patterns
│   └── ...
├── dnhealth_fhir/       # FHIR R4 support
│   ├── resources/       # 145+ resource definitions
│   ├── parser_json.py   # JSON parsing
│   ├── parser_xml.py    # XML parsing
│   ├── validation.py    # Validation framework
│   ├── operations.py    # FHIR operations
│   ├── rest_server.py   # REST API server
│   ├── fhirpath.py      # FHIRPath evaluation
│   ├── profile.py       # Profile validation
│   └── ...
├── mapping/             # Cross-standard mapping
│   ├── hl7v2_to_fhir.py
│   ├── hl7v3_to_fhir.py
│   └── ...
├── validation/          # Official validation
│   └── official_validation.py
└── util/                # Shared utilities
    ├── validation_pipeline.py
    ├── logging.py
    └── ...
```

## License

Copyright 2025 DNAi inc.

Dual-licensed under the DNAi Free License v1.1 and the
DNAi Commercial License v1.1.
See the LICENSE files in the project root for details.

## Documentation

Comprehensive documentation is available:

- **User Guides**: Getting started guides for each standard
  - [HL7v2 User Guide](docs/user_guides/HL7V2_USER_GUIDE.md)
  - [HL7v3 User Guide](docs/user_guides/HL7V3_USER_GUIDE.md)
  - [FHIR R4 User Guide](docs/user_guides/FHIR_R4_USER_GUIDE.md)
  - [Getting Started](docs/user_guides/GETTING_STARTED.md)
  - [Migration Guide](docs/user_guides/MIGRATION_GUIDE.md)

- **Developer Guides**: Architecture and development documentation
  - [Architecture](docs/developer_guides/ARCHITECTURE.md)
  - [Best Practices](docs/developer_guides/BEST_PRACTICES.md)
  - [Extension Guide](docs/developer_guides/EXTENSION_GUIDE.md)
  - [Performance Tuning](docs/developer_guides/PERFORMANCE_TUNING.md)
  - [Troubleshooting](docs/developer_guides/TROUBLESHOOTING.md)

- **API Documentation**: Detailed docstrings in each module (accessible via Python's `help()` function)

## Performance

DNHealth is optimized for production use:

- **Memory Efficient**: Streaming parsers for large message files
- **Fast Parsing**: Optimized parsers for high-throughput scenarios
- **Caching**: Built-in caching for validation and terminology operations
- **Parallel Processing**: Multi-threaded message processing support
- **Lazy Loading**: Efficient resource loading for large datasets

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key areas for contribution:
- Additional FHIR resource implementations (if any are missing)
- Performance optimizations
- Documentation improvements
- Test coverage enhancements
- Cross-standard mapping improvements

