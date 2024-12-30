"""
This modules provides an exception hierarchy for exceptions specific to this library.
"""


class SensuError(Exception):
    """
    Base exception for errors from this library.
    """


class SensuConnectionError(SensuError):
    """
    An exception that indicates there was a problem with a connection to the Sensu server
    """


class SensuClientError(SensuError):
    """
    Indicates that the client is not properly configured, or missing.
    """


class SensuAuthError(SensuError):
    """
    Indicates that there was a problem with authentication with the Sensu server
    """


class SensuNeedRefresh(SensuError):
    """
    Indicates that a login token needs to be refreshed
    """


class SensuNeedLogin(SensuError):
    """
    Indicates there is no active/valid login session
    """


class SensuIncompleteError(SensuError):
    """
    Indicates that a given resource was incomplete when trying to be used
    """


class SensuResourceError(SensuError):
    """
    A generic error for resource operations
    """


class SensuResourceMissingError(SensuResourceError):
    """
    Indicates that a resource is missing
    """


class SensuResourceExistsError(SensuResourceError):
    """
    Indicates that a resource unexpectedly exists
    """
