"""
Implements a class to act as a Sensu client.
"""

# Built in imports
import json
from pprint import pformat

# 3rd party imports
import requests

# Our imports
from sensu.token import Token, token_from_dict
from sensu.exception import SensuConnectionError, SensuNeedRefresh, SensuAuthError, SensuNeedLogin, SensuResourceMissingError, SensuError
from sensu.resources.base import ResourceBase, CallData


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

    def _make_call(self, method, path, fields=None, use_filter=True):
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
        if isinstance(fields, dict):
            fields = json.dumps(fields)

        # TODO - Add ssl param(s)
        r = self.session.request(method, url, data=fields)

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

        if r.status_code < 200 or r.status_code > 299:
            raise SensuAuthError("Failed to login")

        self.token = token_from_dict(r.json())
        self.session.headers.update({"Authorization": f"Bearer {self.token.access_token}"})

        return True

    def refresh_token(self):
        """
        Refresh the token with the Sensu server."""

        # TODO - Add ssl param(s)
        data = {"refresh_token": self.token.refresh_token}
        r = self._make_call("POST", "/auth/token", fields=data, use_filter=False)

        if r.status_code < 200 or r.status_code > 299:
            raise SensuAuthError(f"Failed to refresh token ({r.text})")

        self.token = token_from_dict(r.json())
        self.session.headers.update({"Authorization": f"Bearer {self.token.access_token}"})

        return True

    def resource_get(self, call_data):
        """
        Get a resource or resources from the Sensu server.

        :param call_data: The CallData object to use for the call.
        :return: A list of objects representing the resource(s).
        """

        if isinstance(call_data, ResourceBase):
            call_data = CallData(resource=call_data)

        if call_data.resource is None:
            raise(ValueError("CallData object must have a resource defined."))

        r = self._make_call("GET", call_data["url"], fields=call_data["fields"])

        if r.status_code < 200 or r.status_code > 299:
            raise SensuResourceMissingError(f"Failed to get resource {call_data["url"]} ({r.status_code}: {r.text})")

        klass = type(call_data.resource)
        retrieved_data = r.json()
        if isinstance(retrieved_data, dict):
            resources = list(klass.instantiate_resources(data=[retrieved_data], client=self))
        else:
            resources = list(klass.instantiate_resources(data=retrieved_data, client=self))
        return resources

    def resource_post(self, call_data):
        """
        Post a resource to the Sensu server.

        :param resource: The resource to post, or dictionary containing post data.
        :return: The object representing the resource.
        """

        if isinstance(call_data, ResourceBase):
            call_data = CallData(resource=call_data)

        r = self._make_call("POST", call_data["url"], fields=call_data["fields"])

        if r.status_code < 200 or r.status_code > 299:
            raise SensuError(f"Failed to post resource {call_data["url"]} ({r.status_code}: {r.text})")

        # Posts don't return resource data, so we'll just return a True.  The caller will have to perform a get if they want to do that.
        return True

    def resource_put(self, call_data):
        """
        Put a resource to the Sensu server.

        :param call_data: The CallData object to put
        :return: The object representing the resource.
        """

        if isinstance(call_data, ResourceBase):
            call_data = CallData(resource=call_data)

        r = self._make_call("PUT", call_data["url"], fields=call_data["fields"])

        if r.status_code < 200 or r.status_code > 299:
            raise SensuError(f"Failed to put resource {call_data["url"]} ({r.status_code}: {r.text})")

        klass = type(call_data.resource)
        new_obj = klass(call_data["fields"], client=self)
        return new_obj 

    def resource_delete(self, call_data):
        """
        Delete a resource from the Sensu server.

        :param resource: The resource to delete.
        :return: True if the resource was deleted
        """

        if isinstance(call_data, ResourceBase):
            call_data = CallData(resource=call_data)

        r = self._make_call("DELETE", call_data["url"])

        if r.status_code < 200 or r.status_code > 299:
            raise SensuError(f"Failed to delete resource {call_data["url"]} ({r.status_code}: {r.text})")

        return True