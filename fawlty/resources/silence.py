"""
A module for Sensu silence resources.
"""

# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from sensu.resources.base import ResourceBase, MetadataWithNamespace
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, model_validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/silenced"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching silenced resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class SilenceMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a silence metadata
    """


class Silence(ResourceBase):
    check: Optional[str] = None
    subscription: Optional[str] = None
    begin: int = None
    expire: int = None
    expire_at: int = None
    expire_on_resolve: bool = False
    creator: Optional[str] = None
    reason: Optional[str] = None
    metadata: SilenceMetadata

    @model_validator(mode='after')
    def check_fields(self):
        # If neither "check" nor "subscription" is set, there's a problem
        if not self.check and not self.subscription:
            raise ValueError("One of either 'check' or 'subscription' must be set.")

        return self

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the silence resource(s).

        :return: The URL for the handler resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url 
