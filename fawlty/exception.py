class SensuError(Exception):
    pass


class SensuConnectionError(SensuError):
    pass


class SensuClientError(SensuError):
    """
    Indicates that the client is not properly configured, or missing.
    """
    pass


class SensuAuthError(SensuError):
    pass


class SensuNeedRefresh(SensuError):
    """
    Indicates that a login token needs to be refreshed
    """
    pass


class SensuNeedLogin(SensuError):
    """
    Indicates there is no active/valid login session
    """
    pass


class SensuIncompleteError(SensuError):
    """
    Indicates that a given resource was incomplete when trying to be used
    """
    pass

class SensuResourceError(SensuError):
    """
    A generic error for resource operations
    """

class SensuResourceMissingError(SensuResourceError):
    """
    Indicates that a resource is missing
    """
    pass

class SensuResourceExistsError(SensuResourceError):
    """
    Indicates that a resource unexpectedly exists
    """
    pass