"""
A module to represent the connection information to a Sensu server API
"""

class Server(object):
    """
    A class to represent the connection information to a Sensu server API
    """

    def __init__(self, host, port, use_ssl=False, ignore_cert=False):
        """
        Initialize a new Sensu server connection.

        :param host: The hostname or IP address of the server.
        :param port: The port number of the server.
        :param use_ssl: Whether to use SSL for the connection (default is False).
        :param ignore_cert: Whether to ignore SSL certificate validation (default is False).
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.ignore_cert = ignore_cert
        self.api_url = f"http{'s' if use_ssl else ''}://{host}:{port}"


    def __str__(self):
        """
        Return the API URL.

        :return: The API URL.
        """
        return self.api_url


    def __repr__(self):
        """
        Return the API URL.

        :return: The API URL.
        """
        return self.api_url