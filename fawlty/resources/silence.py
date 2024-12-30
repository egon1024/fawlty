"""
A module for Sensu silence resources.
"""

# Built in imports
from typing import Optional, ClassVar

# 3rd party imports
from pydantic import model_validator

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient


class SilenceMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a silence metadata
    """


class Silence(ResourceBase):
    """
    A class to represent a Sensu silence resource
    """
    check: Optional[str] = None
    subscription: Optional[str] = None
    begin: int = None
    expire: int = None
    expire_at: int = None
    expire_on_resolve: bool = False
    creator: Optional[str] = None
    reason: Optional[str] = None
    metadata: SilenceMetadata
    _sensu_client: Optional[SensuClient] = None

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate the fields of a Silence instance
        """
        # If neither "check" nor "subscription" is set, there's a problem
        if not self.check and not self.subscription:
            raise ValueError("One of either 'check' or 'subscription' must be set.")

        return self

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/silenced"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        """
        Use the namespaced version of the class method.
        """
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the silence resource(s).

        :return: The URL for the handler resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)
        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
