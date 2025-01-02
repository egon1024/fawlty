"""
Test cases for the Silence resource.
"""

# Built in imports

# 3rd party imports
import pytest

# Our imports
from fawlty.resources.base import ResourceBase, MetadataWithNamespace
from fawlty.resources.silence import Silence, SilenceMetadata
from fawlty.sensu_client import SensuClient

@pytest.fixture
def silence_metadata():
    return SilenceMetadata(name="test_silence", namespace="default")

@pytest.fixture
def silence(silence_metadata):
    return Silence(
        check="check_name",
        subscription="subscription_name",
        begin=1234567890,
        expire=1234567890,
        expire_at=1234567890,
        expire_on_resolve=True,
        creator="test_user",
        reason="test_reason",
        metadata=silence_metadata
    )

class TestSilenceMetadata:
    def test_silence_metadata(self, silence_metadata):
        assert silence_metadata.name == "test_silence"
        assert silence_metadata.namespace == "default"
        assert isinstance(silence_metadata, MetadataWithNamespace)

class TestSilenceInitialization:
    def test_silence_initialization(self, silence):
        assert silence.check == "check_name"
        assert silence.subscription == "subscription_name"
        assert silence.begin == 1234567890
        assert silence.expire == 1234567890
        assert silence.expire_at == 1234567890
        assert silence.expire_on_resolve is True
        assert silence.creator == "test_user"
        assert silence.reason == "test_reason"
        assert silence.metadata.name == "test_silence"
        assert silence.metadata.namespace == "default"
        assert silence._sensu_client is None
        assert isinstance(silence, ResourceBase)

    def test_silence_check_fields(self, silence):
        silence.check = None
        silence.subscription = None
        with pytest.raises(ValueError):
            silence.check_fields()

class TestSilenceMethods:
    def test_silence_get_url(self):
        url = Silence.get_url(namespace="default")
        assert url == "/api/core/v2/namespaces/default/silenced"

    def test_silence_urlify(self, silence):
        url = silence.urlify()
        assert url == "/api/core/v2/namespaces/default/silenced/test_silence"

    def test_silence_urlify_create(self, silence):
        url = silence.urlify(purpose="create")
        assert url == "/api/core/v2/namespaces/default/silenced"

class TestResourceBaseMethods:
    def test_set_client(self, silence):
        client = SensuClient()
        silence.set_client(client)
        assert silence._sensu_client == client