class SensuError(Exception):
    pass


class SensuConnectionError(SensuError):
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