"""
A module to represent a Sensu namespace resource
"""

# Built in imports
from typing import Optional, ClassVar

# My imports
from fawlty.resources.base import ResourceBase
from fawlty.sensu_client import SensuClient


class Namespace(ResourceBase):
    """
    A class to represent a Sensu namespace resource
    """

    name: str
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_without_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the namespace resource(s).

        :return: The URL for the namespace resource.
        """

        url = self.BASE_URL

        if purpose != "create":
            url += f"/{self.name}"

        return url
