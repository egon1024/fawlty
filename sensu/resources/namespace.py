"""
A module to represent a Sensu namespace resource
"""

from sensu.resources.base import ResourceBase, CallData
from sensu.exception import SensuClientError

class Namespace(ResourceBase):
    """
    A class to represent a Sensu namespace resource
    """

    VALID_FIELDS = ("name",)

    def __init__(self, fields=None, client=None):
        """
        Initialize a new Sensu namespace resource.

        :param data: The data for the namespace.
        """

        fields = fields or {}

        self.base_url = "/api/core/v2/namespaces"
        self.fields = {}
        self.client = client

        self.fields['name'] = fields.get("name")

    def get_data(self) -> dict:
        """
        Return the URL for getting the namespace resource(s).

        :return: The URL for the namespace resource.
        """

        if self.fields['name'] is None:
            return {"url": self.base_url, "fields": None}
        else:
            return {"url": f"{self.base_url}/{self.fields['name']}", "fields": {"name": self.fields['name']}}

    def create(self):
        """
        Create namespace resource.
        """

        if not self.client:
            raise SensuClientError("Could not create namespace without a client")

        return self.client.resource_put(CallData(resource=self))

    create_or_update = create

    def delete(self):
        """
        Delete namespace resource.
        """

        if not self.client:
            raise SensuClientError("Could not delete namespace without a client")

        self.client.resource_delete(CallData(resource=self))

        return True

    def __str__(self):
        """
        Return the namespace name.

        :return: The namespace name.
        """

        return str(self.fields)