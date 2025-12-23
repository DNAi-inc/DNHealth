# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 Subscription resource.

The subscription resource describes a particular client's request to be notified about a SubscriptionTopic.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, Coding, ContactPoint, Extension, Identifier, Reference
from typing import List, Optional

@dataclass
class SubscriptionFilterBy:
    """
    SubscriptionFilterBy nested class.
    """

    filterParameter: Optional[str] = None  # The filter as defined in the `SubscriptionTopic.canFilterBy.filterParameter` element.
    value: Optional[str] = None  # The literal value or resource path as is legal in search - for example, `Patient/123` or `le1950`.
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    resourceType: Optional[str] = None  # A resource listed in the `SubscriptionTopic` this `Subscription` references (`SubscriptionTopic.c...
    comparator: Optional[str] = None  # Comparator applied to this filter parameter.
    modifier: Optional[str] = None  # Modifier applied to this filter parameter.

@dataclass
class SubscriptionParameter:
    """
    SubscriptionParameter nested class.
    """

    name: Optional[str] = None  # Parameter name for information passed to the channel for notifications, for example in the case o...
    value: Optional[str] = None  # Parameter value for information passed to the channel for notifications, for example in the case ...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...


@dataclass
class Subscription(FHIRResource):
    """
    The subscription resource describes a particular client's request to be notified about a SubscriptionTopic.
    """

    status: Optional[str] = None  # The status of the subscription, which marks the server state for managing the subscription.
    topic: Optional[str] = None  # The reference to the subscription topic to be notified about.
    channelType: Optional[Coding] = None  # The type of channel to send notifications on.
    resourceType: str = "Subscription"
    identifier: Optional[List[Identifier]] = field(default_factory=list)  # A formal identifier that is used to identify this code system when it is represented in other for...
    name: Optional[str] = None  # A natural language name identifying the subscription.
    contact: Optional[List[ContactPoint]] = field(default_factory=list)  # Contact details for a human to contact about the subscription. The primary use of this for system...
    end: Optional[str] = None  # The time for the server to turn the subscription off.
    managingEntity: Optional[Reference] = None  # Entity with authorization to make subsequent revisions to the Subscription and also determines wh...
    reason: Optional[str] = None  # A description of why this subscription is defined.
    filterBy: Optional[List[BackboneElement]] = field(default_factory=list)  # The filter properties to be applied to narrow the subscription topic stream.  When multiple filte...
    endpoint: Optional[str] = None  # The url that describes the actual end-point to send notifications to.
    parameter: Optional[List[BackboneElement]] = field(default_factory=list)  # Channel-dependent information to send as part of the notification (e.g., HTTP Headers).
    heartbeatPeriod: Optional[int] = None  # If present, a 'heartbeat' notification (keep-alive) is sent via this channel with an interval per...
    timeout: Optional[int] = None  # If present, the maximum amount of time a server will allow before failing a notification attempt.
    contentType: Optional[str] = None  # The MIME type to send the payload in - e.g., `application/fhir+xml` or `application/fhir+json`. N...
    content: Optional[str] = None  # How much of the resource content to deliver in the notification payload. The choices are an empty...
    maxCount: Optional[int] = None  # If present, the maximum number of events that will be included in a notification bundle. Note tha...