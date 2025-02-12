"""
A module for Sensu hook resources.
"""

# Built in imports
from typing import Optional, List, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports


class HookMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a hook metadata
    """


class Hook(ResourceBase):
    """
    A class to represent a Sensu hook resource.
    """
    command: str
    runtime_assets: Optional[List[str]] = None
    stdin: Optional[bool] = False
    timeout: Optional[int] = 60
    metadata: HookMetadata
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/hooks"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the namespaced version of the class method.
        """
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the hook resource(s).

        :return: The URL for the hook resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
