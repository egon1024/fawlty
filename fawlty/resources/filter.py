"""
A module to represent a Sensu filter resource
"""

# Built in imports
from typing import Optional, List, Literal, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports


class FilterMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a filter metadata
    """


class Filter(ResourceBase):
    """
    A class to represent a Sensu filter resource
    """

    action: Literal["allow", "deny"]
    expressions: List[str] = []
    runtime_assets: Optional[List[str]] = []
    metadata: FilterMetadata
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/filters"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the filter resource(s).

        :return: The URL for the filter resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
