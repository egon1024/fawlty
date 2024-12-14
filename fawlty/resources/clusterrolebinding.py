"""
A module to represent a Sensu clusterrolebinding resource
"""
# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithoutNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/clusterrolebindings"

def get_url(name: str = None) -> str:
    """
    Get a url to retrieve a list of matching clusterrolebinding resources.
    """

    url = BASE_URL
    if name is not None:
        url += f"/{name}"
    
    return url


class ClusterRoleBindingMetadata(MetadataWithoutNamespace):
    """
    A class to represent the data structure of a clusterrole-binding metadata
    """


class ClusterRoleBindingSubject(BaseModel):
    """
    A class to represent the data structure of a clusterrole-binding subject
    """
    name: str
    type: Literal["Group", "User"]


class ClusterRoleBindingRoleRef(BaseModel):
    """
    A class to represent the data structure of a clusterrole-binding role_ref
    """
    name: str
    type: Literal["ClusterRole"] = "ClusterRole"


class ClusterRoleBinding(ResourceBase):
    """
    A class to represent a Sensu clusterrolebinding resource
    """
    metadata: ClusterRoleBindingMetadata
    role_ref: ClusterRoleBindingRoleRef
    subjects: List[ClusterRoleBindingSubject]
    _sensu_client: Optional[SensuClient] = None

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the clusterrole resource.

        :return: The URL for the clusterrole resource.
        """

        url = BASE_URL

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url


