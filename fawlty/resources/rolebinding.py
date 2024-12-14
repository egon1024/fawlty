"""
A module to represent a Sensu rolebinding resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/rolebindings"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching rolebindings resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class RoleBindingMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a rolebinding metadata
    """


class RoleBindingSubject(BaseModel):
    """
    A class to represent the data structure of a rolebinding subject
    """
    name: str
    type: Literal["Group", "User"]


class RoleBindingRoleRef(BaseModel):
    """
    A class to represent the data structure of a rolebinding role_ref
    """
    name: str
    type: Literal["Role"] = "Role"


class RoleBinding(ResourceBase):
    """
    A class to represent a Sensu rolebinding resource
    """

    metadata: RoleBindingMetadata
    role_ref: RoleBindingRoleRef
    subjects: List[RoleBindingSubject]
    _sensu_client: Optional[SensuClient] = None


    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the rolebinding resource(s).

        :return: The URL for the rolebinding resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
