# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.


"""
FHIR R5 SubscriptionStatus resource.

The SubscriptionStatus resource describes the state of a Subscription during notifications. It is not persisted.
"""

from dataclasses import dataclass, field
from dnhealth.dnhealth_fhir.resources.base import FHIRResource
from dnhealth.dnhealth_fhir.types import BackboneElement, CodeableConcept, Extension, Reference
from typing import Any, List, Optional

@dataclass
class SubscriptionStatusNotificationEvent:
    """
    SubscriptionStatusNotificationEvent nested class.
    """

    eventNumber: Optional[Any] = None  # Either the sequential number of this event in this subscription context or a relative event numbe...
    id: Optional[str] = None  # Unique id for the element within a resource (for internal references). This may be any string val...
    extension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    modifierExtension: Optional[List[Extension]] = field(default_factory=list)  # May be used to represent additional information that is not part of the basic definition of the e...
    timestamp: Optional[str] = None  # The actual time this event occurred on the server.
    focus: Optional[Reference] = None  # The focus of this event. While this will usually be a reference to the focus resource of the even...
    additionalContext: Optional[List[Reference]] = field(default_factory=list)  # Additional context information for this event. Generally, this will contain references to additio...


@dataclass
class SubscriptionStatus(FHIRResource):
    """
    The SubscriptionStatus resource describes the state of a Subscription during notifications. It is not persisted.
    """

    type: Optional[str] = None  # The type of event being conveyed with this notification.
    subscription: Optional[Reference] = None  # The reference to the Subscription which generated this notification.
    resourceType: str = "SubscriptionStatus"
    status: Optional[str] = None  # The status of the subscription, which marks the server state for managing the subscription.
    eventsSinceSubscriptionStart: Optional[Any] = None  # The total number of actual events which have been generated since the Subscription was created (i...
    notificationEvent: Optional[List[BackboneElement]] = field(default_factory=list)  # Detailed information about events relevant to this subscription notification.
    topic: Optional[str] = None  # The reference to the SubscriptionTopic for the Subscription which generated this notification.
    error: Optional[List[CodeableConcept]] = field(default_factory=list)  # A record of errors that occurred when the server processed a notification.