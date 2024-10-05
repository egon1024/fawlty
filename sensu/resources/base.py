"""
A module containing a base class to use for Sensu resource objects
"""

from typing import Any


class ResourceBase(object):
    """
    A Base class to use for Sensu resource objects
    """

    @classmethod
    def instantiate_resources(cls, data, client=None):
        """
        Create list of objects based on provided data
        """
        for item in data:
            yield cls(item, client=client)


    def __getitem__(self, name):
        """
        Get an attribute from "data"
        """

        return self.fields.get(name)


    def __setitem__(self, name, value):
        """
        Set an attribute in "data"
        """

        if name not in self.VALID_FIELDS:
            raise IndexError(f"'{type(self).__name__}' object has no element '{name}'")

        self.fields[name] = value


class CallData(object):
    """
    A class to represent the data for an API call.  It will derive the needed data from a combination of a ResourceBase object, a url, and fields, as necessary.
    """

    def __init__(self, resource=None, url=None, fields=None):
        """
        Initialize a new CallData object.
        """

        self.resource = resource

        if url is None and resource is None:
            raise ValueError("Either 'resource' or 'url' must be provided")

        self.url = url or resource.get_data()["url"]

        if fields is not None:
            self.fields = fields
        elif resource is not None:
            self.fields = resource.get_data()["fields"]

    def __getitem__(self, name):
        """
        Get an attribute from "data"
        """

        if name == "url":
            return self.url
        elif name == "fields":
            return self.fields
        elif name == "resource":
            return self.resource

    def __setitem__(self, name, value):
        """
        Set an attribute in "data"
        """

        if name == "url":
            self.url = value
        elif name == "fields":
            self.fields = value
        elif name == "resource":
            self.resource = value