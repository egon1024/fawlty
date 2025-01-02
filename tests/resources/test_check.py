"""
Test the check resource
"""
import pytest
from pydantic import ValidationError

from fawlty.sensu_client import SensuClient
from fawlty.resources.check import Check, CheckMetadata, CheckMetricThreshold, CheckProxyRequests

@pytest.fixture
def check_metadata():
    return CheckMetadata(name="test", namespace="default")

@pytest.fixture
def check(check_metadata):
    return Check(command="echo test", subscriptions=["test"], metadata=check_metadata)

class TestCheckMetricThresholdValidation:
    def test_invalid_status(self):
        with pytest.raises(ValidationError):
            CheckMetricThreshold(status=1)

    def test_valid_threshold(self):
        threshold = CheckMetricThreshold(status=1, max="100")
        assert threshold.max == "100"
        assert threshold.min is None

class TestCheckProxyRequestsValidation:
    def test_invalid_splay(self):
        with pytest.raises(ValidationError):
            CheckProxyRequests(splay=True)

    def test_valid_proxy_request(self):
        proxy_request = CheckProxyRequests(splay=True, splay_coverage=50)
        assert proxy_request.splay is True
        assert proxy_request.splay_coverage == 50

class TestCheckProxyEntityNameValidation:
    def test_invalid_proxy_entity_name(self):
        with pytest.raises(ValidationError):
            Check(proxy_entity_name="invalid name", command="echo test", subscriptions=["test"], metadata=CheckMetadata(name="test", namespace="default"))

    def test_valid_proxy_entity_name(self):
        check = Check(proxy_entity_name="valid-name", command="echo test", subscriptions=["test"], metadata=CheckMetadata(name="test", namespace="default"))
        assert check.proxy_entity_name == "valid-name"

class TestCheckSubscriptionsValidation:
    def test_invalid_subscriptions(self):
        with pytest.raises(ValidationError):
            Check(command="echo test", subscriptions=[], metadata=CheckMetadata(name="test", namespace="default"))

    def test_valid_subscriptions(self):
        check = Check(command="echo test", subscriptions=["test"], metadata=CheckMetadata(name="test", namespace="default"))
        assert check.subscriptions == ["test"]

class TestCheckMethods:
    def test_get_url(self):
        url = Check.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/checks"

    def test_urlify_non_create(self, check):
        url = check.urlify()
        assert url == "/api/core/v2/namespaces/default/checks/test"

    def test_urlify_create(self, check):
        url = check.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/checks"

class TestResourceBaseMethods:
    def test_set_client(self, check):
        client = SensuClient()
        check.set_client(client)
        assert check._sensu_client == client

