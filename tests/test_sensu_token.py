"""
Tests for fawlty.sensu_token module
"""

import time
from fawlty.sensu_token import SensuToken


class TestSensuToken:
    """
    Test cases for SensuToken class
    """
    def test_is_expired(self):
        """
        Test cases for is_expired method
        """
        # Token that is already expired
        expired_token = SensuToken(access_token="expired", expires_at=int(time.time()) - 10, refresh_token="refresh")
        assert expired_token.is_expired() is True

        # Token that is not expired
        valid_token = SensuToken(access_token="valid", expires_at=int(time.time()) + 100, refresh_token="refresh")
        assert valid_token.is_expired() is False

    def test_need_refresh(self):
        """
        Test cases for need_refresh method
        """
        # Token that needs refresh
        token_needs_refresh = SensuToken(access_token="needs_refresh", expires_at=int(time.time()) + 30, refresh_token="refresh")
        assert token_needs_refresh.need_refresh() is True

        # Token that does not need refresh
        token_no_refresh = SensuToken(access_token="no_refresh", expires_at=int(time.time()) + 100, refresh_token="refresh")
        assert token_no_refresh.need_refresh() is False