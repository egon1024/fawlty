"""
A module to represent a Sensu role resource
"""

# Built in imports
from typing import Optional, List, Literal, ClassVar

# 3rd party imports
from pydantic import BaseModel, validator

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient


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
        """
        Make sure the verb(s) passed in are valid
        """
        if "*" in value and len(value) > 1:
            raise ValueError("if '*' is in the list, it must be the only item.")
        return value

    @validator("resources")
    def validate_resources(cls, value):
        """
        Make sure the list of resources is valid
        """
        if "*" in value and len(value) > 1:
            raise ValueError("if '*' is in the list, it must be the only item.")
        return value


class Role(ResourceBase):
    """
    A class to represent a Sensu role resource
    """

    metadata: RoleMetadata
    rules: List[RoleRule]
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/roles"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the namespaced version of the class method.
        """
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the role resource(s).

        :return: The URL for the role resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
