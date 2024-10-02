"""
A class to encapsulte a Sensu API token.
"""

import time

def token_from_dict(token_data):
    token = Token(
        access_token=token_data['access_token'],
        expire_ts=token_data['expires_at'], 
        refresh_token=token_data['refresh_token'],
    )

    return token


class Token(object):
    """
    A class to encapsulte a Sensu API token.
    """

    def __init__(self, access_token, expire_ts, refresh_token):
        """
        Initialize a new Sensu API token.

        :param access_token: The token used to authenticate each request
        :param expire_ts: The timestamp when the access_token expires
        :param refresh_token: The token used to refresh the access_token
        """
        self.access_token = access_token
        self.expire_ts = expire_ts
        self.refresh_token = refresh_token

        # When the token expiration is within this many seconds, the object
        # will indicate that it's time to refresh
        self.refresh_threshold = 60


    def __str__(self):
        """
        Return the token string.

        :return: The token string.
        """
        return self.access_token


    def __repr__(self):
        """
        Return the token string.

        :return: The token string.
        """
        return self.access_token


    def is_expired(self):
        """
        Check if the token is expired.

        :return: True if the token is expired, False otherwise.
        """
        return time.time() > self.expire_ts


    def need_refresh(self):
        return self.expire_ts - time.time() < self.refresh_threshold
