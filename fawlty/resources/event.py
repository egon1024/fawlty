"""
A module to represent a Sensu event resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal, Any, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient


# 3rd party imports


class EventMetadata(ResourceBase):
    """
    A class to represent the data structure of an event metadata
    """
    namespace: str


class EventCheckMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a check metadata
    """


class EventCheckHistory(ResourceBase):
    """
    A class to represent the data structure of an event check history
    """
    status: int
    executed: int


class EventCheckMetricTag(ResourceBase):
    """
    A class to represent the data structure of an event check metric tag
    """
    name: str
    value: str


class EventCheckSecret(ResourceBase):
    """
    A class to represent the data structure of an event check secret
    """
    name: str
    secret: str


class EventCheckSubdue(ResourceBase):
    """
    A class to represent the data structure of a check subdue
    """
    begin: str
    end: str
    repeat: Optional[List[Literal[
        "mondays", "tuesdays", "wednesdays", "thursdays", "fridays", "saturdays", "sundays"
        "weekdays", "weekends", "daily", "weekly", "monthly", "annually"
    ]]] = None


class EventCheck(ResourceBase):
    """
    A class to represent the data structure of checks in the context of an event
    """
    metadata: EventCheckMetadata
    check_hooks: Optional[List[Dict[str, List[str]]]] = None
    command: Optional[str] = None   # Optional because of keepalive checks
    duration: Optional[float] = None
    env_vars: Optional[List[str]] = None
    executed: int
    handlers: Optional[List[str]] = None
    high_flap_threshold: Optional[int] = None
    history: List[EventCheckHistory]
    interval: Optional[int] = None
    is_silenced: bool
    issued: int
    last_ok: int
    low_flap_threshold: Optional[int] = None
    occurrences: int
    occurrences_watermark: int
    output: Optional[str] = None
    output_metric_format: Optional[str] = None
    output_metric_handlers: Optional[List[str]] = None
    pipelines: Optional[List[EventCheckMetricTag]] = None
    processed_by: Optional[str] = None
    proxy_entity_name: Optional[str] = None
    publish: Optional[bool] = False
    round_robin: Optional[bool] = False
    runtime_assets: Optional[List[str]] = None
    scheduler: Optional[str] = None
    secrets: Optional[List[EventCheckSecret]] = None
    status: int
    state: Literal["passing", "flapping", "failing"]
    status: int
    stdin: Optional[bool] = False
    subdue: Optional[EventCheckSubdue] = None
    subscriptions: Optional[List[str]] = None
    timeout: Optional[int] = None
    total_state_change: int
    ttl: Optional[int] = None


class EventEntityMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a check metadata
    """


class EventEntity(ResourceBase):
    """
    A class to represent the data structure of an event entity
    """
    metadata: EventEntityMetadata
    deregister: bool
    deregistration: Optional[Dict[str, str]] = None
    entity_class: Literal["agent", "proxy", "service"]
    last_seen: int
    redact: Optional[List[str]] = []
    sensu_agent_version: str
    subscriptions: List[str] = None
    system: Optional[Dict[str, Any]] = None
    user: Optional[str] = "agent"


class Event(ResourceBase):
    """
    A class to represent a Sensu event resource
    """
    check: Optional[EventCheck] = None
    entity: Optional[EventEntity] = None
    pipelines: Optional[List[str]] = None  # Might need to play with this a bit
    id: str
    sequence: Optional[int] = None
    timestamp: Optional[int] = None
    metadata: Optional[EventMetadata]
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/events"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the namespaced version of the class method.
        """
        return cls.get_url_with_namespace(*args, **kwargs)

    # pylint: disable=W0613
    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the event resource(s).

        :return: The URL for the event resource.
        """

        # We ignore "purpose" because we don't need it for events

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        return url
