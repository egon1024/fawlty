"""
A module to represent a Sensu clusterrole resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from sensu.resources.base import ResourceBase
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/clusterroles"


def get_url(name: str = None) -> str:
    """
    Get a url to retrieve a list of matching clusterrole resources.
    """

    url = BASE_URL
    if name is not None:
        url += f"/{name}"
    
    return url


class ClusterRoleMetadata(BaseModel):
    """
    A class to represent the data structure of a cluster-role metadata
    """
    name: str
    created_by: Optional[str] = None
    labels: Optional[dict[str, str]] = {}
    annotations: Optional[dict[str, str]] = {}


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

    @validator("verbs")
    def validate_verbs(cls, value):
        if "*" in value and len(value) > 1:
            raise valueerror("if '*' is in the list, it must be the only item.")
        return value

    @validator("resources")
    def validate_resources(cls, value):
        if "*" in value and len(value) > 1:
            raise valueerror("if '*' is in the list, it must be the only item.")
        return value


class ClusterRole(ResourceBase):
    """
    A class to represent a Sensu clusterrole resource
    """

    metadata: ClusterRoleMetadata
    rules: List[ClusterRoleRule]
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


