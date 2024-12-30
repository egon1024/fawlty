"""
A module to represent a Sensu entity resource
"""
# Built in imports
from typing import Optional, List, Dict, Literal, Any, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import validator


class EntityMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a cluster-role metadata
    """


class Entity(ResourceBase):
    """
    A class to represent a Sensu entity resource
    """

    metadata: EntityMetadata
    deregister: bool = False
    entity_class: Literal["agent", "proxy", "service"]
    deregistration: Optional[Dict[str, str]]
    last_seen: Optional[int] = 0
    redact: Optional[List[str]] = []
    sensu_agent_version: str
    subscriptions: List[str]
    system: Optional[Dict[str, Any]] = None
    user: Optional[str] = "agent"
    _sensu_client: Optional[SensuClient] = None

    @validator("deregistration")
    def validate_deregistration(cls, value):

        # Allow an empty dictionary or None
        if not value:
            return value

        # Validate that there is exactly one key
        if len(value) > 1:
            raise ValueError("The 'deregistration' dictionary can contain at most one key.")

        # Validate that the only valid key is 'handler'
        if "handler" not in value:
            raise ValueError("The only valid key in 'deregistration' is 'handler'.")

        return value

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/entities"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the entity resource(s).

        :return: The URL for the entity resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
