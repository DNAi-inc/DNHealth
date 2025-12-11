# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
FHIR R4 primitive and complex data types.

Implements FHIR data types using Python dataclasses.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from dnhealth.dnhealth_fhir.types import Extension


# Primitive types are represented as Python types with validation
# For now, we use simple type aliases and validation functions


@dataclass
class Element:
    """
    FHIR Element base class.
    
    Base class for all FHIR elements.
    All elements have an id and extension fields.
    """
    
    id: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class BackboneElement(Element):
    """
    FHIR BackboneElement base class.
    
    Base class for elements that are part of a backbone structure.
    Extends Element with modifierExtension field.
    """
    
    modifierExtension: List["Extension"] = field(default_factory=list)


@dataclass
class FHIRPrimitive:
    """Base class for FHIR primitive types."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)


@dataclass
class FHIRString(FHIRPrimitive):
    """FHIR string primitive type."""

    pass


@dataclass
class FHIRBoolean(FHIRPrimitive):
    """FHIR boolean primitive type."""

    value: bool

    def __str__(self) -> str:
        """String representation."""
        return "true" if self.value else "false"


@dataclass
class FHIRInteger(FHIRPrimitive):
    """FHIR integer primitive type."""

    value: int


@dataclass
class FHIRDecimal(FHIRPrimitive):
    """FHIR decimal primitive type."""

    value: float


@dataclass
class FHIRDate(FHIRPrimitive):
    """FHIR date primitive type (YYYY-MM-DD)."""

    pass


@dataclass
class FHIRDateTime(FHIRPrimitive):
    """FHIR dateTime primitive type (ISO 8601)."""

    pass


@dataclass
class FHIRUri(FHIRPrimitive):
    """FHIR uri primitive type."""

    pass


@dataclass
class FHIRCode(FHIRPrimitive):
    """FHIR code primitive type."""

    pass


@dataclass
class FHIRId(FHIRPrimitive):
    """
    FHIR id primitive type.
    
    A string that contains an id value (up to 64 characters, matching regex [A-Za-z0-9\\-\\.]{1,64}).
    """

    def __post_init__(self):
        """Validate id format."""
        if self.value and len(self.value) > 64:
            raise ValueError(f"FHIR id must be <= 64 characters, got {len(self.value)}")
        # Basic validation - should match [A-Za-z0-9\-\.]{1,64}
        import re
        if self.value and not re.match(r'^[A-Za-z0-9\\-\\.]{1,64}$', self.value):
            raise ValueError(f"FHIR id must match pattern [A-Za-z0-9\\-\\.]{{1,64}}, got: {self.value}")
@dataclass
class FHIRInstant(FHIRPrimitive):
    """
    FHIR instant primitive type.
    
    An instant in time (ISO 8601 format with timezone, e.g., YYYY-MM-DDThh:mm:ss.sss+zz:zz).
    """

    def __post_init__(self):
        """Validate instant format."""
        if self.value:
            # Basic validation - should be ISO 8601 format
            import re
            # Pattern: YYYY-MM-DDThh:mm:ss.sss+zz:zz or YYYY-MM-DDThh:mm:ss.sssZ
            pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$'
            if not re.match(pattern, self.value):
                raise ValueError(f"FHIR instant must be ISO 8601 format, got: {self.value}")
@dataclass
class FHIRTime(FHIRPrimitive):
    """
    FHIR time primitive type.
    
    A time during the day (HH:MM:SS format).
    """

    def __post_init__(self):
        """Validate time format."""
        if self.value:
            # Basic validation - should be HH:MM:SS format
            import re
            pattern = r'^\d{2}:\d{2}:\d{2}$'
            if not re.match(pattern, self.value):
                raise ValueError(f"FHIR time must be HH:MM:SS format, got: {self.value}")
@dataclass
class FHIRPositiveInt(FHIRPrimitive):
    """
    FHIR positiveInt primitive type.
    
    A positive integer (>= 1).
    """

    value: int

    def __post_init__(self):
        """Validate positive integer."""
        if self.value < 1:
            raise ValueError(f"FHIR positiveInt must be >= 1, got: {self.value}")
@dataclass
class FHIRBase64Binary(FHIRPrimitive):
    """
    FHIR base64Binary primitive type.
    
    A base64-encoded string.
    """

    def __post_init__(self):
        """Validate base64 format."""
        if self.value:
            import base64
            try:
                # Try to decode to validate base64 format
                base64.b64decode(self.value, validate=True)
            except Exception:
                raise ValueError(f"FHIR base64Binary must be valid base64, got invalid value")
@dataclass
class FHIRCanonical(FHIRPrimitive):
    """
    FHIR canonical primitive type.
    
    A URI that refers to a resource by its canonical URL.
    """

    pass


@dataclass
class FHIRMarkdown(FHIRPrimitive):
    """
    FHIR markdown primitive type.
    
    A string that may contain markdown syntax for rich text representation.
    """

    pass


@dataclass
class FHIROid(FHIRPrimitive):
    """
    FHIR oid primitive type.
    
    An OID (Object Identifier) represented as a URI (urn:oid:1.2.3.4.5).
    """

    def __post_init__(self):
        """Validate OID format."""
        if self.value:
            # Should start with urn:oid: or be a valid OID pattern
            import re
            if self.value.startswith("urn:oid:"):
                oid_part = self.value[8:]
                pattern = r'^\d+(\.\d+)*$'
                if not re.match(pattern, oid_part):
                    raise ValueError(f"FHIR oid must have valid OID format after urn:oid:, got: {oid_part}")
            else:
                # Try to validate as direct OID
                pattern = r'^\d+(\.\d+)*$'
                if not re.match(pattern, self.value):
                    raise ValueError(f"FHIR oid must be urn:oid:... or valid OID format, got: {self.value}")
@dataclass
class FHIRUnsignedInt(FHIRPrimitive):
    """
    FHIR unsignedInt primitive type.
    
    An unsigned integer (>= 0).
    """

    value: int

    def __post_init__(self):
        """Validate unsigned integer."""
        if self.value < 0:
            raise ValueError(f"FHIR unsignedInt must be >= 0, got: {self.value}")
@dataclass
class FHIRUrl(FHIRPrimitive):
    """
    FHIR url primitive type.
    
    A URI that refers to a resource.
    """

    pass


@dataclass
class FHIRUuid(FHIRPrimitive):
    """
    FHIR uuid primitive type.
    
    A UUID (Universally Unique Identifier) in RFC 4122 format.
    """

    def __post_init__(self):
        """Validate UUID format."""
        if self.value:
            import re
            # UUID pattern: 8-4-4-4-12 hexadecimal digits
            pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            if not re.match(pattern, self.value):
                raise ValueError(f"FHIR uuid must be RFC 4122 format, got: {self.value}")


# Complex types


@dataclass
class Extension:
    """
    FHIR Extension complex type.

    Extensions allow additional content to be added to resources.
    """

    url: str
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueDecimal: Optional[float] = None
    valueDate: Optional[str] = None
    valueDateTime: Optional[str] = None
    valueUri: Optional[str] = None
    valueCode: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Coding:
    """
    FHIR Coding complex type.

    Represents a coded value with system, code, display, etc.
    """

    system: Optional[str] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    userSelected: Optional[bool] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class CodeableConcept:
    """
    FHIR CodeableConcept complex type.

    Represents a concept with one or more codings.
    """

    coding: List[Coding] = field(default_factory=list)
    text: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Identifier:
    """
    FHIR Identifier complex type.

    Represents an identifier (e.g., MRN, SSN).
    """

    use: Optional[str] = None
    type: Optional[CodeableConcept] = None
    system: Optional[str] = None
    value: Optional[str] = None
    period: Optional["Period"] = None
    assigner: Optional["Reference"] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class HumanName:
    """
    FHIR HumanName complex type.

    Represents a person's name.
    """

    use: Optional[str] = None
    text: Optional[str] = None
    family: Optional[str] = None
    given: List[str] = field(default_factory=list)
    prefix: List[str] = field(default_factory=list)
    suffix: List[str] = field(default_factory=list)
    period: Optional["Period"] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Address:
    """
    FHIR Address complex type.

    Represents a postal address.
    """

    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: List[str] = field(default_factory=list)
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    period: Optional["Period"] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class ContactPoint:
    """
    FHIR ContactPoint complex type.

    Represents a phone, email, etc.
    """

    system: Optional[str] = None  # phone, fax, email, pager, url, sms, other
    value: Optional[str] = None
    use: Optional[str] = None  # home, work, temp, old, mobile
    rank: Optional[int] = None
    period: Optional["Period"] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class ContactDetail:
    """
    FHIR ContactDetail complex type.

    Specifies contact information for a person or organization.
    """

    name: Optional[str] = None  # Name of an individual to contact
    telecom: List[ContactPoint] = field(default_factory=list)  # Contact details for individual or organization
    extension: List["Extension"] = field(default_factory=list)
    modifierExtension: List["Extension"] = field(default_factory=list)


@dataclass
class UsageContext:
    """
    FHIR UsageContext complex type.

    Specifies the context in which a resource is intended to be used.
    """

    code: "CodeableConcept"  # Type of context being specified (required)
    valueCodeableConcept: Optional["CodeableConcept"] = None  # Value that defines the context
    valueQuantity: Optional["Quantity"] = None  # Value that defines the context
    valueRange: Optional["Range"] = None  # Value that defines the context
    valueReference: Optional["Reference"] = None  # Value that defines the context
    extension: List["Extension"] = field(default_factory=list)
    modifierExtension: List["Extension"] = field(default_factory=list)


@dataclass
class Period:
    """
    FHIR Period complex type.

    Represents a time period.
    """

    start: Optional[str] = None
    end: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Reference:
    """
    FHIR Reference complex type.

    References another resource.
    """

    reference: Optional[str] = None
    type: Optional[str] = None
    identifier: Optional[Identifier] = None
    display: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Quantity:
    """
    FHIR Quantity complex type.

    Represents a measured amount.
    """

    value: Optional[float] = None
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class CodeableReference:
    """
    FHIR CodeableReference complex type.

    A reference to a concept or a resource.
    """

    concept: Optional[CodeableConcept] = None
    reference: Optional[Reference] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Attachment:
    """
    FHIR Attachment complex type.

    Represents content in a format other than FHIR.
    """

    contentType: Optional[str] = None
    language: Optional[str] = None
    data: Optional[str] = None
    url: Optional[str] = None
    size: Optional[int] = None
    hash: Optional[str] = None
    title: Optional[str] = None
    creation: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Annotation:
    """
    FHIR Annotation complex type.

    A text note.
    """

    text: str
    authorReference: Optional[Reference] = None
    authorString: Optional[str] = None
    time: Optional[str] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Age(Quantity):
    """
    FHIR Age complex type.
    
    A duration of time during which an organism has existed.
    Extends Quantity with age-specific semantics.
    """

    pass


@dataclass
class Distance(Quantity):
    """
    FHIR Distance complex type.
    
    A length - a value with a unit that is a physical distance.
    Extends Quantity with distance-specific semantics.
    """

    pass


@dataclass
class Duration(Quantity):
    """
    FHIR Duration complex type.
    
    A length of time.
    Extends Quantity with duration-specific semantics.
    """

    pass


@dataclass
class Count(Quantity):
    """
    FHIR Count complex type.
    
    A count of a discrete element.
    Extends Quantity with count-specific semantics.
    """

    pass


@dataclass
class Money:
    """
    FHIR Money complex type.
    
    An amount of money with its currency.
    """

    value: Optional[float] = None
    currency: Optional[str] = None  # ISO 4217 currency code
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Range:
    """
    FHIR Range complex type.
    
    A set of ordered Quantities defined by a low and high value.
    """

    low: Optional[Quantity] = None
    high: Optional[Quantity] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Ratio:
    """
    FHIR Ratio complex type.
    
    A ratio of two Quantity values.
    """
    
    numerator: Optional[Quantity] = None
    denominator: Optional[Quantity] = None
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Narrative:
    """
    FHIR Narrative complex type.
    
    A human-readable summary of the resource.
    Contains XHTML content for display purposes.
    """
    
    status: str  # generated, extensions, additional, empty
    div: str  # XHTML content (required)
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate Narrative after initialization."""
        valid_statuses = {"generated", "extensions", "additional", "empty"}
        if self.status not in valid_statuses:
            raise ValueError(f"Narrative status must be one of {valid_statuses}, got: {self.status}")
        
        if not self.div:
            raise ValueError("Narrative div (XHTML content) is required")
@dataclass
class SampledData:
    """
    FHIR SampledData complex type.
    
    A series of measurements taken by a device, with upper and lower limits.
    Used for waveform data, time-series data, etc.
    """
    
    origin: Quantity  # Zero value and units (required)
    period: float  # Number of milliseconds between samples (required, must be > 0)
    dimensions: int  # Number of sample points at each time point (required, must be >= 1)
    factor: Optional[float] = None  # Multiply data by this before adding to origin
    lowerLimit: Optional[float] = None  # Lower limit of detection
    upperLimit: Optional[float] = None  # Upper limit of detection
    data: Optional[str] = None  # Decimal values separated by single space (optional)
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate SampledData after initialization."""
        if self.period <= 0:
            raise ValueError(f"SampledData period must be > 0, got: {self.period}")
        
        if self.dimensions < 1:
            raise ValueError(f"SampledData dimensions must be >= 1, got: {self.dimensions}")
@dataclass
class Signature:
    """
    FHIR Signature complex type.
    
    A digital signature along with supporting context.
    Used for electronic signatures on documents, consents, etc.
    """
    
    when: str  # When the signature was created (required, instant format)
    who: Reference  # Who signed (required)
    type: List[Coding] = field(default_factory=list)  # Indication of the reason the entity signed
    onBehalfOf: Optional[Reference] = None  # The party represented
    targetFormat: Optional[str] = None  # MIME type of signed content
    sigFormat: Optional[str] = None  # MIME type of signature
    data: Optional[str] = None  # The actual signature content (base64Binary)
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate Signature after initialization."""
        if not self.when:
            raise ValueError("Signature when (timestamp) is required")
        
        if not self.who:
            raise ValueError("Signature who (reference) is required")
@dataclass
class TimingRepeat:
    """
    FHIR Timing.repeat complex type.
    
    Defines a repeating pattern for timing.
    """
    
    boundsDuration: Optional["Duration"] = None
    boundsRange: Optional["Range"] = None
    boundsPeriod: Optional[Period] = None
    count: Optional[int] = None
    countMax: Optional[int] = None
    duration: Optional[float] = None
    durationMax: Optional[float] = None
    durationUnit: Optional[str] = None  # s, min, h, d, wk, mo, a
    frequency: Optional[int] = None
    frequencyMax: Optional[int] = None
    period: Optional[float] = None
    periodMax: Optional[float] = None
    periodUnit: Optional[str] = None  # s, min, h, d, wk, mo, a
    dayOfWeek: List[str] = field(default_factory=list)  # mon, tue, wed, thu, fri, sat, sun
    timeOfDay: List[str] = field(default_factory=list)  # Time of day (HH:MM:SS)
    when: List[str] = field(default_factory=list)  # Code for time period of occurrence
    offset: Optional[int] = None  # Minutes from event
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate TimingRepeat after initialization."""
        if self.count is not None and self.count < 0:
            raise ValueError(f"TimingRepeat count must be >= 0, got: {self.count}")
        
        if self.frequency is not None and self.frequency < 0:
            raise ValueError(f"TimingRepeat frequency must be >= 0, got: {self.frequency}")
@dataclass
class Timing:
    """
    FHIR Timing complex type.
    
    Specifies an event that may occur multiple times.
    Used for medication schedules, appointment times, etc.
    """
    
    event: List[str] = field(default_factory=list)  # When the event occurs (dateTime)
    repeat: Optional[TimingRepeat] = None  # When the event is to occur
    code: Optional["CodeableConcept"] = None  # BID, TID, QID, AM, PM, etc.
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class TriggerDefinition:
    """
    FHIR TriggerDefinition complex type.
    
    Defines when an event should be triggered.
    Used in EventDefinition, PlanDefinition, etc.
    """
    
    type: str  # named-event | periodic | data-changed | data-added | data-modified | data-removed | data-accessed | data-access-ended (required)
    name: Optional[str] = None  # Name or URI that identifies the event
    timingTiming: Optional["Timing"] = None  # Timing of the event
    timingReference: Optional["Reference"] = None  # Timing of the event
    timingDate: Optional[str] = None  # Timing of the event
    timingDateTime: Optional[str] = None  # Timing of the event
    data: List[Any] = field(default_factory=list)  # Triggering data of the event (DataRequirement)
    condition: Optional[Any] = None  # Whether the event triggers (boolean expression, Expression type)
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class RelatedArtifact:
    """
    FHIR RelatedArtifact complex type.
    
    Related artifacts such as additional documentation, citations, etc.
    Used in Library, Evidence, PlanDefinition, and other resources.
    """
    
    type: str  # documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of (required)
    label: Optional[str] = None  # Short label
    display: Optional[str] = None  # Brief description of the artifact
    citation: Optional[str] = None  # Bibliographic citation for the artifact (markdown)
    url: Optional[str] = None  # URL where the artifact can be accessed
    document: Optional[Attachment] = None  # The actual artifact, if provided inline
    resource: Optional[str] = None  # Canonical reference to a related resource
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate RelatedArtifact after initialization."""
        valid_types = {
            "documentation", "justification", "citation", "predecessor",
            "successor", "derived-from", "depends-on", "composed-of"
        }
        if self.type not in valid_types:
            raise ValueError(
                f"RelatedArtifact type must be one of {valid_types}, got: {self.type}"
            )


@dataclass
class Contributor:
    """
    FHIR Contributor complex type.
    
    A contributor to the content of a knowledge asset, including authors, editors, reviewers, and endorsers.
    Used in Library, Evidence, and other knowledge resources.
    """
    
    type: str  # author | editor | reviewer | endorser (required)
    name: Optional[str] = None  # Who contributed the content
    contact: List["ContactDetail"] = field(default_factory=list)  # Contact details of the contributor
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate Contributor after initialization."""
        valid_types = {"author", "editor", "reviewer", "endorser"}
        if self.type not in valid_types:
            raise ValueError(
                f"Contributor type must be one of {valid_types}, got: {self.type}"
            )


@dataclass
class DataRequirement:
    """
    FHIR DataRequirement complex type.
    
    Describes a required data item for evaluation in order for an artifact to be successfully used.
    Used in TriggerDefinition, PlanDefinition, ActivityDefinition, etc.
    """
    
    type: str  # The type of the required data (required)
    profile: List[str] = field(default_factory=list)  # The profile of the required data
    subjectCodeableConcept: Optional["CodeableConcept"] = None  # E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device
    subjectReference: Optional["Reference"] = None  # E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device
    mustSupport: List[str] = field(default_factory=list)  # Indicates that specific structure elements are required
    codeFilter: List[Any] = field(default_factory=list)  # Code filters for the data
    dateFilter: List[Any] = field(default_factory=list)  # Date filters for the data
    limit: Optional[int] = None  # Number of results (positive integer)
    sort: List[Any] = field(default_factory=list)  # Order of the results
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Dosage:
    """
    FHIR Dosage complex type.
    
    Indicates how the medication is/was taken or should be taken by the patient.
    Used in MedicationStatement, MedicationRequest, MedicationAdministration, etc.
    """
    
    sequence: Optional[int] = None  # The order of the dosage instructions
    text: Optional[str] = None  # Free text dosage instructions e.g. SIG
    additionalInstruction: List["CodeableConcept"] = field(default_factory=list)  # Supplemental instruction
    patientInstruction: Optional[str] = None  # Patient or consumer oriented instructions
    timing: Optional["Timing"] = None  # When medication should be administered
    asNeededBoolean: Optional[bool] = None  # Take "as needed" (for x/PRN)
    asNeededCodeableConcept: Optional["CodeableConcept"] = None  # Take "as needed" (for x/PRN)
    site: Optional["CodeableConcept"] = None  # Body site to administer to
    route: Optional["CodeableConcept"] = None  # How drug should enter body
    method: Optional["CodeableConcept"] = None  # Technique for administering medication
    doseAndRate: List[Any] = field(default_factory=list)  # Amount of medication administered
    maxDosePerPeriod: Optional["Ratio"] = None  # Upper limit on medication per unit of time
    maxDosePerAdministration: Optional["Quantity"] = None  # Upper limit on medication per administration
    maxDosePerLifetime: Optional["Quantity"] = None  # Upper limit on medication per lifetime of the patient
    extension: List["Extension"] = field(default_factory=list)


@dataclass
class Expression:
    """
    FHIR Expression complex type.
    
    A expression that is evaluated in a specified context and returns a value.
    Used in various resources for computable expressions.
    """
    
    language: str  # text/cql | text/fhirpath | application/x-fhir-query | etc. (required)
    description: Optional[str] = None  # Natural language description of the condition
    name: Optional[str] = None  # Short name assigned to expression for reuse
    expression: Optional[str] = None  # Expression in specified language
    reference: Optional[str] = None  # Where the expression is found
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate Expression after initialization."""
        if not self.language:
            raise ValueError("Expression language is required")


@dataclass
class MoneyQuantity(Quantity):
    """
    FHIR MoneyQuantity complex type.
    
    A measured amount (or an amount that can potentially be measured).
    Extends Quantity with currency support.
    """
    
    # Inherits all fields from Quantity
    # currency: Optional[str] = None  # ISO 4217 Currency Code (can be added if needed)
    pass


@dataclass
class ParameterDefinition:
    """
    FHIR ParameterDefinition complex type.
    
    The parameters to the module.
    Used in OperationDefinition, PlanDefinition, etc.
    """
    
    use: str  # in | out (required)
    type: str  # What type of value (required)
    name: Optional[str] = None  # Parameter name
    min: Optional[int] = None  # Minimum cardinality
    max: Optional[str] = None  # Maximum cardinality (e.g. 1, *)
    documentation: Optional[str] = None  # A brief description of the parameter
    profile: Optional[str] = None  # What profile the value is expected to be
    extension: List["Extension"] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate ParameterDefinition after initialization."""
        valid_uses = {"in", "out"}
        if self.use not in valid_uses:
            raise ValueError(
                f"ParameterDefinition use must be one of {valid_uses}, got: {self.use}"
            )


@dataclass
class SimpleQuantity(Quantity):
    """
    FHIR SimpleQuantity complex type.
    
    A fixed quantity (no comparator).
    Extends Quantity but without comparator field.
    """
    
    # Inherits all fields from Quantity except comparator
    # comparator is not allowed in SimpleQuantity
    pass


@dataclass
class FHIRXhtml(FHIRPrimitive):
    """
    FHIR xhtml primitive type.
    
    XHTML content for Narrative.div and other XHTML fields.
    Must be valid XHTML content.
    """
    
    def __post_init__(self):
        """Validate XHTML content."""
        if self.value:
            # Basic validation - should contain valid XHTML tags
            import re
            # Check for basic XHTML structure (at least one tag)
            if not re.search(r'<[^>]+>', self.value):
                # Allow empty div for empty narrative
                if self.value.strip() != '<div xmlns="http://www.w3.org/1999/xhtml"></div>':
                    raise ValueError("FHIR xhtml must contain valid XHTML content")


# Type aliases for verification script compatibility
# Primitive types
base64Binary = FHIRBase64Binary
boolean = FHIRBoolean
canonical = FHIRCanonical
code = FHIRCode
date = FHIRDate
dateTime = FHIRDateTime
decimal = FHIRDecimal
id = FHIRId
instant = FHIRInstant
integer = FHIRInteger
markdown = FHIRMarkdown
oid = FHIROid
positiveInt = FHIRPositiveInt
string = FHIRString
time = FHIRTime
unsignedInt = FHIRUnsignedInt
uri = FHIRUri
url = FHIRUrl
uuid = FHIRUuid
xhtml = FHIRXhtml

@dataclass
class Population(Element):
    """
    FHIR Population complex type.
    
    A population group (e.g. patients, practitioners, etc.).
    Used in EvidenceVariable, ResearchElementDefinition, etc.
    """
    
    ageRange: Optional["Range"] = None  # Age of the specific population
    ageCodeableConcept: Optional["CodeableConcept"] = None  # Age of the specific population
    gender: Optional["CodeableConcept"] = None  # Gender of the specific population
    race: Optional["CodeableConcept"] = None  # Race of the specific population
    physiologicalCondition: Optional["CodeableConcept"] = None  # Physiological condition of the specific population


# Import complex types from other modules for discoverability
from dnhealth.dnhealth_fhir.structuredefinition import ElementDefinition
from dnhealth.dnhealth_fhir.resources.base import Meta

# Type aliases for complex types
ElementDefinition = ElementDefinition  # ElementDefinition complex type
Meta = Meta  # Meta complex type


# ============================================================================
# Additional FHIR Data Types
# ============================================================================

@dataclass
class Address(Element):
    """FHIR Address data type."""
    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: List[str] = field(default_factory=list)
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    period: Optional["Period"] = None

@dataclass
class Annotation(Element):
    """FHIR Annotation data type."""
    authorReference: Optional["Reference"] = None
    authorString: Optional[str] = None
    time: Optional[str] = None  # DateTime
    text: str  # Required

@dataclass
class Attachment(Element):
    """FHIR Attachment data type."""
    contentType: Optional[str] = None
    language: Optional[str] = None
    data: Optional[str] = None  # Base64Binary
    url: Optional[str] = None  # Url
    size: Optional[int] = None  # UnsignedInt
    hash: Optional[str] = None  # Base64Binary
    title: Optional[str] = None
    creation: Optional[str] = None  # DateTime

@dataclass
class CodeableConcept(Element):
    """FHIR CodeableConcept data type."""
    coding: List["Coding"] = field(default_factory=list)
    text: Optional[str] = None

@dataclass
class Coding(Element):
    """FHIR Coding data type."""
    system: Optional[str] = None  # Uri
    version: Optional[str] = None
    code: Optional[str] = None  # Code
    display: Optional[str] = None
    userSelected: Optional[bool] = None

@dataclass
class ContactDetail(Element):
    """FHIR ContactDetail data type."""
    name: Optional[str] = None
    telecom: List["ContactPoint"] = field(default_factory=list)

@dataclass
class ContactPoint(Element):
    """FHIR ContactPoint data type."""
    system: Optional[str] = None  # Code
    value: Optional[str] = None
    use: Optional[str] = None  # Code
    rank: Optional[int] = None  # PositiveInt
    period: Optional["Period"] = None

@dataclass
class Contributor(Element):
    """FHIR Contributor data type."""
    type: str  # Required, Code
    name: str  # Required
    contact: List["ContactDetail"] = field(default_factory=list)

@dataclass
class DataRequirement(Element):
    """FHIR DataRequirement data type."""
    type: str  # Required, Code
    profile: List[str] = field(default_factory=list)  # Canonical
    mustSupport: List[str] = field(default_factory=list)
    codeFilter: List[Any] = field(default_factory=list)
    dateFilter: List[Any] = field(default_factory=list)
    limit: Optional[int] = None  # PositiveInt
    sort: List[Any] = field(default_factory=list)

@dataclass
class Dosage(BackboneElement):
    """FHIR Dosage data type."""
    sequence: Optional[int] = None  # Integer
    text: Optional[str] = None
    additionalInstruction: List["CodeableConcept"] = field(default_factory=list)
    patientInstruction: Optional[str] = None
    timing: Optional["Timing"] = None
    asNeededBoolean: Optional[bool] = None
    asNeededCodeableConcept: Optional["CodeableConcept"] = None
    site: Optional["CodeableConcept"] = None
    route: Optional["CodeableConcept"] = None
    method: Optional["CodeableConcept"] = None
    doseAndRate: List["DosageDoseAndRate"] = field(default_factory=list)
    maxDosePerPeriod: Optional["Ratio"] = None
    maxDosePerAdministration: Optional["Quantity"] = None
    maxDosePerLifetime: Optional["Quantity"] = None

@dataclass
class DosageDoseAndRate(Element):
    """FHIR DosageDoseAndRate data type."""
    type: Optional["CodeableConcept"] = None
    doseRange: Optional["Range"] = None
    doseQuantity: Optional["Quantity"] = None
    rateRatio: Optional["Ratio"] = None
    rateRange: Optional["Range"] = None
    rateQuantity: Optional["Quantity"] = None

# Already defined as base class

@dataclass
class ElementDefinition(Element):
    """FHIR ElementDefinition data type."""
    path: str  # Required
    representation: List[str] = field(default_factory=list)  # Code
    sliceName: Optional[str] = None  # String
    sliceIsConstraining: Optional[bool] = None
    label: Optional[str] = None  # String
    code: List["Coding"] = field(default_factory=list)
    slicing: Optional[Any] = None
    short: Optional[str] = None  # String
    definition: Optional[str] = None  # Markdown
    comment: Optional[str] = None  # Markdown
    requirements: Optional[str] = None  # Markdown
    alias: List[str] = field(default_factory=list)  # String
    min: Optional[int] = None  # UnsignedInt
    max: Optional[str] = None  # String
    base: Optional[Any] = None
    contentReference: Optional[str] = None  # Uri
    type: List[Any] = field(default_factory=list)
    defaultValueBase64Binary: Optional[str] = None
    defaultValueBoolean: Optional[bool] = None
    defaultValueCanonical: Optional[str] = None
    defaultValueCode: Optional[str] = None
    defaultValueDate: Optional[str] = None
    defaultValueDateTime: Optional[str] = None
    defaultValueDecimal: Optional[float] = None
    defaultValueId: Optional[str] = None
    defaultValueInstant: Optional[str] = None
    defaultValueInteger: Optional[int] = None
    defaultValueMarkdown: Optional[str] = None
    defaultValueOid: Optional[str] = None
    defaultValuePositiveInt: Optional[int] = None
    defaultValueString: Optional[str] = None
    defaultValueTime: Optional[str] = None
    defaultValueUnsignedInt: Optional[int] = None
    defaultValueUri: Optional[str] = None
    defaultValueUrl: Optional[str] = None
    defaultValueUuid: Optional[str] = None
    defaultValueAddress: Optional["Address"] = None
    defaultValueAge: Optional["Age"] = None
    defaultValueAnnotation: Optional["Annotation"] = None
    defaultValueAttachment: Optional["Attachment"] = None
    defaultValueCodeableConcept: Optional["CodeableConcept"] = None
    defaultValueCoding: Optional["Coding"] = None
    defaultValueContactPoint: Optional["ContactPoint"] = None
    defaultValueCount: Optional["Count"] = None
    defaultValueDistance: Optional["Distance"] = None
    defaultValueDuration: Optional["Duration"] = None
    defaultValueHumanName: Optional["HumanName"] = None
    defaultValueIdentifier: Optional["Identifier"] = None
    defaultValueMoney: Optional["Money"] = None
    defaultValuePeriod: Optional["Period"] = None
    defaultValueQuantity: Optional["Quantity"] = None
    defaultValueRange: Optional["Range"] = None
    defaultValueRatio: Optional["Ratio"] = None
    defaultValueReference: Optional["Reference"] = None
    defaultValueSampledData: Optional["SampledData"] = None
    defaultValueSignature: Optional["Signature"] = None
    defaultValueTiming: Optional["Timing"] = None
    defaultValueContactDetail: Optional["ContactDetail"] = None
    defaultValueContributor: Optional["Contributor"] = None
    defaultValueDataRequirement: Optional["DataRequirement"] = None
    defaultValueExpression: Optional["Expression"] = None
    defaultValueParameterDefinition: Optional["ParameterDefinition"] = None
    defaultValueRelatedArtifact: Optional["RelatedArtifact"] = None
    defaultValueTriggerDefinition: Optional["TriggerDefinition"] = None
    defaultValueUsageContext: Optional["UsageContext"] = None
    defaultValueDosage: Optional["Dosage"] = None
    defaultValueMeta: Optional["Meta"] = None
    meaningWhenMissing: Optional[str] = None  # Markdown
    orderMeaning: Optional[str] = None  # String
    fixedBase64Binary: Optional[str] = None
    fixedBoolean: Optional[bool] = None
    fixedCanonical: Optional[str] = None
    fixedCode: Optional[str] = None
    fixedDate: Optional[str] = None
    fixedDateTime: Optional[str] = None
    fixedDecimal: Optional[float] = None
    fixedId: Optional[str] = None
    fixedInstant: Optional[str] = None
    fixedInteger: Optional[int] = None
    fixedMarkdown: Optional[str] = None
    fixedOid: Optional[str] = None
    fixedPositiveInt: Optional[int] = None
    fixedString: Optional[str] = None
    fixedTime: Optional[str] = None
    fixedUnsignedInt: Optional[int] = None
    fixedUri: Optional[str] = None
    fixedUrl: Optional[str] = None
    fixedUuid: Optional[str] = None
    fixedAddress: Optional["Address"] = None
    fixedAge: Optional["Age"] = None
    fixedAnnotation: Optional["Annotation"] = None
    fixedAttachment: Optional["Attachment"] = None
    fixedCodeableConcept: Optional["CodeableConcept"] = None
    fixedCoding: Optional["Coding"] = None
    fixedContactPoint: Optional["ContactPoint"] = None
    fixedCount: Optional["Count"] = None
    fixedDistance: Optional["Distance"] = None
    fixedDuration: Optional["Duration"] = None
    fixedHumanName: Optional["HumanName"] = None
    fixedIdentifier: Optional["Identifier"] = None
    fixedMoney: Optional["Money"] = None
    fixedPeriod: Optional["Period"] = None
    fixedQuantity: Optional["Quantity"] = None
    fixedRange: Optional["Range"] = None
    fixedRatio: Optional["Ratio"] = None
    fixedReference: Optional["Reference"] = None
    fixedSampledData: Optional["SampledData"] = None
    fixedSignature: Optional["Signature"] = None
    fixedTiming: Optional["Timing"] = None
    fixedContactDetail: Optional["ContactDetail"] = None
    fixedContributor: Optional["Contributor"] = None
    fixedDataRequirement: Optional["DataRequirement"] = None
    fixedExpression: Optional["Expression"] = None
    fixedParameterDefinition: Optional["ParameterDefinition"] = None
    fixedRelatedArtifact: Optional["RelatedArtifact"] = None
    fixedTriggerDefinition: Optional["TriggerDefinition"] = None
    fixedUsageContext: Optional["UsageContext"] = None
    fixedDosage: Optional["Dosage"] = None
    fixedMeta: Optional["Meta"] = None
    patternBase64Binary: Optional[str] = None
    patternBoolean: Optional[bool] = None
    patternCanonical: Optional[str] = None
    patternCode: Optional[str] = None
    patternDate: Optional[str] = None
    patternDateTime: Optional[str] = None
    patternDecimal: Optional[float] = None
    patternId: Optional[str] = None
    patternInstant: Optional[str] = None
    patternInteger: Optional[int] = None
    patternMarkdown: Optional[str] = None
    patternOid: Optional[str] = None
    patternPositiveInt: Optional[int] = None
    patternString: Optional[str] = None
    patternTime: Optional[str] = None
    patternUnsignedInt: Optional[int] = None
    patternUri: Optional[str] = None
    patternUrl: Optional[str] = None
    patternUuid: Optional[str] = None
    patternAddress: Optional["Address"] = None
    patternAge: Optional["Age"] = None
    patternAnnotation: Optional["Annotation"] = None
    patternAttachment: Optional["Attachment"] = None
    patternCodeableConcept: Optional["CodeableConcept"] = None
    patternCoding: Optional["Coding"] = None
    patternContactPoint: Optional["ContactPoint"] = None
    patternCount: Optional["Count"] = None
    patternDistance: Optional["Distance"] = None
    patternDuration: Optional["Duration"] = None
    patternHumanName: Optional["HumanName"] = None
    patternIdentifier: Optional["Identifier"] = None
    patternMoney: Optional["Money"] = None
    patternPeriod: Optional["Period"] = None
    patternQuantity: Optional["Quantity"] = None
    patternRange: Optional["Range"] = None
    patternRatio: Optional["Ratio"] = None
    patternReference: Optional["Reference"] = None
    patternSampledData: Optional["SampledData"] = None
    patternSignature: Optional["Signature"] = None
    patternTiming: Optional["Timing"] = None
    patternContactDetail: Optional["ContactDetail"] = None
    patternContributor: Optional["Contributor"] = None
    patternDataRequirement: Optional["DataRequirement"] = None
    patternExpression: Optional["Expression"] = None
    patternParameterDefinition: Optional["ParameterDefinition"] = None
    patternRelatedArtifact: Optional["RelatedArtifact"] = None
    patternTriggerDefinition: Optional["TriggerDefinition"] = None
    patternUsageContext: Optional["UsageContext"] = None
    patternDosage: Optional["Dosage"] = None
    patternMeta: Optional["Meta"] = None
    example: List[Any] = field(default_factory=list)
    minValueDate: Optional[str] = None
    minValueDateTime: Optional[str] = None
    minValueInstant: Optional[str] = None
    minValueTime: Optional[str] = None
    minValueDecimal: Optional[float] = None
    minValueInteger: Optional[int] = None
    minValuePositiveInt: Optional[int] = None
    minValueUnsignedInt: Optional[int] = None
    minValueQuantity: Optional["Quantity"] = None
    maxValueDate: Optional[str] = None
    maxValueDateTime: Optional[str] = None
    maxValueInstant: Optional[str] = None
    maxValueTime: Optional[str] = None
    maxValueDecimal: Optional[float] = None
    maxValueInteger: Optional[int] = None
    maxValuePositiveInt: Optional[int] = None
    maxValueUnsignedInt: Optional[int] = None
    maxValueQuantity: Optional["Quantity"] = None
    maxLength: Optional[int] = None  # Integer
    condition: List[str] = field(default_factory=list)  # Id
    constraint: List[Any] = field(default_factory=list)
    mustSupport: Optional[bool] = None
    isModifier: Optional[bool] = None
    isModifierReason: Optional[str] = None  # String
    isSummary: Optional[bool] = None
    binding: Optional[Any] = None
    mapping: List[Any] = field(default_factory=list)

@dataclass
class Expression(Element):
    """FHIR Expression data type."""
    description: Optional[str] = None  # String
    name: Optional[str] = None  # Id
    language: str  # Required, Code
    expression: Optional[str] = None  # String
    reference: Optional[str] = None  # Uri

# Already defined

@dataclass
class HumanName(Element):
    """FHIR HumanName data type."""
    use: Optional[str] = None  # Code
    text: Optional[str] = None  # String
    family: Optional[str] = None  # String
    given: List[str] = field(default_factory=list)  # String
    prefix: List[str] = field(default_factory=list)  # String
    suffix: List[str] = field(default_factory=list)  # String
    period: Optional["Period"] = None

@dataclass
class Identifier(Element):
    """FHIR Identifier data type."""
    use: Optional[str] = None  # Code
    type: Optional["CodeableConcept"] = None
    system: Optional[str] = None  # Uri
    value: Optional[str] = None  # String
    period: Optional["Period"] = None
    assigner: Optional["Reference"] = None

@dataclass
class Meta(Element):
    """FHIR Meta data type."""
    versionId: Optional[str] = None  # Id
    lastUpdated: Optional[str] = None  # Instant
    source: Optional[str] = None  # Uri
    profile: List[str] = field(default_factory=list)  # Canonical
    security: List["Coding"] = field(default_factory=list)
    tag: List["Coding"] = field(default_factory=list)

@dataclass
class Money(Element):
    """FHIR Money data type."""
    value: Optional[float] = None  # Decimal
    currency: Optional[str] = None  # Code

@dataclass
class Narrative(Element):
    """FHIR Narrative data type."""
    status: str  # Required, Code
    div: str  # Required, Xhtml

@dataclass
class ParameterDefinition(Element):
    """FHIR ParameterDefinition data type."""
    name: Optional[str] = None  # Code
    use: str  # Required, Code
    min: Optional[int] = None  # Integer
    max: Optional[str] = None  # String
    documentation: Optional[str] = None  # String
    type: str  # Required, Code
    profile: Optional[str] = None  # Canonical

@dataclass
class Period(Element):
    """FHIR Period data type."""
    start: Optional[str] = None  # DateTime
    end: Optional[str] = None  # DateTime

@dataclass
class Quantity(Element):
    """FHIR Quantity data type."""
    value: Optional[float] = None  # Decimal
    comparator: Optional[str] = None  # Code
    unit: Optional[str] = None  # String
    system: Optional[str] = None  # Uri
    code: Optional[str] = None  # Code

@dataclass
class Range(Element):
    """FHIR Range data type."""
    low: Optional["Quantity"] = None
    high: Optional["Quantity"] = None

@dataclass
class Ratio(Element):
    """FHIR Ratio data type."""
    numerator: Optional["Quantity"] = None
    denominator: Optional["Quantity"] = None

@dataclass
class RatioRange(Element):
    """
    FHIR RatioRange data type.
    
    A range of ratios expressed as a low and high ratio.
    Used in various resources to represent ranges of ratios.
    """
    lowNumerator: Optional["Quantity"] = None
    highNumerator: Optional["Quantity"] = None
    denominator: Optional["Quantity"] = None

@dataclass
class SubstanceAmount(Element):
    """
    FHIR SubstanceAmount data type.
    
    Chemical substances are a single substance type whose primary defining element
    is the molecular structure. Chemical substances shall be defined on the basis
    of their complete covalent molecular structure; the presence of a salt (counter-ion)
    and/or solvates (water, alcohols) is also captured.
    """
    amountQuantity: Optional["Quantity"] = None
    amountRange: Optional["Range"] = None
    amountString: Optional[str] = None
    amountType: Optional["CodeableConcept"] = None
    amountText: Optional[str] = None
    referenceRange: Optional["Element"] = None

@dataclass
class Reference(Element):
    """FHIR Reference data type."""
    reference: Optional[str] = None  # String
    type: Optional[str] = None  # Uri
    identifier: Optional["Identifier"] = None
    display: Optional[str] = None  # String

@dataclass
class RelatedArtifact(Element):
    """FHIR RelatedArtifact data type."""
    type: str  # Required, Code
    label: Optional[str] = None  # String
    display: Optional[str] = None  # String
    citation: Optional[str] = None  # Markdown
    url: Optional[str] = None  # Url
    document: Optional["Attachment"] = None
    resource: Optional[str] = None  # Canonical

@dataclass
class SampledData(Element):
    """FHIR SampledData data type."""
    origin: "Quantity"  # Required
    period: float  # Required, Decimal
    factor: Optional[float] = None  # Decimal
    lowerLimit: Optional[float] = None  # Decimal
    upperLimit: Optional[float] = None  # Decimal
    dimensions: int  # Required, PositiveInt
    data: Optional[str] = None  # String

@dataclass
class Signature(Element):
    """FHIR Signature data type."""
    type: List["Coding"] = field(default_factory=list)  # Required
    when: str  # Required, Instant
    who: "Reference"  # Required
    onBehalfOf: Optional["Reference"] = None
    targetFormat: Optional[str] = None  # Code
    sigFormat: Optional[str] = None  # Code
    data: Optional[str] = None  # Base64Binary

@dataclass
class Timing(BackboneElement):
    """FHIR Timing data type."""
    event: List[str] = field(default_factory=list)  # DateTime
    repeat: Optional[Any] = None
    code: Optional["CodeableConcept"] = None

@dataclass
class TriggerDefinition(Element):
    """FHIR TriggerDefinition data type."""
    type: str  # Required, Code
    name: Optional[str] = None  # String
    timingTiming: Optional["Timing"] = None
    timingReference: Optional["Reference"] = None
    timingDate: Optional[str] = None  # Date
    timingDateTime: Optional[str] = None  # DateTime
    data: List["DataRequirement"] = field(default_factory=list)
    condition: Optional["Expression"] = None

@dataclass
class ProdCharacteristic(Element):
    '''
    FHIR ProdCharacteristic data type.
    
    The marketing status describes the date when a medicinal product is actually put on the market
    or the date as of which it is no longer available.
    '''
    height: Optional["Quantity"] = None
    width: Optional["Quantity"] = None
    depth: Optional["Quantity"] = None
    weight: Optional["Quantity"] = None
    nominalVolume: Optional["Quantity"] = None
    externalDiameter: Optional["Quantity"] = None
    shape: Optional[str] = None  # String
    color: List[str] = field(default_factory=list)  # List of strings
    imprint: List[str] = field(default_factory=list)  # List of strings
    image: List["Attachment"] = field(default_factory=list)
    scoring: Optional["CodeableConcept"] = None


@dataclass
class ProductShelfLife(Element):
    '''
    FHIR ProductShelfLife data type.
    
    The shelf-life and storage information for a medicinal product item or container can be described
    using this class.
    '''
    identifier: Optional["Identifier"] = None
    type: "CodeableConcept"  # Required
    period: "Quantity"  # Required
    specialPrecautionsForStorage: List["CodeableConcept"] = field(default_factory=list)


@dataclass
class MarketingStatus(Element):
    '''
    FHIR MarketingStatus data type.
    
    The marketing status describes the date when a medicinal product is actually put on the market
    or the date as of which it is no longer available.
    '''
    country: Optional["CodeableConcept"] = None
    jurisdiction: Optional["CodeableConcept"] = None
    status: "CodeableConcept"  # Required
    dateRange: Optional["Period"] = None
    restoreDate: Optional[str] = None  # ISO 8601 dateTime
    """FHIR UsageContext data type."""
    code: "Coding"  # Required
    valueCodeableConcept: Optional["CodeableConcept"] = None
    valueQuantity: Optional["Quantity"] = None
    valueRange: Optional["Range"] = None
    valueReference: Optional["Reference"] = None
