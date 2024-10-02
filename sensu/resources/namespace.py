"""
A module to represent a Sensu namespace resource
"""

from sensu.resources.base import Base

class Namespace(Base):
    """
    A class to represent a Sensu namespace resource
    """

#    def instantiate_resources(data):
#        """
#        Create list of objects based of provided data
#        """
#        for item in data:
#            yield Namespace(item)

    def __init__(self, data=None):
        """
        Initialize a new Sensu namespace resource.

        :param data: The data for the namespace.
        """

        data = data or {}

        self.base_url = "/api/core/v2/namespaces"
        self.data = {}

        self.data['name'] = data.get("name")

    def get_data(self) -> dict:
        """
        Return the URL for getting the namespace resource(s).

        :return: The URL for the namespace resource.
        """

        if self.data['name'] is None:
            return {"url": self.base_url, "data": None}
        else:
            return {"url": f"{self.base_url}/{self.data['name']}", "data": None}

    def __str__(self):
        """
        Return the namespace name.

        :return: The namespace name.
        """

        return str(self.data)