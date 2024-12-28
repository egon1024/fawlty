"""
A module to represent a Sensu asset resource
"""

# Built in imports
from typing import Optional, Dict, List, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient


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

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/assets"
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the asset resource(s).

        :return: The URL for the asset resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
