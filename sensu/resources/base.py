"""
A module containing a base class to use for Sensu resource objects
"""

class Base(object):
    """
    A Base class to use for Sensu resource objects
    """

    @classmethod
    def instantiate_resources(cls, data):
        """
        Create list of objects based on provided data
        """
        for item in data:
            yield cls(item)