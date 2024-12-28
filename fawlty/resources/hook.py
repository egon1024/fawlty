"""
A module for Sensu hook resources.
"""

# Built in imports
from typing import Optional, List, Dict, Literal, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel, model_validator

class HookMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a hook metadata
    """


class Hook(ResourceBase):
    """
    A class to represent a Sensu hook resource.
    """
    command: str
    runtime_assets: Optional[List[str]] = None
    stdin: Optional[bool] = False
    timeout: Optional[int] = 60
    metadata: HookMetadata

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/hooks"

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the hook resource(s).

        :return: The URL for the hook resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
