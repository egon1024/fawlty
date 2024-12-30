"""
A class to encapsulte a Sensu API token.
"""

# Built in imports
import time

# 3rd party imports
from pydantic import BaseModel

# Constants
DEFAULT_THRESHOLD = 60


class SensuToken(BaseModel):
    """
    A class to encapsulte a Sensu API token.
    """
    access_token: str
    expires_at: int
    refresh_token: str
    _refresh_threshold: int = DEFAULT_THRESHOLD

    def is_expired(self) -> bool:
        """
        Check if the sensu token is expired.

        :return: True if the sensu token is expired, False otherwise.
        """
        return time.time() > self.expires_at

    def need_refresh(self) -> bool:
        """
        Check if the sensu token needs to be refreshed.

        :return: True if the sensu token needs to be refreshed, False otherwise.
        """
        return self.expires_at - time.time() < self._refresh_threshold
