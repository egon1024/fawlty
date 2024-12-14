"""
A module to represent a Sensu asset resource
"""

# Built in imports
from typing import Optional, Dict, List

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/assets"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching asset resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class AssetMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of an asset metadata
    """


class Asset(ResourceBase):
    """
    A class to represent a Sensu asset resource
    """

    url: str
    sha512: str
    filters: Optional[List[str]] = []
    headers: Optional[Dict[str, str]] = {}
    metadata: AssetMetadata
    _sensu_client: Optional[SensuClient] = None

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the asset resource(s).

        :return: The URL for the asset resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
