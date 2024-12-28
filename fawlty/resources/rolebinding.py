"""
A module to represent a Sensu rolebinding resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator


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

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/rolebindings"
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_with_namespace(*args, **kwargs

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the rolebinding resource(s).

        :return: The URL for the rolebinding resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
