"""
A module to represent a Sensu clusterrolebinding resource
"""
# Built in imports
from typing import Optional, List, Dict, Literal, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithoutNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

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

    BASE_URL: ClassVar[str] = "/api/core/v2/clusterrolebindings"
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_without_namespace(*args, **kwargs)

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the clusterrole resource.

        :return: The URL for the clusterrole resource.
        """

        url = self.BASE_URL

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url


