"""
A module to represent a Sensu entity resource
"""
# Built in imports
from typing import Optional, List, Dict, Literal, Any

# Our imports
from sensu.resources.base import ResourceBase
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/entities"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching entity resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class EntityMetadata(BaseModel):
    """
    A class to represent the data structure of a cluster-role metadata
    """
    name: str
    namespace: str
    created_by: Optional[str] = None
    labels: Optional[dict[str, str]] = {}
    annotations: Optional[dict[str, str]] = {}



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

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the entity resource(s).

        :return: The URL for the entity resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
