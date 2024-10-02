"""
A module to represent a Sensu asset resource
"""

from sensu.resources.base import Base

class Asset(Base):
    """
    A class to represent a Sensu asset resource
    """

    FIELDS = (
        "url",
        "sha512",
        "filters",
        "builds",
        "metadata",
        "headers"
    )

    def __init__(self, data=None):
        """
        Initialize a new Sensu asset resource.

        :param data: The data for the asset.
        """

        data = data or {}
        self.data = {}

        namepsace = None
        if 'namespace' in data:
            namespace = data['namespace']
        elif 'metadata' in data and 'namespace' in data['metadata']:
            namespace = data['metadata']['namespace']

        if namespace is None:
            raise ValueError("Namespace is required for asset")

        self.data['namespace'] = namespace

        self.base_url = f"/api/core/v2/namespaces/{self.data['namespace']}/assets"

        for field in self.FIELDS:
            self.data[field] = data.get(field)

    def get_data(self) -> dict:
        """
        Return the URL for getting the asset resource(s).

        :return: The URL for the asset resource.
        """

        if not self.data['metadata'] or not self.data['metadata'].get("name"):
            return {"url": self.base_url, "data": None}
        
        else:
            return {"url": f"{self.base_url}/{self.data['metadata']['name']}", "data": None}

    def __str__(self):
        """
        Return the asset name.

        :return: The asset name.
        """

        return str(self.data)