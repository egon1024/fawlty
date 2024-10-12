"""
A module to represent a Sensu filter resource
"""

from copy import deepcopy

from sensu.resources.base import ResourceBase, CallData

from sensu.exception import SensuClientError, SensuResourceMissingError, SensuResourceExistsError

class Filter(ResourceBase):
    """
    A class to represent a Sensu filter resource
    """

    VALID_FIELDS = (
        "action",
        "expressions",
        "runtime_assets",
        "metadata",
    )

    METADATA_FIELDS = (
        "name",
        "namespace",
        "labels",
        "annotations",
        "created_by"
    )

    def __init__(self, fields=None, name=None, namespace=None, client=None):
        """
        Initialize a new Sensu filter resource.

        :param data: The data for the filter.
        """

        fields = fields or {}
        self.fields = {
            "metadata": {
                "name": name,
                "namespace": namespace,
                "labels": {},
                "annotations": {},
                "created_by": None
            },
            "action": None,
            "expressions": [],
            "runtime_assets": [],
        }
        self.client = client

        for field in self.VALID_FIELDS:
            if field in fields:
                self.fields[field] = fields[field]

        # Just to help simplify the call to instantiation
        if name:
            self.fields["metadata"]["name"] = name

        if namespace:
            self.fields["metadata"]["namespace"] = namespace

        # Must have a namespace
        if not self.fields["metadata"]["namespace"]:
            raise SensuClientError("Filter must have a namespace")

        self.base_url = f"/api/core/v2/namespaces/{self.fields['metadata']['namespace']}/filters"

    def get_data(self):
        """
        Get the data for the Sensu filter(s).

        :return: The data for the Sensu filter(s).
        """

        if self.fields["metadata"]["name"] is None:
            return {"url": self.base_url, "fields": None}

        field_data = {
            key: deepcopy(self.fields[key])
            for key in self.VALID_FIELDS
            if key in self.fields
        }

        return {
            "url": f"{self.base_url}/{self.fields['metadata']['name']}",
            "fields": field_data
        }

    def create_or_update(self):
        """
        Create or update the Sensu filter.

        :return: The result of the create or update operation.
        """

        data = self.get_data()
        if data["fields"] is None:
            raise SensuResourceMissingError("Filter name is required")

        return self.client.resource_put(CallData(resource=self))

    def create(self):
        """
        Create the Sensu filter.

        :return: The result of the create operation.
        """

        data = self.get_data()
        if data["fields"] is None:
            raise SensuResourceMissingError("Filter name is required")

        # Check if the filter already exists
        if self.client.resource_get(CallData(resource=self)):
            raise SensuResourceExistsError("Filter already exists")

        return self.client.resource_post(CallData(resource=self))

    def update(self):
        """
        Update the Sensu filter.

        :return: The result of the update operation.
        """

        data = self.get_data()
        if data["fields"] is None:
            raise SensuResourceMissingError("Filter name is required")

        # Check if the filter exists
        if not self.client.resource_get(CallData(resource=self)):
            raise SensuResourceMissingError("Filter does not exist")

        return self.client.resource_put(CallData(resource=self))

    def delete(self):
        """
        Delete the Sensu filter.

        :return: The result of the delete operation.
        """

        data = self.get_data()
        if data["fields"] is None:
            raise SensuResourceMissingError("Filter name is required")

        return self.client.resource_delete(CallData(resource=self))