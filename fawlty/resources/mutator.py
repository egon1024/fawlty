"""
A module for Sensu mutator resources.
"""

# Built in imports
from typing import Optional, List, Dict, Literal, ClassVar

# 3rd party imports
from pydantic import model_validator

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient


class MutatorMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a mutator metadata
    """


class Mutator(ResourceBase):
    """
    A class to represent a Sensu mutator resource.
    """
    command: Optional[str] = None
    env_vars: Optional[List[str]] = None
    eval: Optional[str] = None
    runtime_assets: Optional[List[str]] = None
    secrets: Optional[List[Dict[str, str]]] = None
    timeout: int = 30
    type: Literal['pipe', 'javascript'] = 'pipe'
    metadata: MutatorMetadata
    _sensu_client: Optional[SensuClient] = None

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate the values of the fields in the instance
        """

        # If type is pipe, command should be set and eval should not
        if self.type == "pipe":
            if not self.command:
                raise ValueError(
                    "If type is 'pip', the 'command' attribute must be set."
                )
            if self.eval is not None:
                raise ValueError(
                    "If type is 'pipe', the 'eval' attribute must not be set."
                )

        elif self.type == "javascript":
            if not self.eval:
                raise ValueError(
                    "If type is 'javascript', the 'eval' attribute must be set."
                )
            if self.command is not None:
                raise ValueError(
                    "If type is 'javascript', the 'command' attribute must not be set."
                )

        return self

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/mutators"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the namespaced version of the class method.
        """
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the mutator resource(s).

        :return: The URL for the mutator resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
