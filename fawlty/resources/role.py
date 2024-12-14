"""
A module to represent a Sensu role resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from sensu.resources.base import ResourceBase, MetadataWithNamespace
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/roles"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching role resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class RoleMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a filter metadata
    """


class RoleRule(BaseModel):
    """
    A class to represent the data structure of a role rule
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


class Role(ResourceBase):
    """
    A class to represent a Sensu role resource
    """

    metadata: RoleMetadata
    rules: List[RoleRule]
    _sensu_client: Optional[SensuClient] = None

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the role resource(s).

        :return: The URL for the role resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
