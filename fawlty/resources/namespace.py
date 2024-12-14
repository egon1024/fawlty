"""
A module to represent a Sensu namespace resource
"""

# Built in imports
from typing import Optional

# My imports
from sensu.resources.base import ResourceBase
from sensu.client import SensuClient

# Constants
BASE_URL = "/api/core/v2/namespaces"

def get_url(name: str=None) -> str:
    """
    Get a url to retrieve a list of matching namespace resources.
    """

    url = BASE_URL

    if name is not None:
        url += f"/{name}"

    return BASE_URL
    

class Namespace(ResourceBase):
    """
    A class to represent a Sensu namespace resource
    """

    name: str
    _sensu_client: Optional[SensuClient] = None

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the namespace resource(s).

        :return: The URL for the namespace resource.
        """

        url = BASE_URL

        if purpose != "create":
            url = f"{BASE_URL}/{self.name}"

        return url

