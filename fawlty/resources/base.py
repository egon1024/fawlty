"""
A module containing a base class to use for Sensu resource objects
"""

# Built in imports
from typing import Optional, Dict

# Our imports
from sensu.exception import SensuClientError
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel

###
# TODO:
#
# Track whether the object has been changed since last write to the sensu
# server (dirty = T/F perhaps?).  Write ops would be noops if dirty == F. 
# "Force" flag to override
#
###

class ResourceBase(BaseModel):
    """
    A Base class to use for Sensu resource objects
    """

    def set_client(self, client: SensuClient):
        """
        Sets the sensu client for the object
        """
        self._sensu_client = client


    def create(self) -> bool:
        """
        Create resource.
        """

        if not self._sensu_client:
            raise SensuClientError(f"Could not create '{self.__class__.__name__}' object without a client")

        return self._sensu_client.resource_post(obj=self)


    def update(self) -> bool:
        """
        Update resource.
        """

        if not self._sensu_client:
            raise SensuClientError(f"Could not update '{self.__class__.__name__}' object without a client")

        return self._sensu_client.resource_put(obj=self)


    def delete(self) -> bool:
        """
        Delete namespace resource.
        """

        if not self._sensu_client:
            raise SensuClientError(f"Could not delete '{self.__class__.__name__}' object without a client")

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