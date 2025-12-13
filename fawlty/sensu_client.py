"""
Implements a class to act as a Sensu client.
"""

# Built in imports
import json
import os
import urllib3

# 3rd party imports
import requests
from pydantic import ValidationError

# Our imports
from fawlty.sensu_token import SensuToken
from fawlty.exceptions import (
    SensuConnectionError, SensuNeedRefresh,
    SensuAuthError, SensuNeedLogin,
    SensuResourceError, SensuError
)


def get_system_ca_bundle():
    """
    Get the path to the system CA certificate bundle.
    Returns None if not found, which tells requests to use its default certifi bundle.
    """
    # Common locations for system CA bundles
    ca_bundle_paths = [
        # Debian/Ubuntu/Gentoo etc.
        '/etc/ssl/certs/ca-certificates.crt',
        # RedHat/Fedora/CentOS
        '/etc/pki/tls/certs/ca-bundle.crt',
        # OpenSUSE
        '/etc/ssl/ca-bundle.pem',
        # OpenBSD
        '/etc/ssl/cert.pem',
        # macOS (Homebrew)
        '/usr/local/etc/openssl/cert.pem',
        '/usr/local/etc/openssl@1.1/cert.pem',
        # macOS (system)
        '/etc/ssl/cert.pem',
    ]

    # Check environment variables first
    for env_var in ['REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE']:
        if env_var in os.environ and os.path.isfile(os.environ[env_var]):
            return os.environ[env_var]

    # Check common paths
    for path in ca_bundle_paths:
        if os.path.isfile(path):
            return path

    # Fall back to None, which means use certifi's default bundle
    return None


def debug_r(r: object):
    """
    Debug a requests response
    """
    print(f"Status code: {r.status_code}")
    print(f"Text: {r.text}")


class SensuClient:
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

        # Configure SSL verification
        if server and server.ignore_cert:
            # Disable SSL verification completely
            self.session.verify = False
            # Disable SSL warnings when ignoring certificates
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        elif server and server.use_ssl:
            # Use system CA bundle for SSL verification
            ca_bundle = get_system_ca_bundle()
            if ca_bundle:
                self.session.verify = ca_bundle
            # else: leave as default (True), which uses certifi bundle

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
        Wraps the call to the requests library to help manage session timeouts and token refreshes.

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

        r = self.session.request(method, url, data=fields)

        return r

    def login(self, username, password):
        """
        Login to the Sensu server.

        :param username: The username to login with.
        :param password: The password to login with.
        """

        # TODO - Add error handling
        self.session.headers.pop("Authorization", None)
        r = self.session.get(self.server.api_url + "/auth", auth=(username, password))

        if r.status_code < 200 or r.status_code > 299:
            raise SensuAuthError("Failed to login")

        self.token = SensuToken(**r.json())
        self.session.headers.update({"Authorization": f"Bearer {self.token.access_token}"})

        return True

    def refresh_token(self):
        """
        Refresh the token with the Sensu server."""

        data = {"refresh_token": self.token.refresh_token}
        r = self._make_call("POST", "/auth/token", fields=data, use_filter=False)

        if r.status_code < 200 or r.status_code > 299:
            raise SensuAuthError(f"Failed to refresh token ({r.text})")

        self.token = SensuToken(**r.json())
        self.session.headers.update({"Authorization": f"Bearer {self.token.access_token}"})

        return True

    def resource_get(self, cls, get_url) -> list[object]:
        """
        Get a resource or resources from the Sensu server.
        :return: A list of objects representing the resource(s).
        """

        r = self._make_call("GET", get_url)

        if r.status_code < 200 or r.status_code > 299:
            raise SensuError(f"Failed to get resource(s) ({r.text})")

        resources = []
        for _ in r.json():
            obj = cls(**_)
            obj.set_client(self)
            resources.append(obj)

        return resources

    def resource_post(self, obj, url=None) -> bool:
        """
        Post a resource to the Sensu server.
        :return: The object representing the resource.
        """

        try:
            obj.model_validate(obj)
        except ValidationError as err:
            raise SensuResourceError(str(err)) from err

        if url is None:
            url = obj.urlify(purpose="create")

        self._make_call(method="POST", path=url, fields=obj.model_dump())

        # TODO: Handle a failure

        return True

    def resource_put(self, obj, url=None) -> bool:
        """
        Put a resource to the Sensu server.
        :return: The object representing the resource.
        """

        try:
            obj.model_validate(obj)
        except ValidationError as err:
            raise SensuResourceError(str(err)) from err

        if url is None:
            url = obj.urlify()

        self._make_call(method="PUT", path=url, fields=obj.model_dump())

        # TODO: Handle a failure

        return True

    def resource_delete(self, obj, url=None) -> bool:
        """
        Delete a resource from the Sensu server.

        :param resource: The resource to delete.
        :return: True if the resource was deleted
        """

        if url is None:
            url = obj.urlify()

        self._make_call(method="DELETE", path=url)

        return True
