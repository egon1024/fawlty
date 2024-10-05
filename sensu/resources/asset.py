"""
A module to represent a Sensu asset resource
"""

from copy import deepcopy

from sensu.resources.base import ResourceBase, CallData

class Asset(ResourceBase):
    """
    A class to represent a Sensu asset resource
    """

    VALID_FIELDS = (
        "url",
        "sha512",
        "filters",
        "builds",
        "metadata",
        "headers"
    )

    def __init__(self, fields=None, client=None):
        """
        Initialize a new Sensu asset resource.

        :param data: The data for the asset.
        """

        fields = fields or {}
        self.fields = {
            "metadata": {},
            "headers": {},
            "filters": [],
        }
        self.client = client

        namespace = None
        if "namespace" in fields:
            namespace = fields["namespace"]

        elif "metadata" in fields and "namespace" in fields["metadata"]:
            namespace = fields["metadata"]["namespace"]

        if namespace is None:
            raise ValueError("Namespace is required for asset")

        self.fields["namespace"] = namespace

        self.base_url = f"/api/core/v2/namespaces/{self.fields["namespace"]}/assets"

        for field in self.VALID_FIELDS:
            self.fields[field] = fields.get(field, self.fields.get(field))

    def get_data(self) -> dict:
        """
        Return the URL for getting the asset resource(s).

        :return: The URL for the asset resource.
        """

        if not self.fields["metadata"] or not self.fields["metadata"].get("name"):
            return {"url": self.base_url, "fields": None}
        
        call_data = {"url": f"{self.base_url}/{self.fields["metadata"]["name"]}", "fields": deepcopy(self.fields)}

        # Some fields don't get sent to the API, they are only expected to be returned
        del call_data["fields"]["builds"]

        if "created_by" in call_data["fields"]["metadata"]:
            del call_data["fields"]["metadata"]["created_by"]

        return call_data

    def create_or_update(self):
        """
        Create or update asset resource.
        """

        if not self.client:
            raise SensuClientError("Could not create asset without a client")

        if not self.fields["metadata"] or not self.fields["metadata"].get("name"):
            raise ValueError("Asset metadata name is required to create a new asset")

        call_data = CallData(resource=self)

        return self.client.resource_put(call_data)

    def create(self):
        """
        Create new asset resource.
        """

        if not self.client:
            raise SensuClientError("Could not create asset without a client")

        # Check if it already exists
        call_data = CallData(resource=self)
        try:
            self.client.resource_get(call_data)
        except SensuResourceMissingError:
            pass
        else:
            raise SensuResourceExistsError("Asset already exists")

        return self.create_or_update()

    def delete(self):
        """
        Delete asset resource.
        """

        if not self.client:
            raise SensuClientError("Could not delete asset without a client")

        if not self.fields["metadata"] or not self.fields["metadata"].get("name"):
            raise ValueError("Asset metadata name is required to delete an asset")

        self.client.resource_delete(CallData(resource=self))

        return True

    def __str__(self):
        """
        Return the asset name.

        :return: The asset name.
        """

        return str(self.fields)