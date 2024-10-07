"""
A module to represent a Sensu clusterrole resource
"""

from copy import deepcopy
from pprint import pformat

from sensu.resources.base import ResourceBase, CallData
from sensu.exception import SensuClientError, SensuResourceMissingError, SensuResourceExistsError

class ClusterRole(ResourceBase):
    """
    A class to represent a Sensu clusterrole resource
    """

    VALID_FIELDS = (
        "metadata",
        "rules"
    )

    METADATA_FIELDS = (
        "name",
        "labels",
        "annotations",
        "created_by"
    )


    def __init__(self, fields=None, name=None, client=None):
        """
        Initialize a new Sensu role resource.

        # TODO - fix this
        :param data: The data for the role.
        """

        fields = fields or {}
        self.fields = {
            "metadata": {
                "name": None,
                "labels": {},
                "annotations": {},
                "created_by": None,
            },
            "rules": [],
        }
        self.client = client

        if "metadata" in fields:
            for field in self.METADATA_FIELDS:
                self.fields["metadata"][field] = fields["metadata"].get(field, self.fields["metadata"].get(field))

        if "rules" in fields and \
        len(fields["rules"]) > 0 and \
        isinstance(fields["rules"][0], dict):
            self.fields["rules"] = [ClusterRoleRule(**_) for _ in fields["rules"]]

        # Helper to simplify instantiation
        if name is not None:
            self.fields["metadata"]["name"] = name
        
        self.base_url = f"/api/core/v2/clusterroles"


    def get_data(self) -> dict:
        """
        Return the URL for getting the role resource(s).

        :return: The URL for the role resource.
        """

        if self.fields['metadata']['name'] is None:
            return {"url": self.base_url, "fields": None}

        field_data = deepcopy(self.fields)
        rules = [_.as_dict() for _ in self["rules"]]
        field_data["rules"] = rules

        return {"url": f"{self.base_url}/{self.fields['metadata']['name']}", "fields": field_data}


    def create(self):
        """
        Create role resource.
        """

        if not self.client:
            raise SensuClientError("Could not create role without a client")

        if not self.fields["metadata"]["name"]:
            raise ValueError("Role name is required")

        try:
            self.client.resource_get(CallData(resource=self))
        except SensuResourceMissingError:
            pass
        else:
            raise SensuResourceExistsError("Role already exists")

        return self.client.resource_post(CallData(resource=self))


    def create_or_update(self):
        """
        Create or update role resource.
        """

        if not self.client:
            raise SensuClientError("Could not create role without a client")

        if not self.fields["metadata"]["name"]:
            raise ValueError("Role name is required")

        return self.client.resource_put(CallData(resource=self))


    def delete(self):
        """
        Delete role resource.
        """

        if not self.client:
            raise SensuClientError("Could not delete role without a client")

        return self.client.resource_delete(CallData(resource=self))


class ClusterRoleRule(object):
    """
    A class to represent a Sensu clusterrole rule
    """

    VALID_NAMESPACE_RESOURCES = (
        "assets",
        "checks",
        "entities",
        "events",
        "filters",
        "handlers",
        "hooks",
        "mutators",
        "pipelines",
        "rolebindings",
        "roles",
        "silenced",
        "cluster",
        "clusterrolebindings",
        "clusterroles",
        "namespaces",
        "users",
        "authproviders",
        "license",
        "sumo-logic-metrics-handlers",
        "tcp-stream-handlers",
        "*",  # This is a special case for all resources
    )

    VALID_VERBS = (
        "get",
        "list",
        "create",
        "update",
        "delete",
        "*",  # This is a special case for all verbs
    )

    # TODO: Data validation

    def __init__(self, resources=None, resource_names=None, verbs=None):
        """
        Initialize a new Sensu role rule.

        :param resources: A list of resources for the role rule.
        :param resource_names: Any resource names for the role rule.
        :param verbs: The verbs for the role rule.
        """

        self.resources = resources or []
        self.resource_names = resource_names or []
        self.verbs = verbs or []

    def as_dict(self) -> dict:
        """
        Return the role rule as a dictionary.

        :return: The role rule as a dictionary.
        """

        return {
            "resources": deepcopy(self.resources),
            "resource_names": deepcopy(self.resource_names),
            "verbs": deepcopy(self.verbs),
        }