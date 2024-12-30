"""
A module for Sensu handler resources.
"""

# Built in imports
from typing import Optional, List, Dict, Literal, ClassVar

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import BaseModel, model_validator


class HandlerMetadata(MetadataWithNamespace):
    """
    A class to represent the data structure of a handler metadata
    """


class HandlerSocket(BaseModel):
    host: str
    port: int


class Handler(ResourceBase):
    """
    A class to represent a Sensu handler resource.
    """
    type: Literal["pipe", "tcp", "udp", "set"]
    command: Optional[str] = None
    env_vars: Optional[List[str]] = None
    filters: Optional[List[str]] = None
    handlers: Optional[List[str]] = None
    mutator: Optional[str] = None
    runtime_assets: Optional[List[str]] = None
    secrets: Optional[List[Dict[str, str]]] = None
    socket: Optional[HandlerSocket] = None
    timeout: Optional[int] = 60
    metadata: HandlerMetadata
    _sensu_client: Optional[SensuClient] = None

    @model_validator(mode='after')
    def check_fields(self):
        # If type is "set", handlers must be defined
        if self.type == "set":
            if not self.handlers:
                raise ValueError("If type is 'set', the 'handlers' attribute must be set.")

        # If type is "udp" or "tcp", socket must be defined
        if self.type in ("udp", "tcp"):
            if not self.socket:
                raise ValueError("If type is 'udp' or 'tcp', the 'socket' attribute must be set.")

        # Command is only usable for pipe handlers
        if self.command and self.type != "pipe":
            raise ValueError("Attribute 'command' is only valid when type='pipe'")

        # env_vars is only usable for pipe handlers
        if self.env_vars and self.type != "pipe":
            raise ValueError("Attribute 'env_vars' is only valid when type='pipe'")

        # handlers is only usable for set handlers
        if self.handlers and self.type != "set":
            raise ValueError("Attribute 'handlers' is only valid when type='set'")

        # socket is only usable for "udp" and "tcp" handlers
        if self.socket and self.type not in ("udp", "tcp"):
            raise ValueError("Attribute 'socket' is only valid when type='udp' or type='tcp'")

        # Secrets dictionaries must have exactly two keys, "name" and "secret"
        if self.secrets:
            valid_key_set = set(("name", "secret"))

            for entry in self.secrets:
                if entry.keys() != valid_key_set:
                    raise ValueError(
                        "Secrets dictionaries must have exactly two keys: 'name' and 'secret'"
                    )

        return self

    BASE_URL: ClassVar[str] = "/api/core/v2/namespaces/{namespace}/handlers"

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_with_namespace(*args, **kwargs)

    def urlify(self, purpose: str = None) -> str:
        """
        Return the URL for the handler resource(s).

        :return: The URL for the handler resource.
        """

        url = self.BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
