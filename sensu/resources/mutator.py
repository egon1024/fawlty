"""
A module for Sensu mutator resources.
"""

from sensu.resources.base import ResourceBase, CallData
from sensu.exception import SensuClientError, SensuResourceMissingError, SensuResourceExistsError

class Mutator(ResourceBase):
    """
    A class to represent a Sensu mutator resource.
    """

    VALID_FIELDS = (
        "command",
        "timeout",
        "env_vars",
        "runtime_assets",
        "secrets",
        "type",
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
        Initialize a new Sensu mutator resource.

        :param data: The data for the mutator.
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
            "command": None,
            "timeout": None,
            "env_vars": [],
            "runtime_assets": [],
            "secrets": [],
            "type": "pipe",
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
            raise SensuClientError("Mutator must have a namespace")

        self.base_url = f"/api/core/v2/namespaces/{self.fields['metadata']['namespace']}/mutators"

    def get_data(self):
        """
        Get the data for the Sensu mutator(s).
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
        Create or update the Sensu mutator.
        """

        data = self.get_data()

        if data["fields"]["metadata"]["name"] is None:
            raise SensuResourceMissingError("No name provided for mutator")

        return self.client.resource_put(CallData(resource=self, data=data))