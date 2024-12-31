"""
A module to represent a Sensu clusterrole resource
"""

# Built in imports
from typing import Optional, List, Literal, ClassVar

# 3rd party imports
from pydantic import BaseModel, field_validator

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithoutNamespace
from fawlty.sensu_client import SensuClient


class ClusterRoleMetadata(MetadataWithoutNamespace):
    """
    A class to represent the data structure of a cluster-role metadata
    """


class ClusterRoleRule(BaseModel):
    """
    A class to represent the data structure of a cluster-role rule
    """
    verbs: List[Literal['*', 'get', 'list', 'create', 'update', 'delete']]
    resources: List[Literal[
        # Special
        '*', 'localselfuser',

        # Namespaced
        'assets', 'checks', 'entities', 'events', 'extensions', 'filters', 'handlers', 'hooks',
        'mutators', 'pipelines', 'rolebindings', 'roles', 'rule-templates', 'searches',
        'secrets', 'service-components', 'silenced', 'sumo-logic-metrics-handlers',
        'tcp-stream-handlers',

        # Non namespaced
        'apikeys', 'authproviders', 'clusterrolebindings', 'clusterroles', 'clusters', 'config',
        'etcd-replicators', 'license', 'namespaces', 'provider', 'providers', 'users'
    ]]
    resource_names: Optional[List[str]] = None

    @field_validator("verbs")
    def validate_verbs(cls, value):
        """
        Validate the verb list
        """
        if "*" in value and len(value) > 1:
            raise ValueError("if '*' is in the list, it must be the only item.")
        return value

    @field_validator("resources")
    def validate_resources(cls, value):
        """
        Validate the resource list
        """
        if "*" in value and len(value) > 1:
            raise ValueError("if '*' is in the list, it must be the only item.")
        return value


class ClusterRole(ResourceBase):
    """
    A class to represent a Sensu clusterrole resource
    """

    metadata: ClusterRoleMetadata
    rules: List[ClusterRoleRule]
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/clusterroles"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the non-namespaced version of the class method.
        """
        return cls.get_url_without_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the clusterrole resource.

        :return: The URL for the clusterrole resource.
        """

        url = self.BASE_URL

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
