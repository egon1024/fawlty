"""
A module to represent a Sensu entity resource
"""

from copy import deepcopy

from sensu.resources.base import ResourceBase, CallData
from sensu.exception import SensuClientError, SensuResourceMissingError, SensuResourceExistsError

class Entity(ResourceBase):
    """
    A class to represent a Sensu entity resource
    """

    VALID_FIELDS = (
        "deregister",
        "deregistration",
        "entity_class",
        "last_seen",
        "redact",
        "subscriptions",
        "metadata",
        "system",
        "sensu_agent_version",
        "user",
    )

    METADATA_FIELDS = (
        "name",
        "namespace",
        "labels",
        "annotations",
        "created_by"
    )

    DEREGISTRATION_FIELDS = (
        "handler",
        "timeout",
    )

    def __init__(self, fields=None, name=None, namespace=None, client=None):
        """
        Initialize a new Sensu entity resource.

        # TODO - fix this
        :param data: The data for the entity.
        """

        fields = fields or {}
        self.fields = {
            "deregister": False,
            "deregistration": {
                "handler": None,
                "timeout": None,
            },
            "entity_class": "agent",
            "last_seen": None,
            "redact": [],
            "subscriptions": [],
            "metadata": {
                "name": None,
                "namespace": None,
                "labels": {},
                "annotations": {},
                "created_by": None,
            },
            "system": {},
            "sensu_agent_version": None,
            "user": None,
        }
        self.client = client

        if "deregister" in fields:
            self.fields["deregister"] = fields["deregister"]

        if "deregistration" in fields:
            for field in self.DEREGISTRATION_FIELDS:
                self.fields["deregistration"][field] = fields["deregistration"].get(field, self.fields["deregistration"].get(field))

        for field in ("entity_class", "last_seen", "redact", "subscriptions", "system", "sensu_agent_version", "user"):
            if field in fields:
                self.fields[field] = fields[field]

        if "metadata" in fields:
            for field in self.METADATA_FIELDS:
                self.fields["metadata"][field] = fields["metadata"].get(field, self.fields["metadata"].get(field))

        # Some helpers to simplify instantiation
        if name is not None:
            self.fields["metadata"]["name"] = name

        if namespace is not None:
            self.fields["metadata"]["namespace"] = namespace

        if not self.fields["metadata"]["namespace"]:
            raise ValueError("Namespace is required for entity")
        
        self.base_url = f"/api/core/v2/namespaces/{self.fields['metadata']['namespace']}/entities"

    def get_data(self) -> dict:
        """
        Return the URL and field data for the entity resource.
        """

        if self.fields['metadata']['name'] is None:
            return {"url": self.base_url, "fields": None}

        field_data = deepcopy(self.fields)

        # The only time we need get_data is for interacting with the API.  We only want the data relevant to the API to be available here

        keep_fields = ("entity_class", "sensu_agent_version", "subscriptions", "deregister", "deregistration", "metadata", "redact")

        for field in list(field_data.keys()):
            if field not in keep_fields:
                del field_data[field]

        return {"url": f"{self.base_url}/{self.fields['metadata']['name']}", "fields": field_data}

    def create_or_update(self):
        """
        Create or update the entity resource.
        """

        data = self.get_data()

        if data["fields"] is None:
            raise SensuClientError("Entity name is required")

        return self.client.resource_put(CallData(resource=self))
    
    def create(self):
        """
        Create the entity resource.
        """

        data = self.get_data()

        if data["fields"] is None:
            raise SensuClientError("Entity name is required")

        # Check if the entity already exists
        try:
            self.client.resource_get(CallData(resource=self))
            raise SensuResourceExistsError(f"Entity {self.fields['metadata']['name']} already exists")
        except SensuResourceMissingError:
            pass

        return self.client.resource_post(CallData(resource=self))

    def update(self):
        """
        Update the entity resource.
        """

        data = self.get_data()

        if data["fields"] is None:
            raise SensuClientError("Entity name is required")

        # Check if the entity exists and fail if not
        try:
            self.client.resource_get(CallData(resource=self))
        except SensuResourceMissingError:
            raise SensuResourceMissingError(f"Entity {self.fields['metadata']['name']} does not exist")

        return self.client.resource_put(CallData(resource=self))

    def delete(self):
        """
        Delete the entity resource.
        """

        data = self.get_data()

        if data["fields"] is None:
            raise SensuClientError("Entity name is required")

        # Check if the entity exists and fail if not
        try:
            self.client.resource_get(CallData(resource=self))
        except SensuResourceMissingError:
            raise SensuResourceMissingError(f"Entity {self.fields['metadata']['name']} does not exist")

        return self.client.resource_delete(CallData(resource=self))