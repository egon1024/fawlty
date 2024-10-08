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
        return {"url": f"{self.base_url}/{self.fields['metadata']['name']}", "fields": field_data}

    