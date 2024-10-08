"""
A module to represent a Sensu clusterrolebinding resource
"""

from copy import deepcopy

from sensu.resources.base import ResourceBase, CallData
from sensu.exception import SensuClientError, SensuResourceMissingError, SensuResourceExistsError

class ClusterRoleBinding(ResourceBase):
    """
    A class to represent a Sensu clusterrolebinding resource
    """

    VALID_FIELDS = (
        "metadata",
        "role_ref",
        "subjects"
    )

    METADATA_FIELDS = (
        "name",
        "labels",
        "annotations",
        "created_by"
    )

    ROLEREFS_FIELDS = ("name", "kind")

    def __init__(self, fields=None, name=None, client=None):
        """
        Initialize a new Sensu clusterrolebinding resource.

        # TODO - document this
        """

        fields = fields or {}
        self.fields = {
            "metadata": {
                "name": None,
                "labels": {},
                "annotations": {},
                "created_by": None,
            },
            "role_ref": {},
            "subjects": []
        }
        self.client = client

        if "metadata" in fields:
            for field in self.METADATA_FIELDS:
                self.fields["metadata"][field] = fields["metadata"].get(field, self.fields["metadata"].get(field))

        if "role_ref" in fields:
            for field in self.ROLEREFS_FIELDS:
                self.fields["role_ref"][field] = fields["role_ref"].get(field)

        if "subjects" in fields and \
        len(fields["subjects"]) > 0 and \
        isinstance(fields["subjects"][0], dict):
            self.fields["subjects"] = [
                ClusterRoleBindingSubject(kind=_.get("kind", _.get("type")), name=_["name"])
                for _ in fields["subjects"]
            ]

        # Helper to simplify instantiation
        if name is not None:
            self.fields["metadata"]["name"] = name

        self.base_url = f"/api/core/v2/clusterrolebindings"


    def get_data(self) -> dict:
        """
        Return the URL and field data for getting/setting the clusterrolebinding resource(s).

        :return: The URL and field data for the clusterrolebinding resource.
        """

        if self.fields['metadata']['name'] is None:
            return {"url": self.base_url, "fields": None}

        field_data = deepcopy(self.fields)
        subjects = [_.as_dict() for _ in self["subjects"]]
        field_data["subjects"] = subjects

        # Play games with renaming because "type" is a reserved keyword in Python
        field_data["role_ref"]["type"] = field_data["role_ref"]["kind"]
        del field_data["role_ref"]["kind"]

        return {"url": f"{self.base_url}/{self.fields['metadata']['name']}", "fields": field_data}

    def create(self):
        """
        Create clusterrolebinding resource.
        """

        if not self.client:
            raise SensuClientError("Could not create clusterrolebinding without a client")

        if not self.fields["metadata"]["name"]:
            raise ValueError("ClusterRoleBinding name is required")

        try:
            self.client.resource_post(CallData(resource=self))
        except SensuResourceExistsError:
            pass
        else:
            raise SensuResourceExistsError("ClusterRoleBinding already exists")

        return self.client.resource_post(CallData(resource=self))

    def create_or_update(self):
        """
        Create or update clusterrolebinding resource.
        """

        if not self.client:
            raise SensuClientError("Could not create clusterrolebinding without a client")

        if not self.fields["metadata"]["name"]:
            raise ValueError("ClusterRoleBinding name is required")

        return self.client.resource_put(CallData(resource=self))

    def delete(self):
        """
        Delete clusterrolebinding resource.
        """

        if not self.client:
            raise SensuClientError("Could not delete clusterrolebinding without a client")

        if not self.fields["metadata"]["name"]:
            raise ValueError("ClusterRoleBinding name is required")

        self.client.resource_delete(CallData(resource=self))

        return True


class ClusterRoleBindingSubject(object):
    """
    A class to represent a Sensu clusterrolebinding subject

    Note: Because "type" is a reserved keyword in Python, it is referred to as "kind" in this class.
    """

    VALID_FIELDS = (
        "kind",
        "name",
    )

    VALID_KINDS = ("Group", "User")

    def __init__(self, kind=None, name=None):
        """
        Initialize a new Sensu clusterrolebinding subject.

        :param data: The data for the clusterrolebinding subject.
        """

        self.fields = {
            "kind": None,
            "name": None,
        }

        if kind is not None:
            if kind not in self.VALID_KINDS:
                raise ValueError(f"Invalid clusterrolebinding subject type: {kind}")
            self.fields["kind"] = kind

        if name is not None:
            self.fields["name"] = name

    def as_dict(self) -> dict:
        """
        Return the clusterrolebinding subject as a dictionary.

        :return: The clusterrolebinding subject as a dictionary.
        """

        return {
            "type": self.fields["kind"],
            "name": self.fields["name"],
        }