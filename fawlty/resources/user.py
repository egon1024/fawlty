"""
A module to represent a Sensu user resource
"""
# Built in imports
from typing import Optional, List

# Our imports
from fawlty.resources.base import ResourceBase
from fawlty.sensu_client import SensuClient

# 3rd party imports
from pydantic import validator
import bcrypt

def hash_password(passwd: str) -> str:
    """
    Takes a password and switches it to a hashed form for use in Sensu
    """

    bytes = passwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    hashed_str = hash.decode('utf-8')

    return hashed_str


class UserPasswordReset(ResourceBase):
    """
    This is a special class being used to represent the structure and URL specifically
    for the purpose of performing a password reset.
    """
    username: str
    password_hash: str
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/users"
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_without_namespace(*args, **kwargs)

    def urlify(self, purpose: str=None) -> str:
        """
        Provide the url for reseting the user's password
        """

        # We ignore the purpose field - it's only present to preserve the
        # method signature

        return cls.BASE_URL + f"/{self.username}/reset_password"


class UserChangePassword(ResourceBase):
    """
    This is a special class being used to represent the structure and URL specifically
    for the purpose of a user to update their own password
    """
    username: str
    password: str
    password_hash: str
    _sensu_client: Optional[SensuClient] = None

    BASE_URL: ClassVar[str] = "/api/core/v2/users"
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_without_namespace(*args, **kwargs)

    def urlify(self, purpose: str=None) -> str:
        """
        Provide the url for reseting the user's password
        """

        # We ignore the purpose field - it's only present to preserve the
        # method signature

        return cls.BASE_URL + f"/{self.username}/password"



class User(ResourceBase):
    """
    A class to represent a Sensu user resource
    """

    username: str
    groups: List[str]
    disabled: bool
    password: Optional[str] = None
    _sensu_client: Optional[SensuClient] = None

    @validator("password")
    def validate_password(cls, value):
        if value is not None and len(value) < 8:
            raise ValueError ("Password must be at least 8 characters long")
        return value

    BASE_URL: ClassVar[str] = "/api/core/v2/users"
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return cls.get_url_without_namespace(*args, **kwargs)

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the user resource.

        :return: The URL for the user resource.
        """

        url = cls.BASE_URL

        if purpose != "create":
            url += f"/{self.username}"

        return url

    def disable(self):
        """
        Marks the user as disabled
        """

        self.delete()

    def reset_password(self, new_password: str):
        """
        Cause the user's password to be reset
        """

        if not self._sensu_client:
            raise SensuClientError(f"Could not create '{self.__class__.__name__}' object without a client")

        password_hash = hash_password(new_password)
        reset_obj = UserPasswordReset(
            username=self.username, password_hash=password_hash
        )
        reset_obj.set_client(self._sensu_client)

        return reset_obj.update()

    def change_password(self, old_password: str, new_password: str):
        """
        Update the user's own password.

        Requires the current password to be provided, as well as the new one.
        """

        if not self._sensu_client:
            raise SensuClientError(f"Could not create '{self.__class__.__name__}' object without a client")

        password_hash = hash_password(new_password)
        reset_obj = UserChangePassword(
            username=self.username,
            password=old_password,
            password_hash=password_hash
        )
        reset_obj.set_client(self._sensu_client)

        return reset_obj.update()

    def reinstate(self):
        """
        Reinstates the user
        """

        if not self._sensu_client:
            raise SensuClientError(f"Could not create '{self.__class__.__name__}' object without a client")

        result = self._sensu_client.resource_put(
            obj=self,
            url=cls.BASE_URL + f"/{self.username}/reinstate"
        )
        if result:
            self.disabled = False
