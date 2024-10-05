"""
A module to represent a Sensu user resource
"""

from sensu.resources.base import ResourceBase, CallData
from sensu.exception import SensuClientError, SensuResourceMissingError, SensuResourceExistsError

class User(ResourceBase):
    """
    A class to represent a Sensu user resource

    Methods:
        create: Create the user resource.
        create_or_update: Create or update the user resource.
        update: Update the user resource.
        disable: Disable the user.
        reinstate: Reinstate the user.
        reset_password: Change the user's password without knowing the current one.
    """

    VALID_FIELDS = (
        "username",
        "groups",
        "password",
        "disabled",
    )

    def __init__(self, fields=None, client=None):
        """
        Initialize a new Sensu user resource.

        :param fields: The fields for the user.
        """

        fields = fields or {}
        self.fields = {}
        self.client = client

        self.base_url = "/api/core/v2/users"

        for field in self.VALID_FIELDS:
            if field not in fields:
                self.fields[field] = None
            else:
                self.fields[field] = fields[field]

    def get_data(self) -> dict:
        """
        Return the URL for getting the user resource(s).

        :return: The URL for the user resource.
        """

        if self.fields['username'] is None:
            return {"url": self.base_url, "fields": None}
        else:
            return {"url": f"{self.base_url}/{self.fields['username']}", "fields": self.fields}

    def create(self):
        """
        Create the user resource.

        Will fail if the user already exists.
        """

        if not self.client:
            raise SensuClientError("Could not create user without a client")

        call_data = CallData(resource=self)

        try:
            self.client.resource_get(call_data)
        except SensuResourceMissingError:
            pass
        else:
            raise SensuResourceExistsError("User already exists")

        self.create_or_update()

    def update(self):
        """
        Update the user resource.

        Will fail if the user does not exist.
        """

        if not self.client:
            raise SensuClientError("Could not update user without a client")

        call_data = CallData(resource=self)
        try:
            self.client.resource_get(call_data)
        except SensuResourceMissingError:
            raise SensuResourceMissingError("User does not exist")

        if self['password'] is not None:
            return self.create_or_update()

        else:
            return self.update_no_password()

    def create_or_update(self):
        """
        Create or update the user resource.
        """

        if not self.client:
            raise SensuClientError("Could not create user without a client")

        # If there's no password, this can only be an updatte
        if self['password'] is None:
            return self.update_no_password()

        else:
            return self.client.resource_put(CallData(resource=self))

    def update_no_password(self):
        """
        Update the user resource, but we don't have access to the password.
        """

        # Start with the user's status
        if not self['disabled']:
            self.reinstate()
        else:
            self.disable()

        # Find out what groups they are in so we can make it match
        live_user = list(self.client.resource_get(CallData(resource=self)))[0]
        current_groups = live_user['groups']

        if self['groups'] is not None:
            for group in self["groups"]:
                if group not in current_groups:
                    call_data = CallData(resource=self)
                    call_data.url = f"{self.base_url}/{self['username']}/groups/{group}"
                    self.client.resource_put(call_data)

        if current_groups is not None:
            for group in current_groups:
                if group not in self["groups"]:
                    call_data = CallData(resource=self)
                    call_data.url = f"{self.base_url}/{self['username']}/groups/{group}"
                    self.client.resource_delete(call_data)

        return list(self.client.resource_get(CallData(resource=self)))[0]

    def disable(self):
        """
        Disable the user.
        """

        if not self.client:
            raise SensuClientError("Could not create user without a client")

        self.client.resource_delete(self)
        self["disabled"] = True

        return list(self.instantiate_resources(data=[self.fields], client=self.client))[0]
    
    def reinstate(self):
        """
        Reinstate the user.
        """

        if not self.client:
            raise SensuClientError("Could not create user without a client")

        call_data = CallData(resource=self)

        try:
            live = list(self.client.resource_get(call_data))[0]
        except SensuResourceMissingError:
            raise SensuResourceMissingError("User does not exist")

        # If they're already enabled, no sense in making an API call
        if not live['disabled']:
            return live

        call_data.url = f"{self.base_url}/{self.fields['username']}/reinstate"

        return self.client.resource_put(call_data)

    def reset_password(self):
        """
        Reset the user's password.

        Does not require knowledge of the existing password to use.
        """

        if not self.client:
            raise SensuClientError("Could not create user without a client")

        data = {
            "url": f"{self.base_url}/{self.fields['username']}/reset_password",
            "fields": {
                "username": self["username"],
                "password": self["password"],
            }
        }

        return self.client.resource_put(self, data)

    def __str__(self):
        """
        Return the username.

        :return: The username.
        """

        return str(self.fields)