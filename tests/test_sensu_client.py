"""
Tests for the fawlty.sensu_client module
"""
import time
from unittest.mock import patch, MagicMock

import pytest
#with patch("fawlty.sensu_client.ValidationError", new_callable=MagicMock) as ValidationError:
#    from pydantic import ValidationError as RealValidationError

from fawlty.sensu_client import SensuClient, ValidationError
from fawlty.sensu_token import SensuToken
from fawlty.sensu_server import SensuServer

from fawlty.exceptions import (
    SensuConnectionError, SensuNeedRefresh,
    SensuAuthError, SensuNeedLogin,
    SensuResourceError, SensuError
)

@pytest.fixture
def sensu_client():
    client = SensuClient()
    client.token = SensuToken(access_token="token", refresh_token="refresh", expires_at=int(time.time()) + 100)
    client.server = SensuServer(host="localhost")
    return client

class TestCallFilter:

    def test_no_server(self):
        client = SensuClient()
        with pytest.raises(SensuConnectionError):
            client.call_filter()

    def test_no_token(self, sensu_client):
        sensu_client.token = None
        with pytest.raises(SensuNeedLogin):
            sensu_client.call_filter()

    def test_expired_token(self, sensu_client):
        sensu_client.token = MagicMock(is_expired=lambda: True)
        with pytest.raises(SensuNeedLogin):
            sensu_client.call_filter()

    def test_need_refresh(self, sensu_client):
        sensu_client.token = MagicMock(is_expired=lambda: False, need_refresh=lambda: True)
        with pytest.raises(SensuNeedRefresh):
            sensu_client.call_filter()


class TestMakeCall:

    @patch("fawlty.sensu_client.requests.Session.request")
    def test_make_call(self, mock_request, sensu_client):
        sensu_client.token = MagicMock(is_expired=lambda: False, need_refresh=lambda: False)
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {})
        response = sensu_client._make_call("GET", "/test")
        assert response.status_code == 200

    @patch("fawlty.sensu_client.requests.Session.request")
    def test_need_refresh(self, mock_request, sensu_client):
        sensu_client.token = MagicMock(is_expired=lambda: False, need_refresh=lambda: True)
        mock_request.return_value = MagicMock(status_code=401)
        sensu_client.refresh_token = MagicMock()

        # Make sure refresh_token is called
        sensu_client._make_call("GET", "/test")
        sensu_client.refresh_token.assert_called_once()


class TestLogin:

    @patch("fawlty.sensu_client.requests.Session.get")
    def test_success(self, mock_get, sensu_client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"access_token": "token", "refresh_token": "refresh", "expires_at": int(time.time()) + 100})
        assert sensu_client.login("user", "pass") is True
        assert sensu_client.token.access_token == "token"

    @patch("fawlty.sensu_client.requests.Session.get")
    def test_failure(self, mock_get, sensu_client):
        mock_get.return_value = MagicMock(status_code=401)
        with pytest.raises(SensuAuthError):
            sensu_client.login("user", "pass")


class TestRefreshToken:

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_success(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=200, json=lambda: {"access_token": "new_token", "refresh_token": "new_refresh", "expires_at": int(time.time()) + 100})
        sensu_client.token = SensuToken(access_token="token", refresh_token="refresh", expires_at=int(time.time()))
        assert sensu_client.refresh_token() is True
        assert sensu_client.token.access_token == "new_token"

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_failure(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=401, text="Unauthorized")
        sensu_client.token = SensuToken(access_token="token", refresh_token="refresh", expires_at=int(time.time()))
        with pytest.raises(SensuAuthError):
            sensu_client.refresh_token()


class TestResourceGet:

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_success(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=200, json=lambda: [{}])
        resources = sensu_client.resource_get(MagicMock, "/test")
        assert len(resources) == 1

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_failure(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=404, text="Not Found")
        with pytest.raises(SensuError):
            sensu_client.resource_get(MagicMock, "/test")


class TestResourcePost:

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_success(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=201)
        obj = MagicMock()
        obj.model_validate = MagicMock()
        obj.model_dump = MagicMock(return_value={})
        assert sensu_client.resource_post(obj) is True

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_validation_error(self, mock_make_call, sensu_client):
        obj = MagicMock()
        obj.model_validate = MagicMock(side_effect=ValidationError.from_exception_data("Invalid data", line_errors=[]))
        with pytest.raises(SensuResourceError):
            sensu_client.resource_post(obj)


class TestResourcePut:

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_success(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=200)
        obj = MagicMock()
        obj.model_validate = MagicMock()
        obj.model_dump = MagicMock(return_value={})
        assert sensu_client.resource_put(obj) is True

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_validation_error(self, mock_make_call, sensu_client):
        obj = MagicMock()
        obj.model_validate = MagicMock(side_effect=ValidationError.from_exception_data("Invalid data", line_errors=[]))
        with pytest.raises(SensuResourceError):
            sensu_client.resource_put(obj)


class TestResourceDelete:

    @patch("fawlty.sensu_client.SensuClient._make_call")
    def test_success(self, mock_make_call, sensu_client):
        mock_make_call.return_value = MagicMock(status_code=204)
        obj = MagicMock()
        assert sensu_client.resource_delete(obj) is True