"""
A module containing a base class to use for Sensu resource objects
"""

# Built in imports
from typing import Optional, Dict

# 3rd party imports
from pydantic import BaseModel, ConfigDict

# Our imports
from fawlty.exceptions import SensuClientError
from fawlty.sensu_client import SensuClient


class ResourceBase(BaseModel):
    """
    A Base class to use for Sensu resource objects
    """

    # Needed to set arbitrary items like BASE_URL and the get_url method
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, *args, **kwargs):
        """
        Instance initialization
        """

        super().__init__(*args, **kwargs)

        self._sensu_client = None

    def set_client(self, client: SensuClient):
        """
        Sets the sensu client for the object
        """
        self._sensu_client = client

    @classmethod
    def get_url_with_namespace(cls, namespace: str, name: str = None) -> str:
        """
        Get the URL to retrieve a resource or resources, with a namespace.
        """

        if not hasattr(cls, "BASE_URL"):
            raise NotImplementedError(f"{cls.__name__} must define a BASE_URL.")

        url = cls.BASE_URL.format(namespace=namespace)
        if name is not None:
            url += f"/{name}"

        return url

    @classmethod
    def get_url_without_namespace(cls, name: str = None) -> str:
        """
        Get the URL to retrieve a resource or resources, without a namespace.
        """

        url = cls.BASE_URL
        if name is not None:
            url += f"/{name}"

        return url

    @classmethod
    def get(cls, client: SensuClient, namespace: str = None, name: str = None) -> list[object]:
        """
        Get a resource or resources from the Sensu server.
        :return: A list of objects representing the resource(s).
        """

        if namespace is None:
            get_url = cls.get_url(name=name)

        else:
            get_url = cls.get_url(namespace=namespace, name=name)

        resources = client.resource_get(cls=cls, get_url=get_url)

        return resources

    def create(self) -> bool:
        """
        Create resource.
        """

        if not self._sensu_client:
            raise SensuClientError(
                f"Could not create '{self.__class__.__name__}' object without a client"
            )

        return self._sensu_client.resource_post(obj=self)

    def update(self) -> bool:
        """
        Update resource.
        """

        if not self._sensu_client:
            raise SensuClientError(
                f"Could not update '{self.__class__.__name__}' object without a client"
            )

        return self._sensu_client.resource_put(obj=self)

    def delete(self) -> bool:
        """
        Delete namespace resource.
        """

        if not self._sensu_client:
            raise SensuClientError(
                f"Could not delete '{self.__class__.__name__}' object without a client"
            )

        return self._sensu_client.resource_delete(obj=self)


class MetadataWithoutNamespace(BaseModel):
    """
    A class to represent the data structure of a metadata
    """
    name: str
    created_by: Optional[str] = None
    labels: Optional[Dict[str, str]] = {}
    annotations: Optional[Dict[str, str]] = {}


class MetadataWithNamespace(BaseModel):
    """
    A class to represent the data structure of a metadata
    """
    name: str
    namespace: str
    created_by: Optional[str] = None
    labels: Optional[Dict[str, str]] = {}
    annotations: Optional[Dict[str, str]] = {}
