"""
Implements a class to act as a Sensu client.
"""

# Built in imports
import json

# 3rd party imports
import requests

# Our imports
from sensu.token import Token, token_from_dict
from sensu.exception import SensuConnectionError, SensuNeedRefresh, SensuAuthError, SensuNeedLogin


class SensuClient(object):
    """
    A class to act as a Sensu client.
    """

    def __init__(self, server=None):
        """
        Initialize a new Sensu client.

        :param server: The name of the client.
        :param address: The address of the client.
        """
        self.server = server
        self.token = None
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})


    def call_filter(self):
        """
        Filter out making calls to the server, based on object state.
        """

        if not self.server:
            raise SensuConnectionError("No sensu server defined")

        if not self.token:
            raise SensuNeedLogin("No login token found")

        if self.token.is_expired():
            raise SensuNeedLogin("Expired login token")

        if self.token.need_refresh():
            raise SensuNeedRefresh("Token needs to be refreshed")

    def _make_call(self, method, path, data=None, use_filter=True):
        """
        Make a call to the Sensu server.

        :param method: The HTTP method to use.
        :param path: The path to the API endpoint.
        :param data: The data to send (default is None).
        :param use_filter: Whether to use the call_filter (default is True).
        :return: The response from the server.
        """

        if use_filter:
            try:
                self.call_filter()
            except SensuNeedRefresh:
                self.refresh_token()

        url = self.server.api_url + path
        if isinstance(data, dict):
            data = json.dumps(data)

        # TODO - Add ssl param(s)
        r = self.session.request(method, url, data=data)

        return r

    def login(self, username, password):
        """
        Login to the Sensu server.

        :param username: The username to login with.
        :param password: The password to login with.
        """

        # TODO - Add ssl param(s)
        # TODO - Add error handling
        self.session.headers.pop("Authorization", None)
        r = self.session.get(self.server.api_url + "/auth", auth=(username, password))

        if r.status_code != 200:
            raise SensuAuthError("Failed to login")

        self.token = token_from_dict(r.json())
        self.session.headers.update({"Authorization": f"Bearer {self.token.access_token}"})

        return True

    def refresh_token(self):
        """
        Refresh the token with the Sensu server."""

        # TODO - Add ssl param(s)
        data = {"refresh_token": self.token.refresh_token}
        r = self._make_call("POST", "/auth/token", data=data, use_filter=False)

        if r.status_code != 200:
            raise SensuAuthError(f"Failed to refresh token ({r.text})")

        self.token = token_from_dict(r.json())
        self.session.headers.update({"Authorization": f"Bearer {self.token.access_token}"})

        return True

    def resource_get(self, resource):
        """
        Get a resource or resources from the Sensu server.

        :param resource: The resource to get.
        :return: A list of objects representing the resource(s).
        """

        data = resource.get_data()

        r = self._make_call("GET", data["url"], data=data["data"])

        if r.status_code != 200:
            raise SensuError(f"Failed to get resource ({r.text})")

        klass = type(resource)
        resources = list(klass.instantiate_resources(r.json()))
        return resources